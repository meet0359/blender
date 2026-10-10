# Raven XR (Phase E) — original Japanese-inspired front-engine two-door performance coupe, design blockout. Blender -b --factory-startup --python rv_blockout.py
# Long hood sitting in a valley between raised front-fender crests, cabin set back, compact fastback greenhouse, coke-bottle waist + muscular rear haunches,
# slim angular headlights with an inboard "fang" DRL, wide inverted-trapezoid honeycomb grille, corner air curtains, sculpted lower doors + side-skirt blade,
# short deck with a deck spoiler, chevron tail-light signature, 5-strake diffuser, one oval exhaust per side. Convention: +Z up, nose -Y, vehicle left +X, 1 BU = 1 m.
# Surfacing = the refined Vortex R method: coarse evenly spaced quad cage from smooth pchip design curves, Taubin-faired along Y and around each section,
# Catmull-Clark subdivision, fender-crest crease that fades out at the nose and tail (no tail-corner pinch). Helpers are copied verbatim from vx_blockout.py.
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, math, json
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = lambda *a: os.path.join(ROOT, *a)
SCR = os.environ.get('RV_SCRATCH')
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
DIM = dict(length=4.52, width_body=1.99, height=1.30, wheelbase=2.68, track_f=1.66, track_r=1.67, overhang_f=.96, overhang_r=.88, ground_clearance=.12,
           tire_f='255/35 R19 (R 0.331)', tire_r='285/35 R19 (R 0.341)')
YF, YR = -1.34, 1.34; RF, RR = .331, .341; WF, WR = .255, .285; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.30, 2.22
# centreline top: nose -> long hood (valley between the fender crests) -> cowl -> 32 deg windshield -> roof peak (cab set back) -> fastback -> short deck -> ducktail
ZC = pchip([YN, -2.15, -1.80, -1.34, -.90, -.52, -.20, .15, .40, .65, 1.00, 1.36, 1.64, 1.95, 2.12, YT], [.50, .625, .675, .715, .78, .85, 1.04, 1.255, 1.30, 1.29, 1.20, 1.085, 1.005, .99, 1.0, .965])
ZBELT = pchip([YN, -2.12, -1.75, -1.34, -.95, -.50, .30, .90, 1.34, 1.80, 2.10, YT], [.52, .685, .80, .86, .835, .86, .905, .945, .985, .99, .97, .93])        # fender crest / belt
WBELT = pchip([YN, -2.12, -1.75, -1.34, -.95, -.50, .30, .90, 1.34, 1.80, 2.10, YT], [.62, .76, .82, .845, .815, .805, .815, .855, .885, .865, .825, .77])
WMAX = pchip([YN, -2.12, -1.75, -1.34, -.95, -.40, .30, .90, 1.34, 1.80, 2.10, YT], [.80, .92, .97, .985, .945, .918, .93, .972, .998, .985, .955, .91])      # coke-bottle waist, muscular rear haunches
ZSH = pchip([YN, -1.34, 0, 1.34, YT], [.42, .52, .55, .58, .54])
ZFLOOR = pchip([YN, -2.10, -1.85, 1.80, 2.05, YT], [.26, .17, .12, .12, .19, .27])
WFLOOR = pchip([YN, -2.1, 0, 2.1, YT], [.62, .80, .82, .80, .70])
CAB = lambda y: ss(-.70, -.48, y) * (1 - ss(1.46, 1.70, y))                                         # greenhouse presence (windshield base -> fastback end)
ROOFW = pchip([-.55, -.20, .20, .70, 1.20, 1.66], [.69, .655, .625, .60, .555, .50])                    # roof rail half-width (compact greenhouse, tumblehome)
SK = lambda y: .028 * ss(-.95, -.70, y) * (1 - ss(.72, .98, y))                                      # concave lower-door sculpt (rises into the rear haunch)
def ring_half(y):
    zb, wf, wm, zs, zb_, wb, zc, c = ZFLOOR(y), WFLOOR(y), WMAX(y), ZSH(y), ZBELT(y), WBELT(y), ZC(y), CAB(y); sk = SK(y)
    side = [(0.0, zb), (.5 * wf, zb), (wf, zb + .005), (wm - .045 - sk * .3, zb + .07), (wm - .012 - sk, lerp(zb + .07, zs, .5)), (wm, zs), (lerp(wm, wb, .45), lerp(zs, zb_, .55)), (wb, zb_)]
    crown = lambda t: zb_ + (zc - zb_) * (1 - (1 - t) ** 2.0)
    deck = [(wb * (1 - t), crown(t)) for t in (.08, .26, .50, .74, .90, 1.0)]
    rw = ROOFW(min(max(y, -.55), 1.66)); sw = wb - .055
    gh = [(wb - .04, zb_ + .008), (sw, zb_ + .03), (lerp(sw, rw, .80) + .01, lerp(zb_ + .03, zc - .06, .90)), (rw, zc - .035), (.50 * rw, zc - .008), (0.0, zc)]   # DLO top (10) below a painted roof rail (11)
    top = [(lerp(d[0], g[0], c), lerp(d[1], g[1], c)) for d, g in zip(deck, gh)]
    return side + top
