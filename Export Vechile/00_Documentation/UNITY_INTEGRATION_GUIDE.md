# Unity integration guide: keep the existing game systems

This package adds vehicle **visuals and data**. It does **not** ask Unity to replace any of these:
- `RoadStreamer`;
- `TrafficSpawner` / `TrafficManager`;
- `TrafficVehicleData`;
- `VehicleVisual`;
- the analytic collision and near-miss systems;
- traffic pooling;
- camera modes;
- quality tiers.

It was built without access to the Unity project, so it **does not know the field names** of those classes. Inspect them first, then map the values below. Nothing here is runtime-verified.

## 1. Traffic stays analytic: no new physics

- **Do not add a Rigidbody or WheelColliders to traffic.** The current traffic uses analytic collision and near-miss detection; keep that.
- `Collision_*` hulls and `WheelColliderRef_*` empties are **optional integration resources**:
  - hulls: convex, 4 per traffic vehicle, ≤ 255 triangles each;
  - refs: wheel centres, with radius / width as FBX user properties.
- For pooled traffic, disable or strip the `Collision_*` objects in the prefab, so pooled instances carry no MeshColliders.
- **Wheels:** the visual wheel transforms (`Wheel_XX_LOD0..3`, `SteerPivot_FL/FR_LOD0..3`) can be spun and steered by `VehicleVisual` (or whatever drives wheel visuals today) from the analytic speed. Each pivot sits exactly on the wheel centre (0.0000 mm offset measured on every LOD).
- **`TrafficVehicleData` footprint:** use `traffic.footprint_override` from `04_Unity_Setup/Vehicle_Configuration/<vehicle>.json`. It is the **collision body without mirrors**, measured from the packaged collision hulls:
  - width = the widest hull that stays inside the design body width;
  - length and height = all hulls.

  Do **not** use the mirror-inclusive visual width for collision.

| Vehicle | Footprint W × L × H (m) | Visual width incl. mirrors (m) | Wheelbase (m) | Notes |
|---|---|---|---|---|
| Sedan A r3 | 1.807 × 4.645 × 1.308 | 2.060 | 2.70 | within 15k |
| Sedan B | 1.900 × 4.967 × 1.300 | 2.180 | 2.97 | |
| Hatchback A r2 | 1.799 × 4.260 × 1.360 | 2.080 | 2.63 | |
| SUV A v2 | 1.847 × 4.474 × 1.481 | 2.190 | 2.68 | |
| SUV B v3 | 1.970 × 4.970 × 1.549 | 2.300 | 2.98 | |
| Box Truck A r7 | 2.342 × 6.891 × 2.644 | 2.544 | 3.85 | box width; cab hulls reach the mirrors |
| Bus A v4 | 2.557 × 11.970 × 2.684 | 2.984 | 6.00 | front / cabin hulls reach the mirrors |

The footprint centre is about (0, y, ±0.05) in Unity space. Exact values are in each JSON. If near-miss should trigger on the mirrors, use the visual width for near-miss only, never for collision.

## 2. The 15,000-triangle traffic validation budget

The existing Unity validation allows 15,000 LOD0 triangles per traffic vehicle. **Only Sedan A r3 (14,961) is within it.**

| Vehicle | LOD0 triangles | Over 15k by |
|---|---|---|
| Sedan B | 17,987 | 2,987 |
| Hatchback A r2 | 17,174 | 2,174 |
| SUV A v2 | 17,998 | 2,998 |
| SUV B v3 | 19,840 | 4,840 (owner-approved 20k class budget) |
| Box Truck A r7 | 20,063 | 5,063 |
| Bus A v4 | 34,506 | 19,506 |

These are the approved, frozen releases. **Do not weaken the validation just to make an import pass.** Bring it to the owner as a decision:

| Option | What it means |
|---|---|
| (a) | Per-class budgets (car 20k, truck 20k, bus 35k) |
| (b) | Validate LOD1 as the gameplay mesh: 7,756–10,765 for the five cars and the truck, all within 15k. The bus LOD1 is 15,126, which is 126 over. |
| (c) | Keep 15k and exclude the over-budget vehicles |

LOD1–3 for every traffic vehicle: 7,756–15,126 / 3,546–6,210 / 1,383–2,999 triangles.

## 3. Object names vs what `VehicleVisual` expects

The FBX names are fixed by the frozen releases. **Map them in Unity; don't rename inside the FBX.** That would break the release hashes and the LOD-wide naming.

| Purpose | FBX name(s) |
|---|---|
| Prefab root | `Car_Root` |
| LOD sets | `LOD0_Root`, `LOD1_Root`, `LOD2_Root`, `LOD3_Root` |
| Front wheels: steer, then roll | `SteerPivot_FL_LODn` (yaw, local Y) → `Wheel_FL_LODn` (roll, local X); same for FR |
| Rear wheels: roll | `Wheel_RL_LODn`, `Wheel_RR_LODn` (roll, local X) |
| Body / paint | `Body_LODn` (Hypercar also has `Body_Buttress_LODn`) |
| Lamps | `Lights_LODn` (traffic: `TS_Lights` channels; player: `<P>_LED_*` materials) |
| Wheel centres | `WheelColliderRef_FL/FR/RL/RR` |
| Centre of mass | `CenterOfMass` |
| Colliders | `Collision` → `Collision_Front/Body/Cabin/Rear` (+ `Collision_Side_L/R` on the Hypercar, `Collision_Wing` on Vortex R r1) |

