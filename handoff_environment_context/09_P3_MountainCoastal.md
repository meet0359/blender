# P3-BLENDER-01 — Premium Mountain & Coastal Highway Biome

Digest 09 of the environment handoff. Folder: `environment/P3_MountainCoastal/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/mountainCoastal_07_export_ready.blend`
- **Asset index source:** `reports/P3_MC_geometry.json` + `reports/P3_MC_export_manifest.json`
- **Checkpoints (7):** `mountainCoastal_01_blockout.blend`, `mountainCoastal_02_mountain.blend`, `mountainCoastal_03_coastal.blend`, `mountainCoastal_04_transitions.blend`, `mountainCoastal_05_materials_masks.blend`, `mountainCoastal_06_lods_collision.blend`, `mountainCoastal_07_export_ready.blend`
- **FBX (10):** `MountainTerrain.fbx` (90 objects), `MountainCliffs.fbx` (30 objects), `MountainRocks.fbx` (28 objects), `MountainVistas.fbx` (30 objects), `CoastalTerrain.fbx` (84 objects), `CoastalShore.fbx` (50 objects), `CoastalVistas.fbx` (15 objects), `MC_Infrastructure.fbx` (24 objects), `MC_Collision.fbx` (4 objects), `mountainCoastal_complete.fbx` (355 objects)
- **Textures:** 16 PNG files · **Previews:** 16 renders · **UnityTransfer README:** `MC_IMPORT_NOTES.md`, `MC_PERFORMANCE_GUIDE.md`, `MC_PLACEMENT_GUIDE.md`, `MC_WATERLINE_GUIDE.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `CoastalCliff_A` | 2,520 / 594 / 120 | CoastalTerrain.fbx |
| `CoastalCliff_B` | 2,100 / 506 / 100 | CoastalTerrain.fbx |
| `CoastalCliff_C` | 2,720 / 682 / 130 | CoastalTerrain.fbx |
| `CoastalDistantLand_A` | 800 / 200 | CoastalVistas.fbx |
| `CoastalHeadland_A` | 3,600 / 900 / 240 | CoastalTerrain.fbx |
| `CoastalHeadland_B` | 3,600 / 900 / 240 | CoastalTerrain.fbx |
| `CoastalHeadland_C` | 3,600 / 900 / 240 | CoastalTerrain.fbx |
| `CoastalIsland_A` | 968 / 242 | CoastalVistas.fbx |
| `CoastalIsland_B` | 968 / 242 | CoastalVistas.fbx |
| `CoastalOverlook_A` | 288 / 120 | MC_Infrastructure.fbx |
| `CoastalPebbleBeach_A` | 9,520 / 2,600 / 576 | CoastalShore.fbx |
| `CoastalPebbleBeach_B` | 9,520 / 2,600 / 576 | CoastalShore.fbx |
| `CoastalRockShore_A` | 11,120 / 3,176 / 828 | CoastalShore.fbx |
| `CoastalRockShore_B` | 11,120 / 3,176 / 864 | CoastalShore.fbx |
| `CoastalRockShore_C` | 11,120 / 3,176 / 900 | CoastalShore.fbx |
| `CoastalRockStack_A` | 1,440 / 720 / 360 | CoastalShore.fbx |
| `CoastalRockStack_B` | 1,440 / 720 / 360 | CoastalShore.fbx |
| `CoastalSandStrip_A` | 9,520 / 2,600 / 576 | CoastalShore.fbx |
| `CoastalSlope_A` | 9,520 / 2,600 / 576 | CoastalTerrain.fbx |
| `CoastalSlope_B` | 9,520 / 2,600 / 576 | CoastalTerrain.fbx |
| `CoastalSlope_C` | 9,520 / 2,600 / 576 | CoastalTerrain.fbx |
| `CoastalVista_A` | 968 / 242 | CoastalVistas.fbx |
| `CoastalVista_B` | 968 / 242 | CoastalVistas.fbx |
| `Coastal_CliffFence_A` | 72 / 60 | MC_Infrastructure.fbx |
| `Coastal_In_20m` | 4,760 / 1,300 / 288 | CoastalTerrain.fbx |
| `Coastal_In_40m` | 9,520 / 2,600 / 576 | CoastalTerrain.fbx |
| `Coastal_Out_20m` | 4,760 / 1,300 / 288 | CoastalTerrain.fbx |
| `Coastal_Out_40m` | 9,520 / 2,600 / 576 | CoastalTerrain.fbx |
| `Coastal_RockBarrier_A` | 1,620 / 500 | MC_Infrastructure.fbx |
| `Coastal_Run_40m` | 9,520 / 2,600 / 576 | CoastalTerrain.fbx |
| `Coastal_SeaWall_A` | 96 / 60 | MC_Infrastructure.fbx |
| `MountainCliff_A` | 4,824 / 1,080 / 208 | MountainCliffs.fbx |
| `MountainCliff_B` | 3,360 / 800 / 154 | MountainCliffs.fbx |
| `MountainCliff_C` | 6,776 / 1,540 / 300 | MountainCliffs.fbx |
| `MountainDistantRange_A` | 800 / 200 | MountainVistas.fbx |
| `MountainDistantRange_B` | 800 / 200 | MountainVistas.fbx |
| `MountainOverlook_A` | 180 / 72 | MC_Infrastructure.fbx |
| `MountainRidge_A` | 3,872 / 968 / 242 | MountainVistas.fbx |
| `MountainRidge_B` | 3,872 / 968 / 242 | MountainVistas.fbx |
| `MountainRidge_C` | 3,200 / 800 / 200 | MountainVistas.fbx |
| `MountainRockCluster_A` | 1,296 / 400 / 144 | MountainRocks.fbx |
| `MountainRockCluster_B` | 1,944 / 600 / 216 | MountainRocks.fbx |
| `MountainRockCluster_C` | 972 / 300 / 108 | MountainRocks.fbx |
| `MountainRockCut_A` | 1,300 / 308 / 80 | MountainCliffs.fbx |
| `MountainRockCut_B` | 1,200 / 264 / 80 | MountainCliffs.fbx |
| `MountainRockCut_C` | 2,200 / 440 / 100 | MountainCliffs.fbx |
| `MountainScree_A` | 816 / 216 / 60 | MountainRocks.fbx |
| `MountainScree_B` | 816 / 216 / 60 | MountainRocks.fbx |
| `MountainSlope_Low_A` | 10,480 / 2,840 / 624 | MountainTerrain.fbx |
| `MountainSlope_Low_B` | 9,520 / 2,600 / 576 | MountainTerrain.fbx |
| `MountainSlope_Medium_A` | 10,480 / 2,840 / 624 | MountainTerrain.fbx |
| `MountainSlope_Medium_B` | 9,520 / 2,600 / 576 | MountainTerrain.fbx |
| `MountainSlope_Steep_A` | 10,480 / 2,840 / 624 | MountainTerrain.fbx |
| `MountainSlope_Steep_B` | 9,520 / 2,600 / 576 | MountainTerrain.fbx |
| `MountainTalus_A` | 1,816 / 576 / 240 | MountainRocks.fbx |
| `MountainTalus_B` | 2,416 / 792 / 348 | MountainRocks.fbx |
| `MountainVista_A` | 4,608 / 1,152 / 288 | MountainVistas.fbx |
| `MountainVista_B` | 4,608 / 1,152 / 288 | MountainVistas.fbx |
| `MountainVista_C` | 3,872 / 968 / 242 | MountainVistas.fbx |
| `Mountain_DrainChannel_A` | 160 / 16 | MC_Infrastructure.fbx |
| `Mountain_In_20m` | 10,000 / 2,720 / 600 | MountainTerrain.fbx |
| `Mountain_In_40m` | 20,000 / 5,440 / 1,200 | MountainTerrain.fbx |
| `Mountain_In_L_40m` | 10,480 / 2,840 / 624 | MountainTerrain.fbx |
| `Mountain_In_R_40m` | 9,520 / 2,600 / 576 | MountainTerrain.fbx |
| `Mountain_Out_20m` | 10,000 / 2,720 / 600 | MountainTerrain.fbx |
| `Mountain_Out_40m` | 20,000 / 5,440 / 1,200 | MountainTerrain.fbx |
| `Mountain_Out_L_40m` | 10,480 / 2,840 / 624 | MountainTerrain.fbx |
| `Mountain_Out_R_40m` | 9,520 / 2,600 / 576 | MountainTerrain.fbx |
| `Mountain_RockfallFence_A` | 360 / 108 | MC_Infrastructure.fbx |
| `Mountain_RockfallFence_B` | 360 / 108 | MC_Infrastructure.fbx |
| `Mountain_Run_40m` | 20,000 / 5,440 / 1,200 | MountainTerrain.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `CoastalShore.fbx` (18): CoastalPebbleBeach_A_Snap_End, CoastalPebbleBeach_A_Snap_Start, CoastalPebbleBeach_A_Waterline, CoastalPebbleBeach_B_Snap_End, CoastalPebbleBeach_B_Snap_Start, CoastalPebbleBeach_B_Waterline, CoastalRockShore_A_Snap_End, CoastalRockShore_A_Snap_Start, CoastalRockShore_A_Waterline, CoastalRockShore_B_Snap_End, CoastalRockShore_B_Snap_Start, CoastalRockShore_B_Waterline, CoastalRockShore_C_Snap_End, CoastalRockShore_C_Snap_Start, CoastalRockShore_C_Waterline, CoastalSandStrip_A_Snap_End, CoastalSandStrip_A_Snap_Start, CoastalSandStrip_A_Waterline
- `CoastalTerrain.fbx` (28): CoastalHorizon, CoastalSlope_A_Snap_End, CoastalSlope_A_Snap_Start, CoastalSlope_A_Waterline, CoastalSlope_B_Snap_End, CoastalSlope_B_Snap_Start, CoastalSlope_B_Waterline, CoastalSlope_C_Snap_End, CoastalSlope_C_Snap_Start, CoastalSlope_C_Waterline, Coastal_In_20m_Snap_End, Coastal_In_20m_Snap_Start, Coastal_In_20m_Waterline, Coastal_In_40m_Snap_End, Coastal_In_40m_Snap_Start, Coastal_In_40m_Waterline, Coastal_Out_20m_Snap_End, Coastal_Out_20m_Snap_Start, Coastal_Out_20m_Waterline, Coastal_Out_40m_Snap_End, Coastal_Out_40m_Snap_Start, Coastal_Out_40m_Waterline, Coastal_Run_40m_Snap_End, Coastal_Run_40m_Snap_Start, Coastal_Run_40m_Waterline, SeaFloorReference, ShorelineReference, Waterline
- `MC_Collision.fbx` (4): Collision_CoastalCliff (80), Collision_MountainCliff (8), Collision_MountainSlope (120), Collision_Overlook (12)
- `MountainCliffs.fbx` (6): MountainRockCut_A_Snap_End, MountainRockCut_A_Snap_Start, MountainRockCut_B_Snap_End, MountainRockCut_B_Snap_Start, MountainRockCut_C_Snap_End, MountainRockCut_C_Snap_Start
- `MountainTerrain.fbx` (30): MountainSlope_Low_A_Snap_End, MountainSlope_Low_A_Snap_Start, MountainSlope_Low_B_Snap_End, MountainSlope_Low_B_Snap_Start, MountainSlope_Medium_A_Snap_End, MountainSlope_Medium_A_Snap_Start, MountainSlope_Medium_B_Snap_End, MountainSlope_Medium_B_Snap_Start, MountainSlope_Steep_A_Snap_End, MountainSlope_Steep_A_Snap_Start, MountainSlope_Steep_B_Snap_End, MountainSlope_Steep_B_Snap_Start, Mountain_In_20m_Snap_End, Mountain_In_20m_Snap_Start, Mountain_In_40m_Snap_End, Mountain_In_40m_Snap_Start, Mountain_In_L_40m_Snap_End, Mountain_In_L_40m_Snap_Start, Mountain_In_R_40m_Snap_End, Mountain_In_R_40m_Snap_Start, Mountain_Out_20m_Snap_End, Mountain_Out_20m_Snap_Start, Mountain_Out_40m_Snap_End, Mountain_Out_40m_Snap_Start, Mountain_Out_L_40m_Snap_End, Mountain_Out_L_40m_Snap_Start, Mountain_Out_R_40m_Snap_End, Mountain_Out_R_40m_Snap_Start, Mountain_Run_40m_Snap_End, Mountain_Run_40m_Snap_Start

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `reports/P3_MC_FINAL_REPORT.md`

### P3-BLENDER-01 — Premium Mountain & Coastal Highway Biome — FINAL REPORT

**Status: COMPLETE and FROZEN** (2026-10-07). Blender only.
- No Unity work, and no prefabs, shaders or scripts were created for Unity.
- No frozen phase or vehicle was modified.
- The road stays straight and level on 40 m and 20 m modules.

#### 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/P3_MC_validation.txt`) | **33 checks — 0 errors, 0 warnings** |
| FBX clean re-import | 10 / 10 files pass: names, hierarchy, triangles, UVs, colour sets and materials preserved; world deviation ≤ 5.0e-4 m; Unity axes verified |
| Frozen-source integrity (`P3_MC_source_integrity_check.md`) | **PASS**: 1,412 baseline files byte-identical, 0 files added outside the phase folder |
| Previews | 16 / 16 at 1920 × 1080, all reviewed visually |
| Checkpoints | `mountainCoastal_01_blockout` … `_06_lods_collision`, final source `_07_export_ready`; each written once, none overwritten |

