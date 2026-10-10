# Phase D — Vortex R: final production QA report

**Status: APPROVED and FROZEN — Phase D technical release** (2026-10-08). Any later change requires a separate revision folder; nothing here is edited. Remaining limitations are recorded in section 6 and the Titan GT cross-check in section 5 (repaired separately in `vehicles/C_TitanGT_r1/`).

**Base:** the approved blockout `blend/vortexr_01_blockout.blend`. It is byte-identical after this work (SHA-1 `fd2cff0f15bbd1dfc31280c7b95c6260b3179e67`).

## 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/VX_validation.txt`) | **18 checks: 0 errors, 0 warnings** |
| FBX clean re-import | 2 of 2 files pass. Names, hierarchy, triangles, materials, UVs and textures are preserved. Bounds deviate by 3.0e-7 m and pivots by 1.5e-7 m. Checked in raw Unity space: nose +Z, up +Y, FL on −X |
| Protected files | **PASS** (`va_integrity.py`: 0 changed, 0 added, 0 missing): 1,554 baseline files (frozen P0–P3, Hypercar), 70 frozen Zero Gap R files, 81 frozen Titan GT files, and the approved Vortex R blockout |
| Checkpoints | `vortexr_02_body_panels` … `_09_export_ready`, each written once. The official build matches the validated scratch run to within a few hundred bytes per file |

## 2. Numbers

| Metric | Vortex R | Target |
|---|---|---|
| LOD0 triangles | **73,665** (blockout: 112,806, unoptimised) | 60–90 k (ceiling 120 k) |
| LOD1 | **34,060 (46 %)** | 40–50 % |
| LOD2 | **15,026 (20 %)** | 15–25 % |
| LOD3 | **6,146 (8 %)** | 5–10 % |
| Render objects per LOD | 22 / 22 / 22 / 13 | — |
| Materials | 15 (8 surface + 7 light channels) at every LOD | ≤ 16 |
| Textures | 7 PNGs: 0.13 MB on disk, 10.8 MB as uncompressed RGBA; 1 UV channel | — |
| Silhouette IoU against LOD0 (side / front / top) | LOD1 0.9999 / 0.9999 / 0.9999; LOD2 0.9987 / 0.994 / 0.9999; LOD3 0.9879 / 0.9884 / 0.9956 | ≥ .97 / .95 / .90 |
| LOD dimension drift | 0.8 mm max | ≤ 10 mm |
| Dimensions (L × W × H) | 4.58 × 2.27 × 1.275 m, mirrors and wing endplates included; body 2.09 m wide | — |
| Wheelbase / track | 2.72 m; 1.72 m front / 1.70 m rear | — |
| Ground clearance | 0.100 m (body, splitter, diffuser) | ≥ 0.10 m |

## 3. What was built (blockout → production)

### Body
- Built from the approved blockout cage, faired along its length and around each section. Character lines are locked.
- Subdivision uses a fender-crest crease that fades out at the nose and tail.
- Skin normals come from a level-4 smooth reference, so the highlights stay continuous across the boolean cuts.
- Panel gaps are cut as real grooves for the hood, doors, engine deck and front clam.
- Zebra QA ran after each major operation (`previews/zebra_VX_final/`, compared with Titan GT in `VX_zebra_compare_titangt_vortexr_final.jpg`).

### Front
- Recessed twin-blade intakes with carbon vanes and dark back walls.
- Central lower intake with mesh.
- Carbon splitter with endplates and dive planes.
- Two slatted hood vents.

### Headlights
- A recessed housing per side.
- A boomerang DRL blade with a down-hook, three LED projector modules, an amber indicator and a clear lens.

### Side
- A deep recessed side intake behind each door, with an inner wall and carbon floor.
- A side blade and a carbon rocker.
- Arch liners in every wheel arch.
- Mirrors on stalks.

### Rear
- Recessed tail-light housings with three raked LED slashes per side, a brake bar, indicator and reverse lamps, and a red lens.
- A thin full-width tail thread.
- A lattice rear mesh panel, a central twin oval exhaust and a full-width diffuser whose strakes follow the floor line.
- Engine-deck louvres.

### Wing
- An airfoil main plane on swan-neck pylons, with endplates.
- The **third brake light** sits on the wing trailing edge, on `VX_LED_Brake`.

### Tail corner
- The pinch reported at blockout is corrected: the crease fades out between 1.40 and 1.92 m, and normals come from the smooth reference.
- See `zebra_tail_corner.png`: the bands now flow continuously around the corner.

### Wheels
- Forged 10-spoke rims with a machined lip, and LOD-scaled segment counts.
- Drilled rotors and **acid-green calipers**.

### Interior
- Track cockpit with carbon tub, bucket seats with acid-green harnesses, an alcantara wheel with a green top marker, a display, and the roll hoop.
- LHD: the driver sits on +X.

### Materials
- Satin deep-violet paint: base (0.075, 0.028, 0.155), metallic 0.80, roughness 0.36, clear coat 0.35.
- The paint is untextured, so the colour can be swapped in Unity.
- Tail lights read **red in daylight**: no pink cast, unlike Zero Gap R's PB-1.

### Rig
- `Car_Root` → `LOD0_Root` … `LOD3_Root`, with a `SteerPivot_FL/FR` on each front wheel.
- `WheelColliderRef_FL/FR/RL/RR`, and `CenterOfMass` at (0, 0.25, 0.38).
- **5 convex colliders:** Front 184, Body 168, Cabin 166, Rear 142 and Wing 14 triangles. All are closed and outward-facing, and together they cover the body to within 0.020 m.
- Pivot tests pass: ±30° roll, +25° steer, and calipers steer but do not roll.

