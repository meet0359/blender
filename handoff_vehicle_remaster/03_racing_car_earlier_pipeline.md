# Earlier unnamed racing car (racing_car_00 ... 09): pipeline notes

This is a separate, earlier generic racing car (4.58 m, wheelbase 2.70 m). As far as the workspace shows, it is not one of the five player cars. It is included for its LOD category breakdown, its material/UV export notes and its phase-validation style.


---

## `lod_report.md`

_LOD0-3 targets and per-category triangle breakdown (body, wheels, tires, brakes, interior, glass, lights, aero)_

# Optimized racing car — checkpoint 07

Checkpoint 06 remains the high-resolution reference. All work was performed in Blender. No engine export, colliders or gameplay were created. Only Car_LOD0 is visible by default; enable one LOD collection at a time. The hidden REFERENCE_Master_06 collection is for comparison and is not part of any production LOD.

## 1–6. Evaluated triangle counts and reductions

| Version | Triangles | Reduction from master | Requested range |
|---|---:|---:|---|
| Master | 650,684 | — | Preserved |
| LOD0 | 176,152 | 72.93% | 140,000–180,000 |
| LOD1 | 99,084 | 84.77% | 70,000–100,000 |
| LOD2 | 44,985 | 93.09% | 30,000–50,000 |
| LOD3 | 16,386 | 97.48% | 8,000–18,000 |

Counts use evaluated mesh loop triangles__not polygon counts. The delivered LOD meshes have their modeling reductions resolved; their logical objects, materials, UVs and wheel transforms remain editable. The reference master retains its original modeling modifiers.

## 7. Geometry by category

| Category | Master | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---:|---:|---:|---:|---:|
| Body | 156,968 | 70,250 | 33,491 | 13,726 | 4,256 |
| Wheels | 29,616 | 18,200 | 12,040 | 5,104 | 1,744 |
| Tires | 73,728 | 14,544 | 8,928 | 5,304 | 2,048 |
| Brakes | 44,912 | 8,140 | 5,096 | 1,480 | 504 |
| Interior | 119,164 | 27,110 | 15,080 | 6,490 | 2,238 |
| Glass | 55,000 | 6,508 | 2,777 | 1,373 | 558 |
| Lights | 71,152 | 16,938 | 9,390 | 4,372 | 1,674 |
| Aero/Trim | 100,144 | 14,462 | 12,282 | 7,136 | 3,364 |
| **Total** | 650,684 | 176,152 | 99,084 | 44,985 | 16,386 |

## 8–9. Lettering and seams

- Removed the four physical tire-lettering meshes from every production LOD: **45,056 evaluated triangles saved**. The generic “AERO SPORT” and tire-size markings are retained through a 4096² tangent normal bake and a separate baked color mask, using the existing tire atlas UVs. No raised-letter geometry or decal carriers remain.
- Removed the 20 identified interior seam/pad-division meshes: **12,464 evaluated triangles saved**. The final seam normal map was baked in isolated groups onto the dashboard, console, doors, seat bolsters, cushions and backrest pads. Isolation prevents other cabin parts contaminating the seam normals. Seat, dashboard and steering-wheel silhouette geometry remains.

## 10. Subdivision and panel strategy

The production geometry was evaluated from the master, then reduced by component. It was not reduced as one vehicle-wide mesh. Nearly planar regions use angle-limited dissolve while preserving UV/material seams. Curved components use individually assigned budgets, followed by topology, silhouette and shading checks.

For LOD0, the main body, hood and front/rear bumpers retain the exact master exterior surfaces and their corner normals; their hidden duplicate inner skins are removed. This avoids interference between closely overlapping panels. Other outer panels retain perimeter walls where appropriate. LOD1 reuses this exterior-surface approach, retaining the touching hood and bumper surfaces and simplifying other curvature without moving surviving vertices. The higher LOD0 count is deliberate: close-view paint quality takes precedence over the preferred 160k target.

## 11. Lights and glass

Lens silhouettes, projectors and DRL/taillight signatures remain in the hero version. Small light components use separate budgets; lower LODs discard internal shrouds and the far version omits projector lenses. Glass is rebuilt as smooth optical sheets with source normals and progressively fewer faces. All four LODs share **MAT_Glass_LOD_Thin**, a straight-transmission/Fresnel-reflection approximation with IOR 1.46 in the Fresnel node. This intentionally differs from the thick refractive master glass, avoiding visible distortion from closely spaced simplified front/back surfaces. Cabin visibility and reflection remain; volumetric optical thickness is not represented in the LOD windows.

