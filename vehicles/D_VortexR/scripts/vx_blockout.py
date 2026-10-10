# Vortex R (Phase D) — original mid-engine supercar design blockout. Blender -b --factory-startup --python vx_blockout.py
# Wedge nose, short front overhang, cab-forward teardrop canopy, deep side intakes, big rear haunches, engine cover with louvres, swan-neck wing,
# segmented slash tail lights, large diffuser, centre twin exhaust. Convention: +Z up, nose -Y, vehicle left +X, 1 BU = 1 m.
# Surface-quality rule (lesson from Titan GT TG-PB-1/2): the body is a COARSE, evenly spaced quad cage (few stations, few points per section)
# subdivided Catmull-Clark style; design curves are smooth monotone splines with few knots. No dense stations, no smoothing hacks.
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, math, json
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = lambda *a: os.path.join(ROOT, *a)
SCR = os.environ.get('VX_SCRATCH')
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
DIM = dict(length=4.56, width_body=2.07, height=1.13, wheelbase=2.72, track_f=1.72, track_r=1.70, overhang_f=.94, overhang_r=.90, ground_clearance=.105,
           tire_f='255/30 R20 (R 0.339)', tire_r='325/25 R21 (R 0.348)')
YF, YR = -1.36, 1.36; RF, RR = .339, .348; WF, WR = .255, .325; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.30, 2.26
# centreline top: low wedge nose -> hood valley -> fast windshield -> canopy peak (cab-forward) -> engine cover -> wing deck / kick
ZC = pchip([YN, -2.12, -1.70, -1.20, -.92, -.55, -.10, .25, .62, 1.10, 1.70, 2.12, YT], [.40, .565, .655, .725, .79, .99, 1.13, 1.10, 1.00, .955, .945, .962, .935])
ZBELT = pchip([YN, -2.12, -1.70, -1.36, -1.00, -.40, .30, .90, 1.36, 1.85, 2.15, YT], [.43, .60, .735, .81, .78, .785, .84, .925, .975, .965, .935, .895])   # fender crest
WBELT = pchip([YN, -2.12, -1.75, -1.36, -.95, -.35, .30, .85, 1.36, 1.85, 2.15, YT], [.66, .84, .93, .965, .905, .845, .86, .955, 1.005, .985, .935, .885])
WMAX = pchip([YN, -2.12, -1.75, -1.36, -.90, -.25, .35, .90, 1.36, 1.85, 2.15, YT], [.78, .93, .995, 1.025, .975, .945, .955, 1.005, 1.035, 1.015, .975, .945])   # square, wide rump
ZSH = pchip([YN, -1.36, 0, 1.36, YT], [.38, .47, .50, .56, .50])
ZFLOOR = pchip([YN, -2.10, -1.85, 1.85, 2.10, YT], [.22, .14, .105, .105, .17, .30])
WFLOOR = pchip([YN, -2.1, 0, 2.1, YT], [.60, .80, .82, .80, .70])
CAB = lambda y: ss(-1.02, -.86, y) * (1 - ss(.55, .78, y))                                          # canopy presence
ROOFW = pchip([-.95, -.55, -.10, .30, .70], [.66, .58, .52, .50, .44])                               # teardrop canopy (narrow, strong tumblehome)
SCOOP = lambda y: .115 * ss(.18, .42, y) * (1 - ss(.86, 1.02, y))                                     # deep side intake behind the doors
SCOOP_F = lambda y: .02 * ss(-.95, -.70, y) * (1 - ss(.10, .35, y))                                   # subtle door blade sculpt leading into the intake
def ring_half(y):
    zb, wf, wm, zs, zb_, wb, zc, c = ZFLOOR(y), WFLOOR(y), WMAX(y), ZSH(y), ZBELT(y), WBELT(y), ZC(y), CAB(y)
    sc_ = SCOOP(y) + SCOOP_F(y)
    side = [(0.0, zb), (.5 * wf, zb), (wf, zb + .005), (wm - .035, zb + .07), (wm - sc_ * .8, zs - .11), (wm - sc_, zs + .03), (wm - sc_ * .55 - .01, zs + .17), (wb, zb_)]
    crown = lambda t: zb_ + (zc - zb_) * (1 - (1 - t) ** 2.0)
    deck = [(wb * (1 - t), crown(t)) for t in (.08, .26, .50, .74, .90, 1.0)]
    rw = ROOFW(min(max(y, -.95), .70)); sw = wb - .10
    gh = [(wb - .04, zb_ + .008), (sw, zb_ + .03), (lerp(sw, rw, .62) + .02, lerp(zb_ + .03, zc - .035, .66)), (rw, zc - .035), (.48 * rw, zc - .006), (0.0, zc)]
    top = [(lerp(d[0], g[0], c), lerp(d[1], g[1], c)) for d, g in zip(deck, gh)]
    return side + top
