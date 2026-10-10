# P1-BLENDER-04 — Premium Modular Tunnel & Highway Structures

Digest 05 of the environment handoff. Folder: `environment/P1_Tunnel/`. **Status: COMPLETE and FROZEN.** Read-only; later work may only link from it.

- **Final source blend:** `blend/tunnel_07_export_ready.blend`
- **Asset index source:** `reports/P1_tunnel_geometry.json` + `reports/P1_tunnel_export_manifest.json`
- **Checkpoints (7):** `tunnel_01_blockout.blend`, `tunnel_02_shell_portal.blend`, `tunnel_03_structures.blend`, `tunnel_04_service_safety.blend`, `tunnel_05_materials_uv.blend`, `tunnel_06_lods_collision.blend`, `tunnel_07_export_ready.blend`
- **FBX (9):** `Tunnel_Shell.fbx` (65 objects), `Tunnel_Portals.fbx` (35 objects), `Tunnel_Structures.fbx` (44 objects), `Tunnel_Lights.fbx` (16 objects), `Tunnel_Ventilation.fbx` (17 objects), `Tunnel_ServiceSafety.fbx` (38 objects), `Tunnel_Drainage.fbx` (12 objects), `Tunnel_Collision.fbx` (10 objects), `tunnel_complete.fbx` (237 objects)
- **Textures:** 15 PNG files · **Previews:** 20 renders · **UnityTransfer README:** `TUNNEL_IMPORT_NOTES.md`, `TUNNEL_LIGHTING_GUIDE.md`, `TUNNEL_STREAMING_GUIDE.md`

## Asset index (generated from the export manifest + geometry report)

| Asset (LOD group) | Triangles LOD0 / LOD1 / LOD2 / LOD3 | FBX |
|---|---|---|
| `TunnelLight_EntranceBoost` | 158 / 62 | Tunnel_Lights.fbx |
| `TunnelLight_Inspection` | 84 / 32 | Tunnel_Lights.fbx |
| `TunnelLight_Linear` | 58 / 14 | Tunnel_Lights.fbx |
| `TunnelLight_Linear_Double` | 104 / 40 | Tunnel_Lights.fbx |
| `TunnelLight_Wall` | 86 / 38 | Tunnel_Lights.fbx |
| `TunnelShell_20m` | 1,044 / 210 / 150 | Tunnel_Shell.fbx |
| `TunnelShell_40m` | 2,088 / 420 / 300 | Tunnel_Shell.fbx |
| `Tunnel_Barrier_20m` | 280 / 50 | Tunnel_Structures.fbx |
| `Tunnel_Barrier_40m` | 560 / 100 | Tunnel_Structures.fbx |
| `Tunnel_Barrier_EndFlare` | 44 / 20 | Tunnel_Structures.fbx |
| `Tunnel_CableTray_4m` | 196 / 12 | Tunnel_ServiceSafety.fbx |
| `Tunnel_CableTray_8m` | 348 / 20 | Tunnel_ServiceSafety.fbx |
| `Tunnel_DarkVariant_40m` | 12,926 / 2,460 / 872 | Tunnel_Shell.fbx |
| `Tunnel_Drain_Access` | 72 / 12 | Tunnel_Drainage.fbx |
| `Tunnel_Drain_Channel` | 36 / 10 | Tunnel_Drainage.fbx |
| `Tunnel_Drain_Grate_4m` | 170 / 2 | Tunnel_Drainage.fbx |
| `Tunnel_Drain_Grate_8m` | 342 / 4 | Tunnel_Drainage.fbx |
| `Tunnel_EmergencyBay_40m` | 12,892 / 2,678 / 1,056 | Tunnel_Shell.fbx |
| `Tunnel_EmergencyDoor` | 110 / 26 | Tunnel_ServiceSafety.fbx |
| `Tunnel_EmergencyLight` | 100 / 52 | Tunnel_ServiceSafety.fbx |
| `Tunnel_EmergencyPhone` | 38 / 14 | Tunnel_ServiceSafety.fbx |
| `Tunnel_Entry_40m` | 13,682 / 3,506 / 1,138 | Tunnel_Shell.fbx |
| `Tunnel_Exit_40m` | 11,878 / 2,790 / 1,042 | Tunnel_Shell.fbx |
| `Tunnel_FanSupport` | 168 / 72 | Tunnel_Ventilation.fbx |
| `Tunnel_FireCabinet_A` | 230 / 74 | Tunnel_ServiceSafety.fbx |
| `Tunnel_FireCabinet_B` | 142 / 74 | Tunnel_ServiceSafety.fbx |
| `Tunnel_JetFan` | 1,172 / 420 / 156 | Tunnel_Ventilation.fbx |
| `Tunnel_JetFan_DoubleMount` | 2,440 / 864 / 336 | Tunnel_Ventilation.fbx |
| `Tunnel_LaneSignal_Frame` | 260 / 164 | Tunnel_Structures.fbx |
| `Tunnel_LightTrack_4m` | 68 / 36 | Tunnel_Structures.fbx |
| `Tunnel_LightTrack_8m` | 132 / 68 | Tunnel_Structures.fbx |
| `Tunnel_OverheadSignFrame` | 156 / 108 | Tunnel_Structures.fbx |
| `Tunnel_PortalRetaining_L` | 84 / 24 | Tunnel_Portals.fbx |
| `Tunnel_PortalRetaining_R` | 84 / 24 | Tunnel_Portals.fbx |
| `Tunnel_PortalTop` | 86 / 12 | Tunnel_Portals.fbx |
| `Tunnel_PortalWing_L` | 84 / 36 | Tunnel_Portals.fbx |
| `Tunnel_PortalWing_R` | 84 / 36 | Tunnel_Portals.fbx |
| `Tunnel_Portal_Entry` | 1,366 / 478 / 282 | Tunnel_Portals.fbx |
| `Tunnel_Portal_Exit` | 1,366 / 478 / 282 | Tunnel_Portals.fbx |
| `Tunnel_Recess_A` | 250 / 70 | Tunnel_Structures.fbx |
| `Tunnel_Recess_B` | 254 / 74 | Tunnel_Structures.fbx |
| `Tunnel_ServiceBay_40m` | 14,488 / 3,092 / 1,346 | Tunnel_Shell.fbx |
| `Tunnel_ServiceBox_A` | 62 / 12 | Tunnel_ServiceSafety.fbx |
| `Tunnel_ServiceBox_B` | 90 / 28 | Tunnel_ServiceSafety.fbx |
| `Tunnel_ServiceDoor_A` | 108 / 12 | Tunnel_ServiceSafety.fbx |
| `Tunnel_ServiceDoor_B` | 144 / 24 | Tunnel_ServiceSafety.fbx |
| `Tunnel_Straight_20m` | 7,158 / 1,408 / 510 | Tunnel_Shell.fbx |
| `Tunnel_Straight_40m` | 13,654 / 2,644 / 968 | Tunnel_Shell.fbx |
| `Tunnel_UtilityConduit_A` | 296 / 64 | Tunnel_ServiceSafety.fbx |
| `Tunnel_VMS_Frame` | 108 / 84 | Tunnel_Structures.fbx |
| `Tunnel_Vent_Duct_A` | 48 / 12 | Tunnel_Ventilation.fbx |
| `Tunnel_Vent_Grille` | 132 / 84 | Tunnel_Ventilation.fbx |
| `Tunnel_Ventilation_40m` | 16,274 / 3,604 / 1,304 | Tunnel_Shell.fbx |

**Other exported objects** (single meshes, colliders, snap / reference empties; triangles where known):

