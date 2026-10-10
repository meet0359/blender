import bpy,bmesh,json,math,hashlib,sys
import numpy as np
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;lines=[];errors=[];warnings=[];source=json.loads((R/'export_geometry_source.json').read_text());old=json.loads((R/'lod_validation.json').read_text());summary={'lods':{},'wheel_tests':[]}
def check(ok,msg):
 lines.append(('PASS: ' if ok else 'ERROR: ')+msg)
 if not ok:errors.append(msg)
def warn(msg):warnings.append(msg);lines.append('WARNING: '+msg)
check(hashlib.sha256((R/'racing_car_07_optimized_lods.blend').read_bytes()).hexdigest()==S['source_07_sha256'],'Checkpoint 07 preserved byte-for-byte')
required=['Car_Root','Collision_Body','WheelColliderRef_FL','WheelColliderRef_FR','WheelColliderRef_RL','WheelColliderRef_RR','CenterOfMass']
check(all(n in bpy.data.objects for n in required),'Required root, collision and reference objects exist')
check(all('Car_LOD'+str(i) in bpy.data.collections for i in range(4)),'Four original LOD collections exist')
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];col.hide_viewport=False;bpy.context.view_layer.update();objs=list(col.all_objects);count=0;slots=0;mats=set()
 for o in objs:
  me=o.data;me.calc_loop_triangles();count+=len(me.loop_triangles);slots+=len(me.materials);mats.update(m.name for m in me.materials);s=source[o.name]
  h=hashlib.sha256(np.array([tuple(v.co) for v in me.vertices],dtype=np.float32).tobytes()).hexdigest();f=hashlib.sha256(str([tuple(p.vertices) for p in me.polygons]).encode()).hexdigest();uv=hashlib.sha256(np.array([tuple(l.uv) for l in me.uv_layers['UVMap'].data],dtype=np.float32).tobytes()).hexdigest()
  check(h==s['vertices_sha256'] and f==s['faces_sha256'] and uv==s['uv_sha256'],o.name+' geometry and original atlas UVs preserved')
  check(np.max(np.abs(np.array(o.matrix_world)-s['matrix_world']))<2e-6,o.name+' world placement preserved')
  check(all(abs(x-1)<1e-6 for x in o.scale) and o.matrix_world.determinant()>0,o.name+' unit positive scale')
  check({'UVMap','UV_Game','UV_Rotor'}.issubset({u.name for u in me.uv_layers}),o.name+' explicit export UV channels')
  check(all(m and m.name.endswith('_Engine') for m in me.materials),o.name+' named engine materials')
 check(count==old['lods'][str(lod)]['total'],f'LOD{lod} triangle count unchanged: {count}')
 summary['lods'][str(lod)]={'triangles':count,'objects':len(objs),'material_slots':slots,'unique_materials':len(mats)}
 # Rolling and steering are temporary tests only; no animation data is authored.
 for key in ['FL','FR','RL','RR']:
  wheel=bpy.data.objects['Wheel_'+key+'_LOD'+str(lod)];ref=bpy.data.objects['WheelColliderRef_'+key];check((wheel.matrix_world.translation-ref.matrix_world.translation).length<1e-6,wheel.name+' exact axle origin')
  check((wheel.matrix_world.to_3x3()@Vector((1,0,0))-Vector((1,0,0))).length<1e-6,wheel.name+' X axle')
  baseline=wheel.matrix_basis.copy();world={o.name:o.matrix_world.copy() for o in objs};center=wheel.matrix_world.translation.copy();desc=set(wheel.children_recursive);cal=[o for o in objs if o['source_object'].startswith('Caliper_') and '_'+key in o.name]
  for angle in [30,-30]:
   wheel.rotation_euler.x=math.radians(angle);bpy.context.view_layer.update();delta=Matrix.Translation(center)@Matrix.Rotation(math.radians(angle),4,'X')@Matrix.Translation(-center)
   ok=all(np.max(np.abs(np.array(o.matrix_world)-np.array(delta@world[o.name])))<3e-6 for o in desc)
   fixed=all(np.max(np.abs(np.array(o.matrix_world)-np.array(world[o.name])))<1e-6 for o in cal)
   check(ok and fixed,wheel.name+f' {angle:+} degree roll: tire/rim/rotor follow, calipers fixed')
   summary['wheel_tests'].append({'wheel':wheel.name,'angle':angle,'rolling_children':len(desc),'calipers_fixed':fixed,'pass':ok and fixed})
  wheel.matrix_basis=baseline;bpy.context.view_layer.update()
 col.hide_viewport=lod!=0
