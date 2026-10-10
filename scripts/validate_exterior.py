"""Geometry/assembly audit. No UV/LOD/export production or geometry decimation."""
import bpy
import bmesh
import json
import math
import re
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene
asset=[]
for name in ['CAR','WHEELS','BRAKES','INTERIOR','GLASS','LIGHTS']:
    asset.extend(o for o in bpy.data.collections[name].objects if o.type in {'MESH','CURVE'})
lines=['EXTERIOR 04 VALIDATION — no export certification / no optimization phase']
errors=[]; warnings=[]
def check(ok,message):
    lines.append(('PASS: ' if ok else 'ERROR: ')+message)
    if not ok: errors.append(message)
def warn(message):
    lines.append('WARNING: '+message); warnings.append(message)

required=['Car_Body','Hood','Car_Door_L','Car_Door_R','Front_Bumper','Rear_Bumper','Roof_Panel',
    'Rear_Engine_Cover','Front_Splitter','Side_Skirt_L','Side_Skirt_R','Rear_Diffuser','Rear_Wing',
    'Windshield','Rear_Glass','Window_FL','Window_FR','Window_RL','Window_RR',
    'Headlight_L','Headlight_R','Taillight_L','Taillight_R','Mirror_L','Mirror_R','Exhaust_L','Exhaust_R']
required += [p+k for p in ['Wheel_','BrakeDisc_','Caliper_'] for k in ['FL','FR','RL','RR']]
check(all(n in bpy.data.objects for n in required),'Required exterior objects and integrated aero anchor exist')
check(all(n in bpy.data.collections for n in ['CAR','WHEELS','BRAKES','INTERIOR','GLASS','LIGHTS','COLLIDERS','LODS','REFERENCES','PRESENTATION']),
      'Original collection structure preserved')
check(all((o.scale-Vector((1,1,1))).length<1e-5 and o.matrix_world.determinant()>0 for o in asset),
      'Positive uniform unit scales; no reflected object transforms')
check(len({o.name for o in bpy.data.objects})==len(bpy.data.objects),'No duplicate exact object names')
bad=[o.name for o in asset if re.match(r'^(Cube|Cylinder|Sphere|Object|Tire_Emboss_Glyph)(\.\d+)?$',o.name)]
check(not bad,'No meaningless default names or unjoined glyph objects: '+str(bad))
check(all(not o.hide_get() and not o.hide_viewport and not o.hide_render for o in asset),
      'No accidental hidden vehicle meshes/curves; reference empties excluded')
check(scene.unit_settings.system=='METRIC' and scene['forward_axis']=='-Y','Metric / -Y front / +Z up preserved')

for key,x,y,z in [('FL',-.825,-1.35,.345),('FR',.825,-1.35,.345),('RL',-.835,1.35,.365),('RR',.835,1.35,.365)]:
    wheel=bpy.data.objects['Wheel_'+key]
    check((wheel.location-Vector((x,y,z))).length<1e-6 and wheel.rotation_euler.to_matrix().is_identity,
          key+' axle center and local-X wheel axis preserved')
    cal=bpy.data.objects['Caliper_'+key]; before=cal.matrix_world.copy()
    rim=bpy.data.objects['Rim_Barrel_'+key]
    p0=rim.matrix_world@rim.data.vertices[0].co
    wheel.rotation_euler.x=math.pi/2; bpy.context.view_layer.update()
    p1=rim.matrix_world@rim.data.vertices[0].co
    axis0=Vector((x,y,z))
    r0=math.hypot((p0-axis0).y,(p0-axis0).z)
    r1=math.hypot((p1-axis0).y,(p1-axis0).z)
    check(abs(r0-r1)<1e-5 and (p1-p0).length>.01 and rim.parent==wheel,key+' actual rim rotation around centered X axle')
    check(cal.parent is None and (cal.matrix_world.translation-before.translation).length<1e-7,
          key+' caliper remains stationary during wheel rotation')
    wheel.rotation_euler.x=0; bpy.context.view_layer.update()

