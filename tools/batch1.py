import sys
sys.path.insert(0, r"C:\Users\PF1AZ\AppData\Local\Temp\claude\C--Users-PF1AZ--claude-spares-spare-LE37js\daaec113-244e-4034-bf51-f048fdfb14d7\scratchpad")
from glyphs import *

# candidate-sheet index -> English word (single-glyph white tag icons)
GLYPH = {275: "Loan", 292: "Loan", 339: "Lucky", 375: "Safe", 447: "Surplus", 467: "Prosper", 521: "Fortune",
         567: "Brocade", 597: "Flourish", 638: "Peace", 667: "Virtue", 683: "Years", 848: "Longevity",
         883: "Thrive", 897: "Strong", 929: "Wisdom", 938: "Just", 952: "Resolve", 966: "Smooth", 985: "Wave",
         995: "Bright", 1010: "Gift", 1171: "Luck", 1180: "Joy", 1196: "Elite", 1337: "Harmony",
         1478: "Omen", 1652: "Auspice", 1746: "Health"}
MULT = {13: "1x", 715: "2x", 1153: "5x", 1360: "10x", 1542: "20x", 1676: "50x"}

items = []
plan = []
for ci, w in GLYPH.items():
    o = img_of(ci)
    n = word_on_transparent(ci, w, key="black")
    items.append((f"{ci} {w} fmt{IDX[pid_of(ci)]['fmt']}", o, n)); plan.append((ci, n))
for ci, w in MULT.items():
    o = img_of(ci)
    n = word_on_transparent(ci, w, key="black", outline=(40, 40, 40), hmax=0.8, pad=0.05)
    items.append((f"{ci} {w} fmt{IDX[pid_of(ci)]['fmt']}", o, n)); plan.append((ci, n))
sheet(items, S + r"\prev_batch1.png")
import pickle
pickle.dump([(ci, n) for ci, n in plan], open(S + r"\plan1.pkl", "wb"))
print(len(items), "previews")
