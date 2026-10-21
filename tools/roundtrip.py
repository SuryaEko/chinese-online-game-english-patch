import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = r"D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator"
REPO = os.path.join(HERE, "repo")
man = json.load(open(os.path.join(REPO, "textures", "manifest.json"), encoding="utf-8"))


def digest():
    out = {}
    for t in man["textures"]:
        with open(os.path.join(GAME, "MMOSimulator_Data", t["file"]), "rb") as f:
            f.seek(t["offset"])
            out[t["pid"]] = hashlib.sha1(f.read(t["size"])).hexdigest()
    return out


py = sys.executable
before = digest()
subprocess.run([py, os.path.join(GAME, "_texture_backup", "restore_textures.py")], check=True)
mid = digest()
print("changed by restore:", sum(before[k] != mid[k] for k in before), "of", len(before))
subprocess.run([py, os.path.join(REPO, "textures", "patch_textures.py"), GAME], check=True)
after = digest()
bad = [k for k in before if before[k] != after[k]]
print("ROUND TRIP", "OK - identical" if not bad else f"MISMATCH {bad[:10]}")
