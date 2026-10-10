# Overnight Traffic Fleet Sprint — Progress Report

Sprint window: 2026-10-09 00:32 → ~03:45 IST. Blender 5.2.2, macOS. No Unity, FBX or UnityTransfer output was produced during the sprint.

**Nothing in this report has received visual approval.** Every new vehicle below is a **COMPLETE BLOCKOUT — STATUS: AWAITING VISUAL APPROVAL**. None is frozen. None is final production.

## 1. Status summary

| Vehicle | Status | Folder |
|---|---|---|
| Traffic Sedan A r3 | **FROZEN** (approved earlier; untouched tonight, SHA verified) | `Traffic_Sedan_A_r3/` |
| Traffic Sedan B | **FINAL PRODUCTION COMPLETE (Blender)** — awaiting final visual approval, **NOT frozen**, no UnityTransfer | `Traffic_Sedan_B/` |
| Traffic Hatchback A | **COMPLETE BLOCKOUT** — AWAITING VISUAL APPROVAL | `Traffic_Hatchback_A/` |
| Traffic SUV A | **COMPLETE BLOCKOUT** — AWAITING VISUAL APPROVAL | `Traffic_SUV_A/` |
| Traffic SUV B (3-row) | **COMPLETE BLOCKOUT** — AWAITING VISUAL APPROVAL | `Traffic_SUV_B/` |
| Traffic Pickup A (bonus) | **TRIAL ONLY — NOT promoted to an official blockout** (see §5) | scratch only |

Sedan B ongoing operations were finished before the sprint work. No renders were run in parallel; one Blender process at a time.

## 2. Measured dimensions (from `reports/blockout_check.json`, measured on the built geometry)

| | Hatchback A | SUV A | SUV B |
|---|---|---|---|
| Brief target L × W × H (m) | 4.0–4.3 | 4.35–4.55 × 1.80–1.86 × 1.60–1.70 | 4.85–5.10 × 1.93–2.00 × 1.72–1.80 |
| Length | 4.255 | 4.464 | 4.953 |
| Body width (side slice z 0.45–0.85) | 1.795 | 1.842 | 1.965 |
| Width incl. mirrors | 2.080 | 2.190 | 2.300 |
| Roof height | 1.472 | 1.678 | 1.785 |
| Wheelbase | 2.630 | 2.680 | 2.980 |
| Track F / R | 1.54 / 1.53 | 1.60 / 1.61 | 1.68 / 1.69 |
| Tire radius | 0.317 | 0.370 | 0.391 |
| Overhang F / R | 0.877 / 0.748 | 0.909 / 0.875 | 0.925 / 1.047 |
| Ground clearance (body min z) | 0.145 | 0.201 | 0.220 |
| Triangles, total incl. subdivided master body | 134,293 | 137,423 | 150,025 |
| Triangles, excluding master body | 10,621 | 11,504 | 12,651 |
| Blockout check | PASS | PASS | PASS |

All dimensions are within the brief ranges. Class references (published dimensions only, no design copied): Golf Mk8 / i30 (hatchback); Tiguan / Tucson (SUV A); XC90 / X5 / GV80 (SUV B).

Blockout geometry notes:
- The master body is the unreduced subdivided loft (~120k+ tris). LODs, bakes, UVs and atlas packing are production-phase work and have not been done.
- Blockouts carry 15–16 atlas-cell materials. The ≤ 8 material target applies at production, after atlas merge, as it did on Sedan B.
- 2–4 zero-area faces exist on each master body (degenerate pole faces). They are harmless at blockout stage and are removed by the production `dissolve_degenerate` pass.

## 3. Files

Each vehicle folder follows `Traffic_<Name>/{blend,previews,reports,scripts}`:
- `blend/<ckp>_01_blockout.blend` — checkpoint
- `previews/<design>_{front34,rear34,front,rear,side,game_close}.png` + `<design>_clay_front34.png` — 7 previews, 1280×720, Cycles 24 spp + denoise
- `reports/blockout_check.json`, `reports/build.log`, `reports/<PRE>_blockout_stats.json`
- `scripts/ts_vehicle.py` + `scripts/<design>.py` — exact snapshot used for the build

SUV A and SUV B were rebuilt once tonight for the roof-rail fix (§4). The previous builds were **moved, not deleted**, to `blend/_superseded_0245/` (SUV A) and `blend/_superseded_0301/` (SUV B), together with their previews.

**Consolidated comparison sheet:** `H_TrafficFleet/previews/FLEET_COMPARISON_SedanA_SedanB_HatchbackA_SUVA_SUVB.jpg`
- Rows top→bottom: Sedan A r3 · Sedan B · Hatchback A · SUV A · SUV B.
- Columns: front¾ · side · rear¾ · **orthographic side at one shared scale** (5.75 m frame, same camera), so relative size is true in that column only.
- The perspective columns are framed per vehicle.
- Source frames: `H_TrafficFleet/previews/fleet_compare/`. Sedan A r3 was rendered read-only from its 09 file; its SHA was checked before and after (OK).

## 4. Open defects, recorded for review (not fixed unless stated)

**Hatchback A**
- Tail lamps read small; the rear still leans sedan-like at rear¾. It needs a bolder lamp graphic and a more vertical hatch face.

