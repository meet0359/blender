# Traffic_Sedan_A — H1-r3 focused quality pass

**Status: COMPLETE — AWAITING YOUR VISUAL APPROVAL** (2026-10-08)

- r3 is **not** frozen and is **not** the fleet benchmark.
- None of the remaining eight traffic vehicles has been started.
- Pulse EV is still postponed and untouched.
- H1 and r2 are preserved. Their candidate manifests are byte-identical: 25/25 and 25/25 files.

**My verdict:** r3 removes every surface artifact you rejected in r2.

- The front-fender squiggle is gone.
- The rear-quarter streaks are gone.
- The bumpers are firmer.
- Distant plates are clean.
- The cabin is readable.

At normal gameplay distances it reads as a believable, unremarkable compact sedan. It is **not AAA**. The design-level limits in §6 remain and are the honest ceiling of this procedural body. I do not see a fundamental problem that blocks the traffic-car standard.

| Gate | Result |
|---|---|
| Validation (`trafficsedanar3_validation.txt`) | **18 checks + shading screen S1 on every LOD: 0 errors, 0 warnings** (worst torn-normal mesh: Body_LOD2 0.059 %) |
| FBX clean re-import | 2 of 2 files (27 and 71 objects). Bounds dev 2.7e-7 m, pivots 1.5e-7 m. Unity space: nose +Z, up +Y, FL on −X |
| Protected workspace | Before and after: frozen check PASS; baseline 0 changed / 0 missing / 0 added; shared library 12/12; H1 25/25; r2 25/25; Pulse EV `18af7277976a` unchanged |
| Triangles | LOD0 **14,961** · LOD1 7,756 (52 %) · LOD2 3,546 (24 %) · LOD3 1,383 (9 %) |
| Unity runtime / performance | **Not tested** (Unity is not installed, by design) |

## 1. Artifact root causes (verified) and fixes

Method: for each artifact, three zebra renders from identical cameras were compared:

- the high-res master;
- the low-poly game mesh with the normal map **disconnected**;
- the fully shaded game mesh.

This shows whether the defect lives in geometry, in the bake, or in shading. Evidence is in `previews/zebra_diag/` (R2_*, R3_*, R*master_*) and `TrafficSedanA_sheet_zebra_artifact_zones_r2_vs_r3.jpg`.

| # | Artifact (r2) | Where it lived | Verified cause | r3 correction |
|---|---|---|---|---|
| 1 | Squiggle / torn highlight beside the headlamp | **Master geometry → baked normal map.** The game mesh without the normal map was clean there. | The fascia/fender shut-line groove was traced with side rays at grazing incidence on the curved corner, sampled every 30 mm. The groove cutter twisted into a zigzag, the master boolean became a sawtooth, and the bake copied it. | The shut line is now a 3D guide curve: Catmull-Rom, resampled every 5 mm, closest-point projected, smoothed, with a smoothed surface frame. The groove starts inside the headlamp opening and ends under the arch lip, so it has no visible open end. |
| 2 | Streaks on the rear quarter by the arch / bumper | Same mechanism as #1 (master → bake). | Same grazing-ray zigzag at the end of the rear bumper shut line. The groove also stopped in open paint. | One continuous path from arch to arch: under the RR arch lip → quarter → around the corner (radial rays, never grazing) → across the face → under the RL arch lip. |
| 3 | Concentric swirls at the hood-to-fender corner | **Real surface geometry.** The master and the un-mapped game mesh both showed it. | (a) The edge-ring crease weights on the end faces stepped .92 → .55 → .25, computed from the *unsmoothed* corner radius. (b) The shoulder crease faded out from .72 to 0 within 16 cm of the lamp. (c) The blend rings behind the end face copied the end outline instead of the section at their own position. | (a) Crease weight is now continuous, from the same smoothed radius the geometry uses. (b) The shoulder line now runs into the hood/headlamp corner, as on real sedans. (c) Blend rings carry the section at their own y, eased toward the outline. |
| 4 | Rings at the lower rear corner | Geometry (master and un-mapped game mesh). | Faired loft rings met unfaired designed blend rings, leaving 3–7 mm kinks along the cage columns (for example x .848 → .851 → .844 m). | Chord-weighted Taubin fairing along each column across the end transition (x, z only). Normal-probe inflections on the lower side went from 3–5 to 1–3, and peak 3rd-difference roughly halved. Some closed contours remain in zebra at this corner. They come from the smooth three-way blend seen from a low camera and are not a kink (§6). |
| 5 | Jagged lamp, plate and arch edges on the master bake | Shading of the master. | Boolean sliver faces shaded with their own smooth normals. | The master's skin loops take the **uncut skin's interpolated normal**; groove and pocket walls get flat normals. Invalid bake faces went from 13 to **1** (of 5,075). |
| 6 | Stair-stepped / wavy hood highlight | Bake correction on 0.6 m sliver triangles. | The 3° planar dissolve made the hood a few huge triangles, so the 8-bit normal map carried large corrections that quantize into steps. | Hood, roof and deck (faces with nz > .55) dissolve at only 0.5°. Sides stay at 3°. The hood zebra now matches the master. |
| 7 | Dashed / beaded panel gaps (seen during r3 QA) | Bake aliasing plus groove placement. | A 5.8 mm gap is about 2.4 texels at 2048. The door top gap also ran 18 mm under the crisp shoulder, which the 10 cm game mesh cannot follow. | Normal maps are baked **2× supersampled** and box-filtered to 2048 / 1024 in float before 8-bit. The door top shut line moved under the belt seal, as on real doors. |

