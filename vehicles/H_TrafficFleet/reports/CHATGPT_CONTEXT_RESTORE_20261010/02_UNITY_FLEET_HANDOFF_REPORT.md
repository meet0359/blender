# Unity fleet handoff report: seven traffic vehicles (2026-10-10)

**Scope:** export and validation only, on the Blender Mac (Blender 5.2.2).
- No frozen file was modified.
- No output was written inside a frozen vehicle folder.
- No modelling was done.
- Unity was not installed or run.

**Unity runtime verification is not claimed.** It belongs to **P0-05** on the Unity machine.

## 1. Result

| # | Release | Status | FBX re-import (validator 17, 18) | FBX audit | Validator |
|---|---|---|---|---|---|
| 1 | Sedan A r3 | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |
| 2 | Sedan B | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |
| 3 | Hatchback A **r2** | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |
| 4 | SUV A v2 | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |
| 5 | SUV B v3 | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |
| 6 | Box Truck A r7 | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |
| 7 | Bus A **v4** | **EXPORTED + VALIDATED** | PASS / PASS | PASS | 18 PASS, check 1 FAIL (environment) |

**Versions exported:**
- Exported: exactly the seven release versions from `FLEET_FINAL_RELEASE_20261010.md`.
- Not exported: the original Hatchback A, the Bus A v3 rollback, and every other superseded copy.
- Unity status for all seven: **PENDING P0-05**.

**About check 1** (protected files byte-identical):
- On every vehicle, the failures are only the archived `environment/` files: 0 added files, and 0 changed files in any frozen release (§7).
- Every vehicle-specific check passes. They cover:
  - hierarchy, LODs, orientation;
  - wheel pivots and steering, ground clearance;
  - budgets, materials, silhouette;
  - light channels, textures, UVs, topology;
  - colliders and CenterOfMass, QA renders.
- S1 shading also passes.

## 2. Method

**Pre-flight:**
- `va_frozen_check.py` passed for 14 releases with 0 changed files.
- 8.5 GB of disk was free.

**Isolated workspace** `H_TrafficFleet/_UNITY_EXPORT_WS_20261010/`:
- It holds copies of each frozen `*_09_export_ready.blend`, its vehicle textures and the shared textures.
- Every copy was SHA-1-verified against its freeze manifest before export and again after export, and was unchanged.
- The relative texture layout was preserved, so the copies resolve their own textures.
- The frozen QA previews are linked read-only, for validator check 16.

**Pipeline:** the existing `ts_export.py`, with unchanged FBX settings and conventions:
- in-memory axis bake;
- n-gon triangulation and duplicate-face removal;
- `-Z` forward, `Y` up, scale 1, `FBX_SCALE_ALL`;
- relative texture paths, no embedding;
- MikkTSpace tangents, custom properties on.

**One opt-in addition:** `TS_FROM_09=1`, which needs `TS_SCRATCH`.
- It exports from the 09 copy and saves nothing.
- Production behaviour without the flag is unchanged.

**Pilot first:** SUV A was exported, validated with the FBX re-import, audited and inspected value by value before the other six ran automatically.
- SUV A: 45 s.
- The other six: 4 min 38 s.

**Validation** (`ts_validate.py`, full 16 checks + S1, with **FBX clean re-import on**):
- names and hierarchy;
- bounds (≤ 1 mm) and pivots (≤ 0.1 mm);
- triangles, materials, UVs and texture references;
- a raw Unity-space axis test.

**Supplementary audit** (`scripts/ts_fbx_audit.py`, new, read-only). It runs on the **packaged** FBX, against the 09 copy:
- FBX file globals;
- texture paths resolved from the package folder;
- per-LOD objects, triangles and materials;
- wheel pivots vs refs, and wheel custom properties;
- colliders and CenterOfMass;
- light-channel faces;
- NaN or zero-length normals, degenerate and duplicate faces, S1 on the FBX meshes;
- Unity-space transforms and dimensions;
- material mapping.

