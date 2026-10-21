import os, re, json, glob, collections
import xml.etree.ElementTree as ET

S = os.path.dirname(os.path.abspath(__file__))
han = re.compile("[㐀-鿿]")
cache = json.load(open(S + "/final.json", encoding="utf-8"))
known = {k.strip() for k in cache}
SKIP = ("Chinese", "LineBreaking", "SensitiveWords")
found = {}
per = collections.Counter()


def add(s, src):
    for q in re.split(r"[\r\n]+", s or ""):
        q = q.strip()
        if q and han.search(q) and q not in known and q not in found:
            found[q] = src
            per[src] += 1


for f in sorted(glob.glob(S + "/txt/*.txt")):
    name = re.sub(r" @\d+\.txt$", "", os.path.basename(f))
    if name.startswith(SKIP):
        continue
    raw = open(f, "rb").read().decode("utf-8", "replace").lstrip("﻿")
    try:
        root = ET.fromstring(raw.encode("utf-8"))
    except ET.ParseError as e:
        print("parse fail", name, e)
        continue
    for el in root.iter():
        add(el.text, name)
        add(el.tail, name)
        for v in el.attrib.values():
            add(v, name)
miss = sorted(found, key=lambda s: (len(s), s))
json.dump(miss, open(S + "/miss.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(found, open(S + "/miss_src.json", "w", encoding="utf-8"), ensure_ascii=False)
print(len(miss), sum(map(len, miss)))
print(per.most_common(60))
