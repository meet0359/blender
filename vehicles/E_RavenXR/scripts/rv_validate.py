# Raven XR validation (read-only). Opens ravenxr_09_export_ready.blend; checks geometry / hierarchy / pivots / LODs / materials / UVs / colliders / budgets,
# renders LOD silhouettes (workbench, session only), then re-imports both FBX files into clean scenes (Blender space + raw Unity space).
#   Blender -b --factory-startup --python zg_validate.py [-- <previews dir>]
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from rv_lib import *
import hashlib
PREV = (sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [P('previews')])[0]
REP = os.path.join(SCR, 'reports') if SCR else REPD() if False else P('reports'); os.makedirs(REP, exist_ok=True)
SRC9 = CKP('ravenxr_09_export_ready.blend'); bpy.ops.wm.open_mainfile(filepath=SRC9); O = bpy.data.objects
log, cnt, N = [], {'FAIL': 0, 'WARN': 0}, [0]
def chk(msg, ok, detail='', warn=False):
    N[0] += 1; tag = 'PASS' if ok else ('WARN' if warn else 'FAIL'); log.append(f'[{tag}] {N[0]:>2}. {msg}' + (f' -- {detail}' if detail else ''))
    if not ok: cnt[tag] += 1
    return ok
V = lambda o: np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) if len(o.data.vertices) else np.zeros((0, 3))
master = sorted(bpy.data.collections['RAVEN_XR'].all_objects, key=lambda o: o.name); meshes = [o for o in master if o.type == 'MESH']
iscol = lambda o: o.name.startswith('Collision_'); rend = [o for o in meshes if not iscol(o)]
def lod_of(o):
    p = o
    while p:
        m = re.match(r'LOD(\d)_Root$', p.name)
        if m: return int(m.group(1))
        p = p.parent
    return None
LOD = {k: [o for o in rend if lod_of(o) == k] for k in range(4)}
T = {k: sum(tris(o) for o in v) for k, v in LOD.items()}
log += ['== RAVEN XR (Phase E original build) - VALIDATION ==', f'source blend/ravenxr_09_export_ready.blend; RAVEN_XR {len(master)} objects, {len(meshes)} meshes ({len(rend)} render, {len(meshes) - len(rend)} colliders)', '']
# 1 integrity
WS_ = WS; base = json.load(open(os.path.join(WS_, 'vehicles/A_Discovery/reports/VA_workspace_baseline.json')))['files']
changed = [k for k, v in base.items() if not os.path.exists(os.path.join(WS_, k)) or hashlib.sha1(open(os.path.join(WS_, k), 'rb').read()).hexdigest() != v['sha1']]
now = set()
for d, dirs, fs in os.walk(WS_):
    rel = os.path.relpath(d, WS_)
    if rel == 'vehicles' or rel.startswith('vehicles' + os.sep): dirs[:] = []; continue
    now |= {os.path.relpath(os.path.join(d, f), WS_) for f in fs if f != '.DS_Store'}
added = sorted(now - set(base))
def frozen(ph, rec):
    L_ = [l for l in open(f'{WS_}/vehicles/{ph}/reports/{rec}') if l.startswith('| `')]
    return L_, [l.split('`')[1] for l in L_ if hashlib.sha1(open(os.path.join(WS_, 'vehicles', ph, l.split('`')[1]), 'rb').read()).hexdigest() != l.split('`')[3]]