If `VehicleVisual` expects one transform per wheel, give it the LOD0 wheel and drive the LOD1–3 copies with the same rotation. Alternatively, have it rotate all four LOD copies; inactive LOD renderers cost nothing to transform.

## 4. LOD Group, pooling and quality tiers

- **LOD Group on `Car_Root`** with 4 LODs (renderers under `LODk_Root`). Start values:
  - traffic: 50 / 22 / 8 / 1.5 %;
  - player: 60 / 30 / 12 / 3 %.
- **Pooling:** the LOD Group works on pooled instances unchanged. Per-renderer light intensities should go through a MaterialPropertyBlock, so pooled cars share materials. Paint variants are material instances (no extra meshes).
- **Quality tiers:** use `QualitySettings.lodBias` / `maximumLODLevel` per tier. For example, low tier starts traffic at LOD1. LOD3 keeps 1.4k–3.0k triangles and 6 materials.
- **Draw calls:** traffic is about 19–20 at LOD0 and 13–14 at LOD1 (8 / 8 / 8 / 6 materials). Player cars use 15 materials per LOD; the Hypercar uses 24 / 24 / 20 / 15.

## 5. Large truck and bus

- **Lengths:**
  - Box Truck A r7: 7.07 m long, 3.25 m high.
  - Bus A v4: 12.01 m long, 3.20 m high.

  Check spawn spacing, lane occupancy and despawn distance in `TrafficSpawner` / `TrafficManager`. The spawn gap logic must use their real length (`footprint_override.length`).
- **Visibility:**
  - They block the view in rear-follow camera modes. Test every camera mode behind them.
  - LOD3 switches at a larger distance because they are big on screen.
  - Their 8th light channel, **Marker** (clearance, ID and side markers), helps at night.
- **Pool sizes:** keep bus and truck counts low; the bus is the heaviest traffic asset.

## 6. Replacing existing vehicle slots

Which current traffic slot each new vehicle replaces, or whether they extend the pool, is a **Unity / owner decision**. This package does not assume it. A natural mapping by class:

| Class | Vehicles |
|---|---|
| Compact | Hatchback A r2 |
| Sedan | Sedan A r3, Sedan B |
| SUV | SUV A v2, SUV B v3 |
| Truck | Box Truck A r7 |
| Bus | Bus A v4 |

Keep the old prefabs until P0-05 passes.

## 7. Player cars

- **Releases:**
  - Zero Gap R;
  - Titan GT r1 and Vortex R r1 (the r1 revisions replace the originals for import);
  - Raven XR;
  - the Hypercar (flagship).
- **What each ships:** `WheelColliderRef_*`, `CenterOfMass` and convex hulls for whatever the existing player controller needs. Use them only if the controller works that way.
- **Budget:** LOD0 is 73.7k–89.7k for the four sports cars, which sits inside the 60–120k mobile player budget. The **Hypercar LOD0 is 206k** (LOD1 107k), far above it.
  - Treat it as a high-tier or showroom asset;
  - or start it at LOD1 / LOD2 on mobile.

  Decide in Unity.
- **Hypercar extra pivots** (not driven by anything in the FBX):
  - doors `Door_L/R_LOD0-1`;
  - active spoiler `ActiveSpoiler_LOD0-3` (3° rest, 18° deployed);
  - steering wheel and paddles.

  See `reports/unity_import_notes.md`.

## 8. Known compatibility items (summary)

| Item | Impact | Action in Unity |
|---|---|---|
| 15k traffic triangle budget | 6 of 7 over at LOD0 | Owner decision (§2); do not weaken validation |
| Hypercar 206k LOD0 | Mobile cost | High tier / start at LOD1+ |
| LOD Group not auto-built | Manual or scripted setup | Use `unity_import.lod_group` from the spec JSON |
| Object naming | `VehicleVisual` mapping | Map names (§3) |
| Footprint vs visual width | Collision too wide if the visual width is used | Use `traffic.footprint_override` |
| Light channels | Traffic: ChannelID shader. Player: per-material | Shader Graph (`MATERIAL_SETUP_GUIDE.md`) |
| AO in R (traffic paint) | Wrong AO if plugged into URP Occlusion | Shader Graph or repack |
| Hypercar unpacked metal / roughness | URP Lit needs MetallicSmoothness | Pack in Unity |
| Hypercar indicators | One amber material for both sides | Accept, or request a Blender revision |
| Truck / bus size | Spawn gaps, camera occlusion | Use real length; test cameras |
| Pooling | Material copies per instance | Use MaterialPropertyBlock for lights |
