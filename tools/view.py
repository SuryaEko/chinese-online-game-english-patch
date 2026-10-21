import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from glyphs import *

ids = [int(x) for x in sys.argv[2:]]
T = 300
cols = 4
rows = (len(ids) + cols - 1) // cols
sh = Image.new("RGB", (cols * T, rows * (T + 14)), (70, 70, 80))
dr = ImageDraw.Draw(sh)
for i, ci in enumerate(ids):
    im = img_of(ci)
    s = im.size
    im.thumbnail((T - 4, T - 4), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, (110, 110, 125, 255)); bg.alpha_composite(im)
    x, y = (i % cols) * T, (i // cols) * (T + 14)
    sh.paste(bg.convert("RGB"), (x + 2, y + 2))
    dr.text((x + 2, y + T), f"{ci} {s[0]}x{s[1]} fmt{IDX[pid_of(ci)]['fmt']}", fill=(255, 255, 0))
sh.save(os.path.join(HERE, sys.argv[1]))
