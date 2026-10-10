# Traffic Box Truck A — production handoff (2026-10-09)

## How to use this file

This file is the context for a Blender traffic-vehicle asset made for a mobile racing/traffic game.

- The asset is built **entirely by Python scripts in Blender 5.2**, not by hand. The owner runs the scripts and does the visual review.
- You will receive this file and the images listed in §9.
- **What you can do:** advise on design and realism, and propose changes to the design file or scripts. The owner (or Claude Code on their machine) applies them and rebuilds.
- **What you cannot do:** you cannot run Blender or open the `.blend` files.

**Production rule set by the owner:** Blender-only.
- No FBX export and no Unity transfer at this stage.
- The FBX re-import check is therefore marked SKIP.

---

## 1. The asset

| | |
|---|---|
| Name | `Traffic_Box_Truck_A`: an **original, fictional** design (no manufacturer design is copied) |
| Class | Medium-duty **cab-over box truck**, 16 ft box class |
| Class references (published dimensions only) | Isuzu NPR-HD, Hino 155, Fuso Canter |
| Length × width × height | 6.90 m × 2.00 m (cab) / 2.34 m (box) × 3.25 m |
| Wheelbase / track | 3.85 m / 1.68 m |
| Overhang (front / rear) | 1.15 m / 1.90 m |
| Tires | 225/70 R19.5 (radius 0.405 m), **dual rear wheels** with a 30 mm gap |
| Review paint | fleet white `(0.62, 0.62, 0.60)`. Paint variants exist on a sheet. |
| Axes | nose toward −Y, vehicle left = +X, +Z up. LHD (driver on +X). |

**Construction:** two separate shells, so it is not "a box with wheels".

**Shell 0 is the cab-over cab:**
- a flat raked front face carrying the windshield;
- a door above the front wheel;
- a flat roof and a flat cab-back wall.

**Shell 1 is the cargo box:**
- crisp edges;
- side panel seams;
- a floor at 0.95 m sitting on exposed chassis rails;
- an 80 mm gap between the cab-back wall and the box front wall.

**Detail that exists in the model:**
- **Front:**
  - large black grille panel with 6 dark-chrome horizontal bars, under the windshield;
  - two rectangular headlamps;
  - lower lamps;
  - front plate;
  - front bumper bar, plus a step strip;
  - badge.
- **Cab:**
  - tall truck mirrors on arms;
  - two windshield wipers;
  - door with handle;
  - amber side marker;
  - cab steps under the door.
- **Cab interior,** visible through the windshield:
  - driver and passenger seat;
  - dashboard;
  - steering wheel.
- **Cargo box rear:**
  - two swing doors with a centre split;
  - 4 vertical locking bars with handles and keepers;
  - hinges (3 per side);
  - corner posts, sill and header;
  - tail lamps;
  - high-mount brake strip;
  - rear plate.
- **Chassis:**
  - exposed chassis rails;
  - leaf springs and axle beams (front and rear);
  - fuel tank;
  - side guards;
  - rear underride bar with uprights;
  - rear mud flaps;
  - mudguard liners that span both rear tires.
- **Wheels:**
  - steel-style 8-spoke disc with small hand holes;
  - dual rear tires on one pivot.

---

## 2. Status

| Item | State |
|---|---|
| Blockout | **Approved by the owner** |
| Production run r3 | **Complete.** These are the images in this handoff. |
| Production run r4 | **Queued.** It is identical to r3 except one shading setting is reverted to fix S1 (see §5). The geometry and look are the same. |
| Freeze | Not frozen. It awaits the owner's final approval after r4 validates. |

### Validation of r3 (16 checks, the S1 shading screen, and an FBX check)

