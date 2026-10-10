import bpy,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
R=Path(__file__).resolve().parents[1];master=bpy.data.collections['REFERENCE_Master_06'];master.hide_viewport=False
cache={}
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];col.hide_viewport=False;bpy.context.view_layer.update()
 for oi,o in enumerate(list(col.all_objects)):
  if o.get('intentional_open_surface') or o['source_object'].startswith('Wheel_Well_') or o.get('far_tire'):continue
  src=bpy.data.objects[o['source_object']]
  if src.name not in cache:
   dg=bpy.context.evaluated_depsgraph_get();me=bpy.data.meshes.new_from_object(src.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);me.calc_loop_triangles()
   vs=[v.co.copy() for v in me.vertices];ts=[tuple(t.vertices) for t in me.loop_triangles];norm=[n.vector.copy() for n in me.corner_normals];tn=[t.normal.copy() for t in me.loop_triangles];loops=[tuple(t.loops) for t in me.loop_triangles];tree=BVHTree.FromPolygons(vs,ts,all_triangles=True);cache[src.name]=(vs,ts,norm,tn,loops,tree)
  vs,ts,norm,tn,loops,tree=cache[src.name];low=o.data;result=[(0,0,0)]*len(low.loops)
  for p in low.polygons:
   for li in p.loop_indices:
    pos=low.vertices[low.loops[li].vertex_index].co;hit=tree.find_nearest(pos)
    if hit[0] is None:continue
    if tn[hit[2]].dot(p.normal)<.25:
     options=[h for h in tree.find_nearest_range(pos,max(.008,hit[3]*3)) if tn[h[2]].dot(p.normal)>.25]
     if options:hit=min(options,key=lambda h:h[3])
    pt,_,idx,dist=hit;a,b,c=ts[idx];l0,l1,l2=loops[idx];n=barycentric_transform(pt,vs[a],vs[b],vs[c],norm[l0],norm[l1],norm[l2]);n.normalize();result[li]=tuple(n)
  low.normals_split_custom_set(result);low.update()
  if oi%100==0:print('NORMALS',lod,oi,flush=True)
 col.hide_viewport=lod!=0
master.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