dg=bpy.context.evaluated_depsgraph_get()
categories={k:{'base_vertices':0,'base_polygons':0,'base_triangles':0,'evaluated_vertices':0,'evaluated_polygons':0,'evaluated_triangles':0}
    for k in ['Body','Wheels','Tires','Brakes','Glass','Lights','Aero']}
def category(o):
    names={c.name for c in o.users_collection}
    if 'BRAKES' in names: return 'Brakes'
    if 'GLASS' in names: return 'Glass'
    if 'LIGHTS' in names: return 'Lights'
    if 'WHEELS' in names:
        return 'Tires' if re.match(r'^Wheel_(FL|FR|RL|RR)$',o.name) or o.name.startswith('Tire_') else 'Wheels'
    if o.name.startswith(('Front_Splitter','Splitter_','Side_Skirt','Rear_Diffuser','Diffuser_Fin','Rear_Wing')): return 'Aero'
    return 'Body'

points=[]; degenerate=[]; inverted=[]; nonmanifold=[]; base_open=[]; loose=[]
trees={}; geom={}; mesh_counts={}; quad_count=face_count=0
for obj in asset:
    row=categories[category(obj)]
    if obj.type=='MESH':
        data=obj.data; data.calc_loop_triangles()
        row['base_vertices']+=len(data.vertices); row['base_polygons']+=len(data.polygons); row['base_triangles']+=len(data.loop_triangles)
        face_count+=len(data.polygons); quad_count+=sum(len(p.vertices)==4 for p in data.polygons)
        if any(p.area<1e-12 for p in data.polygons): degenerate.append(obj.name)
        used={i for p in data.polygons for i in p.vertices}
        if len(used)!=len(data.vertices): loose.append(obj.name)
        bm=bmesh.new(); bm.from_mesh(data)
        if any(not e.is_manifold for e in bm.edges): base_open.append(obj.name)
        bm.free()
    evaluated=obj.evaluated_get(dg); data=evaluated.to_mesh(); data.calc_loop_triangles()
    row['evaluated_vertices']+=len(data.vertices); row['evaluated_polygons']+=len(data.polygons); row['evaluated_triangles']+=len(data.loop_triangles)
    coords=[evaluated.matrix_world@v.co for v in data.vertices]
    points.extend(coords)
    if any(not math.isfinite(c) for p in coords for c in p): errors.append('Non-finite evaluated vertices: '+obj.name)
    bm=bmesh.new(); bm.from_mesh(data)
    nm=sum(not e.is_manifold for e in bm.edges)
    if nm: nonmanifold.append({'object':obj.name,'edges':nm})
    elif bm.faces and bm.calc_volume(signed=True)<-1e-10: inverted.append(obj.name)
    bm.free()
    if obj.name in ['Car_Body','Hood','Car_Door_L','Car_Door_R','Roof_Panel','Front_Bumper','Rear_Bumper',
                    'Rear_Engine_Cover','Windshield','Rear_Glass','Window_FL','Window_FR','Window_RL','Window_RR']:
        faces=[tuple(t.vertices) for t in data.loop_triangles]
        trees[obj.name]=BVHTree.FromPolygons(coords,faces,all_triangles=True,epsilon=0)
        geom[obj.name]=(coords,faces)
    mesh_counts[obj.name]=len(data.loop_triangles)
    evaluated.to_mesh_clear()

check(not degenerate,'Zero-area base face audit: '+str(degenerate))
check(not loose,'Unused base vertex audit: '+str(loose))
check(not inverted,'Closed evaluated signed-volume / inverted-normal audit: '+str(inverted))
if nonmanifold:
    warn('Evaluated non-manifold edges: '+json.dumps(nonmanifold))
else: check(True,'All evaluated mesh/curve surfaces are manifold')
if base_open: lines.append('PASS: '+str(len(base_open))+' open editable panel/curve base meshes become thickened/capped at evaluation; base openness recorded')

