# Phase B — Zero Gap R remaster: technical QA report

**Status: APPROVED and FROZEN — Phase B technical release** (2026-10-08). Any later change requires a separate revision folder; nothing here is edited.

**Source.** The source was `racing_car_09_unity_export_ready.blend`, opened read-only. It is byte-identical after the work, and a read-only copy sits in `source_import/`.

## 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/ZG_validation.txt`) | **18 checks: 0 errors, 0 warnings** |
| FBX clean re-import | 2 of 2 files pass. Names, hierarchy, triangles, materials, UVs and texture paths are preserved. Bounds deviate by 3e-7 m and pivots by 1.5e-7 m. Checked both in Blender space and in raw Unity space (nose +Z, up +Y, FL on −X) |
| Protected files | **PASS**: 1,554 files byte-identical to the Phase A baseline (frozen P0–P3, Hypercar, racing_car_00…09), and nothing was added outside `vehicles/` |
| Checkpoints | `zerogapr_01_intake` … `_09_export_ready`. Each was written once, none was overwritten. One earlier official set was superseded and **moved** to the scratchpad, not overwritten, after LOD2/3 shading was fixed |

## 2. Before → after

| Metric | Source (racing_car_09) | Zero Gap R | Target |
|---|---|---|---|
| LOD0 triangles | 176,152 | **89,681** | 60–90 k (ceiling 120 k) |
| LOD1 / LOD2 / LOD3 | 99,084 / 44,985 / 16,386 | **44,794 (50 %) / 20,372 (23 %) / 6,513 (7 %)** | 40–50 % / 15–25 % / 5–10 % |
| Render objects per LOD | 642 / 452 / 248 / 199 | **24 / 24 / 24 / 15** | — |
| Materials | 27 (LOD0) | **15** (8 surface + 7 light channels) | — |
| Textures | 88 images, 221 MB, 3 UV channels, custom shader required | **7 PNGs, 0.8 MB on disk, 16.8 MB RGBA in memory, 1 UV channel** | — |
| Left / right | FL / RL on −X (mirrored) | **FL / RL on +X (project convention)**, LHD driver on +X | — |
| LOD0 topology | 366 zero-area faces, 183 duplicate vertices | **0 / 0**, no duplicate faces, consistent winding | — |
| Light channels | Tail and brake shared one emissive; no reverse; indicators not split | **DRL, Headlamp, Tail, Brake, Indicator_L, Indicator_R, Reverse**, each its own material | — |
| Unity export | none | `ZeroGapR_complete_unity.fbx` (110 objects) + `ZeroGapR_LOD0_unity_test.fbx` | — |

## 3. Defects from the discovery report — how each was fixed

1. **Left/right convention.** True X-mirror of all geometry. Wheel, door, indicator and steering labels now match the project convention. Tires are rotated 180° instead of mirrored, so the sidewall text stays readable.
2. **Front fascia** (no headlight units, boxy grille and bumper):
   - The old bumper, intakes, ducts and grille plate were removed. A new fascia skin is a Coons patch closing the body opening; its top edge tucks 4 mm behind the hood lip to form a shut line.
   - Three rounded, recessed intakes (central plus two sides) have gloss-black bezels, depth walls and dark back plates. The side intakes have carbon vanes, and the source hex grille sits recessed in the central intake.
   - An LED DRL blade runs along the lip, with an amber indicator line above each side intake.
   - The existing projector headlight units are kept and lit on the new Headlamp and DRL channels.
3. **Splitter.** Rebuilt as a slim carbon blade 25 mm proud of the chin (the old one overhung by about 60 mm), with endplates. The front overhang went from 2.29 m to 2.23 m.
4. **Tail lights.** The chrome-strip lights were removed. New units have a gloss-black housing, parallel red LED tail strips, separate brake segments, amber indicators (left and right), reverse lights, a smoked red outer lens with side walls, and a full-width signature bar.
5. **Exhaust.** The tips no longer pierce the side of the bumper. They exit through a recessed full-width vent band (two carbon slats), with double-wall chrome tips and dark inner sleeves.
6. **Diffuser.** The rear edge sits on the fascia chin and the front edge inside the floor tray. Four fins and two side plates stand on the diffuser surface, so it reads as one attached unit.
7. **Glass, roof tubes and A-pillars.**
   - The glass is now one thin dark-tinted sheet (alpha 0.42), with no frosted look.
   - The A-pillars, roof rails, B-pillars and rear pillars are gloss black, so they read as the glass frame rather than an exposed roll cage.
8. **Wavy reflections.**
   - The paint panels (body, hood, roof, engine cover, doors) were rebuilt from the source's own clean master subdivision cages: level 0 plus mirror plus panel thickness.
   - This removes the zig-zag highlights of the old LOD0, as seen in the before/after belt and hood close-ups.