## 12. Brakes, wheels and tires

The five split-spoke design and independent wheel origins remain. Invisible brake ventilation hardware is removed; the hero retains major rotor slots, calipers and front piston bosses, while tiny rear bosses are omitted. Lower LODs remove lugs/recesses and other small components. Wheel wells were rebuilt as closed, low-segment liners rather than accepting collapsed thin shells. Grille bars are deliberate front-facing sheets, backed by the dark intake.

LOD0 retains the primary tire grooves and shoulder detail. LOD1 removes shoulder-sipe objects; lower versions simplify the tire profile. LOD3 uses a smooth 32-segment, eight-ring tire with no physical tread. The same rubber and baked lettering system is reused.

## 13. High-to-low bakes

New shared maps (all 4096², Non-Color):

- `textures/racing_car/tires/lod_detail_Normal.png`
- `textures/racing_car/tires/lod_detail_AO.png`
- `textures/racing_car/tires/lod_detail_Mask.png`
- `textures/racing_car/interior/lod_detail_Normal.png`
- `textures/racing_car/interior/lod_detail_AO.png`

The normals are tangent-space (+Y) maps. Fine tire/seam detail was projected from checkpoint 06 onto canonical surfaces, then reused through preserved UVs on the optimized meshes. Geometry retains the main shapes. AO uses a finite 25 mm distance and is supplied separately rather than multiplied into Cycles lighting. The maps are production inputs, not an automatic final engine material export.

## 14. UV changes

Existing UVMap coordinates are retained/interpolated through the reductions. No whole-vehicle repack was performed. Newly rebuilt wheel-well liners use simple world-scaled trim UVs; far tires receive nearest-surface UV transfer from the master. Curves converted for the LOD meshes receive simple trim coordinates where needed. Microtexture scaling stays in the existing per-object UV-to-meter attribute. That attribute still requires an equivalent engine setup or atlas baking during the later export phase.

## 15. Materials

The existing library and texture sets are reused. Tire and interior detail variants are shared across every LOD, rather than making separate libraries per LOD. The single additional thin-glass variant is also shared. Paint, wheels, brakes, carbon and light materials otherwise retain the established system. External texture paths remain relative to the checkpoint folder.

## 16. Visual comparisons

Close hero views preserve the body identity, arches, split spokes, cockpit forms and principal lights. Changes include slightly brighter texture-based tire lettering, less tiny brake/cabin hardware, simplified carbon/trim geometry and the thin-glass rendering approximation. The lower LODs intentionally reduce internal detail. LOD3 is designed for a distant opponent, not a garage camera.

Distance reviews use approximately **14 m, 28 m and 60 m**, with a 50 mm camera. These are inspection distances, not final engine switching thresholds.

Silhouette sheets contain five rows, top to bottom: **Master, LOD0, LOD1, LOD2, LOD3**. Red pixels mark silhouette disagreement. LOD0 is compared with the master; LOD1–3 are compared with LOD0. Measurements use 640×360 binary alpha masks, so they assess outline agreement rather than reflection, interior detail or temporal popping.

| View | LOD0 vs master IoU | LOD1 vs LOD0 | LOD2 vs LOD0 | LOD3 vs LOD0 |
|---|---:|---:|---:|---:|
| side | 99.532% | 99.900% | 99.663% | 99.065% |
| front_3q | 99.975% | 99.877% | 99.860% | 99.287% |
| rear_3q | 99.960% | 99.940% | 99.731% | 98.301% |
| front | 99.586% | 99.736% | 99.568% | 99.445% |
| rear | 99.652% | 99.985% | 99.933% | 99.716% |

## 17. Validation

Machine validation reports **0 errors**. Source-file SHA-256 preservation, resolved texture links, UV presence, valid material slots, unchanged wheel centers/axes and dimensions were checked for all LODs. Wheelbase remains 2.700 m.

| LOD | Width delta (mm) | Length delta (mm) | Height delta (mm) | New topology flags |
|---|---:|---:|---:|---:|
| LOD0 | -1.296 | -0.003 | 0.000 | 0 |
| LOD1 | -1.300 | 0.000 | -0.506 | 0 |
| LOD2 | -1.300 | -0.117 | -0.529 | 0 |
| LOD3 | -1.300 | -0.348 | -0.506 | 0 |

All dimensions meet the ±10 mm allowance. Deliberate optical sheets, exterior skins and grille fronts are explicitly tagged as open surfaces; these are not claimed to be watertight solids. Other reductions were compared against source boundary/non-manifold/winding counts. Render reviews complement these checks; this is not a guarantee against every possible self-intersection or every future camera angle.

