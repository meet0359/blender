# Phase C — Titan GT: design blockout (checkpoint 01)

**Status: blockout complete, awaiting design approval.** Final detailing has not started.
- Checkpoint: `blend/titangt_01_blockout.blend`
- Script: `scripts/tg_blockout.py`
- Renders: `previews/TG_*.png` (100 %, same camera rig and lighting as the Hypercar and Zero Gap R renders)
- Comparison sheet: `previews/TG_blockout_compare_hypercar_zerogapr.jpg`

## Design intent

Titan GT is an original front-engine grand tourer. Its visual identity is built from these elements:

1. A long sculpted hood (about 1.8 m from the nose to the windshield base), with the fender tops rising above the hood centre.
2. The cabin is set well back: a low fastback greenhouse with strong tumblehome (roof 1.15 m wide over a 2.0 m body).
3. Wide rear haunches. The shoulder grows from 1.97 m at the front axle to 2.02 m at the rear axle, which gives a planted, high-speed-stability stance.
4. A sculpted lower bodyside scallop between the wheels, a carbon sill blade, and a front-fender aero vent with three bright fins.
5. Front: a wide trapezoid grille with horizontal dark-chrome slats and frame, slim swept LED headlight units (DRL blade, projector strip, amber indicator), lower corner intakes and a carbon splitter lip.
6. Rear: a ducktail deck, a full-width red LED light bar wrapping into C-shaped corner signatures, a satin-black lower valance with integrated quad exhaust, diffuser strakes, and a blank plate recess.
7. Five twin-spoke 20/21-inch wheels in dark graphite, large rotors, and bronze calipers.
8. Paint: deep metallic midnight blue with clear coat.

These elements separate it from the other cars:
- **Hypercar:** mid-engine wedge, red, canopy cabin.
- **Zero Gap R:** mid-engine, red, side intakes, open greenhouse frame.
- **Planned Vortex R, Raven XR and Pulse EV:** a mid-engine supercar, a JDM coupe and an EV sedan.

## Dimensions (design / measured)

| | Titan GT | Zero Gap R | Hypercar |
|---|---|---|---|
| Length | 4.72 / 4.728 m | 4.46 m | 4.70 m |
| Body width (excl. mirrors) | 2.01 / 2.004 m | 2.01 m | 2.05 m |
| Height | 1.295 / 1.288 m | 1.20 m | 1.17 m |
| Wheelbase | 2.82 m | 2.70 m | 2.78 m |
| Track, front / rear | 1.69 / 1.71 m | 1.65 / 1.67 m | 1.67 / 1.67 m |
| Overhang, front / rear | 0.92 / 0.98 m | — | — |
| Tires | 265/35 R20, 305/30 R21 | — | — |
| Ground clearance | 0.125 m | — | — |

## Blockout state and plan for detailing

These are expected at blockout and will be addressed in later checkpoints.

- **Triangles:** about 82,230 at blockout, from a level-2 subdivided lofted cage. This is not optimised. The final LOD0 will be re-topologised and budgeted to 60–90 k.
- **Surface details:** the grille, lights, vents and shut lines are projected onto the surface. Final detailing replaces them with real openings, lamp housings, door and hood shut lines, and panel gaps.
- **Interior:** only a silhouette (seats, dash, console, wheel). The sport-luxury interior comes in the detailing stage.
- **Not yet built:** LODs, UVs, textures, colliders, hierarchy and pivots. These follow the established pipeline after approval.

## Protected files

Checked 2026-10-08 11:57:
- **Phase A baseline (1554 files):** 0 changed, 0 added outside `vehicles/`.
- **Frozen Zero Gap R (70 hashed files):** 0 changed.
- **Result:** PASS.
