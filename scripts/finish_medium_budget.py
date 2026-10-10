import bpy,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[1];c=bpy.data.collections['Car_LOD1'];c.hide_viewport=False
for n,ratio in [('Mirror_L',.45),('Mirror_R',.45),('Seat_Driver',.8),('Seat_Passenger',.8),('Dashboard',.85),('Floor',.3),('Headliner',.35)]:
 o=bpy.data.objects[n+'_LOD1'];d=o.modifiers.new('Medium visibility budget','DECIMATE');d.ratio=ratio;bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
c.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
