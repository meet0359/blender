# Traffic fleet: Blender release report (2026-10-10)

This was a Blender-only pass: no FBX, UnityTransfer or Unity files were produced, and the 494 MB cleanup staging folder was not touched.

**Night review images:** `reports/NIGHT_REVIEW_20261010/`. Start with `README_NIGHT_REVIEW.md`.

**Day / approval images (earlier pass):** `reports/FINAL_REVIEW_20261010/`

## 1. Fleet status

| Vehicle | Freeze status | LOD0 / LOD1 / LOD2 / LOD3 tris | Materials / draw calls (LOD0) | Validation |
|---|---|---|---|---|
| Sedan A r3 | **FROZEN** 2026-10-08, unchanged | 14,961 / 7,756 / 3,546 / 1,383 | 8 / 19 | 0 errors at freeze |
| Sedan B | **FROZEN** 2026-10-09, unchanged | 17,987 / 8,739 / 4,012 / 1,746 | 8 / 19 | 0 errors at freeze |
| Hatchback A | **FROZEN** 2026-10-09, **unchanged**: the original is preserved | 17,126 / 8,367 / 3,880 / 1,647 | 8 / 19 | 0 errors at freeze |
| **Hatchback A r2** | **Validated, NOT frozen**: awaiting your approval | 17,174 / 8,391 / 3,887 / 1,652 | 8 / 19 | all PASS except check 1 |
| SUV A v2 | **FROZEN 2026-10-10**: 294 files hashed | 17,998 / 8,768 / 4,027 / 1,728 | 8 / 19 | all PASS except check 1 |
| SUV B v3 | **FROZEN 2026-10-10**: 422 files hashed | 19,840 / 9,566 / 4,325 / 1,939 | 8 / 19 | all PASS except check 1 |
| Box Truck A r7 | **FROZEN 2026-10-10**: 1,015 files hashed | 20,063 / 10,765 / 4,796 / 2,591 | 8 / 20 | all PASS except check 1 |
| **Bus A** | **NOT frozen.** v3 was approved, but a visible defect was found (§4). **v4 is validated and awaits your approval.** | v4: 34,506 / 15,126 / 6,210 / 2,999 | 8 / 20 | v4: all PASS except check 1 |

**Check 1** is the protected-files check:
- **FAIL** for every vehicle.
- **Cause:** the frozen `environment/` folder (1,186 files) is archived on `/Volumes/Denish`.
- **Status:** it is an accepted relocation, hash-verified in the archive, and is not vehicle corruption.

Every vehicle-specific check passes. "All PASS" means all 16 checks plus the S1 shading screen. They cover:
- hierarchy, LODs, orientation;
- wheel pivots and steering, ground clearance;
- budgets, materials, silhouette;
- independent light channels;
- textures, UVs, topology;
- colliders and CenterOfMass, QA renders.

**Other results:**
- FBX re-import is SKIPPED (Blender-only).
- All triangle and material budgets are within limits.
- Box Truck A's freeze includes its rollback and handoff folders, because a freeze covers the whole vehicle folder (Hatchback A was frozen the same way).

## 2. Night visibility

### Root cause (measured)

A frozen car, Sedan B, was rendered under the old night rig twice: once with white clay on every surface, once with its real paint.

| Metric (rear ¾ body region) | White clay | Real paint |
|---|---|---|
| Median luminance | 0.118 | 0.020 |
| Pixels below 0.02 | 9 % | 51 % |

**The problem was the review rig, not the vehicle materials:**
- **Near-black sky.** The old night sky was almost black (strength 0.004). Clear-coated paint and glass mainly reflect their surroundings, so they mirrored black.
- **Weak, harsh light.** Light came only from two side street lights with no fill or rim, and the AgX "Medium High Contrast" look crushed the low end.

The same thing would happen in Unity with a black reflection probe.

### Fix: night rig v2 (`scripts/ts_night_rig.py`, loaded by `ts_render.py`)