NS = len(ring_half(0.0))                                                                              # 14 points per half
I_GH = 9; I_ROOF = 11
STAT = [-2.18, -2.02, -1.84, -1.64, -1.44, -1.24, -1.04, -.84, -.64, -.44, -.24, -.04, .16, .36, .56, .76, .96, 1.16, 1.36, 1.56, 1.76, 1.94, 2.08]   # coarse, ~0.2 m
NOSE = [(YN + .04, 1.0), (YN + .012, .84), (YN, .50)]
TAIL = [(YT - .02, 1.0), (YT - .005, .93), (YT, .62)]                                                 # Kamm tail (flat rear face, crisp edge)
def full_ring(y, scale=1.0, centre=None):
    h = ring_half(y); cz = centre if centre is not None else (h[0][1] + h[-1][1]) * .5
    pts = [(x * scale, y, cz + (z - cz) * scale) for x, z in h]
    return pts + [(-x, yy, z) for x, yy, z in pts[1:-1]][::-1]
rings = []
for y, s in NOSE[::-1]: rings.append(full_ring(y, s, .40))
for y in STAT: rings.append(full_ring(y))
for y, s in TAIL: rings.append(full_ring(y, s, .62))
NR = len(rings[0])
def fair_cage(rings, iters=30, lam=.5, mu=-.53, fixed=4):
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
    if a >= I_ROOF and -.46 < y < .10: return 'glass'                                                   # windshield (between the A-pillars = faces (10, 11))
    if a >= I_ROOF and .76 < y < 1.48: return 'glass'                                                   # fastback rear glass (body-colour roof between)
    if (a, b) == (9, 10) and -.40 < y < 1.08: return 'glass'                                            # side glass (DLO; sail panel / C-pillar behind)
    if (a, b) == (8, 9) and -.44 < y < 1.12: return 'black'                                             # DLO surround
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
MAT = dict(paint=pbr('RV_Paint', (.008, .062, .040), .78, .30, .6), glass=pbr('RV_Glass', (.005, .006, .008), 0, .03, .3, alpha=.7), black=pbr('RV_GlossBlack', (.008, .008, .009), 0, .1, .6),
           trim=pbr('RV_SatinBlack', (.016, .016, .018), .2, .5), carbon=pbr('RV_AeroBlack', (.012, .012, .013), .2, .35, .5), mesh=pbr('RV_Honeycomb', (.01, .01, .011), .4, .5),
           rim=pbr('RV_WheelForged', (.028, .03, .032), 1, .30), rim_lip=pbr('RV_WheelLip', (.05, .05, .055), 1, .25), tire=pbr('RV_Tire', (.022, .022, .024), 0, .85),
           rotor=pbr('RV_Rotor', (.32, .32, .33), 1, .35), caliper=pbr('RV_Caliper', (.60, .02, .02), .1, .3, .6), exhaust=pbr('RV_Exhaust', (.18, .17, .16), 1, .25),
           leather=pbr('RV_Leather', (.02, .02, .022), 0, .7), accent=pbr('RV_Accent', (.45, .015, .015), 0, .45),
           lens=pbr('RV_LensClear', (.8, .85, .9), 0, .02, .3, alpha=.12), drl=pbr('RV_LED_DRL', (.85, .92, 1), 0, .3, emit=(.85, .93, 1.0), es=12),
           tail=pbr('RV_LED_Tail', (.6, 0, .01), 0, .3, emit=(1, .01, .015), es=9), lensred=pbr('RV_LensRed', (.30, 0, .004), 0, .03, .3, alpha=.8),
           ind=pbr('RV_LED_Indicator', (.8, .3, 0), 0, .3, emit=(1, .35, 0), es=.7))
