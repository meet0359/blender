# P0-BLENDER-01 — Road Foundation

Digest 01 of the environment handoff. Folder: `environment/P0_RoadFoundation/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/road_05_export_ready.blend`
- **Asset index source:** `reports/P0_road_geometry.json` + `reports/P0_road_export_manifest.json`
- **Checkpoints (5):** `road_01_blockout.blend`, `road_02_modular_geometry.blend`, `road_03_materials_uv.blend`, `road_04_lods_collision.blend`, `road_05_export_ready.blend`
- **FBX (7):** `Road_4Lane_40m.fbx` (7 objects), `Road_4Lane_20m.fbx` (7 objects), `Shoulders.fbx` (12 objects), `Medians.fbx` (12 objects), `Drainage.fbx` (5 objects), `RoadSafety_Core.fbx` (5 objects), `road_foundation_unity.fbx` (48 objects)
- **Textures:** 24 PNG files · **Previews:** 9 renders · **UnityTransfer README:** `ROAD_IMPORT_NOTES.md`

**Module dimensions (x, y, z m):** `{"Collision_Barrier_20m": [0.61, 20.0, 0.81], "Collision_Barrier_40m": [0.61, 40.0, 0.81], "Collision_Road_20m": [18.9, 20.0, 0.636], "Collision_Road_40m": [18.9, 40.0, 0.636], "Drain_Channel_4m": [0.5, 4.0, 0.1915], "Drain_Grate_LOD0": [0.296, 0.998, 0.02], "Drain_Grate_LOD1": [0.296, 0.998, 0.02], "Drain_Grate_LOD2": [0.296, 0.998, 0.0], "EdgeBreakup_Verge_L": [1.76165, 40.0, 0.229], "EdgeBreakup_Verge_L_20m": [1.67131, 20.0, 0.229], "EdgeBreakup_Verge_R": [1.75024, 40.0, 0.1915], "EdgeBreakup_Verge_R_20m": [1.66885, 20.0, 0.1915], "Marking_Warning_20m": [7.35, 20.0, 0.03675], "Marking_Warning_40m": [7.35, 40.0, 0.03675], "Median_Barrier_20m_LOD0": [0.61, 20.0, 0.81], "Median_Barrier_20m_LOD1": [0.61, 20.0, 0.81], "Median_Barrier_LOD0": [0.61, 40.0, 0.81], "Median_Barrier_LOD1": [0.61, 40.0, 0.81], "Median_Concrete": [2.0, 40.0, 0.384], "Median_Concrete_20m": [2.0, 20.0, 0.384], "Median_Grass": [6.0, 40.0, 0.349], "Median_Grass_20m": [6.0, 20.0, 0.349], "Road_4Lane_20m": [15.5, 20.0, 0.336], "Road_4Lane_20m_Dividers": [7.35, 14.0, 0.03675], "Road_4Lane_20m_EdgeLines": [14.65, 20.0, 0.00375], "Road_4Lane_40m": [15.5, 40.0, 0.336], "Road_4Lane_40m_Dividers": [7.35, 34.0, 0.03675], "Road_4Lane_40m_EdgeLines": [14.65, 40.0, 0.00375], "Road_4Lane_Joint": [15.4, 0.4, 0.0855], "Road_Reflector_LOD0": [0.1, 0.1, 0.018], "Road_Reflector_LOD1": [0.1, 0.1, 0.018], "RumbleStrip_4m": [0.3, 4.0, 0.0145], "Shoulder_Gravel_L": [1.0, 40.0, 0.23794], "Shoulder_Gravel_L_20m": [1.0, 20.0, 0.23813], "Shoulder_Gravel_R": [2.5, 40.0, 0.23762], "Shoulder_Gravel_R_20m": [2.5, 20.0, 0.2374], "Shoulder_Paved_L": [1.0, 40.0, 0.254], "Shoulder_Paved_L_20m": [1.0, 20.0, 0.254], "Shoulder_Paved_R": [2.5, 40.0, 0.254], "Shoulder_Paved_R_20m": [2.5, 20.0, 0.254]}`

