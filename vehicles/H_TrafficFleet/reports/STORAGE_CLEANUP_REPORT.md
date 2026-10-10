# Storage cleanup report (2026-10-09)

## Result

- **Project size:** 3,112.6 MB before. It is 2,630.5 MB without the staging folder, which shows **493.2 MB** ready to recover.
- **Disk recovered so far: 0 MB.** The safety layer blocks Claude from deleting files permanently. The 41 verified-safe items were **moved**, not deleted, into one staging folder with their paths preserved:
  `vehicles/_TO_DELETE_cleanup_20261009/` (494 MB)
- **To recover the space, the owner runs:**
  `rm -rf /Users/meetshah/Documents/blender/vehicles/_TO_DELETE_cleanup_20261009`
- **To undo instead,** move any item back to the path that appears after the staging folder name.
- **Protected storage:** 1,366 files (1,509.8 MB) listed in 9 frozen manifests, all untouched.

## Integrity after cleanup

- `va_frozen_check.py`: **FROZEN CHECK PASS**, 0 files changed or missing in all 9 releases:
  - ZeroGapR, TitanGT, TitanGT r1, VortexR, VortexR r1, RavenXR;
  - Hatchback A, Sedan A r3, Sedan B.
- `va_integrity.py`: reports **FAIL (0 changed, 0 added, 1,186 removed outside `vehicles/`)**. All 1,186 are the `environment/` folder, which the owner moved off this Mac before this session.
  - **It is archived, not lost:** `/Volumes/Denish/Assets/environment.zip` (2.02 GB, 16:37).
  - That archive was hashed in place, read-only: **all 1,186 frozen environment files match the baseline SHA-1s, with 0 differing and 0 missing.**
  - The same drive also holds `blender.zip` (3.19 GB, 16:59).
  - The integrity FAIL will clear when `environment/` is restored. Until then it only reflects the archive move.
- **Renderer impact:** `ts_render.py` daylight and game modes link the frozen P0 road. When that file is missing, they now build a stand-in 4-lane road with the same lane layout, and the log prints `P0 MISSING`.
  - Box Truck A and Bus A daylight and game renders therefore show the stand-in road.
  - Restoring `environment/` brings the real road back automatically.

## Staged for deletion (verified safe, 41 items, 493.2 MB)

Before each move, every path was checked again: it is not a file in any frozen manifest, not inside a frozen release folder, not named in any manifest's text, and not part of Pulse EV or Pickup A.

| Category | Path | MB | Result |
|---|---|---|---|
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/blend/_failed_r1` | 4.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/blend/_failed_r2` | 4.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/previews/_failed_r1` | 8.4 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/previews/_failed_r2` | 8.4 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/reports/_failed_r1` | 0.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/reports/_failed_r2` | 0.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/scripts/_failed_r1_snapshot` | 0.1 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_Bus_A/scripts/_failed_r2_snapshot` | 0.1 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/_superseded_prod1` | 112.5 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/_superseded_prod2` | 112.4 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/blend/_failed_v2` | 2.7 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/blend/_superseded_0245` | 9.3 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/previews/_failed_v2` | 8.7 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/reports/_failed_prod1` | 0.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/reports/_failed_v2` | 0.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/scripts/_failed_prod1_snapshot` | 0.2 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_A/scripts/_failed_v2_snapshot` | 0.1 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/_superseded_prod2` | 114.6 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/blend/_superseded_0301` | 9.5 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/blend/_superseded_v2_doorslots` | 2.9 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/previews/_superseded_v2_doorslots` | 8.9 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/reports/_failed_prod_disk` | 0.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/reports/_superseded_v2_doorslots` | 0.0 | STAGED |
| failed_superseded_attempts | `H_TrafficFleet/Traffic_SUV_B/scripts/_superseded_v2_doorslots_snapshot` | 0.1 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_clay_front34.png` | 1.0 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_front.png` | 0.9 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_front34.png` | 1.0 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_game_close.png` | 1.1 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_rear.png` | 0.9 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_rear34.png` | 1.0 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_A/previews/suv_a_side.png` | 0.9 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_clay_front34.png` | 1.0 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_front.png` | 0.9 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_front34.png` | 1.0 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_game_close.png` | 1.1 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_rear.png` | 0.9 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_rear34.png` | 1.0 | STAGED |
| v1_blockout_previews | `H_TrafficFleet/Traffic_SUV_B/previews/suv_b_side.png` | 0.9 | STAGED |
| fleet_comparison_source_frames | `H_TrafficFleet/previews/fleet_compare` | 19.1 | STAGED |
| fleet_comparison_source_frames | `H_TrafficFleet/previews/fleet_compare_v2` | 22.8 | STAGED |
| fleet_comparison_source_frames | `H_TrafficFleet/previews/fleet_final` | 30.7 | STAGED |

**What the categories are:**
- **Failed and superseded attempts:** earlier production runs and blockout trials of SUV A, SUV B and Bus A.
  - Each was replaced by a validated run or by the approved blockout.
  - The current `_01_blockout`, `_01_blockout_v2` and `_02`–`_09` blends stay in each `blend/` folder.
- **v1 blockout previews:** replaced by the approved v2 blockouts.
- **Fleet comparison source frames:** all three comparison sheets are kept, including `FLEET_FINAL_7_...jpg`. The frames can be re-rendered.

## Kept: ask first (not touched, 252 MB)

| Item | MB | Why it was kept |
|---|---|---|
| `Traffic_Sedan_A/` (H1) and `Traffic_Sedan_A_r2/` | 94.2 + 138.4 | The frozen r3 manifest says these are "preserved unchanged for reference". This includes their previews, FBX and UnityTransfer (about 188 MB). Approval would mean overriding that frozen statement. |
| SUV A / SUV B `previews/qa`, `lod`, `zebra_master`, `zebra_game` | 82.1 | Review evidence: SUV A is awaiting your review and SUV B is awaiting freeze. |
| `A_Discovery/previews` | 34.7 | Phase A discovery evidence. |
| `Traffic_Box_Truck_A/_superseded_prod1/` | 91.3 | Pre-fix truck build. Safe to stage once the new production validates. |

## Already gone before this session

The previous session's scratchpad was removed with that session. It held about 1.3 GB of scratch trials and 0.44 GB of superseded official builds, all of them disposables listed in `STORAGE_SCRATCH_INVENTORY.md`.

The production runner that lived there was rebuilt at `H_TrafficFleet/scripts/production.sh`.