| # | Check | r3 result |
|---|---|---|
| 1 | Protected files byte-identical across the workspace | **FAIL, owner-acknowledged.** The owner archived the frozen `environment/` folder to an external drive. Nothing in the truck is wrong. |
| 2 | Hierarchy: `Car_Root` → `LOD0_Root`..`LOD3_Root`, `Collision`, `WheelColliderRef_FL/FR/RL/RR`, `CenterOfMass` | PASS |
| 3 | Every LOD has the full vehicle | PASS (13 / 13 / 13 / 9 parts) |
| 4 | Orientation | PASS |
| 5 | Wheel pivots: ±30° roll keeps the hub centre; front steer pivot | PASS |
| 6 | Ground contact; body clearance ≥ 0.12 m | PASS (body min z 0.18) |
| 7 | Triangle budget: LOD0 15k–25k; LOD1 40–60 %, LOD2 15–30 %, LOD3 5–15 % | PASS: **19,604 / 10,606 / 4,690 / 2,249** |
| 8 | Materials ≤ 8 per LOD; draw calls | PASS (8 / 8 / 8 / 6 materials; 20 / 20 / 20 / 14 draw calls) |
| 9 | LOD silhouette | PASS. IoU vs LOD0: LOD1 ≥ 0.997, LOD2 ≥ 0.988, LOD3 side 0.979 / front 0.951. Max dimension delta 4.5 mm. |
| 10 | Materials come only from the shared traffic library plus this vehicle's instances | PASS |
| 11 | Independent light channels (DRL, headlamp, tail, brake, indicators, reverse) | PASS |
| 12 | Textures: 12 external PNGs | PASS |
| 13 | UVs: one channel; atlas faces in their cells; unique body unwrap | PASS |
| 14 | Topology: no zero-area, loose or duplicate faces | PASS |
| 15 | Colliders: 4 convex hulls, each ≤ 255 tris; CenterOfMass | PASS (COM z 1.10) |
| 16 | Visual QA renders present | PASS |
| S1 | Shading screen: torn loop normals ≤ 1 % per mesh | **FAIL in r3:** body LOD1 3.0 %, LOD2 2.7 %, LOD3 2.9 %. Cause and fix in §5. The previous full run without that setting passed (worst 0.26 %). |
| — | FBX re-import | SKIP (Blender-only rule) |

### LOD0 triangle breakdown (19,604)

| Part | Tris |
|---|---|
| Body | 6,049 |
| Trim (atlas parts: grille, bumper, chassis, doors hardware, mirrors…) | 6,616 |
| Interior | 1,869 |
| Lights | 1,046 |
| Glass | 56 |
| Wheels | 750 each front, 1,130 each rear (duals) |
| Calipers | 52 each |

**Materials (8 per LOD):**
- `TS_Atlas` (shared trim atlas);
- `TS_BoxTruckA_Paint` (body paint with baked normal and AO maps);
- `TS_BoxTruckA_Glass`;
- `TS_BoxTruckA_Interior`;
- `TS_Lens`, `TS_LensRed`, `TS_Lights` (light mask);
- `TS_Tire`.

---

## 3. What was fixed in production, and why

Each fix states the cause that was found, because several were builder-level bugs.

| # | Defect seen in renders | Root cause | Fix |
|---|---|---|---|
| 1 | Dark marks on the cab front face | The loft's end cap converges ("pinches") at the face centre, around z 1.5 m | Grille panel made taller (z 1.00–1.52) so it covers that spot. Badge moved to z 1.30. Grille bars 4 → 6. |
| 2 | Crumpled white wedge on the cab roof | The shared car "shark-fin" antenna was being added to the truck | Antenna removed for this vehicle. The builder now supports "no fin". |
| 3 | Rear door frame, corner posts and side guards looked dented and wavy | Those parts used the `alu_brushed` atlas cell. Its brushed normal pattern is fitted to a part's longest side, so on 2 m long parts it is magnified into "dents". | Large and long metal parts switched to the pattern-free `wheel_silver` cell |
| 4 | Wheels read as car alloy wheels | The design's spoke width was too narrow (open car-style spokes) | Spokes widen toward the rim, which leaves 8 small hand holes and reads as a steel truck wheel |
| 5 | Two dark curved "cracks" on the rear doors at x ±0.27–0.39 m, z 2.2–2.5 m. Visible from the game follow camera. | The loft closed the box's flat rear end with a top/bottom "quad bridge". On a rectangular outline it **folds** at the inner ring's corners, which gave inverted faces and pinholes in the skin. | Flat box ends are now closed with one planar n-gon. Inverted body faces went from 95 to 24, and the cracks are gone (compare the before and after images). |
| 6 | The windshield looked opaque, and paint showed through it | The windshield glass was a patch floating 4 mm over **uncut painted body** | Real opening: a 5 cm pocket is cut behind the glass and its floor removed, so you now see into the cab, framed by a black reveal |

---

## 4. Known limitations: good topics for further work

These are honest gaps against a real medium-duty truck. Nothing below is broken.

1. **Clearance and identification lamps.** The box is 2.34 m wide, but it has no clearance lamps and no row of 3 identification lamps.
   - Real trucks wider than 2.03 m need amber clearance lamps at the front upper corners and red ones at the rear.
   - The red identification row sits centred at the top of the rear doors. The model has only a high-mount brake strip there.
   - Side marker lamps and reflectors are also missing along the box sides.
