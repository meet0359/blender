# P2-BLENDER-02 — Premium City / Urban Highway Environment

Digest 08 of the environment handoff. Folder: `environment/P2_City/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/city_07_export_ready.blend`
- **Asset index source:** `reports/P2_city_geometry.json` + `reports/P2_city_export_manifest.json`
- **Checkpoints (7):** `city_01_blockout.blend`, `city_02_buildings.blend`, `city_03_facades_rooftops.blend`, `city_04_clusters.blend`, `city_05_materials_uv.blend`, `city_06_lods_hlod_collision.blend`, `city_07_export_ready.blend`
- **FBX (11):** `City_Office.fbx` (30 objects), `City_Residential.fbx` (30 objects), `City_Commercial.fbx` (28 objects), `City_ServiceParking.fbx` (45 objects), `City_Landmarks.fbx` (10 objects), `City_UrbanStructures.fbx` (44 objects), `City_Rooftops.fbx` (30 objects), `City_Clusters.fbx` (41 objects), `City_Skyline.fbx` (26 objects), `City_Collision.fbx` (27 objects), `city_complete.fbx` (311 objects)
- **Textures:** 33 PNG files · **Previews:** 32 renders · **UnityTransfer README:** `CITY_IMPORT_NOTES.md`, `CITY_MATERIAL_GUIDE.md`, `CITY_PERFORMANCE_GUIDE.md`, `CITY_PLACEMENT_GUIDE.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `Building_Podium_A` | 1,274 / 442 / 82 / 18 | City_UrbanStructures.fbx |
| `Building_Podium_B` | 964 / 444 / 92 / 36 | City_UrbanStructures.fbx |
| `City_Landmark_A` | 7,804 / 5,368 / 1,476 / 460 | City_Landmarks.fbx |
| `City_Landmark_B` | 7,308 / 4,124 / 2,300 / 460 | City_Landmarks.fbx |
| `Commercial_Block_A` | 1,520 / 460 / 172 / 44 | City_Commercial.fbx |
| `Commercial_Block_A_V2` | 1,388 / 356 / 148 / 36 | City_Commercial.fbx |
| `Commercial_Block_B` | 1,972 / 572 / 132 / 36 | City_Commercial.fbx |
| `Commercial_Podium_A` | 756 / 292 / 92 / 36 | City_UrbanStructures.fbx |
| `Facade_Commercial_4m` | 42 / 18 | City_UrbanStructures.fbx |
| `Facade_OfficeConcrete_4m` | 54 / 30 | City_UrbanStructures.fbx |
| `Facade_OfficeGlass_4m` | 60 / 18 | City_UrbanStructures.fbx |
| `Facade_Residential_4m` | 54 / 30 | City_UrbanStructures.fbx |
| `Facade_Service_4m` | 54 / 30 | City_UrbanStructures.fbx |
| `Hotel_Midrise_A` | 7,482 / 2,562 / 578 / 76 | City_Commercial.fbx |
| `Hotel_Midrise_A_V2` | 9,066 / 3,138 / 698 / 84 | City_Commercial.fbx |
| `Office_Midrise_A` | 1,924 / 724 / 308 / 68 | City_Office.fbx |
| `Office_Midrise_A_V2` | 1,900 / 708 / 260 / 60 | City_Office.fbx |
| `Office_Midrise_B` | 2,272 / 580 / 252 / 60 | City_Office.fbx |
| `Office_Tower_A` | 4,498 / 2,174 / 926 / 158 | City_Office.fbx |
| `Office_Tower_A_V2` | 4,086 / 1,902 / 926 / 158 | City_Office.fbx |
| `Office_Tower_B` | 10,228 / 3,676 / 1,020 / 116 | City_Office.fbx |
| `ParkingGarage_A` | 2,370 / 834 / 154 / 64 | City_ServiceParking.fbx |
| `ParkingGarage_B` | 2,858 / 1,352 / 122 / 56 | City_ServiceParking.fbx |
| `ParkingGarage_RampVisual_A` | 108 / 58 | City_ServiceParking.fbx |
| `ParkingGarage_Roof_A` | 236 / 124 | City_ServiceParking.fbx |
| `ParkingPodium_A` | 2,450 / 1,182 / 90 / 48 | City_ServiceParking.fbx |
| `Residential_Midrise_A` | 5,016 / 1,324 / 340 / 52 | City_Residential.fbx |
| `Residential_Midrise_A_V2` | 3,796 / 1,228 / 300 / 52 | City_Residential.fbx |
| `Residential_Midrise_B` | 3,218 / 1,034 / 282 / 34 | City_Residential.fbx |
| `Residential_Tower_A` | 15,968 / 4,020 / 1,004 / 132 | City_Residential.fbx |
| `Residential_Tower_A_V2` | 9,100 / 3,300 / 1,052 / 116 | City_Residential.fbx |
| `Residential_Tower_B` | 10,510 / 4,510 / 2,902 / 338 | City_Residential.fbx |
| `Roof_Antenna_A` | 196 / 28 | City_Rooftops.fbx |
| `Roof_Chiller_A` | 198 / 12 | City_Rooftops.fbx |
| `Roof_Cluster_A` | 600 / 48 | City_Rooftops.fbx |
| `Roof_Cluster_B` | 676 / 128 | City_Rooftops.fbx |
| `Roof_HVAC_A` | 70 / 12 | City_Rooftops.fbx |
| `Roof_HVAC_B` | 114 / 12 | City_Rooftops.fbx |
| `Roof_Railing_A` | 72 / 36 | City_Rooftops.fbx |
| `Roof_ServiceRoom_A` | 28 / 24 | City_Rooftops.fbx |
| `Roof_Vent_A` | 72 / 20 | City_Rooftops.fbx |
| `Roof_WaterTank_A` | 168 / 104 | City_Rooftops.fbx |
| `ServiceBuilding_A` | 598 / 256 / 82 / 18 | City_ServiceParking.fbx |
| `Urban_Fence_A` | 684 / 360 | City_UrbanStructures.fbx |
| `Urban_RetainingWall_A` | 136 / 24 | City_UrbanStructures.fbx |
| `Urban_RetainingWall_B` | 60 / 48 | City_UrbanStructures.fbx |
| `Urban_ServiceWall_A` | 74 / 24 | City_UrbanStructures.fbx |
| `UtilityBuilding_A` | 294 / 174 / 50 / 18 | City_ServiceParking.fbx |
| `Warehouse_Urban_A` | 832 / 176 / 144 / 54 | City_ServiceParking.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `City_Clusters.fbx` (41): CityCluster_Mid_A, CityCluster_Mid_A_HLOD (550), CityCluster_Mid_A__Commercial_Block_B_03 (572), CityCluster_Mid_A__Office_Midrise_A_V2_02 (708), CityCluster_Mid_A__Office_Tower_B_00 (3,676), CityCluster_Mid_A__Residential_Tower_B_01 (4,510), CityCluster_Mid_B, CityCluster_Mid_B_HLOD (392), CityCluster_Mid_B__Hotel_Midrise_A_V2_03 (3,138), CityCluster_Mid_B__Office_Tower_A_V2_01 (1,902), CityCluster_Mid_B__Residential_Midrise_B_02 (1,034), CityCluster_Mid_B__Residential_Tower_A_V2_00 (3,300), CityCluster_Mid_C, CityCluster_Mid_C_HLOD (272), CityCluster_Mid_C__Commercial_Block_A_V2_03 (356), CityCluster_Mid_C__Office_Midrise_A_00 (724), CityCluster_Mid_C__Office_Tower_B_02 (3,676), CityCluster_Mid_C__Residential_Midrise_A_V2_01 (1,228), CityCluster_Near_A, CityCluster_Near_A_HLOD (266), CityCluster_Near_A__City_RooftopSign_A_04 (86), CityCluster_Near_A__Commercial_Block_A_01 (1,520), CityCluster_Near_A__Office_Tower_A_00 (4,498), CityCluster_Near_A__ParkingGarage_A_02 (2,370), CityCluster_Near_A__ServiceLot_A_03 (60), CityCluster_Near_A__Urban_Fence_A_05 (684), CityCluster_Near_B, CityCluster_Near_B_HLOD (278), CityCluster_Near_B__Hotel_Midrise_A_02 (7,482), CityCluster_Near_B__Residential_Midrise_A_01 (5,016), CityCluster_Near_B__Residential_Tower_A_00 (15,968), CityCluster_Near_B__UrbanConcretePad_A_04 (60), CityCluster_Near_B__UtilityBuilding_A_03 (294), CityCluster_Near_C, CityCluster_Near_C_HLOD (188), CityCluster_Near_C__BuildingLoadingArea_A_05 (228), CityCluster_Near_C__Office_Midrise_B_00 (2,272), CityCluster_Near_C__ParkingGarage_B_01 (2,858), CityCluster_Near_C__ParkingSurface_A_04 (104), CityCluster_Near_C__ServiceBuilding_A_03 (598), CityCluster_Near_C__Warehouse_Urban_A_02 (832)
- `City_Collision.fbx` (27): Collision_City_Landmark_A (12), Collision_City_Landmark_B (12), Collision_Commercial_Block_A (24), Collision_Commercial_Block_A_V2 (24), Collision_Commercial_Block_B (24), Collision_Hotel_Midrise_A (24), Collision_Hotel_Midrise_A_V2 (24), Collision_Office_Midrise_A (24), Collision_Office_Midrise_A_V2 (24), Collision_Office_Midrise_B (24), Collision_Office_Tower_A (36), Collision_Office_Tower_A_V2 (36), Collision_Office_Tower_B (24), Collision_ParkingGarage_A (12), Collision_ParkingGarage_B (12), Collision_Residential_Midrise_A (24), Collision_Residential_Midrise_A_V2 (24), Collision_Residential_Midrise_B (12), Collision_Residential_Tower_A (24), Collision_Residential_Tower_A_V2 (24), Collision_Residential_Tower_B (36), Collision_ServiceBuilding_A (12), Collision_UrbanWall_Noise (12), Collision_UrbanWall_Retaining (12), Collision_UrbanWall_Service (12), Collision_UtilityBuilding_A (12), Collision_Warehouse_Urban_A (12)
- `City_Commercial.fbx` (3): City_RooftopSign_A (86), City_SignPanel_A (14), City_SignPanel_B (28)
- `City_ServiceParking.fbx` (9): BuildingLoadingArea_A (228), City_ServiceDoor_A (50), City_TransformerBox_A (86), City_UtilityCabinet_A (26), City_UtilityCabinet_B (26), City_VentUnit_A (14), ParkingSurface_A (104), ServiceLot_A (60), UrbanConcretePad_A (60)
- `City_Skyline.fbx` (26): CityCluster_Skyline_A, CityCluster_Skyline_A_HLOD (1,944), CityCluster_Skyline_A__Office_Tower_A_03 (158), CityCluster_Skyline_A__Residential_Tower_B_06 (338), CityCluster_Skyline_A__Skyline_Tower_A_00 (248), CityCluster_Skyline_A__Skyline_Tower_B_02 (306), CityCluster_Skyline_A__Skyline_Tower_C_04 (160), CityCluster_Skyline_A__Skyline_Tower_D_01 (296), CityCluster_Skyline_A__Skyline_Tower_E_07 (94), CityCluster_Skyline_A__Skyline_Tower_F_05 (344), CityCluster_Skyline_B, CityCluster_Skyline_B_HLOD (1,696), CityCluster_Skyline_B__Office_Tower_B_04 (116), CityCluster_Skyline_B__Residential_Tower_A_06 (132), CityCluster_Skyline_B__Skyline_Tower_A_03 (248), CityCluster_Skyline_B__Skyline_Tower_B_07 (306), CityCluster_Skyline_B__Skyline_Tower_C_02 (160), CityCluster_Skyline_B__Skyline_Tower_D_00 (296), CityCluster_Skyline_B__Skyline_Tower_E_05 (94), CityCluster_Skyline_B__Skyline_Tower_F_01 (344), Skyline_Tower_A (248), Skyline_Tower_B (306), Skyline_Tower_C (160), Skyline_Tower_D (296), Skyline_Tower_E (94), Skyline_Tower_F (344)
- `City_UrbanStructures.fbx` (2): Urban_NoiseWall_A (68), Urban_NoiseWall_B (64)

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `reports/P2_city_FINAL_REPORT.md`

### P2-BLENDER-02 — Premium City / Urban Highway Environment — FINAL REPORT

Date: 2026-10-07 · Blender 5.2, Blender-only (no Unity) · Status: **COMPLETE, FROZEN**. Figures below come from `P2_city_validation.txt`, `P2_city_geometry.json` and the reviewed previews.

1. **Discovery:** road kit and P1 prop corridor out to \|x\| 16 m; streetlights at x −12.0 m; gantry sign bottom 6.0 m; P2 Overpass_Hero soffit 6.18 m; P1 tunnel portal 31.2 × 10.6 m; driver camera 1.15 m, chase camera 2.4 m. Details in `P2_city_discovery.md`.
2. **Source integrity:** **PASS.** All 1,244 frozen files are byte-for-byte unchanged: P0 95, Props 77, Terrain 166, Vegetation 257, Tunnel 113, Bridges 123, BridgeTerrainContext 73, cars 108, other 232. No files changed or added.
3. **City art direction:** a modern, international, generic business / mixed-use city. Warm-grey concrete and stone, red brick, neutral to slightly cool glass (no bright blue), dark painted metal fins, invented signage only.
4. **Urban corridor strategy:** P0 road plus P1 props out to \|x\| 16 m, urban walls at \|x\| ≈ 17 m, setback trees and service lots, then façades from 20–35 m.
5. **Near / mid / far layers:**

   | Layer | Distance | Content |
   |---|---|---|
   | Near | 20–80 m | LOD0 / LOD1, real recesses, balconies, fins, rooftop clusters |
   | Mid | 80–250 m | LOD1 / LOD2 clusters |
   | Far | 250 m – 1.6 km | LOD3, skyline towers, skyline clusters, HLOD |

6. **Building families:** 16 primary archetypes (LOD0–3) plus 6 restrained variants (`_V2`). Variants change material, window category, floor count, podium or roof; none are made by scaling.
7. **Office:**

   | Asset | Description | Height |
   |---|---|---|
   | Office_Tower_A | curtain wall, setback crown | 136 m |
   | Office_Tower_B | punched windows | 94 m |
   | Office_Midrise_A | curtain wall | 42 m |
   | Office_Midrise_B | ribbon windows, panel atlas | 41 m |

8. **Residential:**

   | Asset | Description | Height |
   |---|---|---|
   | Residential_Tower_A | render, balconies with glass rails | 94 m |
   | Residential_Tower_B | chamfered, cool | 117 m |
   | Residential_Midrise_A | brick, balconies | 27 m |
   | Residential_Midrise_B | render | 23 m |

9. **Commercial:** Commercial_Block_A (27 m, ribbon / commercial panels), Commercial_Block_B (17 m, stone), Hotel_Midrise_A (51 m, with invented ARIA HOTEL sign). Also City_SignPanel_A / _B and City_RooftopSign_A.
10. **Service:** Warehouse_Urban_A (12 m, 3 loading docks), ServiceBuilding_A, UtilityBuilding_A.
11. **Parking:** ParkingGarage_A (4 levels) and _B (3 levels with a fin screen): open bays, columns on an 8 m grid, 1.05 m upstands, ramp hint, cores, ceiling lights. Also ParkingPodium_A, ParkingGarage_RampVisual_A and ParkingGarage_Roof_A. Exterior only.
12. **Landmarks:**
    - **City_Landmark_A** (262.7 m): a tapering glass tower that twists 1.6° per floor, with a glass pyramid crown and mast.
    - **City_Landmark_B** (205.7 m): a stepped, chamfered octagon with dark glass, fins and an open "sky frame" crown with lit inner edges.
    - Both are original designs and distinct at 200, 500 and 1,000 m (`P2_city_landmark_{A,B}_{200,500,1000}m.png`).
13. **Building heights:** service 5–12 m, commercial 17–27 m, midrises 23–61 m, towers 81–136 m, landmarks 206–263 m, skyline towers 56–215 m.
14. **Window scale (measured, check 11):**
    - Office: curtain-wall panel 1.5 m, punched 1.8 × 2.4 m, ribbon 1.6 m modules.
    - Residential: 1.2–1.5 × 1.5–1.7 m. Hotel: 1.4 × 1.8 m. Storefront: 2.6 × 3.4 m.
    - One atlas cell equals one window. **PASS.**
15. **Floor-height audit (check 12):** office 3.8–3.9 m, residential 3.1–3.2 m, hotel 3.3 m, ground-floor commercial 4.8 m, upper commercial 4.2 m, parking 3.1 m. LOD0 window rows step by exactly one floor height. **PASS.** Full detail in `P2_city_scale_audit.md`.
16. **Façade system:**
    - One façade generator with 16 dimension styles: curtain, punched or ribbon windows, recess depth 0.15–0.35 m, slab-edge bands, fins, balconies and canopies.
    - Modules Facade_OfficeGlass / OfficeConcrete / Residential / Commercial / Service_4m (LOD0–1).
    - Podiums Building_Podium_A / B and Commercial_Podium_A.
17. **Rooftop system:** HVAC A / B, vent, chiller, water tank, antenna (red aviation light), service room, railing, plus the clustered assemblies Roof_Cluster_A / B. Clusters are merged into building LOD0 / LOD1, a single service room stays at LOD2, and LOD3 / skyline have none.
18. **Urban walls / noise barriers:** Urban_RetainingWall_A (counterforts) and _B (terraced); Urban_NoiseWall_A (solid acoustic) and _B (single-layer acrylic); Urban_ServiceWall_A (brick plus door); Urban_Fence_A. All are 8 m modules.
19. **Utility / service kit:** City_UtilityCabinet_A / B, City_TransformerBox_A, City_ServiceDoor_A, City_VentUnit_A. Ground pieces: ServiceLot_A, ParkingSurface_A (with lines), BuildingLoadingArea_A (with bollards), UrbanConcretePad_A.
20. **Materials:** 15 shared `MAT_City_*` materials: Concrete, ConcreteDark, Glass, GlassClear, Window, Brick, Stone, PaintedMetal, Galvanized, Roof, AsphaltRoof, Signage, Facade, Ground, Light.
21. **Trim sheet:** T_City_Trim_2K (BaseColor / Normal / Roughness / Metallic / AO), 13 strips, U tiles every 4 m.
22. **Façade atlas:** T_City_Facade_2K with 4 strips (office panel, residential render, commercial batten, service rib). Each strip is one floor band.
23. **Window atlas:** T_City_Windows_2K, 16 × 16 cells in 7 categories (office bright / dark, residential warm / cool, commercial, hotel, utility). Each cell has a frame, a painted interior and a restrained reflection.
24. **Emission mask:** T_City_WindowEmissionMask_2K, with per-window warm / cool / neutral colour and black for unlit. Lit share per category runs 3–56 %. The CityWindowData vertex colour carries random, floor and category values per window.
25. **Night-lighting strategy:**
    - Emission is stored as data: window mask, sign emissive, light fixtures, red aviation lights.
    - Per-building lit share is 16–67 % (check 17), so no façade is fully lit.
    - The Blender preview uses a `NightEmission` value saved at 0. Unity owns the final intensities.
26. **Glass strategy:** opaque neutral spandrel glass plus window cells with painted interiors. Transparency only on the acrylic noise wall and balcony rails (one layer). No complex Blender-only glass.
27. **UV strategy:**
    - Tileable concrete, stone, brick, roof and ground are box-mapped in world space (a tower spans 37 V tiles).
    - Façade, trim, window and sign faces stay inside their atlas regions (checks 13, 15, 16, 18).
    - No unique per-building textures.
28. **Texel density:**
    - Near: 512 px/m for concrete, stone and trim; 1,024 px/m for brick; 70–85 px/m per window cell.
    - Mid: same textures at LOD1 / LOD2.
    - Far: window atlas on 2-floor bands plus flat concrete.
29. **LOD strategy:**
    - LOD0: real recesses, balconies, fins, slab bands, rooftop clusters.
    - LOD1: flush windows, thinned fins and bands, simplified roof.
    - LOD2: per-floor window bands and a service room.
    - LOD3: tier masses with 2-floor bands.
    - Removed first: rooftop detail, balconies, canopies. Preserved: mass, setbacks, podium, floor rhythm (check 19, 49 groups).
30. **Triangle counts (LOD0 → LOD3):**

    | Asset | LOD0 | LOD1 | LOD2 | LOD3 |
    |---|---|---|---|---|
    | Office_Tower_A | 4,498 | 2,174 | 926 | 158 |
    | Office_Tower_B | 10,228 | 3,676 | 1,020 | 116 |
    | Residential_Tower_A | 15,968 | 4,020 | 1,004 | 132 |
    | Residential_Tower_B | 10,510 | 4,510 | 2,902 | 338 |
    | Hotel_Midrise_A | 7,482 | 2,562 | 578 | 76 |
    | City_Landmark_A | 7,804 | 5,368 | 1,476 | 460 |
    | City_Landmark_B | 7,308 | 4,124 | 2,300 | 460 |

    Skyline towers are 94–344 tris each.
31. **Clusters:** CityCluster_Near_A / B / C, _Mid_A / B / C and _Skyline_A / B. Each holds 4–8 instances that share building meshes and keep individual buildings available.
32. **HLOD-ready assets:** each cluster has a merged `<Cluster>_HLOD`: near 188–278 tris, mid 272–550 tris, skyline 1,696–1,944 tris.
33. **Skyline system:** 6 Skyline_Tower_* meshes (94–344 tris, window bands only) plus the skyline clusters. In QA they sit at 420–520 m frontage, with extra towers at 1.4–1.65 km.
34. **Collision:** 27 closed boxes (max 36 tris): buildings per tier, landmarks, garages, retaining / noise / service walls. No per-window, rooftop or skyline collision.
35. **Day QA:** **PASS.** Buildings read as distinct concrete, glass, brick and stone volumes with real depth and shadows, not flat grey or plastic boxes (`P2_city_full_environment.png`, `_near_cluster.png`, `_mid_cluster.png`, `_facade_closeup.png`, libraries).
36. **Driver QA:** **PASS** (`P2_city_driver_view.png`, `_windows_scale.png`). Window and storefront scale reads correctly next to cars and floors, and the road stays open and readable.
37. **Chase QA:** **PASS** (`P2_city_chase_view.png`). Near façade depth, varied buildings, skyline layering.
38. **High-chase QA:** **PASS** (`P2_city_high_chase.png`, `_high_chase_golden.png`). Roofs carry HVAC, service rooms, tanks and antennas; garages and service areas read; no empty roofs everywhere.
39. **Side-depth QA:** **PASS** (`P2_city_side_depth.png`). Highway, near, mid and far skyline layers all visible.
40. **Golden-hour QA:** **PASS** (`P2_city_golden_hour.png`). Long shadows, façade depth, glass response.
41. **Night QA:** **PASS** (`P2_city_night.png`, `_chase_view_night.png`). Mixed occupancy with warm / cool differences, silhouettes identifiable, garage lights and aviation-light accents, no neon overload.
42. **Repetition QA:** **PASS** (check 27). The same building mesh is at least 142 m apart in the near / mid layers, helped by variants, rotations, cluster mixing and roof swaps.
43. **Overpass integration QA:** **PASS** (`P2_city_overpass.png`). Frozen P2 Overpass_Hero sits in the business district with the P2 abutment-terrain embankments; its V-piers stay readable.
44. **Tunnel approach QA:** **performed.** The 1 km strip ends with Urban_RetainingWall runs into the frozen P1 tunnel portal, with buildings on the QA deck above it (seen in `P2_city_full_environment.png` and `_skyline.png`).
45. **Checkpoints:** `blend/city_01_blockout` … `city_06_lods_hlod_collision`, then `city_07_export_ready.blend` (the final source), each written once. All WIP iterations went to the session scratchpad.
46. **Previews:** 32 images in `previews/`: all 21 required (`P2_city_*`) plus the landmark 200 / 500 / 1,000 m set, chase night, high-chase golden, landmark / skyline / façade-module libraries.
47. **FBXs:** `exports/city_complete.fbx`, City_Office, City_Residential, City_Commercial, City_ServiceParking, City_Landmarks, City_UrbanStructures, City_Rooftops, City_Clusters, City_Skyline, City_Collision. 11 files, 311 objects. Axis-bake residual is 2.4e-5 m (float32 rounding at about 250 m instance offsets; tolerance 1e-4).
48. **FBX re-import:** **all 11 PASS.** Names, hierarchy, triangles, UVs, materials and CityWindowData match; world deviation ≤ 3.1e-5 m; Unity +Y up (Office_Tower_A spans Y 0 … 135.84) and +Z forward (wall module Z 0 … 8.0).
49. **Validation:** **40 checks, 0 errors, 0 warnings.** That is all 29 required checks plus topology and the 11 per-FBX re-imports.
50. **UnityTransfer:** `environment/P2_City/UnityTransfer/` (FBX ×11, Textures, Reports ×10, README ×4).
51. **Import notes:** `UnityTransfer/README/CITY_IMPORT_NOTES.md` (all 18 topics, Blender-only statement).
52. **Material guide:** `UnityTransfer/README/CITY_MATERIAL_GUIDE.md`.
53. **Placement guide:** `UnityTransfer/README/CITY_PLACEMENT_GUIDE.md`.
54. **Performance guide:** `UnityTransfer/README/CITY_PERFORMANCE_GUIDE.md` (concepts only, no FPS claims).
55. **Freeze report:** `reports/P2_city_FINAL_FREEZE.md` with SHA-1 hashes. `environment/P2_City/` is **FROZEN**.
56. **Known limitations:**
    - **Triangle guidance:** most buildings are below the LOD0 guidance (Office_Tower_A 4.5k vs 8–25k). Nothing was padded; depth comes from recesses, fins and bands.
    - **LOD ratios:** LOD1 ratios vary (some below 40 %) because recesses and balconies drop at LOD1.
    - **Not created (optional):** no parallax-interior atlas, no decals, no rain preview.
    - **Session cameras:** the landmark-distance and skyline previews use elevated render-session cameras. The saved ground-level QA cameras are blocked by the near layer. No saved file was changed (checkpoint hash verified before and after).
    - **QA ground:** QA urban ground and the tunnel hill are preview-only.
    - **Landmark collider:** City_Landmark_A's collider stops at the roof (214 m); the 48 m crown and mast are not collidable.
57. **Recommended next Blender phase:** **P3 Mountain / Coastal** (`environment/P3_MountainCoastal/`, empty). Recommendation only; not started.

---

### `UnityTransfer/README/CITY_IMPORT_NOTES.md`

### City / Urban Highway — Unity import notes (P2-BLENDER-02)

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.** Unity-side materials, window / night emission, reflections, real lights, LODGroup / HLOD setup, culling, quality tiers and performance testing must be completed on the Unity workstation.

1. **Orientation:** Unity +Y up, +Z forward (traffic). This uses the same in-memory axis bake as every earlier package (G = Rot(−90°, X), Apply Transform OFF). Blender (x, y, z) → Unity (−x, z, −y).
2. **Scale:** 1 unit = 1 m. Use Scale Factor 1 with Convert Units ON.
3. **Building families:**

   | Family | Assets |
   |---|---|
   | Office | Office_Tower_A / B, Office_Midrise_A / B |
   | Residential | Residential_Tower_A / B, Residential_Midrise_A / B |
   | Commercial | Commercial_Block_A / B, Hotel_Midrise_A |
   | Service | Warehouse_Urban_A, ServiceBuilding_A, UtilityBuilding_A |
   | Landmark | City_Landmark_A (twisting glass tower + spire), City_Landmark_B (stepped octagon + sky frame) |
   | Variants | Office_Tower_A_V2, Office_Midrise_A_V2, Residential_Tower_A_V2, Residential_Midrise_A_V2, Commercial_Block_A_V2, Hotel_Midrise_A_V2 |
4. **Distance layers:**
   - near 20–80 m: building LOD0 / LOD1;
   - mid 80–250 m: LOD1 / LOD2 or `CityCluster_Mid_*`;
   - far 250 m–1.5 km+: LOD3, `Skyline_Tower_*`, `CityCluster_Skyline_*`, `<Cluster>_HLOD`.
5. **FBX list:**

   | File | Contents |
   |---|---|
   | city_complete.fbx | everything below |
   | City_Office.fbx, City_Residential.fbx | |
   | City_Commercial.fbx | incl. signage, ground pads |
   | City_ServiceParking.fbx | |
   | City_Landmarks.fbx | |
   | City_UrbanStructures.fbx | walls, podiums, façade modules |
   | City_Rooftops.fbx | |
   | City_Clusters.fbx | near + mid clusters |
   | City_Skyline.fbx | skyline towers + skyline clusters |
   | City_Collision.fbx | |
6. **Building LODs:** a root empty `<Asset>` with children `<Asset>_LOD0..3`.
   - LOD0: recessed windows / balconies / fins / slab bands / rooftop clusters.
   - LOD1: flush windows, simplified roof.
   - LOD2: per-floor window bands.
   - LOD3: tier masses + 2-floor bands.
   - Suggested screen heights: 0.5 / 0.25 / 0.1 / 0.03.
7. **Cluster / HLOD sources:**
   - `CityCluster_*` roots hold instance children named `<Cluster>__<Asset>_<nn>`. They share the building meshes (Near → LOD0, Mid → LOD1, Skyline → LOD3 / skyline), so they can be swapped for the building prefabs.
   - `<Cluster>_HLOD` is the merged far representation.
   - Cluster origin = frontage-line centre, local +X toward the road. Mirror placement (180°) for the other side.
8. **Window atlas:** `T_City_Windows_2K` (BaseColor / Normal / Roughness). One cell = one physical window; 7 category bands.
9. **Emission mask:** `T_City_WindowEmissionMask_2K`, RGB = per-window emission colour, black = off. Plus colour set `CityWindowData`: R random, G floor fraction, B category / 8, A window flag.
10. **Materials:** `MAT_City_Concrete`, `_ConcreteDark`, `_Glass`, `_GlassClear`, `_Window`, `_Brick`, `_Stone`, `_PaintedMetal`, `_Galvanized`, `_Roof`, `_AsphaltRoof`, `_Signage`, `_Facade`, `_Ground`, `_Light`.
11. **Trim sheet:** `T_City_Trim_2K` (BaseColor / Normal / Roughness / Metallic / AO), 13 strips, U 4 m.
12. **Rooftop assets:** `Roof_HVAC_A / B`, `Roof_Vent_A`, `Roof_Chiller_A`, `Roof_WaterTank_A`, `Roof_Antenna_A` (red aviation light), `Roof_ServiceRoom_A`, `Roof_Railing_A`, plus clustered `Roof_Cluster_A / B`. These are already merged into the building LOD0 / LOD1.
13. **Parking / service assets:** `ParkingGarage_A / B`, `ParkingPodium_A`, `ParkingGarage_RampVisual_A`, `ParkingGarage_Roof_A` (exterior only, no drivable interior); utility cabinets, transformer, service door, vent unit; ServiceLot / ParkingSurface / LoadingArea / ConcretePad.
14. **Urban structures:** `Urban_RetainingWall_A / B`, `Urban_NoiseWall_A` (solid acoustic) / `_B` (single-layer acrylic), `Urban_ServiceWall_A`, `Urban_Fence_A`. 8 m modules along the road; the road-facing face is local +X. Also podiums (`Building_Podium_A / B`, `Commercial_Podium_A`) and `Facade_*_4m` modules.
15. **Collision:** `City_Collision.fbx`, 27 closed boxes: buildings per tier (`Collision_<Building>`), landmarks, garages, urban walls (retaining / noise / service). No per-window or rooftop collision.
16. **Intended highway setback:** walls at \|x\| ≈ 17 m; first building frontage at **20–35 m** from the centreline; mid layer 80–250 m; skyline 250 m–1.5 km.
17. **Night-light expectations:**
    - Drive the window emission from mask × `CityWindowData` × time-of-night.
    - Signs use their Emissive mask; red aviation lights on tall tops; garage `MAT_City_Light` fixtures.
    - Unity decides the intensities and which real lights exist. **No Blender light values are final.**
18. **Excluded QA assets:** the CITY_QA strip is not exported (linked P0 road, P1 terrain / props / vegetation, P1 tunnel, P2 Overpass_Hero + abutment terrain, hypercar, QA urban ground / tunnel hill, strip + library instances, 40 m chunk guides), and neither are the cameras or lights.

---

### `UnityTransfer/README/CITY_PLACEMENT_GUIDE.md`

### City placement guide (straight / level 40 m highway)

#### Layers
| Layer | Distance from centreline | Use |
|---|---|---|
| Near | 20–80 m | individual buildings at LOD0 / 1, podiums, garages, service pads, `CityCluster_Near_*`, urban walls at ≈ 17 m |
| Mid | 80–250 m | `CityCluster_Mid_*` (LOD1 instances) or individual LOD1 / 2 |
| Far | 250 m – 1.5 km+ | `CityCluster_Skyline_*`, `Skyline_Tower_*`, building LOD3, `<Cluster>_HLOD`; landmarks 300 m – 1 km |

#### Setback principles
- Keep the P0 road kit + P1 props corridor (to \|x\| 16 m) clear.
- Put urban walls / fences at \|x\| ≈ 17 m.
- Start building frontages at 20–35 m. Towers go further back (≥ 30 m) than podiums / commercial blocks.
- Use service lots, parking surfaces and setback trees between the wall line and the façades.

#### Clusters
- **Origin:** frontage-line centre, local +X toward the road.
- **Right side:** place at x = −frontage. **Left side:** rotate 180° and place at x = +frontage.
- **Spacing:** clusters span about 120–150 m of road (3–4 chunks). Align the cluster centre with a 40 m chunk boundary or chunk centre (the QA strip has `CityChunk_nn` guides every 40 m), but buildings do not need 40 m footprints.
- **Variety:** alternate near clusters A / B / C, put a different mid cluster behind each, and keep skyline clusters as a continuous backdrop.

#### Overpass and tunnel
- **Overpasses:** put an urban overpass (P2 `Overpass_Hero` / `_Standard`) on a normal chunk with the P2 `BridgeAbutmentTerrain_L/R` embankments. Keep buildings ≥ 45 m from the overpass centre on both sides so the abutments and V-piers stay readable.
- **Tunnel approach:** end the urban corridor with `Urban_RetainingWall_A` runs into the P1 tunnel portal (`Tunnel_Entry_40m` + `Tunnel_Portal_Entry`). Buildings may sit on the deck above the tunnel.

#### Vegetation
Reuse P1 vegetation sparingly:
- small roadside trees at 18–21 m;
- shrubs along retaining walls;
- no dense forest in the urban section.

No new vegetation assets were created.

#### Repetition avoidance
- Do not repeat the same building within about 120 m on the same side.
- Swap in the `_V2` variants; use 90° / 180° rotations only.
- Vary the cluster order and keep the rooftop kit varied.
- The QA strip passes the 120 m same-mesh rule (validation check 27).

---

### `UnityTransfer/README/CITY_MATERIAL_GUIDE.md`

### City material guide (Unity)

- **Façade materials:**
  - concrete / stone / brick: tileable, box-mapped at 4 / 4 / 2 m per tile.
  - `MAT_City_Facade`: 4-strip atlas, one strip per floor band. Do not change V tiling.
  - All share URP Lit with mask maps; use the same shader for every opaque city material so instancing / SRP batching works.
- **Glass:**
  - `MAT_City_Glass`: opaque spandrel glass. Keep it neutral / slightly cool; add a reflection probe or SSR. No bright-blue glass.
  - `MAT_City_GlassClear`: one transparent layer, double-sided. Use it only for the acrylic noise wall and balcony rails; switch to opaque on mobile.
- **Window masks and night emission:**
  - `MAT_City_Window` = window BaseColor (interior painted in) + emission mask (RGB colour, black = off).
  - Per-window control comes from vertex colour `CityWindowData`:
    - **R** random → on / off threshold that moves with time of night;
    - **G** floor → e.g. darker upper office floors late at night;
    - **B** category;
    - **A** = 1 on window faces.
  - Keep total lit share around 15–45 %. **Never light every window.**
- **Fake interiors:** not provided; the cells contain painted interiors. A parallax-interior atlas can be added later with the same per-cell UVs.
- **Trim sheet:** `T_City_Trim_2K` (13 strips): painted / dark / galvanized metal, mullion, balcony edge, parapet, service door, vent louvres, utility metal, sign frame, spandrel glass, paint line.
- **Concrete:** `T_City_Concrete_2K` (BaseColor / Normal / Roughness / AO); ConcreteDark is a tint of the same set.
- **Metal:** trim strips only; no per-object metal textures.
- **Sharing / GPU instancing:** 15 materials cover the whole kit. Enable GPU instancing on all opaque city materials. Clusters reference the same meshes (instances), and repeated buildings / walls / rooftop kit share meshes and materials.

---

### `UnityTransfer/README/CITY_PERFORMANCE_GUIDE.md`

### City performance guide (concepts only — no Unity measurements were taken)

#### PC
- **Near:** LOD0 within about 80 m, LOD1 to about 200 m.
- **Mid:** LOD1 / LOD2 (mid clusters use LOD1 instances); switch to `<Cluster>_HLOD` beyond about 400 m.
- **Far:** skyline meshes / HLOD only. Each skyline cluster HLOD is a few thousand triangles.
- **Windows:** the full window shader (per-window randomisation, warm / cool, floor variation). Optionally add parallax interiors later.

#### Mobile
- **LODs:** aggressive switching (about 0.5× PC distances). HLOD for mid clusters from about 200 m.
- **Windows:** simplified emission (mask only, no per-window animation).
- **Glass:** opaque everywhere (swap `MAT_City_GlassClear` for an opaque variant or remove the acrylic noise walls).
- **Rooftops:** keep the rooftop kit only on LOD0 / LOD1.
- **Distance:** fewer skyline instances; fog / sky for the far horizon.
- **Sharing:** GPU instancing + material sharing (15 materials, shared atlases).

#### General
- Skyline towers and LOD3 avoid window, balcony and rooftop geometry.
- Colliders are simple boxes; buildings beyond the near layer need no collider.
- Clusters are instances of shared meshes, so memory stays low even with many placements.

---

### `reports/P2_city_materials.md`

### P2-BLENDER-02 — City materials, atlases and night data

These are Blender **source / preview** materials, not Unity shaders.

| Material | Texture | Use | UV / scale |
|---|---|---|---|
| `MAT_City_Concrete` | T_City_Concrete_2K | frames, slabs, piers, parapets, walls, garages | box-projected, 4 m / tile (512 px/m) |
| `MAT_City_ConcreteDark` | Concrete × 0.55 | curtain-wall backing (LOD3), recess reveals, ramps | 4 m |
| `MAT_City_Brick` | T_City_Brick_2K | residential / utility / service walls | 2 m / tile (1024 px/m), 0.25 × 0.083 m bricks |
| `MAT_City_Stone` | T_City_Stone_2K | podiums, hotel, commercial, landmark crown | 4 m, 1.0 × 0.5 m ashlar |
| `MAT_City_Facade` | T_City_Facade_2K | office panel, residential render, commercial batten, service ribbed walls | 4 strips; **one strip = one floor band**, U 4 m / tile |
| `MAT_City_Window` | T_City_Windows_2K + T_City_WindowEmissionMask_2K | all windows | one cell = one window (128 px); 7 categories |
| `MAT_City_Glass` | trim `glass_spandrel` | curtain-wall spandrels, landmark spire glass | opaque, restrained neutral / cool |
| `MAT_City_GlassClear` | trim `glass_spandrel`, alpha 0.35 | transparent noise wall, balcony rails | **single layer** only |
| `MAT_City_PaintedMetal` / `MAT_City_Galvanized` | T_City_Trim_2K | fins, canopies, rooftop kit, rails, posts, doors, louvres | trim strips, U 4 m |
| `MAT_City_Roof` / `MAT_City_AsphaltRoof` | T_City_Roof_2K (× 0.42 for asphalt) | membrane roofs / gravel-asphalt roofs + parking surface | 8 m / tile |
| `MAT_City_Ground` | T_City_Ground_2K | service lots, concrete pads | 8 m / tile (2 m pavers) |
| `MAT_City_Signage` | T_City_Signs_1K (+ Emissive mask) | invented signs (NOVA, METRO HUB, ARIA HOTEL, KAIRO, ATLAS PLAZA, P), warning lights | atlas rects |
| `MAT_City_Light` | emissive source colour | garage ceiling lights, landmark crown strips, roof lamp heads | n/a |

#### Trim sheet `T_City_Trim_2K` (BaseColor / Normal / Roughness / Metallic / AO)
Strips, as px from the bottom:

| Strip | px |
|---|---|
| concrete_frame | 0–192 |
| painted_metal | 192–352 |
| dark_metal | 352–512 |
| mullion | 512–608 |
| balcony_edge | 608–768 |
| roof_parapet | 768–960 |
| service_door | 960–1216 |
| vent | 1216–1408 |
| utility_metal | 1408–1568 |
| sign_frame | 1568–1664 |
| galvanized | 1664–1792 |
| glass_spandrel | 1792–1984 |
| paint_line | 1984–2048 |

U tiles every 4 m.

#### Window atlas `T_City_Windows_2K` (BaseColor / Normal / Roughness) + `T_City_WindowEmissionMask_2K`
- **Layout:** 16 × 16 cells, 128 px each. Rows from the top:

  | Rows | Category |
  |---|---|
  | 0–2 | office bright |
  | 3–4 | office dark (tinted) |
  | 5–7 | residential warm (curtains) |
  | 8–9 | residential cool (blinds) |
  | 10–11 | commercial storefront |
  | 12–13 | hotel |
  | 14–15 | utility (louvres / frosted) |

- **Cell content:** frame, mullion / transom, interior (ceiling lights, desks, curtains, blinds, shop shelves), plus a restrained neutral / cool reflection gradient. No bright-blue glass.
- **Emission mask:** RGB = emission colour of a lit window (warm / cool / neutral, intensity 0.45–1.0), dimmed behind blinds / curtains; black = unlit.
- **Lit probability per category:** office bright 0.42, office dark 0.22, residential warm 0.36, residential cool 0.30, commercial 0.62, hotel 0.40, utility 0.06.
- **Vertex data:** `CityWindowData` (corner colour) — R per-window random, G floor fraction, B category id / 8, A 1 on window faces. Unity can switch windows on / off over time, vary warm / cool, or darken by floor without new textures.
- **Interior parallax:** not provided (optional). The window cells already contain a painted interior. A `T_City_InteriorRooms_2K` can be added later without changing UVs.

#### Façade atlas `T_City_Facade_2K` (BaseColor / Normal / Roughness)
4 strips of 512 px: `office_panel`, `residential_render`, `commercial_panel`, `service_wall`. Façade faces are built per floor, so each face's V spans exactly one floor band in one strip.

#### Night-light strategy
- **Sources:** emission is DATA. The window mask × an intensity Unity controls; sign Emissive mask; `MAT_City_Light` source colour; red aviation-light faces (sign atlas `Lens_Red`) on towers, landmarks and skyline tops.
- **Blender preview:** the night preview drives a `NightEmission` value node (preview only, saved at 0). Final intensities, bloom and exposure belong to Unity.

#### Texel density
| Layer | Density |
|---|---|
| Near | concrete / stone 512 px/m, brick 1024 px/m, trim 512 px/m along U, window cells about 70–85 px/m |
| Mid | the same textures at LOD1 / LOD2 |
| Far | LOD3 / skyline use only the window atlas (2 floors per quad) + flat concrete |

#### Unity expectations
- **Shaders:** URP Lit for concrete / brick / stone / façade / trim / roof (mask map = Metallic + 1 − Roughness); a city window shader (emission from mask × per-window data × time-of-day); single-layer transparent for GlassClear.
- **Reflections:** reflection probes or SSR for glass.
- **Batching:** GPU instancing of shared materials.

---

### `reports/P2_city_scale_audit.md`

### P2-BLENDER-02 — City scale audit

The previous city failed on wrong-scale windows, flat boxes and no floor rhythm. In this kit **every facade is generated from one fixed dimension table**, so scale cannot drift per building.

- **Validation measured it, not just declared it:**
  - window size on every LOD0 / LOD1 window face, as face size ÷ atlas-cell span (`P2_city_geometry.json → window_sizes_m`);
  - the LOD0 window-row step equals the floor height on every archetype (validation checks 11–12).
- **Atlas mapping:** one atlas cell = one physical window at LOD0 / LOD1. LOD2 / LOD3 keep the bay rhythm as window bands (one cell per bay), so the window count and floor count are preserved at distance.

#### Facade dimension table (metres)
| Style | Kind | Window category | Floor-to-floor | Bay | Window width | Window height | Sill / spandrel | LOD0 recess |
|---|---|---|---|---|---|---|---|---|
| `curtain_office` | curtain | office_bright | 3.9 | 1.5 | 1.5 | 2.6 | 0.85 | 0.00 |
| `curtain_dark` | curtain | office_dark | 3.9 | 1.5 | 1.5 | 2.5 | 0.90 | 0.00 |
| `curtain_mid` | curtain | office_bright | 3.8 | 1.5 | 1.5 | 2.5 | 0.85 | 0.00 |
| `punched_office` | punched | office_dark | 3.9 | 3.0 | 1.8 | 2.4 | 0.90 | 0.35 |
| `ribbon_office` | ribbon | office_dark | 3.8 | 1.6 | 1.6 | 1.9 | 0.95 | 0.30 |
| `res_tower` | punched | res_warm | 3.1 | 3.0 | 1.4 | 1.6 | 0.90 | 0.25 |
| `res_tower_b` | punched | res_cool | 3.1 | 3.2 | 1.5 | 1.7 | 0.85 | 0.25 |
| `res_mid` | punched | res_warm | 3.1 | 2.8 | 1.2 | 1.5 | 0.90 | 0.22 |
| `res_mid_b` | punched | res_cool | 3.2 | 2.6 | 1.2 | 1.5 | 0.90 | 0.22 |
| `hotel` | punched | hotel | 3.3 | 2.4 | 1.4 | 1.8 | 0.75 | 0.28 |
| `storefront` | punched | commercial | 4.8 | 3.0 | 2.6 | 3.4 | 0.35 | 0.30 |
| `commercial_up` | ribbon | commercial | 4.2 | 2.0 | 2.0 | 2.2 | 1.00 | 0.30 |
| `commercial_big` | punched | commercial | 4.2 | 4.0 | 2.0 | 2.6 | 0.90 | 0.35 |
| `service` | punched | utility | 4.0 | 3.5 | 1.2 | 1.2 | 1.50 | 0.18 |
| `utility` | punched | utility | 5.0 | 4.0 | 1.2 | 0.9 | 3.00 | 0.15 |
| `industrial` | ribbon | utility | 9.0 | 2.0 | 2.0 | 1.2 | 6.60 | 0.20 |

- **Curtain wall:** one panel = one 1.5 m cell (inside the 1.2–1.8 m bay rule). Vision glass is 2.5–2.6 m; spandrel glass and a 0.3 m slab-edge band make up the rest of the 3.8–3.9 m floor.
- **Ribbon windows:** the mullion module is 1.6 m (office) or 2.0 m (commercial).

#### Against the city scale standard
| Rule | Standard | This kit | Result |
|---|---|---|---|
| Office floor-to-floor | 3.6–4.2 | 3.8 / 3.9 (landmarks 4.0) | PASS |
| Residential floor-to-floor | 3.0–3.4 | 3.1 / 3.2 (hotel 3.3) | PASS |
| Ground-floor commercial | 4–5 | 4.8 (upper commercial 4.2) | PASS |
| Office windows | 1.2–2.0 wide | 1.5 (curtain panel), 1.6 (ribbon), 1.8 × 2.4 (punched) | PASS |
| Residential windows | 0.9–1.5 wide | 1.2 / 1.4 / 1.5 × 1.5–1.7 | PASS |
| Curtain-wall bay | 1.2–1.8 | 1.5 | PASS |

#### Doors and service scale
| Element | Size |
|---|---|
| `City_ServiceDoor_A` | 1.0 × 2.1 m leaf, 1.2 × 2.2 m frame |
| Warehouse dock doors | 3.6 × 4.2 m, 1.2 m dock level, 4.8 × 3.5 m canopy at 5.6 m |
| Storefront panes | 2.6 × 3.4 m in a 3.0 m bay; canopy 1.8 m deep at 4.3 m |

#### Parking structures
| Element | Value |
|---|---|
| Deck spacing | floor-to-floor 3.1 m, 0.3 m slab, **2.8 m clear** |
| Edge protection | 1.05 m solid upstand + rail at 1.15–1.2 m |
| Structure | columns 0.6 × 0.6 m on an 8 m grid |
| Ramp | rises 3.1 m over 30 m (≈ 10 %) |
| Cores | 6 × 6 m stair / lift cores |
| Light fixtures | 1.2 m ceiling fixtures every 8 m |

#### Car and guardrail comparison (linked frozen references)
- **Hypercar:** about 4.69 × 2.21 × 1.55 m.
- **Car vs building:** an office storey (3.9 m) ≈ 2.5 car heights; an office window (1.8 × 2.4) ≈ 1.5 car heights tall; a residential window (1.4 × 1.6) ≈ one car height; a storefront pane (2.6 × 3.4) ≈ 2.2 car heights.
- **Guardrail:** the P1 W-beam guardrail top (≈ 0.75 m) is about the residential sill (0.9 m).
- **Clearances:** P1 gantry sign bottom 6.0 m; P2 Hero overpass soffit 6.18 m. Ground-floor commercial (4.8 m) and parking clear height (2.8 m) read correctly next to them in `P2_city_windows_scale.png` and `P2_city_overpass.png`.

---

### `reports/P2_city_FINAL_FREEZE.md`

### P2_City — FINAL FREEZE

Date: 2026-10-07 · Phase P2-BLENDER-02 · Status: **FROZEN**. Nothing under `environment/P2_City/` is to be edited; later phases may only link from it read-only.

#### Final deliverables
- **Final source blend:** `blend/city_07_export_ready.blend` (checkpoints `city_01_blockout` … `city_06_lods_hlod_collision` kept unchanged).
- **FBX (`exports/`, identical in `UnityTransfer/FBX/`):** `City_Clusters.fbx`, `City_Collision.fbx`, `City_Commercial.fbx`, `City_Landmarks.fbx`, `City_Office.fbx`, `City_Residential.fbx`, `City_Rooftops.fbx`, `City_ServiceParking.fbx`, `City_Skyline.fbx`, `City_UrbanStructures.fbx`, `city_complete.fbx`
- **Textures:** windows (T_City_Windows_2K ×3 + T_City_WindowEmissionMask_2K), facades (T_City_Facade_2K ×3), trim (T_City_Trim_2K ×5), concrete (Concrete ×4, Brick ×4, Stone ×4, Ground ×3), roofs (T_City_Roof_2K ×3), signs (T_City_Signs_1K ×3); `metal/` and `decals/` intentionally empty (README).
- **Reports:** `reports/P2_city_discovery.md`, `_materials.md`, `_scale_audit.md`, `_validation.txt`, `_geometry.json`, `_export_manifest.json`, `_source_baseline.json`, `_source_integrity_check.md`, `_textures.json`, `_qa_layout.json`, `_FINAL_REPORT.md`.
- **Previews:** 32 images in `previews/`.
- **UnityTransfer:** `UnityTransfer/` (FBX, Textures, Reports, README: `CITY_IMPORT_NOTES.md`, `CITY_MATERIAL_GUIDE.md`, `CITY_PLACEMENT_GUIDE.md`, `CITY_PERFORMANCE_GUIDE.md`).

#### Validation
`reports/P2_city_validation.txt`: **SUMMARY: 0 errors, 0 warnings**.
Source integrity: **PASS** (`reports/P2_city_source_integrity_check.md`).

#### Known limitations
- Most near / mid buildings are below the LOD0 triangle guidance (e.g. Office_Tower_A 4.5k, Office_Midrise_A 1.9k); geometry was not padded. The richest are Residential_Tower_A (16k, balconies) and Office_Tower_B / Residential_Tower_B (~10k).
- LOD1 / LOD2 ratios vary by family (window recesses / balconies drop out at LOD1); some LOD1s are below 40 % of LOD0.
- No fake-interior parallax atlas (optional); window cells carry painted interiors.
- No decals and no rain / overcast preview (optional).
- Landmark / skyline distance previews use render-session elevated cameras (the saved QA cameras are at ground level and blocked by the near layer); this changes nothing in the saved files.
- QA urban ground is a flat preview plane; Unity supplies the real city ground / terrain beyond the P1 corridor.

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P2_city_validation.txt`