**Cross-check against earlier exports:** Sedan A r3 and Sedan B already had FBX frozen inside their release folders, from 2026-10-08/09. The new exports have the same object lists (27 / 71), materials and textures.
- The size difference is under 1 KB, from the longer workspace path stored in the FBX.
- The package uses the new, uniformly named exports. The old in-folder copies stay frozen and untouched.

Driver: `scripts/ts_unity_handoff.py` (`ws | run | audit | package | verify`).

## 3. FBX validation and LOD counts

**Every FBX:**
- FBX 7400, Y-up, `UnitScaleFactor` 100 (1 unit = 1 m);
- no embedded media;
- 71 objects (complete) or 27 objects (LOD0 test);
- 0 leaked selection;
- n-gons triangulated: truck 4 meshes, others 0;
- duplicate triangles removed: 0.

| Release | LOD0 / LOD1 / LOD2 / LOD3 tris (FBX = source) | Objects per LOD | Materials per LOD | Complete FBX (bytes) |
|---|---|---|---|---|
| Sedan A r3 | 14,961 / 7,756 / 3,546 / 1,383 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 2,212,284 |
| Sedan B | 17,987 / 8,739 / 4,012 / 1,746 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 2,581,804 |
| Hatchback A r2 | 17,174 / 8,391 / 3,887 / 1,652 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 2,472,108 |
| SUV A v2 | 17,998 / 8,768 / 4,027 / 1,728 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 2,596,044 |
| SUV B v3 | 19,840 / 9,566 / 4,325 / 1,939 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 2,836,636 |
| Box Truck A r7 | 20,063 / 10,765 / 4,796 / 2,591 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 2,607,948 |
| Bus A v4 | 34,506 / 15,126 / 6,210 / 2,999 | 16 / 16 / 16 / 12 | 8 / 8 / 8 / 6 | 3,997,036 |

**Agreement with the source:**
- Triangle, object and material counts are **identical** to the frozen source at every LOD, and equal the released budget figures.
- Re-imported bounds deviate ≤ 3.6e-7 m and pivots ≤ 1.8e-7 m.

**Normals and duplicates:**
- 0 NaN values, 0 zero-length normals, 0 degenerate faces and 0 duplicate faces on every FBX.
- No duplicate object or material names after import.
- Worst torn-normal share (S1) on the FBX meshes, all within the 1 % limit and equal to the source:

| Release | Worst mesh | S1 |
|---|---|---|
| Sedan A r3 | Body_LOD2 | 0.06 % |
| Sedan B | Body_LOD3 | 0.19 % |
| Hatchback A r2 | Glass_LOD3 | 0.79 % |
| SUV A v2 | Body_LOD2 | 0.14 % |
| SUV B v3 | Body_LOD3 | 0.17 % |
| Box Truck A r7 | Body_LOD0 | 0.00 % |
| Bus A v4 | Body_LOD1 | 0.48 % |

## 4. Materials and textures

**Materials:**
- 8 per LOD (6 at LOD3), only from the shared library plus per-vehicle instances.
- The material set per LOD is identical in FBX and source.

**Textures:**
- Every texture the 09 uses is in the package:
  - 3 vehicle bakes per vehicle;
  - 12 shared PNGs, including the Unity-side `TS_Atlas_MetallicSmoothness`, `TS_Lights_ChannelID` and `TS_PaintFlake_Normal`.
- Each complete FBX references 10 textures by relative path, and **all resolve from the package location**: 0 missing.

**Not in the FBX, set up by hand in Unity:** the FBX format cannot express these Blender node setups. The integration README covers each one.
- the paint AO/grime map;
- `TS_Lights_Emission`;
- the light-channel ID map;
- the metallic-smoothness map;
- the paint-flake detail normal.

**Found during packaging** (documentation only, no asset change):
- The `unity` note on the paint materials is a generic fleet note. It does not match the box truck's actual paint (solid: metallic 0, coat 0.55).
- The per-vehicle READMEs list the actual frozen material values.
- Also flagged: URP reads occlusion from the G channel, but AO is stored in R, so the AO map must not go straight into URP's Occlusion slot.

