# Pitfalls (each one cost time here)

## Tooling / environment
| Symptom | Cause | Fix |
|---|---|---|
| Bash tool: `unexpected EOF`, or backslashes vanish from Python/PowerShell code in a heredoc | The tool mangles `\` and some quotes in long heredocs | Create files with the **Write tool** (Windows path), run them with `python file.py`. For short fixes use Edit. |
| `FileNotFoundError ... scratchpadout...` | `\o` etc. eaten by the shell | Build paths with `os.path.join` / `"\\x"` inside files written by Write. |
| `pip install UnityPy` fails | Python 3.15, no C compiler | Skip UnityPy. Use AssetStudio CLI. |
| AssetStudio: `Unknown option [videoclip]` | wrong mode/name | `-m exportRaw -t video` |
| Python can't open `/c/Users/...` | Git Bash path passed to Windows Python | Use `C:/Users/...` in Python code and args. |
| Screenshot shows the Claude window | game not in front | `(New-Object -ComObject WScript.Shell).AppActivate(<pid>)` then wait 3 s |
| Data edit fails or game crashes | game still running | `taskkill //F //IM MMOSimulator.exe` first |
| Auto-mode classifier blocks overwriting game data | modifying game files needs explicit consent | Ask the user (AskUserQuestion), state backup + restore. Do not work around the block. |
| Edit/Write hook warns about `pickle` / `xml` | security plugin | Files are our own/local game data; fine. Prefer JSON when cheap. |

## XUnity.AutoTranslator
* **Texture replacement does not work** here: dumping creates nothing, replacement files are accepted
  (`Image not loaded (no hash)` disappears once named `name [HASH1-HASH2].png`) but nothing changes on screen,
  even with `EnableTextureScanOnSceneLoad=True`. Patch the `.resS` bytes instead ([TEXTURES.md](TEXTURES.md)).
* Cache key escaping: `\n`, `\r`, `\\`, and `=` as `\=`. Colour-tag keys contain `=` so this matters (verified).
* Empty `Endpoint=` -> no online translation, no "pending". Leave `FromLanguage=zh`.
* Resizer file name must end in `resizer.txt`. Path matching is **prefix** based (`/UI_Select(Clone)`),
  `/` alone or `(Clone)` alone match nothing. Add both `/Name` and `/Name(Clone)` for each UI root.
* Regex lines go in the same cache file: `r:"^...$"=replacement` (whole string) and
  `sr:"^(?<a>..)(?<b>..)$"="${a} ${b}"` (split, each group translated; a group named `x_i` is copied untouched).
  Replacement `${1}0,000` is needed when a digit follows a group (`$10` would mean group 10).
* A string that contains a number the cache does not know ("第4天 黄昏", "钻石x300") needs a regex rule.
* Warnings about `TMP_Text_SetCharArray_Hook3`, `WWW`, `AssetBundle` at start-up are harmless.

## Extraction
* Length-prefix scan of `.assets` with a 4 KB limit misses large XML tables. Always export TextAssets.
* `<![CDATA[<color=..>]]>` splits element text; the game sees the joined string (with tags). Use an XML parser.
* **Scene/prefab strings with several tags** (e.g. `<size=35>注意:</size>游戏支持<size=35>自动存档</size>...`) live in `resources.assets`
  as ordinary strings. A heuristic that treated any string with >3 tags as XML and split it into fragments lost the
  whole string. Keep full strings from the scan (`strings_zh.json`) and diff them against the cache (`build4.py`,
  `tr3/`). Check this class after every extraction.
* Some text assets are JSON, not XML (`BillingMode`, `HeroExp`, `TaskInfo`) and have no Chinese. Parse failures are OK.
* Strings **longer than 4096 bytes** were skipped by the first scan (e.g. the 1.7 KB-of-Chinese Version Update Notes, 4.3 KB in UTF-8).
  `tools/long.py` rescans for length-prefixed strings up to 300 KB (slow: ~5 min on 900 MB) and lists those not in the cache.
  Other long hits here were only a censor word list and font character lists.
* Garbage hits (random symbols, font files) appear in any raw scan. Drop them.
* Chat/nickname "pools" are one long comma-separated string; the game splits it. Translate the phrases, not the pool.

## Images
* Texture formats seen: 12=DXT5, 10=DXT1, 4=RGBA32, 3=RGB24 (+1,2,5,25,28,29 not handled). 130 textures are inline in
  `resources.assets` (no `.resS` range) and cannot be patched this way.
* Rows are stored bottom-up. Mip chains must be rebuilt (Pillow writes one level; encode each level).
* DXT needs width/height multiples of 4 at every mip level.
* A sprite may show only part of its texture. The logo texture was 1024x375 but only the opaque box
  (89,124)-(941,255) was drawn; text placed outside it was cut off. Measure the original alpha bbox first.
* Single-glyph tag icons: same colour, bold font, word centred. Multipliers "N倍" -> "Nx" with dark outline.
* Auto-erase (`signs.relabel`) works on flat plates only. For buildings/arches give an explicit `box` or skip.
* Poster art with painted titles and photos: do not attempt automatic edits.

## Process
* Do not announce a task finished until the screen was actually checked; say what was not checked.
* Mark the ~80 garbage/skip indices rather than inventing translations.

## Finding what the game really displays (recording mode)
Static extraction misses strings that are assembled at runtime (descriptions split by CDATA, chat history, numbers).
Record them instead:
1. `python tools/echo_srv.py` (echoes text back on 127.0.0.1:8799).
2. In `AutoTranslatorConfig.ini`: `Endpoint=CustomTranslate`, `[Custom] Url=http://127.0.0.1:8799`,
   `OutputFile=Translation/{Lang}/Text/_Observed.txt` (use forward slashes; do not edit with `sed` + backslashes).
3. Play to the screens in question (drive the UI with SetCursorPos/mouse_event, screenshot).
4. `python tools/obs.py` lists the recorded keys not in the cache. Translate them, or add regex rules.
5. Restore `Endpoint=` empty and the original `OutputFile`; delete `_Observed.txt`; stop the echo server.

## Chat / multi-line rich text
The chat is ONE text (all lines joined by `
`, each fragment wrapped in `<color=#..>`). Regex rules in `tools/regex.txt`:
split off a leading newline, split first line / rest, split first `<color>` segment / rest, translate each segment
alone (segments are plain-text keys derived by `build5.py`), keep the player-name segment untouched because it is not in
the cache. Needs `MaxTextParserRecursion=100`. In regex lines write `=` inside patterns as `=`, and never write
`
` through a shell heredoc (it becomes a real newline and breaks the rule).
