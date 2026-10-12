# FBX validation

Generated 2026-10-11. Each packaged `*_complete_unity.fbx` was parsed at FBX level (what Unity reads) and re-imported into a factory-clean Blender 5.2.2 scene, once in place and once from an independent copy of the package in a separate temporary folder outside the Blender project. Values are compared with each vehicle's release record. Raw data: `06_QA/fbx_measurements.json`.

| Vehicle | 02 | 03 | 05 | 06 | 07 | 08 | 14 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|
| Sedan A r3 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Sedan B | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Hatchback A r2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SUV A v2 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SUV B v3 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Box Truck A r7 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Bus A v4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Hypercar | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Zero Gap R | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Titan GT r1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Vortex R r1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| Raven XR | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

- **02**: Correct approved release version
- **03**: Complete FBX exists
- **05**: All paths resolve inside the portable package
- **06**: FBX hierarchy valid
- **07**: Model orientation (+Z forward, +Y up, -X left)
- **08**: Dimensions and scale (metres, scale 1, ground Y 0)
- **14**: Material names and assignments preserved
- **17**: No corrupted textures
- **18**: No unexpectedly missing dependencies

## Sedan A r3

- 02 Correct approved release version: **PASS**. FBX SHA-1 70361cfb6efe = release record; release 'Sedan A r3'; freeze manifest TS_SedanA_r3_FINAL_FREEZE.md unchanged since export (fa869fd4e3bc)
- 03 Complete FBX exists: **PASS**. TrafficSedanA_r3_complete_unity.fbx: 2,212,284 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 2.2772 (release 2.2772), tail -2.3721; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.6494 x 2.0600 x 1.4685 m vs release 4.6494 x 2.06 x 1.4685; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Sedan B

- 02 Correct approved release version: **PASS**. FBX SHA-1 eef0b9310911 = release record; release 'Sedan B'; freeze manifest TS_SedanB_FINAL_FREEZE.md unchanged since export (f9fdc7cd1280)
- 03 Complete FBX exists: **PASS**. TrafficSedanB_complete_unity.fbx: 2,581,804 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 2.4808 (release 2.4808), tail -2.4907; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.9715 x 2.1800 x 1.4934 m vs release 4.9716 x 2.18 x 1.4934; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Hatchback A r2

- 02 Correct approved release version: **PASS**. FBX SHA-1 e1808489b4b8 = release record; release 'Hatchback A r2'; freeze manifest TS_HatchA_r2_FINAL_FREEZE.md unchanged since export (b5747b1c5304)
- 03 Complete FBX exists: **PASS**. TrafficHatchbackA_r2_complete_unity.fbx: 2,472,108 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 2.1317 (release 2.1317), tail -2.1351; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.2668 x 2.0800 x 1.5158 m vs release 4.2668 x 2.08 x 1.5158; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## SUV A v2

- 02 Correct approved release version: **PASS**. FBX SHA-1 e8a197c42445 = release record; release 'SUV A v2'; freeze manifest TS_SUVA_FINAL_FREEZE.md unchanged since export (a91289cc6742)
- 03 Complete FBX exists: **PASS**. TrafficSUVA_complete_unity.fbx: 2,596,044 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 2.2445 (release 2.2446), tail -2.2340; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.4786 x 2.1900 x 1.7043 m vs release 4.4786 x 2.19 x 1.7043; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## SUV B v3

- 02 Correct approved release version: **PASS**. FBX SHA-1 2f3836ff6185 = release record; release 'SUV B v3'; freeze manifest TS_SUVB_FINAL_FREEZE.md unchanged since export (45387cb9dc64)
- 03 Complete FBX exists: **PASS**. TrafficSUVB_complete_unity.fbx: 2,836,636 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 2.4943 (release 2.4943), tail -2.4840; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.9783 x 2.3000 x 1.8109 m vs release 4.9783 x 2.3 x 1.8109; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Box Truck A r7

- 02 Correct approved release version: **PASS**. FBX SHA-1 05f3847d5c31 = release record; release 'Box Truck A r7'; freeze manifest TS_BoxTruckA_FINAL_FREEZE.md unchanged since export (b75247ff12d1)
- 03 Complete FBX exists: **PASS**. TrafficBoxTruckA_complete_unity.fbx: 2,607,948 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 3.5650 (release 3.565), tail -3.5050; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 7.0700 x 2.5440 x 3.2540 m vs release 7.07 x 2.544 x 3.254; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Bus A v4

- 02 Correct approved release version: **PASS**. FBX SHA-1 2c94b8758708 = release record; release 'Bus A v4'; freeze manifest TS_BusA_FINAL_FREEZE.md unchanged since export (2e3136287415)
- 03 Complete FBX exists: **PASS**. TrafficBusA_complete_unity.fbx: 3,997,036 bytes, 71 objects (release 71)
- 05 All paths resolve inside the portable package: **PASS**. 10 relative texture paths resolve in the package and in the portable copy; importer loaded 14 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; nose Z 5.9935 (release 5.9935), tail -6.0140; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 12.0075 x 2.9840 x 3.1980 m vs release 12.0075 x 2.984 x 3.198; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 8, LOD1 8, LOD2 8, LOD3 6); every face has a material
- 17 No corrupted textures: **PASS**. 12 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 14 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Hypercar

