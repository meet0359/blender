# Traffic Fleet — Design Corrections Review (2026-10-09)

**Nothing here has visual approval.** The revised blockouts are design blockouts only. None is frozen, and none has final detailing: no UV baking, LOD production or detailed materials. No Unity, FBX or UnityTransfer output was produced. No Pulse EV or player-car work was done.

## 1. Status

| Vehicle | Status | Review files |
|---|---|---|
| Sedan A r3 | FROZEN (untouched; SHA re-verified) | — |
| Sedan B | **AWAITING FINAL APPROVAL**. Blender production complete; not frozen. | `Traffic_Sedan_B/previews/TrafficSedanB_sheet_FINAL_REVIEW.jpg`, `reports/TS_SedanB_STATUS.md` |
| Hatchback A | **REVISED BLOCKOUT v2 — AWAITING VISUAL APPROVAL** | `Traffic_Hatchback_A/previews/v2/` |
| SUV A | **REVISED BLOCKOUT v2 — AWAITING VISUAL APPROVAL** | `Traffic_SUV_A/previews/v2/` |
| SUV B | **REVISED BLOCKOUT v2 — AWAITING VISUAL APPROVAL** | `Traffic_SUV_B/previews/v2/` |
| Pickup A | **NEW BLOCKOUT v2 (pickup builder) — AWAITING VISUAL APPROVAL** | `Traffic_Pickup_A/previews/v2/` |

Each revised vehicle has:
- `blend/<ckp>_01_blockout_v2.blend` (new versioned checkpoint);
- `reports/blockout_check_v2.json`, `build_v2.log` and `*_blockout_stats_v2.json`;
- `scripts/v2/` (exact builder + design snapshot);
- `previews/v2/`: front¾, rear¾, front, rear, side, chase camera, clay front¾, and a zebra diagnostic of the master body in `previews/v2/zebra/` (hood, quarter, full side).

The v1 blockouts are untouched next to them.

**Consolidated comparison:** `previews/FLEET_COMPARISON_v2_SedanA_SedanB_HatchbackA_SUVA_SUVB_PickupA.jpg`
- Rows: Sedan A r3 · Sedan B · Hatchback A v2 · SUV A v2 · SUV B v2 · Pickup A v2.
- Columns: front¾ · side · rear¾ · orthographic side at **one shared scale** (5.75 m frame, same camera).
- Same studio, lights, camera rig and 24 spp for every row. Source frames are in `previews/fleet_compare_v2/`.

## 2. Measured (built geometry, `blockout_check_v2.json`) — all checks PASS

| | Hatchback A | SUV A | SUV B | Pickup A |
|---|---|---|---|---|
| L × W(body) × H (m) | 4.255 × 1.798 × 1.469 | 4.474 × 1.845 × 1.681 | 4.966 × 1.978 × 1.795 | 5.300 × 1.891 × 1.854 |
| Brief range | L 4.0–4.3 | 4.35–4.55 × 1.80–1.86 × 1.60–1.70 | 4.85–5.10 × 1.93–2.00 × 1.72–1.80 | mid-size crew cab |
| Wheelbase / track F | 2.63 / 1.54 | 2.68 / 1.60 | 2.98 / 1.68 | 3.25 / 1.62 |
| Tire radius | 0.317 | 0.370 | 0.391 | 0.388 |
| Overhang F / R | 0.877 / 0.748 | 0.919 / 0.875 | 0.938 / 1.048 | 0.918 / 1.132 |
| Body min z | 0.146 | 0.201 | 0.220 | 0.397 (cab and bed floor; frame not modelled) |
| Triangles, excl. subdivided master | 11,137 | 11,809 | 13,308 | 10,844 |
| Deviation from design L / W / H (m) | −.005 / +.008 / +.009 | −.006 / +.005 / +.021 | −.014 / +.018 / +.035 | −.020 / −.009 / +.024 |

