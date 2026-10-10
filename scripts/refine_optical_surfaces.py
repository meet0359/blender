import bpy,math
from pathlib import Path
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parents[1];bpy.data.collections['REFERENCE_Master_06'].hide_viewport=False

def ev(o):
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();return bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
def rep(o,me):
 old=o.data;o.data=me;bpy.data.meshes.remove(old)
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];col.hide_viewport=False
 for o in list(col.all_objects):
  name=o['source_object'];src=bpy.data.objects[name]
  if o['lod_category']!='Glass' or name.startswith('Mirror_'):continue
  solid=[m for m in src.modifiers if m.type=='SOLIDIFY']
  for m in solid:m.show_viewport=False
  me=ev(src)
  for m in solid:m.show_viewport=True
  norms=[v.normal.copy() for v in me.vertices];tree=KDTree(len(me.vertices))
  for v in me.vertices:tree.insert(v.co,v.index)
  tree.balance();rep(o,me)
  d=o.modifiers.new('Optical surface simplification','DECIMATE');d.decimate_type='DISSOLVE';d.angle_limit=math.radians([1.8,3,5,10][lod]);d.delimit={'UV','SEAM','MATERIAL'}
  me=ev(o);o.modifiers.clear();rep(o,me)
  normal=[tuple(norms[tree.find(me.vertices[l.vertex_index].co)[1]]) for l in me.loops];me.normals_split_custom_set(normal)
  # Thin optical sheets avoid folding a second close parallel refraction surface.
  o['intentional_open_surface']='Optical glass sheet, smooth source normals; edge trim provides perimeter'
  o['glass_lod_policy']='Single smooth transmissive sheet, shared glass shader, no intersecting back skin'
  me.calc_loop_triangles();print(o.name,len(me.loop_triangles),flush=True)
 col.hide_viewport=lod!=0
bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
