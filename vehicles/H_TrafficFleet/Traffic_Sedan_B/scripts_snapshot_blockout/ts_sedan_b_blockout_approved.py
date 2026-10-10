# Traffic_Sedan_B — premium executive sedan (Phase H traffic fleet, vehicle 2). ORIGINAL fictional design; reuses the Sedan A r3 technical
# systems (loft cage + designed end surfaces + r3 root-cause fixes, high-to-low bake, shared library, LODs, rig, validation) — NOT its body.
# Art direction: reports/TS_SedanB_ART_DIRECTION.md (class references: E-Class W214 / 5 Series G60 / Genesis G80 published dimensions).
#   env TS_BLOCKOUT=1: design blockout (no bakes, no stage checkpoints) -> blend/trafficsedanb_01_blockout.blend; TS_NOCKP=1 skips stage checkpoints.
# Sedan A r3 header (systems):
#   Blender -b --factory-startup --python ts_sedan_a.py [-- <last stage 2..8>]      env TS_SCRATCH=<dir> for trial runs
# Method (TRAFFIC_REALISM_STANDARDS.md §2): high-res master (cage level 3 + real openings + panel-gap grooves) -> decimated, uniquely unwrapped
# low-poly game body with baked tangent-space normals (+ AO / grime later). Real-world compact-sedan proportions; constructed (creased) front and
# rear faces; recessed lamps with housings, reflectors, projector and light guides under surface-following lenses; inset glass with seals + frit.
#  02 body (master, game body, bake)  03 exterior parts + lights + glass  04 wheels  05 interior  06 merge, UVs, AO / grime bake  07 LODs (+ LOD1 bake)  08 rig
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from ts_lib import *
VEH = 'Traffic_Sedan_B'; PRE = 'TS_SedanB'; ROOT = vroot(VEH); CKP_ = 'trafficsedanb'
LAST = int(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else 8
def OUTD(*a):
    d = os.path.join(SCR, *a[:-1]) if SCR else os.path.join(ROOT, *a[:-1]); os.makedirs(d, exist_ok=True); return os.path.join(d, a[-1])
BLOCKOUT = bool(os.environ.get('TS_BLOCKOUT'))
def save_ckp(name):
    if os.environ.get('TS_NOCKP') or BLOCKOUT: return
    path = OUTD('blend', name); assert SCR or not os.path.exists(path), 'checkpoint exists: ' + path
    bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=path, copy=True, relative_remap=True); print('SAVED', path, flush=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'
REPORT = {}
# ================================================================ design (metres) — premium executive sedan (class refs: L 4.95-5.06, W 1.88-1.93, H 1.47-1.52, WB 2.96-3.01)
# RWD premium proportions: short front overhang, LONG dash-to-axle (cowl ~0.98 m behind the front axle), cab-rearward greenhouse, longer rear overhang,
# flush 19" wheels on wide tracks, high crisp shoulder from headlamp to tail lamp, lower rocker sculpt, upright recessed grille, slim lamps.
DIM = dict(length=4.98, width_body=1.89, height=1.47, wheelbase=2.97, track_f=1.625, track_r=1.640, overhang_f=.86, overhang_r=1.15, ground_clearance=.14, tire='245/40 R20 (R 0.352, rim 20")')
YF, YR = -1.62, 1.35; RW = .352; WT = .245; RIM = .254; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.48, 2.50
COWL = -.74                                                                                             # windshield base: dash-to-axle 0.88 m (Sedan A: 0.37 m)
# side profile: nose -> hood leading edge (high, upright face) -> long flat hood -> cowl -> 30 deg windshield -> roof peak over the B-pillar -> fast rear glass -> short deck -> crisp lip
ZC = pchip([YN, -2.38, -2.25, -1.90, -1.62, -1.20, COWL, -.40, -.05, .25, .55, .85, 1.12, 1.45, 1.78, 2.10, 2.38, YT], [.60, .800, .835, .872, .898, .930, .975, 1.220, 1.425, 1.462, 1.468, 1.458, 1.420, 1.245, 1.085, 1.092, 1.100, 1.040])   # long flat roof crown
_YS = [YN, -2.35, -1.95, -1.62, -1.10, -.40, .40, 1.10, 1.60, 2.05, 2.35, YT]
ZBELT = pchip(_YS, [.70, .800, .860, .885, .905, .925, .950, .975, .990, 1.000, .990, .950])            # shoulder / belt: rises gently rearward (wedge)
WBELT = pchip(_YS, [.80, .872, .893, .898, .890, .886, .888, .895, .898, .893, .878, .835])
WMAX = pchip(_YS, [.86, .915, .938, .946, .938, .936, .938, .944, .946, .940, .925, .885])               # 1.89 m body; widest over the wheels (flush 19" fitment)
ZSH = pchip([YN, YF, 0, YR, YT], [.52, .64, .67, .68, .62])                                 # max width high (modern, no pear section)
ZFLOOR = pchip([YN, -2.30, -2.05, 2.05, 2.30, YT], [.30, .23, .150, .150, .23, .32])
WFLOOR = pchip([YN, -2.3, 0, 2.3, YT], [.64, .80, .84, .80, .68])
CAB = lambda y: ss(COWL - .14, COWL + .06, y) * (1 - ss(1.62, 1.84, y))
ROOFW = pchip([COWL, -.30, .20, .70, 1.10, 1.78], [.750, .715, .700, .690, .665, .635])
SK = lambda y: .024 * ss(-1.20, -1.00, y) * (1 - ss(.92, 1.12, y))                                      # lower rocker sculpt (concave band, rises rearward with ZSH)
def ring_half(y):
    zb, wf, wm, zs, zb_, wb, zc, c = ZFLOOR(y), WFLOOR(y), WMAX(y), ZSH(y), ZBELT(y), WBELT(y), ZC(y), CAB(y); sk = SK(y)
    side = [(0.0, zb), (.5 * wf, zb), (wf, zb + .006), (wm - .040 - sk * .3, zb + .075), (wm - .010 - sk, lerp(zb + .075, zs, .5)), (wm, zs), (lerp(wm, wb, .45), lerp(zs, zb_, .55)), (wb, zb_)]
    crown = lambda t: zb_ + (zc - zb_) * (1 - (1 - t) ** 2.2)
    rw = ROOFW(min(max(y, COWL), 1.78)); sw = wb - .05
    gh = [(wb - .035, zb_ + .008), (sw, zb_ + .028), (lerp(sw, rw, .82) + .008, lerp(zb_ + .028, zc - .065, .92)), (rw, zc - .032), (.50 * rw, zc - .007), (0.0, zc)]
    w = ss(1.10, 1.70, y)                                                                                # Raven P0 rule: rear deck points at the greenhouse x (pure vertical fade)
    ts = [lerp(t, min(max(1 - g[0] / wb, 0.0), 1.0), w) for t, g in zip((.08, .26, .50, .74, .90, 1.0), gh)]
    deck = [(wb * (1 - t), crown(t)) for t in ts]
    top = [(lerp(d[0], g[0], c), lerp(d[1], g[1], c)) for d, g in zip(deck, gh)]
    return side + top
NS = len(ring_half(0.0)); I_ROOF = 11
STAT = [round(v, 3) for v in np.linspace(-1.96, 2.08, 21)]   # loft stations (ends are dedicated surfaces)
def full_ring(y, scale=1.0, centre=None):
    h = ring_half(y); cz = centre if centre is not None else (h[0][1] + h[-1][1]) * .5
    pts = [(x * scale, y, cz + (z - cz) * scale) for x, z in h]
    return pts + [(-x, yy, z) for x, yy, z in pts[1:-1]][::-1]
NR = len(full_ring(0.0)); col_tag = lambda j: j if j < NS else NR - j
# ---- r2 END SURFACES. Each end = a designed face y = Yface(x, z) (side profile pchip + plan curvature), joined to the loft by a controlled-radius
#      corner (quarter circle, radius by outline direction: side / top / bottom), shallow inward-offset rings (corner), then rings scaled toward the
#      face centre, closed by a quad bridge (no fan pole, no folds).
YC_R = pchip([.20, .26, .34, .45, .58, .64, .69, .82, .95, 1.05, 1.10], [2.40, 2.45, 2.48, 2.495, 2.492, 2.486, 2.465, 2.468, 2.462, 2.448, 2.43])   # rear: valance, bumper (proud 2 cm, ledge .64-.69), trunk face, crisp lip
YC_F = pchip([.16, .22, .30, .42, .55, .65, .72, .78, .82], [-2.36, -2.42, -2.455, -2.475, -2.48, -2.476, -2.464, -2.442, -2.418])   # front: chin, intake, upright grille face, hood leading edge
E_ = lambda k, d: float(os.environ.get(k, d))
RS_R = pchip([.20, .34, .50, .66, .80, 1.10], [.075, .077, .080, .082, .085, .088])          # plan corner radius by height (tight bumper corners)
RS_F = pchip([.16, .30, .48, .58, .70, .84], [.072, .074, .078, .082, .088, .095])               # crisp front plan corners (no pillow nose)
END = {'R': dict(sgn=1, ysec=2.32, Yc=YC_R, plan=.06, Rs=RS_R, Rt=.020, Rb=.080, d=(.12, .025), sc=(.982, .94, .84, .58, .24)),
       'F': dict(sgn=-1, ysec=-2.30, Yc=YC_F, plan=.08, Rs=RS_F, Rt=.022, Rb=.065, d=(.12, .025), sc=(.982, .94, .84, .56, .22))}
CREASE_W = pchip([.020, .030, .050, .080, .120, .160], [.92, .85, .60, .36, .24, .20])                 # r3: continuous edge-ring crease weight from the (smoothed) corner radius
ENDR = {}
def outline_normals(ring):
    P = [Vector((x, z)) for x, _, z in ring]; n = len(P); c = sum(P, Vector((0, 0))) / n; out = []
    for i in range(n):
        tg = P[(i + 1) % n] - P[i - 1]; nn = Vector((tg.y, -tg.x)).normalized()
        if nn.dot(c - P[i]) < 0: nn = -nn
        out.append(nn)                                                                                  # inward 2D normal (x, z)
    return out
def corner_R(e, nin, z):
    """corner radius from the outline direction: side-facing -> Rs(z), top -> Rt, bottom -> Rb."""
    ax, az = abs(nin.x), nin.y; return e['Rs'](z) * ax + (e['Rt'] if az < 0 else e['Rb']) * abs(az)
def yplane(e, x, z): return e['Yc'](z) - e['sgn'] * e['plan'] * (x / .9) ** 2
def end_rings(e, edge):
    """edge = faired outline ring (NR pts, x, z). returns (d rings far->near, edge ring, cap rings near->inner) with designed y."""
    nin = outline_normals(edge); R = [corner_R(e, n, p[2]) for n, p in zip(nin, edge)]; sg = e['sgn']
    for _ in range(int(E_('TS_RSMOOTH', 8))): R = [(R[i - 1] + 2 * R[i] + R[(i + 1) % len(R)]) / 4 for i in range(len(R))]   # smooth radius changes along the outline (no lip ripple at the corners)
    ENDR[e['sgn']] = R                                                                                 # the crease weights use the same smoothed radius (r2 used the raw one -> steps)
    mk = lambda pts: [tuple(p) for p in pts]
    DW = {e['d'][0]: E_('TS_DW0', .25), e['d'][1]: E_('TS_DW1', .75)}                                 # r3: blend rings carry the loft section AT THEIR OWN y, eased toward the end outline
    def dpt(i, x, z, d):                                                                               # (r2 copied the end outline -> hood-corner / lower-corner bumps)
        y_ = yplane(e, x, z) - sg * (R[i] + d); xs, _, zs = full_ring(y_)[i]; w = DW[d]; xq, zq = lerp(xs, x, w), lerp(zs, z, w)
        return (xq, yplane(e, xq, zq) - sg * (R[i] + d), zq)
    drings = [mk([dpt(i, x, z, d) for i, (x, _, z) in enumerate(edge)]) for d in e['d']]
    ering = mk([(x, yplane(e, x, z) - sg * R[i], z) for i, (x, _, z) in enumerate(edge)])
    zs_ = [z for _, _, z in edge]; zc_ = (min(zs_) + max(zs_)) / 2; caps = []
    for s_ in e['sc']:                                                                                 # scale toward the face centre (star-shaped outline: cannot fold)
        r_ = []
        for i, (x, _, z) in enumerate(edge):
            d_ = (1 - s_) * math.hypot(x, z - zc_); pull = R[i] - math.sqrt(max(0.0, R[i] ** 2 - (R[i] - min(d_, R[i])) ** 2))
            xq, zq = x * s_, zc_ + (z - zc_) * s_; r_.append((xq, yplane(e, xq, zq) - sg * pull, zq))
        caps.append(r_)
    return drings, ering, caps
ef = full_ring(END['F']['ysec']); er = full_ring(END['R']['ysec'])
dF, eF, cF = end_rings(END['F'], ef); dR, eR, cR = end_rings(END['R'], er)
RAW = [eF] + dF[::-1] + [full_ring(y) for y in STAT] + dR + [eR]                                        # front edge ... loft ... rear edge
def fair_cage(rings, iters=30, lam=.5, mu=-.53, fixed=2):
    R = np.array(rings, float); n = len(R)
    for it in range(iters):
        for f in (lam, mu):
            L = np.zeros_like(R); L[1:-1] = (R[:-2] + R[2:]) * .5 - R[1:-1]; L[:fixed] = 0; L[n - fixed:] = 0; L[..., 1] = 0; R = R + f * L
    return [[tuple(p) for p in r] for r in R]
def fair_lateral(rings, iters=12, lam=.45, mu=-.48, lock=3):
    out = []
    for r in rings:
        R = np.array(r, float); n = len(R); fix = set(range(lock)) | set(range(n - lock + 1, n)) | {7, n - 7}
        if CAB(r[0][1]) > .05: fix |= set(range(8, n - 7))                                               # designed greenhouse stays exact (Pulse EV lesson)
        for it in range(iters):
            for f in (lam, mu):
                L = (np.roll(R, 1, 0) + np.roll(R, -1, 0)) * .5 - R; L[list(fix)] = 0; L[:, 1] = 0; R = R + f * L
        R[NS - 1, 0] = 0.0; out.append([tuple(p) for p in R])
    return out
FAIRED = fair_lateral(fair_cage(RAW))
dF, eF, cF = end_rings(END['F'], [(x, 0, z) for x, _, z in FAIRED[0]]); dR, eR, cR = end_rings(END['R'], [(x, 0, z) for x, _, z in FAIRED[-1]])   # end surfaces from the faired outline
FAIRED = [eF] + dF[::-1] + FAIRED[1 + len(dF):len(FAIRED) - 1 - len(dR)] + dR + [eR]
RINGS = cF[::-1] + FAIRED + cR
I_FRONTFACE = len(cF); I_REARFACE = len(cF) + len(FAIRED) - 1
def fair_columns(rings, idx, iters=int(E_('TS_CFAIR', 40)), lam=.5, mu=-.53):
    """r3: chord-weighted Taubin fairing of x, z ALONG each cage column across the end transition (faired loft rings -> designed blend rings).
    r2 had 3-7 mm kinks there (e.g. lower bumper side x .848 -> .851 -> .844) = zebra rings on the corners. y (designed) and the face edge ring stay fixed."""
    R = np.array(rings, float)
    for _ in range(iters):
        for f in (lam, mu):
            L = np.zeros_like(R)
            for i in idx:
                wp = 1 / np.maximum(np.abs(R[i, :, 1] - R[i - 1, :, 1]), 1e-3); wn = 1 / np.maximum(np.abs(R[i + 1, :, 1] - R[i, :, 1]), 1e-3)
                L[i] = (wp[:, None] * R[i - 1] + wn[:, None] * R[i + 1]) / (wp + wn)[:, None] - R[i]
            L[..., 1] = 0; R = R + f * L
    return [[tuple(p) for p in r] for r in R]
_nd = len(dF); RINGS = fair_columns(RINGS, list(range(I_FRONTFACE + 1, I_FRONTFACE + _nd + 2)) + list(range(I_REARFACE - _nd - 1, I_REARFACE)))
if os.environ.get('TS_DUMP'): json.dump(dict(rings=RINGS, ff=len(cF), rf=len(cF) + len(FAIRED) - 1, ns=NS, nr=NR), open(os.environ['TS_DUMP'], 'w')); sys.exit(0)   # diagnosis
LIFT = (E_('TS_LIFT_A', .10), E_('TS_LIFT_B', .34))                                                     # r3: lift eased over a wider band (r2 .15-.24 put a 6 mm step on the lower corners)
RINGS = [[(x, y, z + .006 * (1 - ss(LIFT[0], LIFT[1], z))) for x, y, z in r] for r in RINGS]            # floor lift: subdivided underside >= clearance
VB = [p for r in RINGS for p in r]; F = []; FT = []
for i in range(len(RINGS) - 1):
    for j in range(NR):
        a = i * NR + j; b = i * NR + (j + 1) % NR; cc = (i + 1) * NR + (j + 1) % NR; d = (i + 1) * NR + j
        endf = i < I_FRONTFACE or i >= I_REARFACE
        F.append((a, d, cc, b)); ym = (RINGS[i][0][1] + RINGS[i + 1][0][1]) / 2; h0, h1 = col_tag(j), col_tag((j + 1) % NR); FT.append(('cap', 0, 0) if endf else (ym, min(h0, h1), max(h0, h1)))
for ri in (0, len(RINGS) - 1):                                                                       # quad bridge of the innermost ring (top row <-> bottom row, each half)
    o_ = ri * NR
    for half in (0, 1):
        idx = list(range(0, NS)) if half == 0 else [0] + list(range(NR - 1, NS - 2, -1))
        for k in range(NS // 2 - 1):
            a, b, c2, d2 = idx[k], idx[k + 1], idx[NS - 2 - k], idx[NS - 1 - k]
            f = (o_ + a, o_ + b, o_ + c2, o_ + d2); F.append(f); FT.append(('cap', 0, 0))
def tag(t):
    if t[0] == 'cap': return 'paint'
    y, a, b = t
    if CAB(y) < .5: return 'paint'
    if a >= I_ROOF and COWL + .02 < y < -.03: return 'glass'                                                  # windshield
    if a >= I_ROOF and 1.14 < y < 1.74: return 'glass'                                                   # rear window
    if (a, b) == (9, 10) and COWL + .08 < y < 1.50: return 'glass'                                            # side glass (front door, rear door, quarter light)
    if (a, b) == (8, 9) and COWL + .04 < y < 1.54: return 'seal'                                              # belt / DLO seal
    return 'paint'
TAGS = [tag(t) for t in FT]
# ================================================================ materials
TEX = make_shared_textures(); PAINT_RGB = (.150, .155, .165)                                           # review colour: mineral grey metallic (reads surfaces honestly)
M = build_library(TEX, PRE, PAINT_RGB)
TMP = {}
def tmp(n):
    if n not in TMP: m = bpy.data.materials.new('TMP_' + n); m.diffuse_color = (.02, .02, .02, 1); TMP[n] = m
    return TMP[n]
MM = dict(M); MM.update({'TMP_' + k: tmp(k) for k in ('seal', 'pocket', 'housing', 'grille', 'plastic', 'arch', 'plate')})
WORK = coll('TS_WORK'); CUT = coll('TS_CUTTERS'); CUT_G = coll('TS_GROOVES')
def cage_obj(name):
    tags = [PRE + '_Paint' if t == 'paint' else 'TS_Glass' if t == 'glass' else 'TMP_seal' for t in TAGS]
    me = bpy.data.meshes.new(name); me.from_pydata(VB, [], F); me.update(); order = list(dict.fromkeys(tags))
    for m in order: me.materials.append(MM[m])
    me.polygons.foreach_set('material_index', [order.index(t) for t in tags]); o = bpy.data.objects.new(name, me); WORK.objects.link(o)
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    cr = me.attributes.new('crease_edge', 'FLOAT', 'EDGE'); n_ = len(RINGS)
    crest = {i * NR + j for i in range(n_) for j in (7, NR - 7)}
    rail = {i * NR + j for i in range(n_) if COWL < RINGS[i][0][1] < 1.74 for j in (I_ROOF, NR - I_ROOF)}
    for e in me.edges:
        a_, b_ = e.vertices
        if a_ >= n_ * NR or b_ >= n_ * NR: continue
        ia, ja = divmod(a_, NR); ib, jb = divmod(b_, NR); ym_ = (VB[a_][1] + VB[b_][1]) / 2
        endz = min(ia, ib) < I_FRONTFACE or max(ia, ib) > I_REARFACE
        if ia == ib and ia in (I_FRONTFACE, I_REARFACE) and 'face' in COFF: continue
        if ia == ib and ia in (I_FRONTFACE, I_REARFACE):                                                                    # face edge ring: crisp where the corner radius is small (trunk lip, hood edge)
            Rl = ENDR[-1 if ia == I_FRONTFACE else 1]; cr.data[e.index].value = float(CREASE_W((Rl[ja] + Rl[jb]) / 2))   # continuous (r3)
            continue
        if endz: continue
        if ia != ib and ja == jb:
            if ja in (3, NR - 3) and 'j3' in COFF: continue
            if a_ in crest and b_ in crest and 'crest' in COFF: continue
            if a_ in crest and b_ in crest: cr.data[e.index].value = .80 * ss(E_('TS_CRF0', -2.70), E_('TS_CRF1', -2.60), ym_) * (1 - ss(2.42, 2.55, ym_))   # strong shoulder, lamp to lamp   # shoulder line (crisp, real-car)
            elif a_ in rail and b_ in rail: cr.data[e.index].value = .55                                                    # roof drip rail
            elif ja in (3, NR - 3):                                                                                         # sill / bumper lower edge: hands over to the face edge weight (r3)
                sg_ = -1 if ym_ < 0 else 1; w_end = float(CREASE_W(ENDR[sg_][ja])); t_ = ss(1.96, 2.36, -ym_) if sg_ < 0 else ss(2.08, 2.40, ym_)
                cr.data[e.index].value = lerp(.30, w_end, t_)
            elif ja in (4, NR - 4): cr.data[e.index].value = .55 * ss(-1.25, -1.02, ym_) * (1 - ss(.98, 1.20, ym_))        # lower rocker sculpt line (doors only)
    return o
COFF = set(os.environ.get('TS_CREASE_OFF', '').split(','))                                               # diagnosis only
def subdiv(o, lv):
    m = o.modifiers.new('s', 'SUBSURF'); m.levels = m.render_levels = lv; m.boundary_smooth = 'ALL'
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='s')
# ================================================================ 02 body
REF = cage_obj('REF_Skin'); subdiv(REF, 3)                                                              # uncut limit surface: projection reference (cutters, lenses, parts)
BVH = BVHTree.FromObject(REF, bpy.context.evaluated_depsgraph_get())
def ray(o, d):
    loc, nrm, i, dist = BVH.ray_cast(Vector(o), Vector(d))
    if loc is None: return None, None
    if nrm.dot(Vector(d)) > 0: nrm = -nrm
    return loc, nrm
fhit = lambda x, z: ray((x, -4, z), (0, 1, 0)); rhit = lambda x, z: ray((x, 4, z), (0, -1, 0))
shit = lambda sx, y, z: ray((sx * 3, y, z), (-sx, 0, 0)); thit = lambda x, y: ray((x, y, 3), (0, 0, -1))
def solid(name, outer, inner, mat, c=None):
    bm = bmesh.new(); a = [bm.verts.new(p) for p in outer]; b = [bm.verts.new(p) for p in inner]; n = len(a)
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(n): j = (i + 1) % n; bm.faces.new((a[i], b[i], b[j], a[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bmesh.ops.triangulate(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_' + mat]); o = bpy.data.objects.new(name, me); (c or CUT).objects.link(o); return o
def rounded(pts, r, seg=3):
    out = []; n = len(pts); rs = r if isinstance(r, (list, tuple)) else [r] * n
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n]); d1 = (p0 - p1).normalized(); d2 = (p2 - p1).normalized()
        rr = min(rs[i], (p0 - p1).length * .45, (p2 - p1).length * .45); a_ = p1 + d1 * rr; b_ = p1 + d2 * rr
        for k in range(seg + 1): t = k / seg; q = (1 - t) ** 2 * a_ + 2 * (1 - t) * t * p1 + t * t * b_; out.append((q.x, q.y))
    return out
def mirror_x(poly): return [(-x, z) for x, z in poly][::-1]
def front_pocket(name, poly, depth, mat, rear=False, c=None):
    hitf = rhit if rear else fhit; s = 1 if rear else -1; outer, inner = [], []
    for x, z in poly:
        p, n = hitf(x, z)
        if p is None: print('CUT MISS', name, x, z); return None
        outer.append((x, s * 3.5, z)); inner.append((p.x, p.y - s * depth, p.z))
    return solid(name, outer, inner, mat, c)
def side_pocket(name, poly, depth, mat, sx, c=None):
    outer, inner = [], []
    for y, z in poly:
        p, n = shit(sx, y, z)
        if p is None: print('CUT MISS', name, y, z); return None
        outer.append((sx * 2.0, y, z)); inner.append((p.x - sx * depth, p.y, p.z))
    return solid(name, outer, inner, mat, c)
def top_pocket(name, poly, depth, mat, c=None):
    outer, inner = [], []
    for x, y in poly:
        p, n = thit(x, y)
        if p is None: print('CUT MISS', name, x, y); return None
        outer.append((x, y, 3.0)); inner.append((p.x, p.y, p.z - depth))
    return solid(name, outer, inner, mat, c)
def sample_poly(poly, step=.015, closed=True):
    out = []; pairs = list(zip(poly, poly[1:] + (poly[:1] if closed else [])))
    for a_, b_ in pairs:
        a_, b_ = Vector(a_), Vector(b_); n = max(1, int((b_ - a_).length / step)); out += [tuple(a_.lerp(b_, k / n)) for k in range(n)]
    return out
def fence(name, pts_normals, w=.0058, d_in=.009, d_out=.02):
    """closed groove cutter (panel gap, 4.5 mm wide) along a loop on the surface — high-res master only (baked into the normal map)."""
    n = len(pts_normals); bm = bmesh.new(); rr = []
    for i, (p, nr) in enumerate(pts_normals):
        q = pts_normals[(i + 1) % n][0]; r_ = pts_normals[i - 1][0]; tg = (q - r_).normalized(); b = tg.cross(nr).normalized()
        rr.append([bm.verts.new(p + b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 - nr * d_in), bm.verts.new(p + b * w / 2 - nr * d_in)])
    for i in range(n):
        A, B = rr[i], rr[(i + 1) % n]
        for k in range(4): bm.faces.new((A[k], A[(k + 1) % 4], B[(k + 1) % 4], B[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_pocket'])
    o = bpy.data.objects.new(name, me); CUT_G.objects.link(o); return o
def slot(name, pts_normals, w=.0058, d_in=.009, d_out=.02):
    """open groove (bumper split line): a thin closed loop around a polyline (out and back)."""
    return fence(name, pts_normals + [(p + n * 0, n) for p, n in pts_normals[::-1][1:-1]], w, d_in, d_out)
def loop_top(pts): return [(p, n) for p, n in (thit(x, y) for x, y in pts) if p is not None]
def loop_side(sx, pts): return [(p, n) for p, n in (shit(sx, y, z) for y, z in pts) if p is not None]
def loop_front(pts, rear=False): return [(p, n) for p, n in ((rhit if rear else fhit)(x, z) for x, z in pts) if p is not None]
# ---- openings (cut into master AND game body)
for (y, sx) in ((YF, 1), (YF, -1), (YR, 1), (YR, -1)):                                                   # wheel arches: 55 mm tire clearance, centre 20 mm above the axle
    R_ = RW + .042; seg = 24; zc = RW + .014                                                       # the flared lip owns the visible arch edge
    outer = [(sx * 1.4, y + R_ * math.cos(2 * math.pi * k / seg), zc + R_ * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    solid(f'arch_{y}_{sx}', outer, [(sx * .56, py, pz) for _, py, pz in outer], 'arch')
HL = lambda sx: rounded([(sx * .43, .704), (sx * .62, .720), (sx * .78, .750), (sx * .85, .772), (sx * .862, .726), (sx * .82, .682), (sx * .64, .664), (sx * .45, .672)], [.010, .03, .03, .012, .014, .02, .03, .010], 3)   # slim matrix unit
GRILLE = rounded([(-.40, .705), (.40, .705), (.34, .480), (-.34, .480)], [.03, .03, .05, .05], 3)          # upright, deep, recessed
LOWER = rounded([(-.56, .345), (.56, .345), (.50, .210), (-.50, .210)], [.03, .03, .04, .04], 3)
FOG = lambda sx: rounded([(sx * .64, .520), (sx * .770, .535), (sx * .785, .300), (sx * .70, .265)], .025, 2)   # vertical side intakes (air curtain)
TL = lambda sx: rounded([(sx * .40, .950), (sx * .70, .965), (sx * .845, .955), (sx * .852, .880), (sx * .76, .855), (sx * .42, .880)], [.010, .02, .02, .016, .02, .012], 3)   # slim LED, wraps the corner
PLATE_R = rounded([(-.265, .835), (.265, .835), (.265, .722), (-.265, .722)], .014, 3)                   # plate on the trunk face, under the light strip
VALANCE = rounded([(-.76, .360), (.76, .360), (.70, .205), (-.70, .205)], .02, 3)
EXH = lambda sx: rounded([(sx * .46, .312), (sx * .66, .312), (sx * .64, .246), (sx * .48, .246)], .02, 3)   # integrated trapezoid outlets
for sx in (1, -1):
    front_pocket(f'headlamp_{sx}', HL(sx)[::-1] if sx > 0 else HL(sx), .095, 'housing')
    front_pocket(f'fog_{sx}', FOG(sx) if sx > 0 else FOG(sx)[::-1], .055, 'pocket')
    front_pocket(f'taillamp_{sx}', TL(sx) if sx < 0 else TL(sx)[::-1], .075, 'housing', rear=True)
    for (y0, y1) in ((-.05, .09), (.99, 1.13)):                                                         # door-handle recesses (under the shoulder)
        side_pocket(f'handle_{sx}_{y0}', rounded([(y0, .884), (y1, .888), (y1, .860), (y0, .856)], .01, 3), .018, 'pocket', sx)
    front_pocket(f'exhaust_{sx}', EXH(sx) if sx < 0 else EXH(sx)[::-1], .07, 'plastic', rear=True)
front_pocket('grille', GRILLE[::-1], .075, 'grille'); front_pocket('lower', LOWER[::-1], .085, 'grille')
front_pocket('plate_r', PLATE_R[::-1], .018, 'plate', rear=True); front_pocket('valance', VALANCE[::-1], .022, 'plastic', rear=True)
# ---- panel gaps (master only -> baked): hood, trunk, 4 doors, fuel door, bumper splits (front + rear, both sides)
fence('gap_hood', loop_top(sample_poly(rounded([(.72, COWL - .03), (.80, -1.30), (.76, -2.30), (-.76, -2.30), (-.80, -1.30), (-.72, COWL - .03)], [.02, .3, .08, .08, .3, .02], 6))))
fence('gap_trunk', loop_top(sample_poly(rounded([(.62, 1.80), (.70, 2.10), (.66, 2.36), (-.66, 2.36), (-.70, 2.10), (-.62, 1.80)], [.02, .2, .05, .05, .2, .02], 6))))   # trailing edge on the deck, clear of the crisp trunk edge
for sx in (1, -1):
    TOPZ = lambda y: ZBELT(y) + E_('TS_DOORTOP', .022)                                                # r3: door top shut line hidden under the belt seal (real-car); r2 ran it 18 mm under the crisp shoulder -> dashed bake
    FD = rounded([(-1.14, .33), (.33, .33), (.33, TOPZ(.33)), (-1.06, TOPZ(-1.06))], [.04, .02, .01, .02], 5)
    RD = rounded([(.39, .33), (.86, .33), (.887, .406), (.947, .598), (1.083, .746), (1.50, TOPZ(1.50)), (.39, TOPZ(.39))], [.02, .03, .03, .06, .06, .02, .01], 5)   # rear door follows the arch lip
    fence(f'gap_fdoor_{sx}', loop_side(sx, sample_poly(FD))); fence(f'gap_rdoor_{sx}', loop_side(sx, sample_poly(RD)))
fence('gap_fuel', loop_side(-1, sample_poly(rounded([(1.62, .80), (1.78, .80), (1.78, .93), (1.62, .93)], .025, 4))))   # fuel door (right rear quarter)
def groove_open(name, pn, w=.0055, d_in=.009, d_out=.02):
    """open groove cutter along a polyline on the surface (bumper shut line): square tube with end caps."""
    bm = bmesh.new(); rr = []; n = len(pn)
    for i, (p, nr) in enumerate(pn):
        q = pn[min(i + 1, n - 1)][0]; r_ = pn[max(i - 1, 0)][0]; tg = (q - r_).normalized(); b = tg.cross(nr).normalized()
        rr.append([bm.verts.new(p + b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 - nr * d_in), bm.verts.new(p + b * w / 2 - nr * d_in)])
    for i in range(n - 1):
        A, B = rr[i], rr[i + 1]
        for k in range(4): bm.faces.new((A[k], A[(k + 1) % 4], B[(k + 1) % 4], B[k]))
    bm.faces.new(rr[0][::-1]); bm.faces.new(rr[-1]); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_pocket']); o = bpy.data.objects.new(name, me); CUT_G.objects.link(o); return o
def sweep_rear(z, c=(0, 2.12), a0=-86, a1=86, n=44):
    out = []
    for a in np.linspace(math.radians(a0), math.radians(a1), n):
        d = Vector((math.sin(a), math.cos(a), 0)); loc, nrm, i_, dist = BVH.ray_cast(Vector((c[0], c[1], z)), d)
        if loc is not None: out.append((loc, (-nrm if nrm.dot(d) < 0 else nrm)))                     # outward normal
    return out
def surf_curve(guides, step=.005, iters=24):
    """r3: shut-line path = Catmull-Rom through 3D guide points, arc-length resampled every `step`, closest-point projected onto the skin,
    Laplacian-smoothed (ends fixed) with re-projection; frame normal = smoothed skin normal. No grazing ray casts, no twist."""
    G = [Vector(g) for g in guides]; G = [G[0] * 2 - G[1]] + G + [G[-1] * 2 - G[-2]]; dense = []
    for i in range(1, len(G) - 2):
        p0, p1, p2, p3 = G[i - 1], G[i], G[i + 1], G[i + 2]
        for k in range(40):
            t = k / 40; dense.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    dense.append(G[-2]); L = [0.0]
    for a_, b_ in zip(dense, dense[1:]): L.append(L[-1] + (b_ - a_).length)
    n = max(2, int(L[-1] / step)); P = []; j = 0
    for k in range(n + 1):
        s_ = L[-1] * k / n
        while j < len(L) - 2 and L[j + 1] < s_: j += 1
        t = (s_ - L[j]) / max(L[j + 1] - L[j], 1e-9); P.append(dense[j].lerp(dense[j + 1], t))
    proj = lambda p: BVH.find_nearest(p)[0]
    P = [proj(p) for p in P]
    for _ in range(iters):
        P = [P[0]] + [proj((P[i - 1] + 2 * P[i] + P[i + 1]) / 4) for i in range(1, len(P) - 1)] + [P[-1]]
    N = [BVH.find_nearest(p)[1].normalized() for p in P]
    for _ in range(6): N = [N[0]] + [(N[i - 1] + 2 * N[i] + N[i + 1]).normalized() for i in range(1, len(N) - 1)] + [N[-1]]
    return list(zip(P, N))
ARC = lambda y0, ang, r=RW + .042 + .020: (y0 + r * math.cos(math.radians(ang)), RW + .014 + r * math.sin(math.radians(ang)))   # point under the flared arch lip
def side_pt(sx, y, z): p, n = shit(sx, y, z); return p
# rear bumper shut line: under the RR arch lip -> quarter -> around the corner -> across the face -> quarter -> under the RL arch lip
rs = [ARC(YR, 35), (1.95, .640), (2.12, .668), (2.28, .684)]
side_R = [side_pt(-1, y, z) for y, z in rs]; side_L = [side_pt(1, y, z) for y, z in rs]
face_ = [p for p, n in sweep_rear(.686, n=60) if p.y > 2.34]                                            # corner + face (radial rays: never grazing)
groove_open('shut_rear_bumper', surf_curve(side_R + face_[::4] + [face_[-1]] + side_L[::-1]))
for sx in (1, -1):                                                                                     # fascia / fender split: starts inside the headlamp opening, ends under the arch lip
    lamp = fhit(sx * .845, .730)[0]
    yA, zA = ARC(YF, 150)
    groove_open(f'shut_front_{sx}', surf_curve([lamp, side_pt(sx, lamp.y + .07, .715), side_pt(sx, -2.10, .660), side_pt(sx, yA, zA)]))
def apply_cuts(o, cc):
    m_ = o.modifiers.new('cuts', 'BOOLEAN'); m_.operation = 'DIFFERENCE'; m_.solver = 'EXACT'; m_.operand_type = 'COLLECTION'; m_.collection = cc
    if hasattr(m_, 'material_mode'): m_.material_mode = 'TRANSFER'
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='cuts')
ALLC = coll('TS_ALLCUT')
for o in list(CUT.objects) + list(CUT_G.objects): ALLC.objects.link(o)
HI = cage_obj('REF_Master'); subdiv(HI, 3); apply_cuts(HI, ALLC); HI.data.shade_smooth()
LO = cage_obj('Body_Game'); subdiv(LO, 1); apply_cuts(LO, CUT)
REPORT['master_tris'] = tris(HI); REPORT['cutters'] = sorted(o.name for o in CUT.objects); REPORT['grooves'] = sorted(o.name for o in CUT_G.objects)
for c_ in (ALLC, CUT, CUT_G):
    for o in list(c_.objects): bpy.data.objects.remove(o, do_unlink=True) if o.name in bpy.data.objects else None
clean(LO)
# game body = cage at subdivision level 1 (clean quads; material boundaries stay on cage lines - no decimation tears); smoothness comes from the bake
def split_by(o, pred, new_name):
    me2 = o.data.copy(); n = bpy.data.objects.new(new_name, me2); o.users_collection[0].objects.link(n)
    for ob, keep in ((o, lambda m: not pred(m)), (n, pred)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(mats[f.material_index].name if mats[f.material_index] else '')], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    purge_slots(n); purge_slots(o); return n
GLASS = split_by(LO, lambda m: m == 'TS_Glass', 'Glass_Shell')
BODYTRIM = split_by(LO, lambda m: m.startswith('TMP_'), 'BodyTrim')                                   # pocket walls, seals, arch walls -> atlas
REPORT['body_paint_tris'] = tris(LO); REPORT['bodytrim_tris'] = tris(BODYTRIM); REPORT['glass_tris'] = tris(GLASS)
# ---- body-colour mirror housings + roof antenna fin: part of the paint body (unique UVs, baked like the rest; copies added to the master)
MIRC = {sx: Vector((sx * .99, COWL + .09, 1.03)) for sx in (1, -1)}
def mirror_housing(sx):
    """tapered rounded-box housing: outboard end taller, flat rear face (glass sits there), rounded aero front."""
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(.17, .085, .110), verts=bm.verts)
    bmesh.ops.bevel(bm, geom=[e for e in bm.edges if not all(v.co.y > .04 for v in e.verts)], offset=.028, segments=2, affect='EDGES', profile=.5)
    for v in bm.verts:
        t = (v.co.x * sx + .10) / .20; v.co.z *= lerp(.72, 1.0, t); v.co.y *= lerp(.80, 1.0, t)                                 # narrower / lower toward the door
        if v.co.y < 0: v.co.y *= 1.0 + .35 * (1 - abs(v.co.z) / .06) * (1 - abs(v.co.x) / .10)                                  # rounded aero front bulge
        v.co += MIRC[sx]
    me = bpy.data.meshes.new('MirH'); bm.to_mesh(me); bm.free(); me.materials.append(M[PRE + '_Paint']); o = bpy.data.objects.new(f'MirrorHousing_{sx}', me); WORK.objects.link(o); return o
def antenna_fin():
    prof = [(.80, 0.0), (.90, .012), (.98, .045), (1.02, .058), (1.05, .040), (1.065, 0.0)]; Vs = []; Fs = []
    for y, h in prof:
        p, n = thit(0, y); Vs += [(-.028 * (h > 0) - .006, y, p.z - .004), (.028 * (h > 0) + .006, y, p.z - .004), (0, y, p.z + h)]
    for i in range(len(prof) - 1):
        a0 = 3 * i; b0 = 3 * (i + 1); Fs += [(a0, b0, b0 + 2, a0 + 2), (a0 + 1, a0 + 2, b0 + 2, b0 + 1)]
    me = bpy.data.meshes.new('Fin'); me.from_pydata(Vs, [], Fs); me.materials.append(M[PRE + '_Paint']); o = bpy.data.objects.new('AntennaFin', me); WORK.objects.link(o)
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free(); return o
def arch_lip(y, sx, seg=20):
    Re = RW + .042; zc = RW + .014; a0, a1 = math.radians(-6), math.radians(186); rows = [[], [], []]
    for q in range(seg + 1):
        a = lerp(a0, a1, q / seg); ca, sa = math.cos(a), math.sin(a)
        p0, n0 = shit(sx, y + (Re + .036) * ca, zc + (Re + .036) * sa); p1, n1 = shit(sx, y + (Re + .006) * ca, zc + (Re + .006) * sa)
        if p0 is None or p1 is None: return None
        rows[0].append(p0 + n0 * .0015); rows[1].append(p1 + n1 * .009)
        rows[2].append(Vector((p1.x - sx * .032, y + (Re - .002) * ca, zc + (Re - .002) * sa)))
    g = Geo(); g.strip(rows[0], rows[1], PRE + '_Paint', flip=sx < 0); g.strip(rows[1], rows[2], PRE + '_Paint', flip=sx < 0)
    o = mk(f'ArchLip_{y}_{sx}', g.V, g.F, g.T, WORK, M); orient_out(o, centre=(0, y, zc))
    fa = o.data.attributes.new('flatbake', 'INT', 'FACE'); fa.data.foreach_set('value', [1] * len(o.data.polygons)); return o
LIPS = [l_ for l_ in (arch_lip(y, sx) for y in (YF, YR) for sx in (1, -1)) if l_]
REPORT['arch_lips'] = len(LIPS)
EXTRA = [mirror_housing(1), mirror_housing(-1), antenna_fin()] + LIPS
for e_ in EXTRA:
    c_ = e_.copy(); c_.data = e_.data.copy(); WORK.objects.link(c_); HI = join([HI, c_], 'REF_Master', WORK)
def master_normals(o, tol=.0005, agree=.82):
    """r3: loops on the skin get the uncut skin's interpolated smooth normal (boolean slivers no longer shade themselves);
    loops of faces that disagree (groove / pocket walls) get their flat face normal; everything off the skin keeps its own."""
    from mathutils.interpolate import poly_3d_calc
    rme = REF.data; RV = [v.co.copy() for v in rme.vertices]; RN = [v.normal.copy() for v in rme.vertices]; RP = [tuple(p.vertices) for p in rme.polygons]
    bvp = BVHTree.FromPolygons(RV, RP); me = o.data; cn = [c.vector.copy() for c in me.corner_normals]; vmap = {}
    for v in me.vertices:
        loc, nrm, fi, d = bvp.find_nearest(v.co)
        if loc is None or d > tol: continue
        ids = RP[fi]; w = poly_3d_calc([RV[i] for i in ids], v.co); vmap[v.index] = sum((RN[i] * wi for i, wi in zip(ids, w)), Vector()).normalized()
    nrep = nflat = 0
    for p in me.polygons:
        for li in p.loop_indices:
            vi = me.loops[li].vertex_index
            if vi not in vmap: continue
            if p.normal.dot(vmap[vi]) > agree: cn[li] = vmap[vi]; nrep += 1
            else: cn[li] = p.normal.copy(); nflat += 1
    me.normals_split_custom_set(cn); REPORT['master_normals'] = dict(skin_loops=nrep, wall_loops_flat=nflat, verts_on_skin=len(vmap)); print('MASTER NORMALS', nrep, nflat, len(vmap), flush=True)
master_normals(HI)
LO = join([LO] + EXTRA, 'Body_Game', WORK)
_t0 = tris(LO); bm = bmesh.new(); bm.from_mesh(LO.data); bm.faces.ensure_lookup_table()
near_cut = {v for e in bm.edges if e.is_boundary for v in e.verts}                                     # vertices on any opening / arch edge
okf = lambda f: not any(v in near_cut for v in f.verts)
bm.normal_update(); top_ = lambda f: f.normal.z > E_('TS_TOP_NZ', .55)                              # r3: hood / roof / deck keep a finer mesh (long slivers forced big 8-bit normal-map
ed = [e for e in bm.edges if len(e.link_faces) == 2 and all(okf(f) for f in e.link_faces)]             #     corrections -> stair-stepped highlight on the hood)
dn_ = lambda f: f.normal.z < -.70 and f.calc_center_median().z < .34                                  # r3: under-bumper / underside faces (never seen from any game camera): coarse dissolve, surface stays closed
edd = [e for e in ed if all(dn_(f) for f in e.link_faces)]; ed = [e for e in ed if not all(dn_(f) for f in e.link_faces)]
bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(E_('TS_PLANAR_DOWN_DEG', 12.0)), use_dissolve_boundaries=False, edges=edd, verts=[], delimit={'MATERIAL'})
ed = [e for e in ed if e.is_valid]
edt = [e for e in ed if all(top_(f) for f in e.link_faces)]; eds = [e for e in ed if not all(top_(f) for f in e.link_faces)]
bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(float(os.environ.get('TS_PLANAR_DEG', 3.0))), use_dissolve_boundaries=False, edges=eds, verts=[], delimit={'MATERIAL'})
edt = [e for e in edt if e.is_valid]
if E_('TS_PLANAR_TOP_DEG', 0.5) > 0: bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(E_('TS_PLANAR_TOP_DEG', 0.5)), use_dissolve_boundaries=False, edges=edt, verts=[], delimit={'MATERIAL'})
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4], quad_method='BEAUTY', ngon_method='BEAUTY'); bm.to_mesh(LO.data); bm.free(); clean(LO)
inv_ = 0
for p_ in LO.data.polygons:
    loc_, nrm_, i_, d_ = BVH.find_nearest(p_.center)
    if loc_ is not None and d_ < .05 and nrm_.dot(p_.normal) < -.2: inv_ += 1
REPORT['body_inverted_faces'] = inv_; print('INVERTED', inv_, flush=True)
REPORT['body_planar_dissolve'] = dict(before=_t0, after=tris(LO)); print('PLANAR', _t0, '->', tris(LO), flush=True)   # flat regions: fewer triangles, the baked normal map carries the shading
bm = bmesh.new(); bm.from_mesh(LO.data); bm.normal_update()
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.normal.z < -.75 and f.calc_center_median().z < .26 and abs(f.calc_center_median().y) < 2.12], context='FACES'); bm.to_mesh(LO.data); bm.free()   # hidden underside (underbody tray covers it)
# ---- shading of the game body: smooth, hard edges only at real breaks (opening rims), then UV unwrap + normal bake from the master
LO.data.shade_smooth(); LO.data.set_sharp_from_angle(angle=math.radians(48))
bpy.context.view_layer.objects.active = LO
for o in bpy.context.view_layer.objects: o.select_set(o == LO)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(float(os.environ.get('TS_UV_ANGLE', 58))), island_margin=.006, area_weight=.3, correct_aspect=True, scale_to_bounds=False)
bpy.ops.uv.pack_islands(margin=.006, rotate=True)
bpy.ops.object.mode_set(mode='OBJECT')
def bake_normal(low, high, img_name, res, path):
    SS = int(E_('TS_BAKE_SS', 2)); out_res = res; res = res * SS                                     # r3: supersampled bake (2x, box-filtered down): 5.8 mm panel gaps were ~2.4 texels -> dashed / beaded
    img = bpy.data.images.new(img_name + '_ss', res, res, alpha=False, float_buffer=True); img.colorspace_settings.name = 'Non-Color'
    bm_ = bpy.data.materials.new('BAKE_TMP'); bm_.use_nodes = True; tn = bm_.node_tree.nodes.new('ShaderNodeTexImage'); tn.image = img; bm_.node_tree.nodes.active = tn
    saved = [m for m in low.data.materials]; low.data.materials.clear(); low.data.materials.append(bm_)
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 1
    try:
        pr = bpy.context.preferences.addons['cycles'].preferences; pr.compute_device_type = 'METAL'; pr.get_devices(); [setattr(d, 'use', True) for d in pr.devices]; sc.cycles.device = 'GPU'
    except Exception as e: print('bake on CPU', e)
    hr, hv = high.hide_render, high.hide_viewport; high.hide_render = False; high.hide_viewport = False
    for o in bpy.context.view_layer.objects: o.select_set(o in (low, high))
    bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(type='NORMAL', normal_space='TANGENT', use_selected_to_active=True, cage_extrusion=float(os.environ.get('TS_CAGE', .03)), max_ray_distance=float(os.environ.get('TS_RAY', .07)), margin=8 * SS, use_clear=True)
    high.hide_render, high.hide_viewport = hr, hv
    fl = low.data.attributes.get('flatbake')                                                         # thin rolled parts (arch lips): flat tangent normal (own smooth geometry shades them)
    if fl:
        W_ = img.size[0]; px = np.array(img.pixels[:], np.float32).reshape(W_, W_, 4); uvd = low.data.uv_layers.active.data; nflat = 0
        for p_ in low.data.polygons:
            if not fl.data[p_.index].value: continue
            P = np.array([uvd[li].uv[:] for li in p_.loop_indices]) * W_; c_ = P.mean(0); P = c_ + (P - c_) * 1.0 + np.sign(P - c_) * 3.0   # 3 px dilation
            for k_ in range(1, len(P) - 1):
                T_ = np.array([P[0], P[k_], P[k_ + 1]]); x0, y0 = np.floor(T_.min(0)).astype(int); x1, y1 = np.ceil(T_.max(0)).astype(int)
                x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W_ - 1), min(y1, W_ - 1)
                if x1 < x0 or y1 < y0: continue
                yy, xx = np.mgrid[y0:y1 + 1, x0:x1 + 1] + .5; a_, b_, c2 = T_
                den = (b_[1] - c2[1]) * (a_[0] - c2[0]) + (c2[0] - b_[0]) * (a_[1] - c2[1])
                if abs(den) < 1e-9: continue
                l1 = ((b_[1] - c2[1]) * (xx - c2[0]) + (c2[0] - b_[0]) * (yy - c2[1])) / den; l2 = ((c2[1] - a_[1]) * (xx - c2[0]) + (a_[0] - c2[0]) * (yy - c2[1])) / den
                m_ = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1); sub = px[y0:y1 + 1, x0:x1 + 1]; sub[m_] = (.5, .5, 1.0, 1.0); nflat += int(m_.sum())
        img.pixels.foreach_set(px.ravel()); print('FLATBAKE texels', nflat, flush=True)
    if SS > 1:
        px = np.array(img.pixels[:], np.float32).reshape(res, res, 4); n_ = px[..., :3] * 2 - 1
        n_ = n_.reshape(out_res, SS, out_res, SS, 3).mean((1, 3)); n_ /= np.maximum(np.linalg.norm(n_, axis=2, keepdims=True), 1e-6)
        o_ = np.dstack([n_ * .5 + .5, np.ones((out_res, out_res, 1), np.float32)]); bpy.data.images.remove(img)
        img = bpy.data.images.new(img_name, out_res, out_res, alpha=False, float_buffer=False); img.colorspace_settings.name = 'Non-Color'; img.pixels.foreach_set(o_.ravel())
    img.filepath_raw = path; img.file_format = 'PNG'; img.save(); low.data.materials.clear()
    for m in saved: low.data.materials.append(m)
    bpy.data.materials.remove(bm_); return path
