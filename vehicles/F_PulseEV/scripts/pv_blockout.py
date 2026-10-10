# Pulse EV (Phase F) — original premium electric four-door performance sedan, design blockout. Blender -b --factory-startup --python pv_blockout.py
# Enclosed EV nose with a slim lower cooling slot (active-shutter slats) and vertical corner air curtains, low smooth hood (flush with the fenders),
# short front overhang, long 2.95 m wheelbase, cab-forward four-door greenhouse with a panoramic glass roof and gloss-black rails, fastback into a
# clean deck with an integrated active lip spoiler, sculpted rear haunches, flush handles, slim camera-style mirrors, aero-cover wheels.
# Light signature "pulse line": a slim DRL blade per side with a small heartbeat-like blip near its inboard end above four segmented LED modules;
# rear: full-width red bar with the same blip at the centre, segmented vertical end blocks. No exhaust (fully electric).
# Convention: +Z up, nose -Y, vehicle left +X, 1 BU = 1 m.
# Surfacing = the refined Vortex R / Raven XR method: coarse evenly spaced quad cage from smooth pchip design curves, Taubin-faired along Y and
# around each section, Catmull-Clark subdivision, fender-crest crease fading out at nose + tail, and (Raven XR P0 lesson, from the start) rear-deck
# control points placed at the greenhouse x positions so the fastback-to-deck fade is purely vertical (no sail-to-deck bunching).
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, math, json
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = lambda *a: os.path.join(ROOT, *a)
SCR = os.environ.get('PV_SCRATCH')
def CKP(n):
    d = SCR or P('blend'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def REPD():
    d = os.path.join(SCR, 'reports') if SCR else P('reports'); os.makedirs(d, exist_ok=True); return d
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'
def ss(a, b, x): t = min(1.0, max(0.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t
def pchip(xk, yk):
    xk = np.asarray(xk, float); yk = np.asarray(yk, float); h = np.diff(xk); d = np.diff(yk) / h; m = np.zeros_like(yk)
    for i in range(1, len(xk) - 1):
        if d[i - 1] * d[i] > 0: w1 = 2 * h[i] + h[i - 1]; w2 = h[i] + 2 * h[i - 1]; m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    m[0], m[-1] = d[0], d[-1]
    def f(x):
        x = min(max(x, xk[0]), xk[-1]); i = min(len(h) - 1, max(0, int(np.searchsorted(xk, x) - 1))); t = (x - xk[i]) / h[i]
        return float((2 * t**3 - 3 * t**2 + 1) * yk[i] + (t**3 - 2 * t**2 + t) * h[i] * m[i] + (-2 * t**3 + 3 * t**2) * yk[i + 1] + (t**3 - t**2) * h[i] * m[i + 1])
    return f
# ================================================================ design parameters (metres)
DIM = dict(length=4.84, width_body=1.98, height=1.43, wheelbase=2.95, track_f=1.69, track_r=1.70, overhang_f=.905, overhang_r=.985, ground_clearance=.135,
           tire_f='265/35 R21 (R 0.359)', tire_r='295/30 R21 (R 0.355)')
YF, YR = -1.475, 1.475; RF, RR = .359, .355; WF, WR = .265, .295; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.38, 2.46
# centreline top: low enclosed nose -> low smooth hood -> cowl -> fast windshield -> long roof (peak over the B-pillar) -> fastback -> deck -> lip
ZC = pchip([YN, -2.22, -1.85, -1.475, -1.05, -.74, -.35, .10, .55, 1.00, 1.45, 1.82, 2.15, 2.36, YT], [.56, .725, .80, .845, .855, .885, 1.12, 1.37, 1.43, 1.405, 1.27, 1.115, 1.045, 1.05, 1.0])   # hood crown 1-2 cm above the shoulders (smooth convex EV hood, no valley)
ZBELT = pchip([YN, -2.22, -1.85, -1.475, -1.00, -.40, .40, 1.00, 1.475, 1.90, 2.25, YT], [.60, .71, .785, .825, .835, .865, .905, .955, .985, .975, .945, .90])   # shoulder / fender crest
WBELT = pchip([YN, -2.22, -1.85, -1.475, -1.00, -.40, .40, 1.00, 1.475, 1.90, 2.25, YT], [.64, .79, .855, .88, .865, .855, .865, .905, .935, .915, .86, .78])
WMAX = pchip([YN, -2.22, -1.85, -1.475, -1.00, -.30, .40, 1.00, 1.475, 1.90, 2.25, YT], [.82, .925, .97, .982, .962, .952, .958, .982, .99, .978, .945, .90])   # haunches at the rear axle
ZSH = pchip([YN, -1.475, 0, 1.475, YT], [.46, .56, .59, .61, .57])
ZFLOOR = pchip([YN, -2.20, -1.95, 1.95, 2.25, YT], [.30, .19, .135, .135, .20, .30])
WFLOOR = pchip([YN, -2.2, 0, 2.2, YT], [.62, .80, .84, .80, .70])
CAB = lambda y: ss(-.86, -.62, y) * (1 - ss(1.62, 1.88, y))                                         # greenhouse: windshield base -> fastback end
ROOFW = pchip([-.70, -.30, .20, .70, 1.20, 1.75], [.70, .668, .645, .63, .585, .52])                # roof-rail half-width (wide four-seat roof, tumblehome)
SK = lambda y: .018 * ss(-1.10, -.85, y) * (1 - ss(1.00, 1.25, y))                                 # subtle concave lower-door sculpt
def ring_half(y):
    zb, wf, wm, zs, zb_, wb, zc, c = ZFLOOR(y), WFLOOR(y), WMAX(y), ZSH(y), ZBELT(y), WBELT(y), ZC(y), CAB(y); sk = SK(y)
    side = [(0.0, zb), (.5 * wf, zb), (wf, zb + .005), (wm - .045 - sk * .3, zb + .07), (wm - .012 - sk, lerp(zb + .07, zs, .5)), (wm, zs), (lerp(wm, wb, .45), lerp(zs, zb_, .55)), (wb, zb_)]
    crown = lambda t: zb_ + (zc - zb_) * (1 - (1 - t) ** 2.0)
    rw = ROOFW(min(max(y, -.70), 1.75)); sw = wb - .055
    gh = [(wb - .04, zb_ + .008), (sw, zb_ + .03), (lerp(sw, rw, .80) + .01, lerp(zb_ + .03, zc - .06, .90)), (rw, zc - .035), (.50 * rw, zc - .008), (0.0, zc)]
    w = ss(.80, 1.40, y)                                                                              # Raven P0 rule: rear deck points at the greenhouse x (pure vertical fade)
    ts = [lerp(t, min(max(1 - g[0] / wb, 0.0), 1.0), w) for t, g in zip((.08, .26, .50, .74, .90, 1.0), gh)]
    deck = [(wb * (1 - t), crown(t)) for t in ts]
    top = [(lerp(d[0], g[0], c), lerp(d[1], g[1], c)) for d, g in zip(deck, gh)]
    return side + top
NS = len(ring_half(0.0))                                                                              # 14 points per half
I_GH = 9; I_ROOF = 11
STAT = [-2.26, -2.10, -1.92, -1.72, -1.52, -1.32, -1.12, -.92, -.72, -.52, -.32, -.12, .08, .28, .48, .68, .88, 1.08, 1.28, 1.48, 1.68, 1.88, 2.06, 2.22, 2.34]   # coarse, ~0.2 m
NOSE = [(YN + .04, 1.0), (YN + .012, .84), (YN, .50)]
TAIL = [(YT - .02, 1.0), (YT - .005, .93), (YT, .62)]
def full_ring(y, scale=1.0, centre=None):
    h = ring_half(y); cz = centre if centre is not None else (h[0][1] + h[-1][1]) * .5
    pts = [(x * scale, y, cz + (z - cz) * scale) for x, z in h]
    return pts + [(-x, yy, z) for x, yy, z in pts[1:-1]][::-1]
rings = []
for y, s in NOSE[::-1]: rings.append(full_ring(y, s, .42))
for y in STAT: rings.append(full_ring(y))
for y, s in TAIL: rings.append(full_ring(y, s, .64))
NR = len(rings[0])
def fair_cage(rings, iters=30, lam=.5, mu=-.53, fixed=2):
    R = np.array(rings, float); n = len(R)
    for it in range(iters):
        for f in (lam, mu):
            L = np.zeros_like(R); L[1:-1] = (R[:-2] + R[2:]) * .5 - R[1:-1]
            L[:fixed] = 0; L[n - fixed:] = 0; L[..., 1] = 0; R = R + f * L
    return [[tuple(p) for p in r] for r in R]
def fair_lateral(rings, iters=12, lam=.45, mu=-.48, lock=3):
    """Taubin smoothing around each ring (x, z only); the floor points (first `lock` and mirrored) stay fixed; centre-top stays on x = 0 by symmetry."""
    out = []
    for r in rings:
        R = np.array(r, float); n = len(R); fix = set(range(lock)) | set(range(n - lock + 1, n)) | {7, n - 7}          # floor + fender-crest character line stay fixed
        if CAB(r[0][1]) > .05: fix |= set(range(8, n - 7))                                       # greenhouse (DLO, rail, roof) is explicitly designed: fairing smooths the body side only
        for it in range(iters):
            for f in (lam, mu):
                L = (np.roll(R, 1, 0) + np.roll(R, -1, 0)) * .5 - R; L[list(fix)] = 0; L[:, 1] = 0; R = R + f * L
        R[NS - 1, 0] = 0.0; out.append([tuple(p) for p in R])
    return out
RAW_RINGS = [list(r) for r in rings]
rings = fair_lateral(fair_cage(rings))
CAGE_SHIFT_MM = float(np.abs(np.array(rings) - np.array(RAW_RINGS)).max() * 1000)
V = [p for r in rings for p in r]; F = []; FT = []
col_tag = lambda j: j if j < NS else NR - j
for i in range(len(rings) - 1):
    for j in range(NR):
        a = i * NR + j; b = i * NR + (j + 1) % NR; cc = (i + 1) * NR + (j + 1) % NR; d = (i + 1) * NR + j
        F.append((a, d, cc, b)); ym = (rings[i][0][1] + rings[i + 1][0][1]) / 2; h0, h1 = col_tag(j), col_tag((j + 1) % NR); FT.append((ym, min(h0, h1), max(h0, h1)))
for ri, flip in ((0, False), (len(rings) - 1, True)):
    r = rings[ri]; cidx = len(V); V.append(tuple(np.mean(np.array(r), axis=0)))
    for j in range(NR):
        f = (ri * NR + j, ri * NR + (j + 1) % NR, cidx); F.append(f[::-1] if not flip else f); FT.append(('cap', 0, 0))
def tag(t):
    if t[0] == 'cap': return 'paint'
    y, a, b = t
    if CAB(y) < .5: return 'paint'
    if a >= I_ROOF and -.66 < y < 1.66: return 'glass'                                                  # windshield + panoramic glass roof + rear glass (one sweep)
    if (a, b) == (10, 11) and -.66 < y < 1.66: return 'black'                                           # gloss-black roof rails / A-pillars
    if (a, b) == (9, 10) and -.58 < y < 1.50: return 'glass'                                            # side glass (front + rear doors + quarter light)
    if (a, b) == (8, 9) and -.62 < y < 1.54: return 'black'                                             # DLO surround / seals
    return 'paint'
TAGS = [tag(t) for t in FT]
# ================================================================ materials (blockout preview)
def pbr(name, col, metal=0.0, rough=.4, coat=0.0, alpha=1.0, emit=None, es=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat; b.inputs['Alpha'].default_value = alpha
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    if alpha < 1 and hasattr(m, 'surface_render_method'): m.surface_render_method = 'BLENDED'
    return m
MAT = dict(paint=pbr('PV_Paint', (.40, .43, .48), .92, .22, .7), glass=pbr('PV_Glass', (.004, .006, .010), 0, .03, .3, alpha=.72), black=pbr('PV_GlossBlack', (.008, .008, .009), 0, .1, .6),
           trim=pbr('PV_SatinBlack', (.016, .016, .018), .2, .5), aero=pbr('PV_AeroDark', (.022, .024, .028), .5, .42), mesh=pbr('PV_Shutter', (.012, .012, .014), .3, .45),
           rim=pbr('PV_WheelAero', (.030, .032, .036), .7, .40), rim_lip=pbr('PV_WheelLip', (.10, .105, .115), 1, .3), tire=pbr('PV_Tire', (.022, .022, .024), 0, .85),
           rotor=pbr('PV_Rotor', (.32, .32, .33), 1, .35), caliper=pbr('PV_Caliper', (.03, .16, .48), .2, .3, .6),
           leather=pbr('PV_Leather', (.30, .30, .31), 0, .55), int_dark=pbr('PV_IntDark', (.02, .02, .022), .1, .5), accent=pbr('PV_Accent', (.05, .25, .65), .6, .3),
           screen=pbr('PV_Display', (.02, .03, .05), 0, .1, emit=(.35, .55, .85), es=1.2),
           lens=pbr('PV_LensClear', (.8, .85, .9), 0, .02, .3, alpha=.12), drl=pbr('PV_LED_DRL', (.85, .92, 1), 0, .3, emit=(.80, .90, 1.0), es=12),
           tail=pbr('PV_LED_Tail', (.6, 0, .01), 0, .3, emit=(1, .01, .015), es=9), lensred=pbr('PV_LensRed', (.30, 0, .004), 0, .03, .3, alpha=.8),
           ind=pbr('PV_LED_Indicator', (.8, .3, 0), 0, .3, emit=(1, .35, 0), es=.7), rev=pbr('PV_LED_Reverse', (.9, .9, .9), 0, .3, emit=(1, 1, 1), es=.3))
CAR = bpy.data.collections.new('PULSE_EV'); sc.collection.children.link(CAR)
def obj(name, Vs, Fs, tags, parent=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in Vs], [], [tuple(f) for f in Fs]); me.update()
    order = list(dict.fromkeys(tags if not isinstance(tags, str) else [tags]))
    tl = tags if not isinstance(tags, str) else [tags] * len(Fs)
    for t in order: me.materials.append(MAT[t])
    me.polygons.foreach_set('material_index', [order.index(t) for t in tl]); me.update()
    o = bpy.data.objects.new(name, me); CAR.objects.link(o)
    if parent: o.parent = parent
    return o
body = obj('Body_Blockout', V, F, TAGS)
bm = bmesh.new(); bm.from_mesh(body.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(body.data); bm.free()
cr = body.data.attributes.new('crease_edge', 'FLOAT', 'EDGE'); nrings = len(rings); VB = body.data.vertices
crest = {i * NR + j for i in range(nrings) for j in (7, NR - 7)}
rail = {i * NR + j for i in range(nrings) if -.62 < rings[i][0][1] < 1.62 for j in (I_ROOF, NR - I_ROOF)}
for e in body.data.edges:
    a_, b_ = e.vertices
    if a_ in rail and b_ in rail and abs(a_ - b_) == NR: cr.data[e.index].value = .40                     # roof-rail edge (panoramic roof frame)
    if a_ in crest and b_ in crest and abs(a_ - b_) == NR:                                              # shoulder line: soft-crisp, fades at nose + tail
        ym_ = (VB[a_].co.y + VB[b_].co.y) / 2; cr.data[e.index].value = .50 * ss(-2.24, -1.92, ym_) * (1 - ss(1.80, 2.22, ym_))
REPORT = dict(cage=dict(stations=len(rings), points_per_ring=NR, cage_faces=len(F), fairing='Taubin 30 x (0.5, -0.53) along Y (2 end rings fixed) + 12 x (0.45, -0.48) around each section', max_control_point_shift_mm=round(CAGE_SHIFT_MM, 1)))
sub = body.modifiers.new('sub', 'SUBSURF'); sub.levels = sub.render_levels = 3
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='sub')
def cyl(r, x0, x1, y, z, seg=64):
    bm = bmesh.new(); r0 = [bm.verts.new((x0, y + r * math.cos(2 * math.pi * k / seg), z + r * math.sin(2 * math.pi * k / seg))) for k in range(seg)]; r1 = [bm.verts.new((x1, v.co.y, v.co.z)) for v in r0]
    for k in range(seg): bm.faces.new((r0[k], r0[(k + 1) % seg], r1[(k + 1) % seg], r1[k]))
    bm.faces.new(r0[::-1]); bm.faces.new(r1); bm.normal_update(); me = bpy.data.meshes.new('cut'); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('cut', me); sc.collection.objects.link(o); return o
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    c = cyl(r + .045, sx * .55, sx * 1.4, y, r + .012)
    m = body.modifiers.new('arch', 'BOOLEAN'); m.object = c; m.operation = 'DIFFERENCE'; m.solver = 'EXACT'
    with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='arch')
    bpy.data.objects.remove(c, do_unlink=True)
body.data.shade_smooth()
G = {'V': [], 'F': [], 'T': []}
def add(Vs, Fs, t):
    n = len(G['V']); G['V'] += [tuple(v) for v in Vs]; G['F'] += [tuple(i + n for i in f) for f in Fs]; G['T'] += ([t] * len(Fs) if isinstance(t, str) else t)
def strip(A, B, t, closed=False, flip=False):
    n = len(A); n0 = len(G['V']); G['V'] += [tuple(p) for p in A] + [tuple(p) for p in B]
    for i in range(n - (0 if closed else 1)):
        j = (i + 1) % n; f = (n0 + i, n0 + j, n0 + n + j, n0 + n + i); G['F'].append(f[::-1] if flip else f); G['T'].append(t)
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):                          # wheel-well liners
    R_ = r + .043; zc = r + .012; seg = 28; a0, a1 = math.radians(-25), math.radians(205)
    arc = [(y + R_ * math.cos(lerp(a0, a1, q / seg)), zc + R_ * math.sin(lerp(a0, a1, q / seg))) for q in range(seg + 1)]
    strip([(sx * .55, yy, zz) for yy, zz in arc], [(sx * (WMAX(y) - .015), yy, zz) for yy, zz in arc], 'trim', flip=sx > 0)
# ================================================================ surface-projected design details (blockout level)
BV = BVHTree.FromObject(body, bpy.context.evaluated_depsgraph_get())
def ray(o, d):
    loc, nrm, i, dist = BV.ray_cast(Vector(o), Vector(d))
    if loc is None: return None
    n = nrm if nrm.dot(Vector(d)) < 0 else -nrm; return loc, n
def fh(x, z, off): r = ray((x, -4, z), (0, 1, 0)); return r[0] + r[1] * off if r else None
def rh(x, z, off): r = ray((x, 4, z), (0, -1, 0)); return r[0] + r[1] * off if r else None
def sh(sx, y, z, off): r = ray((sx * 3, y, z), (-sx, 0, 0)); return r[0] + r[1] * off if r else None
def th(x, y, off): r = ray((x, y, 3), (0, 0, -1)); return r[0] + r[1] * off if r else None
def quad_patch(fn, corners, nu, nv, t, off, flip=False):
    """bilinear patch over 4 corner parameters (a, b) projected with fn(a, b, off)."""
    (a0, b0), (a1, b1), (a2, b2), (a3, b3) = corners; rows = []
    for j in range(nv + 1):
        v = j / nv; row = []
        for i in range(nu + 1):
            u = i / nu; a = lerp(lerp(a0, a1, u), lerp(a3, a2, u), v); b = lerp(lerp(b0, b1, u), lerp(b3, b2, u), v); row.append(fn(a, b, off))
        rows.append(row)
    if any(p is None for r in rows for p in r): print('PATCH MISS', t, corners); return
    n0 = len(G['V']); nc = nu + 1
    for r in rows: G['V'] += [tuple(p) for p in r]
    for j in range(nv):
        for i in range(nu):
            f = (n0 + j * nc + i, n0 + j * nc + i + 1, n0 + (j + 1) * nc + i + 1, n0 + (j + 1) * nc + i); G['F'].append(f[::-1] if flip else f); G['T'].append(t)
def ribbon(fn, pts, h, t, off, flip=False):
    """thin light ribbon of height h along a polyline of (a, b) points."""
    for (a0, b0), (a1, b1) in zip(pts, pts[1:]): quad_patch(fn, [(a0, b0 + h / 2), (a1, b1 + h / 2), (a1, b1 - h / 2), (a0, b0 - h / 2)], 2, 1, t, off, flip)
def pulse(x0, x1, z, bx, bw=.05, bh=.016):
    """polyline from x0 to x1 at height z with a heartbeat blip (up-down-up) centred at bx (|x| units, signed via x0/x1)."""
    s = 1 if x1 > x0 else -1; pts = [(x0, z)]
    for dx, dz in ((-bw * .5, 0), (-bw * .25, bh), (0, -bh * .6), (bw * .25, bh * .35), (bw * .5, 0)): pts.append((bx + s * dx, z + dz))
    pts.append((x1, z)); return sorted(pts, key=lambda p: s * p[0])
# ---- front: enclosed nose, slim pulse-line DRL above four segmented LED modules, lower cooling slot with active shutters, corner air curtains, aero lip
for sx in (1, -1):
    fl = sx < 0
    quad_patch(fh, [(sx * .56, .655), (sx * .90, .700), (sx * .905, .615), (sx * .58, .585)], 14, 3, 'trim', .002, fl)           # slim headlamp housing (rises outboard)
    ribbon(fh, [(x * sx, z) for x, z in pulse(.58, .89, .650, .66)][:: (1 if sx > 0 else 1)], .009, 'drl', .005, fl)          # pulse-line DRL
    for k in range(4):                                                                                                         # four segmented LED modules
        x0 = .615 + .066 * k; z0 = .603 + .010 * k
        quad_patch(fh, [(sx * x0, z0 + .022), (sx * (x0 + .048), z0 + .025), (sx * (x0 + .048), z0 + .004), (sx * x0, z0 + .001)], 2, 1, 'lens', .006, fl)
    quad_patch(fh, [(sx * .865, .640), (sx * .898, .650), (sx * .900, .632), (sx * .866, .624)], 2, 1, 'ind', .006, fl)        # amber indicator (outer tip)
    quad_patch(fh, [(sx * .56, .657), (sx * .90, .702), (sx * .906, .613), (sx * .58, .583)], 14, 3, 'lens', .009, fl)
    quad_patch(fh, [(sx * .785, .47), (sx * .815, .475), (sx * .825, .30), (sx * .795, .295)], 1, 5, 'mesh', .002, fl)         # vertical corner air curtain
quad_patch(fh, [(-.48, .315), (.48, .315), (.44, .245), (-.44, .245)], 16, 2, 'mesh', .002, True)                              # slim lower cooling slot
for k in range(3): quad_patch(fh, [(-.46, .300 - .022 * k), (.46, .300 - .022 * k), (.46, .292 - .022 * k), (-.46, .292 - .022 * k)], 16, 1, 'aero', .006, True)   # active shutter slats
quad_patch(fh, [(-.80, .215), (.80, .215), (.78, .195), (-.78, .195)], 24, 1, 'aero', .006, True)                              # aero lip
# ---- hood: a single sensor strip at the hood leading edge (subtle tech detail)
quad_patch(th, [(-.22, -2.205), (.22, -2.205), (.22, -2.19), (-.22, -2.19)], 8, 1, 'black', .002)
# ---- side: four-door shut lines, flush handles, B-pillar applique, aero side-sill blade, front-fender air outlet
for sx in (1, -1):
    s_ = lambda y, z, o: sh(sx, y, z, o)
    for yb, yt in ((-.66, -.62), (.40, .44), (1.06, 1.22)):                                                                   # front door front, B-line, rear door rear
        quad_patch(s_, [(yb, .29), (yb + .005, .29), (yt + .005, ZBELT(yt) - .015), (yt, ZBELT(yt) - .015)], 1, 8, 'black', .001, sx > 0)
    for y0 in (.04, .92):                                                                                                      # flush door handles
        quad_patch(s_, [(y0, .832), (y0 + .17, .842), (y0 + .17, .826), (y0, .816)], 3, 1, 'black', .002, sx > 0)
    rows = []
    for z in np.linspace(0, 1, 6):
        row = []
        for y in (.38, .46):
            zz = lerp(ZBELT(y) + .035, lerp(ZBELT(y) + .03, ZC(y) - .06, .90) - .01, z); p = sh(sx, y, zz, .004); row.append(p)
        rows.append(row)
    if all(p is not None for r in rows for p in r):
        n0 = len(G['V']); [G['V'].extend([tuple(p) for p in r]) for r in rows]
        for j in range(len(rows) - 1): f = (n0 + 2 * j, n0 + 2 * j + 1, n0 + 2 * j + 3, n0 + 2 * j + 2); G['F'].append(f[::-1] if sx > 0 else f); G['T'].append('black')
    quad_patch(s_, [(-1.04, .225), (1.04, .235), (1.04, .27), (-1.04, .26)], 30, 1, 'aero', .010, sx > 0)                    # aero side-sill blade
    quad_patch(s_, [(-1.00, .66), (-.90, .67), (-.90, .62), (-1.00, .61)], 2, 2, 'mesh', .002, sx > 0)                        # front-fender air outlet (air-curtain exit)
# ---- rear: full-width pulse-line tail bar, segmented vertical end blocks under a red lens, brake / reverse / indicator, aero diffuser, active lip spoiler
ribbon(rh, pulse(-.86, .86, .885, 0.0, bw=.12, bh=.022), .011, 'tail', .005)                                                    # full-width pulse line
quad_patch(rh, [(-.88, .905), (.88, .905), (.88, .866), (-.88, .866)], 30, 2, 'lensred', .009)
for sx in (1, -1):
    fl = sx > 0
    for k in range(3):                                                                                                         # segmented end blocks
        x0 = .74 + .045 * k
        quad_patch(rh, [(sx * x0, .860), (sx * (x0 + .032), .860), (sx * (x0 + .032), .790), (sx * x0, .790)], 1, 3, 'tail', .005, not fl)
    quad_patch(rh, [(sx * .70, .785), (sx * .88, .785), (sx * .88, .773), (sx * .70, .773)], 4, 1, 'ind', .005, not fl)          # amber indicator under the blocks
    quad_patch(rh, [(sx * .735, .865), (sx * .885, .865), (sx * .885, .765), (sx * .735, .765)], 4, 3, 'lensred', .010, not fl)
    quad_patch(rh, [(sx * .40, .50), (sx * .52, .50), (sx * .52, .485), (sx * .40, .485)], 3, 1, 'rev', .004, not fl)            # reverse lamps (lower)
quad_patch(rh, [(-.24, .70), (.24, .70), (.24, .58), (-.24, .58)], 6, 2, 'black', .002)                                         # plate recess
quad_patch(rh, [(-.82, .42), (.82, .42), (.76, .28), (-.76, .28)], 24, 3, 'aero', .003)                                         # dark lower valance (no exhaust)
xs = list(np.linspace(-.80, .80, 25)); ys = list(np.linspace(1.86, 2.46, 10)); dz = lambda y: lerp(.135, .28, ss(1.86, 2.46, y) ** 1.3)
rows = [[(x, y, dz(y)) for x in xs] for y in ys]; n0 = len(G['V'])
for r in rows: G['V'] += r
for j in range(len(ys) - 1):
    for i in range(len(xs) - 1): G['F'].append((n0 + j * 25 + i, n0 + (j + 1) * 25 + i, n0 + (j + 1) * 25 + i + 1, n0 + j * 25 + i + 1)); G['T'].append('aero')
for xf in (-.30, 0.0, .30):                                                                                                     # three clean diffuser fins
    for off in (-.004, .004): strip([(xf + off, y, dz(y)) for y in ys], [(xf + off, y, max(.135, min(dz(y) - .006, lerp(.13, .20, ss(2.0, 2.46, y))))) for y in ys], 'aero', flip=off > 0)
quad_patch(th, [(-.70, 2.355), (.70, 2.355), (.70, 2.37), (-.70, 2.37)], 20, 1, 'black', .002)                                  # active lip-spoiler split line (deck edge)
quad_patch(th, [(-.16, 1.70), (.16, 1.70), (.16, 1.72), (-.16, 1.72)], 6, 1, 'tail', .003)                                      # third brake light (top of the rear glass)
det = obj('Details', G['V'], G['F'], G['T'])
bm = bmesh.new(); bm.from_mesh(det.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6); bm.to_mesh(det.data); bm.free(); det.data.shade_smooth(); det.data.set_sharp_from_angle(angle=math.radians(35))
# slim camera-style mirrors: low wide pod on a thin blade
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=20, v_segments=12, radius=1.0)
    for v in bmm.verts:
        x, y, z = v.co; y = y * (1.0 if y < 0 else .40); v.co = Vector((x * .095, y * .07, z * .036)) + Vector((sx * .985, -.48, .985))
    me = bpy.data.meshes.new('M'); bmm.to_mesh(me); bmm.free(); mo = bpy.data.objects.new('Mirror_' + ('L' if sx > 0 else 'R'), me); CAR.objects.link(mo); me.materials.append(MAT['paint']); me.shade_smooth()
    Vs = [(sx * .84, -.54, .92), (sx * .84, -.47, .92), (sx * .93, -.46, .975), (sx * .93, -.50, .975)]
    so = obj('MirrorBlade_' + ('L' if sx > 0 else 'R'), Vs + [(x, y, z + .010) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'black')
    b2 = bmesh.new(); b2.from_mesh(so.data); bmesh.ops.recalc_face_normals(b2, faces=b2.faces); b2.to_mesh(so.data); b2.free()
# ================================================================ wheels: 21" aero wheels (10 broad twisted turbine spokes + flush outer aero ring), cool-blue calipers
def revolve(profile, seg, sxn):
    Vs, Fs = [], []; n = len(profile)
    for k in range(seg):
        a = 2 * math.pi * k / seg
        for dx, r in profile: Vs.append((sxn * dx, r * math.cos(a), r * math.sin(a)))
    for k in range(seg):
        for i in range(n - 1):
            a0, b0 = k * n + i, k * n + i + 1; a1, b1 = ((k + 1) % seg) * n + i, ((k + 1) % seg) * n + i + 1
            Fs.append((a0, a1, b1, b0) if sxn > 0 else (a0, b0, b1, a1))
    return Vs, Fs
def wheel(name, y, R, W, sx, rr):
    o = bpy.data.objects.new(name, None); CAR.objects.link(o); o.location = (sx * (XF if y < 0 else XR), y, R); hw = W / 2
    tire = [(-hw * .80, rr + .006), (-hw * .97, rr + .025), (-hw, R * .82), (-hw * .96, R * .95), (-hw * .80, R * .997), (0, R), (hw * .80, R * .997), (hw * .96, R * .95), (hw, R * .82), (hw * .97, rr + .025), (hw * .80, rr + .006)]
    Vt, Ft = revolve(tire, 64, sx); obj(name.replace('Wheel', 'Tire'), Vt, Ft, 'tire', o)
    Vl, Fl = revolve([(hw * .82, rr - .022), (hw * .88, rr + .004), (hw * .74, rr + .009), (hw * .66, rr - .015), (-hw * .75, rr - .02), (-hw * .82, rr + .004)], 64, sx); obj(name.replace('Wheel', 'RimBarrel'), Vl, Fl, ['rim_lip'] * len(Fl), o)
    Gs = {'V': [], 'F': []}; face = hw * .60
    for s_ in range(10):                                                                                # broad twisted turbine spokes
        a_in = 2 * math.pi * s_ / 10; secs = []
        for t in np.linspace(0, 1, 5):
            rr_ = lerp(.08, rr - .055, t); a = a_in + .32 * t ** 1.3; w = lerp(.022, .040, t); xx = face - .012 * math.sin(math.pi * t)
            Rm = Matrix.Rotation(a, 3, 'X'); secs.append([Rm @ Vector((sx * (xx + .004), -w, rr_)), Rm @ Vector((sx * (xx + .004), w, rr_)), Rm @ Vector((sx * (xx - .016), w, rr_)), Rm @ Vector((sx * (xx - .016), -w, rr_))])
        for A, B in zip(secs, secs[1:]):
            n0 = len(Gs['V']); Gs['V'] += [tuple(p) for p in A + B]
            for i in range(4): f = (n0 + i, n0 + (i + 1) % 4, n0 + 4 + (i + 1) % 4, n0 + 4 + i); Gs['F'].append(f if sx > 0 else f[::-1])
    Va, Fa = revolve([(face + .004, rr - .060), (face + .006, rr - .040), (face, rr - .018)], 64, sx); n0 = len(Gs['V']); Gs['V'] += Va; Gs['F'] += [tuple(n0 + i for i in f) for f in Fa]   # flush outer aero ring
    Vh, Fh = revolve([(face + .010, 0.0), (face + .010, .045), (face + .004, .07), (face - .01, .085)], 24, sx); n0 = len(Gs['V']); Gs['V'] += Vh; Gs['F'] += [tuple(n0 + i for i in f) for f in Fh]  # aero centre cap
    obj(name.replace('Wheel', 'Spokes'), Gs['V'], Gs['F'], 'rim', o)
    Vd, Fd = revolve([(hw * .12, .10), (hw * .12, rr - .05), (-hw * .05, rr - .05), (-hw * .05, .10)], 48, sx); obj(name.replace('Wheel', 'BrakeDisc'), Vd, Fd, 'rotor', o)
    Gc = {'V': [], 'F': []}; front = y < 0
    for k in range(9):
        a = math.radians(32 + 8 * k); a2 = math.radians(32 + 8 * (k + 1)); r0, r1 = rr - .11, rr - .06
        Vs = []
        for xx in (sx * hw * .22, -sx * hw * .20):
            Vs += [(xx, rr_ * math.cos(aa) * (1 if front else -1), rr_ * math.sin(aa)) for rr_, aa in ((r0, a), (r1, a), (r1, a2), (r0, a2))]
        n0 = len(Gc['V']); Gc['V'] += Vs
        for f in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): Gc['F'].append(tuple(n0 + i for i in f))
    cal = obj(name.replace('Wheel', 'Caliper'), Gc['V'], Gc['F'], 'caliper', o)
    for ch in o.children:
        b2 = bmesh.new(); b2.from_mesh(ch.data); bmesh.ops.recalc_face_normals(b2, faces=b2.faces) if ch == cal else None; b2.to_mesh(ch.data); b2.free(); ch.data.shade_smooth(); ch.data.set_sharp_from_angle(angle=math.radians(40))
