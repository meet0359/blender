# Unity import (Unity 6000.6.0f1, URP 17.6)

These are the **intended** settings. They come from the validated FBX data and each vehicle's frozen release notes. **They have not been run in Unity** (P0-05). The same values are machine-readable in `04_Unity_Setup/Import_Settings/unity_import_settings.json`, as `model_importer` per FBX and `texture_importer` per PNG.

## 1. Where to put the files

Copy `01_Traffic_Vehicles/` and `02_Player_Vehicles/` into `Assets/`, for example `Assets/Vehicles/`, **unchanged**.

The FBX files link their textures relatively from the `FBX/` folder:

| Vehicles | Relative texture paths |
|---|---|
| Traffic | `../textures/<Paint>_Body_*.png` and `../../shared/textures/TS_*.png` |
| Zero Gap R, Titan GT r1, Vortex R r1, Raven XR | `../textures/<PREFIX>_*.png` |
| Hypercar | `../textures/hypercar/<group>/*.png` |

All 12 FBX files were checked from a copy of this package in another folder. Every reference resolved inside the copy, and Blender's importer loaded every image from there. Each FBX also stores the absolute path of the Blender Mac folder it was written from. That path doesn't exist on the Unity machine and is ignored once the relative path resolves.

## 2. Model importer (every `*_complete_unity.fbx`)

| Tab | Setting | Value | Why |
|---|---|---|---|
| Model | Scale Factor | **1** | The FBX is in metres (UnitScaleFactor 100 = 1 m per unit). |
| Model | Convert Units | **On** | Same reason: 1 Unity unit = 1 m. |
| Model | Bake Axis Conversion | **Off** | Axes are baked into the meshes. `Car_Root` is identity, and the FBX axes are Up +Y / Front +Z. |
| Model | Import BlendShapes / Visibility / Cameras / Lights | Off | None are present. |
| Model | Preserve Hierarchy | On | Keeps `Car_Root` as the root. |
| Model | Mesh Compression | **Off** | Keeps wheel pivots and collider hulls exact. |
| Model | Read/Write | Off | Turn on only if a runtime system needs mesh access. |
| Model | Generate Colliders | **Off** | Colliders are authored (`Collision_*`) and optional. |
| Model | Normals | **Import** | Authored split normals. |
| Model | Tangents | Traffic: **Calculate Mikktspace**. Player: **Import** | Traffic body normals are MikkTSpace bakes; the player FBX files carry exported MikkTSpace tangents. |
| Rig | Animation Type | None | |
| Animation | Import Animation | Off | No animation data; pivots only. |
| Materials | Material Creation Mode | Import via MaterialDescription | Then remap to your URP materials **by exact name**: On Demand Remap → Search and Remap (Project-Wide). The auto-created materials are incomplete. |

**Unity space** (verified on every packaged FBX):
- Blender point (x, y, z) becomes Unity (−x, z, −y).
- Forward +Z, up +Y, vehicle left −X, front axle at +Z, ground at Y = 0.
- Every node rotation is identity, with one exception: the Hypercar's authored pivots `ActiveSpoiler_LODn` (3° rest), `SteeringWheel_LODn` and `Paddle_L/R_LODn` (raked column). Its notes document them.
- No negative scale anywhere.

## 3. Texture importer

