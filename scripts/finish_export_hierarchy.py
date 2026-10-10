import bpy
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[1]
for lod in range(4):
 for o in list(bpy.data.collections['Car_LOD'+str(lod)].all_objects):
  n=o['source_object']
  if n.startswith(('BrakeDisc_','Brake_Hat_','Brake_Radial_Slot_')):
   key=next(k for k in ['FL','FR','RL','RR'] if '_'+k in n);mw=o.matrix_world.copy();o.parent=bpy.data.objects['Wheel_'+key+'_LOD'+str(lod)];o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_world=mw;o['rotation_policy']='Rolls with wheel; caliper remains fixed'
  elif n.startswith('Caliper_'):o['rotation_policy']='Fixed to chassis; does not roll with wheel'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_08_export_ready.blend'))