**World and lights (both conditions):**
- **Sky:** a deep-blue sky gradient with a warm light-pollution glow at the horizon, which gives glossy paint and glass something real to reflect.
- **Moonlight:** cool and raking, at 0.35 W/m².
- **Street lights:** five warm LED street lights, two of them far ahead and behind, which gives a natural silhouette rim.

**Tone:**
- **Realistic:** AgX Base Contrast at real exposure.
- **Visibility QA:** adds soft fills, Medium Low Contrast and +0.4 EV.

**Result on Sedan B** (same camera, rear ¾):

| Rig | Median luminance | Pixels below 0.02 |
|---|---|---|
| Old | 0.020 | 51 % |
| **Realistic** | **0.110** | **13 %** |
| QA | 0.302 | 1 % |

The background stays dark: sky and road are not lifted uniformly.

### What changed where

| Layer | Changes |
|---|---|
| **Blender preview rig only** | <ul><li>World gradient, moon, street lights, tone mapping, QA fills.</li><li>New night camera set: rear follow and front approach at close, normal and far.</li><li>Long-vehicle camera correction (truck +0.5 m, bus +3.0 m; cars unchanged).</li></ul>**No vehicle material or geometry was changed for night visibility.** |
| **Assets** | Only the two fixes in §4 (Hatchback A r2, Bus A v4). Neither is night-related. |
| **Unity (recommended, not done)** | <ul><li>A night skybox or reflection probe with the same horizon glow;</li><li>low ambient;</li><li>the existing emissive light-mask channels for lamps.</li></ul>No per-vehicle realtime lights are needed. **Night visibility in Unity is not claimed until runtime testing.** |

### Evidence (`reports/NIGHT_REVIEW_20261010/`)

| File | Shows |
|---|---|
| `FLEET_NIGHT_OLD_vs_NEW.jpg` | All 7 vehicles, old vs new with **identical cameras**. Per vehicle: `<vehicle>/<vehicle>_NIGHT_OLD_vs_NEW.jpg`. |
| `FLEET_NIGHT_REALISTIC_OVERVIEW.jpg` | 8 rows (including Hatchback A r2). Per vehicle: `<vehicle>/<vehicle>_NIGHT_REALISTIC.jpg`, 9 views covering 3 angles, rear follow at 3 distances, front approach at 3 distances. |
| `FLEET_NIGHT_VISIBILITY_QA_OVERVIEW.jpg` | Per vehicle: `<vehicle>/<vehicle>_NIGHT_VISIBILITY_QA.jpg` |
| `FLEET_NIGHT_RUNNING_vs_BRAKE.jpg` | Running lights vs brakes on |

### Silhouette and class read

All classes are recognisable at close, normal and far distance, from both the rear-follow and front-approach cameras:
- sedans: low and long;
- hatchback: short tail;
- SUVs: tall glasshouse;
- box truck: cab plus box, with the identification and clearance row;
- bus: 12 m body, window band, doors, identification and clearance row.

Body panels, wheels, windows and grilles stay readable; no body panel goes fully black.

### Headlights and tail lights

**Running lights:**
- At the front, headlamps and DRLs are visible from the approach camera at every distance.
- At the rear, tails are visible from the follow camera at every distance.

**Brake test** (follow close; red-lamp area and white clipping measured on the render):

| Vehicles | Brakes on vs running | White-clipped pixels |
|---|---|---|
| Sedans and SUVs | Red area grows 2–2.5× | Unchanged |
| Truck and bus | The lamp body brightens and the high-mount strip lights | No clipping |

The brake lamps are distinct and not overexposed.

**Truck clearance and identification lamps:** independent channels, verified with brake, indicator and reverse on and off (`Traffic_Box_Truck_A/previews`, run r7).

## 3. Chase-camera visibility

| Camera | Result |
|---|---|
| Rear follow, 7.5 / 22 / 60 m | Vehicle class and lamps read at every distance |
| Front approach, 10 / 25 / 60 m | Vehicle class and lamps read at every distance |

**Defect found and fixed:** the bus's **gameplay close camera had been inside the bus** in every earlier review set, day and night. That was a review-camera bug, not a model defect. Gameplay cameras are now offset from the vehicle's real rear and front, and the bus game and LOD game-close evidence was re-rendered.

