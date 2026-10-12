# Titan GT r1 — LOD repair revision: QA report

**Status: VALIDATED and FROZEN — corrected revision of Titan GT, preferred Unity import candidate** (2026-10-08).
- The original release `vehicles/C_TitanGT/` is kept frozen and byte-identical; it was only read.
- Approved by the project owner as "Titan GT — approve revision r1".

## 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/TG_validation.txt`) | **18 checks: 0 errors, 0 warnings** |
| FBX clean re-import | 2 of 2 files pass, 36 and 102 objects. Bounds deviate by 3.0e-7 m and pivots by 1.8e-7 m. Checked in raw Unity space: nose +Z, up +Y, FL on −X |
| Protected files | **PASS**: 1,554 baseline files, frozen Zero Gap R (70), the original Titan GT release (81) and Vortex R (109). All are byte-identical, and nothing was added outside `vehicles/` |
| Scope check | All 102 objects were diffed between the original and r1 export-ready files. **Only 5 meshes differ**, all of them intended (section 3). Every other object is identical in geometry, normals, materials, transform and parent: all of LOD0, glass, lights, interior, wheels, steering wheel, colliders, wheel refs, CenterOfMass and the LOD roots |

## 2. Defect and cause

- **Defect:** LOD1 showed jagged, chrome-like tears along every panel gap (hood, doors, deck lid, rocker). LOD2 and LOD3 had dark sliver shards on the hood and deck.
  - Evidence: `previews/lod_compare/TGorig_*`, and the odd rows of `previews/TG_r1_lod_compare_original_vs_repaired.jpg`.
- **Cause:** the reduced LODs were decimated from the LOD0 body with its 4.5 mm panel-gap grooves.
  - Collapse decimation folds each groove into slivers.
  - At LOD1, the normals transferred from LOD0 then smear across the folded faces.
- **Why validation missed it:** no check renders the reduced LODs close-up.

## 3. What changed (r1)

| Object | Change |
|---|---|
| `Body_LOD1`, `Body_LOD2`, `Body_LOD3` | Rebuilt using the Vortex R method (details below) |
| `Trim_LOD3` | Its four wheel-arch liners had collapsed to 12-triangle chords that sliced through the front and rear fenders (the dark slash on LOD3). The liners are taken from the clean `Trim_LOD2`; every other LOD3 trim part is unchanged. +60 triangles, given back by `Body_LOD3`, so the LOD3 total stays at the original count |
| `Trim_LOD1` | **Normals only:** own smooth normals with 38° hard edges, the same treatment as LOD2/3, instead of normals transferred from LOD0. This removes the chrome blotches on the rocker strip. Geometry unchanged |

How `Body_LOD1–3` were rebuilt:
- Titan's own frozen build code was re-run in memory with only the three panel-gap groove cutters disabled. All openings, pockets, arches, handles and vents stay.
- That groove-free body was collapse-decimated to the original per-LOD body triangle counts.
- Skin faces take the smooth normal of the high-resolution reference (KD-tree, 8 nearest normals); opening walls stay flat-shaded.
- 4 sliver faces lying flat on the paint skin were set back to paint (2 at LOD2, 2 at LOD3).

## 4. Numbers

| | Original | r1 | Target |
|---|---|---|---|
| LOD0 | 77,370 | **77,370 (identical)** | 60–90k |
| LOD1 | 39,752 (51 %) | **39,752 (51 %)** | 40–50 % |
| LOD2 | 18,527 (24 %) | **18,527 (24 %)** | 15–25 % |
| LOD3 | 7,731 (10 %) | **7,729 (10 %)** | 5–10 % |

Silhouette IoU against LOD0 (side / front / top). The silhouette is preserved: every value is within 0.001 of the original.

| LOD | Original | r1 |
|---|---|---|
| LOD1 | 0.9998 / 1.0 / 1.0 | 0.9999 / 1.0 / 0.9999 |
| LOD2 | 0.999 / 0.999 / 0.9997 | 0.9991 / 0.999 / 0.9996 |
| LOD3 | 0.9956 / 0.9984 / 0.9991 | 0.9963 / 0.9987 / 0.9994 |

- Maximum LOD dimension drift is 1.8 mm.
- The LOD1 budget of 51 % is unchanged from the approved original (validator band 38–52 %).

## 5. Comparisons (identical camera rig)

- **`previews/TG_r1_lod_compare_original_vs_repaired.jpg`.** Rows: original LOD1, r1 LOD1, original LOD2, r1 LOD2, original LOD3, r1 LOD3. Columns: front ¾, rear ¾, side, hood close-up, chase on the frozen P0 road.
- **`previews/lod_compare/`:** the 30 individual renders behind the sheet.
- **`previews/TG_*.png`:** the full 14-render review set of r1, which is identical to the original at LOD0, plus `TG_lod_lineup.png`.

## 6. Known limitations (unchanged from the original release)

- **LOD3 trim simplification:** at 6 % of LOD0, the rear diffuser fins and exhaust tips show faceted shards, and the rocker strip fades. This is visible only in close-ups well inside LOD3's switch distance; it was the same in the original release and was not changed.
- **Doors:** shut lines are modelled only at LOD0. LOD1–3 are groove-free by design; at those distances the gaps are sub-pixel. Doors don't open.
- **Polish items:** TG-PB-1 (mild rear-deck reflection waviness) and TG-PB-2 (slight hood-centre dip) are LOD0 items, so they are unchanged.
- **Testing:** no Unity runtime or performance testing was done; Unity is not installed.

## 7. Unity

- **Use `C_TitanGT_r1/UnityTransfer/`.**
- FBX file names are unchanged (`TitanGT_complete_unity.fbx`, `TitanGT_LOD0_unity_test.fbx`), so r1 drops in as a replacement for the original.
- Object names, hierarchy, pivots, colliders, materials and textures are identical to the original. Textures are byte-identical copies.
- Import notes: `UnityTransfer/README/TG_UNITY_IMPORT_NOTES.md`.

## 8. Files

| Path | Contents |
|---|---|
| `blend/titangt_r1_08_colliders_hierarchy.blend` | The original checkpoint 08 with the 5 repaired meshes |
| `blend/titangt_r1_09_export_ready.blend` | Export-ready source |
| `exports/` | 2 FBX files |
| `textures/` | 8 PNGs, byte-identical to the original release |
| `previews/` | 14 review renders, the LOD comparison sheet plus 30 renders, a three-car comparison, and details |
| `reports/` | `TG_validation.txt`, `TG_geometry.json`, `TG_export_manifest.json`, `TG_r1_lod_rebuild_log.json`, `TG_source_integrity_check.md`, `TG_FREEZE_CANDIDATE.md`, `TG_R1_FINAL_FREEZE.md`, this report |
| `scripts/` | `tg_r1_lods.py` (the repair), plus r1 copies of `tg_lib` / `tg_export` / `tg_render` / `tg_validate` / `tg_package`, each re-pointed to `C_TitanGT_r1` (a header line in each states this) |
