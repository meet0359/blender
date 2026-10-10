# P2-BLENDER-01A — Bridge Valley, Embankment & Terrain Context Addendum

Digest 07 of the environment handoff. Folder: `environment/P2_BridgeTerrainContext/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/bridgeTerrain_07_export_ready.blend`
- **Asset index source:** `reports/P2_bridgeTerrain_geometry.json` + `reports/P2_bridgeTerrain_export_manifest.json`
- **Checkpoints (7):** `bridgeTerrain_01_blockout.blend`, `bridgeTerrain_02_valleys.blend`, `bridgeTerrain_03_approaches.blend`, `bridgeTerrain_04_ravine_riverbed.blend`, `bridgeTerrain_05_materials_masks.blend`, `bridgeTerrain_06_lods_collision.blend`, `bridgeTerrain_07_export_ready.blend`
- **FBX (8):** `BridgeValleys.fbx` (60 objects), `BridgeValleyTransitions.fbx` (48 objects), `BridgeApproaches.fbx` (30 objects), `BridgeUnderTerrain.fbx` (12 objects), `BridgeRavines.fbx` (12 objects), `BridgeRiverbeds.fbx` (18 objects), `BridgeTerrainCollision.fbx` (7 objects), `bridgeTerrain_complete.fbx` (187 objects)
- **Textures:** 0 PNG files · **Previews:** 16 renders · **UnityTransfer README:** `BRIDGE_TERRAIN_COMPOSITION_GUIDE.md`, `BRIDGE_TERRAIN_IMPORT_NOTES.md`, `BRIDGE_TERRAIN_PERFORMANCE_GUIDE.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `BridgeAbutmentTerrain_L` | 1,830 / 576 | BridgeApproaches.fbx |
| `BridgeAbutmentTerrain_R` | 1,794 / 572 | BridgeApproaches.fbx |
| `BridgeApproach_Exit_L` | 9,940 / 1,596 / 414 | BridgeApproaches.fbx |
| `BridgeApproach_Exit_R` | 8,540 / 1,386 / 342 | BridgeApproaches.fbx |
| `BridgeApproach_L` | 9,940 / 1,596 / 414 | BridgeApproaches.fbx |
| `BridgeApproach_R` | 8,540 / 1,386 / 342 | BridgeApproaches.fbx |
| `BridgeDryRiverbed_A` | 11,840 / 3,200 / 752 | BridgeRiverbeds.fbx |
| `BridgeDryRiverbed_B` | 11,840 / 3,200 / 752 | BridgeRiverbeds.fbx |
| `BridgePierGround_A` | 286 / 40 | BridgeUnderTerrain.fbx |
| `BridgePierGround_B` | 416 / 60 | BridgeUnderTerrain.fbx |
| `BridgeRavine_A` | 11,840 / 3,200 / 1,504 | BridgeRavines.fbx |
| `BridgeRavine_B` | 11,840 / 3,200 / 1,504 | BridgeRavines.fbx |
| `BridgeStreamBed_A` | 11,840 / 3,200 / 1,504 | BridgeRiverbeds.fbx |
| `BridgeUnderTerrain_A` | 480 / 80 | BridgeUnderTerrain.fbx |
| `BridgeUnderTerrain_B` | 256 / 36 | BridgeUnderTerrain.fbx |
| `BridgeValleyVista_L` | 1,056 / 288 | BridgeValleys.fbx |
| `BridgeValleyVista_R` | 1,056 / 288 | BridgeValleys.fbx |
| `BridgeValley_Deep_Both_40m` | 11,840 / 3,200 / 752 | BridgeValleys.fbx |
| `BridgeValley_Deep_L_40m` | 6,240 / 1,680 / 400 | BridgeValleys.fbx |
| `BridgeValley_Deep_R_40m` | 5,600 / 1,520 / 352 | BridgeValleys.fbx |
| `BridgeValley_In_20m` | 5,920 / 1,600 / 376 | BridgeValleyTransitions.fbx |
| `BridgeValley_In_L_40m` | 6,240 / 1,680 / 400 | BridgeValleyTransitions.fbx |
| `BridgeValley_In_R_40m` | 5,600 / 1,520 / 352 | BridgeValleyTransitions.fbx |
| `BridgeValley_Medium_Both_40m` | 11,840 / 3,200 / 752 | BridgeValleys.fbx |
| `BridgeValley_Medium_L_40m` | 6,240 / 1,680 / 400 | BridgeValleys.fbx |
| `BridgeValley_Medium_R_40m` | 5,600 / 1,520 / 352 | BridgeValleys.fbx |
| `BridgeValley_Out_20m` | 5,920 / 1,600 / 376 | BridgeValleyTransitions.fbx |
| `BridgeValley_Out_L_40m` | 6,240 / 1,680 / 400 | BridgeValleyTransitions.fbx |
| `BridgeValley_Out_R_40m` | 5,600 / 1,520 / 352 | BridgeValleyTransitions.fbx |
| `BridgeValley_Run_L_40m` | 6,240 / 1,680 / 400 | BridgeValleyTransitions.fbx |
| `BridgeValley_Run_R_40m` | 5,600 / 1,520 / 352 | BridgeValleyTransitions.fbx |
| `BridgeValley_Shallow_Both_40m` | 11,840 / 3,200 / 752 | BridgeValleys.fbx |
| `BridgeValley_Shallow_L_40m` | 6,240 / 1,680 / 400 | BridgeValleys.fbx |
| `BridgeValley_Shallow_R_40m` | 5,600 / 1,520 / 352 | BridgeValleys.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `BridgeApproaches.fbx` (8): BridgeApproach_Exit_L_Snap_End, BridgeApproach_Exit_L_Snap_Start, BridgeApproach_Exit_R_Snap_End, BridgeApproach_Exit_R_Snap_Start, BridgeApproach_L_Snap_End, BridgeApproach_L_Snap_Start, BridgeApproach_R_Snap_End, BridgeApproach_R_Snap_Start
- `BridgeRavines.fbx` (4): BridgeRavine_A_Snap_End, BridgeRavine_A_Snap_Start, BridgeRavine_B_Snap_End, BridgeRavine_B_Snap_Start
- `BridgeRiverbeds.fbx` (6): BridgeDryRiverbed_A_Snap_End, BridgeDryRiverbed_A_Snap_Start, BridgeDryRiverbed_B_Snap_End, BridgeDryRiverbed_B_Snap_Start, BridgeStreamBed_A_Snap_End, BridgeStreamBed_A_Snap_Start
- `BridgeTerrainCollision.fbx` (7): Collision_BridgeApproach_L (70), Collision_BridgeApproach_R (70), Collision_BridgeRavine (240), Collision_BridgeUnderTerrain (32), Collision_BridgeValleyDeep (240), Collision_BridgeValley_L (40), Collision_BridgeValley_R (40)
- `BridgeValleyTransitions.fbx` (16): BridgeValley_In_20m_Snap_End, BridgeValley_In_20m_Snap_Start, BridgeValley_In_L_40m_Snap_End, BridgeValley_In_L_40m_Snap_Start, BridgeValley_In_R_40m_Snap_End, BridgeValley_In_R_40m_Snap_Start, BridgeValley_Out_20m_Snap_End, BridgeValley_Out_20m_Snap_Start, BridgeValley_Out_L_40m_Snap_End, BridgeValley_Out_L_40m_Snap_Start, BridgeValley_Out_R_40m_Snap_End, BridgeValley_Out_R_40m_Snap_Start, BridgeValley_Run_L_40m_Snap_End, BridgeValley_Run_L_40m_Snap_Start, BridgeValley_Run_R_40m_Snap_End, BridgeValley_Run_R_40m_Snap_Start
- `BridgeValleys.fbx` (18): BridgeValley_Deep_Both_40m_Snap_End, BridgeValley_Deep_Both_40m_Snap_Start, BridgeValley_Deep_L_40m_Snap_End, BridgeValley_Deep_L_40m_Snap_Start, BridgeValley_Deep_R_40m_Snap_End, BridgeValley_Deep_R_40m_Snap_Start, BridgeValley_Medium_Both_40m_Snap_End, BridgeValley_Medium_Both_40m_Snap_Start, BridgeValley_Medium_L_40m_Snap_End, BridgeValley_Medium_L_40m_Snap_Start, BridgeValley_Medium_R_40m_Snap_End, BridgeValley_Medium_R_40m_Snap_Start, BridgeValley_Shallow_Both_40m_Snap_End, BridgeValley_Shallow_Both_40m_Snap_Start, BridgeValley_Shallow_L_40m_Snap_End, BridgeValley_Shallow_L_40m_Snap_Start, BridgeValley_Shallow_R_40m_Snap_End, BridgeValley_Shallow_R_40m_Snap_Start

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `reports/P2_bridgeTerrain_FINAL_REPORT.md`

### P2-BLENDER-01A — Bridge Valley, Embankment & Terrain Context — FINAL REPORT

Date: 2026-10-07 · Blender 5.2, Blender-only (no Unity) · Status: **COMPLETE, FROZEN**. Figures below come from `P2_bridgeTerrain_validation.txt`, `P2_bridgeTerrain_geometry.json` and the reviewed previews.

1. **Discovery:**
   - Frozen P1 seam rows sampled (`references/frozen_seam_rows.json`): Flat + TerrainTransition, identical at y 0 / −40.
   - P2 Bridges measured: Start / End overlap **8.705 m**, wing walls x ±11.3 → ±16.9, Pier_A at x ±5 on the y −20 pier line (footing −15.3 … −14.25), cap bottom −4.32, girders −2.57, Hero abutment faces x −36 / +35.
   - Details: `P2_bridgeTerrain_discovery.md`.
2. **Integrity:** **PASS.** 1,171 frozen files are byte-for-byte unchanged (P0 95, Props 77, Terrain 166, Vegetation 257, Tunnel 113, P2 Bridges 123, cars 108, other 232; 0 changed, 0 added).
3. **Reason for addendum:** P1 Terrain's deepest module (Fill_Medium, ≈ 4.9 m, to \|x\| 50) cannot carry a bridge run whose piers stand at −14.5 m. P2's QA valley was preview-only and excluded from the Bridge export. This package turns that context into reusable modules **without editing P1 Terrain or P2 Bridges**.
4. **Shallow valley:** `BridgeValley_Shallow_L / _R / _Both_40m`. A gentle swale with an asymmetric cross-fall toward −X and a meandering wash channel. Seam class S at both ends.
5. **Medium valley:** `BridgeValley_Medium_L / _R / _Both_40m`. A broad dip with a drainage channel; R side broader and deeper. Seam class V.
6. **Deep valley:** `BridgeValley_Deep_L / _R / _Both_40m`. A 9 m-wide floor at the P2 pier level (d 15–24), asymmetric banks (L steeper with rock exposure, R broader), a channel and natural toe transitions. Seam class V.
7. **Valley depths** (max below the road, context zone 13–60 m from the centreline):

   | Valley | Depth | Target |
   |---|---|---|
   | Shallow | 3.77 / 4.35 m | 2–4 |
   | Medium | 8.64 / 8.82 m | 5–9 |
   | Deep | 14.67 / 14.84 m | 10–16 |

   Under the deck the terrain is always ≤ −2.95 m, and ≤ −4.62 m at pier lines.
8. **Valley widths:**
   - Near-context modules reach **100 m** each side (2 m skirt at x ±100).
   - Valley floors: deep about 9 m flat + 30–40 m slopes; riverbed A 25 m.
   - Far ground: `BridgeValleyVista_L/R` to 700 m, for the reference crossing.
9. **In / Run / Out system:**
   - `BridgeValley_In_L/R_40m` (S → V, drainage swale), `_Run_L/R_40m` (V → V, meandering channel), `_Out_L/R_40m` (V → S), plus `BridgeValley_In_20m` / `_Out_20m`.
   - 42 composition joints validated seamless (< 1 mm), at every LOD.
10. **Bridge approaches:** `BridgeApproach_L/R` (chunk before Bridge_Deck_Start) and `BridgeApproach_Exit_L/R` (after Bridge_Deck_End).
    - At the open-road side the outer seam row equals the frozen P1 profile exactly.
    - Towards the abutment the ground falls away from the road (to −3.2 m), with an embankment crest at −0.30 to the wing tips and 1:1.7 side slopes.
    - **The road never moves.**
11. **Abutment context:**
    - **Bridge runs:** the approach modules carry the fill behind Abutment_A and the wing walls (terrain at −0.30 inside the walls, stepping down inside the 0.6 m concrete, so there is no hole and no piercing).
    - **Overpasses:** `BridgeAbutmentTerrain_L/R` builds the embankment behind the Hero seat abutments: top 8.0, 1:1.8 slopes from the return walls, sinking 0.25 m into P1 ground.
12. **8.7 m overlap handling:** in the zone ≤ 9.5 m from the abutment and \|x\| < 18 m, terrain stays ≤ −0.30 m (below the −0.15 coping), with no rock (TerrainBlend B = 0) and vegetation density 0. Validation check 11 passes, and `P2_BT_abutment_transition.png` / `_bridge_approach.png` show it.
13. **Under-bridge terrain:** `BridgeUnderTerrain_A` (24 × 10 m soil / gravel shade strip with drip-line grooves) and `_B` (16 × 8 m rock scour). Ground-conforming overlays; the valley modules also carry under-deck soil / gravel weighting and zero vegetation.
14. **Pier-ground context:** `BridgePierGround_A` (6.6 × 5.4 m compacted gravel pad) and `_B` (8.0 × 6.4 m riprap) around Pier_A columns.
    - The terrain is clamped below the cap beam.
    - Ground at the pier line in every crossing sits above the footing bottom (−15.3), so **no pier floats**. In the deep valley about 0.25 m of footing implication shows.
15. **Ravines:** `BridgeRavine_A` (3.2 m gravel channel, asymmetric rock walls about 8 m deep) and `_B` (wider, with a soil ledge). TerrainBlend rock walls, gravel base, vegetation-compatible ledges.
16. **Dry riverbeds:** `BridgeDryRiverbed_A` (25 m braided gravel floodplain with bars) and `_B` (12 m channel with point bars). Gravel / soil / rock weights; **no water, no simulation**.
17. **Optional stream bed:** `BridgeStreamBed_A`, a small channel; geometry only.
18. **TerrainBlend:** R grass, G soil, B rock, A gravel, normalised. It is the render / export colour on every mesh. Identical semantics to P1 (check 13).
19. **VegetationMask:** colour (R density, G dryness) plus UV1 `VegetationMaskUV` (U density, V dryness), identical to P1. Density is 0 under the deck, at pier lines, on beds / steep rock, in the abutment / wing zone and near the overpass return walls (check 14). Vegetation in QA was scattered from this mask.
20. **Materials:** **only the frozen P1 `MAT_Terrain_Blend`, linked read-only.** No new materials were needed; the optional MAT_BridgeTerrain_* set was not created.
21. **Textures:** **none new**. The P1 Terrain textures are reused by reference (`textures/README.txt`).
22. **UV strategy:** `UVMap` world-planar U = x/4, V = −y/4 (4 m per tile, identical to P1 `planar_uv`), continuous across modules and with P1. `VegetationMaskUV` is UV1.
23. **LODs:**
    - 34 LOD groups.
    - Valley / transition / ravine / riverbed / approach modules: LOD0–2. Abutment / patches / vistas: LOD0–1.
    - Triangle counts strictly decreasing; the lowest point stays within 0.6 m of LOD0 (the valley never flattens); seam rows are kept at every LOD.
24. **Triangle counts (LOD0 / 1 / 2):**

    | Asset | LOD0 | LOD1 | LOD2 |
    |---|---|---|---|
    | Valley side module | 5,600–6,240 | 1,520–1,680 | 352–400 |
    | Both modules | 11,840 | 3,200 | 752 (1,504 for narrow channels) |
    | Approach | 8,540–9,940 | 1,386–1,596 | 342–414 |
    | Abutment terrain | ~1,800 | ~575 | |
    | Vista | 1,056 | 288 | |
    | Patches | 256–480 | | |
25. **Collision:** 7 coarse sheets (32–240 tris, no material, none in the road volume): `Collision_BridgeValley_L/R`, `_BridgeValleyDeep`, `_BridgeUnderTerrain`, `_BridgeRavine`, `_BridgeApproach_L/R`. No road or pier colliders (P0 / P2 own them).
26. **Snap points:** 26 road-aligned modules with `_Snap_Start` (root = road centre at chunk start) / `_Snap_End`: exactly **40.000 m** (24) and **20.000 m** (2). Every LOD spans y 0 … −L (check 16). The FBX re-import confirms Unity +Z 0 … 40.000 / 20.000.
27. **Driver QA:** **PASS.** `P2_BT_driver_view.png`: from the level road on the bridge the world visibly falls away; no world holes.
28. **Chase QA:** **PASS.** `P2_BT_chase_view.png`: valley depth, abutment / wing-wall transition, distant ground.
29. **High-chase QA:** **PASS.** `P2_BT_high_chase.png`.
30. **Side-view QA:** **PASS.** `P2_BT_side_view.png` reads as road / deck → piers → valley floor with believable proportions. The bridge looks necessary.
31. **Full bridge sequence:** **PASS.** 1,120 m on the **linked** frozen P0 road with linked P2 modules:
    - Approach | Start / In | Deep | Run | End / Out | Exit;
    - a two-module shallow crossing;
    - Approach | In | Ravine_A | DryRiverbed_A | Medium | Out | Exit;
    - Overpass_Hero on normal roadside terrain with abutment embankments (its V-piers are not buried).
    - Linked P1 terrain, P1 vegetation (mask-driven), P1 guardrails into the P2 parapet transitions, hypercar.
32. **Checkpoint files:** `blend/bridgeTerrain_01_blockout` … `_06_lods_collision`, `_07_export_ready` (final source). Written once in the final pass; one earlier official set was superseded by a QA-placement fix and moved, not overwritten, to the session scratchpad.
33. **Previews:** `previews/P2_BT_{shallow_valley, medium_valley, deep_valley, valley_transition, bridge_approach, abutment_transition, underbridge, ravine, dry_riverbed, driver_view, chase_view, high_chase, side_view, bridge_full_sequence, asset_library}.png`, plus `hero_context`. 16 images.
34. **FBX files:** `exports/bridgeTerrain_complete.fbx`, `BridgeValleys.fbx` (incl. vistas), `BridgeValleyTransitions.fbx`, `BridgeApproaches.fbx` (incl. abutment terrain), `BridgeUnderTerrain.fbx`, `BridgeRavines.fbx`, `BridgeRiverbeds.fbx`, `BridgeTerrainCollision.fbx`. 8 files, 187 objects, axis-bake residual 4.8e-6.
35. **FBX re-import:** **all 8 PASS.**
    - Names, hierarchy and triangle counts match.
    - UVMap, VegetationMaskUV, TerrainBlend, VegetationMask and material preserved.
    - World deviation ≤ 5e-4 m.
    - Unity +Y up / +Z forward verified.
36. **Validation:** **31 checks, 0 errors, 0 warnings.** All 23 required checks plus the per-FBX re-import and topology checks.
37. **UnityTransfer:** `environment/P2_BridgeTerrainContext/UnityTransfer/` (FBX / Textures README / Reports / README).
38. **Import notes:** `UnityTransfer/README/BRIDGE_TERRAIN_IMPORT_NOTES.md`, covering all 21 topics.
39. **Composition guide:** `UnityTransfer/README/BRIDGE_TERRAIN_COMPOSITION_GUIDE.md`. Bridge and Terrain Context are separate runtime layers; seam-class chains; the reference crossing table.
40. **Performance guide:** `UnityTransfer/README/BRIDGE_TERRAIN_PERFORMANCE_GUIDE.md`. PC / mobile concepts, no measured numbers.
41. **Freeze report:** `reports/P2_bridgeTerrain_FINAL_FREEZE.md`, with SHA-1 hashes. `environment/P2_BridgeTerrainContext/` is **FROZEN**.
42. **Known limitations:**
    - **Both-side modules:** 11.8 k tris at LOD0, within the 2–8 k guidance per side.
    - **Aerial stripes:** drainage gravel bands run the full 100 m and read as stripes from high aerial views (fine at gameplay height).
    - **Far ground:** P1 Terrain ends at \|x\| 50 on open-road chunks, while this package reaches 100 m. Unity must supply far ground beyond that next to crossings; the QA used preview strips, and `BridgeValleyVista` covers only the reference crossing.
    - **Overpass embankments:** `BridgeAbutmentTerrain` is placed for Overpass_Hero; Standard / Wide need an X offset.
    - **Out of scope:** no water, new textures or wet preview, by design.
43. **Recommended next Blender phase:** **P2-BLENDER City** (`environment/P2_City/`, empty), or Mountain / Coastal when the roadmap calls for it. This is a recommendation only; it was not started.

---

### `UnityTransfer/README/BRIDGE_TERRAIN_IMPORT_NOTES.md`

### Bridge Terrain Context — Unity import notes (P2-BLENDER-01A)

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.** Unity-side materials, terrain placement, LODGroup components, culling, quality tiers and performance testing must be completed on the Unity workstation.

1. **Phase:** P2-BLENDER-01A, Bridge Valley, Embankment & Terrain Context Addendum. Source `environment/P2_BridgeTerrainContext/blend/bridgeTerrain_07_export_ready.blend`. All frozen phases (P0, P1 Props / Terrain / Vegetation / Tunnel, P2 Bridges, vehicles) are byte-for-byte unchanged.
2. **Scale:** 1 unit = 1 m (FBX cm + FBX_SCALE_ALL). Use Scale Factor 1 with Convert Units ON.
3. **Orientation:** Unity +Y up, +Z forward (traffic), using the same in-memory axis bake as every earlier package (Blender (x, y, z) → Unity (−x, z, −y)). In Unity, Blender L (+X) = −X.
4. **Relationship to frozen P1 Terrain:**
   - These are **additional** terrain modules with P1's data conventions and P1's material.
   - **Open-road boundary:** the approach modules' outer seam row reproduces the frozen P1 `Terrain_Flat` + `TerrainTransition` profile exactly, so P1 Flat chunks continue seamlessly.
   - **No P1 under the bridge:** do NOT also spawn P1 Flat / Transition on chunks that carry a valley or approach module; they replace them.
5. **Relationship to P2 Bridges:**
   - **Separate runtime layer:** spawn it on the same chunk transform as the P2 bridge module.
   - **No duplication:** no P2 geometry or colliders are duplicated.
   - **Clearances:** terrain stays ≤ −2.95 m under the deck (girders −2.57) and ≤ −4.62 m at the pier lines (caps −4.32).
6. **Shallow valley:** `BridgeValley_Shallow_L / _R / _Both_40m`, 3.8–4.4 m below the road, seam class S at both ends.
7. **Medium valley:** `BridgeValley_Medium_L / _R / _Both_40m`, 8.6–8.8 m, seam class V.
8. **Deep valley:** `BridgeValley_Deep_L / _R / _Both_40m`, 14.7–14.9 m. The floor matches the P2 pier base (−14.5); the asymmetric banks (L steeper, R broader) have rock exposure.
9. **Transitions:** `BridgeValley_In_L / _R_40m` (S→V), `_Run_L / _R_40m` (V→V with a meandering drainage channel), `_Out_L / _R_40m` (V→S), plus `BridgeValley_In_20m` / `_Out_20m` (both sides).
10. **Approaches:** `BridgeApproach_L / _R`, for the open-road chunk BEFORE `Bridge_Deck_Start` (abutment at the chunk end), and `BridgeApproach_Exit_L / _R`, for the chunk AFTER `Bridge_Deck_End` (abutment at the chunk start). Each covers x from the P1 TerrainTransition inner edge (L 9.9 / R −11.9) to 100 m.
11. **Abutment terrain:** `BridgeAbutmentTerrain_L / _R`, embankments behind the `Overpass_Hero` seat abutments (same origin as Overpass_Hero; use them for Standard / Wide by offsetting X to the abutment face). For bridge runs, the abutment terrain is part of `BridgeApproach_*`.
12. **Under-bridge terrain:** `BridgeUnderTerrain_A` (24 × 10 m soil / gravel shade strip) and `_B` (16 × 8 m rock scour), plus `BridgePierGround_A` (gravel pad) and `_B` (riprap) around Pier_A columns. All are optional overlays: origin = ground contact, edges sink 0.3 m.
13. **Ravines:** `BridgeRavine_A` (narrow 3.2 m erosion channel, asymmetric rock walls) and `_B` (wider, with a ledge). Both use seam class V and sit under a bridge run.
14. **Riverbeds:** `BridgeDryRiverbed_A` (25 m braided gravel floodplain) and `_B` (12 m channel with point bars), plus `BridgeStreamBed_A` (small stream channel). These are geometry only; **no water** (Unity may add it).
15. **LOD naming:** a root empty `<Asset>` with children `<Asset>_LOD0..2` (vistas, abutment and patch assets `_LOD0..1`); one LODGroup per root.
16. **TerrainBlend:** colour attribute, R grass, G soil, B rock, A gravel, normalised, identical to P1.
17. **VegetationMask:** colour (R density, G dryness) plus UV1 `VegetationMaskUV` (U density, V dryness), identical to P1. Density is 0 under the deck (\|x\| < 12.8), at pier lines, on beds / rock, and in the abutment / wing-wall overlap zone.
18. **Colliders (`BridgeTerrainCollision.fbx`):** `Collision_BridgeValley_L / _R` (Run profile), `Collision_BridgeValleyDeep`, `Collision_BridgeUnderTerrain`, `Collision_BridgeRavine`, `Collision_BridgeApproach_L / _R`. These are coarse heightfield sheets for off-road falls and the under-bridge ground; use them as non-convex MeshColliders. There are no road or pier colliders (P0 and P2 own those).
19. **Snap points:** every road-aligned module has `<Name>_Snap_Start` (root origin = road centre at the chunk start) and `_Snap_End` at (0, 0, +40.000), or (0, 0, +20.000) for the 20 m modules.
20. **Bridge Start / End 8.7 m overlap:** the approach modules keep the zone within 9.5 m of the abutment and \|x\| < 18 m clear:
    - terrain ≤ −0.30 (fill to the wing-wall coping at −0.15);
    - no rock, no vegetation, no terrain walls;
    - the wing walls sit on the fill, and the 1:1.7 embankment slope starts at the wing tips.
    - **Never place P1 Terrain / P1 Vegetation / rocks in that zone either.**
21. **Excluded QA assets:** the QA world is not exported. It contains linked P0 road, P1 terrain modules / rocks / vistas / props / vegetation, P2 bridge modules / Overpass_Hero, hypercar, QA far-ground strips, library instances, cameras and lights. `BridgeValleyVista_L/R` IS exported (reference far ground for the Approach / In / Deep / Run / Out / Exit composition).

---

### `UnityTransfer/README/BRIDGE_TERRAIN_COMPOSITION_GUIDE.md`

### Bridge terrain composition guide

**The Bridge and the Terrain Context are separate runtime layers on the same 40 m chunk transforms.** The P0 road chunk is always spawned at its normal level; nothing raises, lowers or curves it.

#### Reference deep crossing
| Chunk | Road (P0) | Bridge (P2) | Terrain context (this package) |
|---|---|---|---|
| n−1 | Road_4Lane_40m | — | P1 Terrain_Flat / Fill + TerrainTransition |
| n | Road_4Lane_40m | — (Bridge_Deck_Start wing walls overlap 8.7 m into this chunk) | `BridgeApproach_L` + `BridgeApproach_R` |
| n+1 | Road_4Lane_40m | Bridge_Deck_Start | `BridgeValley_In_L_40m` + `_In_R_40m` |
| n+2 | Road_4Lane_40m | Bridge_Deck_40m | `BridgeValley_Deep_Both_40m` (or Run / Medium / Ravine / Riverbed) |
| n+3 | Road_4Lane_40m | Bridge_Deck_40m | `BridgeValley_Run_L_40m` + `_Run_R_40m` |
| n+4 | Road_4Lane_40m | Bridge_Deck_End | `BridgeValley_Out_L_40m` + `_Out_R_40m` |
| n+5 | Road_4Lane_40m | — (Bridge_Deck_End overlaps 8.7 m) | `BridgeApproach_Exit_L` + `_Exit_R` |
| n+6 | Road_4Lane_40m | — | P1 Terrain_Flat / Fill + TerrainTransition |

Optional: `BridgeValleyVista_L/R` at chunk n+1's origin for the distant ground; vegetation from VegetationMaskUV; `BridgePierGround_A` at each pier column, `BridgeUnderTerrain_A/B` under the deck.

#### Seam classes (any chain that matches classes is seamless)
| Class | Profile |
|---|---|
| **P** | the frozen P1 Flat / Transition profile |
| **S** | shallow, −3.2 m |
| **V** | valley, −6.5 m |

| Module | Start → End |
|---|---|
| Approach (P→S, abutment end) | P → S |
| Exit approach (S at abutment → P) | S → P |
| In_L / R, In_20m | S → V |
| Out_L / R, Out_20m | V → S |
| Run, Medium, Deep, Ravine_A / B, DryRiverbed_A / B, StreamBed_A | V → V |
| Shallow | S → S |

**Examples:**
- **Short shallow crossing:** P1 | Approach | (Start) Shallow | (End) Shallow | Exit approach | P1. That is a 2-module bridge (Bridge_Deck_Start + Bridge_Deck_End).
- **Medium valley:** Approach | In | Medium | Run | Out | Exit.
- **Ravine crossing:** Approach | In | Ravine_A | Out | Exit.
- **Dry riverbed:** Approach | In | DryRiverbed_A | DryRiverbed_B | Out | Exit.
- **20 m granularity:** In_20m / Out_20m pair with P2 Bridge_Deck_20m.

#### Rules
- **L / R:** use either one Both module or the L + R pair on a chunk, never both.
- **Overpasses (`Overpass_Hero` / `_Standard` / `_Wide`):** use normal roadside terrain (P1 Flat / Cut), not valleys. Add `BridgeAbutmentTerrain_L/R` behind the overpass abutments.
- **8.7 m overlap:** keep P1 rocks, props and vegetation out of the approach modules' wing zone (≤ 9.5 m from the abutment, \|x\| < 18 m).
- **Bridge-chunk placement:** do not spawn P1 TerrainTransition on bridge chunks. The bridge parapet / drain occupy that strip, and the valley modules supply the ground below.

---

### `UnityTransfer/README/BRIDGE_TERRAIN_PERFORMANCE_GUIDE.md`

### Bridge terrain performance guide (concepts only — no Unity measurements were taken)

#### Triangle reference (LOD0 / LOD1 / LOD2)
| Asset | LOD0 | LOD1 | LOD2 |
|---|---|---|---|
| Valley side module (L or R) | 5,600–6,240 | 1,520–1,680 | 352–400 |
| Both modules (two sides) | 11,840 | 3,200 | 752 (narrow-channel modules 1,504) |
| Approach | 8,540–9,940 | 1,386–1,596 | 342–414 |
| Abutment terrain | ~1,800 | ~575 | |
| Vista | 1,056 | 288 | |
| Patches | 256–480 | 36–80 | |
| Colliders | 32–240 | | |

#### PC
- Keep LOD0 within about 80 m, LOD1 to about 250 m, LOD2 beyond.
- Show the valley vistas to their full 700 m.
- Keep the under-bridge patches, pier pads, and rock / erosion detail (TerrainBlend B, riprap patches).
- Allow dense VegetationMask-driven scatter on the slopes.

#### Mobile
- Use earlier terrain LOD switches (about 0.5× the PC distances).
- Simplify the under-bridge ground: skip BridgeUnderTerrain / PierGround patches, because TerrainBlend already carries soil / gravel.
- Reduce or remove the far vista (use LOD1 only, or a fog / skybox horizon).
- Cut vegetation density from the mask by tier.
- Use only the coarse collider sheets.

#### General
- Modules are static and share one material (P1 MAT_Terrain_Blend), so batching is effective.
- Long valleys repeat Run / Medium modules; the asymmetric L / R variants and the alternating ravine / riverbed modules break up repetition without extra cost.

---

### `reports/P2_bridgeTerrain_materials_masks.md`

### P2-BLENDER-01A — materials, masks and exclusion zones

#### Materials
- **Reused:** `MAT_Terrain_Blend` from `P1_Terrain/blend/terrain_09_final_frozen.blend`, **linked read-only** (the material and its textures are not copied, re-authored or modified). The FBX references it by name; in Unity, assign the existing P1 terrain material.
- **New materials:** none. The optional `MAT_BridgeTerrain_*` set was **not needed**, because the grass / soil / rock / gravel / dry-ground looks come from the TerrainBlend weights that MAT_Terrain_Blend already blends.
- **Texture sources:** P1 Terrain textures (Grass, Soil, Rock, Gravel, …), unchanged. **No new textures** (`textures/README.txt`).

#### UV scale
- `UVMap`: world-planar, **U = x / 4, V = −y / 4 (4 m per tile)**, identical to P1 `planar_uv`. Modules tile continuously with each other and with P1 Terrain; no 0–1 stretching.
- `VegetationMaskUV` (UV1): U density, V dryness.

#### TerrainBlend (colour attribute, point domain, the render / export colour)
| Channel | Meaning | Where it is strong |
|---|---|---|
| R grass | | stable slopes, shoulders, valley flats |
| G soil | | steep soil slopes, erosion noise, under-deck shade strip, abutment fill / wing zones |
| B rock | | slopes steeper than ~35°, ravine walls, deep-valley bank exposure, BridgePierGround_B / BridgeUnderTerrain_B riprap |
| A gravel | | channel / riverbed / stream beds, pier pads, scattered under-deck gravel, approach fill |

Weights are clamped and normalised (sum = 1, checked).

#### VegetationMask (colour) + VegetationMaskUV (UV1)
Same semantics as P1: R / U = density 0–1, G / V = dryness 0–1.
- **High density:** broad grass slopes, valley shoulders, stable flats.
- **Reduced:** soil, steep or dry slopes.
- **Dryness:** rises with steepness, soil, gravel and shade; falls near valley bottoms.

#### Bridge exclusion zones (density forced to 0)
| Zone | Rule |
|---|---|
| Under the deck / girders / parapet fascia | \|x\| < 12.8 m in every valley / ravine / riverbed module |
| Pier lines | y = −L/2 ± 2 m (P2 Pier_A + CapBeam_A); BridgePierGround_A / B pads are gravel / rock |
| Drainage outlets, channels, riverbed / ravine beds | bed weight |
| Steep rock (B > 0.55) and gravel beds (A > 0.8) | |
| Abutment fill, wing-wall zone and crest | approach modules, ≤ 9.5 m from the abutment, \|x\| < 18 m (covers the 8.7 m overlap) |
| Overpass abutment embankment | within 2.5–4 m of the return walls |

---

### `reports/P2_bridgeTerrain_FINAL_FREEZE.md`

### P2_BridgeTerrainContext — FINAL FREEZE

Date: 2026-10-07 · Phase P2-BLENDER-01A · Status: **FROZEN**. Nothing under `environment/P2_BridgeTerrainContext/` is to be edited; later phases may only link from it read-only.

#### Final deliverables
- **Final source blend:** `blend/bridgeTerrain_07_export_ready.blend` (checkpoints `bridgeTerrain_01_blockout` … `_06_lods_collision` kept unchanged).
- **FBX (`exports/`, identical in `UnityTransfer/FBX/`):** `BridgeApproaches.fbx`, `BridgeRavines.fbx`, `BridgeRiverbeds.fbx`, `BridgeTerrainCollision.fbx`, `BridgeUnderTerrain.fbx`, `BridgeValleyTransitions.fbx`, `BridgeValleys.fbx`, `bridgeTerrain_complete.fbx`
- **Textures:** none new (frozen P1 `MAT_Terrain_Blend` + P1 textures reused by reference; `textures/README.txt`).
- **Reports:** `reports/P2_bridgeTerrain_discovery.md`, `_materials_masks.md`, `_validation.txt`, `_geometry.json`, `_export_manifest.json`, `_source_baseline.json`, `_source_integrity_check.md`, `_qa_sequence.json`, `_FINAL_REPORT.md`; `references/frozen_seam_rows.json`.
- **Previews:** 16 images in `previews/`.
- **UnityTransfer:** `UnityTransfer/` (FBX, Textures/README, Reports, README: `BRIDGE_TERRAIN_IMPORT_NOTES.md`, `BRIDGE_TERRAIN_COMPOSITION_GUIDE.md`, `BRIDGE_TERRAIN_PERFORMANCE_GUIDE.md`).

#### Validation result
`reports/P2_bridgeTerrain_validation.txt`: **SUMMARY: 0 errors, 0 warnings**.
Source integrity: **PASS** (`reports/P2_bridgeTerrain_source_integrity_check.md`).

#### Known limitations
- Both-side valley modules are 11.8 k tris at LOD0 (5.6–6.2 k per side, inside the 2–8 k per-side guidance).
- Drainage-channel gravel bands extend across the full 100 m module width and read as stripes from high aerial views (fine at gameplay height).
- Deep-valley floor (-14.2 … -14.8) leaves up to ~0.25 m of the P2 Pier_A footing implication visible: intended (not floating).
- The P1 Terrain ends at |x| 50 m on open-road chunks; this package reaches 100 m on bridge / approach chunks, so open-road chunks next to a crossing still need Unity-side far ground (the QA scene used preview strips; BridgeValleyVista covers the reference crossing only).
- BridgeAbutmentTerrain is authored for Overpass_Hero abutment positions; Standard / Wide need an X offset to their abutment faces.
- No water, no new textures, no wet preview (by design).

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P2_bridgeTerrain_validation.txt`