```text
== P2-BLENDER-02 CITY / URBAN HIGHWAY - VALIDATION ==
source blend/city_07_export_ready.blend; CITY_MASTER 311 objects, 254 meshes (227 renderable incl. cluster instances, 27 colliders)

[PASS]  1. frozen source integrity: P0, P1 Props / Terrain / Vegetation / Tunnel, P2 Bridges, P2 BridgeTerrainContext, vehicles and all other workspace files byte-identical to the pre-phase baseline
[PASS]  2. required building families: 16 primary archetypes (LOD0-3) + 6 restrained variants (material / window category / floor count / podium / roof, never XYZ scaling)
[PASS]  3. office assets exist: Office_Tower_A, Office_Tower_B, Office_Midrise_A, Office_Midrise_B
[PASS]  4. residential assets exist: Residential_Tower_A, Residential_Tower_B, Residential_Midrise_A, Residential_Midrise_B
[PASS]  5. commercial assets exist: Commercial_Block_A, Commercial_Block_B, Hotel_Midrise_A, City_SignPanel_A, City_SignPanel_B, City_RooftopSign_A
[PASS]  6. service / industrial assets exist: Warehouse_Urban_A, ServiceBuilding_A, UtilityBuilding_A, City_UtilityCabinet_A, City_UtilityCabinet_B, City_TransformerBox_A, City_ServiceDoor_A, City_VentUnit_A, ServiceLot_A, ParkingSurface_A, BuildingLoadingArea_A, UrbanConcretePad_A
[PASS]  7. parking assets exist: ParkingGarage_A, ParkingGarage_B, ParkingGarage_RampVisual_A, ParkingGarage_Roof_A, ParkingPodium_A
[PASS]  8. landmark assets exist: City_Landmark_A, City_Landmark_B
[PASS]  9. rooftop kit assets exist: Roof_HVAC_A, Roof_HVAC_B, Roof_Vent_A, Roof_Chiller_A, Roof_WaterTank_A, Roof_Antenna_A, Roof_ServiceRoom_A, Roof_Railing_A, Roof_Cluster_A, Roof_Cluster_B
[PASS] 10. urban walls / noise barriers (solid + transparent) assets exist: Urban_RetainingWall_A, Urban_RetainingWall_B, Urban_NoiseWall_A, Urban_NoiseWall_B, Urban_ServiceWall_A, Urban_Fence_A
[PASS] 11. window scale (measured from every LOD0 / LOD1 window face: face size / atlas-cell span): office 1.2-2.0 m wide, residential 0.9-1.5, hotel 0.9-1.6, curtain-wall panel 1.5 m, storefront 1.8-3.0; heights 0.9-3.4 m
[PASS] 12. floor-height scale: office 3.6-4.2 m, residential / hotel 3.0-3.4 m, ground-floor commercial 4.0-5.0 m (style tables), and LOD0 window rows step by exactly the floor height
[PASS] 13. facade modules: Facade_OfficeGlass_4m, Facade_OfficeConcrete_4m, Facade_Residential_4m, Facade_Commercial_4m, Facade_Service_4m (LOD0 + LOD1); facade-atlas faces stay inside one T_City_Facade_2K strip (one floor band)
[PASS] 14. materials: only the 15 shared MAT_City_* families, every slot used, colliders have none
[PASS] 15. city trim sheet T_City_Trim_2K (BaseColor / Normal / Roughness / Metallic / AO, 2048) exists; every trim face stays inside one strip
[PASS] 16. window atlas T_City_Windows_2K (BaseColor / Normal / Roughness, 16 x 16 cells, 7 categories) exists; every window face maps whole cell rows inside ONE category band (1 floor = 1 row; LOD3 2 floors = 2 rows)
[PASS] 17. window emission mask T_City_WindowEmissionMask_2K (RGB = per-window warm / cool / neutral emission, black = off) exists; mixed occupancy: every lit building has 10-70 % of its LOD0 windows on (never all on); CityWindowData (R random / G floor / B category / A window) on every window face
[PASS] 18. UVs: UVMap on every mesh; tileable materials world-scale (concrete / stone 4 m, brick 2 m, roof / ground 8 m per tile
[PASS] 19. LODs: 49 LOD groups, triangle counts strictly decreasing; LOD3 keeps the silhouette (full building mass height incl. setbacks, footprint within 2.6 m; only rooftop kit / balconies / canopies / fins removed)
[PASS] 20. HLOD-ready clusters: CityCluster_Near_A/B/C, _Mid_A/B/C, _Skyline_A/B exist; members are non-destructive instances sharing the building meshes; each has a merged <Cluster>_HLOD source (skyline HLOD < 8k tris, near / mid < 20k)
[PASS] 21. far skyline assets: 6 Skyline_Tower_* single-LOD meshes, <= 2,000 tris each (below-guidance counts are not errors), window bands only (no window / balcony / rooftop geometry)
[PASS] 22. colliders: 27 simple closed boxes (buildings per tier, garages, urban walls), < 100 tris each, no materials, no per-window collision
[PASS] 23. transforms: every production mesh has an identity world matrix; cluster instances have scale 1 and only 90-degree Z rotations; roots at the world origin
[PASS] 24. pivots / origins: buildings, podiums, garages and skyline towers at ground centre (min z 0, footprint centred); rooftop kit at its mount point; urban walls at the module start on the road face
[PASS] 25. day QA: all required day / golden-hour previews rendered from the final source (reviewed visually: depth, materials, rooftops, road readability
[PASS] 26. night QA: P2_city_night.png rendered; occupancy mixed per building (check 17); window emission is data (mask + CityWindowData), not baked lighting
[PASS] 27. repetition QA: in the 1 km QA strip, the same building mesh never repeats within 120 m in the near / mid layers (variants, rotation, spacing, roof swaps)
[PASS] 28. export selection == CITY_MASTER; no P0 / P1 / P2 / tunnel / vehicle data, no QA / camera / light / helper objects in any FBX
[PASS] 29. normals / topology: no zero-area faces, ngons, duplicate faces or inconsistently wound neighbours; hard edges on structure (35 deg auto-sharp)
[PASS] 30. FBX re-import City_Office.fbx: 30 objects, names + hierarchy match, world deviation 9.5e-06 m, triangles / UVs / materials / CityWindowData preserved; {"Office_Tower_A": {"up_Y": [-0.0, 135.84]}}
[PASS] 31. FBX re-import City_Residential.fbx: 30 objects, names + hierarchy match, world deviation 8.6e-06 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 32. FBX re-import City_Commercial.fbx: 28 objects, names + hierarchy match, world deviation 4.8e-06 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 33. FBX re-import City_ServiceParking.fbx: 45 objects, names + hierarchy match, world deviation 3.8e-06 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 34. FBX re-import City_Landmarks.fbx: 10 objects, names + hierarchy match, world deviation 1.9e-05 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 35. FBX re-import City_UrbanStructures.fbx: 44 objects, names + hierarchy match, world deviation 1.9e-06 m, triangles / UVs / materials / CityWindowData preserved; {"Urban_RetainingWall_A": {"forward_Z": [-0.0, 8.0]}}
[PASS] 36. FBX re-import City_Rooftops.fbx: 30 objects, names + hierarchy match, world deviation 1.1e-06 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 37. FBX re-import City_Clusters.fbx: 41 objects, names + hierarchy match, world deviation 1.5e-05 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 38. FBX re-import City_Skyline.fbx: 26 objects, names + hierarchy match, world deviation 3.1e-05 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 39. FBX re-import City_Collision.fbx: 27 objects, names + hierarchy match, world deviation 2.5e-05 m, triangles / UVs / materials / CityWindowData preserved
[PASS] 40. FBX re-import city_complete.fbx: 311 objects, names + hierarchy match, world deviation 3.1e-05 m, triangles / UVs / materials / CityWindowData preserved; {"Office_Tower_A": {"up_Y": [-0.0, 135.84]}, "Urban_RetainingWall_A": {"forward_Z": [-0.0, 8.0]}}

Triangle budgets are guidance only; below-budget assets are not reported as warnings.
SUMMARY: 0 errors, 0 warnings
```