CAR = bpy.data.collections.new('RAVEN_XR'); sc.collection.children.link(CAR)
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
cr = body.data.attributes.new('crease_edge', 'FLOAT', 'EDGE'); nrings = len(rings); crest = set(); VB = body.data.vertices
rail = {i * NR + j for i in range(nrings) if -.42 < rings[i][0][1] < 1.42 for j in (I_ROOF, NR - I_ROOF)}
for i in range(nrings):
    for j in (7, NR - 7): crest.add(i * NR + j)
for e in body.data.edges:
    a_, b_ = e.vertices
    if a_ in rail and b_ in rail and abs(a_ - b_) == NR: cr.data[e.index].value = .45                   # roof rail: crisp coupe roof edge
    if a_ in crest and b_ in crest and abs(a_ - b_) == NR:                                             # fender-crest character line: crisp, fades out at nose + tail (no corner pinch)
        ym_ = (VB[a_].co.y + VB[b_].co.y) / 2; cr.data[e.index].value = .66 * ss(-2.14, -1.84, ym_) * (1 - ss(1.62, 2.02, ym_))
REPORT = dict(cage=dict(stations=len(rings), points_per_ring=NR, cage_faces=len(F), fairing='Taubin 30 x (0.5, -0.53) along Y + 12 x (0.45, -0.48) around each section', max_control_point_shift_mm=round(CAGE_SHIFT_MM, 1)))
sub = body.modifiers.new('sub', 'SUBSURF'); sub.levels = sub.render_levels = 3
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='sub')
# wheel arches (exact boolean) + liners
def cyl(r, x0, x1, y, z, seg=64):
    bm = bmesh.new(); r0 = [bm.verts.new((x0, y + r * math.cos(2 * math.pi * k / seg), z + r * math.sin(2 * math.pi * k / seg))) for k in range(seg)]; r1 = [bm.verts.new((x1, v.co.y, v.co.z)) for v in r0]
    for k in range(seg): bm.faces.new((r0[k], r0[(k + 1) % seg], r1[(k + 1) % seg], r1[k]))
    bm.faces.new(r0[::-1]); bm.faces.new(r1); bm.normal_update(); me = bpy.data.meshes.new('cut'); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('cut', me); sc.collection.objects.link(o); return o
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    c = cyl(r + .048, sx * .55, sx * 1.4, y, r + .012)
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
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):                          # wheel-well liners (inside the body side)
    R_ = r + .046; zc = r + .012; seg = 28; a0, a1 = math.radians(-25), math.radians(205)
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
# ---- front: wide inverted-trapezoid honeycomb grille, thin upper slot, vertical corner air curtains, slim angular headlights with an inboard fang DRL
quad_patch(fh, [(-.54, .42), (.54, .42), (.40, .20), (-.40, .20)], 18, 6, 'mesh', .002, True)
quad_patch(fh, [(-.56, .435), (.56, .435), (.555, .42), (-.555, .42)], 18, 1, 'black', .004, True)                      # gloss-black grille brow
quad_patch(fh, [(-.34, .535), (.34, .535), (.33, .515), (-.33, .515)], 12, 1, 'black', .003, True)                     # upper slot under the hood leading edge
for sx in (1, -1):
    fl = sx < 0
    quad_patch(fh, [(sx * .70, .45), (sx * .755, .47), (sx * .76, .24), (sx * .705, .22)], 2, 6, 'mesh', .002, fl)            # corner air curtain
    quad_patch(fh, [(sx * .46, .585), (sx * .86, .655), (sx * .875, .600), (sx * .50, .540)], 14, 2, 'trim', .002, fl)         # headlamp housing (slim, rising outboard)
    quad_patch(fh, [(sx * .48, .582), (sx * .85, .648), (sx * .852, .637), (sx * .48, .571)], 14, 1, 'drl', .004, fl)          # upper DRL blade
    quad_patch(fh, [(sx * .462, .586), (sx * .484, .584), (sx * .512, .47), (sx * .497, .47)], 1, 5, 'drl', .004, fl)          # inboard fang (drops beside the grille)
    for k in range(2):                                                                                                       # two projector modules
        x0 = .60 + .11 * k; z0 = .582 + .02 * k
        quad_patch(fh, [(sx * x0, z0 + .028), (sx * (x0 + .07), z0 + .040), (sx * (x0 + .07), z0 + .012), (sx * x0, z0)], 2, 1, 'lens', .006, fl)
    quad_patch(fh, [(sx * .78, .606), (sx * .862, .622), (sx * .866, .611), (sx * .78, .596)], 3, 1, 'ind', .004, fl)
    quad_patch(fh, [(sx * .46, .588), (sx * .86, .658), (sx * .877, .598), (sx * .50, .537)], 14, 2, 'lens', .008, fl)
    # hood: twin long heat-extractor vents beside the power-dome, near the cowl
    quad_patch(th, [(sx * .18, -1.18), (sx * .36, -1.14), (sx * .36, -.92), (sx * .20, -.96)], 4, 6, 'mesh', .002, sx > 0)
    # side: front-fender gill, door shut lines, flush handle, black side-skirt blade (rises toward the rear)
    ss_ = lambda y, z, o: sh(sx, y, z, o)
    quad_patch(ss_, [(-.93, .66), (-.80, .67), (-.82, .50), (-.93, .55)], 3, 4, 'mesh', .002, sx > 0)
    quad_patch(ss_, [(-.42, .30), (-.415, .30), (-.40, .86), (-.405, .86)], 1, 8, 'black', .001, sx > 0)
    quad_patch(ss_, [(.74, .30), (.745, .30), (.725, .90), (.72, .90)], 1, 8, 'black', .001, sx > 0)
    quad_patch(ss_, [(.40, .815), (.56, .815), (.56, .795), (.40, .795)], 3, 1, 'black', .002, sx > 0)
    quad_patch(ss_, [(-.98, .205), (.98, .215), (.98, .275), (-.98, .245)], 30, 1, 'carbon', .010, sx > 0)
