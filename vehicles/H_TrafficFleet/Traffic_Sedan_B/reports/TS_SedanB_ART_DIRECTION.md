# Traffic_Sedan_B — art direction (premium executive sedan)

Stage: **design blockout, awaiting design approval** (2026-10-08). No final modeling has started.

## 1. Process change for every remaining traffic vehicle

Sedan A reached production quality through technical correction rounds, but its body began as a procedural loft with generic proportions. From Sedan B onward, each vehicle starts with an **art-direction stage before any geometry**:

1. **Class references.** Collect *published* real-world dimensions and proportions for 3–4 class leaders. Only facts are used: length, width, height, wheelbase, tracks, tire sizes, overhangs and the dash-to-axle relationship. **No design is copied.** Every vehicle is an original fictional design.
2. **Proportion brief.** Define the numbers that make the archetype read correctly: overhang split, dash-to-axle, cabin position, belt height vs greenhouse, section (where the maximum width sits), wheel diameter and fitment.
3. **Design language.** For each item, state one intent and its realistic engineering basis:
   - shoulder and character lines;
   - hood and trunk construction (where the shut lines go);
   - bumper architecture;
   - lamp geometry;
   - window graphic (DLO);
   - wheel design;
   - rear-quarter construction.
4. **Iterative blockout with self-critique.**
   - Blockout → studio, side and front renders → written art-director critique → revise.
   - Repeat until the silhouette, section and graphics read as the target class.
   - Sedan B took 4 iterations, listed in §5.
5. **Blockout approval.** Same-camera comparison against the previous approved vehicle, plus clay and zebra. Only then the production pipeline:
   - bake, LODs, rig, validation;
   - the r3 root-cause rules (shut-line paths, continuous creases, column fairing, master normals, supersampled bakes).
6. **Reuse systems, never bodies.** Each vehicle gets its own design coordinates. Sedan B shares no body coordinate with Sedan A.

## 2. Class references (published dimensions, facts only)

| Car | Length | Width | Height | Wheelbase | Notes |
|---|---|---|---|---|---|
| Mercedes-Benz E-Class (W214) | 4,949 | 1,880 | 1,468 | 2,961 | tracks 1,634 / 1,651 |
| BMW 5 Series (G60) | 5,060 | 1,900 | 1,515 | 2,995 | 245/45 R19 available; 19–21" wheels |
| Genesis G80 | 4,995 | 1,925 | 1,465 | 3,010 | |
| **Traffic_Sedan_B (fictional)** | **4,980** | **1,890** | **1,470** | **2,970** | tracks 1,625 / 1,640; **245/40 R20** |
| Traffic_Sedan_A r3 (compact, for contrast) | 4,640 | 1,800 | 1,450 | 2,700 | 205/55 R16 |

All dimensions are in mm.

Design-principle reference: a long **dash-to-axle** distance (windshield base well behind the front axle) is the classic visual marker of a premium rear-drive car. Too much tips into awkward. Sources: Hagerty, "Car Design Fundamentals: Dash to axle ratio"; Jalopnik, "The Dash-To-Axle Ratio Is A Delicate Balance".

Data sources: dimensions.com / ultimatespecs (W214); BMW Group press and vehiclesizes.com (G60); carexpert.com.au (G80).

## 3. Proportion brief (Sedan B vs Sedan A)

| Proportion | Sedan A r3 (compact, FWD) | **Sedan B (executive, RWD layout)** |
|---|---|---|
| Front overhang | 0.92 m | **0.86 m** (short) |
| Rear overhang | 1.02 m | **1.15 m** (longer: formal deck) |
| Dash-to-axle | 0.37 m | **0.88 m**: long hood, cab-rearward stance |
| Hood length (nose to cowl) | about 1.29 m | about 1.74 m |
| Roof | short dome, peak over the front seats | **long flat crown** from B-pillar to C-pillar, defined windshield and rear-glass breaks |
| Section (maximum width height) | z 0.58–0.62 | **z 0.64–0.68**: no pear section |
| Shoulder | soft crease | **strong crisp shoulder (crease 0.80), lamp to lamp**, rising gently rearward (wedge) |
| Lower body | — | **rocker sculpt line** (concave band + crease) on the doors |
| Wheels | 16" in 205/55: tall sidewall, inset | **20" in 245/40**: thin sidewall, wide tracks, near-flush fitment |
| Belt / DLO | black seal | **satin-aluminium belt trim**; narrow gloss-black B-pillar (10 cm) |

## 4. Design language

- **Front.**
  - Upright, deep-recessed grille: a chrome frame, five gloss bars with depth, and a dark mesh 7 cm back.
  - Slim **matrix headlamps** with four projector cells, an upper LED DRL guide and an amber indicator strip, placed high under a crisp hood leading edge (22 mm radius).
  - Vertical side air intakes, a wide dark lower intake band, and a plate on the bumper.
  - Tight plan corners at bumper height (72–95 mm).
- **Side.**
  - A long hood and a set-back cabin.
  - One shoulder line from headlamp to tail lamp.
  - A lower rocker sculpt.
  - The rear door follows the arch lip. The front door shut line runs from the lamp corner into the arch lip; the door top shut lines run under the belt seal.
  - Flush handles under the shoulder.
- **Rear.**
  - Short formal deck with a crisp trunk lip (20 mm) and an **integrated high-mount brake light in the lip**.
  - **Slim LED tail lamps wrapping the corner**, joined by an unlit dark-chrome strip across the trunk.
  - Plate recess on the trunk face.
  - Bumper ledge with a shut line from arch lip to arch lip, a deep dark valance and **integrated trapezoid exhaust outlets** with chrome frames.
- **Wheels.** A 20" ten-spoke alloy with straight, tapering spokes, a light dish, machined faces, a 350 mm disc and a larger caliper.
- **Interior** (visible through the glass):
  - light (cream) seats;
  - dark dashboard with an aluminium inlay;
  - wide centre display;
  - **anthracite headliner**, which avoids the pale-liner sheet seen in Sedan A studio views.
- **Paint (review).** Mineral grey metallic, chosen because it shows the surfaces honestly. Colour variants come later.

## 5. Blockout iterations (self-critique)

| Version | Critique | Change |
|---|---|---|
| v1 | <ul><li>Hood 1.83 m long, reading as an old luxury barge.</li><li>Bubble roof.</li><li>Pillowy, droopy front corners.</li><li>B-pillar appliqué 14 cm wide.</li><li>Pear-shaped section.</li></ul> | Dash-to-axle 0.97 → 0.88 m; flatter roof; maximum width raised; tighter front plan corners; B-pillar 10 cm. |
| v2 | <ul><li>The satin belt (on the cut master seal) showed noise.</li><li>The B-pillar overshot the DLO.</li><li>Headlamps were 5 cm slits.</li><li>The rear was heavy, with small lamps and round upper corners.</li></ul> | Separate belt-trim geometry; taller headlamps; taller wrap-around tail lamps; tighter rear corners; deeper valance. |
| v3 | <ul><li>The DLO still followed an arched roof.</li><li>The hood edge was high (0.84 m).</li><li>The rims looked small.</li></ul> | Long flat roof crown; hood edge at 0.82 m; 20" wheels; wider lower intake. |
| v4 | Proportions and graphics now read as a modern executive sedan. | Anthracite headliner. **Submitted for approval.** |