- `Tunnel_Collision.fbx` (10): Collision_ServiceBay (60), Collision_TunnelBarrier (16), Collision_TunnelBarrierEnd (16), Collision_TunnelBarrier_20m (16), Collision_TunnelPortal (72), Collision_TunnelPortal_Exit (72), Collision_TunnelWall_L_20m (12), Collision_TunnelWall_L_40m (12), Collision_TunnelWall_R_20m (12), Collision_TunnelWall_R_40m (12)
- `Tunnel_Lights.fbx` (1): TunnelLight_Emergency (14)
- `Tunnel_Portals.fbx` (12): Tunnel_Portal_Entry_CeilingClearance, Tunnel_Portal_Entry_PortalFace, Tunnel_Portal_Entry_RoadCenter, Tunnel_Portal_Entry_TunnelCenter, Tunnel_Portal_Entry_WallInner_L, Tunnel_Portal_Entry_WallInner_R, Tunnel_Portal_Exit_CeilingClearance, Tunnel_Portal_Exit_PortalFace, Tunnel_Portal_Exit_RoadCenter, Tunnel_Portal_Exit_TunnelCenter, Tunnel_Portal_Exit_WallInner_L, Tunnel_Portal_Exit_WallInner_R
- `Tunnel_ServiceSafety.fbx` (2): Tunnel_ExitSign (44), Tunnel_SOS_Sign (28)
- `Tunnel_Shell.fbx` (25): TunnelShell_20m_Snap_End, TunnelShell_20m_Snap_Start, TunnelShell_40m_Snap_End, TunnelShell_40m_Snap_Start, Tunnel_DarkVariant_40m_Snap_End, Tunnel_DarkVariant_40m_Snap_Start, Tunnel_EmergencyBay_40m_Snap_End, Tunnel_EmergencyBay_40m_Snap_Start, Tunnel_Entry_40m_Snap_End, Tunnel_Entry_40m_Snap_Start, Tunnel_Exit_40m_Snap_End, Tunnel_Exit_40m_Snap_Start, Tunnel_ServiceBay_40m_Snap_End, Tunnel_ServiceBay_40m_Snap_Start, Tunnel_Straight_20m_Snap_End, Tunnel_Straight_20m_Snap_Start, Tunnel_Straight_40m_CeilingClearance, Tunnel_Straight_40m_RoadCenter, Tunnel_Straight_40m_Snap_End, Tunnel_Straight_40m_Snap_Start, Tunnel_Straight_40m_TunnelCenter, Tunnel_Straight_40m_WallInner_L, Tunnel_Straight_40m_WallInner_R, Tunnel_Ventilation_40m_Snap_End, Tunnel_Ventilation_40m_Snap_Start
- `Tunnel_Structures.fbx` (14): TunnelWall_DirtyVariant (44), TunnelWall_EndTrim (12), TunnelWall_LowerPanel (36), TunnelWall_Panel_A (44), TunnelWall_Panel_B (88), TunnelWall_ServicePanel (92), Tunnel_LaneSignal_Face_Arrow (2), Tunnel_LaneSignal_Face_X (2), Tunnel_LeakStain_A (2), Tunnel_LeakStain_B (2), Tunnel_RepairPatch_A (2), Tunnel_Soot_A (2), Tunnel_WallGrime_A (2), Tunnel_WallSignBracket (36)

## Phase documents (verbatim; validation lists keep every check but drop the long evidence text)

---

### `reports/P1_tunnel_FINAL_REPORT.md`

### P1-BLENDER-04 — Premium Modular Tunnel & Highway Structures — FINAL REPORT

Date: 2026-10-07 · Blender 5.2 (Blender-only workstation, Unity was not touched) · Status: **COMPLETE, FROZEN**. Every number below comes from the generated reports in `environment/P1_Tunnel/reports/`.

1. **Discovery findings:** P0 carriageway 4 × 3.6 = 14.4 m; right shoulder to x −10.2; drain corridor −10.2 … −10.7; left shoulder to 8.7; median strip 8.7 … 10.7 with an F-barrier at 9.7; crown +36 mm. P1 Terrain cut modules start at \|x\| 16 m. P1 sign panels: Small 2.5 × 1.5, VMS 5 × 1.6. Hypercar ≈ 2.2 × 4.7 × 1.55 m. Cameras: driver 1.15, chase 2.4, high chase 5.5 m. Details: `reports/P1_tunnel_discovery.md`.
2. **Source integrity:** 935 files outside `P1_Tunnel` (P0 95, Props 77, Terrain 166, Vegetation 257, cars 108, other 232) were SHA-1 hashed before any work. They are **byte-for-byte unchanged** at the end: 0 changed, 0 added (`P1_tunnel_source_integrity_check.md`, validation check 33). The frozen sources were linked read-only only; every tunnel script disables `__pycache__`.
3. **Tunnel dimensions:** 23.8 m wall to wall (x −12.3 … +11.5). Springing at 3.6 m, crown at 8.2 m. Arch ≥ 6.21 m above the road-kit edges; lowest equipment over the road 5.6 m. Right walkway 0.99 m (top +0.30) behind the barrier; left ledge 0.8 m.
4. **Tunnel profile:** vertical clad lower walls, then a broad elliptical arch (11.9 × 4.6 m semi-axes, 24 / 16 / 10 segments per LOD). Neither a box nor a pipe.
5. **Structural rhythm:**
   - 5 m bays: 8 per 40 m, 4 per 20 m, panels 5 m;
   - lining joints every 10 m, as half-grooves at module ends;
   - barrier V-joints every 4 m;
   - brackets, hangers and louvres every 2 m.
   - Every rhythm divides 20 m, so nothing straddles a snap boundary.
6. **40 m module:** 8 runtime 40 m modules span exactly y 0 … −40.000, and Snap_Start → Snap_End is 40.000 m (checks 2, 4). Straight_40m LOD0/1/2 = 13,654 / 2,644 / 968 tris.
7. **20 m module:** `Tunnel_Straight_20m` spans exactly 0 … −20.000, snap 20.000 m (7,158 / 1,408 / 510 tris). `TunnelShell_20m` is also provided.
8. **Entry:** `Tunnel_Entry_40m` = open approach with the portal wings → a 12 m flat louvre sun-screen (partially enclosed, daylight striping) → `Tunnel_Portal_Entry` at y −14 → full tunnel with 2.5 m EntranceBoost lighting. A barrier end flare points at oncoming traffic. Geometry only, no exposure logic.
9. **Exit:** `Tunnel_Exit_40m` = full tunnel with Linear_Double lighting → `Tunnel_Portal_Exit` at y −26 → louvre canopy → open road. The bright-exit sightline is clear (`P1_tunnel_exit.png`).
10. **Portal:**
    - Headwall 31.2 × 10.6 m (coping 11.05 m) with a projecting opening ring, pilasters and a cladding band.
    - Generic `TUNNEL 1` name plate, height sign, floodlight mounts and a service door.
    - Stepped wings and retaining walls with drainage gutters; assembly 39.5 × 28.8 × 11.45 m.
    - Kit pieces: `Tunnel_PortalWing_L/R`, `Tunnel_PortalTop`, `Tunnel_PortalRetaining_L/R`. The Exit portal is a proper mirror with readable text.
    - Reference empties: RoadCenter, PortalFace, TunnelCenter, CeilingClearance, WallInner_L/R.
11. **Wall system:** `TunnelWall_Panel_A`, `_Panel_B` (split), `_LowerPanel` (precast plinth), `_ServicePanel` (access hatch), `_EndTrim`, `_DirtyVariant` (heavy TunnelWear), plus `Tunnel_Recess_A` (equipment niche) and `_B` (door niche). Panel A/B patterns vary per module.
12. **Ceiling:** segmented concrete arch with 10 m lining joints, continuous light tracks (`Tunnel_LightTrack_4m/8m`) with hangers, the fan pair on the crown in the Ventilation module, and a smoke damper on the upper wall. Nothing else clutters it (`P1_tunnel_ceiling.png`).
13. **Barriers:**
    - `Tunnel_Barrier_40m/20m`: a tunnel-specific safety-shape barrier integrated with the raised walkway (P0/P1 barriers were not modified). It needed its own profile to carry the walkway behind it.
    - `Tunnel_Barrier_EndFlare` at the Entry/Exit ends.
    - On the left, the P0 median barrier is reused unchanged.