NS = len(ring_half(0.0))                                                                              # 14 points per half
I_GH = 9; I_ROOF = 11
STAT = [-2.18, -2.02, -1.84, -1.64, -1.44, -1.24, -1.04, -.92, -.72, -.50, -.28, -.06, .16, .38, .58, .74, .92, 1.12, 1.34, 1.56, 1.78, 1.98, 2.14]   # coarse, ~0.2 m
NOSE = [(YN + .04, 1.0), (YN + .012, .84), (YN, .50)]
TAIL = [(YT - .02, 1.0), (YT - .005, .93), (YT, .62)]                                                 # chopped Kamm tail (flat rear face, crisp edge)
def full_ring(y, scale=1.0, centre=None):
    h = ring_half(y); cz = centre if centre is not None else (h[0][1] + h[-1][1]) * .5
    pts = [(x * scale, y, cz + (z - cz) * scale) for x, z in h]
    return pts + [(-x, yy, z) for x, yy, z in pts[1:-1]][::-1]
rings = []
for y, s in NOSE[::-1]: rings.append(full_ring(y, s, .36))
for y in STAT: rings.append(full_ring(y))
for y, s in TAIL: rings.append(full_ring(y, s, .58))
NR = len(rings[0])
# cage fairing: Taubin (lambda / mu) smoothing of every longitudinal control line (x and z only; y stations fixed; nose / tail rings fixed).
# Removes control-polygon irregularities between stations (the cause of reflection wobble) without shrinking the design volume.
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
    if a >= I_ROOF and -.88 < y < -.20: return 'glass'                                                  # windshield
    if a >= I_ROOF and .30 < y < .62: return 'glass'                                                    # small rear screen (engine bay behind)
    if (a, b) in ((9, 10), (10, 11)) and -.82 < y < .56: return 'glass'                                 # side glass
    if (a, b) == (8, 9) and -.86 < y < .60: return 'black'                                              # glass surround
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
MAT = dict(paint=pbr('VX_Paint', (.075, .028, .155), .8, .36, .35), glass=pbr('VX_Glass', (.005, .006, .008), 0, .03, .3, alpha=.7), black=pbr('VX_GlossBlack', (.008, .008, .009), 0, .1, .6),
           trim=pbr('VX_SatinBlack', (.016, .016, .018), .2, .5), carbon=pbr('VX_Carbon', (.02, .02, .022), .3, .3, .8), mesh=pbr('VX_Mesh', (.01, .01, .011), .4, .5),
           rim=pbr('VX_WheelForged', (.035, .036, .04), 1, .32), rim_lip=pbr('VX_WheelLip', (.22, .22, .23), 1, .25), tire=pbr('VX_Tire', (.022, .022, .024), 0, .85),
           rotor=pbr('VX_Rotor', (.32, .32, .33), 1, .35), caliper=pbr('VX_Caliper', (.55, .75, .02), .1, .3, .6), exhaust=pbr('VX_Exhaust', (.30, .28, .26), 1, .2),
           leather=pbr('VX_Alcantara', (.02, .02, .022), 0, .85), accent=pbr('VX_Accent', (.55, .75, .02), 0, .4),
           lens=pbr('VX_LensClear', (.8, .85, .9), 0, .02, .3, alpha=.12), drl=pbr('VX_LED_DRL', (.85, .92, 1), 0, .3, emit=(.85, .93, 1.0), es=12),
           tail=pbr('VX_LED_Tail', (.6, 0, .01), 0, .3, emit=(1, .01, .015), es=9), lensred=pbr('VX_LensRed', (.30, 0, .004), 0, .03, .3, alpha=.8),
           ind=pbr('VX_LED_Indicator', (.8, .3, 0), 0, .3, emit=(1, .35, 0), es=.7))
