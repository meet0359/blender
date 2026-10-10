# Phase E — Raven XR: design blockout report

**Status: BLOCKOUT COMPLETE, AWAITING DESIGN APPROVAL** (2026-10-08). Final detailing has not started. Pulse EV and the traffic fleet have not started.

- Checkpoint: `blend/ravenxr_01_blockout.blend`, written once.
- Integrity before and after this phase: **PASS**.
  - Baseline: 1,554 files.
  - Frozen Zero Gap R (70 files), Titan GT original release (81), Titan GT r1 (89) and Vortex R (109): 0 changed.

## 1. Design intent

Raven XR is an original Japanese-inspired front-engine two-door performance coupe built for balanced handling. It does not copy any production car.

| Area | Design |
|---|---|
| Proportion | Long hood with the cabin set back (windshield base about 0.82 m behind the front axle) and a compact fastback greenhouse with a body-colour roof, rail and sail panel. A short deck ends in a slight ducktail |
| Hood | Sits in a **valley between raised front-fender crests**, 14 cm below the crests at the front axle in the design curves, before fairing. Twin long heat-extractor vents sit near the cowl |
| Fenders and side | A crisp fender-crest character line runs from the front fender to the rear haunch and fades out at the nose and tail. Coke-bottle waist (0.918 m half-width at the doors, 0.998 m at the rear haunch). Concave lower-door sculpt, black side-skirt blade, front-fender gill |
| Front | Slim angular LED headlights that rise outboard, with an upper DRL blade and an **inboard "fang"** dropping beside the grille. Two projector modules and an amber indicator per side. A wide inverted-trapezoid honeycomb grille with a gloss-black brow, a thin upper slot, vertical corner air curtains and a black splitter |
| Rear | A **chevron (">") signature** on each side: two red blades meeting at an outboard tip under a red lens, with no full-width bar. A small amber indicator sits inside each chevron. Also a plate recess, a black lower valance, an aggressive 5-strake diffuser, one large oval exhaust in each outboard corner, and lower reflectors |
| Aero | A deck spoiler (cambered blade on two short pylons, not a wing) and a black splitter and skirts |
| Wheels | Dark forged 14-spoke wheels (7 pairs), large rotors and red calipers. 255/35 R19 front, 285/35 R19 rear |
| Colour | Dark emerald metallic paint (blockout base 0.008 / 0.062 / 0.040, metallic 0.78, roughness 0.30, coat 0.6), with black aero accents |
| Interior | Driver-focused LHD layout (driver on +X): sport seats with red accents, a cluster hood over the driver, a centre console angled toward the driver, and a parcel shelf under the fastback glass |

### How it differs from the fleet (`previews/RV_blockout_compare_5cars.jpg`)

- **Hypercar and Zero Gap R:** red, mid-engine.
- **Vortex R:** violet mid-engine with a canopy, big wing and slash lamps.
- **Titan GT:** a blue grand tourer with a horizontal-bar grille and a full-width tail bar.
- **Raven XR:** the only fastback front-engine coupe, the only green car, the only one with a deck spoiler and chevron lamps, and the only one whose hood sits in a valley between the fenders.

## 2. Dimensions

| | Target | Measured |
|---|---|---|
| Length | 4.40–4.65 m | **4.549 m** (body 4.52 m) |
| Width | 1.90–2.02 m | **1.975 m body**, 2.04 m with mirrors |
| Height | 1.22–1.35 m | **1.320 m** |
| Wheelbase | 2.60–2.75 m | **2.68 m** |
| Track (front / rear) | — | 1.66 / 1.67 m |
| Overhang (front / rear) | — | 0.96 / 0.88 m |
| Ground clearance | ≥ 0.10 m | **0.113 m** (body lowest point) |

## 3. Surfacing (refined Vortex R method)