for c, (y, R, W) in {'FL': (YF, RF, WF), 'FR': (YF, RF, WF), 'RL': (YR, RR, WR), 'RR': (YR, RR, WR)}.items():
    wheel(f'Wheel_{c}', y, R, W, 1 if c[1] == 'L' else -1, .2667)
# ================================================================ interior silhouette: minimal premium EV cabin (LHD, driver on +X), 2 front seats + rear bench, panoramic roof
GI = {'V': [], 'F': [], 'T': []}
def ibox(c, s, t, tilt=0.0, yaw=0.0):
    rot = Matrix.Rotation(yaw, 3, 'Z') @ Matrix.Rotation(tilt, 3, 'X'); hx, hy, hz = s; Vb = [Vector((x, y, z)) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
    n0 = len(GI['V']); GI['V'] += [tuple(rot @ v + Vector(c)) for v in Vb]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): GI['F'].append(tuple(n0 + i for i in f)); GI['T'].append(t)
for sx in (1, -1):
    ibox((sx * .38, -.02, .40), (.23, .25, .06), 'leather'); ibox((sx * .38, .24, .76), (.22, .06, .33), 'leather', -.22); ibox((sx * .38, .26, 1.10), (.12, .05, .07), 'leather', -.22)   # front seats
ibox((0, .98, .40), (.66, .25, .07), 'leather'); ibox((0, 1.20, .72), (.66, .06, .30), 'leather', -.28)                                                                          # rear bench
ibox((0, -.58, .78), (.74, .14, .05), 'int_dark')                                                                             # minimal floating dashboard
ibox((0, -.565, .745), (.70, .004, .006), 'accent')                                                                           # ambient light line
ibox((.38, -.56, .86), (.13, .015, .045), 'screen', .25)                                                                      # digital instrument cluster
ibox((-.02, -.50, .82), (.20, .015, .12), 'screen', .30)                                                                      # large central display
ibox((.06, -.12, .52), (.10, .42, .06), 'int_dark')                                                                           # floating centre console
ibox((.38, -.36, .80), (.16, .02, .13), 'int_dark', .40)                                                                       # steering wheel (driver side +X)
ibox((0, 1.40, .86), (.66, .14, .02), 'int_dark')                                                                             # parcel shelf
interior = obj('Interior_Blockout', GI['V'], GI['F'], GI['T'])
m_ = interior.modifiers.new('b', 'BEVEL'); m_.width = .02; m_.segments = 2
with bpy.context.temp_override(object=interior, active_object=interior): bpy.ops.object.modifier_apply(modifier='b')
interior.data.shade_smooth()
obj('Floor', [(-.82, -1.9, .138), (.82, -1.9, .138), (.82, 1.9, .138), (-.82, 1.9, .138)], [(3, 2, 1, 0)], 'trim')
# ================================================================ surface-quality metric (waviness): longitudinal + lateral sections on the paint (both sides)
dg = bpy.context.evaluated_depsgraph_get(); BV2 = BVHTree.FromObject(body, dg)
def sect(xf, ys_):
    z = []
    for y in ys_:
        loc = BV2.ray_cast(Vector((xf, y, 3)), Vector((0, 0, -1)))[0]; z.append(loc.z if loc else np.nan)
    return np.array(z)