Shut lines now terminate where real ones do: in the lamp opening, under the arch lip, or under the belt seal.

## 2. Bumper and body shape (P0 3)

| Change | Values |
|---|---|
| Front plan corner radius by height (bumper tighter) | r2: one radius of 0.13 m. r3: 0.080 m at the bumper, 0.105 m at the lamp, 0.122 m at the fender top |
| Rear plan corner radius by height | r2: 0.10 m. r3: 0.080 m at the bumper, 0.094–0.10 m up the quarter |
| Lower corner radius | Front .12 → .07; rear .14 → .085 |
| Chin / valance roll-under | Front reduced from 10 cm to 5.5 cm over the same height; rear 13.5 cm → 9.7 cm. This gives a defined lower edge instead of a pillow |
| Hood-to-bumper edge | Kept crisp (28 mm). The shoulder line now runs cleanly into it |

Proportions, headlamp design, tail-lamp design and dimensions are unchanged. It is still an everyday compact sedan, not a sports car.

## 3. Glass, cabin and plates (P0 4–5)

- **Glass.** The shared `TS_Glass` tint (0.50, 0.58, 0.56) was too dark: about 55 % per pane, about 30 % through two panes.
  - r3 uses `TS_SedanA_Glass`, a **revision-specific instance**. Base (0.78, 0.84, 0.82), Unity alpha 0.22. This is a light-green automotive tint with about 75 % visible transmission.
  - The daylight close-up (`TrafficSedanA_day_glass.png`) shows seats, wheel, dash, headrests and the rear bench.
  - The studio interior view uses fill lights placed below the softbox reflection angle.
  - Studio softbox reflections in the side glass are physically correct and are not a material problem. The daylight view shows the difference.
- **Seats.** `TS_SedanA_Interior` is an instance of `TS_Atlas` (same textures and UVs) with normal scale **0.12** instead of 1.0. The weave reads as fabric instead of crumpled.
- **Shared library untouched.** It is still 12/12 byte-identical. Validation accepts the two instances because each declares `instance_of`.
- **Distant plates (LOD2/3).**
  - The plate quads are kept out of the collapse decimation. r2 merged half of each plate into the holder.
  - Their UVs are pinned to the plain white band of the plate cell; the blue band is kept.
  - Result: a clean plate with no glyphs, at no extra geometry or material cost (6 faces per LOD).

## 4. Performance, LODs and memory (P0 7)

| LOD | r2 triangles | **r3 triangles** | Ratio | r2 / **r3** materials | r2 / **r3** draw calls | r3 vertices (unique / split upper bound) |
|---|---|---|---|---|---|---|
| LOD0 | 14,970 | **14,961** | — | 7 / **8** | 19 / **19** | 10,504 / 35,341 |
| LOD1 | 7,746 | **7,756** | 52 % | 7 / **8** | 19 / **19** | 5,665 / 20,262 |
| LOD2 | 3,527 | **3,546** | 24 % | 7 / **8** | 19 / **19** | 2,826 / 9,202 |
| LOD3 | 1,375 | **1,383** | 9 % | 5 / **6** | 13 / **13** | 1,230 / 3,551 |

