# Phase E — Raven XR: final production QA report

**Status: APPROVED and FROZEN — Phase E technical release** (2026-10-08). Any later change requires a separate revision folder; nothing here is edited. Non-blocking limitations are recorded in section 8; the Vortex R cross-check (section 7) is repaired separately in `vehicles/D_VortexR_r1/`.

**Base:** the approved blockout `blend/ravenxr_01_blockout.blend` (SHA-1 `52a857d7f323648633deed30a1389214029c7f75`). It is byte-identical after this work; it was only read.

## 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/RV_validation.txt`) | **18 checks + supplementary S1: 0 errors, 0 warnings** |
| FBX clean re-import | 2 of 2 files pass, 36 and 102 objects. Bounds deviate by 2.7e-7 m and pivots by 1.5e-7 m. Checked in raw Unity space: nose +Z, up +Y, FL on −X |
| Close-up LOD1 shading (S1, numeric) | Every LOD1/LOD2 body, glass, trim, lights, interior and steering mesh has ≤ 0.09 % torn loop normals; Body_LOD1 is 0 %. The test is calibrated so that Titan GT original fails (11.9 % / 26.6 %) and Titan GT r1 passes (0 %). Visual close-ups: `previews/RV_lod1_closeup_shading.jpg` (top row LOD0, bottom row LOD1) |
| Protected files | **PASS** before and after the phase. Baseline 1,554 files; frozen Zero Gap R (70), Titan GT original (81), Titan GT r1 (89) and Vortex R (109) are unchanged; the approved blockout SHA matches |
| Checkpoints | `ravenxr_02_body_panels` … `_09_export_ready`, each written once |

## 2. Mandatory P0 corrections (done before detailing)

### P0-a: rear-deck sail-to-deck waviness — fixed

- **Cause:** in the blockout, the fading greenhouse control points (C-pillar and sail) slid sideways onto the deck-crown points between y 1.46 and 1.70 m. One point moved from x ≈ 0.62 to ≈ 0.44, which bunched the reflections around x ≈ 0.55.
- **Fix (`rv_lib.ring_half_p0`):**
  - In the rear half, the deck control points sit at the same lateral positions as the greenhouse points, so the fade only moves them vertically.
  - The hood and front (y < 0.6 m) keep the approved point distribution exactly (0.0 mm difference).
  - The shoulder character line is locked and untouched, so the rear haunch and ducktail are preserved.
- **Verified before any detailing**, on the stage-02 body, on both sides:

| Section | Blockout: inflections / fairness RMS | Production |
|---|---|---|
| Deck x = +0.55 | 9 / 106 | **1 / 5.1** |
| Deck x = −0.55 | 11 / 149 | **1 / 14.7** |
| Deck x = ±0.62 | 7–13 / 103–144 | **1 / 5.0–10.3** |
| Sail x = +0.60 | 4 / 41 | **1 / 1.6** |
| Sail x = −0.55 | 12 / 69 | **1 / 4.3** |

The one remaining inflection is the designed ducktail. Zebra QA was re-run on the deck, quarter panels and tail corners, **both sides**: `previews/zebra_RV_final/` (`deck`, `deck_r`, `quarter`, `quarter_r`, `tail_corner`, `tail_corner_r`). The comparison is in `RV_zebra_compare_final.jpg`, with rows Titan GT r1, Vortex R, Raven blockout and Raven final.

### P0-b: sharper design — done without making the body angular

- **Hood leading edge:** a controlled transverse crease (0.55).
- **Rear deck edge:** a crease (0.50). Both taper to zero toward the fender crest, so there is no crease-end knot at the corners.
- **Fender-crest crease:** unchanged (0.66), with the same nose and tail fade, so the crest transitions stay clean.
- **Front bumper and intakes:** these are now real recessed openings with crisp walls:
  - the inverted-trapezoid grille, 10 cm deep, with a gloss-black brow bezel;
  - a thin upper slot;
  - corner air curtains, 8 cm deep, with vanes;
  - angular headlamp housings, 6.5 cm deep, with tight corner radii, including the fang.
- **Rear bumper and diffuser:** they are now integrated:
  - a satin-black valance recess that frames the exhausts;
  - a diffuser tunnel cut into the underbody;
  - five strakes plus side plates that taper to about 6 cm at the tail. An earlier scratch build showed strakes hanging 14 cm below the valance; fixed.

## 3. Production detailing

