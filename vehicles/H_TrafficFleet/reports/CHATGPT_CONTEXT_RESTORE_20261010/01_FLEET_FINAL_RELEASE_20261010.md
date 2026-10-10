# Traffic fleet: final Blender release (2026-10-10 09:15)

**All seven priority traffic vehicles are FROZEN (Blender-only).** No FBX, UnityTransfer or Unity files were produced. Nothing was deleted: the 494 MB cleanup staging folder and all rollback folders are retained.

## 1. Approved release versions

All paths are under `/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/`.

| # | Vehicle | Released version | Final file (source of truth) | Freeze manifest | Frozen files |
|---|---|---|---|---|---|
| 1 | Sedan A | **r3** | `Traffic_Sedan_A_r3/blend/trafficsedanar3_09_export_ready.blend` | `Traffic_Sedan_A_r3/reports/TS_SedanA_r3_FINAL_FREEZE.md` | 246 |
| 2 | Sedan B | **production** | `Traffic_Sedan_B/blend/trafficsedanb_09_export_ready.blend` | `Traffic_Sedan_B/reports/TS_SedanB_FINAL_FREEZE.md` | 259 |
| 3 | Hatchback A | **r2** (corrected revision) | `Traffic_Hatchback_A_r2/blend/traffichatchbackar2_09_export_ready.blend` | `Traffic_Hatchback_A_r2/reports/TS_HatchA_r2_FINAL_FREEZE.md` | 278 |
| 4 | SUV A | **v2** | `Traffic_SUV_A/blend/trafficsuva_09_export_ready.blend` | `Traffic_SUV_A/reports/TS_SUVA_FINAL_FREEZE.md` | 294 |
| 5 | SUV B | **v3** | `Traffic_SUV_B/blend/trafficsuvb_09_export_ready.blend` | `Traffic_SUV_B/reports/TS_SUVB_FINAL_FREEZE.md` | 422 |
| 6 | Box Truck A | **r7** | `Traffic_Box_Truck_A/blend/trafficboxtrucka_09_export_ready.blend` | `Traffic_Box_Truck_A/reports/TS_BoxTruckA_FINAL_FREEZE.md` | 1,015 |
| 7 | Bus A | **v4** | `Traffic_Bus_A/blend/trafficbusa_09_export_ready.blend` | `Traffic_Bus_A/reports/TS_BusA_FINAL_FREEZE.md` | 799 |

**Superseded or historical copies:**
- **Original Hatchback A:** `Traffic_Hatchback_A/`, 298 files. It stays frozen and unchanged, but it is **not the release**; r2 replaces it.
- **Bus A v3:** not released. It is kept only as `Traffic_Bus_A/_rollback_v3/`.

**Why some manifests are large:** freezes cover the whole vehicle folder, so rollback and superseded folders are hashed too. The same convention was used for the original Hatchback A.

## 2. Budgets and validation (release versions)

| Vehicle | LOD0 / LOD1 / LOD2 / LOD3 tris | Budget | Materials per LOD | Draw calls per LOD | Worst S1 |
|---|---|---|---|---|---|
| Sedan A r3 | 14,961 / 7,756 / 3,546 / 1,383 | 10–15k | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0.06 % |
| Sedan B | 17,987 / 8,739 / 4,012 / 1,746 | 12–18k | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0.19 % |
| Hatchback A r2 | 17,174 / 8,391 / 3,887 / 1,652 | 12–18k | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0.79 % |
| SUV A v2 | 17,998 / 8,768 / 4,027 / 1,728 | 12–18k | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0.14 % |
| SUV B v3 | 19,840 / 9,566 / 4,325 / 1,939 | 13–20k (approved) | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0.17 % |
| Box Truck A r7 | 20,063 / 10,765 / 4,796 / 2,591 | 15–25k | 8 / 8 / 8 / 6 | 20 / 20 / 20 / 14 | 0.10 % |
| Bus A v4 | 34,506 / 15,126 / 6,210 / 2,999 | 20–35k | 8 / 8 / 8 / 6 | 20 / 20 / 20 / 14 | 0.48 % |

