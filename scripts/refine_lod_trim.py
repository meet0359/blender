import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];col.hide_viewport=False;col.hide_render=False
 for o in list(col.all_objects):
  ratio=[.78,.9,.9,.65][lod] if o.get('lod_category')=='Aero_Trim' else .75 if lod==3 and o.get('lod_category')=='Interior' else 1
  if ratio==1 or len(o.data.polygons)<12:continue
  d=o.modifiers.new('Secondary trim budget','DECIMATE');d.ratio=ratio
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
  dt=o.modifiers.new('Reference highlight normals','DATA_TRANSFER');dt.object=bpy.data.objects[o['source_object']];dt.use_loop_data=True;dt.data_types_loops={'CUSTOM_NORMAL'};dt.loop_mapping='POLYINTERP_NEAREST'
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
 col.hide_viewport=lod!=0;col.hide_render=lod!=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
