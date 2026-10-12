# Vehicle inventory

12 vehicles included (7 traffic, 5 player). One approved release per vehicle identity.

## Included

| # | Vehicle | Type | Approved release | Package folder | Source release record | Blender validation |
|---|---|---|---|---|---|---|
| 1 | Sedan A r3 | traffic | Sedan A r3 | `01_Traffic_Vehicles/Traffic_Sedan_A_r3/` | `H_TrafficFleet/Traffic_Sedan_A_r3/reports/TS_SedanA_r3_FINAL_FREEZE.md` | PASS |
| 2 | Sedan B | traffic | Sedan B | `01_Traffic_Vehicles/Traffic_Sedan_B/` | `H_TrafficFleet/Traffic_Sedan_B/reports/TS_SedanB_FINAL_FREEZE.md` | PASS |
| 3 | Hatchback A r2 | traffic | Hatchback A r2 | `01_Traffic_Vehicles/Traffic_Hatchback_A_r2/` | `H_TrafficFleet/Traffic_Hatchback_A_r2/reports/TS_HatchA_r2_FINAL_FREEZE.md` | PASS |
| 4 | SUV A v2 | traffic | SUV A v2 | `01_Traffic_Vehicles/Traffic_SUV_A_v2/` | `H_TrafficFleet/Traffic_SUV_A/reports/TS_SUVA_FINAL_FREEZE.md` | PASS |
| 5 | SUV B v3 | traffic | SUV B v3 | `01_Traffic_Vehicles/Traffic_SUV_B_v3/` | `H_TrafficFleet/Traffic_SUV_B/reports/TS_SUVB_FINAL_FREEZE.md` | PASS |
| 6 | Box Truck A r7 | traffic | Box Truck A r7 | `01_Traffic_Vehicles/Traffic_Box_Truck_A_r7/` | `H_TrafficFleet/Traffic_Box_Truck_A/reports/TS_BoxTruckA_FINAL_FREEZE.md` | PASS |
| 7 | Bus A v4 | traffic | Bus A v4 | `01_Traffic_Vehicles/Traffic_Bus_A_v4/` | `H_TrafficFleet/Traffic_Bus_A/reports/TS_BusA_FINAL_FREEZE.md` | PASS |
| 8 | Hypercar | player | Hypercar (flagship, Phase 9 export checkpoint hypercar_08) | `02_Player_Vehicles/Hypercar/` | `new_car/reports/final_export_manifest.json` | PASS |
| 9 | Zero Gap R | player | Zero Gap R (Phase B release) | `02_Player_Vehicles/ZeroGapR/` | `vehicles/B_ZeroGapR/reports/ZG_FINAL_FREEZE.md` | PASS |
| 10 | Titan GT r1 | player | Titan GT r1 (Phase C revision r1) | `02_Player_Vehicles/TitanGT_r1/` | `vehicles/C_TitanGT_r1/reports/TG_R1_FINAL_FREEZE.md` | PASS |
| 11 | Vortex R r1 | player | Vortex R r1 (Phase D revision r1) | `02_Player_Vehicles/VortexR_r1/` | `vehicles/D_VortexR_r1/reports/VX_R1_FINAL_FREEZE.md` | PASS |
| 12 | Raven XR | player | Raven XR (Phase E release) | `02_Player_Vehicles/RavenXR/` | `vehicles/E_RavenXR/reports/RV_FINAL_FREEZE.md` | PASS |

Purpose: traffic vehicles replace or extend the existing `TrafficSpawner` pool (analytic collision, no physics required). Player vehicles are the frozen player-car releases; the Hypercar is the flagship player car (its LOD0 is far above mobile budgets, see the integration guide).

## Excluded (and why)

| Item | Location | Reason |
|---|---|---|
| Titan GT (original) | `vehicles/C_TitanGT/` | Frozen but superseded for Unity import by Titan GT r1 (LOD1-3 panel-gap shading tears). Same identity: only r1 ships. |
| Vortex R (original) | `vehicles/D_VortexR/` | Frozen but superseded for Unity import by Vortex R r1 (LOD1 trim normal tears). Same identity: only r1 ships. |
| Zero Gap R r1 | `(proposal only, no folder)` | Proposed LOD1 trim/lights normals revision; never approved or built. The frozen Phase B release ships. |
| Titan GT r2 | `(proposal only, no folder)` | Proposed Lights_LOD1 normals-only revision; never approved or built. Titan GT r1 ships. |
| Pulse EV | `vehicles/F_PulseEV/` | POSTPONED by the project owner (2026-10-08); design blockout only, no production model, no FBX. |
| Traffic Pickup A | `vehicles/H_TrafficFleet/Traffic_Pickup_A/` | POSTPONED by the project owner; blockout / scratch trial only. |
| Traffic Van A | `(never started)` | POSTPONED by the project owner; no model exists. |
| Traffic Sedan A (H1) and r2 | `vehicles/H_TrafficFleet/Traffic_Sedan_A/, Traffic_Sedan_A_r2/` | Superseded by Sedan A r3 (r2 rejected as benchmark); kept for reference only. |
| Traffic Hatchback A (original) | `vehicles/H_TrafficFleet/Traffic_Hatchback_A/` | Frozen as history; superseded by Hatchback A r2 (released version). |
| Earlier SUV A v1, SUV B v1/v2, Box Truck r1-r6, Bus v1-v3 | `rollback folders inside the vehicle directories` | Superseded iterations / rollbacks; Bus v3 is rollback only. The released versions ship. |
| racing_car_00 ... 09 (.blend) | `project root` | Older unnamed generic car; racing_car_09 was the Zero Gap R intake source, superseded by vehicles/B_ZeroGapR/. |
| *_LOD0_unity_test.fbx | `every vehicle` | LOD0-only quick-import reference, a strict subset of the complete FBX. Not a vehicle; not shipped (saves ~40 MB). |
| Old UnityTransfer folders, _UNITY_EXPORT_WS_20261010, _TO_DELETE_cleanup_20261009 | `vehicles/...` | Staging / workspace copies. Their verified files are re-copied here with hash checks; the folders themselves are not shipped. |
| Source .blend files, previews, renders, scripts | `all vehicles` | Not needed in Unity. Every source stays untouched on the Blender machine. |
| environment/ (P0-P3 world) | `/Volumes/Denish/Assets/environment.zip` | Not a vehicle asset; archived off this Mac by the owner (separate known integrity item, see validation report). |
