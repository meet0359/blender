# Box Truck A r7: Unity import notes (`TrafficBoxTruckA`)

Release **Box Truck A r7**, exported from the frozen `H_TrafficFleet/Traffic_Box_Truck_A/blend/trafficboxtrucka_09_export_ready.blend` (SHA-1 `7ef36071193fa30a56c05a2ec069fe24b496226b`, verified against `TS_BoxTruckA_FINAL_FREEZE.md`). Exported 2026-10-10 09:45 with `ts_export.py` (unchanged FBX settings; source opened read-only, never saved).
**Not opened in Unity.** Runtime verification is P0-05 on the Unity machine. Follow `../README_UNITY_IMPORT.md` for importer and material setup.

## Files

| File | Objects | Bytes | SHA-1 |
|---|---|---|---|
| `FBX/TrafficBoxTruckA_LOD0_unity_test.fbx` | 27 | 1,359,452 | `689376d2a659effcc00089d870a67a7c203587f1` |
| `FBX/TrafficBoxTruckA_complete_unity.fbx` | 71 | 2,607,948 | `05f3847d5c31fc85e5bcc322d3486546c219afad` |

Vehicle textures (`textures/`): `TS_BoxTruckA_Body_AO_Grime.png`, `TS_BoxTruckA_Body_Normal.png`, `TS_BoxTruckA_Body_Normal_LOD1.png`. Shared textures: `../shared/textures/`. The FBX references textures by relative path (`../textures/`, `../../shared/textures/`); all 10 resolve inside this package.

## Size and orientation (Unity space, LOD0 incl. mirrors)

Length (Z) **7.07 m**, width (X) **2.544 m**, height (Y) **3.254 m**. Nose at +Z 3.565, tail -3.505, ground Y -0.0. Car_Root identity; all node rotations identity, scale 1, no negative scale.

## LODs

| LOD | Triangles | Objects | Materials |
|---|---|---|---|
| LOD0 | 20,063 | 16 | 8 |
| LOD1 | 10,765 | 16 | 8 |
| LOD2 | 4,796 | 16 | 8 |
| LOD3 | 2,591 | 12 | 6 |

Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 % (tune in P0-05).

## Wheels and centre of mass (Unity local space under Car_Root)

| Wheel | WheelColliderRef position | radius m | width m | Wheel pivots (all LODs) |
|---|---|---|---|---|
| FL | (-0.84, 0.405, 2.3) | 0.405 | 0.225 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| FR | (0.84, 0.405, 2.3) | 0.405 | 0.225 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RL | (-0.84, 0.405, -1.55) | 0.405 | 0.225 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RR | (0.84, 0.405, -1.55) | 0.405 | 0.225 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |

`CenterOfMass` (-0.0, 1.1, 0.4). Front wheels steer on `SteerPivot_FL/FR_LOD*` (yaw about local Y); wheels roll about local X.

## Colliders

| Collider | Triangles | Materials |
|---|---|---|
| `Collision_Body` | 76 | 0 |
| `Collision_Cabin` | 128 | 0 |
| `Collision_Front` | 174 | 0 |
| `Collision_Rear` | 92 | 0 |

Light channels on `Lights_LOD*`: Brake, DRL, Headlamp, Indicator_L, Indicator_R, Marker, Reverse, Tail.

## Materials (values from the frozen source; smoothness = 1 - roughness; colours linear)

| Material | LODs | Unity shader | Base | Metallic | Smoothness | Alpha | Coat | Carried by the FBX | Set manually |
|---|---|---|---|---|---|---|---|---|---|
| `TS_Atlas` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_BoxTruckA_Glass` | [0, 1, 2, 3] | URP Lit, Surface Transparent | (0.78, 0.84, 0.82) | 0.0 | 1.0 | 0.22 | 0.0 | - | - |
| `TS_BoxTruckA_Interior` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_BoxTruckA_Paint` | [0] | URP Complex Lit (clear coat) | PaintColour (0.62, 0.62, 0.6) x AO (R of AO_Grime), grime by G | 0.0 | 0.6 | 1.0 | 0.55 | NormalMap: TS_BoxTruckA_Body_Normal.png | TS_BoxTruckA_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_BoxTruckA_Paint_Far` | [2, 3] | URP Complex Lit (clear coat) | PaintColour (0.62, 0.62, 0.6) | 0.0 | 0.6 | 1.0 | 0.55 | - | - |
| `TS_BoxTruckA_Paint_LOD1` | [1] | URP Complex Lit (clear coat) | PaintColour (0.62, 0.62, 0.6) x AO (R of AO_Grime), grime by G | 0.0 | 0.6 | 1.0 | 0.55 | NormalMap: TS_BoxTruckA_Body_Normal_LOD1.png | TS_BoxTruckA_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_Lens` | [0, 1, 2] | URP Lit, Surface Transparent | (0.92, 0.94, 0.96) | 0.0 | 0.99 | 0.1 | 0.0 | - | - |
| `TS_LensRed` | [0, 1, 2] | URP Lit, Surface Transparent | (0.42, 0.0, 0.006) | 0.0 | 0.98 | 0.55 | 0.0 | - | - |
| `TS_Lights` | [0, 1, 2, 3] | Emissive light-channel shader (Shader Graph; see README) | TS_Lights_BaseColor.png | 0.0 | 0.75 | 1.0 | 0.0 | DiffuseColor: TS_Lights_BaseColor.png | TS_Lights_Emission.png; TS_Lights_ChannelID.png (R x 15 = channel; point filter, no compression) |
| `TS_Tire` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Tire_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Tire_BaseColor.png; NormalMap: TS_Tire_Normal.png; ShininessExponent: TS_Tire_Roughness.png | smoothness = 1 - TS_Tire_Roughness (pack into a map alpha, or use the constant) |

Validation: SUMMARY: 1 errors, 0 warnings (`reports/TrafficBoxTruckA_validation.txt`; the only failure, check 1, is the archived `environment/` folder, not this vehicle). FBX audit: PASS (`reports/TrafficBoxTruckA_fbx_audit.json`).