glass_contacts=[]
for glass_name in ['Windshield','Rear_Glass','Window_FL','Window_FR','Window_RL','Window_RR']:
    for body_name in ['Car_Body','Hood','Roof_Panel','Car_Door_L','Car_Door_R','Rear_Engine_Cover']:
        pairs=trees[glass_name].overlap(trees[body_name])
        if pairs:
            glass_contacts.append({'glass':glass_name,'body':body_name,'triangle_pairs':len(pairs)})
if glass_contacts: warn('Body/glass BVH contacts require seating review: '+json.dumps(glass_contacts))
else: check(True,'No body/glass triangle overlaps in audited primary surfaces')

self_candidates=[]
for name in ['Car_Body','Hood','Roof_Panel','Car_Door_L','Car_Door_R','Front_Bumper','Rear_Bumper','Rear_Engine_Cover']:
    coords,faces=geom[name]
    pairs=trees[name].overlap(trees[name])
    unique=[]
    for a,b in pairs:
        if a>=b or set(faces[a])&set(faces[b]): continue
        unique.append((a,b))
    if unique:
        bins={}
        for a,b in unique:
            c=sum((coords[i] for i in faces[a]+faces[b]),Vector())/6
            key=str(round(c.y*5)/5)
            bins[key]=bins.get(key,0)+1
        self_candidates.append({'object':name,'nonadjacent_candidates':len(unique),'longitudinal_bins_m':bins})
if self_candidates: warn('Non-adjacent self-contact candidates (BVH; assess hidden thickness/trim contacts separately): '+json.dumps(self_candidates))
else: check(True,'No non-adjacent self-overlap candidates in audited primary surfaces')

minimum=Vector([min(p[i] for p in points) for i in range(3)])
maximum=Vector([max(p[i] for p in points) for i in range(3)])
d=maximum-minimum
check(4.4<d.y<4.7 and 1.9<d.x<2.05 and 1.15<d.z<1.25,
      f'Evaluated envelope: L {d.y:.4f}, W {d.x:.4f}, H {d.z:.4f} m')
check(abs(abs(bpy.data.objects['Wheel_FL'].location.y-bpy.data.objects['Wheel_RL'].location.y)-2.7)<1e-6,'2.7000 m wheelbase')
check(all(n in bpy.data.materials for n in ['MAT_DRL','MAT_Headlight','MAT_Taillight','MAT_BrakeLight','MAT_ReverseLight','MAT_Indicator']),
      'Independent front/rear light channels exist')
check(len([o for o in asset if o.name.startswith('Diffuser_Fin_')])==4,'Four restrained diffuser fins')
total={k:sum(row[k] for row in categories.values()) for k in next(iter(categories.values()))}
lines.append('PASS: Base mesh totals '+str(total))
lines.append(f'PASS: Base quad fraction {quad_count/max(1,face_count):.1%}; major skin panels are quads')
for name,row in categories.items(): lines.append(name+': '+str(row))
warn('No final UV/textures, full interior, collider, LOD or export checks were undertaken, as requested.')
warn('Intersection tests cover primary surfaces; intentional optical/trim/duct assembly seating is not globally unioned.')
lines.append(f'RESULT: {len(errors)} errors / {len(warnings)} warnings')
report='\n'.join(lines)+'\n'
print(report)
(ROOT/'exterior_validation.txt').write_text(report)
result={'totals':total,'categories':categories,'dimensions_m':{'length':d.y,'width':d.x,'height':d.z},
    'base_quad_fraction':quad_count/max(1,face_count),'asset_objects':len(asset),
    'errors':errors,'warnings':warnings,'nonmanifold':nonmanifold,'inverted':inverted,'degenerate':degenerate,
    'glass_contacts':glass_contacts,'self_contact_candidates':self_candidates,'open_base_meshes':base_open}
(ROOT/'exterior_stats.json').write_text(json.dumps(result,indent=2))
if errors: raise RuntimeError('Exterior validation has errors')
