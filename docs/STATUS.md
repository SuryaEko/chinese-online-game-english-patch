# Status (as of the last commit)

## Done
* Runtime installed (BepInEx 6 pre.2 + XUnity 5.6.3.1), no online translator.
* ~7,800 pre-translated strings + 24 regex rules; font resizer 0.6 on ~46 UI roots.
* 61 textures replaced (see [TEXTURES.md](TEXTURES.md)).
* Public repo with install script, texture patch/restore, tools and these docs.
* Verified in game: title menu, announcement, leaderboard, home screen ("Day 4 Dusk", "Wednesday (Workday)"),
  calendar countdown, personal belongings panel (partly).

## Known gaps / next steps
1. **Videos 0-49** have burned-in Chinese subtitles (82 `.webm` total, 1.35 GB; 800+ are cartoon cutscenes without subs).
   Plan: get ffmpeg (ask user), read cues by sampling frames, build SRT per video, hard-sub English over a box,
   write the new webm back into the game (VideoClip data lives in `resources.assets.resS`; size must fit or the
   clip must be re-pointed - untested). Alternative: a BepInEx plugin that overlays timed English subtitles
   (needs a C# toolchain; dotnet SDK not installed).
2. 130 inline textures and the painted posters (see TEXTURES.md "Not done").
3. Screens not yet checked in game: Game Save list, phone shop, store packs, arena, guild, fishing/lottery modes.
   Strings seen in the user's screenshots (e.g. "钻石x300", "存档2", "71,203.77元", "目标:赚30万", skill tooltip
   "奥术炸弹Lv.2 / 冷却时间:5秒") now have regex rules but were not re-checked visually.
4. Player nickname pools and some dynamic strings may still be Chinese. Ask for a screenshot, then add a pair or a
   regex rule (see [TRANSLATION-FORMAT.md](TRANSLATION-FORMAT.md)).
5. `N万` with 3+ digits renders as `N0,000` without thousands separators.

## How the user reports problems
Screenshots with "beberapa text masih berbahasa china" (user writes Indonesian). Handle each visible Chinese string:
exists-in-cache? (grep the file) -> no: translate or add regex -> rebuild (`build3.py`) -> install -> screenshot.
Reply in Indonesian, short, outcome first.
