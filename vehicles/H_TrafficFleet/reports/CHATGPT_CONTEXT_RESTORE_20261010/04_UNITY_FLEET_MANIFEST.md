# Unity fleet manifest (traffic, 7 vehicles)

Created 2026-10-10 09:45. Package `H_TrafficFleet/UNITY_HANDOFF_20261010`. Unity runtime verification: **not done** (P0-05, Unity machine).

| # | Release | Folder | Source 09 SHA-1 (= freeze manifest) | Complete FBX | SHA-1 | LOD0 / 1 / 2 / 3 tris | Materials per LOD | Validation | FBX audit |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Sedan A r3** | `01_Traffic_Sedan_A_r3` | `898791c95ae3a8ef6e2a2d34aaf989786f51194b` | `FBX/TrafficSedanA_r3_complete_unity.fbx` | `70361cfb6efed020f77e13628f878f04770e9212` | 14,961 / 7,756 / 3,546 / 1,383 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |
| 2 | **Sedan B** | `02_Traffic_Sedan_B` | `a681c5bf5cc603f40394aeaafb3d109d6130fd37` | `FBX/TrafficSedanB_complete_unity.fbx` | `eef0b9310911077376dba57de606622438842855` | 17,987 / 8,739 / 4,012 / 1,746 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |
| 3 | **Hatchback A r2** | `03_Traffic_Hatchback_A_r2` | `317c2ea5f01b14579d6fa0a12c820d63816748d0` | `FBX/TrafficHatchbackA_r2_complete_unity.fbx` | `e1808489b4b8f278cfca2d41616c483f7d462fcd` | 17,174 / 8,391 / 3,887 / 1,652 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |
| 4 | **SUV A v2** | `04_Traffic_SUV_A` | `02b50f74ea09181c2ec33d58bca67abf024e4e3c` | `FBX/TrafficSUVA_complete_unity.fbx` | `e8a197c424459f4c8e55ed079dc76c5f488a23cb` | 17,998 / 8,768 / 4,027 / 1,728 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |
| 5 | **SUV B v3** | `05_Traffic_SUV_B` | `cc4d2ae0a7493cd22ccf44f893b731404141f12c` | `FBX/TrafficSUVB_complete_unity.fbx` | `2f3836ff6185883f98e2eec1dbc0db265aafd407` | 19,840 / 9,566 / 4,325 / 1,939 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |
| 6 | **Box Truck A r7** | `06_Traffic_Box_Truck_A` | `7ef36071193fa30a56c05a2ec069fe24b496226b` | `FBX/TrafficBoxTruckA_complete_unity.fbx` | `05f3847d5c31fc85e5bcc322d3486546c219afad` | 20,063 / 10,765 / 4,796 / 2,591 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |
| 7 | **Bus A v4** | `07_Traffic_Bus_A` | `ec863fdfb66866330765d28cdab50febfae4eb45` | `FBX/TrafficBusA_complete_unity.fbx` | `2c94b87587081021a1f3f569e580396de0719797` | 34,506 / 15,126 / 6,210 / 2,999 | 8 / 8 / 8 / 6 | 1 errors, 0 warnings (check 1 = environment archive) | PASS |

## Shared textures (`shared/textures/`)

| File | SHA-1 |
|---|---|
| `TS_Atlas_BaseColor.png` | `478e55fdeb2f83b290ff174e0fd976ffc7cc727f` |
| `TS_Atlas_Metallic.png` | `e5de8cdb579c670c127fd4456960caae52387d20` |
| `TS_Atlas_MetallicSmoothness.png` | `4420edba6dba74cfb4206ec7f69796fca89e2ac4` |
| `TS_Atlas_Normal.png` | `3e023d1b7c1f969918e5eaf203c387159ba150fb` |
| `TS_Atlas_Roughness.png` | `9f845c3a1236bed57f596313fd3aa8143b9c401b` |
| `TS_Lights_BaseColor.png` | `5ef7f4fef04acb94350c9709e2f5c75009813127` |
| `TS_Lights_ChannelID.png` | `0efb36167fd6dbd5db7874fd8d841028da798430` |
| `TS_Lights_Emission.png` | `cf305913ac336e2fdb21acd1d0de4a67326fc942` |
| `TS_PaintFlake_Normal.png` | `eea9e5960841e08937eaef45c4346587376a70ac` |
| `TS_Tire_BaseColor.png` | `f9ce8bbfe8ed6d1e58bba5747126419969b9e4b1` |
| `TS_Tire_Normal.png` | `b9e1998b42e42c530aa504f2be840995ccde2f87` |
| `TS_Tire_Roughness.png` | `4cdea5f8c04a5fbcf305a32d3fb64d22986144e5` |