# ---- rear: chevron tail lamps (">" pointing outboard) under a red lens, plate recess, lower reflectors / reverse, 5-strake diffuser, one oval exhaust per side
for sx in (1, -1):
    fl = sx > 0
    quad_patch(rh, [(sx * .50, .878), (sx * .89, .812), (sx * .89, .758), (sx * .54, .700)], 10, 4, 'trim', .002, not fl)      # dark lamp housing
    quad_patch(rh, [(sx * .52, .866), (sx * .87, .806), (sx * .87, .790), (sx * .52, .848)], 10, 1, 'tail', .005, not fl)      # upper chevron blade
    quad_patch(rh, [(sx * .555, .712), (sx * .87, .772), (sx * .87, .787), (sx * .555, .728)], 10, 1, 'tail', .005, fl)        # lower chevron blade
    quad_patch(rh, [(sx * .835, .80), (sx * .87, .806), (sx * .87, .772), (sx * .835, .768)], 1, 2, 'tail', .005, not fl)       # chevron tip
    quad_patch(rh, [(sx * .64, .797), (sx * .72, .785), (sx * .72, .774), (sx * .65, .763)], 2, 1, 'ind', .004, not fl)       # small indicator inside the chevron
    quad_patch(rh, [(sx * .50, .880), (sx * .89, .814), (sx * .89, .756), (sx * .54, .698)], 10, 4, 'lensred', .009, not fl)
    quad_patch(rh, [(sx * .66, .48), (sx * .80, .48), (sx * .80, .465), (sx * .66, .465)], 3, 1, 'tail', .004, not fl)       # lower reflector / rear fog
quad_patch(rh, [(-.25, .66), (.25, .66), (.25, .54), (-.25, .54)], 6, 2, 'black', .002)                                     # plate recess
quad_patch(rh, [(-.80, .425), (.80, .425), (.74, .27), (-.74, .27)], 24, 3, 'carbon', .003)                                 # black rear valance (frames the exhausts + diffuser)
xs = list(np.linspace(-.78, .78, 25)); ys = list(np.linspace(1.70, 2.22, 10)); dz = lambda y: lerp(.125, .30, ss(1.70, 2.22, y) ** 1.3)
rows = [[(x, y, dz(y)) for x in xs] for y in ys]; n0 = len(G['V'])
for r in rows: G['V'] += r
for j in range(len(ys) - 1):
    for i in range(len(xs) - 1): G['F'].append((n0 + j * 25 + i, n0 + (j + 1) * 25 + i, n0 + (j + 1) * 25 + i + 1, n0 + j * 25 + i + 1)); G['T'].append('carbon')
