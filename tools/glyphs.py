import sys, re, json, os
sys.path.insert(0, r"C:\Users\PF1AZ\AppData\Local\Temp\claude\C--Users-PF1AZ--claude-spares-spare-LE37js\daaec113-244e-4034-bf51-f048fdfb14d7\scratchpad")
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
from patcher import IDX, patch, S
SRC = S + "\\out\\Texture2D"

CAND = json.load(open(S + r"\cand.json"))
BYNAME = {}
for pid, i in IDX.items():
    BYNAME.setdefault(i["name"], []).append(pid)


PIDS = {int(k): v for k, v in json.load(open(S + "\cand_pids.json")).items()}


def pids_of(cidx):
    return PIDS[cidx]


def pid_of(cidx):
    return PIDS[cidx][0]


def img_of(cidx):
    return Image.open(os.path.join(SRC, CAND[cidx])).convert("RGBA")


FONT = {"black": r"C:\Windows\Fonts\ariblk.ttf", "bold": r"C:\Windows\Fonts\arialbd.ttf", "impact": r"C:\Windows\Fonts\impact.ttf"}


def fit_font(draw, text, maxw, maxh, key, start=300):
    fs = start
    while fs > 6:
        f = ImageFont.truetype(FONT[key], fs)
        l, t, r, b = draw.textbbox((0, 0), text, font=f)
        if r - l <= maxw and b - t <= maxh:
            return f, (l, t, r, b)
        fs -= 2
    f = ImageFont.truetype(FONT[key], 6)
    return f, draw.textbbox((0, 0), text, font=f)


def opaque_info(im):
    a = np.array(im)
    m = a[..., 3] > 40
    if not m.any():
        return None, (255, 255, 255)
    ys, xs = np.where(m)
    col = tuple(int(v) for v in np.median(a[m][:, :3], axis=0))
    return (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1), col


def word_on_transparent(cidx, word, key="black", outline=None, fill=None, pad=0.06, hmax=0.55):
    """Replace a glyph/label drawn on a transparent background with `word`, keeping its colour."""
    im = img_of(cidx)
    W, H = im.size
    bb, col = opaque_info(im)
    col = fill or col
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    bw = int(W * (1 - 2 * pad))
    f, (l, t, r, b) = fit_font(d, word, bw, int(H * hmax), key)
    x = (W - (r - l)) // 2 - l
    y = (H - (b - t)) // 2 - t
    if outline:
        d.text((x, y), word, font=f, fill=outline + (255,), stroke_width=max(1, f.size // 14), stroke_fill=outline + (255,))
    d.text((x, y), word, font=f, fill=col + (255,))
    return out


def sheet(items, path, T=160):
    """items: list of (label, original, replacement) -> side-by-side preview."""
    cols = 4
    rows = (len(items) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (T * 2 + 8), rows * (T + 16)), (70, 70, 80))
    dr = ImageDraw.Draw(sh)
    for i, (lab, o, n) in enumerate(items):
        x, y = (i % cols) * (T * 2 + 8), (i // cols) * (T + 16)
        for k, im in enumerate((o, n)):
            t = im.copy()
            t.thumbnail((T - 4, T - 4))
            bg = Image.new("RGBA", t.size, (110, 110, 125, 255))
            bg.alpha_composite(t)
            sh.paste(bg.convert("RGB"), (x + k * T + 2, y + 2))
        dr.text((x + 2, y + T), lab, fill=(255, 255, 0))
    sh.save(path)
