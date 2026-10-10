import bpy,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];master=bpy.data.collections['REFERENCE_Master_06'];master.hide_viewport=False
col=bpy.data.collections['Car_LOD0'];col.hide_viewport=False
for o in list(col.all_objects):
 if o['lod_category'] not in ['Body','Glass']:continue
 src=bpy.data.objects[o['source_object']];mods=[]
 # Keep the actual master exterior surface and thin perimeter walls, discard hidden back skins.
 for m in src.modifiers:
  if m.type=='SOLIDIFY':mods.append((m,m.show_viewport));m.show_viewport=False
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(src.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
 for m,v in mods:m.show_viewport=v
 old=o.data;o.data=me;bpy.data.meshes.remove(old)
 d=o.modifiers.new('Curvature-limited planar surface simplification','DECIMATE');d.decimate_type='DISSOLVE';d.angle_limit=math.radians(.4 if o['lod_category']=='Body' else .3);d.delimit={'MATERIAL','UV','SEAM'}
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
 for m,v in mods:
  so=o.modifiers.new('Retained panel edge thickness','SOLIDIFY');so.thickness=m.thickness;so.offset=m.offset;so.use_even_offset=m.use_even_offset;so.use_rim=True;so.use_rim_only=o['lod_category']=='Body'
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
 if o['lod_category']=='Body':o['intentional_open_surface']='Exterior panel and perimeter wall; hidden duplicate inner skin removed'
 me.calc_loop_triangles();print(o.name,len(me.loop_triangles),flush=True)
master.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