CAR = bpy.data.collections.new('VORTEX_R'); sc.collection.children.link(CAR)
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
cr = body.data.attributes.new('crease_edge', 'FLOAT', 'EDGE'); nrings = len(rings); crest = set()
for i in range(nrings):
    if not (-2.12 < rings[i][0][1] < 2.16): continue
    for j in (7, NR - 7): crest.add(i * NR + j)
for e in body.data.edges:
    a_, b_ = e.vertices
    if a_ in crest and b_ in crest and abs(a_ - b_) == NR: cr.data[e.index].value = .62                       # fender-crest / shoulder character line (crisp, still flowing)
REPORT = dict(cage=dict(stations=len(rings), points_per_ring=NR, cage_faces=len(F), fairing='Taubin 30 x (0.5, -0.53) along Y + 12 x (0.45, -0.48) around each section', max_control_point_shift_mm=round(CAGE_SHIFT_MM, 1)))
sub = body.modifiers.new('sub', 'SUBSURF'); sub.levels = sub.render_levels = 3
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='sub')
# wheel arches (exact boolean) + liners
def cyl(r, x0, x1, y, z, seg=64):
    bm = bmesh.new(); r0 = [bm.verts.new((x0, y + r * math.cos(2 * math.pi * k / seg), z + r * math.sin(2 * math.pi * k / seg))) for k in range(seg)]; r1 = [bm.verts.new((x1, v.co.y, v.co.z)) for v in r0]
    for k in range(seg): bm.faces.new((r0[k], r0[(k + 1) % seg], r1[(k + 1) % seg], r1[k]))
    bm.faces.new(r0[::-1]); bm.faces.new(r1); bm.normal_update(); me = bpy.data.meshes.new('cut'); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new('cut', me); sc.collection.objects.link(o); return o
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    c = cyl(r + .045, sx * .55, sx * 1.4, y, r + .01)
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
    R_ = r + .043; zc = r + .01; seg = 28; a0, a1 = math.radians(-25), math.radians(205)
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
    if any(p is None for r in rows for p in r): print('PATCH MISS', t); return
    n0 = len(G['V']); nc = nu + 1
    for r in rows: G['V'] += [tuple(p) for p in r]
    for j in range(nv):
        for i in range(nu):
            f = (n0 + j * nc + i, n0 + j * nc + i + 1, n0 + (j + 1) * nc + i + 1, n0 + (j + 1) * nc + i); G['F'].append(f[::-1] if flip else f); G['T'].append(t)