### LODs
- LOD1–3 are decimated from a copy of the body without panel-gap grooves, then re-normalled from the smooth reference.
- This avoids the smeared normals and slivers that decimating the grooves produced (section 5).
- LOD3 drops the brake hardware and the steering wheel; these are hidden behind the spokes and glass.

## 4. Fixes made during production

| Found in | Problem | Fix |
|---|---|---|
| Zebra, crease | Sawtooth highlight along the fender crest | Normal probe moved 8 % toward the face centre, so it picks the correct side of the crease |
| Zebra, tail corner | Crumpled highlights | Smooth normals from the KD-tree; crease fade 1.40–1.92 m |
| LOD lineup | LOD1 grooves smeared the normals; LOD2/3 showed slivers | LODs built from the groove-free body + smooth-reference normals |
| Side view | Diffuser fins hung below the floor line | Fin bottom clamped to the floor curve |
| Validation 6 | Clearance 0.096 m | Cage floor raised by 12 mm, giving 0.100 m |
| Validation 15 | Collider cover 0.153 m at the wing, then 0.070 m at the right mirror | Added `Collision_Wing`; hulls keep the 6 extreme points |
| Titan zebra reference | The reference render was uniformly grey | The zebra script renders LOD0 only |
| Validation report text | Labels left over from Zero Gap R ("source: 88 images", "mirror corrected") | Corrected to Vortex R wording and re-run (still 18 / 18) |

## 5. Cross-check: frozen Titan GT LOD1 (read-only, nothing changed)

The groove-smearing found on Vortex R's LOD1 led to a check of the two frozen vehicles.
- **Method:** each frozen `_09_export_ready.blend` was opened without saving, and LOD0 and LOD1 were rendered into a scratch folder. The SHA-1 of each file was checked before and after: unchanged. `va_integrity` reports PASS.
- **Titan GT: defect confirmed.** LOD1 shows jagged, chrome-like tears along every panel gap: hood, doors, deck lid and rocker. LOD0 is clean. Its validation passed because no check renders LOD1 close-up.
  - Evidence: `previews/xcheck_TitanGT_LOD1/` (LOD0 and LOD1 from the front, side and rear).
- **Zero Gap R: not affected.** Its panels are separate meshes rather than grooves cut into one shell, and LOD1 is clean.
- **Proposed fix (needs your approval, because Titan GT is frozen):** a revision folder `C_TitanGT_r1/` that rebuilds only LOD1–3 with the Vortex R method (groove-free body + smooth-reference normals). LOD0, the rig and the materials stay the same. The frozen `C_TitanGT/` would not be touched.
- **Gameplay impact:** LOD1 appears at mid distance, so the tears would likely be visible in-game.

## 6. Known limitations

These are honest notes for your visual review.

- **Doors** are panel-gap grooves in the body, not separate objects, so they cannot be opened.
- **Hood zebra:** the concentric bands around the hood vents and canopy base come from real double curvature; they are not waviness. The door and side bands run straight.
- **Interior** reads well through the tinted canopy but is not built for hero close-ups.
- **Light materials at LOD3** stay separate: 15 materials at every LOD, the same decision as Zero Gap R and Titan GT.
- **Tail and brake emission** need tuning in Unity with bloom. Suggested: tail at ×7 and brake at ×1.5 resting, raised to about ×8 when braking.
- **Texture memory:** 10.8 MB is the uncompressed RGBA figure. **No Unity runtime or performance testing was done**; Unity is not installed.

## 7. Deliverables

| Path | Contents |
|---|---|
| `previews/VX_compare_4cars.jpg` | Hypercar, Zero Gap R, Titan GT and Vortex R with identical cameras (7 views each) |
| `previews/VX_compare_blockout_final.jpg` | Approved blockout compared with final |
| `previews/VX_zebra_compare_titangt_vortexr_final.jpg` + `zebra_VX_final/` | Zebra: hood, roof, deck, door, full side, tail corner |
| `previews/VX_lod_lineup.png` | LOD0–LOD3 side by side |
| `previews/VX_details_front_side.jpg`, `VX_details_rear_wheel_interior.jpg` | Close-up sheets |
| `previews/VX_*.png` | 18 renders: 8 views (front, rear, left, right, ¾ front and rear, top, chase on the frozen P0 road), interior, wheel, 7 close-ups (front, hood, intake, door, canopy, tail, wing) and the LOD lineup |
| `previews/VX_blockout_*` + `zebra_VX/` | The blockout-stage renders, kept for reference |
| `blend/` | Checkpoints 01 (approved blockout) to 09 (export ready) |
| `exports/` | `VortexR_complete_unity.fbx` (103 objects) and `VortexR_LOD0_unity_test.fbx` (37 objects) |
| `textures/` | 8 PNGs (7 referenced + MetallicSmoothness for Unity) |
| `reports/` | `VX_validation.txt`, `VX_geometry.json`, `VX_export_manifest.json`, `VX_build_log.json`, `VX_source_integrity_check.md`, `VX_FREEZE_CANDIDATE.md` (SHA-1 of 19 deliverables), and this report |
| `UnityTransfer/` | FBX, Textures, Reports, `README/VX_UNITY_IMPORT_NOTES.md` |
| `scripts/` | `vx_lib`, `vx_blockout`, `vx_build`, `vx_export`, `vx_render`, `vx_zebra`, `vx_sheet`, `vx_validate`, `vx_package` |