14. **Lighting fixtures:** `TunnelLight_Linear` (58 / 14 tris), `_Linear_Double` (104 / 40), `_EntranceBoost` (158 / 62), `_Wall` (86 / 38), `_Emergency` (guidance LED, 14), `_Inspection` (84 / 32), plus `Tunnel_EmergencyLight` (beacon). All are geometry plus emissive-source materials; there are no Unity lights.
15. **Light spacing:** two rows at XC ± 4.6 m, 7.55 m mounting height. Spacing: 5 m standard; 2.5 m entrance boost; 5 m double in the exit zone; 10 m in DarkVariant; guidance LEDs every 10 m.
16. **Ventilation:** `Tunnel_JetFan` (Ø 1.25 m × 4.6 m housing, silencers, flanges, bellmouths, hub, guard grille; 1,172 / 420 / 156 tris), `_JetFan_DoubleMount` (±1.6 m, 2,440 / 864 / 336), `Tunnel_FanSupport`, `Tunnel_Vent_Duct_A`, `Tunnel_Vent_Grille`. 6.5 m clear below the fans.
17. **Cable / service infrastructure:** `Tunnel_CableTray_4m/8m` (cornice, both walls, with cables), `Tunnel_UtilityConduit_A` (fire main + conduit, stopping at recesses), `Tunnel_ServiceBox_A/B`.
18. **Emergency bay:** `Tunnel_EmergencyBay_40m` is a 20 m × 2.5 m refuge recess with 5 m tapers and a 3.4 m roof. It holds the emergency door, phone, hose cabinet, beacon, SOS flag sign, wall lights and guidance LEDs. The barrier stays continuous, so road gameplay is unchanged. Use `Collision_ServiceBay` here.
19. **Service doors:** `Tunnel_ServiceDoor_A` (1.0 × 2.1 m) and `_B` (double 1.8 × 2.4 m, louvre), each with frame, leaf, handle and a warning-plate area from the trim. Used in `Tunnel_ServiceBay_40m` and the portal pier.
20. **Safety equipment:** `Tunnel_EmergencyDoor` (+ illuminated EXIT box), `Tunnel_EmergencyPhone`, `Tunnel_FireCabinet_A` (hose reel + extinguisher; "Tunnel_FireCabinet" in the brief), `_B`, `Tunnel_SOS_Sign`, `Tunnel_ExitSign` (+ EXIT 150 M plaque), `Tunnel_EmergencyLight`.
21. **Signs / VMS supports:** `Tunnel_OverheadSignFrame` (for 2 × P1 SignPanel_Small, 5.6 m clear), `Tunnel_VMS_Frame` (for the P1 VMS_Panel, 5.6 m clear), `Tunnel_LaneSignal_Frame` (4 signals, 5.9 m clear), `Tunnel_LaneSignal_Face_Arrow/_X`, `Tunnel_WallSignBracket` (for P1 wall signs). The P1 panels are linked in QA and not duplicated.
22. **Drainage:** `Tunnel_Drain_Channel` (slot drain in the P0 drain corridor), `Tunnel_Drain_Grate_4m/8m` (LOD0 bars 170 / 342 tris → LOD1 textured plate 2 / 4 tris), `Tunnel_Drain_Access` (walkway sump cover every 40 m).
23. **Material list (11):** Concrete, Concrete_Dark, WallPanel, Metal, Galvanized, Rubber, Drain, Light_White, Light_Emergency, Sign, Decal. All are `MAT_Tunnel_*`; every slot is used; colliders have no material.
24. **Trim-sheet strategy:** one `T_Tunnel_Trim_2K` (BaseColor / Normal / Roughness / Metallic / AO) with 9 strips: panel, dirty concrete, clean edge, galvanized, painted metal, rubber, door, sign frame, grate. It serves 5 materials; there are no per-object textures.
25. **Concrete textures:** `T_Tunnel_Concrete_2K` (BaseColor / Normal / Roughness / AO), tileable, 4 m per tile = 512 px/m, with restrained staining.
26. **Decal / wear strategy:**
    - Reusable decals: `Tunnel_LeakStain_A/B`, `_WallGrime_A`, `_RepairPatch_A`, `_Soot_A` (alpha atlas).
    - The `TunnelWear` vertex layer: R grime (lower walls), G wetness / leaks (low + drains), B soot (toward the crown), A variation. It is previewed in Blender and documented for the Unity shader.
    - The roughness maps stay dry, so Unity can drive wetness. No Blender-only wet material is used.
27. **UV scale:**
    - Shell: U = −y / 4, V = arc / 4 (10 tiles per 40 m; integer at every Snap_End).
    - Concrete parts: 4 m box projection.
    - Panels: one 5 m panel per trim tile (410–427 px/m).
    - Other trim strips: 4 m per U tile.
    - Check 14 confirms no stretched 0–1 UVs and every trim face inside its strip.
28. **LOD strategy:**
    - Modules and portals: LOD0–2. LOD1 is a 16-segment arch with simplified fixtures and plates; LOD2 a 10-segment arch with band walls and lens quads.
    - Fans: LOD0–2.
    - Fixtures, sign frames, service / safety equipment, recesses, grates, trays, tracks, barrier: LOD0–1.
    - No pointless LODs on simple panels or decals.
    - 53 LOD groups, all with strictly decreasing counts.
29. **Triangle counts (LOD0 / LOD1 / LOD2):**

    | Asset | LOD0 | LOD1 | LOD2 |
    |---|---|---|---|
    | Straight_40m | 13,654 | 2,644 | 968 |
    | Entry | 13,682 | 3,506 | 1,138 |
    | Exit | 11,878 | 2,790 | 1,042 |
    | ServiceBay | 14,488 | 3,092 | 1,346 |
    | EmergencyBay | 12,892 | 2,678 | 1,056 |
    | Ventilation | 16,274 | 3,604 | 1,304 |
    | DarkVariant | 12,926 | 2,460 | 872 |
    | TunnelShell_40m | 2,088 | 420 | 300 |
    | Portal | 1,366 | 478 | 282 |

    Per-asset figures are in `P1_tunnel_geometry.json`.
30. **Collider strategy:** `Collision_TunnelWall_L/R_40m/_20m` (boxes to 3.6 m), `Collision_TunnelBarrier` / `_20m` / `TunnelBarrierEnd`, `Collision_TunnelPortal` / `_Exit` (piers, wings, retaining walls), `Collision_ServiceBay`. All are closed, 12–72 tris each, with no ceiling collision. Road collision stays with P0.
31. **Snap points:** every runtime module and shell has `<Name>_Snap_Start` (root origin = road centre at the module start) and `_Snap_End` (0, −L, 0) in Blender, i.e. (0, 0, +L) in Unity. Distances are exactly 40.000 / 20.000, and the FBX re-import checks them in Unity file space.
32. **Car-clearance QA:** the linked hypercar sits at lane 2, the road centre and the approach. ≥ 4.6 m of headroom above the car over the full road kit, 5.6 m minimum to any equipment, and walls 2.1 m beyond the shoulder edge. PASS (`P1_tunnel_chase_view.png`, `P1_tunnel_entry.png`).
33. **Driver-view QA:** `P1_tunnel_driver_view.png` at 1.15 m. The tunnel is neither too low nor too narrow: bright clad walls, a readable arch and services, lanes clear. PASS.
34. **Chase-view QA:** `P1_tunnel_chase_view.png` (2.4 m) and `P1_tunnel_high_chase.png` (5.5 m). The structural rhythm (joints, light rows, panels, LEDs) reads at speed and the road stays readable. PASS.
35. **Portal QA:** `P1_tunnel_portal_front.png`, `_50m`, `_100m`, `_200m`, `_300m`. A strong landmark at every distance. PASS.
36. **Night QA:** `P1_tunnel_night.png` (Blender preview lights only). Fixture rhythm, ceiling, walls, green guidance accents and EXIT signs all read. PASS.
37. **Full-sequence QA:** 680 m of QA road.
    - Layout: 320 m flat approach → cut → rock cut → Entry → Straight → ServiceBay → Ventilation → 2 × Straight_20m → EmergencyBay → DarkVariant → Straight → Exit → rock cut → cut. 332 m between headwalls.
    - Built on the **linked real P0 road** and P1 terrain.
    - Renders: `P1_tunnel_full_sequence.png`, `P1_tunnel_full_cutaway.png`. PASS.
38. **Checkpoint files:** `blend/tunnel_01_blockout`, `_02_shell_portal`, `_03_structures`, `_04_service_safety`, `_05_materials_uv`, `_06_lods_collision`, `_07_export_ready.blend`. None was overwritten (the build asserts this).
    - Superseded drafts: during validation-driven fixes, one earlier set of WIP checkpoints and exports was superseded. It was moved, not overwritten, to the session scratchpad before the final set was written in a single pass.