#### 2. Deliverables

- **Blend files.** `blend/mountainCoastal_01 … 07`. The final source is `mountainCoastal_07_export_ready.blend`.
- **FBX files** in `exports/`, also copied to `UnityTransfer/FBX/`. Together they hold 355 objects: 71 LOD groups, 202 meshes, snap points and waterline empties.
  - `mountainCoastal_complete`
  - `MountainTerrain`, `MountainCliffs`, `MountainRocks`, `MountainVistas`
  - `CoastalTerrain`, `CoastalShore`, `CoastalVistas`
  - `MC_Infrastructure`, `MC_Collision`
- **Textures** (2K, procedural, tileable): `rock/T_MC_MountainRock_2K`, `rock/T_MC_CoastalRock_2K`, `ground/T_MC_Pebble_2K`, `ground/T_MC_Sand_2K`. Each set has BaseColor, Normal, Roughness and AO.
- **Reports:**
  - `P3_MC_validation.txt`, `_geometry.json`, `_materials_masks.md`, `_export_manifest.json`
  - `_source_baseline.json`, `_source_integrity_check.md`
  - `_qa_sequence.json`, `_textures.json`
  - `_FINAL_FREEZE.md` (SHA-1 of 33 final files) and this report
- **UnityTransfer.** FBX, Textures, Reports, and README files:
  - `MC_IMPORT_NOTES.md`
  - `MC_PLACEMENT_GUIDE.md`
  - `MC_WATERLINE_GUIDE.md`
  - `MC_PERFORMANCE_GUIDE.md`

  Every README states that Unity owns water, waves, foam, reflections, fog, lighting, weather, terrain shaders, LODGroups, streaming, quality tiers and profiling.
- **Scripts** in `scripts/`: `mc_discover`, `mc_textures`, `mc_lib`, `mc_assets`, `mc_registry`, `mc_materials`, `mc_build`, `mc_qa`, `mc_render`, `mc_export`, `mc_validate`, `mc_package`.

#### 3. Asset library

##### Mountain (27 required, plus 4 extra one-sided transitions)

- **Streaming modules.** `Mountain_In / Run / Out_40m` and `Mountain_In / Out_20m` cover both sides.
  - Extra one-sided `Mountain_In / Out_L / _R_40m` modules exist for mixed compositions.
  - `MountainSlope_Low / Medium / Steep_A` (left) and `_B` (right) are M-class run variants. Low is softened; Steep adds a rock step above the bench.
