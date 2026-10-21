import json, os

S = os.path.dirname(os.path.abspath(__file__))
final = json.load(open(S + "/final.json", encoding="utf-8"))
zh = open(S + "/notes_zh.txt", encoding="utf-8").read().replace("\r\n", "\n")
en = open(S + "/notes_en.txt", encoding="utf-8").read().replace("\r\n", "\n")
final[zh.strip()] = en.strip()
json.dump(final, open(S + "/final.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(final))
