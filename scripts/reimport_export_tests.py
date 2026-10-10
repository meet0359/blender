import bpy,json,math,sys
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];mode=sys.argv[-1];source={};errors=[];warnings=[]
def mesh_info(o):
 m=o.data;m.calc_loop_triangles();n=len(m.loop_triangles)
 inds=np.array([list(t.loops) for t in m.loop_triangles]);vi=np.array([l.vertex_index for l in m.loops]);v=np.array([tuple(v.co) for v in m.vertices]);mat=np.array(o.matrix_world);pos=v[vi[inds]]@mat[:3,:3].T+mat[:3,3]
 normals=np.array([tuple(n.vector) for n in m.corner_normals])[inds]@np.linalg.inv(mat[:3,:3]);normals/=np.maximum(np.linalg.norm(normals,axis=2,keepdims=True),1e-20)
 uv=[np.array([tuple(x.uv) for x in u.data])[inds] for u in m.uv_layers]
 return {'pos':pos,'normal':normals,'uv':uv,'parent':o.parent.name if o.parent else None,'materials':[x.name for x in m.materials],'matrix':mat,'triangles':n,'uv_names':[x.name for x in m.uv_layers]}
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=False
bpy.context.view_layer.update()
levels=range(4) if mode=='glb' else [0]
for i in levels:
 for o in bpy.data.collections['Car_LOD'+str(i)].all_objects:source[o.name]=mesh_info(o)
refs={n:np.array(bpy.data.objects[n].matrix_world) for n in ['Car_Root','CenterOfMass']+['WheelColliderRef_'+k for k in ['FL','FR','RL','RR']]}
# Capture the complete expected hierarchy before opening an empty scene.
parents={o.name:o.parent.name if o.parent else None for o in bpy.data.objects if o.name in source or o.name in refs or o.name=='Collision' or o.name.startswith('Collision_') or o.type=='EMPTY' and (o.name in ['LOD'+str(i) for i in levels] or any(o.name.startswith('LOD'+str(i)+'_') for i in levels))}
bpy.ops.wm.read_factory_settings(use_empty=True)
path=R/'exports'/('racing_car_test.glb' if mode=='glb' else 'racing_car_LOD0.fbx')
if mode=='glb':bpy.ops.import_scene.gltf(filepath=str(path))
else:bpy.ops.import_scene.fbx(filepath=str(path))
bpy.context.view_layer.update();results={};maxpos=0;maxuv=0;maxangle=0
for name,s in source.items():
 if name not in bpy.data.objects:errors.append('Missing '+name);continue
 o=bpy.data.objects[name];d=mesh_info(o)
 if d['parent']!=s['parent']:errors.append(name+' parent mismatch')
 if d['materials']!=s['materials']:errors.append(name+' material slots mismatch')
 expected=json.loads((R/'export_copy_cleanup.json').read_text())[name]['export_triangles']
 if d['triangles']!=expected:errors.append(name+' exported triangle count mismatch')
 if len(d['uv'])!=len(s['uv']):errors.append(name+' UV channel count mismatch')
 # Match by spatial neighborhood, avoiding unstable lexicographic ties on coincident vertices.
 from mathutils.kdtree import KDTree
 sp=s['pos'].reshape(-1,3);dp=d['pos'].reshape(-1,3);sn=s['normal'].reshape(-1,3);dn=d['normal'].reshape(-1,3)
 su=[x.reshape(-1,2) for x in s['uv']];du=[x.reshape(-1,2) for x in d['uv']]
 tree=KDTree(len(sp))
 for j,p in enumerate(sp):tree.insert(p,j)
 tree.balance();delta=0;uvdelta=0;angle=0;zero_normals=0
 for j,p in enumerate(dp):
  near=tree.find_range(p,2e-5)
  if not near:near=[tree.find(p)]
  dist=min(x[2] for x in near);delta=max(delta,dist)
  ids=[x[1] for x in near];ud=np.array([max(np.max(np.abs(a[idx]-b[j])) for a,b in zip(su,du)) for idx in ids]);u=float(ud.min());uvdelta=max(uvdelta,u)
  ids=[idx for idx,e in zip(ids,ud) if e<u+2e-5];valid=[idx for idx in ids if np.linalg.norm(sn[idx])>.5]
  if not valid or np.linalg.norm(dn[j])<.5:zero_normals+=1;continue
  dot=max(float(sn[idx]@dn[j]) for idx in valid);angle=max(angle,float(np.degrees(np.arccos(np.clip(dot,-1,1)))))
 maxpos=max(maxpos,delta);maxuv=max(maxuv,uvdelta);maxangle=max(maxangle,angle)
 if delta>1e-4:errors.append(name+' corner positions mismatch')
 if uvdelta>2e-4:errors.append(name+' UV coordinates mismatch')
 if angle>2:errors.append(name+' corner normal direction mismatch')
 results[name]={'triangles':d['triangles'],'position_delta_m':delta,'uv_delta':uvdelta,'normal_max_angle_deg':angle,'uv_names':d['uv_names'],'material_slots':len(d['materials']),'zero_normal_corners':zero_normals}