if os.environ.get('TS_NOBAKE'): assert SCR; save_ckp(CKP_ + '_02_body.blend'); sys.exit(0)                     # geometry trials only (scratch)
NORMAL0 = None if BLOCKOUT else bake_normal(LO, HI,f'{PRE}_Body_Normal', int(os.environ.get('TS_BAKE_RES', 2048)), OUTD('textures', f'{PRE}_Body_Normal.png'))
M.update(paint_material(PRE + '_Paint', PAINT_RGB, dict(normal=NORMAL0) if NORMAL0 else None, TEX))
REPORT['body_normal'] = os.path.basename(NORMAL0) if NORMAL0 else None
HI.hide_render = True; HI.hide_viewport = True
save_ckp(CKP_ + '_02_body.blend') if LAST >= 2 else None
if LAST <= 2: sys.exit(0)
# ================================================================ 03 exterior parts, lamps, glass (real depth; nothing painted-on)
TR, LI = Geo(), Geo()
def grow(poly, d):
    c = centroid2(poly); return [tuple(c + (Vector(p) - c) * (1 + d / max((Vector(p) - c).length, 1e-6))) for p in poly]
def rim_band(g, poly, hitf, w_out, w_in, off, t, step=.030):
    """thin frame on the skin across an opening outline (outline grown by w_out .. shrunk by w_in), `off` above the skin."""
    ring = sample_poly(poly, step); c = centroid2(ring); A, B = [], []
    for x, z in ring:
        q = Vector((x, z)); dv = (q - c).normalized(); pa, na = hitf(*(q + dv * w_out)); pb, nb = hitf(*(q - dv * w_in))
        if pa is None or pb is None: print('RIM MISS', t); return
        A.append(pa + na * off); B.append(pb + nb * off)
    g.strip(A, B, t, closed=True)