for sx in (1, -1):
    fl = sx < 0
    # large corner intakes (trapezoid, tall) + carbon blade dividing each
    quad_patch(fh, [(sx * .40, .43), (sx * .78, .50), (sx * .76, .20), (sx * .44, .19)], 10, 6, 'mesh', .002, fl)            # corner intake (stays inside the fascia)
    quad_patch(fh, [(sx * .40, .44), (sx * .78, .51), (sx * .782, .496), (sx * .40, .426)], 10, 1, 'carbon', .004, fl)
    quad_patch(fh, [(sx * .59, .465), (sx * .608, .468), (sx * .60, .195), (sx * .582, .195)], 1, 6, 'carbon', .006, fl)
    # headlight: sharp boomerang — slim blade along the fender front + hook down the intake edge
    quad_patch(fh, [(sx * .50, .555), (sx * .90, .655), (sx * .905, .625), (sx * .50, .535)], 14, 2, 'trim', .002, fl)
    quad_patch(fh, [(sx * .54, .552), (sx * .88, .645), (sx * .882, .634), (sx * .54, .543)], 14, 1, 'drl', .004, fl)
    quad_patch(fh, [(sx * .845, .64), (sx * .875, .645), (sx * .875, .52), (sx * .855, .53)], 1, 5, 'drl', .004, fl)
    quad_patch(fh, [(sx * .60, .564), (sx * .80, .612), (sx * .80, .597), (sx * .60, .552)], 6, 1, 'ind', .004, fl)
    quad_patch(fh, [(sx * .50, .558), (sx * .90, .658), (sx * .905, .622), (sx * .50, .532)], 14, 2, 'lens', .007, fl)
    # hood vents (aero), front fender louvre exit
    quad_patch(th, [(sx * .14, -1.62), (sx * .40, -1.58), (sx * .42, -1.32), (sx * .18, -1.36)], 6, 4, 'mesh', .002, sx > 0)
    # side: deep intake (dark inner), carbon blade, door shut line, rocker blade, mirror stalks
    quad_patch(lambda y, z, o: sh(sx, y, z, o), [(.42, .60), (.90, .74), (.90, .33), (.48, .40)], 10, 6, 'mesh', .002, sx > 0)    # intake throat inside the scoop
    quad_patch(lambda y, z, o: sh(sx, y, z, o), [(.30, .66), (.40, .62), (.46, .38), (.36, .35)], 2, 6, 'carbon', .006, sx > 0)   # carbon blade at the scoop mouth
    quad_patch(lambda y, z, o: sh(sx, y, z, o), [(-1.02, .20), (.95, .20), (.95, .24), (-1.02, .24)], 30, 1, 'carbon', .008, sx > 0)
    quad_patch(lambda y, z, o: sh(sx, y, z, o), [(-.93, .26), (-.925, .26), (-.88, .76), (-.885, .76)], 1, 8, 'black', .001, sx > 0)
    quad_patch(lambda y, z, o: sh(sx, y, z, o), [(.205, .26), (.21, .26), (.205, .76), (.20, .76)], 1, 8, 'black', .001, sx > 0)
quad_patch(fh, [(-.30, .30), (.30, .30), (.24, .20), (-.24, .20)], 10, 3, 'mesh', .002, True)            # centre nose intake (three-intake front signature)
# rear: black mesh panel across the tail, segmented raked slash lights (3 per side), centre twin exhaust, diffuser + strakes
quad_patch(rh, [(-.60, .725), (.60, .725), (.50, .43), (-.50, .43)], 20, 5, 'mesh', .002)
quad_patch(rh, [(-.52, .43), (.52, .43), (.56, .41), (-.56, .41)], 20, 1, 'carbon', .004)
for sx in (1, -1):
    for k in range(3):
        x0 = .66 + .065 * k; z0 = .82 - .012 * k
        quad_patch(rh, [(sx * x0, z0), (sx * (x0 + .05), z0 + .012), (sx * (x0 + .02), z0 - .16), (sx * (x0 - .03), z0 - .172)], 2, 5, 'tail', .004, sx < 0)
    quad_patch(rh, [(sx * .645, .835), (sx * .87, .84), (sx * .86, .63), (sx * .62, .63)], 8, 6, 'lensred', .008, sx < 0)
    quad_patch(rh, [(sx * .67, .60), (sx * .82, .60), (sx * .82, .585), (sx * .67, .585)], 4, 1, 'ind', .004, sx < 0)
