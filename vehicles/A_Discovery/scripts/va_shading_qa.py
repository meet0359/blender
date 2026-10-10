# Vehicle shading QA (read-only; never saves). Mandatory for every vehicle release from Phase E on.
#   Blender -b --factory-startup --python va_shading_qa.py -- <blend> <out.json>
# For every render mesh under LOD0_Root..LOD3_Root: fraction of loop (corner) normals that deviate > 50 deg from their own face normal ("torn" normals).
# Torn normals are what transferred / smeared normals on decimated or creased geometry look like in a render (chrome tears, blotches, silvery carbon).
# Calibration (2026-10-08, confirmed visually with close-up and gameplay-distance renders):
#   BAD  Titan GT original Body_LOD1 11.9 %, Trim_LOD1 26.6 %;  Vortex R Trim_LOD1 23.0 %;  Raven XR scratch Lights_LOD1 9.8 %, Interior_LOD1 3.5 %
#   GOOD Titan GT r1 0 %;  Raven XR final <= 0.09 %;  LOD0 bodies with real cut edges 0.03 - 0.12 %
# Verdict per mesh: FAIL > 1 %, WARN > 0.3 %, else PASS. The number is a screen, not the final word: confirm visually (LOD close-up + chase renders).
import bpy, sys, json, math
a = sys.argv[sys.argv.index('--') + 1:]; SRC, OUT = a[0], a[1]
bpy.ops.wm.open_mainfile(filepath=SRC); O = bpy.data.objects
FAIL, WARN, LIM = 1.0, 0.3, math.radians(50)
def lod_of(o):
    p = o
    while p:
        if p.name.startswith('LOD') and p.name.endswith('_Root'): return int(p.name[3])
        p = p.parent
    return None
def tear(o):
    me = o.data; cn = me.corner_normals; bad = tot = 0
    for p in me.polygons:
        if p.area < 2e-6: continue
        for li in p.loop_indices:
            tot += 1; bad += cn[li].vector.angle(p.normal, 0) > LIM
    return round(100.0 * bad / max(tot, 1), 3), tot
res = {}
for o in sorted(O, key=lambda o: o.name):
    k = lod_of(o)
    if o.type != 'MESH' or k is None or o.name.startswith('Collision'): continue
    pct, n = tear(o); res[o.name] = dict(lod=k, torn_pct=pct, loops=n, verdict='FAIL' if pct > FAIL else 'WARN' if pct > WARN else 'PASS')
summ = {v: sum(1 for r in res.values() if r['verdict'] == v) for v in ('PASS', 'WARN', 'FAIL')}
json.dump(dict(source=SRC, thresholds=dict(fail_pct=FAIL, warn_pct=WARN, angle_deg=50), summary=summ, meshes=res), open(OUT, 'w'), indent=1)
for n, r in res.items():
    if r['verdict'] != 'PASS': print('QA', r['verdict'], n, r['torn_pct'], flush=True)
print('SHADING_QA', summ, flush=True)