- **Cliffs.** `MountainCliff_A / B / C` are 26–44 m faceted faces.
  - The facets come from Voronoi planes in three styles: broad, angular and diagonal-layered.
  - Each cliff has plan curvature (buttresses and gullies), an irregular crest, a crest shelf and a closed back, and tapered, buried ends.
- **Rock cuts.** `MountainRockCut_A` (left), `_B` (right) and `_C` (left, 16 m tall) are road-aligned 40 m overlays on the M-class cut slope.
  - A and B together make a two-sided cut.
  - The toe is buried in the ditch, and the ends fade into the slope.
- **Rocks.** `MountainTalus_A / B` are fans with boulders. `MountainScree_A / B` are polar fans with a sunken skirt. `MountainRockCluster_A / B / C` are faceted blocks.
- **Distance layers:**
  - Mid: `MountainRidge_A / B / C`, 100–500 m.
  - Mid / far: `MountainVista_A / B / C`.
  - Far: `MountainDistantRange_A / B`, 800 triangles each.

##### Coastal (22 required)

- **Streaming modules (sea on the right):**
  - `Coastal_In / Run / Out_40m` and `_In / Out_20m`: shoulder, sea cliff to the −18 m waterline, irregular toe shelf, sea floor down to −30 m.
  - `CoastalSlope_A / B / C`: low-coast In / Run / Out. Open land runs down to a sand beach at the waterline 100 m out.
  - `CoastalRockShore_A / B / C`: an outcrop shelf plus fallen blocks along the waterline; B adds a surge channel.
  - `CoastalPebbleBeach_A / B` and `CoastalSandStrip_A`: cove beaches below the cliff.
- **Stand-alone pieces:**
  - `CoastalCliff_A / B / C`: sea cliffs whose toe sits on the waterline and whose crest meets the shoulder.
  - `CoastalHeadland_A / B / C`: promontories rooted at the sea-cliff edge.
  - `CoastalRockStack_A / B`: blocky bedded stacks.
  - `CoastalIsland_A / B`, `CoastalVista_A / B` and `CoastalDistantLand_A` (4.2 km wide, 800 triangles).
- **Waterline references.** `Waterline`, `ShorelineReference`, `CoastalHorizon` and `SeaFloorReference` sit at one biome-wide level: z −18.0 Blender, y −18.0 Unity.
  - Every coastal module also has a `<Module>_Waterline` child.
  - The shoreline is irregular by construction and validated.

##### Overlooks, infrastructure and colliders

- **Overlooks.** `MountainOverlook_A` has a parapet and rail. `CoastalOverlook_A` has a cantilever deck, rail and brackets.
- **Infrastructure:**
  - `Mountain_RockfallFence_A / B` and `Mountain_DrainChannel_A`
  - `Coastal_CliffFence_A`, `Coastal_SeaWall_A` and `Coastal_RockBarrier_A`
  - No P1 prop was re-created. Guardrails and streetlights in QA are the linked P1 Props.
- **Colliders.** `Collision_MountainSlope`, `_MountainCliff`, `_CoastalCliff` and `_Overlook`, each under 300 triangles with no material.

#### 4. Key technical decisions

- **Seam system.** Each side has four boundary classes:
  - P: the frozen P1 Terrain_Flat + TerrainTransition row, exact.
  - M: mountain cut with ditch and bench.
  - C: sea cliff.
  - L: low coast.

  All streaming modules share per-side columns, so every end-class = start-class joint matches. 228 joints were checked, all under 1 mm. LOD1 / LOD2 columns are subsets of LOD0.
- **Road corridor.** Within |x| < 10.7 the terrain never rises above −0.289 m.
- **Snap points.** Snap_Start to Snap_End is exactly 40.000 m or 20.000 m.
- **Material policy.**
  - Terrain modules stay on the linked P1 `MAT_Terrain_Blend`. Rock, scree and the splash shelf are TerrainBlend channels, so no stair-stepped material borders appear beside the road.
  - MC rock goes on sheer faces away from the road, on stand-alone landforms and on all rock meshes.
  - Pebble and sand go only on beaches and the sea floor.
  - The P1 materials are linked by name and not re-authored.
- **Data compatibility.**
  - `TerrainBlend`: R grass, G soil, B rock, A gravel, normalised.
  - `VegetationMask` and UV1 `VegetationMaskUV`: U density, V dryness.
  - Coastal meshes add `MC_ShoreData`: wetness, foam proximity and submerged depth for Unity wet-shore and foam shading.
  - Vegetation density is ≤ 0.02 on cliffs, cuts, scree, rocks, beaches, the sea floor, the road zone and within 2 m above the waterline.
- **UVs.** All UVs are world-scaled: P1 planar 4 m on terrain, pebble and sand; box 8 m on rock; box 4 m on the rest.
- **LODs.** There are 71 LOD groups with strictly decreasing triangle counts. Coarse rock LODs are fitted to the LOD0 bounds, so major silhouettes stay within the larger of 0.6 m or 4% of the largest dimension.
- **Export.** In-memory axis bake (Blender (x, y, z) → Unity (−x, z, −y)), residual 4.8e-6. The export selection equals `MC_MASTER`. The QA content, preview water, cameras and lights were not exported.

#### 5. Triangle counts at LOD0 (guidance only, not padded)

| Category | Guidance | Delivered |
|---|---|---|
| Medium terrain module, per side | 3–12k | 4.8–11.1k |
| Near cliff / rock cut | 8–30k | 1.2–6.8k |
| Rock cluster / talus / stack | 1–6k | 1.0–2.4k |
| Ridge / headland / island / vista | 500–4k | 1.0–4.6k |
| Distant range / far land | hundreds to a few thousand | 800–1.0k |

The cliffs come in below the near-cliff guidance on purpose. Their big facets carry the silhouette, and the 2K fracture texture and normal map carry the detail. Nothing was padded to reach a number.

#### 6. QA

All three strips use the linked frozen P0 road, P1 Terrain open chunks, P1 guardrails and streetlights, P1 vegetation scattered from the VegetationMask, and the hypercar.
- **Mountain strip, 680 m:** Open → Mountain_In → rock cut (A + B with drain channel) → Run / Slopes with rockfall fence → cliff (MountainCliff_A + talus, MountainCliff_C) → overlook opening (Out_R, MountainOverlook_A, In_R) → RockCut_C → Mountain_Out → Open. Ridges, vistas and distant ranges fill the mid and far layers.
- **Coastal strip, 800 m:** Open → Coastal_In → cliff (CoastalCliff_A) → rocky shore with stacks → headland → rocky shore → pebble beach → CoastalOverlook_A with cliff fence → sand strip → rocky shore with CoastalCliff_B → pebble beach → Coastal_Out → low coast (CoastalSlope_A / B / C with sea wall and rock barrier) → Open. Islands, coastal vistas and distant land form the horizon.
- **Mixed strip, 400 m:** mountain side + highway + coastal drop (Mountain_In_L + Coastal_In … Mountain_Out_L + Coastal_Out, with CoastalCliff_C behind a pebble beach).
- **Cameras.** Each strip has driver, low chase, high chase, side cinematic and long-distance approach cameras, plus the 16 preview cameras.
- **Preview water.** `QA_PreviewWater_NOT_EXPORTED` exists in the QA collection only.

#### 7. Issues found and resolved during the phase

These were found in scratch iterations; the official checkpoints were written once, afterwards.

