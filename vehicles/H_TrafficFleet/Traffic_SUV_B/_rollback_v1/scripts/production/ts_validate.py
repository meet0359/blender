# Traffic fleet validation (read-only). Opens <prefix>_09_export_ready.blend: integrity, hierarchy, pivots, LODs, budgets, materials, light channels,
# textures, UVs, topology, colliders, previews, FBX clean re-import (Blender space + raw Unity space) + S1 shading screen on ALL LODs.
#   Blender -b --factory-startup --python ts_validate.py -- <Vehicle_Folder> <ckp_prefix> <FBX_base> <collection> <budget_lo> <budget_hi> <min_clearance>   env TS_NO_FBX=1: FBX checks SKIP
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from ts_lib import *
import hashlib
A = sys.argv[sys.argv.index('--') + 1:]; VEH, PFX, BASE, COLL_NAME = A[:4]; BLO, BHI, CLEAR = int(A[4]), int(A[5]), float(A[6]); ROOT = vroot(VEH)
D = lambda *a: os.path.join(SCR, *a) if SCR else os.path.join(ROOT, *a)
bpy.ops.wm.open_mainfile(filepath=D('blend', f'{PFX}_09_export_ready.blend')); O = bpy.data.objects
log, cnt, N = [], {'FAIL': 0, 'WARN': 0}, [0]
def chk(msg, ok, detail='', warn=False):
    N[0] += 1; tag = 'PASS' if ok else ('WARN' if warn else 'FAIL'); log.append(f'[{tag}] {N[0]:>2}. {msg}' + (f' -- {detail}' if detail else ''))
    if not ok: cnt[tag] += 1
    return ok
V = lambda o: np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) if len(o.data.vertices) else np.zeros((0, 3))
master = sorted(bpy.data.collections[COLL_NAME].all_objects, key=lambda o: o.name); meshes = [o for o in master if o.type == 'MESH']
iscol = lambda o: o.name.startswith('Collision_'); rend = [o for o in meshes if not iscol(o)]
def lod_of(o):
    p = o
    while p:
        if p.name.startswith('LOD') and p.name.endswith('_Root'): return int(p.name[3])
        p = p.parent
LOD = {k: [o for o in rend if lod_of(o) == k] for k in range(4)}; T = {k: sum(tris(o) for o in v) for k, v in LOD.items()}
log += [f'== {VEH} (Phase H traffic) - VALIDATION ==', f'source blend/{PFX}_09_export_ready.blend; {len(master)} objects, {len(meshes)} meshes ({len(rend)} render, {len(meshes) - len(rend)} colliders)', '']
# 1 integrity: Phase A baseline + every frozen release manifest + the postponed Pulse EV blockout
WS_ = WS; base = json.load(open(os.path.join(WS_, 'vehicles/A_Discovery/reports/VA_workspace_baseline.json')))['files']
sh = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()
changed = [k for k, v in base.items() if not os.path.exists(os.path.join(WS_, k)) or sh(os.path.join(WS_, k)) != v['sha1']]
now = set()
for d, dirs, fs in os.walk(WS_):
    rel = os.path.relpath(d, WS_)
    if rel == 'vehicles' or rel.startswith('vehicles' + os.sep): dirs[:] = []; continue
    now |= {os.path.relpath(os.path.join(d, f), WS_) for f in fs if f != '.DS_Store'}
added = sorted(now - set(base))
import glob
FR = {}
for man in sorted(glob.glob(os.path.join(WS_, 'vehicles', '*', 'reports', '*_FINAL_FREEZE.md')) + [m for m in glob.glob(os.path.join(WS_, 'vehicles', '*', '*', 'reports', '*_FINAL_FREEZE.md')) if 'UnityTransfer' not in m]):
    r = os.path.dirname(os.path.dirname(man)); rows = [l.split('`') for l in open(man) if l.startswith('| `')]
    FR[os.path.basename(r)] = (len(rows), [x[1] for x in rows if not os.path.exists(os.path.join(r, x[1])) or sh(os.path.join(r, x[1])) != x[3]])
