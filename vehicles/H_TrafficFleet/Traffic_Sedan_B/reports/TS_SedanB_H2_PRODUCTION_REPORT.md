# Traffic_Sedan_B — H2 final production report

**Status: Blender production complete, awaiting your final visual approval** (2026-10-08).

- Not frozen.
- Unity runtime verification pending.
- UnityTransfer was not generated (overnight instruction).
- No other traffic vehicle started; Pulse EV untouched.
- The approved blockout design is preserved:
  - 4.98 m length, 1.89 m body width, 1.47 m height, 2.97 m wheelbase;
  - long executive hood, flat roof crown, wide stance, strong shoulder;
  - 20" wheels.
- No manufacturer's design was copied, and no Sedan A body geometry was reused.

**My verdict.**

- Sedan B is clearly more convincing than Sedan A r3 in:
  - proportions (RWD stance, dash-to-axle 0.88 m vs 0.37 m);
  - front lighting and grille;
  - rear construction (real trunk lid, split lamps, bumper, exhaust finishers);
  - interior (sculpted seats).
- It reads as a believable premium traffic sedan at gameplay distances.
- It is **not AAA**. The remaining plain areas are listed in §7.

| Gate | Result |
|---|---|
| Validation (`trafficsedanb_validation.txt`) | **18 checks + shading screen S1 on every LOD: 0 errors, 0 warnings** |
| FBX re-import | 2 / 2 clean (27 and 71 objects; bounds dev 3.6e-7 m, pivots 1.8e-7 m); Unity space nose +Z, up +Y, FL on −X |
| Protected files | Unchanged: baseline, all frozen releases including **Sedan A r3**, shared library, Pulse EV |
| Unity runtime / performance | **Not tested** |

Note: per your overnight instruction, **no UnityTransfer package was generated**. The two FBX files in `exports/` come from the official H2 build, made before that instruction; no new FBX was created afterwards.

## 1. Storage safety gate

- **Before production:** 1.8 GB free.
- **Your decisions:**
  - remove `~/.gradle/caches` (9.2 GB, done);
  - nothing else removed;
  - proceed at about 11 GB free.
- **Disk guard:** every heavy step checked free space and would stop below 5 GB.
  - Free space never dropped below 10 GB.
  - No checkpoint or export was at risk.
- **Superseded builds:** superseded official build sets were *moved* to scratch, not deleted.
  - `b_superseded_official_1`: 18-segment tires.
  - `b_superseded_official_2`: edge-on grille vanes.
- **Disposable scratch:** listed in `../reports/STORAGE_SCRATCH_INVENTORY.md`. Nothing deleted.

## 2. P0 front fascia

| Item | Built |
|---|---|
| **Grille** | <ul><li>Recessed grille with a chrome bezel inside the opening plus a separate chrome surround on the skin.</li><li>**11 vertical vanes as real bars**: 9 mm chrome front faces, gloss-black side walls 4 cm deep.</li><li>Dark honeycomb mesh 7 cm back, in shadow.</li></ul> |
| **Headlamps** | <ul><li>Dark housing back plate 4.8 cm deep and an inner bezel.</li><li>**4 matrix projector modules** (reflector cups + emitters).</li><li>**7 segmented LED DRL blocks**.</li><li>Independent amber indicator strip; clear outer lens; gloss frame owning the cut edge.</li></ul> |
| **Bumper** | <ul><li>Tight plan corners at bumper height (72–78 mm).</li><li>Vertical side air intakes with **two aero blades each** (real bars) and honeycomb backs.</li><li>Wide lower intake with frame and bar; gloss-black lower lip / splitter edge; front plate on a holder.</li></ul> |
| **Gaps** | <ul><li>Hood shut line just behind the crisp hood leading edge.</li><li>Fascia/fender shut line from the lamp tip into the arch lip (3D-path method).</li><li>The start sits 4 mm outside the lamp under its frame. Starting inside the opening had grazed the cut wall and made a baked sawtooth, found and fixed during QA.</li></ul> |

Wording: "no flat black openings" — the first production build failed this. The vanes were edge-on planes and invisible from the front. They were rebuilt as faced bars, and the grille now reads as chrome vanes in depth.

