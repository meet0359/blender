# Export Vechile: start here

This is the vehicle handoff from the Blender Mac to the Unity machine. It contains **12 approved, frozen vehicle releases**: the 7 mandatory traffic vehicles and 5 player cars. Each one is a single Unity-ready FBX (LOD0–LOD3, colliders, wheel references, centre of mass) with all its textures, a machine-readable spec, and its release reports.

**Status.** Everything was verified on the Blender side: an FBX re-import of every file in place, the same again from a copy in another folder, and source hashes. All 20 required checks pass (`EXPORT_VALIDATION_REPORT.md`). **Nothing has been opened in Unity yet.** Unity import, prefabs, materials, shaders, lighting, gameplay and Android performance are still to be done; that is task P0-05 (`06_QA/UNITY_PENDING_TESTS.md`).

Targets: Unity **6000.6.0f1**, URP **17.6**. Units are metres, import scale 1, **+Z forward, +Y up, −X vehicle left**, ground at Y = 0.

## 1. Included vehicles

| # | Vehicle | Type | Release | FBX to import | LOD0 tris |
|---|---|---|---|---|---|
| 1 | Sedan A r3 | traffic | Sedan A r3 | `01_Traffic_Vehicles/Traffic_Sedan_A_r3/FBX/TrafficSedanA_r3_complete_unity.fbx` | 14,961 |
| 2 | Sedan B | traffic | Sedan B (final release) | `01_Traffic_Vehicles/Traffic_Sedan_B/FBX/TrafficSedanB_complete_unity.fbx` | 17,987 |
| 3 | Hatchback A r2 | traffic | Hatchback A r2 | `01_Traffic_Vehicles/Traffic_Hatchback_A_r2/FBX/TrafficHatchbackA_r2_complete_unity.fbx` | 17,174 |
| 4 | SUV A v2 | traffic | SUV A v2 | `01_Traffic_Vehicles/Traffic_SUV_A_v2/FBX/TrafficSUVA_complete_unity.fbx` | 17,998 |
| 5 | SUV B v3 | traffic | SUV B v3 | `01_Traffic_Vehicles/Traffic_SUV_B_v3/FBX/TrafficSUVB_complete_unity.fbx` | 19,840 |
| 6 | Box Truck A r7 | traffic | Box Truck A r7 | `01_Traffic_Vehicles/Traffic_Box_Truck_A_r7/FBX/TrafficBoxTruckA_complete_unity.fbx` | 20,063 |
| 7 | Bus A v4 | traffic | Bus A v4 | `01_Traffic_Vehicles/Traffic_Bus_A_v4/FBX/TrafficBusA_complete_unity.fbx` | 34,506 |
| 8 | Hypercar | player (flagship) | Phase 9 export checkpoint | `02_Player_Vehicles/Hypercar/FBX/hypercar_complete_unity.fbx` | 206,327 |
| 9 | Zero Gap R | player | Phase B release | `02_Player_Vehicles/ZeroGapR/FBX/ZeroGapR_complete_unity.fbx` | 89,681 |
| 10 | Titan GT r1 | player | revision r1 | `02_Player_Vehicles/TitanGT_r1/FBX/TitanGT_complete_unity.fbx` | 77,370 |
| 11 | Vortex R r1 | player | revision r1 | `02_Player_Vehicles/VortexR_r1/FBX/VortexR_complete_unity.fbx` | 73,665 |
| 12 | Raven XR | player | Phase E release | `02_Player_Vehicles/RavenXR/FBX/RavenXR_complete_unity.fbx` | 74,271 |

**What was left out, and why** (superseded originals, postponed Pulse EV / Pickup A / Van A, LOD0-only test files, source `.blend` files): see `VEHICLE_INVENTORY.md`.

## 2. Transfer the ZIP

Copy **`Export Vechile.zip`** and the small **`Export Vechile.zip.sha256`** next to it to the Unity machine. Any route works: USB drive, AirDrop, network share, cloud drive.

Check the ZIP arrived intact. The printed hash must equal the one in `Export Vechile.zip.sha256`:
- macOS / Linux: `shasum -a 256 "Export Vechile.zip"`
- Windows PowerShell: `(Get-FileHash -Algorithm SHA256 "Export Vechile.zip").Hash.ToLower()`

## 3. Extract

- macOS: double-click the ZIP, or run `unzip "Export Vechile.zip"`.
- Windows: right-click → Extract All, or `Expand-Archive "Export Vechile.zip" -DestinationPath .`

You get one folder, `Export Vechile/`. **Keep its internal structure.** The FBX files find their textures through relative paths such as `../textures/...` and `../../shared/textures/...`.