- The body is a coarse, evenly spaced quad cage of 29 stations × 26 points, built from smooth design curves.
- It is Taubin-faired along the length and around each section, with the floor and the fender-crest line locked.
- Catmull-Clark subdivision is applied at level 3.
- The fender-crest crease (0.66) fades out at the nose (−2.14 to −1.84 m) and the tail (1.62 to 2.02 m). This is the lesson from Vortex R's tail-corner pinch.
- A lighter roof-rail crease (0.45) keeps the coupe roof edge crisp.
- Avoided by construction:
  - **Titan GT's lofting defects:** dense stations and smoothing hacks.
  - **Its LOD defects:** groove-free LOD bodies will be used in production.

## 4. Zebra and waviness QA

Zebra renders for hood, roof, deck, door, full side, tail corner and quarter panel are in `previews/zebra_RV/`. They are compared with Titan GT r1 and Vortex R using identical cameras in `previews/RV_zebra_compare_titangt_vortexr_ravenxr.jpg`; the references are in `zebra_ref_TG_r1/` and `zebra_ref_VX/`.

| Panel | Result |
|---|---|
| Hood | Smooth, wide bands with 1 inflection per section (the designed valley). Fairness 1.3–2.5, versus Vortex's 12–14 at blockout |
| Roof | No inflections |
| Doors and full side | Straight, evenly spaced bands with 0 lateral inflections (fairness 0.37, versus Vortex's 1.28). The cleanest side of the three cars |
| Tail corner and quarter | Continuous bands flow around the rear haunch into the tail, with no pinch |
| **Rear deck, outboard** | **Open item:** the section at x = 0.55 m shows 9 inflections where the fastback sail panel blends into the deck (the greenhouse fades out between y 1.46 and 1.70 m). It is visible in the zebra as bunched bands at the sail-to-deck transition. The centreline is clean (1 inflection, the designed ducktail). To be faired in final production |

Measurement notes:
- The quarter-panel lateral waviness figure in `RV_blockout_stats.json` is **invalid**: its probe line at z 0.70 m passes through the rear wheel-arch opening. The zebra `quarter` view is the valid check.
- The cage fairing moved control points by up to 198 mm (Vortex: 123 mm). This is mostly at the greenhouse rail and DLO points, where the section turns sharply. The renders show the faired result, which is the design under review.

## 5. Known blockout limitations (for final detailing)

- **Soft forms:** the forms are softer than a crisp Japanese surface. The nose and tail plan corners are well rounded, and the fascia is surface-projected rather than cut.
- **Final production will add:**
  - recessed openings: grille, air curtains, hood vents, gill, lamp housings, plate recess;
  - panel gaps;
  - a sharper hood leading edge and fascia creases;
  - real lamp housings with the 7 light channels (the third brake light will sit at the top of the fastback glass);
  - a production interior.
- **Arch edges:** they show the blockout boolean stair-step in close zebra views. This is resolved in production, as on Vortex R.
- **Blockout triangles:** 112,874, unoptimised. The production targets are LOD0 60–90k and LOD1/2/3 at 40–50 / 15–25 / 5–10 %, with optimised materials, 7 light channels, pivots, convex colliders, CenterOfMass, WheelCollider references, Unity axes and FBX with clean re-import.

## 6. Files

| Path | Contents |
|---|---|
| `blend/ravenxr_01_blockout.blend` | Approved-candidate blockout |
| `previews/RV_{front34,rear34,front,rear,left,top,chase}.png` | 7 views with the shared camera rig. The chase view is on the frozen P0 road |
| `previews/RV_blockout_compare_5cars.jpg` | Hypercar, Zero Gap R, Titan GT r1, Vortex R and Raven XR with matching cameras, lighting and settings |
| `previews/RV_zebra_compare_titangt_vortexr_ravenxr.jpg` | Zebra comparison |
| `previews/zebra_RV/`, `zebra_ref_TG_r1/`, `zebra_ref_VX/` | Zebra renders. The references were rendered read-only from the frozen files |
| `reports/RV_blockout_stats.json` | Cage, dimensions, waviness and triangle counts |
| `scripts/` | `rv_blockout.py` (helpers copied from Vortex R), `rv_render.py`, `rv_zebra.py` (adds the quarter view), `rv_sheet.py` |
