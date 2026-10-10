# P1-BLENDER-02 + 02A — Terrain & Roadside Transition Kit (visual polish + final freeze)

Digest 03 of the environment handoff. Folder: `environment/P1_Terrain/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/terrain_09_final_frozen.blend`
- **Asset index source:** `reports/P1_terrain_02A_geometry.json` + `reports/P1_terrain_02A_export_manifest.json`
- **Checkpoints (9):** `terrain_01_blockout.blend`, `terrain_02_flat_transition.blend`, `terrain_03_cut_fill.blend`, `terrain_04_retaining_rocks.blend`, `terrain_05_materials_uv.blend`, `terrain_06_lods_collision.blend`, `terrain_07_export_ready.blend`, `terrain_08_visual_polish.blend`, `terrain_09_final_frozen.blend`
- **FBX (8):** `Terrain_Flat.fbx` (48 objects), `Terrain_Cut.fbx` (98 objects), `Terrain_Fill.fbx` (66 objects), `Terrain_Drainage.fbx` (20 objects), `Terrain_Retaining.fbx` (32 objects), `Terrain_Rocks.fbx` (71 objects), `Terrain_Vistas.fbx` (18 objects), `terrain_complete.fbx` (353 objects)
- **Textures:** 30 PNG files · **Previews:** 40 renders · **UnityTransfer README:** `TERRAIN_BLEND_GUIDE.md`, `TERRAIN_IMPORT_NOTES.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `Cliff_Module_A` | 2,240 / 1,119 / 448 / 179 | Terrain_Rocks.fbx |
| `Cliff_Module_B` | 2,378 / 1,188 / 475 / 189 | Terrain_Rocks.fbx |
| `Cliff_Module_C` | 2,204 / 1,101 / 440 / 175 | Terrain_Rocks.fbx |
| `RetainingWall_20m` | 400 / 70 | Terrain_Retaining.fbx |
| `RetainingWall_4m` | 80 / 14 | Terrain_Retaining.fbx |
| `RetainingWall_8m` | 160 / 28 | Terrain_Retaining.fbx |
| `RetainingWall_End` | 128 / 33 | Terrain_Retaining.fbx |
| `RetainingWall_End_Mirror` | 128 / 33 | Terrain_Retaining.fbx |
| `RetainingWall_Tiered` | 320 / 56 | Terrain_Retaining.fbx |
| `RockCluster_A` | 480 / 240 / 96 / 38 | Terrain_Rocks.fbx |
| `RockCluster_B` | 800 / 400 / 160 / 64 | Terrain_Rocks.fbx |
| `RockCut_A` | 1,584 / 791 / 316 / 126 | Terrain_Rocks.fbx |
| `RockCut_B` | 1,408 / 704 / 280 / 112 | Terrain_Rocks.fbx |
| `RockCut_C` | 1,944 / 972 / 387 / 154 | Terrain_Rocks.fbx |
| `Rock_A` | 80 / 40 / 16 | Terrain_Rocks.fbx |
| `Rock_B` | 80 / 40 / 16 | Terrain_Rocks.fbx |
| `Rock_C` | 320 / 160 / 64 / 24 | Terrain_Rocks.fbx |
| `Rock_D` | 320 / 160 / 64 / 24 | Terrain_Rocks.fbx |
| `Rock_E` | 320 / 160 / 64 / 24 | Terrain_Rocks.fbx |
| `Rock_F` | 320 / 160 / 64 / 24 | Terrain_Rocks.fbx |
| `TerrainTransition_L_20m` | 880 / 20 | Terrain_Flat.fbx |
| `TerrainTransition_L_40m` | 1,760 / 40 | Terrain_Flat.fbx |
| `TerrainTransition_R_20m` | 560 / 20 | Terrain_Flat.fbx |
| `TerrainTransition_R_40m` | 1,120 / 40 | Terrain_Flat.fbx |
| `Terrain_CutWall_L_40m` | 2,400 / 720 / 240 | Terrain_Cut.fbx |
| `Terrain_CutWall_R_40m` | 2,400 / 720 / 240 | Terrain_Cut.fbx |
| `Terrain_Cut_Both_40m` | 4,320 / 1,360 / 400 | Terrain_Cut.fbx |
| `Terrain_Cut_Low_L_40m` | 2,160 / 640 / 180 | Terrain_Cut.fbx |
| `Terrain_Cut_Low_R_40m` | 2,160 / 640 / 180 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_L_40m` | 2,160 / 680 / 200 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_L_In_20m` | 1,080 / 340 / 100 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_L_Out_20m` | 1,080 / 340 / 100 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_L_Run_40m` | 2,160 / 680 / 200 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_R_40m` | 2,160 / 680 / 200 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_R_In_20m` | 1,080 / 340 / 100 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_R_Out_20m` | 1,080 / 340 / 100 | Terrain_Cut.fbx |
| `Terrain_Cut_Medium_R_Run_40m` | 2,160 / 680 / 200 | Terrain_Cut.fbx |
| `Terrain_Ditch_L_40m` | 2,160 / 640 / 180 | Terrain_Drainage.fbx |
| `Terrain_Ditch_R_40m` | 2,160 / 640 / 180 | Terrain_Drainage.fbx |
| `Terrain_Fill_Both_40m` | 4,480 / 1,280 / 320 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_L_40m` | 2,080 / 640 / 180 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_L_In_20m` | 1,040 / 320 / 90 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_L_Out_20m` | 1,040 / 320 / 90 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_L_Run_40m` | 2,080 / 640 / 180 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_R_40m` | 2,080 / 640 / 180 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_R_In_20m` | 1,040 / 320 / 90 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_R_Out_20m` | 1,040 / 320 / 90 | Terrain_Fill.fbx |
| `Terrain_Fill_Medium_R_Run_40m` | 2,080 / 640 / 180 | Terrain_Fill.fbx |
| `Terrain_Fill_Shallow_L_40m` | 2,240 / 640 / 160 | Terrain_Fill.fbx |
| `Terrain_Fill_Shallow_R_40m` | 2,240 / 640 / 160 | Terrain_Fill.fbx |
| `Terrain_Flat_L_20m` | 1,000 / 260 / 50 | Terrain_Flat.fbx |
| `Terrain_Flat_L_40m` | 2,000 / 520 / 100 | Terrain_Flat.fbx |
| `Terrain_Flat_R_20m` | 1,000 / 260 / 50 | Terrain_Flat.fbx |
| `Terrain_Flat_R_40m` | 2,000 / 520 / 100 | Terrain_Flat.fbx |
| `Terrain_RockCut_L_40m` | 2,320 / 720 / 220 | Terrain_Cut.fbx |
| `Terrain_RockCut_R_40m` | 2,320 / 720 / 220 | Terrain_Cut.fbx |
| `Vista_DistantMountain_A` | 1,920 / 480 | Terrain_Vistas.fbx |
| `Vista_FarGround_A` | 640 / 72 | Terrain_Vistas.fbx |
| `Vista_Hills_A` | 1,152 / 288 | Terrain_Vistas.fbx |
| `Vista_Hills_B` | 1,152 / 288 | Terrain_Vistas.fbx |
| `Vista_Hills_C` | 800 / 200 | Terrain_Vistas.fbx |
| `Vista_Ridge_A` | 1,024 / 256 | Terrain_Vistas.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `Terrain_Cut.fbx` (38): Collision_Terrain_CutWall_L_40m (120), Collision_Terrain_CutWall_R_40m (120), Collision_Terrain_Cut_Low_L_40m (90), Collision_Terrain_Cut_Low_R_40m (90), Collision_Terrain_Cut_Medium_L_40m (100), Collision_Terrain_Cut_Medium_R_40m (100), Collision_Terrain_RockCut_L_40m (110), Collision_Terrain_RockCut_R_40m (110), Terrain_CutWall_L_40m_Snap_End, Terrain_CutWall_L_40m_Snap_Start, Terrain_CutWall_R_40m_Snap_End, Terrain_CutWall_R_40m_Snap_Start, Terrain_Cut_Both_40m_Snap_End, Terrain_Cut_Both_40m_Snap_Start, Terrain_Cut_Low_L_40m_Snap_End, Terrain_Cut_Low_L_40m_Snap_Start, Terrain_Cut_Low_R_40m_Snap_End, Terrain_Cut_Low_R_40m_Snap_Start, Terrain_Cut_Medium_L_40m_Snap_End, Terrain_Cut_Medium_L_40m_Snap_Start, Terrain_Cut_Medium_L_In_20m_Snap_End, Terrain_Cut_Medium_L_In_20m_Snap_Start, Terrain_Cut_Medium_L_Out_20m_Snap_End, Terrain_Cut_Medium_L_Out_20m_Snap_Start, Terrain_Cut_Medium_L_Run_40m_Snap_End, Terrain_Cut_Medium_L_Run_40m_Snap_Start, Terrain_Cut_Medium_R_40m_Snap_End, Terrain_Cut_Medium_R_40m_Snap_Start, Terrain_Cut_Medium_R_In_20m_Snap_End, Terrain_Cut_Medium_R_In_20m_Snap_Start, Terrain_Cut_Medium_R_Out_20m_Snap_End, Terrain_Cut_Medium_R_Out_20m_Snap_Start, Terrain_Cut_Medium_R_Run_40m_Snap_End, Terrain_Cut_Medium_R_Run_40m_Snap_Start, Terrain_RockCut_L_40m_Snap_End, Terrain_RockCut_L_40m_Snap_Start, Terrain_RockCut_R_40m_Snap_End, Terrain_RockCut_R_40m_Snap_Start
- `Terrain_Drainage.fbx` (12): Culvert_Box (60), Culvert_Concrete_Round (108), Terrain_Ditch_Deep_4m (56), Terrain_Ditch_Deep_4m_Snap_End, Terrain_Ditch_Deep_4m_Snap_Start, Terrain_Ditch_L_40m_Snap_End, Terrain_Ditch_L_40m_Snap_Start, Terrain_Ditch_R_40m_Snap_End, Terrain_Ditch_R_40m_Snap_Start, Terrain_Ditch_Shallow_4m (56), Terrain_Ditch_Shallow_4m_Snap_End, Terrain_Ditch_Shallow_4m_Snap_Start
- `Terrain_Fill.fbx` (22): Terrain_Fill_Both_40m_Snap_End, Terrain_Fill_Both_40m_Snap_Start, Terrain_Fill_Medium_L_40m_Snap_End, Terrain_Fill_Medium_L_40m_Snap_Start, Terrain_Fill_Medium_L_In_20m_Snap_End, Terrain_Fill_Medium_L_In_20m_Snap_Start, Terrain_Fill_Medium_L_Out_20m_Snap_End, Terrain_Fill_Medium_L_Out_20m_Snap_Start, Terrain_Fill_Medium_L_Run_40m_Snap_End, Terrain_Fill_Medium_L_Run_40m_Snap_Start, Terrain_Fill_Medium_R_40m_Snap_End, Terrain_Fill_Medium_R_40m_Snap_Start, Terrain_Fill_Medium_R_In_20m_Snap_End, Terrain_Fill_Medium_R_In_20m_Snap_Start, Terrain_Fill_Medium_R_Out_20m_Snap_End, Terrain_Fill_Medium_R_Out_20m_Snap_Start, Terrain_Fill_Medium_R_Run_40m_Snap_End, Terrain_Fill_Medium_R_Run_40m_Snap_Start, Terrain_Fill_Shallow_L_40m_Snap_End, Terrain_Fill_Shallow_L_40m_Snap_Start, Terrain_Fill_Shallow_R_40m_Snap_End, Terrain_Fill_Shallow_R_40m_Snap_Start
- `Terrain_Flat.fbx` (20): Collision_TerrainTransition_L_40m (20), Collision_TerrainTransition_R_40m (20), Collision_Terrain_Flat_L_40m (50), Collision_Terrain_Flat_R_40m (50), TerrainTransition_L_20m_Snap_End, TerrainTransition_L_20m_Snap_Start, TerrainTransition_L_40m_Snap_End, TerrainTransition_L_40m_Snap_Start, TerrainTransition_R_20m_Snap_End, TerrainTransition_R_20m_Snap_Start, TerrainTransition_R_40m_Snap_End, TerrainTransition_R_40m_Snap_Start, Terrain_Flat_L_20m_Snap_End, Terrain_Flat_L_20m_Snap_Start, Terrain_Flat_L_40m_Snap_End, Terrain_Flat_L_40m_Snap_Start, Terrain_Flat_R_20m_Snap_End, Terrain_Flat_R_20m_Snap_Start, Terrain_Flat_R_40m_Snap_End, Terrain_Flat_R_40m_Snap_Start
- `Terrain_Retaining.fbx` (14): Collision_RetainingWall_20m (12), Collision_RetainingWall_4m (12), Collision_RetainingWall_8m (12), RetainingWall_20m_Snap_End, RetainingWall_20m_Snap_Start, RetainingWall_4m_Snap_End, RetainingWall_4m_Snap_Start, RetainingWall_8m_Snap_End, RetainingWall_8m_Snap_Start, RetainingWall_CornerVisual (80), RetainingWall_End_Snap_End, RetainingWall_End_Snap_Start, RetainingWall_Tiered_Snap_End, RetainingWall_Tiered_Snap_Start
- `Terrain_Rocks.fbx` (3): Collision_RockCut_A (12), Collision_RockCut_B (12), Collision_RockCut_C (12)

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `UnityTransfer/README/TERRAIN_IMPORT_NOTES.md`

### Terrain & Roadside Transition Kit (P1-BLENDER-02, polished by P1-BLENDER-02A) — Unity import notes

> **P1-BLENDER-02A terrain polish applied.** FBX files, textures, `Reports/P1_terrain_02A_*` and this note are the final frozen versions
> (`blend/terrain_09_final_frozen.blend`). File names, hierarchy, LOD suffixes, snap points, 40/20 m lengths, seam rules, TerrainBlend / VegetationMask
> conventions and colliders are **unchanged** from P1-BLENDER-02. The pre-polish exports are archived in `exports/_pre_02A/` (not part of this package).

#### What the 02A polish changed
- **Rock cuts / cliffs** (`RockCut_A/B/C`, `Cliff_Module_A/B/C`): rebuilt LOD0-LOD3 as fractured rock masses with a distinct silhouette per variant (no repeated horizontal slabs).
  Triangles: RockCut_A 1584 / 791 / 316 / 126, Cliff_Module_A 2240 / 1119 / 448 / 179 (about +20 % vs 02). Rock vertices now carry a soil/gravel toe in TerrainBlend (G 0-0.3, A 0-0.22) and stay B-dominant above 1.2 m.
- **Road-edge transition**: `TerrainTransition_*` LOD0 is now 1760 triangles (0.25 m columns, was 240-320). The gravel strip is irregular (0.05-0.96 m wide, mean about 0.35 m) with soil / grass mixing; the type bands' gravel is noisy and narrower.
  TerrainBlend A (gravel) is therefore no longer a constant strip; do not assume a fixed width in Unity.
- **Flat terrain**: `Terrain_Flat_*` LOD0 2000 (40 m); per-module mounds / depressions / drainage channels (±0.1-0.35 m in the type band, none in the d < 21 prop corridor or the 2 m seam zones). All other type modules +240 triangles at LOD0; LOD1 / LOD2 unchanged.
- **Textures** (same names and tile sizes): Grass is muted with straw / lush / soil patches; Rock has no horizontal strata; Gravel is darker; `T_Terrain_MacroVariation_1K` is a 3-octave R tone / G dryness / B wetness mask (sample it at 64 m **and** a second scale of about 21 m for best results).
- **VegetationMask** (UV1 / colour set 1): density is lower on soil patches and gravel; still 0 for d < 16.5, transitions, rock and gravel-heavy ground.
- The single QA scene change you may notice: the 02A preview shows the macro mask used at two scales; that is a Blender preview only.

---


> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.**
> **UNITY TERRAIN MATERIALS, PREFABS, ROADSTREAMER PLACEMENT, VEGETATION SYSTEMS, CULLING, HLOD, FOG AND PERFORMANCE TESTING MUST BE
> COMPLETED ON THE UNITY WORKSTATION.**
> Nothing here has been opened in Unity. Every number was measured in Blender, including a re-import of every FBX into an empty scene
> (`Reports/P1_terrain_validation.txt`, 0 errors).

#### 1. Source phase
Third Blender environment phase, after P0 Road Foundation (road kit) and P1 Props. Both were only *linked read-only* for scale and clearance.
This package contains **terrain only**: no road, no props, no vegetation.

#### 2. Unity orientation
Same method as the hypercar, P0 and P1: in-memory axis bake, Apply Transform OFF. Blender +Z up / road toward -Y / driver-left +X
becomes Unity **+Y up / +Z forward**, X mirrored by the importer: point (x, y, z) -> (-x, z, -y).
**`_L` = vehicle left = Blender +X = Unity -X. `_R` = vehicle right = Blender -X = Unity +X.** Importer: Scale Factor 1, Convert Units ON,
Bake Axis Conversion OFF, Normals Import, Tangents Calculate, Read/Write ON only if you need runtime colour access, Generate Colliders OFF.

#### 3. Scale / 4. module lengths
1 unit = 1 m. Terrain strips are exactly **40.000 m** or **20.000 m**, running from Unity z 0 to z +40 (+20) from the chunk origin
(road centreline, y 0). Place every terrain module at the **same position as its road chunk**. Every one carries `<Asset>_Snap_Start` (0,0,0) and `_Snap_End` (0,0,L).

#### 5. Terrain width / 6. road-edge transition / 7. ground level
Per side: transition corridor + 34 m shaped band = about 38-40 m outside the road kit, ending at **d 50 m** from the centreline, then
`Vista_FarGround_A` takes over at the same height (d 50, y -1.2) out to 1.5 km.

| Zone (d = distance from centreline) | Asset | Height (y) |
|---|---|---|
| right verge outer edge 12.0-12.4, left 10.0-10.5 | (P0 kit) | -0.30 |
| **Transition** R 11.9-16, L 9.9-16 | `TerrainTransition_R/L_*` | -0.30 → -0.29 → **-0.32**; starts under the verge's ragged edge, so there is no gap or green straight line |
| **Type band** 16-50 | `Terrain_*` | begins at -0.32 (drained toe) and returns to -1.2 at d 50 |
| far ground 50-1500 | `Vista_FarGround_A` | -1.2 + low swell |

Base ground is **-0.30 m** relative to the gameplay road. The prop corridor (d 12-16) is level at -0.29...-0.32, so P1 streetlights
(base -0.30 at d 12), signs (d 12.8), CCTV (14) and gantry plinths sit on the terrain. The guardrail (d 11, on the verge) is not covered by terrain.

#### 8. Terrain types (each exists for L and R; `Both` = L and R in one mesh)
| Type | Peak above road | Notes |
|---|---|---|
| `Terrain_Flat_*_40m / _20m` | ±0.1 | gentle undulation, 0.6 m noise, fades to 0 at the seams |
| `Terrain_Cut_Low_*` | +2.4...+3.0 m | 1:2.4 slope after a drained toe |
| `Terrain_Cut_Medium_*` (self / Run / In / Out) | +5.4...+6.3 m | `Run` = full section at both ends; `In` = B0→full, `Out` = full→B0 (20 m) |
| `Terrain_RockCut_*` | +7.0...+7.9 m | steep (~76°) slope, **designed to carry `RockCut_*` / `Cliff_Module_*`** |
| `Terrain_CutWall_*` | +2.9...+5.9 m | a near-vertical 3 m toe face at d 18.2-18.8 (seat a `RetainingWall_*` against it), then a 1:2 → 1:4 slope |
| `Terrain_Fill_Shallow_*` | -2.3...-2.5 m | embankment 1:2.4, crest/shoulder at d 21.6 |
| `Terrain_Fill_Medium_*` (self / Run / In / Out) | -4.6...-4.8 m | |
| `Terrain_Ditch_*_40m` | -0.8 m V-ditch at d 18-19.8 | meets the P0 drain; **do not duplicate P0 `Drain_Channel_4m`** |
| `Terrain_Ditch_Shallow_4m / _Deep_4m` | 0.4 / 1.0 m deep | local 4 m inserts (origin = ditch centreline), for authoring custom drainage |
| `Culvert_Concrete_Round / _Box` | headwall 3.0 × 1.6 m | origin = ground at the front-face centre, outlet looks +Y (Blender) |

**Seam rule:** the first and last 2 m of every module equal a standard boundary profile exactly (no noise, constant along Y), so *any* self-contained
module can follow any other: Flat, Cut_Low, Cut_Medium, RockCut, CutWall, Fill_*, Ditch and Transition all begin and end with the same standard profile. `Run` modules
chain with `In`/`Out`; mix freely. The Blender seam tests (Flat + Cut + Flat + Fill + RockCut + Ditch, and In + Run + Run + Out + Flat) show 0.000 m gaps.

#### 9. FBX files
| File | Contents |
|---|---|
| `Terrain_Flat.fbx` | flat + transition (40/20 m, L/R) |
| `Terrain_Cut.fbx` | all cut modules: Low, Medium (self/Run/In/Out), RockCut, CutWall, Both |
| `Terrain_Fill.fbx` | all fill modules, Both |
| `Terrain_Drainage.fbx` | ditch strips, 4 m inserts, culverts |
| `Terrain_Retaining.fbx` | retaining walls 4/8/20 m, end (+mirror), corner, tiered |
| `Terrain_Rocks.fbx` | rock cuts, cliffs, 6 rocks, 2 clusters |
| `Terrain_Vistas.fbx` | 5 vistas + far ground |
| `terrain_complete.fbx` | everything (353 objects) — use *either* the split files or this one |

#### 10. LOD naming
`<Asset>` empty → `<Asset>_LOD0..n` (+ `Collision_*` + `Snap_*`) → Unity builds a LOD Group from the suffixes. Single-LOD assets (`Terrain_Ditch_*_4m`, culverts, `RetainingWall_CornerVisual`) are plain meshes.
Terrain strips: LOD0 1 m rows (1.8-2.2 k tris) / LOD1 2 m rows (520-720) / LOD2 4 m rows (100-250). **Every LOD shares the module boundary polyline** (end rows equal, breakpoint columns kept), so neighbouring modules at different LODs show no cracks.
Rocks / cliffs: 100 / 50 / 20 / 8 %. Vistas: 2 levels. Walls: 2 levels. Suggested LOD Group screen heights: strips 30 / 10 / 3 %, rock cuts 40 / 15 / 5 / 1 %.

#### 11-12. Materials and textures
`MAT_Terrain_Blend` (all terrain strips + ditch inserts), `MAT_Terrain_Rock` (rocks, cliffs, distant mountain), `MAT_Terrain_Grass` / `MAT_Terrain_DryGrass` (far ground, vistas),
`MAT_Terrain_Concrete` (walls + culverts; **P1 trim sheet, concrete strip**; not duplicated here), `MAT_Terrain_Soil` and `MAT_Terrain_Gravel` (layer sources of the blend material).
Textures are in `Textures/{grass,soil,rock,gravel,masks}`; tile sizes and channel maps are in **`TERRAIN_BLEND_GUIDE.md`**. Normals are OpenGL; roughness must be inverted for URP smoothness.
The FBX auto-links nothing; assign layer textures to a Unity material by hand.

#### 13-14. Vertex data
**TerrainBlend** = colour set 0 (R grass, G soil, B rock, A gravel, sum = 1). **VegetationMask** = colour set 1 (DCC) *and* UV channel 1 (Unity `uv2`: U density, V dryness).
Full details in `TERRAIN_BLEND_GUIDE.md`.

#### 15. Colliders (18)
Simple, material-free, parented prisms or heightfields (8 m grid), kept to ≤ 25 % of LOD0 triangles:
`Collision_Terrain_Flat_L/R_40m` (50 tris), `Collision_TerrainTransition_L/R_40m` (20), `Collision_Terrain_Cut_Low/Medium/RockCut/CutWall_L/R_40m` (90-120),
`Collision_RetainingWall_4m/8m/20m` (12, box), `Collision_RockCut_A/B/C` (12, box). **No fill or ditch colliders.** The road collider is P0's. If gameplay never allows cars off the road,
use none of them. Add MeshCollider (non-convex for strips, Convex for boxes) and disable the collider MeshRenderer.

#### 16. Snap points / origins
Terrain strips, transitions: chunk origin (Blender (0,0,0); `_Snap_End` at -L m). Retaining walls: origin = **toe of the traffic face at the start**; the face looks Blender +X; walls run Y 0 → -L; place on the right side facing the road,
rotate 180° about Z (Unity Y) for the left. `RetainingWall_End` steps down 3.0 → 0.85 m over 3 m (`_End_Mirror` steps the other way). Rocks and cliffs: bottom-centre origin; rock faces look +X (toward the road on the right side).
Vistas, far ground: ground-centre origin; the viewer side is -Y.

#### 17. Expected instancing
Rocks, clusters, culverts, wall pieces and ditch inserts are instanced props. Place them on the terrain and rotate freely. Terrain modules are placed once per road chunk and are never instanced.
Rocks are Y-up with a flat bearing face; sink them 5-10 cm.

#### 18. Expected RoadStreamer relationship
One terrain object per side per road chunk (40 m) or half-chunk (20 m), spawned and recycled with the road chunk; choose the type from a sequence table
(Flat → Cut_Low → Cut_Medium → Flat → Fill_Shallow → Fill_Medium …). For long cuts and fills use `Run`, entered by `In` and left by `Out`. Props (guardrail, lights, gantry) are placed separately from the P1 package.
Nothing here changes road height or alignment.

#### 19. Vista usage
`Vista_Hills_A/B/C` (hundreds of metres), `Vista_Ridge_A`, `Vista_DistantMountain_A` (kilometres), `Vista_FarGround_A` (always, centred on the road). They are **not** part of chunks: place them once per level and
**recentre them on the camera in z** (not x) so the road always has a horizon; fade them with fog / HLOD. Vista LOD0 total ≈ 6.0 k tris (hills, ridge, mountain) + 640 for the far ground. Do not scale them.
The QA scene placed hills at 140-1200 m, a ridge at 1.7 km and the mountain at 2.9 km from the road.

#### 20. Excluded QA content
Not in any FBX: the linked P0 road strips, linked P1 props, hypercar reference, both QA terrain sequences (240 m and 140 m), the library rows, the QA corridor filler and QA ground, all cameras, and the preview lights / world (unsaved render session).
Only `TERRAIN_MASTER` is exported; the full list is in `Reports/P1_terrain_export_manifest.json`.

---

### `UnityTransfer/README/TERRAIN_BLEND_GUIDE.md`

### Terrain blend data — TerrainBlend / VegetationMask guide

One convention for every terrain mesh. The data is stored in the vertices, not in a Blender-only procedural material.

#### TerrainBlend (vertex colour set 0, LINEAR float; this is the colour Unity imports as `mesh.colors`)

| Channel | Meaning | Typical use |
|---|---|---|
| **R** | grass weight | gentle slopes, field, verge-side lawn |
| **G** | soil weight | steep earth (up to ~0.8), noise patches, exposed embankment faces |
| **B** | rock weight | steep surfaces of cut modules above Z 1 m (`Terrain_Cut_*`, `RockCut`, `CutWall`) |
| **A** | gravel weight | the road-edge strip: since 02A an *irregular* band (width 0.05-0.96 m, mixed with soil/grass), plus ditch beds, fill-crest shoulders, and a thin toe on rock meshes (0-0.22) |

R + G + B + A = **1.0** on every vertex (validated). Rocks, cliffs and boulders carry the constant (0, 0, 1, 0).
Blend as `lerp` chains or a weighted sum; do not renormalise. In URP Shader Graph, read the Vertex Color node and split R/G/B/A.

The FBX stores this set as 8-bit corner colours. The re-import check shows a maximum error of 0.002 (half a byte step); treat it as 8-bit data.
Blender's byte colour `.color` is displayed through a colour-space conversion. The raw stored bytes (`color_srgb`) are the correct weights.

#### VegetationMask (the next phase's placement data)

| Channel | Meaning |
|---|---|
| **R** | vegetation density 0-1 (0 = never place) |
| **G** | dryness 0-1 (0 lush, 1 dry; drives grass vs dry-grass choice) |
| **B** | reserved, 0 |
| **A** | 1 |

Density is 0 inside the prop corridor (d < 16.5 m from the road centreline, so on road, shoulders, drain, verge, guardrail,
streetlight bases, gantry plinths and signs), on every transition module, on rock (TerrainBlend B > 0.7) and on gravel.
It ramps to full over d 16.5-19.5 and falls to 0.5 on steep ground.

**Unity delivery.** Unity imports one vertex-colour set. VegetationMask is therefore stored **twice**:
1. as colour set 1 in the FBX (visible in DCC tools, ignored by Unity), and
2. as **UV channel 1 (`VegetationMaskUV`, Unity `mesh.uv2`): U = density, V = dryness**. Read this one in Unity. It interpolates
   per vertex, so sample it in the vertex or fragment stage, or bake it into a splat texture for placement.
The ditch inserts carry the same two sets in local space (density rises toward the bank edge).

#### Texture sources (`Textures/`, 2048², tileable; normals OpenGL, no flip; roughness is *roughness*, so invert for URP smoothness)

| Layer | Folder | Metres per tile | px/m | Notes |
|---|---|---|---|---|
| Grass | `grass/T_Terrain_Grass_2K_*` | 4.0 | 512 | blades over clumps; soil shows through in places |
| Soil | `soil/T_Terrain_Soil_2K_*` | 4.0 | 512 | clods, pebbles |
| Rock | `rock/T_Terrain_Rock_2K_*` | 4.0 | 512 | horizontal strata; use triplanar on steep faces |
| Gravel | `gravel/T_Terrain_Gravel_2K_*` | **2.0** | 1024 | angular stones on dark fines |
| Macro mask | `masks/T_Terrain_MacroVariation_1K.png` | **64.0** (and optionally ~21.3) | 16 | 02A: 3-octave. R tone, G dryness, B wetness / roughness hint; multiply albedo by 0.87-1.13 x R and roughness by 0.92-1.08 x B, sampled at two scales |

Maps: BaseColor (sRGB), Normal, Roughness, AO. Terrain UVs are **world-planar**: U = X / 4, V = -Y / 4, so every layer
sits at the metres-per-tile above with UV scale 1 (gravel UV scale 2). There is **no per-module 0-1 stretch**. UV channel 1 is the VegetationMask carrier. Vistas
use X / 64.

> Updated for P1-BLENDER-02A: grass, rock and gravel textures were regenerated (same names / sizes / metres-per-tile); channel meanings are unchanged.

#### Unity shader expectations

- A 4-layer terrain shader (URP Lit-based Shader Graph) blending Grass / Soil / Rock / Gravel by the TerrainBlend weights.
- **Triplanar sampling for Rock and Soil** (steep faces); planar for Grass and Gravel. The Blender preview does exactly this.
- Height-biased blending is optional: add the layer's normal/AO influence to the weight before normalising.
- Dry-grass tint: lerp the grass albedo toward (1.45, 1.15, 0.55) × albedo by VegetationMask.G (as in the Blender preview).
- Mobile: drop to 2 layers (Grass + Rock) from weights G+A merged into soil, skip normal maps, and use LOD1/LOD2 meshes.
- Concrete (`MAT_Terrain_Concrete`) uses the **P1 props trim sheet** (`T_RoadProps_Trim_2K`, concrete strip, from the P1 transfer package). Reuse P1's trim material.

---

### `reports/P1_terrain_02A_visual_polish.md`

### P1-BLENDER-02A — visual polish report

Checkpoints: `blend/terrain_08_visual_polish.blend` (working), `blend/terrain_09_final_frozen.blend` (export source). `terrain_01..07` are unchanged (hash-verified).

#### 1. Rock cuts and cliffs
Original issue: stacked stratified slabs. Changes: each variant has its own fracture-cell shape (Voronoi plane field, per-cell tilt and offset), bedding that is
*interrupted* by fracture noise and thresholded (so ledges do not run across the face), per-variant bedding angle, rare outward-leaning outcrop cells (undercuts),
a ragged, stepped, asymmetric crest, a lean that varies across the width, a talus toe that breaks the rock/grass line, and a gentler edge fade so module ends no longer
show a vertical lip. The Rock texture was rebuilt without horizontal strata (warped Voronoi plates, per-plate tone, fracture network, vertical streaks).

| Variant | Identity |
|---|---|
| RockCut_A | tall narrow cells (strong vertical joints), mild diagonal bedding |
| RockCut_B | massive blocks, little layering, flat crest |
| RockCut_C | diagonal / fractured geology, 7° lean asymmetry, high crest tilt |
| Cliff_Module_A | broad large planes |
| Cliff_Module_B | small fractured cells |
| Cliff_Module_C | shelves in the lower zone, tall vertical breaks above |

Toe: TerrainBlend on rock vertices is now (0, soil 0-0.3, rock 0.7-1.0, gravel 0-0.22) near the base, so rock fades into soil/gravel instead of a hard line (B stays dominant above Z 1.2 m).

#### 2. Road edge
Transition strips use 0.25 m columns (was ~1 m): gravel width now varies 0.05-0.88 m (R) / 0.14-0.96 m (L), mean 0.33-0.40 m, std 0.20 m; soil intrusions, grass patches and
occasional exposed dirt. The type bands' gravel strip (d 16.5-18) is noisy (width and position) and darker. No geometry enters the road, shoulder, drain or guardrail corridor.

#### 3. Flat terrain
Large scale: broad 0.4 m noise. Medium scale: 1-2 of {mound, depression, drainage channel} + an optional soil patch per module, seeded per module and side (asymmetric).
Measured Z range inside the type band: R 40 m -0.21..+0.25, L 40 m -0.27..+0.35, 20 m modules -0.29..+0.17 (target 0.10-0.45). Prop corridor (d < 21) and the 2 m seam zones deviate 0.000000 m from the standard profile.
Small scale: grass texture muted (straw / lush / soil patches), macro mask now 3 octaves sampled at 64 m and ~21 m.

#### 4. Triangle / LOD impact (LOD0 sum of the 42 rebuilt asset families: 66,560 -> 78,878)
| Asset | Before -> after (LOD0 / LOD1 / LOD2 / LOD3) |
|---|---|
| Terrain_Flat_*_40m | 1760->2000 / 520 / 100 |
| Terrain_Cut / Fill / Ditch / RockCut / CutWall (40 m) | +240 each at LOD0 (e.g. Cut_Medium 1920->2160); LOD1-2 unchanged |
| TerrainTransition_*_40m | 240-320 -> 1760 LOD0 (0.25 m columns); LOD1 40 unchanged |
| RockCut_A | 1320->1584 / 659->791 / 264->316 / 105->126 |
| Cliff_Module_A | 1980->2240 / 990->1119 / 396->448 / 157->179 |
Rock LODs are decimated from the new LOD0; LOD1-3 stay within 0.15 m mean / 0.30 m p95 of LOD0 (measured), so fracture masses and the silhouette are kept.
Colliders are unchanged in count and size (18, 12-120 tris); terrain colliders match the visual mesh to 0.000 m in the accessible zone. Rock-cut collider boxes were refitted to the new bounds.

#### 5. Mask impact
TerrainBlend: same channels, weights still sum to 1; gravel is irregular, soil appears around gravel edges and in patches; rock vertices carry a soil/gravel toe.
VegetationMask (UV1 and colour set 1): density reduced on soil patches and gravel, still 0 for d < 16.5, transitions, rock > 0.7, gravel-heavy ground; more lateral variation.

#### 6. Textures
Regenerated (same names, sizes, tile metres): Grass, Rock, Gravel (BaseColor / Normal / Roughness / AO) and `T_Terrain_MacroVariation_1K` (R tone, G dryness, B wetness). Soil unchanged.

#### 7. Renders (all under `previews/`)
Before / after: `02A_before_rockcut.png` / `02A_after_rockcut.png`, `02A_before_roadedge.png` / `02A_after_roadedge.png`, `02A_before_flatterrain.png` / `02A_after_flatterrain.png`.
Others: `02A_rockcut_driver`, `02A_rockcut_chase`, `02A_roadedge_close`, `02A_flat_chase`, `02A_240m_sequence`, `02A_240m_driver`, `02A_240m_chase`, `02A_240m_high_chase`, `02A_full_environment`,
`02A_rock_light_day / _golden / _overcast`, `02A_rock_lods`, `02A_rock_library`.

#### 8. Manual visual acceptance
A rock: no longer reads as repeated horizontal slabs (pass). B road edge: irregular, no single straight line (pass). C flat: visible tonal / drainage / mound variation (pass).
Remaining weaknesses (not blocking): recessed fracture pockets look a little boxy up close; cliff modules have flat crest tops; flat terrain is still plain without vegetation.

---

### `reports/P1_terrain_discovery.md`

### P1-BLENDER-02 — Terrain & Roadside Transition: Discovery

Date: 2026-10-07 · Blender 5.2.2 · Blender-only workstation. P0 and P1 are linked read-only; neither file is ever saved.

#### 1. Measured from the linked sources (Blender X; driver-left = +X; d = |X|)

| Element | Measured | Notes |
|---|---|---|
| Road module (incl. 50 mm chamfer) | X ±7.75, Z -0.30 … +0.036 | crown +0.036 at X 0 |
| Right shoulder / drain | -7.7 … -10.2 / -10.2 … -10.7 | drain lip Z -0.1085 |
| Right verge, ragged outer edge | **X -12.01 … -12.42** at Z -0.30 | noise-driven edge, verge surface -0.11 → -0.30 |
| Left verge (alternative to the median), outer edge | **X +9.99 … +10.46** at Z -0.30 | |
| Concrete median | +8.7 … +10.70, top +0.084, skirt to -0.30 | barrier top +0.889 |
| Grass median (alternative) | +8.7 … +14.7 | |
| P1 guardrail post line | X -11.0, ground ≈ -0.16 (on the verge) | 0.43 m deep incl. rail |
| P1 streetlight line | X -12.0, base plate 0.4 m | |
| P1 gantry | right plinth X -11.8 … -13.0 (base -0.45); left plinth on the median; lowest member over lanes **6.15 m** | |
| P1 signs / CCTV / cabinets | X -12.8 / -14.0 / -14.2 | |
| Module ends | Y 0 → -40.000 (-20.000) | traffic travels -Y |

No terrain references or old terrain meshes exist in the workspace. `references/` is empty.

#### 2. Lateral zoning (per side)

| Zone | d (m) | Asset | Purpose |
|---|---|---|---|
| Road kit (P0) | 0 … verge edge | P0 | unchanged |
| **Transition / prop corridor** | R 11.9 … 16.0, L 9.9 … 16.0 | `TerrainTransition_*` | starts *under* the verge (hidden), meets the verge's ragged edge 1 cm higher so the edge blends in, then a level corridor at Z ≈ -0.29 … -0.32 for streetlights, signs, gantry plinths, CCTV, cabinets |
| **Terrain type band** | 16.0 … 50.0 | `Terrain_Flat/Cut/Fill/Ditch_*` | 34 m of shaped terrain per side |
| Outer convergence | 38/40 … 50 | (inside every type module) | every type returns to Z **-1.2** at d 50 |
| Far ground | 50 … 1500 | `Vista_FarGround_A` | inner edge exactly Z -1.2; no world edge |
| Vistas | 400 m … 3 km | `Vista_*` | horizon silhouettes |

**Chosen near-terrain width: 34 m type band + 4–6 m corridor ≈ 38–40 m outside the road kit on each side** (the outer
edge sits at 50 m from the centreline). Camera QA from driver, low-chase, high-chase and side views shows no edge,
because the far-ground ring continues at the same height.

#### 3. Base ground height

Roadside base ground is **Z -0.30** at the verge edge. The corridor holds -0.29 … -0.32. The standard boundary is
Z -0.32 at d 16, the flat profile drifts to about -0.6 by d 38, and every module converges to -1.2 at d 50.
Prop ground heights (right side): X -12.0 → -0.299 · -12.8 → -0.292 · -14.0 → -0.297.

#### 4. Seam policy (deterministic boundaries)

- Origin of every terrain module = the **chunk origin** (road centreline, Y 0, Z 0), the same as P0. Modules run Y 0 → -40 (-20).
- **Seam-safe zone = the first and last 2.0 m**: there the surface equals a *boundary profile* exactly (no noise), and
  is constant along Y, so slopes continue smoothly across the seam.
- Boundary classes:
  - **B0 (standard)**: Flat, Transition, Ditch and every self-contained Cut/Fill module start and end with it, so any of them can follow any other.
  - **Cut_Medium / Fill_Medium run profiles**: `_Run_40m` modules carry the full section at both ends. `_In_20m` (B0 → full) and `_Out_20m` (full → B0) connect them, for long cuts and fills without a 40 m rhythm.
- Inner edge (d 16) is always Z -0.32 and the outer edge (d 50) always Z -1.2, so every type meets the transition corridor and the far ground.
- Every boundary profile is piecewise linear, and its breakpoints are columns in every LOD. Neighbouring modules at different LODs therefore share the same boundary polyline: no cracks.

#### 5. Module strategy

Self-contained 40 m variants (B0 at both ends; 12 m smooth ramps; full section in the middle): Flat, Cut_Low (+2.4 … +3.0 m),
Cut_Medium (+5.4 … +6.3 m), Fill_Shallow (-2.3 … -2.5 m), Fill_Medium (-4.6 … -4.8 m), Ditch (0.8 m V-ditch). Each exists for L and R,
plus `Both` assemblies. The road surface itself never changes. Cuts keep a 1–2 m drained toe at d 16–18 before the slope
starts (1:2 for cuts, 1:2.4 for fills).

#### 6. Material strategy

One terrain material per mesh (`MAT_Terrain_Blend`) blending four tileable layers by the vertex colour **TerrainBlend**
(R grass, G soil, B rock, A gravel). A second data set, **VegetationMask** (density, dryness), is stored both as a colour
attribute and as UV channel 1, because Unity's FBX importer reads only one vertex-colour set. Rocks and cliffs use `MAT_Terrain_Rock`.
Retaining walls and culverts use `MAT_Terrain_Concrete`, which samples the **existing P1 trim sheet's concrete strip**. That
matches the P0/P1 concrete look without duplicating a texture.

#### 7. LOD strategy

- Terrain strips: LOD0 (1 m rows) / LOD1 (2 m rows) / LOD2 (4 m rows, breakpoint columns only).
- Rocks and cliffs: collapse decimation 50 / 20 / 8 %.
- Vistas: 2 levels.
- Retaining walls: 2 levels.
- No LODs for meshes under about 100 tris.

---

### `reports/P1_terrain_FINAL_FREEZE.md`

### P1_Terrain — FINAL FREEZE

Date: 2026-10-07 · Phase: P1-BLENDER-02 + P1-BLENDER-02A (visual polish) · Status: **FROZEN**. Do not edit anything under `environment/P1_Terrain/`; the next phase may only *link* from it.

#### Final deliverables
- Final blend: `blend/terrain_09_final_frozen.blend` (export source). `terrain_08_visual_polish.blend` = the working copy; `terrain_01 .. 07` = original validated checkpoints (unchanged).
- Final FBX (`exports/`, identical in `UnityTransfer/FBX/`): `terrain_complete.fbx`, `Terrain_Flat`, `Terrain_Cut`, `Terrain_Fill`, `Terrain_Drainage`, `Terrain_Retaining`, `Terrain_Rocks`, `Terrain_Vistas`. Pre-polish set archived in `exports/_pre_02A/`; pre-polish textures in `textures/_pre_02A/`.
- Unity package: `UnityTransfer/` (36 files, 96 MB): FBX, Textures, Reports, README (`TERRAIN_IMPORT_NOTES.md`, `TERRAIN_BLEND_GUIDE.md`).

#### Validation status
- `reports/P1_terrain_02A_validation.txt`: **0 errors, 0 warnings** (the full P1-BLENDER-02 suite re-run on terrain_09, plus 02A checks 21-27).
- Re-import of all 8 FBX: all pass (world deviation <= 0.19 mm, TerrainBlend drift <= 0.002, Unity forward Z 0 -> 40).
- Seams: all module/LOD ends equal the boundary profile; 240 m and long-cut sequences join with max gap 4.5e-08 m.
- Source integrity: P0 (95), P1 Props (77), cars (108) and the 232 earlier root files are byte-identical; `terrain_01 .. 07` byte-identical. See `reports/P1_terrain_02A_source_integrity_check.md`.

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P1_terrain_02A_validation.txt`

