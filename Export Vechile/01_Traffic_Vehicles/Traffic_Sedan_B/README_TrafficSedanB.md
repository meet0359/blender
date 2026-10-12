# Sedan B: Unity import notes (`TrafficSedanB`)

Release **Sedan B**, exported from the frozen `H_TrafficFleet/Traffic_Sedan_B/blend/trafficsedanb_09_export_ready.blend` (SHA-1 `a681c5bf5cc603f40394aeaafb3d109d6130fd37`, verified against `TS_SedanB_FINAL_FREEZE.md`). Exported 2026-10-10 09:45 with `ts_export.py` (unchanged FBX settings; source opened read-only, never saved).
**Not opened in Unity.** Runtime verification is P0-05 on the Unity machine. Follow `../README_UNITY_IMPORT.md` for importer and material setup.

## Files

| File | Objects | Bytes | SHA-1 |
|---|---|---|---|
| `FBX/TrafficSedanB_LOD0_unity_test.fbx` | 27 | 1,305,772 | `d45c180aecaa9ff0cb39db2cd7069f9ecae68411` |
| `FBX/TrafficSedanB_complete_unity.fbx` | 71 | 2,581,804 | `eef0b9310911077376dba57de606622438842855` |

Vehicle textures (`textures/`): `TS_SedanB_Body_AO_Grime.png`, `TS_SedanB_Body_Normal.png`, `TS_SedanB_Body_Normal_LOD1.png`. Shared textures: `../shared/textures/`. The FBX references textures by relative path (`../textures/`, `../../shared/textures/`); all 10 resolve inside this package.

## Size and orientation (Unity space, LOD0 incl. mirrors)

Length (Z) **4.9716 m**, width (X) **2.18 m**, height (Y) **1.4934 m**. Nose at +Z 2.4808, tail -2.4907, ground Y -0.0. Car_Root identity; all node rotations identity, scale 1, no negative scale.

## LODs

| LOD | Triangles | Objects | Materials |
|---|---|---|---|
| LOD0 | 17,987 | 16 | 8 |
| LOD1 | 8,739 | 16 | 8 |
| LOD2 | 4,012 | 16 | 8 |
| LOD3 | 1,746 | 12 | 6 |

Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 % (tune in P0-05).

## Wheels and centre of mass (Unity local space under Car_Root)

| Wheel | WheelColliderRef position | radius m | width m | Wheel pivots (all LODs) |
|---|---|---|---|---|
| FL | (-0.8125, 0.352, 1.62) | 0.352 | 0.245 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| FR | (0.8125, 0.352, 1.62) | 0.352 | 0.245 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RL | (-0.82, 0.352, -1.35) | 0.352 | 0.245 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RR | (0.82, 0.352, -1.35) | 0.352 | 0.245 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |

`CenterOfMass` (-0.0, 0.53, 0.08). Front wheels steer on `SteerPivot_FL/FR_LOD*` (yaw about local Y); wheels roll about local X.

## Colliders

| Collider | Triangles | Materials |
|---|---|---|
| `Collision_Body` | 94 | 0 |
| `Collision_Cabin` | 152 | 0 |
| `Collision_Front` | 152 | 0 |
| `Collision_Rear` | 166 | 0 |

Light channels on `Lights_LOD*`: Brake, DRL, Headlamp, Indicator_L, Indicator_R, Reverse, Tail.

## Materials (values from the frozen source; smoothness = 1 - roughness; colours linear)

| Material | LODs | Unity shader | Base | Metallic | Smoothness | Alpha | Coat | Carried by the FBX | Set manually |
|---|---|---|---|---|---|---|---|---|---|
| `TS_Atlas` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_Lens` | [0, 1, 2] | URP Lit, Surface Transparent | (0.92, 0.94, 0.96) | 0.0 | 0.99 | 0.1 | 0.0 | - | - |
| `TS_LensRed` | [0, 1, 2] | URP Lit, Surface Transparent | (0.42, 0.0, 0.006) | 0.0 | 0.98 | 0.55 | 0.0 | - | - |
| `TS_Lights` | [0, 1, 2, 3] | Emissive light-channel shader (Shader Graph; see README) | TS_Lights_BaseColor.png | 0.0 | 0.75 | 1.0 | 0.0 | DiffuseColor: TS_Lights_BaseColor.png | TS_Lights_Emission.png; TS_Lights_ChannelID.png (R x 15 = channel; point filter, no compression) |
| `TS_SedanB_Glass` | [0, 1, 2, 3] | URP Lit, Surface Transparent | (0.78, 0.84, 0.82) | 0.0 | 1.0 | 0.22 | 0.0 | - | - |
| `TS_SedanB_Interior` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_SedanB_Paint` | [0] | URP Complex Lit (clear coat) | PaintColour (0.15, 0.155, 0.165) x AO (R of AO_Grime), grime by G | 0.55 | 0.64 | 1.0 | 1.0 | NormalMap: TS_SedanB_Body_Normal.png | TS_SedanB_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_SedanB_Paint_Far` | [2, 3] | URP Complex Lit (clear coat) | PaintColour (0.15, 0.155, 0.165) | 0.55 | 0.64 | 1.0 | 1.0 | - | - |
| `TS_SedanB_Paint_LOD1` | [1] | URP Complex Lit (clear coat) | PaintColour (0.15, 0.155, 0.165) x AO (R of AO_Grime), grime by G | 0.55 | 0.64 | 1.0 | 1.0 | NormalMap: TS_SedanB_Body_Normal_LOD1.png | TS_SedanB_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_Tire` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Tire_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Tire_BaseColor.png; NormalMap: TS_Tire_Normal.png; ShininessExponent: TS_Tire_Roughness.png | smoothness = 1 - TS_Tire_Roughness (pack into a map alpha, or use the constant) |

Validation: SUMMARY: 1 errors, 0 warnings (`reports/TrafficSedanB_validation.txt`; the only failure, check 1, is the archived `environment/` folder, not this vehicle). FBX audit: PASS (`reports/TrafficSedanB_fbx_audit.json`).