- **Cobblestone look.** The first rock textures read as cobblestones. They were redesigned with fragmented angular fractures, joint sets, facets and speckle. A bright salt spot that repeated with the tiling was removed.
- **Floating plates.** Square talus and scree aprons floated on slopes. They were rebuilt as polar fans with sunken skirts and tilted to the slope in QA. Ridge skirts were also placed below the ground.
- **Stair-stepped materials.** Per-face rock and scree materials on terrain modules made blocky patches. These moved into TerrainBlend channels.
- **Cliff shape.** Cliffs had overhanging lean, exposed crest shelves and wall-like plans. They now lean back and have plan curvature, a closed back and tapered shelves.
- **Rock-cut toe.** The toe gap and dark undercut slot are gone: the toe is buried and the facets ramp in above it.
- **Vegetation on edges.** Vegetation density on vertices bordering rock, scree, sand or pebble faces was set to no-grow.
- **LOD silhouettes.** Coarse rock LODs are fitted to the LOD0 bounds. Fence arms, sea-wall crests and overlook brackets are kept in every LOD.
- **Validator fixes.** Argument parsing and the relative-texture-path test were fixed. These were validator bugs, not data problems.

#### 8. Known limitations

- **Steep In / Out end faces.** In / Out modules rise from P class to the full M profile (up to 62 m at 200 m) within 40 m (20 m for the short variants). The far part of the transition is a steep rock end face. The front is wavy and spurred, but it reads as a cut mountain end from high aerial views. At gameplay height it reads as a mountain front. Frame it with spurs or ridges, or with Unity terrain.
- **P1 open chunks end at |x| 50 m.** Open chunks next to the biome need Unity far ground beyond that. QA used a preview ground plane and open-land strips.
- **LOD T-junctions.** LOD transitions between neighbouring modules at different LODs can show small T-junction cracks, because the coarser LODs use column subsets. The boundary rows themselves are identical. Use matching LODs per chunk or skirts in Unity.
- **No final water.** There is no water surface, waves, foam, reflection or underwater system (Unity owns these), and no decals. Wet shore is data only (`MC_ShoreData`).
- **Placement origins.** Coastal stand-alone pieces (stacks, islands, vistas, sea wall) are authored at absolute biome elevation, so place them with origin z = 0. Mountain cliffs must be sunk 1–2 m into the slope; where the slope behind is lower, the closed rock back is visible.
- **Preview renderer.** Previews are Eevee QA renders; final look and lighting are Unity's. Grazing-angle sparkle on the coastal-rock normal map shows in some previews.

#### 9. Freeze

`environment/P3_MountainCoastal/` is **FROZEN** (see `reports/P3_MC_FINAL_FREEZE.md`).

Per the instructions, work stops here. No other biome was started. City, Bridges, Tunnel, Terrain and Road were not modified, and Unity integration was not started.

---

### `UnityTransfer/README/MC_IMPORT_NOTES.md`

### P3 Mountain & Coastal - Import notes

**Unity owns** (not authored here, by design): water surface, waves, foam, reflections, underwater rendering, fog / atmospheric perspective, lighting, weather, terrain / rock / wet-shore shaders, LODGroup components, streaming, quality tiers and profiling. This package delivers geometry, vertex data, materials as source, LOD meshes, simple colliders and reference empties only.

#### Files (`FBX/`)
| FBX | Content |
|---|---|
| `mountainCoastal_complete.fbx` | everything below in one file (355 objects) |
| `MountainTerrain.fbx` | Mountain_In / Run / Out (40 m + 20 m, both sides), one-sided Mountain_In / Out_L / _R_40m, MountainSlope_Low / Medium / Steep_A (left) / _B (right) |
| `MountainCliffs.fbx` | MountainCliff_A / B / C (stand-alone faces), MountainRockCut_A / B / C (road-aligned 40 m overlays) |
| `MountainRocks.fbx` | MountainRockCluster_A / B / C, MountainTalus_A / B, MountainScree_A / B |
| `MountainVistas.fbx` | MountainRidge_A / B / C (mid), MountainVista_A / B / C (mid / far), MountainDistantRange_A / B (far) |
| `CoastalTerrain.fbx` | Coastal_In / Run / Out (40 m + 20 m), CoastalSlope_A / B / C (low coast In / Run / Out), CoastalCliff_A / B / C, CoastalHeadland_A / B / C, waterline reference empties |
| `CoastalShore.fbx` | CoastalRockShore_A / B / C, CoastalPebbleBeach_A / B, CoastalSandStrip_A (road-aligned 40 m variants), CoastalRockStack_A / B |
| `CoastalVistas.fbx` | CoastalIsland_A / B, CoastalVista_A / B, CoastalDistantLand_A |
| `MC_Infrastructure.fbx` | Mountain_RockfallFence_A / B, Mountain_DrainChannel_A, Coastal_CliffFence_A, Coastal_SeaWall_A, Coastal_RockBarrier_A, MountainOverlook_A, CoastalOverlook_A |
| `MC_Collision.fbx` | Collision_MountainSlope, Collision_MountainCliff, Collision_CoastalCliff, Collision_Overlook |

#### Import settings
- Scale 1 (1 unit = 1 m), *Convert Units* on, *Bake Axis Conversion* off (the axis bake is already in the mesh data; same convention as P0 / P1 / P2 / hypercar).
- Blender (x, y, z) -> Unity (-x, z, -y): road-aligned modules run from Unity z 0 (Snap_Start) to z +40 / +20 (Snap_End); driver-left (+X Blender) is Unity -X.
- Every asset is an empty root `<Asset>` with children `<Asset>_LOD0..2` (some 2 LODs). Build a LODGroup on the root in Unity (Unity owns LODGroups). Suggested screen-relative heights: LOD0 0.45, LOD1 0.18, LOD2 0.05; far vistas 0.25 / 0.03.
- Road-aligned modules carry `<Module>_Snap_Start` (0, 0, 0) and `<Module>_Snap_End` empties; coastal modules carry `<Module>_Waterline`.
- Import colliders from `MC_Collision.fbx` as MeshColliders (convex off), hide their renderers.

#### Vertex data (keep *Import vertex colours*, all colour sets)
- `TerrainBlend` colour set (LINEAR): R grass, G soil, B rock, A gravel - normalised, identical semantics to P1 Terrain.
- `VegetationMask` colour set: R density, G dryness, B 0, A 1; UV1 `VegetationMaskUV` = (density, dryness) - identical to P1.
- `MC_ShoreData` colour set (coastal meshes only): R wetness potential, G foam proximity, B submerged depth (0..8 m -> 0..1), A 1 - drives Unity wet-rock / wet-sand / foam shading.
- UV0 `UVMap`: world-scaled (P1 planar x / 4, -y / 4 on terrain / pebble / sand; box-projected 8 m rock, 4 m scree / concrete / metal).

#### Materials (`Textures/`)
| Material | Source |
|---|---|
| MAT_Terrain_Blend, MAT_Terrain_Concrete | frozen P1 Terrain materials (name reference; use the P1 Unity materials) |
| MAT_MC_MountainRock | `rock/T_MC_MountainRock_2K_*` tinted 0.58 / 0.57 / 0.55, box UV 8 m |
| MAT_MC_CoastalRock | `rock/T_MC_CoastalRock_2K_*`, box UV 8 m |
| MAT_MC_Scree | `ground/T_MC_Pebble_2K_*` tinted 0.78 / 0.74 / 0.68, box UV 4 m |
| MAT_MC_Pebble, MAT_MC_Sand | `ground/T_MC_Pebble_2K_*`, `ground/T_MC_Sand_2K_*`, planar 4 m |
| MAT_MC_Metal | flat galvanised steel (no texture): albedo 0.56 / 0.57 / 0.58, metallic 1, smoothness 0.55 |
Each texture set: BaseColor (sRGB), Normal (OpenGL +Y, set Unity type Normal map), Roughness (smoothness = 1 - roughness), AO.

---

### `UnityTransfer/README/MC_PLACEMENT_GUIDE.md`

### P3 Mountain & Coastal - Placement guide

**Unity owns** (not authored here, by design): water surface, waves, foam, reflections, underwater rendering, fog / atmospheric perspective, lighting, weather, terrain / rock / wet-shore shaders, LODGroup components, streaming, quality tiers and profiling. This package delivers geometry, vertex data, materials as source, LOD meshes, simple colliders and reference empties only.