for xf in (-.40, -.20, 0.0, .20, .40):
    for off in (-.004, .004): strip([(xf + off, y, dz(y)) for y in ys], [(xf + off, y, max(.125, dz(y) - .14)) for y in ys], 'carbon', flip=off > 0)
for cx in (-.62, .62):                                                                                       # one large oval tip each outboard corner
    p = rh(cx, .34, 0); seg = 24; ax, az = .07, .04
    A = [(cx + ax * math.cos(2 * math.pi * k / seg), p.y - .10, .34 + az * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    B = [(x, p.y + .03, z) for x, y, z in A]; Ci = [(cx + (ax - .009) * math.cos(2 * math.pi * k / seg), p.y + .03, .34 + (az - .009) * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    strip(A, B, 'exhaust', closed=True); strip(B, Ci, 'exhaust', closed=True); strip(Ci, [(x, y - .08, z) for x, y, z in Ci], 'trim', closed=True)
# ---- deck spoiler: a flat cambered blade at the deck trailing edge on two short pylons (not a wing)
sp_y = 2.04; base_ = th(0, sp_y, 0); sp_z = base_.z + .075
af = [(0.0, 0.0), (.04, .012), (.10, .016), (.16, .010), (.20, .002), (.16, .0), (.10, -.004), (.04, -.003)]
xsw = list(np.linspace(-.76, .76, 21)); ring_w = []
for x in xsw:
    zb0 = th(x, sp_y, 0); ring_w.append([(x, sp_y - .10 + c, max(sp_z, zb0.z + .055) + z) for c, z in af])
for A, B in zip(ring_w, ring_w[1:]):
    n0 = len(G['V']); G['V'] += A + B; k = len(A)
    for i in range(k): G['F'].append((n0 + i, n0 + (i + 1) % k, n0 + k + (i + 1) % k, n0 + k + i)); G['T'].append('carbon')
for sx in (1, -1):
    b0 = th(sx * .46, sp_y - .02, 0); Vb = []
    for z in (b0.z - .01, sp_z + .004): Vb += [(sx * .46 - .008, sp_y - .07, z), (sx * .46 + .008, sp_y - .07, z), (sx * .46 + .008, sp_y + .02, z), (sx * .46 - .008, sp_y + .02, z)]
    add(Vb, [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], 'carbon')
# ---- front splitter blade (black aero)
xs = list(np.linspace(-.84, .84, 37)); fr = [fh(x, .19, 0) for x in xs]
A = [(x, (p.y if p else -2.2) - .035, .165) for x, p in zip(xs, fr)]; B = [(x, -1.92, .165) for x in xs]
strip(B, A, 'carbon'); strip([(x, y, z - .012) for x, y, z in A], [(x, y, z - .012) for x, y, z in B], 'carbon'); strip(A, [(x, y, z - .012) for x, y, z in A], 'carbon', flip=True)
det = obj('Details', G['V'], G['F'], G['T'])
bm = bmesh.new(); bm.from_mesh(det.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6); bm.to_mesh(det.data); bm.free(); det.data.shade_smooth(); det.data.set_sharp_from_angle(angle=math.radians(35))
# mirrors (body-colour pod on a black arm from the door)
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=20, v_segments=12, radius=1.0)
    for v in bmm.verts:
        x, y, z = v.co; y = y * (1.0 if y < 0 else .45); v.co = Vector((x * .085, y * .08, z * .048)) + Vector((sx * .935, -.32, .975))
    me = bpy.data.meshes.new('M'); bmm.to_mesh(me); bmm.free(); mo = bpy.data.objects.new('Mirror_' + ('L' if sx > 0 else 'R'), me); CAR.objects.link(mo); me.materials.append(MAT['paint']); me.shade_smooth()
    Vs = [(sx * .80, -.38, .905), (sx * .80, -.31, .905), (sx * .88, -.30, .95), (sx * .88, -.35, .95)]
    so = obj('MirrorArm_' + ('L' if sx > 0 else 'R'), Vs + [(x, y, z + .014) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'carbon')
    b2 = bmesh.new(); b2.from_mesh(so.data); bmesh.ops.recalc_face_normals(b2, faces=b2.faces); b2.to_mesh(so.data); b2.free()
# ================================================================ wheels: dark forged 14-spoke (7 pairs) + big rotors + red calipers
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
    tire = [(-hw * .80, rr + .006), (-hw * .97, rr + .025), (-hw, R * .80), (-hw * .96, R * .94), (-hw * .80, R * .997), (0, R), (hw * .80, R * .997), (hw * .96, R * .94), (hw, R * .80), (hw * .97, rr + .025), (hw * .80, rr + .006)]
    Vt, Ft = revolve(tire, 64, sx); obj(name.replace('Wheel', 'Tire'), Vt, Ft, 'tire', o)
    Vl, Fl = revolve([(hw * .82, rr - .022), (hw * .88, rr + .004), (hw * .74, rr + .009), (hw * .66, rr - .015), (-hw * .75, rr - .02), (-hw * .82, rr + .004)], 64, sx); obj(name.replace('Wheel', 'RimBarrel'), Vl, Fl, ['rim_lip'] * len(Fl), o)
    Gs = {'V': [], 'F': []}
    face = hw * .58
    for s_ in range(7):
        for side_ in (-1, 1):
            a_in = 2 * math.pi * s_ / 7; a_out = a_in + side_ * .17; secs = []
            for t in np.linspace(0, 1, 5):
                rr_ = lerp(.07, rr - .02, t); a = lerp(a_in + side_ * .025, a_out, t ** 1.2); w = lerp(.018, .011, t); xx = face - .025 * math.sin(math.pi * t)
                Rm = Matrix.Rotation(a, 3, 'X'); secs.append([Rm @ Vector((sx * (xx + .004), -w, rr_)), Rm @ Vector((sx * (xx + .004), w, rr_)), Rm @ Vector((sx * (xx - .018), w, rr_)), Rm @ Vector((sx * (xx - .018), -w, rr_))])
            for A, B in zip(secs, secs[1:]):
                n0 = len(Gs['V']); Gs['V'] += [tuple(p) for p in A + B]
                for i in range(4): f = (n0 + i, n0 + (i + 1) % 4, n0 + 4 + (i + 1) % 4, n0 + 4 + i); Gs['F'].append(f if sx > 0 else f[::-1])
    Vh, Fh = revolve([(face + .008, 0.0), (face + .008, .03), (face, .05), (face - .01, .075)], 24, sx); n0 = len(Gs['V']); Gs['V'] += Vh; Gs['F'] += [tuple(n0 + i for i in f) for f in Fh]
    obj(name.replace('Wheel', 'Spokes'), Gs['V'], Gs['F'], 'rim', o)
    Vd, Fd = revolve([(hw * .12, .10), (hw * .12, rr - .03), (-hw * .05, rr - .03), (-hw * .05, .10)], 48, sx); obj(name.replace('Wheel', 'BrakeDisc'), Vd, Fd, 'rotor', o)
    Gc = {'V': [], 'F': []}; front = y < 0
    for k in range(10):
        a = math.radians(30 + 8 * k); a2 = math.radians(30 + 8 * (k + 1)); r0, r1 = rr - .085, rr - .015
        Vs = []
        for xx in (sx * hw * .30, -sx * hw * .14):
            Vs += [(xx, rr_ * math.cos(aa) * (1 if front else -1), rr_ * math.sin(aa)) for rr_, aa in ((r0, a), (r1, a), (r1, a2), (r0, a2))]
        n0 = len(Gc['V']); Gc['V'] += Vs
        for f in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): Gc['F'].append(tuple(n0 + i for i in f))
    cal = obj(name.replace('Wheel', 'Caliper'), Gc['V'], Gc['F'], 'caliper', o)
    for ch in o.children:
        b2 = bmesh.new(); b2.from_mesh(ch.data); bmesh.ops.recalc_face_normals(b2, faces=b2.faces) if ch == cal else None; b2.to_mesh(ch.data); b2.free(); ch.data.shade_smooth(); ch.data.set_sharp_from_angle(angle=math.radians(40))
for c, (y, R, W) in {'FL': (YF, RF, WF), 'FR': (YF, RF, WF), 'RL': (YR, RR, WR), 'RR': (YR, RR, WR)}.items():
    wheel(f'Wheel_{c}', y, R, W, 1 if c[1] == 'L' else -1, .2413)
# ================================================================ interior silhouette: driver-focused (LHD, driver on +X) — sport seats, cluster hood, console angled to the driver
GI = {'V': [], 'F': [], 'T': []}
def ibox(c, s, t, tilt=0.0, yaw=0.0):
    rot = Matrix.Rotation(yaw, 3, 'Z') @ Matrix.Rotation(tilt, 3, 'X'); hx, hy, hz = s; Vb = [Vector((x, y, z)) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
    n0 = len(GI['V']); GI['V'] += [tuple(rot @ v + Vector(c)) for v in Vb]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): GI['F'].append(tuple(n0 + i for i in f)); GI['T'].append(t)
for sx in (1, -1):
    ibox((sx * .37, .32, .32), (.22, .25, .06), 'leather'); ibox((sx * .37, .60, .68), (.21, .06, .32), 'leather', -.30); ibox((sx * .37, .55, .68), (.05, .065, .28), 'accent', -.30)
ibox((0, -.32, .74), (.74, .16, .07), 'leather'); ibox((.37, -.23, .83), (.17, .07, .035), 'trim', .25)                  # dash + cluster hood over the driver
ibox((.08, .0, .46), (.11, .45, .13), 'trim', 0.0, -.08)                                                                   # centre console angled toward the driver
ibox((.37, -.10, .78), (.15, .02, .15), 'trim', .45)                                                                         # steering wheel (driver side +X)
ibox((0, .92, .80), (.70, .30, .03), 'trim')                                                                                 # parcel shelf under the fastback glass
interior = obj('Interior_Blockout', GI['V'], GI['F'], GI['T'])
m_ = interior.modifiers.new('b', 'BEVEL'); m_.width = .02; m_.segments = 2
with bpy.context.temp_override(object=interior, active_object=interior): bpy.ops.object.modifier_apply(modifier='b')
interior.data.shade_smooth()
obj('Floor', [(-.82, -1.9, .123), (.82, -1.9, .123), (.82, 1.70, .123), (-.82, 1.70, .123)], [(3, 2, 1, 0)], 'trim')
# ================================================================ surface-quality metric (waviness): longitudinal and lateral section curvature on the paint
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
for nm, (y0, y1, xs_) in {'hood': (-2.0, -.75, (0, .25, .45)), 'roof': (.0, .90, (0, .2, .35)), 'rear_deck': (1.62, 2.10, (0, .3, .55))}.items():
    ys_ = np.linspace(y0, y1, 60); h = ys_[1] - ys_[0]; W_[nm] = {f'x={x}': dict(zip(('inflections', 'fairness_rms'), waviness(sect(x, ys_), h))) for x in xs_}
for sx_name, ys_, zz in (('door_lateral', np.linspace(-.85, .55, 50), .62), ('quarter_lateral', np.linspace(.75, 2.0, 50), .70)):
    xs = []
    for y in ys_:
        loc = BV2.ray_cast(Vector((3, y, zz)), Vector((-1, 0, 0)))[0]; xs.append(loc.x if loc else np.nan)
    W_[sx_name] = dict(zip(('inflections', 'fairness_rms'), waviness(np.array(xs), ys_[1] - ys_[0])))
REPORT['waviness'] = W_
# ================================================================ report + save
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons) if o.type == 'MESH' else 0
allm = [o for o in CAR.objects if o.type == 'MESH']; pts = np.array([(o.matrix_world @ v.co)[:] for o in allm for v in o.data.vertices])
bp = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices])
REPORT.update(stage='01 blockout', design=DIM, measured=dict(length=round(float(np.ptp(pts[:, 1])), 3), width_overall=round(float(np.ptp(pts[:, 0])), 3), width_body=round(float(np.ptp(bp[:, 0])), 3),
              height=round(float(pts[:, 2].max()), 3), height_body=round(float(bp[:, 2].max()), 3), body_min_z=round(float(bp[:, 2].min()), 3)), triangles_total=sum(tris(o) for o in allm), objects={o.name: tris(o) for o in allm})
json.dump(REPORT, open(os.path.join(REPD(), 'RV_blockout_stats.json'), 'w'), indent=1)
print('DIMS', REPORT['measured'], 'TRIS', REPORT['triangles_total']); print('WAVE', json.dumps(W_))
path = CKP('ravenxr_01_blockout.blend'); assert SCR or not os.path.exists(path), path
bpy.ops.wm.save_as_mainfile(filepath=path); print('SAVED', path)