## Asset index (generated from the export manifest + geometry report)

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `Drainage.fbx` (5): Drain_Channel_4m (52), Drain_Grate, Drain_Grate_LOD0 (140), Drain_Grate_LOD1 (34), Drain_Grate_LOD2 (2)
- `Medians.fbx` (12): Collision_Barrier_20m (12), Collision_Barrier_40m (12), Median_Barrier, Median_Barrier_20m, Median_Barrier_20m_LOD0 (360), Median_Barrier_20m_LOD1 (70), Median_Barrier_LOD0 (720), Median_Barrier_LOD1 (140), Median_Concrete (240), Median_Concrete_20m (120), Median_Grass (440), Median_Grass_20m (220)
- `RoadSafety_Core.fbx` (5): Road_4Lane_Joint (72), Road_Reflector, Road_Reflector_LOD0 (74), Road_Reflector_LOD1 (10), RumbleStrip_4m (198)
- `Road_4Lane_20m.fbx` (7): Collision_Road_20m (32), Marking_Warning_20m (80), Road_4Lane_20m (840), Road_4Lane_20m_Dividers (32), Road_4Lane_20m_EdgeLines (80), Road_4Lane_20m_Snap_End, Road_4Lane_20m_Snap_Start
- `Road_4Lane_40m.fbx` (7): Collision_Road_40m (32), Marking_Warning_40m (160), Road_4Lane_40m (1,680), Road_4Lane_40m_Dividers (64), Road_4Lane_40m_EdgeLines (160), Road_4Lane_40m_Snap_End, Road_4Lane_40m_Snap_Start
- `Shoulders.fbx` (12): EdgeBreakup_Verge_L (640), EdgeBreakup_Verge_L_20m (320), EdgeBreakup_Verge_R (640), EdgeBreakup_Verge_R_20m (320), Shoulder_Gravel_L (320), Shoulder_Gravel_L_20m (160), Shoulder_Gravel_R (320), Shoulder_Gravel_R_20m (160), Shoulder_Paved_L (80), Shoulder_Paved_L_20m (40), Shoulder_Paved_R (80), Shoulder_Paved_R_20m (40)

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `UnityTransfer/README/ROAD_IMPORT_NOTES.md`

### Road Foundation (P0-BLENDER-01) — Unity import notes

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.**
> **UNITY-SIDE SHADERS, PREFABS, ROADSTREAMER CONFIGURATION AND PERFORMANCE TESTING MUST BE DONE ON THE UNITY WORKSTATION.**
> Nothing in here has been opened in Unity. Every number below was measured in Blender, including a re-import of each FBX.

#### 1. Contents

| Folder | What |
|---|---|
| `FBX/` | `road_foundation_unity.fbx` (all 48 objects) and the same objects split into 6 files (table below) |
| `Textures/asphalt/` | `T_Road_Asphalt_{BaseColor,Normal,Roughness,AO}.png`, 2048², tileable |
| `Textures/decals/` | `T_Decal_<name>_{BaseColor,Normal}.png`, 1024², for URP Decal Projectors |
| `Reports/` | validation (0 errors), geometry stats, export manifest, discovery, texture list |

| FBX | Objects |
|---|---|
| `Road_4Lane_40m.fbx` | `Road_4Lane_40m` → `_EdgeLines`, `_Dividers`, `_Snap_Start`, `_Snap_End`, `Collision_Road_40m`; plus `Marking_Warning_40m` |
| `Road_4Lane_20m.fbx` | the same for 20 m |
| `Shoulders.fbx` | `Shoulder_Paved_L/R`, `Shoulder_Gravel_L/R`, `EdgeBreakup_Verge_L/R`, each also as `_20m` |
| `Medians.fbx` | `Median_Concrete`, `Median_Grass`, `Median_Barrier` (→ `_LOD0`, `_LOD1`, `Collision_Barrier_40m`), each also as `_20m` |
| `Drainage.fbx` | `Drain_Channel_4m`, `Drain_Grate` (→ `_LOD0/1/2`) |
| `RoadSafety_Core.fbx` | `Road_Reflector` (→ `_LOD0/1`), `RumbleStrip_4m`, `Road_4Lane_Joint` |

Use either the single file or the split files, not both. The split files are recommended: one model per prefab family.

#### 2. Importer settings (Model tab)