## 3. P0 rear

| Item | Built |
|---|---|
| **Trunk lid** | <ul><li>**Real trunk-lid shut line**, one continuous 3D path: across the deck just behind the rear-glass seal, back along the deck sides, over the crisp lip, down the rear face beside the lamps, meeting the bumper shut line.</li><li>Defined deck surface, clean leading edge, crisp trailing lip (20 mm radius).</li><li>Integrated high-mount brake LED in the lip.</li></ul> |
| **Lamps** | <ul><li>Slim LED tail lamps wrapping the corner, with housing, bezel depth, dimensional light guide, brake block, indicator and red lens.</li><li>**Lamp split at the lid shut line**, as on production cars.</li><li>Unlit dark-chrome strip across the lid.</li></ul> |
| **Bumper** | <ul><li>Separate bumper: proud 2 cm, with a top ledge and a shut line running from arch lip to arch lip, giving a bumper-to-quarter transition.</li><li>Deep dark valance with a satin trim strip.</li><li>**Integrated trapezoid exhaust finishers**: chrome frame plus inner chrome sleeve.</li><li>Subtle red reflectors; reverse lamps; clean plate recess with holder frame.</li></ul> |

## 4. P0 body surface quality

**Lower-rear-corner zebra: diagnosed, not just smoothed.**

- **Normal probes:** monotonic along the lower quarter, with no kink.
- **Quadric-fit principal curvature:**
  - The region is **96 % convex** (both curvatures bending away from the normal), with 4 % shallow saddle.
  - The front lower corner is the control, and its zebra shows no visible problem. It measures **96 % / 4 %**.
- **Conclusion:** the closed contours there are the reflection extremum of a convex three-way blend seen from a low camera. That is natural double curvature, not a defect.
- **Real improvement made:** the rear floor rise was eased from over 0.25 m to over 0.44 m. This cut peak saddle curvature from 1.8 to 1.1 per metre.
- **Kept on purpose:** the intentional corner radii and the crisp lip.

**Sedan A r3 methods carried over:**

- 3D shut-line paths with hidden ends;
- continuous creases;
- column fairing;
- master normals from the uncut skin;
- 2× supersampled normal bakes;
- no dissolve on top panels.

**Bake health:**

- 6 invalid-bake faces out of 5,276;
- 6 tiny folded master end-cap faces out of 61,440, none visible;
- 10 inverted game faces out of about 6,500.

## 5. P1 body details and interior

- **Hood.** Two subtle ridge lines built into the cage (7 mm, soft crease 0.30), fading out before the cowl and the leading edge.
- **Doors and rocker.**
  - Deeper lower-door sculpt: concave band of 30 mm plus crease 0.65.
  - **Dark-chrome rocker trim** between the arches.
  - Satin-aluminium belt trim; gloss-black B-pillar appliqué.
  - Door shut lines with the top edge under the belt seal; flush handles under the shoulder.
- **Mirror.** A new Sedan B wing housing: thin at the door, tall outboard, swept lower edge, aero front.
- **Interior.**
  - **Sculpted cream seats:** cushion with side bolsters, raked backrest with bolsters, headrests on aluminium posts; rear outboard and centre seats.
  - Two-tone dash (dark upper, cream lower) with satin inlay and four vents; cluster and central display.
  - Steering wheel (12 segments); console with cream armrest and selector.
  - Door cards: dark lower, cream upper, armrests, inlay.
  - Anthracite headliner.
  - Interior instance normal scale 0.12 (restrained); fabric/leather roughness from the shared atlas.
  - The cream seats now read as shaped seats through the glass, not white blocks (daylight glass and studio interior views).

## 6. Performance (estimates, not profiled)

| LOD | Triangles | Ratio | Materials | Draw calls (mesh × material, pre-batching estimate) |
|---|---|---|---|---|
| LOD0 | **17,987** | — | 8 | 19 |
| LOD1 | **8,739** | 49 % | 8 | 19 |
| LOD2 | **4,012** | 22 % | 8 | 19 |
| LOD3 | **1,746** | 10 % | 6 | 13 |

