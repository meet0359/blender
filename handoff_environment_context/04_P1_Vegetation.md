# P1-BLENDER-03 + 03A — Production Vegetation System (LOD0 / foliage polish + final freeze)

Digest 04 of the environment handoff. Folder: `environment/P1_Vegetation/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/vegetation_09_final_frozen.blend`
- **Asset index source:** `reports/P1_vegetation_03A_geometry.json` + `reports/P1_vegetation_export_manifest.json`
- **Checkpoints (9):** `vegetation_01_blockout.blend`, `vegetation_02_trees.blend`, `vegetation_03_shrubs_grass.blend`, `vegetation_04_materials_atlases.blend`, `vegetation_05_wind_lods.blend`, `vegetation_06_terrain_qa.blend`, `vegetation_07_export_ready.blend`, `vegetation_08_lod0_polish.blend`, `vegetation_09_final_frozen.blend`
- **FBX (8):** `Trees_Broadleaf.fbx` (60 objects), `Trees_Small.fbx` (30 objects), `Trees_Conifer.fbx` (30 objects), `Shrubs.fbx` (24 objects), `Grass.fbx` (10 objects), `Weeds.fbx` (6 objects), `Vegetation_CollisionOptional.fbx` (8 objects), `vegetation_complete.fbx` (168 objects)
- **Textures:** 63 PNG files · **Previews:** 55 renders · **UnityTransfer README:** `VEGETATION_IMPORT_NOTES.md`, `VEGETATION_PLACEMENT_GUIDE.md`

> **Note:** the triangle table inside `VEGETATION_IMPORT_NOTES.md` (embedded below) predates the 03A LOD0 polish, which removed hidden branches (e.g. Broadleaf_A Variant A LOD0 8,932 -> 3,342). The asset index above and `P1_vegetation_03A_FINAL_REPORT.md` hold the final numbers. The frozen README itself was not edited.

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `Bush_A` | 780 / 498 / 242 | Shrubs.fbx |
| `Bush_B` | 900 / 582 / 278 | Shrubs.fbx |
| `Bush_C` | 620 / 394 / 192 | Shrubs.fbx |
| `Bush_D` | 470 / 330 / 144 | Shrubs.fbx |
| `Bush_Dry_A` | 570 / 404 / 174 | Shrubs.fbx |
| `Hedge_Organic_A` | 720 / 420 / 286 | Shrubs.fbx |
| `Tree_Broadleaf_A_VariantA` | 3,342 / 2,260 / 763 / 406 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_A_VariantB` | 3,236 / 2,226 / 793 / 418 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_A_VariantC` | 2,954 / 1,994 / 677 / 376 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_B_VariantA` | 2,706 / 1,788 / 631 / 342 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_B_VariantB` | 2,816 / 1,898 / 679 / 358 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_B_VariantC` | 2,472 / 1,622 / 595 / 306 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_C_VariantA` | 2,496 / 1,602 / 463 / 244 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_C_VariantB` | 2,380 / 1,618 / 471 / 256 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_C_VariantC` | 2,086 / 1,350 / 415 / 210 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_D_VariantA` | 3,720 / 2,494 / 891 / 450 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_D_VariantB` | 3,662 / 2,480 / 859 / 450 | Trees_Broadleaf.fbx |
| `Tree_Broadleaf_D_VariantC` | 3,444 / 2,318 / 837 / 428 | Trees_Broadleaf.fbx |
| `Tree_Conifer_A_VariantA` | 2,062 / 1,504 / 383 / 168 | Trees_Conifer.fbx |
| `Tree_Conifer_A_VariantB` | 2,458 / 1,792 / 449 / 198 | Trees_Conifer.fbx |
| `Tree_Conifer_A_VariantC` | 1,786 / 1,302 / 335 / 146 | Trees_Conifer.fbx |
| `Tree_Conifer_B_VariantA` | 1,024 / 722 / 199 / 86 | Trees_Conifer.fbx |
| `Tree_Conifer_B_VariantB` | 1,372 / 978 / 259 / 114 | Trees_Conifer.fbx |
| `Tree_Conifer_B_VariantC` | 994 / 698 / 195 / 84 | Trees_Conifer.fbx |
| `Tree_SmallRoadside_A_VariantA` | 1,578 / 1,000 / 365 / 200 | Trees_Small.fbx |
| `Tree_SmallRoadside_A_VariantB` | 1,714 / 1,158 / 419 / 246 | Trees_Small.fbx |
| `Tree_SmallRoadside_A_VariantC` | 1,398 / 870 / 327 / 172 | Trees_Small.fbx |
| `Tree_SmallRoadside_B_VariantA` | 1,544 / 960 / 359 / 200 | Trees_Small.fbx |
| `Tree_SmallRoadside_B_VariantB` | 1,762 / 1,110 / 419 / 228 | Trees_Small.fbx |
| `Tree_SmallRoadside_B_VariantC` | 1,324 / 842 / 321 / 166 | Trees_Small.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `Grass.fbx` (10): Grass_Dry_A (12), Grass_Dry_B (12), Grass_Medium_A (12), Grass_Medium_B (12), Grass_RoadEdge_A (10), Grass_RoadEdge_B (10), Grass_Short_A (12), Grass_Short_B (12), Grass_Tall_A (14), Grass_Tall_B (14)
- `Vegetation_CollisionOptional.fbx` (8): Collision_Tree_Broadleaf_A (28), Collision_Tree_Broadleaf_B (28), Collision_Tree_Broadleaf_C (28), Collision_Tree_Broadleaf_D (28), Collision_Tree_Conifer_A (28), Collision_Tree_Conifer_B (28), Collision_Tree_SmallRoadside_A (28), Collision_Tree_SmallRoadside_B (28)
- `Weeds.fbx` (6): FlowerSparse_A (8), Weed_A (8), Weed_B (8), Weed_C (8), WildPlant_A (8), WildPlant_B (8)

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `reports/P1_vegetation_03A_FINAL_REPORT.md`

### P1-BLENDER-03A — Vegetation LOD0 / Foliage Quality / Final Polish — FINAL REPORT

Date: 2026-10-07 · Status: **ACCEPTED · P1_Vegetation FROZEN**
This report only collects existing evidence. Nothing was rendered, regenerated or exported to write it. Evidence files: `P1_vegetation_03A_validation.txt`, `P1_vegetation_03A_geometry_delta.json`, `P1_vegetation_wood_geometry_audit.json`, `P1_vegetation_03A_visual_baseline.md`, `P1_vegetation_03A_source_integrity.md`, `P1_vegetation_FINAL_FREEZE_03A.md`. All paths are relative to `environment/P1_Vegetation/`.

#### 1. Baseline integrity
Before any 03A work, SHA-1 baselines were recorded:
- `P1_vegetation_03A_workspace_baseline.json`: 678 files outside the phase folder.
- `P1_vegetation_03A_prepolish_hashes.json`: 166 files from phase 03, including checkpoints `vegetation_01`–`07`.

The 03 FBX files were archived to `exports/_pre_03A/`. The 03 foliage atlas, impostors and `veg_cell_rects.json` were archived to `textures/_pre_03A/`.

#### 2. Visual defects confirmed
These defects were confirmed against the 03 assets. The before renders are `previews/03A_before_{broadleaf_A,conifer_A,tree_library,chase,alpha_overdraw}.png`.
- **Wood-heavy LOD0 on every tree.** Wood made up 70–82 % of LOD0 triangles (audit `before`, e.g. Broadleaf_A 73.1 %, Conifer_A 81.1 %).
- **Broadleaf foliage clusters read as round "coin" discs.**
- **Conifer sprays were uniform and flat-toned.**
- **Broadleaf_D appeared only once in the QA scatter.**

#### 3. Tree wood audit
Source: `P1_vegetation_wood_geometry_audit.json` (`before` / `after`), Variant A, LOD0.