- **Scale Factor 1, Convert Units ON.** The file unit is 1 m, so 1 Unity unit = 1 m and every root has scale 1.
- **Bake Axis Conversion OFF.** Axes are already baked; roots have identity rotation in the file.
- Normals: **Import**. Tangents: **Calculate Mikktspace** (or Import). Smoothing comes from the file (sharp edges at 30°).
- Read/Write: only if a runtime curved-world or mesh-combine script needs it. Generate Colliders: **OFF**. Use the `Collision_*` meshes (§7).
- Animation: none. Rig: None. There are no cameras or lights in the files.
- Materials: extract, then replace with URP materials (§5). The FBX auto-links only the asphalt normal map; assign everything else by hand.

#### 3. Scale and orientation (verified by FBX re-import)

| | Blender source | FBX / Unity |
|---|---|---|
| up | +Z | **+Y** |
| road forward (travel direction) | -Y | **+Z** |
| driver's left (median side) | +X | **-X** (Unity mirrors FBX X on import) |
| point | (x, y, z) | Unity (-x, z, -y) |

Chunk modules run from **Unity z = 0 to z = +40.000** (or +20.000). The re-import measured the road's file-space Z
range as 0 → 40.0000 and the snap distance as 40.000000 m.

#### 4. Grid, origins, snap points

- **Chunk modules** (everything with `40m`/`20m` in its name, plus shoulders, verges, medians, barrier and markings): the
  origin is the **chunk start on the road centreline**. All of them are authored in their final cross-section position,
  so place every piece of a chunk at the **same position** as the chunk itself, with no per-piece offsets.
- `Road_4Lane_40m_Snap_Start` sits at the origin and `Road_4Lane_40m_Snap_End` at Unity (0, 0, 40) (20 m: (0, 0, 20)).
  Next chunk position = `Snap_End` world position.
- 40 m and 20 m chunks mix freely in any order. Every repeating pattern divides 20 m: 2 m segments, 4 m UV tile,
  10 m marking cycle, and the 4 m drain/rumble/barrier-joint pitch.
- Long modules are subdivided every **2 m** along the road (barrier LOD1: 4 m) so a curved-world shader has vertices to bend.

**Repeating props** have their own origin. Placement is relative to the chunk origin, in Unity coordinates (x mirrored):

| Prop | Origin | Placement in chunk (Unity x, y, z) | Spacing |
|---|---|---|---|
| `Drain_Channel_4m` | channel centre, start, top of lip | (+10.45, -0.1085, 4k) | 4 m → 10 per 40 m |
| `Drain_Grate` | grate centre, top | (+10.45, -0.1085, 4k + 0.5 + j), j = 0..3 | 1 m, 4 per channel |
| `RumbleStrip_4m` right (outer) side | strip centre, start, on surface | (+7.5, -0.042, 4k) | 4 m |
| `RumbleStrip_4m` left (median) side | same | (-7.5, -0.042, 4k + 4), **rotate Y 180°** (keeps the cross-slope correct) | 4 m |
| `Road_Reflector` | base centre | x ∈ {+3.6, 0, -3.6}, y = surface - 0.002, z ∈ {8, 18, 28, 38} | 10 m, in the dash gaps |
| `Road_4Lane_Joint` | chunk origin, straddles z ±0.2 | (0, 0, 0) at any chunk seam | as wanted (e.g. every 2–5 chunks) |

Surface y at a reflector: x = ±3.6 → 0.000, x = 0 → +0.036 (minus 0.002 embed). The reflective face looks toward oncoming traffic (Unity -Z).
Instance reflectors, grates and rumble strips with GPU instancing. They are deliberately **not** merged into road meshes.

#### 5. Materials and textures

Material slot names stay as they are. These are Blender review materials; build URP Lit (or custom) materials with the same names:

