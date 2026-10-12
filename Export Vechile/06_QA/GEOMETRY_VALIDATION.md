# Geometry validation

Generated 2026-10-11. Each packaged `*_complete_unity.fbx` was parsed at FBX level (what Unity reads) and re-imported into a factory-clean Blender 5.2.2 scene, once in place and once from an independent copy of the package in a separate temporary folder outside the Blender project. Values are compared with each vehicle's release record. Raw data: `06_QA/fbx_measurements.json`.

| Vehicle | 09 | 10 | 11 | 12 | 13 | 15 |
|---|---|---|---|---|---|---|
| Sedan A r3 | PASS | PASS | PASS | PASS | PASS | PASS |
| Sedan B | PASS | PASS | PASS | PASS | PASS | PASS |
| Hatchback A r2 | PASS | PASS | PASS | PASS | PASS | PASS |
| SUV A v2 | PASS | PASS | PASS | PASS | PASS | PASS |
| SUV B v3 | PASS | PASS | PASS | PASS | PASS | PASS |
| Box Truck A r7 | PASS | PASS | PASS | PASS | PASS | PASS |
| Bus A v4 | PASS | PASS | PASS | PASS | PASS | PASS |
| Hypercar | PASS | PASS | PASS | PASS | PASS | PASS |
| Zero Gap R | PASS | PASS | PASS | PASS | PASS | PASS |
| Titan GT r1 | PASS | PASS | PASS | PASS | PASS | PASS |
| Vortex R r1 | PASS | PASS | PASS | PASS | PASS | PASS |
| Raven XR | PASS | PASS | PASS | PASS | PASS | PASS |

- **09**: All LODs preserved (LOD0-3)
- **10**: Triangle counts match the release manifest
- **11**: Wheel pivots match the validated source
- **12**: Collider references preserved
- **13**: Centre-of-mass reference preserved
- **15**: Light-channel data preserved

## Sedan A r3

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 14,961, LOD1 7,756, LOD2 3,546, LOD3 1,383
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.78, 0.316, 1.35]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 88, 'Collision_Cabin': 178, 'Collision_Front': 158, 'Collision_Rear': 184}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.52, 0.22] (release [-0.0, 0.52, 0.22])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 7 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse']

## Sedan B

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 17,987, LOD1 8,739, LOD2 4,012, LOD3 1,746
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.8125, 0.352, 1.62]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 94, 'Collision_Cabin': 152, 'Collision_Front': 152, 'Collision_Rear': 166}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.53, 0.08] (release [-0.0, 0.53, 0.08])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 7 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse']

## Hatchback A r2

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 17,174, LOD1 8,391, LOD2 3,887, LOD3 1,652
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.77, 0.317, 1.25]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 90, 'Collision_Cabin': 172, 'Collision_Front': 184, 'Collision_Rear': 194}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.5, 0.18] (release [-0.0, 0.5, 0.18])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 7 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse']

## SUV A v2

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 17,998, LOD1 8,768, LOD2 4,027, LOD3 1,728
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.8, 0.37, 1.32]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 74, 'Collision_Cabin': 182, 'Collision_Front': 172, 'Collision_Rear': 166}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.62, 0.12] (release [-0.0, 0.62, 0.12])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 7 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse']

## SUV B v3

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 19,840, LOD1 9,566, LOD2 4,325, LOD3 1,939
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.84, 0.391, 1.55]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 68, 'Collision_Cabin': 170, 'Collision_Front': 200, 'Collision_Rear': 190}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.7, 0.1] (release [-0.0, 0.7, 0.1])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 7 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse']

## Box Truck A r7

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 20,063, LOD1 10,765, LOD2 4,796, LOD3 2,591
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.84, 0.405, 2.3]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 76, 'Collision_Cabin': 128, 'Collision_Front': 174, 'Collision_Rear': 92}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 1.1, 0.4] (release [-0.0, 1.1, 0.4])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 8 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse', 'Marker']

## Bus A v4

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 34,506, LOD1 15,126, LOD2 6,210, LOD3 2,999
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-1.05, 0.478, 3.3]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 154, 'Collision_Cabin': 128, 'Collision_Front': 180, 'Collision_Rear': 174}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 1.1, -0.3] (release [-0.0, 1.1, -0.3])
- 15 Light-channel data preserved: **PASS**. TS_Lights channel faces decoded from UVs identical to the FBX audit on 4 Lights_LODn objects; 8 channels ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse', 'Marker']

## Hypercar

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 206,327, LOD1 107,210, LOD2 53,786, LOD3 17,747
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.835, 0.355, 1.39]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 6 convex hulls {'Collision_Body': 52, 'Collision_Cabin': 60, 'Collision_Front': 74, 'Collision_Rear': 76, 'Collision_Side_L': 64, 'Collision_Side_R': 66}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.35, -0.12] (release [-0.0, 0.35, -0.12])
- 15 Light-channel data preserved: **PASS**. emissive channel materials per LOD = release ({'LOD0': 6, 'LOD1': 6, 'LOD2': 6, 'LOD3': 5}); all 6 carry faces at LOD0

## Zero Gap R

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 89,681, LOD1 44,794, LOD2 20,372, LOD3 6,513
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.825, 0.345, 1.35]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 52, 'Collision_Cabin': 192, 'Collision_Front': 162, 'Collision_Rear': 170}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.37, -0.22] (release [-0.0, 0.37, -0.22])
- 15 Light-channel data preserved: **PASS**. 7 light-channel materials, LOD0 face counts = release geometry report

## Titan GT r1

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 77,370, LOD1 39,752, LOD2 18,527, LOD3 7,729
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.845, 0.347, 1.41]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 182, 'Collision_Cabin': 184, 'Collision_Front': 168, 'Collision_Rear': 150}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.42, -0.15] (release [-0.0, 0.42, -0.15])
- 15 Light-channel data preserved: **PASS**. 7 light-channel materials, LOD0 face counts = release geometry report

## Vortex R r1

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 73,665, LOD1 34,060, LOD2 15,026, LOD3 6,146
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.86, 0.339, 1.36]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 5 convex hulls {'Collision_Body': 168, 'Collision_Cabin': 166, 'Collision_Front': 184, 'Collision_Rear': 142, 'Collision_Wing': 14}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.38, -0.25] (release [-0.0, 0.38, -0.25])
- 15 Light-channel data preserved: **PASS**. 7 light-channel materials, LOD0 face counts = release geometry report

## Raven XR

- 09 All LODs preserved (LOD0-3): **PASS**. 4 LOD roots
- 10 Triangle counts match the release manifest: **PASS**. LOD0 74,271, LOD1 34,711, LOD2 15,185, LOD3 5,818
- 11 Wheel pivots match the validated source: **PASS**. 4 WheelColliderRef positions = release (Unity FL [-0.83, 0.331, 1.34]); 24 Wheel/SteerPivot pivots, max offset from ref 0.0000 mm; wheel mesh radius = release radius within 1 mm
- 12 Collider references preserved: **PASS**. 4 convex hulls {'Collision_Body': 186, 'Collision_Cabin': 148, 'Collision_Front': 176, 'Collision_Rear': 150}, no materials
- 13 Centre-of-mass reference preserved: **PASS**. CenterOfMass Unity [-0.0, 0.44, 0.08] (release [-0.0, 0.44, 0.08])
- 15 Light-channel data preserved: **PASS**. 7 light-channel materials, LOD0 face counts = release geometry report

