# Vehicle & Traffic Remaster — project handoff (read this first)

You are joining a Blender-only 3D asset pipeline for a Unity endless-highway traffic racer.
- The **environment** (road, props, terrain, vegetation, tunnel, bridges, city, mountain/coastal biome) is finished and frozen.
- The **flagship Hypercar** is finished and frozen.
- The next work is **remastering and rebuilding the other player cars**, plus **the traffic vehicles**.

This file holds everything you need: how we work, what exists, the conventions every vehicle must follow, the improved phase plan with budgets and gates, and your first task. The other attached files are reference material from the finished Hypercar.

---

## 1. How we work together (important)

- **You can't run Blender or see my disk.** I run your scripts on my Mac and send back the console output, report files and preview images.
  - Blender **5.2.2 LTS**, macOS.
  - Command: `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python <script.py> -- <args> </dev/null`
- **Write complete, runnable scripts.** No fragments like "add this to your scene". Each script:
  - Starts with `import sys; sys.dont_write_bytecode = True`, so no `__pycache__` lands in my folders.
  - Is deterministic. Seed with `random.Random(n)`. Derive name-based seeds with `zlib.crc32(name.encode())`, **never** Python's salted `hash()`.
  - Takes its arguments after `--`. Prints clear lines: `SAVED <path>`, `RENDERED <path>`, `[PASS] ...` / `[FAIL] ...`, `SUMMARY: N errors, M warnings`.
  - Supports a **scratch mode** through an environment variable (for example `VEH_SCRATCH=/some/tmp`). Iterations then write checkpoints and exports to a scratch folder, and the official checkpoints are written **once**, at the end.
  - Before saving a checkpoint: `assert SCRATCH or not os.path.exists(path)`. **Never overwrite a checkpoint.**
  - Never saves a file it only opened to read, export, render or validate.
- **Frozen material is linked read-only and never imported.** Use `bpy.data.libraries.load(path, link=True)`. Never edit or re-save a frozen file.
- **One phase at a time.** Each phase ends with a **completion gate**: the validator reports 0 errors and every preview has been reviewed. Then you freeze the folder, write the final report and **STOP** until I approve the next phase.
- **You must look at every preview I send you** and call out problems:
  - floating geometry, gaps, z-fighting;
  - inverted normals, shading seams, stretched UVs;
  - wrong scale, wheels not touching the ground, intersecting parts;
  - missing lights or glass, ugly LOD pops.

  Validators alone are not enough.

## 2. Project state (2026-10-08)

| Item | State |
|---|---|
| Game | Unity endless traffic racer. A single straight 4-lane carriageway, **one travel direction**, streamed in 40 m road modules. |
| Pipeline | **Blender only.** Unity is not on this machine. Never create Unity prefabs, C# scripts or shaders; Unity integration happens later, separately. |
| Environment P0–P3 | **Complete and FROZEN**: P0 Road, P1 Props / Terrain / Vegetation / Tunnel, P2 Bridges / BridgeTerrainContext / City, P3 Mountain & Coastal. Read-only. |
| Hypercar (`new_car/`) | **Complete and FROZEN.** Flagship player car and the **reference for every vehicle convention** (see `01_hypercar_reference_reports.md`). Do not touch it. |
| `racing_car_00 … 09.blend` (workspace root) | An earlier, unnamed generic racing car (4.58 m long, 2.70 m wheelbase, LOD0–3, 27 materials). As far as I know it is **not** one of the five player cars. Ask me before using it as a base. |
| Zero Gap R, Titan GT, Vortex R, Raven XR, Pulse EV | **Not in the Blender workspace yet.** They live in the Unity project. I will export them for you (see §8). |
| Existing traffic cars | **Not in the Blender workspace yet.** I will export them too. |

## 3. Workspace paths

| Path | What |
|---|---|
| `/Users/meetshah/Documents/blender/` | Workspace root |
| `new_car/hypercar_08_unity_export.blend` | Hypercar final source (FROZEN, read-only) |
| `new_car/reports/`, `new_car/scripts/` | Hypercar reports and scripts (FROZEN; digests attached) |
| `environment/P0_RoadFoundation/blend/road_05_export_ready.blend` | Frozen road. Link these meshes read-only for road-context QA renders: `Road_4Lane_40m`, `Road_4Lane_40m_EdgeLines`, `Road_4Lane_40m_Dividers`, `Shoulder_Paved_R`, `Shoulder_Paved_L`, `Median_Concrete`, `Median_Barrier_LOD0` |
| `vehicles/<ID>_<Name>/` | **New:** one folder per vehicle phase (layout in §6) |

