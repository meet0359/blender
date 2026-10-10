# Phase F — Pulse EV: design blockout report

**Status: BLOCKOUT COMPLETE, AWAITING DESIGN APPROVAL** (2026-10-08). Final detailing has not started. The traffic fleet has not started.

- Checkpoint: `blend/pulseev_01_blockout.blend` (SHA-1 `18af7277976ab32e89c103f81c4e9c941c367f4d`), written once.
- Integrity before and after this phase: **PASS**.
  - Baseline: 1,554 files.
  - Frozen: Zero Gap R, Titan GT original, Titan GT r1, Vortex R original, Vortex R r1 and Raven XR; 0 changed.
  - The reference zebras were rendered read-only, and the files' SHA-1 was checked afterwards.

## 1. Design identity

Pulse EV is an original premium electric four-door performance sedan. It does not copy any production EV.

| Area | Design |
|---|---|
| Proportion | Short front overhang (0.905 m), long 2.95 m wheelbase, cab-forward four-door greenhouse with a fastback into a clean deck. Wide stance (track 1.69 / 1.70 m) with sculpted rear haunches |
| Front | **Enclosed EV nose**, with no combustion grille. A low, smoothly crowned hood, flush with the shoulders. A slim lower cooling slot with three **active-shutter slats**, vertical **corner air curtains** exiting through front-fender outlets, an aero lip, and a sensor strip at the hood leading edge |
| Light signature: the "pulse line" | Front: a slim cool-white DRL blade per side with a small **heartbeat blip** near its inboard end, above **four segmented LED modules**, with an amber indicator at the outer tip. Rear: a **full-width red pulse line** with the same blip at the centre, **segmented vertical end blocks**, amber indicators beneath, and lower reverse lamps. The third brake light sits at the top of the rear glass |
| Greenhouse | **Panoramic glass sweep** from the windshield over the roof to the rear glass, framed by **gloss-black roof rails and A-pillars**. Gloss-black B-pillar applique and DLO seals. Four side windows plus a quarter light |
| Side | Four-door shut lines, **flush door handles**, an aero side-sill blade, a subtle concave lower-door sculpt, and **slim camera-style mirrors** on thin blades |
| Rear | Clean deck with an **integrated active lip spoiler** (split line at the deck edge). A dark lower valance with **no exhaust**, and a modern three-fin diffuser integrated with the underbody |
| Wheels | 21-inch **aero wheels**: 10 broad twisted turbine spokes, a flush outer aero ring and an aero centre cap, in satin dark. Tires 265/35 R21 front and 295/30 R21 rear. Cool-blue calipers |
| Colour (proposal) | **Liquid titanium silver with cool-blue metallic highlights** (linear 0.40 / 0.43 / 0.48, metallic 0.92, roughness 0.22, coat 0.7). Gloss-black roof details, satin-dark wheels, cool-white front lighting, deep-red rear lighting. It does not repeat any fleet colour (red, red, blue, violet, emerald) |
| Interior | LHD. A minimal floating dashboard with an ambient-light line, a **large central display**, a **digital instrument cluster**, a modern steering wheel, a **floating centre console**, **two front seats and a rear bench**, and a parcel shelf, all under the glass roof |

**How it differs from the fleet** (`previews/PV_blockout_compare_6cars.jpg`): it is the only four-door, the only silver car, the only EV with an enclosed nose and no exhaust, the only one with a panoramic glass roof, and the only one with pulse-line lighting.

## 2. Dimensions

| | Target | Measured |
|---|---|---|
| Length | 4.70–4.95 m | **4.848 m** |
| Body width | 1.92–2.05 m | **1.968 m** (2.16 m with mirrors) |
| Height | 1.38–1.50 m | **1.444 m** |
| Wheelbase | 2.80–3.00 m | **2.95 m** |
| Ground clearance | about 0.12–0.15 m | **0.128 m** body lowest point (floor 0.135 m) |

## 3. Surfacing (refined Vortex R and Raven XR method)

