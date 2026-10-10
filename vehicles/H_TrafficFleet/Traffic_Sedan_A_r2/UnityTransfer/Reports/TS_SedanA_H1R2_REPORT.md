# Traffic_Sedan_A — H1-r2 realism revision report

**Status: COMPLETE, AWAITING YOUR VISUAL APPROVAL** (2026-10-08).
- r2 is **not** frozen and is **not** the fleet benchmark.
- No other traffic vehicle has been started.
- Pulse EV remains postponed and untouched.
- The H1 deliverables in `../Traffic_Sedan_A/` are preserved: all 25 candidate-manifest files are unchanged.

**My visual verdict: a clear step up from H1, and the main H1 rejection causes are fixed. It is still not AAA, and some issues remain (section 6).** I would accept it as a realistic traffic car at gameplay distance. The front lower corners and the shut-line ends are worth one more short pass if you want it to serve as the fleet benchmark.

## 1. Technical result

| Gate | Result |
|---|---|
| Validation (`trafficsedanar2_validation.txt`) | **18 checks + shading screen S1 on every LOD: 0 errors, 0 warnings** |
| FBX re-import | Both files pass: `complete` has 71 objects, `LOD0_unity_test` has 27. Axis-bake residual is 1.5e-7. In Unity space the nose is +Z, up is +Y and FL is on −X |
| Protected files | Before and after, all of these **PASS / are unchanged**: <ul><li>frozen check;</li><li>baseline integrity (0 changed, 0 missing, 0 new);</li><li>H1 25/25;</li><li>shared library textures 12/12;</li><li>Pulse EV `18af7277976a`.</li></ul> |
| Dimension drift across LODs | 6.3 mm maximum (LOD3 length) |
| Colliders | 4 convex hulls (84 / 168 / 178 / 176 triangles), 0.005 m cover |
| Unity runtime and performance | **Not tested.** Unity is not installed, by design |

## 2. LOD and draw-call report

| LOD | H1 triangles | **r2 triangles** | Ratio | Materials | H1 draw calls | **r2 draw calls** |
|---|---|---|---|---|---|---|
| LOD0 | 14,721 | **14,970** | — | 7 | 21 | **19** |
| LOD1 | 7,813 | **7,746** | 52 % | 7 | 21 | **19** |
| LOD2 | 3,524 | **3,527** | 24 % | 7 | 20 | **19** |
| LOD3 | 1,399 | **1,375** | 9 % | 5 | 14 | **13** |

- **All targets are met:** LOD0 10–15k, LOD1 40–55 %, LOD2 15–25 %, LOD3 5–10 %, and ≤ 8 material slots.
- **Draw calls are counted as (mesh, material) submeshes before Unity batching.** This is an estimate, not a profiled number.
  - The drop from 21 to 19 comes from moving the atlas faces of Lights and Glass into the Trim mesh (`move_atlas`), which removes 2 submeshes.
  - Going further would mean merging meshes with different roles: lights need their own mask material and glass must stay transparent. I did not do that.
  - Material count is not the same as draw calls. Unity SRP batching and the wheel instancing setup will decide the real cost.
- **Silhouette IoU against LOD0:**

  | LOD | Side | Front | Top |
  |---|---|---|---|
  | LOD1 | 0.999 | 1.000 | 1.000 |
  | LOD2 | 0.993 | 0.998 | 0.995 |
  | LOD3 | 0.971 | 0.980 | 0.993 |

### LOD0 geometry changes vs H1 (triangles)

| Part | H1 | r2 | Why |
|---|---|---|---|
| Body | 5,677 | 6,160 | Dedicated front and rear end surfaces, trunk lid edge, flared arch lips |
| Trim | 2,680 | 3,726 | Bumper shut lines and valance, plate and lamp frames, plus the atlas faces moved in from Lights and Glass |
| Lights | 1,066 | 632 | The atlas faces moved to Trim; the lamp units themselves were rebuilt with clean rims |
| Glass | 504 | 266 | 3° planar dissolve; the frit band moved to Trim |
| Interior | 1,258 | 898 | Hidden boxes unbevelled, coarser liner |
| Wheels (4 assemblies) | 3,328 | 3,080 | New twin-spoke design: dished face, machined edge, 9-point tire profile; lug caps removed |