def waviness(zs, h):
    """count curvature sign changes (inflections) with |kappa| above noise, and RMS of the 3rd derivative (fairness)."""
    k = np.diff(zs, 2) / h ** 2; k = k[np.isfinite(k)]; sig = k[np.abs(k) > .05]
    flips = int(np.sum(np.diff(np.sign(sig)) != 0)) if len(sig) > 1 else 0
    j = np.diff(zs, 3) / h ** 3; j = j[np.isfinite(j)]; return flips, float(np.sqrt(np.mean(j ** 2))) if len(j) else 0.0
W_ = {}
for nm, (y0, y1, xs_) in {'hood': (-2.15, -.85, (0, .25, .45, -.45)), 'roof': (-.40, 1.40, (0, .30, .50, -.50)), 'rear_deck': (1.80, 2.32, (0, .3, .55, -.55))}.items():
    ys_ = np.linspace(y0, y1, 60); h = ys_[1] - ys_[0]; W_[nm] = {f'x={x}': dict(zip(('inflections', 'fairness_rms'), waviness(sect(x, ys_), h))) for x in xs_}
for nm, ys_, zz, sx in (('front_door_L', np.linspace(-.60, .38, 40), .62, 1), ('rear_door_L', np.linspace(.46, 1.00, 30), .62, 1), ('front_door_R', np.linspace(-.60, .38, 40), .62, -1),
                        ('quarter_L', np.linspace(1.95, 2.30, 24), .75, 1), ('quarter_R', np.linspace(1.95, 2.30, 24), .75, -1)):
    xs = []
    for y in ys_:
        loc = BV2.ray_cast(Vector((sx * 3, y, zz)), Vector((-sx, 0, 0)))[0]; xs.append(abs(loc.x) if loc else np.nan)
    W_[nm] = dict(zip(('inflections', 'fairness_rms'), waviness(np.array(xs), ys_[1] - ys_[0])))
REPORT['waviness'] = W_
# ================================================================ report + save
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons) if o.type == 'MESH' else 0
allm = [o for o in CAR.objects if o.type == 'MESH']; pts = np.array([(o.matrix_world @ v.co)[:] for o in allm for v in o.data.vertices])
bp = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices])
REPORT.update(stage='01 blockout', design=DIM, measured=dict(length=round(float(np.ptp(pts[:, 1])), 3), width_overall=round(float(np.ptp(pts[:, 0])), 3), width_body=round(float(np.ptp(bp[:, 0])), 3),
              height=round(float(pts[:, 2].max()), 3), height_body=round(float(bp[:, 2].max()), 3), body_min_z=round(float(bp[:, 2].min()), 3)), triangles_total=sum(tris(o) for o in allm), objects={o.name: tris(o) for o in allm})
json.dump(REPORT, open(os.path.join(REPD(), 'PV_blockout_stats.json'), 'w'), indent=1)
print('DIMS', REPORT['measured'], 'TRIS', REPORT['triangles_total']); print('WAVE', json.dumps(W_))
path = CKP('pulseev_01_blockout.blend'); assert SCR or not os.path.exists(path), path
bpy.ops.wm.save_as_mainfile(filepath=path); print('SAVED', path)
