# Traffic fleet: Unity import and integration (Unity 6000.6.0f1, URP 17.6)

This package holds seven frozen traffic vehicles, exported from Blender 5.2.2 on 2026-10-10.

**Nothing here has been opened in Unity.** The importer settings and material setups below are the intended configuration. They are derived from the validated FBX data, but they are **not runtime-verified**. Runtime verification is task **P0-05**, on the Unity machine (checklist in §9).

## 1. Package layout (keep it intact)

```
UNITY_HANDOFF_20261010/
  README_UNITY_IMPORT.md          this file
  UNITY_FLEET_MANIFEST.md / .json source release, checksums, FBX, textures, materials, LODs, dependencies
  UNITY_FLEET_HANDOFF_REPORT.md   export and validation report
  SHA1SUMS.txt                    SHA-1 of every file in the package
  shared/textures/                fleet texture library (12 PNG), used by every vehicle
  01_Traffic_Sedan_A_r3/  02_Traffic_Sedan_B/  03_Traffic_Hatchback_A_r2/  04_Traffic_SUV_A/
  05_Traffic_SUV_B/  06_Traffic_Box_Truck_A/  07_Traffic_Bus_A/
      FBX/<Base>_complete_unity.fbx   LOD0-3 + colliders + wheel refs + CenterOfMass (71 objects). This is the game asset.
      FBX/<Base>_LOD0_unity_test.fbx  LOD0 only (27 objects), for a quick import check. Do not ship both.
      textures/                       vehicle bakes: <Paint>_Body_Normal (2048), _Body_Normal_LOD1 (1024), _Body_AO_Grime (1024)
      reports/                        validation, FBX audit, export manifest, geometry, per-vehicle Unity manifest (JSON)
      README_<Base>.md                vehicle numbers: size, LODs, wheel and COM positions, colliders, material values
```

The FBX files reference textures by **relative path**:
- `../textures/<file>.png`
- `../../shared/textures/<file>.png`

Copy the whole folder into the project as-is, for example to `Assets/Vehicles/Traffic/UNITY_HANDOFF_20261010/`, so these paths still resolve. All references were checked from the package location; none is unresolved.

The FBX files also store the original absolute paths from the Blender Mac. That path is informational only, and it exposes the local user name in the path.

**Before importing**, check `SHA1SUMS.txt`:
- macOS: `shasum -c SHA1SUMS.txt`
- Windows (PowerShell): `Get-FileHash -Algorithm SHA1` per file

## 2. Texture import settings (set before or right after the first import)