def ptat(hitf, a, b, depth):
    p, n = hitf(a, b); return None if p is None else p - n * depth
def centroid2(poly): return Vector((sum(x for x, _ in poly) / len(poly), sum(z for _, z in poly) / len(poly)))
def surf_patch(g, poly, hitf, off, t, step=.026, shrink=1.0):
    """surface-following panel / lens over a closed outline (polar fan from the outline centroid; exact outline), offset `off` along the skin normal."""
    ring = sample_poly(poly, step); c = centroid2(ring); rows = []
    for k in (shrink, shrink * .5):
        row = []
        for x, z in ring:
            q = c.lerp(Vector((x, z)), k); p, n = hitf(q.x, q.y); row.append(p + n * off if p is not None else None)
        rows.append(row)
    if any(p is None for r in rows for p in r): print('PATCH MISS', t); return
    pc, nc = hitf(c.x, c.y); n0 = len(g.V); nr = len(ring)
    for r in rows: g.V += [tuple(p) for p in r]
    g.V.append(tuple(pc + nc * off))
    for i in range(1):
        for j in range(nr): g.F.append((n0 + i * nr + j, n0 + i * nr + (j + 1) % nr, n0 + (i + 1) * nr + (j + 1) % nr, n0 + (i + 1) * nr + j)); g.T.append(t)
    for j in range(nr): g.F.append((n0 + nr + j, n0 + nr + (j + 1) % nr, n0 + 2 * nr)); g.T.append(t)