39. **Preview paths:** `previews/P1_tunnel_{portal_front, portal_50m, portal_100m, portal_200m, portal_300m, entry, straight, driver_view, chase_view, high_chase, wall_detail, ceiling, ventilation, emergency_bay, drainage, night, exit, full_sequence, full_cutaway, asset_library}.png`. That is 20 images, all 16 required plus 4 extra.
40. **FBX paths:** `exports/tunnel_complete.fbx`, `Tunnel_Shell.fbx`, `Tunnel_Portals.fbx`, `Tunnel_Structures.fbx`, `Tunnel_Lights.fbx`, `Tunnel_Ventilation.fbx`, `Tunnel_ServiceSafety.fbx`, `Tunnel_Drainage.fbx`, `Tunnel_Collision.fbx`. That is 9 files and 237 objects; the axis-bake residual is 4.8e-6.
41. **Re-import result:** all 9 FBX files re-imported into clean scenes.
    - Names, triangle counts, UVs, `TunnelWear` and materials preserved; hierarchy identical.
    - World deviation ≤ 5e-4 m.
    - Unity file space: the 40 m module spans Y −0.33 … 8.22 (up) and Z 0 … 40.000 (forward); snaps are 40.000 / 20.000.
42. **Validation result:** `reports/P1_tunnel_validation.txt`: **33 checks, 0 errors, 0 warnings** (the 23 required checks + per-FBX re-import + hierarchy + vertex data).
43. **UnityTransfer path:** `environment/P1_Tunnel/UnityTransfer/` (FBX/, Textures/{Concrete, Trim, Signs, Decals}/, Reports/, README/).
44. **Import notes:** `UnityTransfer/README/TUNNEL_IMPORT_NOTES.md`. It covers all 22 required topics and carries the Blender-only / Unity-side statement.
45. **Lighting guide:** `UnityTransfer/README/TUNNEL_LIGHTING_GUIDE.md`. It covers the families, spacing, the real-vs-emissive split and mobile tiers, with no fabricated lumen values.
46. **Streaming guide:** `UnityTransfer/README/TUNNEL_STREAMING_GUIDE.md`. It covers the 40 m assumptions, entry / straight / special / exit modules, snap convention, optional vs required assets, no-duplication rules and the recommended composition.
47. **Freeze report:** `reports/P1_tunnel_FINAL_FREEZE.md`. It has SHA-1 hashes for the blends, FBX and textures; `environment/P1_Tunnel/` is FROZEN.
48. **Known limitations:**
    - Module LOD1 / LOD2 are 19–26 % / 7–9 % of LOD0, below the 40–60 % / 15–30 % guidance. LOD0 detail sits in small features, so set LOD0 screen height high.
    - Portal LOD0 is 1,366 tris, below the 8–20 k guidance. It was not padded; its readability was verified out to 300 m.
    - The QA hill is preview-only and not exported. It has approximate shading near the wing tops and one small sky gap at the far right of the portal-front view.
    - Blender preview lighting is not photometric; Eevee's shadow buffer overflowed at 220+ preview lights.
    - The optional wet-road QA was not rendered, because the P0 road material is frozen.
    - The asset-library preview uses a render-session camera; the saved camera crops it.
    - The Exit / Entry barrier flares extend 3.8 m outside the module by design.
49. **Recommended next Blender phase:** **P2-BLENDER Bridges / Overpasses** (`environment/P2_Bridges/` already exists, empty). It would link P0 / P1 / Tunnel read-only and use the same 40 m snap convention. This is a recommendation only; it was not started.

---

### `UnityTransfer/README/TUNNEL_IMPORT_NOTES.md`

### Tunnel — Unity import notes (P1-BLENDER-04)

> **THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.**
> **UNITY-SIDE: TUNNEL MATERIALS, REAL LIGHTS, EMISSIVE INTENSITY, REFLECTION PROBES, EXPOSURE TRANSITION, FOG, ROADSTREAMER INTEGRATION, LODGroup COMPONENTS, CULLING, QUALITY TIERS AND PERFORMANCE TESTING MUST BE COMPLETED ON THE UNITY WORKSTATION.**

#### 1. Source phase
- **Phase:** P1-BLENDER-04, Premium Modular Tunnel & Highway Structures.
- **Source:** `environment/P1_Tunnel/blend/tunnel_07_export_ready.blend`.
- **Frozen upstream (linked read-only, never modified):** P0 Road Foundation, P1 Props, P1 Terrain, P1 Vegetation, vehicles.

#### 2. Orientation
- **Unity:** +Y up, +Z forward (traffic direction), +X to the driver's right.
- **Blender:** +Z up, traffic −Y.
- **Conversion:** the same in-memory axis bake as hypercar / P0 / P1 / Terrain / Vegetation, G = Rot(−90°, X) on mesh data and object matrices, with Apply Transform OFF. Point map Blender (x, y, z) → Unity (−x, z, −y).
- **Verified:** after FBX re-import, the 40 m module spans file-space Y −0.33 … 8.22 (up) and Z 0 … 40.000 (forward).

#### 3. Scale
1 unit = 1 m. Import with Scale Factor 1 and Convert Units ON. The FBX unit is cm with FBX_SCALE_ALL, the same as every earlier package.

#### 4. Road relationship
- **P0 road stays in place.** Keep spawning the P0 road chunks (`Road_4Lane_40m` / `_20m`, edge lines, dividers, paved shoulders, `Median_Concrete`, `Median_Barrier`) inside the tunnel. The tunnel modules wrap that road; they contain no road surface.
- **Do NOT spawn inside tunnel chunks:**
  - the P0 `Drain_Channel_4m` / `Drain_Grate`, because the tunnel slot drain occupies the same corridor (x −10.2 … −10.7 Blender = +10.2 … +10.7 Unity);
  - the P0 grass verge (`EdgeBreakup_Verge_R`).
- **No P0/P1 geometry is duplicated** in any tunnel FBX.

#### 5. 40 m module convention
- **Root origin:** `Snap_Start` = road centre at the module start (same as the P0 chunk origin).
- **Snap_End:** at (0, 0, +40.000) in Unity.
- **Bounds:** all module geometry lies inside the 40 m. The one exception is the 3.8 m barrier end flare of Entry / Exit, pointing at outside traffic.

#### 6. 20 m convention
`Tunnel_Straight_20m` (and `TunnelShell_20m`), with Snap_End at (0, 0, +20.000). Every rhythm (5 m bays, 10 m joints, 4 m barrier joints, 2 m brackets) divides 20 m.

#### 7. Portal dimensions
- **Headwall:** 31.2 m wide, 1.2 m thick, 10.6 m high (coping 11.05 m).
- **Opening:** 23.8 m wide, crown 8.2 m.
- **Overall assembly:** 39.5 × 28.8 × 11.45 m including wings and retaining walls.
- **Origin:** road centre on the portal face plane.
- **Placement:** `Tunnel_Portal_Entry` goes 14 m into `Tunnel_Entry_40m` (module-local Unity z = +14); `Tunnel_Portal_Exit` goes 26 m into `Tunnel_Exit_40m` (z = +26).
- **Reference empties** on each portal: `_RoadCenter`, `_PortalFace`, `_TunnelCenter`, `_CeilingClearance`, `_WallInner_L`, `_WallInner_R`.

#### 8. Tunnel interior dimensions
- **Width:** 23.8 m between the structural walls (Unity x −11.5 … +12.3).
- **Walls:** vertical up to 3.6 m, then an elliptical arch to an 8.2 m crown.
- **Clearance:** ≥ 6.21 m at the road-kit edges; lowest equipment over the road 5.6 m.
- **Edges:** 0.99 m walkway behind the tunnel barrier on the right; 0.8 m ledge on the left.

#### 9. FBX list (`FBX/`)
| File | Content |
|---|---|
| `tunnel_complete.fbx` | everything below (237 objects) |
| `Tunnel_Shell.fbx` | 8 runtime modules (+ snap / reference empties), `TunnelShell_40m` / `_20m` |
| `Tunnel_Portals.fbx` | `Tunnel_Portal_Entry` / `_Exit` (LOD0–2) + kit pieces (wings, top, retaining) |
| `Tunnel_Structures.fbx` | wall panels, recesses, barrier (+ end flare), decals, light tracks, sign / VMS / lane-signal supports, signal faces, wall sign bracket |
| `Tunnel_Lights.fbx` | 6 fixture families |
| `Tunnel_Ventilation.fbx` | jet fan, double mount, fan support, duct, grille |
| `Tunnel_ServiceSafety.fbx` | trays, conduit, service boxes / doors, emergency door / phone / cabinets / signs / beacon |
| `Tunnel_Drainage.fbx` | slot drain channel, grates 4 / 8 m, access cover |
| `Tunnel_Collision.fbx` | 10 simple colliders |

