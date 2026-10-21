import sys, os, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signs import *

items, plan = [], []


def add(ci, n, lab):
    items.append((f"{ci} {lab}", img_of(ci), n))
    plan.append((ci, n))


# ---- 1522: scratch-card rules text on dark red -------------------------------------------------------
im = img_of(1522)
a = np.array(im)
lum = a[..., :3].astype(int).sum(axis=-1) / 3
mask = (np.abs(a[..., :3].astype(int) - np.array([104, 32, 31])).sum(axis=-1) > 110)
m = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.MaxFilter(7))
bgc = tuple(int(v) for v in np.median(a[..., :3][~mask], axis=0))
tcol = tuple(int(v) for v in np.median(a[..., :3][mask], axis=0))
out = im.copy()
out.paste(Image.new("RGBA", im.size, bgc + (255,)), (0, 0), m)
d = ImageDraw.Draw(out)
text = ("Scratch off the coating. If the Fortune symbol appears, you win the prize shown below the symbol. "
        "If the Get Rich symbol appears, you win 5x the prize shown below it. If the Get Rich Big symbol "
        "appears, you win 10x the prize shown below it. Winnings stack.")
f = ImageFont.truetype(FONT["bold"], 36)
W = im.size[0] - 60
lines, cur = [], ""
for w in text.split():
    t = (cur + " " + w).strip()
    if d.textbbox((0, 0), t, font=f)[2] <= W:
        cur = t
    else:
        lines.append(cur); cur = w
lines.append(cur)
y = 110
for ln in lines:
    d.text((30, y), ln, font=f, fill=tcol + (255,))
    y += 52
add(1522, out, "rules")

sheet(items, os.path.join(HERE, "prev_batch4.png"), T=300)
pickle.dump(plan, open(os.path.join(HERE, "plan4.pkl"), "wb"))
print(len(plan), bgc, tcol, len(lines))
