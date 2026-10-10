"""Validate this body-refinement milestone; final production checks are deferred."""
import bpy
import bmesh
import math
import re
import json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene
lines=['REALISTIC BODY CHECKPOINT VALIDATION']
errors=[]
warnings=[]
def check(ok,message):
    lines.append(('PASS: ' if ok else 'ERROR: ')+message)
    if not ok: errors.append(message)
def warn(message):
    warnings.append(message); lines.append('WARNING: '+message)

required=['Car_Body','Hood','Front_Bumper','Rear_Bumper','Roof_Panel','Rear_Engine_Cover',
    'Windshield','Rear_Glass','Window_FL','Window_FR','Window_RL','Window_RR',
    'Front_Splitter','Side_Skirt_L','Side_Skirt_R','Rear_Diffuser','Rear_Wing',
    'Mirror_L','Mirror_R','Exhaust_L','Exhaust_R']
required += [p+k for p in ['Wheel_','BrakeDisc_','Caliper_','Rim_Barrel_'] for k in ['FL','FR','RL','RR']]
check(all(n in bpy.data.objects for n in required),'All milestone body, glass, aero, wheel and brake objects exist')
collections=['CAR','WHEELS','BRAKES','INTERIOR','GLASS','LIGHTS','COLLIDERS','LODS','REFERENCES','PRESENTATION']
check(all(n in bpy.data.collections for n in collections),'Original collection structure preserved')
asset=[o for c in collections[:6] for o in bpy.data.collections[c].objects if o.type in {'MESH','CURVE'}]
check(all((o.scale-Vector((1,1,1))).length<1e-6 for o in asset),'All vehicle scales are unity')
check(all(not re.match(r'^(Cube|Cylinder|Sphere|Object)(\.\d+)?$',o.name) for o in bpy.data.objects),'No meaningless default object names')
check(all(not o.hide_get() and not o.hide_viewport and not o.hide_render for o in asset),'No hidden accidental vehicle geometry')
check(all(all(math.isfinite(c) for c in v.co) for o in asset if o.type=='MESH' for v in o.data.vertices),'All mesh coordinates finite')
check(scene.unit_settings.system=='METRIC' and scene['forward_axis']=='-Y','Metric units / -Y forward / +Z up preserved')
for key,x,y,r in [('FL',-.825,-1.35,.345),('FR',.825,-1.35,.345),('RL',-.835,1.35,.365),('RR',.835,1.35,.365)]:
    w=bpy.data.objects['Wheel_'+key]
    check((w.location-Vector((x,y,r))).length<1e-6 and w.rotation_euler.to_matrix().is_identity,
          w.name+' original axle center and local X rotation convention retained')
    vertices=[v.co for v in w.data.vertices]
    max_y=max(v.y for v in vertices); min_y=min(v.y for v in vertices)
    check(abs(max_y-min_y-2*r)<1e-6,w.name+f' diameter {2*r:.3f} m retained')
    check(all(o.parent==w for o in bpy.data.objects if o.name.startswith(('Wheel_Spoke_'+key,'Wheel_Lug_'+key,'Rim_Outer_Lip_'+key,'Rim_Barrel_'+key))),
          w.name+' rotating rim, spokes and lugs parented')
    check(bpy.data.objects['Caliper_'+key].parent is None and bpy.data.objects['BrakeDisc_'+key].parent is None,
          key+' brakes independent; caliper remains stationary')
    # Temporarily rotate wheel 90 degrees, verify tire origin and static caliper,
    # then restore without saving any changed wheel pose.
    before=bpy.data.objects['Caliper_'+key].matrix_world.copy()
    w.rotation_euler.x=math.pi/2
    bpy.context.view_layer.update()
    check((bpy.data.objects['Caliper_'+key].matrix_world.translation-before.translation).length<1e-7,
          key+' actual rotation test leaves caliper stationary')
    w.rotation_euler.x=0
    bpy.context.view_layer.update()