## 18. Remaining limitations

- Far LOD shading and very small trim are visibly simpler under close inspection. Final switching distances and any cross-fade require testing in the target engine.
- UV-to-meter attributes, rotor object-space mapping, glass approximation and texture packing still need engine-specific translation. No final export has been made.
- Many logical parts remain separate for editability and wheel/steering control. Engine batching/draw-call optimization is a later integration task.
- Intentional sheet geometry is appropriate to the visible surfaces but is not a collider. Do not use the render mesh as a watertight physics volume.
- The bake atlases retain the master packing, including small islands; tiny detail can disappear at distance as intended. Unique livery, weathering and final display artwork remain outside this phase.

## 19. Saved checkpoint

`/Users/meetshah/Documents/blender/racing_car_07_optimized_lods.blend`

Collections: `Car_LOD0`, `Car_LOD1`, `Car_LOD2`, `Car_LOD3`. Each contains Body, Wheels, Tires, Brakes, Interior, Glass, Lights and Aero/Trim subcollections. Wheel_FL/FR/RL/RR_LOD# remain at the original wheel centers with X-axis axles; rolling components are parented to their wheel, while brakes remain separate. LOD0 cockpit steering components are parented to a separate Steering_Wheel_LOD0.

## 20. Previews

- `/Users/meetshah/Documents/blender/previews/lod0_front_3q.png`
- `/Users/meetshah/Documents/blender/previews/lod0_rear_3q.png`
- `/Users/meetshah/Documents/blender/previews/lod0_side.png`
- `/Users/meetshah/Documents/blender/previews/lod0_wheel.png`
- `/Users/meetshah/Documents/blender/previews/lod0_cockpit.png`
- `/Users/meetshah/Documents/blender/previews/lod1_distance.png`
- `/Users/meetshah/Documents/blender/previews/lod2_distance.png`
- `/Users/meetshah/Documents/blender/previews/lod3_distance.png`
- `/Users/meetshah/Documents/blender/previews/lod_comparison_side.png`
- `/Users/meetshah/Documents/blender/previews/lod_comparison_front_3q.png`
- `/Users/meetshah/Documents/blender/previews/lod_comparison_rear_3q.png`
- `/Users/meetshah/Documents/blender/previews/lod_comparison_front.png`
- `/Users/meetshah/Documents/blender/previews/lod_comparison_rear.png`

The cockpit inspection uses identical temporary fill and suppressed softbox reflections for master/LOD comparison; these lighting changes are not saved. Its master reference is `previews/master_cockpit_through_glass.png`. Individual master/LOD silhouette masks are in `previews/lod_silhouettes/`. Supporting data: `lod_validation.json`, `lod_silhouette_metrics.json`, `lod_bake_manifest.json`, `lod_material_changes.json` and `lod_source_inventory.json`.

Work stops at checkpoint 07. No colliders or final engine export.

---

## `material_export_notes.md`

_Engine material handoff: UV channels, ORM packing, glass approximation_

# Checkpoint 08 material handoff

All 27 production materials have `_Engine` names. Original shader assets and separate source maps remain in the hidden reference library and texture folders. `engine_material_manifest.json` lists each material's images. FBX stores material identities and UV channels, but cannot preserve the full Blender node graph; rebuild the materials from this manifest and the packed maps.

## UV mapping

Channel 0 (`UVMap`) is the unchanged atlas UV map. Channel 1 (`UV_Game`) encodes the former per-object physical scale divided by material `tile_m` into loop UV coordinates. Channel 2 (`UV_Rotor`) encodes radial disc sampling as `(0, 8 * sqrt(local_y² + local_z²))`. No production shader requires an object attribute, object coordinates, or procedural scale. Original authoring properties remain as documentation only.

Use channel 1 for regular tile BaseColor, ORM and micro-normal textures. Brake-disc BaseColor/ORM use channel 2; its micro-normal uses channel 1. Tire atlas BaseColor, tire ORM, and all composite tire/interior normal maps use channel 0. Interior BaseColor/ORM tile maps use channel 1. GLB declares these texture coordinate channels explicitly. FBX material importers may default to channel 0; reassign the correct channel during material recreation.

Tire lettering is baked into `game/tire_BaseColor.png`; tire AO is packed into `game/tire_ORM.png`. Interior/tire micro-plus-detail normal arithmetic is realized in the composite atlas maps. Normal strength remains 0.3 for these detail materials, 0.65 for speaker detail. The original standalone display/mirror detail maps retain their prior strength. Tinted color variants are baked with explicit linear/sRGB conversion. Source textures remain untouched.

