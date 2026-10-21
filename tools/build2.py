import glob, json, os, re

S = os.path.dirname(os.path.abspath(__file__))
miss = json.load(open(S + "/miss.json", encoding="utf-8"))
final = json.load(open(S + "/final.json", encoding="utf-8"))
tr = {}
for f in sorted(glob.glob(S + "/tr2/m*.txt")):
    for ln in open(f, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if ln:
            i, _, t = ln.partition("|")
            tr[int(i)] = t

# season-medal patterns (S1..S19)
RULES = [
    (r"^购买S(\d+)赛季限定礼包解锁的勋章$", "Medal unlocked by buying the S{0} Season Limited Gift Pack"),
    (r"^S(\d+)赛季皇城竞技场5000荣誉兑换解锁的勋章$", "Medal unlocked by exchanging 5,000 Honor in the S{0} Season Imperial City Arena"),
    (r"^购买S(\d+)赛季通行证并且完成S\d+赛季通行证任务解锁的勋章$", "Medal unlocked by buying the S{0} Season Pass and completing its quests"),
    (r"^S(\d+)赛季战令勋章$", "S{0} Season Battle Pass Medal"),
    (r"^S(\d+)赛季荣誉勋章$", "S{0} Season Honor Medal"),
    (r"^S(\d+)赛季限定勋章$", "S{0} Season Limited Medal"),
    (r"^S(\d+)赛季幸运宝箱奖励$", "S{0} Season Lucky Chest Reward"),
]
added = 0
left = []
for i, z in enumerate(miss):
    if i in tr:
        final[z] = tr[i]
        added += 1
        continue
    for pat, out in RULES:
        m = re.match(pat, z)
        if m:
            final[z] = out.format(*m.groups())
            added += 1
            break
    else:
        left.append(i)
han = re.compile("[㐀-鿿]")
bad = [i for i in tr if han.search(tr[i])]
tagbad = [i for i in tr if re.findall(r"<[^>]*>", miss[i]) != re.findall(r"<[^>]*>", tr[i])]
json.dump(final, open(S + "/final.json", "w", encoding="utf-8"), ensure_ascii=False)
print("added", added, "left", len(left), "han-in-output", bad[:10], "tag mismatch", tagbad[:10])
# left items are name/phrase lists; list their size
print([ (i, miss[i][:20]) for i in left][:30])

REGEX = r'''sr:"^第(?<n_i>[0-9]+)天\s*(?<rest>[\s\S]*)$"="Day ${n_i} ${rest}"
r:"^第([0-9]+)天$"=Day $1
r:"^([0-9]+)天$"=$1 Days
r:"^([0-9]+)级$"=Level $1
r:"^([0-9]+)星$"=$1 Stars
r:"^([0-9]+)次$"=$1 times
r:"^([0-9]+)元$"=$1 Yuan
r:"^([0-9]+)层$"=Floor $1
r:"^([0-9]+)倍$"=$1x
r:"^([0-9]+)分钟$"=$1 min
r:"^第([0-9]+)名$"=No. $1
r:"^第([0-9]+)局$"=Round $1
r:"^([0-9]+)小时$"=$1 hours
'''
open(S + "/regex.txt", "w", encoding="utf-8").write(REGEX)
