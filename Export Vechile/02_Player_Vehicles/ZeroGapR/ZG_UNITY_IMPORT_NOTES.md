# Zero Gap R — Unity import notes

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/ZeroGapR_complete_unity.fbx`: LOD0-3 + colliders + references (110 objects).
- `FBX/ZeroGapR_LOD0_unity_test.fbx`: LOD0 only (quick check).
- `Textures/`: 7 PNGs (palette 256 px x 3, carbon 1 K x 2, tire 1 K x 2). Copy next to the FBX folder structure or reassign by name.

## Importer
Scale Factor 1, Convert Units ON, **Bake Axis Conversion OFF** (axes are baked in the file; Car_Root identity). Normals Import, Tangents Import / Calculate (MikkTSpace). Animation Type None. Generate Colliders OFF.

| | Blender | Unity |
|---|---|---|
| forward | -Y | **+Z** |
| up | +Z | **+Y** |
| vehicle left | +X | **-X** |
| point | (x, y, z) | (-x, z, -y) |

## Dimensions
L x W x H 4.460 x 2.006 x 1.200 m (mirrors incl.). Wheelbase 2.70 m, track 1.65 m front / 1.67 m rear.

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root      Body, Door_L, Door_R, Trim, Lights, Glass, Interior, SteeringWheel (LOD0-2)
 │   ├─ SteerPivot_FL / FR      yaw on local Y about the wheel centre (±25°)
 │   │   ├─ Wheel_FL / FR       roll on local X  → Tire, BrakeDisc (children, roll)   Caliper (child of the SteerPivot, steers, does not roll)
 │   ├─ Wheel_RL / RR           roll on local X  → Tire, BrakeDisc;  Caliper (sibling, static)
 ├─ Collision                   Collision_Front / Body / Cabin / Rear (convex)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
LOD3 has no separate brake hardware (a rotor disc is part of each wheel mesh). Door_L / Door_R pivots sit on the front (hinge) edge.
Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

## LODs
| LOD | triangles | ratio | objects | materials |
|---|---|---|---|---|
| LOD0 | 89,681 | 100% | 24 | 15 |
| LOD1 | 44,794 | 50% | 24 | 15 |
| LOD2 | 20,372 | 23% | 24 | 15 |
| LOD3 | 6,513 | 7% | 15 | 15 |

## Wheels (WheelCollider positions)
| Ref | Blender | Unity (local to Car_Root) | radius m | width m |
|---|---|---|---|---|
| FL | (0.825, -1.35, 0.345) | (-0.825, 0.345, 1.35) | 0.3445 | 0.296 |
| FR | (-0.825, -1.35, 0.345) | (0.825, 0.345, 1.35) | 0.3445 | 0.296 |
| RL | (0.835, 1.35, 0.365) | (-0.835, 0.365, -1.35) | 0.3645 | 0.336 |
| RR | (-0.835, 1.35, 0.365) | (0.835, 0.365, -1.35) | 0.3645 | 0.336 |

Drive visual wheels from `WheelCollider.GetWorldPose` (Unity mirrors X on import).

## Centre of mass
`CenterOfMass` Blender (0.0, 0.22, 0.37) → Unity local (-0.0, 0.37, -0.22). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Colliders
- `Collision_Body`: 52 tris, closed, convex
- `Collision_Cabin`: 192 tris, closed, convex
- `Collision_Front`: 162 tris, closed, convex
- `Collision_Rear`: 170 tris, closed, convex
MeshCollider with **Convex ON**, renderers off, vehicle physics layer.

## Materials (15)
| Material | Unity setup |
|---|---|
| `ZG_Paint` | Car paint, clear coat. Linear base (0.58, 0.018, 0.024), metallic 0.55, smoothness 0.72, coat 1.0 / coat smoothness 0.97. No texture: colour is runtime-swappable. |
| `ZG_Palette` | Lit opaque. BaseMap ZG_Palette_BaseColor; Metallic/Smoothness map ZG_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps (256 px swatch atlas: trim, black plastic, chrome, wheel metal, caliper, rotor, interior leather / alcantara / plastic / metal, grille, mirror, exhaust). |
| `ZG_Carbon` | Lit opaque. ZG_Carbon_BaseColor + ZG_Carbon_Normal (OpenGL, no flip), smoothness 0.7, clear coat 0.6. UVs are world-scale (0.25 m tile). |
| `ZG_Tire` | Lit opaque. ZG_Tire_BaseColor + ZG_Tire_Normal (sidewall lettering baked), smoothness 0.18. |
| `ZG_Glass` | Lit transparent, alpha 0.42, near-black tint (0.015, 0.02, 0.025), smoothness 0.98. Single thin sheet: no refraction, no double-sided darkening. |
| `ZG_LensClear` | Lit transparent, alpha 0.12, smoothness 0.98 (headlight outer lens). |
| `ZG_LensRed` | Lit transparent, alpha 0.55, smoked red (0.22, 0.004, 0.008) (tail-light outer lens). |
| `ZG_Display` | Lit + emission (0.10, 0.35, 0.60) x1.4 (cluster / screen); swap for a RenderTexture to drive live gauges. |
| `ZG_LED_DRL` | Lit opaque + emission (0.8, 0.9, 1.0) x9.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `ZG_LED_Headlamp` | Lit opaque + emission (0.95, 0.97, 1.0) x2.5. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `ZG_LED_Tail` | Lit opaque + emission (1.0, 0.015, 0.02) x7.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `ZG_LED_Brake` | Lit opaque + emission (1.0, 0.01, 0.015) x1.2. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `ZG_LED_Indicator_L` | Lit opaque + emission (1.0, 0.32, 0.0) x0.6. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `ZG_LED_Indicator_R` | Lit opaque + emission (1.0, 0.32, 0.0) x0.6. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `ZG_LED_Reverse` | Lit opaque + emission (1.0, 1.0, 1.0) x0.25. RUNTIME CHANNEL: drive _EmissionColor intensity. |

Smoothness = 1 - roughness. Normal maps are OpenGL (+Y): Texture Type Normal map, no flip.
Light channels: `ZG_LED_DRL` (daytime running, front blades + headlamp DRL), `ZG_LED_Headlamp` (projectors, low / high beam), `ZG_LED_Tail` (tail bars), `ZG_LED_Brake` (brake segments, raise to ~8 when braking), `ZG_LED_Indicator_L` / `_R` (vehicle left / right, front + rear, blink independently), `ZG_LED_Reverse`.
