# Traffic_Sedan_A — Phase H1 prototype report

**Status: COMPLETE AS A PROTOTYPE, AWAITING YOUR VISUAL AND TECHNICAL REVIEW** (2026-10-08). None of the other eight vehicles has been started; Pulse EV remains postponed and untouched.

**My visual verdict: NOT YET at the target realism bar.** It is clearly better than the procedural player cars, but I recommend one more design pass before Sedan A becomes the fleet baseline (section 5).

## 1. Technical result

| Gate | Result |
|---|---|
| Validation (`reports/trafficsedana_validation.txt`) | **18 checks + shading screen S1 on all LODs: 0 errors, 0 warnings** |
| FBX clean re-import | 2 of 2 files pass (27 and 71 objects). Bounds deviate by 2.7e-7 m and pivots by 1.5e-7 m. Checked in raw Unity space: nose +Z, up +Y, FL on −X |
| Protected files | **PASS**, before and after: baseline 1,554 files, 7 frozen releases (587 files) and the Pulse EV blockout are unchanged |
| Dimensions | 4.64 m long, 1.80 m body width (2.06 m with mirrors), 1.47 m high, 2.70 m wheelbase, track 1.56 m, 205/55 R16 tires, 0.167 m body clearance. All within the compact-sedan class range |

| LOD | Triangles | Ratio | Materials | Draw calls |
|---|---|---|---|---|
| LOD0 | **14,721** | — | 7 | 21 |
| LOD1 | 7,813 | 53 % | 7 | 21 |
| LOD2 | 3,524 | 24 % | 7 | 20 |
| LOD3 | 1,399 | 10 % | 5 | 14 |

- **Silhouette:** IoU against LOD0 is ≥ 0.983 at every LOD; dimension drift is 4.6 mm.
- **Colliders:** 4 convex hulls covering the body.
- **CenterOfMass:** (0, −0.22, 0.52), giving a front-engine weight bias.
- **Shading screen:** worst mesh is 0.31 % torn normals (Interior_LOD3); the LOD comparison renders show no tears.
- **No Unity runtime or performance testing was done.**

## 2. What changed in the method (Phase H0 → H1)

- **High-poly to low-poly bake.**
  - The master body has real 5.8 mm panel-gap grooves (hood, trunk, four doors, fuel door) and recessed openings.
  - The 5.7k-triangle game body is a clean quad cage with a unique unwrap and a **baked tangent-space normal map** (2048 at LOD0, 1024 at LOD1).
  - It also has a baked **AO and road-grime mask**.
  - Panel gaps come from the normal map, not from triangles.
- **Real depth.**
  - Headlamps have a housing, two chrome reflector bowls with emitters, an LED light guide, an amber indicator and a clear lens seated over the cut.
  - Tail lamps have a reflector field, light guide, brake block, indicator and red lens.
  - The grille has a chrome frame, gloss slats and a honeycomb back plate in shadow.
  - Fog lamps, reverse lamps and reflectors have depth too.
- **Glass.** It is inset 6 mm with rubber and gloss-black seals and a continuous black frit band, and it is tinted and see-through (alpha 0.35 for Unity). Through it you can see seats, headrests, the rear bench, dash, wheel, door cards and the pillar liner.
- **Scale cues.** Mirrors with mirror glass, door handles in recesses, wipers, fictional license plates, a badge, antenna fin, side repeaters, an exhaust tip, an underbody tray and arch liners.
- **Wheels.** A real 55-series tire profile, a tread and sidewall normal map with mild wear, a 16-inch 10-spoke alloy with a dished face, 5 lug nuts, centre cap, 280 mm disc and caliper.
- **Shared fleet library.**
  - 7 material slots: paint instance, 2048 atlas with textured cells, tire, glass, two lenses, and **one emissive lights material whose channel comes from a mask**. This gives 7 independent channels in one draw call.
  - Six paint variants are material instances only.
  - The same scripts serve all nine vehicles: `ts_lib`, `ts_render`, `ts_zebra`, `ts_export`, `ts_validate`, `ts_package`.

## 3. Evidence (all in `previews/`)