**SUV A / SUV B**
- The front composition family-resembles Sedan B (lamp and grille placement). SUV identity needs its own front graphic.
- The hood leading edge reads low and long in the side view, more estate-car than SUV. Raising it is recommended at the design-approval stage.
- Roof rails: dashed "paint poking through" artifacts were **fixed tonight**. Root cause: the quadratic rail top line dipped below the roof surface. Fix: a minimum 28 mm clearance in `ts_vehicle.py`. The rails still show a mottled shading on the thin brushed-alu strips. This is cosmetic and is to be replaced by a proper rail profile in production.
- The softbox reflection reads as a bright white patch in the windshield in the front¾ views. This is a studio-light artifact, not geometry.
- SUV B: a black sliver at the D-pillar / rear-glass junction.
- Both SUVs: black vertical pillar bars are visible through the side glass in rear¾ views.

**All three**
- These are blockouts on the master body: no LODs, bakes, UVs, colliders validation, FBX or Unity work. Production detailing has not been done, as instructed for unapproved designs.

## 5. Pickup A (bonus) — not promoted

There was time and disk available, so two trials were built and previewed in scratch only:
- v1: `scratchpad/pickup_a.v1`, previews in `pv_pickup_a.v1`
- v2: `scratchpad/pickup_a.v2`, previews in `pv_pickup_a.v2`

v2 fixed the hood-above-belt and lamp heights. Both still read as a **coupe-utility (car-based ute)**, not a mid-size pickup:
- the cab roof is domed;
- the windshield is car-raked;
- the cab back flows into the bed sides as a sail.

This is a builder limitation, not a curve-tuning problem. The single-loft builder cannot make a crisp, separate cab box over a bed. It needs a new **separate cab volume** feature in `ts_vehicle.py`.

I did not promote this to `Traffic_Pickup_A/` because presenting it as a pickup blockout would be misleading. The design file `scripts/designs/pickup_a.py` holds v2; the v1 copy is at `scratchpad/pickup_a_v1_design.py`.

## 6. Shared pipeline components (created or improved)

| Component | What it does |
|---|---|
| `scripts/ts_vehicle.py` | Generic design-driven builder; one design file per vehicle in `scripts/designs/`. Regression-checked against Sedan B. Generic components: headlamp (housing, cells, segmented DRL, indicator), tail lamp, grille vanes (vertical or horizontal, frame material), intake blades, plates, trims, rocker/cladding, roof rails, mirrors, seat rows, BED cavity, CAB_GAP grooves. |
| `scripts/designs/` | `sedan_b` (regression reference), `hatchback_a`, `suv_a`, `suv_b`, `pickup_a` (trial) |
| `scripts/ts_blockout_check.py` | Basic blockout validation: dimensions, wheels on ground, clearance, mesh sanity, part presence → JSON |
| `scripts/ts_fleet_sheet.py` | **New tonight.** Consolidated fleet comparison sheet |
| `scripts/ts_render.py` | Options `TS_LOOK`, `TS_ONLY`, `TS_CAM_SCALE`, `TS_SHIFT_*`, `TS_ORTHO_SCALE`, extra views |
| `scripts/ts_package.py`, `ts_validate.py` | Nested-fleet freeze glob, material instances, `TS_NO_UNITY` |
| Scratch helpers | `official_blockout.sh` (build → check → 7 previews; moves any previous blockout aside, never deletes), `preview.sh`, `diskguard.sh` (refuses below 5 GB) |

## 7. Validation and integrity (run at end of sprint)

- `va_frozen_check.py`: **FROZEN CHECK PASS**. B_ZeroGapR 70, C_TitanGT 81, C_TitanGT_r1 89, D_VortexR 109, D_VortexR_r1 91, E_RavenXR 147, Traffic_Sedan_A_r3 246 files (includes `shared/textures`) — 0 changed or missing.
- `va_integrity.py` (frozen P0–P3, Hypercar and all files outside `vehicles/`): **INTEGRITY PASS** — 0 changed, 0 added, 0 removed.
- Pulse EV `pulseev_01_blockout.blend` SHA `18af7277976a…`: unchanged.
- Sedan A r3 09 file SHA: unchanged before and after the comparison render.
- No `.fbx`, `.meta`, Unity or UnityTransfer files created since 00:32.
- Nothing deleted. Superseded builds moved aside only. Shared material libraries not overwritten.

## 8. Storage

- Free space: about **11 GB** at end of sprint, down from about 12 GB. Disk guard never tripped.
- Sprint additions: Hatchback A 9 MB, SUV A 19 MB, SUV B 19 MB, fleet previews 22 MB. Scratch is now 1.3 GB.
- Scratch cleanup is pending your permission; see `STORAGE_SCRATCH_INVENTORY.md`.

## 9. Recommended next order

1. **Review and approve or reject** Sedan B (final visual approval → freeze + UnityTransfer) and the three blockouts.
2. Fix the blockout design notes you agree with. Priorities: SUV front identity and higher hood; hatchback tail lamps.
3. Production for approved blockouts in this order: **SUV A → Hatchback A → SUV B**. SUV A is the most common traffic class and reuses the most Sedan B production steps.
4. Pickup A: add the separate-cab builder feature first, then a fresh blockout.
5. Remaining archetypes after that (van, bus/truck, etc., per inventory).
