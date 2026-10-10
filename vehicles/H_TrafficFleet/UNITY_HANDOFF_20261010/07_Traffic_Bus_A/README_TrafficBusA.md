# Bus A v4: Unity import notes (`TrafficBusA`)

Release **Bus A v4**, exported from the frozen `H_TrafficFleet/Traffic_Bus_A/blend/trafficbusa_09_export_ready.blend` (SHA-1 `ec863fdfb66866330765d28cdab50febfae4eb45`, verified against `TS_BusA_FINAL_FREEZE.md`). Exported 2026-10-10 09:45 with `ts_export.py` (unchanged FBX settings; source opened read-only, never saved).
**Not opened in Unity.** Runtime verification is P0-05 on the Unity machine. Follow `../README_UNITY_IMPORT.md` for importer and material setup.

## Files

| File | Objects | Bytes | SHA-1 |
|---|---|---|---|
| `FBX/TrafficBusA_LOD0_unity_test.fbx` | 27 | 2,190,220 | `b9bd14e47dcfa6bd1efe7f4ac41547c32f0ac94b` |
| `FBX/TrafficBusA_complete_unity.fbx` | 71 | 3,997,036 | `2c94b87587081021a1f3f569e580396de0719797` |

Vehicle textures (`textures/`): `TS_BusA_Body_AO_Grime.png`, `TS_BusA_Body_Normal.png`, `TS_BusA_Body_Normal_LOD1.png`. Shared textures: `../shared/textures/`. The FBX references textures by relative path (`../textures/`, `../../shared/textures/`); all 10 resolve inside this package.

## Size and orientation (Unity space, LOD0 incl. mirrors)

Length (Z) **12.0075 m**, width (X) **2.984 m**, height (Y) **3.198 m**. Nose at +Z 5.9935, tail -6.014, ground Y -0.0. Car_Root identity; all node rotations identity, scale 1, no negative scale.

## LODs

| LOD | Triangles | Objects | Materials |
|---|---|---|---|
| LOD0 | 34,506 | 16 | 8 |
| LOD1 | 15,126 | 16 | 8 |
| LOD2 | 6,210 | 16 | 8 |
| LOD3 | 2,999 | 12 | 6 |

Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 % (tune in P0-05).

## Wheels and centre of mass (Unity local space under Car_Root)

| Wheel | WheelColliderRef position | radius m | width m | Wheel pivots (all LODs) |
|---|---|---|---|---|
| FL | (-1.05, 0.478, 3.3) | 0.478 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| FR | (1.05, 0.478, 3.3) | 0.478 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RL | (-0.95, 0.478, -2.7) | 0.478 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RR | (0.95, 0.478, -2.7) | 0.478 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |

`CenterOfMass` (-0.0, 1.1, -0.3). Front wheels steer on `SteerPivot_FL/FR_LOD*` (yaw about local Y); wheels roll about local X.

## Colliders

| Collider | Triangles | Materials |
|---|---|---|
| `Collision_Body` | 154 | 0 |
| `Collision_Cabin` | 128 | 0 |
| `Collision_Front` | 180 | 0 |
| `Collision_Rear` | 174 | 0 |

Light channels on `Lights_LOD*`: Brake, DRL, Headlamp, Indicator_L, Indicator_R, Marker, Reverse, Tail.

## Materials (values from the frozen source; smoothness = 1 - roughness; colours linear)

| Material | LODs | Unity shader | Base | Metallic | Smoothness | Alpha | Coat | Carried by the FBX | Set manually |
|---|---|---|---|---|---|---|---|---|---|
| `TS_Atlas` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_BusA_Glass` | [0, 1, 2, 3] | URP Lit, Surface Transparent | (0.78, 0.84, 0.82) | 0.0 | 1.0 | 0.22 | 0.0 | - | - |
| `TS_BusA_Interior` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_BusA_Paint` | [0] | URP Complex Lit (clear coat) | PaintColour (0.5, 0.3, 0.04) x AO (R of AO_Grime), grime by G | 0.55 | 0.64 | 1.0 | 1.0 | NormalMap: TS_BusA_Body_Normal.png | TS_BusA_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_BusA_Paint_Far` | [2, 3] | URP Complex Lit (clear coat) | PaintColour (0.5, 0.3, 0.04) | 0.55 | 0.64 | 1.0 | 1.0 | - | - |
| `TS_BusA_Paint_LOD1` | [1] | URP Complex Lit (clear coat) | PaintColour (0.5, 0.3, 0.04) x AO (R of AO_Grime), grime by G | 0.55 | 0.64 | 1.0 | 1.0 | NormalMap: TS_BusA_Body_Normal_LOD1.png | TS_BusA_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_Lens` | [0, 1, 2] | URP Lit, Surface Transparent | (0.92, 0.94, 0.96) | 0.0 | 0.99 | 0.1 | 0.0 | - | - |
| `TS_LensRed` | [0, 1, 2] | URP Lit, Surface Transparent | (0.42, 0.0, 0.006) | 0.0 | 0.98 | 0.55 | 0.0 | - | - |
| `TS_Lights` | [0, 1, 2, 3] | Emissive light-channel shader (Shader Graph; see README) | TS_Lights_BaseColor.png | 0.0 | 0.75 | 1.0 | 0.0 | DiffuseColor: TS_Lights_BaseColor.png | TS_Lights_Emission.png; TS_Lights_ChannelID.png (R x 15 = channel; point filter, no compression) |
| `TS_Tire` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Tire_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Tire_BaseColor.png; NormalMap: TS_Tire_Normal.png; ShininessExponent: TS_Tire_Roughness.png | smoothness = 1 - TS_Tire_Roughness (pack into a map alpha, or use the constant) |

Validation: SUMMARY: 1 errors, 0 warnings (`reports/TrafficBusA_validation.txt`; the only failure, check 1, is the archived `environment/` folder, not this vehicle). FBX audit: PASS (`reports/TrafficBusA_fbx_audit.json`).