#### Road-aligned streaming modules (snap to the P0 road)
Origin = road centre at Snap_Start (= the P0 Road_4Lane_40m origin of the same chunk). Span y 0 .. -L Blender (Unity z 0 .. +L). Width: from the P1 TerrainTransition inner edge (|x| 9.9 left / 11.9 right) to 200 m. Road stays straight and level; the corridor |x| < 10.7 never rises above -0.289 m.

Boundary classes per side (first / last 2 m of every module use the class profile exactly, so any end-class == start-class pair joins without a crack):
| Class | Profile (|x| -> z) |
|---|---|
| P | frozen P1 Terrain_Flat + TerrainTransition row (exact), beyond 50 m `-1.2 - 0.4 (a - 50) / 50` |
| M | mountain cut: ditch 13.6 (-0.92), cut face to the bench 23-26.5 (L 9.5-10.2 / R 8.0-8.6), slope to 55 (L 30 / R 23), 105 (46 / 40), 200 (62 / 56) |
| C | sea cliff: shoulder edge 24 (-1.25), cliff to the toe 44 (-18.35), shelf, sea floor to 200 (-30) |
| L | low coast: open land sloping to the beach / waterline at 100 m, sea floor to 200 (-28) |

| Module | Side | Start -> End |
|---|---|---|
| Mountain_In_40m / _20m | both | P -> M |
| Mountain_Run_40m | both | M -> M |
| Mountain_Out_40m / _20m | both | M -> P |
| Mountain_In_L / _R_40m, Mountain_Out_L / _R_40m | one side | P -> M / M -> P |
| MountainSlope_Low / Medium / Steep_A | left (+X Blender) | M -> M |
| MountainSlope_Low / Medium / Steep_B | right (-X Blender) | M -> M |
| Coastal_In_40m / _20m, Coastal_Run_40m, Coastal_Out_40m / _20m | right (sea side) | P -> C, C -> C, C -> P |
| CoastalRockShore_A / B / C, CoastalPebbleBeach_A / B, CoastalSandStrip_A | right | C -> C |
| CoastalSlope_A / B / C (low coast In / Run / Out) | right | P -> L, L -> L, L -> P |
| MountainRockCut_A (L) / _B (R) / _C (L, tall cut) | overlay | sits on an M-class chunk at the same origin; A + B on one chunk = two-sided cut |
| Mountain_DrainChannel_A | overlay | left M-class ditch lining at the same origin (rotate 180 deg about the module centre for the right) |

Example compositions (all validated in the QA scene):
- Mountain: Open, Mountain_In, Run + RockCut_A + RockCut_B, Slope_Medium_A | Slope_Medium_B, Slope_Steep_A | Slope_Low_B, Run, Slope_Medium_A | Mountain_Out_R, Slope_Low_A | open + MountainOverlook_A, Slope_Medium_A | open, Slope_Medium_A | Mountain_In_R, Run + RockCut_C, Mountain_Out, Open.
- Coastal (sea on the right): Open, Coastal_In, Run + CoastalCliff_A, RockShore_A + stacks, Run + CoastalHeadland_A, RockShore_B, PebbleBeach_A, Run + CoastalOverlook_A, SandStrip_A, RockShore_C + CoastalCliff_B, PebbleBeach_B, Coastal_Out, Open, CoastalSlope_A / B / C (+ sea wall), Open.
- Mixed (mountain | highway | coast): Mountain_In_L + Coastal_In, Slope_Medium_A + Coastal_Run, Slope_Steep_A + RockShore_A, Slope_Low_A + PebbleBeach_A (+ CoastalCliff_C), Slope_Medium_A + Coastal_Run, Mountain_Out_L + Coastal_Out.
- On the open side of one-sided chunks use P1 Terrain_Flat + TerrainTransition; P1 rows end at |x| 50 m, so Unity far ground is needed beyond.

#### Stand-alone pieces
| Asset | Origin / orientation |
|---|---|
| MountainCliff_A / B / C | base start of the face; face points +X Blender (use as-is on the right side, rotate 180 deg about Z on the left); runs along -Y; closed crest shelf + back so the piece reads as rock from any side; sink the base 1-2 m into the slope |
| CoastalCliff_A / B / C | toe start on the waterline; rotate 180 deg about Z on the sea (right) side, toe at |x| ~40, origin z = waterline (-18.0) |
| MountainTalus_A / B, MountainScree_A / B | fan apex at the cliff foot, fan spreads +X; tilt to the slope along the fan |
| MountainRockCluster_A / B / C | ground centre of the main block; sink 0.1-0.3 m |
| CoastalHeadland_A / B / C | landward root centre on the road datum, root edge at shoulder level; place at |x| 24.5 (sea-cliff edge), projects -X |
| CoastalRockStack_A / B, CoastalIsland_A / B, CoastalVista_A / B, CoastalDistantLand_A, Coastal_SeaWall_A | authored at absolute biome elevation (waterline -18.0): place origin at road datum z 0 |
| MountainRidge / Vista / DistantRange | footprint centre at base level; skirts sink 0.4 x height below the base; ridges 100-500 m, vistas 300 m-1 km, ranges 1.5-4 km |
| Rockfall fences, cliff fence, rock barrier | 8 m modules along -Y from the origin; repeat every 8 m |
| MountainOverlook_A / CoastalOverlook_A | 30 x 9 m platform, origin = road-side edge centre at z 0, view direction +X (rotate 180 deg on the right side); P1 Props supply guardrails / signs / lights |

#### Distance layers
Near 0-100 m: streaming modules, cliffs, rock cuts, rocks, shore, infrastructure. Mid 100-500 m: ridges, headlands, islands, MountainVista. Far 500 m-2 km+: MountainVista_B, CoastalVista, MountainDistantRange, CoastalDistantLand (<= 800 tris at LOD0).

---

### `UnityTransfer/README/MC_WATERLINE_GUIDE.md`

### P3 Mountain & Coastal - Waterline guide

**Unity owns** (not authored here, by design): water surface, waves, foam, reflections, underwater rendering, fog / atmospheric perspective, lighting, weather, terrain / rock / wet-shore shaders, LODGroup components, streaming, quality tiers and profiling. This package delivers geometry, vertex data, materials as source, LOD meshes, simple colliders and reference empties only.

- One biome-wide still-water level: **Blender z -18.0 = Unity y -18.0** (18 m below the road datum). Every coastal asset is authored against it.
- Reference empties (`CoastalTerrain.fbx`, collection MC_WATERLINE_REFERENCES): `Waterline` (0, 0, -18.0), `ShorelineReference` (-44, 0, -18.0: nominal C-class shoreline offset), `CoastalHorizon` (-5000, 0, -18.0: horizon direction / distance for the sea plane and fog), `SeaFloorReference` (-200, 0, -30). Every coastal streaming module has a `<Module>_Waterline` child at (0, -L/2, -18.0).
- Place the Unity water surface at the Waterline height. The shoreline is irregular by construction (toe shelf / bays / surge channel / coves / fallen blocks): the shoreline position varies 4.5-24.2 m along each 40 m module.
- Sea floor: SAND material below -18.6 m, continuing down to -26..-30 m at 200 m from the road, so the water has a depth gradient for absorption / colour.
- `MC_ShoreData` (coastal meshes): R wetness potential (1 at and below the waterline, fading out 0.3-2.5 m above it), G foam proximity (Gaussian, sigma 0.7 m around the waterline), B submerged depth (0..8 m -> 0..1), A 1. Use R for wet darkening / smoothness, G for shoreline foam masks, B for underwater tint; drive wave run-up offsets from the Unity water system.
- VegetationMask density is 0 within 2 m above the waterline, on beaches, sea floor, rocky shore, cliffs and rocks.
- The QA preview water (`QA_PreviewWater_NOT_EXPORTED`) existed only in the Blender QA scene and is not exported. No waves, foam, reflections, water shader or underwater system are part of this package.

