import os, re, json, glob, sys

S = os.path.dirname(os.path.abspath(__file__))
han = re.compile("[㐀-鿿]")
cache = json.load(open(S + "/final.json", encoding="utf-8"))
known = {k.strip() for k in cache}
found = {}
for f in glob.glob(S + "/txt/**/*", recursive=True):
    if not os.path.isfile(f):
        continue
    t = open(f, "rb").read().decode("utf-8", "replace").lstrip("﻿")
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    parts = re.findall(r">([^<>]+)<", t) + re.findall(r'="([^"]*)"', t)
    if not parts:  # not xml: take lines
        parts = t.splitlines()
    for p in parts:
        for q in re.split(r"[\r\n]+", p):
            q = q.strip()
            if han.search(q) and q not in known:
                found.setdefault(q, os.path.basename(f))
miss = sorted(found, key=lambda s: (len(s), s))
json.dump(miss, open(S + "/miss.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(miss), sum(map(len, miss)))
print(miss[:15])