- **Silhouette IoU vs LOD0:**

  | LOD | Side | Front | Top |
  |---|---|---|---|
  | LOD1 | 0.999 | 1.000 | 1.000 |
  | LOD2 | 0.994 | 0.998 | 0.997 |
  | LOD3 | 0.976 | 0.993 | 0.989 |

- **Max dimension drift:** 4.7 mm (r2: 6.3 mm).
- **Colliders:** 4 convex hulls (88 / 178 / 158 / 184 triangles).

- **Materials.**
  - +1 effective material per LOD, because the interior now uses its own instance. All four LODs stay **≤ 8** slots.
  - The glass instance replaces `TS_Glass` one-for-one, so it adds no slot.
- **Draw calls.** Unchanged versus r2. They are counted as (mesh × material) submeshes before Unity batching, so this is an estimate, not a profile.
- **Triangle budget.** Removing the hood dissolve cost about 630 LOD0 triangles. These were recovered without visible cost:
  - coarse dissolve of never-visible under-bumper faces (the surface stays closed);
  - top-panel dissolve at 0.5°;
  - arch lips at 20 segments (1.4 mm chord sag);
  - pillar liner at 0.16;
  - fog-lamp cups, exhaust, wipers, arch-liner arcs, tail-lamp bezel and steering-wheel rim slightly coarser.

### Texture memory — the 94.5 MB explained

The 94.5 MB reported in H1/r2 is **the set of images Blender binds, as uncompressed RGBA8 with no mip-maps**. It includes 32 MB of Blender-only maps (`TS_Atlas_Metallic`, `TS_Atlas_Roughness`), which Unity replaces with the single `TS_Atlas_MetallicSmoothness`. PNG file size is not GPU memory. The estimates below are arithmetic from dimensions, with mip chains at ×4/3. **They have not been profiled in Unity.**

| Set | Textures | Pixels | RGBA8 + mips | ASTC 4×4 + mips | ASTC 6×6 + mips |
|---|---|---|---|---|---|
| **Shared, loaded once for the whole fleet** | Atlas BaseColor, MetallicSmoothness, Normal (2048); Tire ×3 (1024×512); PaintFlake, Lights Base / Emission / ChannelID (256) | 14.4 M | 73.3 MB | 18.5 MB | 8.4 MB |
| **Sedan-specific** | Body Normal 2048, Body Normal LOD1 1024, AO/Grime 1024 | 6.3 M | 32.0 MB | 8.0 MB | 3.6 MB |

- `TS_Lights_ChannelID` must stay point-sampled and uncompressed, but it is tiny: 256 KB.
- Recommended: ASTC 6×6 for colour and masks, ASTC 5×5 or 4×4 for normal maps.
- Expected footprint: about 4–8 MB per sedan plus about 8–19 MB once for the whole fleet.
- **Mesh memory.** Upper bound at 48 B per split vertex (position, normal, tangent, UV) plus 16-bit indices:
  - LOD0: about 1.7 MB vertex buffer + 0.09 MB index buffer;
  - all four LODs: about 3.3 MB in total.
  - This is within 1 % of r2; geometry did not grow.

## 5. Validation, export, integrity (P0 8)

- All checks are in `reports/trafficsedanar3_validation.txt`. They cover:
  - hierarchy and pivots;
  - orientation and ground contact (body clearance 0.165 m);
  - budget and material slots (8 / 8 / 8 / 6);
  - silhouette and materials, with the instances declared;
  - all 7 light channels independent in one draw call;
  - textures (12 present, none missing) and UVs (atlas faces inside cells, paint UVs in 0–1);
  - topology and colliders;
  - renders, FBX re-import and shading screen.
- **Extra r3 checks** (scratch tools, numbers recorded here):
  - invalid-bake faces 1 / 5,075 (r2: 13 / 5,273);
  - folded master faces 2 / 58,112 (unchanged, not visible);
  - master normals: 219,669 skin loops re-shaded, 16,024 wall loops flat;
  - distant plate faces kept whole at LOD2/LOD3: 6 each.
- **Integrity before and after the build:**
  - the frozen environments, Hypercar, Zero Gap R, Titan GT (+r1), Vortex R (+r1) and Raven XR are byte-identical;
  - the Pulse EV blockout is unchanged;
  - the shared traffic library is unchanged;
  - the H1 and r2 deliverables are unchanged (see `reports/trafficsedanar3_integrity_check.md`).