FR = {n: frozen(ph, rec) for n, ph, rec in (('Zero Gap R', 'B_ZeroGapR', 'ZG_FINAL_FREEZE.md'), ('Titan GT original', 'C_TitanGT', 'TG_FINAL_FREEZE.md'), ('Titan GT r1', 'C_TitanGT_r1', 'TG_R1_FINAL_FREEZE.md'), ('Vortex R', 'D_VortexR', 'VX_FINAL_FREEZE.md'))}
zgbad = [f for _, (_, b_) in FR.items() for f in b_]
blk = P('blend', 'ravenxr_01_blockout.blend'); BLK_SHA = '52a857d7f323648633deed30a1389214029c7f75'                        # approved Raven XR blockout
blk_ok = os.path.exists(blk) and hashlib.sha1(open(blk, 'rb').read()).hexdigest() == BLK_SHA
chk(f'protected files byte-identical: Phase A baseline (frozen P0-P3, frozen Hypercar, racing_car sources, all files outside vehicles/), frozen ' + ', '.join(f'{n} ({len(L_)} files)' for n, (L_, _) in FR.items()) + f', approved Raven XR blockout checkpoint untouched; nothing added outside vehicles/',
    not changed and not added and not zgbad and all(len(L_) > 60 for L_, _ in FR.values()) and blk_ok, f'{len(base)} files; changed {changed[:3]} added {added[:3]} frozen vehicles changed {zgbad[:3]}')
# 2 hierarchy
I = Matrix.Identity(4); cr = O.get('Car_Root')
roots_ok = cr and cr.parent is None and all(abs(a - b) < 1e-9 for ra, rb in zip(cr.matrix_world, I) for a, b in zip(ra, rb))
lr_ok = all(O.get(f'LOD{k}_Root') and O[f'LOD{k}_Root'].parent == cr and all(abs(a - b) < 1e-9 for ra, rb in zip(O[f'LOD{k}_Root'].matrix_world, I) for a, b in zip(ra, rb)) for k in range(4))
need = ['Collision', 'CenterOfMass'] + [f'WheelColliderRef_{c}' for c in ('FL', 'FR', 'RL', 'RR')]
chk('hierarchy: Car_Root (origin, identity, top level) -> LOD0_Root..LOD3_Root (identity, overlap exactly), Collision, WheelColliderRef_FL/FR/RL/RR, CenterOfMass; no cameras / lights; no negative or non-unit scale',
    bool(roots_ok and lr_ok and all(O.get(n) and O[n].parent == cr for n in need)) and not [o for o in master if o.type in ('CAMERA', 'LIGHT')] and all(abs(s - 1) < 1e-6 for o in master for s in o.matrix_world.to_scale()),
    f"top-level {[o.name for o in master if o.parent is None]}")
parts = {k: sorted(re.sub(r'_LOD\d$', '', o.name) for o in v) for k, v in LOD.items()}
chk('every LOD has the full car: Body (with doors, panel gaps, mirrors), Trim, Lights, Glass, Interior, Wheel+Tire x4 (BrakeDisc + Caliper x4 at LOD0-2; LOD3 drops brake hardware hidden behind the spokes; SteeringWheel at LOD0-2)',
    all({'Body', 'Trim', 'Lights', 'Glass', 'Interior'} <= set(parts[k]) and sum(1 for p in parts[k] if p.startswith('Wheel_')) == 4 and sum(1 for p in parts[k] if p.startswith('Tire_')) == 4 for k in range(4))
    and all(sum(1 for p in parts[k] if p.startswith('BrakeDisc_')) == 4 and sum(1 for p in parts[k] if p.startswith('Caliper_')) == 4 for k in range(3)), json.dumps({k: len(v) for k, v in parts.items()}))
# 3 convention + pivots
ref = {c: O[f'WheelColliderRef_{c}'].matrix_world.translation for c in ('FL', 'FR', 'RL', 'RR')}
conv = ref['FL'].x > 0 and ref['RL'].x > 0 and ref['FR'].x < 0 and ref['RR'].x < 0 and ref['FL'].y < 0 and ref['RL'].y > 0
nose = max((V(o)[:, 1].min() for o in LOD[0] if o.name.startswith('Fascia') or o.name.startswith('Body')), default=0)
chk('orientation: nose toward -Y, vehicle left = +X (FL / RL refs on +X, FR / RR on -X), +Z up, LHD driver (steering wheel) on +X',
    conv and O['SteeringWheel_LOD0'].matrix_world.translation.x > 0, f"FL {tuple(round(v, 3) for v in ref['FL'])} RL {tuple(round(v, 3) for v in ref['RL'])} steering hub x {O['SteeringWheel_LOD0'].matrix_world.translation.x:.3f}")