## ORM and AO

All packed maps are non-color data: R ambient occlusion, G roughness, B metallic. Twelve material tile sets have packed ORM maps; tire has an additional atlas ORM map. Interior isolated cavity AO atlases remain separate on channel 0 because combining atlas AO with channel-1 tile roughness/metallic would require resampling different coordinate domains. Use the retained isolated AO maps for additional interior cavity shading where the engine supports it. Tile ORM AO and tire AO are provided through the exporter-recognized `glTF Material Output` Occlusion socket. Do not multiply AO into base color again.

## Glass

`MAT_Glass_LOD_Thin_Engine` uses linear tint (0.83, 0.91, 0.95), opacity 0.18, roughness 0.025, metallic 0, transmission weight 1 and IOR 1.46. Geometry is the existing single optical sheet. This Principled approximation replaces the original transparent/Fresnel custom graph. Recreate as a thin transparent surface in the engine; avoid double darkening from simultaneously applying full alpha blending and transmission. FBX does not preserve the original optical behavior. glTF stores transmission/IOR extensions, whose rendering varies by viewer.

## Other Blender features

Clear coat, sheen, emission strength, transmission and IOR are retained in the Blender engine variants. GLB uses KHR material extensions where applicable; FBX needs explicit recreation. Emissive light meshes remain geometry, not exported light objects. Alpha sorting, thin glass, clear-coat appearance and material culling require a target-engine visual check. This phase creates no Unity assets or physics settings.

## Normal convention

Normal maps remain OpenGL tangent-space +Y. No silent green-channel inversion was performed. Leave green unflipped as the initial later Unity import setting; verify the imported result against the Blender reference before enabling any pipeline-specific flip. Mark ORM and normals as non-color data, and BaseColor as sRGB. FBX meshes include tangents; GLB render primitives include tangents, while untextured collision pieces do not require them.

## Geometry and portability

FBX and GLB use temporary triangle copies with custom normals explicitly transferred. Zero-area and duplicate triangles are excluded only from export copies; `export_copy_cleanup.json` records each difference. The editable meshes and original UVMap remain unchanged. This avoids importer validation changing triangle topology unpredictably. FBX references external textures through relative paths; distribute `exports/` together with sibling `textures/`. GLB embeds images. UV layer names may become generic on GLB re-import, but channel order and coordinates are validated.

The complete FBX and GLB contain overlapping LOD groups. Show one LOD group at a time; these files do not implement automatic LOD switching. Collision meshes are independent physics candidates, not render meshes. Engines must disable their rendering and set each hull as a convex compound collider. COM is an initial tuning reference only. Fixed calipers do not roll; rotor assemblies roll with the wheels. A later steering carrier can steer both the rolling wheel and fixed caliper together without changing these axle pivots.

---

## `phase_02_validation.txt`

_Example phase gate (blockout validation)_

```text
PHASE 2 BLOCKOUT VALIDATION
PASS: All Phase 2 required objects exist
PASS: All eight requested collections exist
PASS: All vehicle mesh scales are (1,1,1)
PASS: No default object names
PASS: No hidden vehicle meshes
PASS: Mesh coordinates are finite
PASS: Wheel_FL origin at rotational center
PASS: Wheel_FL circular around local X axis
PASS: Wheel_FL center placeholder follows wheel rotation
PASS: Wheel_FR origin at rotational center
PASS: Wheel_FR circular around local X axis
PASS: Wheel_FR center placeholder follows wheel rotation
PASS: Wheel_RL origin at rotational center
PASS: Wheel_RL circular around local X axis
PASS: Wheel_RL center placeholder follows wheel rotation
PASS: Wheel_RR origin at rotational center
PASS: Wheel_RR circular around local X axis
PASS: Wheel_RR center placeholder follows wheel rotation
PASS: Evaluated vehicle envelope: length 4.580 m, width 2.016 m, height 1.200 m
PASS: Wheelbase 2.700 m
PASS: Metric scene units
PASS: Main body origin at central chassis XY position
WARNING: Blockout only. Body curvature and arch transitions need manual review before Phase 3.
WARNING: Opaque cabin and simple bumper volumes are intentional.
WARNING: Final materials, UVs, detailed lights, interior, brakes, collider and LOD meshes are deferred.
PASS: Hidden reference empties and review floor are intentional; no hidden accidental vehicle geometry.
RESULT: 0 errors
```
