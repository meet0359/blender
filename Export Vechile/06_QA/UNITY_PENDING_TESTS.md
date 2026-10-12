# Unity pending tests (P0-05, on the Unity machine)

Every item below is **NOT RUN**. No Unity editor or device was available on the Blender Mac. Tick each item in Unity and record the result.

## 1. Package integrity

- [ ] `Export Vechile.zip` SHA-256 equals `Export Vechile.zip.sha256`.
- [ ] `05_Manifests/FILE_CHECKSUMS_SHA256.txt` verifies with no failures (commands in `README_START_HERE.md` §4).

## 2. Import (each of the 12 `*_complete_unity.fbx`)

- [ ] No missing-texture warnings. All relative paths resolve after copying `01_Traffic_Vehicles/` and `02_Player_Vehicles/` into `Assets/`.
- [ ] Imported with Scale Factor 1, Convert Units on, Bake Axis Conversion off.
- [ ] 1 unit = 1 m, and the vehicle stands on Y = 0 facing +Z.
- [ ] Bounds match `VEHICLE_SPECS.md`, for example Bus A v4: 12.008 × 2.984 × 3.198 m.
- [ ] `Car_Root` rotation (0, 0, 0) and scale 1.
- [ ] FL wheel at −X / +Z.
- [ ] Object count per FBX matches the spec JSON: 71 for traffic; 308 / 110 / 102 / 103 / 102 for Hypercar / Zero Gap R / Titan GT r1 / Vortex R r1 / Raven XR.
- [ ] Tangents (traffic: Calculate Mikktspace) show no seams on body-normal bakes.

## 3. Prefab and LOD Group

- [ ] LOD Group on `Car_Root` with `LOD0_Root` … `LOD3_Root` renderers.
- [ ] Switching heights tuned. No popping of mirrors, lamps or wheels between LODs.
- [ ] Draw calls per LOD as expected: traffic about 19–20 / 13–14 / … ; LOD3 uses 6 materials.
- [ ] Wheels roll about local X and front steer pivots yaw about local Y, on all four LOD copies. Roll sign checked per side.
- [ ] Traffic prefabs carry **no** Rigidbody or WheelColliders. `Collision_*` disabled or stripped.

## 4. Materials (per `MATERIAL_SETUP_GUIDE.md`)

- [ ] Traffic paint: AO taken from **R** of `_AO_Grime`, grime from G, clear coat, flake detail normal. No "green AO" look.
- [ ] Paint variants are material instances only.
- [ ] Atlas: MetallicSmoothness (Metallic Alpha). No cell bleed at distance.
- [ ] Glass / lenses: transparency sorting against paint, interior and the other lens.
- [ ] Player cars: palette MetallicSmoothness, point filter. Carbon tiling. Tyre lettering.
- [ ] Zero Gap R PB-1: tail-lens colour in daylight.
- [ ] Hypercar: MetallicSmoothness packed from Metallic + (1 − Roughness). AO assigned. Clear coat.

## 5. Lights

- [ ] Traffic `TS_Lights`: each channel toggles independently via the intensity array (DRL, Headlamp, Tail, Brake, Indicator_L, Indicator_R, Reverse; truck and bus also Marker).
- [ ] Brake is distinct from tail. Indicators blink per side.
- [ ] `TS_Lights_ChannelID` imported with Point filter / no compression / no mip maps. No channel bleeding at distance.
- [ ] Player LED materials: 7 channels each. Hypercar: 6 emissive materials; its indicators blink together (known).
- [ ] Night scene with a night skybox or reflection probe (never black). Vehicles readable at rear-follow distances of 7.5 / 22 / 60 m.

## 6. Android (target devices)

- [ ] Full traffic pool on the lowest and highest quality tiers: CPU and GPU frame time within the game's target.
- [ ] Triangles per frame and draw calls per frame with the pool at its maximum. Test bus- and truck-heavy spawns separately.
- [ ] Texture memory with ASTC: traffic shares one 12-PNG library; each traffic vehicle adds 3 bakes (2048 / 1024 / 1024). Hypercar atlases go up to 4096.
- [ ] Transparent overdraw (glass, lenses) in dense traffic.
- [ ] LOD distances on a phone screen. Low tier may start traffic at LOD1.
- [ ] 10-minute thermal run, with no sustained throttling beyond the game's existing baseline.
- [ ] Player cars: LOD0 at 73.7k–89.7k triangles in the chase camera. Hypercar (206k LOD0) only on the high tier, or starting at LOD1+.

## 7. Gameplay compatibility

- [ ] `TrafficVehicleData` uses `traffic.footprint_override` (mirrors excluded). Analytic collision and near-miss behave the same as the old vehicles of the same class.
- [ ] `TrafficSpawner` / `TrafficManager`: spawn gaps and lane occupancy correct for the 7.07 m truck and the 12.01 m bus.
- [ ] Pooling: spawn / despawn cycles keep LOD Group and light state. No per-instance material leaks.
- [ ] Camera modes: no clipping or occlusion problems behind the truck and bus.
- [ ] `RoadStreamer` unaffected (no vehicle data touches road streaming).
- [ ] The existing 15,000-triangle validation still passes or fails truthfully. The owner has decided on the over-budget vehicles (`UNITY_INTEGRATION_GUIDE.md` §2).

## 8. Sign-off

- [ ] Record the results here, or in the Unity project's QA log, and only then retire the old traffic prefabs.