**Road facts for QA scenes and traffic:**
- Lane width 3.60 m. Lane centres are at **x = −5.4, −1.8, +1.8, +5.4** (Blender), and the carriageway runs from −7.2 to +7.2.
- Traffic drives toward **−Y**. Place cars at z ≈ 0.018, the crown height at the lane centres.
- Each road module is 40 m long, from y 0 to −40.

## 4. Vehicle conventions (mandatory, taken from the Hypercar)

The full details and the code are in the attachments. This is the contract every new vehicle must meet.

### 4.1 Axes, units, transforms

- Units: 1 BU = 1 m, metric.
- Blender axes: **+Z up, car nose toward −Y, vehicle left = +X** (left-hand drive, driver seat on the left).
- The FBX gets an explicit in-memory axis bake: `world' = world @ G⁻¹`, `mesh' = G·v`, where `G = Rot(−90°, X)`.
  - Exporter settings: `axis_forward='-Z'`, `axis_up='Y'`, `apply_scale_options='FBX_SCALE_ALL'`, `bake_space_transform=False`, `use_tspace=True`, `mesh_smooth_type='FACE'`, `add_leaf_bones=False`, `bake_anim=False`, `path_mode='RELATIVE'`, `embed_textures=False`, `object_types={'EMPTY','MESH'}`, `use_selection=True`.
  - In Unity: forward **+Z**, up **+Y**, vehicle left **−X**. A point (x, y, z) in Blender becomes **(−x, z, −y)** in Unity.
  - Assert that the bake residual is below 2e-5 (1e-4 when offsets are large).
- `Car_Root` sits at the origin with identity rotation and scale 1. **All scales are applied.**
- The origin is ground-centre, under the middle of the wheelbase.

### 4.2 Hierarchy and naming

```
Car_Root                         (empty, identity)
 ├─ LOD0_Root … LOD3_Root        (empties, identity; LODs overlap exactly)
 │   └─ <Part>_LODn              e.g. Body_LOD0, Glass_LOD0, Headlight_L_LOD0, Interior_LOD0 …
 │      ├─ SteerPivot_FL_LODn / SteerPivot_FR_LODn  (front: yaw on local Y about the wheel centre, ±25°)
 │      │   └─ Wheel_FL_LODn      (roll on local X; tire + brake disc are children; caliper steers but does not roll)
 │      └─ Wheel_RL_LODn / Wheel_RR_LODn (rear: roll on local X)
 ├─ Collision                    (empty) → Collision_Front / _Body / _Side_L / _Side_R / _Cabin / _Rear …
 ├─ WheelColliderRef_FL / FR / RL / RR  (empties at the exact wheel centres; custom properties radius_m, width_m)
 └─ CenterOfMass                 (empty; centreline, low, slightly rear-biased)
```

- Use exact names with LOD suffixes, and no default names (`Cube.001` and the like).
- Wheel origins sit **exactly** on the rotation centre. Validate with rigid ±30° roll and ±25° steer tests: error below 0.001 mm, calipers static on roll.
- Optional animated parts keep correct pivots: doors (hinge, local X), steering wheel (column hub), paddles, active spoiler. Pivots only; no animation data is exported.

### 4.3 Colliders

- Use **4–6 convex hull pieces for player cars** and **1–3 for traffic**.
- Each piece is closed, has outward normals and **≤ 255 triangles**. No material, no UVs. In Unity they become MeshColliders with Convex ON and the renderer off.
- The Hypercar's total is 392 triangles across 6 pieces.

### 4.4 Materials and light channels

- Opaque parts are **baked into per-group atlases**: Body_Paint, Trim, Wheels, Tire, Brakes, Interior, Lights, Glass. Each atlas has BaseColor (sRGB), Metallic, Roughness, Normal (**OpenGL +Y**) and AO.
- Some materials **stay separate** because the game drives them at runtime or they need a special shader:
  - Paint: clear coat, colour-swappable.
  - Glass: thin, transparent, a single optical sheet.
  - Headlight lens and taillight lens.
  - **Light channels**: `MAT_LED_White` (DRL), `MAT_ProjectorLens` (low/high beam), `MAT_LED_Red` (tail), `MAT_LED_Brake`, `MAT_LED_Amber` (indicators), `MAT_LED_Reverse`.
  - Caliper colour.
  - Displays (optional).
