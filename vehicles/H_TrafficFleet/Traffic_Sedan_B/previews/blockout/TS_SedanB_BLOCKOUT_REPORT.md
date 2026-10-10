# Traffic_Sedan_B — design blockout (awaiting design approval)

Date: 2026-10-08.

- This is a **blockout only**. No production modeling, bakes, LODs, rig or export have been done for Sedan B.
- The remaining seven traffic vehicles have not been started.
- Art direction, references and the iteration log are in `TS_SedanB_ART_DIRECTION.md`.

## 1. What the blockout contains

`blend/trafficsedanb_01_blockout.blend` (single file, about 3 MB) contains:

- **Body.** The full high-res body (`Body_Blockout`, 130k triangles).
  - It is built with the Sedan A r3 systems: designed end surfaces, continuous creases, column fairing, master normals.
  - It has real openings and panel-gap grooves.
- **Glass.** Inset glass shell with the revision tint.
- **Lamps.** Lamp units with depth and lenses.
- **Trim.** Grille, intakes, exhaust outlets, plate recesses, mirrors, belt trim and B-pillar.
- **Wheels.** LOD0 wheels: 20" ten-spoke, 245/40 R20.
- **Interior.** A simple premium interior: cream seats, dark dash with aluminium inlays, anthracite headliner.

Dimensions (`reports/TS_SedanB_blockout_stats.json`):

| Dimension | Value |
|---|---|
| Length | 4.97 m |
| Body width | 1.89 m (2.15 m with mirrors) |
| Height | 1.47 m roof (1.49 m to the antenna fin tip) |
| Wheelbase | 2.97 m |
| Tracks | 1.625 / 1.640 m |
| Dash-to-axle | 0.88 m |
| Overhangs | 0.86 m front, 1.15 m rear |
| Body clearance | 0.149 m |

## 2. Review images (`previews/blockout/`)

| Request | Sheet / files |
|---|---|
| Front ¾, rear ¾, front, rear, side, top | `SedanB_blockout_sheet_studio_1.jpg`, `_studio_2.jpg` (1920 frames: `SedanB_*.png`) |
| Chase camera | `SedanB_blockout_sheet_chase_camera.jpg` (7.5 / 22 / 60 m) |
| Neutral clay | `SedanB_blockout_sheet_clay.jpg` (`clay/`) |
| Zebra comparison | `SedanB_blockout_sheet_zebra_SedanA_vs_SedanB.jpg`: Sedan A r3 master on the top row, Sedan B blockout below, same 10 views |
| **A r3 vs B side by side** | <ul><li>`SedanB_blockout_sheet_SedanA_vs_SedanB_threequarter_side.jpg`</li><li>`_front_rear_top.jpg`</li><li>`_orthographic_same_scale.jpg`: true relative size</li><li>`_clay.jpg`</li><li>`_chase.jpg`</li></ul> |
| Daylight (extra) | `SedanB_blockout_sheet_daylight.jpg` |

- **Sedan A r3** is rendered read-only from its frozen export file into `previews/blockout/compare_A/`, with identical cameras, lights and samples.
- **Studio cameras** are pulled back 10 % for **both** cars (`TS_CAM_SCALE=1.1`), so the 4.98 m car is fully framed.

## 3. My design assessment (honest)

**Distinct identity from Sedan A.** The difference is clear in every view:

- the long-hood, cab-rearward RWD proportion;
- the flat long roof;
- the high, wedge-shaped crisp shoulder;
- the 20" flush wheels on wide tracks;
- the upright recessed grille with slim matrix lamps;
- the slim wrap-around tail lamps with the trunk strip;
- the integrated exhausts;
- the satin belt line.

**Not yet final quality.** These are expected at the blockout stage and will be addressed in final modeling:

1. **Fascia surfacing.** The front and rear fascias are still single large surfaces. Bumper sub-shapes, lower lip and intake surrounds are needed to reach a premium read up close.
2. **Seats are boxes.** Cream seatbacks lit through the windshield by the studio softbox read as a pale flat shape in the front ¾ view. They need sculpted seats. This is not a material defect.
3. **Rocker sculpt.** The lower sculpt line is subtle in studio lighting. Final modeling may deepen it or add a dark rocker insert.
4. **Hood surface.** The hood is long and plain. A pair of subtle hood creases would add the premium read.
5. **Mirrors** reuse the Sedan A housing shape and need a premium redesign.
6. **Zebra.** The blockout uses the master body, so the zebra shows the master surface. The game-mesh bake and its shading QA come after approval.

## 4. Production targets after approval (unchanged from your brief)

- **Budget:** LOD0 12k–18k; LOD1 40–55 %; LOD2 15–25 %; LOD3 5–10 %; at most 8 effective materials.
- **Systems:** the shared atlas, tire and light-mask library; independent light channels; correct wheel pivots; convex colliders; Unity axes; clean FBX re-import.
- **Quality pipeline:** the full r3 bake and shading-QA pipeline, including:
  - 2× supersampled bakes;
  - 3D shut-line paths;
  - continuous creases;
  - master normals;
  - zebra on the master and the game mesh.

## 5. Storage

- Disk had about 2.1 GB free before this stage.
- Sedan B so far uses about 70 MB: one blockout file plus renders.
- Disposable scratch files are listed in `../reports/STORAGE_SCRATCH_INVENTORY.md` (about 890 MB). **Nothing was deleted.**