| Area | Built |
|---|---|
| Front | Recessed honeycomb grille (back plate plus lattice) with a gloss-black brow. Upper slot. Corner air curtains with vanes. **Angular headlight units:** upper DRL blade plus inboard **fang DRL**, **two projector modules**, amber indicator and clear lens. **Real hood heat-extractor vents** (recessed, 5 gloss-black slats each). Front splitter with endplates |
| Side | Panel gaps (4.5 mm grooves): hood (inboard of the fender crests), deck lid and doors. Flush door handles. **Refined front-fender gills** (recessed, 3 slats). **Sculpted side-skirt blade** in gloss black, rising toward the rear. Wheel arches and liners. Mirrors: body-colour pods on gloss-black arms. Gloss-black window seals and DLO surround |
| Rear | **Mirrored chevron signatures** (upper and lower blade plus tip) under integrated red lenses in recessed housings. **Separate brake** (inner chevron fill) and **reverse** (recessed lower lamps). Independent amber indicators (inside each chevron). **Short deck spoiler** on two pylons, carrying the third brake light on its trailing edge. Recessed plate. Black lower valance. **Two oval exhausts.** Five-strake diffuser integrated with the underbody |
| Roof and glass | **Body-colour dark-emerald roof.** Gloss black on the **A-pillars and roof-rail trim**, a **B-pillar applique**, window surrounds, the skirts and mirror arms. Tinted glass is a single sheet with smooth reference normals |
| Wheels and brakes | Dark forged **14-spoke** wheels (7 pairs). Tires 255/35 R19 front and 285/35 R19 rear (approved sizes, with tread and sidewall normal maps). Hub, **5 lug nuts** and a red centre cap. Brake discs with hats. **Red calipers.** Calipers sit inside the barrel clearance (they no longer cut into it; this was found on Vortex and fixed here) |
| Interior | LHD driver on +X. **Sport bucket seats** (alcantara with leather bolsters, **red stitching lines** and integrated headrests). **Driver-oriented dashboard** with red stitching. **Cluster hood with instrument cluster.** Centre screen and **centre console angled toward the driver**, with shifter. **Flat-bottom steering wheel** with a red 12-o'clock marker and paddles. **Door trims** with armrest and red stitching. Headliner, parcel shelf and luggage bulkhead. Built for what is visible through the glass and at chase distance |

## 4. Materials and lighting

- **15 materials:** Paint, Palette, Carbon, Tire, Glass, LensClear, LensRed, Display, plus 7 LED channels.
- **Paint:** dark emerald metallic with a glossy coat (linear 0.008 / 0.062 / 0.040, metallic 0.78, roughness 0.30, coat 0.6). It is untextured, so the colour can be swapped in Unity.
- **Palette:** a single 256 px swatch atlas covering the forged wheel, lug nuts, red caliper and interior accents, gloss and satin black, honeycomb, housings, exhaust and leather.
- **Light channels (independent):** `RV_LED_DRL`, `_Headlamp`, `_Tail`, `_Brake`, `_Indicator_L` (+X), `_Indicator_R` (−X), `_Reverse`. Validation check 11 verified their positions.
- **Tail lenses:** `RV_LensRed` (deep red, alpha 0.80) reads **red in daylight** (`RV_tail_zoom.png`).
- **Textures:** 7 PNGs, 0.1 MB on disk and 10.8 MB as uncompressed RGBA.

## 5. LODs and mobile budget

| | Triangles | Ratio | Target |
|---|---|---|---|
| LOD0 | **74,271** | — | 60–90k |
| LOD1 | 34,711 | 47 % | 40–50 % |
| LOD2 | 15,185 | 20 % | 15–25 % |
| LOD3 | 5,818 | 8 % | 5–10 % |

- **Render objects** are 22 / 22 / 22 / 13 per LOD, with 15 materials.
- **Silhouette IoU:** LOD1 ≥ 0.9998 and LOD3 ≥ 0.9925. Dimension drift is 1.3 mm.
- **Vortex R method:** the LOD1–3 bodies are decimated from a **groove-free body**, then re-projected with smooth-reference normals.
- **New for Raven:** LOD1 hard-surface parts (trim, lights, interior, steering) use **their own normals with 38° hard edges, not normals transferred from LOD0**. Only the glass keeps the transfer.
  - The first scratch build measured 9.8 % torn loops on Lights_LOD1 and 3.5 % on Interior_LOD1 with the transfer. Now it is ≤ 0.04 %.
- **LOD3** drops the brake hardware and steering wheel.

## 6. Unity rig