| Slot | Unity setup |
|---|---|
| `MAT_Road_Asphalt` | Base `T_Road_Asphalt_BaseColor` (sRGB), Normal `T_Road_Asphalt_Normal` (Normal map, OpenGL / +Y, **no flip**), Smoothness = 1 - `T_Road_Asphalt_Roughness`, Occlusion `T_Road_Asphalt_AO`. Tiling **1,1**: the UVs are already world-scale (1 UV = 4 m). |
| `MAT_Road_Shoulder` | same textures, base colour × ~1.5 (older, lighter), smoothness -0.05 |
| `MAT_Road_Marking_White` / `_Yellow` | sRGB ~(0.80, 0.80, 0.78) / (0.86, 0.64, 0.10), smoothness ~0.45 |
| `MAT_Road_Concrete` | sRGB ~0.60 grey, smoothness ~0.15 |
| `MAT_Road_Metal` | metallic 1, smoothness ~0.6 (galvanised / cast body) |
| `MAT_Road_Drain` | dark cast iron/grime, metallic ~0.6, smoothness ~0.4. Grate LOD1/LOD2 need a slot normal map (not supplied). |
| `MAT_Road_Reflector` | white retroreflector, smoothness ~0.9, emission ~1–2 for night readability |
| `MAT_Road_Gravel`, `MAT_Road_Grass` | verge / gravel shoulder / grass median. Placeholder colours only. Two extra slots beyond the original eight. |

- Every mesh has **UVMap**: object-space box projection at **4 m per tile**. The texel density is the same on every
  asset (512 px/m with a 2048 tile on top faces, 473–512 px/m including side faces). V runs along the road and the
  chunk ends fall on whole tiles, so textures are continuous across chunks.
- `Road_4Lane_40m/20m` carry a vertex colour attribute **`Wear`** (R = 0..1, 1 on the wheel paths 0.65–1.05 m either
  side of each lane centre). Use it in the asphalt shader for subtle polish or darkening.
- Decals (URP Decal Projector, Base + Normal): suggested world sizes Crack_A/B 2×2 m, Crack_C 4×1 m, Patch_A 3×2 m,
  Patch_B 2.5×2 m, TarLine_A/B 0.6×5 m, Skid_A 2.2×7 m, Skid_B 2×6 m, OilStain_A 1.6×1.6 m. They are not baked into the road.

#### 6. Cross-section (Unity x = -Blender x; heights in m)

| Element | Width | Notes |
|---|---|---|
| Lanes | 4 × **3.60** = **14.40** | crown at the centre divider, y = +0.036; 1.0 % cross-slope |
| Edge strips (in road module) | 0.50 each side | 2.0 % slope, edge y = -0.046, 50×30 mm chamfer, skirt to y = -0.30 |
| Outer (right) hard shoulder | 2.50 module (3.00 paved outside the edge line) | 2.5 % slope to y = -0.1085 |
| Inner (left) shoulder | 1.00 module (1.50 inside the edge line) | 2.5 % slope to y = -0.071 |
| Drain channel | 0.50 | outside the right shoulder; grates flush with the lip |
| Verge / edge breakup | ≈1.5, irregular | broken asphalt lip → gravel → ground y = -0.30 |
| Median: concrete | 2.00, kerb 150 mm | carries `Median_Barrier` (F-shape, 810 mm, 610 mm base) |
| Median: grass | 6.00 | concrete kerbs + grass swale (alternative to concrete + barrier) |
| Nominal ground | y = -0.30 | |

Lane-centre surface heights: ±1.8 m → +0.018, ±5.4 m → -0.018. Gameplay that assumes y = 0 is within ±18 mm.
Markings: 2 mm above the surface. Dividers are 0.15 m wide, 4 m dash / 6 m gap; edge lines 0.25 m, white outside and
yellow on the median side. `Marking_Warning_*` (solid dividers) **replaces** `_Dividers` in no-lane-change zones, so disable one of them.
Alternates that share a slot (enable one per side): `Shoulder_Paved_*` / `Shoulder_Gravel_*`; on the left,
`Median_Concrete` + `Median_Barrier` / `Median_Grass` / `EdgeBreakup_Verge_L`.

#### 7. Colliders

| Collider | Shape | Tris |
|---|---|---|
| `Collision_Road_40m` / `_20m` (child of the road) | closed prism following the crown + both paved shoulders (x -8.7 … +10.2 Unity), 0.6 m deep | 32 |
| `Collision_Barrier_40m` / `_20m` (child of `Median_Barrier`) | closed trapezoid prism of the F-barrier | 12 |

Add a **MeshCollider** (road: static, non-convex is fine; the barrier can be Convex), then disable or strip the collider
MeshRenderer. Colliders carry no material and no micro-detail: no reflectors, markings or joints.

#### 8. LODs and budgets

