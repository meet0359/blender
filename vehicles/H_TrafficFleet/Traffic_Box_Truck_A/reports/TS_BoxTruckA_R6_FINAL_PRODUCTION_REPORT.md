# Traffic Box Truck A — final realism pass: production report (r6, 2026-10-10)

**Status:**
- Production r6 is complete.
- All validation checks pass except check 1. That is the protected-files check, which fails because you archived `environment/` (see §4).
- **The truck is not frozen.** It awaits your final visual review.
- Nothing was exported to FBX or packaged for Unity. Frozen assets are untouched: `va_frozen_check.py` passes all 9 releases.

**Images to review**, all in one folder:

`/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/Traffic_Box_Truck_A/handoff_chatgpt/images_latest/` (33 JPGs)

---

## 1. Changes implemented

| Area | Change |
|---|---|
| **r4: shading fix** | Removed the `FLAT_PLANAR` setting. S1 now passes (worst mesh 0.095 %), and the rear doors stay crack-free. r4 is kept as a rollback. |
| **Wheels** | Truck steel disc wheel: <ul><li>flat mounting face with **8 wheel nuts on a 275 mm bolt circle** (ISO 8×275, 19.5");</li><li>chrome front hub cap and dark rear axle hub;</li><li>8 hand holes between the mounting face and the rim;</li><li>**brake drums** and backing plates replace the car disc and caliper;</li><li>rear outer dual **deep-dished** (17 cm) to a back-to-back mounting face with the inner dual;</li><li>30 mm dual gap, wheel pivots and collider references unchanged.</li></ul> |
| **Marker lighting** | <ul><li>Amber front clearance lamps on the box front upper corners.</li><li>Red rear clearance lamps and **3 red identification lamps** on the rear header.</li><li>Amber front and red rear side markers, plus amber and red side reflectors.</li><li>All on the existing light channels: `Marker` for amber, `Tail` for red.</li></ul> |
| **Tail lamps** | They now glow across most of the lens. The thin car-style LED strip alone read as two red lines at night. |
| **Cargo box** | <ul><li>Aluminium-look corner caps.</li><li>Top rails on the sides and front, and bottom side rails.</li><li>A subframe on the chassis rails, with 7 crossmembers visible under the box.</li><li>All long parts use pattern-free materials, so there are no artificial "dents".</li></ul> |
| **Paint** | Solid commercial fleet finish (non-metallic, softer clear coat) instead of a car metallic finish |
| **Cab front** | The centre "pinch" in the cab front skin is fixed at the root: the end cap is now closed with an n-gon. Inverted body faces went from 24 to **0**. The grille and proportions are unchanged. |
| **Silhouette (r6)** | Trim parts that set the vehicle's outer limits, such as the mirror glass, are now kept at every LOD. LOD bounds match LOD0 exactly. |
| **Review renders** | <ul><li>New `night` render mode: moonlit sky, two street lights, running lights on.</li><li>Opt-in close-up views for the marker lamps.</li><li>Night views are now part of every production run.</li></ul> |

**Unchanged:**
- the original fictional design, cab-over proportions and dimensions;
- the 4-LOD layout;
- the 25k LOD0 ceiling;
- no branding.

---

## 2. Before / after

All are in the images folder.

| Sheet | Shows |
|---|---|
| `sheet_before_r4_vs_after.jpg` | r4 (left) vs r6 (right): front ¾, rear ¾, wheel, game camera |
| `sheet_defect_history.jpg` | First production build vs r6: <ul><li>roof antenna fin and car wheels;</li><li>dented-looking rear trim;</li><li>rear-door "cracks" in the follow camera.</li></ul> |
| `sheet_marker_lamps_wheels_closeups.jpg` | Rear header lamps, front clearance lamp, side markers and reflectors, deep-dish rear dual (lamps lit) |
| `sheet_night.jpg` | Night front ¾, rear ¾, follow camera close and normal |

---

## 3. Budgets

| | r4 (before) | **r6 (final)** | Limit |
|---|---|---|---|
| LOD0 tris | 19,604 | **20,069** | 15,000–25,000 |
| LOD1 | 10,606 (54 %) | **10,768 (54 %)** | 40–60 % |
| LOD2 | 4,690 (24 %) | **4,785 (24 %)** | 15–30 % |
| LOD3 | 2,249 (11 %) | **2,587 (13 %)** | 5–15 % |
| Materials per LOD | 8 / 8 / 8 / 6 | **8 / 8 / 8 / 6** | ≤ 8 |
| Draw calls per LOD | 20 / 20 / 20 / 14 | **20 / 20 / 20 / 14** | — |
| Inverted body faces | 24 | **0** | — |

**Headroom:** about 4,900 LOD0 tris remain under the ceiling. Materials and draw calls are unchanged; every addition reuses the shared atlas and light mask.

**Measured LOD0 bounds:**
- length 7.07 m, including the front bumper bar and rear lamps;
- width 2.54 m across the mirrors (box 2.34 m, cab 2.00 m);
- height 3.25 m.

---

## 4. Validation results (r6)

Full report: `reports/trafficboxtrucka_validation.txt`

| # | Check | Result |
|---|---|---|
| 1 | Protected files byte-identical | **FAIL, owner-acknowledged** (details below the table). Nothing in the truck is wrong. |
| 2 | Hierarchy: `Car_Root`, LOD0–3 roots, Collision, 4 `WheelColliderRef`s, CenterOfMass | PASS |
| 3 | Every LOD complete (13 / 13 / 13 / 9 parts) | PASS |
| 4 | Orientation: nose −Y, left +X, LHD | PASS |
| 5 | Wheel pivots: ±30° roll < 2 mm; front steering pivot steers wheel and brake plate | PASS |
| 6 | Ground contact; body clearance 0.18 m | PASS |
| 7 | Triangle budget | PASS |
| 8 | Material slots / draw calls | PASS |
| 9 | LOD silhouette: max dimension delta **0.0 mm** | PASS. IoU: LOD1 0.999 / 0.999; LOD2 0.995 / 1.000; LOD3 0.985 / 0.953 (side / front). |
| 10 | Materials from the shared library only | PASS |
| 11 | Independent light channels | PASS. Tail faces went from 8 to 56 with the new lamps. |
| 12 | 12 external textures present | PASS |
| 13 | One UV channel; atlas and light-mask cells respected | PASS |
| 14 | Topology: no zero-area, loose or duplicate faces | PASS |
| 15 | 4 convex colliders; CenterOfMass z 1.10 | PASS |
| 16 | Studio, daylight and game renders present | PASS |
| S1 | Shading screen, all LODs: worst Interior_LOD0 0.096 % (limit 1 %); all body LODs 0.0 % | **PASS** |
| — | FBX re-import | SKIP (Blender-only rule) |

**About check 1:**
- **What fails:** the frozen environment phases P0–P3 (1,186 files) are no longer in the workspace.
- **Where they are:** you archived them to `/Volumes/Denish/Assets/environment.zip`.
- **Integrity of the archive:** I verified it against the original baseline. All 1,186 files match by SHA-1.
- **How it was handled:** the check was **not** weakened, and no manifest was edited. It will pass again once `environment/` is restored.
- **Frozen vehicle releases:** separately, all 9 pass `va_frozen_check.py` (0 changed or missing).

---

## 5. Remaining warnings

1. **Stand-in road.** Daylight, game and night renders use a plain stand-in road, because the real P0 road is archived. Restoring `environment/` restores the real road automatically.
2. **Mirror heads stay body colour.** Many real cab-overs have black mirror heads. The heads are part of the baked paint body, so changing them needs a builder change. Not done.
3. **Cab interior** reuses the car interior: seats, dash, steering wheel. A true cab-over interior (flat floor, engine tunnel, flat steering wheel) was not built. It is barely visible through the glass.
4. **Hand holes** are formed between 8 wide radial "spokes", not stamped oval holes. The inner dual shows only as a dark disc through them.
5. **No exhaust outlet.** The licence plate is a placeholder and the badge is generic. No decals or branding were added, as instructed.
6. **Two review images have small issues:**
   - the LOD-comparison sheet layout leaves 2 empty columns for this vehicle class (cosmetic);
   - the zebra cameras are framed for cars, so they show partial views of the truck.

---

## 6. Realism improvements, in short

The truck now reads as a commercial vehicle rather than a car-derived model:
- steel wheels with visible nut circles and a deep-dished rear dual;
- the legally expected lamp set for a 2.34 m wide box (clearance, identification, side markers, reflectors);
- an aluminium-framed box on a visible subframe;
- solid fleet paint;
- tail lamps that read at night.

---

## 7. Gameplay-camera quality

- **Close follow camera:**
  - rear doors are clean, with no cracks;
  - locking bars, hinges, plate and tail lamps are crisp;
  - **at night the tail lamps glow fully.**
- **Normal follow distance (22 m):** at night the 3 identification lamps and 2 clearance lamps are clearly visible, which is the classic "truck ahead" read.
- **Far (60 m):** the silhouette is stable; the LOD3 bounds equal LOD0.
- **Daylight:** the new rails, crossmembers and side markers add detail with no shading artifacts.

---

## 8. Freeze readiness

**Technically ready.** Every check passes except the owner-acknowledged check 1. The freeze waits only for your visual approval.

Before freezing, I recommend staging the truck's old build folders for deletion. A freeze hashes everything in the vehicle folder:
- `_superseded_prod1`, `_superseded_prod2`, `_superseded_prod4`, `_superseded_prod5`, `_superseded_r5` and `_failed_prod3` total **about 520 MB**;
- keep or remove `_rollback_r4` (112 MB) as you prefer.

---

## 9. Files modified (this pass)

| File | Change |
|---|---|
| `scripts/designs/box_truck_a.py` | r4: `FLAT_PLANAR` removed. r5/r6: added `TRUCK_WHEEL`, `SPOKES`, `PAINT_FINISH`, `PLAIN_BOXES`, `MARKER_LAMPS`, `TAIL_FILL`, and n-gon end caps on the cab. |
| `scripts/ts_vehicle_v2.py` | New opt-in features: <ul><li>truck wheel mode;</li><li>plain boxes and marker lamps;</li><li>tail fill;</li><li>paint finish pass-through.</li></ul>For the boxy-vehicle classes only (box truck, bus): <ul><li>far-LOD torn-normal repair (`untear`);</li><li>LOD keep-rule for silhouette-defining trim.</li></ul> |
| `scripts/ts_lib.py` | `paint_material(..., finish=None)`, an optional override; the default is unchanged |
| `scripts/ts_render.py` | `night` mode; `TS_EXTRA_VIEWS` close-ups (opt-in) |
| `scripts/production.sh` | Adds the night render pass |

**Effect on other vehicles:**
- Sedans, SUVs and the hatchback do not use these features, and frozen vehicles build from their own script snapshots.
- Bus A shares the boxy-vehicle LOD rules and was validated with the far-LOD normal repair.

**Rollback points inside `Traffic_Box_Truck_A/`:**
- `_rollback_r4/` (validated r4);
- `scripts/production/` (exact r6 script snapshot);
- the earlier `_superseded_*` runs.

---

## 10. Next recommended action

1. **Review** these sheets in `images_latest/`, and approve or list corrections:
   - `sheet_before_r4_vs_after.jpg`;
   - `sheet_marker_lamps_wheels_closeups.jpg`;
   - `sheet_night.jpg`;
   - `sheet_game_camera.jpg`.
2. **On approval:**
   - stage the old build folders for deletion (about 520 MB);
   - freeze Box Truck A (Blender-only) with a hash manifest, as was done for Hatchback A.
3. **Optional realism follow-ups**, if you want them:
   - black mirror heads;
   - an exhaust outlet;
   - a fleet graphic decal on the box sides, the biggest realism gain per triangle.
