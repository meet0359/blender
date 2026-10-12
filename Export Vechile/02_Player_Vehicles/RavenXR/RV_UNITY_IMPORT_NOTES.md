# Raven XR — Unity import notes

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/RavenXR_complete_unity.fbx`: LOD0-3 + colliders + references (102 objects).
- `FBX/RavenXR_LOD0_unity_test.fbx`: LOD0 only (quick check).
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
L x W x H 4.521 x 2.046 x 1.320 m (mirrors incl.; body width ~1.98 m). Wheelbase 2.68 m, track 1.66 m front / 1.67 m rear. Tires 255/35 R19 front, 285/35 R19 rear. LHD (driver on vehicle left, Unity -X).

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root      Body (incl. mirrors, panel gaps), Trim, Lights, Glass, Interior, SteeringWheel (LOD0-2)
 │   ├─ SteerPivot_FL / FR      yaw on local Y about the wheel centre (±25°)
 │   │   ├─ Wheel_FL / FR       roll on local X  → Tire, BrakeDisc (children, roll)   Caliper (child of the SteerPivot, steers, does not roll)
 │   ├─ Wheel_RL / RR           roll on local X  → Tire, BrakeDisc;  Caliper (sibling, static)
 ├─ Collision                   Collision_Front / Body / Cabin / Rear (convex; Rear includes the deck spoiler)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
LOD3 has no separate brake hardware (a rotor disc is part of each wheel mesh). Doors are part of the body (shut lines modelled at LOD0; LOD1-3 are built from a groove-free body by design; doors do not open).
Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

## LODs
| LOD | triangles | ratio | objects | materials |
|---|---|---|---|---|
| LOD0 | 74,271 | 100% | 22 | 15 |
| LOD1 | 34,711 | 47% | 22 | 15 |
| LOD2 | 15,185 | 20% | 22 | 15 |
| LOD3 | 5,818 | 8% | 13 | 15 |

## Wheels (WheelCollider positions)
| Ref | Blender | Unity (local to Car_Root) | radius m | width m |
|---|---|---|---|---|
| FL | (0.83, -1.34, 0.331) | (-0.83, 0.331, 1.34) | 0.331 | 0.255 |
| FR | (-0.83, -1.34, 0.331) | (0.83, 0.331, 1.34) | 0.331 | 0.255 |
| RL | (0.835, 1.34, 0.341) | (-0.835, 0.341, -1.34) | 0.341 | 0.285 |
| RR | (-0.835, 1.34, 0.341) | (0.835, 0.341, -1.34) | 0.341 | 0.285 |

Drive visual wheels from `WheelCollider.GetWorldPose` (Unity mirrors X on import).

## Centre of mass
`CenterOfMass` Blender (0.0, -0.08, 0.44) → Unity local (-0.0, 0.44, 0.08). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Colliders
- `Collision_Body`: 186 tris, closed, convex
- `Collision_Cabin`: 148 tris, closed, convex
- `Collision_Front`: 176 tris, closed, convex
- `Collision_Rear`: 150 tris, closed, convex
MeshCollider with **Convex ON**, renderers off, vehicle physics layer.

## Materials (15)
| Material | Unity setup |
|---|---|
| `RV_Paint` | Car paint, dark emerald metallic with a glossy clear coat: linear base (0.008, 0.062, 0.040), metallic 0.78, smoothness 0.70, coat 0.6 / coat smoothness 0.94. Body-colour roof. No texture: colour is runtime-swappable. |
| `RV_Palette` | Lit opaque. BaseMap RV_Palette_BaseColor; Metallic/Smoothness map RV_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps. 256 px swatch atlas: dark forged wheel + lip, lug nuts, red caliper / red interior accents, rotor, exhaust, mesh, gloss / satin black, alcantara, leather, aluminium, mirror, grille. |
| `RV_Carbon` | Lit opaque. RV_Carbon_BaseColor + RV_Carbon_Normal (2x2 twill, OpenGL, no flip), smoothness 0.7, clear coat 0.7. UVs are world-scale (0.25 m tile). |
| `RV_Tire` | Lit opaque. RV_Tire_BaseColor + RV_Tire_Normal (tread grooves, sipes, sidewall ring), smoothness 0.15. UV U = circumference, V = profile. |
| `RV_Glass` | Lit transparent, alpha 0.66, near-black tint, smoothness 0.98. Single sheet: no refraction. |
| `RV_LensClear` | Lit transparent, alpha 0.10, smoothness 0.98 (headlamp lenses). |
| `RV_LensRed` | Lit transparent, alpha 0.80, deep red (0.30, 0.0, 0.004): reads red in daylight and lit (Zero Gap R PB-1 lesson). |
| `RV_Display` | Lit + emission (0.55, 0.62, 0.70) x1.2 (digital cluster, wheel display); swap for a RenderTexture to drive live gauges. |
| `RV_LED_DRL` | Lit opaque + emission (0.82, 0.92, 1.0) x10.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `RV_LED_Headlamp` | Lit opaque + emission (0.95, 0.97, 1.0) x3.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `RV_LED_Tail` | Lit opaque + emission (1.0, 0.012, 0.015) x7.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `RV_LED_Brake` | Lit opaque + emission (1.0, 0.01, 0.012) x1.5. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `RV_LED_Indicator_L` | Lit opaque + emission (1.0, 0.32, 0.0) x0.7. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `RV_LED_Indicator_R` | Lit opaque + emission (1.0, 0.32, 0.0) x0.7. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `RV_LED_Reverse` | Lit opaque + emission (1.0, 1.0, 1.0) x0.3. RUNTIME CHANNEL: drive _EmissionColor intensity. |

Smoothness = 1 - roughness. Normal maps are OpenGL (+Y): Texture Type Normal map, no flip.
Light channels: `RV_LED_DRL` (upper blade + inboard fang per headlamp), `RV_LED_Headlamp` (two projector modules per side, low / high beam), `RV_LED_Tail` (chevron: upper + lower blade + tip per side), `RV_LED_Brake` (inner chevron fill per side + third brake light on the deck-spoiler trailing edge; raise to ~8 when braking), `RV_LED_Indicator_L` / `_R` (vehicle left / right; amber strip at the outer base of each headlamp + amber segment inside each chevron), `RV_LED_Reverse` (lower rear lamps above the valance). Tail lenses use `RV_LensRed` (reads red in daylight).
