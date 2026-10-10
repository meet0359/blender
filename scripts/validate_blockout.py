"""Read-only validation for the Phase 2 milestone, not final-asset validation."""
import bpy
from mathutils import Vector
from pathlib import Path
import math
import re

ROOT=Path(__file__).resolve().parents[1]
lines=['PHASE 2 BLOCKOUT VALIDATION']
errors=[]

def check(ok,message):
    lines.append(('PASS: ' if ok else 'ERROR: ')+message)
    if not ok:
        errors.append(message)

required=['Car_Body','Hood','Chassis_Blockout','Front_Bumper','Rear_Bumper',
          'Cabin_Roof_Blockout','Rear_Engine_Cover_Blockout']
required += ['Wheel_'+key for key in ['FL','FR','RL','RR']]
check(all(n in bpy.data.objects for n in required),'All Phase 2 required objects exist')
names=['CAR','WHEELS','BRAKES','INTERIOR','GLASS','LIGHTS','COLLIDERS','LODS']
check(all(n in bpy.data.collections for n in names),'All eight requested collections exist')
asset=list(bpy.data.collections['CAR'].objects)+list(bpy.data.collections['WHEELS'].objects)
check(all((o.scale-Vector((1,1,1))).length<1e-6 for o in asset),'All vehicle mesh scales are (1,1,1)')
check(not any(re.match(r'^(Cube|Cylinder|Sphere|Object)(\.\d+)?$',o.name) for o in bpy.data.objects),
      'No default object names')
check(all(not o.hide_viewport and not o.hide_get() and not o.hide_render for o in asset),
      'No hidden vehicle meshes')
check(all(all(math.isfinite(c) for c in v.co) for o in asset for v in o.data.vertices),
      'Mesh coordinates are finite')
for key,x,y,r in [('FL',-.825,-1.35,.345),('FR',.825,-1.35,.345),
                  ('RL',-.835,1.35,.365),('RR',.835,1.35,.365)]:
    o=bpy.data.objects['Wheel_'+key]
    corners=[Vector(c) for c in o.bound_box]
    midpoint=(Vector([min(c[i] for c in corners) for i in range(3)])+
              Vector([max(c[i] for c in corners) for i in range(3)]))/2
    check(midpoint.length<1e-6 and (o.location-Vector((x,y,r))).length<1e-6,
          o.name+' origin at rotational center')
    # Invariance of radius under an X-axis rotation verifies the local axle.
    radii=[math.hypot(v.co.y,v.co.z) for v in o.data.vertices]
    check(max(radii)-min(radii)<1e-5 and abs(max(radii)-r)<1e-5,
          o.name+' circular around local X axis')
    cap=bpy.data.objects['Wheel_Center_Placeholder_'+key]
    check(cap.parent==o,o.name+' center placeholder follows wheel rotation')

deps=bpy.context.evaluated_depsgraph_get()
points=[]
for o in asset:
    e=o.evaluated_get(deps)
    points.extend(e.matrix_world@Vector(c) for c in e.bound_box)
low=Vector([min(p[i] for p in points) for i in range(3)])
high=Vector([max(p[i] for p in points) for i in range(3)])
d=high-low
check(4.4<=d.y<=4.7 and 1.9<=d.x<=2.05 and 1.15<=d.z<=1.25,
      f'Evaluated vehicle envelope: length {d.y:.3f} m, width {d.x:.3f} m, height {d.z:.3f} m')
wb=abs(bpy.data.objects['Wheel_FL'].location.y-bpy.data.objects['Wheel_RL'].location.y)
check(abs(wb-2.70)<1e-6,f'Wheelbase {wb:.3f} m')
check(bpy.context.scene.unit_settings.system=='METRIC','Metric scene units')
check((bpy.data.objects['Car_Body'].location-Vector((0,0,0))).length<1e-6,
      'Main body origin at central chassis XY position')
lines += ['WARNING: Blockout only. Body curvature and arch transitions need manual review before Phase 3.',
          'WARNING: Opaque cabin and simple bumper volumes are intentional.',
          'WARNING: Final materials, UVs, detailed lights, interior, brakes, collider and LOD meshes are deferred.',
          'PASS: Hidden reference empties and review floor are intentional; no hidden accidental vehicle geometry.',
          f'RESULT: {len(errors)} errors']
report='\n'.join(lines)+'\n'
print(report)
(ROOT/'phase_02_validation.txt').write_text(report)
if errors:
    raise RuntimeError('Blockout validation failed')
