# SUV B v3: Unity import notes (`TrafficSUVB`)

Release **SUV B v3**, exported from the frozen `H_TrafficFleet/Traffic_SUV_B/blend/trafficsuvb_09_export_ready.blend` (SHA-1 `cc4d2ae0a7493cd22ccf44f893b731404141f12c`, verified against `TS_SUVB_FINAL_FREEZE.md`). Exported 2026-10-10 09:45 with `ts_export.py` (unchanged FBX settings; source opened read-only, never saved).
**Not opened in Unity.** Runtime verification is P0-05 on the Unity machine. Follow `../README_UNITY_IMPORT.md` for importer and material setup.

## Files

| File | Objects | Bytes | SHA-1 |
|---|---|---|---|
| `FBX/TrafficSUVB_LOD0_unity_test.fbx` | 27 | 1,437,420 | `27d3b723e8fb10985d2173227bba2183b88fc196` |
| `FBX/TrafficSUVB_complete_unity.fbx` | 71 | 2,836,636 | `2f3836ff6185883f98e2eec1dbc0db265aafd407` |

Vehicle textures (`textures/`): `TS_SUVB_Body_AO_Grime.png`, `TS_SUVB_Body_Normal.png`, `TS_SUVB_Body_Normal_LOD1.png`. Shared textures: `../shared/textures/`. The FBX references textures by relative path (`../textures/`, `../../shared/textures/`); all 10 resolve inside this package.

## Size and orientation (Unity space, LOD0 incl. mirrors)

Length (Z) **4.9783 m**, width (X) **2.3 m**, height (Y) **1.8109 m**. Nose at +Z 2.4943, tail -2.484, ground Y -0.0. Car_Root identity; all node rotations identity, scale 1, no negative scale.

## LODs

| LOD | Triangles | Objects | Materials |
|---|---|---|---|
| LOD0 | 19,840 | 16 | 8 |
| LOD1 | 9,566 | 16 | 8 |
| LOD2 | 4,325 | 16 | 8 |
| LOD3 | 1,939 | 12 | 6 |

Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 % (tune in P0-05).

## Wheels and centre of mass (Unity local space under Car_Root)

| Wheel | WheelColliderRef position | radius m | width m | Wheel pivots (all LODs) |
|---|---|---|---|---|
| FL | (-0.84, 0.391, 1.55) | 0.391 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| FR | (0.84, 0.391, 1.55) | 0.391 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RL | (-0.845, 0.391, -1.43) | 0.391 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |
| RR | (0.845, 0.391, -1.43) | 0.391 | 0.275 | on the ref (max dev 0.0e+00 m), LODs [0, 1, 2, 3] |

`CenterOfMass` (-0.0, 0.7, 0.1). Front wheels steer on `SteerPivot_FL/FR_LOD*` (yaw about local Y); wheels roll about local X.

## Colliders

| Collider | Triangles | Materials |
|---|---|---|
| `Collision_Body` | 68 | 0 |
| `Collision_Cabin` | 170 | 0 |
| `Collision_Front` | 200 | 0 |
| `Collision_Rear` | 190 | 0 |

Light channels on `Lights_LOD*`: Brake, DRL, Headlamp, Indicator_L, Indicator_R, Reverse, Tail.

## Materials (values from the frozen source; smoothness = 1 - roughness; colours linear)

| Material | LODs | Unity shader | Base | Metallic | Smoothness | Alpha | Coat | Carried by the FBX | Set manually |
|---|---|---|---|---|---|---|---|---|---|
| `TS_Atlas` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_Lens` | [0, 1, 2] | URP Lit, Surface Transparent | (0.92, 0.94, 0.96) | 0.0 | 0.99 | 0.1 | 0.0 | - | - |
| `TS_LensRed` | [0, 1, 2] | URP Lit, Surface Transparent | (0.42, 0.0, 0.006) | 0.0 | 0.98 | 0.55 | 0.0 | - | - |
| `TS_Lights` | [0, 1, 2, 3] | Emissive light-channel shader (Shader Graph; see README) | TS_Lights_BaseColor.png | 0.0 | 0.75 | 1.0 | 0.0 | DiffuseColor: TS_Lights_BaseColor.png | TS_Lights_Emission.png; TS_Lights_ChannelID.png (R x 15 = channel; point filter, no compression) |
| `TS_SUVB_Glass` | [0, 1, 2, 3] | URP Lit, Surface Transparent | (0.78, 0.84, 0.82) | 0.0 | 1.0 | 0.22 | 0.0 | - | - |
| `TS_SUVB_Interior` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Atlas_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Atlas_BaseColor.png; NormalMap: TS_Atlas_Normal.png; ShininessExponent: TS_Atlas_Roughness.png; ReflectionFactor: TS_Atlas_Metallic.png | TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness) |
| `TS_SUVB_Paint` | [0] | URP Complex Lit (clear coat) | PaintColour (0.62, 0.62, 0.6) x AO (R of AO_Grime), grime by G | 0.55 | 0.64 | 1.0 | 1.0 | NormalMap: TS_SUVB_Body_Normal.png | TS_SUVB_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_SUVB_Paint_Far` | [2, 3] | URP Complex Lit (clear coat) | PaintColour (0.62, 0.62, 0.6) | 0.55 | 0.64 | 1.0 | 1.0 | - | - |
| `TS_SUVB_Paint_LOD1` | [1] | URP Complex Lit (clear coat) | PaintColour (0.62, 0.62, 0.6) x AO (R of AO_Grime), grime by G | 0.55 | 0.64 | 1.0 | 1.0 | NormalMap: TS_SUVB_Body_Normal_LOD1.png | TS_SUVB_Body_AO_Grime.png; TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15) |
| `TS_Tire` | [0, 1, 2, 3] | URP Lit (opaque) | TS_Tire_BaseColor.png | 0.0 | 0.5 | 1.0 | 0.0 | DiffuseColor: TS_Tire_BaseColor.png; NormalMap: TS_Tire_Normal.png; ShininessExponent: TS_Tire_Roughness.png | smoothness = 1 - TS_Tire_Roughness (pack into a map alpha, or use the constant) |

Validation: SUMMARY: 1 errors, 0 warnings (`reports/TrafficSUVB_validation.txt`; the only failure, check 1, is the archived `environment/` folder, not this vehicle). FBX audit: PASS (`reports/TrafficSUVB_fbx_audit.json`).
