"""Apply the English texture patch to a local copy of the game.

    python patch_textures.py "D:\\SteamLibrary\\steamapps\\common\\MMOSimulator\\MMOSimulator"

Needs: Python 3 + Pillow (pip install pillow). Close the game first.
For every texture in manifest.json it encodes textures/<pathID>.png into the texture's exact on-disk
format and overwrites those bytes inside MMOSimulator_Data/*.resS. The original bytes are saved once to
<game>/_texture_backup so restore_textures.py can undo everything.
"""
import io
import json
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DDS = {12: "DXT5", 10: "DXT1"}


def encode(img, t):
    """RGBA PIL image -> bytes in the texture's own format, including its mip chain."""
    w, h, fmt, mips = t["w"], t["h"], t["fmt"], max(1, t["mips"])
    img = img.convert("RGBA")
    if img.size != (w, h):
        img = img.resize((w, h), Image.LANCZOS)
    out = bytearray()
    for m in range(mips):
        mw, mh = max(1, w >> m), max(1, h >> m)
        lvl = img.resize((mw, mh), Image.LANCZOS) if m else img
        flipped = lvl.transpose(Image.FLIP_TOP_BOTTOM)  # Unity stores rows bottom-up
        if fmt == 4:      # RGBA32
            out += flipped.tobytes("raw", "RGBA")
        elif fmt == 3:    # RGB24
            out += flipped.convert("RGB").tobytes("raw", "RGB")
        elif fmt in DDS:  # DXT1 / DXT5
            buf = io.BytesIO()
            flipped.save(buf, format="DDS", pixel_format=DDS[fmt])
            d = buf.getvalue()
            out += d[148 if d[84:88] == b"DX10" else 128:]
        else:
            raise ValueError(f"unsupported texture format {fmt}")
    return bytes(out)


def game_running():
    try:
        out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout
        return "MMOSimulator.exe" in out
    except OSError:
        return False


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    game = sys.argv[1]
    data = os.path.join(game, "MMOSimulator_Data")
    if not os.path.isdir(data):
        sys.exit(f"Not a game folder (no MMOSimulator_Data): {game}")
    if game_running():
        sys.exit("Close MMOSimulator first.")
    man = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
    for f, size in man["file_sizes"].items():
        p = os.path.join(data, f)
        if not os.path.exists(p) or os.path.getsize(p) != size:
            sys.exit(f"{f} does not match game build {man['game_build']} (size differs). Texture patch skipped.")
    backup = os.path.join(game, "_texture_backup")
    os.makedirs(backup, exist_ok=True)
    idx_path = os.path.join(backup, "index.json")
    idx = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else {}
    done = 0
    for t in man["textures"]:
        data_bytes = encode(Image.open(os.path.join(HERE, f"{t['pid']}.png")), t)
        if len(data_bytes) != t["size"]:
            sys.exit(f"texture {t['pid']} ({t['name']}): encoded {len(data_bytes)} bytes, expected {t['size']}")
        with open(os.path.join(data, t["file"]), "r+b") as fh:
            fh.seek(t["offset"])
            orig = os.path.join(backup, f"{t['pid']}.orig")
            if not os.path.exists(orig):  # keep only the very first (true original) bytes
                open(orig, "wb").write(fh.read(t["size"]))
                fh.seek(t["offset"])
            fh.write(data_bytes)
        idx[str(t["pid"])] = {"file": t["file"], "off": t["offset"], "size": t["size"], "name": t["name"]}
        done += 1
    json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(backup, "restore_textures.py"), "w", encoding="utf-8").write(
        open(os.path.join(HERE, "restore_textures.py"), encoding="utf-8").read())
    print(f"Patched {done} textures. Originals saved in {backup}")


if __name__ == "__main__":
    main()