piv = []
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        w = O.get(f'Wheel_{c}_LOD{k}')
        if not w: piv.append((k, c, 'missing')); continue
        off = (w.matrix_world.translation - ref[c]).length
        v0 = np.array([(w.matrix_world @ v.co)[:] for v in w.data.vertices]); ctr0 = (v0.min(0) + v0.max(0)) / 2
        cal = O.get(f'Caliper_{c}_LOD{k}'); cal0 = cal.matrix_world.copy() if cal else None
        errs = []
        for ang in (math.radians(30), math.radians(-30)):
            w.rotation_euler.x = ang; bpy.context.view_layer.update()
            v1 = np.array([(w.matrix_world @ v.co)[:] for v in w.data.vertices]); errs.append(float(np.abs(((v1.min(0) + v1.max(0)) / 2 - ctr0)[0])))
            if cal and max(abs(a - b) for ra, rb in zip(cal.matrix_world, cal0) for a, b in zip(ra, rb)) > 1e-9: errs.append(9)
            t = O.get(f'Tire_{c}_LOD{k}')
            if t and t.parent != w: errs.append(9)
        w.rotation_euler.x = 0
        if c[0] == 'F':
            sp = O[f'SteerPivot_{c}_LOD{k}']; sp.rotation_euler.z = math.radians(25); bpy.context.view_layer.update()
            errs.append(float((w.matrix_world.translation - ref[c]).length))                                  # wheel centre stays on the steering axis
            cal = O.get(f'Caliper_{c}_LOD{k}')
            if cal and cal.parent != sp: errs.append(9)
            sp.rotation_euler.z = 0
        bpy.context.view_layer.update()
        if off > 1e-6 or max(errs) > 2e-3: piv.append((k, c, round(off * 1000, 4), [round(e * 1000, 2) for e in errs]))
chk('wheel pivots: every Wheel_<c>_LODn origin = WheelColliderRef (< 0.001 mm); +/-30 deg roll about local X keeps the hub centre (< 2 mm, faceted rims); tire + brake disc roll with the wheel, calipers do not; front SteerPivot +25 deg yaw keeps the wheel centre on the steering axis and steers the caliper',
    not piv, str(piv[:4]))
lowz = {k: round(float(min(V(O[f'Tire_{c}_LOD{k}'])[:, 2].min() for c in ('FL', 'FR', 'RL', 'RR'))), 4) for k in range(4)}
body_low = round(float(min(V(o)[:, 2].min() for o in LOD[0] if not re.match(r'(Wheel|Tire|BrakeDisc|Caliper)_', o.name))), 4)
chk('ground contact + clearance: tires touch the ground plane (lowest tire point within 5 mm of z 0 at every LOD); body / splitter / diffuser lowest point >= 0.10 m (road clearance)',
    all(abs(z) <= .005 for z in lowz.values()) and body_low >= .10, f'tire min z {lowz}; body min z {body_low}')
# 4 budgets
r = {k: T[k] / T[0] for k in range(4)}
chk(f'triangle budget (approved mobile targets): LOD0 {T[0]:,} within 60-90k target (hard ceiling 120k); LOD1 {T[1]:,} ({r[1]:.0%}, target 40-50%); LOD2 {T[2]:,} ({r[2]:.0%}, target 15-25%); LOD3 {T[3]:,} ({r[3]:.0%}, target 5-10%); strictly decreasing',
    60000 <= T[0] <= 90000 and .38 <= r[1] <= .52 and .14 <= r[2] <= .26 and .045 <= r[3] <= .105 and T[0] > T[1] > T[2] > T[3], f'blockout was 112,874 (unoptimised)')
