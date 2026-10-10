# Phase C — Titan GT: final production QA report

**Status: APPROVED and FROZEN: Phase C technical release** (2026-10-08). Any later change requires a separate revision folder.

Built from the approved blockout `blend/titangt_01_blockout.blend`, which is byte-identical, SHA-1 065d7849…. The production design curves are copied verbatim from it.

## 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/TG_validation.txt`) | **18 checks: 0 errors, 0 warnings.** This is the Zero Gap R standard, adapted for Titan GT: doors are part of the body, and the extra close-up and LOD-lineup renders are required |
| FBX clean re-import | 2 of 2 files pass. Names, hierarchy, triangles, materials, UVs and textures are preserved. Bounds deviate by 3e-7 m and pivots by 1.8e-7 m. In raw Unity space the nose points +Z, up is +Y, and the front-left wheel is on −X |
| Protected files | **PASS.** All 1,554 Phase A baseline files are byte-identical (frozen P0–P3, Hypercar, racing_car sources). The 70 frozen Zero Gap R files are unchanged, and the approved blockout is unchanged |
| Checkpoints | `titangt_01_blockout` (approved) and `_02_body_panels` … `_09_export_ready`, each written once |

## 2. Numbers

| LOD | Triangles | Ratio | Target | Objects | Materials |
|---|---|---|---|---|---|
| LOD0 | 77,370 | 100% | 60–90 k | 22 | 15 |
| LOD1 | 39,752 | 51% | 40–50 % | 22 | 15 |
| LOD2 | 18,527 | 24% | 15–25 % | 22 | 15 |
| LOD3 | 7,731 | 10% | 5–10 % | 13 | 15 |

- **Silhouette IoU against LOD0:** {"LOD1": {"side": 0.9998, "front": 1.0, "top": 1.0}, "LOD2": {"side": 0.999, "front": 0.999, "top": 0.9997}, "LOD3": {"side": 0.9956, "front": 0.9984, "top": 0.9991}}. Dimensions stay within 1.8 mm.
- **Textures:** 7 PNG files used by the materials (plus the Unity MetallicSmoothness pack = 8 files), 0.13 MB on disk and 10.75 MB as uncompressed RGBA, all generated procedurally (no third-party assets):
  - a 256 px palette;
  - carbon twill at 512 px;
  - tire tread and sidewall at 1K.

**LOD0 triangle budget**

| Part | Triangles |
|---|---|
| Body (shell with all openings, panel gaps, mirrors) | 39,834 |
| Trim (grille slats and bezel, intake fins, splitter, side vents, handles, sills, valance, plate recess, quad exhaust, diffuser and 6 strakes, wheel-well liners) | 5,112 |
| Lights | 2,000 |
| Glass | 1,792 |
| Interior plus steering wheel | 7,720 |
| Wheels (4 assemblies) | 20,912 |

## 3. What was built (blockout → production)

### Body
- The lofted design cage is faired with a Laplacian smooth (station ripples removed), subdivided twice, then reduced with a curvature-adaptive collapse.
- Real recessed openings are cut by one exact boolean: the grille, two corner intakes, two headlamp housings, the full-width tail-light channel with C-shaped corners, four wheel arches, door handles and fender vents.
- Real panel-gap grooves (4.5 mm wide, 11 mm deep) run around the hood, the trunk lid and both doors.
- The skin carries the high-resolution body normals, so reflections stay smooth. Openings and gaps keep crisp flat normals.

### Front
- The grille has a dark-chrome bezel and seven recessed slats with depth.
- The corner intakes have carbon fins, and a carbon splitter blade runs below.

### Headlights
- Each recessed housing holds a DRL blade, two projector modules (housing, reflector and lens), an amber indicator, and a clear outer lens.

### Rear
- A full-width red tail bar runs into corner verticals, with stacked brake, indicator and reverse blocks.
- The red lens is deep red at alpha 0.80, so it reads red in daylight. This applies the PB-1 lesson from Zero Gap R; daylight renders confirm it.
- Below: a satin-black valance with a dark-chrome accent, a blank plate recess, and a quad exhaust with tubes, rolled lips and dark inner sleeves.
- **Diffuser:** now attached to the floor line. The six strakes are 45 mm deep and no longer hang below the body (blockout issue fixed).