```text
== P1-BLENDER-02A TERRAIN VISUAL POLISH — VALIDATION (full 02 suite + 02A checks) ==
source blend/terrain_09_final_frozen.blend; TERRAIN_MASTER 353 objects, 205 meshes

[PASS]  1. required modules exist (51 required, 67 assets built)
[PASS]  2. naming: no .001 / illegal characters; <Asset> empty -> <Asset>_LOD0..n contiguous; _L = +X, _R = -X
      side convention: OK
[PASS]  3. 40 m terrain meshes span exactly Y 0 .. -40.000 (70 meshes incl. LODs/colliders)
[PASS]  4. 20 m terrain meshes span exactly Y 0 .. -20.000 (34 meshes)
[PASS]  5. snap spacing: 43 assets, Snap_Start -> Snap_End = module length along -Y (40.000 / 20.000 / 8 / 4 / 3 m)
[PASS]  6. ground level: every type module meets the corridor at d 16 Z -0.320 and the far ground at d 50 Z -1.200; transitions end at d 16 Z -0.320
[PASS]  7. seam-safe boundaries: every module/LOD end row equals its boundary profile exactly (B0, or the full section for Run / In-end / Out-start)
[PASS]  7. road transition: terrain starts under the verge (R d 11.899999618530273, verge outer edge 12.01-12.42; L d 9.899999618530273, verge 9.99-10.46) and stays at Z <= -0.290 (below verge top, P0 drain untouched, 1 cm over the verge edge so it blends)
[PASS]  7. prop clearance: P1 bases sit on (<= 5 mm above) or in the terrain at their documented lines; no terrain above Z -0.28 inside d 16 (sightlines, guardrail, gantry)
[PASS]  7. sequence joins: main 240 m strip (Flat+Cut+Flat+Fill+RockCut+Ditch / L variants) 44 joints and long-cut strip (In+Run+Run+Out+Flat) 16 joints, no cracks or steps
[PASS]  8. P0 / P1 / car sources byte-identical to the phase baseline (512 files: P0 95, P1 77, new_car 108)
[PASS]  9. transforms: every asset root at origin; every mesh identity world matrix (scale 1, no rotation)
[PASS] 10. normals: terrain/vista/ditch heightfields all face up; consistent winding on shared edges; closed shells outward (smooth terrain, sharp rock / concrete edges by angle)
[PASS] 11. UVs: UVMap on every mesh; terrain = world-planar X/4, -Y/4 (seamless across 40/20 m modules); VegetationMaskUV (UV1) on terrain
[PASS] 12. TerrainBlend: on every terrain strip / ditch insert / rock; RGBA weights in 0-1 summing to 1; it is the render (export) colour
[PASS] 13. VegetationMask: present; density 0 in the road / prop corridor (d < 16.5), on transitions, on rock (B > 0.7) and gravel ditch beds
[PASS] 14. materials: only MAT_Terrain_Blend, MAT_Terrain_Grass, MAT_Terrain_Soil, MAT_Terrain_Rock, MAT_Terrain_Gravel, MAT_Terrain_Concrete, MAT_Terrain_DryGrass; colliders have none
[PASS] 15. LODs: 62 LOD groups, strictly decreasing triangle counts
[PASS] 16. colliders: 18 (flat / transition / cut / rock-cut / cut-wall terrain surfaces, retaining walls, rock cuts), no materials, parented, <= 25 % of LOD0 tris
[PASS] 17. no non-manifold edges / loose geometry / ngons (205 meshes)
[PASS] 18. no zero-area faces
[PASS] 19. export selection == TERRAIN_MASTER; no QA / linked P0 / P1 / car / camera objects; no leaked selection; no export-time fix-ups
[PASS] 20. re-import Terrain_Flat.fbx: 48 objects (20 LOD meshes, 4 colliders)
[PASS] 20. re-import Terrain_Cut.fbx: 98 objects (45 LOD meshes, 8 colliders)
[PASS] 20. re-import Terrain_Fill.fbx: 66 objects (33 LOD meshes, 0 colliders)
[PASS] 20. re-import Terrain_Drainage.fbx: 20 objects (6 LOD meshes, 0 colliders)
[PASS] 20. re-import Terrain_Retaining.fbx: 32 objects (12 LOD meshes, 3 colliders)
[PASS] 20. re-import Terrain_Rocks.fbx: 71 objects (54 LOD meshes, 3 colliders)
[PASS] 20. re-import Terrain_Vistas.fbx: 18 objects (12 LOD meshes, 0 colliders)
[PASS] 20. re-import terrain_complete.fbx: 353 objects (182 LOD meshes, 18 colliders)
[PASS] 21. original terrain checkpoints terrain_01 .. terrain_07 byte-identical to the pre-polish hashes
[PASS] 22. road-edge gravel: effective width varies along the road (std >= 0.06 m) and never exceeds 1.0 m (min / mean / max / std per strip below)
[PASS] 23. flat terrain: large/medium-scale variation 0.10-0.45 m in the type band; prop corridor (d < 21) and the 2 m seam zones exactly on the standard profile
[PASS] 24. rock LOD fidelity: LOD1-3 stay within 0.15 m mean / 0.30 m p95 of LOD0 (silhouette and fracture planes preserved; (mean, p95) per LOD1,2,3 below)
[PASS] 25. rock variants have distinct silhouettes (six different LOD0 bounding boxes; not one asset rotated)
[PASS] 26. collider vs visual terrain: exact in the accessible zone (d < 21), within 0.5 m beyond (max deviation near-road / off-road per collider below)
[PASS] 27. prop clearance: terrain in the prop corridor (transition d 11.9 -> 16) stays in Z -0.321 .. -0.289 (P1 bases at -0.299 .. -0.292 not buried, none floating)

Triangle budgets are guidance only; below-budget assets are not reported as warnings.
SUMMARY: 0 errors, 0 warnings
```