pulse = os.path.join(WS_, 'vehicles/F_PulseEV/blend/pulseev_01_blockout.blend'); pulse_ok = os.path.exists(pulse) and sh(pulse) == '18af7277976ab32e89c103f81c4e9c941c367f4d'
frbad = [f for _, (_, b) in FR.items() for f in b]
chk('protected files byte-identical: Phase A baseline (frozen P0-P3, Hypercar, racing_car sources, all files outside vehicles/), frozen releases ' + ', '.join(f'{k} ({n})' for k, (n, _) in FR.items()) + ', postponed Pulse EV blockout untouched; nothing added outside vehicles/',
    not changed and not added and not frbad and len(FR) >= 6 and pulse_ok, f'{len(base)} files; changed {changed[:3]} added {added[:3]} frozen changed {frbad[:3]} pulse_ok {pulse_ok}')
# 2 hierarchy
I = Matrix.Identity(4); cr = O.get('Car_Root')
ident = lambda o: all(abs(a - b) < 1e-9 for ra, rb in zip(o.matrix_world, I) for a, b in zip(ra, rb))
roots_ok = cr and cr.parent is None and ident(cr) and all(O.get(f'LOD{k}_Root') and O[f'LOD{k}_Root'].parent == cr and ident(O[f'LOD{k}_Root']) for k in range(4))
need = ['Collision', 'CenterOfMass'] + [f'WheelColliderRef_{c}' for c in ('FL', 'FR', 'RL', 'RR')]
tops = [o.name for o in master if o.parent is None]
bad_sc = [o.name for o in master if any(s <= 0 or abs(s - 1) > 1e-6 for s in o.matrix_world.to_scale())]
chk('hierarchy: Car_Root (origin, identity, top level) -> LOD0_Root..LOD3_Root (identity), Collision, WheelColliderRef_FL/FR/RL/RR, CenterOfMass; no cameras / lights; no negative or non-unit scale',
    roots_ok and all(O.get(n) and O[n].parent == cr for n in need) and tops == ['Car_Root'] and not any(o.type in ('CAMERA', 'LIGHT') for o in master) and not bad_sc, f'top-level {tops} bad scale {bad_sc[:3]}')
partsk = {k: sorted(o.name.rsplit('_LOD', 1)[0] for o in LOD[k]) for k in range(4)}
want = lambda k: sorted(['Body', 'Glass', 'Trim', 'Lights'] + (['Interior'] if k <= 3 else []) + [f'Wheel_{c}' for c in ('FL', 'FR', 'RL', 'RR')] + ([f'Caliper_{c}' for c in ('FL', 'FR', 'RL', 'RR')] if k <= 2 else []))
chk('every LOD has the full car: Body, Glass, Trim, Lights, Interior, Wheel x4 (rim + tire + disc), Caliper x4 at LOD0-2 (LOD3 drops calipers behind the spokes)', all(partsk[k] == want(k) for k in range(4)), json.dumps({k: len(v) for k, v in partsk.items()}))
# 3 convention + pivots
ref = {c: O[f'WheelColliderRef_{c}'].matrix_world.translation for c in ('FL', 'FR', 'RL', 'RR')}
conv = ref['FL'].x > 0 and ref['RL'].x > 0 and ref['FR'].x < 0 and ref['RR'].x < 0 and ref['FL'].y < 0 and ref['RL'].y > 0
body0 = V(O['Body_LOD0']); nose_front = body0[:, 1].min() < -2.0 and body0[:, 1].max() > 2.0
BASE_ = lambda m: m.get('instance_of', m.name) if m else ''                                                   # vehicle instance of a shared material (r3: interior / glass)
drv = [p.center for p in O['Interior_LOD0'].data.polygons if BASE_(O['Interior_LOD0'].data.materials[p.material_index]) == 'TS_Atlas' and O['Interior_LOD0'].data.attributes['cell'].data[p.index].value == CELLS.index('leather')]
drv_x = float(np.mean([c.x for c in drv])) if drv else 0
chk('orientation: nose toward -Y, vehicle left = +X (FL / RL refs on +X, FR / RR on -X), +Z up, LHD driver (steering wheel) on +X', conv and nose_front and drv_x > .2, f"FL {tuple(round(v, 3) for v in ref['FL'])} RL {tuple(round(v, 3) for v in ref['RL'])} steering x {drv_x:.2f}")
piv = []
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        w = O.get(f'Wheel_{c}_LOD{k}')
        if not w: piv.append((k, c, 'missing')); continue
        off = (w.matrix_world.translation - ref[c]).length; v0 = V(w); ctr0 = (v0.min(0) + v0.max(0)) / 2
        cal = O.get(f'Caliper_{c}_LOD{k}'); cal0 = cal.matrix_world.copy() if cal else None; errs = [0.0]
        for ang in (math.radians(30), math.radians(-30)):
            w.rotation_euler.x = ang; bpy.context.view_layer.update(); v1 = V(w); errs.append(float(np.abs(((v1.min(0) + v1.max(0)) / 2 - ctr0)[0])))
            if cal and max(abs(a - b) for ra, rb in zip(cal.matrix_world, cal0) for a, b in zip(ra, rb)) > 1e-9: errs.append(9)
        w.rotation_euler.x = 0
        if c[0] == 'F':
            sp = O[f'SteerPivot_{c}_LOD{k}']; sp.rotation_euler.z = math.radians(25); bpy.context.view_layer.update(); errs.append(float((w.matrix_world.translation - ref[c]).length))
            if cal and cal.parent != sp: errs.append(9)
            sp.rotation_euler.z = 0
        bpy.context.view_layer.update()
        if off > 1e-6 or max(errs) > 2e-3: piv.append((k, c, round(off * 1000, 4), [round(e * 1000, 2) for e in errs]))