LOD meshes are named `_LOD0.._LOD2` under one parent empty, so Unity builds a LOD Group automatically.

| Asset | LOD0 | LOD1 | LOD2 |
|---|---|---|---|
| `Drain_Grate` | 140 | 34 (bars → recessed plate, slots via normal map) | 2 |
| `Road_Reflector` | 74 | 10 | – |
| `Median_Barrier` (40 m) | 720 (V-joints every 4 m) | 140 | – |

No LODs for the road, shoulders or medians: they are already low (road 1,680 tris per 40 m).
A fully dressed standard 40 m chunk is ≈14.6k tris at LOD0, and 40 grates (5,600) plus 20 rumble strips (3,960) make up
most of that. On mobile, push grates to LOD1/LOD2 early and consider dropping rumble strips. Per-asset counts are in `Reports/P0_road_geometry.json`.

#### 9. Excluded from the FBX

The Blender QA strip (120 m), the variant strips, the decal preview planes, the linked hypercar scale reference, the QA
ground, cameras and lights. Only the `ROAD_MASTER` collection is exported. The full list is in `Reports/P0_road_export_manifest.json`.

#### 10. Still to do on the Unity workstation

URP asphalt shader (wetness, wear from `Wear`, decals), prefabs per chunk type, RoadStreamer prefab swap and spacing
(40 m, `Snap_End`), GPU instancing of props, LOD Group thresholds, collider/physics check with the player car, curved-world
shader test, and mobile and PC profiling.

---

### `reports/P0_road_discovery.md`

### P0-BLENDER-01 — Road Foundation: Discovery

Date: 2026-10-06 · Blender 5.2.2 LTS · Workstation: Blender-only (no Unity project on this machine)

#### 1. References found

| Searched for | Result |
|---|---|
| Road / lane / highway / asphalt files anywhere under `/Users/meetshah/Documents/blender` | **None.** No road meshes, exports, screenshots or reference images. |
| `exports/` (old road exports) | Folder does not exist. |
| AssetPreviews / road screenshots | None. |
| Unity road chunk source | Not on this machine (by design). |
| Hypercar (scale reference) | `new_car/hypercar_08_unity_export.blend`, collection `Car_LOD3` (17,747 tris). 4.695 x 2.052 m, track 1.67 m. Usable as a linked reference. |
| Proven Unity export convention | `new_car/scripts/export_fbx.py` + `new_car/reports/unity_import_notes.md` (see §6). |

Conclusion: no original road geometry exists here. The kit is built from the documented architecture
(straight 40 m streaming chunks, lateral lane changes, 4 lanes) plus real-world motorway dimensions.

#### 2. Assumptions

- The game shows a **single 4-lane carriageway, one travel direction** (endless traffic racer). The median is on
  the driver's left, the hard shoulder on the right (right-hand traffic).
- Gameplay places cars on a surface close to height 0. The crown is therefore centred on 0 so that lane-centre
  heights stay within ±18 mm (see §4).
- Road length runs straight. Curved-world bending happens later in a Unity shader, so every long module is
  subdivided lengthwise every **2 m** to give that shader vertices to bend.
- Ground level next to the road is nominally **Z = -0.30 m** (verge outer edge / skirt bottoms).

#### 3. Chosen dimensions

| Item | Value |
|---|---|
| Lane width | **3.60 m** (between line centres) |
| Lanes | 4 |
| Carriageway (lanes) | **14.40 m** (X -7.2 … +7.2) |
| Edge strips (inside Road_4Lane module, beyond edge lines) | 0.50 m each side → road module width 15.40 m |
| Outer (right) hard shoulder | Shoulder module 2.50 m + 0.50 m edge strip = **3.00 m paved** outside the edge line |
| Inner (left, median-side) shoulder | Shoulder module 1.00 m + 0.50 m edge strip = **1.50 m** |
| Drain channel (right, outside shoulder) | 0.50 m |
| Verge / edge breakup | 1.50 m nominal (irregular) |
| Median | Concrete 2.00 m raised 150 mm, or Grass 6.00 m swale; F-shape barrier (810 mm) on the concrete median |
| Road slab thickness | ≈0.25 m visible skirt (surface to Z -0.30), 50 x 30 mm edge chamfer |
| Lane markings | 0.15 m dashed dividers (4 m dash / 6 m gap, 10 m cycle), 0.25 m solid edge lines, 2 mm above surface |