### Memory

- **Textures:** 94.5 MB, unchanged from H1. Same resolutions: 2048 body normal, 1024 LOD1 normal, AO/grime map, and the shared library.
- **Shared library:** its 12 PNGs were **not** modified.
- **Mesh memory:** the vertex count difference against H1 is below 2 %.
- **Folder size:** 139 MB for the r2 folder, including the blend checkpoints and renders.

## 3. What was done (P0 and P1)

**Rear (the H1 "soap bar")**
- The tail is now built as a dedicated end surface, not creases on the old loft. It is a designed face with its own plan curvature, and its corner radius varies around the outline:
  - 25 mm at the trunk-lid edge;
  - 100 mm at the side corners;
  - 140 mm at the bottom.
- The trunk-lid plane ends in a crisp edge, and the rear face below it is vertical.
- The bumper reads as a separate part: a shut line runs from the arch to the tail-lamp base, with a ledge below it.
- Below that are the plate recess with a frame, the valance roll-under and integrated tail-lamp housings.
- The trunk gap sits behind the crisp edge at y 2.255, so the lid edge has no ripple.

**Front**
- The fascia has the same end-surface treatment. A defined hood-to-bumper edge (28 mm radius) and real bumper volume give a normal modern-sedan face, not a supercar one.
- The headlamps are seated against the fender. The bumper split line runs from the headlamp to the arch.
- Grille and lower intake are recessed with frames.

**Rear arches**
- A real lip with thickness and a smooth subtle flare: 22 segments, with a flat-baked normal so there is no faceting.
- Arch liners, and clearance that matches H1.

**Lamp and plate edges**
- Cutter outlines were redrawn inside the body, so they no longer cross the side corner.
- Frame bands (12 mm on lamps, 14 mm on plates) own the edge, so there are no jagged cuts.
- Lens depth is preserved. Lamps were checked both off and on.
- Plates fill their atlas cell per island, so the front and rear glyphs are no longer clipped. This was fixed in `ts_lib.atlas_uvs` and does not change the textures.

**Wheels**
- Twin curved spokes with a 48 mm dish.
- Machined silver faces with dark spoke sides, centre cap and hub.
- Brake disc and caliper behind the spokes.
- A 9-point tire profile with a rounded shoulder.
- The size is unchanged (205/55 R16).

**Materials**
- Paint, glass, lenses and lights are unchanged; they are already shared library instances.
- The interior was re-shot with fill lights and a new camera, so the cabin is clearly visible.

**Construction fixes made along the way**
- Folded cap faces dropped from 1,126 to 2. Cap rings are now built by scaling toward the face centre, not by inward offset.
- Planar dissolve is held at 3°; 5.5° made the game-mesh zebra blocky.
- LOD3 extremes are protected with an inverted vertex group (dimension drift went from 10.2 mm to 6.3 mm).
- The thin cabin liner is dropped at LOD2 and LOD3; it spiked at those LODs.
- Body LOD UVs are clamped to 0–1.

## 4. Evidence (all in `previews/`, same cameras and lighting as H1)

| Sheet | Contents |
|---|---|
| `TrafficSedanA_sheet_H1_vs_r2_overall.jpg` | H1 compared with r2: front ¾, rear ¾, side |
| `…_H1_vs_r2_rear.jpg` | Rear, rear ¾, rear detail |
| `…_H1_vs_r2_front_arch.jpg` | Front, front detail, arch |
| `…_H1_vs_r2_wheel_interior_day_game.jpg` | Wheel, interior, daylight, game camera |
| `…_closeups_bumpers_lamps.jpg` | Front and rear bumper corners, front and rear lamps |
| `…_closeups_plate_arch_wheel_interior.jpg` | Rear plate, rear arch, wheel, interior |
| `…_orthographic.jpg` | Front, rear and side orthographic views |
| `…_studio_1/2.jpg`, `…_daylight.jpg` | Studio set, and physical sky on the frozen P0 road (read-only link) |
| `…_game_camera.jpg` | Chase camera at 7.5, 22 and 60 m |
| `…_lod_comparison.jpg` | LOD0–3 lineup with matching cameras |
| `…_lights_off_on.jpg` | Front and rear lamps, off and on |
| `…_zebra_master_vs_game.jpg` | Zebra on the master compared with the game mesh, both sides (`zebra_master/`, `zebra_game/`) |
| `…_paint_variants_a/b.jpg` | Six paint instances |

