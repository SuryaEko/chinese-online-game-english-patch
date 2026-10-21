import sys, os, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signs import *

plan = pickle.load(open(os.path.join(HERE, "plan2.pkl"), "rb"))
keep = {3468, 1778, 1809, 977, 982, 900, 1681, 998, 606, 497, 670, 868}
plan = [(ci, n) for ci, n in plan if ci in keep]


def fb(ci, f):
    W, H = img_of(ci).size
    return (int(f[0] * W), int(f[1] * H), int(f[2] * W), int(f[3] * H))


FIX = [
    (624, ["No Smoking"], dict(box=(0, 0, 0, 0), frac=(0.42, 0.05, 0.97, 0.95))),
    (2027, ["Foot Massage"], dict(frac=(0.1, 0.0, 0.9, 0.17))),
    (1139, ["EXIT"], dict(frac=(0.2, 0.1, 0.82, 0.3))),
    (886, ["EXIT"], dict(frac=(0.2, 0.1, 0.82, 0.3))),
    (449, ["Fishing Garden"], dict(frac=(0.08, 0.0, 0.95, 0.17))),
]
items = []
for ci, lines, kw in FIX:
    kw = dict(kw)
    frac = kw.pop("frac")
    kw["box"] = fb(ci, frac)
    n = relabel(ci, lines, **kw)
    items.append((f"{ci} {lines[0]}", img_of(ci), n))
    plan.append((ci, n))
sheet(items, os.path.join(HERE, "prev_batch2b.png"), T=240)
pickle.dump(plan, open(os.path.join(HERE, "plan2.pkl"), "wb"))
print(len(plan), "total in plan2")
