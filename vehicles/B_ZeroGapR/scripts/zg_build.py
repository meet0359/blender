# Zero Gap R (Phase B) build. Blender -b --factory-startup --python zg_build.py [-- <last stage 1..8>]
# Reads the frozen-in-place source racing_car_09 READ-ONLY and writes numbered checkpoints into vehicles/B_ZeroGapR/blend (or ZG_SCRATCH).
#  01 intake | 02 cleanup + convention mirror + material consolidation | 03 exterior (front / rear fascia, lights, exhaust, diffuser, pillars, surfaces)
#  04 wheels / tires / brakes assemblies | 05 glass, lights, interior | 06 merge + UVs | 07 LODs | 08 colliders, hierarchy, pivots, refs
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from zg_lib import *
LAST = int(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else 8
bpy.ops.wm.open_mainfile(filepath=SRC); sc = bpy.context.scene; O = bpy.data.objects
REPORT = {}
# ================================================================ 00 measurements from the source (read-only)
sw = measure_source_swatches()
pm = bpy.data.materials['MAT_CarPaint_BrightRed']; pimg = next(n.image for n in pm.node_tree.nodes if n.type == 'TEX_IMAGE' and 'BaseColor' in n.image.name)
sw['paint_source_mean'] = img_mean(pimg, True); sw['paint'] = [.58, .018, .024]                    # source mean reads maroon under the flat clear-coat; restore the bright racing red
sw['wheel_metal'] = dict(base=[.46, .48, .51], rough=.24, metal=1.0)                                      # source mean rendered near-black; bright machined alloy
cm = bpy.data.materials['MAT_CarbonFiber_Engine']; tm = bpy.data.materials['MAT_Tire_LOD_Detail_Engine']
img = lambda m, key: next(n.image for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image and key in n.image.name)
tex = write_palette({k: v for k, v in sw.items() if isinstance(v, dict)})
tex['ZG_Carbon_BaseColor'] = resave(img(cm, 'BaseColor'), 'ZG_Carbon_BaseColor', 1024, False); tex['ZG_Carbon_Normal'] = resave(img(cm, 'Normal'), 'ZG_Carbon_Normal', 1024, True)
tex['ZG_Tire_BaseColor'] = resave(img(tm, 'BaseColor'), 'ZG_Tire_BaseColor', 1024, False); tex['ZG_Tire_Normal'] = resave(img(tm, 'Normal'), 'ZG_Tire_Normal', 1024, True)
carbon_tile = float(cm.get('tile_m', .25)) if cm.get('tile_m') else .25
REPORT['swatches'] = {k: {kk: [round(x, 4) for x in vv] if isinstance(vv, list) else round(vv, 4) for kk, vv in v.items()} for k, v in sw.items() if isinstance(v, dict)}; REPORT['paint_linear'] = [round(x, 4) for x in sw['paint']]
REPORT['carbon_tile_m'] = carbon_tile
refs = {n: O[n].matrix_world.translation.copy() for n in ('WheelColliderRef_FL', 'WheelColliderRef_FR', 'WheelColliderRef_RL', 'WheelColliderRef_RR', 'CenterOfMass') if n in O}
steer_hub = O['Steering_Wheel_LOD0'].matrix_world.translation.copy() if 'Steering_Wheel_LOD0' in O else None
save_ckp('zerogapr_01_intake.blend') if LAST >= 1 else None
# ================================================================ 02 cleanup: keep only what the remaster uses, convention mirror, topology clean, materials
CAT = {}
for c in bpy.data.collections:
    m = re.match(r'LOD(\d)_(\w+)$', c.name)
    if m:
        for o in c.objects: CAT[o.name] = (int(m.group(1)), m.group(2))
USE = {('Body', 0), ('Aero_Trim', 0), ('Lights', 1), ('Glass', 1)} | {(k, l) for k in ('Wheels', 'Tires', 'Brakes', 'Interior') for l in (1, 2, 3)}
PAN = ['Car_Body', 'Hood', 'Roof_Panel', 'Rear_Engine_Cover', 'Car_Door_L', 'Car_Door_R']           # paint panels: rebuilt from the master subdivision cages (level 0 + mirror + solidify)
CAGE = {}
for n in PAN:
    t = O[n].copy(); t.data = O[n].data.copy(); sc.collection.objects.link(t); t.hide_viewport = False; t.hide_render = False
    for m in t.modifiers:
        if m.type == 'SUBSURF': m.levels = m.render_levels = 0
    dg_ = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(t.evaluated_get(dg_)); me.transform(t.matrix_world); me.name = n + '_cage'; me.use_fake_user = True; CAGE[n] = me
    bpy.data.objects.remove(t, do_unlink=True)
br = O['Car_Body_LOD0'].copy(); br.data = O['Car_Body_LOD0'].data.copy(); sc.collection.objects.link(br); br.name = 'KEEP_BodyRef'   # open shell: front / rear opening edges for the fascias
dead = [o for o in O if not (o.name in CAT and (CAT[o.name][1], CAT[o.name][0]) in USE and o.type == 'MESH') and not o.name.startswith('KEEP_')]
REMOVE = re.compile(r'^(Front_(Bumper|Central_Intake|Cooling_Duct|Intake_Grille|Splitter|Duct_Guide|Nose_Shutline)|Splitter_Side_Return|Rear_(Bumper|Center_Recess|Diffuser|Vent_Rib)|Diffuser_Fin|Exhaust_|Taillight_)')
grille_src = O['Front_Intake_Grille_LOD0'].copy(); grille_src.data = grille_src.data.copy(); sc.collection.objects.link(grille_src); grille_src.name = 'KEEP_HexGrille'
removed = sorted(o.name for o in O if o.name in CAT and REMOVE.search(o.name) and (CAT[o.name][1], CAT[o.name][0]) in USE)
for o in dead + [O[n] for n in removed]: bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    for x in list(d):
        if x.users == 0: d.remove(x)
REPORT['removed_parts'] = removed
WORK = coll('ZG_WORK'); keep = [o for o in O]
for n in PAN:                                                                                     # swap the LOD0 panel meshes for the clean master cages
    o = O[n + '_LOD0']; o.matrix_world = Matrix.Identity(4); o.data = CAGE[n]; CAGE[n].use_fake_user = False
for o in keep:
    if not o.name.startswith('KEEP_'): o['src_lod'], o['cat'] = CAT[o.name][0], CAT[o.name][1]
    link_only(o, WORK)
REPORT['paint_panels'] = {n: 'master cage level 0 (mirror + solidify): %d tris' % sum(len(p.vertices) - 2 for p in CAGE[n].polygons) for n in PAN}
bpy.ops.object.select_all(action='DESELECT')
for o in keep:
    mw = o.matrix_world.copy(); o.parent = None
    if o.data.users > 1: o.data = o.data.copy()
    if o.get('cat') == 'Tires':                                                                 # tires: 180 deg about the vertical axis through the axle line (keeps sidewall text readable)
        cy = sum((mw @ Vector(b)).y for b in o.bound_box) / 8; o.matrix_world = Matrix.Translation((0, cy, 0)) @ Matrix.Rotation(math.pi, 4, 'Z') @ Matrix.Translation((0, -cy, 0)) @ mw
    else: o.matrix_world = Matrix.Scale(-1, 4, (1, 0, 0)) @ mw                                    # true X mirror: vehicle left becomes +X (project convention), driver to +X (LHD)
    o.select_set(True)
bpy.context.view_layer.objects.active = keep[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
refs = {k: Vector((-v.x, v.y, v.z)) for k, v in refs.items()}; steer_hub = Vector((-steer_hub.x, steer_hub.y, steer_hub.z)) if steer_hub else None
# the source labels were relative to its own (-X) left; after the true mirror the labels FL / RL / _L now sit on +X = project left. WheelColliderRef positions follow the geometry.
topo = dict(merged_verts=0, degenerate=0, loose=0)
for o in keep:
    bm = bmesh.new(); bm.from_mesh(o.data); n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5); topo['merged_verts'] += n0 - len(bm.verts)
    f0 = len(bm.faces); bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=1e-6); topo['degenerate'] += f0 - len(bm.faces)
    lv = [v for v in bm.verts if not v.link_edges]; topo['loose'] += len(lv); bmesh.ops.delete(bm, geom=lv, context='VERTS')
    bm.to_mesh(o.data); bm.free(); o.data.update()
