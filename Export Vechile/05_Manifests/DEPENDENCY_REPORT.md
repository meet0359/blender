# Dependency report

Every FBX references its textures by **relative path** (no embedded media). All paths below were resolved from the FBX location inside this package and from an independent copy; Blender's importer loaded every linked image from inside the copy.

Each FBX also stores the absolute path of the folder it was written from on the Blender Mac (`/Users/meetshah/...` or a scratch folder). That path is informational only and does not exist on the Unity machine; it exposes the local user name. Unity resolves the relative path first.

## Sedan A r3 (`01_Traffic_Vehicles/Traffic_Sedan_A_r3/FBX/TrafficSedanA_r3_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_SedanA_Body_Normal.png`, `../textures/TS_SedanA_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`, `01_Traffic_Vehicles/Traffic_Sedan_A_r3/textures/TS_SedanA_Body_AO_Grime.png`

## Sedan B (`01_Traffic_Vehicles/Traffic_Sedan_B/FBX/TrafficSedanB_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_SedanB_Body_Normal.png`, `../textures/TS_SedanB_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`, `01_Traffic_Vehicles/Traffic_Sedan_B/textures/TS_SedanB_Body_AO_Grime.png`

## Hatchback A r2 (`01_Traffic_Vehicles/Traffic_Hatchback_A_r2/FBX/TrafficHatchbackA_r2_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_HatchA_Body_Normal.png`, `../textures/TS_HatchA_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/Traffic_Hatchback_A_r2/textures/TS_HatchA_Body_AO_Grime.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`

## SUV A v2 (`01_Traffic_Vehicles/Traffic_SUV_A_v2/FBX/TrafficSUVA_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_SUVA_Body_Normal.png`, `../textures/TS_SUVA_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`, `01_Traffic_Vehicles/Traffic_SUV_A_v2/textures/TS_SUVA_Body_AO_Grime.png`

## SUV B v3 (`01_Traffic_Vehicles/Traffic_SUV_B_v3/FBX/TrafficSUVB_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_SUVB_Body_Normal.png`, `../textures/TS_SUVB_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`, `01_Traffic_Vehicles/Traffic_SUV_B_v3/textures/TS_SUVB_Body_AO_Grime.png`

## Box Truck A r7 (`01_Traffic_Vehicles/Traffic_Box_Truck_A_r7/FBX/TrafficBoxTruckA_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_BoxTruckA_Body_Normal.png`, `../textures/TS_BoxTruckA_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/Traffic_Box_Truck_A_r7/textures/TS_BoxTruckA_Body_AO_Grime.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`

## Bus A v4 (`01_Traffic_Vehicles/Traffic_Bus_A_v4/FBX/TrafficBusA_complete_unity.fbx`)

- Relative references in the FBX (10): `../../shared/textures/TS_Atlas_BaseColor.png`, `../../shared/textures/TS_Atlas_Metallic.png`, `../../shared/textures/TS_Atlas_Normal.png`, `../../shared/textures/TS_Atlas_Roughness.png`, `../../shared/textures/TS_Lights_BaseColor.png`, `../../shared/textures/TS_Tire_BaseColor.png`, `../../shared/textures/TS_Tire_Normal.png`, `../../shared/textures/TS_Tire_Roughness.png`, `../textures/TS_BusA_Body_Normal.png`, `../textures/TS_BusA_Body_Normal_LOD1.png`
- Resolved: 10, unresolved: 0; embedded media 0; absolute paths stored 10
- Not linked by the FBX, required for the URP material setup: `01_Traffic_Vehicles/shared/textures/TS_Atlas_MetallicSmoothness.png`, `01_Traffic_Vehicles/Traffic_Bus_A_v4/textures/TS_BusA_Body_AO_Grime.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_ChannelID.png`, `01_Traffic_Vehicles/shared/textures/TS_Lights_Emission.png`, `01_Traffic_Vehicles/shared/textures/TS_PaintFlake_Normal.png`

## Hypercar (`02_Player_Vehicles/Hypercar/FBX/hypercar_complete_unity.fbx`)