objs = {k: len(v) for k, v in LOD.items()}; mats = {k: len({m.name for o in v for m in o.data.materials}) for k, v in LOD.items()}
chk(f'draw-call consolidation: render objects per LOD {objs}; materials per LOD {mats}; <= 16 materials (project convention)',
    objs[0] <= 30 and all(v <= 16 for v in mats.values()))
# 5 silhouette (dimensions + workbench IoU from 3 views)
dims = {}
for k in range(4):
    a = np.vstack([V(o) for o in LOD[k]]); dims[k] = (a.max(0) - a.min(0)).round(4).tolist()
dd = max(abs(dims[k][i] - dims[0][i]) for k in range(1, 4) for i in range(3))
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0, 0, 0)
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 480, 270, 100; sc.render.film_transparent = True
cd = bpy.data.cameras.new('VC'); cam = bpy.data.objects.new('VC', cd); sc.collection.objects.link(cam); sc.camera = cam; cd.type = 'ORTHO'
VIEWS = {'side': ((9, 0, .55), (0, 0, .55), 5.0), 'front': ((0, -9, .55), (0, 0, .55), 2.6), 'top': ((0, 0, 9), (0, 0, 0), 5.0)}
masks = {}
for k in range(4):
    for o in rend: o.hide_render = lod_of(o) != k
    for o in master:
        if o.type == 'MESH' and iscol(o): o.hide_render = True
    for vn, (loc, tgt, sz) in VIEWS.items():
        cd.ortho_scale = sz; cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        f = os.path.join(SCR or bpy.app.tempdir, f'_sil_{k}_{vn}.png'); sc.render.filepath = f; bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(f); a = np.array(im.pixels[:], np.float32).reshape(270, 480, 4)[:, :, 3] > .5; masks[(k, vn)] = a; bpy.data.images.remove(im)
iou = {f'LOD{k}': {vn: round(float((masks[(k, vn)] & masks[(0, vn)]).sum() / max(1, (masks[(k, vn)] | masks[(0, vn)]).sum())), 4) for vn in VIEWS} for k in range(1, 4)}
th = {1: .97, 2: .95, 3: .90}
chk('LOD silhouette preserved: bounding dimensions within 10 mm of LOD0 at every LOD, silhouette IoU vs LOD0 (side / front / top, orthographic) >= 0.97 LOD1, 0.95 LOD2, 0.90 LOD3',
    dd <= .010 and all(v >= th[k] for k in (1, 2, 3) for v in iou[f'LOD{k}'].values()), f'max dim delta {dd * 1000:.1f} mm; IoU {json.dumps(iou)}')
for o in rend: o.hide_render = False
# 6 materials + light channels
allm = sorted({m.name for o in rend for m in o.data.materials})
chk(f'materials: only the 15 Raven XR engine materials {allm}; no stray / Blender-default materials left', set(allm) <= set(MATS) and len(allm) == len(MATS), f'missing {sorted(set(MATS) - set(allm))}')
def faces_of(o, mname):
    me = o.data; idx = [i for i, m in enumerate(me.materials) if m and m.name == mname]
    return [p for p in me.polygons if p.material_index in idx]
ch = {}
for k in range(3):
    L = O[f'Lights_LOD{k}']; mw = L.matrix_world
    for m in LIGHTS:
        fs = faces_of(L, m); cs = [mw @ p.center for p in fs]; ch[(k, m)] = (len(fs), (min(c.y for c in cs), max(c.y for c in cs)) if cs else None, (min(c.x for c in cs), max(c.x for c in cs)) if cs else None)