REPORT['topology_cleanup'] = topo
M = build_materials(sw, tex)
EMIT_BY_NAME = [(r'Projector_Emitter', 'ZG_LED_Headlamp'), (r'DRL|SecondaryLED', 'ZG_LED_DRL')]
def remap(o):
    me = o.data; slots = [s.material.name if s.material else None for s in o.material_slots]; old = [p.material_index for p in me.polygons]
    tg = []
    for n in slots:
        if n in SRC2SW: tg.append(('ZG_Palette', SRC2SW[n]))
        elif n == 'MAT_EmissiveWhite_Engine': tg.append((next((m for k, m in EMIT_BY_NAME if re.search(k, o.name)), 'ZG_LED_DRL'), None))
        elif n in SRC2MAT: tg.append((SRC2MAT[n], None))
        elif n and n.startswith('MAT_CarPaint'): tg.append(('ZG_Paint', None))                                # master cages carry the original paint variant names
        else: tg.append(('ZG_Palette', 'black_plastic'))
    order = list(dict.fromkeys(t[0] for t in tg)) or ['ZG_Palette']
    me.materials.clear()
    for m in order: me.materials.append(M[m])
    if not tg: tg = [('ZG_Palette', 'black_plastic')]; old = [0] * len(old)
    me.polygons.foreach_set('material_index', [order.index(tg[i][0]) for i in old])
    a = me.attributes.get('swatch') or me.attributes.new('swatch', 'INT', 'FACE'); a.data.foreach_set('value', [SWATCH.index(tg[i][1]) if tg[i][1] else 0 for i in old])
REPORT['unmapped_source_materials'] = sorted({n for o in keep for n in [s_.material.name for s_ in o.material_slots if s_.material] if n not in SRC2SW and n not in SRC2MAT and not n.startswith(('MAT_CarPaint', 'MAT_EmissiveWhite'))})
for o in keep: remap(o)
PILLARS = re.compile(r'^(A_Pillar_[LR]|Roof_Rail_[LR]|Rear_Cabin_Pillar_[LR]|Window_B_Pillar_[LR])_LOD')
for o in keep:
    if PILLARS.search(o.name):                                                                    # blacked-out pillars / roof rails: read as glass frame, not exposed tubing
        o.data.materials.clear(); o.data.materials.append(M['ZG_Palette']); o.data.polygons.foreach_set('material_index', [0] * len(o.data.polygons)); set_swatch(o, 'gloss_black')