## 4. Verify every file

The SHA-256 list covers every file except itself and `05_Manifests/PACKAGE_VERIFICATION_LOG.md`.

macOS / Linux:
```sh
cd "Export Vechile" && shasum -a 256 -c 05_Manifests/FILE_CHECKSUMS_SHA256.txt | grep -v ': OK$' ; echo "done"
```
Only `done` should print.


Windows PowerShell, from inside `Export Vechile`:
```powershell
Get-Content 05_Manifests/FILE_CHECKSUMS_SHA256.txt | ForEach-Object { $h, $p = $_ -split '  ', 2; if ((Get-FileHash -Algorithm SHA256 -LiteralPath $p).Hash.ToLower() -ne $h) { "FAIL $p" } }; "done"
```
Only `done` should print.

## 5. Put it in the Unity project

1. Keep the whole extracted folder **outside** `Assets/`, for example at `<UnityProject>/VehicleHandoff/Export Vechile/`. It holds the documentation and JSON; Unity should not import those as assets.
2. Copy **`01_Traffic_Vehicles/`** and **`02_Player_Vehicles/`** into the project, for example to `Assets/Vehicles/`. Keep each folder's internal layout:
   - `FBX/` must stay next to `textures/`;
   - the traffic `shared/textures/` must stay one level above the vehicle folders.
3. Before Unity finishes the first import, apply the importer settings in `README_UNITY_IMPORT.md`. The same settings are in machine-readable form in `04_Unity_Setup/Import_Settings/unity_import_settings.json`, if you want an `AssetPostprocessor` to apply them.
4. **Import only the 12 `*_complete_unity.fbx` files** listed above, and every PNG in their `textures/` folders plus `01_Traffic_Vehicles/shared/textures/`. You can leave the `reports/` folders and the `.md` / `.json` files inside 01/02 in place: Unity treats them as text assets and nothing references them.

## 6. Which materials need URP-specific setup

The FBX only carries base-colour and normal-map links. You must set up these by hand, as described in `MATERIAL_SETUP_GUIDE.md`:
- **Traffic paint:** AO is in the **red** channel of `<Paint>_Body_AO_Grime` and grime is in green, but URP Occlusion reads green. This needs a Shader Graph or a repacked texture. Paint also needs clear coat and the `TS_PaintFlake_Normal` detail normal.
- **Traffic lights:** `TS_Lights` is one material with 7 channels on cars and 8 on the truck and bus. The channel index is `round(TS_Lights_ChannelID.R × 15)`, and the emission comes from `TS_Lights_Emission`. This needs a small Shader Graph.
- **Atlas materials:** use `*_MetallicSmoothness.png` (R = metal, A = smoothness).
- **Hypercar:** its atlases ship as separate Metallic and Roughness maps. Pack them for URP (R = metal, A = 1 − roughness). Assign AO by hand.
- **Glass and lenses:** transparent, alpha values are per vehicle.

No Unity shaders or material scripts are included. None existed in a verified state, and untested shaders were not invented.

## 7. LOD Groups

Add a **LOD Group** on `Car_Root`. Put the renderers under `LOD0_Root` … `LOD3_Root` into LOD0 … LOD3. Unity will not build this automatically, because the meshes are grouped under per-LOD roots.

Starting screen heights:
- traffic: 50 / 22 / 8 / 1.5 %;
- player: 60 / 30 / 12 / 3 %.

Colliders, wheel references and `CenterOfMass` sit outside the LOD roots and are shared by all LODs.

## 8. Blender names → Unity roles

| FBX object | Role in Unity |
|---|---|
| `Car_Root` | Prefab root (LOD Group, plus Rigidbody only if the game uses physics for this vehicle) |
| `LOD0_Root` … `LOD3_Root` | LOD Group renderer sets |
| `Body_LODn` | Paint body (the paint material swaps per variant) |
| `Lights_LODn` | Lamp meshes (traffic: `TS_Lights` + lenses; player: per-channel LED materials) |
| `Wheel_FL/FR/RL/RR_LODn` | Visual wheel: rolls about local X; pivot is exactly on the wheel centre |
| `SteerPivot_FL/FR_LODn` | Steering: yaws about local Y and carries the front wheel and caliper |
| `Collision` / `Collision_*` | Optional convex reference hulls (MeshCollider Convex, renderers off) |
| `WheelColliderRef_FL/FR/RL/RR` | Wheel-centre markers (radius / width also stored as FBX user properties) |
| `CenterOfMass` | `rigidbody.centerOfMass = CenterOfMass.localPosition` (physics only) |

These names may differ from what the existing `VehicleVisual` expects. Map them, don't rename the FBX (`UNITY_INTEGRATION_GUIDE.md` §3).

