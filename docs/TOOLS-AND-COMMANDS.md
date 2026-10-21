# Tools and commands

Windows 11, Git Bash + PowerShell. Python 3.15 only (no compiler). Paths below use `$GAME` for
`D:\SteamLibrary\steamapps\common\MMOSimulator\MMOSimulator`.

## Runtime (text)
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1 -GamePath "$GAME"
```
Official sources used by `install.ps1`:
* https://github.com/BepInEx/BepInEx/releases/download/v6.0.0-pre.2/BepInEx-Unity.IL2CPP-win-x64-6.0.0-pre.2.zip (34 MB)
* https://github.com/bbepis/XUnity.AutoTranslator/releases/download/v5.6.3.1/XUnity.AutoTranslator-BepInEx-IL2CPP-5.6.3.1.zip (0.7 MB)

Installed layout: `BepInEx/`, `dotnet/`, `winhttp.dll`, `doorstop_config.ini`. Remove those to uninstall.
Log: `$GAME\BepInEx\LogOutput.log`. Config: `$GAME\BepInEx\config\AutoTranslatorConfig.ini`.

## Python environment
`UnityPy` does NOT install on Python 3.15 (needs to compile lz4/brotli). Do not waste time on it.
Pillow and numpy have wheels:
```bash
python -m venv venv
./venv/Scripts/python -m pip install --only-binary=:all: pillow numpy
```
Use `python -I` for scripts that read untrusted game data.

## AssetStudio CLI (extract assets)
Release: https://github.com/aelurum/AssetStudio/releases/tag/v0.19.0 -> `AssetStudioModCLI_net472_win32_64.zip`
(11 MB, runs on built-in .NET Framework, no dotnet install). Ask the user before downloading.
Run from **PowerShell** with Windows paths (Git Bash path conversion breaks arguments):
```powershell
$D = "$GAME\MMOSimulator_Data"
.\AssetStudioModCLI.exe $D -m export    -t tex2d     -g none -f assetName_pathID -o out2      # images, name "x @pathID.png"
.\AssetStudioModCLI.exe $D -m export    -t textasset -g none -f assetName_pathID -o txt       # XML tables
.\AssetStudioModCLI.exe $D -m exportRaw -t video     -g type -o vid                           # VideoClip -> *_data.dat (= webm)
.\AssetStudioModCLI.exe $D -m dump      -t tex2d     -o dump                                  # JSON per texture (format, mips, resS offset/size)
.\AssetStudioModCLI.exe $D -m info                                                           # counts per asset type
```
Notes: `-t videoClip` is rejected in `export` mode; use `exportRaw -t video`. `--filter-by-pathid N` exports one asset.
The `_#NNN` suffix in default file names is NOT the path ID and changes between runs. Always use `-f assetName_pathID`
and map old exports to path IDs by MD5 of the PNG bytes.

## Viewing results
* Screenshot of the game: PowerShell `Graphics.CopyFromScreen`, after `AppActivate`-ing the game window
  (otherwise you capture the Claude window). Then Read the PNG.
* Clicking in the game: `user32 SetCursorPos` + `mouse_event`. Screen is 1920x1080; main menu Start Game ~ (250,375).
* Contact sheets: draw numbered thumbnails with Pillow (`tools/` scripts) and Read them.
* Playing `.webm`: the in-app browser cannot open `file://` pages interactively; serve the folder with
  `python -I -m http.server 8765 --directory <dir>` and navigate to `http://127.0.0.1:8765/...`. Stop the server after.

## Texture patch
```bash
python textures/patch_textures.py "$GAME"     # needs Pillow, game closed
python "$GAME/_texture_backup/restore_textures.py"
```
Round-trip test used before pushing: `roundtrip.py` (hash 61 ranges, restore, patch, compare).

## Game control
```bash
(start "" MMOSimulator.exe || cmd //c start "" MMOSimulator.exe)   # launch
taskkill //F //IM MMOSimulator.exe                                   # close (required before editing data)
```

## Git / GitHub
`gh` is logged in as SuryaEko. Repo: `SuryaEko/chinese-online-game-english-patch` (public).
`gh repo create ... --public --source . --push`; later changes: commit + `git push origin main`.
`.gitattributes`: `translation/* -text` keeps LF in the translation files.
