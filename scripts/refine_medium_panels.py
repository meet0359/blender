import bpy,math
from pathlib import Path
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parents[1];bpy.data.collections['REFERENCE_Master_06'].hide_viewport=False

def ev(o):
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();return bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
def rep(o,me):
 old=o.data;o.data=me;bpy.data.meshes.remove(old)
col=bpy.data.collections['Car_LOD1'];col.hide_viewport=False
for o in list(col.all_objects):
 if o['lod_category']!='Body':continue
 name=o['source_object'];src=bpy.data.objects[name]
 # Reuse the validated hero exterior skin. Preserve the touching nose/hood panels exactly.
 hero=bpy.data.objects[name+'_LOD0'];me=hero.data.copy();tree=KDTree(len(me.vertices));norms=[v.normal.copy() for v in me.vertices]
 # Hero custom corner normals are the reference at each surviving vertex.
 for p in me.polygons:
  for l in p.loop_indices:norms[me.loops[l].vertex_index]=me.corner_normals[l].vector.copy()
 for v in me.vertices:tree.insert(v.co,v.index)
 tree.balance();rep(o,me)
 if name not in ['Front_Bumper','Hood','Rear_Bumper']:
  d=o.modifiers.new('Medium distance curvature reduction','DECIMATE');d.decimate_type='DISSOLVE';d.angle_limit=math.radians(2.2 if name=='Car_Body' else 3.0);d.delimit={'UV','SEAM','MATERIAL'};me=ev(o);o.modifiers.clear();rep(o,me)
 me.normals_split_custom_set([tuple(norms[tree.find(me.vertices[l.vertex_index].co)[1]]) for l in me.loops]);o['intentional_open_surface']='Master exterior skin and perimeter; inner duplicate surfaces removed'
 me.calc_loop_triangles();print(name,len(me.loop_triangles),flush=True)
col.hide_viewport=True
# One shared thin-glass variant for all LODs: straight transmission plus Fresnel reflection.
m=bpy.data.materials.get('MAT_Glass_LOD_Thin') or bpy.data.materials.new('MAT_Glass_LOD_Thin');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();lk=m.node_tree.links
trans=ns.new('ShaderNodeBsdfTransparent');trans.inputs[0].default_value=(.83,.91,.95,1)
reflect=ns.new('ShaderNodeBsdfPrincipled');reflect.inputs['Base Color'].default_value=(.8,.9,.95,1);reflect.inputs['Metallic'].default_value=1;reflect.inputs['Roughness'].default_value=.025
fr=ns.new('ShaderNodeFresnel');fr.inputs['IOR'].default_value=1.46
mix=ns.new('ShaderNodeMixShader');lk.new(fr.outputs[0],mix.inputs[0]);lk.new(trans.outputs[0],mix.inputs[1]);lk.new(reflect.outputs[0],mix.inputs[2]);out=ns.new('ShaderNodeOutputMaterial');lk.new(mix.outputs[0],out.inputs['Surface'])
m['purpose']='Shared game thin-glass approximation; Fresnel 1.46, straight transmission, avoids thin-shell refraction distortion'
for lod in range(4):
 for o in bpy.data.collections['Car_LOD'+str(lod)].all_objects:
  if o.get('glass_lod_policy'):
   for slot in o.material_slots:
    if slot.material.name=='MAT_Glass':slot.material=m
bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
