# Vortex R r1 — Unity import notes

**Revision r1 (preferred Unity import candidate).** Replaces the original Vortex R release (`vehicles/D_VortexR/`, kept frozen) for import. Only the normals of Trim_LOD1, Lights_LOD1, Interior_LOD1 and SteeringWheel_LOD1 changed (LOD1 carbon wing / rocker / diffuser shading tears removed); geometry, triangle counts, UVs, materials, rig, colliders, pivots and object names are identical. FBX file names are unchanged, so r1 is a drop-in replacement.

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/VortexR_complete_unity.fbx`: LOD0-3 + colliders + references (103 objects).
- `FBX/VortexR_LOD0_unity_test.fbx`: LOD0 only (quick check).
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
L x W x H 4.580 x 2.270 x 1.275 m (mirrors + wing endplates incl.; body width 2.09 m). Wheelbase 2.72 m, track 1.72 m front / 1.70 m rear. Tires 255/30 R20 front, 325/25 R21 rear.

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root      Body (incl. mirrors, panel gaps), Trim, Lights, Glass, Interior, SteeringWheel (LOD0-2)
 │   ├─ SteerPivot_FL / FR      yaw on local Y about the wheel centre (±25°)
 │   │   ├─ Wheel_FL / FR       roll on local X  → Tire, BrakeDisc (children, roll)   Caliper (child of the SteerPivot, steers, does not roll)
 │   ├─ Wheel_RL / RR           roll on local X  → Tire, BrakeDisc;  Caliper (sibling, static)
 ├─ Collision                   Collision_Front / Body / Cabin / Rear (convex)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
LOD3 has no separate brake hardware (a rotor disc is part of each wheel mesh). Doors are part of the body (shut lines modelled, not opening).
Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

## LODs
| LOD | triangles | ratio | objects | materials |
|---|---|---|---|---|
| LOD0 | 73,665 | 100% | 22 | 15 |
| LOD1 | 34,060 | 46% | 22 | 15 |
| LOD2 | 15,026 | 20% | 22 | 15 |
| LOD3 | 6,146 | 8% | 13 | 15 |

## Wheels (WheelCollider positions)
| Ref | Blender | Unity (local to Car_Root) | radius m | width m |
|---|---|---|---|---|
| FL | (0.86, -1.36, 0.339) | (-0.86, 0.339, 1.36) | 0.339 | 0.255 |
| FR | (-0.86, -1.36, 0.339) | (0.86, 0.339, 1.36) | 0.339 | 0.255 |
| RL | (0.85, 1.36, 0.348) | (-0.85, 0.348, -1.36) | 0.348 | 0.325 |
| RR | (-0.85, 1.36, 0.348) | (0.85, 0.348, -1.36) | 0.348 | 0.325 |

Drive visual wheels from `WheelCollider.GetWorldPose` (Unity mirrors X on import).

## Centre of mass
`CenterOfMass` Blender (0.0, 0.25, 0.38) → Unity local (-0.0, 0.38, -0.25). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Colliders
- `Collision_Body`: 168 tris, closed, convex
- `Collision_Cabin`: 166 tris, closed, convex
- `Collision_Front`: 184 tris, closed, convex
- `Collision_Rear`: 142 tris, closed, convex
- `Collision_Wing`: 14 tris, closed, convex
MeshCollider with **Convex ON**, renderers off, vehicle physics layer.

## Materials (15)
| Material | Unity setup |
|---|---|
| `VX_Paint` | Car paint, satin metallic deep violet: linear base (0.075, 0.028, 0.155), metallic 0.80, smoothness 0.64, coat 0.35 / coat smoothness 0.82. No texture: colour is runtime-swappable. |
| `VX_Palette` | Lit opaque. BaseMap VX_Palette_BaseColor; Metallic/Smoothness map VX_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps. 256 px swatch atlas: forged wheel + lip, acid-green caliper / accents, rotor, exhaust, mesh, gloss / satin black, alcantara, leather, aluminium, mirror, grille. |
| `VX_Carbon` | Lit opaque. VX_Carbon_BaseColor + VX_Carbon_Normal (2x2 twill, OpenGL, no flip), smoothness 0.7, clear coat 0.7. UVs are world-scale (0.25 m tile). |
| `VX_Tire` | Lit opaque. VX_Tire_BaseColor + VX_Tire_Normal (tread grooves, sipes, sidewall ring), smoothness 0.15. UV U = circumference, V = profile. |
| `VX_Glass` | Lit transparent, alpha 0.66, near-black tint, smoothness 0.98. Single sheet: no refraction. |
| `VX_LensClear` | Lit transparent, alpha 0.10, smoothness 0.98 (headlamp lenses). |
| `VX_LensRed` | Lit transparent, alpha 0.80, deep red (0.30, 0.0, 0.004): reads red in daylight and lit (Zero Gap R PB-1 lesson). |
| `VX_Display` | Lit + emission (0.55, 0.62, 0.70) x1.2 (digital cluster, wheel display); swap for a RenderTexture to drive live gauges. |
| `VX_LED_DRL` | Lit opaque + emission (0.82, 0.92, 1.0) x10.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `VX_LED_Headlamp` | Lit opaque + emission (0.95, 0.97, 1.0) x3.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `VX_LED_Tail` | Lit opaque + emission (1.0, 0.012, 0.015) x7.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `VX_LED_Brake` | Lit opaque + emission (1.0, 0.01, 0.012) x1.5. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `VX_LED_Indicator_L` | Lit opaque + emission (1.0, 0.32, 0.0) x0.7. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `VX_LED_Indicator_R` | Lit opaque + emission (1.0, 0.32, 0.0) x0.7. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `VX_LED_Reverse` | Lit opaque + emission (1.0, 1.0, 1.0) x0.3. RUNTIME CHANNEL: drive _EmissionColor intensity. |

Smoothness = 1 - roughness. Normal maps are OpenGL (+Y): Texture Type Normal map, no flip.
Light channels: `VX_LED_DRL` (boomerang blade + down-hook per side), `VX_LED_Headlamp` (three LED projector modules per side, low / high beam), `VX_LED_Tail` (three raked slashes per side + thin full-width thread), `VX_LED_Brake` (bar under each slash cluster + the third brake light on the wing trailing edge; raise to ~8 when braking), `VX_LED_Indicator_L` / `_R` (vehicle left / right, front + rear), `VX_LED_Reverse`.
