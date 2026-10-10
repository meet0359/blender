> **CURRENT STATUS: 2026-10-10 09:15. ALL SEVEN PRIORITY TRAFFIC VEHICLES FROZEN (Blender-only).** This supersedes everything below, which is kept for history. Release record: `reports/FLEET_FINAL_RELEASE_20261010.md`.
>
> | Vehicle | Released version | Status | LOD0 |
> |---|---|---|---|
> | Sedan A | r3 | FROZEN | 14,961 |
> | Sedan B | production | FROZEN | 17,987 |
> | Hatchback A | **r2** (`Traffic_Hatchback_A_r2/`) | FROZEN 2026-10-10. The original `Traffic_Hatchback_A/` stays frozen as history. | 17,174 |
> | SUV A | v2 | FROZEN 2026-10-10 | 17,998 |
> | SUV B | v3 | FROZEN 2026-10-10 | 19,840 |
> | Box Truck A | r7 | FROZEN 2026-10-10 | 20,063 |
> | Bus A | **v4** | FROZEN 2026-10-10. v3 is rollback only. | 34,506 |
>
> Hash check: PASS, 14 releases. Check 1 (protected files) FAILs only because `environment/` is archived externally. Archive last verified 2026-10-09 (1,186/1,186); not re-verifiable on 2026-10-10 because the drive was not connected. Night rig v2 is the standard preview lighting. Unity export DONE 2026-10-10 09:45: package `UNITY_HANDOFF_20261010/`, report `reports/UNITY_FLEET_HANDOFF_REPORT.md`. Next: P0-05 Unity runtime verification on the Unity machine.

# Traffic Fleet — 7 Priority Vehicles: Production Status (2026-10-09)

All work is Blender-only. **No FBX, UnityTransfer or Unity files were generated.** Nothing is frozen except Sedan A r3 and Sedan B. Hatchback A, SUV A and SUV B **await your review of the final production images** before any freeze.

**Comparison sheet:** `previews/FLEET_FINAL_7_SedanA_SedanB_HatchbackA_SUVA_SUVB_BoxTruckA_BusA.jpg`
- Rows: Sedan A r3 · Sedan B · Hatchback A · SUV A · SUV B · Box Truck A · Bus A.
- Columns: front¾ · side · rear¾ · orthographic side at **one shared scale** (12.5 m frame, same camera and studio), so relative size is true in that column.
- The perspective columns use each vehicle's own framing; the truck and bus use a pulled-back camera and a scaled studio.
- Source frames: `previews/fleet_final/`.

## 1. Status

| Vehicle | Status | Evidence |
|---|---|---|
| Sedan A r3 | **FROZEN** (earlier approval) | `Traffic_Sedan_A_r3/reports/TS_SedanA_r3_FINAL_FREEZE.md` |
| Sedan B | **FROZEN (Blender-only), 2026-10-09** — 259 files hashed | `Traffic_Sedan_B/reports/TS_SedanB_FINAL_FREEZE.md`, `TS_SedanB_STATUS.md`, `previews/TrafficSedanB_sheet_FINAL_REVIEW.jpg` |
| Hatchback A | **FINAL PRODUCTION COMPLETE — AWAITING FINAL APPROVAL** (not frozen) | `Traffic_Hatchback_A/` |
| SUV A | **FINAL PRODUCTION COMPLETE — AWAITING FINAL APPROVAL** (not frozen) | `Traffic_SUV_A/` |
| SUV B | **FINAL PRODUCTION COMPLETE — AWAITING FINAL APPROVAL** (not frozen; class budget needs sign-off, §3) | `Traffic_SUV_B/` |
| Box Truck A | **DESIGN BLOCKOUT — AWAITING VISUAL APPROVAL** | `Traffic_Box_Truck_A/` |
| Bus A | **DESIGN BLOCKOUT — AWAITING VISUAL APPROVAL** | `Traffic_Bus_A/` |
| Pickup A, Van A, Pulse EV | **POSTPONED** — untouched (Pickup A v2 blockout preserved) | — |

## 2. Final production — Hatchback A, SUV A, SUV B