9. **Degenerate topology.** Duplicate vertices were merged and degenerate faces dissolved. Coincident faces and loose vertices are removed after every reduction.
10. **Object and material count.** Merged per LOD into Body, Door_L, Door_R, Trim, Lights, Glass, Interior and SteeringWheel, plus per-wheel Wheel, Tire, BrakeDisc and Caliper. Opaque flat parts share one 256 px swatch palette (`ZG_Palette`, a single draw call).
11. **Light channels.** Seven independent materials, validated by position: front versus rear, and the left indicator on +X.
12. **Texture memory and UVs.**
    - 221 MB became 0.8 MB on disk, with a single UV channel.
    - Paint is an untextured clear coat, so the colour is swappable in Unity.
    - The tire keeps its sidewall-lettering atlas at 1K, and carbon uses world-scaled box UVs.
13. **Export configuration.** Uses the Hypercar method (in-memory axis bake, residual 1.5e-7) instead of the old `FBX_SCALE_UNITS` notes.

## 4. Kept from the source, as instructed

- **Proportions:** 4.46 × 2.01 × 1.20 m, wheelbase 2.70 m, track 1.65 / 1.67 m.
- **Running gear:** the wheel models (multi-spoke rims), tires, slotted brake discs and yellow calipers, at the original source LOD levels.
- **Body features:** mirrors, door handles, side intakes, engine-cover louvres.
- **Interior:** seats, dashboard, steering wheel, console.
- **References:** the centre-of-mass position (0, 0.22, 0.37).

## 5. Unity rig

- `Car_Root` → `LOD0_Root` … `LOD3_Root`. Front wheels are parented as `SteerPivot_FL/FR` → `Wheel` → `Tire` + `BrakeDisc`, with the caliper on the SteerPivot.
- **Pivot tests (all pass):**
  - wheels roll ±30° about local X (hub centre within 2 mm);
  - front wheels steer ±25° and the wheel stays on the steering axis;
  - calipers steer but do not roll.
- **Colliders:** `Collision_Front / Body / Cabin / Rear` are convex, closed hulls of ≤ 200 tris each with no material. They cover the body within 6 cm.
- **References:** `WheelColliderRef_FL/FR/RL/RR` (with radius and width) and `CenterOfMass`.
- **Doors:** hinge pivots on the front edge. Opening was not animated or validated.
- The full import table is in `UnityTransfer/README/ZG_UNITY_IMPORT_NOTES.md`.

## 6. LODs

- **Silhouette IoU against LOD0** (side / front / top):

  | LOD | Side | Front | Top |
  |---|---|---|---|
  | LOD1 | 0.996 | 1.000 | 1.000 |
  | LOD2 | 0.973 | 0.993 | 0.998 |
  | LOD3 | 0.924 | 0.980 | 0.986 |

- **Dimensions** stay within 6.8 mm of LOD0.
- **Shading:** LOD0 and LOD1 carry LOD0's normals. LOD2 and LOD3 use their own smooth normals with hard edges at 38°, because transferred normals caused mottling at that reduction (found in the LOD lineup render and fixed).
- **LOD3** replaces the separate brake hardware with a 16-gon rotor disc inside each wheel.

## 7. Known limitations

These are honest notes for your visual review.

- **Exterior detail quality:**
  - The front fascia corners are flatter and squarer than the Hypercar's, because the new skin follows the body's existing opening edges and the body shell was preserved.
  - The hex grille is subtle at gameplay distance.
- **Lights in daylight:** the tail-light lens reads slightly pink in daylight Eevee renders. Brightness and emission are meant to be tuned in Unity with bloom.
- **Interior:** reduced from the source rather than rebuilt. It is fine through the dark glass, but not hero-close-up quality.
- **Light materials at LOD3:** they stay separate (15 materials at every LOD). Merging them into one masked emissive at LOD3 would save draw calls, but needs a Unity shader decision.
- **Texture memory:** 16.8 MB is the uncompressed RGBA figure; GPU-compressed formats in Unity will be much smaller. No Unity performance is claimed.

## 8. Open polish items (non-blocking)

- **PB-1:** the tail-light lens (`ZG_LensRed`) reads slightly pink in daylight renders. To be resolved in the final Unity material review (lens tint / alpha, `ZG_LED_Tail` intensity with bloom). No Blender change is planned.

## 9. Files

| Path | Contents |
|---|---|
| `blend/` | 9 checkpoints. Final source: `zerogapr_09_export_ready.blend` |
| `exports/` | 2 FBX files |
| `textures/` | 7 PNG files |
| `previews/` | 16 renders (front, rear, left, right, ¾ front and rear, top, interior, wheel, chase on the frozen P0 road, front / rear / side close-ups, belt and hood zooms, LOD lineup) and 2 comparison sheets |
| `reports/` | `ZG_validation.txt`, `ZG_geometry.json`, `ZG_export_manifest.json`, `ZG_build_log.json`, `ZG_source_inventory.json`, `ZG_source_integrity_check.md`, `ZG_FREEZE_CANDIDATE.md` (SHA-1 of 19 files), this report |
| `UnityTransfer/` | FBX, Textures, Reports, `README/ZG_UNITY_IMPORT_NOTES.md` |
| `scripts/` | `zg_lib`, `zg_inventory`, `zg_build`, `zg_export`, `zg_render`, `zg_validate`, `zg_package` |