#### 10. LOD naming
- **LOD assets:** a root `<Asset>` (empty, at the origin) with children `<Asset>_LOD0 … _LOD2`. Create one LODGroup per root.
- **Suggested screen-relative heights:**
  - modules: 0.60 / 0.25 / 0.08;
  - portals: 0.5 / 0.2 / 0.05;
  - fixtures and props: 0.25 / 0.08, then cull.
- **Single-mesh assets:** have no LODs (panels, decals, signal faces, guidance LED, flag signs).

#### 11. Material names
`MAT_Tunnel_Concrete`, `MAT_Tunnel_Concrete_Dark`, `MAT_Tunnel_WallPanel`, `MAT_Tunnel_Metal`, `MAT_Tunnel_Galvanized`, `MAT_Tunnel_Rubber`, `MAT_Tunnel_Drain`, `MAT_Tunnel_Light_White`, `MAT_Tunnel_Light_Emergency`, `MAT_Tunnel_Sign`, `MAT_Tunnel_Decal`.

#### 12. Trim sheet
`T_Tunnel_Trim_2K` strips, as pixels from the bottom:

| Strip | px |
|---|---|
| panel | 0–1024 (5 m per U tile) |
| concrete_dirty | 1024–1280 |
| concrete_edge | 1280–1408 |
| galvanized | 1408–1536 |
| painted_metal | 1536–1664 |
| rubber | 1664–1728 |
| door | 1728–1920 |
| sign_frame | 1920–1984 |
| grate | 1984–2048 |

Every strip except panel tiles at 4 m per U tile. Details are in `Reports/P1_tunnel_materials.md`.

#### 13. Texture channels (`Textures/`)
| Texture | Channels |
|---|---|
| Concrete `T_Tunnel_Concrete_2K` | BaseColor, Normal (OpenGL +Y), Roughness, AO; tileable, 4 m per tile |
| Trim `T_Tunnel_Trim_2K` | BaseColor, Normal, Roughness, Metallic, AO |
| Signs `T_Tunnel_Signs_2K` | BaseColor, Roughness, Emissive (mask) |
| Decals `T_Tunnel_Decals_2K` | BaseColor (+alpha), Normal, Roughness |

- **Import settings:** sRGB for BaseColor only; Normal as a normal map; the rest linear.
- **Packing:** URP Lit Metallic/Smoothness = Metallic in R and (1 − Roughness) in A.
- **Vertex colour set 0 `TunnelWear` (linear):**

| Channel | Meaning |
|---|---|
| R | road-spray grime |
| G | wetness / leak potential |
| B | soot |
| A | per-element variation |

#### 14. Emissive source materials
`MAT_Tunnel_Light_White` (warm white lenses), `MAT_Tunnel_Light_Emergency` (green guidance / beacon), and `MAT_Tunnel_Sign` lit faces via the Emissive mask. These carry colour only; Unity sets the intensities.

#### 15. Light fixture spacing
| Family | Spacing |
|---|---|
| `TunnelLight_Linear` | 5 m standard, 10 m in DarkVariant |
| `TunnelLight_EntranceBoost` | 2.5 m in the Entry threshold |
| `TunnelLight_Linear_Double` | 5 m in the Exit module |

Two rows at x = XC ± 4.6 m (Unity x −4.2 / +5.0), mounted at 7.55 m. See `TUNNEL_LIGHTING_GUIDE.md`.

#### 16. Ventilation assets
| Asset | Detail |
|---|---|
| `Tunnel_JetFan` | Ø 1.25 m housing, 4.6 m long, origin = ceiling mount, axis 0.95 m below |
| `Tunnel_JetFan_DoubleMount` | 2 fans at ±1.6 m |
| `Tunnel_FanSupport` | |
| `Tunnel_Vent_Duct_A` | |
| `Tunnel_Vent_Grille` | |

In `Tunnel_Ventilation_40m` the pair hangs at the crown, 20 m into the module, with 6.5 m clear below.

#### 17. Safety assets
`Tunnel_EmergencyDoor` (cross passage + EXIT box), `Tunnel_EmergencyPhone`, `Tunnel_FireCabinet_A` (hose reel + extinguisher; "Tunnel_FireCabinet" in the brief), `Tunnel_FireCabinet_B`, `Tunnel_SOS_Sign`, `Tunnel_ExitSign`, `Tunnel_EmergencyLight` (beacon), `TunnelLight_Emergency` (guidance LED). Wall pieces use the right-wall frame: local x 0 = wall plane, +x into the tunnel. For the left wall, rotate them 180° about the up axis.

#### 18. Drainage
- **Assets:** `Tunnel_Drain_Channel` (4 m slot drain, P0 drain-corridor origin), `Tunnel_Drain_Grate_4m` / `_8m` (LOD1 = flat textured plate), `Tunnel_Drain_Access` (walkway sump cover, every 40 m).
- **In the modules:** the drainage is already included.

#### 19. Collider strategy
- **Ownership:** road collision stays with P0 (`Collision_Road_*`, `Collision_Barrier_*` for the median).
- **Tunnel colliders:**

| Collider | Notes |
|---|---|
| `Collision_TunnelWall_R/L_40m` / `_20m` | boxes, 0.4 m thick, up to the 3.6 m springing line |
| `Collision_TunnelBarrier` / `_20m` | |
| `Collision_TunnelBarrierEnd` | Entry / Exit flare |
| `Collision_TunnelPortal` / `_Exit` | piers, wings, retaining walls |
| `Collision_ServiceBay` | lay-by back wall and tapers; use it instead of `Collision_TunnelWall_R_40m` in `Tunnel_EmergencyBay_40m` |

- **Unity import:** all are closed and low-poly; use them as non-convex static MeshColliders.
- **No ceiling collision:** vehicles cannot reach the ceiling.

#### 20. Snap points
- **Runtime modules and shells:** `<Module>_Snap_Start` (root origin) and `<Module>_Snap_End` (0, 0, +L).
- **Portals:** reference empties as in §7.

#### 21. Excluded QA assets
Not in any FBX:
- the QA sequence: linked P0 road, P1 terrain modules, P1 sign / VMS panels, hypercar, QA hill and filler, module / portal instances, asset-library instances;
- presentation cameras;
- render-session lights and world.

The full list is in `Reports/P1_tunnel_export_manifest.json`.

#### 22. Expected RoadStreamer usage
See `TUNNEL_STREAMING_GUIDE.md`. In short, each tunnel chunk is one P0 road chunk plus one tunnel module at the same transform. Entry and Exit chunks also get their portal at z = +14 / +26.

---

### `UnityTransfer/README/TUNNEL_LIGHTING_GUIDE.md`

### Tunnel lighting guide (Blender source → Unity)

These are geometry and emissive-SOURCE materials only. No Unity Light components were created, and no real photometric values were measured. **Do not treat any Blender preview value as a Unity light value.** Final intensities, lumen / lux targets, exposure and quality tiers must come from Unity tests.

#### Fixture families
| Asset | Use | Geometry |
|---|---|---|
| `TunnelLight_Linear` | standard interior | 1.5 m linear luminaire, lens down, hung from `Tunnel_LightTrack_4m/8m` |
| `TunnelLight_Linear_Double` | exit zone / higher-level interior | twin 1.5 m tubes on a carrier |
| `TunnelLight_EntranceBoost` | entrance threshold | 0.7 × 0.55 m high-output housing, lens tilted ~20° toward entering traffic |
| `TunnelLight_Wall` | lay-by / refuge, portal floodlight style | wall bracket floodlight, aimed down / out |
| `TunnelLight_Emergency` | guidance / emergency LEDs | flush LED on the lower panel, 0.75 m above the road |
| `TunnelLight_Inspection` | service recesses / doors | caged bulkhead |
| `Tunnel_EmergencyLight` | lay-by beacon | green beacon over the emergency door |