The S1 limit is 1 %.

**Validation:**
- Hatchback A r2 and Bus A v4 were **re-validated at 09:12–09:13 today, immediately before freezing**.
- On every release version, checks 2–16 and S1 **PASS**. They cover:
  - hierarchy, LOD completeness, orientation;
  - wheel pivots and steering, ground clearance;
  - triangle budget, material slots, LOD silhouette;
  - shared materials, independent light channels;
  - textures, UVs, topology;
  - colliders and CenterOfMass, QA renders.
- **Check 1** (protected files) FAILs on every vehicle, see §4.
- FBX re-import is **SKIPPED** (Blender-only).
- Sedan A r3, Sedan B and the original Hatchback A were validated at freeze with 0 errors, before the environment archive existed.

**Dependency check at freeze** (each final blend re-opened):
- `Car_Root`, LOD0–3 roots, 4 `WheelColliderRef`s, `CenterOfMass` and colliders present;
- all 12 external images resolve;
- 0 linked libraries;
- only the review light-state mask is packed.

## 3. Post-freeze hash verification

`A_Discovery/scripts/va_frozen_check.py`: **FROZEN CHECK PASS**, 14 releases, 0 changed or missing files.

| Group | Releases |
|---|---|
| Player cars | Zero Gap R 70; Titan GT 81 / r1 89; Vortex R 109 / r1 91; Raven XR 147 |
| Traffic, released | Sedan A r3 246; Sedan B 259; Hatchback A r2 278; SUV A 294; SUV B 422; Box Truck A 1,015; Bus A 799 |
| Traffic, historical | Hatchback A (original) 298 |

## 4. Protected environment files (reported separately, not hidden)

- `va_integrity.py`: **FAIL**, with 0 changed, 0 added and 1,186 removed outside `vehicles/`. The 1,186 files are the frozen `environment/` folder, which you archived to the external drive `Denish` (`/Volumes/Denish/Assets/environment.zip`).
- **Archive verification:**
  - **Last result (2026-10-09):** all 1,186 files matched their baseline SHA-1, with 0 differing and 0 missing.
  - **Today (2026-10-10):** it **could not be re-run**, because the `Denish` drive is **not connected**. Only Macintosh HD is mounted.
  - **To re-verify once the drive is connected:** `python3 vehicles/A_Discovery/scripts/va_verify_env_archive.py`
- Vehicle check 1 will keep reporting FAIL until `environment/` is restored. No manifest or baseline was edited.

## 5. Night review standard

**Approved as the standard Blender preview lighting:** rig v2, `scripts/ts_night_rig.py`, loaded by `scripts/ts_render.py`. It has two modes:
- `night`: Realistic Highway Night;
- `night_qa`: Visibility QA.

It is a preview-rig change only: no vehicle material or geometry changed. `production.sh` renders the realistic night set automatically.

**Unity note:** night visibility in Unity is unverified until runtime testing. The recommended Unity equivalent is a night skybox or reflection probe with horizon glow, low ambient, and the existing emissive light-mask channels.

**Evidence:**
- `reports/NIGHT_REVIEW_20261010/` (see `README_NIGHT_REVIEW.md`);
- `reports/FLEET_RELEASE_REPORT_20261010.md`.

## 6. Readiness for the Unity export / integration phase

**Ready to start**, with these items for that phase:
1. **FBX export and clean re-import validation** have not run yet; they were deliberately skipped under the Blender-only rule. Use the existing `ts_export.py` / `ts_validate.py` path without `TS_NO_FBX`.
2. **Protected-files check 1** stays FAIL until `environment/` is restored, or until you formally accept it for that phase.
3. **Unity runtime checks:**
   - night lighting;
   - LOD switching;
   - colliders and wheel colliders;
   - light-channel shader hookup.

   None of these is claimed yet.
4. **Export the correct Hatchback A:** Hatchback A **r2**, not the original.
