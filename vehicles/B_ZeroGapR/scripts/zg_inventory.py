# Phase B: per-part inventory of the Zero Gap R source (read-only). Writes reports/ZG_source_inventory.json
import sys; sys.dont_write_bytecode = True
import bpy, os, re, json
from mathutils import Vector
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath='/Users/meetshah/Documents/blender/racing_car_09_unity_export_ready.blend')
dg = bpy.context.evaluated_depsgraph_get(); out = {}
for c in bpy.data.collections:
    m = re.match(r'LOD(\d)_(\w+)', c.name)
    if not m: continue
    for o in c.objects:
        if o.type not in ('MESH', 'CURVE'): continue
        ev = o.evaluated_get(dg); me = ev.to_mesh(); me.calc_loop_triangles()
        pts = [o.matrix_world @ Vector(b) for b in o.bound_box]
        out[o.name] = dict(lod=int(m.group(1)), cat=m.group(2), type=o.type, tris=len(me.loop_triangles), mats=[s.material.name if s.material else None for s in o.material_slots],
                           uv=[u.name for u in o.data.uv_layers] if o.type == 'MESH' else [], parent=o.parent.name if o.parent else None,
                           loc=[round(v, 3) for v in o.matrix_world.translation], bmin=[round(min(p[i] for p in pts), 3) for i in range(3)], bmax=[round(max(p[i] for p in pts), 3) for i in range(3)])
        ev.to_mesh_clear()
json.dump(out, open(os.path.join(HERE, 'reports', 'ZG_source_inventory.json'), 'w'), indent=0)
from collections import defaultdict
agg = defaultdict(lambda: [0, 0])
for n, d in out.items(): agg[(d['lod'], d['cat'])][0] += 1; agg[(d['lod'], d['cat'])][1] += d['tris']
for k in sorted(agg): print('CAT', k, agg[k])
for n, d in sorted(out.items(), key=lambda x: -x[1]['tris']):
    if d['lod'] == 0 and d['cat'] in ('Body', 'Aero_Trim', 'Lights', 'Glass'): print('L0', d['cat'], n, d['tris'], d['mats'], d['bmin'], d['bmax'], d['uv'])
