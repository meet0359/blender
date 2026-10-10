# P1-BLENDER-01 — Core Roadside Props

Digest 02 of the environment handoff. Folder: `environment/P1_Props/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/props_07_export_ready.blend`
- **Asset index source:** `reports/P1_props_geometry.json` + `reports/P1_props_export_manifest.json`
- **Checkpoints (7):** `props_01_blockout.blend`, `props_02_guardrails_safety.blend`, `props_03_lighting_gantries.blend`, `props_04_signs_infrastructure.blend`, `props_05_materials_uv.blend`, `props_06_lods_colliders.blend`, `props_07_export_ready.blend`
- **FBX (8):** `Guardrails.fbx` (43 objects), `RoadSafety.fbx` (51 objects), `Streetlights.fbx` (26 objects), `Gantries.fbx` (34 objects), `RoadSigns.fbx` (44 objects), `Delineators.fbx` (20 objects), `Infrastructure.fbx` (32 objects), `roadside_props_complete.fbx` (250 objects)
- **Textures:** 7 PNG files · **Previews:** 15 renders · **UnityTransfer README:** `PROPS_IMPORT_NOTES.md`, `ROAD_PROPS_TRIM_GUIDE.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `Barrier_End_Transition` | 116 / 44 / 12 | RoadSafety.fbx |
| `CCTV_Camera` | 70 / 40 | Infrastructure.fbx |
| `CCTV_Pole` | 324 / 154 / 24 | Infrastructure.fbx |
| `CrashCushion_Main` | 1,022 / 542 / 184 | RoadSafety.fbx |
| `CrashCushion_Short` | 536 / 296 / 112 | RoadSafety.fbx |
| `Delineator_Double` | 48 / 22 / 20 | Delineators.fbx |
| `Delineator_Left` | 72 / 22 / 20 | Delineators.fbx |
| `Delineator_Right` | 38 / 20 / 18 | Delineators.fbx |
| `EdgeMarker` | 84 / 42 / 28 | Delineators.fbx |
| `EmergencyPhoneBox` | 46 / 24 | Infrastructure.fbx |
| `FlexibleBollard` | 240 / 120 / 90 | RoadSafety.fbx |
| `Gantry_4Lane_Full` | 1,952 / 1,082 / 392 / 132 | Gantries.fbx |
| `Gantry_4Lane_Half` | 1,230 / 674 / 246 / 102 | Gantries.fbx |
| `Gantry_CrossBeam` | 1,272 / 616 / 216 / 72 | Gantries.fbx |
| `Gantry_Support_Left` | 226 / 166 / 82 | Gantries.fbx |
| `Gantry_Support_Right` | 226 / 166 / 82 | Gantries.fbx |
| `Guardrail_End_Terminal` | 572 / 280 / 76 | Guardrails.fbx |
| `Guardrail_Median_Variant` | 1,432 / 680 / 288 | Guardrails.fbx |
| `Guardrail_To_Concrete_Transition` | 730 / 360 / 82 | RoadSafety.fbx |
| `Guardrail_Transition` | 696 / 324 / 56 | Guardrails.fbx |
| `Guardrail_WBeam_4m` | 304 / 144 / 48 | Guardrails.fbx |
| `Guardrail_WBeam_8m` | 608 / 288 / 96 | Guardrails.fbx |
| `Guardrail_WBeam_8m_Assembly` | 784 / 360 / 160 | Guardrails.fbx |
| `HighMastLight` | 668 / 348 / 134 / 100 | Streetlights.fbx |
| `ImpactAttenuator` | 2,340 / 1,134 / 450 | RoadSafety.fbx |
| `MedianReflectorPost` | 30 / 14 / 8 | Delineators.fbx |
| `PortableBarrier` | 100 / 44 / 12 | RoadSafety.fbx |
| `RoadDrum` | 552 / 276 / 152 | RoadSafety.fbx |
| `RoadsideSensor` | 84 / 54 | Infrastructure.fbx |
| `SOS_Pillar` | 70 / 40 | Infrastructure.fbx |
| `Sign_CurveWarning` | 68 / 20 / 2 | RoadSigns.fbx |
| `Sign_Direction` | 108 / 28 / 4 | RoadSigns.fbx |
| `Sign_Emergency` | 84 / 28 / 4 | RoadSigns.fbx |
| `Sign_Exit` | 84 / 28 / 4 | RoadSigns.fbx |
| `Sign_LaneEnds` | 68 / 20 / 2 | RoadSigns.fbx |
| `Sign_Merge` | 68 / 20 / 2 | RoadSigns.fbx |
| `Sign_NoStopping` | 148 / 60 / 12 | RoadSigns.fbx |
| `Sign_RouteMarker` | 64 / 24 / 6 | RoadSigns.fbx |
| `Sign_SpeedLimit` | 148 / 60 / 12 | RoadSigns.fbx |
| `Sign_WorkZone` | 68 / 20 / 2 | RoadSigns.fbx |
| `Streetlight_Double` | 636 / 314 / 124 / 60 | Streetlights.fbx |
| `Streetlight_Median_Double` | 636 / 314 / 124 / 60 | Streetlights.fbx |
| `Streetlight_Single` | 460 / 218 / 82 / 36 | Streetlights.fbx |
| `TrafficCone` | 178 / 94 / 40 | RoadSafety.fbx |
| `TrafficCone_WithReflectiveBands` | 370 / 190 / 88 | RoadSafety.fbx |
| `UtilityCabinet_Large` | 76 / 20 | Infrastructure.fbx |
| `UtilityCabinet_Small` | 54 / 20 | Infrastructure.fbx |
| `WarningBeacon` | 90 / 34 | RoadSafety.fbx |
| `WeatherSensor` | 384 / 106 | Infrastructure.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `Gantries.fbx` (11): Collision_Gantry_Half_Right (12), Collision_Gantry_Left (12), Collision_Gantry_Right (12), ExitPanel (32), Gantry_SignFrame (92), Gantry_VMS_Frame (76), LaneArrowPanel (32), SignPanel_Large (32), SignPanel_Medium (32), SignPanel_Small (32), VMS_Panel (32)
- `Guardrails.fbx` (19): Collision_Guardrail_4m (12), Collision_Guardrail_8m (12), Collision_Guardrail_8m_Rail (12), Collision_Guardrail_Median (12), Collision_Guardrail_Terminal (12), Collision_Guardrail_Transition (12), Guardrail_End_Terminal_Snap_Start, Guardrail_Median_Variant_Snap_End, Guardrail_Median_Variant_Snap_Start, Guardrail_OffsetBlock (10), Guardrail_Post (34), Guardrail_Transition_Snap_End, Guardrail_Transition_Snap_Start, Guardrail_WBeam_4m_Snap_End, Guardrail_WBeam_4m_Snap_Start, Guardrail_WBeam_8m_Assembly_Snap_End, Guardrail_WBeam_8m_Assembly_Snap_Start, Guardrail_WBeam_8m_Snap_End, Guardrail_WBeam_8m_Snap_Start
- `Infrastructure.fbx` (7): Collision_CCTV_Pole (28), Collision_EmergencyPhoneBox (12), Collision_RoadsideSensor (28), Collision_SOS_Pillar (12), Collision_UtilityCabinet (12), Collision_UtilityCabinet_Small (12), Collision_WeatherSensor (28)
- `RoadSafety.fbx` (8): Collision_Barrier_End_Transition (12), Collision_CrashCushion (12), Collision_CrashCushion_Short (12), Collision_Guardrail_To_Concrete (12), Collision_ImpactAttenuator (12), Collision_PortableBarrier (12), Guardrail_To_Concrete_Transition_Snap_End, Guardrail_To_Concrete_Transition_Snap_Start
- `RoadSigns.fbx` (4): SignPost_Double (72), SignPost_Round (48), SignPost_Single (36), SignPost_Square (10)
- `Streetlights.fbx` (6): Collision_HighMast (28), Collision_Streetlight (28), Collision_Streetlight_Double (28), Collision_Streetlight_Median (28), Streetlight_Fixture (46), Streetlight_Pole (284)

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `UnityTransfer/README/PROPS_IMPORT_NOTES.md`

### Core Roadside Props (P1-BLENDER-01) — Unity import notes

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.**
> **UNITY PREFABS, UNITY LIGHTS, UNITY MATERIALS, LODGROUP COMPONENTS, REFLECTION SETTINGS AND PERFORMANCE TESTING MUST BE
> COMPLETED ON THE UNITY WORKSTATION.**
> Nothing here has been opened in Unity. All numbers were measured in Blender, including a re-import of every FBX into an
> empty scene (`Reports/P1_props_reimport_validation.txt`, 0 errors).

#### 1. Unity axis / orientation

| | Blender source | FBX file = Unity |
|---|---|---|
| up | +Z | **+Y** |
| traffic direction | -Y (traffic approaches from +Y) | **+Z** (traffic approaches from -Z) |
| driver-left / median side | +X | **-X** (Unity mirrors FBX X on import) |
| point | (x, y, z) | (-x, z, -y) |

This is the same method as the hypercar and the P0 road kit: an in-memory axis bake, FBX `axis_forward -Z / axis_up Y`, and Apply Transform
**OFF**. Every root has identity rotation and scale 1 in the file. Sign faces, reflectors, crash-cushion noses and
terminal heads look toward **oncoming traffic (Unity -Z)**. Roadside assets are authored for the **right verge**, with
arms, luminaires and radar heads reaching toward the road (Unity -X). For the median or left side, rotate 180° about Y.
Text on signs reads correctly in Unity; Unity's X mirror is a handedness conversion, not a visual flip.

#### 2. Scale / importer settings

Scale Factor **1**, Convert Units **ON**: 1 unit = 1 m. **Bake Axis Conversion OFF.** Normals: Import (smoothing from file,
sharp edges at 40°). Tangents: Calculate Mikktspace. Generate Colliders **OFF**; use the `Collision_*` meshes. No
animation, cameras or lights in the files. Materials: extract, then rebuild as URP materials (§5).

#### 3. FBX files (`FBX/`)

| File | Objects | Contents |
|---|---|---|
| `Guardrails.fbx` | 43 | W-beam 4 m / 8 m, 8 m assembly, post, offset block, end terminal, W→thrie transition, median (double-sided) variant |
| `RoadSafety.fbx` | 51 | crash cushion main / short, impact attenuator, barrier end transition, guardrail→concrete transition, cones, bollard, drum, beacon, portable barrier |
| `Streetlights.fbx` | 26 | single, double (back-to-back), median double, high mast, bare pole, bare luminaire |
| `Gantries.fbx` | 34 | 4-lane full, 4-lane half (cantilever), supports L/R, cross beam, sign frame, VMS cabinet, 5 sign panels, VMS panel |
| `RoadSigns.fbx` | 44 | 10 roadside signs + 4 posts |
| `Delineators.fbx` | 20 | delineator left / right / double, median reflector post, edge marker |
| `Infrastructure.fbx` | 32 | CCTV pole + camera unit, utility cabinets S/L, emergency phone, SOS pillar, roadside radar sensor, weather station |
| `roadside_props_complete.fbx` | 250 | all of the above in one file |

Use either the split files (recommended: one model per prefab family) or the complete file, not both.

#### 4. LOD hierarchy

Every asset with LODs is an **empty root `<Asset>`** with children `<Asset>_LOD0 … _LODn`, plus its `Collision_*` and
`Snap_*` children. Unity builds a LOD Group automatically from the `_LODn` suffixes; you then set the thresholds.
Single-LOD assets are a plain mesh named `<Asset>`, used for small, sub-100-triangle parts and components.

| Group | LOD0 / LOD1 / LOD2 / LOD3 triangles | Suggested LOD Group screen % |
|---|---|---|
| Guardrail_WBeam_8m_Assembly | 784 / 360 / 160 | 25 / 8 / 2 |
| Guardrail_Median_Variant | 1432 / 680 / 288 | 25 / 8 / 2 |
| Streetlight_Single | 460 / 218 / 82 / 36 | 40 / 15 / 5 / 1 |
| Streetlight_Median_Double | 636 / 314 / 124 / 60 | 40 / 15 / 5 / 1 |
| HighMastLight | 668 / 348 / 134 / 100 | 30 / 12 / 4 / 1 |
| Gantry_4Lane_Full | 1952 / 1082 / 392 / 132 | 50 / 20 / 6 / 1.5 |
| CrashCushion_Main | 1022 / 542 / 184 | 20 / 8 / 2 |
| ImpactAttenuator | 2340 / 1134 / 450 | 20 / 8 / 2 |
| Sign_* (circle / rect / triangle) | 148 / 60 / 12, 84–108 / 28 / 4, 68 / 20 / 2 | 10 / 4 / 1 |
| Delineator_Right | 38 / 20 / 18 | 6 / 2 / 0.5 |
| TrafficCone_WithReflectiveBands | 370 / 190 / 88 | 8 / 3 / 1 |

Full per-asset, per-LOD numbers are in `Reports/P1_props_geometry.json` and `Reports/P1_props_validation.txt`. Most
assets sit **below** the brief's suggested triangle budgets. That is deliberate: the silhouettes are complete, and the detail
lives in the trim normal map.

#### 5. Materials (12 shared)

| Material | Texture | Unity notes |
|---|---|---|
| `MAT_Prop_GalvanizedSteel` | trim | metallic from map, smoothness = 1 - roughness |
| `MAT_Prop_PaintedMetal_Light` / `_Dark` | trim | dielectric paint |
| `MAT_Prop_Concrete` | trim | |
| `MAT_Prop_Plastic_Orange` / `_Black`, `MAT_Prop_Rubber` | trim (neutral strip) | **tint** the base colour (orange ≈ linear 0.90, 0.18, 0.02) |
| `MAT_Prop_Reflective` | trim (white or chevron strip) | **night / retroreflective slot** (§7) |
| `MAT_Prop_Sign_Back` | trim (brushed aluminium) | |
| `MAT_Prop_LightLens` | trim (microprism strip) | **emissive slot** (§10) |
| `MAT_Prop_Sign_Face` | `Textures/signs/T_Signs_Atlas_2K_BaseColor.png` | sign-face slot (§11) |
| `MAT_Prop_VMS` | `Textures/signs/T_VMS_Face_BaseColor.png` | emissive LED face |

The FBX links only the trim Metallic, Roughness and Normal paths automatically. Assign BaseColor and AO by hand.

#### 6. Trim-sheet textures

`Textures/trim/T_RoadProps_Trim_2K_{BaseColor,Normal,Roughness,Metallic,AO}.png`, 2048². Strip layout, channels and
per-family usage are in **`ROAD_PROPS_TRIM_GUIDE.md`**. Normal maps are OpenGL (no flip). Set the sampler to Repeat,
because trim UVs run past 0–1 in U by design.

#### 7. Reflective material slots

`MAT_Prop_Reflective` sits on: delineator reflectors (white), median reflector posts (both faces), edge-marker band,
cone and drum bands, bollard bands, sand-barrel band, crash-cushion nose and guardrail-terminal chevrons (yellow/black
strip). Give it the night treatment in Unity: view-angle or headlight-driven brightening, or high smoothness plus an
emission boost at night. The geometry carries no baked glow.

#### 8. Collider meshes (26)

Closed boxes (12 tris) or 8-sided prisms (28 tris). No materials. Each is parented to its asset root and placed in
`PROPS_COLLIDERS` in the source.

| Collider | Parent | Shape |
|---|---|---|
| `Collision_Guardrail_8m` / `_4m` / `_8m_Rail` / `_Median` / `_Terminal` / `_Transition` / `_To_Concrete` | guardrail assets | box over rail face + posts |
| `Collision_CrashCushion` / `_Short`, `Collision_ImpactAttenuator`, `Collision_Barrier_End_Transition` | crash assets | box |
| `Collision_Streetlight` / `_Double` / `_Median`, `Collision_HighMast` | lighting | 8-sided pole prism (arms not collided) |
| `Collision_Gantry_Left`, `Collision_Gantry_Right` | `Gantry_4Lane_Full` | box around each support tower and plinth |
| `Collision_Gantry_Half_Right` | `Gantry_4Lane_Half` | box |
| `Collision_UtilityCabinet` / `_Small`, `Collision_EmergencyPhoneBox`, `Collision_SOS_Pillar`, `Collision_CCTV_Pole`, `Collision_RoadsideSensor`, `Collision_WeatherSensor`, `Collision_PortableBarrier` | infrastructure / safety | box or prism |

Add a MeshCollider (Convex) on each and disable its MeshRenderer. Cones, drums, bollards, beacons, delineators and signs
have no mesh collider. Give them Unity primitives (capsule / box) if they must react physically.

#### 9. Instancing strategy

Everything repeated is a **separate asset placed per instance**; nothing is baked into road chunks. Enable GPU
Instancing on every material. Suggested spacing per 40 m road chunk:

| Prop | Spacing | Position in a chunk (Unity x, y) |
|---|---|---|
| `Guardrail_WBeam_8m_Assembly` | 5 per 40 m, chained by `Snap_End` | right verge: post line (11.0, -0.16) |
| `Streetlight_Single` | 1 per 40 m (40 m) | (12.0, -0.25) |
| `Streetlight_Median_Double` | 1 per 40 m, offset 20 m | barrier top (-9.7, 0.889) |
| `Delineator_Right` | every 12.5 m where there is no guardrail | (11.2, -0.17) |
| `MedianReflectorPost` | every 12.5 m | barrier top (-9.7, 0.889) |
| Gantries | rare (one per several km) | chunk centreline (0, 0) |
| Signs | context | right verge (12.8, -0.30) |

#### 10. Streetlight emissive slots

`MAT_Prop_LightLens` covers the luminaire lens (flat panel under each head), the 6 high-mast floodlight faces, the
warning-beacon dome and the SOS pillar lamp. In Unity make it emissive (≈ 3,000–4,000 K white for luminaires; amber
for the beacon), driven by time of day. **No Unity lights are included.** Recommended light anchors:
- `Streetlight_Single`: luminaire centre at local Unity (-3.4, 10.15, 0). The arm reaches -X, toward the road.
- Median double: Unity (±2.9, 12.1, 0).
- High mast: 6 heads at radius 0.95 m, y 21.45.

#### 11. Sign-face material strategy

All sign graphics are **generic preview art**: no real place names, no country-specific legal set. They are packed in one 2048²
atlas (`T_Signs_Atlas_2K_BaseColor.png`). Each sign face maps to its own rectangle of the atlas, recorded as `ATLAS` in
`scripts/props_common.py`. To make real signs, either paint new content into the same rectangles, or give a sign
instance its own material/texture on the `MAT_Prop_Sign_Face` slot. Backs and edges are `MAT_Prop_Sign_Back`.
Panels are separate from the gantry structure so their faces can be swapped freely. VMS content is a texture
(`T_VMS_Face_BaseColor.png`, 120 × 38 LED dot matrix, "SLOW DOWN"), so replace it with a RenderTexture for live messages.

#### 12. Gantry setup

- `Gantry_4Lane_Full`: origin = **road chunk centreline** (0, 0, 0). Place it at the chunk position plus z. The supports sit
  at Unity x = +12.4 (right verge, behind the guardrail) and x = -10.35 (on the concrete median, behind the barrier). Span is 22.75 m.
  The bottom chord is at y 6.2 (6.1 m+ clear over the crown). There is a maintenance walkway at the back, with signs hanging at the front.
- Panels and frames attach at their own origin (panel bottom centre, back face), relative to the gantry origin at z_g:
  `SignPanel_Large` + `Gantry_SignFrame` → (4.5, 6.0, z_g - 0.80); `Gantry_VMS_Frame` + `VMS_Panel` → (-1.6, 6.2, z_g - 1.285);
  `SignPanel_Medium` → (-6.3, 6.2, z_g - 0.80). Faces look -Z, toward approaching traffic.
- `Gantry_4Lane_Half`: cantilever from the right support to x = -0.6 (over the two right-hand lanes), same origin rule.
- `Gantry_Support_Left` / `_Right` / `Gantry_CrossBeam`: kit parts. Supports have their origin at plinth-base centre; place them at (-10.35, -0.20) and (12.4, -0.45).
  The cross beam uses the road-centre origin.

#### 13. Guardrail modularity

- Origin of every guardrail part = **ground at the post centre line, module start**. Rails run from z 0 → +4 / +8 m.
  `<Asset>_Snap_Start` / `_Snap_End` are 4.000 / 8.000 m apart. Start and end profiles are identical, so modules tile with no seam.
- Posts sit at 1, 3, 5, 7 m, so chained modules never double a post on the seam. Rail top is 0.755 m above local ground,
  and the rail traffic face is 0.36 m in front of the post line.
- Chain: `Guardrail_End_Terminal` (head extends upstream, -z) → n × `Guardrail_WBeam_8m_Assembly` (or 4 m) →
  `Guardrail_Transition` (W → thrie, 4 m) → `Guardrail_To_Concrete_Transition` (6 m, ends in a concrete F-shape block
  whose traffic face is flush with the rail).
- For custom builds: use `Guardrail_WBeam_4m/8m` (rail only) + instanced `Guardrail_Post` + `Guardrail_OffsetBlock` at the post points.

#### 14. Expected 40 m road-grid usage

Every along-road asset is a divisor of 40 m and 20 m: guardrail modules 4 / 8 m, portable barrier 2 m (centre origin,
2.000 m pitch). Lateral placement uses the P0 cross-section: lanes ±7.2, right shoulder to 10.2, drain 10.2–10.7, verge
to ≈12.4 (Unity x positive = right side), concrete median -8.7 … -10.7 with the barrier top at y 0.889. Props are meant to be
placed by Unity (spawner / RoadStreamer decoration lists) per chunk, not merged into chunk meshes.

#### 15. Excluded QA assets

Not in any FBX: the 160 m QA road strip (linked read-only from P0), all `QA_*` instances and library rows, the linked
hypercar scale reference, the blockout boxes (kept only in `props_01_blockout.blend`), cameras, the QA ground, and the
preview lights and world (created only in the unsaved render session). Only `PROPS_MASTER` is exported, and the full list is in
`Reports/P1_props_export_manifest.json`.

---

### `UnityTransfer/README/ROAD_PROPS_TRIM_GUIDE.md`

### RoadProps trim sheet — `T_RoadProps_Trim_2K`

Shared by every structural prop (P1) and reusable by later road, bridge and tunnel kits.

#### Maps (2048 × 2048 PNG, `Textures/trim/`)

| File | Unity import | Notes |
|---|---|---|
| `T_RoadProps_Trim_2K_BaseColor.png` | sRGB, Default | real colours per strip; the plastic strip is neutral 50 % grey, so tint it in the material |
| `T_RoadProps_Trim_2K_Normal.png` | **Normal map**, no flip | tangent space, **OpenGL (+Y / green up)**, Unity's convention |
| `T_RoadProps_Trim_2K_Roughness.png` | Linear (sRGB off) | **roughness**: URP wants smoothness = 1 - R (invert, or pack into Metallic alpha) |
| `T_RoadProps_Trim_2K_Metallic.png` | Linear (sRGB off) | 1 = galvanised / sign backing / bolt strip, 0.8 = fixture metal, 0 = paint / concrete / plastic / reflective |
| `T_RoadProps_Trim_2K_AO.png` | Linear (sRGB off) | URP Lit Occlusion map |

URP Lit packing suggestion: build one mask texture with R = Metallic, A = 1 - Roughness and use it as the Metallic map
(Source = Metallic Alpha), plus the Normal and Occlusion maps. Every trim material can share these textures.

#### Strip layout (horizontal strips, V measured from the bottom; Unity and Blender UV origins are both bottom-left)

| # | Strip | Pixel rows | V range | Content |
|---|---|---|---|---|
| 1 | galvanised rail | 0–256 | 0.0000–0.1250 | cool zinc, soft spangle, mid roughness |
| 2 | painted steel (light) | 256–512 | 0.1250–0.2500 | off-white paint, orange peel |
| 3 | painted steel (dark) | 512–768 | 0.2500–0.3750 | dark grey paint |
| 4 | concrete edge | 768–1024 | 0.3750–0.5000 | light concrete with pores |
| 5 | reflective strip (white) | 1024–1152 | 0.5000–0.5625 | microprism sheeting (also lamp lenses) |
| 6 | reflective chevron | 1152–1280 | 0.5625–0.6250 | yellow/black 45° chevron, 0.125 m pitch |
| 7 | rubber / plastic | 1280–1536 | 0.6250–0.7500 | neutral moulded plastic, tinted per material |
| 8 | light-fixture metal | 1536–1664 | 0.7500–0.8125 | cast/painted luminaire housing |
| 9 | sign backing | 1664–1792 | 0.8125–0.8750 | brushed aluminium (grain along U) |
| 10 | utility metal | 1792–1920 | 0.8750–0.9375 | painted cabinet sheet, panel seam every 1 m, louvre band |
| 11 | bolt / rivet strip | 1920–2048 | 0.9375–1.0000 | galvanised plate, two bolt rows every 0.125 m |

In an image viewer the PNG's top row is V = 1, so the bolt strip appears at the top and galvanised at the bottom.

#### UV convention

- Strips **tile in U only**. U = metres along the member / 4 → 1 U = 4 m = 2048 px = **512 px/m** along every member
  (the same density as the P0 road kit). U values outside 0–1 are intended; the sampler must be set to Repeat.
- V = position across the profile (tube circumference, beam profile, box face) scaled into the strip, with a 2 px guard band
  on each side. Every face stays inside one strip, which validation checks.
- Undersides, buried post ends and hidden contact faces are not modelled, so no texture space is spent on them.

#### Which assets use which strip

| Strip | Materials | Asset families |
|---|---|---|
| galvanised | `MAT_Prop_GalvanizedSteel` | W/thrie-beam rails, guardrail posts, crash-cushion frames and fenders, all poles and arms, high mast, gantry trusses, walkway, sign posts, sign frame, CCTV pole |
| painted light | `MAT_Prop_PaintedMetal_Light` | delineator bodies, edge markers |
| painted dark | `MAT_Prop_PaintedMetal_Dark` | dark accents (solar-panel faces) |
| concrete | `MAT_Prop_Concrete` | gantry plinths, cabinet plinths, barrier end / concrete transition, SOS plinth |
| reflective white | `MAT_Prop_Reflective`, `MAT_Prop_LightLens` | delineator / barrier / cone / drum reflectors; luminaire, floodlight and beacon lenses |
| reflective chevron | `MAT_Prop_Reflective` | crash-cushion nose panel, guardrail terminal face |
| rubber / plastic | `MAT_Prop_Plastic_Orange`, `MAT_Prop_Plastic_Black`, `MAT_Prop_Rubber` | cones, drums, bollards, barrels, portable barrier, offset blocks, delineator caps, beacon housing |
| fixture metal | `MAT_Prop_PaintedMetal_Dark` | streetlight luminaire housings, high-mast floodlights |
| sign backing | `MAT_Prop_Sign_Back` | backs and edges of every sign and gantry panel |
| utility metal | `MAT_Prop_PaintedMetal_Light`, `_Dark` | utility cabinets, VMS cabinet, CCTV camera, radar / weather sensor housings, radiation shield |
| bolt strip | `MAT_Prop_GalvanizedSteel` | pole base plates, gantry leg base plates, sign clamps, frame brackets, CCTV mount plate |

Coverage: the trim sheet carries **99.3 %** of all production triangles. The rest are sign faces (sign atlas) and the VMS face.

#### Material tints used in the Blender preview (multiply the BaseColor)

| Material | Tint (linear) | Notes |
|---|---|---|
| `MAT_Prop_Plastic_Orange` | (4.2, 0.85, 0.09) × the 50 % grey strip | gives traffic orange ≈ (0.90, 0.18, 0.02) linear |
| `MAT_Prop_Plastic_Black` | 0.10 | |
| `MAT_Prop_Rubber` | 0.07, roughness +0.15 | |
| all others | 1.0 | the strip already holds the colour |

---

### `reports/P1_props_discovery.md`

### P1-BLENDER-01 — Core Roadside Props: Discovery

Date: 2026-10-06 · Blender 5.2.2 · Blender-only workstation

#### 1. Road foundation (linked read-only from `P0_RoadFoundation/blend/road_05_export_ready.blend`)

Measured from the linked meshes; matches the P0 spec:

| Item | Blender X (driver-left = +X) | Z (m) |
|---|---|---|
| Lanes, 4 × 3.60 | -7.2 … +7.2 (dividers -3.6 / 0 / +3.6) | crown +0.036 at X 0; ±3.6 → 0.000; ±7.2 → -0.036 |
| Road module edge (edge strips) | ±7.7 (skirt ±7.75) | -0.046 |
| Outer (right) shoulder | -7.7 … -10.2 | -0.046 → -0.1085 |
| Drain channel | -10.2 … -10.7 | lip -0.1085 |
| Verge (irregular) | -10.7 … ≈-12.4 | → ground -0.30 |
| Inner (left) shoulder | +7.7 … +8.7 | → -0.071 |
| Concrete median | +8.7 … +10.7 | top +0.084 |
| Median barrier (F-shape) | centre +9.7, base 9.395 … 10.005 | top +0.889 |
| Grass median (alternative) | +8.7 … +14.7 | swale ≈ -0.19 |

Module endpoints: Y 0 → -40.000 (20 m: -20.000). Orientation: +Z up, travel toward -Y, so traffic **approaches
from +Y**. Unity after export: +Y up, +Z forward, point (x, y, z) → (-x, z, -y).

Other references: there are no roadside-prop images, models or old assets anywhere in the workspace. `references/` is
empty. Everything is built from the road kit plus real-world highway infrastructure proportions.

#### 2. Placement assumptions (QA strip and README offsets)

| Prop | Position (Blender) | Why |
|---|---|---|
| Right W-beam guardrail | post line X -11.0, ground ≈ -0.16 | in the verge just outside the drain channel; rail face 0.36 m toward the road |
| Right streetlights | X -12.0, every 40 m | behind the guardrail; 3.0 m arm puts the luminaire over the hard shoulder |
| Median twin streetlights | on the barrier top, X +9.7, Z +0.889, every 40 m | standard barrier-mounted median lighting |
| Gantry supports | right X -12.4 (plinth in the verge, behind the guardrail); left X +10.35 (median, behind the barrier) | nothing intrudes into lanes or shoulders |
| Roadside signs | X -12.8 | outside the verge |
| Delineators | X -11.2 where there is no guardrail; median barrier: MedianReflectorPost on the barrier top | |
| Crash cushion | in front of the median-barrier start, nose toward +Y | |

#### 3. Standard dimensions chosen

| Family | Key dimensions |
|---|---|
| W-beam guardrail | rail 310 mm tall, 83 mm deep, centre 0.60 m → top **0.755 m**; posts every **2.0 m** at 1 / 3 / 5 / 7 m (never on the module seam); 200 mm offset blocks; modules 4.000 / 8.000 m |
| Thrie-beam (transitions) | 508 mm, 3 corrugations, centre 0.60 m |
| Streetlight | pole **10.0 m** (median twin 12.0 m), Ø220 → Ø120 mm, arm reach 3.0 m (median 2.5 m), luminaire 0.75 × 0.32 m |
| High mast | **22 m**, 16-sided Ø640 → Ø260 mm, ring head Ø1.8 m with 6 floodlights |
| Gantry | span **22.75 m** (X -12.4 … +10.35); truss 1.2 m (Y) × 1.4 m (Z); bottom chord 6.2 m → ≥6.1 m clear over the crown |
| Gantry panels | Large 6.0 × 3.0, Medium 4.0 × 2.5, Small 2.5 × 1.5, Exit 3.0 × 0.9, LaneArrow 3.0 × 2.2, VMS 5.0 × 1.6 |
| Road signs | circle Ø0.90, triangle 1.05, rectangles 1.0–2.4 m; panel bottom 2.0 m above the post base |
| Delineator | 1.0 m above ground, 120 × 100 mm section |
| Traffic cone | 0.75 m; drum 0.92 m |

#### 4. Grid / modularity decisions

- Everything that runs along the road is a 4 m or 8 m multiple: guardrails, portable barrier (2 m). That divides the 40 / 20 m chunks.
- Guardrail posts sit at odd metres, so chained modules never double a post on the seam.
- Repeating props are **separate instanced assets** with their own origin, and are not baked into road chunks.
  Spacing (lights 40 m, delineators 12.5 m, …) is a placement decision made in Unity.
- Assemblies (`Guardrail_WBeam_8m_Assembly`, `Gantry_4Lane_Full`, streetlights) are merged per-LOD meshes for one-draw
  placement. The parts are also exported separately.

#### 5. Art direction

Modern, clean, engineered motorway infrastructure. Galvanised steel, light/dark painted steel, concrete, orange
plastics, white/yellow-black retroreflective sheeting. Geometry goes into silhouettes: W-beam corrugation, tapered poles, truss
members, cushion bays. Bolts, galvanising spangle, louvres and brushing come from the trim sheet's normal/roughness maps.
No rust, no sci-fi, no decorative detail invisible from the driving camera.

#### 6. Material strategy

12 shared materials: GalvanizedSteel, PaintedMetal_Light, PaintedMetal_Dark, Concrete, Plastic_Black,
Plastic_Orange, Rubber, Reflective, Sign_Back, Sign_Face, LightLens, VMS.
- Structural materials all sample **one** 2048² trim sheet (`T_RoadProps_Trim_2K`: BaseColor / Normal / Roughness / Metallic / AO)
  with 11 horizontal strips that tile in U. UVs are generated at build time: U = metres along the member / 4 m
  (512 px/m), V = position across the profile inside the strip.
- `Sign_Face` uses a 2048² generic sign atlas (no real place names). `VMS` uses its own dot-matrix face texture.
- `Reflective` and `LightLens` stay separate slots for Unity's night treatment and emission.

---

### `reports/P1_props_validation.txt`

```text
== P1-BLENDER-01 CORE ROADSIDE PROPS — VALIDATION ==
source: blend/props_07_export_ready.blend; PROPS_MASTER objects 250, meshes 188