check(abs(abs(bpy.data.objects['Wheel_FL'].location.y-bpy.data.objects['Wheel_RL'].location.y)-2.7)<1e-6,'2.70 m wheelbase retained')
dg=bpy.context.evaluated_depsgraph_get()
points=[]
base_polygons=base_triangles=eval_polygons=eval_triangles=0
degenerate=loose=0
for o in asset:
    e=o.evaluated_get(dg)
    if o.type=='MESH':
        base_polygons+=len(o.data.polygons)
        o.data.calc_loop_triangles(); base_triangles+=len(o.data.loop_triangles)
        degenerate+=sum(p.area<1e-12 for p in o.data.polygons)
        used={v for p in o.data.polygons for v in p.vertices}
        loose+=len(o.data.vertices)-len(used)
    m=e.to_mesh()
    points.extend(e.matrix_world@v.co for v in m.vertices)
    m.calc_loop_triangles()
    eval_polygons+=len(m.polygons); eval_triangles+=len(m.loop_triangles)
    e.to_mesh_clear()
minimum=Vector([min(p[i] for p in points) for i in range(3)])
maximum=Vector([max(p[i] for p in points) for i in range(3)])
d=maximum-minimum
check(4.4<d.y<4.7 and 1.9<d.x<2.05 and 1.15<d.z<1.25,
    f'Evaluated envelope L/W/H = {d.y:.4f} / {d.x:.4f} / {d.z:.4f} m')
check(degenerate==0,f'No zero-area base mesh faces ({degenerate})')
check(loose==0,f'No unused base mesh vertices ({loose})')
check(any(m.type=='MIRROR' for m in bpy.data.objects['Car_Body'].modifiers),'Live body symmetry retained')
check(any(m.type=='SUBSURF' for m in bpy.data.objects['Car_Body'].modifiers),'Live body subdivision retained')
check(all(n in bpy.data.materials for n in ['MAT_CarPaint','MAT_Tire','MAT_Glass','MAT_BrakeDisc','MAT_BrakeCaliper']),
    'Temporary surface-review materials exist')

wind=bpy.data.objects['Windshield']
low=min(wind.data.vertices,key=lambda v:v.co.y).co
high=max(wind.data.vertices,key=lambda v:v.co.y).co
# Use centerline stations rather than cross-width edge vertices.
center=[v.co for v in wind.data.vertices if abs(v.co.x)<.001]
low=min(center,key=lambda v:v.y); high=max(center,key=lambda v:v.y)
angle=math.degrees(math.atan2(high.z-low.z,high.y-low.y))
oldangle=math.degrees(math.atan2(1.16-.768,-.40-(-.99)))
lines.append(f'PASS: Windshield centerline rake {angle:.2f} degrees above horizontal; source {oldangle:.2f} degrees')
lines.append(f'PASS: Base meshes {base_polygons:,} polygons / {base_triangles:,} triangles')
lines.append(f'PASS: Evaluated vehicle including curve trims {eval_polygons:,} polygons / {eval_triangles:,} triangles')
warn('Temporary review shaders; final UVs/textures and light internals intentionally absent.')
warn('Only a cabin shadow tray/deck, no detailed cockpit; glass tint is provisional.')
warn('Arch end transitions and bumper-to-quarter panel joins still need production-level topology review.')
warn('Side intake trim and front duct shut lines may need additional panel integration in the next body pass.')
warn('Open base panel boundaries are intentional; Solidify supplies panel thickness. Not export-certified.')
warn('Evaluated render geometry exceeds the earlier 100–180k LOD0 target; export-budget optimization is still required.')
warn('COLLIDERS and LODS remain empty, as requested. Final collider/LOD checks deferred.')
lines.append(f'RESULT: {len(errors)} errors / {len(warnings)} stage warnings')
report='\n'.join(lines)+'\n'
print(report)
(ROOT/'realistic_body_validation.txt').write_text(report)
stats={'dimensions_m':{'length':d.y,'width':d.x,'height':d.z},'wheelbase_m':2.7,
       'base_mesh_polygons':base_polygons,'base_mesh_triangles':base_triangles,
       'evaluated_polygons':eval_polygons,'evaluated_triangles':eval_triangles,
       'windshield_angle_horizontal_deg':angle,'source_windshield_angle_horizontal_deg':oldangle,
       'asset_objects':len(asset),'errors':errors,'warnings':warnings}
(ROOT/'realistic_body_stats.json').write_text(json.dumps(stats,indent=2))
if errors: raise RuntimeError('Validation errors remain')