---

### `UnityTransfer/README/MC_PERFORMANCE_GUIDE.md`

### P3 Mountain & Coastal - Performance guide

**Unity owns** (not authored here, by design): water surface, waves, foam, reflections, underwater rendering, fog / atmospheric perspective, lighting, weather, terrain / rock / wet-shore shaders, LODGroup components, streaming, quality tiers and profiling. This package delivers geometry, vertex data, materials as source, LOD meshes, simple colliders and reference empties only.

Triangle counts per LOD (LOD0 / LOD1 / LOD2). Budgets were treated as guidance only and nothing is padded. Both-side mountain modules contain two sides in one mesh.

| Asset | Triangles |
|---|---|
| CoastalCliff_A | 2,520 / 594 / 120 |
| CoastalCliff_B | 2,100 / 506 / 100 |
| CoastalCliff_C | 2,720 / 682 / 130 |
| CoastalDistantLand_A | 800 / 200 |
| CoastalHeadland_A | 3,600 / 900 / 240 |
| CoastalHeadland_B | 3,600 / 900 / 240 |
| CoastalHeadland_C | 3,600 / 900 / 240 |
| CoastalIsland_A | 968 / 242 |
| CoastalIsland_B | 968 / 242 |
| CoastalOverlook_A | 288 / 120 |
| CoastalPebbleBeach_A | 9,520 / 2,600 / 576 |
| CoastalPebbleBeach_B | 9,520 / 2,600 / 576 |
| CoastalRockShore_A | 11,120 / 3,176 / 828 |
| CoastalRockShore_B | 11,120 / 3,176 / 864 |
| CoastalRockShore_C | 11,120 / 3,176 / 900 |
| CoastalRockStack_A | 1,440 / 720 / 360 |
| CoastalRockStack_B | 1,440 / 720 / 360 |
| CoastalSandStrip_A | 9,520 / 2,600 / 576 |
| CoastalSlope_A | 9,520 / 2,600 / 576 |
| CoastalSlope_B | 9,520 / 2,600 / 576 |
| CoastalSlope_C | 9,520 / 2,600 / 576 |
| CoastalVista_A | 968 / 242 |
| CoastalVista_B | 968 / 242 |
| Coastal_CliffFence_A | 72 / 60 |
| Coastal_In_20m | 4,760 / 1,300 / 288 |
| Coastal_In_40m | 9,520 / 2,600 / 576 |
| Coastal_Out_20m | 4,760 / 1,300 / 288 |
| Coastal_Out_40m | 9,520 / 2,600 / 576 |
| Coastal_RockBarrier_A | 1,620 / 500 |
| Coastal_Run_40m | 9,520 / 2,600 / 576 |
| Coastal_SeaWall_A | 96 / 60 |
| MountainCliff_A | 4,824 / 1,080 / 208 |
| MountainCliff_B | 3,360 / 800 / 154 |
| MountainCliff_C | 6,776 / 1,540 / 300 |
| MountainDistantRange_A | 800 / 200 |
| MountainDistantRange_B | 800 / 200 |
| MountainOverlook_A | 180 / 72 |
| MountainRidge_A | 3,872 / 968 / 242 |
| MountainRidge_B | 3,872 / 968 / 242 |
| MountainRidge_C | 3,200 / 800 / 200 |
| MountainRockCluster_A | 1,296 / 400 / 144 |
| MountainRockCluster_B | 1,944 / 600 / 216 |
| MountainRockCluster_C | 972 / 300 / 108 |
| MountainRockCut_A | 1,300 / 308 / 80 |
| MountainRockCut_B | 1,200 / 264 / 80 |
| MountainRockCut_C | 2,200 / 440 / 100 |
| MountainScree_A | 816 / 216 / 60 |
| MountainScree_B | 816 / 216 / 60 |
| MountainSlope_Low_A | 10,480 / 2,840 / 624 |
| MountainSlope_Low_B | 9,520 / 2,600 / 576 |
| MountainSlope_Medium_A | 10,480 / 2,840 / 624 |
| MountainSlope_Medium_B | 9,520 / 2,600 / 576 |
| MountainSlope_Steep_A | 10,480 / 2,840 / 624 |
| MountainSlope_Steep_B | 9,520 / 2,600 / 576 |
| MountainTalus_A | 1,816 / 576 / 240 |
| MountainTalus_B | 2,416 / 792 / 348 |
| MountainVista_A | 4,608 / 1,152 / 288 |
| MountainVista_B | 4,608 / 1,152 / 288 |
| MountainVista_C | 3,872 / 968 / 242 |
| Mountain_DrainChannel_A | 160 / 16 |
| Mountain_In_20m | 10,000 / 2,720 / 600 |
| Mountain_In_40m | 20,000 / 5,440 / 1,200 |
| Mountain_In_L_40m | 10,480 / 2,840 / 624 |
| Mountain_In_R_40m | 9,520 / 2,600 / 576 |
| Mountain_Out_20m | 10,000 / 2,720 / 600 |
| Mountain_Out_40m | 20,000 / 5,440 / 1,200 |
| Mountain_Out_L_40m | 10,480 / 2,840 / 624 |
| Mountain_Out_R_40m | 9,520 / 2,600 / 576 |
| Mountain_RockfallFence_A | 360 / 108 |
| Mountain_RockfallFence_B | 360 / 108 |
| Mountain_Run_40m | 20,000 / 5,440 / 1,200 |

Guidance comparison (LOD0, per side): {"near cliff 8-30k": [1200, 6776], "medium terrain module 3-12k (per side)": [4760, 11120], "rock cluster 1-6k": [972, 2416], "far ridge 500-4k": [968, 4608], "distant mountain 100s-few k": [800, 968]}

Recommendations:
- Stream road-aligned modules per 40 m chunk with the P0 road; keep LOD0 within ~120 m, LOD1 to ~300 m, LOD2 beyond.
- Vistas / distant ranges / distant land are single coarse grids (<= 1 k tris at LOD0) meant to stay resident; batch them statically.
- Colliders: use `MC_Collision.fbx` (each < 300 tris) instead of render meshes. Stand-alone rocks / cliffs / stacks: use their LOD2 as a convex/mesh collider if gameplay needs it.
- All rock meshes share two 2 K texture sets; terrain shares the P1 MAT_Terrain_Blend: few materials, good batching. Quality tiers (texture size, LOD bias, vegetation density from VegetationMask) and profiling are Unity-side.

---

### `reports/P3_MC_materials_masks.md`

### P3 Mountain & Coastal — materials, TerrainBlend, VegetationMask, shore data

These are Blender source / preview materials, not Unity shaders. Unity owns terrain, rock, wet-shore and water shading. The data below is what the Unity shaders read.

#### Materials

| Material | Source | UV (`UVMap`) | Used on |
|---|---|---|---|
| `MAT_Terrain_Blend` | Frozen P1 Terrain, linked read-only (not re-authored) | P1 planar: U = x / 4, V = −y / 4 (4 m tile; tiles continuously with P1 Terrain) | All heightfield terrain: slopes, cut faces, benches, shoulders, splash shelf, headland / ridge / vista tops |
| `MAT_Terrain_Concrete` | Frozen P1 Terrain, linked read-only | Box, 4 m | Drain channel, sea wall, overlook platforms / parapets, fence footings |
| `MAT_MC_MountainRock` | `textures/rock/T_MC_MountainRock_2K_*`, tint (0.58, 0.57, 0.55), normal strength 0.9 | Box, 8 m | Mountain cliffs, rock cuts, rock clusters, talus boulders; sheer heightfield faces (normal z < 0.5) further than 40 m from the road |
| `MAT_MC_CoastalRock` | `textures/rock/T_MC_CoastalRock_2K_*`, normal strength 0.7 | Box, 8 m | Coastal cliffs, sea stacks, rock barrier, shore boulders; sheer heightfield faces further than 24 m from the road; headland / island cliffs |
| `MAT_MC_Scree` | `textures/ground/T_MC_Pebble_2K_*`, tint (0.78, 0.74, 0.68), normal strength 1.3 | Box, 4 m | Talus / scree aprons |
| `MAT_MC_Pebble` | `textures/ground/T_MC_Pebble_2K_*` | Planar, 4 m | Pebble beaches (C-class coves, Coastal_* shore band) |
| `MAT_MC_Sand` | `textures/ground/T_MC_Sand_2K_*` | Planar, 4 m | Sand strip / low-coast beach, sea floor below the waterline − 0.6 m |
| `MAT_MC_Metal` | Flat galvanised values, no texture | Box, 4 m | Rockfall fence posts / nets, cliff fence, overlook rails |