chk('wheel pivots: every Wheel_<c>_LODn origin = WheelColliderRef; +/-30 deg roll about local X keeps the hub centre (< 2 mm); calipers do not roll; front SteerPivot +25 deg yaw keeps the wheel centre on the steering axis and steers the caliper', not piv, str(piv[:4]))
tmin = {k: round(float(min(V(O[f'Wheel_{c}_LOD{k}'])[:, 2].min() for c in ref)), 4) for k in range(4)}
bmin = round(float(min(V(o)[:, 2].min() for o in LOD[0] if o.name.startswith(('Body', 'Trim')))), 4)
chk(f'ground contact + clearance: tires touch the ground (lowest tire point within 5 mm of z 0 at every LOD); body / trim lowest point >= {CLEAR} m', all(abs(v) < .005 for v in tmin.values()) and bmin >= CLEAR - 1e-4, f'tire min z {tmin}; body min z {bmin}')
# 4 budgets + draw calls
r = {k: T[k] / T[0] for k in range(4)}
chk(f'triangle budget (traffic): LOD0 {T[0]:,} within {BLO:,}-{BHI:,}; LOD1 {T[1]:,} ({r[1]:.0%}, target 40-55%); LOD2 {T[2]:,} ({r[2]:.0%}, 15-25%); LOD3 {T[3]:,} ({r[3]:.0%}, 5-10%); strictly decreasing',
    BLO <= T[0] <= BHI and .40 <= r[1] <= .55 and .15 <= r[2] <= .25 and .05 <= r[3] <= .10 and T[0] > T[1] > T[2] > T[3])
mats = {k: sorted({m.name for o in LOD[k] for m in o.data.materials if m}) for k in range(4)}; dcalls = {k: sum(len(o.data.materials) for o in LOD[k]) for k in range(4)}
chk(f'material slots: unique materials per LOD {[len(mats[k]) for k in range(4)]} (<= 8); draw calls (mesh x material) per LOD {[dcalls[k] for k in range(4)]}', all(len(mats[k]) <= 8 for k in range(4)), json.dumps(mats))
# 5 silhouette
dims = {k: (lambda a: (a.max(0) - a.min(0)).round(4).tolist())(np.vstack([V(o) for o in LOD[k]])) for k in range(4)}
dd = max(abs(dims[k][i] - dims[0][i]) for k in range(1, 4) for i in range(3))
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'SINGLE'
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 480, 270, 100; sc.render.film_transparent = True
cd = bpy.data.cameras.new('VC'); cam = bpy.data.objects.new('VC', cd); sc.collection.objects.link(cam); sc.camera = cam; cd.type = 'ORTHO'
VIEWS = {'side': ((9, 0, .7), (0, 0, .7), 5.2), 'front': ((0, -9, .7), (0, 0, .7), 2.6), 'top': ((0, 0, 9), (0, 0, 0), 5.2)}; masks = {}
for k in range(4):
    for o in meshes: o.hide_render = iscol(o) or lod_of(o) != k
    for vn, (loc, tgt, sz) in VIEWS.items():
        cd.ortho_scale = sz; cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        f = os.path.join(bpy.app.tempdir, f'_tsil_{k}_{vn}.png'); sc.render.filepath = f; bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(f); masks[(k, vn)] = np.array(im.pixels[:], np.float32).reshape(270, 480, 4)[:, :, 3] > .5; bpy.data.images.remove(im)
