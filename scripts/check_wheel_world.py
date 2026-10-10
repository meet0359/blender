import bpy,json
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=False
bpy.context.view_layer.update()
for i in range(4):
 for k in ['FL','FR','RL','RR']:
  o=bpy.data.objects['Wheel_'+k+'_LOD'+str(i)];print(o.name,list(o.matrix_world.translation),list(o.location),list(o.parent.matrix_world.translation) if o.parent else None)
