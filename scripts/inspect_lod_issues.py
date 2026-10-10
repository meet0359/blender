import bpy
from mathutils import Vector
for i in range(4):
 col=bpy.data.collections['Car_LOD'+str(i)];col.hide_viewport=False;bpy.context.view_layer.update()
 for ax in range(3):
  rows=[( (o.matrix_world@v.co)[ax],o.name) for o in col.all_objects for v in o.data.vertices]
  print(i,ax,min(rows),max(rows))
 for n in ['Front_Intake_Grille','Wheel_Well_FL']:
  o=bpy.data.objects[n+'_LOD'+str(i)];o.data.calc_loop_triangles();print(o.name,len(o.data.loop_triangles))