for b in [x for x in bpy.data.materials if not x.name.startswith('ZG_')]: bpy.data.materials.remove(b)
save_ckp('zerogapr_02_cleanup.blend') if LAST >= 2 else None
# ================================================================ 03 exterior
EXT = coll('ZG_EXTERIOR_NEW'); body = O['KEEP_BodyRef']
ff, frows = fascia(body, True, 80, 26, .17, -2.205, .016, EXT, M); rf, rrows = fascia(body, False, 80, 26, .30, 2.205, .012, EXT, M)
for o in (ff, rf): o['src_lod'], o['cat'] = 0, 'Body'
SF, SR = Surf(ff, True), Surf(rf, False)
def top_z(rows, x):
    r = sorted(((p.x, p.z) for p in rows[0]), key=lambda t: t[0]); return float(np.interp(x, [a for a, _ in r], [b for _, b in r]))
mir = lambda poly: [(-x, z) for x, z in poly][::-1]
gF = Geo(); cuts = []
central = rounded_poly([(-.36, .405), (.36, .405), (.44, .215), (-.44, .215)], .045)
side_r = rounded_poly([(.53, .432), (.785, .478), (.80, .245), (.555, .228)], [.04, .03, .03, .04])
for poly, depth in ((central, .10), (side_r, .075), (mir(side_r), .075)):
    c = opening(gF, SF, poly, depth, .02, ['ZG_Palette:gloss_black', 'ZG_Palette:housing'])
    if c: cuts.append(c)
for sx in (1, -1):                                                                                # side-intake vanes (carbon)
    for xv in (.625, .705):
        x = sx * xv; p0, n0 = SF.at(x, .34, 0)
        if p0 is None: continue
        for k, (a, b) in enumerate(((.010, .060),)):
            ys = [p0.y + a, p0.y + b]; zz = [.25, .445]; t = .005
            V = [(x - t, ys[0], zz[0]), (x + t, ys[0], zz[0]), (x + t, ys[1], zz[0]), (x - t, ys[1], zz[0]), (x - t, ys[0], zz[1]), (x + t, ys[0], zz[1]), (x + t, ys[1], zz[1]), (x - t, ys[1], zz[1])]
            n = len(gF.V); gF.V += V
            for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)): gF.F.append(tuple(n + i for i in f)); gF.FM.append('ZG_Carbon')
# front light signature: DRL blade under the lip + amber indicator line above each side intake
for sx in (1, -1):
    lo, hi = (.44, .79) if sx > 0 else (-.79, -.44)
    zt = lambda x: top_z(frows, x) - .028; zb = lambda x: zt(x) - (.010 + .009 * ss(.44, .79, abs(x)))
    ribbon(gF, SF, lo, hi, lambda x: zb(x) - .006, lambda x: zt(x) + .006, .0015, 'ZG_Palette:gloss_black', nx=36, nz=2)
    ribbon(gF, SF, lo + .01 * sx, hi - .006 * sx, zb, zt, .0035, 'ZG_LED_DRL', nx=36, nz=1)
    li, la = (.62, .79) if sx > 0 else (-.79, -.62); ind = 'ZG_LED_Indicator_L' if sx > 0 else 'ZG_LED_Indicator_R'
    zi = lambda x: .508 + .045 * ss(.62, .79, abs(x))
    ribbon(gF, SF, li, la, lambda x: zi(x) - .004, lambda x: zi(x) + .010, .0015, 'ZG_Palette:gloss_black', nx=14, nz=1)
    ribbon(gF, SF, li + .006 * sx, la - .004 * sx, lambda x: zi(x) - .0005, lambda x: zi(x) + .0065, .0035, ind, nx=14, nz=1)
cut_skin(ff, cuts)
# hex grille behind the central intake (source mesh, refitted)
g = O['KEEP_HexGrille']; pc, _ = SF.at(0, .31, 0)
bb = [g.matrix_world @ Vector(b) for b in g.bound_box]; cx = sum(p.x for p in bb) / 8; cz = sum(p.z for p in bb) / 8; cy = sum(p.y for p in bb) / 8
sxg = .80 / (max(p.x for p in bb) - min(p.x for p in bb)); szg = .175 / (max(p.z for p in bb) - min(p.z for p in bb))
g.data.transform(Matrix.Translation((0, pc.y + .075, .31)) @ Matrix.Diagonal((sxg, 1, szg, 1)) @ Matrix.Translation((-cx, -cy, -cz))); g.matrix_world = Matrix.Identity(4)
g.data.materials.clear(); g.data.materials.append(M['ZG_Palette']); g.data.polygons.foreach_set('material_index', [0] * len(g.data.polygons)); set_swatch(g, 'grille'); g.name = 'Front_HexGrille_LOD0'
link_only(g, EXT); g['src_lod'], g['cat'] = 0, 'Aero_Trim'
# splitter: slim carbon blade, 25 mm proud of the chin, flat underside tied into the chassis tray, small endplates
bot = sorted(((p.x, p.y) for p in frows[-1]), key=lambda t: t[0]); xs = [x for x in np.linspace(-.80, .80, 41)]
yf = [float(np.interp(x, [a for a, _ in bot], [b for _, b in bot])) - .025 for x in xs]
ztop, zbot, yback = .171, .157, -1.86
topR = [(x, y, ztop) for x, y in zip(xs, yf)]; botR = [(x, y - .004, zbot) for x, y in zip(xs, yf)]
gF.quad_strip([(x, yback, ztop) for x in xs], topR, 'ZG_Carbon'); gF.quad_strip(botR, [(x, yback, zbot) for x in xs], 'ZG_Carbon'); gF.quad_strip(topR, botR, 'ZG_Carbon')
for x, y in ((xs[0], yf[0]), (xs[-1], yf[-1])):
    V = [(x - .004, y, zbot), (x + .004, y, zbot), (x + .004, y + .22, zbot), (x - .004, y + .22, zbot), (x - .004, y + .03, .235), (x + .004, y + .03, .235), (x + .004, y + .22, .235), (x - .004, y + .22, .235)]
    n = len(gF.V); gF.V += V
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)): gF.F.append(tuple(n + i for i in f)); gF.FM.append('ZG_Carbon')
fdet = mk('Front_Details_LOD0', gF.V, gF.F, gF.FM, EXT, M); fdet['src_lod'], fdet['cat'] = 0, 'Aero_Trim'
# ---------------- rear: vent band with integrated exhausts, light units, centre bar, diffuser + fins
gR = Geo(); cutsR = []
band = rounded_poly([(-.80, .528), (.80, .528), (.80, .372), (-.80, .372)], .045)
c = opening(gR, SR, band, .065, .02, ['ZG_Palette:gloss_black', 'ZG_Palette:housing'])
if c: cutsR.append(c)
for zs in (.392, .508):                                                                           # slats
    pts = [(x, zs) for x in np.linspace(-.76, .76, 33)]; A = []; B = []
    for x, z in pts:
        p, n = SR.at(x, z, 0); A.append((x, p.y - .025, z + .004)); B.append((x, p.y - .025, z - .004))
    gR.quad_strip(A, B, 'ZG_Carbon'); gR.quad_strip([(x, y - .02, z) for x, y, z in A], A, 'ZG_Carbon')