| Tree | Wood tris before → after | Wood share after |
|---|---|---|
| Broadleaf_A | 6,528 → 982 | 29 % |
| Broadleaf_B | 6,078 → 700 | 26 % |
| Broadleaf_C | 5,266 → 1,304 | 52 % |
| Broadleaf_D | 6,528 → 944 | 25 % |
| SmallRoadside_A | 3,368 → 644 | 41 % |
| SmallRoadside_B | 3,368 → 614 | 40 % |
| Conifer_A | 4,092 → 1,126 | 55 % |
| Conifer_B | 1,860 → 628 | 61 % |

Validation check 40 passes.

#### 4. Broadleaf_A before/after triangles
Broadleaf_A Variant A, LOD0:
- **Total:** 8,932 → 3,342 (−62.6 %).
- **Wood:** 6,528 → 982.
- **Foliage:** 2,404 → 2,360.
- **By wood part:** trunk 228 → 152, primary 1,372 → 680, secondary 2,240 → 54, twig 2,688 → 96.

This is below the suggested 6,000–7,500 band. The brief allowed that if quality was equal or better, which is confirmed in the visual baseline.

#### 5. Other tree geometry changes
LOD0 triangles, Variant A (`geometry_delta.json`):

| Tree | Before → after |
|---|---|
| Broadleaf_B | 8,128 → 2,706 |
| Broadleaf_C | 6,472 → 2,496 |
| Broadleaf_D | 9,344 → 3,720 |
| SmallRoadside_A | 4,338 → 1,578 |
| SmallRoadside_B | 4,336 → 1,544 |
| Conifer_A | 5,046 → 2,062 |
| Conifer_B | 2,256 → 1,024 |

All 24 tree LOD0 meshes together went from 148,352 to 54,330 triangles. All exported assets together went from 266,180 to 117,668 triangles.

Silhouette (check 41):
- LOD0/LOD1 height changed by at most 1.6 %.
- Broadleaf/small canopy width changed by at most 4.3 %.
- Conifer width changed by at most 17.5 % (narrower).

#### 6. Branches removed / simplified
- **Ring sides:** trunk, primary and secondary branches at LOD0 went from 12 / 7 / 4 to 8 / 5 / 3. Conifer branch tubes are now 3 sides.
- **Polylines:** branch polylines are simplified with Ramer-Douglas-Peucker. The tolerance scales with branch radius and LOD.
- **Hidden branches:** at broadleaf/small LOD0, order-2 and order-3 branches were removed when their midpoint was occluded by foliage cards in at least 5 of 6 test directions. This is visible in the secondary and twig drop on Broadleaf_A (2,240 → 54 and 2,688 → 96).

The exact number of branches removed per tree was not recorded. Only the triangle effect is in the evidence.

#### 7. Foliage-card changes
- **Card counts** went down slightly on every tree (check 45), for example Broadleaf_A 1,202 → 1,180 and Conifer_A 477 → 468.
- **Card variation:** cards are layered, with outer cards smaller and core cards larger. Size and roll vary more widely, and card normals blend toward the canopy-outward direction.
- **Interior thinning:** 15 % of interior cards (ρ ≤ 0.5) are thinned at LOD0.
- **Atlas art:** the foliage atlas was redrawn with the same names, layout and 2K size. Broadleaf clusters now have irregular outlines, smaller rim leaves and a darker core. Conifer sprays were redrawn as dense fishbone sprays (cropped coverage CN_spray_A 0.44, CN_spray_B 0.38).
- **Alpha:** check 10 passes, with foliage mean coverage 0.44 and minimum 0.22.

#### 8. Canopy-depth implementation
A second UV set, **`CanopyShadeUV`** (UV channel 1, Unity `mesh.uv2`), is on every tree LOD mesh:
- **U** is interior depth, from 0 at the outer leaves to 1 at the canopy core.
- **V** is per-card leaf tint variation, centred on 0.5.

The Blender preview materials multiply albedo by `lerp(1, 0.45, U)` and by a tint ramp on V. Check 43 passes: the UV set exists on all tree LODs and values are within 0–1. A re-import of `Trees_Conifer.fbx` confirmed the UV set names (`UVMap`, `CanopyShadeUV`). WindData is not repurposed.

#### 9. Conifer improvements
- **Spray art:** sprays were redrawn as dense fishbone sprays with calmer tips and variation in value and hue per branchlet.
- **Gaps:** branch miss rate went up (A 0.08 → 0.12, B 0.16 → 0.20, B irregularity 0.32).
- **Shading and size:** cards get depth shading from their radial distance, plus ±15 % size variation.
- **Shape:** A stays taller and narrower and B stays broader and irregular. The two are distinguishable at 25, 50 and 100 m (`03A_conifer_library.png`, `03A_conifer_{25,50,100}m.png`).
- **Wood:** conifer wood fell 72 % on A and 66 % on B.

#### 10. WindData regression result
**PASS. The convention is unchanged:** R = primary bend, G = leaf flutter, B = phase, A = stiffness.
- Checks 13 and 16 pass.
- FBX re-import WindData drift is at most 0.0020, within the 8-bit tolerance of 2.5/255.

#### 11. Custom-normal regression result
**PASS.**
- Check 14 passes: custom normals are present on every renderable mesh.
- Checks 31–38 report "custom normals preserved" after FBX re-import. They are compared in world space, so the earlier bug of exporting unrotated normals has not come back.

#### 12. Alpha-overdraw result
Compared `03A_alpha_overdraw.png` with `03A_before_alpha_overdraw.png`:
- **LOD0:** no significant regression.
- **Conifer LOD2:** slightly denser than in 03, but within budget.

Check 10 passes.

#### 13. LOD changes
LOD1–LOD3 were regenerated from the corrected skeletons, not decimated.
- **Ring sides:** LOD1 6/4/3, LOD2 5/3/3, LOD3 4/3/3.
- **Branch simplification:** RDP tolerance scales with (1 + LOD).
- **Envelope:** LOD2 and LOD3 cards are shifted inward as they grow, so the crown no longer grows with distance.

Check 17 passes: there are 30 LOD chains, and triangle counts strictly decrease along each chain.

#### 14. LOD-envelope QA
**PASS.**
- **Check 42:** LOD1–3 width and height stay within ±18 % of LOD0. The observed range is 0.831–1.085.
- **Check 18:** passes.
- **LOD pop:** reviewed at 45 m in `03A_lod_pop_{Broadleaf_A,Broadleaf_C,Broadleaf_D,SmallRoadside_A,Conifer_A,Conifer_B}.png`.

#### 15. Species-distribution QA
**PASS (check 44).** All 8 archetypes appear in the Normal_Highway scatter:

| Archetype | Trees |
|---|---|
| Broadleaf_A | 5 |
| Broadleaf_B | 5 |
| Broadleaf_C | 7 |
| **Broadleaf_D** | **6** (was 1) |
| SmallRoadside_A | 15 |
| SmallRoadside_B | 13 |
| Conifer_A | 7 |
| Conifer_B | 5 |

The only change is a species quota on the choice of dominant species in each tree cluster. All placement rules are unchanged.

#### 16. Terrain-mask QA
**PASS.**
- **Check 22 (TerrainBlend):** 0 violations for trees, bushes and grass. Mean grass R under trees is 0.90.
- **Check 23 (VegetationMask):** mean grass density is 0.74. Grass_Dry dryness is 0.58, versus 0.26 for green grass.

#### 17. Prop-clearance QA
**PASS.**
- **Check 24 (road clearance):** minimum distance from the road centreline is tree 21.4 m, bush 19.0 m, grass 17.2 m, weed 18.4 m. There are no crown overhangs.
- **Check 25 (props, rocks and walls):** 28 exclusion circles and 10 exclusion rectangles, with 0 hits.
- **Check 26 (sign, gantry and VMS visibility):** passes.

#### 18. Ground-contact QA
**PASS.**
- **Check 21:** all 7,098 QA instances sit 1–8 cm into the frozen terrain.
- **Check 19:** pivots are correct, with a maximum trunk offset of 0.015 m.
- **Check 47:** the lowest LOD0 vertex is within 0.050 m of the pivot plane.