### Wheel arches
- Satin-black wheel-well liners sit inside the body side. The bright arch-lip sliver from the blockout is gone.

### Wheels
- Graphite five twin-spoke rims with tapered, concave spokes, a machined lip, a hub, five lug nuts and a centre cap.
- 20-inch front and 21-inch rear.
- Tires are revolved with a profile and carry the tread and sidewall texture.
- Slotted-look rotors with dark hats, and bronze multi-segment calipers.

### Interior
Cognac and black leather, built as LHD.
- Seats with bolsters and head restraints.
- The dashboard with an aluminium accent bar, a cluster hood, instrument and centre displays.
- The centre console with an aluminium plate and selector, door cards, armrests, speaker trim, carpet, an alcantara parcel shelf and headliner, and a three-spoke steering wheel.
- All of it sits inside the body skin. One door card pierced the skin near the A-pillar; I found it in review and fixed it.

### Lights and materials
- **15 materials:**
  - paint, palette, carbon, tire, glass;
  - clear and red lenses, display;
  - **7 independent light channels:** DRL, Headlamp, Tail, Brake, Indicator_L, Indicator_R and Reverse.
- Each channel is validated by position (front or rear; the left indicator on +X).

### Rig
- `Car_Root` → `LOD0_Root` … `LOD3_Root`. The front wheels hang from `SteerPivot_FL/FR`, with the caliper on the pivot.
- Wheels roll and steer correctly in the tests.
- `WheelColliderRef_*` markers carry the radius and width. `CenterOfMass` sits at (0, 0.15, 0.42).
- Four convex colliders: Front, Body, Cabin and Rear.

## 4. Known limitations

These are honest notes for your review.

- **Body shading:**
  - The body is generated from lofted sections, not hand-modelled. Its large surfaces read well, but the wide rear deck shows mild broad reflection waviness, which is visible in the rear close-up.
  - The hood centre has a soft dip where the cage stations meet the fenders.
- **Grille and brakes:**
  - The grille's back plate is dark and simple. There is no radiator or mesh behind the slats.
  - The rotors are plain discs: the slotting is implied by colour, not modelled.
- **Interior:** made of bevelled blocks. It is convincing through the dark glass at gameplay distance, but it is not a hero close-up interior.
- **Doors:** they have shut lines but are part of the body, so they don't open.
- **LOD sizes:**
  - LOD1 is 51 % of LOD0 (target 40–50 %). The validator allows a 2 % margin.
  - LOD3 is 10 %, at the top of its range.
- **Unity:** no Unity performance is claimed. 10.8 MB is the uncompressed size; Unity's GPU compression will make it smaller.

## 5. Open polish items (non-blocking)

- **TG-PB-1:** mild broad reflection waviness on the rear deck.
- **TG-PB-2:** slight dip in the hood centre.

Both stem from the lofted-section body. They are left for a future revision; the frozen release is unchanged.

## 6. Files

| Path | Contents |
|---|---|
| `blend/` | 9 checkpoints. Final source: `titangt_09_export_ready.blend` |
| `exports/` | `TitanGT_complete_unity.fbx` (102 objects) and `TitanGT_LOD0_unity_test.fbx` |
| `textures/` | 8 PNG files |
| `previews/` | 14 final renders and 3 sheets: `TG_compare_hypercar_zerogapr_titangt.jpg`, `TG_compare_blockout_final.jpg`, `TG_details.jpg`. The approved blockout renders are kept as `TG_blockout_*` |
| `reports/` | `TG_validation.txt`, `TG_geometry.json`, `TG_export_manifest.json`, `TG_build_log.json`, `TG_blockout_report.md`, `TG_source_integrity_check.md`, `TG_FREEZE_CANDIDATE.md` (integrity manifest, SHA-1 of 19 files), this report |
| `UnityTransfer/` | FBX, Textures, Reports, `README/TG_UNITY_IMPORT_NOTES.md` |
| `scripts/` | `tg_blockout`, `tg_lib`, `tg_build`, `tg_render`, `tg_export`, `tg_validate`, `tg_package`, `tg_sheet` |
