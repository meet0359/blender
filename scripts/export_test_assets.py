import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/'exports';E.mkdir(exist_ok=True);S=bpy.context.scene
root=bpy.data.objects['Car_Root'];refs=[root]+[bpy.data.objects[n] for n in ['Collision','Collision_Body','Collision_Front','Collision_Rear','Collision_Roof','CenterOfMass','WheelColliderRef_FL','WheelColliderRef_FR','WheelColliderRef_RL','WheelColliderRef_RR']]
settings=dict(use_selection=True,object_types={'EMPTY','MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',use_space_transform=True,bake_space_transform=False,use_mesh_modifiers=True,use_triangles=False,mesh_smooth_type='OFF',use_tspace=True,add_leaf_bones=False,bake_anim=False,path_mode='RELATIVE',embed_textures=False,use_custom_props=False)
state={o.name:(o.hide_render,o.hide_viewport) for o in bpy.data.objects};cstate={c.name:(c.hide_render,c.hide_viewport) for c in bpy.data.collections}
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=False;bpy.data.collections['Car_LOD'+str(i)].hide_render=False
for o in refs:o.hide_render=False;o.hide_viewport=False
# Triangulate temporary mesh copies so glTF can export complete tangent data.
original_data={};cleanup={}
for o in [o for i in range(4) for o in bpy.data.collections['Car_LOD'+str(i)].all_objects]+refs:
 if o.type!='MESH':continue
 old=o.data;old.calc_loop_triangles();tri=[];seen=set();zero=0;duplicates=0
 for t in old.loop_triangles:
  co=[old.vertices[v].co for v in t.vertices]
  if (co[1]-co[0]).cross(co[2]-co[0]).length<1e-10:zero+=1;continue
  key=tuple(sorted(tuple(c) for c in co))
  if key in seen:duplicates+=1;continue
  seen.add(key);tri.append(t)
 cleanup[o.name]={'source_triangles':len(old.loop_triangles),'export_triangles':len(tri),'zero_area_removed':zero,'duplicate_removed':duplicates}
 me=bpy.data.meshes.new(old.name+'_ExportTri');me.from_pydata([tuple(v.co) for v in old.vertices],[],[tuple(t.vertices) for t in tri]);me.update()
 for m in old.materials:me.materials.append(m)
 for p,t in zip(me.polygons,tri):p.material_index=old.polygons[t.polygon_index].material_index;p.use_smooth=True
 for uv in old.uv_layers:
  nu=me.uv_layers.new(name=uv.name)
  for p,t in zip(me.polygons,tri):
   for a,b in zip(p.loop_indices,t.loops):nu.data[a].uv=uv.data[b].uv
 me.normals_split_custom_set([tuple(old.corner_normals[li].vector) for t in tri for li in t.loops]);original_data[o]=(old,me);o.data=me
bpy.context.view_layer.update()
outputs=[]
for i in range(4):
 bpy.ops.object.select_all(action='DESELECT');objects=list(bpy.data.collections['Car_LOD'+str(i)].all_objects)+refs+[bpy.data.objects['LOD'+str(i)]]+[o for o in bpy.data.objects if o.type=='EMPTY' and o.name.startswith('LOD'+str(i)+'_')]
 for o in objects:o.hide_set(False);o.select_set(True)
 bpy.context.view_layer.objects.active=root;path=E/('racing_car_LOD'+str(i)+'.fbx');print('EXPORT',path.name,flush=True);bpy.ops.export_scene.fbx(filepath=str(path),**settings);outputs.append(str(path))
bpy.ops.object.select_all(action='DESELECT')
objects=list(set(refs+[o for i in range(4) for o in bpy.data.collections['Car_LOD'+str(i)].all_objects]+[o for o in bpy.data.objects if o.type=='EMPTY' and (o.name in ['LOD0','LOD1','LOD2','LOD3'] or o.name.startswith(('LOD0_','LOD1_','LOD2_','LOD3_')))]))
for o in objects:o.hide_render=False;o.hide_viewport=False;o.hide_set(False);o.select_set(True)
bpy.context.view_layer.objects.active=root;path=E/'racing_car_complete.fbx';bpy.ops.export_scene.fbx(filepath=str(path),**settings);outputs.append(str(path))
path=E/'racing_car_test.glb';print('EXPORT GLB',flush=True);bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_extras=True,export_yup=True,export_normals=True,export_tangents=True,export_materials='EXPORT',export_animations=False,export_cameras=False,export_lights=False,export_apply=False)
for o,(old,temp) in original_data.items():o.data=old;bpy.data.meshes.remove(temp)
for n,(r,v) in state.items():bpy.data.objects[n].hide_render=r;bpy.data.objects[n].hide_viewport=v
for n,(r,v) in cstate.items():bpy.data.collections[n].hide_render=r;bpy.data.collections[n].hide_viewport=v
manifest={'fbx_settings':{k:sorted(v) if isinstance(v,set) else v for k,v in settings.items()},'fbx_files':outputs,'glb_file':str(path),'glb_axes':{'up':'+Y','forward':'+Z','right':'+X','conversion_from_blender_xyz':['x','z','-y']},'root':'Car_Root','authoring_axes':{'forward':'-Y','up':'+Z','right':'+X'},'animation':'disabled','textures_relative_to_fbx':'../textures/racing_car/','normal_maps':'OpenGL tangent +Y; do not flip silently','texture_uv_channels':{'UVMap':0,'UV_Game':1,'UV_Rotor':2}}
(R/'export_copy_cleanup.json').write_text(json.dumps(cleanup,indent=2));manifest['temporary_triangulation']='Explicit triangle copies preserve custom normals; zero-area and duplicate triangles excluded from exports only'
(R/'export_manifest.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_08_export_ready.blend'));print('TEST EXPORTS COMPLETE',flush=True)
