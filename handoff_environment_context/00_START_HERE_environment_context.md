# Highway Racer — Blender environment: full project context (read this first)

This bundle gives you the complete context of the **Blender environment work** for my Unity endless-highway traffic racer: nine phases, P0 to P3, all **finished and frozen**.

Read this file first. It explains the project, the rules every phase followed, the shared technical conventions, what each phase delivered, how the phases connect, and the known limitations. The other files go deeper (index in §10).

A separate bundle, `handoff_vehicle_remaster/`, covers the cars: the frozen Hypercar plus the planned player-car and traffic remasters.

---

## 1. How to work with me on this project

- **You can't run Blender or see my disk.** I run your scripts on my Mac and send you the console output, reports and renders.
  - Blender **5.2.2 LTS** on macOS.
  - Command: `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python <script.py> -- <args> </dev/null`
- **All environment phases are FROZEN.** Never propose edits to their files. New work may only **link them read-only** with `bpy.data.libraries.load(path, link=True)`. If new work exposes a problem in a frozen phase, document it and leave the phase untouched.
- **This workstation is Blender-only.** Unity is not installed here. Never write Unity prefabs, C# or shaders. Unity integration happens later, on another machine, from the `UnityTransfer/` packages.
- **The road never changes.** It is straight and level, built from **40 m** modules (20 m as the secondary length). Never curved, sloped or banked.
- **Phase discipline** (every phase so far followed it):
  1. Work in order: discovery, blockout, build stages, materials, LODs and colliders, QA, export, validation, packaging, freeze. Then **STOP** and wait for my approval.
  2. Checkpoints are numbered (`<phase>_01_blockout.blend` … `_07_export_ready.blend`) and **never overwritten**. Iterations run in a scratch folder, and the official checkpoints are written once.
  3. Record a SHA-1 baseline of every workspace file outside the phase folder before work starts. Re-check it at the end, including a scan for added files.
  4. Every preview render is **reviewed visually**, not only validated by scripts.
  5. Every FBX is **re-imported into a clean scene** and checked: names, hierarchy, triangles, UVs, colour sets, materials, world bounds and Unity-axis coordinates.

## 2. The game and the road (P0 facts everything else is built on)

| Item | Value |
|---|---|
| Road | A single **4-lane carriageway, one travel direction** (endless traffic racer). Lane width 3.60 m; carriageway 14.40 m (x −7.2 … +7.2); road module 15.40 m wide including 0.5 m edge strips |
| Lane centres | x = −5.4, −1.8, +1.8, +5.4. The 1 % crown puts the lane-centre surface at +0.018 / −0.018 m |
| Markings | 0.15 m dashed dividers (4 m dash, 6 m gap); 0.25 m solid edge lines |
| Road kit cross-section | x −10.2 … +8.7. The median strip on the left (+x) extends to +10.7. The right verge carries the drains (x −10.45). P1 guardrails sit at x −11.0, streetlights at −12.0 |
| Modules | 40.000 m and 20.000 m chunks, mixed freely. Origin = chunk start on the road centreline. Every repeating pattern divides 20 m (2 m segments, 4 m UV tile, 10 m marking cycle, 4 m drain / rumble / barrier pitch) |

## 3. Shared technical conventions (identical in every phase)

### Axes and units

| | Blender source | FBX / Unity |
|---|---|---|
| Up | +Z | **+Y** |
| Travel direction (forward) | **−Y** | **+Z** |
| Driver-left / median side | **+X** (`_L`) | **−X** (Unity mirrors FBX X on import) |
| Point | (x, y, z) | **(−x, z, −y)** |

- 1 unit = 1 m.
- `_R` = vehicle right = Blender −X = Unity +X.
- Roadside assets are authored for the **right verge**. Rotate them 180° for the median or left side.

### FBX export (same method as the Hypercar)

- Exporter settings: `axis_forward='-Z'`, `axis_up='Y'`, `apply_scale_options='FBX_SCALE_ALL'`, `bake_space_transform=False`, `colors_type='LINEAR'`, `use_tspace=True`, `mesh_smooth_type='FACE'`, `embed_textures=False`, `path_mode='RELATIVE'`.
- An **in-memory axis bake** is applied before export: mesh data × G and object matrices adjusted, where G = Rot(−90°, X). The bake residual is asserted below 2e-5, or 1e-4 for large offsets. The source blend is never saved after the bake.
- Unity importer settings: Scale Factor 1, Convert Units ON, **Bake Axis Conversion OFF**, Normals Import, Generate Colliders OFF (use the `Collision_*` meshes).

