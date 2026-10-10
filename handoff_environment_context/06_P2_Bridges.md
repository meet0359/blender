# P2-BLENDER-01 — Premium Modular Bridges & Overpasses

Digest 06 of the environment handoff. Folder: `environment/P2_Bridges/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/bridges_07_export_ready.blend`
- **Asset index source:** `reports/P2_bridges_geometry.json` + `reports/P2_bridges_export_manifest.json`
- **Checkpoints (7):** `bridges_01_blockout.blend`, `bridges_02_overpass.blend`, `bridges_03_bridge_deck.blend`, `bridges_04_structures.blend`, `bridges_05_materials_uv.blend`, `bridges_06_lods_collision.blend`, `bridges_07_export_ready.blend`
- **FBX (9):** `Overpasses.fbx` (40 objects), `BridgeDecks.fbx` (42 objects), `Piers_Abutments.fbx` (27 objects), `Underpass.fbx` (34 objects), `BridgeBarriers.fbx` (28 objects), `BridgeDrainage.fbx` (12 objects), `BridgeFixtures.fbx` (27 objects), `BridgeCollision.fbx` (14 objects), `bridges_complete.fbx` (224 objects)
- **Textures:** 21 PNG files · **Previews:** 21 renders · **UnityTransfer README:** `BRIDGES_IMPORT_NOTES.md`, `BRIDGES_PERFORMANCE_GUIDE.md`, `BRIDGES_STREAMING_GUIDE.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `Bridge_Abutment_A` | 408 / 24 | Piers_Abutments.fbx |
| `Bridge_Abutment_B` | 60 / 24 | Piers_Abutments.fbx |
| `Bridge_Bearing_A` | 60 / 36 | BridgeBarriers.fbx |
| `Bridge_Bearing_B` | 164 / 52 | BridgeBarriers.fbx |
| `Bridge_CapBeam_A` | 104 / 36 | Piers_Abutments.fbx |
| `Bridge_CapBeam_B` | 56 / 12 | Piers_Abutments.fbx |
| `Bridge_DeckDrain_4m` | 174 / 12 | BridgeDrainage.fbx |
| `Bridge_DeckDrain_8m` | 334 / 24 | BridgeDrainage.fbx |
| `Bridge_Deck_20m` | 3,794 / 1,456 / 640 | BridgeDecks.fbx |
| `Bridge_Deck_40m` | 6,942 / 2,532 / 1,208 | BridgeDecks.fbx |
| `Bridge_Deck_End` | 7,698 / 2,656 / 1,332 | BridgeDecks.fbx |
| `Bridge_Deck_Start` | 7,698 / 2,656 / 1,332 | BridgeDecks.fbx |
| `Bridge_Downpipe_A` | 168 / 40 | BridgeDrainage.fbx |
| `Bridge_Drain_A` | 92 / 32 | BridgeDrainage.fbx |
| `Bridge_ExpansionJoint_A` | 36 / 12 | BridgeBarriers.fbx |
| `Bridge_LightPoleMount` | 104 / 24 | BridgeFixtures.fbx |
| `Bridge_NoiseBarrier_4m` | 90 / 30 | BridgeBarriers.fbx |
| `Bridge_NoiseBarrier_8m` | 166 / 58 | BridgeBarriers.fbx |
| `Bridge_NoiseBarrier_End` | 54 / 30 | BridgeBarriers.fbx |
| `Bridge_Parapet_Concrete` | 374 / 128 | BridgeBarriers.fbx |
| `Bridge_Parapet_Metal` | 240 / 108 | BridgeBarriers.fbx |
| `Bridge_Parapet_Transition` | 108 / 32 | BridgeBarriers.fbx |
| `Bridge_Pier_A` | 104 / 12 | Piers_Abutments.fbx |
| `Bridge_Pier_B` | 152 / 36 | Piers_Abutments.fbx |
| `Bridge_Pier_Wide` | 168 / 36 | Piers_Abutments.fbx |
| `Bridge_ServiceLightFixture` | 48 / 32 | BridgeFixtures.fbx |
| `Bridge_SignMount` | 96 / 48 | BridgeFixtures.fbx |
| `Bridge_UnderdeckLightFixture` | 74 / 14 | BridgeFixtures.fbx |
| `Bridge_VMS_Mount` | 84 / 72 | BridgeFixtures.fbx |
| `Bridge_WingWall_L` | 48 / 12 | Piers_Abutments.fbx |
| `Bridge_WingWall_R` | 48 / 12 | Piers_Abutments.fbx |
| `Overpass_Hero` | 6,688 / 3,504 / 1,744 / 1,492 | Overpasses.fbx |
| `Overpass_SignFrame` | 96 / 48 | BridgeFixtures.fbx |
| `Overpass_Standard` | 3,924 / 1,328 / 600 | Overpasses.fbx |
| `Overpass_UnderlightFixture` | 38 / 14 | BridgeFixtures.fbx |
| `Overpass_Wide` | 5,300 / 2,788 / 1,272 | Overpasses.fbx |
| `Underpass_20m` | 2,344 / 368 / 168 | Underpass.fbx |
| `Underpass_40m` | 3,680 / 592 / 312 | Underpass.fbx |
| `Underpass_Ceiling` | 1,804 / 140 | Underpass.fbx |
| `Underpass_EndTrim` | 96 / 16 | Underpass.fbx |
| `Underpass_Wall_L` | 328 / 100 | Underpass.fbx |
| `Underpass_Wall_R` | 328 / 100 | Underpass.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `BridgeBarriers.fbx` (1): Bridge_ExpansionJoint_B (36)
- `BridgeCollision.fbx` (14): Collision_Abutment (36), Collision_Abutment_End (36), Collision_Bridge_Parapet_L (12), Collision_Bridge_Parapet_L_20m (12), Collision_Bridge_Parapet_R (12), Collision_Bridge_Parapet_R_20m (12), Collision_Bridge_Pier (36), Collision_Overpass_Pier (72), Collision_Overpass_Pier_Hero (48), Collision_Overpass_Pier_Wide (24), Collision_UnderpassWall_L (12), Collision_UnderpassWall_L_20m (12), Collision_UnderpassWall_R (12), Collision_UnderpassWall_R_20m (12)
- `BridgeDecks.fbx` (26): Bridge_Deck_20m_DeckBottom, Bridge_Deck_20m_DeckTop, Bridge_Deck_20m_PierCenter, Bridge_Deck_20m_RoadCenter, Bridge_Deck_20m_Snap_End, Bridge_Deck_20m_Snap_Start, Bridge_Deck_40m_DeckBottom, Bridge_Deck_40m_DeckTop, Bridge_Deck_40m_PierCenter, Bridge_Deck_40m_RoadCenter, Bridge_Deck_40m_Snap_End, Bridge_Deck_40m_Snap_Start, Bridge_Deck_End_AbutmentFace, Bridge_Deck_End_DeckBottom, Bridge_Deck_End_DeckTop, Bridge_Deck_End_PierCenter, Bridge_Deck_End_RoadCenter, Bridge_Deck_End_Snap_End, Bridge_Deck_End_Snap_Start, Bridge_Deck_Start_AbutmentFace, Bridge_Deck_Start_DeckBottom, Bridge_Deck_Start_DeckTop, Bridge_Deck_Start_PierCenter, Bridge_Deck_Start_RoadCenter, Bridge_Deck_Start_Snap_End, Bridge_Deck_Start_Snap_Start
- `BridgeFixtures.fbx` (6): Bridge_ConcreteStain_A (2), Bridge_DirtEdge_A (2), Bridge_RepairPatch_A (2), Bridge_Runoff_A (2), Bridge_Runoff_B (2), Bridge_RustStreak_A (2)
- `Overpasses.fbx` (27): Overpass_Hero_AbutmentFace, Overpass_Hero_ClearanceBottom, Overpass_Hero_DeckBottom, Overpass_Hero_DeckTop, Overpass_Hero_OverpassCenter, Overpass_Hero_PierCenter, Overpass_Hero_Pier_L, Overpass_Hero_Pier_R, Overpass_Hero_RoadCenter, Overpass_Standard_AbutmentFace, Overpass_Standard_ClearanceBottom, Overpass_Standard_DeckBottom, Overpass_Standard_DeckTop, Overpass_Standard_OverpassCenter, Overpass_Standard_PierCenter, Overpass_Standard_Pier_L, Overpass_Standard_Pier_R, Overpass_Standard_RoadCenter, Overpass_Wide_AbutmentFace, Overpass_Wide_ClearanceBottom, Overpass_Wide_DeckBottom, Overpass_Wide_DeckTop, Overpass_Wide_OverpassCenter, Overpass_Wide_PierCenter, Overpass_Wide_Pier_L, Overpass_Wide_Pier_R, Overpass_Wide_RoadCenter
- `Underpass.fbx` (14): Underpass_20m_ClearanceBottom, Underpass_20m_DeckTop, Underpass_20m_RoadCenter, Underpass_20m_Snap_End, Underpass_20m_Snap_Start, Underpass_20m_WallInner_L, Underpass_20m_WallInner_R, Underpass_40m_ClearanceBottom, Underpass_40m_DeckTop, Underpass_40m_RoadCenter, Underpass_40m_Snap_End, Underpass_40m_Snap_Start, Underpass_40m_WallInner_L, Underpass_40m_WallInner_R

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `reports/P2_bridges_FINAL_REPORT.md`

### P2-BLENDER-01 — Premium Modular Bridges & Overpasses — FINAL REPORT

Date: 2026-10-07 · Blender 5.2, Blender-only (Unity untouched) · Status: **COMPLETE, FROZEN**. All figures below come from `reports/P2_bridges_validation.txt`, `P2_bridges_geometry.json` and the reviewed previews.

1. **Discovery findings:**
   - P0 carriageway 14.4 m, road kit 15.4 m; shoulders to x −10.2 / +8.7; drain corridor −10.2 … −10.7; median strip 8.7 … 10.7 with the barrier at 9.7. Road corridor 21.4 m.
   - P1 guardrail at −11.0, streetlights at −12.0, signs at −12.8, gantry supports −13 … −11.8, gantry sign bottom 6.0 m.
   - Terrain modules from \|x\| 16 m.
   - Hypercar 1.55 m tall; chase camera 2.4 m, high chase 5.3–5.5 m.
   - Tunnel language: warm-grey concrete, 512 px/m.
   - Details: `P2_bridges_discovery.md`.
2. **Source integrity:**
   - **PASS.** 1,048 frozen files are byte-for-byte unchanged: P0 95, Props 77, Terrain 166, Vegetation 257, Tunnel 113, cars 108, other 232. 0 changed, 0 added.
   - Evidence: validation check 1 and `P2_bridges_source_integrity_check.md`.
3. **Chosen design language:** modern highway civil infrastructure.
   - Cast-in-place warm-grey concrete for the substructure and decks.
   - Precast I-girders and bulb-tees, a concrete box and painted steel box girders: one coherent system per structure, never randomly mixed.
   - Galvanised rails and mounts; elastomeric and pot bearings.
   - No sci-fi or decorative forms.
4. **Hero Overpass (`Overpass_Hero`):**
   - **Girders:** twin painted-steel trapezoidal box girders haunched from 1.6 m (over the lanes) to 2.85 m (at the piers), giving a distinctive arched soffit.
   - **Steelwork:** steel cross-girders every 4 m, a painted feature fascia with an underlight strip.
   - **Supports:** inclined concrete V-piers on pier heads with pot bearings; seat abutments with return walls.
   - **Deck furniture:** metal parapets, light-pole mounts. A sign frame + P1 SignPanel_Medium is shown in QA.
5. **Hero dimensions:**
   - Overall 83 × 17 × 10.6 m.
   - Deck 15 m wide.
   - Spans: main 33.5 m, sides 18.5 / 19 m.
   - Deck top 8.23 m, parapet top 9.4 m.
   - Soffit 6.35 m at the centre line, **6.18 m minimum over the road kit**.
   - LOD0 6,688 tris.
6. **50 / 100 / 200 / 300 m landmark QA:** **PASS.**
   - At 300 m the haunched-girder silhouette and V-piers still separate the Hero clearly from the flat Standard / Wide decks beyond.
   - Previews: `P2_bridge_overpass_{50,100,200,300}m.png`, all at driver height.
7. **Standard Overpass:** 12 m deck, 5 precast I-girders + diaphragms, twin round columns (Pier_B) on rectangular caps (CapBeam_B), concrete parapets. 6.0 m soffit; 62 m long. 3,924 / 1,328 / 600 tris.
8. **Wide Overpass:** 18 m deck, 3-cell concrete box girder with ribbed cantilevers, wall piers (Pier_Wide), metal parapets + 3 m glass noise barriers. 6.0 m soffit (5.96 m at the shadow-joint strips); 67 m long. 5,300 / 2,788 / 1,272 tris. Not a scaled copy of Standard.
9. **Clearance:**
   - Lowest structure over the whole road kit (x −10.2 … 8.7) across every LOD: **5.96 m** (Wide soffit strips).

     | Structure | Lowest point |
     |---|---|
     | Hero | 6.18 m |
     | Standard | 6.0 m |
     | Underpass | 6.0 m |
     | Sign frame | 6.4 m |
     | VMS mount | 6.5 m |

   - Target ≥ 5.5 m: **PASS** (check 6).
   - Hypercar clearance checked in `P2_bridge_driver_approach.png` and `_chase_underpass.png`.
10. **Support placement:** **no central pier.** The 2 m median strip is unsafe for one.
    - Overpass piers sit at x −17 … −18.5 / +15 … +16.5, beyond the P1 guardrail / light / sign zone.
    - Underpass walls sit at −12.8 / +11.6.
    - Nothing below 5.5 m inside x −12.2 … 11.2: **PASS** (check 7).
11. **Bridge 40 m module:** `Bridge_Deck_40m`.
    - Under the level P0 road: 0.25 m slab (top −0.32), 6 × 2.0 m bulb-tee girders, diaphragms every 10 m, a mid pier line (2 × Pier_A + hammerhead CapBeam_A + 6 bearings) to the −14.5 m valley floor.
    - At road level: parapets + edge beams, deck slot drains, scuppers, downpipe.
    - Snap 40.000 m. 6,942 / 2,532 / 1,208 tris.
12. **Bridge 20 m module:** `Bridge_Deck_20m`, same system with the pier line at −10. Snap 20.000 m. 3,794 / 1,456 / 640 tris.
13. **Start / End modules:**
    - **`Bridge_Deck_Start`:** abutment A (stem, seat, backwall, footing) at the snap, 30°-splayed stepped wing walls (top −0.30 = the P0 skirt / P1 TerrainTransition level), parapet transitions to the P1 guardrail, a finger expansion joint, plus the first span.
    - **`Bridge_Deck_End`:** the mirror.
    - 7,698 / 2,656 / 1,332 tris each.
14. **Deck structural system:** one system per structure.

    | Structure | System |
    |---|---|
    | Bridge run | precast bulb-tee girders + cast slab |
    | Standard | precast I-girders |
    | Wide | concrete box |
    | Hero | steel twin box + concrete slab |
15. **Underside structure:** readable girders, boxes, cross-girders and diaphragms with real depth (≥ 1.75 m) and 340–660 structural faces per structure. Check 17 passes, and `P2_bridge_understructure.png` and `_piers.png` show the girder rhythm from below.
16. **Pier system:** `Bridge_Pier_A` (chamfered tapered rectangle, 11 m), `_B` (round column + collar), `_Wide` (rounded wall pier 9 × 1.4 m). Footing implications are shallow (0.8 m) and widened at the base.
17. **Cap beams:** `Bridge_CapBeam_A` (hammerhead 21.6 m with tapered cantilevers) and `_B` (rectangular 11 m). Both visibly carry the girders through bearings.
18. **Abutments:** `Bridge_Abutment_A` (bridge run: stem / seat / backwall / footing / drip edge / bearings) and `_B` (overpass seat type with wing returns). Small engineering detail is in the textures.
19. **Wing walls:** `Bridge_WingWall_L/R`, 30° splay, stepped bottom (−14.5 → −5 m), coping. They connect to P1 Terrain_Fill / TerrainTransition without terrain edits (`P2_bridge_start_end.png`).
20. **Underpass:**
    - **Module:** `Underpass_40m` / `_20m`: a 20 m covered heavy deck (slab 7.0–7.6, transverse beams every 2 m, soffit 6.0) on retaining walls that drop to 3 m at both ends. End trims carry ID + clearance plates; underdeck lights and downpipes are included.
    - **Kit:** `Underpass_Wall_L/R`, `_Ceiling`, `_EndTrim`.
    - **Openness:** daylight at both ends, so it is not a tunnel (`P2_bridge_driver_underpass.png`, `_chase_underpass.png`).
21. **Parapets / barriers:** `Bridge_Parapet_Concrete` (single-slope + fascia), `_Metal` (kerb + posts + 3 rails), `_Transition` (ends at the anchor plate for the frozen P1 `Guardrail_To_Concrete_Transition` at x −11.0), `Bridge_NoiseBarrier_4m / _8m / _End` (single-layer acrylic).
22. **Expansion joints:** `Bridge_ExpansionJoint_A` (modular finger) and `_B` (strip seal). Visual only, 4 mm above the road, no collider. Used only at the Start / End abutments.
23. **Bearings:** `Bridge_Bearing_A` (laminated elastomeric) and `_B` (pot), simple geometry. Used on caps, abutments, the Standard overpass and Hero pier heads.
24. **Drainage:**
    - `Bridge_DeckDrain_4m` / `_8m` (LOD0 bars 174 / 334 tris → LOD1 textured plate 12 / 24), `Bridge_Drain_A` (fascia scupper), `Bridge_Downpipe_A`.
    - Placed at deck edges, abutment runoff and pier lines.
25. **Lights / sign supports:**
    - Lights: `Bridge_LightPoleMount` (for the P1 streetlight), `Bridge_UnderdeckLightFixture`, `Overpass_UnderlightFixture`, `Bridge_ServiceLightFixture`.
    - Signs: `Bridge_SignMount`, `Overpass_SignFrame`, `Bridge_VMS_Mount`. The P1 panels are reused in QA, not recreated.
    - Emission is preview only.
26. **Material list (11):** `MAT_Bridge_Concrete`, `_Concrete_Dark`, `_Steel`, `_Galvanized`, `_PaintedMetal`, `_Rubber`, `_Glass`, `_Drain`, `_SignSupport`, `_Light`, `_Decal`.
27. **Trim sheet:** `T_Bridge_Trim_2K` (BaseColor / Normal / Roughness / Metallic / AO) with 10 strips: clean concrete edge, weathered concrete, galvanised, painted steel, dark structural steel, rubber, joint surface, drain metal, utility metal, barrier detail. 4 m per U tile.
28. **Concrete texture:** `T_Bridge_Concrete_2K` (BaseColor / Normal / Roughness / AO). Tileable, 4 m per tile (512 px/m), warm grey with faint tie holes / board joints. It matches the P1 Tunnel / Terrain density and tone; no upstream texture was copied.
    - Also: `T_Bridge_Steel_2K` painted steel, `T_Bridge_Glass_1K`, `T_Bridge_Signs_1K`, `T_Bridge_Decals_2K`.
29. **UV strategy:**
    - Concrete and steel: world-scale box projection at 4 m. A 40 m deck spans 10+ tiles; check 25 confirms no 0–1 stretch.
    - Trim faces: inside one strip.
    - Glass: one 0–1 tile per panel.
    - Signs and decals: inside their atlas rects.
30. **Weathering / decal strategy:**
    - Decals `Bridge_Runoff_A/B`, `_RustStreak_A`, `_ConcreteStain_A`, `_DirtEdge_A`, `_RepairPatch_A`, placed logically (under joints / seats / bearings, wall bases, underpass deck edge).
    - The weathered trim strip on fascias / parapets.
    - No heavy baked damage.
31. **LOD strategy:**
    - **Hero:** LOD0–3.
    - **Overpasses / bridge / underpass modules:** LOD0–2.
    - **Kit pieces:** LOD0–1.
    - **No LOD:** decals and the strip seal.
    - Deck depth, girder count, pier and parapet silhouettes are kept; bearings, brackets, coping, grate bars and underlights are dropped.
    - 42 LOD groups, all strictly decreasing.
32. **Triangle counts (LOD0):**

    | Asset | Tris |
    |---|---|
    | Hero | 6,688 |
    | Wide | 5,300 |
    | Standard | 3,924 |
    | Bridge 40 m | 6,942 |
    | Bridge 20 m | 3,794 |
    | Start / End | 7,698 |
    | Underpass 40 m | 3,680 |
    | Piers | 104–168 |
    | Abutment A | 408 |
    | Parapet Concrete 40 m | 374 |
    | Noise barrier 8 m | 166 |

    Full list: `P2_bridges_geometry.json`.
33. **Collider strategy:** 14 closed boxes / hulls (12–72 tris).
    - Parapets L/R (40 / 20 m), bridge pier line, abutment start / end, overpass piers (Standard / Wide / Hero), underpass walls L/R (40 / 20 m).
    - **No deck / road / joint collider:** P0 owns road collision.
    - None intrude into the drivable road volume (check 27).
34. **Snap points:** `<Module>_Snap_Start` (root origin = road centre at the chunk start) / `_Snap_End` on Bridge_Deck_40m / _20m / _Start / _End and Underpass_40m / _20m. Exactly 40.000 / 20.000 m, verified again after FBX re-import (Unity +Z forward 0 … 40.000).
35. **Alignment references:** sphere empties RoadCenter, DeckTop, DeckBottom, ClearanceBottom, PierCenter, Pier_L, Pier_R, AbutmentFace, WallInner_L, WallInner_R, OverpassCenter on the overpasses, decks and underpasses.
36. **Driver-view QA:** **PASS.**
    - `P2_bridge_driver_approach.png` (Hero ahead), `_driver_underpass.png`, `_overpass_50m … 300m.png` (1.15–1.6 m eye height).
    - The road sightline is clear and the supports sit well outside the corridor.
37. **Chase-view QA:** **PASS.** `P2_bridge_chase_underpass.png`: the beam rhythm under the deck reads at speed; the car scales correctly.
38. **High-chase QA:** **PASS.** `P2_bridge_high_chase.png` under the Hero: haunched box soffit, parapets and supports read; the road stays visible.
39. **Terrain-transition QA:** **PASS** with a QA-only valley.
    - `P2_bridge_abutment.png`, `_start_end.png`, `_deck.png`: abutment stems and wing walls meet the linked P1 TerrainTransition / Fill modules at road level, with no floating abutments and no holes.
    - The valley under the bridge is a QA-only mesh, so Unity must place lower terrain. Overpass abutments sit on the P1 cut slopes.
40. **Full-sequence QA:** **PASS.**
    - 1,000 m on the **linked frozen P0 road**: 25 straight, level, contiguous 40 m chunks.
    - Layout: flat → fill → Bridge Start / 40 / 40 / End over the valley → fill → flat → cut → Hero → cut → Underpass → Standard → Wide.
    - Linked P1 terrain, props (guardrails into the parapet transitions, streetlights, P1 sign and VMS panels on the bridge mounts), P1 vegetation and the hypercar. `P2_bridge_full_sequence.png`, check 31.
41. **Checkpoint paths:** `blend/bridges_01_blockout`, `_02_overpass`, `_03_bridge_deck`, `_04_structures`, `_05_materials_uv`, `_06_lods_collision`, `_07_export_ready.blend`. Each was written once in a final single pass; WIP iterations went to the session scratchpad. **Final source: `bridges_07_export_ready.blend`.**
42. **Preview paths:** `previews/P2_bridge_{hero_overpass, overpass_50m, overpass_100m, overpass_200m, overpass_300m, driver_approach, driver_underpass, chase_underpass, high_chase, deck, understructure, piers, abutment, start_end, expansion_joint, drainage, night, full_sequence, asset_library}.png`, plus `overpass_standard` and `overpass_wide`. 21 images.
43. **FBX paths:** `exports/bridges_complete.fbx`, `Overpasses.fbx`, `BridgeDecks.fbx`, `Piers_Abutments.fbx`, `Underpass.fbx`, `BridgeBarriers.fbx`, `BridgeDrainage.fbx`, `BridgeFixtures.fbx`, `BridgeCollision.fbx`. 9 files, 224 objects; axis-bake residual 4.8e-6.
44. **FBX re-import result:** **all 9 PASS.**
    - Names, hierarchy, materials, UVs and triangle counts match.
    - World deviation ≤ 5e-4 m.
    - Unity +Y up / +Z forward confirmed (deck slab Z 0 … 40.000, Hero up to Y 9.41).
45. **Validation result:** **43 checks, 0 errors, 0 warnings** (`reports/P2_bridges_validation.txt`). It covers all 33 required checks plus the per-FBX re-import, topology and naming.
46. **UnityTransfer path:** `environment/P2_Bridges/UnityTransfer/` (FBX / Textures {Concrete, Metal, Trim, Glass, Signs, Decals} / Reports / README).
47. **Import notes:** `UnityTransfer/README/BRIDGES_IMPORT_NOTES.md`. It covers all 26 topics and carries the Blender-only / Unity-side statement.
48. **Streaming guide:** `UnityTransfer/README/BRIDGES_STREAMING_GUIDE.md`. It covers compositions A bridge run, B overpass and C short underpass; structural vs optional assets; snaps; what stays from P0; what must not be duplicated.
49. **Performance guide:** `UnityTransfer/README/BRIDGES_PERFORMANCE_GUIDE.md`. It covers the PC / mobile LOD concepts, instancing, transparency limits and culling, with no claimed FPS.
50. **Freeze report:** `reports/P2_bridges_FINAL_FREEZE.md`, with SHA-1 hashes of the blends, FBX and textures. `environment/P2_Bridges/` is **FROZEN**.
51. **Known limitations:**
    - **Terrain is preview-only:** the valley under the bridge run, the overpass hills and the tree placement are not exported. Unity must provide the terrain there; the frozen P1 Terrain has no deep-valley module (documented, not edited).
    - **Hero LOD3** is 22 % of LOD0, above the optional 5–10 %. The silhouette was kept rather than collapsed.
    - **Small assets:** piers, abutment B and caps are below the triangle guidance; they were not padded.
    - **Wide soffit:** its shadow-joint strips sit 4 cm below the 6.0 m soffit (5.96 m), still well above 5.5 m.
    - **Overhang by design:** Start / End wing walls and parapet transitions extend 8.7 m into the neighbouring open-road chunk.
    - **Previews:** night lighting is Blender preview only, with no Unity accuracy. No wet preview (optional; the P0 road material is frozen).
    - **QA scene edge:** the far end of the QA scene shows the edge of the vista ground (`full_sequence`).
52. **Recommended next Blender phase:** **P2-BLENDER City** (`environment/P2_City/`, empty) or a terrain addendum providing a deep-valley module for bridge runs. This is a recommendation only; it was not started.

---

### `UnityTransfer/README/BRIDGES_IMPORT_NOTES.md`

### Bridges & Overpasses — Unity import notes (P2-BLENDER-01)

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.**
> **UNITY-SIDE: MATERIALS, REFLECTIONS, REAL LIGHTS, SHADOWS, LODGroup COMPONENTS, ROADSTREAMER INTEGRATION, TERRAIN PLACEMENT, CULLING, QUALITY TIERS AND PERFORMANCE TESTING MUST BE COMPLETED ON THE UNITY WORKSTATION.**

1. **Source phase:** P2-BLENDER-01, Premium Modular Bridges & Overpasses. Source `environment/P2_Bridges/blend/bridges_07_export_ready.blend`. Frozen dependencies (P0, P1 Props / Terrain / Vegetation / Tunnel, vehicles) were linked read-only and are byte-for-byte unchanged.
2. **Unity orientation:** +Y up, +Z forward (traffic), +X driver-right. This uses the same in-memory axis bake as every earlier package (G = Rot(−90°, X), Apply Transform OFF). Blender (x, y, z) → Unity (−x, z, −y).
3. **Scale:** 1 unit = 1 m (FBX cm + FBX_SCALE_ALL). Import with Scale Factor 1 and Convert Units ON.
4. **Road relationship:** the frozen P0 road chunks remain the gameplay road (surface, markings, shoulders, median, barrier, collision). Bridge modules are structure only, around and below the P0 road. Overpasses / underpass span over it. **No lane geometry is duplicated.**
5. **Level-road requirement:** the road stays at P0 height (crown z +0.036). There are no ramps, slopes or banking. "Elevation" comes from the environment dropping away (valley / Terrain_Fill) under the bridge modules.
6. **40 m module convention:**
   - **Modules:** `Bridge_Deck_40m`, `Bridge_Deck_Start`, `Bridge_Deck_End`, `Underpass_40m`.
   - **Snap:** root origin = `Snap_Start` = road centre at chunk start (identical to the P0 chunk origin). `Snap_End` at Unity (0, 0, +40.000).
   - **Outside the 40 m by design:** Start / End wing walls and parapet transitions reach 8.7 m beyond the abutment into the neighbouring open-road chunk.
7. **20 m module convention:** `Bridge_Deck_20m` and `Underpass_20m`, with `Snap_End` at (0, 0, +20.000).
8. **Hero Overpass (`Overpass_Hero`, LOD0–3):**
   - **Structure:** twin painted-steel trapezoidal box girders, haunched from 1.6 m over the lanes to 2.85 m at the piers. Steel cross-girders every 4 m, a painted fascia with an underlight strip, inclined V-piers on pier heads with pot bearings, seat abutments with return walls, metal parapets, light-pole mounts.
   - **Size:** 15 m deck, 33.5 m main span, overall 83 × 17 × 10.6 m; deck top 8.23 m, parapet top 9.4 m.
   - **Clearance:** 6.35 m soffit at the centre line; **6.18 m minimum over the road kit** (haunch begins at the road-kit edge).
   - **Placement:** origin = road centre on the structure centre line. Place it at local Z +20 of a 40 m chunk.
9. **Other overpass variants:**
   - **`Overpass_Standard`:** 12 m deck, 5 precast I-girders + diaphragms, twin round columns on rectangular caps, concrete parapets, 6.0 m soffit.
   - **`Overpass_Wide`:** 18 m deck, 3-cell concrete box with ribbed cantilevers, wall piers, metal parapets + glass noise barriers, 6.0 m soffit.
   - **Supports:** all outside the road corridor (no central pier).
10. **Bridge Deck modules:** `Bridge_Deck_40m` / `_20m`.
    - **Below the P0 road:** 0.25 m slab (top −0.32), 6 precast bulb-tee girders (2.0 m), diaphragms every 10 m, a pier line at mid-length (2 × Pier_A + CapBeam_A + 6 elastomeric bearings) down to the valley floor at −14.5.
    - **At road level:** concrete single-slope parapets with edge-beam fascia on both sides, slot drains in the P0 drain corridor, scuppers + downpipe.
11. **Start / End modules:**
    - **`Bridge_Deck_Start`:** abutment A (seat, backwall, footing) at the snap, 30°-splayed stepped wing walls toward the embankment, parapet transitions to the P1 guardrail, a finger expansion joint, plus the first 40 m span.
    - **`Bridge_Deck_End`:** the exact mirror, with the abutment at its Snap_End.
12. **Piers:**

    | Asset | Shape | Height |
    |---|---|---|
    | `Bridge_Pier_A` | chamfered tapered rectangle | 10.98 m (bridge run) |
    | `Bridge_Pier_B` | round column + collar | 4.75 m (Standard overpass) |
    | `Bridge_Pier_Wide` | rounded wall pier 9 × 1.4 m | 6.2 m |

    Origin = base centre; footing implications extend 0.8 m below.
13. **Cap beams:** `Bridge_CapBeam_A` (hammerhead 21.6 m, X) and `_B` (rectangular 11 m, Y). Origin = top (bearing plane).
14. **Abutments:** `Bridge_Abutment_A` (bridge run; origin = road centre at the deck start) and `_B` (overpass seat type; origin = base / road-facing face, faces +X).
15. **Wing walls:** `Bridge_WingWall_L/R`, splayed 30° and stepped, top −0.30 (the P0 skirt / TerrainTransition level); same origin as Abutment_A.
16. **Underpass:**
    - **Modules:** `Underpass_40m` / `_20m` (walls + ceiling + end trims + underdeck lights + downpipes).
    - **Kit pieces:** `Underpass_Wall_L/R`, `Underpass_Ceiling` (deck 7.0–7.6, transverse beams every 2 m, soffit 6.0), `Underpass_EndTrim` (fascia with ID + clearance plates).
    - **Openness:** the covered deck is 20 m of the 40 m module; the walls drop to 3 m at both ends, so daylight shows at both ends. It is not a tunnel.
17. **Parapets:** `Bridge_Parapet_Concrete` (40 m), `Bridge_Parapet_Metal` (8 m, posts every 2 m), `Bridge_Parapet_Transition` (meets the frozen P1 guardrail / Guardrail_To_Concrete_Transition at x −11.0), plus `Bridge_NoiseBarrier_4m / _8m / _End`.
18. **Expansion joints:** `Bridge_ExpansionJoint_A` (finger) and `_B` (strip seal). Visual only, 4 mm above the road, **no collider**. They appear only at abutments (Start / End), never every few metres.
19. **Drainage:** `Bridge_DeckDrain_4m / _8m` (LOD1 = flat textured plate), `Bridge_Drain_A` (fascia scupper), `Bridge_Downpipe_A`.
20. **LOD naming:** a root empty `<Asset>` with children `<Asset>_LOD0..n`. Create one LODGroup per root (see `BRIDGES_PERFORMANCE_GUIDE.md`).
21. **Materials:** `MAT_Bridge_Concrete`, `_Concrete_Dark`, `_Steel`, `_Galvanized`, `_PaintedMetal`, `_Rubber`, `_Glass`, `_Drain`, `_SignSupport`, `_Light`, `_Decal`.
22. **Texture channels (`Textures/`):**

    | Texture | Channels |
    |---|---|
    | Concrete 2K | BaseColor, Normal (OpenGL), Roughness, AO; 4 m / tile |
    | Steel 2K | BaseColor, Normal, Roughness, Metallic; 4 m / tile |
    | Trim 2K | BaseColor, Normal, Roughness, Metallic, AO |
    | Glass 1K | BaseColor + alpha, Roughness |
    | Signs 1K | BaseColor, Roughness, Emissive |
    | Decals 2K | BaseColor + alpha, Normal, Roughness |

    sRGB for BaseColor only.
23. **Colliders (`BridgeCollision.fbx`):**
    - **Assets:** `Collision_Bridge_Parapet_L/R` (+ `_20m`), `Collision_Bridge_Pier`, `Collision_Abutment` / `_End`, `Collision_Overpass_Pier` (Standard) / `_Wide` / `_Hero`, `Collision_UnderpassWall_L/R` (+ `_20m`).
    - **Form:** closed boxes / convex hulls, no materials. Use static (convex where possible) MeshColliders.
    - **Not provided:** no road / deck collider (P0 provides it) and no joint collider.
24. **Snap points:** `<Module>_Snap_Start` (root origin) and `_Snap_End` on every road-aligned module (Bridge_Deck_40m / 20m / Start / End, Underpass_40m / 20m).
25. **Alignment empties (spheres):**
    - **Overpasses:** `_RoadCenter`, `_OverpassCenter`, `_DeckTop`, `_DeckBottom`, `_ClearanceBottom`, `_Pier_L`, `_Pier_R`, `_PierCenter`, `_AbutmentFace`.
    - **Decks:** `_DeckTop`, `_DeckBottom`, `_RoadCenter`, `_PierCenter`, `_AbutmentFace`.
    - **Underpasses:** `_WallInner_L/R`, `_ClearanceBottom`, `_DeckTop`, `_RoadCenter`.
26. **Excluded QA assets:** QA sequence (linked P0 road, P1 terrain / props / vegetation, hypercar), QA valley, module / overpass instances, asset-library instances, presentation cameras, render-session lights. The list is in `Reports/P2_bridges_export_manifest.json`.

---

### `UnityTransfer/README/BRIDGES_STREAMING_GUIDE.md`

### Bridges & Overpasses — streaming guide (straight / level / 40 m RoadStreamer)

**The road stays STRAIGHT and LEVEL.** Every composition below keeps spawning the frozen P0 road chunk at each 40 m step. Bridge assets add structure around or under it. Never move or raise the road.

#### A. Bridge run
```
Open Road | Bridge_Deck_Start | Bridge_Deck_40m | Bridge_Deck_40m | Bridge_Deck_End | Open Road
```
- **Per chunk:** P0 road chunk + bridge module at the same transform (origin = Snap_Start; next chunk at +40 Z).
- **Optional:** add `Bridge_Deck_20m` pairs for 20 m granularity (the P0 `Road_4Lane_20m` goes with them).
- **Keep from P0:** road surface, edge lines / dividers, paved shoulders, `Median_Concrete`, `Median_Barrier` and all P0 road collision.
- **Skip on bridge chunks:**
  - the P0 `Drain_Channel_4m` / `Drain_Grate`: `Bridge_DeckDrain_*` occupies the same corridor;
  - `Shoulder_Gravel` / `EdgeBreakup_Verge`: the bridge parapet sits there;
  - P1 guardrails on the deck: the parapet replaces them. `Bridge_Parapet_Transition` hands over to the P1 `Guardrail_To_Concrete_Transition` at x −11.0 on the open-road side.
- **Terrain:**
  - under the bridge chunks, Unity places lower ground / valley terrain (the world falls away to about −14.5 m);
  - on the adjacent open-road chunks, use P1 `Terrain_Fill_*` + `TerrainTransition_*`, which meet the wing walls (top −0.30).
  - The start / end chunks' wing walls reach 8.7 m into those open-road chunks by design.

#### B. Overpass
```
Open Road | (Open Road + Overpass_Hero / _Standard / _Wide at local Z +20) | Open Road
```
- **Placement:** the overpass is placed on an ordinary open-road chunk; there is no special road module.
- **Terrain:** use P1 `Terrain_Cut_Both_40m` (or cut modules) on that chunk and its neighbours, so the abutments sit on the cut slopes.
- **Signs:** `Overpass_SignFrame` (+ P1 `SignPanel_Medium`) or `Bridge_VMS_Mount` (+ P1 `VMS_Panel`) can hang on the approach fascia (lowest point 6.4 m sign frame / 6.5 m VMS mount).

#### C. Short underpass
```
Open Road | Underpass_40m | Open Road
```
- **Per chunk:** P0 road chunk + `Underpass_40m` at the same transform. Keep the P0 drain and guardrail.
- **Spacing:** walls stand at x −12.8 / +11.6, outside the guardrail (x −11.0) and the median strip.
- **Terrain:** use cut terrain on the neighbours.
- **20 m variant:** `Underpass_20m`.

#### Structural vs optional
| Structural (spawn with the module) | Optional detail |
|---|---|
| Bridge_Deck_* (deck, girders, piers, caps, bearings, parapets, drains, abutment, wing walls, joints are already merged into the module LODs) | Bridge_NoiseBarrier_* (on deck parapets, +1.10 m) |
| Overpass_* (complete assemblies) | Bridge_LightPoleMount + P1 Streetlight on overpasses |
| Underpass_40m / _20m (walls, ceiling, end trims, lights, downpipes merged) | Overpass_SignFrame / Bridge_VMS_Mount / Bridge_SignMount + P1 panels |
| Colliders listed in the import notes | decals (runoff, rust, stains, dirt edge, repair patch) |

Kit pieces (`Bridge_Pier_*`, `_CapBeam_*`, `_Abutment_*`, `_WingWall_*`, `_Parapet_*`, `_ExpansionJoint_*`, `_Bearing_*`, drains, `Underpass_Wall_*`, `_Ceiling`, `_EndTrim`) are for custom builds only. **They are already inside the modules; do not spawn them in addition.**

#### Snap convention
Module root origin = `Snap_Start` = road centre at the chunk start; `Snap_End` = (0, 0, +40.000) or (0, 0, +20.000). Chunk N+1 origin = chunk N origin + 40 Z. Bridge-run modules are seamless in any order: slab, girders, parapets and drains are continuous, and diaphragms and pier lines fall inside the modules.

#### Must not be duplicated
- P0 road geometry / collision (the modules contain none).
- P1 guardrails / streetlights / signs (linked in QA only; mounts are provided).
- Kit pieces in addition to modules.
- A second road collider on bridge decks.

---

### `UnityTransfer/README/BRIDGES_PERFORMANCE_GUIDE.md`

### Bridges & Overpasses — performance guide (concepts, no measured Unity numbers)

No Unity FPS or GPU timings were measured; this workstation has no Unity. The triangle counts below are from `Reports/P2_bridges_geometry.json`.

#### Triangle reference (LOD0 → LODn)
| Asset | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Overpass_Hero | 6,688 | 3,504 | 1,744 | 1,492 |
| Overpass_Wide | 5,300 | 2,788 | 1,272 | |
| Overpass_Standard | 3,924 | 1,328 | 600 | |
| Bridge_Deck_40m | 6,942 | 2,532 | 1,208 | |
| Bridge_Deck_Start / End | 7,698 | 2,656 | 1,332 | |
| Underpass_40m | 3,680 | 592 | 312 | |

#### PC (high)
- **LODGroup transitions** (screen-relative height):

  | Asset | LOD0 | LOD1 | LOD2 | LOD3 | Cull |
  |---|---|---|---|---|---|
  | Overpass_Hero | 0.35 | 0.15 | 0.06 | 0.02 | |
  | Other overpasses / bridge modules | 0.30 | 0.12 | 0.03 | | |
  | Fixtures / mounts / drains | 0.06 | | | | 0.02 |

- **Underside:** keep it at LOD0/1 while the player is within about 150 m. The girder rhythm is the payoff of driving underneath.
- **Hero:** full quality near. Keep it out of aggressive occlusion culling, because it is a landmark seen from 300 m.
- **Shadows:** concrete and steel cast shadows; glass noise barriers should not cast shadows (or use a cheap shadow-only proxy).

#### Mobile
- **LOD transitions:** earlier (multiply the heights by about 1.5–2). Hero LOD2 / LOD3 from mid distance.
- **Drop small detail:** drain grates, bearings, fixtures and mounts are culled beyond about 40–60 m (their LOD1 is already minimal: the drain LOD1 is a single textured plate).
- **Transparency:** limit transparent noise barriers. On low tiers swap `MAT_Bridge_Glass` for an opaque frit-only variant, or disable the noise barriers. Never stack transparent layers.
- **Decals:** off on low tiers.
- **Materials:** a single material per structure where possible. Concrete + steel + trim share 2K atlases, so batching is effective.

#### Instancing / batching
- Repeated pieces suit GPU instancing: bridge modules, parapets, noise-barrier bays, drains, light / sign mounts, bearings and piers all share materials.
- Static batching is appropriate for non-streamed scenery. The RoadStreamer modules are better served by instancing or pooling.

#### Collision
Simple boxes and hulls only (12–72 tris each). There is no deck or joint collision, because P0 owns the road. Use convex colliders where possible; overpass piers sit outside the drivable corridor.

---

### `reports/P2_bridges_materials.md`

### P2-BLENDER-01 — Bridge materials, textures and texel density

These are Blender **source / preview** materials, not Unity shaders.

#### Materials (11 shared)
| Material | Textures | Used for |
|---|---|---|
| `MAT_Bridge_Concrete` | T_Bridge_Concrete_2K | decks, girders (bridge run / Standard), piers, caps, abutments, wing walls, underpass, parapets |
| `MAT_Bridge_Concrete_Dark` | T_Bridge_Concrete_2K × 0.66 | soffit shadow joints, underpass drip line |
| `MAT_Bridge_Steel` | T_Bridge_Steel_2K | Hero box girders and cross girders (painted structural steel) |
| `MAT_Bridge_PaintedMetal` | Trim: painted_steel | Hero fascia / bottom flange, metal-parapet posts, downpipes, fixture housings |
| `MAT_Bridge_Galvanized` | Trim: galvanized | rails, bearing plates, mounts, noise-barrier posts, finger joints, scuppers |
| `MAT_Bridge_Rubber` | Trim: rubber | elastomeric bearings, strip-seal |
| `MAT_Bridge_Drain` | Trim: drain_metal | slot-drain grates |
| `MAT_Bridge_Glass` | T_Bridge_Glass_1K | acrylic noise-barrier panels (single layer, alpha) |
| `MAT_Bridge_SignSupport` | T_Bridge_Signs_1K | clearance sign, bridge-ID plate |
| `MAT_Bridge_Light` | — (emissive source colour) | fixture lenses |
| `MAT_Bridge_Decal` | T_Bridge_Decals_2K | runoff, rust streak, stains, dirt edge, repair patch |

#### Trim sheet `T_Bridge_Trim_2K` (BaseColor, Normal, Roughness, Metallic, AO)
Strips are in px from the bottom; U tiles every **4 m** (512 px/m along members).

| Strip | px | Content |
|---|---|---|
| concrete_edge | 0–256 | clean precast edge with a chamfer highlight |
| concrete_weathered | 256–512 | runoff / grime gradient |
| galvanized | 512–704 | spangle, metallic 1 |
| painted_steel | 704–896 | blue-grey paint, metallic 0.1 |
| dark_steel | 896–1088 | dark structural steel with light rust |
| rubber | 1088–1184 | |
| joint_surface | 1184–1376 | modular finger-joint pattern |
| drain_metal | 1376–1536 | slot grate (used by LOD1 drain plates) |
| utility_metal | 1536–1728 | |
| barrier_detail | 1728–2048 | parapet face with scupper band and anchor-plate rhythm |

There is a 2 px guard band inside every strip. Trim faces: U = metres along the face's longest edge, V = across the strip.

#### Concrete `T_Bridge_Concrete_2K` (BaseColor, Normal, Roughness, AO)
- **Tiling:** tileable (FFT noise). **4 m per tile = 512 px/m.**
- **Content:**
  - warm-grey modern concrete;
  - faint formwork tie holes on a 1 m grid and board joints every 1 m;
  - restrained mottling and staining;
  - no cracks, no heavy damage.
- **Language:** matches P1 Tunnel / P1 Terrain retaining walls (same 512 px/m, similar warm grey). This is a new texture; no upstream file was copied or modified.
- **UVs:** world-scale box projection everywhere. A 40 m deck covers 10+ tiles; one 0–1 UV is never stretched over 40 m.

#### Steel `T_Bridge_Steel_2K` (BaseColor, Normal, Roughness, Metallic)
- **Tiling:** tileable, 4 m per tile, box projected.
- **Finish:** painted structural steel (paint film, metallic 0.15), with subtle orange-peel, roller variation and faint weld seams every 2 m. Not chrome, not flat grey.

#### Glass / noise barrier `T_Bridge_Glass_1K` (BaseColor + alpha, Roughness)
- **Mapping:** one acrylic panel per 0–1 tile (one quad per 2 m bay).
- **Alpha:** 0.32 clear, 0.95 on the top and bottom frit bands, bird-safety dot lines.
- **Layering:** a **single transparent layer**. Posts are opaque galvanised; there is no layered transparency.

#### Signs `T_Bridge_Signs_1K` (BaseColor, Roughness, Emissive)
Clearance 6.0 M roundel, `BR-01` ID plate, lens, hazard stripes, blank. Generic, no branding.

#### Decals `T_Bridge_Decals_2K` (BaseColor + alpha, Normal, Roughness)
`Bridge_Runoff_A` (1.0 × 2.5 m), `_B` (1.4 × 2.0), `Bridge_RustStreak_A` (0.4 × 1.6), `Bridge_ConcreteStain_A` (2.4 × 1.6), `Bridge_DirtEdge_A` (4.0 × 1.0), `Bridge_RepairPatch_A` (1.6 × 1.2). Separate quads facing +X; place them 5 mm off the surface.

#### Weathering strategy
- **Placed decals (logical locations):** runoff under expansion joints, abutment seats and the underpass deck edge; rust streaks below bearings and steel connections; dirt edges at wall bases.
- **In the textures:** the weathered-concrete trim strip on parapet faces and edge beams.
- **Not done:** no heavy damage baked anywhere. No vertex-wear layer this phase (decals + trim cover it).

#### Texel density summary
| Surface | Metres per tile | px / m |
|---|---|---|
| Concrete | 4 | 512 |
| Painted steel | 4 | 512 |
| Trim strips | 4 (U) | 512 along U |
| Glass | 1 panel (2 × 3 m) | 512 / 341 |
| Decals | per decal size | ~400–1000 |

#### Unity expectations
- **Shaders:** Unity URP Lit for concrete / steel / trim (Metallic + 1−Roughness packed into the mask map), transparent Lit for glass (single sided off, no depth sorting issues since it is one layer), and the URP Decal Projector or transparent mesh decals.
- **Emissive:** `MAT_Bridge_Light` is an emissive source colour only.
- **Unity-side tasks:** real lights, reflections, shadows and wetness are Unity-side.

---

### `reports/P2_bridges_FINAL_FREEZE.md`

### P2_Bridges — FINAL FREEZE

Date: 2026-10-07 · Phase P2-BLENDER-01 · Status: **FROZEN**. Nothing under `environment/P2_Bridges/` is to be edited; later phases may only link from it read-only.

#### Final deliverables
- **Final source blend:** `blend/bridges_07_export_ready.blend` (checkpoints `bridges_01_blockout` … `bridges_06_lods_collision` kept unchanged).
- **FBX (`exports/`, identical in `UnityTransfer/FBX/`):** `BridgeBarriers.fbx`, `BridgeCollision.fbx`, `BridgeDecks.fbx`, `BridgeDrainage.fbx`, `BridgeFixtures.fbx`, `Overpasses.fbx`, `Piers_Abutments.fbx`, `Underpass.fbx`, `bridges_complete.fbx`
- **Textures:** concrete (T_Bridge_Concrete_2K ×4), metal (T_Bridge_Steel_2K ×4), trim (T_Bridge_Trim_2K ×5), glass (T_Bridge_Glass_1K ×2), signs (T_Bridge_Signs_1K ×3), decals (T_Bridge_Decals_2K ×3).
- **Reports:** `reports/P2_bridges_discovery.md`, `_materials.md`, `_validation.txt`, `_geometry.json`, `_export_manifest.json`, `_source_baseline.json`, `_source_integrity_check.md`, `_textures.json`, `_qa_sequence.json`, `_FINAL_REPORT.md`.
- **Previews:** 21 images in `previews/`.
- **UnityTransfer:** `UnityTransfer/` (FBX, Textures, Reports, README: `BRIDGES_IMPORT_NOTES.md`, `BRIDGES_STREAMING_GUIDE.md`, `BRIDGES_PERFORMANCE_GUIDE.md`).

#### Validation state
`reports/P2_bridges_validation.txt`: **SUMMARY: 0 errors, 0 warnings**.
Source integrity: **PASS** (`reports/P2_bridges_source_integrity_check.md`).

#### Known limitations
- The QA valley, overpass hills and vegetation placement are preview-only (not exported); Unity must supply terrain under bridge runs and around overpasses.
- Hero LOD3 (1,492 tris) is 22 % of LOD0, above the optional 5–10 % guidance: the deck depth / twin-box / V-pier silhouette was kept rather than collapsed.
- Piers (104–168 tris) and abutment B (60) are below the triangle guidance; not padded.
- Preview lighting is Blender-only (area lights at the lenses); not photometric, not Unity values. No wet preview (optional; P0 road material frozen).
- Start / End wing walls and parapet transitions extend 8.7 m outside their module into the neighbouring open-road chunk by design.

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P2_bridges_validation.txt`