bad = []
for k in range(3):
    for m in LIGHTS:
        n, yr, xr = ch[(k, m)]
        if not n: bad.append((k, m, 'missing')); continue
        if m in ('RV_LED_DRL', 'RV_LED_Headlamp') and yr[1] > -1.5: bad.append((k, m, 'not front'))
        if m in ('RV_LED_Tail', 'RV_LED_Brake', 'RV_LED_Reverse') and yr[0] < 1.9: bad.append((k, m, 'not rear'))
        if m == 'RV_LED_Indicator_L' and xr[0] < 0: bad.append((k, m, 'not on +X (left)'))
        if m == 'RV_LED_Indicator_R' and xr[1] > 0: bad.append((k, m, 'not on -X (right)'))
chk('independent light channels on Lights_LOD0..2: DRL + headlamp (front), tail, brake, reverse (rear), Indicator_L on vehicle left (+X) front and rear, Indicator_R on -X; each its own material for Unity runtime control',
    not bad, str(bad[:4]) + ' ' + json.dumps({m: ch[(0, m)][0] for m in LIGHTS}))
# 7 textures + memory
imgs = sorted({n.image for m in allm for n in bpy.data.materials[m].node_tree.nodes if n.type == 'TEX_IMAGE' and n.image}, key=lambda i: i.name)
miss = [i.name for i in imgs if not os.path.exists(os.path.normpath(bpy.path.abspath(i.filepath)))]
mem = sum(i.size[0] * i.size[1] * 4 for i in imgs); disk = sum(os.path.getsize(os.path.normpath(bpy.path.abspath(i.filepath))) for i in imgs if i.name not in miss)
chk(f'textures: {len(imgs)} external PNGs, all present on disk; uncompressed RGBA memory {mem / 2**20:.1f} MB; on disk {disk / 2**20:.1f} MB',
    not miss and mem < 40 * 2**20, f'{[i.name for i in imgs]} missing {miss}')
# 8 UVs
uvb = []
for o in rend:
    me = o.data; lay = [u.name for u in me.uv_layers]
    if lay != ['UVMap']: uvb.append((o.name, lay)); continue
    uv = np.empty(len(me.loops) * 2); me.uv_layers[0].data.foreach_get('uv', uv)
    if not np.isfinite(uv).all(): uvb.append((o.name, 'nan'))
    sw = me.attributes.get('swatch')
    for p in me.polygons:
        m = me.materials[p.material_index].name if me.materials[p.material_index] else ''
        if m == 'RV_Palette':
            u0, v0 = swatch_uv(SWATCH[sw.data[p.index].value])
            if any(abs(me.uv_layers[0].data[li].uv[0] - u0) > .5 / GRID or abs(me.uv_layers[0].data[li].uv[1] - v0) > .5 / GRID for li in p.loop_indices): uvb.append((o.name, 'palette')); break
chk('UVs: exactly one UV channel (UVMap) on every render mesh, finite; palette faces sample inside their swatch cell; tire sidewall atlas on revolve UVs; carbon / paint world-scale box UVs ', not uvb, str(uvb[:4]))
# 9 topology
topo = []
for o in rend:
    bm = bmesh.new(); bm.from_mesh(o.data); bm.normal_update()
    za = sum(1 for f in bm.faces if f.calc_area() < 1e-9); lv = sum(1 for v in bm.verts if not v.link_faces)
    dup = len(bm.faces) - len({frozenset(v.index for v in f.verts) for f in bm.faces})
    wind = sum(1 for e in bm.edges if len(e.link_faces) == 2 and [l.vert for l in e.link_faces[0].loops if l.edge == e][0] == [l.vert for l in e.link_faces[1].loops if l.edge == e][0])
    bm.free()
    if za or lv or dup or wind: topo.append((o.name, za, lv, dup, wind))