#### 4. Cross-section / crown

Crown at the centre divider (X = 0), Z = +0.036 m.

| Zone | Cross-slope | Z at outer end |
|---|---|---|
| Lanes, X 0 → ±7.2 | 1.0 % | -0.036 |
| Edge strip ±7.2 → ±7.7 | 2.0 % | -0.046 |
| Shoulder R -7.7 → -10.2 | 2.5 % | -0.1085 |
| Shoulder L +7.7 → +8.7 | 2.5 % | -0.071 |

Lane-centre surface heights: ±1.8 m → **+0.018**, ±5.4 m → **-0.018**. The maximum deviation from Z = 0 inside
any lane centre is 18 mm, so lane-based gameplay that assumes a flat road is unaffected.

#### 5. Module grid / coordinate convention

- 1 Blender unit = 1 m. Metric.
- **+Z up, road forward = -Y** (same convention as the hypercar: car nose points -Y). Driver's left = +X.
- Chunk modules (40 m / 20 m): origin = `Snap_Start` = road centreline at the chunk start, (0,0,0).
  Geometry runs Y 0 → -40.000 (or -20.000). `Snap_End` = (0, -L, 0).
- All chunk-length side modules (shoulders, verges, medians, barrier, markings, colliders) are authored **in their
  final position relative to the same chunk origin**. In Unity they are all dropped at the chunk's position.
- Repeating props (drain channel 4 m, grate, reflector, rumble strip 4 m, joint) have their own local origin and
  a documented placement offset/spacing.
- Lengths: 40.000 / 20.000 m exactly. Every repeating pattern (2 m segments, 4 m UV tile, 10 m marking cycle, 4 m
  drain/rumble/barrier-joint pitch) divides 20 m, so 40 m and 20 m modules can mix in any order.
- Unity: FBX exported with the hypercar method → Unity **+Y up, +Z forward**. Chunk runs Unity z 0 → +40.

#### 6. Export convention reused from the hypercar

`axis_forward='-Z', axis_up='Y', bake_space_transform=False` (Apply Transform OFF), plus the explicit in-memory
axis bake (`G = Rot(-90°, X)` applied to mesh data, object matrices set to `W·G⁻¹`) in an unsaved export
session. Point mapping Blender (x, y, z) → Unity (-x, z, -y).

---

### `reports/P0_road_validation.txt`