No licensed photographic references are available offline. Comparison against real cars should be done with your own sources.

## 5. Rejection-rule check

| Rule | r2 |
|---|---|
| Rear still a soap bar | **Fixed.** It has a trunk edge, a vertical face and a separate bumper |
| Soft bumper corners | **Partly fixed.** The rear upper corners are crisp. The **front lower corners are still slightly soft**, and the rear-quarter-to-bumper corner is somewhat round |
| Faceted arches | **Fixed** |
| Jagged lamp and plate edges | **Fixed** at LOD0 and LOD1 |
| Plastic paint | Not plastic: it shows a clear-coat highlight (unchanged from H1) |
| Toy-like wheels | **Improved.** It reads as a real twin-spoke alloy |
| Opaque windows | Not opaque: the cabin is visible |
| Broken transitions | Clean, except at the groove ends (section 6, item 1) |
| Wavy reflections | The master is smooth. The game mesh is mildly blockier in zebra (item 3); this is not visible in the paint renders |
| Unbelievable at gameplay distance | It is believable at 7.5, 22 and 60 m |

## 6. Remaining issues (honest)

1. **Squiggle highlights at the ends of the shut-line grooves.** These appear on the rear quarter near the arch and at the front fascia split next to the headlamp. They are visible in close studio views, not in game views.
2. **The LOD2 and LOD3 plate texture is garbled** in close game views, because the decimated UVs compress the plate cell. Its glyphs cannot be read at LOD2/3 distances anyway.
3. **The game-mesh zebra is still somewhat blockier than the master** in the tail corners. This is a limit of baking onto a 6k-triangle cage.
4. **The interior seats look crumpled.** The shared fabric weave normal is too strong at this scale. Fixing it means changing the shared library, which I did not touch.
5. **The front lower bumper corners are slightly soft** (see section 5).
6. **2 tiny folded faces remain** on the master tail cap. There are 13 bad bake faces out of 5,273, and none of them is visible.
7. **No photographic reference comparison** and **no Unity runtime test.**

## 7. Deliverables

| # | Deliverable | Location |
|---|---|---|
| 1 | H1-r2 Blender model | `blend/trafficsedanar2_02_body` … `_08_rig`, `_09_export_ready.blend` |
| 2 | FBX files | `exports/TrafficSedanA_complete_unity.fbx`, `TrafficSedanA_LOD0_unity_test.fbx` |
| 3 | Textures and bakes | `textures/` (normal map for LOD0 and LOD1, AO/grime), plus the unchanged `../shared/textures/` |
| 4 | Before/after sheets | `previews/…_sheet_H1_vs_r2_*.jpg`, `previews/h1_compare/` |
| 5 | Studio and daylight renders | `previews/` and its sheets |
| 6 | Game-camera screenshots | `previews/game_*`, `…_sheet_game_camera.jpg` |
| 7 | Zebra reports | `previews/zebra_master/`, `zebra_game/`, and the zebra sheet |
| 8 | LOD and draw-call report | Section 2 of this report, and `reports/trafficsedanar2_geometry.json` |
| 9 | Technical QA | This report, plus the following in `reports/`: <ul><li>`trafficsedanar2_validation.txt`</li><li>`_export_manifest.json`</li><li>`_integrity_check.md`</li><li>`TS_SedanA_build_log.json`</li></ul> |
| 10 | UnityTransfer | `UnityTransfer/`: FBX, Textures (+Shared), Reports and README with import notes |

`reports/trafficsedanar2_FREEZE_CANDIDATE.md` lists the SHA-1 of every r2 deliverable. It is a candidate only, and will be frozen once you approve it.
