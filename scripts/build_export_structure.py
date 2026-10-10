import bpy,bmesh,json,hashlib,math
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];S=bpy.context.scene
source=R/'racing_car_07_optimized_lods.blend';S['source_07_sha256']=hashlib.sha256(source.read_bytes()).hexdigest();snapshot={}
exports=R/'exports';exports.mkdir(exist_ok=True)
col=bpy.data.collections.new('ENGINE_REFERENCES');S.collection.children.link(col)
cc=bpy.data.collections.new('COLLISION');S.collection.children.link(cc)
def empty(name,loc=(0,0,0),parent=None,collection=col):
 o=bpy.data.objects.new(name,None);collection.objects.link(o);o.empty_display_type='PLAIN_AXES';o.empty_display_size=.14;o.location=loc
 if parent:o.parent=parent
 return o
def parent(o,p):
 mw=o.matrix_world.copy();o.parent=p;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_world=mw
root=empty('Car_Root');root['forward']='-Y';root['up']='+Z';root['right']='+X';root['origin_policy']='Axle midpoint projected to nominal ground, centered laterally';root['units']='meters'
collroot=empty('Collision',parent=root,collection=cc)
for i in range(4):
 lc=bpy.data.collections['Car_LOD'+str(i)];lc.hide_viewport=False
 lr=empty('LOD'+str(i),parent=root);lr['lod_index']=i
 groups={n:empty('LOD'+str(i)+'_'+n,parent=lr) for n in ['Body','Interior','Glass','Lights','Aero','Brakes']}
 objs=list(lc.all_objects)
 for o in objs:
  me=o.data;me.calc_loop_triangles();snapshot[o.name]={'vertices_sha256':hashlib.sha256(np.array([tuple(v.co) for v in me.vertices],dtype=np.float32).tobytes()).hexdigest(),'faces_sha256':hashlib.sha256(str([tuple(p.vertices) for p in me.polygons]).encode()).hexdigest(),'matrix_world':[list(a) for a in o.matrix_world],'triangles':len(me.loop_triangles),'materials':[m.name for m in me.materials],'uv_sha256':hashlib.sha256(np.array([tuple(l.uv) for l in me.uv_layers['UVMap'].data],dtype=np.float32).tobytes()).hexdigest()}
  if o.parent and o.parent.name in {x.name for x in objs}:continue
  cat=o['lod_category'];p=lr if cat in ['Wheels','Tires'] or o.name.startswith('Steering_Wheel') else groups.get(cat,groups['Aero']);parent(o,p)
  o['export_lod']=i
 # Realize physical tiling and radial rotor coordinates in UV layers, leaving UVMap untouched.
 for o in objs:
  me=o.data;uv=me.uv_layers['UVMap'];game=me.uv_layers.get('UV_Game') or me.uv_layers.new(name='UV_Game');rotor=me.uv_layers.get('UV_Rotor') or me.uv_layers.new(name='UV_Rotor')
  for p in me.polygons:
   m=me.materials[p.material_index];tile=float(m.get('tile_m',1));scale=float(o.get('uv_meter_scale',1))/tile
   for li in p.loop_indices:
    game.data[li].uv=uv.data[li].uv*scale;co=me.vertices[me.loops[li].vertex_index].co;rotor.data[li].uv=(0,8*math.sqrt(co.y*co.y+co.z*co.z))
  me.uv_layers.active_index=0
 lc.hide_viewport=i!=0
refs={}
for key in ['FL','FR','RL','RR']:
 wheel=bpy.data.objects['Wheel_'+key+'_LOD0'];pos=wheel.matrix_world.translation;ref=empty('WheelColliderRef_'+key,pos,root);ref.empty_display_type='ARROWS';ref.empty_display_size=.23
 coords=np.array([tuple(v.co) for v in wheel.data.vertices]);rad=np.sqrt(coords[:,1]**2+coords[:,2]**2);radius=float(rad.max());width=float(np.ptp(coords[:,0]));nominal=.345 if key[0]=='F' else .365
 info={'position_world_m':list(pos),'position_local_m':list(ref.location),'radius_nominal_m':nominal,'radius_mesh_max_m':radius,'width_mesh_m':width,'width_nominal_m':.29 if key[0]=='F' else .33,'axle_local':[1,0,0],'axle_world':[1,0,0]}
 for k,v in info.items():ref[k]=v
 refs[key]=info
com=empty('CenterOfMass',(0,.22,.37),root);com.empty_display_type='SPHERE';com['purpose']='Starting tuning reference only; not a computed mass distribution or physics setting'
# Convex sections deliberately exclude fragile aero, mirrors, wheels and lights.
def hull(name,stations):
 verts=[]
 for y,w,lo,hi in stations:
  for x,z in [(-w,lo),(w,lo),(-w,hi),(w,hi)]:verts.append((x,y,z))
 me=bpy.data.meshes.new(name);o=bpy.data.objects.new(name,me);cc.objects.link(o);bm=bmesh.new()
 for v in verts:bm.verts.new(v)
 bmesh.ops.convex_hull(bm,input=list(bm.verts),use_existing_faces=False);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();o.parent=collroot;o.display_type='WIRE';o.hide_render=True;o['physics_role']='Convex compound body piece, not render geometry';o['convex']=True
 return o
hull('Collision_Body',[(-1.45,.75,.16,.55),(-.72,.78,.16,.67),(.65,.79,.16,.70),(1.40,.78,.16,.65)])
hull('Collision_Front',[(-2.17,.68,.19,.42),(-1.75,.80,.17,.54),(-1.22,.80,.17,.60)])
hull('Collision_Rear',[(.97,.78,.17,.67),(1.62,.83,.18,.78),(2.17,.74,.22,.67)])
hull('Collision_Roof',[(-.88,.54,.53,.94),(-.40,.58,.55,1.14),(.45,.58,.55,1.15),(1.08,.50,.55,.89)])
S['export_phase']='08 colliders, references and test export';S['center_of_mass_reference']=list(com.location)
(R/'export_geometry_source.json').write_text(json.dumps(snapshot,indent=2));(R/'wheel_reference_points.json').write_text(json.dumps({'wheelbase_m':2.7,'wheels':refs,'center_of_mass_m':list(com.location),'root_location_m':list(root.location),'axes':{'forward':'-Y','up':'+Z','right':'+X','axle':'X'}},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_08_export_ready.blend'));print('STRUCTURE SAVED',flush=True)
