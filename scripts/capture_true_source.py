import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];d=json.loads((R/'export_geometry_source.json').read_text())
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=False
bpy.context.view_layer.update()
for n,v in d.items():v['matrix_world']=[list(a) for a in bpy.data.objects[n].matrix_world]
(R/'export_geometry_source.json').write_text(json.dumps(d,indent=2))
print('TRUE SOURCE WHEELS',[(o.name,list(o.matrix_world.translation)) for o in bpy.data.objects if o.name.startswith('Wheel_FL_LOD')]);print('SOURCE SHA',hashlib.sha256((R/'racing_car_07_optimized_lods.blend').read_bytes()).hexdigest())