#### Intended spacing (as built in the modules)
- **Rows:** two, at x = XC ± 4.6 m (over lanes 1 and 4), mounted at 7.55 m. Centres sit at y −2.5 − 5k, so no fixture crosses a snap seam.
- **Interior (Straight / Service / Vent / Emergency):** Linear every 5 m.
- **Entrance threshold (`Tunnel_Entry_40m`, first 23 m after the portal):** EntranceBoost every 2.5 m.
- **Exit zone (`Tunnel_Exit_40m`):** Linear_Double every 5 m.
- **Deep interior / night zone (`Tunnel_DarkVariant_40m`):** Linear every 10 m.
- **Guidance LEDs:** every 10 m on both walls (y −2.5 − 10k).
- **Lay-by:** 2 wall floodlights plus the beacon.

#### Emissive surfaces
- `MAT_Tunnel_Light_White` lenses (warm white).
- `MAT_Tunnel_Light_Emergency` LEDs / beacon (green).
- `MAT_Tunnel_Sign` faces where the Emissive mask = 1: SOS, EXIT, EXIT 150 M, lane-control arrow / X, LAY-BY.
- **The P1 `VMS_Panel` is a P1 asset;** its emissive belongs to the P1 material.

#### Real lights vs emissive-only (recommended Unity split)
- **Emissive only:**
  - every lens, using a per-tier emissive intensity;
  - guidance LEDs, signs and the beacon, which never need real lights.
- **Real lights:**
  - **Option A (recommended for mobile / mid tiers):** no per-fixture lights. Use baked or mixed lighting from the emissive lenses (lightmaps / APV), plus one or two shadowless real lights near the player (moving with the chase camera) for dynamic objects and wet reflections.
  - **Option B (PC premium):** shadowless spot / area lights at every second or third fixture in the entrance threshold, and every fourth fixture in the interior. Shadows only on a few fixtures near the camera. Light layers keep the tunnel lights off the exterior terrain.
- **Entrance / exit adaptation:** this is an exposure transition owned by Unity (post-processing / volume blending by tunnel depth). It is **not** baked into the materials.
- **Reflection probes:** use one per 2–3 modules, box-projected to the 23.8 × 8.2 m interior, so wet-road reflections pick up the light rows.

#### Mobile scalability concept
| Tier | Lighting approach |
|---|---|
| Low | emissive lenses + baked / ambient tunnel tint, no real lights, fog for depth, LOD1 at short range |
| Mid | emissive + 1–2 camera-following shadowless lights, reflection probes, LOD bias 1.0 |
| High / PC | Option B lights in the threshold, SSR / planar reflections for the wet road, contact shadows, LOD0 near |

#### Preview note
The Blender previews (`previews/P1_tunnel_*.png`) put a temporary Blender area light under every lens, in the render session only, never saved. They exist to check fixture rhythm, ceiling readability, emergency accents, wall readability and silhouette. They are not a photometric study.

---

### `UnityTransfer/README/TUNNEL_STREAMING_GUIDE.md`

### Tunnel streaming guide (RoadStreamer, straight / level / 40 m chunks)

The RoadStreamer stays STRAIGHT, LEVEL, 40 m. The tunnel adds no curves, no grades, no junctions or forks, and no spline-dependent modules.

#### Chunk assumptions
- **Every tunnel chunk is one P0 road chunk plus one tunnel module, at the same transform.** The module root origin = `Snap_Start` = the P0 chunk origin (road centre, chunk start).
- **Snap_End:** (0, 0, +40.000) in Unity, or +20.000 for `Tunnel_Straight_20m`.
- **Keep inside tunnel chunks:** the P0 road surface, markings, paved shoulders, median concrete and median barrier.
- **Skip inside tunnel chunks:** the P0 drain channel / grates and the grass verge. The tunnel's own slot drain uses the same corridor.

#### Modules
| Role | Asset | Notes |
|---|---|---|
| Entry | `Tunnel_Entry_40m` + `Tunnel_Portal_Entry` at (0, 0, +14) | z 0–12 louvre sun-screen canopy (partially enclosed, daylight through), portal headwall at z 14, then full tunnel with the entrance-boost lighting. Its wings / retaining walls reach 28.8 m back into the previous (open) chunk. The barrier end flare points back 3.8 m. |
| Straight | `Tunnel_Straight_40m`, `Tunnel_Straight_20m` | standard interior (5 m lights) |
| Special | `Tunnel_ServiceBay_40m` | 2 equipment recesses (right), service door recess (left) |
| | `Tunnel_EmergencyBay_40m` | 20 m refuge lay-by with emergency door / phone / cabinet / SOS; use `Collision_ServiceBay` instead of `Collision_TunnelWall_R_40m` |
| | `Tunnel_Ventilation_40m` | jet-fan pair + smoke damper |
| | `Tunnel_DarkVariant_40m` | soot-darkened deep-interior / night zone, 10 m lights |
| Exit | `Tunnel_Exit_40m` + `Tunnel_Portal_Exit` at (0, 0, +26) | tunnel, then the portal at z 26, then the louvre canopy z 28–40; flare forward 3.8 m |

#### Snap convention
Chunk N+1 origin = chunk N origin + (0, 0, 40). Every module has identical shell cross-sections at both ends (half lining joints), a texture U that is continuous across the seam, and light, panel and bracket rhythms that never straddle a seam. Any order of interior modules is seamless.

#### Recommended runtime composition
```
open road ... | Entry(+Portal_Entry) | Straight | Ventilation | Straight | ServiceBay | Straight | EmergencyBay | Straight
             | Ventilation | DarkVariant x n (long tunnels) | Straight | Straight_20m (x2 or with a 20 m road pair) | Exit(+Portal_Exit) | open road ...
```
- **Minimum tunnel:** Entry + Exit back to back puts the portal headwalls 52 m apart (z 14 and z 40 + 26). Each additional 40 m module adds 40 m.
- **Long tunnels:** one Ventilation module every 3 chunks (≈ 120 m), and one EmergencyBay every 4–6 chunks (≈ 160–240 m).
- **Variety:** do not repeat the same interior module more than 2–3 times in a row. Alternate Straight with ServiceBay / Ventilation / DarkVariant, and add decals (`Tunnel_LeakStain_*`, `Tunnel_WallGrime_A`, `Tunnel_RepairPatch_A`, `Tunnel_Soot_A`) on random bays.
- **Terrain:** keep terrain chunks that rise toward the portal before the Entry chunk (e.g. P1 Terrain `Terrain_Cut_Medium` → `Terrain_RockCut`). Unity provides the hillside over the tunnel (terrain / hill mesh); the QA hill in the Blender preview is not exported.

#### Optional vs required
- **Required per chunk:** module LOD group, P0 road chunk, the colliders listed above, and the portal on Entry / Exit.
- **Optional:**
  - sign supports: `Tunnel_OverheadSignFrame` + P1 `SignPanel_Small`, `Tunnel_VMS_Frame` + P1 `VMS_Panel`, `Tunnel_LaneSignal_Frame`, `Tunnel_WallSignBracket` + P1 wall signs;
  - flag signs: `Tunnel_ExitSign`, `Tunnel_SOS_Sign`;
  - decals.
  - Place these at bay mid-points (y −2.5 − 5k in Blender, z 2.5 + 5k in Unity) between light rows.

#### Must not be duplicated
- P0 road / shoulder / median geometry: the modules contain none.
- The P1 sign / VMS panels: only their tunnel supports are new.
- The P0 drain inside the tunnel: replaced by the tunnel slot drain.
- The kit pieces (wings, top, retaining, wall panels, fixtures): already merged into the module / portal LODs. Use them only for custom builds, never in addition to a module.

---

### `reports/P1_tunnel_materials.md`

### P1-BLENDER-04 — Tunnel materials, textures and texel density

These are Blender **source / preview** materials, not Unity shaders. Unity owns final shading, emissive intensity, wetness, reflections and exposure.