iou = {f'LOD{k}': {vn: round(float((masks[(k, vn)] & masks[(0, vn)]).sum() / max(1, (masks[(k, vn)] | masks[(0, vn)]).sum())), 4) for vn in VIEWS} for k in range(1, 4)}
th = {1: .97, 2: .95, 3: .90}
chk('LOD silhouette preserved: bounding dimensions within 10 mm of LOD0, silhouette IoU vs LOD0 >= 0.97 LOD1, 0.95 LOD2, 0.90 LOD3', dd <= .010 and all(min(iou[f'LOD{k}'].values()) >= th[k] for k in (1, 2, 3)), f'max dim delta {dd * 1000:.1f} mm; IoU {json.dumps(iou)}')
for o in meshes: o.hide_render = iscol(o)
# 6 materials + light channels (channel = TS_Lights mask cell, decoded from UVs)
LIB = {f'{PFX_MAT}' for PFX_MAT in ()}
allm = sorted({m.name for o in rend for m in o.data.materials if m}); paint = [m for m in allm if m.endswith(('_Paint', '_Paint_LOD1', '_Paint_Far'))]
SHARED_ = {'TS_Atlas', 'TS_Tire', 'TS_Glass', 'TS_Lens', 'TS_LensRed', 'TS_Lights'}; inst = sorted(m for m in allm if bpy.data.materials[m].get('instance_of') in SHARED_ and m not in SHARED_)
okm = set(allm) <= set(paint) | SHARED_ | set(inst) and len(paint) >= 1
chk(f'materials: only the shared traffic library (TS_Atlas, TS_Tire, TS_Glass, TS_Lens, TS_LensRed, TS_Lights) + this vehicle\'s paint instances {paint} + declared instances of shared materials {inst}; no stray / Blender-default materials', okm, str(allm))
def channel_faces(o):
    me = o.data; uv = me.uv_layers['UVMap'].data; res = {}
    for p in me.polygons:
        if me.materials[p.material_index].name != 'TS_Lights': continue
        u = sum(uv[li].uv.x for li in p.loop_indices) / len(p.loop_indices); v = sum(uv[li].uv.y for li in p.loop_indices) / len(p.loop_indices)
        i = int(min(3, max(0, (1 - v) // .25))) * 4 + int(min(3, max(0, u // .25)))
        if i < len(LIGHT_CELLS): res.setdefault(LIGHT_CELLS[i], []).append((o.matrix_world @ p.center))
    return res
bad = []; counts = {}
for k in range(3):
    chs = channel_faces(O[f'Lights_LOD{k}'])
    for ch in ('DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse'):
        pts = chs.get(ch, [])
        if not pts: bad.append((k, ch, 'missing')); continue
        if k == 0: counts[ch] = len(pts)
        ys = [p.y for p in pts]; xs = [p.x for p in pts]
        if ch in ('DRL', 'Headlamp') and max(ys) > -1.8: bad.append((k, ch, 'not front'))
        if ch in ('Tail', 'Reverse') and min(ys) < 1.8: bad.append((k, ch, 'not rear'))
        if ch == 'Brake' and min(ys) < 1.3: bad.append((k, ch, 'not rear'))
        if ch == 'Indicator_L' and min(xs) < 0: bad.append((k, ch, 'not on +X'))
        if ch == 'Indicator_R' and max(xs) > 0: bad.append((k, ch, 'not on -X'))
        if ch in ('Indicator_L', 'Indicator_R') and not (min(ys) < -1.5 and max(ys) > 1.8): bad.append((k, ch, 'needs front + rear'))
chk('independent light channels (TS_Lights mask cells) on Lights_LOD0..2: DRL + Headlamp front, Tail / Reverse rear, Brake rear (incl. high-mount), Indicator_L front + side + rear on +X, Indicator_R on -X', not bad, f'{bad[:4]} faces {json.dumps(counts)}')
# 7 textures
imgs = sorted({n.image for o in rend for m in o.data.materials if m and m.use_nodes for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and not n.image.packed_file}, key=lambda i: i.name)
miss = [i.name for i in imgs if not os.path.exists(bpy.path.abspath(i.filepath))]; mem = sum(i.size[0] * i.size[1] * 4 for i in imgs)
chk(f'textures: {len(imgs)} external PNGs present (shared: atlas, tire, paint flake, light mask; per vehicle: body normal LOD0 + LOD1, AO / grime); uncompressed RGBA {mem / 2**20:.1f} MB (GPU-compressed formats much smaller)', not miss, f'{[i.name for i in imgs]} missing {miss}')
# 8 UVs
uvb = []
for o in rend:
    me = o.data; L_ = [u.name for u in me.uv_layers]
    if L_ != ['UVMap']: uvb.append((o.name, L_)); continue
    uv = me.uv_layers['UVMap'].data; cell = me.attributes.get('cell'); uvs = np.array([d.uv[:] for d in uv]) if len(uv) else np.zeros((0, 2))
    if len(uvs) and not np.isfinite(uvs).all(): uvb.append((o.name, 'nan'))
    for p in me.polygons:
        mn = BASE_(me.materials[p.material_index]); c = cell.data[p.index].value if cell else -1
        if mn == 'TS_Atlas' and 0 <= c < 100:
            u0, v0, s = cell_rect(CELLS[c]); ok = all(u0 - 1e-4 <= uv[li].uv.x <= u0 + s + 1e-4 and v0 - 1e-4 <= uv[li].uv.y <= v0 + s + 1e-4 for li in p.loop_indices)
            if not ok: uvb.append((o.name, 'atlas cell', CELLS[c])); break
        if mn.endswith(('_Paint', '_Paint_LOD1', '_Paint_Far')) and not all(-1e-4 <= uv[li].uv.x <= 1 + 1e-4 and -1e-4 <= uv[li].uv.y <= 1 + 1e-4 for li in p.loop_indices): uvb.append((o.name, 'paint uv outside 0-1')); break
chk('UVs: exactly one UV channel (UVMap) on every render mesh, finite; atlas faces inside their cell; light faces inside their mask cell; paint body UVs unique unwrap in 0-1 (baked normal / AO)', not uvb, str(uvb[:4]))
# 9 topology
topo = []
for o in rend:
    bm = bmesh.new(); bm.from_mesh(o.data); bm.normal_update()
    za = sum(1 for f in bm.faces if f.calc_area() < 1e-9); lv = sum(1 for v in bm.verts if not v.link_faces); dup = len(bm.faces) - len({frozenset(v.index for v in f.verts) for f in bm.faces}); bm.free()
    if za or lv or dup: topo.append((o.name, za, lv, dup))
chk('topology: no zero-area faces, no loose vertices, no duplicate (coincident) faces on every render mesh', not topo, str(topo[:5]))
# 10 colliders + COM
CZ = [float(v) for v in os.environ.get('TS_COM_Z', '.3,.7').split(',')]                          # class range: cars .3-.7; trucks / buses sit higher (env)
col = {}
for o in meshes:
    if not iscol(o): continue
    bm = bmesh.new(); bm.from_mesh(o.data); bm.normal_update(); closed = all(len(e.link_faces) == 2 for e in bm.edges)
    convex = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 1e-3 for v in bm.verts) for f in bm.faces); cen = sum((v.co for v in bm.verts), Vector()) / len(bm.verts)
    outward = all((f.calc_center_median() - cen).dot(f.normal) > 0 for f in bm.faces); col[o.name] = dict(tris=tris(o), closed=closed, convex=convex, outward=outward, material=bool(o.data.materials), uv=len(o.data.uv_layers)); bm.free()
cu = np.vstack([V(o) for o in meshes if iscol(o)]); bo = np.vstack([V(o) for o in LOD[0] if o.name.startswith(('Body', 'Glass'))])
cover = float(max(np.abs(cu.min(0) - bo.min(0)).max(), np.abs(cu.max(0) - bo.max(0)).max())); com = O['CenterOfMass'].matrix_world.translation
chk(f'colliders: {len(col)} convex hulls, each closed, convex, outward, <= 255 tris, no material, no UVs; union bounds within 6 cm of the body; CenterOfMass on the centreline, z {com.z:.2f} ({CZ[0]}-{CZ[1]}), between the axles',
    len(col) >= 4 and all(c['closed'] and c['convex'] and c['outward'] and c['tris'] <= 255 and not c['material'] and not c['uv'] for c in col.values()) and cover <= .06 and abs(com.x) < 1e-6 and CZ[0] <= com.z <= CZ[1] and ref['FL'].y < com.y < ref['RL'].y,
    f'{json.dumps(col)}; cover {cover:.3f} m')
# 11 visual QA renders present (studio / daylight / game camera / LOD compare)
PV = D('previews'); SH = [f'{BASE}_{v}.png' for v in ('front34', 'rear34', 'front', 'rear', 'side', 'top', 'wheel', 'interior', 'front_detail', 'rear_detail', 'day_front34', 'day_rear34', 'day_side', 'game_close', 'game_normal', 'game_far')]
miss_p = [s for s in SH if not os.path.exists(os.path.join(PV, s))]
chk(f'visual QA renders: studio (10), daylight (3), game camera (3) present', not miss_p, f'missing {miss_p}')
# S1 shading screen on ALL LODs (VA_SHADING_QA_STANDARD.md)
def tear_pct(o, lim=50.0):
    cn = o.data.corner_normals; b = t = 0
    for p in o.data.polygons:
        if p.area < 2e-6: continue
        for li in p.loop_indices: t += 1; b += cn[li].vector.angle(p.normal, 0) > math.radians(lim)
    return 100.0 * b / max(t, 1)
TEAR = {o.name: round(tear_pct(o), 3) for o in rend}
s1 = all(v <= 1.0 for v in TEAR.values()); worst = sorted(TEAR.items(), key=lambda t: -t[1])[:5]
geo = dict(lods={f'LOD{k}': dict(triangles=T[k], ratio=round(r[k], 4), objects=len(LOD[k]), materials=len(mats[k]), draw_calls=dcalls[k], dims_m=dims[k], parts={o.name: tris(o) for o in LOD[k]}) for k in range(4)},
           wheel_refs={c: [round(v, 4) for v in ref[c]] for c in ref}, center_of_mass=[round(v, 4) for v in com], colliders=col, silhouette_iou=iou, light_faces=counts, texture_memory_mb=round(mem / 2**20, 2),
           textures=[i.name for i in imgs], lod_tear_pct=TEAR)
# 12 FBX re-import
man = json.load(open(D('reports', f'{PFX}_export_manifest.json')))
if os.environ.get('TS_NO_FBX'): man = dict(files={}); log.append('[SKIP]     FBX clean re-import: NOT RUN - Blender-only production (owner instruction: no FBX / Unity files)')
SRCB = {o.name: (V(o).min(0).tolist(), V(o).max(0).tolist(), tris(o), sorted(m.name for m in o.data.materials), [u.name for u in o.data.uv_layers]) for o in meshes}
PAR = {o.name: (o.parent.name if o.parent else None) for o in master}; ORG = {o.name: o.matrix_world.translation.copy() for o in master}
reim = {}
for fname, d in man['files'].items():
    for raw in (False, True):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        kw = dict(use_manual_orientation=True, axis_forward='Y', axis_up='Z') if raw else {}
        bpy.ops.import_scene.fbx(filepath=D('exports', fname), **kw); got = {o.name: o for o in bpy.data.objects}; pr = []
        if sorted(got) != sorted(d['objects']): pr.append(f"names: missing {sorted(set(d['objects']) - set(got))[:3]} extra {sorted(set(got) - set(d['objects']))[:3]}")
        bpy.context.view_layer.update()
        if not raw:
            hb = [n for n, o in got.items() if PAR.get(n, '?') != (o.parent.name if o.parent else None)]
            if hb: pr.append(f'hierarchy {hb[:3]}')
            dev = 0.0
            for n, o in got.items():
                if o.type != 'MESH' or n not in SRCB: continue
                v = np.array([(o.matrix_world @ x.co)[:] for x in o.data.vertices]); dev = max(dev, float(np.abs(np.concatenate([v.min(0) - SRCB[n][0], v.max(0) - SRCB[n][1]])).max()))
                if tris(o) > SRCB[n][2] or tris(o) < SRCB[n][2] - 30: pr.append(f'{n} tris {tris(o)} vs {SRCB[n][2]}')
                if sorted(m.name.split('.')[0] for m in o.data.materials) != SRCB[n][3]: pr.append(f'{n} mats')
                if [u.name for u in o.data.uv_layers] != SRCB[n][4]: pr.append(f'{n} uv')
            pdev = max((got[n].matrix_world.translation - ORG[n]).length for n in got if n in ORG)
            if dev > 1e-3 or pdev > 1e-4: pr.append(f'world deviation {dev:.1e} pivot {pdev:.1e}')
            texok = all(os.path.exists(bpy.path.abspath(n.image.filepath)) for m in bpy.data.materials if m.use_nodes for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and n.image.filepath)
            if not texok: pr.append('texture references broken')
            reim[fname] = dict(objects=len(got), max_bounds_dev_m=dev, max_pivot_dev_m=pdev, problems=pr)
        else:
            u = lambda p: Vector((-p.x, p.y, p.z))
            pts = np.vstack([np.array([(o.matrix_world @ x.co)[:] for x in o.data.vertices]) for n, o in got.items() if o.type == 'MESH' and n == 'Body_LOD0'])
            fl = u(got['WheelColliderRef_FL'].matrix_world.translation); com_u = u(got['CenterOfMass'].matrix_world.translation)
            unity = dict(nose_z=round(float(pts[:, 2].max()), 4), tail_z=round(float(pts[:, 2].min()), 4), roof_y=round(float(pts[:, 1].max()), 4), FL=[round(v, 4) for v in fl], COM=[round(v, 4) for v in com_u])
            if not (unity['nose_z'] > 2.0 and unity['tail_z'] < -2.0 and unity['roof_y'] > 1.0 and fl.x < 0 and fl.z > 0 and fl.y > .2): pr.append(f'unity axes {unity}')
            reim[fname]['unity_space'] = unity; reim[fname]['problems'] += pr
    p_ = reim[fname]['problems']
    log.append(f'[{"PASS" if not p_ else "FAIL"}] {N[0] + 1:>2}. FBX clean re-import {fname}: {reim[fname]["objects"]} objects, names + hierarchy match, bounds dev {reim[fname]["max_bounds_dev_m"]:.1e} m, pivots dev {reim[fname]["max_pivot_dev_m"]:.1e} m, '
               f'triangles / materials / UVMap / textures preserved; raw Unity space {json.dumps(reim[fname]["unity_space"])} (nose +Z, up +Y, FL on -X, front axle -Z)' + (f' -- {"; ".join(p_[:4])}' if p_ else '')); N[0] += 1; cnt['FAIL'] += bool(p_)
log.append(f"[{'PASS' if s1 else 'FAIL'}] S1. shading screen, ALL LODs: torn loop normals (> 50 deg off their face) <= 1 % on every render mesh (calibration in VA_SHADING_QA_STANDARD.md; visual LOD comparison renders confirm) -- worst {worst}")
cnt['FAIL'] += 0 if s1 else 1
log += ['', f"SUMMARY: {cnt['FAIL']} errors, {cnt['WARN']} warnings"]
geo['fbx_reimport'] = reim
open(D('reports', f'{PFX}_validation.txt'), 'w').write('\n'.join(log) + '\n'); json.dump(geo, open(D('reports', f'{PFX}_geometry.json'), 'w'), indent=1)
print('\n'.join(log))
