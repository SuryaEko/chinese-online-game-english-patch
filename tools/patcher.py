"""Overwrite Texture2D pixel data inside the game's .resS files, keeping a byte-exact backup of every region touched."""
import io, json, os, sys
from PIL import Image

S = r"C:\Users\PF1AZ\AppData\Local\Temp\claude\C--Users-PF1AZ--claude-spares-spare-LE37js\daaec113-244e-4034-bf51-f048fdfb14d7\scratchpad"
DATA = r"D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator\MMOSimulator_Data"
BACKUP = r"D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator\_texture_backup"
IDX = {i["pid"]: i for i in json.load(open(S + r"\texindex.json"))}

DDS_FMT = {12: "DXT5", 10: "DXT1"}


def _dds_payload(img, fmt):
    buf = io.BytesIO()
    img.save(buf, format="DDS", pixel_format=fmt)
    d = buf.getvalue()
    # 128-byte header, plus 20-byte DX10 header only when FourCC == 'DX10'
    off = 148 if d[84:88] == b"DX10" else 128
    return d[off:]


def encode(img, info):
    """Encode RGBA PIL image into the texture's exact on-disk byte layout (incl. mip chain)."""
    fmt, w, h, mips = info["fmt"], info["w"], info["h"], max(1, info["mip"])
    img = img.convert("RGBA")
    if img.size != (w, h):
        img = img.resize((w, h), Image.LANCZOS)
    out = bytearray()
    cur = img
    for m in range(mips):
        mw, mh = max(1, w >> m), max(1, h >> m)
        lvl = img.resize((mw, mh), Image.LANCZOS) if m else cur
        flipped = lvl.transpose(Image.FLIP_TOP_BOTTOM)  # Unity stores rows bottom-up
        if fmt == 4:
            out += flipped.tobytes("raw", "RGBA")
        elif fmt == 3:
            out += flipped.convert("RGB").tobytes("raw", "RGB")
        elif fmt in DDS_FMT:
            if mw % 4 or mh % 4:
                raise ValueError("block formats need size%4==0 at every mip")
            out += _dds_payload(flipped, DDS_FMT[fmt])
        else:
            raise ValueError(f"unsupported texture format {fmt}")
    return bytes(out)


def patch(pid, img):
    info = IDX[pid]
    if not info["path"]:
        raise ValueError("inline texture (not in .resS)")
    data = encode(img, info)
    if len(data) != info["ssize"]:
        raise ValueError(f"size mismatch {len(data)} != {info['ssize']} (fmt {info['fmt']})")
    target = os.path.join(DATA, info["path"])
    os.makedirs(BACKUP, exist_ok=True)
    bk = os.path.join(BACKUP, f"{info['pid']}.orig")
    with open(target, "r+b") as f:
        f.seek(info["off"])
        if not os.path.exists(bk):  # keep the FIRST original only
            orig = f.read(info["ssize"])
            open(bk, "wb").write(orig)
            f.seek(info["off"])
        f.write(data)
    meta = os.path.join(BACKUP, "index.json")
    m = json.load(open(meta)) if os.path.exists(meta) else {}
    m[str(pid)] = {"file": info["path"], "off": info["off"], "size": info["ssize"], "name": info["name"]}
    json.dump(m, open(meta, "w"), ensure_ascii=False, indent=1)


def restore_all():
    meta = os.path.join(BACKUP, "index.json")
    m = json.load(open(meta))
    for pid, e in m.items():
        with open(os.path.join(DATA, e["file"]), "r+b") as f:
            f.seek(e["off"])
            f.write(open(os.path.join(BACKUP, f"{pid}.orig"), "rb").read())
    print("restored", len(m))


if __name__ == "__main__":
    if sys.argv[1:] == ["restore"]:
        restore_all()