2. **Wheels are derived from the car wheel builder.**
   - They have **5 lug nuts**; real 19.5" truck wheels use 6 or 8 studs on a larger circle.
   - A car-style disc and caliper sits behind the spokes, where real trucks show a hub or drum.
   - The rear duals are correct in count and spacing, but the outer rear wheel is not deep-dished the way real dual wheels are.
3. **Cab interior** reuses the car interior builder: seats, dash and steering wheel. A real cab-over has a flat floor, an engine tunnel and a large, nearly horizontal steering wheel.
4. **Cab front face:** the centre "pinch" is hidden by the grille, not fixed at the root. The n-gon fix only applies to flat ends, and the cab face is slightly curved.
5. **Materials are procedural.** The atlas uses single colours plus a small set of normal patterns, so it is not photoreal. The plate text is a placeholder (`FEEEEE`) and the badge is a generic disc.
6. **Daylight and game-camera renders use a plain stand-in road.** The frozen P0 highway scene is archived off this machine, so these images show plain asphalt and lane lines instead of the real game road.
7. **No branding or decals** on the box sides. Real fleet trucks usually carry a large side graphic, and this would be the biggest realism gain per triangle.
8. No exhaust stack or pipe outlet is modelled. No cab roof marker lamps are modelled either; they're optional at a 2.0 m cab width.

### Budget headroom

LOD0 is 19,604 against a 25,000 ceiling. That leaves **about 5,400 tris** for items 1, 2 and 8.

---

## 5. The S1 issue in r3 (being fixed in r4)

While chasing defect #5, a setting called `FLAT_PLANAR` was tried. It gives large flat body panels flat custom normals.

- It did **not** fix the cracks; the n-gon end cap did.
- Its custom normals carried into the decimated LOD1–3 bodies and tore there, which is why S1 fails.

r4 removes that setting. Nothing else changes. The previous full run without it passed S1 (worst mesh 0.26 %).

---

## 6. Pipeline: how the truck is built

All paths are under `/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/`.

| File | Role |
|---|---|
| `scripts/designs/box_truck_a.py` | **The design file.** It holds all dimensions, outlines (cab, box, grille, lamps, doors), part lists (`BOXES`, `FACE_PARTS`, `FACE_GLASS`), materials, wheel spokes, LOD settings and interior. Most realism changes go here. |
| `scripts/ts_vehicle_v2.py` | Generic builder. Stages: 02 body (master + game body + normal bake), 03 parts, lights and glass, 04 wheels, 05 interior, 06 materials, UV and AO bake, 07 LODs, 08 rig. |
| `scripts/ts_loft.py` | Loft surface per shell (rings, end faces, end caps) |
| `scripts/ts_classes.py` | Class presets (`box_truck`, `bus`, sedan…) |
| `scripts/ts_lib.py` | Shared material library and the atlas cell list (`CELLS`) |
| `scripts/ts_export.py`, `ts_validate.py`, `ts_render.py`, `ts_zebra.py`, `ts_package.py` | Export-ready file, validator, renders, zebra QA, review sheets |
| `scripts/production.sh` | One-command production run |

### Design-file vocabulary

Proposals should be written in this vocabulary.

**Part lists:**
- `BOXES += [((x, y, z), (half_x, half_y, half_z), 'TS_Atlas:<cell>')]` adds a free-standing rounded box: chassis parts, lamps, bars.
- `FACE_PARTS` places parts on an end face. Each entry is `('R', 'box' | 'rod', ...)` for the rear face, or `'F'` for the front.
- `FACE_GLASS` defines glass in an end face, given as an outline in (x, z).
- `EXTRA_GROOVES`, `LID_SIDE`, `LID_MID` define panel shut lines.

**Atlas cells:**
- **Pattern-free cells** are safe on large parts: `gloss_black`, `chrome`, `wheel_silver`, `wheel_dark`, `lamp_housing`, `lamp_inner`, `dark_chrome`, `caliper`, `exhaust`, `screen`, `frit`.
- **Patterned cells magnify on parts longer than about 0.5 m:** `plastic_black`, `plastic_dark`, `alu_brushed`, `underbody`, `arch_liner`.
- **Lights** use `TS_Lights:<channel>`. Channels are `DRL`, `Headlamp`, `Tail`, `Brake`, `Indicator_L`, `Indicator_R`, `Reverse` and `Marker`.

**Rules learned the hard way:**
- Never give a trim part the body paint material.
- Long parts must use pattern-free cells.
- Flat loft ends use `END[...]['ngon'] = True`.

### Production command (run by the owner)