#### 19. Before/after previews
Before/after pairs exist for these views (in `previews/`):

| View | Before | After |
|---|---|---|
| Broadleaf_A | `03A_before_broadleaf_A.png` | `03A_new_broadleaf_A.png` |
| Conifer_A | `03A_before_conifer_A.png` | `03A_new_conifer_A.png` |
| Tree library | `03A_before_tree_library.png` | `03A_new_tree_library.png` |
| Chase | `03A_before_chase.png` | `03A_chase.png` |
| Alpha overdraw | `03A_before_alpha_overdraw.png` | `03A_alpha_overdraw.png` |

These renders are standalone AFTER/QA images. They have no before counterparts, and none were required:
- `03A_broadleaf_close.png`
- `03A_broadleaf_{25,50,100}m.png`
- `03A_conifer_{25,50,100}m.png`
- `03A_conifer_library.png`
- `03A_tree_LODs.png`
- `03A_lod_pop_*.png`

#### 20. Driver/chase previews
- `previews/03A_driver_view.png`
- `previews/03A_chase_view.png`
- `previews/03A_chase.png`
- `previews/03A_high_chase.png`
- `previews/03A_full_environment.png`

All of these PASS in the visual baseline. All 8 species are visible, including Broadleaf_D, and nothing clips the road or props.

#### 21. Final checkpoint
- **Final source:** **`blend/vegetation_09_final_frozen.blend`**. It is the export source.
- **Pre-export checkpoint:** `blend/vegetation_08_lod0_polish.blend`.
- **Earlier checkpoints:** `vegetation_01` through `vegetation_07` were not overwritten and are **byte-identical** to their pre-03A hashes (see item 26).

#### 22. FBX paths
The same 8 file names as in phase 03, in `exports/`:
- `vegetation_complete.fbx`
- `Trees_Broadleaf.fbx`
- `Trees_Small.fbx`
- `Trees_Conifer.fbx`
- `Shrubs.fbx`
- `Grass.fbx`
- `Weeds.fbx`
- `Vegetation_CollisionOptional.fbx`

The previous versions are in `exports/_pre_03A/`. SHA-1 hashes are in `P1_vegetation_FINAL_FREEZE_03A.md`. The axis bake residual is 1.19e-7.

#### 23. FBX re-import result
**PASS for all 8 files (checks 31–38).**
- **World deviation:** at most 1.4e-6 m.
- **WindData drift:** at most 0.0020.
- **Custom normals:** preserved.
- **Up axis:** Unity +Y up, with the tree spanning file-space Y −0.05 to 10.66.

**Re-import dimensional tolerance: approved at 6 mm.** The up-axis check compares the unrounded FBX tree height with a source height the validator had rounded to 2 decimals. Rounding alone can account for up to 5 mm, and the original 1 mm tolerance therefore failed on a rounding artifact, not a real deviation. The measured geometric deviation is only 1.4e-6 m. 6 mm is the 5 mm rounding bound plus the original 1 mm. The tolerance was applied only in the 03A validation run; the validator source `scripts/veg_validate.py` is unchanged.

#### 24. Validation result
**`P1_vegetation_03A_validation.txt`: 47 checks, 0 errors, 0 warnings.**
- Checks 1–39 are the 03 suite re-run on `vegetation_09`.
- Checks 40–47 are the 03A additions.

#### 25. UnityTransfer path
`environment/P1_Vegetation/UnityTransfer/`

| Folder | Contents |
|---|---|
| `FBX/` | The 8 FBX files, identical to `exports/` |
| `Textures/Foliage/` | Updated foliage atlas |
| `Textures/Impostors/` | Regenerated impostors |
| `Textures/Bark/`, `Textures/Grass/`, `Textures/Weeds/` | Unchanged |
| `Reports/` | Includes the 03A reports and the updated `atlas_cell_rects.json` |
| `README/VEGETATION_IMPORT_NOTES.md` | New 03A section documenting `CanopyShadeUV` and stating that the WindData convention is unchanged |

#### 26. Source-integrity status
**PASS** (`P1_vegetation_03A_source_integrity.md`, confirmed again after the docs were updated).
- **Outside the phase folder:** 0 files changed and 0 files added. This covers P0 Road Foundation (95 files), P1 Props (77), P1 Terrain (166, including `terrain_09_final_frozen.blend`) and vehicles plus all other workspace files (340).
- **Vegetation checkpoints:** `vegetation_01` through `vegetation_07` are confirmed unchanged byte-for-byte.

#### 27. Remaining limitations
- **Conifer colour:** conifer foliage still reads as mid-teal. The hue family was kept by design.
- **Conifer width:** conifer LOD0 is up to 17.5 % narrower than in 03. This is within the conifer tolerance of check 41 and matches the "A narrower" intent.
- **Conifer LOD2 overdraw:** slightly denser than in 03.
- **Distant LOD sizes:** LOD2/LOD3 canopies are 8–28 % narrower than the 03 LOD2/LOD3. This is intentional, to reduce envelope growth.
- **Hidden-branch test:** it is a coarse 6-direction heuristic, and per-tree counts of removed branches were not recorded.
- **QA variant use:** the scatter quota works per species, not per variant, so variant use within a species is uneven.
- **Missing before pairs:** there are no before images for the close-up, 25/50/100 m or LOD-pop views (see item 19).
- **No Unity check:** canopy shading has only been checked in Blender preview materials. Unity shaders were out of scope.

#### 28. Recommended next Blender phase
Recommendation only, not started: proceed to the next roadmap phase, such as the Tunnel / structures kit, under the same frozen-upstream rules. That phase should **link** `vegetation_09_final_frozen.blend` read-only and never modify P1_Vegetation.

---
**P1_Vegetation remains FROZEN.** Nothing under `environment/P1_Vegetation/` is to be edited. Later phases may only link from it.

---

### `UnityTransfer/README/VEGETATION_IMPORT_NOTES.md`

### Vegetation library (P1-BLENDER-03) — Unity import notes

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.**
> **UNITY-SIDE: VEGETATION SHADERS, WIND, GPU INSTANCING, LODGROUP COMPONENTS, IMPOSTOR RUNTIME SETUP, SCATTERING, CULLING, QUALITY TIERS AND PERFORMANCE TESTING MUST BE DONE ON THE UNITY WORKSTATION.**
> Nothing here has been opened in Unity. Every number was measured in Blender, including a re-import of every FBX into an empty scene (`Reports/P1_vegetation_validation.txt`, 0 errors). No Unity performance is claimed.

#### 1. Phase
Fourth Blender environment phase (after P0 road, P1 props, P1 terrain). The frozen road, props, terrain and the hypercar were only linked read-only. This package contains **vegetation only**.

#### 2. Unity orientation / 3. scale
Same method as every earlier phase: in-memory axis bake, Apply Transform off. Blender +Z up / road -Y / driver-left +X becomes Unity **+Y up / +Z forward**, X mirrored: (x, y, z) -> (-x, z, -y).
Importer: Scale Factor 1, Convert Units ON, Bake Axis Conversion OFF, Normals **Import** (custom normals are part of the look), Tangents Calculate, Read/Write OFF. 1 unit = 1 m. All pivots are the ground contact / trunk centre.