## 4. Fixes made this pass

| Vehicle | Defect | Root cause | Fix | Status |
|---|---|---|---|---|
| Hatchback A (frozen) | Hexagon-shaped plate recess; crack marks under the plate | <ul><li>A corner-only plate cutter gave a flat recess floor on a convex rear, so the recess was deeper at the middle of each edge.</li><li>The rear end-cap fold left 18 inverted faces at x ±0.21, z 0.69.</li></ul> | **New revision, `Traffic_Hatchback_A_r2/`:** <ul><li>dense plate outline (`PLATE_R_STEP` 2 cm);</li><li>rear n-gon end cap plus a small 7 % ring.</li></ul>The frozen original is untouched. | Validated. **Awaiting your approval.** |
| Bus A v3 | Large crumpled swirl on the rear engine panel (visible in the corrected close follow view) | A grain-patterned atlas cell magnified over a 1.4 × 0.67 m recess | **v4:** pattern-free gloss-black recess, plus 8 real horizontal louvre slats | Validated. **Awaiting your approval.** v3 is kept in `_rollback_v3`. |

**My own regression, found and fixed before release:**
- **What happened:** the plate-densify edit hid the rear valance cutter inside a code comment.
- **Effect:** the first Hatchback r2 build and the first Bus v4 build lacked their lower valance recess.
- **Detection:** I caught it from the before/after renders.
- **Fix:** I rebuilt both. The faulty builds are kept in `_superseded_valance_bug/`.
- **Check:** a scan of all builder scripts found no other code hidden in comments.
- **Frozen vehicles:** SUV A, SUV B and the truck were built before that edit and are unaffected.

## 5. Frozen asset integrity

- `va_frozen_check.py`: **PASS.** 12 releases, all with 0 changed or missing files:
  - Zero Gap R, Titan GT (+r1), Vortex R (+r1), Raven XR;
  - Sedan A r3, Sedan B, Hatchback A;
  - **SUV A, SUV B, Box Truck A** (new).
- Each new manifest re-opened its final blend for a dependency check, with these results:
  - hierarchy, wheel references, CenterOfMass and colliders all present;
  - all external images resolve;
  - no linked libraries.
- `va_integrity.py`: **FAIL**, with 0 changed, 0 added and 1,186 removed. This is the archived `environment/` only, reported separately from vehicle integrity.
- No manifest was edited to hide a failure.

## 6. Remaining issues

1. **Bus A has no freeze.** Approve v4 (louvre fix) to freeze it, or tell me to freeze v3 as originally approved.
2. **Hatchback A r2 awaits your approval.** If approved, I'll freeze it as a separate release; the original stays frozen.
3. **SUV A hood:** zebra-only stepping, accepted by you.
4. **Unity:** night visibility in Unity is unverified. The recommended Unity setup is in §2.
5. **Stand-in road:** daylight, game and night renders use a stand-in road while `environment/` is archived.
6. **Storage:** 7.6 GB free.
   - The staging folder (494 MB) is kept, per your instruction.
   - The night review adds 93 MB, mostly 96 source PNGs.

## 7. Files for your approval

| Vehicle | Final file | Validation | Evidence |
|---|---|---|---|
| Hatchback A r2 | `Traffic_Hatchback_A_r2/blend/traffichatchbackar2_09_export_ready.blend` | `Traffic_Hatchback_A_r2/reports/traffichatchbackar2_validation.txt` | `reports/NIGHT_REVIEW_20261010/Traffic_Hatchback_A_r2/Traffic_Hatchback_A_r2_BEFORE_AFTER.jpg` |
| Bus A v4 | `Traffic_Bus_A/blend/trafficbusa_09_export_ready.blend` | `Traffic_Bus_A/reports/trafficbusa_validation.txt` | `reports/NIGHT_REVIEW_20261010/Traffic_Bus_A/Traffic_Bus_A_v4_BEFORE_AFTER.jpg` |