| Textures | Texture Type | sRGB | Other |
|---|---|---|---|
| `*_BaseColor.png`, `TS_Lights_Emission.png` | Default | **On** | Mip maps on |
| `*_Normal.png`, `*_Normal_LOD1.png`, `TS_PaintFlake_Normal.png` | **Normal map** | – | OpenGL / Y+ (Unity's convention), so no green flip |
| `<Paint>_Body_AO_Grime.png` (traffic) | Default | Off | R = AO, G = grime mask |
| `*_MetallicSmoothness.png` | Default | Off | R = metallic, A = smoothness |
| `*_Metallic.png`, `*_Roughness.png`, `*_AO.png`, `*_Mask.png` | Default | Off | Hypercar: pack for URP, see the material guide |
| `TS_Lights_ChannelID.png` | Default | Off | **Filter Point, Compression None, Mip maps off** (R × 15 = exact channel index) |
| `<PREFIX>_Palette_*.png` (player) | Default | BaseColor on, others off | **Filter Point, mip maps off** (256 px swatch atlas) |

Android: use ASTC compression, except for `TS_Lights_ChannelID`, which must stay uncompressed.

## 4. Prefab assembly (per vehicle)

```
Car_Root                              prefab root: LOD Group (+ Rigidbody only where the game uses physics)
 ├─ LOD0_Root … LOD3_Root             render meshes; wheel / steer pivots inside
 │   ├─ SteerPivot_FL/FR_LODn         yaw about local Y (±25° suggested) → Wheel_FL/FR_LODn (+ caliper)
 │   └─ Wheel_RL/RR_LODn              roll about local X
 ├─ Collision                         Collision_* convex hulls (optional)
 ├─ WheelColliderRef_FL/FR/RL/RR      wheel centres (user properties radius_m, width_m)
 └─ CenterOfMass
```

1. Create a prefab, or a prefab variant, from the `*_complete_unity.fbx`.
2. Add a **LOD Group** on `Car_Root`:
   - LOD k = all renderers under `LODk_Root`.
   - Suggested screen heights: traffic 50 / 22 / 8 / 1.5 %; player 60 / 30 / 12 / 3 %. Tune on device.
3. **Colliders (optional).** If you use them: a MeshCollider with **Convex** on each `Collision_*`; disable their MeshRenderers (no material, no UVs). For analytic traffic, disable or strip them in the prefab.
4. **Visual wheels.** Drive all four LOD copies of each wheel, `Wheel_XX_LOD0..3`: roll about local X, steer `SteerPivot_FL/FR_LODn` about local Y. Because Unity mirrors X on import, verify the roll sign once per side, or drive the wheels from `WheelCollider.GetWorldPose` if physics is used. Every wheel and steer-pivot origin sits exactly on its `WheelColliderRef` (0.0000 mm measured).
5. **Physics (player cars only, if the controller uses them).** `rigidbody.centerOfMass = CenterOfMass.localPosition`. WheelColliders at `WheelColliderRef_*` with the radius and width from the spec JSON.

## 5. Mapping from the earlier traffic handoff

`01_Traffic_Vehicles/_fleet_reference_20261010/README_UNITY_IMPORT.md` is the original verified fleet README, kept verbatim for its detailed per-material tables. It uses the earlier folder names:

| Earlier handoff (`UNITY_HANDOFF_20261010/`) | This package |
|---|---|
| `01_Traffic_Sedan_A_r3/` | `01_Traffic_Vehicles/Traffic_Sedan_A_r3/` |
| `02_Traffic_Sedan_B/` | `01_Traffic_Vehicles/Traffic_Sedan_B/` |
| `03_Traffic_Hatchback_A_r2/` | `01_Traffic_Vehicles/Traffic_Hatchback_A_r2/` |
| `04_Traffic_SUV_A/` | `01_Traffic_Vehicles/Traffic_SUV_A_v2/` |
| `05_Traffic_SUV_B/` | `01_Traffic_Vehicles/Traffic_SUV_B_v3/` |
| `06_Traffic_Box_Truck_A/` | `01_Traffic_Vehicles/Traffic_Box_Truck_A_r7/` |
| `07_Traffic_Bus_A/` | `01_Traffic_Vehicles/Traffic_Bus_A_v4/` |
| `shared/textures/` | `01_Traffic_Vehicles/shared/textures/` |
| `SHA1SUMS.txt` | `05_Manifests/FILE_CHECKSUMS_SHA256.txt` (SHA-256, whole package) |
| `<Base>_LOD0_unity_test.fbx` | not shipped (LOD0-only subset of the complete FBX) |

The traffic FBX, texture and report files are byte-identical to that handoff: each was checked against its `SHA1SUMS.txt` while packaging.

The player-car notes (`<PREFIX>_UNITY_IMPORT_NOTES.md`) also mention a `Textures/` folder and a LOD0 test FBX. In this package the folder is `textures/` (lower case, matching what the FBX references), and the test FBX is not shipped.