for sx in (1, -1):                                                                                # exhaust tips through the band (not through the bumper side)
    cx, cz, r1, r2 = sx * .62, .45, .046, .039; p, n = SR.at(cx, cz, 0); y_out = p.y + .016; y_in = p.y - .10; seg = 20
    ringO = [(cx + r1 * math.cos(2 * math.pi * k / seg), y_out, cz + r1 * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    ringOi = [(x, y_in, z) for x, y, z in ringO]; ringI = [(cx + r2 * math.cos(2 * math.pi * k / seg), y_out, cz + r2 * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    ringIi = [(x, y_in + .02, z) for x, y, z in ringI]
    gR.quad_strip(ringOi, ringO, 'ZG_Palette:chrome', closed=True); gR.quad_strip(ringO, ringI, 'ZG_Palette:chrome', closed=True)
    gR.quad_strip(ringI, ringIi, 'ZG_Palette:exhaust_inner', closed=True); gR.fan(ringIi, (cx, y_in + .02, cz), 'ZG_Palette:exhaust_inner', flip=True)
# light units (vehicle left = +X -> indicator L)
for sx in (1, -1):
    s = lambda x: ss(.50, .84, abs(x)); taper = lambda x: .55 + .45 * ss(.15, .32, abs(x))                   # parallel strips (no converging 'X' read at the centre)
    zt = lambda x: .676 + taper(x) * (.022 + .030 * s(x)); zb = lambda x: .676 - taper(x) * (.020 + .042 * s(x))
    x0, x1 = (.15, .838) if sx > 0 else (-.838, -.15); ind = 'ZG_LED_Indicator_L' if sx > 0 else 'ZG_LED_Indicator_R'
    ribbon(gR, SR, x0, x1, zb, zt, .0015, 'ZG_Palette:housing', nx=48, nz=4)
    ribbon(gR, SR, x0 + .03 * sx, x1 - .012 * sx, lambda x: zt(x) - .011, lambda x: zt(x) - .004, .004, 'ZG_LED_Tail', nx=44, nz=1)
    ribbon(gR, SR, x0 + .06 * sx, x1 - .012 * sx, lambda x: zb(x) + .004, lambda x: zb(x) + .010, .004, 'ZG_LED_Tail', nx=44, nz=1)
    for a, b, mat in ((.30, .60, 'ZG_LED_Brake'), (.665, .80, ind), (.19, .27, 'ZG_LED_Reverse')):
        lo, hi = (a, b) if sx > 0 else (-b, -a)
        ribbon(gR, SR, lo, hi, lambda x: zb(x) + .016, lambda x: zt(x) - .016, .0035, mat, nx=14, nz=2)
    ribbon(gR, SR, x0, x1, zb, zt, .0075, 'ZG_LensRed', nx=48, nz=4, wall=1, wall_mat='ZG_Palette:gloss_black')
ribbon(gR, SR, -.15, .15, lambda x: .671, lambda x: .681, .004, 'ZG_LED_Tail', nx=16, nz=1)        # full-width signature bar
ribbon(gR, SR, -.152, .152, lambda x: .666, lambda x: .686, .0065, 'ZG_LensRed', nx=16, nz=1, wall=1, wall_mat='ZG_Palette:gloss_black')
cut_skin(rf, cutsR)
# diffuser (attached: rear edge on the fascia chin, front edge inside the chassis tray) + fins standing on it
bot = sorted(((p.x, p.y, p.z) for p in rrows[-1]), key=lambda t: t[0]); xs = list(np.linspace(-.80, .80, 33))
yb = lambda x: float(np.interp(x, [a for a, _, _ in bot], [b for _, b, _ in bot])); zb_ = lambda x: float(np.interp(x, [a for a, _, _ in bot], [c for _, _, c in bot]))
rows = []
for k in range(9):
    t = k / 8; rows.append([(x, lerp(yb(x) - .004, 1.74, t), lerp(zb_(x) - .004, .176, ss(0, 1, t) ** .9)) for x in xs])
gR.grid(rows, 'ZG_Carbon')
dz = lambda x, y: lerp(zb_(x) - .004, .176, ss(0, 1, (yb(x) - y) / (yb(x) - 1.74)) ** .9)
for xf in (-.55, -.22, .22, .55):
    ys = list(np.linspace(1.80, yb(xf) - .02, 10)); A = [(xf, y, dz(xf, y) - .002) for y in ys]; Bt = [(xf, y, .158) for y in ys]
    for off in (-.004, .004): gR.quad_strip([(x + off, y, z) for x, y, z in A], [(x + off, y, z) for x, y, z in Bt], 'ZG_Carbon', flip=off > 0)
    gR.quad_strip([(x - .004, y, z) for x, y, z in Bt], [(x + .004, y, z) for x, y, z in Bt], 'ZG_Carbon')
for xs_ in (-.80, .80):                                                                            # diffuser side plates: close the diffuser into one integrated unit
    ys = list(np.linspace(1.74, yb(xs_) - .004, 10)); top_ = [(xs_, y, dz(xs_, y) + .002) for y in ys]; bot_ = [(xs_, y, .158) for y in ys]
    for off in (-.005, .005): gR.quad_strip([(x + off, y, z) for x, y, z in top_], [(x + off, y, z) for x, y, z in bot_], 'ZG_Carbon', flip=off > 0)
    gR.quad_strip([(x - .005, y, z) for x, y, z in bot_], [(x + .005, y, z) for x, y, z in bot_], 'ZG_Carbon')
    gR.quad_strip([(x - .005, ys[-1], z) for x, y, z in [top_[-1], bot_[-1]]], [(x + .005, ys[-1], z) for x, y, z in [top_[-1], bot_[-1]]], 'ZG_Carbon')
rdet = mk('Rear_Details_LOD0', gR.V, gR.F, gR.FM, EXT, M); rdet['src_lod'], rdet['cat'] = 0, 'Aero_Trim'
for o in (fdet, rdet):
    o.data.update()
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free()
for o in (ff, rf, fdet, rdet):
    o.data.shade_smooth() if hasattr(o.data, 'shade_smooth') else None; o.data.set_sharp_from_angle(angle=math.radians(35))
# door skins: smooth the reflection field (custom normals transferred from a relaxed copy) -> removes the wavy highlights without moving geometry
def relaxed_normals(o, iters=25, factor=.9):
    ref = o.copy(); ref.data = o.data.copy(); WORK.objects.link(ref)
    m = ref.modifiers.new('relax', 'SMOOTH'); m.factor = factor; m.iterations = iters
    with bpy.context.temp_override(object=ref, active_object=ref): bpy.ops.object.modifier_apply(modifier='relax')
    o.data.shade_smooth(); dt = o.modifiers.new('nt', 'DATA_TRANSFER'); dt.object = ref; dt.use_loop_data = True; dt.data_types_loops = {'CUSTOM_NORMAL'}; dt.loop_mapping = 'POLYINTERP_NEAREST'
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='nt')
    bpy.data.objects.remove(ref, do_unlink=True)
bpy.data.objects.remove(O['KEEP_BodyRef'], do_unlink=True)
for n in PAN: O[n + '_LOD0'].data.shade_smooth()
json.dump(REPORT, open(P('reports', 'ZG_build_log.json'), 'w'), indent=1)
save_ckp('zerogapr_03_exterior.blend') if LAST >= 3 else None
if LAST <= 3: sys.exit(0)

# ================================================================ 04 wheels / tires / brakes (per LOD source: target LOD0..3 <- source LOD1, 2, 3, 3)
WHEELS = coll('ZG_WHEELS'); CORNER = re.compile(r'_(FL|FR|RL|RR)(?=_|$)')
def join(objs, name, c):
    objs = [o for o in objs if o and o.type == 'MESH']
    if not objs: return None
    for o in objs: link_only(o, c)
    a = objs[0]
    if len(objs) > 1:
        with bpy.context.temp_override(active_object=a, object=a, selected_objects=objs, selected_editable_objects=objs): bpy.ops.object.join()
    a.name = name; a.data.name = name; return a
def set_origin(o, p):
    p = Vector(p); o.data.transform(Matrix.Translation(-p)); o.matrix_world = Matrix.Translation(p)
WREF = {c: refs[f'WheelColliderRef_{c}'] for c in ('FL', 'FR', 'RL', 'RR')}
SRCMAP = {0: 1, 1: 2, 2: 3, 3: 3}
ASM = {}
unmatched = []
for k, sl in SRCMAP.items():
    for corner in ('FL', 'FR', 'RL', 'RR'):
        part = lambda cat, f=lambda n: True: [o for o in list(O) if o.get('cat') == cat and o.get('src_lod') == sl and not o.get('asm') and CORNER.search(o.name) and CORNER.search(o.name).group(1) == corner and f(o.name)]
        groups = {'Wheel': part('Wheels'), 'Tire': part('Tires'), 'BrakeDisc': part('Brakes', lambda n: 'Caliper' not in n), 'Caliper': part('Brakes', lambda n: 'Caliper' in n)}
        for key, objs in groups.items():
            if sl != k + 1 and k != 3:
                objs = [o for o in objs]
            if k == 3 and sl == 3:                                                                 # LOD3 reuses source LOD3: duplicate (LOD2 already consumed the originals)
                objs = [o for o in objs]
            dup = []
            for o in objs:
                d = o.copy(); d.data = o.data.copy(); WHEELS.objects.link(d); dup.append(d)
            j = join(dup, f'{key}_{corner}_LOD{k}', WHEELS)
            if j: set_origin(j, WREF[corner]); ASM[(k, corner, key)] = j; j['asm'] = 1                 # assembled: never re-used as a source part
    for o in [o for o in O if o.get('cat') in ('Wheels', 'Tires', 'Brakes') and o.get('src_lod') == sl and not CORNER.search(o.name)]: unmatched.append(o.name)
REPORT['wheel_parts_without_corner'] = sorted(set(unmatched))
save_ckp('zerogapr_04_wheels.blend') if LAST >= 4 else None
# ================================================================ 05 glass, lights, interior
def split_faces(o, pred, name):
    """move faces whose material name satisfies pred into a new object."""
    me2 = o.data.copy(); n = bpy.data.objects.new(name, me2); o.users_collection[0].objects.link(n); n.matrix_world = o.matrix_world.copy()
    for ob, keep_pred in ((o, lambda m: not pred(m)), (n, pred)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        dead = [f for f in bm.faces if not keep_pred(mats[f.material_index].name if mats[f.material_index] else '')]
        bmesh.ops.delete(bm, geom=dead, context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    return n
is_light = lambda m: m.startswith('ZG_LED_') or m in ('ZG_LensClear', 'ZG_LensRed')
fl = split_faces(O['Front_Details_LOD0'], is_light, 'Front_Lights_LOD0'); rl = split_faces(O['Rear_Details_LOD0'], is_light, 'Rear_Lights_LOD0')
for o in (fl, rl): o['src_lod'], o['cat'] = 0, 'Lights'
INT = coll('ZG_INTERIOR')
for k, sl in SRCMAP.items():
    src = [o for o in O if o.get('cat') == 'Interior' and o.get('src_lod') == sl and not o.get('asm')]
    sw_parts = [o for o in src if re.search(r'Steering_Wheel|Paddle|Horn', o.name)]; rest = [o for o in src if o not in sw_parts]
    for nm, objs in ((f'Interior_LOD{k}', rest), (f'SteeringWheel_LOD{k}', sw_parts)):
        if k == 3 and nm.startswith('Steering'): continue                                             # no steering wheel at LOD3
        dup = []
        for o in objs:
            d = o.copy(); d.data = o.data.copy(); INT.objects.link(d); dup.append(d)
        j = join(dup, nm, INT)
        if j: j['asm'] = 1
        if j and nm.startswith('Steering') and steer_hub: set_origin(j, steer_hub)
save_ckp('zerogapr_05_glass_lights_interior.blend') if LAST >= 5 else None
# ================================================================ 06 merge LOD0 + budget reduction + UVs
def decimate(o, ratio, ref=None, sym=True, unsub=0, transfer=True):
    """reduce keeping the original shading: custom normals transferred back from the pre-reduction surface.
    unsub > 0: un-subdivide n times (regular quad panels: clean topology); else collapse to `ratio`."""
    if ratio >= .999 and not unsub: return o
    src = ref or o.copy()
    if ref is None: src.data = o.data.copy(); WORK.objects.link(src)
    m = o.modifiers.new('dec', 'DECIMATE')
    if unsub: m.decimate_type = 'UNSUBDIV'; m.iterations = unsub
    else: m.decimate_type = 'COLLAPSE'; m.ratio = ratio; m.use_symmetry = sym; m.symmetry_axis = 'X'; m.use_collapse_triangulate = True
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='dec')
    if transfer:
        o.data.shade_smooth(); dt = o.modifiers.new('nt', 'DATA_TRANSFER'); dt.object = src; dt.use_loop_data = True; dt.data_types_loops = {'CUSTOM_NORMAL'}; dt.loop_mapping = 'POLYINTERP_NEAREST'
        with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='nt')
    else:                                                                                           # heavy reductions: own smooth normals + angle-based hard edges (transferred normals mottle)
        with bpy.context.temp_override(object=o, active_object=o): bpy.ops.mesh.customdata_custom_splitnormals_clear()
        o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(38))
    if ref is None: bpy.data.objects.remove(src, do_unlink=True)
    bm = bmesh.new(); bm.from_mesh(o.data); seen, dups = set(), []
    for f in bm.faces:
        key_ = frozenset(v.index for v in f.verts); (dups.append(f) if key_ in seen else seen.add(key_))
    bmesh.ops.delete(bm, geom=dups, context='FACES_ONLY'); bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_area() < 1e-9], context='FACES_ONLY'); bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return o