- Name engine materials consistently (`LODMAT_*` for atlases, `MAT_*` for separate ones).
- Textures are **external**, with relative paths, at 4096 (body, interior) or 2048 / 1024 (others). Unity smoothness = 1 − roughness.
- **No real brands.** No manufacturer logos, badges, plates or recognisable copied designs. Tire lettering is generic. License plates are blank or a fictional pattern.

### 4.5 LODs

- Every LOD covers the whole car: body, wheels, tires, brakes, glass, lights and interior proxy.
- The **silhouette is preserved**. Bounding-box dimensions stay within a few millimetres of LOD0, and silhouette IoU against LOD0 is ≥ 0.97 (LOD1), ≥ 0.95 (LOD2) and ≥ 0.90 (LOD3) from front, side, top and rear.
- Triangle counts strictly decrease from LOD to LOD, and so do material counts (LOD3 collapses to a few materials).
- Light channels stay separate down to LOD2. LOD3 may merge them into one emissive material with a channel mask.
- Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

### 4.6 Validation pattern (copy it from `02_hypercar_reference_scripts.md`)

- **Per-phase validator**: a `chk()` that writes PASS/FAIL lines to `reports/<car>_validation.txt` and ends with `SUMMARY: N errors`.
- **Topology**: no zero-area faces and no loose verts. N-gons are allowed in source but the export copy is triangulated. Consistent winding, outward normals, no duplicate triangles, no hidden or internal junk geometry.
- **FBX clean re-import** of every exported file into a factory-clean scene, twice:
  - (a) a normal import, comparing names, hierarchy, triangles per object, materials, UV layers, bounding boxes (≤ 1 mm) and pivots;
  - (b) a raw import **without** axis conversion, so you check exactly the coordinates Unity reads: nose +Z, roof +Y, left −X, wheel refs.
- **Integrity**:
  - Before the phase starts, record the SHA-1 of every workspace file outside the phase folder.
  - At the end, re-hash, check for added files, and write `<car>_source_integrity_check.md`.
  - The FBX manifest records file SHA-1s, object lists, excluded objects and the bake residual.

## 5. Budgets (proposed; tell me if you want different numbers)

| Class | LOD0 tris | LOD1 | LOD2 | LOD3 | Materials LOD0 → LOD3 | Textures |
|---|---|---|---|---|---|---|
| Hypercar (reference, frozen) | 206 k | 107 k | 54 k | 18 k | 24 → 15 | Body / interior 4K, others 2K / 1K |
| Player remaster (Zero Gap R, Titan GT) | 100–140 k | 50–70 k | 20–30 k | 6–10 k | ≤ 16 → ≤ 6 | Body 4K, interior 2K, others 2K / 1K |
| Player rebuild (Vortex R, Raven XR, Pulse EV) | 120–160 k | 60–80 k | 25–35 k | 8–12 k | ≤ 18 → ≤ 6 | as the Hypercar |
| Traffic car (sedan / hatch / SUV / pickup) | 12–20 k | 5–8 k | 1.5–3 k | 0.4–0.8 k | **≤ 4 → 2** | Shared fleet atlas, 2K |
| Traffic large (van, box truck, bus) | 18–30 k | 8–12 k | 2.5–4.5 k | 0.6–1.2 k | ≤ 4 → 2 | Shared fleet atlas, 2K |

**Traffic performance rules.** Dozens of traffic vehicles (30–50) must fit on screen at once.
- The **whole fleet shares the same few materials**:
  - `TRF_Body` (atlas; paint colour comes from a paint mask, so Unity can tint per instance);
  - `TRF_Glass`;
  - `TRF_Lights` (one emissive material);
  - `TRF_Tire_Wheel` (atlas).

  These suit GPU instancing and the SRP Batcher.
- **Light channels for traffic are vertex-colour data**, not separate materials: R tail, G brake, B indicator left, A indicator right. Headlights use the UV region or a second attribute. A single Unity shader can then switch brake lights and indicators per instance.
- **Dirt / wear variation** is a grayscale mask channel (vertex colour or a second UV set into the atlas), blended in Unity. There are no extra materials for it.
- **Interiors are fake**: seats, dashboard and steering-wheel silhouettes behind tinted glass, with no detail.
- Brake discs are modelled only where they are visible through the wheels.
- Colliders are 1–3 convex pieces totalling ≤ 150 triangles.