[PASS] all required assets exist (65 required, 65 built, 8 families)
[PASS] all 8 families populated
[PASS] naming: no .001 suffixes / illegal characters
[PASS] LOD hierarchy: <Asset> empty -> <Asset>_LOD0..n (contiguous); single-LOD assets are plain meshes
[PASS] transforms: every asset root at origin, every mesh identity world matrix (scale 1, no rotation)
[PASS] no zero/negative scale
[PASS] topology: no non-manifold edges, loose geometry, zero-area faces, ngons >4, duplicate or coincident faces (188 meshes)
[PASS] normals: consistent winding on every shared edge; every closed shell faces outward
[PASS] UVs: UVMap on every mesh; trim faces stay inside one trim strip; sign faces inside atlas rects; VMS in 0-1
[PASS] materials: 12 shared materials, every slot used, colliders without materials
[PASS] trim usage: structural assets (guardrails, gantries, poles, posts, cabinets, CCTV pole, barrier ends) >= 95 % trim-sheet triangles
[INFO] trim sheet carries 99.3% of all 35316 production triangles; the rest are sign faces / VMS (atlas)
[WARN] budget Guardrail_WBeam_8m_Assembly LOD0 784 tris vs suggested 1000-2500
[WARN] budget Guardrail_WBeam_8m_Assembly LOD1 360 tris vs suggested 500-1200
[WARN] budget Streetlight_Single LOD0 460 tris vs suggested 1000-2000
[WARN] budget Streetlight_Single LOD1 218 tris vs suggested 400-900
[WARN] budget Streetlight_Single LOD2 82 tris vs suggested 120-300
[WARN] budget HighMastLight LOD0 668 tris vs suggested 2000-4000
[WARN] budget HighMastLight LOD1 348 tris vs suggested 800-1500
[WARN] budget HighMastLight LOD2 134 tris vs suggested 200-500
[WARN] budget Gantry_4Lane_Full LOD0 1952 tris vs suggested 3000-6000
[WARN] budget Gantry_4Lane_Full LOD1 1082 tris vs suggested 1500-3000
[WARN] budget Gantry_4Lane_Full LOD2 392 tris vs suggested 500-1200
[WARN] budget Gantry_4Lane_Full LOD3 132 tris vs suggested 150-400
[WARN] budget Sign_SpeedLimit LOD0 148 tris vs suggested 200-600
[WARN] budget Sign_SpeedLimit LOD1 60 tris vs suggested 80-250
[WARN] budget Sign_SpeedLimit LOD2 12 tris vs suggested 20-80
[PASS] LOD chains strictly decreasing (49 LOD groups)
[INFO] LOD triangle chains (LOD0 / LOD1 / ...):
      Guardrail_WBeam_4m                 304 / 144 / 48   (100% / 47% / 16%)
      Guardrail_WBeam_8m                 608 / 288 / 96   (100% / 47% / 16%)
      Guardrail_WBeam_8m_Assembly        784 / 360 / 160   (100% / 46% / 20%)
      Guardrail_End_Terminal             572 / 280 / 76   (100% / 49% / 13%)
      Guardrail_Transition               696 / 324 / 56   (100% / 47% / 8%)
      Guardrail_Median_Variant           1432 / 680 / 288   (100% / 47% / 20%)
      Guardrail_To_Concrete_Transition   730 / 360 / 82   (100% / 49% / 11%)
      CrashCushion_Main                  1022 / 542 / 184   (100% / 53% / 18%)
      CrashCushion_Short                 536 / 296 / 112   (100% / 55% / 21%)
      ImpactAttenuator                   2340 / 1134 / 450   (100% / 48% / 19%)
      Barrier_End_Transition             116 / 44 / 12   (100% / 38% / 10%)
      Streetlight_Single                 460 / 218 / 82 / 36   (100% / 47% / 18% / 8%)
      Streetlight_Double                 636 / 314 / 124 / 60   (100% / 49% / 19% / 9%)
      Streetlight_Median_Double          636 / 314 / 124 / 60   (100% / 49% / 19% / 9%)
      HighMastLight                      668 / 348 / 134 / 100   (100% / 52% / 20% / 15%)
      Gantry_4Lane_Full                  1952 / 1082 / 392 / 132   (100% / 55% / 20% / 7%)
      Gantry_4Lane_Half                  1230 / 674 / 246 / 102   (100% / 55% / 20% / 8%)
      Gantry_Support_Left                226 / 166 / 82   (100% / 73% / 36%)
      Gantry_Support_Right               226 / 166 / 82   (100% / 73% / 36%)
      Gantry_CrossBeam                   1272 / 616 / 216 / 72   (100% / 48% / 17% / 6%)
      Sign_SpeedLimit                    148 / 60 / 12   (100% / 41% / 8%)
      Sign_NoStopping                    148 / 60 / 12   (100% / 41% / 8%)
      Sign_CurveWarning                  68 / 20 / 2   (100% / 29% / 3%)
      Sign_Merge                         68 / 20 / 2   (100% / 29% / 3%)
      Sign_LaneEnds                      68 / 20 / 2   (100% / 29% / 3%)
      Sign_WorkZone                      68 / 20 / 2   (100% / 29% / 3%)
      Sign_RouteMarker                   64 / 24 / 6   (100% / 38% / 9%)
      Sign_Exit                          84 / 28 / 4   (100% / 33% / 5%)
      Sign_Direction                     108 / 28 / 4   (100% / 26% / 4%)
      Sign_Emergency                     84 / 28 / 4   (100% / 33% / 5%)
      Delineator_Left                    72 / 22 / 20   (100% / 31% / 28%)
      Delineator_Right                   38 / 20 / 18   (100% / 53% / 47%)
      Delineator_Double                  48 / 22 / 20   (100% / 46% / 42%)
      MedianReflectorPost                30 / 14 / 8   (100% / 47% / 27%)
      EdgeMarker                         84 / 42 / 28   (100% / 50% / 33%)
      TrafficCone                        178 / 94 / 40   (100% / 53% / 22%)
      TrafficCone_WithReflectiveBands    370 / 190 / 88   (100% / 51% / 24%)
      FlexibleBollard                    240 / 120 / 90   (100% / 50% / 38%)
      RoadDrum                           552 / 276 / 152   (100% / 50% / 28%)
      WarningBeacon                      90 / 34   (100% / 38%)
      PortableBarrier                    100 / 44 / 12   (100% / 44% / 12%)
      CCTV_Camera                        70 / 40   (100% / 57%)
      CCTV_Pole                          324 / 154 / 24   (100% / 48% / 7%)
      UtilityCabinet_Small               54 / 20   (100% / 37%)
      UtilityCabinet_Large               76 / 20   (100% / 26%)
      EmergencyPhoneBox                  46 / 24   (100% / 52%)
      SOS_Pillar                         70 / 40   (100% / 57%)
      RoadsideSensor                     84 / 54   (100% / 64%)
      WeatherSensor                      384 / 106   (100% / 28%)