L0 = coll('LOD0_PARTS')
def grab(pred): return [o for o in list(O) if o.get('src_lod') is not None and o.get('cat') and pred(o)]
door = lambda side: grab(lambda o: o.get('cat') in ('Body', 'Aero_Trim') and re.search(rf'^(Car_Door_{side}|Door_Handle_FlushBlade_{side}|Door_Handle_Recess_{side})_LOD0', o.name) is not None)
D_L, D_R = door('L'), door('R')
body = grab(lambda o: o.get('cat') == 'Body' and o not in D_L + D_R)
lights = grab(lambda o: o.get('cat') == 'Lights')
glass = grab(lambda o: o.get('cat') == 'Glass')
trim = grab(lambda o: o.get('cat') == 'Aero_Trim' and o not in D_L + D_R)
BODY_COLLAPSE = {0: 1.0, 1: .5, 2: .24, 3: .085}; DOOR = {0: 1.0, 1: .5, 2: .25, 3: .1}
def lod_copy(o, k, coll_):
    d = o.copy(); d.data = o.data.copy(); coll_.objects.link(d)
    decimate(d, BODY_COLLAPSE[k] if o in body else DOOR[k], ref=o, transfer=k <= 1)                                  # LOD0 = untouched; LOD1-3 collapse with LOD0 normals transferred
    return d