quad_patch(rh, [(-.62, .765), (.62, .765), (.62, .752), (-.62, .752)], 30, 1, 'tail', .004)                 # thin full-width tail thread joining the slashes
for cx in (-.11, .11):                                                                                       # centre twin exhaust (high, in the mesh panel)
    p = rh(cx, .52, 0); seg = 22
    A = [(cx + .055 * math.cos(2 * math.pi * k / seg), p.y - .10, .52 + .045 * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    B = [(x, p.y + .025, z) for x, y, z in A]; Ci = [(cx + .046 * math.cos(2 * math.pi * k / seg), p.y + .025, .52 + .037 * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    strip(A, B, 'exhaust', closed=True); strip(B, Ci, 'exhaust', closed=True); strip(Ci, [(x, y - .08, z) for x, y, z in Ci], 'trim', closed=True)
xs = list(np.linspace(-.80, .80, 25)); ys = list(np.linspace(1.62, 2.20, 10)); dz = lambda y: lerp(.108, .40, ss(1.62, 2.20, y) ** 1.25)
rows = [[(x, y, dz(y)) for x in xs] for y in ys]; n0 = len(G['V'])
for r in rows: G['V'] += r
for j in range(len(ys) - 1):
    for i in range(len(xs) - 1): G['F'].append((n0 + j * 25 + i, n0 + (j + 1) * 25 + i, n0 + (j + 1) * 25 + i + 1, n0 + j * 25 + i + 1)); G['T'].append('carbon')
for xf in (-.62, -.36, -.12, .12, .36, .62):
    for off in (-.004, .004): strip([(xf + off, y, dz(y)) for y in ys], [(xf + off, y, max(.108, dz(y) - .12)) for y in ys], 'carbon', flip=off > 0)
# engine-cover louvres (black slats across the deck) + swan-neck rear wing
for k in range(6):
    y = 1.02 + .10 * k
    quad_patch(th, [(-.42, y), (.42, y), (.42, y + .05), (-.42, y + .05)], 12, 1, 'black', .002)
wing_y, wing_z = 1.98, 1.205
for sx in (1, -1):                                                                                           # swan-neck pylons: rise from the deck, hook over the wing
    base = th(sx * .40, 1.80, 0); pts = []
    for t in np.linspace(0, 1, 9):
        y = lerp(1.80, wing_y + .06, t); z = lerp(base.z, wing_z + .04, ss(0, .85, t)) + .03 * math.sin(math.pi * t); pts.append((sx * .40, y, z))
    for (a, b) in zip(pts, pts[1:]):
        Vb = []
        for p in (a, b): Vb += [(p[0] - .012, p[1] - .02, p[2]), (p[0] + .012, p[1] - .02, p[2]), (p[0] + .012, p[1] + .02, p[2]), (p[0] - .012, p[1] + .02, p[2])]
        add(Vb, [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], 'carbon')
af = [(0.0, 0.0), (.05, .018), (.14, .026), (.24, .018), (.30, .004), (.24, .0), (.14, -.006), (.05, -.004)]     # cambered airfoil (chord .30)
xsw = list(np.linspace(-.86, .86, 23)); ring_w = []
for x in xsw:
    tip = ss(.70, .86, abs(x)); ring_w.append([(x, wing_y - .14 + c, wing_z + z + .02 * tip) for c, z in af])
for A, B in zip(ring_w, ring_w[1:]):
    n0 = len(G['V']); G['V'] += A + B; k = len(A)
    for i in range(k): G['F'].append((n0 + i, n0 + (i + 1) % k, n0 + k + (i + 1) % k, n0 + k + i)); G['T'].append('carbon')
for x in (-.86, .86):                                                                                        # endplates
    add([(x, wing_y - .20, wing_z - .07), (x, wing_y + .20, wing_z - .07), (x, wing_y + .20, wing_z + .07), (x, wing_y - .20, wing_z + .06)], [(0, 1, 2, 3)], 'carbon')
    add([(x + .006 * (1 if x > 0 else -1), wing_y - .20, wing_z - .07), (x + .006 * (1 if x > 0 else -1), wing_y + .20, wing_z - .07), (x + .006 * (1 if x > 0 else -1), wing_y + .20, wing_z + .07), (x + .006 * (1 if x > 0 else -1), wing_y - .20, wing_z + .06)], [(3, 2, 1, 0)], 'carbon')
quad_patch(lambda x, z, o: Vector((x, wing_y + .158 + o, z)), [(-.12, wing_z + .012), (.12, wing_z + .012), (.12, wing_z + .002), (-.12, wing_z + .002)], 6, 1, 'tail', .0)   # third brake light
# front splitter blade
xs = list(np.linspace(-.80, .80, 37)); fr = [fh(x, .17, 0) for x in xs]
A = [(x, (p.y if p else -2.2) - .03, .15) for x, p in zip(xs, fr)]; B = [(x, -1.90, .15) for x in xs]
strip(B, A, 'carbon'); strip([(x, y, z - .012) for x, y, z in A], [(x, y, z - .012) for x, y, z in B], 'carbon'); strip(A, [(x, y, z - .012) for x, y, z in A], 'carbon', flip=True)
det = obj('Details', G['V'], G['F'], G['T'])
bm = bmesh.new(); bm.from_mesh(det.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6); bm.to_mesh(det.data); bm.free(); det.data.shade_smooth(); det.data.set_sharp_from_angle(angle=math.radians(35))
# mirrors (aero pod on a twin-blade stalk from the door top)
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=20, v_segments=12, radius=1.0)
    for v in bmm.verts:
        x, y, z = v.co; y = y * (1.0 if y < 0 else .4); v.co = Vector((x * .095, y * .09, z * .042)) + Vector((sx * 1.035, -.62, .91))
    me = bpy.data.meshes.new('M'); bmm.to_mesh(me); bmm.free(); mo = bpy.data.objects.new('Mirror_' + ('L' if sx > 0 else 'R'), me); CAR.objects.link(mo); me.materials.append(MAT['paint']); me.shade_smooth()
    Vs = [(sx * .88, -.70, .835), (sx * .88, -.60, .835), (sx * 1.0, -.60, .895), (sx * 1.0, -.66, .895)]
    so = obj('MirrorStalk_' + ('L' if sx > 0 else 'R'), Vs + [(x, y, z + .012) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'carbon')
    b2 = bmesh.new(); b2.from_mesh(so.data); bmesh.ops.recalc_face_normals(b2, faces=b2.faces); b2.to_mesh(so.data); b2.free()
# ================================================================ wheels: dark forged 10-spoke (5 Y pairs) + big rotors + acid-green calipers
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
    Gs = {'V': [], 'F': []}
    face = hw * .58
    for s_ in range(5):
        for side_ in (-1, 1):
            a_in = 2 * math.pi * s_ / 5; a_out = a_in + side_ * .30; secs = []
            for t in np.linspace(0, 1, 5):
                rr_ = lerp(.07, rr - .02, t); a = lerp(a_in + side_ * .03, a_out, t ** 1.4); w = lerp(.026, .016, t); xx = face - .02 * math.sin(math.pi * t)
                Rm = Matrix.Rotation(a, 3, 'X'); secs.append([Rm @ Vector((sx * (xx + .004), -w, rr_)), Rm @ Vector((sx * (xx + .004), w, rr_)), Rm @ Vector((sx * (xx - .016), w, rr_)), Rm @ Vector((sx * (xx - .016), -w, rr_))])
            for A, B in zip(secs, secs[1:]):
                n0 = len(Gs['V']); Gs['V'] += [tuple(p) for p in A + B]
                for i in range(4): f = (n0 + i, n0 + (i + 1) % 4, n0 + 4 + (i + 1) % 4, n0 + 4 + i); Gs['F'].append(f if sx > 0 else f[::-1])
    Vh, Fh = revolve([(face + .008, 0.0), (face + .008, .03), (face, .05), (face - .01, .075)], 24, sx); n0 = len(Gs['V']); Gs['V'] += Vh; Gs['F'] += [tuple(n0 + i for i in f) for f in Fh]
    obj(name.replace('Wheel', 'Spokes'), Gs['V'], Gs['F'], 'rim', o)
    Vd, Fd = revolve([(hw * .12, .10), (hw * .12, rr - .03), (-hw * .05, rr - .03), (-hw * .05, .10)], 48, sx); obj(name.replace('Wheel', 'BrakeDisc'), Vd, Fd, 'rotor', o)
    Gc = {'V': [], 'F': []}; front = y < 0
    for k in range(10):
        a = math.radians(30 + 8 * k); a2 = math.radians(30 + 8 * (k + 1)); r0, r1 = rr - .09, rr - .015
        Vs = []
        for xx in (sx * hw * .30, -sx * hw * .14):
            Vs += [(xx, rr_ * math.cos(aa) * (1 if front else -1), rr_ * math.sin(aa)) for rr_, aa in ((r0, a), (r1, a), (r1, a2), (r0, a2))]
        n0 = len(Gc['V']); Gc['V'] += Vs
        for f in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): Gc['F'].append(tuple(n0 + i for i in f))
    cal = obj(name.replace('Wheel', 'Caliper'), Gc['V'], Gc['F'], 'caliper', o)
    for ch in o.children:
        b2 = bmesh.new(); b2.from_mesh(ch.data); bmesh.ops.recalc_face_normals(b2, faces=b2.faces) if ch == cal else None; b2.to_mesh(ch.data); b2.free(); ch.data.shade_smooth(); ch.data.set_sharp_from_angle(angle=math.radians(40))
for c, (y, R, W) in {'FL': (YF, RF, WF), 'FR': (YF, RF, WF), 'RL': (YR, RR, WR), 'RR': (YR, RR, WR)}.items():
    wheel(f'Wheel_{c}', y, R, W, 1 if c[1] == 'L' else -1, .254 if y < 0 else .267)
# ================================================================ interior silhouette (low race seats, wraparound dash, yoke-shaped wheel) + floor
GI = {'V': [], 'F': [], 'T': []}
def ibox(c, s, t, tilt=0.0):
    rot = Matrix.Rotation(tilt, 3, 'X'); hx, hy, hz = s; Vb = [Vector((x, y, z)) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
    n0 = len(GI['V']); GI['V'] += [tuple(rot @ v + Vector(c)) for v in Vb]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): GI['F'].append(tuple(n0 + i for i in f)); GI['T'].append(t)
for sx in (1, -1):
    ibox((sx * .36, .05, .28), (.22, .24, .05), 'leather'); ibox((sx * .36, .30, .60), (.21, .06, .30), 'leather', -.38); ibox((sx * .36, .25, .58), (.05, .06, .26), 'accent', -.38)
ibox((0, -.55, .66), (.72, .14, .06), 'leather'); ibox((0, -.25, .38), (.12, .50, .12), 'trim'); ibox((.36, -.36, .66), (.13, .025, .09), 'trim', .45)
ibox((0, .52, .62), (.70, .05, .30), 'trim')                                                                  # bulkhead behind the seats (engine bay)
interior = obj('Interior_Blockout', GI['V'], GI['F'], GI['T'])
m_ = interior.modifiers.new('b', 'BEVEL'); m_.width = .02; m_.segments = 2
with bpy.context.temp_override(object=interior, active_object=interior): bpy.ops.object.modifier_apply(modifier='b')
interior.data.shade_smooth()
obj('Floor', [(-.82, -1.9, .108), (.82, -1.9, .108), (.82, 1.70, .108), (-.82, 1.70, .108)], [(3, 2, 1, 0)], 'trim')
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
for nm, (y0, y1, xs_) in {'hood': (-1.95, -1.0, (0, .25, .45)), 'roof': (-.15, .55, (0, .2, .35)), 'rear_deck': (1.0, 2.15, (0, .3, .55))}.items():
    ys_ = np.linspace(y0, y1, 60); h = ys_[1] - ys_[0]; W_[nm] = {f'x={x}': dict(zip(('inflections', 'fairness_rms'), waviness(sect(x, ys_), h))) for x in xs_}
for sx_name, ys_ in (('door_lateral', np.linspace(-.80, .10, 50)),):
    zz = .52; xs = []
    for y in ys_:
        loc = BV2.ray_cast(Vector((3, y, zz)), Vector((-1, 0, 0)))[0]; xs.append(loc.x if loc else np.nan)
    W_[sx_name] = dict(zip(('inflections', 'fairness_rms'), waviness(np.array(xs), ys_[1] - ys_[0])))
REPORT['waviness'] = W_
# ================================================================ report + save
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons) if o.type == 'MESH' else 0
allm = [o for o in CAR.objects if o.type == 'MESH']; pts = np.array([(o.matrix_world @ v.co)[:] for o in allm for v in o.data.vertices])
bp = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices])
REPORT.update(stage='01 blockout', design=DIM, measured=dict(length=round(float(np.ptp(pts[:, 1])), 3), width_overall=round(float(np.ptp(pts[:, 0])), 3), width_body=round(float(np.ptp(bp[:, 0])), 3),
              height=round(float(pts[:, 2].max()), 3), height_body=round(float(bp[:, 2].max()), 3)), triangles_total=sum(tris(o) for o in allm), objects={o.name: tris(o) for o in allm})
json.dump(REPORT, open(os.path.join(REPD(), 'VX_blockout_stats.json'), 'w'), indent=1)
print('DIMS', REPORT['measured'], 'TRIS', REPORT['triangles_total']); print('WAVE', json.dumps(W_))
path = CKP('vortexr_01_blockout.blend'); assert SCR or not os.path.exists(path), path
bpy.ops.wm.save_as_mainfile(filepath=path); print('SAVED', path)
