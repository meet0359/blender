import bpy,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.data.collections['REFERENCE_Master_06'].hide_viewport=False
col=bpy.data.collections['Car_LOD0'];col.hide_viewport=False

def ev(o):
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();return bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
def replace(o,me):
 old=o.data;o.data=me;bpy.data.meshes.remove(old)
for o in list(col.all_objects):
 n=o['source_object'];c=o['lod_category'];src=bpy.data.objects[n]
 if c=='Glass':
  mods=[m for m in src.modifiers if m.type=='SOLIDIFY']
  for m in mods:m.show_viewport=False
  me=ev(src)
  for m in mods:m.show_viewport=True
  replace(o,me);d=o.modifiers.new('Glass curvature angle budget','DECIMATE');d.decimate_type='DISSOLVE';d.angle_limit=math.radians(1.8);d.delimit={'MATERIAL','UV','SEAM'};me=ev(o);o.modifiers.clear();replace(o,me)
  for m in mods:
   so=o.modifiers.new('Optical glass thickness','SOLIDIFY');so.thickness=m.thickness;so.offset=m.offset;so.use_even_offset=m.use_even_offset
  me=ev(o);o.modifiers.clear();replace(o,me)
 else:
  ratio=.35 if n in ['Mirror_L','Mirror_R'] else {'Interior':.70,'Aero_Trim':.70,'Wheels':.8,'Tires':.85,'Brakes':.9}.get(c,1)
  if n.startswith(('Wheel_Well','Front_Intake_Grille')):ratio=1
  if ratio==1:continue
  o.data.calc_loop_triangles()
  if len(o.data.loop_triangles)<80:continue
  d=o.modifiers.new('Secondary component budget after exterior restoration','DECIMATE');d.ratio=ratio;me=ev(o);o.modifiers.clear();replace(o,me)
 o.data.calc_loop_triangles()
counts={}
for o in col.all_objects:o.data.calc_loop_triangles();c=o['lod_category'];counts[c]=counts.get(c,0)+len(o.data.loop_triangles)
print('LOD0 BALANCED',counts,sum(counts.values()),flush=True)
bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
