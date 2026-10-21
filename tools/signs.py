import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from glyphs import *
from collections import Counter


def dist(a, b):
    return np.abs(a.astype(int) - np.array(b, dtype=int)).sum(axis=-1)


def relabel(cidx, lines, box=None, font="black", textcol=None, bgcol=None, thr=70, hmax=0.8, wmax=0.92,
            outline=None, bold_stroke=0, base=None, big=False):
    """Erase the (CJK) text inside `box` (x0,y0,x1,y1 in px; default whole image) and write English `lines`.
    Works for text on a flat-colour plate: the plate colour is the most common colour in the box."""
    im = base if base is not None else img_of(cidx)
    W, H = im.size
    x0, y0, x1, y1 = box or (0, 0, W, H)
    a = np.array(im)
    reg = a[y0:y1, x0:x1]
    opaque = reg[..., 3] > 200
    flat = reg[..., :3].reshape(-1, 3)[opaque.reshape(-1)] // 8 * 8
    cnt = Counter(map(tuple, flat))
    bg = bgcol or tuple(int(v) for v in np.median(reg[..., :3].reshape(-1, 3)[opaque.reshape(-1)][
        dist(flat, cnt.most_common(1)[0][0]) < 24], axis=0))
    d = dist(reg[..., :3], bg)
    textmask = (d > thr) & opaque
    if textmask.any():
        # close the glyph strokes so the erase covers anti-aliasing
        tm = Image.fromarray((textmask * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5))
        ys, xs = np.where(np.array(tm) > 0)
        tb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
        col = textcol or tuple(int(v) for v in np.median(reg[..., :3][textmask], axis=0))
        # paint over text with plate colour
        fill = Image.new("RGBA", tm.size, bg + (255,))
        sub = Image.fromarray(reg.copy())
        sub.paste(fill, (0, 0), tm)
    else:
        tb = (0, 0, x1 - x0, y1 - y0)
        col = textcol or (255, 255, 255)
        sub = Image.fromarray(reg.copy())
    # fit the English text into the old text's bbox (at least 50% of the box)
    bw = max(int((x1 - x0) * 0.5), tb[2] - tb[0]) if textmask.any() else int((x1 - x0) * wmax)
    bw = min(bw, int((x1 - x0) * wmax))
    bh = max(int((y1 - y0) * 0.35), tb[3] - tb[1]) if textmask.any() else int((y1 - y0) * hmax)
    bh = min(bh, int((y1 - y0) * hmax))
    if big:
        bw, bh = int((x1 - x0) * wmax), int((y1 - y0) * hmax)
    d2 = ImageDraw.Draw(sub)
    n = len(lines)
    # shared font size: every line must fit
    fs = 200
    while fs > 6:
        f = ImageFont.truetype(FONT[font], fs)
        ws = [d2.textbbox((0, 0), t, font=f)[2] - d2.textbbox((0, 0), t, font=f)[0] for t in lines]
        lh = int(fs * 1.05)
        if max(ws) <= bw and lh * n <= bh:
            break
        fs -= 2
    f = ImageFont.truetype(FONT[font], fs)
    cx = (tb[0] + tb[2]) // 2 if textmask.any() else (x1 - x0) // 2
    cy = (tb[1] + tb[3]) // 2 if textmask.any() else (y1 - y0) // 2
    top = cy - (fs * 1.05 * n) / 2
    for i, t in enumerate(lines):
        bb = d2.textbbox((0, 0), t, font=f)
        x = cx - (bb[2] - bb[0]) / 2 - bb[0]
        y = top + i * fs * 1.05 - bb[1] + (fs * 1.05 - (bb[3] - bb[1])) / 2
        if outline:
            d2.text((x, y), t, font=f, fill=outline + (255,), stroke_width=max(1, fs // 12), stroke_fill=outline + (255,))
        d2.text((x, y), t, font=f, fill=col + (255,))
    out = im.copy()
    out.paste(sub, (x0, y0))
    return out
