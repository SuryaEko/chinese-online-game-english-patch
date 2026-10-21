import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
G = r"D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator\BepInEx\Translation\en\Text\_Observed.txt"
han = re.compile("[\u3400-\u9fff]")
final = json.load(open(S + "/final.json", encoding="utf-8"))
known = {k.strip() for k in final}


def split(line):
    k = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            n = line[i + 1]
            k.append({"n": "\n", "r": "\r"}.get(n, n))
            i += 2
            continue
        if c == "=":
            return "".join(k)
        k.append(c)
        i += 1
    return "".join(k)


# regex-handled patterns (keep in sync with tools/regex.txt) - skip these
SKIP = [r"^战斗力\+[0-9]+$", r"^充值[0-9]+元$", r"^账号累计充值[0-9]+元(解锁)?$", r"^累计充值达到[0-9]+元解锁$",
        r"^[Vv]ip[0-9]+特权内容$", r"^今日消费满[0-9]+元解锁购买$", r"^消费[0-9]+元福利礼包$", r"^关卡[0-9]+-[0-9]+$",
        r"^剩余[0-9]+天$", r"^累计签到:[0-9]+天$", r"^今日答题[0-9]+/[0-9]+$", r"^[0-9]+场$", r"^翅膀解锁[0-9]+/[0-9]+$"]
out = []
for ln in open(G, encoding="utf-8"):
    ln = ln.rstrip("\n").lstrip("\ufeff")
    k = split(ln).strip()
    if not han.search(k) or k in known or any(re.match(p, k) for p in SKIP):
        continue
    if k not in out:
        out.append(k)
json.dump(out, open(S + "/obs_miss.json", "w", encoding="utf-8"), ensure_ascii=False)
for i, k in enumerate(out):
    print(i, "|", k.replace("\n", "<NL>"))