- `MAT_MC_DryRock` was not needed. Dryness is carried by `VegetationMask` G and `TerrainBlend`.
- `MAT_MC_WetShoreSource` was not needed either. Wet-shore support is a data channel (`MC_ShoreData`), not a Blender material.
- Each texture set has BaseColor (sRGB), Normal (OpenGL), Roughness and AO.
  - The four sets are procedural, deterministic and tileable (`scripts/mc_textures.py`). Tile sizes are recorded in `reports/P3_MC_textures.json`.
  - The rock sets have fragmented angular fractures, joint lines, broad facets and speckle, with no closed cell outlines.
- `textures/mountain`, `textures/coastal` and `textures/decals` hold README files only. Mountain and coastal assets use `textures/rock` and `textures/ground`. There are no decals: foam and wetness are Unity-side.

##### Material policy for heightfields

- Terrain modules stay on `MAT_Terrain_Blend`. Rock, scree and the splash shelf are `TerrainBlend` channels, so per-face material borders never stair-step across the visible slopes beside the road.
- Only four zones get their own material:
  - beaches (pebble or sand);
  - the submerged sea floor (sand);
  - sheer faces (normal z < 0.5) more than 40 m (mountain) or 24 m (coastal) from the road, which get MC rock;
  - stand-alone landforms, whose sheer faces get MC rock (box UV, no planar stretching on cliffs).
- Cliffs, rock cuts, rocks, stacks and aprons are separate MC rock meshes.

#### TerrainBlend (colour attribute, POINT, FLOAT_COLOR, render / export colour)

Channels: R grass, G soil, B rock, A gravel. Normalised: the sum is 1 and every channel is in 0..1, the same semantics as P1 Terrain.

| Zone | Rule |
|---|---|
| Rock meshes (MC rock material) | rock 0.85, gravel 0.05, soil 0.10. Upward tops (normal z ≥ 0.75): rock 0.45, gravel 0.10, soil 0.20, rest grass |
| Heightfield slopes | rock = smoothstep(0.22, 0.40, 1 − normal z). Fully rock above ≈ 53° |
| Coastal splash shelf | rock ≥ 1 − smoothstep(waterline + 1.5, waterline + 3.5, z), except on beaches |
| Scree band (M-class cut toe, \|x\| 15.5–23.5) | gravel = 0.85 × scree (continuous noise band; stronger on Run / Steep) |
| Beach | pebble beach: gravel 0.9. Sand beach: soil 0.9 |
| Sea floor | soil + 0.6 |
| Elsewhere | soil = 0.2 × steepness + 0.35 × noise. Grass is the remainder |

#### VegetationMask (colour attribute) + UV1 `VegetationMaskUV`

- R / U = density, G / V = dryness, B = 0, A = 1. UV1 is identical to the colour, the same as P1.
- **Density = grass × (1 − exclusion) × noise.** The exclusion is the maximum of:
  - steepness (smoothstep 0.30–0.42) and rock (smoothstep 0.35–0.55);
  - beach, scree and `nogrow` (cliffs, rock cuts, rocks, aprons, stacks, crest shelves);
  - road zone: 1 − smoothstep(15.5, 17.5, |x|) on road-aligned modules;
  - coastal: 1 − smoothstep(waterline + 2, waterline + 4, z).
- Infrastructure carries no terrain data. Vegetation there is excluded by placement.
- **Dryness:**
  - coastal: 0.55 base (salt / wind);
  - mountain: 0.30 base, plus up to 0.15 with altitude (20–70 m);
  - both: + 0.3 × steepness, + noise.

The validator checks that density is ≤ 0.02 on every cliff, rock cut, scree, talus, rock, beach and sea-floor face, on TerrainBlend rock (B > 0.55) or gravel (A > 0.6), in |x| < 15.5 and within 2 m above the waterline.

#### MC_ShoreData (coastal meshes only; colour attribute, POINT)

- R = wetness potential: 1 at and below the waterline, 1 − smoothstep(0.3, 2.5, z − waterline) above it.
- G = foam proximity: exp(−((z − waterline) / 0.7)²).
- B = submerged depth: clamp(−(z − waterline) / 8, 0, 1).
- A = 1.

Unity uses R for wet darkening and smoothness, G for shoreline foam masks, and B for underwater tint and absorption.

#### Waterline

One biome-wide still-water level at z −18.0 (Unity y −18.0), 18 m below the road datum. See `UnityTransfer/README/MC_WATERLINE_GUIDE.md`.

---

### `reports/P3_MC_FINAL_FREEZE.md`

### P3_MountainCoastal - FINAL FREEZE

Date: 2026-10-07 · Phase P3-BLENDER-01 · Status: **FROZEN**. Nothing under `environment/P3_MountainCoastal/` is to be edited; later phases may only link from it read-only.

#### Final deliverables
- **Final source blend:** `blend/mountainCoastal_07_export_ready.blend` (checkpoints `mountainCoastal_01_blockout` ... `_06_lods_collision` kept unchanged).
- **FBX (`exports/`, identical in `UnityTransfer/FBX/`):** `CoastalShore.fbx`, `CoastalTerrain.fbx`, `CoastalVistas.fbx`, `MC_Collision.fbx`, `MC_Infrastructure.fbx`, `MountainCliffs.fbx`, `MountainRocks.fbx`, `MountainTerrain.fbx`, `MountainVistas.fbx`, `mountainCoastal_complete.fbx`
- **Textures:** `textures/rock/T_MC_MountainRock_2K_*`, `T_MC_CoastalRock_2K_*`, `textures/ground/T_MC_Pebble_2K_*`, `T_MC_Sand_2K_*` (BaseColor / Normal / Roughness / AO); `textures/mountain`, `coastal`, `decals` hold README only.
- **Reports:** `reports/P3_MC_validation.txt`, `_geometry.json`, `_materials_masks.md`, `_export_manifest.json`, `_source_baseline.json`, `_source_integrity_check.md`, `_qa_sequence.json`, `_textures.json`, `_FINAL_FREEZE.md`, `_FINAL_REPORT.md`; `references/frozen_seam_rows.json`.
- **Previews:** 16 images in `previews/`.
- **UnityTransfer:** `UnityTransfer/` (FBX, Textures, Reports, README: `MC_IMPORT_NOTES.md`, `MC_PLACEMENT_GUIDE.md`, `MC_WATERLINE_GUIDE.md`, `MC_PERFORMANCE_GUIDE.md`).

#### Validation result
`reports/P3_MC_validation.txt`: **SUMMARY: 0 errors, 0 warnings**.
Source integrity: **PASS** (`reports/P3_MC_source_integrity_check.md`).

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P3_MC_validation.txt`

```text
== P3-BLENDER-01 PREMIUM MOUNTAIN & COASTAL HIGHWAY BIOME - VALIDATION ==
source blend/mountainCoastal_07_export_ready.blend; MC_MASTER 355 objects, 202 meshes (198 renderable, 4 colliders)

