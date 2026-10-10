import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
o=bpy.data.objects['RearBulkhead']
for v in o.data.vertices: v.co.x*=1.16/1.31
o.data.update()
for name in ['InnerSill_L','InnerSill_R']:
    o=bpy.data.objects[name]
    for v in o.data.vertices: v.co.y*=1.30/1.46
    o.location.y=-.21; o.data.update()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_05_interior.blend'))