```text
== P2-BLENDER-01 BRIDGES & OVERPASSES - VALIDATION ==
source blend/bridges_07_export_ready.blend; BRIDGES_MASTER 224 objects, 115 meshes (101 renderable, 14 colliders)

[PASS]  1. source integrity: P0, P1 Props, P1 Terrain, P1 Vegetation, P1 Tunnel, vehicles and all other workspace files byte-identical to the pre-phase baseline
[PASS]  2. Overpass_Hero exists (LOD chain [6688, 3504, 1744, 1492])
[PASS]  3. Overpass_Standard exists (LOD chain [3924, 1328, 600])
[PASS]  4. Overpass_Wide exists (LOD chain [5300, 2788, 1272])
[PASS]  5. Hero 300 m readability QA exists: driver-height cameras at 50 / 100 / 200 / 300 m with rendered previews (reviewed visually, see FINAL_REPORT)
[PASS]  6. vertical clearance: lowest structure over the full road kit (x -10.2 .. 8.7) >= 5.5 m for every overpass / underpass LOD and sign / VMS mount (designed soffit 6.0 m, Hero 6.17 m minimum)
[PASS]  7. supports outside active lanes: no overpass / underpass geometry below 5.5 m inside x -12.2 .. 11.2 (shoulder edge - 2 m .. median strip + 0.5 m); no central pier (median strip only 2 m)
[PASS]  8. Bridge_Deck_40m exists (LOD0-2, snap empties)
[PASS]  9. Bridge_Deck_20m exists (LOD0-2, snap empties)
[PASS] 10. Bridge_Deck_Start exists (LOD0-2, snap empties)
[PASS] 11. Bridge_Deck_End exists (LOD0-2, snap empties)
[PASS] 12. piers (Bridge_Pier_A / _B / _Wide) exist
[PASS] 13. cap beams (Bridge_CapBeam_A / _B) exist
[PASS] 14. abutments (Bridge_Abutment_A / _B) exist
[PASS] 15. wing walls (Bridge_WingWall_L / _R) exist
[PASS] 16. underpass (Underpass_40m / _20m / _Wall_L / _Wall_R / _Ceiling / _EndTrim) exist
[PASS] 17. underside structure exists (not a flat plane): >= 150 structural faces between soffit and deck slab, structural depth >= 1.0 m (girders / boxes / cross-girders / beams)
[PASS] 18. parapets / barriers (Concrete, Metal, Transition, NoiseBarrier 4 / 8 / End) exist
[PASS] 19. expansion joints (A finger, B strip seal) exist; joint top 4 mm above the road crown, no collider (visual only)
[PASS] 20. bearings (A elastomeric, B pot) exist
[PASS] 21. drainage (Drain_A scupper, Downpipe_A, DeckDrain 4 / 8 m) exist
[PASS] 22. lighting / sign mounts (LightPoleMount, UnderdeckLight, Overpass_Underlight, ServiceLight, SignMount, Overpass_SignFrame, VMS_Mount) exist
[PASS] 23. materials: only the 11 shared MAT_Bridge_* materials, every slot used, colliders have none
[PASS] 24. trim sheet T_Bridge_Trim_2K (BaseColor / Normal / Roughness / Metallic / AO) + tileable T_Bridge_Concrete_2K + T_Bridge_Steel_2K (2048), glass / sign atlases (1024), decal atlas (2048)
[PASS] 25. UVs: UVMap on every renderable mesh; trim faces inside one trim strip; sign / decal faces inside one atlas rect; glass panel = one 0..1 tile; concrete / steel world-scale 4 m tiles (never one 0-1 over 40 m)
[PASS] 26. LODs: 42 LOD groups (<Asset> root + _LOD0..n), triangle counts strictly decreasing; Hero LOD ratios [1.0, 0.52, 0.26, 0.22] (guidance 1 / 0.4-0.6 / 0.15-0.3 / 0.05-0.1)
[PASS] 27. colliders: closed, low-poly (< 200 tris), no material, none inside the drivable road volume (P0 keeps road collision; no deck / joint collider)
[PASS] 28. transforms: every production mesh has an identity world matrix (scale 1, no rotation, no negative scale); every root at the world origin
[PASS] 29. pivots / origins: modules at road centre Snap_Start; overpasses at road centre on the structure centre line; piers at base centre; cap beams at top (bearing plane); bearings at bottom; fixtures at mount point
[PASS] 30. snap distances: Snap_Start (root origin) -> Snap_End exactly 40.000 / 20.000 m for Bridge_Deck_40m / _Start / _End, Bridge_Deck_20m, Underpass_40m / _20m; deck slab / wall footprint spans exactly y 0 .. -L on every LOD
[PASS] 31. QA sequence passes: 1000 m on the LINKED frozen P0 road (25 straight, level, contiguous 40 m chunks at x 1000, z 0, no rotation); bridge run (Start / 40 / 40 / End over a valley), Hero + Standard + Wide overpasses, Underpass; nothing above the road surface on the bridge decks
[PASS] 32. exports contain no frozen linked assets: export selection == BRIDGES_MASTER; no P0 / P1 / Terrain / Vegetation / Tunnel / car data, no QA / camera / light / helper objects
[PASS] 33. normals / topology: no zero-area faces, ngons, loose vertices, duplicate faces or inconsistently wound neighbours; concrete / steel hard at structural edges (35 deg auto-sharp)
[PASS] 34. naming: every production object uses Bridge_ / Overpass_ / Underpass_ / Collision_ prefixes, LODs _LOD0..n, snaps _Snap_Start / _Snap_End, no .001 duplicates
[PASS] 35. FBX re-import Overpasses.fbx: 40 objects, names + hierarchy match, world deviation 1.5e-06 m, triangles / UVs / materials preserved; Unity +Y up / +Z forward (mesh data in FBX space; empties re-converted to Blender world): {"Overpass_Hero": {"up_Y_max": 9.41}}
[PASS] 36. FBX re-import BridgeDecks.fbx: 42 objects, names + hierarchy match, world deviation 4.9e-04 m, triangles / UVs / materials preserved; Unity +Y up / +Z forward (mesh data in FBX space; empties re-converted to Blender world): {"Bridge_Deck_40m": {"up_Y": [-15.3, 1.1], "forward_Z": [0.0, 40.0], "snap": 40.0, "snap_end...
[PASS] 37. FBX re-import Piers_Abutments.fbx: 27 objects, names + hierarchy match, world deviation 4.4e-04 m, triangles / UVs / materials preserved
[PASS] 38. FBX re-import Underpass.fbx: 34 objects, names + hierarchy match, world deviation 4.4e-06 m, triangles / UVs / materials preserved; Unity +Y up / +Z forward (mesh data in FBX space; empties re-converted to Blender world): {"Underpass_40m": {"up_Y": [-0.6, 8.7], "forward_Z": [-0.0, 40.0], "snap": 40.0, "snap_end_ble...
[PASS] 39. FBX re-import BridgeBarriers.fbx: 28 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVs / materials preserved
[PASS] 40. FBX re-import BridgeDrainage.fbx: 12 objects, names + hierarchy match, world deviation 4.8e-04 m, triangles / UVs / materials preserved
[PASS] 41. FBX re-import BridgeFixtures.fbx: 27 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVs / materials preserved
[PASS] 42. FBX re-import BridgeCollision.fbx: 14 objects, names + hierarchy match, world deviation 3.8e-04 m, triangles / UVs / materials preserved
[PASS] 43. FBX re-import bridges_complete.fbx: 224 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVs / materials preserved; Unity +Y up / +Z forward (mesh data in FBX space; empties re-converted to Blender world): {"Bridge_Deck_40m": {"up_Y": [-15.3, 1.1], "forward_Z": [0.0, 40.0], "snap": 40.0, "sn...

Triangle budgets are guidance only; below-budget assets are not reported as warnings.
SUMMARY: 0 errors, 0 warnings
```

