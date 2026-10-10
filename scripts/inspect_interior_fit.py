import bpy,json
from mathutils import Vector
from pathlib import Path
s=bpy.context.scene; dg=bpy.context.evaluated_depsgraph_get()
names=[o.name for o in bpy.data.collections['INTERIOR'].all_objects]+['Car_Body','Car_Door_L','Car_Door_R','Roof_Panel','Windshield','Rear_Glass','Window_FL','Window_FR','Window_RL','Window_RR']
data={}
for name in names:
 o=bpy.data.objects[name]; e=o.evaluated_get(dg)
 corners=[e.matrix_world@Vector(p) for p in e.bound_box]
 data[name]={'type':o.type,'location':list(o.location),'bounds':[[min(p[i] for p in corners) for i in range(3)],[max(p[i] for p in corners) for i in range(3)]],'materials':[m.name if m else None for m in o.data.materials] if o.type=='MESH' else [],'modifiers':[(m.name,m.type) for m in o.modifiers]}
print(json.dumps(data,indent=2))
(Path(__file__).resolve().parents[1]/'interior_source_fit.json').write_text(json.dumps(data,indent=2))
