import sys, os, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from signs import *

# (candidate index, lines, kwargs)
SIGNS = [
    (3468, ["Domestic Online Game"], {}),
    (1778, ["Dynamic Internet Cafe"], {}),
    (1809, ["Jiayuan Fortune Market"], {}),
    (2027, ["Foot Massage"], {"box": None}),
    (977, ["Foot Massage"], {}),
    (982, ["Convenience Store"], {}),
    (900, ["Clinic"], {}),
    (1681, ["Clinic"], {}),
    (1139, ["EXIT"], {}),
    (868, ["EXIT"], {}),
    (886, ["EXIT"], {}),
    (998, ["Parcel Station"], {}),
    (606, ["Luxury Goods Sale"], {}),
    (497, ["Supermarket Entrance"], {}),
    (449, ["Fishing Garden"], {}),
    (670, ["Fishing Garden"], {}),
    (624, ["No Smoking"], {}),
    (889, ["Adi WANG Apparel"], {}),
    (910, ["Candy Snow Milk Tea"], {}),
    (1583, ["Lottery"], {}),
]
items, plan = [], []
for ci, lines, kw in SIGNS:
    try:
        o = img_of(ci)
        n = relabel(ci, lines, **kw)
        items.append((f"{ci} {' '.join(lines)}", o, n)); plan.append((ci, n))
    except Exception as e:
        print("skip", ci, e)
sheet(items, os.path.join(HERE, "prev_batch2.png"), T=220)
pickle.dump(plan, open(os.path.join(HERE, "plan2.pkl"), "wb"))
print(len(items))