- **Cage:** a sparse quad cage of 31 stations × 26 points, built from smooth pchip design curves. It is Taubin-faired along the length and around each section, then given Catmull-Clark subdivision.
- **Creases:** the shoulder crease (0.50) fades out at the nose and tail, and a light crease (0.40) runs along the roof rail.
- **Lessons applied from the start:**
  - **Raven XR P0:** the rear-deck control points sit at the greenhouse x positions, so the fastback-to-deck fade is purely vertical. There is no sail-to-deck bunching.
  - **New in Pulse EV:** sideways fairing now only smooths the body side. The explicitly designed greenhouse points (DLO, rail, roof) are locked. Without this, fairing rounded the DLO corner and raised the roof by 57 mm (to 1.48 m); with it, the roof is 1.444 m as designed.
- **Design fix found by zebra:** the first iteration's hood sat about 3 cm below the shoulders, and its zebra bands wobbled through a shallow valley. The hood now has a slight positive crown and the bands are clean and parallel.

## 4. Zebra and waviness QA

There are 12 zebra views, covering **both sides**: hood, roof, front corner, door (L/R), full side, quarter (L/R), deck (L/R) and tail corner (L/R).
- They are in `previews/zebra_PV/`.
- They are compared, with identical cameras, against Titan GT r1, Vortex R r1 and Raven XR in `previews/PV_zebra_compare_references.jpg`.

| Panel | Result |
|---|---|
| Hood | Clean parallel bands, 1 inflection per section (the crown), fairness 2.0–2.6 |
| Roof (glass sweep) | 1 inflection (the roof peak), fairness 1.8–1.9 |
| Doors | **0 inflections**, front doors fairness 0.11–0.12. The straightest door bands of the four cars compared |
| Quarters | 0 inflections both sides. Bands flow continuously over the rear haunches into the tail |
| Front and rear corners | Continuous bands, no pinch |
| Rear deck | Smooth wide saddle bands with no bunching; 1 inflection at x = 0, 0.3 and +0.55 |

Measurement note: deck x = −0.55 reports 21 inflections. Its height profile matches the +0.55 side to 0.1 mm (probed), so this is the curvature metric reacting to sub-millimetre facet noise on the blockout mesh. The zebra on both deck sides is clean.

## 5. Known blockout limitations (for final detailing)

- **Projected details:** lights, shutters, intakes and shut lines are projected onto the surface. Production will add recessed housings, real shutter slats, door panel gaps (groove-free bodies for LOD1–3), and the 7 light channels: DRL, Headlamp, Tail, Brake, Indicator_L/R, Reverse.
- **Arch edges:** they show the blockout boolean stair-step in close zebra views. This is resolved in production.
- **Rear overhang:** at 0.985 m it is longer than the front, to give the fastback room. It can be shortened at approval if you prefer a tighter tail.
- **Interior:** box silhouettes only.
- **Blockout triangles:** 119,046, unoptimised. Production targets are LOD0 60–90k and LOD1/2/3 at 40–50 / 15–25 / 5–10 %, using the full pipeline with mandatory LOD shading QA (`A_Discovery/reports/VA_SHADING_QA_STANDARD.md`).

## 6. Files

| Path | Contents |
|---|---|
| `blend/pulseev_01_blockout.blend` | Blockout checkpoint |
| `previews/PV_{front34,rear34,front,rear,left,top,chase}.png` | 7 views on the shared camera rig. The chase view is on the frozen P0 road |
| `previews/PV_blockout_compare_6cars.jpg` | Hypercar, Zero Gap R, Titan GT r1, Vortex R r1, Raven XR and Pulse EV with identical cameras, lighting and settings |
| `previews/PV_zebra_compare_references.jpg` + `zebra_PV/`, `zebra_ref_*` | Zebra QA, 12 views per car |
| `reports/PV_blockout_stats.json` | Cage, dimensions, waviness and triangle counts |
| `scripts/` | `pv_blockout.py`, `pv_render.py`, `pv_zebra.py` (12 views, both sides), `pv_sheet.py` |