```text
== P2-BLENDER-01A BRIDGE TERRAIN CONTEXT - VALIDATION ==
source blend/bridgeTerrain_07_export_ready.blend; BRIDGE_TERRAIN_MASTER 187 objects, 101 meshes (94 renderable, 7 colliders)

[PASS]  1. frozen source integrity: P0, P1 Props, P1 Terrain, P1 Vegetation, P1 Tunnel, P2 Bridges, vehicles and all other workspace files byte-identical to the pre-phase baseline
[PASS]  2. shallow valley: BridgeValley_Shallow_L / _R / _Both_40m exist (LOD0-2); depth below road 2-4.5 m (max depth in the valley context zone 13-60 m from the centreline)
[PASS]  3. medium valley: BridgeValley_Medium_L / _R / _Both_40m exist (LOD0-2); depth below road 5-9.5 m (max depth in the valley context zone 13-60 m from the centreline)
[PASS]  4. deep valley: BridgeValley_Deep_L / _R / _Both_40m exist (LOD0-2); depth below road 10-16.5 m (max depth in the valley context zone 13-60 m from the centreline)
[PASS]  5. In / Run / Out system: BridgeValley_In / _Run / _Out L / R 40 m + In / Out 20 m exist (LOD0-2)
[PASS]  6. approach context: BridgeApproach_L / _R (+ _Exit_L / _R) exist; start row matches the frozen P1 Terrain_Flat + TerrainTransition seam profile
[PASS]  7. abutment transition: BridgeAbutmentTerrain_L / _R exist (overpass abutment embankments)
[PASS]  8. under-bridge terrain: BridgeUnderTerrain_A / _B + BridgePierGround_A / _B exist
[PASS]  9. ravine: BridgeRavine_A / _B exist (LOD0-2)
[PASS] 10. dry riverbed: BridgeDryRiverbed_A / _B (+ optional BridgeStreamBed_A, geometry only, no water) exist (LOD0-2)
[PASS] 11. Bridge Start / End 8.7 m overlap respected: in the approach-module zone the P2 wing walls / parapet transitions occupy (<= 9.5 m from the abutment, |x| < 18 m): terrain never rises above -0.30 m (wing-wall coping -0.15), no rock (TerrainBlend B < 0.3), vegetation density 0
[PASS] 12. road stays straight and level: QA uses the LINKED frozen P0 road at z 0, x 1000, no rotation, contiguous 40 m chunks; no terrain-context vertex above -0.289 m (the frozen P1 TerrainTransition level) inside the road corridor |x| < 10.7 (terrain never touches / lifts the road)
[PASS] 13. TerrainBlend compatible: colour attribute TerrainBlend (R grass, G soil, B rock, A gravel) on every mesh, normalised (sum 1, 0..1), render / export colour
[PASS] 14. VegetationMask compatible: VegetationMask colour (R density, G dryness) + UV1 VegetationMaskUV (U density, V dryness) identical; density 0 under the deck (|x| < 12.8), at pier lines, on rock (B > .55) and bed gravel (A > .8)
[PASS] 15. seam safety: 42 documented composition joints (Approach / In / Run / Medium / Deep / Ravine / Riverbed / Stream / Shallow / Out / Exit / 20 m) have identical boundary rows (< 1 mm) on every shared column; first / last 2 m use the controlled seam class profile; LOD1 / LOD2 boundary rows equal LOD0
[PASS] 16. snap distances: Snap_Start (root origin) -> Snap_End exactly 40.000 m (24 modules) / 20.000 m (2); every LOD spans exactly y 0 .. -L
[PASS] 17. LODs: 34 LOD groups, triangle counts strictly decreasing; valley depth preserved at every LOD (lowest point within 0.6 m of LOD0)
[PASS] 18. colliders: simple terrain sheets (< 300 tris, no material), substantially simpler than the visuals, none inside the road volume; no bridge / pier colliders duplicated (P2 owns them)
[PASS] 19. UVs: UVMap = world-planar (U = x / 4, V = -y / 4: 4 m per tile, identical to P1 Terrain planar_uv) on every mesh, so modules tile continuously with P1 and each other; no 0-1 stretch
[PASS] 20. materials: every terrain mesh uses only the frozen P1 material MAT_Terrain_Blend (linked read-only, not re-authored; drives TerrainBlend); colliders have no material
[PASS] 21. QA bridge sequence: 1120 m on the LINKED frozen P0 road with LINKED P2 ['Bridge_Deck_40m_LOD0', 'Bridge_Deck_End_LOD0', 'Bridge_Deck_Start_LOD0', 'Overpass_Hero_LOD0']: Approach | In | Deep | Run | Out | Exit, Shallow crossing, In | Ravine | Riverbed | Medium | Out, Overpass_Hero with abutment terrain; piers never ...
[PASS] 22. FBX export: 8 files written; export selection == BRIDGE_TERRAIN_MASTER; no P0 / P1 / P2 Bridges / vehicle objects or meshes, no QA / camera / light / helper objects; only the P1 material NAME is referenced
[PASS] 23. normals / topology: no zero-area faces, no downward-facing heightfield faces, smooth shading (no faceted grid)
[PASS] 24. FBX re-import BridgeValleys.fbx: 60 objects, names + hierarchy match, world deviation 4.9e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved; Unity +Y up / +Z forward (FBX mesh space): {"BridgeValley_Deep_Both_40m": {"up_Y": [-14.94, -4.7], "forward_Z": [0.0, 40.0]}}
[PASS] 25. FBX re-import BridgeValleyTransitions.fbx: 48 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved; Unity +Y up / +Z forward (FBX mesh space): {"BridgeValley_In_20m": {"up_Y": [-9.42, -2.0], "forward_Z": [0.0, 20.0]}}
[PASS] 26. FBX re-import BridgeApproaches.fbx: 30 objects, names + hierarchy match, world deviation 4.5e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved
[PASS] 27. FBX re-import BridgeUnderTerrain.fbx: 12 objects, names + hierarchy match, world deviation 4.6e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved
[PASS] 28. FBX re-import BridgeRavines.fbx: 12 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved
[PASS] 29. FBX re-import BridgeRiverbeds.fbx: 18 objects, names + hierarchy match, world deviation 3.5e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved
[PASS] 30. FBX re-import BridgeTerrainCollision.fbx: 7 objects, names + hierarchy match, world deviation 4.5e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved
[PASS] 31. FBX re-import bridgeTerrain_complete.fbx: 187 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / material preserved; Unity +Y up / +Z forward (FBX mesh space): {"BridgeValley_Deep_Both_40m": {"up_Y": [-14.94, -4.7], "forward_Z": [0.0, ...

Triangle budgets are guidance only; below-budget assets are not reported as warnings.
SUMMARY: 0 errors, 0 warnings
```