```text
== P0-BLENDER-01 ROAD FOUNDATION VALIDATION ==
source: blend/road_05_export_ready.blend  objects in ROAD_MASTER: 48  meshes: 40
[PASS] required objects exist
[PASS] naming: no .001 suffixes / illegal characters
[PASS] LOD naming (_LODn children of a common empty)
[PASS] all production meshes: identity world transform (scale 1, no rotation, authored in place)
[PASS] no zero/negative scale
[PASS] Collision_Barrier_20m: length = 20.000 m
[PASS] Collision_Barrier_40m: length = 40.000 m
[PASS] Collision_Road_20m: length = 20.000 m
[PASS] Collision_Road_40m: length = 40.000 m
[PASS] EdgeBreakup_Verge_L: length = 40.000 m
[PASS] EdgeBreakup_Verge_L_20m: length = 20.000 m
[PASS] EdgeBreakup_Verge_R: length = 40.000 m
[PASS] EdgeBreakup_Verge_R_20m: length = 20.000 m
[PASS] Marking_Warning_20m: length = 20.000 m
[PASS] Marking_Warning_40m: length = 40.000 m
[PASS] Median_Barrier_20m_LOD0: length = 20.000 m
[PASS] Median_Barrier_20m_LOD1: length = 20.000 m
[PASS] Median_Barrier_LOD0: length = 40.000 m
[PASS] Median_Barrier_LOD1: length = 40.000 m
[PASS] Median_Concrete: length = 40.000 m
[PASS] Median_Concrete_20m: length = 20.000 m
[PASS] Median_Grass: length = 40.000 m
[PASS] Median_Grass_20m: length = 20.000 m
[PASS] Road_4Lane_20m: length = 20.000 m
[PASS] Road_4Lane_20m_EdgeLines: length = 20.000 m
[PASS] Road_4Lane_40m: length = 40.000 m
[PASS] Road_4Lane_40m_EdgeLines: length = 40.000 m
[PASS] Shoulder_Gravel_L: length = 40.000 m
[PASS] Shoulder_Gravel_L_20m: length = 20.000 m
[PASS] Shoulder_Gravel_R: length = 40.000 m
[PASS] Shoulder_Gravel_R_20m: length = 20.000 m
[PASS] Shoulder_Paved_L: length = 40.000 m
[PASS] Shoulder_Paved_L_20m: length = 20.000 m
[PASS] Shoulder_Paved_R: length = 40.000 m
[PASS] Shoulder_Paved_R_20m: length = 20.000 m
[PASS] Road_4Lane_40m_Dividers: dashes inside 0..-40 m
[PASS] Road_4Lane_20m_Dividers: dashes inside 0..-20 m
[PASS] Snap_Start -> Snap_End = 40.000 m along -Y
[PASS] Snap_Start -> Snap_End = 20.000 m along -Y
[PASS] road module width 15.50 m incl. 50 mm chamfers (15.40 m surface)
[PASS] Drain_Channel_4m: length 4.000 m
[PASS] RumbleStrip_4m: length 4.000 m
[PASS] road surface follows designed crown (1.0 % lanes / 2.0 % edge strips)
[PASS] crown subtle: lane-centre heights within +/-20 mm of Z=0
[PASS] Road_4Lane_40m_EdgeLines: 2 mm above surface everywhere
[PASS] Road_4Lane_40m_Dividers: 2 mm above surface everywhere
[PASS] Road_4Lane_20m_EdgeLines: 2 mm above surface everywhere
[PASS] Road_4Lane_20m_Dividers: 2 mm above surface everywhere
[PASS] Marking_Warning_40m: 2 mm above surface everywhere
[PASS] Marking_Warning_20m: 2 mm above surface everywhere
[PASS] Road_4Lane_40m dividers at x [-3.6, 0.0, 3.6], 10 m dash cycle (matches across 40/20 m)
[PASS] Road_4Lane_20m dividers at x [-3.6, 0.0, 3.6], 10 m dash cycle (matches across 40/20 m)
[PASS] seams: start row == end row for 30 chunk modules (no vertex/height mismatch)
[PASS] seams: UVs continuous across module ends (offset is whole tiles)
[PASS] QA snap assembly 40+40+20(+20): 21 module joints coincide exactly (road, markings, shoulders, verge, median, barrier)
[PASS] topology: no non-manifold (>2-face) edges, loose geometry or zero-area faces (40 meshes)
[PASS] normals: no inverted top surfaces; colliders closed with outward normals
[PASS] UVs: UVMap on all 40 meshes, world-scale box projection, 1 tile = 4.0 m
[PASS] texel density consistent (2048 px tile / 4 m; side faces projected)
[PASS] materials: 36 renderable meshes use only MAT_Road_* slots, colliders have none
[PASS] Road_4Lane_*: Wear colour attribute present
[PASS] Collision_Road_40m/20m: surface follows road crown + paved shoulders, no micro detail
[PASS] Collision_Road_40m: closed collider, parent Road_4Lane_40m
[PASS] Collision_Road_20m: closed collider, parent Road_4Lane_20m
[PASS] Collision_Barrier_40m: closed collider, parent Median_Barrier
[PASS] Collision_Barrier_20m: closed collider, parent Median_Barrier_20m
[PASS] texture links: 56 image files referenced by materials exist
[PASS] export selection == ROAD_MASTER, no QA/presentation objects, no leaked selection
[PASS] FBX re-import Road_4Lane_40m.fbx: 7 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX re-import Road_4Lane_20m.fbx: 7 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX re-import Shoulders.fbx: 12 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX re-import Medians.fbx: 12 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX re-import Drainage.fbx: 5 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX re-import RoadSafety_Core.fbx: 5 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX re-import road_foundation_unity.fbx: 48 objects, names/parents/scale 1/dimensions/UVs/materials/tris/normals/snaps
[PASS] FBX orientation: file/Unity space +Y up, +Z forward, road z 0 -> +40, scale 1 m

SUMMARY: 0 errors, 0 warnings
```