- 02 Correct approved release version: **PASS**. FBX SHA-1 cf5b184335ac = release record; re-exported from source checkpoints whose SHA-1 match final_export_manifest.json (REEXPORT_PROVENANCE.md)
- 03 Complete FBX exists: **PASS**. hypercar_complete_unity.fbx: 22,085,340 bytes, 308 objects (release 308)
- 05 All paths resolve inside the portable package: **PASS**. 30 relative texture paths resolve in the package and in the portable copy; importer loaded 30 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; body nose Z 2.3967 (release 2.3967), tail -2.2490; FL wheel at -X/+Z; authored pivot rotations only: ['ActiveSpoiler_LOD0', 'ActiveSpoiler_LOD1', 'ActiveSpoiler_LOD2', 'ActiveSpoiler_LOD3', 'Paddle_L_LOD0', 'Paddle_L_LOD1', 'Paddle_R_LOD0', 'Paddle_R_LOD1', 'SteeringWheel_LOD0', 'SteeringWheel_LOD1', 'SteeringWheel_LOD2']
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 6.0e-08, no negative scale; LOD0 L x W x H 4.6950 x 2.0523 x 1.1726 m (mirror objects excluded, as released) vs release 4.695 x 2.05233 x 1.17258; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. per-LOD material sets = release (LOD0 24, LOD1 24, LOD2 20, LOD3 15); every face has a material
- 17 No corrupted textures: **PASS**. 48 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 30 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Zero Gap R

- 02 Correct approved release version: **PASS**. FBX SHA-1 ed40e0666a1c = release record; FBX hash listed in ZG_FINAL_FREEZE.md
- 03 Complete FBX exists: **PASS**. ZeroGapR_complete_unity.fbx: 10,456,076 bytes, 110 objects (release 110)
- 05 All paths resolve inside the portable package: **PASS**. 7 relative texture paths resolve in the package and in the portable copy; importer loaded 10 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; body nose Z 2.2300 (release 2.23), tail -2.2300; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.4600 x 2.0060 x 1.1995 m vs release 4.46 x 2.006 x 1.1995; ground Y +0.0015
- 14 Material names and assignments preserved: **PASS**. 15 materials = export manifest; per LOD [15, 15, 15, 15]; every face has a material
- 17 No corrupted textures: **PASS**. 8 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 10 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Titan GT r1

- 02 Correct approved release version: **PASS**. FBX SHA-1 3b535d63f6d2 = release record; FBX hash listed in TG_R1_FINAL_FREEZE.md
- 03 Complete FBX exists: **PASS**. TitanGT_complete_unity.fbx: 8,833,692 bytes, 102 objects (release 102)
- 05 All paths resolve inside the portable package: **PASS**. 7 relative texture paths resolve in the package and in the portable copy; importer loaded 10 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; body nose Z 2.3744 (release 2.3744), tail -2.4382; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.8141 x 2.2300 x 1.2720 m vs release 4.8141 x 2.23 x 1.272; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. 15 materials = export manifest; per LOD [15, 15, 15, 15]; every face has a material
- 17 No corrupted textures: **PASS**. 8 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 10 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Vortex R r1

- 02 Correct approved release version: **PASS**. FBX SHA-1 23476c898cf1 = release record; FBX hash listed in VX_R1_FINAL_FREEZE.md
- 03 Complete FBX exists: **PASS**. VortexR_complete_unity.fbx: 7,024,940 bytes, 103 objects (release 103)
- 05 All paths resolve inside the portable package: **PASS**. 7 relative texture paths resolve in the package and in the portable copy; importer loaded 10 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; body nose Z 2.3000 (release 2.3), tail -2.2599; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.5800 x 2.2700 x 1.2750 m vs release 4.58 x 2.27 x 1.275; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. 15 materials = export manifest; per LOD [15, 15, 15, 15]; every face has a material
- 17 No corrupted textures: **PASS**. 8 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 10 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

## Raven XR

- 02 Correct approved release version: **PASS**. FBX SHA-1 a771b12414f9 = release record; FBX hash listed in RV_FINAL_FREEZE.md
- 03 Complete FBX exists: **PASS**. RavenXR_complete_unity.fbx: 7,014,076 bytes, 102 objects (release 102)
- 05 All paths resolve inside the portable package: **PASS**. 7 relative texture paths resolve in the package and in the portable copy; importer loaded 10 images, all from inside the copy
- 06 FBX hierarchy valid: **PASS**. single root Car_Root; children 10 incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names
- 07 Model orientation (+Z forward, +Y up, -X left): **PASS**. FBX axes Up +Y / Front +Z / Coord +X; body nose Z 2.3000 (release 2.3), tail -2.2200; FL wheel at -X/+Z; all node rotations identity
- 08 Dimensions and scale (metres, scale 1, ground Y 0): **PASS**. UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation 0.0e+00, no negative scale; LOD0 L x W x H 4.5210 x 2.0460 x 1.3200 m vs release 4.521 x 2.046 x 1.32; ground Y -0.0000
- 14 Material names and assignments preserved: **PASS**. 15 materials = export manifest; per LOD [15, 15, 15, 15]; every face has a material
- 17 No corrupted textures: **PASS**. 8 PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for 10 linked images
- 18 No unexpectedly missing dependencies: **PASS**. no missing or external dependency; the portable-copy measurement is identical to the in-place one

