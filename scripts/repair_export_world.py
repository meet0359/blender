import bpy,json,hashlib
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[1];d=json.loads((R/'export_geometry_source.json').read_text())
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=False
bpy.context.view_layer.update()
# Restore parent transforms first, then descendants, from the unchanged source snapshot.
objects=[bpy.data.objects[n] for n in d]
def depth(o):return 0 if o.parent is None else 1+depth(o.parent)
for o in sorted(objects,key=depth):
 o.matrix_world=Matrix(d[o.name]['matrix_world']);bpy.context.view_layer.update()
bpy.context.scene['source_07_sha256']=hashlib.sha256((R/'racing_car_07_optimized_lods.blend').read_bytes()).hexdigest()
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=i!=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_08_export_ready.blend'))
