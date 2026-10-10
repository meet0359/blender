import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];v=json.loads((R/'lod_validation.json').read_text());sil=json.loads((R/'lod_silhouette_metrics.json').read_text());mat=json.loads((R/'lod_material_changes.json').read_text())
lods=v['lods'];names=['Body','Wheels','Tires','Brakes','Interior','Glass','Lights','Aero_Trim']
text='# Optimized racing car — checkpoint 07\n\n'
text+='Checkpoint 06 remains the high-resolution reference. All work was performed in Blender. No engine export, colliders or gameplay were created. Only Car_LOD0 is visible by default; enable one LOD collection at a time. The hidden REFERENCE_Master_06 collection is for comparison and is not part of any production LOD.\n\n'
text+='## 1–6. Evaluated triangle counts and reductions\n\n| Version | Triangles | Reduction from master | Requested range |\n|---|---:|---:|---|\n'
text+=f'| Master | {v["master_total"]:,} | — | Preserved |\n'
for i,rng in enumerate(['140,000–180,000','70,000–100,000','30,000–50,000','8,000–18,000']):
 d=lods[str(i)];text+=f'| LOD{i} | {d["total"]:,} | {d["reduction_percent"]:.2f}% | {rng} |\n'
text+='\nCounts use evaluated mesh loop triangles, not polygon counts. The delivered LOD meshes have their modeling reductions resolved; their logical objects, materials, UVs and wheel transforms remain editable. The reference master retains its original modeling modifiers.\n\n## 7. Geometry by category\n\n| Category | Master | LOD0 | LOD1 | LOD2 | LOD3 |\n|---|---:|---:|---:|---:|---:|\n'
for c in names:text+='| '+c.replace('_','/')+' | '+' | '.join(f'{d.get(c,0):,}' for d in [v['master_categories']]+[lods[str(i)]['categories'] for i in range(4)])+' |\n'
text+='| **Total** | '+' | '.join(f'{n:,}' for n in [v['master_total']]+[lods[str(i)]['total'] for i in range(4)])+' |\n'
text+='''
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
'''
for view,rows in sil.items():text+='| '+view+' | '+' | '.join(f'{rows["LOD"+str(i)]["iou_reference"]*100:.3f}%' for i in range(4))+' |\n'
text+='\n## 17. Validation\n\n'
text+=f'Machine validation reports **{len(v["errors"])} errors**. Source-file SHA-256 preservation, resolved texture links, UV presence, valid material slots, unchanged wheel centers/axes and dimensions were checked for all LODs. Wheelbase remains 2.700 m.\n\n'
text+='| LOD | Width delta (mm) | Length delta (mm) | Height delta (mm) | New topology flags |\n|---|---:|---:|---:|---:|\n'
for i in range(4):
 d=lods[str(i)];x,y,z=d['dimension_delta_mm'];text+=f'| LOD{i} | {x:.3f} | {y:.3f} | {z:.3f} | {len(d["topology_review"])} |\n'
text+='''
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

'''
for name in ['lod0_front_3q','lod0_rear_3q','lod0_side','lod0_wheel','lod0_cockpit','lod1_distance','lod2_distance','lod3_distance','lod_comparison_side','lod_comparison_front_3q','lod_comparison_rear_3q','lod_comparison_front','lod_comparison_rear']:
 text+=f'- `/Users/meetshah/Documents/blender/previews/{name}.png`\n'
text+='\nThe cockpit inspection uses identical temporary fill and suppressed softbox reflections for master/LOD comparison; these lighting changes are not saved. Its master reference is `previews/master_cockpit_through_glass.png`. Individual master/LOD silhouette masks are in `previews/lod_silhouettes/`. Supporting data: `lod_validation.json`, `lod_silhouette_metrics.json`, `lod_bake_manifest.json`, `lod_material_changes.json` and `lod_source_inventory.json`.\n\nWork stops at checkpoint 07. No colliders or final engine export.\n'
(R/'lod_report.md').write_text(text)