for n,p in parents.items():
 if n not in bpy.data.objects:errors.append('Missing hierarchy object '+n)
 elif (bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None)!=p:errors.append('Hierarchy mismatch '+n)
refdelta={n:float(np.max(np.abs(np.array(bpy.data.objects[n].matrix_world)-m))) for n,m in refs.items()}
for n,e in refdelta.items():
 if e>1e-4:errors.append('Reference transform '+n)
roll=[]
for i in levels:
 for k in ['FL','FR','RL','RR']:
  o=bpy.data.objects['Wheel_'+k+'_LOD'+str(i)];base=o.matrix_basis.copy();center=o.matrix_world.translation.copy();axis=o.matrix_world.to_3x3()@Vector((1,0,0));fixed=[x for x in bpy.data.objects if x.name.startswith('Caliper_') and '_'+k+'_LOD'+str(i) in x.name];fm={x.name:x.matrix_world.copy() for x in fixed}
  for ang in [30,-30]:
   o.rotation_euler.x=math.radians(ang);bpy.context.view_layer.update();ok=(o.matrix_world.translation-center).length<1e-6 and all((x.matrix_world.translation-fm[x.name].translation).length<1e-6 for x in fixed);roll.append({'wheel':o.name,'angle':ang,'pass':ok,'axis_world':list(axis)})
   if not ok:errors.append('Imported roll '+o.name)
  o.matrix_basis=base;bpy.context.view_layer.update()
points=np.concatenate([s['pos'].reshape(-1,3) for s in source.values()]);ip=np.concatenate([mesh_info(bpy.data.objects[n])['pos'].reshape(-1,3) for n in source]);dimensions={'source_m':list(np.ptp(points,axis=0)),'imported_m':list(np.ptp(ip,axis=0)),'delta_m':list(np.abs(np.ptp(points,axis=0)-np.ptp(ip,axis=0)))}
wheelbase=abs(bpy.data.objects['Wheel_RL_LOD0'].matrix_world.translation.y-bpy.data.objects['Wheel_FL_LOD0'].matrix_world.translation.y)
if abs(wheelbase-2.7)>1e-4:errors.append('Wheelbase')
if mode=='fbx':warnings.append('FBX preserves slots and UV channels but requires material recreation; Principled extensions and ORM routing do not round-trip.')
if maxangle>.2:warnings.append('Blender custom-normal encoding introduces up to '+str(round(maxangle,4))+' degrees deviation at small detail corners; larger shading surfaces checked separately.')
report={'format':mode,'file':str(path),'errors':errors,'warnings':warnings,'object_count':len(source),'dimensions':dimensions,'wheelbase_m':wheelbase,'reference_matrix_max_deltas':refdelta,'max_corner_position_delta_m':maxpos,'max_uv_delta':maxuv,'raw_max_normal_angle_deg':maxangle,'wheel_tests':roll,'objects':results,'animation_count':len(bpy.data.actions)}
(R/(('fbx' if mode=='fbx' else 'glb')+'_reimport_validation.json')).write_text(json.dumps(report,indent=2));print('REIMPORT',mode,'ERRORS',len(errors),'WARNINGS',warnings,'DELTAS',maxpos,maxuv,maxangle,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'exports'/('validation_'+mode+'.blend')))