## 6. Remaining honest shortcomings

1. **Not AAA.** The body is a clean procedural loft. It has no secondary surfacing: no door-side sculpting, real wheel-arch blisters or bumper sub-shapes. It reads as a generic, plain compact sedan, convincing at 7.5 / 22 / 60 m, but bland in close studio hero shots.
2. **Lower rear corner zebra.** It still shows closed contours from a low camera. The normal is now monotonic, with no kink, but the three-way blend (side / face / underside) is tighter than a production surface would be.
3. **Baked shut lines** are about 5.5 mm on a 2048 map. They read as fine dark lines, slightly soft in extreme close-ups. This is a texel-density limit.
4. **Game-mesh zebra** at extreme close range (60 mm lens, 0.7 m) shows 8-bit normal-map steps on the 3° dissolved door sides. This is not visible in PBR at studio or gameplay distances. ASTC will requantize these maps anyway.
5. **Hood highlight in extreme close-up.** In the 50 mm headlamp close-up, the overhead-softbox reflection on the hood still has a slightly irregular edge, in r2 and in r3. Most of its shape is the designed hood crown, which the master shows too. The rest is the low-poly mesh plus normal map at grazing angles. It is not visible at front-¾ or gameplay distances.
6. **A-pillar liner.** It is light grey and lit directly by the overhead studio softbox through the windshield, so it reads as a flat pale shape in studio ¾ shots. It is correct shading of a coarse liner. It is less noticeable in daylight.
7. **LOD2 / LOD3.** Facets are visible if those LODs are forced at 7.5 m. At their real switch distances (§4 screen heights) they hold.
8. Two tiny folded faces remain on the master tail cap; neither is visible.
9. There is no licensed photographic reference comparison, and **no Unity runtime or performance testing**.

## 7. Deliverables

| # | Deliverable | Location (`Traffic_Sedan_A_r3/`) |
|---|---|---|
| 1 | H1-r3 Blender model | `blend/trafficsedanar3_02_body` … `_08_rig`, `_09_export_ready.blend` |
| 2 | Unity FBX | `exports/TrafficSedanA_complete_unity.fbx` (71 objects), `TrafficSedanA_LOD0_unity_test.fbx` (27) |
| 3 | Bakes | `textures/TS_SedanA_Body_Normal.png` (2048, 2× supersampled), `_Normal_LOD1.png` (1024), `_AO_Grime.png` |
| 4 | Before / after (r2 vs r3, identical cameras and lighting) | `previews/TrafficSedanA_sheet_r2_vs_r3_front_fender / _rear_quarter / _bumper_corners / _overall / _glass_interior.jpg`; raw frames in `previews/r2_compare/` |
| 5 | Quality checks | `…_sheet_qa_clay / _qa_wire / _qa_normal / _qa_clay_wire_details.jpg` (`previews/qa/`), `…_sheet_studio_1/2`, `…_sheet_daylight`, `…_sheet_closeups_wheel_glass_plate`, `…_sheet_closeups_bumpers_lamps` |
| 6 | Game camera (7.5 / 22 / 60 m) | `…_sheet_game_camera.jpg`, `previews/TrafficSedanA_game_*.png` |
| 7 | Zebra | `…_sheet_zebra_r2game_r3game_r3master.jpg` (10 views, both sides), `…_sheet_zebra_artifact_zones_r2_vs_r3.jpg`, `previews/zebra_master/`, `zebra_game/`, `zebra_diag/` |
| 8 | LOD lineup | `…_sheet_lod_comparison.jpg`, `previews/lod/` (studio and game, LOD0–3) |
| 9 | Reports | this report; `reports/trafficsedanar3_validation.txt`, `_geometry.json`, `_export_manifest.json`, `_integrity_check.md`, `TS_SedanA_build_log.json`, `trafficsedanar3_FREEZE_CANDIDATE.md` (candidate only) |
| 10 | UnityTransfer | `UnityTransfer/` (FBX, Textures + Shared, Reports, README with material-instance setup) |

All renders use Cycles, AgX Medium High Contrast and real exposure, with no bloom, glare, vignette or post-processing. Scripts: `scripts/ts_sedan_a_r3.py` (new); `ts_render.py`, `ts_validate.py` and `ts_package.py` were extended (backward compatible).
