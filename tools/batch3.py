import sys, os, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signs import *

items, plan = [], []


def add(ci, n, lab):
    items.append((f"{ci} {lab}", img_of(ci), n))
    plan.append((ci, n))


# red envelope with voucher
n = relabel(3439, ["Newbie", "Exclusive"], box=(150, 395, 460, 505), hmax=0.98, wmax=0.98, big=True)
n = relabel(3439, ["¥"], box=(430, 155, 480, 205), base=n, font="bold")
add(3439, n, "voucher")
add(3440, img_of(3440), "same") if False else None
# red envelope "open" button
n = relabel(3441, ["Open"], box=(262, 232, 371, 340), font="black", hmax=0.5, wmax=0.98, bgcol=(255, 245, 100), big=True)
add(3441, n, "Open")
# phone-app icons
n = relabel(2928, ["Mobile", "Mall"], box=(5, 280, 260, 365), hmax=0.98, wmax=0.97, big=True); add(2928, n, "Mobile Mall")
n = relabel(3633, ["Online", "Loans"], box=(5, 280, 260, 365), hmax=0.98, wmax=0.97, big=True); add(3633, n, "Online Loans")
n = relabel(3513, ["XX Group"], box=(5, 205, 260, 255), wmax=0.97, big=True)
n = relabel(3513, ["Staff Assistant", "App"], box=(0, 275, 265, 345), base=n, hmax=0.98, wmax=0.98, big=True)
add(3513, n, "XX Group")
# glyph badges
n = word_on_transparent(2008, "Loan", key="black", pad=0.14, hmax=0.4);
base = img_of(2008); base.alpha_composite(n)  # placeholder, replaced below
n = relabel(2008, ["Loan"], box=(14, 14, 114, 114), font="black", hmax=0.55)
add(2008, n, "Loan")
n = relabel(1931, ["Pin"], box=(14, 14, 114, 114), font="black", hmax=0.55); add(1931, n, "Pin")
n = relabel(3499, ["Pin"], box=(0, 0, 265, 475), font="black", hmax=0.25); add(3499, n, "Pin")
# red-gold "get rich" banners
for ci, w in ((829, "Get Rich"), (1136, "Get Rich Big")):
    parts = w.split(" ", 1) if ci == 829 else ["Get Rich", "Big"]
    n = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    for k, t in enumerate(parts):
        layer = word_on_transparent(ci, t, key="black", outline=(255, 200, 60), fill=(235, 70, 40), pad=0.03, hmax=0.42)
        n.paste(layer, (0, int((k - 0.5) * 50)), layer)
    add(ci, n, w)
sheet(items, os.path.join(HERE, "prev_batch3.png"), T=230)
pickle.dump(plan, open(os.path.join(HERE, "plan3.pkl"), "wb"))
print(len(plan))