BODYK, DLK, DRK = {}, {}, {}
for k in range(4):
    Lk = L0 if k == 0 else coll(f'LOD{k}_PARTS')
    BODYK[k] = join([lod_copy(o, k, Lk) for o in body], f'Body_LOD{k}', Lk)
    DLK[k] = join([lod_copy(o, k, Lk) for o in D_L], f'Door_L_LOD{k}', Lk); DRK[k] = join([lod_copy(o, k, Lk) for o in D_R], f'Door_R_LOD{k}', Lk)
for o in body + D_L + D_R: bpy.data.objects.remove(o, do_unlink=True)
FINAL0 = {'Body_LOD0': BODYK[0], 'Door_L_LOD0': DLK[0], 'Door_R_LOD0': DRK[0],
          'Trim_LOD0': join(trim, 'Trim_LOD0', L0), 'Lights_LOD0': join(lights, 'Lights_LOD0', L0), 'Glass_LOD0': join(glass, 'Glass_LOD0', L0)}
INTK = {o.name.split('.')[0]: o for o in O if o.get('asm') and o.get('cat') == 'Interior'}
keepset = set(ASM.values()) | set(INTK.values())
for o in list(O):                                                                                   # consumed source parts of the wheel / interior groups
    if o.get('cat') in ('Wheels', 'Tires', 'Brakes', 'Interior') and o not in keepset: bpy.data.objects.remove(o, do_unlink=True)
