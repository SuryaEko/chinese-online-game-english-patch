# Editing textures

Why: XUnity texture replacement does not work in this IL2CPP build, so pixels are overwritten directly in
`MMOSimulator_Data/resources.assets.resS` (and `sharedassets2.assets.resS`). Needs user consent (game data change).

## Facts
* Each Texture2D has `m_StreamData {path, offset, size}`, `m_TextureFormat`, `m_Width/Height`, `m_MipCount`.
  Get them from `AssetStudioModCLI -m dump -t tex2d` (JSON per texture). Stored in `textures/manifest.json`
  (fields: `pid`, `name`, `fmt`, `mips`, `w`, `h`, `file`, `offset`, `size`).
* Overwrite exactly `size` bytes at `offset`. Never change length.
* Formats handled by `patch_textures.py`: 4 RGBA32, 3 RGB24, 10 DXT1, 12 DXT5.
* Path ID = unique asset id. Edited PNGs are named `<pathID>.png`.
* Same image can exist under several path IDs; identical copies are all patched (`glyphs.pids_of`).

## Add or change an image (workflow)
1. Export everything: `-m export -t tex2d -g none -f assetName_pathID -o out2` (names `name @pid.png`).
2. Find candidates: contact sheets (numbered thumbnails) -> read them -> list Chinese-text images.
   Filter out 3D textures by name (`normal|albedo|wings|weapon|...`). ~3,700 candidates, ~10 per 126-tile sheet.
3. Make the replacement with the same size/alpha as the original:
   * `tools/imgtool.py grad_text_layer` gradient text with outline (logo style).
   * `tools/glyphs.py word_on_transparent` single word/glyph on transparent bg, colour sampled from the original.
   * `tools/signs.py relabel` erase text on a flat plate (box, `bgcol`, `big=True` to fill the box) and write English.
   * Preview side-by-side with `glyphs.sheet(...)` and **look at it** before applying.
4. Apply with `tools/apply.py plan.pkl` (maps candidate index -> path IDs by MD5, backs up originals, patches).
5. Re-export the patched texture with AssetStudio (`--filter-by-pathid`) and compare, then run the game.
6. For the repo: save the PNG as `textures/<pid>.png`, add the entry to `manifest.json`
   (`tools/stage.py` rebuilds both from the plans), run the round trip, commit.

## Done (61)
Logo `Logo - 副本` (pid 1831, drawn area x89-941,y124-255) -> "CHINESE-STYLE ONLINE GAME".
29 single-glyph badges, 6 "N倍" -> "Nx", 14 signs (Clinic, Foot Massage, Convenience Store, No Smoking, EXIT,
Supermarket Entrance, ...), 10 envelope/app/badge/banner images (Newbie Exclusive, Open, Mobile Mall, Online Loans,
XX Group, Loan, Pin, Get Rich, Get Rich Big).

## Not done
* 130 inline textures (e.g. poster 1522 rules text) - needs patching `resources.assets` itself (900 MB, higher risk).
* Scratch-card posters with painted titles, photos/screenshots with small text, signs that auto-edit badly
  (building exit signs 1139/886, park gate 449, 889/910/1583).
* Candidate sheets 19, 21, 22, 24, 25 were never reviewed.

## Backup / restore
`<game>/_texture_backup/<pid>.orig` + `index.json`; `restore_textures.py` writes them back.
Steam "Verify integrity" also restores. A Steam update may overwrite the data and undo the patch.