[PASS] required colliders exist (Collision_Guardrail_8m, Collision_CrashCushion, Collision_Streetlight, Collision_Gantry_Left, Collision_Gantry_Right, Collision_UtilityCabinet)
[PASS] 26 colliders: closed, no materials, in PROPS_COLLIDERS, parented to their asset, overlapping the asset
[PASS] guardrail parts without posts keep the system origin (ground at the post line): rail bottom 0.445 m, block bottom 0.43 m
[PASS] origins: 39 ground-standing assets have their base at Z 0 (posts may be embedded <= 50 mm)
[PASS] origins: poles / posts / cones / cabinets centred on their base (pole centre at X,Y 0)
[PASS] signs: origin at post base, panel bottom exactly 2.000 m above it
[PASS] gantry panels: origin at panel bottom centre
[PASS] gantry: spans the road from the road-centre origin, supports outside lanes and shoulders, >= 6.0 m clear over the crown
[PASS] Guardrail_WBeam_4m: snap distance 4.000 m, rail geometry exactly 0 .. -4 (tiles with no seam)
[PASS] Guardrail_WBeam_8m: snap distance 8.000 m, rail geometry exactly 0 .. -8 (tiles with no seam)
[PASS] Guardrail_WBeam_8m_Assembly: snap distance 8.000 m, rail geometry exactly 0 .. -8 (tiles with no seam)
[PASS] Guardrail_Median_Variant: snap distance 8.000 m, rail geometry exactly 0 .. -8 (tiles with no seam)
[PASS] Guardrail_Transition: snap distance 4.000 m, rail geometry exactly 0 .. -4 (tiles with no seam)
[PASS] guardrail W-beam modules: start profile == end profile (4 m / 8 m / assembly, LOD0)
[PASS] guardrail rail top 0.70-0.80 m above local ground, posts every 2.0 m
[PASS] Streetlight_Single: height 10.248 m within 9.0-12.5
[PASS] HighMastLight: height 22.470 m within 18-25.5
[PASS] Delineator_Right: height 1.000 m within 0.95-1.05
[PASS] TrafficCone: height 0.750 m within 0.74-0.76
[PASS] RoadDrum: height 0.920 m within 0.9-0.95
[PASS] Streetlight_Single arm outreach 3.75 m (1.5-3.0 m target + luminaire)
[PASS] export selection == PROPS_MASTER; no QA / P0 / hypercar / camera / blockout objects; no leaked selection
[PASS] texture files referenced by production materials exist (7)
[PASS] no export-time ngon triangulation or duplicate-face removal was needed
[PASS] FBX re-import: 8 files re-imported with 0 problems (see P1_props_reimport_validation.txt)