### Structure and naming

- Every asset is an **empty root `<Asset>`** with children `<Asset>_LOD0…LODn`. Unity builds a LOD Group from the suffixes.
- Colliders are named `Collision_*`: simple, no material.
- Road-aligned modules carry `<Asset>_Snap_Start` at (0, 0, 0) and `<Asset>_Snap_End` at (0, −L, 0) in Blender, which is (0, 0, L) in Unity. L = 40.000 or 20.000 exactly.
- Materials in the FBX are **Blender review materials**. Rebuild them in Unity with the same names; each phase's material guide gives the mapping. Textures are external PNGs: BaseColor sRGB, Normal **OpenGL +Y** (no flip in Unity), Roughness → Unity smoothness = 1 − roughness, AO assigned by hand.

### Shared vertex-data contracts

| Name | Where | Meaning |
|---|---|---|
| `TerrainBlend` | Colour attribute (POINT, FLOAT_COLOR, render / export colour), on every terrain mesh from P1 Terrain onward | **R grass, G soil, B rock, A gravel**, normalised (sum 1). It drives `MAT_Terrain_Blend` |
| `VegetationMask` + UV1 `VegetationMaskUV` | Same meshes | Colour **R density, G dryness**; UV1 = (U density, V dryness). Density is 0 in the road / prop corridor, on rock, scree, beaches, cliffs, under bridge decks and near the waterline |
| `WindData` | P1 Vegetation | Per-vertex wind weights for a Unity wind shader (see the vegetation wind guide) |
| `CityWindowData` | P2 City | Per-window data for night emission (R random, G floor, B category, A window) |
| `MC_ShoreData` | P3 coastal meshes | R wetness potential, G foam proximity, B submerged depth, A 1, all derived from the single waterline at z −18 |

### Seams

- The frozen P1 rows `Terrain_Flat` + `TerrainTransition` define the **"P" (plain) boundary profile**. Every later terrain module (P2 BridgeTerrainContext, P3 Mountain & Coastal) starts or ends on exactly that profile, so it joins P1 chunks without cracks.
- Later phases add their own boundary classes: valley profiles in P2 01A; mountain cut **M**, sea cliff **C** and low coast **L** in P3. Any end-class = start-class joint matches to under 1 mm on shared columns.
- **The road corridor is sacred.** Within |x| < 10.7 no terrain vertex rises above −0.289 m, the frozen P1 TerrainTransition level.

### Unity owns (stated in every UnityTransfer README)

Shaders (terrain blend, glass, emission, water), prefabs, LOD Group components, streaming and the road-streamer configuration, culling and HLOD runtime, lighting, fog, weather, water (surface, waves, foam, reflections, underwater), vegetation instancing and wind runtime, quality tiers, and performance profiling. Blender delivers geometry, LOD meshes, simple colliders, reference empties, source materials, textures and FBX.

## 4. The nine phases at a glance

All phases are **COMPLETE and FROZEN**, and every validation reports 0 errors. P1 Props additionally carries 15 non-critical LOD-ratio / budget warnings.