- Relative references in the FBX (30): `../textures/hypercar/body/BODY_BaseColor.png`, `../textures/hypercar/body/BODY_Metallic.png`, `../textures/hypercar/body/BODY_Normal.png`, `../textures/hypercar/body/BODY_Roughness.png`, `../textures/hypercar/brakes/BRAKES_BaseColor.png`, `../textures/hypercar/brakes/BRAKES_Metallic.png`, `../textures/hypercar/brakes/BRAKES_Normal.png`, `../textures/hypercar/brakes/BRAKES_Roughness.png`, `../textures/hypercar/interior/INTERIOR_BaseColor.png`, `../textures/hypercar/interior/INTERIOR_Metallic.png`, `../textures/hypercar/interior/INTERIOR_Normal.png`, `../textures/hypercar/interior/INTERIOR_Roughness.png`, `../textures/hypercar/lights/LIGHTS_BaseColor.png`, `../textures/hypercar/lights/LIGHTS_Metallic.png`, `../textures/hypercar/lights/LIGHTS_Normal.png`, `../textures/hypercar/lights/LIGHTS_Roughness.png`, `../textures/hypercar/tires/TIRES_BaseColor.png`, `../textures/hypercar/tires/TIRES_Metallic.png`, `../textures/hypercar/tires/TIRES_Normal.png`, `../textures/hypercar/tires/TIRES_Roughness.png`, `../textures/hypercar/trim/TRIM_BaseColor.png`, `../textures/hypercar/trim/TRIM_Metallic.png`, `../textures/hypercar/trim/TRIM_Normal.png`, `../textures/hypercar/trim/TRIM_Roughness.png`, `../textures/hypercar/trim/carbon_twill_BaseColor.png`, `../textures/hypercar/trim/carbon_twill_Normal.png`, `../textures/hypercar/wheels/WHEELS_BaseColor.png`, `../textures/hypercar/wheels/WHEELS_Metallic.png`, `../textures/hypercar/wheels/WHEELS_Normal.png`, `../textures/hypercar/wheels/WHEELS_Roughness.png`
- Resolved: 30, unresolved: 0; embedded media 0; absolute paths stored 30
- Not linked by the FBX, required for the URP material setup: `02_Player_Vehicles/Hypercar/textures/hypercar/body/BODY_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/brakes/BRAKES_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/glass/GLASS_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/interior/INTERIOR_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/lights/LIGHTS_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/tires/TIRES_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/trim/TRIM_AO.png`, `02_Player_Vehicles/Hypercar/textures/hypercar/wheels/WHEELS_AO.png`

## Zero Gap R (`02_Player_Vehicles/ZeroGapR/FBX/ZeroGapR_complete_unity.fbx`)

- Relative references in the FBX (7): `../textures/ZG_Carbon_BaseColor.png`, `../textures/ZG_Carbon_Normal.png`, `../textures/ZG_Palette_BaseColor.png`, `../textures/ZG_Palette_Metallic.png`, `../textures/ZG_Palette_Roughness.png`, `../textures/ZG_Tire_BaseColor.png`, `../textures/ZG_Tire_Normal.png`
- Resolved: 7, unresolved: 0; embedded media 0; absolute paths stored 7
- Not linked by the FBX, required for the URP material setup: `02_Player_Vehicles/ZeroGapR/textures/ZG_Palette_MetallicSmoothness.png`

## Titan GT r1 (`02_Player_Vehicles/TitanGT_r1/FBX/TitanGT_complete_unity.fbx`)

- Relative references in the FBX (7): `../textures/TG_Carbon_BaseColor.png`, `../textures/TG_Carbon_Normal.png`, `../textures/TG_Palette_BaseColor.png`, `../textures/TG_Palette_Metallic.png`, `../textures/TG_Palette_Roughness.png`, `../textures/TG_Tire_BaseColor.png`, `../textures/TG_Tire_Normal.png`
- Resolved: 7, unresolved: 0; embedded media 0; absolute paths stored 7
- Not linked by the FBX, required for the URP material setup: `02_Player_Vehicles/TitanGT_r1/textures/TG_Palette_MetallicSmoothness.png`

## Vortex R r1 (`02_Player_Vehicles/VortexR_r1/FBX/VortexR_complete_unity.fbx`)

- Relative references in the FBX (7): `../textures/VX_Carbon_BaseColor.png`, `../textures/VX_Carbon_Normal.png`, `../textures/VX_Palette_BaseColor.png`, `../textures/VX_Palette_Metallic.png`, `../textures/VX_Palette_Roughness.png`, `../textures/VX_Tire_BaseColor.png`, `../textures/VX_Tire_Normal.png`
- Resolved: 7, unresolved: 0; embedded media 0; absolute paths stored 7
- Not linked by the FBX, required for the URP material setup: `02_Player_Vehicles/VortexR_r1/textures/VX_Palette_MetallicSmoothness.png`

## Raven XR (`02_Player_Vehicles/RavenXR/FBX/RavenXR_complete_unity.fbx`)

- Relative references in the FBX (7): `../textures/RV_Carbon_BaseColor.png`, `../textures/RV_Carbon_Normal.png`, `../textures/RV_Palette_BaseColor.png`, `../textures/RV_Palette_Metallic.png`, `../textures/RV_Palette_Roughness.png`, `../textures/RV_Tire_BaseColor.png`, `../textures/RV_Tire_Normal.png`
- Resolved: 7, unresolved: 0; embedded media 0; absolute paths stored 7
- Not linked by the FBX, required for the URP material setup: `02_Player_Vehicles/RavenXR/textures/RV_Palette_MetallicSmoothness.png`

## Not shipped on purpose

- `*_LOD0_unity_test.fbx`: LOD0-only subsets of the complete FBX; not needed in Unity.
- Source `.blend` files, previews, scripts: Blender-side only. No FBX links to them.
- `TS_Lights_State` (traffic): a Blender-only 4 x 4 review mask, not used by Unity.