SUMMARY: 0 errors, 15 warnings (warnings = LOD-ratio / budget targets, non-critical)
```

---

### `reports/P1_props_reimport_validation.txt`

```text
== P1-BLENDER-01 FBX RE-IMPORT VALIDATION ==
Each FBX imported into a factory-empty Blender scene (default FBX importer axes).

[PASS] Guardrails.fbx: 43 objects (18 LOD meshes, 6 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] RoadSafety.fbx: 51 objects (32 LOD meshes, 6 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] Streetlights.fbx: 26 objects (16 LOD meshes, 4 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] Gantries.fbx: 34 objects (18 LOD meshes, 3 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] RoadSigns.fbx: 44 objects (30 LOD meshes, 0 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] Delineators.fbx: 20 objects (15 LOD meshes, 0 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] Infrastructure.fbx: 32 objects (17 LOD meshes, 7 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes
[PASS] roadside_props_complete.fbx: 250 objects (146 LOD meshes, 26 colliders) - names, hierarchy, scale 1, world bbox, materials, UVs, tris, snaps, axes

Orientation: Streetlight_Single_LOD0 spans file-space Y 0 -> 10.25 (up = +Y); Guardrail_WBeam_8m_LOD0 spans file-space Z 0 -> 8
(forward = +Z); Unity reads FBX as-is with Bake Axis Conversion OFF and mirrors X (Blender +X driver-left -> Unity -X).

SUMMARY: 0 errors
```

---

### `reports/P1_P0_road_integrity_check.md`

### P1 → P0 Road Foundation integrity check

| | |
|---|---|
| Linked source | `environment/P0_RoadFoundation/blend/road_05_export_ready.blend` (stored in P1 blends as `//../../P0_RoadFoundation/blend/road_05_export_ready.blend`) |
| How it was used | `bpy.data.libraries.load(link=True)`: 11 meshes linked read-only into `PROPS_QA` for the 160 m QA strip. The P0 file was never opened for writing or saved. |
| Baseline | SHA-1 + size + mtime of every file under `P0_RoadFoundation/`, taken before any P1 work (`reports/P1_P0_baseline_hashes.json`, 95 files) |
| Re-check | after export, packaging and validation (`reports/P1_P0_integrity_result.json`) |

#### Result: PASS

- Files: **95 before, 95 after**. Added: none. Removed: none.
- Content (SHA-1) changed: **none**. Timestamps (mtime) changed: **none**.
- `P0_RoadFoundation/blend/`, `exports/` and `UnityTransfer/` are byte-identical to the baseline. No P0 source file was overwritten.

The hypercar reference (`new_car/hypercar_08_unity_export.blend`, collection `Car_LOD3`) was also only linked. Its
modification time is still 2026-10-06 12:26, from before this phase.