root=bpy.data.objects['Car_Root'];check(root.location.length<1e-6 and all(abs(x)<1e-6 for x in root.rotation_euler) and all(abs(x-1)<1e-6 for x in root.scale),'Car_Root ground/axle midpoint with identity orientation and unit scale')
colliders={};total=0
for o in bpy.data.collections['COLLISION'].all_objects:
 if o.type!='MESH':continue
 me=o.data;me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me);nonman=sum(not e.is_manifold for e in bm.edges);zero=sum(f.calc_area()<1e-10 for f in bm.faces);volume=bm.calc_volume(signed=True);convex=all(max((v.co-f.verts[0].co).dot(f.normal) for v in bm.verts)<1e-5 for f in bm.faces)
 colliders[o.name]={'triangles':len(me.loop_triangles),'vertices':len(me.vertices),'volume_m3':volume,'nonmanifold_edges':nonman,'zero_area_faces':zero,'convex':convex,'dimensions_m':list(o.dimensions)};total+=len(me.loop_triangles);check(nonman==0 and zero==0 and volume>0 and convex,o.name+' closed, outward, nondegenerate convex hull');bm.free()
check(total<=500,f'Compound collision triangle budget: {total}');(R/'collider_stats.json').write_text(json.dumps({'pieces':colliders,'total_triangles':total},indent=2))
production={s.material for i in range(4) for o in bpy.data.collections['Car_LOD'+str(i)].all_objects for s in o.material_slots}
for m in production:
 check(not any(n.type in ['ATTRIBUTE','TEX_COORD'] for n in m.node_tree.nodes),m.name+' no object attributes or object-coordinate shader mapping')
 for n in m.node_tree.nodes:
  if n.type=='TEX_IMAGE' and n.image:
   check(Path(bpy.path.abspath(n.image.filepath)).exists() and n.image.filepath.startswith('//textures/racing_car/'),m.name+' texture link '+n.image.name)
check(len(bpy.data.objects)==len({o.name for o in bpy.data.objects}),'Unique Blender object names')
check((R/'exports').is_dir(),'Export folder exists')
if '--pre' not in sys.argv:
 for i in range(4):check((R/'exports'/f'racing_car_LOD{i}.fbx').exists(),f'LOD{i} FBX output exists')
 check((R/'exports/racing_car_test.glb').exists(),'GLB test output exists')
warn('FBX does not reproduce Principled coat, transmission, sheen or ORM channel routing; recreate from engine_material_manifest.json. GLB material extensions are viewer dependent.')
warn('Normal maps remain OpenGL tangent +Y. Unity Texture Type Normal map should retain this convention; test its Flip Green Channel option against the supplied reference, rather than flipping by default.')
warn('CenterOfMass is a tuning reference, not a simulated or measured mass distribution. Compound hulls exclude wheels, mirrors and fragile aero.')
summary['errors']=errors;summary['warnings']=warnings;(R/'export_validation.json').write_text(json.dumps(summary,indent=2));(R/'export_validation.txt').write_text('\n'.join(lines)+'\n');print('EXPORT VALIDATION',len(errors),'errors',len(warnings),'warnings',summary['lods'],flush=True)