## 6. Folder layout, checkpoints, deliverables (per vehicle phase)

```
vehicles/<ID>_<Name>/          e.g. vehicles/V1_ZeroGapR/
  source_import/   read-only copies of what I export from Unity (never edited)
  blend/           <car>_01_intake … <car>_09_export_ready (written once; never overwritten)
  exports/         <Car>_complete_unity.fbx (LOD0-3 + colliders + refs) and <Car>_LOD0_unity_test.fbx
  textures/<car>/  atlas sets (BaseColor / Metallic / Roughness / Normal / AO)
  previews/        renders (list below)
  reports/         see below
  scripts/         every script used (rerunnable)
  UnityTransfer/   FBX + textures + README (import notes, material mapping, hierarchy, pivots, COM, colliders)
```

**Checkpoint sequence.** Adapt it per scope; rebuilds replace step 02 with a blockout.

| # | Checkpoint |
|---|---|
| 01 | Intake (as imported, measured, untouched) |
| 02 | Cleanup or blockout (orientation, scale, topology, hidden-geometry removal) |
| 03 | Body / exterior (surfacing, front and rear styling, light geometry) |
| 04 | Wheels, tires and brakes |
| 05 | Glass, lights and interior |
| 06 | Materials, UVs and atlases (consolidation, bakes) |
| 07 | LODs |
| 08 | Colliders, hierarchy, pivots and centre of mass |
| 09 | Export ready (FBX written + validated) |

**Required previews** (Eevee, 1920×1080, reviewed by you):
- Front ¾, rear ¾, side, front, rear and top.
- Chase-camera view on the linked P0 road (gameplay distance).
- Close-up of a wheel and brake.
- Interior through the glass.
- Lights test (DRL, tail, brake, indicators and reverse switched on).
- LOD lineup (LOD0–3 side by side at the same scale) and LOD switch-distance comparison.
- Collider overlay, wireframe overlay and before/after (for remasters).
- Traffic only: a fleet lineup, and a chase-distance traffic scene with 30+ instances on the road.

**Required reports:**
- `<car>_intake.md` (what came in, dimensions, triangles, materials, problems found).
- `<car>_validation.txt` and `<car>_geometry.json` (dimensions, triangles per LOD per category, materials per LOD, wheel refs, centre of mass).
- `<car>_export_manifest.json`, `<car>_unity_import_notes.md` and `<car>_unity_material_mapping.md`.
- `<car>_source_integrity_check.md`, `<car>_FINAL_FREEZE.md` (SHA-1 of the final files) and `<car>_FINAL_REPORT.md`.

**Unity-ownership statement** (put it in every README). Unity owns the vehicle controller, physics tuning, WheelCollider setup, prefabs, LOD Group components, shaders (paint, glass, lights), lighting, post-processing, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX only.

## 7. Phase plan (improved)

Do one phase at a time, in this order unless I say otherwise. Each phase gets its own detailed spec from me, or you propose one in the format above and I approve it.

### V0 — Intake (each existing car: Zero Gap R, Titan GT, and the traffic cars)

- Import my exported FBX into a fresh blend in `vehicles/<ID>/blend/<car>_01_intake.blend`.
- Report:
  - orientation and scale problems;
  - dimensions, wheelbase, track, wheel radius and width;
  - triangle count per object and category; material and texture count;
  - hidden or internal geometry, n-gons, flipped normals, non-manifold parts, overlapping UVs;
  - pivots and wheel origins.
- Render the before views.
- This is diagnosis only. **Nothing is fixed in V0.**

### V1 — Zero Gap R: optimisation remaster → production-ready starter car

Keep its identity and proportions. Scope:
- Clean topology.
- **Fix the front-end visual problems** (I will show you which).
- Reduce the material count to atlases plus runtime channels.
- Build LOD0–3.
- Improve wheels and tires: round profile, sidewall, tread, rim depth, brake discs and calipers visible through the spokes.
- Improve glass: a single thin sheet, correct tint, no double surfaces.
- Improve light geometry: real lens and reflector depth, separate channels.
- Organise the interior: seats, dash and wheel silhouettes; remove what can't be seen.
- Remove hidden and internal geometry.
- Fix normals: weighted or custom normals so there are no shading seams on panels.
- Set proper pivots and wheel origins.
- Build colliders and the CenterOfMass reference.
- Build the Unity hierarchy (§4.2) and a clean FBX export with re-import validation.