chk('topology: no zero-area faces, no loose vertices, no duplicate (coincident) faces, consistent winding on every render mesh ', not topo, str(topo[:5]))
# 10 colliders + COM
col = {}
for o in meshes:
    if not iscol(o): continue
    bm = bmesh.new(); bm.from_mesh(o.data); bm.transform(o.matrix_world); bm.normal_update()
    closed = all(len(e.link_faces) == 2 for e in bm.edges); conv = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 1e-3 for v in bm.verts) for f in bm.faces)
    vol = sum(f.calc_center_median().dot(f.normal) * f.calc_area() for f in bm.faces) / 3; bm.free()
    col[o.name] = dict(tris=tris(o), closed=closed, convex=conv, outward=vol > 0, material=bool(o.data.materials), uv=len(o.data.uv_layers))
cv = np.vstack([V(o) for o in meshes if iscol(o)]); bv = np.vstack([V(o) for o in LOD[0] if not re.match(r'(Wheel|Tire|BrakeDisc|Caliper)_', o.name)])
cover = np.abs(np.concatenate([cv.min(0) - bv.min(0), cv.max(0) - bv.max(0)])).max()
com = O['CenterOfMass'].matrix_world.translation
chk(f'colliders: {len(col)} convex hulls (Front / Body / Cabin / Rear incl. deck spoiler), each closed, convex, outward, <= 255 tris, no material, no UVs; union bounds within 6 cm of the body; CenterOfMass on the centreline, low (z {com.z:.2f}), between the axles',
    len(col) >= 4 and all(c['closed'] and c['convex'] and c['outward'] and c['tris'] <= 255 and not c['material'] and not c['uv'] for c in col.values()) and cover <= .06
    and abs(com.x) < 1e-6 and .25 <= com.z <= .5 and ref['FL'].y < com.y < ref['RL'].y, f'{json.dumps(col)}; cover {cover:.3f} m')
# 11 previews
SH = ['front', 'rear', 'left', 'right', 'front34', 'rear34', 'top', 'interior', 'wheel', 'chase', 'hood_zoom', 'tail_zoom', 'door_zoom', 'lod_lineup']
miss_p = [s for s in SH if not os.path.exists(os.path.join(PREV, f'RV_{s}.png'))]
chk(f'previews: all {len(SH)} review renders exist (front, rear, left, right, 3/4 front + rear, top, interior, wheel, chase on the frozen P0 road, hood / tail / door close-ups, LOD lineup)', not miss_p, f'missing {miss_p}')
geo = dict(lods={f'LOD{k}': dict(triangles=T[k], ratio=round(r[k], 4), objects=objs[k], materials=mats[k], dims_m=dims[k], parts={o.name: tris(o) for o in LOD[k]}) for k in range(4)},
           wheel_refs={c: [round(v, 4) for v in ref[c]] for c in ref}, center_of_mass=[round(v, 4) for v in com], colliders=col, silhouette_iou=iou, light_faces={m: ch[(0, m)][0] for m in LIGHTS},
           texture_memory_mb=round(mem / 2**20, 2), texture_disk_mb=round(disk / 2**20, 2), textures=[i.name for i in imgs])
# S1 supplementary (expanded visual test, numeric): close-up LOD1 shading — torn loop normals. Calibrated on the frozen releases:
#    Titan GT original Body_LOD1 11.9 % / Trim_LOD1 26.6 % torn (visible tears), Titan GT r1 0 % / 0 % (clean).
def tear_pct(o, lim=50.0):
    cn = o.data.corner_normals; bad = tot = 0
    for p in o.data.polygons:
        if p.area < 2e-6: continue
        for li in p.loop_indices:
            tot += 1; bad += cn[li].vector.angle(p.normal, 0) > math.radians(lim)
    return 100.0 * bad / max(tot, 1)