- `Car_Root` → `LOD0_Root` … `LOD3_Root`.
- `SteerPivot_FL/FR` on the front wheels. Wheel origins sit on the `WheelColliderRef_*` markers (FL 0.83 / −1.34 / 0.331, RL 0.835 / 1.34 / 0.341).
- Pivot tests pass: ±30° roll, +25° steer, and calipers steer but do not roll.
- **4 convex colliders:** Front 176, Body 186, Cabin 148 and Rear 150 triangles; Rear includes the deck spoiler. They cover the body to within **0.002 m**.
- **CenterOfMass** at (0, −0.08, 0.44): front-mid engine, slightly ahead of mid-wheelbase.
- **FBX:** `RavenXR_complete_unity.fbx` (102 objects) and `RavenXR_LOD0_unity_test.fbx` (36), using the in-memory axis bake (residual 1.5e-7).

## 7. Cross-check finding (read-only, reported, NOT changed): Vortex R Trim_LOD1

- **How it was found:** the new S1 metric, run on the frozen releases, measured **23.0 % torn loops on Vortex R `Trim_LOD1`**.
- **Cause:** the same normals transferred from LOD0 that caused Titan GT's rocker blotches. Vortex's Body_LOD1 is clean (0.008 %).
- **Visual evidence:** `previews/xcheck_VortexR_LOD1/` (LOD0 compared with LOD1). The carbon **wing reads silvery and blotchy instead of black at LOD1**, and the rocker blade and diffuser fins show smears.
- **Severity:** milder than Titan's tears, but visible at mid distance.
- **Proposed fix (needs your approval, because Vortex R is frozen):** a `D_VortexR_r1/` revision that changes `Trim_LOD1` (and Lights/Interior LOD1 if they measure above 1 %) to their own normals only. No geometry changes. The same approach as Titan GT r1.

## 8. Known limitations

- **Doors** have modelled shut lines at LOD0 but don't open. LOD1–3 are groove-free by design.
- **Interior** is built for visibility through the glass and at chase distance, not for hero close-ups.
- **Honeycomb grille:** it is a diagonal lattice over a mesh back plate, so it reads as honeycomb at gameplay distance rather than as true hexagonal cells.
- **LOD3 trim** at 6 % shows faceting at unrealistically close range.
- **Emission strengths** need tuning in Unity with bloom. **No Unity runtime or performance testing was done**; Unity is not installed.
- **Cage fairing:** it moved control points by up to 219 mm relative to the raw blockout cage. This is mostly the P0 sail re-placement and the greenhouse rail points. The faired result is what was zebra-checked and is the design under review.

## 9. Deliverables

| Path | Contents |
|---|---|
| `previews/RV_compare_5cars.jpg` | Hypercar, Zero Gap R, **Titan GT r1**, Vortex R and Raven XR with identical cameras, lighting and settings (7 views) |
| `previews/RV_compare_blockout_final.jpg` | Approved blockout (top) compared with final (bottom) |
| `previews/RV_details_front_side.jpg`, `RV_details_rear_wheel_interior.jpg` | Close-ups: front, hood, gill, door; tail, spoiler, wheel, interior, greenhouse |
| `previews/RV_zebra_compare_final.jpg` + `zebra_RV_final/` | Zebra QA, both sides (10 views per car) |
| `previews/RV_lod1_closeup_shading.jpg` + `lod1_closeup/` | Close-up LOD1 shading inspection (LOD0 compared with LOD1, 6 views) |
| `previews/RV_lod_lineup.png` | LOD0–LOD3 lineup |
| `previews/RV_*.png` | 18 review renders, including the chase view on the frozen P0 road |
| `previews/RV_blockout_*`, `zebra_RV/` | Approved blockout renders and zebra, kept |
| `blend/` | 01 (approved blockout) to 09 (export ready) |
| `exports/`, `textures/` | 2 FBX files and 8 PNGs |
| `reports/` | `RV_validation.txt`, `RV_geometry.json`, `RV_export_manifest.json`, `RV_build_log.json`, `RV_source_integrity_check.md`, `RV_FREEZE_CANDIDATE.md`, the blockout report and stats, and this report |
| `UnityTransfer/` | FBX, Textures, Reports, `README/RV_UNITY_IMPORT_NOTES.md` |
| `scripts/` | `rv_lib` (approved design verbatim + P0), `rv_build`, `rv_export`, `rv_render` (+ LOD option), `rv_zebra` (both sides), `rv_validate` (+ S1), `rv_package`, `rv_blockout`, `rv_sheet` |