### V2 — Titan GT: medium remaster

Keep the original identity. Improve:
- body surfacing (panel flow, arches, reflections);
- front and rear styling;
- wheels, lights, glass and interior;
- consolidated materials;
- LODs and colliders.

Show before/after comparisons at every checkpoint.

### V3 — Vortex R: full rebuild

A new, original **modern mid-engine supercar**.
- Full exterior, wheels and brakes, glass, lighting with separate channels, and a simplified interior.
- Materials, UVs and atlases, LODs, colliders and the Unity-ready hierarchy.
- Blockout first: proportions, wheelbase and track, approved by me before surfacing.

### V4 — Raven XR: full rebuild

An original **Japanese-style 2-door front-engine performance coupe**, in the spirit of '90s–'00s JDM coupes but not a copy of any real car.
- Long hood, compact cabin, crisp character lines, pop-out or fixed headlights, a rear wing option.
- Same deliverables as V3.

### V5 — Pulse EV: full or heavy rebuild

An original **electric performance sedan** (4 doors).
- Clean aero surfaces, a closed grille, aero wheel covers, light bars front and rear, flush door handles, a charge-port door, a flat floor and no exhaust.
- Modern interior with screens.
- Same deliverables as V3.

### V6 — Traffic remaster (the existing traffic cars)

Make them convincing at **chase-camera distance** within the traffic budgets (§5):
- better paint (via a paint mask, so colour is per instance in Unity) and realistic glass;
- a basic fake interior (seat, dash and wheel silhouettes);
- better wheels and tires, with brake discs only where visible;
- headlights, brake lights, tail lights and indicators (vertex-colour channels);
- a licence-plate area (blank or fictional);
- a dirt/wear mask;
- LOD0–3, material consolidation into the shared fleet materials, and simple colliders.

### V7 — Traffic fleet kit (later, for variety)

Build the vehicles on **one shared fleet atlas and material set**:
- `Traffic_Sedan_A`, `Traffic_Sedan_B`, `Traffic_Hatchback_A`;
- `Traffic_SUV_A`, `Traffic_SUV_B`, `Traffic_Pickup_A`;
- `Traffic_Van_A`, `Traffic_BoxTruck_A`, `Traffic_Bus_A`.

Each one has LOD0 (close traffic), LOD1 (normal gameplay), LOD2 (distant) and LOD3 (very distant / mobile). Each must be far cheaper than a player car.

Gate: the fleet render with 30+ instances, and a material / draw-call summary table.

## 8. What I will give you, and what to ask me for

**Attached now:**
- `01_hypercar_reference_reports.md`: Hypercar Unity import contract, material mapping, merge reviews, LOD / collider / pivot validation, export settings and FBX re-import validation.
- `02_hypercar_reference_scripts.md`: Hypercar Phase 7 LOD build, Phase 8 colliders + hierarchy + pivots, Phase 9 FBX export with axis bake, and the FBX re-import validator.
- `03_racing_car_earlier_pipeline.md`: the earlier racing car's LOD category breakdown and material/UV export notes.
- `hypercar_ref_front34.png`, `hypercar_ref_rear34.png`, `hypercar_ref_side.png`: the visual quality bar (LOD0, Eevee).

**I will provide per existing car, when we start its phase:**
- an FBX exported from Unity, with its texture folder;
- screenshots: front ¾, rear ¾, side, and the in-game chase view;
- the current triangle and material counts, if Unity shows them;
- a description of what looks wrong. For Zero Gap R, the front end.

**Ask me** whenever proportions, target dimensions (length, width, height, wheelbase), the starting paint colour, the budget class or a design direction is unclear. Don't guess at identity.

## 9. Lessons learned from earlier phases (avoid these)

- **Python and Blender API pitfalls:**
  - Python `hash()` is salted per run, so seeds drift. Use `zlib.crc32`.
  - `bpy.data.libraries.load(link=True)`: assign a **copy** of your name list (`dst.materials = list(names)`). Blender replaces the list items with ID objects in place.
  - After `bpy.ops.file.make_paths_relative()`, paths look like `//../textures/...`. Normalise them (`os.path.normpath(bpy.path.abspath(p))`) before any string check.
- **FBX export:**
  - The exporter triangulates n-gons at export, so remove duplicate or coincident triangles **before** exporting.
  - Strip QA materials from colliders.
  - Unity mirrors X on import. Drive the visual wheels from `WheelCollider.GetWorldPose` rather than accumulated local Euler angles (note this in the import notes).