| # | Phase | Folder | Final source blend | FBX | What it is |
|---|---|---|---|---|---|
| 1 | P0-BLENDER-01 Road Foundation | `P0_RoadFoundation` | `road_05_export_ready.blend` | 7 (48 objects) | 4-lane road chunks 40 / 20 m, shoulders (paved, gravel), verges, medians (concrete, grass, barrier), drains and grates, rumble strips, reflectors, joints, road collision. Asphalt 2K + decals |
| 2 | P1-BLENDER-01 Core Roadside Props | `P1_Props` | `props_07_export_ready.blend` | 8 (250 objects) | Guardrails (W-beam, terminals, transitions), crash cushions and safety items, streetlights (single, double, median, high mast), gantries + sign panels / VMS, road signs, delineators, infrastructure (CCTV, cabinets, SOS, radar, weather station) |
| 3 | P1-BLENDER-02 + 02A Terrain & Roadside Transition Kit | `P1_Terrain` | `terrain_09_final_frozen.blend` | 8 | Road-edge transition, flat terrain, cut / fill slopes, retaining walls, rock cuts / cliffs / rocks, drainage, vistas (far ground to 1.5 km). Introduced `MAT_Terrain_Blend` + TerrainBlend / VegetationMask. Terrain ends at d 50 m per side; `Vista_FarGround_A` continues beyond. 02A was the visual polish |
| 4 | P1-BLENDER-03 + 03A Production Vegetation | `P1_Vegetation` | `vegetation_09_final_frozen.blend` | 8 (168 objects) | 8 tree archetypes × 3 variants (broadleaf A–D, small roadside A–B, conifer A–B), 6 shrubs / hedge, 10 grass clumps, 6 weeds, optional colliders. Leaf / bark / grass atlases, WindData, impostor sources. 03A cut hidden wood at LOD0 |
| 5 | P1-BLENDER-04 Modular Tunnel | `P1_Tunnel` | `tunnel_07_export_ready.blend` | 9 | Tunnel shell modules, portals, structures, service / safety (bays, cabinets), lights, ventilation, drainage, collision. Lighting and streaming guides |
| 6 | P2-BLENDER-01 Bridges & Overpasses | `P2_Bridges` | `bridges_07_export_ready.blend` | 9 | Hero overpass (83 m long, 33.5 m main span, minimum clearance 6.18 m), standard / wide overpasses (wide: 5.96 m clearance), bridge deck Start / 40 m / End modules (Start / End overlap 8.7 m into the neighbouring chunks), piers, abutments, barriers, drainage, fixtures, underpass, collision |
| 7 | P2-BLENDER-01A Bridge Terrain Context | `P2_BridgeTerrainContext` | `bridgeTerrain_07_export_ready.blend` | 8 | Terrain under and around bridges: shallow / medium / deep valleys with In / Run / Out (40 + 20 m), approaches and exits, abutment terrain, under-bridge ground, pier ground, ravines, dry riverbeds, stream bed, valley vistas. Linked P1 `MAT_Terrain_Blend`; no new textures |
| 8 | P2-BLENDER-02 City / Urban Highway | `P2_City` | `city_07_export_ready.blend` | 11 | Office, commercial and residential buildings, landmarks, skyline layer, rooftops, service / parking structures, urban structures, building clusters (near / mid / far), HLOD-style LODs, collision. Window atlas with night emission (CityWindowData) |
| 9 | P3-BLENDER-01 Mountain & Coastal Biome | `P3_MountainCoastal` | `mountainCoastal_07_export_ready.blend` | 10 (355 objects) | Mountain slopes / cut modules (In / Run / Out), cliffs, rock cuts, talus / scree, rock clusters, ridges, vistas, distant ranges. Coastal sea-cliff and low-coast modules, rocky shore, pebble / sand beaches, headlands, sea stacks, islands, distant land. Waterline references at z −18, overlooks, small infrastructure kit, colliders |

**Typical phase folder** (`environment/<Phase>/`):
- `blend/` holds the numbered checkpoints and the final source.
- `exports/` holds the FBX files.
- `textures/` holds the PNG sets.
- `previews/` holds the QA renders.
- `reports/` holds discovery, validation, geometry JSON, export manifest, materials, integrity check, freeze record and final report.
- `scripts/` holds every script used.
- `UnityTransfer/` holds FBX + Textures + Reports + README import, placement and performance guides.

## 5. How the phases depend on each other

- **P1 Props** linked the P0 road read-only for scale and clearances. It verified that P0 stayed byte-identical (`P1_P0_road_integrity_check.md`).
- **P1 Terrain** defines the frozen seam rows (`Terrain_Flat`, `TerrainTransition`), the `MAT_Terrain_Blend` / `MAT_Terrain_Concrete` materials and the TerrainBlend + VegetationMask contracts that every later terrain phase reuses.
- **P1 Vegetation** is placed from the terrain `VegetationMask`. Later phases scatter it in their QA scenes as a visual test of the mask.
- **P2 Bridges** sits on the P0 road. **P2 BridgeTerrainContext** fills the ground under and around the P2 bridges, starting from the P1 terrain profile and linking `MAT_Terrain_Blend`.
- **P2 City** and **P3 Mountain & Coastal** use the P0 road, P1 props, P1 terrain open chunks and P1 vegetation as linked QA context. P3's modules start and end on the P1 "P" profile.
- **The Hypercar** (`new_car/`, frozen) appears in every QA scene for scale. Its own conventions are in the vehicle bundle.

## 6. Cross-phase known limitations (details in each digest)