def bezel(g, poly, hitf, d0, d1, k1, t, step=.04):
    """depth ring inside an opening: outline at depth d0 -> outline shrunk to k1 at depth d1 (gives a lamp / grille real inner wall)."""
    ring = sample_poly(poly, step); c = centroid2(ring); A, B = [], []
    for x, z in ring:
        p0 = ptat(hitf, x, z, d0); q = c.lerp(Vector((x, z)), k1); p1 = ptat(hitf, q.x, q.y, d1)
        if p0 is None or p1 is None: print('BEZEL MISS', t); return
        A.append(p0); B.append(p1)
    g.strip(A, B, t, closed=True)
def ribbon(g, hitf, pts, h, depth, t):
    """light guide / trim ribbon of height h along a polyline of (x, z) points, `depth` behind the skin."""
    A = [ptat(hitf, x, z - h / 2, depth) for x, z in pts]; B = [ptat(hitf, x, z + h / 2, depth) for x, z in pts]
    if any(p is None for p in A + B): print('RIBBON MISS', t); return
    g.strip(A, B, t)
def cup(g, centre, axis, r, depth, seg, t_rim, t_core=None, rc=.010):
    """reflector bowl: rim ring -> apex along -axis; optional emitter disc at the bottom."""
    axis = Vector(axis).normalized(); a = Vector((1, 0, 0)) if abs(axis.x) < .9 else Vector((0, 0, 1)); b1 = axis.cross(a).normalized(); b2 = axis.cross(b1)
    ring = lambda rr, d: [Vector(centre) - axis * d + (b1 * math.cos(2 * math.pi * k / seg) + b2 * math.sin(2 * math.pi * k / seg)) * rr for k in range(seg)]
    g.strip(ring(r, 0), ring(rc + .004, depth), t_rim, closed=True)
    if t_core: g.cap(ring(rc + .004, depth), t_core, centre=Vector(centre) - axis * (depth - .004))
