import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
for i in range(4):
 for o in bpy.data.collections['Car_LOD'+str(i)].all_objects:
  m=o.data;m.calc_loop_triangles();zero=[t for t in m.loop_triangles if (m.vertices[t.vertices[1]].co-m.vertices[t.vertices[0]].co).cross(m.vertices[t.vertices[2]].co-m.vertices[t.vertices[0]].co).length<1e-12]
  if zero:print(o.name,'TRIS',len(m.loop_triangles),'ZERO',len(zero),flush=True)
