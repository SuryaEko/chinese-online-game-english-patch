# tools (development only)

Scripts used to build the patch. They are not needed to install it. Paths are hard-coded to the author's machine and
scratchpad (`S = ...scratchpad`); edit the constants at the top before reuse. See `../docs/` for the workflow.

* `extract.py`, `missing.py`, `missing2.py` - find Chinese strings (metadata, TextAssets via XML parser)
* `build.py`, `build2.py`, `build3.py`, `emit.py` - merge translations, rules, write the cache file
* `tr2/`, `regex.txt` - translation sources and regex rules
* `imgtool.py`, `glyphs.py`, `signs.py`, `batch1-4.py`, `run_logo.py` - make the English images
* `patcher.py`, `apply.py`, `stage.py`, `roundtrip.py`, `view.py`, `drop.py` - patch, stage the repo, verify
* `data/` - texture metadata exported with AssetStudio (`texindex.json`, candidate index and path-ID map)