def tube(g, p0, p1, r, seg, t, cap_end=True):
    p0, p1 = Vector(p0), Vector(p1); ax = (p1 - p0).normalized(); a = Vector((1, 0, 0)) if abs(ax.x) < .9 else Vector((0, 0, 1)); b1 = ax.cross(a).normalized(); b2 = ax.cross(b1)
    ring = lambda p: [p + (b1 * math.cos(2 * math.pi * k / seg) + b2 * math.sin(2 * math.pi * k / seg)) * r for k in range(seg)]
    g.strip(ring(p0), ring(p1), t, closed=True)
    if cap_end: g.cap(ring(p1), t, centre=p1)
for sx in (1, -1):
    IND = 'TS_Lights:Indicator_L' if sx > 0 else 'TS_Lights:Indicator_R'
    # ---- matrix headlamp: dark inner bezel, four projector cells (emitters), upper LED DRL guide, amber indicator strip, clear lens, gloss frame
    bezel(LI, HL(sx), fhit, .004, .030, .90, 'TS_Atlas:lamp_inner', step=.06)
    for x0 in (.50, .585, .67, .755):
        z0 = .700 + (x0 - .45) * .085; p, n = fhit(sx * x0, z0); cup(LI, p - n * .022, -n, .016, .028, 7, 'TS_Atlas:reflector', 'TS_Lights:Headlamp', rc=.007)
    ribbon(LI, fhit, [(sx * x, z) for x, z in ((.46, .697), (.58, .708), (.70, .725), (.80, .742), (.84, .753))], .007, .016, 'TS_Lights:DRL')
    ribbon(LI, fhit, [(sx * x, z) for x, z in ((.70, .682), (.78, .689), (.83, .698))], .008, .020, IND)
    surf_patch(LI, HL(sx), fhit, .004, 'TS_Lens', step=.032)
    rim_band(TR, HL(sx), fhit, .010, .004, .0058, 'TS_Atlas:gloss_black')
    # ---- vertical side intake: honeycomb back plate, gloss frame
    surf_patch(TR, FOG(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .050, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:grille', step=.05)
    rim_band(TR, FOG(sx), fhit, .008, .003, .004, 'TS_Atlas:gloss_black')
    # ---- slim LED tail lamp: dark reflector field, continuous tail guide, brake block, indicator, red lens, frame
    surf_patch(LI, TL(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .040, pn[1]) if pn[0] is not None else pn)(rhit(a, b)), 0.0, 'TS_Atlas:lamp_housing', step=.05, shrink=.97)
    bezel(LI, TL(sx), rhit, .004, .035, .97, 'TS_Atlas:lamp_housing', step=.05)
    ribbon(LI, rhit, [(sx * x, z) for x, z in ((.43, .935), (.56, .943), (.70, .950), (.80, .946), (.838, .935))], .007, .016, 'TS_Lights:Tail')
    LI.grid([[ptat(rhit, sx * x, z, .022) for x in np.linspace(.50, .74, 5)] for z in (.910, .922)], 'TS_Lights:Brake')
    LI.grid([[ptat(rhit, sx * x, z, .022) for x in np.linspace(.62, .78, 4)] for z in (.886, .897)], IND)
    surf_patch(LI, TL(sx), rhit, .004, 'TS_LensRed', step=.032)
    rim_band(TR, TL(sx), rhit, .010, .004, .0058, 'TS_Atlas:gloss_black')
    # ---- exhaust outlet: chrome frame + dark interior; rear bumper: reverse lamp, reflector; side repeater; handles; mirror arm + glass
    rim_band(TR, EXH(sx), rhit, .008, .004, .003, 'TS_Atlas:chrome')
    surf_patch(TR, EXH(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .060, pn[1]) if pn[0] is not None else pn)(rhit(a, b)), 0.0, 'TS_Atlas:underbody', step=.05)
    LI.grid([[ptat(rhit, sx * x, z, .004) for x in np.linspace(.44, .58, 4)] for z in (.500, .520)], 'TS_Lights:Reverse')
    LI.grid([[ptat(rhit, sx * x, z, -.0015) for x in np.linspace(.435, .585, 4)] for z in (.496, .524)], 'TS_Lens')
    TR.grid([[ptat(rhit, sx * x, z, -.002) for x in np.linspace(.66, .78, 3)] for z in (.500, .520)], 'TS_Atlas:reflector_red')
    LI.grid([[ptat(lambda y_, z_: shit(sx, y_, z_), y, z, -.002) for y in np.linspace(-2.10, -2.03, 3)] for z in (.700, .716)], IND)
    for (y0, y1) in ((-.04, .08), (1.00, 1.12)):
        TR.grid([[ptat(lambda y_, z_: shit(sx, y_, z_), y, z, d) for y in np.linspace(y0, y1, 4)] for z, d in ((.862, .002), (.873, -.006), (.882, .002))], 'TS_Atlas:dark_chrome')
    mc = MIRC[sx]; base = shit(sx, mc.y, .955)[0]
    TR.rbox(((base.x + mc.x - sx * .07) / 2, mc.y, (.96 + mc.z - .02) / 2), (abs(mc.x - sx * .07 - base.x) / 2 + .012, .030, .020), 'TS_Atlas:plastic_black', .008)
    TR.add([(mc.x - sx * .072, mc.y + .046, mc.z - .043), (mc.x + sx * .072, mc.y + .046, mc.z - .040), (mc.x + sx * .072, mc.y + .046, mc.z + .046), (mc.x - sx * .072, mc.y + .046, mc.z + .038)], [(0, 1, 2, 3) if sx < 0 else (3, 2, 1, 0)], 'TS_Atlas:mirror_glass')
for (y, sx) in ((YF, 1), (YF, -1), (YR, 1), (YR, -1)):
    R_ = RW + .045; zc = RW + .014; seg = 10; a0, a1 = math.radians(-12), math.radians(192)
    arc = [(y + R_ * math.cos(lerp(a0, a1, q / seg)), zc + R_ * math.sin(lerp(a0, a1, q / seg))) for q in range(seg + 1)]
    xi, xo = sx * .58, sx * (WMAX(y) - .02)
    TR.strip([Vector((xi, yy, zz)) for yy, zz in arc], [Vector((xo, yy, zz)) for yy, zz in arc], 'TS_Atlas:arch_liner', flip=sx > 0)
    TR.cap([Vector((xi, yy, zz)) for yy, zz in arc], 'TS_Atlas:arch_liner', centre=Vector((xi, y, zc - .05)), flip=sx < 0)
