import bpy,bmesh
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for o in list(bpy.data.collections['Car_LOD0'].all_objects):
 n=o['source_object']
 if n.startswith(('Caliper_PistonBoss_RL','Caliper_PistonBoss_RR')):bpy.data.objects.remove(o,do_unlink=True);continue
 # Remove isolated collapse edges without changing the visible polygons or loop normals.
 me=o.data;ns=[tuple(n.vector) for n in me.corner_normals];bm=bmesh.new();bm.from_mesh(me);wire=[e for e in bm.edges if e.is_wire]
 if wire:
  bmesh.ops.delete(bm,geom=wire,context='EDGES');bm.to_mesh(me)
  if len(me.loops)==len(ns):me.normals_split_custom_set(ns)
 bm.free()
for img in bpy.data.images:
 if img.source=='FILE' and 'lod_detail_' in img.filepath:img.reload()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
