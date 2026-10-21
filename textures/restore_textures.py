"""Restore every texture changed by the English image patch.
Close the game first, then run:  python restore_textures.py
(Steam > Properties > Installed Files > Verify integrity also restores the originals.)
This file is copied into <game>/_texture_backup by patch_textures.py and works from there."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "MMOSimulator_Data")
idx = json.load(open(os.path.join(HERE, "index.json"), encoding="utf-8"))
for pid, e in idx.items():
    with open(os.path.join(DATA, e["file"]), "r+b") as f:
        f.seek(e["off"])
        f.write(open(os.path.join(HERE, f"{pid}.orig"), "rb").read())
print("restored", len(idx), "textures")
