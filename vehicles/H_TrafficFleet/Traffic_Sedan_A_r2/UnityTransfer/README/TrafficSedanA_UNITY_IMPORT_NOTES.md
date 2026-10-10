# Traffic_Sedan_A_r2 — Unity import notes

**Unity owns** controller, physics, WheelColliders, prefab, LOD Group, shaders, lighting, audio and profiling. Blender delivers geometry, pivots, reference empties, colliders, materials, textures and FBX. **Nothing here was opened in Unity; no frame-rate claims.**

## Files
- `FBX/TrafficSedanA_complete_unity.fbx` (LOD0-3 + colliders + references, 71 objects); `FBX/TrafficSedanA_LOD0_unity_test.fbx` (LOD0 only).
- `Textures/` — vehicle bakes: `TS_SedanA_Body_Normal` (2048, tangent / MikkTSpace, LOD0), `TS_SedanA_Body_Normal_LOD1` (1024), `TS_SedanA_Body_AO_Grime` (1024; R = ambient occlusion, G = road-grime mask).
- `Textures/Shared/` — fleet library (reused by every traffic vehicle): `TS_Atlas_*` (2048 8x8 material atlas), `TS_Tire_*`, `TS_PaintFlake_Normal`, `TS_Lights_*` (light mask).

## Importer
Scale 1, Convert Units ON, **Bake Axis Conversion OFF** (axes baked; Car_Root identity). Normals: Import. Tangents: Calculate (MikkTSpace — required for the baked body normal map). Animation None. Generate Colliders OFF.
Blender (x, y, z) -> Unity (-x, z, -y): forward -Y -> +Z, up +Z -> +Y, vehicle left +X -> -X.

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root     Body (paint shell incl. mirrors + antenna), Glass, Trim (atlas), Lights (emitters + lenses), Interior
 │   ├─ SteerPivot_FL / FR     yaw on local Y (±25°) → Wheel_FL / FR (rim + tire + disc, roll on local X), Caliper_FL / FR (steers, does not roll)
 │   ├─ Wheel_RL / RR          roll on local X;  Caliper_RL / RR static
 ├─ Collision                  Collision_Front / Body / Cabin / Rear (convex MeshColliders, renderers off)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 %.

## LODs
| LOD | triangles | ratio | materials | draw calls |
|---|---|---|---|---|
| LOD0 | 14,970 | 100% | 7 | 19 |
| LOD1 | 7,746 | 52% | 7 | 19 |
| LOD2 | 3,527 | 24% | 7 | 19 |
| LOD3 | 1,375 | 9% | 5 | 13 |

## Wheels / centre of mass
| Ref | Blender | Unity | radius m | width m |
|---|---|---|---|---|
| FL | (0.78, -1.35, 0.316) | (-0.78, 0.316, 1.35) | 0.316 | 0.205 |
| FR | (-0.78, -1.35, 0.316) | (0.78, 0.316, 1.35) | 0.316 | 0.205 |
| RL | (0.7775, 1.35, 0.316) | (-0.7775, 0.316, -1.35) | 0.316 | 0.205 |
| RR | (-0.7775, 1.35, 0.316) | (0.7775, 0.316, -1.35) | 0.316 | 0.205 |

`CenterOfMass` Blender (0.0, -0.22, 0.52) → Unity (-0.0, 0.52, 0.22) (front-engine FWD bias). `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Materials (7 at LOD0; paint is one instance per colour)
| Material | Unity setup |
|---|---|
| `TS_SedanA_Paint` | Lit clear-coat (or URP Complex Lit): BaseColor = paint colour × AO (R of `TS_SedanA_Body_AO_Grime`), lerp to grime colour (0.11, 0.10, 0.085) by G × 0.55; Normal = `TS_SedanA_Body_Normal`; detail normal `TS_PaintFlake_Normal` tiling 60, strength 0.15; Metallic 0.55, Smoothness 0.64; Clear coat 1.0, coat smoothness 0.955 (grime lowers it). |
| `TS_SedanA_Paint_LOD1` | same, Normal = `TS_SedanA_Body_Normal_LOD1` |
| `TS_SedanA_Paint_Far` | same without normal / AO maps (LOD2-3) |
| `TS_Atlas` | Lit opaque. BaseMap `TS_Atlas_BaseColor`; Metallic/Smoothness `TS_Atlas_MetallicSmoothness` (R metal, A smoothness); Normal `TS_Atlas_Normal`. Bilinear, mip-maps on, **no texture wrap across cells** (UVs are inset 6 %). |
| `TS_Tire` | Lit opaque. `TS_Tire_BaseColor` + `TS_Tire_Normal` (tread blocks, sipes, sidewall rings, fictional lettering band); smoothness 1 - `TS_Tire_Roughness`. UV U wraps around the tire (repeat). |
| `TS_Glass` | Lit transparent, base (0.50, 0.58, 0.56) **alpha 0.35**, smoothness 1.0 — tinted, see-through. |
| `TS_Lens` / `TS_LensRed` | Lit transparent: clear alpha 0.10; red (0.42, 0, 0.006) alpha 0.55 — reads red in daylight. |
| `TS_Lights` | **One emissive material for all channels.** BaseMap `TS_Lights_BaseColor` (off look), Emission `TS_Lights_Emission`; channel = `TS_Lights_ChannelID` R × 15 → 0 DRL, 1 Headlamp, 2 Tail, 3 Brake, 4 Indicator_L, 5 Indicator_R, 6 Reverse, 7 Marker. Drive a per-channel intensity array (MaterialPropertyBlock / small shader): one draw call, independent channels. Suggested intensities: DRL 12, Headlamp 4, Tail 5, Brake 8 (on), Indicators 1.2 (blink), Reverse 0.5. |

## Paint variants (material instances, no extra meshes)
| Variant | Linear base RGB | Metallic |
|---|---|---|
| Arctic white (solid) | (0.80, 0.80, 0.78) | 0.0 |
| Silver metallic | (0.55, 0.57, 0.59) | 0.55 |
| Graphite metallic | (0.090, 0.095, 0.100) | 0.55 |
| Black (solid) | (0.012, 0.012, 0.013) | 0.0 |
| Deep red metallic | (0.30, 0.012, 0.015) | 0.55 |
| Steel blue metallic (review) | (0.060, 0.115, 0.220) | 0.55 |