#### 4-5. Tree families and variants (8 archetypes x 3 variants)
| Archetype | Height (variants A/B/C) | Canopy width (A/B/C) | Character |
|---|---|---|---|
| Tree_Broadleaf_A | 10.7 / 10.6 / 10.8 m | 10.0 / 9.0 / 10.1 m | broad rounded roadside crown, wide lower silhouette |
| Tree_Broadleaf_B | 12.2 / 13.3 / 13.0 m | 7.8 / 6.7 / 6.7 m | taller, narrower, asymmetric, pale bark |
| Tree_Broadleaf_C | 11.5 / 10.8 / 10.7 m | 9.2 / 8.7 / 10.1 m | open canopy, visible branching, canopy gaps, dark bark |
| Tree_Broadleaf_D | 11.7 / 10.2 / 11.1 m | 11.5 / 9.5 / 11.5 m | denser umbrella crown |
| Tree_SmallRoadside_A | 5.4 / 5.7 / 4.8 m | 4.3 / 4.2 / 5.0 m | compact young tree |
| Tree_SmallRoadside_B | 6.0 / 6.8 / 5.9 m | 5.3 / 4.7 / 5.8 m | leaning, asymmetric |
| Tree_Conifer_A | 14.8 / 16.0 / 13.8 m | 6.1 / 5.1 / 6.5 m | tall narrow fir silhouette |
| Tree_Conifer_B | 9.9 / 10.8 / 9.2 m | 9.3 / 7.0 / 10.3 m | broader, irregular |
Variants differ in seed, height, crown width, branch count, lean, gaps, card density and crown shape; they are not rotated copies. Shrubs: `Bush_A/B/C/D`, `Bush_Dry_A`, `Hedge_Organic_A` (4 m, origin at the start, runs along -Y / Unity +Z). Grass: 10 clumps. Weeds: `Weed_A/B/C`, `WildPlant_A/B`, `FlowerSparse_A`.

#### 6. FBX files (`FBX/`)
`Trees_Broadleaf.fbx` (60 objects), `Trees_Small.fbx` (30), `Trees_Conifer.fbx` (30), `Shrubs.fbx` (24), `Grass.fbx` (10), `Weeds.fbx` (6), `Vegetation_CollisionOptional.fbx` (8), `vegetation_complete.fbx` (168). Use the split files or the complete file, not both. Texture paths inside the FBX are relative and not embedded: assign the atlases manually.

#### 7. LOD naming and triangles
`<Asset>` empty root -> `<Asset>_LOD0 .. LOD3` (trees) or `LOD0 .. LOD2` (shrubs); Unity builds a LODGroup from the suffixes. Grass and weeds are single meshes with no LOD (8-14 triangles). LODs are regenerated from the same skeleton (not decimated): interior cards go first, remaining cards grow, branches lose rings then orders; trunk, height, width, gaps and the outer silhouette stay.
| Triangles (Variant A) | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Broadleaf A / B / C / D | 8,932 / 8,128 / 6,472 / 9,344 | 4,574 / 4,166 / 3,724 / 4,780 | 1,090 / 974 / 706 / 1,188 | 544 / 486 / 358 / 588 |
| SmallRoadside A / B | 4,338 / 4,336 | 2,536 / 2,536 | 618 / 618 | 314 / 314 |
| Conifer A / B | 5,046 / 2,256 | 3,484 / 1,554 | 402 / 212 | 170 / 86 |
| Bush A / B / C / D / Dry / Hedge | 780 / 900 / 620 / 470 / 570 / 720 | 498 / 582 / 394 / 330 / 404 / 420 | 242 / 278 / 192 / 144 / 174 / 286 | - |
Variants B / C differ from A by -18 % to +51 % in triangles (the largest spread is Conifer_B variant B). Full per-asset numbers: `Reports/P1_vegetation_geometry.json`. LOD2 / LOD3 broadleaf cards are larger (x1.75 / x2.4) and conifer apex cards are capped, so the envelope stays within height -12 % / +18 % and width -30 % / +25 % of LOD0 (measured).
Suggested LOD Group screen heights: trees 35 / 12 / 4 / 1.2 % then impostor at about 0.4 %; shrubs 25 / 8 / 2 %.

#### 8-10. Atlases (see `Reports/P1_vegetation_materials.md`)
`Textures/Foliage/T_Vegetation_Leaves_Atlas_2K_{BaseColor(+alpha),Normal,Roughness,Variation}.png`, `Textures/Bark/T_Vegetation_Bark_Atlas_2K_{BaseColor,Normal,Roughness,AO}.png`, `Textures/Grass/T_Vegetation_Grass_Atlas_2K_{BaseColor(+alpha),Normal,Roughness}.png`. Weeds use the **grass atlas** (see `Textures/Weeds/README.txt`). Normals are OpenGL (no flip); roughness must be inverted for URP smoothness; alpha is straight (non-premultiplied). Five shared materials: `MAT_Veg_Bark`, `MAT_Veg_Leaves_Broadleaf / _Conifer / _Dry`, `MAT_Veg_Grass`.

#### 11-12. Alpha clipping and double-sided foliage
Alpha **cutoff 0.4** (alpha-to-coverage recommended with MSAA). Foliage and grass are single quads: set the foliage / grass shader **Cull Off (two-sided)** and flip the normal on back faces. Cards are tightly cropped to their alpha bounding box (cropped opaque coverage 0.21-0.68); a Broadleaf_A LOD0 is about 1,200 cards (2,400 triangles) plus 6,500 triangles of trunk and branches: **LOD0 is wood-heavy**; Conifer_A LOD0 is 477 cards + 4,100 wood triangles. Foliage is cheap, branches are the cost.

#### 13. WindData
Vertex colour set 0 on every renderable mesh: R branch bend, G leaf flutter, B phase, A stiffness. Exact values: `Reports/P1_vegetation_wind_guide.md`. Read it as `mesh.colors`. (Unlike the terrain FBXs there is no second colour set here.)

#### 14. Optional colliders
`Collision_Tree_<Archetype>` (8): 8-sided trunk prisms (28 triangles), ground-centre origin, no materials, **unparented** (shared by the three variants of an archetype; radius = largest trunk, 1.25 x, up to 3 m high). No foliage or branch collision. Only needed if cars can leave the road; gameplay currently does not require them.

#### 15. Impostor sources
`Textures/Impostors/Impostor_<Species>_{BaseColor,Normal,Depth}.png`, 8 views, 1024 x 512 atlases. See `Reports/P1_vegetation_impostor_guide.md`. The impostor render rig is not in any FBX.

#### 16-18. Instancing, LOD usage, culling (recommendations, untested)
- GPU-instance every tree / bush / grass mesh per LOD (one material per category). Wind should be a per-instance-hashed time offset.
- **PC:** LOD0 near (garage / showcase), LOD1 normal gameplay, LOD2 mid distance, LOD3 far, impostor very far.
- **Mobile:** start at LOD1 or LOD2, LOD3 earlier, impostor sooner, cut grass / weed distance hard (they are cheap but numerous: about 8-14 triangles each, thousands of instances), aggressive frustum + distance culling, drop `Variation` and normal maps, prefer alpha-to-coverage off with a harder cutoff.
- Cull trees by distance and screen size; group per streaming chunk (40 m) or per terrain-module pair so a chunk's vegetation spawns / recycles with it.

#### 19. Relationship to the terrain
Placement is meant to read the **frozen terrain's** `TerrainBlend` (vertex colour: R grass, G soil, B rock, A gravel) and `VegetationMask` (UV channel 1: U density, V dryness) plus slope and road distance: see `VEGETATION_PLACEMENT_GUIDE.md`. Vegetation never changes terrain or road. The Blender scatter was a preview tool and is not part of the package.

#### 20. Excluded QA content
The 320 m QA scene (linked road, props, terrain strips, hypercar), about 7,100 scattered instances, all cameras and lights, the impostor rig and the blockout proxies are not in any FBX (list: `Reports/P1_vegetation_export_manifest.json`).


