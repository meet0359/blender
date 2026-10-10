import sys,os;sys.path.insert(0,'/Users/meetshah/Documents/blender/scripts')
from unity09_common import *
from pathlib import Path
R=Path('/Users/meetshah/Documents/blender');O=bpy.data.objects;L=lambda s:print(s,flush=True)
SCR=Path(os.environ.get('TMPDIR','/tmp'))
names=['Car_Root','Body_LOD0','Interior_LOD0','Glass_LOD0','Lights_LOD0','Aero_LOD0','Brakes_LOD0','Wheel_FL_LOD0','Wheel_FR_LOD0','Wheel_RL_LOD0','Wheel_RR_LOD0','Steering_Wheel_LOD0','Collision_Body','Collision_Front','Collision_Rear','Collision_Roof','WheelColliderRef_FL','WheelColliderRef_FR','WheelColliderRef_RL','WheelColliderRef_RR','CenterOfMass']
objs=[O[n] for n in names]
def sub(o):
    return [o]+list(o.children_recursive)
exp=[];[exp.append(x) for o in objs for x in ([o] if o.name=='Car_Root' else sub(o)) if x not in exp]
exp=[o for o in exp if o.type in('MESH','EMPTY')]
L(f'export objects {len(exp)}')
cs={c.name:(c.hide_viewport,c.hide_render) for c in bpy.data.collections}
for n in ['Car_LOD0','COLLISION','ENGINE_REFERENCES']:bpy.data.collections[n].hide_viewport=False
def lc(c):
    for x in c.children:yield x;yield from lc(x)
for n in ['Car_LOD0','COLLISION','ENGINE_REFERENCES']:
    for c in lc(bpy.data.collections[n]):c.hide_viewport=False
st={o.name:(o.hide_viewport,o.hide_render) for o in exp}
for o in exp:o.hide_viewport=False;o.hide_set(False)
# triangulated export copies (same approach as checkpoint 08); keep arrays for later shading comparison
orig={};npz={}
for o in exp:
    if o.type!='MESH':continue
    old=o.data;old.calc_loop_triangles();tri=[];seen=set()
    for t in old.loop_triangles:
        co=[old.vertices[v].co for v in t.vertices]
        if (co[1]-co[0]).cross(co[2]-co[0]).length<1e-10:continue
        k=tuple(sorted(tuple(c) for c in co))
        if k in seen:continue
        seen.add(k);tri.append(t)
    me=bpy.data.meshes.new(old.name+'_ExportTri');me.from_pydata([tuple(v.co) for v in old.vertices],[],[tuple(t.vertices) for t in tri]);me.update()
    for m in old.materials:me.materials.append(m)
    for p,t in zip(me.polygons,tri):p.material_index=old.polygons[t.polygon_index].material_index;p.use_smooth=True
    for uv in old.uv_layers:
        nu=me.uv_layers.new(name=uv.name)
        for p,t in zip(me.polygons,tri):
            for a,b in zip(p.loop_indices,t.loops):nu.data[a].uv=uv.data[b].uv
    me.normals_split_custom_set([tuple(old.corner_normals[li].vector) for t in tri for li in t.loops]);orig[o]=(old,me);o.data=me
bpy.context.view_layer.update()
for o in exp:
    if o.type!='MESH' or not o.name.endswith('LOD0'):continue
    me=o.data;n=len(me.loops)
    if n==0:continue
    M=np.array(o.matrix_world);c=np.empty(n*3,np.float32);v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);vi=np.empty(n,np.int32);me.loops.foreach_get('vertex_index',vi)
    pos=v.reshape(-1,3)[vi]@M[:3,:3].T+M[:3,3];nr=np.array([l.vector for l in me.corner_normals],np.float32)@M[:3,:3].T
    uv=np.empty(n*2,np.float32);me.uv_layers[0].data.foreach_get('uv',uv)
    try:
        me.calc_tangents(uvmap=me.uv_layers[0].name);tg=np.array([l.tangent for l in me.loops],np.float32)@M[:3,:3].T;sg=np.array([l.bitangent_sign for l in me.loops],np.float32)
    except Exception as e:
        tg=np.zeros((n,3),np.float32);sg=np.zeros(n,np.float32)
    npz[o.name]=dict(pos=pos.reshape(-1,3,3),nrm=nr.reshape(-1,3,3),uv=uv.reshape(-1,3,2),tan=tg.reshape(-1,3,3),sgn=sg.reshape(-1,3),mat=np.array([p.material_index for p in me.polygons],np.int32),nslots=len(me.materials))
np.savez_compressed(str(SCR/'unity09_src.npz'),**{f'{k}|{kk}':vv for k,d in npz.items() for kk,vv in d.items()})
base=dict(use_selection=True,object_types={'MESH','EMPTY'},global_scale=1.0,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_mesh_modifiers=True,mesh_smooth_type='FACE',use_tspace=True,add_leaf_bones=False,bake_anim=False,path_mode='RELATIVE',embed_textures=False,use_custom_props=False)
out={}
(R/'exports').mkdir(exist_ok=True)
for tag,bake,path in [('bake_false',False,SCR/'v_false.fbx'),('bake_true',True,SCR/'v_true.fbx')]:
    bpy.ops.object.select_all(action='DESELECT')
    for o in exp:o.select_set(True)
    bpy.context.view_layer.objects.active=O['Car_Root']
    bpy.ops.export_scene.fbx(filepath=str(path),bake_space_transform=bake,use_space_transform=True,**base);out[tag]=str(path);L('exported '+tag)
import shutil
bpy.context.view_layer.objects.active=O['Car_Root']
json.dump(dict(variants=out,settings={k:sorted(v) if isinstance(v,set) else v for k,v in base.items()},objects=len(exp)),open(SCR/'unity09_export.json','w'))
for o,(old,t) in orig.items():o.data=old;bpy.data.meshes.remove(t)
print('EXPORT DONE')