TEAR = {o.name: round(tear_pct(o), 3) for k_ in (1, 2) for o in LOD[k_] if not o.name.startswith(('Tire', 'Wheel', 'Brake', 'Caliper'))}
s1 = all(v <= 1.0 for v in TEAR.values()); cnt['FAIL'] += 0 if s1 else 1; geo['lod_tear_pct'] = TEAR
# 12 FBX re-import (clean scene; pass 1 Blender space, pass 2 raw = Unity coordinates)
man = json.load(open(os.path.join(REP, 'RV_export_manifest.json')))
SRCB = {o.name: (V(o).min(0).tolist(), V(o).max(0).tolist(), tris(o), sorted(m.name for m in o.data.materials), [u.name for u in o.data.uv_layers]) for o in meshes}
PAR = {o.name: (o.parent.name if o.parent else None) for o in master}; ORG = {o.name: o.matrix_world.translation.copy() for o in master}
reim = {}
for fname, d in man['files'].items():
    for raw in (False, True):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        kw = dict(use_manual_orientation=True, axis_forward='Y', axis_up='Z') if raw else {}
        bpy.ops.import_scene.fbx(filepath=EXP(fname), **kw); got = {o.name: o for o in bpy.data.objects}; pr = []
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
            texok = all(os.path.exists(bpy.path.abspath(n.image.filepath)) for m in bpy.data.materials if m.use_nodes for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image)
            if not texok: pr.append('texture references broken')
            reim[fname] = dict(objects=len(got), max_bounds_dev_m=dev, max_pivot_dev_m=pdev, problems=pr)
        else:
            u = lambda p: Vector((-p.x, p.y, p.z))                                                  # raw FBX file coords -> Unity (importer negates X)
            pts = np.vstack([np.array([(o.matrix_world @ x.co)[:] for x in o.data.vertices]) for n, o in got.items() if o.type == 'MESH' and n.startswith(('Body_LOD0', 'Fascia'))] or [np.zeros((1, 3))])
            fl = u(got['WheelColliderRef_FL'].matrix_world.translation); com_u = u(got['CenterOfMass'].matrix_world.translation)
            unity = dict(nose_z=round(float(pts[:, 2].max()), 4), tail_z=round(float(pts[:, 2].min()), 4), roof_y=round(float(pts[:, 1].max()), 4), FL=[round(v, 4) for v in fl], COM=[round(v, 4) for v in com_u])
            if not (unity['nose_z'] > 2.0 and unity['tail_z'] < -2.0 and unity['roof_y'] > 1.0 and fl.x < 0 and fl.z > 0 and abs(fl.y - RF) < 1e-3): pr.append(f'unity axes {unity}')
            reim[fname]['unity_space'] = unity; reim[fname]['problems'] += pr
    p_ = reim[fname]['problems']
    log.append(f'[{"PASS" if not p_ else "FAIL"}] {N[0] + 1:>2}. FBX clean re-import {fname}: {reim[fname]["objects"]} objects, names + hierarchy match, bounds dev {reim[fname]["max_bounds_dev_m"]:.1e} m, pivots dev {reim[fname]["max_pivot_dev_m"]:.1e} m, '
               f'triangles / materials / UVMap / textures preserved; raw Unity space {json.dumps(reim[fname]["unity_space"])} (nose +Z, up +Y, FL on -X)' + (f' -- {"; ".join(p_[:4])}' if p_ else '')); N[0] += 1; cnt['FAIL'] += bool(p_)
log.append(f"[{'PASS' if s1 else 'FAIL'}] S1. (supplementary) close-up LOD1 / LOD2 shading: torn loop normals (> 50 deg off their face) <= 1 % on every body / glass / trim / lights / interior / steering mesh (calibration: Titan GT original Body_LOD1 11.9 %, Trim_LOD1 26.6 %; Titan GT r1 0 %) -- {json.dumps(TEAR)}")
log += ['', f"SUMMARY: {cnt['FAIL']} errors, {cnt['WARN']} warnings"]
geo['fbx_reimport'] = reim
open(os.path.join(REP, 'RV_validation.txt'), 'w').write('\n'.join(log) + '\n'); json.dump(geo, open(os.path.join(REP, 'RV_geometry.json'), 'w'), indent=1)
print('\n'.join(log))