Checks per vehicle:
- four wheels on the ground (< 5 mm);
- clearance ≥ 0.12 m;
- no NaN or loose vertices;
- glass, lights, trim and interior present;
- **new:** no part more than 10 cm outside the body bounds;
- **new:** dimensions within 6 cm of the design.

The blockouts carry 14–17 atlas-cell materials. The ≤ 8 target applies at production, after atlas merge.

## 3. Design corrections made

**Hatchback A** (dimensions unchanged)
- Roof-spoiler lip, then about 62° hatch glass running straight into a near-vertical tailgate. The deck under the glass is gone; that deck was what read as a sedan.
- Full-width rear hatch glass, with extra cage stations so the glass covers the whole hatch.
- Wider, squarer roof end; hatch opening shut line at x 0.62.
- Large split boomerang lamps (22 cm at the corner) across the tailgate split.
- Crisper rear corners (radius 55–62 mm instead of 70–100 mm).
- Black diffuser as a defined compact lower bumper.
- The side silhouette now reads as a compact hatchback.

**SUV A** (compact crossover)
- Higher, flatter hood: 1.06 m leading edge, 1.13 m at the cowl. More upright screen and blunt upright face (plan curvature halved, smaller corner radii).
- Original front identity: slim lamps at the hood line joined by a full-width black upper grille band, a large lower grille in a tall bumper, and dark lower cladding. Sedan B instead has a tall central vane grille.
- Belt 4–5 cm higher. Wider, squarer roof (half-width 0.77 m instead of 0.72 m).
- Arch and rocker cladding; defined liftgate.
- Flush structural pillars, so no bars show through the glass.
- Rails start behind the windshield header and are closed box sections.

**SUV B** (premium three-row)
- Tall flat premium hood: 1.14 m leading edge, stronger shoulder crease, high belt. Upright blunt face.
- Large wide grille with horizontal chrome bars; wide lamps at the hood line; horizontal bumper air curtains.
- Wide flat roof over three rows (half-width 0.80 m). Wider rear haunches.
- Original rear signature: tall corner lamps running up the D-pillar edge with a liftgate arm and a lit bar.
- The black D-pillar sliver is gone (the close-up is clean); pillars are flush; rails are box sections starting behind the header.

**Pickup A** (new builder method, not a car-based ute)
- Two separate body shells:
  - engine compartment plus upright crew cab, closed by a real flat **cab-back wall** with its own rear window;
  - separate open **cargo bed** with its own front wall, bedsides (about 10 cm top rails), tailgate face and shut lines.
- 35 mm gap between cab and bed.
- Separate dark-chrome **step bumper**; vertical lamps; big upright grille; 265/65 R17 tires; 3.25 m wheelbase; pickup ride height.
- The v1 and v2 trials are kept in scratch as references.

## 4. Builder v2 (reusable; v1 `ts_vehicle.py` unchanged for the v1 snapshots)

| File | What it does |
|---|---|
| `scripts/ts_vehicle_v2.py` | Class-aware builder |
| `scripts/ts_loft.py` | Body loft, run once per **shell** |
| `scripts/ts_classes.py` | Class presets: sedan, hatchback, suv_compact, suv_full, pickup, van. Has a self-check. |

What v2 adds:
- **Class presets.** Each design declares `CLASS`; presets fill only what the design leaves out, so design values always win. Every coordinate still comes from the design file, so no body is shared between classes.
- **Greenhouse profile per class.** Roof crown, side-glass lean, and an extra roof-edge cage point that keeps SUV, pickup and van roofs square. Subdivision had been pulling the roof edge 5–20 cm inboard.
- **Multi-shell bodies.** `SHELLS` gives the pickup cab and bed as independent lofts, each with its own hood, roof, end surfaces and creases. The van class is preset only and not yet exercised.
- **Construction hooks:**
  - `PILLARS_FLUSH`: B, C and D pillars are part of the skin at exact ring stations; the old appliques floated over one continuous glass strip;
  - `CLAD_F` / `CLAD_R`: lower-bumper cladding;
  - `BUMPER_F` / `BUMPER_R`: separate proud bumper;
  - `CAB_BACK_GLASS`: window in a wall;
  - box-section roof rails (`RAIL_W/H/MAT`).