Each vehicle folder contains:
- `blend/<ckp>_02_body` … `_08_rig` and `_09_export_ready.blend`, saved and re-opened by validation;
- `textures/` holding the baked body normal map (LOD0 and LOD1) and the AO / grime map, plus the shared atlas, tire and light library;
- `previews/`:
  - studio views: front¾, rear¾, front, rear, side, top, wheel, interior, front and rear details, lamp and bumper close-ups;
  - daylight ×3 and chase camera ×3;
  - `qa/` clay and wire views;
  - `lod/` LOD0–3 views;
  - `zebra_master/` and `zebra_game/`;
  - 19 review sheets;
- `reports/<ckp>_validation.txt`, `_geometry.json`, integrity check and `production_logs/`.

| | Hatchback A | SUV A | SUV B |
|---|---|---|---|
| Validation | **0 errors, 0 warnings** | **0 errors, 0 warnings** | **0 errors, 0 warnings** |
| LOD0 / LOD1 / LOD2 / LOD3 (tris) | 17,126 / 8,367 / 3,880 / 1,647 | 17,931 / 8,743 / 4,022 / 1,725 | 19,746 / 9,526 / 4,310 / 1,868 |
| Budget applied | 12,000–18,000 | 12,000–18,000 | **13,000–20,000 (class budget, needs your sign-off)** |
| Materials per LOD / draw calls | 8 · 8 · 8 · 6 / 19 · 19 · 19 · 13 | same | same |
| LOD silhouette IoU | ≥ 0.95 | ≥ 0.95 | ≥ 0.95 |
| Shading screen S1 (all LODs) | PASS (worst 0.8 %) | PASS (worst 0.13 %) | PASS (worst 0.19 %) |
| FBX re-import | SKIPPED (Blender-only) | SKIPPED | SKIPPED |

Validation also covers:
- hierarchy;
- wheel pivots and WheelColliderRefs;
- CenterOfMass;
- 4 convex colliders;
- one clean UV channel;
- topology (no zero-area or loose geometry);
- independent light channels;
- external textures;
- the protected-file integrity check.

The S1 limit is 1 % torn loop normals per mesh.

**Design work done in production:**
- **Hatchback A:** rear bumper 3 cm proud with a defined ledge and diffuser split trim; large split tail lamps; a convex hood crown (the front was slightly concave).
- **SUV A:** the plain front band is now sculpted with a 2 cm bumper shoulder step, a dark-chrome grille-band underline and a satin shoulder trim. The plate moved onto the lower grille. Hood crown added.
- **SUV B:** the wavy hood was fixed at the root. The hood centre had sat *below* the fender line (concave); it now follows the fender line plus a uniform 2.0–2.4 cm convex crown, with no ridge. Zebra confirmed before production.

**Production defects found and fixed (none remain in the files):**
- **Hatchback:** the first production failed S1 (10.6 % torn glass). An extra hatch station lay behind the end blend ring and folded the skin. Fixed, and the builder now refuses any folded loft. The failed run is moved to `_superseded_prod1/`.
- **SUV A:** the approved blockout had the same small fold at the rear corners, caught by the new guard and fixed. The first production was 219 tris over budget; the rails were lightened.
- **Glass wrapping a corner:** now gets split normals.
- **Exact-boolean failures:** they could add a cutter or destroy the skin. Every cut is now verified, with a fallback cascade; nothing was skipped.

**Open visual notes for your review:**
- SUV A: faint diagonal hairlines on the bumper face near x ±0.55; softly wavy hood highlights from the hood-ridge sculpt.
- SUV B: a small crack-like mark below the right corner of the rear plate (baked shut-line artifact).
- All three: plain procedural surfaces in close hero shots (not photoreal / not AAA); single-colour review paint.

## 3. Decision needed: SUV B triangle budget

SUV B LOD0 is 19,746 tris: three seat rows, wide multi-cell lamps, and 21" 12-spoke wheels. I validated it against a **13,000–20,000 full-size-SUV class budget** instead of 12,000–18,000. Reaching 18,000 would mean removing the third-row interior detail or reducing the wheels and lamps. Please confirm the 20k class budget, or ask for a reduction.

## 4. New blockouts — Box Truck A, Bus A (class-specific construction, no sedan body)

