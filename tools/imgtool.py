import hashlib, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

S = r"C:\Users\PF1AZ\AppData\Local\Temp\claude\C--Users-PF1AZ--claude-spares-spare-LE37js\daaec113-244e-4034-bf51-f048fdfb14d7\scratchpad"
SRC = S + r"\out\Texture2D"
DST = r"D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator\BepInEx\Translation\en\Texture"
FONTS = {"black": r"C:\Windows\Fonts\ariblk.ttf", "bold": r"C:\Windows\Fonts\arialbd.ttf", "impact": r"C:\Windows\Fonts\impact.ttf"}


def h5(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10].upper()


def install(name, img, tag=None):
    """Save img as the replacement for the in-game texture called `name`."""
    os.makedirs(DST, exist_ok=True)
    fn = f"{tag or name} [{h5(name)}-0000000000].png"
    img.save(os.path.join(DST, fn))
    return fn


def load(name):
    return Image.open(os.path.join(SRC, name + ".png")).convert("RGBA")


def grad_text_layer(size, lines, font_key="black", top=(255, 205, 120), bot=(240, 130, 30),
                    outline=(70, 35, 10), shadow=(0, 0, 0, 160), box=None, line_gap=0.0):
    """Orange gradient text with dark outline + drop shadow, lines centred inside `box`."""
    W, H = size
    box = box or (0, 0, W, H)
    bx0, by0, bx1, by1 = box
    bw, bh = bx1 - bx0, by1 - by0
    # largest font size where every line fits the box
    fs = 400
    while fs > 8:
        f = ImageFont.truetype(FONTS[font_key], fs)
        ws = [f.getbbox(t)[2] - f.getbbox(t)[0] for t in lines]
        hs = [f.getbbox("Hg")[3] - f.getbbox("Hg")[1] for _ in lines]
        total_h = sum(hs) + int(fs * line_gap) * (len(lines) - 1)
        if max(ws) <= bw * 0.96 and total_h <= bh * 0.9:
            break
        fs -= 2
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    y = by0 + (bh - total_h) // 2
    for t, w, h in zip(lines, ws, hs):
        bb = f.getbbox(t)
        d.text((bx0 + (bw - w) // 2 - bb[0], y - f.getbbox("Hg")[1]), t, font=f, fill=255)
        y += h + int(fs * line_gap)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    # shadow
    sh = mask.filter(ImageFilter.GaussianBlur(3))
    sh_layer = Image.new("RGBA", size, shadow)
    sh_layer.putalpha(ImageChops.multiply(sh, Image.new("L", size, shadow[3])))
    out.alpha_composite(sh_layer, (4, 5))
    # outline
    ol = mask.filter(ImageFilter.MaxFilter(max(3, (fs // 14) | 1)))
    ol_layer = Image.new("RGBA", size, outline + (255,))
    ol_layer.putalpha(ol)
    out.alpha_composite(ol_layer)
    # gradient fill
    g = Image.new("RGBA", size)
    gd = ImageDraw.Draw(g)
    ys = [i for i in range(H) if mask.getbbox() and mask.getbbox()[1] <= i <= mask.getbbox()[3]]
    y0, y1 = (mask.getbbox()[1], mask.getbbox()[3]) if mask.getbbox() else (0, H)
    for yy in range(H):
        t = min(1, max(0, (yy - y0) / max(1, y1 - y0)))
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,)
        gd.line([(0, yy), (W, yy)], fill=c)
    g.putalpha(mask)
    out.alpha_composite(g)
    return out