#### Materials (11 shared)
| Material | Texture set | Used for |
|---|---|---|
| `MAT_Tunnel_Concrete` | T_Tunnel_Concrete_2K | arch / shell, walkway, kerbs, barrier, portal, louvre canopy, recess interiors, drain channel |
| `MAT_Tunnel_Concrete_Dark` | T_Tunnel_Concrete_2K (tinted 0.62) | shell of `Tunnel_DarkVariant_40m` (soot-darkened interior zone) |
| `MAT_Tunnel_WallPanel` | T_Tunnel_Trim_2K | enamel cladding panels, precast lower panels, end trims |
| `MAT_Tunnel_Metal` | T_Tunnel_Trim_2K | fixture housings, fans, ducts, cabinets, doors, signal housings |
| `MAT_Tunnel_Galvanized` | T_Tunnel_Trim_2K | cable trays, light tracks, brackets, hangers, sign / VMS / signal frames, louvres, cover plates |
| `MAT_Tunnel_Rubber` | T_Tunnel_Trim_2K | cables, anti-vibration pads, fan inlet discs, hose reel |
| `MAT_Tunnel_Drain` | T_Tunnel_Trim_2K | slot-drain grates |
| `MAT_Tunnel_Light_White` | — (emissive source colour) | fixture lenses |
| `MAT_Tunnel_Light_Emergency` | — (emissive source colour, green) | guidance LEDs, lay-by beacon |
| `MAT_Tunnel_Sign` | T_Tunnel_Signs_2K | SOS / EXIT / lane-signal faces, name plate, emergency door, cabinet plates |
| `MAT_Tunnel_Decal` | T_Tunnel_Decals_2K | leak stains, grime, soot, repair patch (alpha-blended) |

The brief's `MAT_Tunnel_Light` category is split into `MAT_Tunnel_Light_White` and `MAT_Tunnel_Light_Emergency`.

#### Trim sheet `T_Tunnel_Trim_2K` (BaseColor, Normal, Roughness, Metallic, AO; 2048²)
The sheet is made of horizontal strips, measured in pixels from the bottom. U tiles along the member.

| Strip | px (y, height) | U tile | Texel density |
|---|---|---|---|
| panel (enamel cladding, fixing bolts, faint lower grime) | 0, 1024 | 5 m = one panel | 410 px/m along U, 427 px/m in V (2.4 m panel height) |
| concrete_dirty (precast lower panel, road-spray gradient) | 1024, 256 | 4 m | 512 px/m along U, 284 px/m in V (0.9 m) |
| concrete_edge (clean precast edge / end trim) | 1280, 128 | 4 m | 512 px/m along U |
| galvanized (spangle, metallic 1) | 1408, 128 | 4 m | 512 px/m along U |
| painted_metal | 1536, 128 | 4 m | 512 px/m along U |
| rubber | 1664, 64 | 4 m | 512 px/m along U |
| door (leaf height along U: kick plate, louvre band, warning-plate area) | 1728, 192 | 4 m | 512 px/m along the leaf height, 192 px over the leaf width |
| sign_frame | 1920, 64 | 4 m | 512 px/m along U |
| grate (slot pattern for LOD1 / LOD2 plates) | 1984, 64 | 4 m | 512 px/m along U |

- **Small trim members:** the face fills the strip height. U runs in metres along the face's longest edge, so long members tile continuously.
- **Guard band:** a 2 px guard band sits inside every strip.

#### Concrete `T_Tunnel_Concrete_2K` (BaseColor, Normal, Roughness, AO)
- **Tiling:** tileable in both directions (FFT band-limited noise). **1 tile = 4 m = 512 px/m**, the same density as the P0 asphalt.
- **Content:** mottling, fine pores and very restrained staining. Heavy dirt is not baked in.
- **Shell UVs:** U = −y / 4 and V = profile arc length / 4. A 40 m module is exactly 10 tiles and a 20 m module 5, so the texture is continuous across Snap points.
- **Other concrete:** world-scale box projection at the same 4 m tile. One 0–1 texture is never stretched across 40 m.

#### Signs `T_Tunnel_Signs_2K` (BaseColor, Roughness, Emissive mask)
- **Content:** generic graphics with no branding: SOS, EXIT, EXIT 150 M, lane-control green arrow / red X, phone, extinguisher, hydrant, `TUNNEL 1` name plate, emergency cross-passage door, warning plate, LAY-BY, 4.5 M height limit.
- **Emissive:** a mask (1 = lit face) for Unity's emissive channel.
- **Layout:** atlas rects are in `tun_common.SIGNS` and `reports/P1_tunnel_textures.json`.

#### Decals `T_Tunnel_Decals_2K` (BaseColor + alpha, Normal, Roughness)
- **Assets:** `Tunnel_LeakStain_A` (0.8 × 2.0 m), `_B` (1.2 × 1.6), `Tunnel_WallGrime_A` (5.0 × 1.0), `Tunnel_RepairPatch_A` (1.6 × 1.2), `Tunnel_Soot_A` (6.0 × 3.0).
- **Form:** separate reusable quads facing +X; place them 5 mm in front of the surface.
- **Unity:** URP Decal Projector or a transparent mesh decal.

#### Wear / dirt strategy (`TunnelWear` vertex layer: FLOAT_COLOR, point domain)
Every renderable mesh carries this layer. The values come from an object-space formula, and every asset is authored at its true mounting height.

| Channel | Meaning | Where it is strong |
|---|---|---|
| R | road-spray grime | strongest 0–1.6 m, so the lower walls / plinth are dirty and the upper wall clean; DirtyVariant panels are boosted |
| G | wetness / leak potential | walkway, kerbs, drains, portal-end low zones |
| B | soot | rises from 3 m toward the crown, so the ceiling darkens |
| A | per-element random variation | everywhere (tint variation) |

The Blender preview multiplies albedo by `(1 − 0.45·R)(1 − 0.35·B)` (strength varies per material). Unity should reproduce this in its tunnel shader and drive wet-road / leak effects from G.

**Wetness:** roughness maps are dry values, so Unity can lower roughness by `G × wetness`. No Blender-only wet material is used anywhere.

#### Emissive-source materials
`MAT_Tunnel_Light_White`, `MAT_Tunnel_Light_Emergency` and the lit faces of `MAT_Tunnel_Sign` define colour and mask only. The Blender emission strengths (12 / 6 / 2) are preview values. Unity sets real intensities per quality tier and day / night and decides which fixtures also get real lights (see `UnityTransfer/README/TUNNEL_LIGHTING_GUIDE.md`).

---

### `reports/P1_tunnel_FINAL_FREEZE.md`

### P1_Tunnel — FINAL FREEZE

Date: 2026-10-07 · Phase P1-BLENDER-04 · Status: **FROZEN**. Nothing under `environment/P1_Tunnel/` is to be edited; later phases may only link from it read-only.

#### Final deliverables
- **Final blend (export source):** `blend/tunnel_07_export_ready.blend`. Checkpoints `tunnel_01_blockout` … `tunnel_06_lods_collision` are kept unchanged.
- **FBX (`exports/`, identical in `UnityTransfer/FBX/`):** `Tunnel_Collision.fbx`, `Tunnel_Drainage.fbx`, `Tunnel_Lights.fbx`, `Tunnel_Portals.fbx`, `Tunnel_ServiceSafety.fbx`, `Tunnel_Shell.fbx`, `Tunnel_Structures.fbx`, `Tunnel_Ventilation.fbx`, `tunnel_complete.fbx`
- **Textures:** `textures/concrete/` (T_Tunnel_Concrete_2K ×4), `textures/trim/` (T_Tunnel_Trim_2K ×5), `textures/signs/` (×3), `textures/decals/` (×3); `textures/metal/` is intentionally empty (see README).
- **Reports:** `reports/P1_tunnel_discovery.md`, `P1_tunnel_materials.md`, `P1_tunnel_validation.txt`, `P1_tunnel_geometry.json`, `P1_tunnel_export_manifest.json`, `P1_tunnel_source_baseline.json`, `P1_tunnel_source_integrity_check.md`, `P1_tunnel_textures.json`, `P1_tunnel_qa_sequence.json`, `P1_tunnel_FINAL_REPORT.md`.
- **Previews:** 20 images in `previews/` (P1_tunnel_asset_library.png, P1_tunnel_ceiling.png, P1_tunnel_chase_view.png, P1_tunnel_drainage.png, P1_tunnel_driver_view.png, P1_tunnel_emergency_bay.png, P1_tunnel_entry.png, P1_tunnel_exit.png, P1_tunnel_full_cutaway.png, P1_tunnel_full_sequence.png, P1_tunnel_high_chase.png, P1_tunnel_night.png, P1_tunnel_portal_100m.png, P1_tunnel_portal_200m.png, P1_tunnel_portal_300m.png, P1_tunnel_portal_50m.png, P1_tunnel_portal_front.png, P1_tunnel_straight.png, P1_tunnel_ventilation.png, P1_tunnel_wall_detail.png).
- **UnityTransfer:** `UnityTransfer/` (FBX, Textures, Reports, README: `TUNNEL_IMPORT_NOTES.md`, `TUNNEL_LIGHTING_GUIDE.md`, `TUNNEL_STREAMING_GUIDE.md`).