for (k, c, key), o in ASM.items(): o.name = f'{key}_{c}_LOD{k}'; o.data.name = o.name                # canonical names (source part names no longer collide)
for n, o in INTK.items(): o.name = n; o.data.name = n
R0 = {'Body_LOD0': 1.0, 'Door_L_LOD0': 1.0, 'Door_R_LOD0': 1.0, 'Trim_LOD0': .57, 'Lights_LOD0': .85, 'Glass_LOD0': 1.0}
for n, r in R0.items():
    if FINAL0[n]: decimate(FINAL0[n], r)
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        if k == 0 and (0, c, 'Wheel') in ASM: decimate(ASM[(0, c, 'Wheel')], .72, sym=False)
    if k == 0 and 'Interior_LOD0' in O: decimate(O['Interior_LOD0'], .55)
for o in [x for x in O if x.type == 'MESH']:
    final_uvs(o, carbon_tile)
REPORT['lod0_budget_ratios'] = R0
save_ckp('zerogapr_06_materials_uv.blend') if LAST >= 6 else None
# ================================================================ 07 LODs (exterior shell decimated from LOD0 with LOD0 normals; wheels / tires / brakes / interior from the source LOD chain)
RK = {1: {'Body': .45, 'Door': .45, 'Trim': .42, 'Lights': .5, 'Glass': .65},
      2: {'Body': .17, 'Door': .2, 'Trim': .17, 'Lights': .24, 'Glass': .42},
      3: {'Body': .055, 'Door': .08, 'Trim': .045, 'Lights': .08, 'Glass': .22}}
for k in (1, 2, 3):
    Lk = coll(f'LOD{k}_PARTS')
    for o in (BODYK[k], DLK[k], DRK[k]): final_uvs(o, carbon_tile)
    for n0, o0 in FINAL0.items():
        if not o0 or n0.startswith(('Body_', 'Door_')): continue
        kind = n0.split('_')[0]; kind = 'Door' if kind == 'Door' else kind
        d = o0.copy(); d.data = o0.data.copy(); Lk.objects.link(d); d.name = n0.replace('LOD0', f'LOD{k}'); d.data.name = d.name
        decimate(d, RK[k][kind], ref=o0, transfer=k <= 1)
    if k == 3:
        for c in ('FL', 'FR', 'RL', 'RR'):
            for key, r in (('Wheel', .30), ('Tire', .32)):
                if (3, c, key) in ASM: decimate(ASM[(3, c, key)], r, sym=False)
            bd = ASM.get((2, c, 'BrakeDisc')); w3 = ASM.get((3, c, 'Wheel'))
            if bd and w3:                                                                          # LOD3: brake hardware replaced by one 16-gon rotor disc inside the wheel (keeps the solid wheel read)
                lv = np.array([v.co[:] for v in bd.data.vertices]); rad = float(np.sqrt(lv[:, 1] ** 2 + lv[:, 2] ** 2).max()) * .98; xc = float(lv[:, 0].mean())
                names = [m.name for m in w3.data.materials]
                if 'ZG_Palette' not in names: w3.data.materials.append(M['ZG_Palette']); names.append('ZG_Palette')
                mi = names.index('ZG_Palette'); nf0 = len(w3.data.polygons)
                bm = bmesh.new(); bm.from_mesh(w3.data); n = 16; ring = [bm.verts.new((xc, rad * math.cos(2 * math.pi * i / n), rad * math.sin(2 * math.pi * i / n))) for i in range(n)]
                ctr = bm.verts.new((xc, 0, 0))
                for i in range(n):
                    tri = (ring[i], ring[(i + 1) % n], ctr); f = bm.faces.new(tri if xc > 0 else tri[::-1]); f.material_index = mi
                bm.to_mesh(w3.data); bm.free(); sa = w3.data.attributes['swatch']
                for i in range(nf0, len(w3.data.polygons)): sa.data[i].value = SWATCH.index('rotor')
                final_uvs(w3, carbon_tile)
            for key in ('BrakeDisc', 'Caliper'):                                                  # no separate brake hardware at LOD3
                if (3, c, key) in ASM: bpy.data.objects.remove(ASM.pop((3, c, key)), do_unlink=True)
        if 'Interior_LOD3' in O: decimate(O['Interior_LOD3'], .20)
    if k == 1 and 'Interior_LOD1' in O: decimate(O['Interior_LOD1'], .6)