- **Open land ends early.** The P1 terrain ends at |x| 50 m on open-road chunks. Unity needs far ground beyond that; the QA scenes used preview planes or strips.
- **P2 BridgeTerrainContext** reaches 100 m on bridge and approach chunks. `BridgeAbutmentTerrain` is authored for the Overpass_Hero abutment positions.
- **P3 mountain In / Out ends.** These modules rise to the full mountain profile within 40 m (20 m variants), which reads as a steep end face from high aerial views. Neighbouring modules at different LODs can show small T-junction cracks.
- **No water was authored anywhere.** P3 provides the waterline references and `MC_ShoreData` only; Unity owns the water.
- **Stale Vegetation README table.** The triangle table in `VEGETATION_IMPORT_NOTES.md` predates the 03A polish. Use the 03A numbers (digest 04).
- **Preview look is not final.** All previews are Blender Eevee QA renders; the final look, lighting and performance belong to Unity.

## 7. Paths

| Path | What |
|---|---|
| `/Users/meetshah/Documents/blender/` | Workspace root |
| `environment/<Phase>/` | The nine frozen phases (above) |
| `new_car/hypercar_08_unity_export.blend` | Frozen flagship Hypercar |
| `racing_car_00 … 09.blend` | An earlier, unnamed generic racing car |
| `handoff_vehicle_remaster/` | Separate bundle for the planned vehicle and traffic work |
| `handoff_environment_context/` | This bundle |

## 8. What's next

- **Unity integration has not started.** It will use each phase's `UnityTransfer/` package.
- **The next Blender work is vehicles:** Zero Gap R, Titan GT, Vortex R, Raven XR, Pulse EV, the traffic remaster and a traffic fleet. See `handoff_vehicle_remaster/`.
- **No new environment biome is planned yet.** If I start one, follow the phase discipline in §1 and the conventions in §3, and start or end every terrain module on the P1 "P" profile.

## 9. How to answer questions about this project

- Quote file names and numbers from the digests. Don't guess.
- If something isn't in the bundle, ask me to run a script or paste the file.
- Treat the original specs (files 10–11) as the requirements and the digests as what was actually delivered. Where they differ, the digest's final report explains why.

## 10. Bundle index

| File | Content | Size (≈ tokens) |
|---|---|---|
| `00_START_HERE_environment_context.md` | This overview | ~4k |
| `01_P0_RoadFoundation.md` | Road: import notes, discovery, validation, object index | ~6k |
| `02_P1_Props.md` | Props: import notes, trim guide, discovery, validation, re-import, P0 integrity, asset index | ~10k |
| `03_P1_Terrain.md` | Terrain + 02A: import notes, blend guide, polish report, discovery, freeze, validation, asset index | ~10k |
| `04_P1_Vegetation.md` | Vegetation + 03A: final report, import / placement / impostor / wind guides, materials, discovery, freeze, validation, asset index | ~14k |
| `05_P1_Tunnel.md` | Tunnel: final report, import / lighting / streaming guides, materials, freeze, validation, asset index | ~13k |
| `06_P2_Bridges.md` | Bridges: final report, import / streaming / performance guides, materials, freeze, validation, asset index | ~13k |
| `07_P2_BridgeTerrainContext.md` | Bridge terrain: final report, import / composition / performance guides, materials and masks, freeze, validation, asset index | ~10k |
| `08_P2_City.md` | City: final report, import / placement / material / performance guides, materials, scale audit, freeze, validation, asset index | ~13k |
| `09_P3_MountainCoastal.md` | Mountain & Coastal: final report, import / placement / waterline / performance guides, materials and masks, freeze, validation, asset index | ~13k |
| `10_original_specs_P0_P1.md` | My original instructions for P0, P1-01, 02, 02A, 03, 03A (+ closure), 04, verbatim | ~55k |
| `11_original_specs_P2_P3.md` | My original instructions for P2-01, 01A, 02 and P3-01, verbatim | ~36k |
| `images/01 … 09_*_previews.jpg` | One 2×2 contact sheet of real QA renders per phase | images |

Each digest starts with the phase's checkpoints, FBX files, textures and previews counts, then a **generated asset index** (every LOD group with triangles per LOD and the FBX it ships in), then the phase's own documents verbatim. Validation lists keep every check line but drop the long evidence text, and SHA-1 tables are omitted. The complete originals stay in the frozen phase folders.