```
cd /Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/scripts
TS_COM_Z=.5,1.5 TS_LOD_PCT=.40,.60,.15,.30,.05,.15 TS_LIFT_ALL=.55 TS_CAM_SCALE=1.95 TS_STUDIO_SCALE=1.35 \
TS_SHIFT_F=-1.35 TS_SHIFT_R=1.35 TS_SHIFT_W=-.95 TS_LIFT_I=.20 \
zsh production.sh box_truck_a Traffic_Box_Truck_A TrafficBoxTruckA 15000 25000
```

It takes about 30 minutes and produces:
- blends 02–09;
- textures;
- 55 renders plus 20 zebra renders;
- the validation report;
- 19 review sheets.

---

## 7. Output files

All paths are under `/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/Traffic_Box_Truck_A/`.

| Path | Content |
|---|---|
| `blend/trafficboxtrucka_01_blockout.blend` | Approved blockout |
| `blend/trafficboxtrucka_02_body.blend` … `_08_rig.blend` | Production stages |
| `blend/trafficboxtrucka_09_export_ready.blend` | **Final file** (rig, LOD0–3, colliders, materials) |
| `textures/` | Baked body normal map (LOD0, LOD1), AO/grime, plus the shared atlas, tire and light textures |
| `reports/trafficboxtrucka_validation.txt` | Full validation report |
| `reports/TS_BoxTruckA_build_log.json` | Build statistics (triangles per part, LOD ratios, cutters) |
| `previews/` | All renders and 19 review sheets. r4 regenerates this folder. |
| `_superseded_prod*/`, `_failed_prod3/` | Earlier production attempts, kept only for comparison |

---

## 8. Suggested next steps

The owner decides; these are my recommendations.

1. Approve the r4 result (S1 PASS expected), then freeze Blender-only.
2. Highest realism gain for the triangles:
   - clearance and identification lamps;
   - side marker lamps and reflectors;
   - a fleet graphic decal on the box sides;
   - an exhaust outlet.
3. **Wheel pass:**
   - 8 studs on a larger bolt circle;
   - hub or drum instead of a car disc and caliper;
   - outer dual wheel deep-dished.
4. Optional cab-over interior (flat floor, engine tunnel, flat steering wheel). This is low priority because it is barely visible through tinted glass.

---

## 9. Images in this handoff

All images are copies, so they do not move when the production folder is regenerated. They are under:

`/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/Traffic_Box_Truck_A/handoff_chatgpt/images/`

### Review sheets (several views per image; upload these first)

| File | Shows |
|---|---|
| `sheets/studio_1.jpg`, `sheets/studio_2.jpg` | Studio views: front¾, rear¾, front, rear, side, top |
| `sheets/daylight.jpg` | Daylight front¾, rear¾ and side, on the stand-in road |
| `sheets/game_camera.jpg` | Gameplay follow camera at close, normal and far distance |
| `sheets/details.jpg` | Front detail, rear detail, wheel, interior |
| `sheets/closeups_bumpers_lamps.jpg` | Bumper and lamp close-ups |
| `sheets/closeups_wheel_glass_plate.jpg` | Wheel, glass, plate close-ups |
| `sheets/lod_comparison.jpg` | LOD0–LOD3 side by side |
| `sheets/orthographic.jpg` | Orthographic front, rear and side |
| `sheets/qa_clay.jpg`, `sheets/qa_wire.jpg` | Clay and wireframe QA (shape and topology) |
| `sheets/zebra_master_vs_game.jpg` | Zebra reflection QA, high-poly master vs game mesh |
| `sheets/lights_off_on.jpg` | Light channels on and off |
| `sheets/paint_variants_a.jpg` | Paint colour variants |

### Single views (r3)

All under `views/`:
- **Studio:** `front34.jpg`, `rear34.jpg`, `side.jpg`, `front.jpg`, `rear.jpg`, `front_detail.jpg`, `rear_detail.jpg`, `wheel.jpg`, `interior.jpg`.
- **Daylight:** `day_front34.jpg`, `day_rear34.jpg`, `day_side.jpg`.
- **Game camera:** `game_close.jpg`, `game_normal.jpg`, `game_far.jpg`.

### Before the fixes, for comparison

| File | Defect shown |
|---|---|
| `before_fixes/rear_door_cracks_game_close.jpg` | Two dark "cracks" on the rear doors (defect #5) |
| `before_fixes/roof_fin_car_wheels_front34.jpg` | Car shark-fin on the cab roof and car-alloy wheels (#2, #4) |
| `before_fixes/dented_trim_car_wheels_rear34.jpg` | Dented-looking rear frame and side guards (#3) |