#### Validation status
`reports/P1_tunnel_validation.txt`: **SUMMARY: 0 errors, 0 warnings** (33 checks: the 23 required checks, every FBX re-imported into a clean scene, hierarchy, frozen-source integrity).
Source integrity: **PASS** (`reports/P1_tunnel_source_integrity_check.md`).

#### Known limitations
- Module LOD1 / LOD2 come out at 19–26 % / 7–9 % of LOD0. That is below the 40–60 % / 15–30 % guidance, because LOD0 detail is concentrated in small features (grate bars, chamfers, cables, hangers, brackets, lining grooves) that LOD1 drops. Expect a visible LOD0→1 change at close range; set LOD0 screen height high (≥ 0.6).
- Portal assembly LOD0 is 1,366 tris, below the 8–20 k guidance. It was not padded; its silhouette was checked at 50 / 100 / 200 / 300 m.
- The hillside over the tunnel in the previews is a QA-only mesh (linked P1 terrain materials, not exported). Unity / the level must supply the hill. Its shading near the wing tops is approximate.
- Preview lighting is Blender-only (area lights at the lenses, Eevee shadow budget exceeded at 220+ lights): not photometric, not Unity values.
- The wet-road QA (optional) was not rendered: the P0 road material is frozen and linked, so no preview-only wet override was made. Wetness support lives in `TunnelWear.G` + dry roughness maps.
- Kit pieces with LODs (lights, props) are also merged into module LODs; using both would duplicate geometry (see the streaming guide).

_(SHA-1 table omitted in this digest; it is in the frozen phase folder.)_

---

### `reports/P1_tunnel_validation.txt`

```text
== P1-BLENDER-04 TUNNEL - VALIDATION ==
source blend/tunnel_07_export_ready.blend; TUNNEL_MASTER 237 objects, 147 meshes (137 renderable, 10 colliders)

[PASS]  1. required modules / kit assets / colliders exist in TUNNEL_MASTER (64 required names; 70 registered assets + 10 colliders)
[PASS]  2. 40 m modules: every LOD spans exactly y 0 .. -40.000 (barrier end flare of Entry / Exit excluded by design)
[PASS]  3. 20 m modules: every LOD spans exactly y 0 .. -20.000
[PASS]  4. Snap_Start / Snap_End on every runtime module and shell: distance exactly 40.000 / 20.000 m (Start = root origin)
[PASS]  5. tunnel interior width (structural wall to wall) 22-26 m and wider than the full P0 road kit incl. median strip
[PASS]  6. height clearance over the whole road kit (x -10.2 .. 8.7): lowest tunnel geometry >= 5.5 m (fixtures, fans, louvre canopy, sign / VMS / lane-signal supports)
[PASS]  7. ceiling clearance: arch >= 6.0 m above both road-kit edges, crown 7-9 m
[PASS]  8. portal alignment: the portal opening reveal reproduces the tunnel profile at the portal plane (entry + mirrored exit); reference empties present
[PASS]  9. road clearance: no tunnel / portal geometry inside the drivable envelope (x -10.2 .. 8.7, z 0.045 .. 5.5 m)
[PASS] 10. wall / barrier clearance: barrier toe outside the road kit (>= 0.5 m beyond the shoulder edge), walls >= 2.0 m beyond it, 0.99 m walkway behind the barrier
[PASS] 11. module seams: identical shell cross-section at Snap_Start / Snap_End (lining joints are half-grooves at both ends), shell UV U = -y / 4 lands on an integer at Snap_End (U or V per projection axis) (continuous texture), every detail inside its module
[PASS] 12. materials: only the 11 shared tunnel materials, every slot used, colliders have none
[PASS] 13. trim sheet T_Tunnel_Trim_2K (BaseColor / Normal / Roughness / Metallic / AO), tileable T_Tunnel_Concrete_2K, sign + decal atlases exist at 2048 x 2048
[PASS] 14. UVs: UVMap on every renderable mesh; trim faces stay inside one trim strip; sign / decal faces inside one atlas rect; concrete is world-scale (4 m per tile, never one 0-1 over 40 m)
[PASS] 15. LODs: 53 LOD groups (<Asset> root + <Asset>_LOD0..n), triangle counts strictly decreasing
       info: module LOD1 / LOD2 triangle ratios {"Tunnel_DarkVariant_40m": [0.19, 0.07], "Tunnel_EmergencyBay_40m": [0.21, 0.08], "Tunnel_Entry_40m": [0.26, 0.08], "Tunnel_Exit_40m": [0.23, 0.09], "Tunnel_ServiceBay_40m": [0.21, 0.09], "Tunnel_Straight_20m": [0.2, 0.07], "Tunnel_Straight_40m": [0.19, 0.07], "Tunnel_Ventilation_40m": [0.22, 0.08]}
[PASS] 16. colliders: Collision_TunnelWall_L/R (40/20 m), Collision_TunnelBarrier (+20 m, +End), Collision_TunnelPortal (+Exit), Collision_ServiceBay: closed, low-poly (< 300 tris), no ceiling collision
[PASS] 17. pivots: modules / shells at road centre Snap_Start; ceiling fixtures and fans at their mount point (top, z 0); portals at road centre base; every asset root at the world origin
[PASS] 18. transforms: every production mesh has identity world matrix (scale 1, no rotation, no negative scale)
[PASS] 19. normals / topology: no zero-area faces, ngons, loose vertices, duplicate faces or inconsistently wound neighbours; curved concrete smooth, structural edges sharp (35 deg)
[PASS] 20. vertex data: TunnelWear colour attribute (R grime, G wetness, B soot, A variation) on every renderable mesh, values 0..1
[PASS] 21. naming: every production object matches Tunnel_ / TunnelShell_ / TunnelWall_ / TunnelLight_ / Collision_ prefixes, LODs _LOD0..n, snaps _Snap_Start/_Snap_End, no .001 duplicates
[PASS] 22. export selection == TUNNEL_MASTER; no linked P0 road / P1 props / terrain / vegetation / car data, no QA / camera / light / helper objects in any FBX
[PASS] 23. FBX re-import Tunnel_Shell.fbx: 65 objects, names match, world deviation 5.0e-04 m, triangles / UVs / TunnelWear / materials preserved; Unity +Y up / +Z forward: {"Tunnel_Straight_40m": {"file_space_up_Y": [-0.33, 8.22], "file_space_forward_Z": [-0.0, 40.0], "snap": 40.0}, "Tunnel_Straight_20m": {"file_space_up_Y":...
[PASS] 24. FBX re-import Tunnel_Portals.fbx: 35 objects, names match, world deviation 3.9e-04 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 25. FBX re-import Tunnel_Structures.fbx: 44 objects, names match, world deviation 5.0e-04 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 26. FBX re-import Tunnel_Lights.fbx: 16 objects, names match, world deviation 5.0e-04 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 27. FBX re-import Tunnel_Ventilation.fbx: 17 objects, names match, world deviation 4.9e-04 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 28. FBX re-import Tunnel_ServiceSafety.fbx: 38 objects, names match, world deviation 5.0e-04 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 29. FBX re-import Tunnel_Drainage.fbx: 12 objects, names match, world deviation 9.5e-07 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 30. FBX re-import Tunnel_Collision.fbx: 10 objects, names match, world deviation 5.0e-04 m, triangles / UVs / TunnelWear / materials preserved
[PASS] 31. FBX re-import tunnel_complete.fbx: 237 objects, names match, world deviation 5.0e-04 m, triangles / UVs / TunnelWear / materials preserved; Unity +Y up / +Z forward: {"Tunnel_Straight_40m": {"file_space_up_Y": [-0.33, 8.22], "file_space_forward_Z": [-0.0, 40.0], "snap": 40.0}, "Tunnel_Straight_20m": {"file_space_up...
[PASS] 32. FBX hierarchy: tunnel_complete.fbx re-imports with the same parent / child structure (LOD roots, snap + reference empties)
[PASS] 33. frozen-source integrity: P0 Road, P1 Props, P1 Terrain, P1 Vegetation, cars and all other workspace files byte-identical to the pre-phase baseline

Triangle budgets are guidance only; below-budget assets are not reported as warnings.
SUMMARY: 0 errors, 0 warnings
```