| | Box Truck A | Bus A |
|---|---|---|
| Class | medium-duty cab-over box truck (16 ft box class) | 12 m low-floor city bus |
| Measured L × W × H (m) | 6.893 × 1.976 cab (2.34 box) × 3.281 | 11.977 × 2.557 × 2.948 (3.21 incl. HVAC) |
| Wheelbase / tire R | 3.85 / 0.405 (19.5") | 6.00 / 0.478 (22.5") |
| Body min z | 0.60 (cab) / 0.95 (box floor) | 0.32 (low floor) |
| Blockout check | PASS (all incl. dimensions ±6 cm, stray parts) | PASS |
| Files | `blend/trafficboxtrucka_01_blockout.blend`, `previews/blockout/` (7 + clay + 3 zebra) | `blend/trafficbusa_01_blockout.blend`, `previews/blockout/` |

**Construction:**
- **Box Truck A** is two shells:
  - a cab-over cab with the windshield set into the flat raked face, doors above the front wheel and a flat cab-back wall;
  - a separate cargo box with crisp edges, side panel seams and rear doors with a centre split.

  Also: exposed chassis rails, rear underride bar, side guards, fuel tank, cab steps and tall mirrors.
- **Bus A** is one long box loft with near-vertical sides and a rounded drip rail. It has:
  - a tall window band with flush pillars;
  - windshield and rear window set into the end faces;
  - destination and route displays;
  - full-height glass doors (front and middle) on the curb side;
  - rear engine hatch and louvre;
  - roof HVAC pod and roof hatch;
  - 2+2 seating with a centre aisle.

**Known blockout limits:**
- single rear tires (real trucks and buses run duals — the builder has 4 wheels);
- no mud flaps;
- bus doors are glass panels with no opening or steps;
- the bus doors are on the right side (right-hand traffic); left-hand traffic would need a mirrored design;
- the zebra cameras are car-framed, so they show partial views of these vehicles.

## 5. Builder v2 changes this phase (`scripts/`)

- **`ts_vehicle_v2.py` + `ts_loft.py` + `ts_classes.py`.**
  - New classes: `box_truck` and `bus` (`van` preset only).
  - Ray and cutter extents now come from the vehicle's own size.
  - Optional hood, rear door, bumper split and fender split.
  - New hooks: `FACE_GLASS`, `SIDE_PANELS`, `ROOF_BOXES`, `FRAME`, `BOXES`, `EXTRA_GROOVES`, `FACE_TRIMS`, `WIPERS`, and bus seating (`rear_x`, `bench`).
- **Robustness:**
  - verified boolean cascade;
  - loft fold guard;
  - pillar stations scoped per shell;
  - glass split normals;
  - orphan-vertex sweep.
- **Blender-only production:**
  - `ts_export.py TS_NO_FBX=1` saves `_09` only;
  - `ts_validate.py TS_NO_FBX=1` marks FBX checks as SKIP;
  - `ts_package.py TS_NO_UNITY=1`.
- **Renders:**
  - `ts_render.py` has `TS_LIFT_*` / `TS_LIFT_ALL` for close-up framing of tall vehicles and `TS_STUDIO_SCALE` for a studio sized to trucks and buses.
  - `ts_blockout_check.py` checks dimensions against the design and flags stray parts; declared roof equipment is allowed.
  - `ts_fleet_sheet.py` builds review sheets.

## 6. Integrity and storage

- `va_frozen_check.py`: **FROZEN CHECK PASS.** ZeroGapR, TitanGT (+r1), VortexR (+r1), RavenXR, Traffic_Sedan_A_r3 (246), Traffic_Sedan_B (259).
- `va_integrity.py`: **PASS** (0 changed / added / removed outside `vehicles/`).
- Pulse EV SHA unchanged. No FBX or UnityTransfer created.
- **Disk:**
  - About 6.5 GB free.
  - At 11:10 free space fell to about 0.1 GB while Unity Hub downloaded a Unity 6000.6.5f1 install, which is not part of this work; the disk guard stopped production safely each time.
  - You have since freed space. Unity Hub is still running.
  - Further investigation was postponed at your request.
- Nothing was deleted by me. Failed or superseded attempts were moved into `_superseded_prod1`, `_failed_prod1`, `_failed_r1` and `_failed_r2` folders.

## 7. Recommended next step

1. Review the three production vehicles (sheets in each `previews/`) and either approve them for a Blender-only freeze or list corrections.
2. Confirm the SUV B budget.
3. Review the Box Truck A and Bus A blockouts.
