import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=4;S.render.bake.use_selected_to_active=True;S.render.bake.use_clear=True;S.render.bake.margin=6;S.render.bake.cage_extrusion=.025;S.render.bake.max_ray_distance=.05;S.render.bake.normal_space='TANGENT'
pairs=[('Dashboard',['Dashboard_Seam_-1','Dashboard_Seam_1']),('CenterConsole',['Console_Red_Seam_-1','Console_Red_Seam_1'])]
for label in ['L','R']:pairs.append(('DoorPanel_'+label,['DoorPanel_'+label+'_Seam']))
for label in ['Driver','Passenger']:
 pairs.append(('Seat_'+label+'_BackrestPad',['Seat_'+label+'_PadDivision_'+str(i) for i in range(3)]))
 pairs.append(('Seat_'+label+'_Cushion',['Seat_'+label+'_CushionSeam_'+str(i) for i in [-1,1]]))
 for i in [-1,1]:pairs.append(('Seat_'+label+'_Bolster_'+str(i),['Seat_'+label+'_BackrestSeam_'+str(i)]))
img=bpy.data.images.new('Isolated_Seam_Normal',4096,4096,alpha=False);img.colorspace_settings.name='Non-Color'
mat=bpy.data.materials.new('Bake_Target');mat.use_nodes=True;nd=mat.node_tree.nodes.new('ShaderNodeTexImage');nd.image=img;mat.node_tree.nodes.active=nd
for name,details in pairs:
 src=bpy.data.objects[name];state=[]
 for m in src.modifiers:
  if m.type=='SOLIDIFY':state.append((m,m.show_viewport));m.show_viewport=False
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(src.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
 for m,v in state:m.show_viewport=v
 high=bpy.data.objects.new('High_Canonical',me);S.collection.objects.link(high);high.matrix_world=src.matrix_world
 low=bpy.data.objects.new('Low_Canonical',me.copy());S.collection.objects.link(low);low.matrix_world=src.matrix_world;low.data.materials.clear();low.data.materials.append(mat)
 for p in low.data.polygons:p.material_index=0
 bpy.ops.object.select_all(action='DESELECT');high.select_set(True);low.select_set(True)
 for dn in details:bpy.data.objects[dn].select_set(True)
 bpy.context.view_layer.objects.active=low;print('ISOLATED SEAMS',name,flush=True);bpy.ops.object.bake(type='NORMAL');S.render.bake.use_clear=False
 for o in [low,high]:
  data=o.data;bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(data)
img.filepath_raw=str(R/'textures/racing_car/interior/lod_detail_Normal.png');img.file_format='PNG';img.save();print('ISOLATED SEAM BAKE COMPLETE',flush=True)