## 9. Traffic without new physics

The current game uses **analytic collision** and near-miss detection, plus pooled traffic. **Do not add Rigidbody or WheelColliders to traffic.** The colliders and wheel references are optional resources. Use each vehicle's `traffic.footprint_override`, the collision-body size **without mirrors**, for `TrafficVehicleData`. See `UNITY_INTEGRATION_GUIDE.md`.

## 10. Dimensions and footprints

All values are in `VEHICLE_SPECS.md` and per vehicle in `04_Unity_Setup/Vehicle_Configuration/<vehicle>.json`: length, width (with the mirror flag), height, wheelbase, track, wheel positions / radius / width, centre of mass, colliders, LOD triangles, materials and light channels.

Visual widths include the mirrors. The recommended traffic footprints use the collision body without mirrors:

| Vehicle | Footprint W × L |
|---|---|
| Sedan A r3 | 1.81 × 4.65 m |
| Bus A v4 | 2.56 × 11.97 m |

## 11. What to check visually in Unity

For every vehicle:
- it imports with no missing-texture warnings;
- it stands on Y = 0 facing +Z, and its size matches `VEHICLE_SPECS.md`;
- LOD switching shows no popping of mirrors or lamps;
- paint shows clear coat with AO from R, and no "green AO" darkening;
- glass and lens transparency sort correctly;
- atlas cells don't bleed at distance;
- each light channel toggles on its own: brake vs tail, left vs right indicators, truck/bus markers;
- the night scene uses a night skybox or reflection probe, never black.

Full list: `06_QA/UNITY_PENDING_TESTS.md`.

## 12. What to test on Android

- Frame time and GPU time with a full traffic pool on the lowest and highest quality tiers.
- Draw calls per vehicle per LOD: traffic is about 19–20 at LOD0 and 13–14 at LOD1.
- Triangles per frame.
- ASTC texture memory.
- Transparent overdraw from glass.
- LOD distances on a phone screen.
- Thermal throttling over a 10-minute run.
- Night-scene readability.

The bus (34.5k LOD0), the truck and the player cars (74k–206k LOD0) are the risk items. See `UNITY_PENDING_TESTS.md` §6.

## Folder map

```
Export Vechile/
  00_Documentation/   START HERE, import, integration, materials, specs, inventory, validation report
  01_Traffic_Vehicles/<Vehicle>/   FBX/  textures/  reports/  README_<Base>.md
  01_Traffic_Vehicles/shared/textures/      fleet texture library (12 PNG, used by all 7)
  01_Traffic_Vehicles/_fleet_reference_20261010/   the original verified fleet README + handoff report
  02_Player_Vehicles/<Vehicle>/    FBX/  textures/  reports/  <PREFIX>_UNITY_IMPORT_NOTES.md (Hypercar: reports/unity_import_notes.md)
  04_Unity_Setup/Vehicle_Configuration/   one spec JSON per vehicle (for automated prefab / TrafficVehicleData setup)
  04_Unity_Setup/Import_Settings/         model + texture importer settings (JSON)
  05_Manifests/       COMPLETE_VEHICLE_MANIFEST.json, FILE_CHECKSUMS_SHA256.txt, DEPENDENCY_REPORT.md, verification log
  06_QA/              FBX / geometry validation, raw measurements, Unity pending tests
```

There is no `03_Shared_Assets/` folder. The traffic FBX files reference their shared textures at `../../shared/textures/` relative to `FBX/`, so the shared library has to sit at `01_Traffic_Vehicles/shared/textures/`. Moving it would break the references. Player cars share no textures.

## For Claude Code on the Unity machine

1. Read `05_Manifests/COMPLETE_VEHICLE_MANIFEST.json`. It holds every vehicle spec, the excluded list and the package checks.
2. Read the per-vehicle `04_Unity_Setup/Vehicle_Configuration/*.json` when you automate:
   - prefab building (LOD Group from `unity_import.lod_group`);
   - material remapping (`materials`, `textures.manual_setup`);
   - `TrafficVehicleData` (`traffic.footprint_override`, `dimensions_m`, `wheels`).
3. Treat everything in `validation.checks` as Blender-side only, and `unity_runtime` as NOT RUN.
4. Inspect the existing `TrafficVehicleData`, `VehicleVisual`, `TrafficSpawner` / `TrafficManager` code before mapping fields. This package does not know the Unity field names.
5. Never weaken the existing 15,000-triangle traffic validation just to make an import pass. Bring the six over-budget vehicles to the owner as a decision (`UNITY_INTEGRATION_GUIDE.md` §2).