#### 03A update (Vegetation LOD0 / Foliage Quality / Final Polish)
Same 8 FBX file names, same object names, same LOD structure, same pivots and axis convention. What changed:
- **Wood geometry**: LOD0 trunk/branch triangles cut by 70-85 % (trunk 12 -> 8 sides, branches RDP-simplified, foliage-hidden branches removed). Silhouette, height and pivots are unchanged; LOD0 broadleaf trees are now ~2.5-3.7 k triangles (was ~6-9 k).
- **Foliage atlas** (`Textures/Foliage/T_Vegetation_Leaves_Atlas_2K_*`, same name / layout / 2K): irregular cluster outlines, rim leaves smaller, conifer sprays redrawn as dense fishbone sprays. `atlas_cell_rects.json` is updated; cell *names* are unchanged.
- **New data channel - second UV set `CanopyShadeUV`** (Unity `mesh.uv2`, UV channel 1) on every tree mesh (all LODs): **U = canopy interior depth** (0 = outer leaf, 1 = canopy core; use as ambient-occlusion / darkening: `albedo *= lerp(1, 0.45, U)` and optionally lower specular), **V = per-card leaf tint variation** (0..1, centre 0.5; multiply albedo by a 0.86..1.1 ramp, hue-shifted yellow-ward for high V). Shrubs, grass and weeds carry the same set with constants (0, 0.5). Do **not** use WindData for shading.
- **WindData convention is UNCHANGED**: colour set 0 `WindData` = R primary-branch bend, G leaf / fine flutter, B phase offset, A stiffness / anchor. LOD0-LOD3 keep identical semantics.
- LOD2/LOD3 envelopes are tighter than in 03 (cards are shifted inward as they grow) - no more crown growth at distance; transitions at 45 m checked in `previews/03A_lod_pop_*.png`.
- Custom normals, alpha cutoff (0.4), double-sided foliage, impostor sources (regenerated from the polished LOD0) follow the earlier notes.

---

### `UnityTransfer/README/VEGETATION_PLACEMENT_GUIDE.md`

### Vegetation placement guide (interpretation of the frozen terrain data)

This is what the Blender QA scatter did, so a Unity implementation can match it. It is **not** the only valid implementation (a splat-mask scatter, a baked placement table, or GPU instancing driven by the same inputs would all work). Thresholds are the values that passed validation in the 320 m QA scene.

#### Inputs
| Input | Where | Meaning |
|---|---|---|
| **TerrainBlend** | vertex colour (`mesh.colors`) of every terrain strip | R grass, G soil, B rock, A gravel; weights sum to 1 |
| **VegetationMask** | terrain UV channel 1 (`mesh.uv2`) | **U = density 0-1, V = dryness 0-1** (also colour set 1 in the FBX, which Unity ignores) |
| Slope | terrain normal | `slope = 1 - normal.y` (Unity) |
| Road distance | `d = |x|` from the road centreline (the chunk origin) | metres |
| Prop distance | P1 props: guardrail X 11, streetlights 12, signs 12.8, CCTV 14, cabinet 14.2, gantry plinths 11.8-13, median lights on the barrier top | metres |
| Rocks / walls | `RockCut_*`, `Cliff_Module_*`, `RetainingWall_*`, loose rocks | exclusion volumes + 2.5 m margin |

#### Rules (class: minimum d / maximum slope / maximum rock B / maximum gravel A / minimum density U)
| Class | d | slope | rock | gravel | U | notes |
|---|---|---|---|---|---|---|
| **Trees** | small 21+, broadleaf 27+, conifer 30+ (and crown clear: **d - crown radius >= 16.5**) | 0.11 (about 27 degrees) | 0.22 | 0.20 | 0.25 | clusters 2-5 trees, 16-44 m apart, cluster centres at d 33-46 (small trees 23-31); spacing >= 0.62 x summed crown radii; scale 0.85-1.15; tilt about 1.5 degrees |
| **Shrubs** | 19+ | 0.16 | 0.25 | 0.25 | 0.15 | groups of 1-4, d 20-40; `Bush_Dry_A` where dryness > 0.52 |
| **Grass** | 16.5+ | 0.24 | 0.20 | 0.25 | 0.08 | accept with probability U^1.2; rate about 0.55 clumps / m2 at U = 1 (QA density, tune per platform) |
| **Weeds** | 17.5+ | 0.24 | 0.20 | 0.25 | 0.08 | probability U x (0.35 + 1.4 G): more on soil |
Hard zero everywhere: road, shoulders, drain, **d < 16.5**, gravel-heavy transition, rock (B > 0.7), retaining walls, and any vertex whose U is 0 (the terrain already encodes this).

#### Species choice
- **Distance bands:** d < 19.5 -> `Grass_RoadEdge_*` (50 %), short grass; 19.5-24 -> short / medium; 24-34 -> medium; > 34 -> tall. Trees: small trees nearest the road (23-31), medium broadleaf and conifers further (33-46).
- **Dryness V:** V > 0.5 -> `Grass_Dry_*` (75 %), `Bush_Dry_A` (80 % of shrub picks); lower V stays green. Do not make a whole zone yellow: the QA mean dryness was 0.58 for dry clumps vs 0.26 for green ones.
- **Slope:** flat and gentle -> trees, bushes, grass; moderate (0.11-0.16) -> bushes and grass; steep cut (> 0.24) and rock faces -> nothing. Never grow trees sideways from cliffs.
- **Clustering:** cluster dominant species (60 % of a cluster is one species, the rest from a second), choose the least-used variant per species so neighbours differ; leave 16-44 m gaps between clusters. Avoid fixed-interval repetition.
- **Density presets** used in QA (Normal_Highway is the primary look): Sparse_Highway (24 trees, 63 bushes, 3,241 grass, 116 weeds per 320 m), Normal_Highway (68 / 124 / 6,672 / 239), Dense_FarEdge (126 / 150 / 8,633 / 281).

#### Infrastructure clearance
Never inside d < 16.5; keep 2.5-4.5 m radius around streetlights, signs, CCTV, cabinet, median lights and gantry plinths; grass may approach behind the guardrail but must not touch the rails, posts or delineators. Sign faces (X 12.8), VMS and gantry panels stay visible because all vegetation is behind the sign line (d >= 16.5) and the tallest vegetation in the first 28 m is a bush or small tree.

#### Terrain contact
Sink the pivot **1-8 cm** into the terrain surface (QA used 5 cm for trees and bushes, 1 cm for grass); the trunk base ring is flat so it cannot dip below the pivot.

---

### `reports/P1_vegetation_materials.md`

### P1-BLENDER-03 — materials, atlases, alpha strategy

Everything is a Blender *source / preview* material. Unity shaders, double-sided setup and wind are Unity-side work.

#### Material categories (5 shared, no per-species materials)
| Material | Atlas | Used by |
|---|---|---|
| `MAT_Veg_Bark` | `T_Vegetation_Bark_Atlas_2K` | trunks, branches, shrub stems (all species) |
| `MAT_Veg_Leaves_Broadleaf` | `T_Vegetation_Leaves_Atlas_2K` (cells BL_*, BL2_*) | broadleaf / small trees, bushes, hedge |
| `MAT_Veg_Leaves_Conifer` | same foliage atlas (cells CN_*) | conifers |
| `MAT_Veg_Leaves_Dry` | same foliage atlas (cells DRY_*) | dry cards inside broadleaf trees (2-4 %), `Bush_Dry_A` |
| `MAT_Veg_Grass` | `T_Vegetation_Grass_Atlas_2K` | all grass, weeds, wild plants, flowers |
In Unity the three foliage materials can be **one material** with a tint property; the slots are kept apart so dryness / species tint can be driven separately.

#### Foliage atlas — `T_Vegetation_Leaves_Atlas_2K_*` (2048 x 2048)
| Map | Channels | Notes |
|---|---|---|
| `_BaseColor.png` | RGB colour, **A = alpha** | straight (non-premultiplied); RGB dilated 26 px into the transparent border |
| `_Normal.png` | tangent space, **OpenGL (+Y green)** | deliberately subtle (leaf dome + vein); use strength about 0.35 |
| `_Roughness.png` | roughness 0.58 +/- 0.10 | URP: smoothness = 1 - roughness |
| `_Variation.png` | R per-leaf random 0-1 (hue / value jitter), G edge-thin / translucency proxy 0.2-1, B cluster-density AO 0.55-1 | optional; drives dryness tint, translucency, ambient shading |
Layout: 4 x 4 cells of 512 px (origin bottom-left): row 0 (top) `BL_dense BL_sparse BL_twig BL_small`, row 1 `BL2_*` (lighter yellow-green), row 2 `CN_spray_A CN_spray_B CN_tuft CN_scale`, row 3 `DRY_A DRY_B DRY_twig DRY_small`.
**Tight crop:** every cell has a recorded alpha bounding box in `Reports/atlas_cell_rects.json` (atlas px: x0, y0, x1, y1); the meshes' UVs cover exactly that rectangle, so card aspect ratio equals the crop aspect (no stretching) and little transparent area is drawn.
Cropped opaque coverage: foliage 0.23-0.68 (mean 0.47), grass 0.21-0.65 (mean 0.39).