- **Silhouette IoU** vs LOD0: LOD1 0.997, LOD2 0.990, LOD3 0.970 (minimum over side, front and top).
- **Colliders:** 4 convex hulls (94, 152, 152, 166 triangles).
- **CenterOfMass:** (0, −0.08, 0.53).

**Texture memory:** same architecture as Sedan A.

- **Shared fleet set (loaded once):**

  | Format | Size |
  |---|---|
  | ASTC 6×6 | about 8.4 MB |
  | ASTC 4×4 | about 18.5 MB |
  | RGBA8 + mips | 73 MB |

- **Sedan B maps** (2048 normal, 1024 LOD1 normal, 1024 AO/grime):

  | Format | Size |
  |---|---|
  | ASTC 6×6 | about 3.6 MB |
  | ASTC 4×4 | about 8.0 MB |
  | RGBA8 + mips | 32 MB |

- The "94.5 MB" line in the validation log is the Blender-bound RGBA8 set without mips, including Blender-only metallic and roughness maps (see the Sedan A r3 report).

**Mesh memory:** Similar to Sedan A r3: LOD0 is about 18k triangles, about 1.8 MB vertex and index buffers as an upper bound; all four LODs about 3.4 MB.

## 7. Remaining honest shortcomings

1. **Not AAA.** The body is a clean procedural loft with the features above. The lower front fascia between the intakes and the long door sides are still fairly plain surfaces in studio light.
2. **Lower rear corner.** Shows natural convex zebra contours from low cameras (§4). A production surface would be tuned further by a surfacing specialist.
3. **Baked shut lines** are about 5.5 mm and read soft in extreme close-ups (texel density).
4. **Mirror housing** is clean but simple.
5. **Seats** are built from chamfered boxes. They are convincing through the glass and in the close studio interior view, but not hero-quality.
6. **LOD2/3** facet if forced at close range; they hold at real switch distances.
7. **No photographic comparison and no Unity runtime or performance testing.**

## 8. Deliverables (`Traffic_Sedan_B/`)

| # | Deliverable | Location |
|---|---|---|
| 1 | Blender source | `blend/trafficsedanb_09_export_ready.blend` |
| 2 | Production checkpoints | `blend/trafficsedanb_02_body` … `_08_rig`; approved blockout `_01_blockout` |
| 3 | Unity FBX | `exports/TrafficSedanB_complete_unity.fbx` (71 objects), `TrafficSedanB_LOD0_unity_test.fbx` (27) |
| 4 | Textures and materials | `textures/` (bakes); `../shared/textures/`; material setup in `UnityTransfer/README/TrafficSedanB_UNITY_IMPORT_NOTES.md` |
| 5 | Studio and daylight renders | `previews/TrafficSedanB_*.png`; sheets `…_sheet_studio_1/2`, `…_sheet_daylight`, `…_sheet_closeups_*` |
| 6 | Sedan A r3 vs Sedan B | `…_sheet_SedanA_r3_vs_SedanB_threequarter_side`, `_front_rear_top`, `_clay`, `_chase`, `…_sheet_zebra_SedanA_r3_vs_SedanB_game` |
| 7 | Zebra QA | `…_sheet_zebra_master_vs_game`, `…_sheet_zebra_zones_master_vs_game`; `previews/zebra_master`, `zebra_game`, `zebra_diag/` |
| 8 | LOD lineup | `…_sheet_lod_comparison`, `…_sheet_distant_lods_plates`; `previews/lod/` |
| 9 | Clay, wire, normal | `…_sheet_qa_clay`, `_qa_wire`, `_qa_normal`, `_qa_clay_wire_details`; `previews/qa/` |
| 10 | Validation | `reports/trafficsedanb_validation.txt`, `_geometry.json`, `_export_manifest.json`, `TS_SedanB_build_log.json` |
| 11 | UnityTransfer | **Not generated** (overnight instruction). Run `TS_NO_UNITY= ts_package.py` after approval |
| 12 | Integrity | `reports/trafficsedanb_integrity_check.md`; `trafficsedanb_FREEZE_CANDIDATE.md` (candidate only) |

Design history:

- `reports/TS_SedanB_ART_DIRECTION.md`
- `TS_SedanB_BLOCKOUT_REPORT.md`
- `scripts_snapshot_blockout/` (approved blockout script)