- **LODs:**
  - Coarse LODs of rounded or faceted parts shrink. Fit each coarse LOD to the LOD0 bounds.
  - Keep silhouette-defining parts (mirrors, wing, spoiler supports, exhaust tips) in every LOD.
  - Check every LOD in a lineup render.
- **Rendering and visual review:**
  - Eevee area lights face local −Z. Too many shadowed lights overflow the shadow pool, so use a cutoff distance. Enclosed spaces need a flat world.
  - Repeating features in tiled textures (a bright spot, a logo) show up as an obvious grid on large surfaces. Remove them.
  - Visual review is where most real problems were caught: floating parts, sheets seen from below, flat ramps at tapered ends, cobblestone-looking procedural textures, cameras inside geometry. Always render and inspect before calling a checkpoint done.
- **Safe file handling:** never use `rm -rf $VAR/*`. Use a new scratch folder per iteration instead.

## 10. Your first reply

1. Confirm in ≤ 15 lines what you understood: the conventions, the frozen items and the phase order.
2. List the inputs you still need from me for **V0 Intake of Zero Gap R** (at most 8 bullets).
3. Write `veh_intake.py`. It should:
   - take the car ID, display name and FBX path as arguments;
   - import the FBX into a new scene;
   - **not** fix anything;
   - measure everything in §7 V0;
   - write `vehicles/V1_ZeroGapR/reports/zerogapr_intake.md` and a JSON;
   - render front ¾ / rear ¾ / side / top / front / rear previews;
   - save `zerogapr_01_intake.blend` (scratch-aware, no overwrite);
   - also record the SHA-1 integrity baseline of every workspace file outside `vehicles/V1_ZeroGapR/`.

Do not write the rest of the pipeline yet.

---

## Appendix A — my original brief (verbatim)

> **2. Vehicle / traffic remasters.** This is completely different. Here Blender works on the actual cars.
>
> For your player cars, the likely remaining Blender work is: Zero Gap R, Titan GT, Vortex R, Raven XR, Pulse EV. Your flagship Hypercar is already complete, so I would not touch it.
>
> **Zero Gap R.** This should mainly be an optimization/remaster, not a full rebuild. Blender work: clean topology; fix front-end visual problems; reduce excessive material count; create LOD0 / LOD1 / LOD2 / LOD3; improve wheels and tires; improve glass; improve light geometry; organize interior; optimize hidden geometry; improve normals; proper pivots; wheel origins; collider meshes; center-of-mass reference; Unity hierarchy; clean FBX export. So Zero Gap R becomes a production-ready starter vehicle.
>
> **Titan GT.** I would treat this as a medium remaster. Blender would improve body surfacing, front/rear styling, wheels, lights, glass, interior, materials, LODs and colliders while keeping its original identity.
>
> **Vortex R.** This should probably be a full rebuild. You would create a new original modern supercar with full exterior, wheels/brakes, glass, lighting, simplified interior, materials, UVs, LODs, colliders and Unity-ready hierarchy.
>
> **Raven XR.** Also likely a full rebuild, but with a Japanese-style 2-door performance coupe identity.
>
> **Pulse EV.** Full or heavy rebuild as an electric performance sedan: cleaner aero surfaces, EV-specific details, modern lighting, wheels, interior, LODs and colliders.
>
> **Traffic vehicles.** Traffic cars don't need Hypercar-level detail. We should first make the existing traffic vehicles look convincing from chase-camera distance. Blender work would include: better paint; realistic glass; basic fake/interior geometry; seats/dashboard silhouette; wheel/tire improvements; brake discs where visible; headlights; brake lights; tail lights; indicators; license-plate area; dirt/wear variation; LODs; material consolidation; simple colliders. Then later, if you want more variety, create a reusable traffic fleet. For example: Traffic_Sedan_A, Traffic_Sedan_B, Traffic_Hatchback_A, Traffic_SUV_A, Traffic_SUV_B, Traffic_Pickup_A, Traffic_Van_A, Traffic_BoxTruck_A, Traffic_Bus_A. Each traffic vehicle should be much cheaper than the hero car. For example, conceptually: LOD0 close traffic; LOD1 normal gameplay; LOD2 distant traffic; LOD3 very distant / mobile. The main requirement is that dozens of traffic vehicles can appear without destroying performance.