**Light channels:**
- Channel face counts are identical in FBX and source on `Lights_LOD0`–`LOD3`.
- Cars carry 7 channels; the truck and bus carry 8 (with Marker).
- `TS_Lights_ChannelID` decodes to exactly 8 IDs (0–7).

## 5. Orientation and scale (Unity space, raw FBX read)

**Every vehicle:**
- `Car_Root` identity;
- all node rotations identity (≤ 7.5e-8), scale 1, no negative scale;
- nose at +Z, tail at −Z, up +Y, ground at Y = 0;
- front-left wheel at −X / +Z.

**Point mapping:** Blender (x, y, z) → Unity (−x, z, −y).

**Importer settings:** Scale 1, Convert Units on, Bake Axis Conversion off.

| Release | Length × width (incl. mirrors) × height (m) |
|---|---|
| Sedan A r3 | 4.65 × 2.06 × 1.47 |
| Sedan B | 4.97 × 2.18 × 1.49 |
| Hatchback A r2 | 4.27 × 2.08 × 1.52 |
| SUV A v2 | 4.48 × 2.19 × 1.70 |
| SUV B v3 | 4.98 × 2.30 × 1.81 |
| Box Truck A r7 | 7.07 × 2.54 × 3.25 |
| Bus A v4 | 12.01 × 2.98 × 3.20 |

## 6. Colliders, wheel pivots and CenterOfMass

**Wheels:**
- Four `WheelColliderRef`s per vehicle.
- At every LOD, each wheel, caliper and steer-pivot origin sits **exactly** on its ref: deviation 0 m.
- Wheels are present at LOD0–3.
- The `radius_m` and `width_m` custom properties survive the FBX round trip.

**Colliders:** 4 convex hulls per vehicle, each ≤ 255 triangles, no material.

**CenterOfMass:** matches the source, on the centreline.

| Release | Wheel radius / width (m) | FL wheel (Unity) | CenterOfMass (Unity) |
|---|---|---|---|
| Sedan A r3 | 0.316 / 0.205 | (−0.78, 0.316, 1.35) | (0, 0.52, 0.22) |
| Sedan B | 0.352 / 0.245 | (−0.8125, 0.352, 1.62) | (0, 0.53, 0.08) |
| Hatchback A r2 | 0.317 / 0.225 | (−0.77, 0.317, 1.25) | (0, 0.50, 0.18) |
| SUV A v2 | 0.370 / 0.235 | (−0.80, 0.37, 1.32) | (0, 0.62, 0.12) |
| SUV B v3 | 0.391 / 0.275 | (−0.84, 0.391, 1.55) | (0, 0.70, 0.10) |
| Box Truck A r7 | 0.405 / 0.225 | (−0.84, 0.405, 2.30) | (0, 1.10, 0.40) |
| Bus A v4 | 0.478 / 0.275 | (−1.05, 0.478, 3.30) | (0, 1.10, −0.30) |

All four wheels per vehicle are listed in each `README_<Base>.md`.

## 7. Source integrity

**Frozen releases:**
- `va_frozen_check.py` **after export: FROZEN CHECK PASS**, 14 releases, 0 changed or missing files.
- All seven workspace 09 copies still match their freeze manifests after export.
- No manifest was edited.

**Protected environment files** (reported separately, not hidden):
- `va_integrity.py`: **FAIL**, with 0 changed, **1,186 removed** and 0 added.
- The removed files are the frozen `environment/` folder, archived to the `Denish` drive.
- The handoff added nothing outside `vehicles/`.

**Archive re-verification:**
- `va_verify_env_archive.py`: **NOT RUN**. `/Volumes/Denish` is not connected; only Macintosh HD is mounted.
- Last verified result (2026-10-09): 1,186 / 1,186 files matched their baseline SHA-1.
- This is an open integrity item, not a pass.

**Storage:**
- The 494 MB cleanup staging folder `vehicles/_TO_DELETE_cleanup_20261009/` is intact.
- 8.3 GB is free after export.

