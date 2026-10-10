# Unity import notes: hypercar

Files: `exports/hypercar_complete_unity.fbx` (LOD0-3 + colliders + refs, 308 objects) and
`exports/hypercar_LOD0_unity_test.fbx` (LOD0 only, 102 objects). Textures are external (not embedded), referenced
relatively as `../textures/hypercar/<group>/*.png`. Copy `textures/hypercar/` into the Unity project with the FBX.

## Importer settings (Model tab)
- Scale Factor **1**, Convert Units **ON** (file unit = 1 m, UnitScaleFactor 100 cm). Result: 1 unit = 1 m, root scale 1.
- Bake Axis Conversion **OFF** (not needed: axes are already baked; Car_Root rotation is identity in the file).
- Import Normals: **Import**; Tangents: **Import** (MikkTSpace, exported); Smoothing source: from file.
- Materials: Location "Use External Materials (Legacy)" or extract, then set them up per `unity_material_mapping.md`.
- Animation: none in the file (Animation Type None). No cameras or lights.

## Coordinate conversion (verified by re-import)
| | Blender | FBX file | Unity |
|---|---|---|---|
| forward | -Y | +Z | **+Z** |
| up | +Z | +Y | **+Y** |
| vehicle left | +X | +X | **-X** (Unity's importer negates FBX X) |
| point (x, y, z) | (x, y, z) | (x, z, -y) | (-x, z, -y) |

The car faces +Z, upright, and the LHD driver seat sits on the vehicle's left (Unity -X). Car_Root: position 0, rotation 0, scale 1.
Unity view checks: nose z 2.3967, tail z -2.249, roof y 1.1726.

## Dimensions (LOD0 re-import, mirrors excluded)
Length 4.695 m, width 2.05233 m, height 1.17258 m (all within 0.05 mm of Phase 7).
Wheelbase 2.78 m, track front 1.67 m / rear 1.67 m.

## Wheels (WheelColliderRef_* empties = wheel centres)
| Ref | Side | Blender | Unity local to Car_Root | radius m | width m |
|---|---|---|---|---|---|
| FL | LEFT | (0.835, -1.39, 0.355) | (-0.835, 0.355, 1.39) | 0.355 | 0.31 |
| FR | RIGHT | (-0.835, -1.39, 0.355) | (0.835, 0.355, 1.39) | 0.355 | 0.31 |
| RL | LEFT | (0.835, 1.39, 0.3775) | (-0.835, 0.3775, -1.39) | 0.3775 | 0.35 |
| RR | RIGHT | (-0.835, 1.39, 0.3775) | (0.835, 0.3775, -1.39) | 0.3775 | 0.35 |

Use the refs to position WheelColliders (radius as above; suspension distance tuned in Unity).
Visual wheels: `Wheel_<k>_LODn` rotates on **local X** (axle; tire + rotor are children, calipers do not roll).
Front steering: `SteerPivot_FL/FR_LODn` yaws on **local Y** (= car up) about the wheel centre, carrying wheel and caliper.
Because Unity mirrors X on import, drive the visual wheels from `WheelCollider.GetWorldPose` rather than accumulating
local Euler angles; if spinning by hand, verify the sign once per side.

## Center of mass
`CenterOfMass` empty: Blender (0, 0.12, 0.35) -> Unity local **(0.0, 0.35, -0.12)**
(0.35 m high, 0.12 m behind mid-wheelbase). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition` in a script.

## LODs (one FBX, four roots)
| LOD | triangles | L x W x H (m) | material slots |
|---|---|---|---|
| LOD0 | 206,327 | 4.695 x 2.05233 x 1.17258 | 24 |
| LOD1 | 107,210 | 4.695 x 2.05252 x 1.17258 | 24 |
| LOD2 | 53,786 | 4.695 x 2.05275 x 1.1741 | 20 |
| LOD3 | 17,747 | 4.69201 x 2.05275 x 1.1741 | 15 |

Triangles are Phase 7 counts minus 57 coincident duplicate triangles removed at export ({"Caliper_FL_LOD3": 3, "InstrumentCluster_LOD1": 2, "Caliper_FR_LOD3": 2, "CenterConsole_LOD2": 6, "InstrumentCluster_LOD2": 2, "Body_LOD2": 7, "Body_LOD0": 2, "Interior_LOD3": 21, "Interior_Tub_LOD2": 6, "Caliper_RL_LOD3": 5, "Caliper_RR_LOD3": 1}).
Set up a LOD Group on Car_Root: LOD0_Root ... LOD3_Root renderers (suggested 60 / 30 / 12 / 3 % screen height).
Colliders, refs and CenterOfMass are outside the LOD roots and shared by all LODs.

## Material groups
24 materials per LOD: 8 baked atlases (`LODMAT_Body_Paint`, `Brakes`, `Glass`, `Interior`, `Lights`, `Tire`,
`Trim`, `Wheels`) + carbon (exterior/interior) + caliper + lenses + displays + interior mirror + **6 light channels kept
separate**: `MAT_LED_White`, `MAT_ProjectorLens`, `MAT_LED_Red`, `MAT_LED_Brake`, `MAT_LED_Amber`, `MAT_LED_Reverse` (+ `MAT_AmbientLight`).
Full mapping: `reports/unity_material_mapping.md`.

## Textures (48 files, PNG)
Atlases: BODY 4096, INTERIOR 4096, WHEELS / TIRES / LIGHTS 2048, BRAKES / GLASS / TRIM 1024; each has BaseColor, Metallic,
Roughness, Normal, AO. **Normal maps are OpenGL (+Y up green)**, which is Unity's convention: import as Normal map, no flip.
Roughness must be inverted to smoothness (see mapping). AO is not linked by the FBX; assign it manually.
- `textures/hypercar/body/BODY_AO.png`
- `textures/hypercar/body/BODY_BaseColor.png`
- `textures/hypercar/body/BODY_Metallic.png`
- `textures/hypercar/body/BODY_Normal.png`
- `textures/hypercar/body/BODY_Roughness.png`
- `textures/hypercar/brakes/BRAKES_AO.png`
- `textures/hypercar/brakes/BRAKES_BaseColor.png`
- `textures/hypercar/brakes/BRAKES_Metallic.png`
- `textures/hypercar/brakes/BRAKES_Normal.png`
- `textures/hypercar/brakes/BRAKES_Roughness.png`
- `textures/hypercar/glass/GLASS_AO.png`
- `textures/hypercar/glass/GLASS_BaseColor.png`
- `textures/hypercar/glass/GLASS_Metallic.png`
- `textures/hypercar/glass/GLASS_Normal.png`
- `textures/hypercar/glass/GLASS_Roughness.png`
- `textures/hypercar/interior/INTERIOR_AO.png`
- `textures/hypercar/interior/INTERIOR_BaseColor.png`
- `textures/hypercar/interior/INTERIOR_Metallic.png`
- `textures/hypercar/interior/INTERIOR_Normal.png`
- `textures/hypercar/interior/INTERIOR_Roughness.png`
- `textures/hypercar/interior/speaker_perforation_Mask.png`
- `textures/hypercar/interior/speaker_perforation_Normal.png`
- `textures/hypercar/interior/stitch_Mask.png`
- `textures/hypercar/interior/stitch_Normal.png`
- `textures/hypercar/lights/LIGHTS_AO.png`
- `textures/hypercar/lights/LIGHTS_BaseColor.png`
- `textures/hypercar/lights/LIGHTS_Metallic.png`
- `textures/hypercar/lights/LIGHTS_Normal.png`
- `textures/hypercar/lights/LIGHTS_Roughness.png`
- `textures/hypercar/tires/TIRES_AO.png`
- `textures/hypercar/tires/TIRES_BaseColor.png`
- `textures/hypercar/tires/TIRES_Metallic.png`
- `textures/hypercar/tires/TIRES_Normal.png`
- `textures/hypercar/tires/TIRES_Roughness.png`
- `textures/hypercar/tires/tire_sidewall_Mask.png`
- `textures/hypercar/tires/tire_sidewall_Normal.png`
- `textures/hypercar/trim/TRIM_AO.png`
- `textures/hypercar/trim/TRIM_BaseColor.png`
- `textures/hypercar/trim/TRIM_Metallic.png`
- `textures/hypercar/trim/TRIM_Normal.png`
- `textures/hypercar/trim/TRIM_Roughness.png`
- `textures/hypercar/trim/carbon_twill_BaseColor.png`
- `textures/hypercar/trim/carbon_twill_Normal.png`
- `textures/hypercar/wheels/WHEELS_AO.png`
- `textures/hypercar/wheels/WHEELS_BaseColor.png`
- `textures/hypercar/wheels/WHEELS_Metallic.png`
- `textures/hypercar/wheels/WHEELS_Normal.png`
- `textures/hypercar/wheels/WHEELS_Roughness.png`

## Colliders (`Collision` empty, 6 convex meshes, 392 triangles total)
| Collider | tris | verts |
|---|---|---|
| Collision_Front | 74 | 39 |
| Collision_Body | 52 | 28 |
| Collision_Side_L | 64 | 34 |
| Collision_Side_R | 66 | 35 |
| Collision_Cabin | 60 | 32 |
| Collision_Rear | 76 | 40 |

All convex (<= 255 triangles each), closed, outward normals: add MeshCollider with **Convex ON** to each, disable their
MeshRenderers (they carry no material and no UVs), and put them on a vehicle physics layer.

## Animated / pivot objects (no animation data exported, pivots only)
| Object | Pivot | Axis (Unity local) | Range |
|---|---|---|---|
| `Wheel_FL/FR/RL/RR_LOD0-3` | wheel centre | X (roll) | continuous |
| `SteerPivot_FL/FR_LOD0-3` | wheel centre | Y (yaw) | -25 .. +25 deg |
| `SteeringWheel_LOD0-2` | column hub, Blender (0.36, -0.2, 0.645) | Y (shaft) | ~ +/-270 deg (ratio to taste) |
| `Paddle_L/R_LOD0-1` | paddle hinge | as authored | small pull |
| `Door_L/R_LOD0-1` (+ panel, window, handle) | hinge, Blender (+/-0.9, -0.95, 0.8) | X | 0 .. 15-20 deg (validated 18) |
| `ActiveSpoiler_LOD0-3` | hinge, Blender (0, 1.884, 0.8735) | X | 3 deg rest .. 18 deg deployed |

## Suggested Unity hierarchy (not built: Unity work starts after approval)
```
Hypercar (prefab root) = Car_Root   [Rigidbody, LOD Group, vehicle controller]
 |- LOD0_Root .. LOD3_Root          [render meshes; animated pivots inside]
 |- Collision                       [6 x MeshCollider convex, renderers off]
 |- WheelColliders (new)            [4 x WheelCollider placed at WheelColliderRef_*]
 |- WheelColliderRef_FL/FR/RL/RR    [position references, can be removed after setup]
 '- CenterOfMass                    [read by script -> rigidbody.centerOfMass]
```