| Sheet | Contents |
|---|---|
| `TrafficSedanA_sheet_studio_1/2.jpg` | Neutral Cycles studio: front ¾, rear ¾, front, rear, side, top, wheel, interior |
| `…_sheet_details.jpg` | Front and rear detail, wheel, interior |
| `…_sheet_daylight.jpg` | Physical sky and sun on the frozen P0 road |
| `…_sheet_game_camera.jpg` | Follow camera at 7.5 m, 22 m and 60 m |
| `…_sheet_lod_comparison.jpg` | LOD0–3 with matching cameras (studio front ¾, side, game close and normal) |
| `…_sheet_lights_off_on.jpg` | Lamps off compared with all channels on |
| `…_sheet_paint_variants_a/b.jpg` | White, silver, graphite, black, red, blue |
| `…_sheet_zebra_master_vs_game.jpg` | Zebra on the high-res master compared with the baked game mesh, both sides |
| `…_sheet_realism_vs_h0_audit.jpg` | Vortex R (H0 audit) compared with Sedan A, same studio |

No licensed photographic references are available offline, so the realism comparison uses the class dimensions and these renders. Photographic side-by-sides should come from your licensed sources.

## 4. What works

- **Proportions** read as a real compact sedan, especially in the daylight and game-camera views.
- **Paint** reads as clear-coat automotive paint, not plastic, with sharp coat highlights. White, silver and graphite are all convincing.
- **Glass** reads as tinted glass with a visible cabin, not black paint.
- **Lamps** read as constructed units, lit and unlit.
- **Tires** show tread and shoulder.
- **LOD0 to LOD2** transitions are not noticeable at gameplay distances.

## 5. Honest shortfalls (why I would not yet use it as the fleet baseline)

1. **Body form is still too soft.** The tail is a rounded "soap bar" with no distinct bumper, trunk-lid plane or rear face. Real sedans have a crisp trunk edge, a vertical rear face and a separate bumper with a shadow line. The front bumper corners are also too rounded. Fix: rebuild the end sections with dedicated bumper cages, not more creases on the shared loft.
2. **Faceted rear wheel arches.** The arch cut shows facets and a ragged edge in close studio views; it needs a proper flared arch lip with thickness.
3. **Jagged lens and plate edges.** The tail-lamp lens and plate recess edges are jagged where the cut meets the curved skin. They need cleaner cutter outlines, or lens and recess geometry that owns the edge.
4. **Wheel design is simple.** The 10-spoke reads as a generic 5-spoke at distance; a better spoke shape is needed, or a model of the spokes baked into the atlas.
5. **Distracting reflection in the side glass.** In the studio interior view, the light-grey patch behind the front side glass is the side softbox reflecting in the glass. Rendering is correct, but it hides the cabin; the interior close-up should be re-shot with a different camera angle.
6. **LOD3** wheels are visibly octagonal in close-up. That is acceptable at LOD3 distances, though, as the game-far render shows.
7. **Zebra.** The master body is smooth, but the tail-corner bands bunch where the soft tail turns. This is the same root cause as item 1.

**Recommended next step (your decision):** an **H1-r2 revision of Sedan A** covering items 1–3. That means rebuilt front and rear bumper and trunk volumes, flared arch lips, and clean lamp and plate edges. It reuses everything else unchanged (pipeline, materials, wheels, interior, rig, validation). Re-review after that, then roll the approved quality out to the other eight vehicles.

## 6. Files

- `blend/` contains checkpoints `trafficsedana_02_body` … `_08_rig` and `_09_export_ready`.
- `exports/` contains the 2 FBX files.
- `textures/` contains the body normal (LOD0, LOD1) and the AO/grime map.
- `../shared/textures/` contains the fleet library.
- `reports/` contains:
  - validation, geometry, export manifest and build log;
  - `trafficsedana_integrity_check.md`;
  - `trafficsedana_FREEZE_CANDIDATE.md` (SHA-1 of 25 files);
  - this report.
- `UnityTransfer/` contains FBX, Textures (+Shared), Reports and README with full material and light-channel setup.
- `../reports/TRAFFIC_REALISM_STANDARDS.md` is the H0 standard.