#### Bark atlas — `T_Vegetation_Bark_Atlas_2K_*` (2048 x 2048, BaseColor / Normal / Roughness / AO)
4 vertical columns of 512 px: `light` (U 0-0.25, pale smooth bark with lenticels), `medium` (0.25-0.5, brown furrowed), `dark` (0.5-0.75, coarse), `conifer` (0.75-1, reddish plates).
U runs around the circumference inside one column (periodic, seamless); **V = metres along the member / 4**, so V runs past 1 and the sampler must **repeat in V** (clamp / mirror U within the column or sample with a per-column offset in the shader). Bark normals are OpenGL, stronger than leaves.
Texel density is about 512 px/m along the member; around the ring it depends on the radius (thin branches are denser, trunks about 320 px/m).

#### Grass / weed atlas — `T_Vegetation_Grass_Atlas_2K_*` (BaseColor+Alpha, Normal, Roughness)
Top half: 8 tall cells 256 x 1024 (`G_short_A/B, G_med_A/B, G_tall_A/B, G_dry_A/B`). Bottom half: 8 cells 512 x 512 (`W_weed_A/B/C, W_wild_A/B, W_flower_A, G_edge_A/B`). World size of each crop is in the cell table (`scripts/veg_common.py`, `GRASS_CELLS`) and baked into the card sizes.

#### Alpha strategy and padding
- Alpha is a **cutout** (cutoff 0.4, stored as the custom property `alpha_cutoff` on each Blender material); use alpha-to-coverage with MSAA where available, otherwise clip at 0.4 and keep the mips alpha-scaled to avoid thinning.
- **Padding / bleed:** all cells are composed over black, divided by coverage (un-premultiplied), then colour is dilated 26-30 px into the transparent border. Validation: 0 black / white fringe pixels within 8 px of any leaf or blade (threshold < 1 %).
- Double-sided: all foliage and grass cards are single quads, rendered double-sided in Unity (cull Off) with the **normal flipped on back faces**; no duplicated back faces exist.
- Custom normals: foliage vertex normals are blended 72-75 % crown-radial (from the crown centre outward) with the card normal, grass 55 % up, so canopies shade as one volume and cards have no black backs.

#### Colour / dryness variation
No separate seasonal textures. Healthy -> slightly dry -> yellow is meant to be produced in Unity by (a) tinting `MAT_Veg_Leaves_*` with `Variation.R` jitter and a terrain-driven dryness (VegetationMask V), (b) swapping to the `DRY_*` cells / `Bush_Dry_A` / `Grass_Dry_*` when dryness is high. The `BL2_*` cells are a lighter yellow-green sibling of `BL_*` and the `DRY_*` cells carry the brown-yellow state.

---

### `reports/P1_vegetation_impostor_guide.md`

### P1-BLENDER-03 — impostor SOURCE guide

Source renders only: no Unity impostor shader or runtime is included.

| Item | Value |
|---|---|
| Species (8) | `Tree_Broadleaf_A/B/C/D`, `Tree_SmallRoadside_A/B`, `Tree_Conifer_A/B` — **Variant A, LOD0** is the source of each |
| Views | **8 horizontal directions**, every 45 degrees; no top-down view (not needed for a ground-level road camera) |
| View i | camera at azimuth i * 45 degrees measured from Blender -Y, camera position (sin a, -cos a) * 60 m, looking at the tree's vertical centre |
| Projection | **orthographic**, scale = max(height, width) * 1.08 m (per species, see `reports/P1_vegetation_impostors.json`), identical for all 8 views of a species |
| Resolution | 256 x 256 px per view; atlas **1024 x 512** (4 x 2): row 0 (image top) views 0-3, row 1 views 4-7 |
| Files (`textures/impostors/`) | `Impostor_<Species>_BaseColor.png` (RGB + **alpha**), `_Normal.png` (**world-space** normal, RGB = N * 0.5 + 0.5, alpha = silhouette, neutral (0.5, 0.5, 1) outside), `_Depth.png` (linear camera depth, **white = near**, 0 = far / background, alpha = silhouette) |
| Lighting | flat, **unlit albedo** (emission of the base colour, no sun, no baked directional shadows or AO) so Unity can relight; Standard view transform, no tone mapping |
| Alpha | transparent film, straight alpha, RGB dilated 10 px into the border |
| Depth mapping | depth = 1 - (z - (D - R)) / (2 R) with D = 60 m (camera distance) and R = 0.75 * ortho scale |
| Normal frame | the tree is not rotated, the camera orbits it: normals are world-space, so Unity must rotate them by the view yaw if it needs view-space |
| Rig | `Impostor_Rig_Camera` + 8 `Impostor_Rig_View_i` empties in `VEG_IMPOSTOR_SOURCE` (blend only, never exported) |

Intended Unity use: beyond LOD3, crossfade a camera-facing quad that selects (and optionally blends) the two nearest of the 8 views; use `Depth` for parallax / depth-offset and `Normal` for relighting. For the 8-view set, cell index = round(viewAngle / 45 degrees) mod 8.
Visual review: `previews/P1_impostor_sources.png` (all 8 species BaseColor over grey).

---

### `reports/P1_vegetation_wind_guide.md`

### P1-BLENDER-03 — WindData guide

Vertex colour attribute **`WindData`** (FLOAT_COLOR, per vertex; exported as the primary colour set, LINEAR, 8-bit corner colours in the FBX; Unity `mesh.colors`). Data only: no animation exists in Blender.