- **Boolean robustness.** I found that the exact boolean sometimes *added* a cutter instead of subtracting it. This produced a 0.6 m plank in front of SUV B's headlamp and a 1.3 m plank behind SUV A's plate; both were caught and fixed before anything was saved.
  - Cutters are now subtracted one at a time with a bounds check after each. On a failure the cut is retried hole-tolerant, then with an inflated cutter. A cutter that still fails would be skipped and recorded; none were.
  - Groove fences resolve their own corner self-intersections. Without that, cutting one at a time opened the door gaps into wide slots, which happened on the first SUV B v2 build.
  - Retries used: SUV A 3, Pickup A 3, SUV B 0, Hatchback A 0 (built before this change; checks pass). Skipped: none.
- **Tooling:**
  - `ts_blockout_check.py`: dimension-vs-design and stray-part checks;
  - `ts_zebra.py`: `TS_ZVIEWS` view subset;
  - `ts_fleet_sheet.py`: comparison and review sheets;
  - the scratch `official_v2.sh` refuses to overwrite and writes versioned outputs.

## 5. Unresolved design issues (for review)

- **SUV B:** the hood zebra shows pillowing from the stronger hood-ridge sculpt (0.016). Reduce it or replace it with a crisp character line at the next revision. The front reads as a generic large luxury SUV; the identity could be pushed further.
- **SUV A:** the front face is a plain body-colour slab between the upper band and the lower grille; it needs surface sculpt.
- **Hatchback A:**
  - the tailgate between the lamps and the plate is a tall plain surface;
  - rear overhang stays at 0.75 m, which matches the class reference; I did not shorten it further;
  - the front was not revised (not requested).
- **Pickup A:**
  - the windshield is still fairly raked (about 43° from horizontal);
  - the arch-lip cladding shades jagged around the tires in clay;
  - the hood and front corners are soft;
  - there is no frame or underbody under the bed, because the body floor is 0.40 m.
- **All:**
  - wipers render as bright pieces at the cowl in studio light;
  - softbox reflections in the side glass at the A-pillars in front views;
  - the zebra cameras are framed for sedans, so SUV and pickup views are tighter.
- **Leftovers to clean up with your permission:** three empty or log-only folders (`scripts/game`, `scripts/studio`, `scripts/pickup_a`) from last night's failed preview call. Nothing was deleted.

## 6. Integrity and storage

- `va_frozen_check.py`: **FROZEN CHECK PASS.** ZeroGapR 70, TitanGT 81, TitanGT_r1 89, VortexR 109, VortexR_r1 91, RavenXR 147, Traffic_Sedan_A_r3 246 files (includes shared textures) — 0 changed or missing.
- `va_integrity.py`: **INTEGRITY PASS** — 0 changed, 0 added, 0 removed outside `vehicles/` (frozen P0–P3, Hypercar).
- Pulse EV SHA `18af7277976a…`: unchanged. Sedan A r3 09 file: SHA OK. Sedan B production files: unchanged.
- No `.fbx`, `.meta`, Unity or UnityTransfer files created.
- **Nothing deleted.** Failed or superseded builds were moved, not deleted:
  - `Traffic_SUV_A/*/_failed_v2` (plate plank build);
  - `Traffic_SUV_B/*/_superseded_v2_doorslots`.
- Free disk space: about **10 GB** (was about 11 GB). The disk guard never tripped.
- Usage: scratch 1.4 GB; Hatchback A 20 MB, SUV A 42 MB, SUV B 43 MB, Pickup A 13 MB, fleet previews 46 MB.

## 7. Recommended next step

Review the comparison sheet and the four v2 folders. For each vehicle, approve it, list corrections, or reject it. Once approved, production goes in this order: SUV A → Hatchback A → SUV B → Pickup A, with the Sedan B freeze whenever you approve it. Van and commercial vehicles can start from the `van` preset with a new design file.