[PASS]  1. frozen source integrity: P0, P1 Props / Terrain / Vegetation / Tunnel, P2 Bridges / BridgeTerrainContext / City, vehicles and every other workspace file byte-identical to the pre-phase baseline; nothing added outside P3_MountainCoastal
[PASS]  2. mountain library: all 27 required assets (slopes Low / Medium / Steep A / B, cliffs, rock cuts, talus, scree, rock clusters, ridges, vistas, distant ranges) exist as LOD groups
[PASS]  3. coastal library: all 22 required assets (slopes, cliffs, rocky shore, pebble beaches, sand strip, headlands, rock stacks, islands, vistas, distant land) exist as LOD groups
[PASS]  4. In / Run / Out system: Mountain_In / Run / Out_40m + In / Out_20m and Coastal_In / Run / Out_40m + In / Out_20m exist (LOD0-2), plus one-sided Mountain_In / Out_L / _R_40m for mixed compositions
[PASS]  5. overlooks + biome infrastructure: MountainOverlook_A, CoastalOverlook_A, rockfall fences A / B, drain channel, cliff fence, sea wall, rock barrier exist; no P1 Props asset (guardrail, streetlight, sign, gantry, barrier) re-created
[PASS]  6. distance layers: near (0-100 m) modules / cliffs / rocks, mid (100-500 m) ridges + headlands + islands, far (500 m-2 km+) vistas + distant ranges; far meshes extremely efficient (<= 1,000 tris at LOD0, single coarse grid)
[PASS]  7. waterline system: Waterline / ShorelineReference / CoastalHorizon / SeaFloorReference empties present, Waterline + ShorelineReference + CoastalHorizon at the single biome waterline z -18.0 (Unity y -18.0), SeaFloorReference below it; every coastal streaming module carries a <name>_Waterline child at z -18.0; shorel...
[PASS]  8. preview water: QA_PreviewWater_NOT_EXPORTED exists only in MC_QA (preview of the waterline), is not in MC_MASTER; no wave / foam / reflection / underwater system authored (Unity owns water)
[PASS]  9. road stays straight and level: QA uses the LINKED frozen P0 road at z 0, no rotation, contiguous 40 m chunks on one x per strip; no road-aligned module vertex above -0.289 m (frozen P1 TerrainTransition level) inside the road corridor |x| < 10.7
[PASS] 10. seam safety: all 228 class-compatible end -> start joints between the 29 streaming terrain modules (classes P / M / C / L per side) have identical boundary rows (< 1 mm) on every shared column; every P-class boundary equals the frozen P1 Terrain_Flat + TerrainTransition profile; LOD1 / LOD2 boundary rows equal LOD0...
[PASS] 11. snap points: Snap_Start (root origin, road centre) -> Snap_End exactly 40.000 m (28 modules) / 20.000 m (4); every LOD spans exactly y 0 .. -L (overlays MountainRockCut_A / B / C included)
[PASS] 12. TerrainBlend compatible: colour attribute TerrainBlend (R grass, G soil, B rock, A gravel) on every terrain + rock mesh, normalised (sum 1, 0..1), render / export colour; infrastructure meshes carry none
[PASS] 13. VegetationMask compatible: VegetationMask colour (R density, G dryness) + UV1 VegetationMaskUV (U density, V dryness) identical, in 0..1
[PASS] 14. vegetation exclusions: density <= 0.02 on every cliff / rock cut / scree / talus / rock / beach / sea-floor face, on TerrainBlend rock (B > .55) or gravel (A > .6), in the road + shoulder + ditch zone |x| < 15.5 of road-aligned modules, and within 2 m above the waterline
[PASS] 15. wet-shore support for Unity: every coastal mesh carries MC_ShoreData (R wetness potential, G foam proximity, B submerged depth, A 1) derived from the waterline; no Blender-only wet shader
[PASS] 16. LODs: 71 LOD groups (slopes, cliffs, rock cuts, clusters, talus / scree, ridges, vistas, ranges, coastal modules, shore, headlands, stacks, islands, infrastructure), triangle counts strictly decreasing; major silhouette preserved (bounding box and top height within max(0.6 m, 4 % of the largest dimension) of LOD0)
[PASS] 17. colliders: Collision_MountainCliff / _MountainSlope / _CoastalCliff / _Overlook exist, simple (< 300 tris, no material), far simpler than the visuals
[PASS] 18. UVs: UVMap world-scaled on every face - P1 planar (U = x / 4, V = -y / 4) for MAT_Terrain_Blend / Pebble / Sand (tiles with P1 Terrain), box-projected 8 m (rock) / 4 m (scree, concrete, metal) for the rest; no stretched 0-1 UVs
[PASS] 19. materials: only ['MAT_MC_CoastalRock', 'MAT_MC_Metal', 'MAT_MC_MountainRock', 'MAT_MC_Pebble', 'MAT_MC_Sand', 'MAT_MC_Scree', 'MAT_Terrain_Blend', 'MAT_Terrain_Concrete']; P1 MAT_Terrain_Blend / MAT_Terrain_Concrete LINKED read-only (not re-authored); new MAT_MC_* use only the controlled T_MC_* texture set in textu...
[INFO] triangle guidance (LOD0, not padded; Both-side modules reported per side): {"near cliff 8-30k": [1200, 6776], "medium terrain module 3-12k (per side)": [4760, 11120], "rock cluster 1-6k": [972, 2416], "far ridge 500-4k": [968, 4608], "distant mountain 100s-few k": [800, 968]}
[PASS] 20. topology: no zero-area faces, no n-gons, consistent winding (no edge traversed twice in the same direction), no duplicate vertices in streaming modules, heightfield modules never face down; smooth shading with auto-sharp edges
[PASS] 21. QA strips on the LINKED P0 road with LINKED P1 Terrain open chunks, P1 props, P1 vegetation (scattered from VegetationMask) and the hypercar: mountain 680 m (Open > Mountain_In > rock cut > Run > cliff > overlook > Mountain_Out > Open), coastal 800 m (Open > Coastal_In > cliff > headland > rocky shore > overlook > ...
[PASS] 22. previews: all 16 required P3_MC_*.png renders exist in previews/
[PASS] 23. FBX export: the 10 required files written; export selection == MC_MASTER; no frozen P0 / P1 / P2 / vehicle object or mesh, no QA / preview water / camera / light / library object; frozen P1 materials referenced by NAME only
[PASS] 24. FBX clean re-import CoastalShore.fbx: 50 objects, names + hierarchy match, world deviation 4.8e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 25. FBX clean re-import CoastalTerrain.fbx: 84 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved; Unity +Y up / +Z forward (FBX mesh space): {"Coastal_In_20m": {"up_Y": [-30.0, -0.29], "forward_Z": [0.0,...
[PASS] 26. FBX clean re-import CoastalVistas.fbx: 15 objects, names + hierarchy match, world deviation 4.4e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 27. FBX clean re-import MC_Collision.fbx: 4 objects, names + hierarchy match, world deviation 2.3e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 28. FBX clean re-import MC_Infrastructure.fbx: 24 objects, names + hierarchy match, world deviation 4.8e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 29. FBX clean re-import MountainCliffs.fbx: 30 objects, names + hierarchy match, world deviation 4.9e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 30. FBX clean re-import MountainRocks.fbx: 28 objects, names + hierarchy match, world deviation 4.7e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 31. FBX clean re-import MountainTerrain.fbx: 90 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved; Unity +Y up / +Z forward (FBX mesh space): {"Mountain_Run_40m": {"up_Y": [-0.9, 64.08], "forward_Z": [-0...
[PASS] 32. FBX clean re-import MountainVistas.fbx: 30 objects, names + hierarchy match, world deviation 4.5e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved
[PASS] 33. FBX clean re-import mountainCoastal_complete.fbx: 355 objects, names + hierarchy match, world deviation 5.0e-04 m, triangles / UVMap / VegetationMaskUV / TerrainBlend / VegetationMask / MC_ShoreData / materials preserved; Unity +Y up / +Z forward (FBX mesh space): {"Mountain_Run_40m": {"up_Y": [-0.9, 64.08], "forwa...

Triangle budgets are guidance only (not padded); below-guidance assets are not warnings.
SUMMARY: 0 errors, 0 warnings
```

