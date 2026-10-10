# Basic design-blockout validation (read-only): measured dimensions, wheel placement, clearance, triangle counts, mesh sanity.
#   Blender -b --factory-startup --python ts_blockout_check.py -- <blockout.blend> <out.json> [<blockout_stats.json>: + dimensions vs design DIM]
import bpy, bmesh, sys, json, math
a = sys.argv[sys.argv.index('--') + 1:]; bpy.ops.wm.open_mainfile(filepath=a[0]); O = bpy.data.objects
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons)
meshes = [o for o in O if o.type == 'MESH']; body = O.get('Body_Blockout'); R = {'file': a[0].split('/')[-1], 'checks': {}}
V = [body.matrix_world @ v.co for v in body.data.vertices]
R['length_m'] = round(max(v.y for v in V) - min(v.y for v in V), 3)
R['width_body_m'] = round(2 * max(abs(v.x) for v in V if .45 < v.z < .85), 3)                         # side slice below the mirrors
R['width_mirrors_m'] = round(2 * max(abs(v.x) for v in V), 3)
R['roof_height_m'] = round(max(v.z for v in V if abs(v.x) > .06), 3); R['height_incl_fin_m'] = round(max(v.z for v in V), 3)
R['body_min_z_m'] = round(min(v.z for v in V), 3)
W = {c: O.get(f'Wheel_{c}_LOD0') for c in ('FL', 'FR', 'RL', 'RR')}
ok_w = all(W.values()); R['checks']['four_wheels'] = ok_w
if ok_w:
    org = {c: W[c].matrix_world.translation for c in W}; R['wheelbase_m'] = round(org['RL'].y - org['FL'].y, 3)
    R['track_f_m'] = round(org['FL'].x - org['FR'].x, 3); R['track_r_m'] = round(org['RL'].x - org['RR'].x, 3)
    wz = [min((W[c].matrix_world @ v.co).z for v in W[c].data.vertices) for c in W]; R['tire_radius_m'] = round(max((W['FL'].matrix_world @ v.co).z for v in W['FL'].data.vertices) / 2, 3)
    R['checks']['tires_on_ground (<5 mm)'] = all(abs(z) < .005 for z in wz)
    R['front_overhang_m'] = round(org['FL'].y - min(v.y for v in V), 3); R['rear_overhang_m'] = round(max(v.y for v in V) - org['RL'].y, 3)
R['checks']['body_clearance >= 0.12 m'] = R['body_min_z_m'] >= .12
R['tris'] = {o.name: tris(o) for o in meshes}; R['tris_total'] = sum(R['tris'].values()); R['tris_without_master_body'] = R['tris_total'] - tris(body)
bad = {}
for o in meshes:
    bm = bmesh.new(); bm.from_mesh(o.data)
    za = sum(1 for f in bm.faces if f.calc_area() < 1e-10); lv = sum(1 for v in bm.verts if not v.link_faces); nan = sum(1 for v in bm.verts if any(math.isnan(c) for c in v.co)); bm.free()
    if za or lv or nan: bad[o.name] = dict(zero_area=za, loose=lv, nan=nan)
R['mesh_issues'] = bad; R['checks']['no NaN / loose vertices'] = not any(v['nan'] or v['loose'] for v in bad.values())
R['checks']['glass, lights, trim, interior present'] = all(any(o.name.startswith(p) for o in meshes) for p in ('Glass', 'Lights', 'Trim', 'Interior'))
bx = lambda o: [o.matrix_world @ Vector(c) for c in o.bound_box]
from mathutils import Vector
BX, BY, BZ = max(abs(v.x) for v in V), (min(v.y for v in V), max(v.y for v in V)), max(v.z for v in V)
if len(a) > 2: BZ = max(BZ, json.load(open(a[2]))['DIM'].get('height_incl_hvac', 0))   # declared roof equipment (bus HVAC) is not stray
out_ = {o.name: round(max(max(abs(p.x) - BX, BY[0] - p.y, p.y - BY[1], p.z - BZ) for p in bx(o)), 3) for o in meshes if o is not body and not o.name.startswith(('Wheel', 'Caliper', 'Collision'))}
R['parts_outside_body_bounds_m'] = {k: v for k, v in out_.items() if v > .10}; R['checks']['no part > 10 cm outside the body bounds (stray / floating trim; bumpers may be proud)'] = not R['parts_outside_body_bounds_m']
if len(a) > 2:
    D = json.load(open(a[2]))['DIM']; R['design_dim'] = D
    dev = {'length': R['length_m'] - D['length'], 'width_body': R['width_body_m'] - D['width_body'], 'height': R['roof_height_m'] - D['height']}
    R['dim_deviation_m'] = {k: round(v, 3) for k, v in dev.items()}; R['checks']['dimensions within 6 cm of the design'] = all(abs(v) <= .06 for v in dev.values())
R['materials'] = sorted({m.name for o in meshes for m in o.data.materials if m})
R['PASS'] = all(R['checks'].values())
json.dump(R, open(a[1], 'w'), indent=1); print('BLOCKOUT CHECK', 'PASS' if R['PASS'] else 'FAIL', json.dumps({k: R[k] for k in ('length_m', 'width_body_m', 'roof_height_m', 'wheelbase_m', 'tire_radius_m', 'body_min_z_m', 'tris_without_master_body')}), R['checks'])