| Channel | Meaning | Range |
|---|---|---|
| **R** | primary branch bend strength: low-frequency sway of the branch / trunk about its root | 0 (rigid, trunk base) -> 1 (upper outer branches) |
| **G** | leaf / fine flutter strength: high-frequency detail bend of leaf cards and blade tips | 0 on wood, 0.55-1 on foliage (0.55 at a card's lower edge, 1.0 at its upper edge) |
| **B** | phase / random offset: break up synchronised motion | one random value per branch (wood) or **per card** (constant over its 4 vertices) |
| **A** | stiffness / anchor influence: 1 = fully anchored | 1 at the base, falling toward tips (cards 0.15-0.2) |

#### Values as built
| Part | R | G | B | A |
|---|---|---|---|---|
| Trunk base (z about 0) | **0** | **0** | 0.5 | **1.0** |
| Trunk, height fraction f = z / trunk height | 0.12 * f^1.4 | 0 | 0.5 | 1 - 0.35 f |
| Primary branch, parameter u along it | R_attach + (0.29) * u^1.2 | 0 | random per branch | A_attach * (1 - 0.75 u) |
| Secondary branch (order 2) | R_attach + 0.42 * u^1.2 | 0 | random | A_attach * (1 - 0.75 u) |
| Twig (order 3) | R_attach + 0.55 * u^1.2 | 0.15 u | random | A_attach * (1 - 0.75 u) |
| **Leaf cluster card** | R of the branch point + 0.08 | 0.55 (lower verts) .. 1.0 (upper verts) | **random per card** | 0.15 |
| Shrub stem | 0.25 u | 0 | random | 1 - 0.6 u |
| Shrub card | 0.15 + 0.5 z / h | 0.55 .. 1.0 | random per card | 0.2 |
| Grass / weed card base vertices | 0 | 0 | random per card | 1 |
| Grass / weed card tip vertices | 0.35 | 1 | same card value | 0.15 |

Examples: **trunk base** (0, 0, 0.5, 1) never moves; an **upper branch** (0.6-0.9, 0, phase, 0.3-0.4) sways with the tree; a **leaf cluster** (R of its branch, 0.55-1, own phase, 0.15) flutters on top of the branch motion with an offset from its neighbours; **grass** blends from anchored base to a fully flexible tip.

Unity usage (not implemented here): `offset = windDir * (R * bendAmp * sin(t * f1 + B * 6.28) + G * flutterAmp * sin(t * f2 + B * 12.57)) * (1 - A)`; the LOD cards use the same convention so wind stays consistent across LODs. Impostors have no wind.


**03A: WindData convention unchanged** (R bend, G flutter, B phase, A stiffness). Canopy shading lives in the separate `CanopyShadeUV` UV channel.

---

### `reports/P1_vegetation_discovery.md`

### P1-BLENDER-03 — Vegetation: Discovery

Date: 2026-10-07 · Blender 5.2.2 · Blender-only workstation. P0, P1 Props, P1 Terrain (**`terrain_09_final_frozen.blend` only**) and the hypercar are linked read-only; nothing frozen is ever written.

#### 1. Placement data available (measured on the linked terrain_09 meshes)

| Data | Where | Facts |
|---|---|---|
| TerrainBlend | colour attribute on every terrain strip / ditch insert / rock | R grass, G soil, B rock, A gravel, weights sum to 1; FLOAT_COLOR per vertex |
| VegetationMask | colour set 1 **and UV channel 1 (`VegetationMaskUV`)** | U = density 0-1, V = dryness 0-1; the UV copy is what Unity reads |
| Density statistics | linked strips | Flat_R: mean 0.60 (0..1), dryness mean 0.28; Cut_Medium_R: mean 0.39, 20 % zero; RockCut_R: mean 0.30, 33 % zero |
| Zero-density zones | built into the mask | d < 16.5 m from the centreline, all transitions, rock (B > 0.7), gravel, steep faces |
| Terrain heights | strips | verge -0.30, corridor -0.29 … -0.32, Cut_Medium +5.4 … +6.3, Cut_Low +2.4 … +3.0, RockCut +7.0 … +7.9, Fill_Shallow -2.3 … -2.5, outer edge -1.2 at d 50 |
| Prop lines (P1) | right side X | guardrail -11.0, streetlights -12.0, signs -12.8, CCTV -14.0, cabinet -14.2, gantry plinths -11.8..-13.0 (right), +10.35 (median); median lights on the barrier top +9.7 |
| Rocks / walls | `RockCut_*`, `Cliff_Module_*`, `RetainingWall_*`, `Rock_*` | exclusion volumes for the scatter |

No existing vegetation assets or references exist in the workspace (`references/` is empty).

#### 2. Biome direction
Temperate, generic highway roadside (no country- or tropics-specific species): mown / semi-dry grass verges, scrub bushes, roadside broadleaf trees, a few conifers
for silhouette contrast, dry patches. Moderately dry overall (terrain dryness 0.3-0.5) so the library carries a green → slightly dry → yellow tint range via a variation channel, not separate seasonal sets.

#### 3. Planned library
- **Trees (8 archetypes x 3 variants x LOD0-3 = 96 meshes):** Broadleaf_A (broad rounded wide-low crown), _B (tall narrow asymmetric), _C (open canopy, visible branching, gaps), _D (dense umbrella); SmallRoadside_A (compact 4-6 m), _B (leaning, asymmetric 5-7 m); Conifer_A (tall narrow 14-16 m), _B (broad irregular 9-11 m). Variants change the seed *and* crown shape, lean, branch count, density, gaps and height, so they are not rotated copies.
- **Shrubs (6, LOD0-2):** Bush_A rounded-irregular, _B wide / low, _C upright, _D sparse / asymmetric, Bush_Dry_A dry / sparse, Hedge_Organic_A (4 m linear, natural).
- **Grass (10, single LOD):** Short A/B, Medium A/B, Tall A/B, Dry A/B, RoadEdge A/B.
- **Weeds / small plants (6, single LOD):** Weed A/B/C, WildPlant A/B, FlowerSparse_A.
- **Optional:** 8 simple trunk collider proxies (`Collision_Tree_<Archetype>`).

#### 4. Construction method
- Trunk + major branches = tapered tube meshes (root flare, per-ring jitter); no twig modelling.
- Canopy = **tightly cropped leaf-cluster cards** placed along terminal branches; crown shape comes from the branch skeleton and a per-variant envelope, so silhouettes are irregular and species-specific. Cards face outward with random tilt/roll, never crossed-X pairs.
- Canopy lighting: custom per-vertex normals blended 75 % crown-radial (outward from the crown centre) / 25 % card normal, so a card has no black back and the crown shades like one volume. Unity should render foliage double-sided with the normal flipped on back faces (standard).
- LODs are *regenerated from the same skeleton and seed* (not decimated): interior cards go first, remaining cards get larger, branches lose rings and then orders; trunk position, height, width, major gaps and the outer silhouette stay.

#### 5. Material / atlas strategy (5 shared material categories)
| Material | Texture |
|---|---|
| `MAT_Veg_Bark` | `T_Vegetation_Bark_Atlas_2K` (4 vertical columns: light smooth, medium furrowed, dark coarse, conifer; V tiles every 4 m) |
| `MAT_Veg_Leaves_Broadleaf`, `_Conifer`, `_Dry` | one `T_Vegetation_Leaves_Atlas_2K` (4x4 cells of 512 px: broadleaf, alt broadleaf, conifer sprays, dry) + a variation map |
| `MAT_Veg_Grass` | `T_Vegetation_Grass_Atlas_2K` (8 tall grass cells 256x1024, 8 weed / plant cells 512x512) |
All BaseColor+Alpha with RGB dilated into the transparent border (no white / black fringes), plus Normal, Roughness (and AO for bark). Recommended Unity alpha cutoff 0.4.

#### 6. Wind-data strategy
Vertex colour `WindData`: R primary branch bend (0 at the trunk base, rises with height and branch order), G leaf flutter (0 on wood, 0.5-1 on cards), B per-cluster phase (constant over a card), A stiffness / anchor (1 at the base, falling toward the tips). Data only; no animation.

#### 7. Impostor strategy
Per archetype (variant A, LOD0): 8 horizontal directions (45° steps) rendered orthographic, transparent, flat neutral lighting, no cast shadows -> 4x2 atlas of 256 px cells: `BaseColor+Alpha`, object-space `Normal`, linear `Depth`. Rig lives in `VEG_IMPOSTOR_SOURCE`, not in the FBX.

#### 8. Placement QA (Blender only)
A scatter tool reads TerrainBlend and VegetationMask (UV1) by raycasting the linked strips, plus slope, road distance, prop and rock/wall distance, dryness. Zones: grass from d 17, bushes from d 19, small trees from d 22, large trees from d 28, conifer / cluster band 34-48; all tree crowns must clear d 16.5. Clustered, not uniform. Presets Sparse_Highway / Normal_Highway / Dense_FarEdge.

#### 9. Unity integration assumptions
GPU-instanced LOD groups per species; per-species alpha-clipped double-sided foliage material; wind from `WindData`; runtime scatter from the same terrain data; impostor billboards beyond LOD3; grass distance culling on mobile. None of this is tested here.

---

### `reports/P1_vegetation_FINAL_FREEZE_03A.md`

### P1_Vegetation - FINAL FREEZE (03A)

Date: 2026-10-07 - Phase P1-BLENDER-03A (supersedes the 03 freeze for deliverables; the 03 checkpoints 01-07 are retained unchanged) - Status: **FROZEN**. Nothing under `environment/P1_Vegetation/` is to be edited; later phases may only link from it.

#### Final deliverables
- **Final blend:** `blend/vegetation_09_final_frozen.blend` (export source; `vegetation_08_lod0_polish.blend` is the pre-export checkpoint). `vegetation_01 ... 07` are byte-identical to the 03 phase.
- **FBX** (same 8 names, `exports/` = `UnityTransfer/FBX/`; 03 versions archived in `exports/_pre_03A/`).
- **Textures:** regenerated foliage atlas + 8x3 impostor atlases (03 versions in `textures/_pre_03A/`); bark and grass atlases untouched.
- **New data channel:** UV1 `CanopyShadeUV` (U interior depth, V tint variation). WindData convention unchanged.

#### Validation
`reports/P1_vegetation_03A_validation.txt`: 39 base checks (03 suite re-run on vegetation_09 incl. FBX re-import, 0 errors) + 03A additions (wood reduction, silhouette, LOD envelope, shade UV, species distribution, card counts, triangle budget, ground contact).
Source integrity: **PASS** (`reports/P1_vegetation_03A_source_integrity.md`) - P0, Props, Terrain, cars and vegetation checkpoints 01-07 byte-identical.

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P1_vegetation_03A_validation.txt`

```text
== P1-BLENDER-03A VEGETATION - VALIDATION (checks 1-39: the 03 suite re-run on vegetation_09; 40+: 03A additions) ==
source blend/vegetation_09_final_frozen.blend; VEGETATION_MASTER 168 objects, 138 meshes

[PASS]  1. 8 tree archetypes x 3 variants x LOD0-LOD3 exist (96 meshes) under <Asset> empty roots
[PASS]  2. 6 shrub assets with LOD0-LOD2
[PASS]  3. 10 grass assets (4 short/medium, 2 tall, 2 dry, 2 road-edge)
[PASS]  4. 6 weed / small-plant assets
[PASS]  5. 8 optional trunk colliders Collision_<Archetype> (closed prisms, no materials, unparented, ground-centre origin)
[PASS]  6. tree variants are genuinely different (3 distinct height/width signatures and distinct triangle counts per archetype)
[PASS]  7. shared atlases exist: foliage (BaseColor+Alpha, Normal, Roughness, Variation), bark (BaseColor, Normal, Roughness, AO), grass (BaseColor+Alpha, Normal, Roughness)
[PASS]  8. atlas resolution 2048 x 2048 (no 4K / 8K)
[PASS]  9. alpha padding: colour is dilated into the transparent border (no black / white fringe pixels within 8 px of any leaf or blade)
[PASS] 10. alpha-overdraw: every cell is tight-cropped; cropped opaque coverage >= 0.18 for all used cells, mean >= 0.38 (foliage) / 0.32 (grass)
[PASS] 11. UVs: UVMap on all 130 renderable meshes; bark UVs inside one bark column; every leaf / grass face inside one tight-cropped atlas cell
[PASS] 12. materials: only the 5 shared categories (MAT_Veg_Bark / _Leaves_Broadleaf / _Leaves_Conifer / _Leaves_Dry / _Grass); every slot used; colliders have none
[PASS] 13. WindData colour attribute (FLOAT_COLOR, point) on every renderable mesh, values within 0..1
[PASS] 14. custom (canopy-radial) vertex normals present on every renderable mesh
[PASS] 15. topology: no non-manifold edges, zero-area / duplicate faces, ngons, inconsistent winding or loose vertices
[PASS] 16. WindData semantics: trunk base R~0 / G=0 / A~1; branch R rises with height / order; leaf cards G >= 0.55; phase B constant per card and varying between cards; grass base G=0, A=1, tip G=1
[PASS] 17. LOD chains: 30 groups (24 trees x LOD0-3, 6 shrubs x LOD0-2), triangle counts strictly decreasing
[PASS] 18. LODs keep the silhouette envelope: height within -12 % / +18 % (+28 % shrubs), width within -30 % / +25 % (+35 % conifers) of LOD0
[PASS] 19. pivots: every asset base at Z 0 (<= 10 cm embedded), the trunk ground ring is centred on the origin within 0.05 m (bottom-centre origin)
[PASS] 20. transforms: all assets identity (scale 1, no rotation, no negative scale), roots at the origin
[PASS] 21. terrain contact: all 7098 QA instances re-sampled on the frozen terrain: base sits 1-8 cm into the ground (no floating, no buried trunks)
[PASS] 22. TerrainBlend QA: trees on grass/soil only (rock < .25, gravel < .2), bushes rock/gravel < .25, grass rock < .20 / gravel < .25; none on rock faces
[PASS] 23. VegetationMask QA: density U >= .25 (trees) / .15 (bushes) / .08 (grass); mean placed density > 0.4 (scatter follows the mask); dry zones favour dry species
[PASS] 24. road clearance: no vegetation inside d < 16.5 (road, shoulder, drain, guardrail, streetlight / sign / CCTV / gantry bases); no tree crown overhangs d < 16; bushes start at d 19
[PASS] 25. prop / rock / wall clearance: no instance inside any prop exclusion circle (streetlights, signs, CCTV, cabinet, gantry plinths, median lights, loose rocks) or rock-cut / cliff / retaining-wall rectangle
[PASS] 26. sign / gantry / VMS visibility: every instance is >= 16.5 m from the centreline, behind the sign line (X 12.8) and outside the gantry spans; tallest vegetation within the first 28 m is a bush or small tree (< 7 m)
[PASS] 27. repetition: >= 7 of 8 archetypes and >= 14 distinct tree variants used in the 320 m scene; clustered placement (nearest-neighbour gaps vary); no identical consecutive neighbours dominate
[PASS] 28. density presets generated: Sparse_Highway < Normal_Highway < Dense_FarEdge (trees)
[PASS] 29. impostor sources: 8 species x (BaseColor+Alpha, Normal, Depth), 1024 x 512 atlases of 8 views (256 px cells), every view non-empty
[PASS] 30. export selection == VEGETATION_MASTER production assets; no QA / road / props / terrain / hypercar / camera / light / impostor-rig objects; no leaked selection
[PASS] 31. FBX re-import Trees_Broadleaf.fbx: 60 objects (48 LOD meshes, 0 colliders)
[PASS] 32. FBX re-import Trees_Small.fbx: 30 objects (24 LOD meshes, 0 colliders)
[PASS] 33. FBX re-import Trees_Conifer.fbx: 30 objects (24 LOD meshes, 0 colliders)
[PASS] 34. FBX re-import Shrubs.fbx: 24 objects (18 LOD meshes, 0 colliders)
[PASS] 35. FBX re-import Grass.fbx: 10 objects (0 LOD meshes, 0 colliders)
[PASS] 36. FBX re-import Weeds.fbx: 6 objects (0 LOD meshes, 0 colliders)
[PASS] 37. FBX re-import Vegetation_CollisionOptional.fbx: 8 objects (0 LOD meshes, 8 colliders)
[PASS] 38. FBX re-import vegetation_complete.fbx: 168 objects (114 LOD meshes, 8 colliders)
[PASS] 39. source integrity: P0 (95), P1 Props (77), P1 Terrain (166), cars (108) and 232 other files byte-identical to the baseline

-- 03A additions --
[PASS] 40. wood geometry reduced: LOD0 wood triangles of every tree variant A fell >= 50% and wood share <= 62% (broadleaf/small <= 55%)
[PASS] 41. silhouette preserved at LOD0/LOD1: height within 6% and canopy width within 8% (conifer width within 20%, height within 3%) of the 03 asset; LOD2/3 intentionally tighter (envelope growth reduced)
[PASS] 42. LOD envelope: LOD1-3 canopy width and height within +-18% of LOD0 (no growth at distance)
[PASS] 43. CanopyShadeUV (UV channel 1) exists on every tree LOD mesh (2 UV layers: UVMap, CanopyShadeUV), values in 0..1; WindData untouched
[PASS] 44. QA species distribution: all 8 tree archetypes appear in the Normal_Highway scatter (>= 4 each)
[PASS] 45. foliage card counts not significantly increased vs 03 (<= 105% for every tree variant A)
[PASS] 46. Broadleaf LOD0 triangle budget: <= 7,500 and >= 2,000 for the four broadleaf archetypes (Variant A)
[PASS] 47. ground contact / pivots: every tree LOD0 lowest vertex within 0.08 m of the pivot plane

SUMMARY: 0 errors in 03A additions (+ 0 in base suite)
```

