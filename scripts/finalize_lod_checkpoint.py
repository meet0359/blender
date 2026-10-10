import bpy,json,hashlib,runpy,struct
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=bpy.context.scene
v=json.loads((R/'lod_validation.json').read_text());assert not v['errors'],v['errors']
assert hashlib.sha256((R/'racing_car_06_materials_uv.blend').read_bytes()).hexdigest()==S['master_06_sha256']
removed=0
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];total=0
 for o in list(col.all_objects):
  old=o.data;used=sorted({vi for p in old.polygons for vi in p.vertices})
  if len(used)<len(old.vertices):
   remap={vi:i for i,vi in enumerate(used)};me=bpy.data.meshes.new(old.name+'_compact');me.from_pydata([old.vertices[i].co for i in used],[],[tuple(remap[i] for i in p.vertices) for p in old.polygons]);me.update()
   for m in old.materials:me.materials.append(m)
   for uvold in old.uv_layers:
    uv=me.uv_layers.new(name=uvold.name)
    for a,b in zip(uv.data,uvold.data):a.uv=b.uv
   for a,b in zip(me.polygons,old.polygons):a.material_index=b.material_index;a.use_smooth=b.use_smooth
   edgeprops={tuple(sorted((remap[e.vertices[0]],remap[e.vertices[1]]))):(e.use_seam,e.use_edge_sharp) for e in old.edges if e.vertices[0] in remap and e.vertices[1] in remap}
   for e in me.edges:
    seam,sharp=edgeprops.get(tuple(sorted(e.vertices)),(False,False));e.use_seam=seam;e.use_edge_sharp=sharp
   me.normals_split_custom_set([tuple(n.vector) for n in old.corner_normals])
   removed+=len(old.vertices)-len(used);o.data=me;bpy.data.meshes.remove(old)
  o.data.calc_loop_triangles();total+=len(o.data.loop_triangles)
 assert total==v['lods'][str(lod)]['total'],(lod,total)
 col.hide_render=lod!=0;col.hide_viewport=lod!=0
bpy.data.collections['REFERENCE_Master_06'].hide_render=True;bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
for im in bpy.data.images:
 if im.source=='FILE' and im.filepath:
  p=Path(bpy.path.abspath(im.filepath));assert p.exists(),str(p)
  if p.is_relative_to(R):im.filepath='//'+str(p.relative_to(R))
for n in ['lod0_front_3q','lod0_rear_3q','lod0_side','lod0_wheel','lod0_cockpit','lod1_distance','lod2_distance','lod3_distance']:
 p=R/'previews'/(n+'.png');assert struct.unpack('>II',p.read_bytes()[16:24])==(1920,1080)
for n in ['side','front_3q','rear_3q','front','rear']:assert (R/'previews'/('lod_comparison_'+n+'.png')).exists()
runpy.run_path(str(R/'scripts/write_lod_report.py'))
for fn,name in [('lod_report.md','READ_ME_LOD_07'),('lod_validation.json','VALIDATION_LOD_07'),('lod_silhouette_metrics.json','SILHOUETTE_METRICS_07')]:
 t=bpy.data.texts.get(name) or bpy.data.texts.new(name);t.clear();t.write((R/fn).read_text())
S.camera=bpy.data.objects['Camera_Presentation'];S['LOD_triangle_counts']=str({i:v['lods'][str(i)]['total'] for i in range(4)});S['LOD_validation']='See READ_ME_LOD_07 and VALIDATION_LOD_07; master preserved';S['unused_vertices_removed']=removed
bpy.ops.object.select_all(action='DESELECT');o=bpy.data.objects['Car_Body_LOD0'];o.select_set(True);bpy.context.view_layer.objects.active=o
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   space=area.spaces.active;space.shading.type='MATERIAL';space.overlay.show_overlays=False
   space.region_3d.view_distance=6.7;space.region_3d.view_location=(0,0,.6);space.region_3d.view_rotation=S.camera.rotation_euler.to_quaternion();space.region_3d.view_perspective='PERSP'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
print('FINAL VERIFIED; unused vertices removed',removed,flush=True)