REPORT['lod_ratios'] = RK
save_ckp('zerogapr_07_lods.blend') if LAST >= 7 else None
# ================================================================ 08 colliders, hierarchy, pivots, references
for c in list(bpy.data.collections):
    if c.name.startswith(('ZG_', 'LOD')) and c.name != 'ZG_FINAL': pass
FIN = coll('ZERO_GAP_R'); COLL = coll('ZG_COLLIDERS', FIN)
root = empty('Car_Root', FIN, (0, 0, 0), None, 'PLAIN_AXES', .5)
for k in range(4):
    lr = empty(f'LOD{k}_Root', FIN, (0, 0, 0), root, 'PLAIN_AXES', .3)
    names = [f'Body_LOD{k}', f'Door_L_LOD{k}', f'Door_R_LOD{k}', f'Trim_LOD{k}', f'Lights_LOD{k}', f'Glass_LOD{k}', f'Interior_LOD{k}', f'SteeringWheel_LOD{k}']
    for n in names:
        o = O.get(n)
        if not o: continue
        link_only(o, FIN)
        if not n.startswith(('Door_', 'SteeringWheel')): set_origin(o, (0, 0, 0))                    # static parts: pivot at the car origin
        mw = o.matrix_world.copy(); o.parent = lr; o.matrix_world = mw
        if n.startswith('Door_'):                                                                  # hinge pivot: front edge of the door, mid height
            vs = [o.matrix_world @ v.co for v in o.data.vertices]; set_origin(o, (sum(v.x for v in vs) / len(vs), min(v.y for v in vs), (min(v.z for v in vs) + max(v.z for v in vs)) / 2))
            mw = o.matrix_world.copy(); o.parent = lr; o.matrix_world = mw
    for c in ('FL', 'FR', 'RL', 'RR'):
        w = ASM.get((k, c, 'Wheel'))
        if not w: continue
        parent = lr
        if c in ('FL', 'FR'): parent = empty(f'SteerPivot_{c}_LOD{k}', FIN, WREF[c], lr, 'ARROWS', .15); bpy.context.view_layer.update()
        for key in ('Wheel', 'Tire', 'BrakeDisc', 'Caliper'):
            o = ASM.get((k, c, key))
            if o: link_only(o, FIN)
        local = Matrix.Identity(4) if parent is not lr else Matrix.Translation(WREF[c])               # pivots sit at the wheel centre
        w.parent = parent; w.matrix_parent_inverse = Matrix.Identity(4); w.matrix_basis = local
        for key in ('Tire', 'BrakeDisc'):
            o = ASM.get((k, c, key))
            if o: o.parent = w; o.matrix_parent_inverse = Matrix.Identity(4); o.matrix_basis = Matrix.Identity(4)
        cal = ASM.get((k, c, 'Caliper'))
        if cal: cal.parent = parent; cal.matrix_parent_inverse = Matrix.Identity(4); cal.matrix_basis = local
        bpy.context.view_layer.update()
# colliders: convex hulls of the LOD3 exterior split into front / body / cabin / rear
def hull(name, verts):
    """convex hull of a voxel-thinned point set (grid grows until the hull is <= 200 triangles): always closed and convex."""
    cell = .05
    while True:
        pts = list({(round(v.x / cell), round(v.y / cell), round(v.z / cell)): v for v in verts}.values())
        bm = bmesh.new(); vv = [bm.verts.new(v) for v in pts]; r = bmesh.ops.convex_hull(bm, input=vv)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bmesh.ops.triangulate(bm, faces=bm.faces); bm.normal_update()
        bm.normal_update(); convex = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 5e-4 for v in bm.verts) for f in bm.faces)
        if (len(bm.faces) <= 200 and convex) or cell > .4: break
        bm.free(); cell *= 1.3
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); COLL.objects.link(o); o.display_type = 'WIRE'; return o
shell = [O[f'{n}_LOD3'].matrix_world @ v.co for n in ('Body', 'Door_L', 'Door_R', 'Trim') if O.get(f'{n}_LOD3') for v in O[f'{n}_LOD3'].data.vertices]
gl = [O['Glass_LOD3'].matrix_world @ v.co for v in O['Glass_LOD3'].data.vertices] if O.get('Glass_LOD3') else []
pts = shell + gl
CL = {'Collision_Front': [p for p in pts if p.y < -1.05 and p.z < .95], 'Collision_Body': [p for p in pts if -1.25 < p.y < 1.25 and p.z < .80],
      'Collision_Cabin': [p for p in pts if -1.05 < p.y < 1.15 and p.z > .70], 'Collision_Rear': [p for p in pts if p.y > 1.05 and p.z < 1.0]}
cr = empty('Collision', FIN, (0, 0, 0), root, 'PLAIN_AXES', .2)
for n, vs in CL.items():
    if len(vs) > 8: h = hull(n, vs); h.parent = cr
for c in ('FL', 'FR', 'RL', 'RR'):
    e = empty(f'WheelColliderRef_{c}', FIN, WREF[c], root, 'SPHERE', .1); front = c[0] == 'F'
    e['radius_m'] = .3445 if front else .3645; e['width_m'] = .296 if front else .336
com = empty('CenterOfMass', FIN, refs['CenterOfMass'], root, 'SPHERE', .08)
for c in list(bpy.data.collections):                                                               # drop work collections and anything not in the final hierarchy
    if c.name not in ('ZERO_GAP_R', 'ZG_COLLIDERS'): 
        for o in list(c.objects):
            if o.name not in FIN.all_objects: bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
json.dump(REPORT, open(P('reports', 'ZG_build_log.json'), 'w'), indent=1)
save_ckp('zerogapr_08_colliders_hierarchy.blend') if LAST >= 8 else None
