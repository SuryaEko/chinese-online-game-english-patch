"""Find length-prefixed strings with CJK that are longer than the old 4096 limit (and not XML) in resources.assets."""
import json, os, re, struct, sys

S = os.path.dirname(os.path.abspath(__file__))
D = r"D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator\MMOSimulator_Data"
b = open(os.path.join(D, "resources.assets"), "rb").read()
cjk = re.compile(rb"(?:[\xe3-\xe9][\x80-\xbf]{2}){3,}")
han = re.compile("[\u3400-\u9fff]")
final = json.load(open(S + "/final.json", encoding="utf-8"))
known = {k.strip() for k in final}
seen = {}
last_end = -1
for m in cjk.finditer(b):
    s, e = m.span()
    if s < last_end:
        continue
    for p in range(s - 4, max(0, s - 60000), -1):
        L = struct.unpack_from("<I", b, p)[0]
        if 4096 < L < 300000 and p + 4 <= s and p + 4 + L >= e:
            try:
                t = b[p + 4:p + 4 + L].decode("utf-8")
            except UnicodeDecodeError:
                continue
            if han.search(t) and "\x00" not in t:
                seen[t] = p
                last_end = p + 4 + L
            break
out = {}
for t, p in seen.items():
    q = t.lstrip("\ufeff").strip()
    if q.startswith("<?xml") or q in known:
        continue
    out[q] = p
print(len(seen), "long strings,", len(out), "not xml and not in cache")
for q, p in out.items():
    print(p, len(q), repr(q[:60]))
json.dump(list(out), open(S + "/long_miss.json", "w", encoding="utf-8"), ensure_ascii=False)
