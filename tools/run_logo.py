import sys
sys.path.insert(0, r"C:\Users\PF1AZ\AppData\Local\Temp\claude\C--Users-PF1AZ--claude-spares-spare-LE37js\daaec113-244e-4034-bf51-f048fdfb14d7\scratchpad")
from patcher import *
from imgtool import grad_text_layer, load

pid = 1831
o = load("Logo - 副本")
# the game only draws the opaque area of the original art: x 89-941, y 124-255
img = grad_text_layer(o.size, ["CHINESE-STYLE ONLINE GAME"], font_key="impact",
                      box=(89, 120, 941, 259))
patch(pid, img)
bg = Image.new("RGBA", img.size, (30, 50, 90, 255)); bg.alpha_composite(img); bg.convert("RGB").save(S + r"\logo_preview.png")
print("patched", IDX[pid]["name"])