# ---- grille: chrome frame, five gloss-black bars with depth, dark mesh back plate deep in shadow; lower intake + bar; front plate; badges; rear light strip
bezel(TR, GRILLE, fhit, .002, .014, .955, 'TS_Atlas:chrome')
surf_patch(TR, GRILLE, lambda a, b: (lambda pn: (pn[0] - pn[1] * .070, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:grille', step=.06)
for z in (.528, .566, .604, .642, .680):
    hw_ = lerp(.34, .40, (z - .48) / .225) - .028; xs = np.linspace(-hw_, hw_, 9); A = [ptat(fhit, x, z, .024) for x in xs]
    TR.strip([p - Vector((0, 0, .005)) for p in A], [p + Vector((0, 0, .005)) for p in A], 'TS_Atlas:gloss_black'); TR.strip([p + Vector((0, 0, .005)) for p in A], [p + Vector((0, .034, .005)) for p in A], 'TS_Atlas:gloss_black')
surf_patch(TR, LOWER, lambda a, b: (lambda pn: (pn[0] - pn[1] * .060, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:grille', step=.06)
bezel(TR, LOWER, fhit, .003, .03, .965, 'TS_Atlas:plastic_black')
xs = np.linspace(-.44, .44, 11); A = [ptat(fhit, x, .278, .030) for x in xs]
TR.strip([p - Vector((0, 0, .006)) for p in A], [p + Vector((0, 0, .006)) for p in A], 'TS_Atlas:gloss_black')
TR.grid([[ptat(fhit, x, z, -.006) for x in np.linspace(-.26, .26, 4)] for z in (.360, .470)], 'TS_Atlas:plate')                       # front plate (fictional)
TR.grid([[ptat(fhit, x, z, -.002) for x in np.linspace(-.28, .28, 4)] for z in (.350, .480)], 'TS_Atlas:plastic_black')             # plate holder
TR.grid([[ptat(rhit, x, z, .010) for x in np.linspace(-.25, .25, 4)] for z in (.732, .825)], 'TS_Atlas:plate')                        # rear plate in the recess
rim_band(TR, PLATE_R, rhit, .014, .004, .004, 'TS_Atlas:plastic_black')
ribbon(TR, rhit, [(x, .921) for x in np.linspace(-.41, .41, 9)], .010, -.002, 'TS_Atlas:dark_chrome')                               # connecting trim strip across the trunk (unlit)
p, n = fhit(0, .600); TR.cap([p - n * .012 + Vector((.034 * math.cos(2 * math.pi * k / 12), 0, .026 * math.sin(2 * math.pi * k / 12))) for k in range(12)], 'TS_Atlas:badge', flip=True)
p, n = rhit(0, .985); TR.cap([p + n * .002 + Vector((.030 * math.cos(2 * math.pi * k / 12), 0, .022 * math.sin(2 * math.pi * k / 12))) for k in range(12)], 'TS_Atlas:badge')
# ---- underbody tray, high-mount brake light integrated in the trunk lip, wipers
TR.grid([[Vector((x, y, .158)) for x in np.linspace(-.80, .80, 3)] for y in np.linspace(-2.10, 2.15, 4)], 'TS_Atlas:underbody', flip=True)
LI.grid([[ptat(rhit, x, z, -.001) for x in np.linspace(-.24, .24, 4)] for z in (1.062, 1.072)], 'TS_Lights:Brake')
for x0, x1 in ((-.64, -.06), (.02, .58)):
    pts = [thit(x, COWL + .05)[0] + Vector((0, 0, .012)) for x in np.linspace(x0, x1, 5)]
    TR.strip([p - Vector((0, .006, 0)) for p in pts], [p + Vector((0, .006, .004)) for p in pts], 'TS_Atlas:wiper'); TR.strip([p + Vector((0, .006, .004)) for p in pts], [p + Vector((0, .006, .016)) for p in pts], 'TS_Atlas:wiper')
# ---- glass: inset 6 mm with a rubber seal wall, black frit band on the windshield / rear window, B-pillar applique + quarter-light divider
gme = GLASS.data; bmg = bmesh.new(); bmg.from_mesh(gme); bmg.verts.ensure_lookup_table(); bmg.normal_update()
orig = {v.index: v.co.copy() for v in bmg.verts}
for v in bmg.verts: v.co -= v.normal * .006
bnd = [e for e in bmg.edges if e.is_boundary]
for e in bnd:
    a_, b_ = e.verts; TR.add([orig[a_.index], orig[b_.index], b_.co.copy(), a_.co.copy()], [(0, 1, 2, 3)], 'TS_Atlas:rubber')
isl = {}; seen = set()
for f0 in bmg.faces:
    if f0.index in seen: continue
    st = [f0]; comp = []
    while st:
        f = st.pop()
        if f.index in seen: continue
        seen.add(f.index); comp.append(f); st += [g for e in f.edges for g in e.link_faces if g.index not in seen]
    cen = sum((f.calc_center_median() for f in comp), Vector()) / len(comp)
    for f in comp: isl[f.index] = cen
frit_faces = [f for f in bmg.faces if abs(isl[f.index].x) < .30]                                    # windshield + rear window
res_ = bmesh.ops.inset_region(bmg, faces=frit_faces, thickness=.045, depth=0.0, use_even_offset=True, use_boundary=True)
gme.materials.append(M['TS_Atlas']); FRIT_SLOT = len(gme.materials) - 1
for f in res_['faces']: f.material_index = FRIT_SLOT
bmesh.ops.dissolve_limit(bmg, angle_limit=math.radians(3.0), use_dissolve_boundaries=False, edges=[e for e in bmg.edges if len(e.link_faces) == 2], verts=[], delimit={'MATERIAL'})   # window glass is near-planar
bmesh.ops.triangulate(bmg, faces=[f for f in bmg.faces if len(f.verts) > 4])
bmg.to_mesh(gme); bmg.free(); gme.update()
fa = gme.attributes.get('cell') or gme.attributes.new('cell', 'INT', 'FACE'); fa.data.foreach_set('value', [CELLS.index('frit') if p.material_index == FRIT_SLOT else -1 for p in gme.polygons])
for sx in (1, -1):
    sh_ = lambda y, z: shit(sx, y, z)
    for (ya, yb, t) in ((.31, .41, 'TS_Atlas:gloss_black'),):                                         # B-pillar applique (no quarter divider)
        rows = []
        for z_ in np.linspace(0, 1, 5):
            row = []
            for y in (ya, yb):
                z0 = ZBELT(y) + .04; z1 = lerp(ZBELT(y) + .028, ZC(y) - .065, .92) - .028; p = ptat(sh_, y, lerp(z0, z1, z_), -.003); row.append(p)
            rows.append(row)
        if all(p is not None for r in rows for p in r): TR.grid(rows, t, flip=sx > 0)
    ys_ = np.linspace(COWL + .12, 1.47, 18)                                                              # satin aluminium belt trim (premium DLO line)
    ribbon(TR, lambda y_, z_: shit(sx, y_, z_), [(y, ZBELT(y) + .016) for y in ys_], .009, -.003, 'TS_Atlas:alu_brushed')
trim = mk('Trim_Parts', TR.V, TR.F, TR.T, WORK, M); lights = mk('Lights_LOD0', LI.V, LI.F, LI.T, WORK, M)
for o in (trim, lights): clean(o); orient_out(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(35))
REPORT['trim_parts_tris'], REPORT['lights_tris'] = tris(trim), tris(lights)
save_ckp(CKP_ + '_03_parts_lights.blend') if LAST >= 3 else None
if LAST <= 3: sys.exit(0)
# ================================================================ 04 wheels: 205/55 R16 on a 16" 10-spoke alloy (5 double spokes), lug nuts, centre cap, ventilated disc, caliper
WREF = {'FL': Vector((XF, YF, RW)), 'FR': Vector((-XF, YF, RW)), 'RL': Vector((XR, YR, RW)), 'RR': Vector((-XR, YR, RW))}
WSEG = {0: (20, 20), 1: (14, 12), 2: (10, 8), 3: (8, 6)}                                                 # (tire, rim) segments per LOD
def build_wheel(c, k, coll_):
    sx = 1 if c[1] == 'L' else -1; hw = WT / 2; st, sr = WSEG[k]; g = Geo(); out = {}
    # tire: bead -> sidewall bulge (max section at 45 % height) -> shoulder radius -> slightly crowned tread (real 55-series profile)
    prof = [(-hw * .80, RIM + .006), (-hw * .96, RIM + .020), (-hw * 1.0, RW - .072), (-hw * .985, RW - .040), (-hw * .90, RW - .012), (-hw * .70, RW - .002), (0, RW),
            (hw * .70, RW - .002), (hw * .90, RW - .012), (hw * .985, RW - .040), (hw * 1.0, RW - .072), (hw * .96, RIM + .020), (hw * .80, RIM + .006)]
    prof = [prof[i] for i in ((0, 2, 3, 4, 6, 8, 9, 10, 12) if k <= 1 else (0, 2, 4, 6, 8, 10, 12))]
    Vt, Ft, UVt = revolve(prof, st, sx, a0=-math.pi / 2); n0 = len(g.V); g.add(Vt, Ft, 'TS_Tire'); tire_uv = UVt          # vertex at the contact patch at every LOD
    face = hw * .48
    lip = [(hw * .80, RIM + .006), (hw * .86, RIM - .004), (hw * .55, RIM - .020)]
    if k <= 2: V_, F_, _ = revolve(lip, sr, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')                      # machined rim lip
    barrel = [(hw * .55, RIM - .020), (-hw * .80, RIM - .028), (-hw * .80, RIM + .006)]
    if k <= 2: V_, F_, _ = revolve(barrel, max(8, sr // 2 + 4), sx); g.add(V_, F_, 'TS_Atlas:wheel_dark')
    if k <= 2:
        nsp = 10 if k <= 1 else 5; DISH = .034
        for s_ in range(nsp):                                                                               # curved twin spokes, concave dish, machined (bright) front face, dark painted sides
            a_ = 2 * math.pi * s_ / nsp                                                                     # ten straight, evenly spaced, tapering spokes
            secs = []
            for t in ((0.0, .5, 1.0) if k == 0 else (0.0, 1.0)):
                r_ = lerp(.066, RIM - .016, t); w = lerp(.0115, .0075, t) * (1.0 if nsp == 10 else 1.6); xx = face - DISH * (1 - t) ** 1.6 + .006
                Rm = Matrix.Rotation(a_, 3, 'X')
                secs.append([Rm @ Vector((sx * xx, -w, r_)), Rm @ Vector((sx * xx, w, r_)), Rm @ Vector((sx * (xx - .026), w * 1.25, r_)), Rm @ Vector((sx * (xx - .026), -w * 1.25, r_))])
            for A, B in zip(secs, secs[1:]):
                for q in range(4):
                    f = [A[q], A[(q + 1) % 4], B[(q + 1) % 4], B[q]]; g.add(f, [(0, 1, 2, 3) if sx > 0 else (3, 2, 1, 0)], 'TS_Atlas:wheel_silver' if q == 0 else 'TS_Atlas:wheel_dark')
        hub = [(face - DISH - .002, .070), (face - DISH + .004, .042), (face - DISH + .008, .030)]
        V_, F_, _ = revolve(hub, 10 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')
        V_, F_, _ = revolve([(face - DISH + .010, .030), (face - DISH + .014, .022), (face - DISH + .015, 0.0)], 10 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:badge')     # centre cap
        if k == 0:
            for s_ in range(5):                                                                             # lug nuts (5 x 114.3 PCD)
                a_ = 2 * math.pi * (s_ + .5) / 5; cy, cz = .0572 * math.cos(a_), .0572 * math.sin(a_); hx = [(cy + .0095 * math.cos(2 * math.pi * q / 6), cz + .0095 * math.sin(2 * math.pi * q / 6)) for q in range(6)]
                A = [Vector((sx * (face - DISH - .002), y, z)) for y, z in hx]; Bv = [Vector((sx * (face - DISH + .012), y, z)) for y, z in hx]
                g.strip(A, Bv, 'TS_Atlas:lug', closed=True, flip=sx < 0)
    else:
        V_, F_, _ = revolve([(face - .03, 0.0), (face - .03, RIM - .02)], 8, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')   # LOD3: flat face disc
    if k <= 2:                                                                                              # ventilated disc (280 mm) with hat (rotates with the wheel)
        rd = .172; V_, F_, _ = revolve([(-hw * .25, .105), (-hw * .25, rd), (-hw * .55, rd)], 12 if k <= 1 else 8, sx); g.add(V_, F_, 'TS_Atlas:brake_disc')
        V_, F_, _ = revolve([(face - .030, .090), (-hw * .25, .105)], 10 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:caliper')
    o = mk(f'Wheel_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    uvl = o.data.uv_layers.new(name='tireUV')
    for p in o.data.polygons:
        for li in p.loop_indices:
            vi = o.data.loops[li].vertex_index; uvl.data[li].uv = tire_uv[vi] if vi < len(tire_uv) else (0, 0)
    out['Wheel'] = o
    if k <= 2:                                                                                              # floating caliper (static / steers, does not roll)
        g = Geo(); front = c[0] == 'F'; a0, a1 = (math.radians(20), math.radians(70)) if front else (math.radians(110), math.radians(160)); n_ = 6 if k <= 1 else 3
        secs = []
        for q in range(n_ + 1):
            a = lerp(a0, a1, q / n_); ca, sa = math.cos(a) * (1 if front else -1), math.sin(a)
            pts = [(.128, sx * (-hw * .10)), (.190, sx * (-hw * .10)), (.190, -sx * hw * .62), (.128, -sx * hw * .62)]
            secs.append([Vector((xx, rr * ca, rr * sa)) for rr, xx in pts])
        for A, B in zip(secs, secs[1:]): g.strip(A, B, 'TS_Atlas:caliper', closed=True)
        g.add(secs[0], [(0, 1, 2, 3)], 'TS_Atlas:caliper'); g.add(secs[-1], [(3, 2, 1, 0)], 'TS_Atlas:caliper')
        out['Caliper'] = mk(f'Caliper_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    for key, o in out.items():
        clean(o); orient_out(o, centre=(0, 0, 0)) if key == 'Caliper' else None
        o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40 if key != 'Wheel' else 50))
        o.data.transform(Matrix.Translation(WREF[c])); set_origin(o, WREF[c])
    return out
WH = coll('TS_WHEELS'); ASM = {}
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key, o in build_wheel(c, k, WH).items(): ASM[(k, c, key)] = o
save_ckp(CKP_ + '_04_wheels.blend') if LAST >= 4 else None
# ================================================================ 05 interior (visible through the glass): seats + headrests, rear bench, dashboard, cluster, wheel, console, door cards, headliner
IN = Geo(); DRV = .38; DY = .24                                                                     # cabin sits ~1 m behind the cowl (cab-rearward)
for sx in (1, -1):
    xs_ = sx * DRV; tilt = Matrix.Rotation(-.30, 3, 'X')
    IN.rbox((xs_, -.12 + DY, .42), (.26, .27, .06), 'TS_Atlas:fabric_light', .03)                             # front seat cushion (light leather)
    IN.rbox((xs_, .16 + DY, .76), (.25, .06, .30), 'TS_Atlas:fabric_light', .04, tilt)                        # backrest
    IN.rbox((xs_, .23 + DY, 1.13), (.13, .05, .08), 'TS_Atlas:fabric_light', 0, tilt)                         # headrest
    IN.rbox((sx * .84, .20 + DY, .62), (.03, 1.12, .29), 'TS_Atlas:int_plastic', 0)                           # door cards
    IN.rbox((sx * .812, .20 + DY, .74), (.03, 1.02, .02), 'TS_Atlas:fabric_light', 0)                         # armrest line
    IN.rbox((sx * .815, .20 + DY, .80), (.012, 1.0, .008), 'TS_Atlas:alu_brushed', 0)                         # door trim inlay
    IN.rbox((sx * .37, 1.05 + DY, 1.08), (.12, .05, .075), 'TS_Atlas:fabric_light', 0, Matrix.Rotation(-.20, 3, 'X'))   # rear headrests
IN.rbox((0, .78 + DY, .44), (.72, .26, .07), 'TS_Atlas:fabric_light', 0); IN.rbox((0, 1.02 + DY, .75), (.72, .07, .30), 'TS_Atlas:fabric_light', 0, Matrix.Rotation(-.30, 3, 'X'))  # rear bench
IN.rbox((0, -.78 + DY, .86), (.78, .17, .07), 'TS_Atlas:int_plastic', .04); IN.rbox((0, -.66 + DY, .76), (.76, .06, .06), 'TS_Atlas:int_plastic', 0)   # dashboard
IN.rbox((0, -.615 + DY, .80), (.76, .004, .012), 'TS_Atlas:alu_brushed', 0)                                  # dash trim inlay
IN.rbox((DRV, -.64 + DY, .935), (.15, .05, .03), 'TS_Atlas:int_plastic', 0); IN.rbox((DRV, -.60 + DY, .905), (.13, .004, .035), 'TS_Atlas:screen', .002)  # cluster
IN.rbox((0, -.70 + DY, .90), (.16, .01, .065), 'TS_Atlas:screen', .004, Matrix.Rotation(.25, 3, 'X'))       # centre display
IN.rbox((0, -.28 + DY, .45), (.10, .42, .12), 'TS_Atlas:int_plastic', 0); IN.rbox((0, -.18 + DY, .58), (.04, .05, .03), 'TS_Atlas:leather', .015)   # console + selector
IN.rbox((0, 1.30 + DY, 1.00), (.70, .22, .02), 'TS_Atlas:fabric_dark', 0)                                 # parcel shelf
hub = Vector((DRV, -.45 + DY, .86)); tilt = Matrix.Rotation(math.radians(-62), 3, 'X'); seg, sg2 = 10, 4
for q in range(seg):
    a0, a1 = 2 * math.pi * q / seg, 2 * math.pi * (q + 1) / seg
    ring = lambda a: [hub + tilt @ Vector((.185 * math.cos(a) + .016 * math.cos(2 * math.pi * k / sg2) * math.cos(a), .016 * math.sin(2 * math.pi * k / sg2), .185 * math.sin(a) + .016 * math.cos(2 * math.pi * k / sg2) * math.sin(a))) for k in range(sg2)]
    IN.strip(ring(a0), ring(a1), 'TS_Atlas:leather', closed=True)
IN.rbox(tuple(hub + tilt @ Vector((0, .02, 0))), (.06, .03, .05), 'TS_Atlas:leather', .02, tilt)
for a in (0, math.pi, -math.pi / 2): IN.rbox(tuple(hub + tilt @ Vector((.10 * math.cos(a), .01, .10 * math.sin(a)))), (.06 if a != -math.pi / 2 else .014, .01, .014 if a != -math.pi / 2 else .05), 'TS_Atlas:int_plastic', .004, tilt)
interior = mk('Interior_LOD0', IN.V, IN.F, IN.T, WORK, M); clean(interior); interior.data.shade_smooth(); interior.data.set_sharp_from_angle(angle=math.radians(40))
liner = LO.copy(); liner.data = LO.data.copy(); WORK.objects.link(liner); bm = bmesh.new(); bm.from_mesh(liner.data); bm.normal_update()
bmesh.ops.delete(bm, geom=[f for f in bm.faces if not (f.calc_center_median().z > ZBELT(f.calc_center_median().y) + .02 and CAB(f.calc_center_median().y) > .5 and abs(f.calc_center_median().x) < .95)], context='FACES')
for v in bm.verts: v.co -= v.normal * .018
bmesh.ops.reverse_faces(bm, faces=bm.faces); bm.to_mesh(liner.data); bm.free()
liner.data.materials.clear(); liner.data.materials.append(M['TS_Atlas']); la = liner.data.attributes.get('cell') or liner.data.attributes.new('cell', 'INT', 'FACE'); la.data.foreach_set('value', [CELLS.index('carpet')] * len(liner.data.polygons))   # anthracite headliner / pillar trim (unique cell: dropped at LOD2+)
decim_ = liner.modifiers.new('d', 'DECIMATE'); decim_.ratio = .16; decim_.use_symmetry = True
with bpy.context.temp_override(object=liner, active_object=liner): bpy.ops.object.modifier_apply(modifier='d')
for l_ in list(liner.data.uv_layers): liner.data.uv_layers.remove(l_)
interior = join([interior, liner], 'Interior_LOD0', WORK); clean(interior)
interior.data.shade_smooth(); interior.data.set_sharp_from_angle(angle=math.radians(40))
REPORT['interior_tris'] = tris(interior)
save_ckp(CKP_ + '_05_interior.blend') if LAST >= 5 else None
# ================================================================ 06 merge, UVs, AO + grime bake (all LOD0 parts in place -> real contact occlusion)
TMAP = {'TMP_seal': 'gloss_black', 'TMP_pocket': 'plastic_black', 'TMP_housing': 'lamp_housing', 'TMP_grille': 'grille', 'TMP_plastic': 'plastic_black', 'TMP_arch': 'arch_liner', 'TMP_plate': 'plastic_black'}
def tmp_to_atlas(o):
    me = o.data; names = [m.name for m in me.materials]; idx = [p.material_index for p in me.polygons]
    a = me.attributes.get('cell') or me.attributes.new('cell', 'INT', 'FACE'); vals = [CELLS.index(TMAP[names[i]]) if names[i] in TMAP else -1 for i in idx]
    me.materials.clear(); me.materials.append(M['TS_Atlas']); me.polygons.foreach_set('material_index', [0] * len(idx)); a.data.foreach_set('value', vals)
tmp_to_atlas(BODYTRIM)
d_ = BODYTRIM.modifiers.new('d', 'DECIMATE'); d_.decimate_type = 'DISSOLVE'; d_.angle_limit = math.radians(4.0); d_.delimit = {'MATERIAL', 'NORMAL'}
with bpy.context.temp_override(object=BODYTRIM, active_object=BODYTRIM): bpy.ops.object.modifier_apply(modifier='d')
bm = bmesh.new(); bm.from_mesh(BODYTRIM.data); bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4]); bm.to_mesh(BODYTRIM.data); bm.free()   # planar cut walls: dissolve flat facets
L0 = coll('LOD0_PARTS')
trim0 = join([BODYTRIM, trim], 'Trim_LOD0', L0)
for g_ in [GLASS]:
    g_.name = g_.data.name = 'Glass_LOD0'; link_only(g_, L0)
LO.name = LO.data.name = 'Body_LOD0'; link_only(LO, L0); link_only(lights, L0); link_only(interior, L0)
for o in (trim0, lights, interior, GLASS): atlas_uvs(o)
for k_ in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key in ('Wheel', 'Caliper'):
            o = ASM.get((k_, c, key))
            if o: atlas_uvs(o)
trim0.data.shade_smooth(); trim0.data.set_sharp_from_angle(angle=math.radians(35)); GLASS.data.shade_smooth()
for o in [x for x in bpy.data.objects if x.type == 'MESH']: purge_slots(o)
if BLOCKOUT:                                                                                           # design blockout: master body (smooth, real openings + gaps) + glass, lamps, trim, LOD0 wheels, interior
    for n_ in [o.name for o in bpy.data.objects if o.type == 'MESH' and (o.name in ('Body_LOD0', 'REF_Skin') or (('_LOD' in o.name) and not o.name.endswith('_LOD0')))]: bpy.data.objects.remove(bpy.data.objects[n_], do_unlink=True)
    HI.hide_render = HI.hide_viewport = False; HI.name = 'Body_Blockout'; link_only(HI, L0)
    bm = bmesh.new(); bm.from_mesh(HI.data); mats = HI.data.materials
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if mats[f.material_index] and mats[f.material_index].name == 'TS_Glass'], context='FACES'); bm.to_mesh(HI.data); bm.free(); purge_slots(HI)
    for m in HI.data.materials:
        if m and m.name.startswith('TMP_'):
            m.use_nodes = True; b_ = m.node_tree.nodes['Principled BSDF']; b_.inputs['Base Color'].default_value = (.015, .015, .016, 1); b_.inputs['Roughness'].default_value = .5
    def _inst(src, name, **kw):
        m = bpy.data.materials[src].copy(); m.name = name; m['instance_of'] = src; nt = m.node_tree
        if 'col' in kw: next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED').inputs['Base Color'].default_value = (*kw['col'], 1)
        if 'ns' in kw:
            for n in nt.nodes:
                if n.type == 'NORMAL_MAP': n.inputs['Strength'].default_value = kw['ns']
        return m
    GLb, INb = _inst('TS_Glass', PRE + '_Glass', col=(.78, .84, .82)), _inst('TS_Atlas', PRE + '_Interior', ns=.12)
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        for i, m in enumerate(o.data.materials):
            if m and m.name == 'TS_Glass' and o.name.startswith('Glass'): o.data.materials[i] = GLb
            if m and m.name == 'TS_Atlas' and o.name.startswith('Interior'): o.data.materials[i] = INb
    bb = [HI.matrix_world @ Vector(c) for c in HI.bound_box]
    REPORT['blockout'] = dict(master_tris=tris(HI), length=round(max(v.y for v in bb) - min(v.y for v in bb), 3), width_body=round(max(v.x for v in bb) - min(v.x for v in bb), 3),
                              height=round(max(v.z for v in bb), 3), min_z=round(min(v.z for v in bb), 3), lod0_parts_tris={o.name: tris(o) for o in bpy.data.objects if o.type == 'MESH'})
    os.makedirs(OUTD('reports', 'x') and os.path.dirname(OUTD('reports', 'x')), exist_ok=True)
    json.dump(dict(DIM=DIM, wheel_centres=dict(YF=YF, YR=YR, RW=RW), cowl=COWL, dash_to_axle=round(COWL - YF, 3), **REPORT), open(OUTD('reports', 'TS_SedanB_blockout_stats.json'), 'w'), indent=1)
    p_ = OUTD('blend', CKP_ + '_01_blockout.blend'); assert SCR or not os.path.exists(p_)
    bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=p_, copy=True, relative_remap=True); print('SAVED BLOCKOUT', p_, REPORT['blockout'], flush=True); sys.exit(0)
def bake_ao_grime(body, res, path):
    """AO with every LOD0 part in place (wheels, trim, interior occlude) + road-grime mask (low on the body, in cavities). R = AO, G = grime."""
    for o in bpy.data.objects:
        if o.type == 'MESH': o.hide_render = not (o.name in L0.objects or (o.name.endswith('_LOD0') and o.name.startswith(('Wheel', 'Caliper'))))
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 96
    imgs = {}
    for kind in ('AO', 'EMIT'):
        img = bpy.data.images.new(f'bake_{kind}', res, res, alpha=False); img.colorspace_settings.name = 'Non-Color'; imgs[kind] = img
        bm_ = bpy.data.materials.new('BAKE_TMP'); bm_.use_nodes = True; nt = bm_.node_tree; tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = img; nt.nodes.active = tn
        if kind == 'EMIT':
            em = nt.nodes.new('ShaderNodeEmission'); tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
            mr.inputs['From Min'].default_value = .18; mr.inputs['From Max'].default_value = .62; mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
            nt.links.new(tc.outputs['Object'], sp.inputs[0]); nt.links.new(sp.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs[0], em.inputs['Color'])
            nt.links.new(em.outputs[0], nt.nodes['Material Output'].inputs[0])
        saved = [m for m in body.data.materials]; body.data.materials.clear(); body.data.materials.append(bm_)
        for o in bpy.context.view_layer.objects: o.select_set(o == body)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.bake(type=kind, margin=8, use_clear=True); body.data.materials.clear()
        for m in saved: body.data.materials.append(m)
        bpy.data.materials.remove(bm_)
    ao = np.array(imgs['AO'].pixels[:]).reshape(res, res, 4)[..., 0]; low = np.array(imgs['EMIT'].pixels[:]).reshape(res, res, 4)[..., 0]
    grime = np.clip(.75 * low ** 1.6 + .45 * np.clip(.85 - ao, 0, 1), 0, 1) * .8
    out = np.dstack([ao, grime, np.zeros_like(ao), np.ones_like(ao)])
    im = bpy.data.images.new(os.path.basename(path)[:-4], res, res, alpha=True); im.colorspace_settings.name = 'Non-Color'; im.pixels.foreach_set(out.astype(np.float32).ravel())
    im.filepath_raw = path; im.file_format = 'PNG'; im.save()
    for o in bpy.data.objects:
        if o.type == 'MESH': o.hide_render = False
    HI.hide_render = True; REF.hide_render = True; return path
AOMASK = bake_ao_grime(LO, int(os.environ.get('TS_AO_RES', 1024)), OUTD('textures', f'{PRE}_Body_AO_Grime.png'))
M.update(paint_material(PRE + '_Paint', PAINT_RGB, dict(normal=NORMAL0, aomask=AOMASK), TEX))
T0_ = {o.name: tris(o) for o in bpy.data.objects if o.type == 'MESH' and o.name.endswith('_LOD0')}; REPORT['lod0_parts'] = T0_; REPORT['lod0_total'] = sum(T0_.values())
print('LOD0', REPORT['lod0_total'], T0_, flush=True)
save_ckp(CKP_ + '_06_materials_uv.blend') if LAST >= 6 else None
# ================================================================ 07 LODs: body re-baked at LOD1 (1024); own normals (sharp 35-40 deg) on every hard-surface part; LOD3 drops the interior detail + lenses
def decim(o, ratio):
    if ratio >= .999: return o
    m = o.modifiers.new('dec', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = ratio; m.use_symmetry = True; m.symmetry_axis = 'X'; m.use_collapse_triangulate = True
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='dec')
    clean(o); return o
RK = {1: dict(Body=.44, Glass=.8, Trim=.36, Lights=1.0, Interior=.40), 2: dict(Body=.17, Glass=.5, Trim=.13, Lights=.55, Interior=.15), 3: dict(Body=.065, Glass=.25, Trim=.05, Lights=1.0, Interior=.12)}
if os.environ.get('TS_RK'): RK = {int(k): v for k, v in json.loads(os.environ['TS_RK']).items()}
for k in (1, 2, 3):
    Lk = coll(f'LOD{k}_PARTS')
    for kind in ('Body', 'Glass', 'Trim', 'Lights', 'Interior'):
        o0 = bpy.data.objects[f'{kind}_LOD0']; d = o0.copy(); d.data = o0.data.copy(); Lk.objects.link(d); d.name = d.data.name = f'{kind}_LOD{k}'
        if kind == 'Lights':                                                                             # deterministic light LODs: drop detail, never emitters
            DROP = {1: {'lamp_inner', 'lamp_housing'}, 2: {'lamp_inner', 'reflector', 'lamp_housing'}, 3: {'lamp_inner', 'reflector', 'lamp_housing', 'LENS'}}[k]
            bm = bmesh.new(); bm.from_mesh(d.data); mats = d.data.materials; cl = bm.faces.layers.int.get('cell')
            def drop(f):
                mn = mats[f.material_index].name
                if mn in ('TS_Lens', 'TS_LensRed'): return 'LENS' in DROP
                return mn == 'TS_Atlas' and 0 <= f[cl] < 100 and CELLS[f[cl]] in DROP
            bmesh.ops.delete(bm, geom=[f for f in bm.faces if drop(f)], context='FACES'); bm.to_mesh(d.data); bm.free(); purge_slots(d)
        if kind == 'Body':                                                                               # mirrors + fin decimated gently (silhouette width / height kept)
            bm = bmesh.new(); bm.from_mesh(d.data); bm.verts.ensure_lookup_table()
            ext = [f for f in bm.faces if (abs(f.calc_center_median().x) > .93 and f.calc_center_median().z > .92) or (abs(f.calc_center_median().x) < .045 and f.calc_center_median().z > ZC(f.calc_center_median().y) - .005 and .78 < f.calc_center_median().y < 1.10)]
            sub_ = bmesh.ops.split(bm, geom=ext); bm.to_mesh(d.data); bm.free()
            ex = d.copy(); ex.data = d.data.copy(); Lk.objects.link(ex)
            for ob, keep_ext in ((d, False), (ex, True)):
                bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
                isx = lambda f: (abs(f.calc_center_median().x) > .93 and f.calc_center_median().z > .92) or (abs(f.calc_center_median().x) < .045 and f.calc_center_median().z > ZC(f.calc_center_median().y) - .005 and .78 < f.calc_center_median().y < 1.10)
                bmesh.ops.delete(bm, geom=[f for f in bm.faces if isx(f) != keep_ext], context='FACES'); bm.to_mesh(ob.data); bm.free()
            vg_ = d.vertex_groups.new(name='keep_extremes'); ys_ = [v.co.y for v in d.data.vertices]; ymin_, ymax_ = min(ys_), max(ys_)
            vg_.add([v.index for v in d.data.vertices if v.co.y > ymax_ - .006 or v.co.y < ymin_ + .006], 1.0, 'REPLACE')     # bumper crowns define the length: keep them
            m_ = d.modifiers.new('dec', 'DECIMATE'); m_.decimate_type = 'COLLAPSE'; m_.ratio = RK[k][kind]; m_.use_symmetry = True; m_.symmetry_axis = 'X'; m_.use_collapse_triangulate = True
            m_.vertex_group = 'keep_extremes'; m_.invert_vertex_group = True; m_.vertex_group_factor = 1.0
            with bpy.context.temp_override(object=d, active_object=d): bpy.ops.object.modifier_apply(modifier='dec')
            clean(d); d.vertex_groups.remove(d.vertex_groups['keep_extremes']); d = join([d, ex], f'Body_LOD{k}', Lk); clean(d)                              # mirrors + fin kept whole (tiny; exact silhouette)
            uvl_ = d.data.uv_layers.get('UVMap')
            if uvl_:
                for u_ in uvl_.data: u_.uv = (min(max(u_.uv.x, 0.0), 1.0), min(max(u_.uv.y, 0.0), 1.0))          # collapse can push seam UVs a hair outside 0-1
        else:
            if kind == 'Interior' and k >= 2:                                                           # mid / far: seats + dash only (the thin pillar liner spikes under heavy collapse)
                bm = bmesh.new(); bm.from_mesh(d.data); cl = bm.faces.layers.int.get('cell')
                bmesh.ops.delete(bm, geom=[f for f in bm.faces if cl and f[cl] == CELLS.index('carpet')], context='FACES'); bm.to_mesh(d.data); bm.free()
            pl_ = None
            if kind == 'Trim' and k >= 2:                                                               # r3: plate quads kept out of the collapse (it merged half of each plate into the holder)
                pl_ = d.copy(); pl_.data = d.data.copy(); Lk.objects.link(pl_)
                for ob, keep in ((pl_, True), (d, False)):
                    bm = bmesh.new(); bm.from_mesh(ob.data); cl = bm.faces.layers.int.get('cell')
                    bmesh.ops.delete(bm, geom=[f for f in bm.faces if (f[cl] == CELLS.index('plate')) != keep], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
            decim(d, RK[k][kind])
            if pl_: d = join([d, pl_], f'Trim_LOD{k}', Lk); clean(d)
            if kind == 'Trim' and k >= 2:                                                               # r3: distant plates = clean plate (blue band kept, glyph rows avoided)
                me_ = d.data; cl_ = me_.attributes.get('cell'); uv_ = me_.uv_layers['UVMap'].data; u0, v0, s_ = cell_rect('plate'); npl = 0
                for p_ in me_.polygons:
                    if cl_ and cl_.data[p_.index].value == CELLS.index('plate'):
                        npl += 1
                        for li in p_.loop_indices:
                            u, v = uv_[li].uv; uv_[li].uv = (u, v0 + s_ * (.88 + .06 * min(max((v - v0) / s_, 0.0), 1.0)))
                REPORT.setdefault('distant_plate_faces', {})[k] = npl
        if kind == 'Body':
            d.data.shade_smooth(); d.data.set_sharp_from_angle(angle=math.radians(48))
        else:
            with bpy.context.temp_override(object=d, active_object=d): bpy.ops.mesh.customdata_custom_splitnormals_clear()
            d.data.shade_smooth(); d.data.set_sharp_from_angle(angle=math.radians(35 if kind != 'Glass' else 60))
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key in ('Wheel', 'Caliper'):
            o = ASM.get((k, c, key))
            if o: link_only(o, Lk)
NORMAL1 = bake_normal(bpy.data.objects['Body_LOD1'], HI, f'{PRE}_Body_Normal_LOD1', 1024, OUTD('textures', f'{PRE}_Body_Normal_LOD1.png'))
M.update(paint_material(PRE + '_Paint_LOD1', PAINT_RGB, dict(normal=NORMAL1, aomask=AOMASK), TEX))
M.update(paint_material(PRE + '_Paint_Far', PAINT_RGB, dict(normal=None, aomask=None), TEX) if False else paint_material(PRE + '_Paint_Far', PAINT_RGB, None, TEX))
for k, mname in ((1, PRE + '_Paint_LOD1'), (2, PRE + '_Paint_Far'), (3, PRE + '_Paint_Far')):
    me = bpy.data.objects[f'Body_LOD{k}'].data
    for i, m in enumerate(me.materials):
        if m.name == PRE + '_Paint': me.materials[i] = M[mname]
bpy.data.objects.remove(HI, do_unlink=True); bpy.data.objects.remove(REF, do_unlink=True)
def move_atlas(src, dst):
    cp = src.copy(); cp.data = src.data.copy(); dst.users_collection[0].objects.link(cp)
    for ob, keep in ((cp, True), (src, False)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if (mats[f.material_index].name == 'TS_Atlas') != keep], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    purge_slots(src); purge_slots(cp)
    if not cp.data.polygons: bpy.data.objects.remove(cp, do_unlink=True); return dst
    nm = dst.name; return join([dst, cp], nm, dst.users_collection[0])
for k in range(4):
    for kind in ('Lights', 'Glass'): move_atlas(bpy.data.objects[f'{kind}_LOD{k}'], bpy.data.objects[f'Trim_LOD{k}'])
REPORT['submesh_merge'] = 'TS_Atlas faces of Lights_LODk and Glass_LODk (reflectors, housings, frit) moved into Trim_LODk'
REPORT['lod_ratios'] = RK
save_ckp(CKP_ + '_07_lods.blend') if LAST >= 7 else None
# ================================================================ 08 hierarchy, pivots, colliders, references
FIN = coll('TRAFFIC_SEDAN_B'); COLL = coll('TS_COLLIDERS', FIN)
root = empty('Car_Root', FIN, (0, 0, 0), None, 'PLAIN_AXES', .5)
for k in range(4):
    lr = empty(f'LOD{k}_Root', FIN, (0, 0, 0), root, 'PLAIN_AXES', .3)
    for n in ('Body', 'Glass', 'Trim', 'Lights', 'Interior'):
        o = bpy.data.objects.get(f'{n}_LOD{k}')
        if not o: continue
        link_only(o, FIN); set_origin(o, (0, 0, 0)); mw = o.matrix_world.copy(); o.parent = lr; o.matrix_world = mw
    for c in ('FL', 'FR', 'RL', 'RR'):
        w = ASM[(k, c, 'Wheel')]; cal = ASM.get((k, c, 'Caliper')); parent = lr
        if c in ('FL', 'FR'): parent = empty(f'SteerPivot_{c}_LOD{k}', FIN, WREF[c], lr, 'ARROWS', .15); bpy.context.view_layer.update()
        local = Matrix.Identity(4) if parent is not lr else Matrix.Translation(WREF[c])
        link_only(w, FIN); w.parent = parent; w.matrix_parent_inverse = Matrix.Identity(4); w.matrix_basis = local
        if cal: link_only(cal, FIN); cal.parent = parent; cal.matrix_parent_inverse = Matrix.Identity(4); cal.matrix_basis = local
        bpy.context.view_layer.update()
def hull(name, verts):
    cell = .05
    while True:
        pts = list({(round(v.x / cell), round(v.y / cell), round(v.z / cell)): v for v in verts}.values())
        pts += [max(verts, key=lambda v: v[i] * sg) for i in range(3) for sg in (1, -1)]
        bm = bmesh.new(); vv = [bm.verts.new(v) for v in pts]; bmesh.ops.convex_hull(bm, input=vv)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bmesh.ops.triangulate(bm, faces=bm.faces); bm.normal_update()
        convex = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 5e-4 for v in bm.verts) for f in bm.faces)
        if (len(bm.faces) <= 200 and convex) or cell > .4: break
        bm.free(); cell *= 1.3
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); COLL.objects.link(o); o.display_type = 'WIRE'; return o
pts = [bpy.data.objects[f'{n}_LOD2'].matrix_world @ v.co for n in ('Body', 'Glass') for v in bpy.data.objects[f'{n}_LOD2'].data.vertices]
CL = {'Collision_Front': [p for p in pts if p.y < -1.20 and p.z < .98], 'Collision_Body': [p for p in pts if -1.40 < p.y < 1.15 and p.z < .97],
      'Collision_Cabin': [p for p in pts if COWL - .05 < p.y < 1.80 and p.z > .90], 'Collision_Rear': [p for p in pts if p.y > .95 and p.z < 1.12]}
cr = empty('Collision', FIN, (0, 0, 0), root, 'PLAIN_AXES', .2)
for n, vs in CL.items():
    if len(vs) > 8: h = hull(n, vs); h.parent = cr
for c in ('FL', 'FR', 'RL', 'RR'):
    e = empty(f'WheelColliderRef_{c}', FIN, WREF[c], root, 'SPHERE', .1); e['radius_m'] = RW; e['width_m'] = WT
empty('CenterOfMass', FIN, (0, -.08, .53), root, 'SPHERE', .08)                                       # front-engine RWD executive sedan: ~52/48 front bias, 0.53 m high
for c in list(bpy.data.collections):
    if c.name not in ('TRAFFIC_SEDAN_B', 'TS_COLLIDERS'):
        for o in list(c.objects):
            if o.name not in FIN.all_objects: bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
# r3: revision-specific material INSTANCES (shared library untouched): lighter, realistic side-glass tint; interior with a softer fabric normal
def instance(src, name, **kw):
    m = bpy.data.materials[src].copy(); m.name = name; m['instance_of'] = src; nt = m.node_tree
    if 'col' in kw:
        b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs['Base Color'].default_value = (*kw['col'], 1); m['unity_alpha'] = kw['alpha']
    if 'nstrength' in kw:
        for n in nt.nodes:
            if n.type == 'NORMAL_MAP': n.inputs['Strength'].default_value = kw['nstrength']
    m['unity'] = kw['unity']; return m
GL_ = instance('TS_Glass', PRE + '_Glass', col=(.78, .84, .82), alpha=.22, unity='instance of TS_Glass: Lit transparent, base (0.78, 0.84, 0.82) alpha 0.22, smoothness 1.0 (light green automotive tint, ~75 % visible transmission)')
IN_ = instance('TS_Atlas', PRE + '_Interior', nstrength=.12, unity='instance of TS_Atlas (same textures / UVs): normal scale 0.12 (seat weave reads as fabric, not crumpled at cabin scale)')
for o in FIN.all_objects:
    if o.type != 'MESH': continue
    for i, m in enumerate(o.data.materials):
        if m and m.name == 'TS_Glass' and o.name.startswith('Glass_'): o.data.materials[i] = GL_
        if m and m.name == 'TS_Atlas' and o.name.startswith('Interior_'): o.data.materials[i] = IN_
REPORT['material_instances'] = {GL_.name: dict(GL_.items()), IN_.name: dict(IN_.items())}
json.dump(REPORT, open(OUTD('reports', 'TS_SedanB_build_log.json'), 'w'), indent=1)
save_ckp(CKP_ + '_08_rig.blend') if LAST >= 8 else None
