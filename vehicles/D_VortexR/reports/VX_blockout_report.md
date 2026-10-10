# Phase D — Vortex R: design blockout (checkpoint 01)

**Status: blockout complete, awaiting design approval.** Final detailing has not started.
- Checkpoint: `blend/vortexr_01_blockout.blend`
- Script: `scripts/vx_blockout.py`
- Renders: `previews/VX_*.png` at 100 %, with the same camera rig and lighting as the other cars
- Comparison sheet (4 rows: Hypercar, Zero Gap R, Titan GT, Vortex R): `previews/VX_blockout_compare_4cars.jpg`
- Surface QA: `previews/VX_zebra_compare_titangt_vortexr.jpg` (frozen Titan GT on top, Vortex R below)

## Dimensions

| | Vortex R (design / measured) | Titan GT | Zero Gap R | Hypercar |
|---|---|---|---|---|
| Length | 4.56 / 4.586 m | 4.72 m | 4.46 m | 4.70 m |
| Body width | 2.07 / 2.086 m | 2.00 m | 2.01 m | 2.05 m |
| Body height | 1.13 / 1.123 m; 1.275 m to the wing top | 1.29 m | 1.20 m | 1.17 m |
| Wheelbase | 2.72 m | 2.82 m | 2.70 m | 2.78 m |
| Track, front / rear | 1.72 / 1.70 m | 1.69 / 1.71 m | 1.65 / 1.67 m | 1.67 / 1.67 m |
| Overhang, front / rear | 0.94 / 0.90 m | 0.92 / 0.98 m | — | — |
| Tires | 255/30 R20, 325/25 R21 | 265/35 R20, 305/30 R21 | — | — |
| Ground clearance | 0.105 m | 0.125 m | — | — |

Overall width is 2.26 m including mirrors and the wing endplates.

## Exterior design

Vortex R is an original mid-engine supercar. Its identity reads as extreme speed, track-focused.

- **Silhouette.** A low wedge nose (0.40 m at the tip) rises through a sculpted hood valley between crisp fender crests into a fast windshield.
  - The teardrop canopy is cab-forward, narrow, with strong tumblehome (1.0 m roof over a 2.09 m body).
  - Behind it sits a long engine deck with six louvres.
  - Big rear haunches end in a square, wide Kamm-tail rump.
- **Front.** Three intakes: two large trapezoid corner intakes with a carbon blade, plus a centre nose intake. Two hood vents. A slim carbon splitter.
- **Headlights.** Sharp "boomerang" units: a white LED blade along each fender front with a down-hook beside the intake, and an amber indicator inside the clear lens.
- **Side.** A deep intake behind the door: the body scoops in by 115 mm, with a dark throat and a carbon blade at the mouth. Door shut lines, a carbon rocker blade, and aero mirror pods on carbon stalks.
- **Rear.**
  - Lights: segmented tail lamps (three raked LED slashes per side under a smoked-red lens), joined by a thin full-width red thread.
  - Wing: a swan-neck rear wing (cambered airfoil, endplates) with a centre third brake light.
  - Lower rear: a tapered black mesh panel housing a high-mounted centre twin exhaust, and a large carbon diffuser with six strakes.
- **Wheels.** Dark forged 10-spoke wheels (five swept Y-pairs), 20-inch front and 21-inch rear, large rotors and acid-green calipers.
- **Paint.** Satin metallic deep violet with black carbon aero.

How it differs from the other three cars:
- **Hypercar:** red, organic, curved canopy, active spoiler.
- **Zero Gap R:** red, open glass frame, side intakes ahead of the rear wheels.
- **Titan GT:** blue front-engine GT, long hood, fastback, full-width light bar.

Vortex R is the lowest of the four and the only one with a cab-forward teardrop canopy, a fixed swan-neck wing, slash tail lights and boomerang headlights.

## Surface quality (lessons from TG-PB-1 and TG-PB-2)

Titan GT's rear-deck waviness and hood dip came from a dense, unevenly faired loft. Vortex R is built differently:

1. **A coarse cage:** 29 stations about 0.2 m apart, with 26 points per section. It is subdivided three times (Catmull-Clark).
2. **Cage fairing before subdivision:** Taubin 30 x (0.5, -0.53) along Y + 12 x (0.45, -0.48) around each section. The largest single control-point move was 123.3 mm, at the windshield-base cowl, where the abrupt slope change was softened.
3. **A creased fender-crest character line** (subdivision crease 0.62). The shoulder stays crisp while the panels on either side stay fair, instead of using extra dense geometry for sharpness.
4. **Zebra reflection-line QA** (`scripts/vx_zebra.py`: paint as a mirror under a striped environment) on the hood, roof, rear deck, doors and full side. Vortex R shows continuous, flowing bands with no blotches or kinks. The same test on the frozen Titan GT shows jagged bands on its door and rear deck (TG-PB-1/2), which confirms the method catches that defect class.

During this check I found a bug in my own QA script: the first Titan GT reference render drew all four overlapping LODs at once and came out uniformly grey. I fixed the script to render LOD0 only, re-rendered, and confirmed the Titan normals are clean (median 1.4° from the faces). The invalid render was moved out of the deliverables.

## Triangles

The blockout is about 112,806 triangles. The body alone is the level-3 subdivided cage, roughly 90 k. This is not optimised: the final LOD0 will be budgeted to 60–90 k with the proven Titan GT pipeline.

## Known visual limitations (blockout)

These will be addressed in detailing.

- **Projected panels:** the intakes, hood vents, lights and mesh panels are flat patches projected onto the surface. Detailing replaces them with real recessed openings, housings and grilles, as was done for Titan GT.
- **Mirrors:** simple pods.
- **Interior:** a silhouette only (race seats with acid-green accents, a wraparound dash, a console, a bulkhead).
- **Rear mesh panel:** a large flat rectangle at this stage.
- **Wing:** the pylons are thin box sections, to be refined.
- **Tail corners:** the zebra stripes pinch slightly where the haunch meets the Kamm-tail edge. This is to be checked again after the tail opening is cut.
- **Not yet built:** LODs, UVs and textures, colliders, the Unity rig and FBX. These follow the established pipeline after approval.

## Integrity

Checked 2026-10-08 13:45:
- **Phase A baseline (1554 files outside `vehicles/`):** 0 changed, 0 added.
- **Frozen Zero Gap R (70 files):** 0 changed.
- **Frozen Titan GT (81 files):** 0 changed.
- **Result:** PASS.
