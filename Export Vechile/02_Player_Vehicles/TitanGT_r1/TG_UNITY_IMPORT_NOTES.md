# Titan GT r1 — Unity import notes

**Revision r1 (preferred Unity import candidate).** Replaces the original Titan GT release (`vehicles/C_TitanGT/`, kept frozen) for import. LOD0, rig, colliders, materials, textures, pivots and object names are identical to the original; Body_LOD1-3 were rebuilt groove-free (no panel-gap shading tears), Trim_LOD3 arch liners come from LOD2, and Trim_LOD1 uses its own smooth normals. FBX file names are unchanged so r1 is a drop-in replacement.

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/TitanGT_complete_unity.fbx`: LOD0-3 + colliders + references (102 objects).
- `FBX/TitanGT_LOD0_unity_test.fbx`: LOD0 only (quick check).
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
L x W x H 4.814 x 2.230 x 1.272 m (mirrors incl.; body width 2.00 m). Wheelbase 2.82 m, track 1.69 m front / 1.71 m rear. Tires 265/35 R20 front, 305/30 R21 rear.

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
LOD3 has no separate brake hardware (a rotor disc is part of each wheel mesh). Doors are part of the body (shut lines modelled at LOD0; LOD1-3 are groove-free by design, not opening).
Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

## LODs
| LOD | triangles | ratio | objects | materials |
|---|---|---|---|---|
| LOD0 | 77,370 | 100% | 22 | 15 |
| LOD1 | 39,752 | 51% | 22 | 15 |
| LOD2 | 18,527 | 24% | 22 | 15 |
| LOD3 | 7,729 | 10% | 13 | 15 |

## Wheels (WheelCollider positions)
| Ref | Blender | Unity (local to Car_Root) | radius m | width m |
|---|---|---|---|---|
| FL | (0.845, -1.41, 0.347) | (-0.845, 0.347, 1.41) | 0.347 | 0.265 |
| FR | (-0.845, -1.41, 0.347) | (0.845, 0.347, 1.41) | 0.347 | 0.265 |
| RL | (0.855, 1.41, 0.358) | (-0.855, 0.358, -1.41) | 0.358 | 0.305 |
| RR | (-0.855, 1.41, 0.358) | (0.855, 0.358, -1.41) | 0.358 | 0.305 |

Drive visual wheels from `WheelCollider.GetWorldPose` (Unity mirrors X on import).

## Centre of mass
`CenterOfMass` Blender (0.0, 0.15, 0.42) → Unity local (-0.0, 0.42, -0.15). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Colliders
- `Collision_Body`: 182 tris, closed, convex
- `Collision_Cabin`: 184 tris, closed, convex
- `Collision_Front`: 168 tris, closed, convex
- `Collision_Rear`: 150 tris, closed, convex
MeshCollider with **Convex ON**, renderers off, vehicle physics layer.

## Materials (15)
| Material | Unity setup |
|---|---|
| `TG_Paint` | Car paint, clear coat. Midnight-blue metallic: linear base (0.012, 0.032, 0.085), metallic 0.62, smoothness 0.70, coat 1.0 / coat smoothness 0.975. No texture: colour is runtime-swappable. |
| `TG_Palette` | Lit opaque. BaseMap TG_Palette_BaseColor; Metallic/Smoothness map TG_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps. 256 px swatch atlas: graphite + machined wheel, bronze caliper, rotor, exhaust, dark chrome, gloss / satin black, cognac + black leather, alcantara, aluminium, mirror, grille. |
| `TG_Carbon` | Lit opaque. TG_Carbon_BaseColor + TG_Carbon_Normal (2x2 twill, OpenGL, no flip), smoothness 0.7, clear coat 0.7. UVs are world-scale (0.25 m tile). |
| `TG_Tire` | Lit opaque. TG_Tire_BaseColor + TG_Tire_Normal (tread grooves, sipes, sidewall ring), smoothness 0.15. UV U = circumference (8 tread repeats), V = profile. |
| `TG_Glass` | Lit transparent, alpha 0.66, near-black tint (0.006, 0.008, 0.010), smoothness 0.98. Single sheet: no refraction. |
| `TG_LensClear` | Lit transparent, alpha 0.10, smoothness 0.98 (headlamp and lower rear clear lenses). |
| `TG_LensRed` | Lit transparent, alpha 0.80, deep red (0.30, 0.0, 0.004): reads red in daylight and lit (applies the Zero Gap R PB-1 lesson). |
| `TG_Display` | Lit + emission (0.55, 0.62, 0.70) x1.2 (cluster / centre screen); swap for a RenderTexture to drive live gauges. |
| `TG_LED_DRL` | Lit opaque + emission (0.82, 0.92, 1.0) x10.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `TG_LED_Headlamp` | Lit opaque + emission (0.95, 0.97, 1.0) x3.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `TG_LED_Tail` | Lit opaque + emission (1.0, 0.012, 0.015) x7.0. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `TG_LED_Brake` | Lit opaque + emission (1.0, 0.01, 0.012) x1.5. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `TG_LED_Indicator_L` | Lit opaque + emission (1.0, 0.32, 0.0) x0.7. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `TG_LED_Indicator_R` | Lit opaque + emission (1.0, 0.32, 0.0) x0.7. RUNTIME CHANNEL: drive _EmissionColor intensity. |
| `TG_LED_Reverse` | Lit opaque + emission (1.0, 1.0, 1.0) x0.3. RUNTIME CHANNEL: drive _EmissionColor intensity. |

Smoothness = 1 - roughness. Normal maps are OpenGL (+Y): Texture Type Normal map, no flip.
Light channels: `TG_LED_DRL` (daytime-running blade in each headlamp), `TG_LED_Headlamp` (two projector modules per side, low / high beam), `TG_LED_Tail` (full-width bar + corner verticals), `TG_LED_Brake` (upper corner blocks, raise to ~8 when braking), `TG_LED_Indicator_L` / `_R` (vehicle left / right, front + rear, blink independently), `TG_LED_Reverse`.
