import sys, pickle, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from glyphs import *

plan = pickle.load(open(os.path.join(HERE, sys.argv[1]), "rb"))
ok = 0
for ci, img in plan:
    for pid in pids_of(ci):
        try:
            patch(pid, img)
            ok += 1
        except Exception as e:
            print("FAIL", ci, pid, e)
print("patched", ok)