## 8. Unity import instructions

Read **`UNITY_HANDOFF_20261010/README_UNITY_IMPORT.md`**, targeting Unity 6000.6.0f1 / URP 17.6. It covers:
- texture import settings, including point-filtered, uncompressed and linear `TS_Lights_ChannelID`;
- model importer settings;
- prefab assembly:
  - LOD Group on `Car_Root` (suggested 50 / 22 / 8 / 1.5 %);
  - convex MeshColliders on `Collision_*`;
  - Rigidbody `centerOfMass`;
  - WheelColliders at the refs;
  - wheel and steer drive for all LOD copies;
- the material setup per material: URP Complex Lit paint; the atlas with `MetallicSmoothness`; transparent glass and lenses; the single-draw-call light-channel shader;
- the night-lighting recommendation;
- the P0-05 runtime checklist.

Every setting there is a recommendation derived from the validated FBX data. **None has been run in Unity.**

## 9. Package

**Location:** `/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/UNITY_HANDOFF_20261010/`

**Size:** **48 MB (48,820 KB on disk), 94 files.**

**Root files:**
- `README_UNITY_IMPORT.md`
- `UNITY_FLEET_MANIFEST.md` / `.json`: source release and SHA-1, freeze manifest, FBX, textures, materials, LODs, dependencies
- `UNITY_FLEET_HANDOFF_REPORT.md`: this report
- `SHA1SUMS.txt`: every other file
- `shared/textures/`: 12 PNG

**Vehicle folders:**
- `01_Traffic_Sedan_A_r3`
- `02_Traffic_Sedan_B`
- `03_Traffic_Hatchback_A_r2`
- `04_Traffic_SUV_A`
- `05_Traffic_SUV_B`
- `06_Traffic_Box_Truck_A`
- `07_Traffic_Bus_A`

**Each vehicle folder contains:**
- `FBX/`: complete + LOD0 test;
- `textures/`: 3 bakes;
- `reports/`: validation, FBX audit, export manifest, geometry, Unity manifest;
- `README_<Base>.md`.

**FBX names:** `TrafficSedanA_r3`, `TrafficSedanB`, `TrafficHatchbackA_r2`, `TrafficSUVA`, `TrafficSUVB`, `TrafficBoxTruckA`, `TrafficBusA`. The r3 and r2 suffixes keep the release identity visible in Unity.

**Export workspace** `H_TrafficFleet/_UNITY_EXPORT_WS_20261010/` (54 MB):
- It holds the verified 09 copies, raw exports and logs, and is kept for traceability.
- Delete it whenever you like after acceptance. Nothing frozen depends on it.

## 10. Remaining blockers and open items

1. **Environment archive re-verification:** NOT RUN, because the `Denish` drive is absent.
   - Connect it and run `python3 vehicles/A_Discovery/scripts/va_verify_env_archive.py`.
   - Until `environment/` is restored, or the relocation is formally accepted, `va_integrity` and validator check 1 keep reporting FAIL.
2. **P0-05, Unity runtime verification on the Unity machine:**
   - import;
   - LOD switching;
   - colliders and WheelColliders;
   - centre of mass;
   - transparency sorting;
   - the light-channel shader;
   - the night look;
   - mobile performance.

   None is claimed here.
3. **Unity-side material work:** the paint (AO from R, grime lerp, flake detail) and the light-channel emission need a Shader Graph, or repacked maps. The FBX cannot carry these, as described in §4.
4. **Information only:**
   - The FBX files also store absolute texture paths from this Mac, including the local user name. Unity uses the relative paths, which resolve.
   - The old FBX inside the frozen Sedan A r3 and Sedan B folders are superseded for Unity use by this package. Use only `UNITY_HANDOFF_20261010`.

**Scripts changed this phase:**
- `scripts/ts_export.py`: opt-in `TS_FROM_09`.
- New: `scripts/ts_fbx_audit.py`, `scripts/ts_unity_handoff.py`.
- No builder, design, validator or freeze tooling changed.