| Textures | Texture Type | sRGB (Color Texture) | Notes |
|---|---|---|---|
| `TS_Atlas_BaseColor`, `TS_Tire_BaseColor`, `TS_Lights_BaseColor`, `TS_Lights_Emission` | Default | **On** | Mip maps on. Atlas UVs are inset 6 % per cell, so bilinear filtering does not bleed between cells. |
| `TS_Atlas_Normal`, `TS_Tire_Normal`, `TS_PaintFlake_Normal`, `<Paint>_Body_Normal`, `<Paint>_Body_Normal_LOD1` | **Normal map** | n/a | OpenGL / Y+ convention (Unity's), so no green flip. Body normals are MikkTSpace bakes. |
| `<Paint>_Body_AO_Grime` | Default | **Off** | R = ambient occlusion, G = road-grime mask (see §5, Paint). |
| `TS_Atlas_MetallicSmoothness` | Default | **Off** | R = metallic, A = smoothness (URP "Metallic Alpha" source). |
| `TS_Atlas_Metallic`, `TS_Atlas_Roughness`, `TS_Tire_Roughness` | Default | **Off** | Blender-side maps. `TS_Atlas_MetallicSmoothness` replaces the atlas pair in URP. |
| `TS_Lights_ChannelID` | Default | **Off** | **Filter Mode Point, Compression None, Generate Mip Maps off.** R × 15 = channel index, which must stay exact. |

## 3. Model importer settings (each `*_complete_unity.fbx`)

| Tab | Setting | Value | Why |
|---|---|---|---|
| Model | Scale Factor / Convert Units | **1 / On** | The FBX is in metres (UnitScaleFactor 100 = 1 m per unit), so 1 Unity unit = 1 m. |
| Model | Bake Axis Conversion | **Off** | Axes are baked into the meshes: `Car_Root` is identity, and every node has identity rotation and scale 1. |
| Model | Import BlendShapes / Visibility / Cameras / Lights | Off | None are used. |
| Model | Preserve Hierarchy | On | Keeps `Car_Root` as the root. |
| Model | Mesh Compression | Off | Keeps wheel pivots and collider hulls exact. |
| Model | Read/Write | Off | Turn it on only if P0-05 finds a runtime need. |
| Model | Generate Colliders | **Off** | Colliders are authored (`Collision_*`). |
| Model | Normals | **Import** | Authored split normals (validated S1 ≤ 1 % on every mesh). |
| Model | Tangents | **Calculate Mikktspace** | Matches the MikkTSpace body-normal bake. |
| Rig | Animation Type | None | |
| Animation | Import Animation | Off | |
| Materials | Material Creation Mode | Import via MaterialDescription | Then remap (§5). The FBX carries only some slots, so the auto-created materials are incomplete. |

**Unity space** (point mapping and directions for every vehicle):
- **Point mapping:** Blender (x, y, z) → Unity (−x, z, −y).
- **Directions:**
  - forward +Z;
  - up +Y;
  - vehicle left −X;
  - front axle at +Z;
  - ground at Y = 0.

Raw-file checks on every vehicle confirmed: nose +Z, tail −Z, roof +Y, FL wheel at −X / +Z.

## 4. Prefab assembly (per vehicle)

```
Car_Root
 ├─ LOD0_Root … LOD3_Root     Body_LODn (paint), Glass_LODn, Trim_LODn (atlas), Lights_LODn (emissive + lenses), Interior_LODn
 │   ├─ SteerPivot_FL/FR_LODn  steer: yaw about local Y → Wheel_FL/FR_LODn (roll about local X), Caliper_FL/FR_LODn (steers, no roll)
 │   ├─ Wheel_RL/RR_LODn       roll about local X;  Caliper_RL/RR_LODn static (no calipers at LOD3)
 ├─ Collision                  Collision_Front / Body / Cabin / Rear: convex hulls, ≤ 255 tris, no material
 ├─ WheelColliderRef_FL/FR/RL/RR   empties at the wheel centres (user properties radius_m, width_m)
 └─ CenterOfMass
```

1. Create a prefab, or a prefab variant, from `<Base>_complete_unity.fbx`.
2. **LOD Group** on `Car_Root`:
   - LOD0–LOD3 = the renderers under `LOD0_Root` … `LOD3_Root`.
   - Suggested screen heights: 50 / 22 / 8 / 1.5 %; tune in P0-05.
   - Unity will not build this automatically: the LOD objects are grouped under per-LOD roots, not as `_LODn` siblings.
3. **Colliders:**
   - On each `Collision_*`, remove or disable the MeshRenderer.
   - Add a MeshCollider with **Convex** on.
   - Set the physics layer as the game requires.
4. **Rigidbody** on `Car_Root`:
   - `rigidbody.centerOfMass = CenterOfMass.localPosition` (positions are in each vehicle README).
   - Mass and drag are gameplay values, set in P0-05.
5. **Wheel colliders:**
   - Add a WheelCollider at each `WheelColliderRef_*`.
   - Radius = `radius_m`, width per README.
   - The values also exist as FBX user properties, readable with an `AssetPostprocessor.OnPostprocessGameObjectWithUserProperties`.
   - Every LOD's wheel, caliper and steer-pivot origin sits exactly on its ref (deviation 0 m).
6. **Visual wheels:**
   - Drive all four LOD copies, `Wheel_XX_LOD0..3`, from `WheelCollider.GetWorldPose`, or roll them about local X.
   - Steer `SteerPivot_FL/FR_LOD0..3` about local Y; ±25° suggested.

## 5. Materials

**How to set them up:**
1. Create these once, in for example `Materials/Traffic/`, named **exactly** as the FBX materials:
   - shared: `TS_Atlas`, `TS_Tire`, `TS_Lens`, `TS_LensRed`, `TS_Lights`;
   - per vehicle: `<Paint>_Paint`, `<Paint>_Paint_LOD1`, `<Paint>_Paint_Far`, `<Paint>_Glass`, `<Paint>_Interior`.
2. In each FBX's Materials tab, use **On Demand Remap → Search and Remap (Project-Wide)**, or drag the materials into the Remapped Materials list.

Exact per-vehicle values (paint colour, metallic, smoothness, alpha, coat) are in each `README_<Base>.md`; they come from the frozen Blender materials.

**What the FBX does and does not carry:**
- It carries only these slots: DiffuseColor, NormalMap, plus Blender's Metallic → ReflectionFactor and Roughness → ShininessExponent.
- URP ignores or misreads the last two. Use the maps below instead.
- **Not in the FBX, set by hand:**
  - `<Paint>_Body_AO_Grime`;
  - `TS_Lights_Emission`, `TS_Lights_ChannelID`;
  - `TS_Atlas_MetallicSmoothness`;
  - `TS_PaintFlake_Normal`.

| Material | URP shader | Setup |
|---|---|---|
| `<Paint>_Paint` (LOD0) | Complex Lit (clear coat), or a Shader Graph | <ul><li>**BaseColor** = PaintColour × AO, where AO is the **R** of `_Body_AO_Grime`; lerp to grime (0.11, 0.10, 0.085) by **G × 0.55**.</li><li>**Normal** = `_Body_Normal`, plus detail normal `TS_PaintFlake_Normal` (tiling 60, strength 0.15).</li><li>**Metallic, smoothness, coat:** per vehicle README. Coat smoothness ≈ 0.955; grime lowers it.</li><li>**Do not** put `_AO_Grime` straight into URP's Occlusion Map: URP reads occlusion from **G**, and AO here is in **R**. Use a Shader Graph, or repack.</li></ul> |
| `<Paint>_Paint_LOD1` | same | Normal = `_Body_Normal_LOD1` |
| `<Paint>_Paint_Far` (LOD2–3) | Lit or Complex Lit | PaintColour only; no normal or AO maps |
| `TS_Atlas` | Lit, opaque | <ul><li>BaseMap `TS_Atlas_BaseColor`.</li><li>Metallic map `TS_Atlas_MetallicSmoothness`, Smoothness Source = Metallic Alpha.</li><li>Normal `TS_Atlas_Normal`.</li></ul> |
| `<Paint>_Interior` | Lit, opaque | Same as `TS_Atlas` (it is an instance of it), with **normal scale 0.12** |
| `TS_Tire` | Lit, opaque | <ul><li>BaseMap `TS_Tire_BaseColor`, Normal `TS_Tire_Normal`.</li><li>Smoothness = 1 − `TS_Tire_Roughness`: pack it into a map alpha, or use a constant ≈ 0.5.</li><li>The UV U coordinate wraps around the tire (repeat).</li></ul> |
| `<Paint>_Glass` | Lit, Transparent | Base (0.78, 0.84, 0.82), **alpha 0.22**, smoothness 1.0. Light-green tint, cabin readable. |
| `TS_Lens` / `TS_LensRed` | Lit, Transparent | <ul><li>Clear: alpha 0.10.</li><li>Red: (0.42, 0, 0.006), alpha 0.55.</li></ul> |
| `TS_Lights` | Shader Graph (one material, one draw call) | See the light-channel spec below. |

**`TS_Lights` light channels:**
- **Textures:** BaseMap `TS_Lights_BaseColor` (lamps off), Emission `TS_Lights_Emission`.
- **Channel index:** `round(TS_Lights_ChannelID.R × 15)`.
- **Channels:**

  | Index | Channel |
  |---|---|
  | 0 | DRL |
  | 1 | Headlamp |
  | 2 | Tail |
  | 3 | Brake |
  | 4 | Indicator_L |
  | 5 | Indicator_R |
  | 6 | Reverse |
  | 7 | Marker (truck and bus only) |

- **Emission:** `TS_Lights_Emission × intensity[channel]`, from a per-renderer array (MaterialPropertyBlock).
- **Suggested start intensities:**

  | Channel | Intensity |
  |---|---|
  | DRL | 12 |
  | Headlamp | 4 |
  | Tail | 5 |
  | Brake | 8 (on) |
  | Indicators | 1.2 (blink) |
  | Reverse | 0.5 |
  | Marker | about Tail level |

Channel faces were verified identical between the FBX and the source on every LOD.

**Paint variants** (material instances, no extra meshes; linear RGB, metallic):

| Variant | Linear RGB | Metallic |
|---|---|---|
| Arctic white | (0.80, 0.80, 0.78) | 0 |
| Silver | (0.55, 0.57, 0.59) | 0.55 |
| Graphite | (0.090, 0.095, 0.100) | 0.55 |
| Black | (0.012, 0.012, 0.013) | 0 |
| Deep red | (0.30, 0.012, 0.015) | 0.55 |
| Steel blue | (0.060, 0.115, 0.220) | 0.55 |

The `unity` note text stored on the Blender paint materials is a generic fleet note. Where it differs from the per-vehicle README (for example, the box truck's solid paint is metallic 0, coat 0.55), **the README values are the frozen source values.**

## 6. Blender-only data (not exported, not needed)

`TS_Lights_State` is a packed 4 × 4 review mask that chooses which channels glow in Blender renders. Unity drives the channels at runtime instead.

## 7. Night lighting (recommendation from the Blender night review; not verified in Unity)

- **What to avoid:** a black reflection environment makes clear-coat paint and glass read black at night.
- **What to use:**
  - a night skybox or reflection probe with a warm horizon glow and a deep-blue zenith;
  - low ambient light;
  - lamp light from the emissive light channels.
- **No per-vehicle real-time lights** are needed for traffic.
- **Reference renders:** `H_TrafficFleet/reports/NIGHT_REVIEW_20261010/`, on the Blender machine.

## 8. Vehicle summary

| # | Vehicle | Length × width × height (m) | LOD0 / 1 / 2 / 3 tris | Wheel radius (m) | CenterOfMass (Unity) |
|---|---|---|---|---|---|
| 1 | Sedan A r3 | 4.65 × 2.06 × 1.47 | 14,961 / 7,756 / 3,546 / 1,383 | 0.316 | (0, 0.52, 0.22) |
| 2 | Sedan B | 4.97 × 2.18 × 1.49 | 17,987 / 8,739 / 4,012 / 1,746 | 0.352 | (0, 0.53, 0.08) |
| 3 | Hatchback A r2 | 4.27 × 2.08 × 1.52 | 17,174 / 8,391 / 3,887 / 1,652 | 0.317 | (0, 0.50, 0.18) |
| 4 | SUV A v2 | 4.48 × 2.19 × 1.70 | 17,998 / 8,768 / 4,027 / 1,728 | 0.370 | (0, 0.62, 0.12) |
| 5 | SUV B v3 | 4.98 × 2.30 × 1.81 | 19,840 / 9,566 / 4,325 / 1,939 | 0.391 | (0, 0.70, 0.10) |
| 6 | Box Truck A r7 | 7.07 × 2.54 × 3.25 | 20,063 / 10,765 / 4,796 / 2,591 | 0.405 | (0, 1.10, 0.40) |
| 7 | Bus A v4 | 12.01 × 2.98 × 3.20 | 34,506 / 15,126 / 6,210 / 2,999 | 0.478 | (0, 1.10, −0.30) |

Width includes the mirrors.

**Per LOD:** 8 / 8 / 8 / 6 materials, 4 convex colliders, and 4 wheel refs on every vehicle.

## 9. P0-05 runtime checklist (Unity machine, not done here)

1. **Package integrity:** `SHA1SUMS.txt` verifies.
2. **Import:**
   - each FBX imports with no missing-texture warnings;
   - 1 unit = 1 m, with the vehicle on the ground (Y = 0) facing +Z.
3. **LOD Group:**
   - switching at the chosen heights;
   - no popping of mirrors or lamps;
   - draw calls per LOD as reported (19–20 / 13–14).
4. **Physics:**
   - convex colliders;
   - WheelColliders aligned with the visual wheels at all LODs;
   - suspension and steering on the front SteerPivots;
   - centre of mass behaviour.
5. **Materials:**
   - paint (clear coat, AO from R);
   - glass and lens transparency sorting;
   - atlas without cell bleed at distance.
6. **Lights:**
   - each of the 8 channels toggles independently;
   - brake vs tail distinct;
   - indicators blink per side;
   - truck and bus markers.
7. **Night scene:**
   - with the reflection probe or skybox from §7;
   - vehicles readable at rear-follow distances of 7.5 / 22 / 60 m.
8. **Performance:** profile on the target mobile devices. No frame-rate claims are made by this package.
