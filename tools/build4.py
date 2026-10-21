import glob, json, os, re

S = os.path.dirname(os.path.abspath(__file__))
miss = json.load(open(S + "/miss2.json", encoding="utf-8"))
final = json.load(open(S + "/final.json", encoding="utf-8"))
n = 0
bad = []
for f in sorted(glob.glob(S + "/tr3/n*.txt")):
    for ln in open(f, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln:
            continue
        i, _, t = ln.partition("|")
        z = miss[int(i)].strip()
        e = t.replace("<NL>", "\n").strip()
        if re.findall(r"<[^>]*>", z) != re.findall(r"<[^>]*>", e):
            bad.append(int(i))
        final[z] = e
        n += 1
json.dump(final, open(S + "/final.json", "w", encoding="utf-8"), ensure_ascii=False)
print("added", n, "tag mismatch", bad)
