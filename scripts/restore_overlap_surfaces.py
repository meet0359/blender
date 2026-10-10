import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.data.collections['REFERENCE_Master_06'].hide_viewport=False
for name in ['Car_Body','Front_Bumper','Hood','Rear_Bumper']:
 src=bpy.data.objects[name];low=bpy.data.objects[name+'_LOD0'];solid=[m for m in src.modifiers if m.type=='SOLIDIFY']
 for m in solid:m.show_viewport=False
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();e=src.evaluated_get(dg);pre=e.to_mesh();n=len(pre.polygons);e.to_mesh_clear()
 for m in solid:m.show_viewport=True
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();high=bpy.data.meshes.new_from_object(src.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
 keep=[p for p in high.polygons if p.index<n or p.index>=2*n];me=bpy.data.meshes.new(name+'_exact_outer');me.from_pydata([v.co for v in high.vertices],[],[tuple(p.vertices) for p in keep]);me.update()
 for m in high.materials:me.materials.append(m)
 uv=me.uv_layers.new(name='UVMap');normal=[];i=0
 for p,newp in zip(keep,me.polygons):
  newp.use_smooth=p.use_smooth;newp.material_index=p.material_index
  for li in p.loop_indices:
   uv.data[i].uv=high.uv_layers['UVMap'].data[li].uv;normal.append(tuple(high.corner_normals[li].vector));i+=1
 me.normals_split_custom_set(normal);old=low.data;low.data=me;bpy.data.meshes.remove(old);bpy.data.meshes.remove(high);low['intentional_open_surface']='Exact master exterior and perimeter walls; hidden inner skin omitted';me.calc_loop_triangles();print(name,len(me.loop_triangles),flush=True)
bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
