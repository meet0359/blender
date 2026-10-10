# Titan GT (Phase C) — original grand-touring design blockout. Blender -b --factory-startup --python tg_blockout.py
# Front-engine GT: long hood, cabin set back, fastback greenhouse, ducktail, wide rear haunches. Convention: +Z up, nose -Y, vehicle left +X, 1 BU = 1 m.
# The body is a lofted ring cage (stations along Y, symmetric rings) under subdivision; glass / grille / lights are tagged faces or surface-projected parts.
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, math, json
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = lambda *a: os.path.join(ROOT, *a)
SCR = os.environ.get('TG_SCRATCH')
def CKP(n):
    d = SCR or P('blend'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'
def ss(a, b, x): t = min(1.0, max(0.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t
def pchip(xk, yk):
    """monotone cubic interpolation (smooth, no overshoot) -> f(x)."""
    xk = np.asarray(xk, float); yk = np.asarray(yk, float); h = np.diff(xk); d = np.diff(yk) / h; m = np.zeros_like(yk)
    for i in range(1, len(xk) - 1):
        if d[i - 1] * d[i] > 0: w1 = 2 * h[i] + h[i - 1]; w2 = h[i] + 2 * h[i - 1]; m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    m[0], m[-1] = d[0], d[-1]
    def f(x):
        x = min(max(x, xk[0]), xk[-1]); i = min(len(h) - 1, max(0, int(np.searchsorted(xk, x) - 1))); t = (x - xk[i]) / h[i]
        return float((2 * t**3 - 3 * t**2 + 1) * yk[i] + (t**3 - 2 * t**2 + t) * h[i] * m[i] + (-2 * t**3 + 3 * t**2) * yk[i + 1] + (t**3 - t**2) * h[i] * m[i + 1])
    return f
# ================================================================ design parameters (metres)
DIM = dict(length=4.72, width_body=2.01, height=1.295, wheelbase=2.82, track_f=1.69, track_r=1.71, overhang_f=.92, overhang_r=.98, ground_clearance=.125,
           tire_f='265/35 R20 (R 0.347)', tire_r='305/30 R21 (R 0.358)')
YF, YR = -1.41, 1.41; RF, RR = .347, .358; WF, WR = .265, .305; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.33, 2.39
# centreline top profile: nose -> long hood -> windshield -> roof -> fastback -> ducktail
ZC = pchip([YN, -2.24, -1.9, -1.41, -.9, -.58, -.52, -.25, .05, .30, .58, .95, 1.35, 1.70, 2.05, 2.28, YT],
           [.585, .640, .695, .745, .820, .878, .900, 1.07, 1.255, 1.292, 1.272, 1.170, 1.030, .962, .945, .958, .905])
ZBELT = pchip([YN, -2.2, -1.41, -.9, -.55, 0, .6, 1.1, 1.5, 2.0, 2.3, YT], [.580, .655, .805, .830, .865, .890, .905, .930, .945, .935, .925, .885])  # fender / deck edge
WBELT = pchip([YN, -2.24, -1.95, -1.41, -.8, -.2, .5, 1.05, 1.45, 1.95, 2.3, YT], [.70, .82, .885, .925, .875, .845, .845, .865, .885, .855, .79, .70])
WMAX = pchip([YN, -2.26, -2.0, -1.41, -.95, -.3, .4, .95, 1.41, 1.9, 2.3, YT], [.80, .91, .955, .985, .962, .940, .950, .990, 1.008, .965, .895, .80])  # shoulder / max width
ZSH = pchip([YN, -1.41, 0, 1.0, 1.41, 2.0, YT], [.50, .63, .64, .69, .72, .70, .64])
ZFLOOR = pchip([YN, -2.15, -1.9, 1.80, 2.15, YT], [.23, .155, .125, .125, .20, .34])
WFLOOR = pchip([YN, -2.1, 0, 2.1, YT], [.60, .78, .80, .80, .70])
CAB = lambda y: ss(-.66, -.50, y) * (1 - ss(1.30, 1.62, y))                                       # greenhouse presence (A-pillar foot .. C-pillar end)
ROOFW = pchip([-.55, -.2, .25, .7, 1.2, 1.6], [.60, .585, .575, .57, .55, .50])
SILLW = lambda y: WBELT(y) - .085
def ring_half(y):
    """half-section control points (x >= 0) from bottom centre up the +X side to the top centre."""
    zb, wf, wm, zs, zb_, wb, zc, c = ZFLOOR(y), WFLOOR(y), WMAX(y), ZSH(y), ZBELT(y), WBELT(y), ZC(y), CAB(y)
    zsill = zb + .10 + .02 * ss(-2.2, -1.8, y); wsill = wm - .045
    scoop = .032 * ss(-.95, -.55, y) * (1 - ss(.55, 1.05, y))                                        # sculpted lower bodyside (GT side scallop) between the wheels
    side = [(0.0, zb), (.5 * wf, zb), (wf, zb + .004), (wsill - .02, zb + .03), (wsill + .004, zsill), (wm - .012 - scoop, zs - .17), (wm - .004 - scoop * .45, zs - .07), (wm, zs), (wm - .012, zs + .06),
            (lerp(wm, wb, .55), lerp(zs, zb_, .6)), (wb, zb_)]
    # top: deck crown (outside the cabin) blended with the greenhouse (inside)
    crown = lambda t: zb_ + (zc - zb_) * (1 - (1 - t) ** 2.2)                                      # t 0 at deck edge -> 1 at centre
    deck = [(wb * (1 - t), crown(t)) for t in (.18, .42, .68, .86, 1.0)]
    rw = ROOFW(min(max(y, -.55), 1.6)); sw = SILLW(y)
    gh = [(wb - .035, zb_ + .012), (sw, zb_ + .03), (lerp(sw, rw, .55) + .015, lerp(zb_ + .03, zc - .045, .62)), (rw, zc - .045), (.45 * rw, zc - .008), (0.0, zc)]
    top = [(lerp(d[0], g[0], c), lerp(d[1], g[1], c)) for d, g in zip([(wb * .93, crown(.07))] + deck, gh)]
    return side + top
NS = len(ring_half(0.0))                                                                             # 17 points per half (indices 0..16)
I_SILL_TOP = 11; I_GH_SIDE = (12, 13); I_ROOF = (14, 15, 16)
STAT = sorted(set([round(v, 4) for v in list(np.linspace(-2.22, 2.28, 46)) + [-.52, -.46, .02, .08, .64, .70, 1.38, 1.44, YF - .4, YF + .4, YR - .42, YR + .42]]))
NOSE = [(YN + .095, 1.0), (YN + .05, .93), (YN + .022, .80), (YN + .008, .58), (YN, .30)]            # front face: rings shrink toward the fascia centre (flat-ish nose)
TAIL = [(YT - .07, 1.0), (YT - .035, .93), (YT - .014, .80), (YT - .004, .58), (YT, .30)]
def full_ring(y, scale=1.0, centre=None):
    h = ring_half(y); cz = centre if centre is not None else (h[0][1] + h[-1][1]) * .5
    pts = [(x * scale, y, cz + (z - cz) * scale) for x, z in h]
    left = pts; right = [(-x, yy, z) for x, yy, z in pts[1:-1]][::-1]
    return left + right                                                                              # closed ring: bottom centre -> +X side -> top centre -> -X side
rings = []
for y, s in NOSE[::-1]: rings.append(full_ring(y, s, .43))
for y in STAT: rings.append(full_ring(y))
for y, s in TAIL: rings.append(full_ring(y, s, .62))
NR = len(rings[0])
V = [p for r in rings for p in r]; F = []; FT = []
def col_tag(j):
    """ring index -> half-ring index (mirror side folded)."""
    return j if j < NS else NR - j
for i in range(len(rings) - 1):
    for j in range(NR):
        a = i * NR + j; b = i * NR + (j + 1) % NR; cc = (i + 1) * NR + (j + 1) % NR; d = (i + 1) * NR + j
        F.append((a, d, cc, b)); ym = (rings[i][0][1] + rings[i + 1][0][1]) / 2; h0, h1 = col_tag(j), col_tag((j + 1) % NR); FT.append((ym, min(h0, h1), max(h0, h1)))
# caps (fan to a centre point)
for ri, flip in ((0, False), (len(rings) - 1, True)):
    r = rings[ri]; cidx = len(V); V.append(tuple(np.mean(np.array(r), axis=0)))
    for j in range(NR):
        f = (ri * NR + j, ri * NR + (j + 1) % NR, cidx); F.append(f[::-1] if not flip else f); FT.append(('cap', 0, 0))
# face materials
def tag(t):
    if t[0] == 'cap': return 'paint'
    y, a, b = t
    if CAB(y) < .5: return 'paint'
    if a >= I_ROOF[0] and -.50 < y < .03: return 'glass'                                          # windshield
    if a >= I_ROOF[0] and .68 < y < 1.36: return 'glass'                                          # fastback rear window
    if (a, b) == (12, 13) and -.43 < y < 1.12: return 'glass'                                       # side windows
    if (a, b) in ((11, 12), (13, 14)) and -.46 < y < 1.18: return 'black'                           # window surround (black trim)
    if a >= I_ROOF[0] and -.5 < y < 1.36: return 'roof_black' if False else 'paint'
    return 'paint'
TAGS = [tag(t) for t in FT]
# ================================================================ materials
def pbr(name, col, metal=0.0, rough=.4, coat=0.0, alpha=1.0, emit=None, es=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat; b.inputs['Alpha'].default_value = alpha
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    if alpha < 1:
        if hasattr(m, 'surface_render_method'): m.surface_render_method = 'BLENDED'
    return m
MAT = dict(paint=pbr('TG_Paint', (.018, .045, .105), .7, .3, 1.0), glass=pbr('TG_Glass', (.006, .008, .01), 0, .03, .3, alpha=.66), black=pbr('TG_GlossBlack', (.01, .01, .011), 0, .12, .5),
           trim=pbr('TG_SatinBlack', (.02, .02, .022), .2, .5), chrome=pbr('TG_DarkChrome', (.35, .36, .38), 1, .12), rim=pbr('TG_WheelMetal', (.13, .135, .14), 1, .3),
           rim_dark=pbr('TG_WheelDark', (.45, .46, .48), 1, .2), tire=pbr('TG_Tire', (.025, .025, .027), 0, .85), rotor=pbr('TG_Rotor', (.30, .30, .31), 1, .4),
           caliper=pbr('TG_Caliper', (.55, .45, .38), .9, .32, .6), interior=pbr('TG_Leather', (.06, .035, .022), 0, .5), int_dark=pbr('TG_InteriorDark', (.015, .015, .017), 0, .6),
           lens=pbr('TG_LensClear', (.8, .85, .9), 0, .02, .3, alpha=.15), lensred=pbr('TG_LensRed', (.25, .005, .01), 0, .03, .3, alpha=.6),
           drl=pbr('TG_LED_DRL', (.8, .9, 1), 0, .3, emit=(.82, .92, 1.0), es=10), tail=pbr('TG_LED_Tail', (.6, .01, .015), 0, .3, emit=(1, .02, .02), es=8),
           ind=pbr('TG_LED_Indicator', (.8, .3, 0), 0, .3, emit=(1, .35, 0), es=.6), grille=pbr('TG_Grille', (.012, .012, .013), .3, .45), carbon=pbr('TG_Carbon', (.02, .02, .022), .3, .3, .7))
CAR = bpy.data.collections.new('TITAN_GT'); sc.collection.children.link(CAR)
def obj(name, Vs, Fs, tags, parent=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in Vs], [], [tuple(f) for f in Fs]); me.update()
    order = list(dict.fromkeys(tags))
    for t in order: me.materials.append(MAT[t])
    me.polygons.foreach_set('material_index', [order.index(t) for t in tags]); me.update()
    o = bpy.data.objects.new(name, me); CAR.objects.link(o)
    if parent: o.parent = parent
    return o
body = obj('Body_Blockout', V, F, TAGS)
bm = bmesh.new(); bm.from_mesh(body.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(body.data); bm.free()
sub = body.modifiers.new('sub', 'SUBSURF'); sub.levels = sub.render_levels = 2
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='sub')
# wheel arches: cut the body sides around each wheel, add a satin-black arch liner (wheel well)
def cyl(name, r, x0, x1, y, z, seg=48):
    bm = bmesh.new(); ring0 = [bm.verts.new((x0, y + r * math.cos(2 * math.pi * k / seg), z + r * math.sin(2 * math.pi * k / seg))) for k in range(seg)]
    ring1 = [bm.verts.new((x1, v.co.y, v.co.z)) for v in ring0]
    for k in range(seg): bm.faces.new((ring0[k], ring0[(k + 1) % seg], ring1[(k + 1) % seg], ring1[k]))
    bm.faces.new(ring0[::-1]); bm.faces.new(ring1); bm.normal_update(); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return o
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    c = cyl('cut', r + .052, sx * .52, sx * 1.4, y, r + .012)
    m = body.modifiers.new('arch', 'BOOLEAN'); m.object = c; m.operation = 'DIFFERENCE'; m.solver = 'EXACT'
    with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='arch')
    bpy.data.objects.remove(c, do_unlink=True)
body.data.shade_smooth(); body.data.set_sharp_from_angle(angle=math.radians(50))
gW = {'V': [], 'F': [], 'T': []}
def add(Vs, Fs, t):
    n = len(gW['V']); gW['V'] += [tuple(v) for v in Vs]; gW['F'] += [tuple(i + n for i in f) for f in Fs]; gW['T'] += [t] * len(Fs)
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):                         # wheel-well liners (half drum above the axle)
    R_ = r + .05; seg = 24; xi, xo = sx * .50, sx * (.92 if y < 0 else .94)
    a0, a1 = math.radians(-20), math.radians(200)
    pts = [(y + R_ * math.cos(lerp(a0, a1, k / seg)), r + .012 + R_ * math.sin(lerp(a0, a1, k / seg))) for k in range(seg + 1)]
    Vs = [(xi, yy, zz) for yy, zz in pts] + [(xo, yy, zz) for yy, zz in pts]; n = seg + 1
    Fs = [(k, k + 1, n + k + 1, n + k) if sx > 0 else (k, n + k, n + k + 1, k + 1) for k in range(seg)]
    add(Vs, Fs, 'trim')
    # arch lip: a slim rolled flare following the cut
    lip = []
    for k in range(seg + 1):
        a = lerp(math.radians(-8), math.radians(188), k / seg); yy = y + (r + .052) * math.cos(a); zz = r + .012 + (r + .052) * math.sin(a)
        lip.append((yy, zz, a))
    Vs = []
    for yy, zz, a in lip:
        nx, nz = math.cos(a), math.sin(a)
        xo2 = sx * (WMAX(yy) + .006)
        Vs += [(xo2 - sx * .035, yy, zz), (xo2, yy + nx * .012, zz + nz * .012), (xo2 - sx * .02, yy + nx * .03, zz + nz * .03)]
    Fs = []
    for k in range(seg):
        for q in range(2):
            f = (3 * k + q, 3 * k + q + 1, 3 * (k + 1) + q + 1, 3 * (k + 1) + q); Fs.append(f if sx < 0 else f[::-1])
    add(Vs, Fs, 'paint')
wells = obj('ArchLiners_Lips', gW['V'], gW['F'], gW['T']); wells.data.shade_smooth()
# ================================================================ surface projection helpers (front / rear details)
BV = BVHTree.FromObject(body, bpy.context.evaluated_depsgraph_get())
def hit(x, z, front, off=0.0, ystart=None):
    o = Vector((x, -4 if front else 4, z)); d = Vector((0, 1 if front else -1, 0)); loc, nrm, i, dist = BV.ray_cast(o, d)
    if loc is None: return None
    out = Vector((0, -1 if front else 1, 0)); nrm = nrm if nrm.dot(out) > 0 else -nrm; return loc + nrm * off
def hit_side(x0, y, z, off=0.0):
    o = Vector((x0 * 3, y, z)); d = Vector((-1 if x0 > 0 else 1, 0, 0)); loc, nrm, i, dist = BV.ray_cast(o, d)
    if loc is None: return None
    out = Vector((1 if x0 > 0 else -1, 0, 0)); nrm = nrm if nrm.dot(out) > 0 else -nrm; return loc + nrm * off
def hit_top(x, y, off=0.0):
    o = Vector((x, y, 3)); loc, nrm, i, dist = BV.ray_cast(o, Vector((0, 0, -1)))
    if loc is None: return None
    nrm = nrm if nrm.z > 0 else -nrm; return loc + nrm * off
G = {'V': [], 'F': [], 'T': []}
def patch(fn, us, vs, t, flip=False):
    rows = [[fn(u, v) for u in us] for v in vs]
    if any(p is None for r in rows for p in r): print('PATCH MISS', t); return False
    n0 = len(G['V']); nu = len(us)
    for r in rows: G['V'] += [tuple(p) for p in r]
    for i in range(len(vs) - 1):
        for j in range(nu - 1):
            f = (n0 + i * nu + j, n0 + i * nu + j + 1, n0 + (i + 1) * nu + j + 1, n0 + (i + 1) * nu + j); G['F'].append(f[::-1] if flip else f); G['T'].append(t)
    return True
lin = lambda a, b, n: [a + (b - a) * k / n for k in range(n + 1)]
# grille: wide trapezoid with soft corners, recessed slats (horizontal), framed in dark chrome
def grille_x(v): return lerp(.44, .54, v)                                                           # half width: narrower at the top, wider at the bottom
gz0, gz1 = .245, .495
for k, (off, t) in enumerate(((.004, 'chrome'),)):
    pass
for sx in (1, -1):                                                                                  # grille frame: a dark-chrome ring (top, bottom, sides)
    patch(lambda u, v, sx=sx: hit(sx * lerp(grille_x(v), grille_x(v) + .028, u), lerp(gz1 + .02, gz0 - .02, v), True, .003), [0, 1], lin(0, 1, 8), 'chrome', flip=sx < 0)
patch(lambda u, v: hit(u * (grille_x(0) + .028), lerp(gz1 + .02, gz1, v), True, .003), lin(-1, 1, 30), [0, 1], 'chrome', flip=True)
patch(lambda u, v: hit(u * (grille_x(1) + .028), lerp(gz0, gz0 - .02, v), True, .003), lin(-1, 1, 30), [0, 1], 'chrome', flip=True)
patch(lambda u, v: hit(u * grille_x(v), lerp(gz1, gz0, v), True, .002), lin(-1, 1, 30), lin(0, 1, 6), 'grille', flip=True)
for zs in np.linspace(gz0 + .03, gz1 - .03, 7):                                                     # slats
    v = (gz1 - zs) / (gz1 - gz0)
    patch(lambda u, w, zs=zs, v=v: hit(u * grille_x(v) * .97, zs + lerp(.005, -.005, w), True, .0045), lin(-1, 1, 24), [0, 1], 'chrome', flip=True)
# lower intakes + splitter lip
for sx in (1, -1):
    patch(lambda u, v, sx=sx: hit(sx * lerp(.62, .84, u), lerp(.36, .21, v) + .03 * u, True, .002), lin(0, 1, 8), lin(0, 1, 4), 'grille', flip=sx < 0)
patch(lambda u, v: (lambda p: Vector((p.x, p.y - .03 * (1 - v), lerp(.165, .175, v))) if p else None)(hit(u * .88, .20, True)), lin(-1, 1, 32), [0, 1], 'carbon', flip=True)
# headlights: slim swept LED units on the front corners (lens + DRL blade + projector strip)
for sx in (1, -1):
    def hl(u, v, off, sx=sx):
        x = sx * lerp(.58, .865, u); z = lerp(.525 + .05 * u, .600 + .075 * u, v); return hit(x, z, True, off)
    patch(lambda u, v: hl(u, v, .002), lin(0, 1, 16), lin(0, 1, 3), 'black', flip=sx < 0)
    patch(lambda u, v: hl(lerp(.04, .97, u), lerp(.62, .85, v), .006), lin(0, 1, 16), [0, 1], 'drl', flip=sx < 0)
    patch(lambda u, v: hl(lerp(.08, .55, u), lerp(.18, .45, v), .006), lin(0, 1, 8), [0, 1], 'lens' if False else 'chrome', flip=sx < 0)
    patch(lambda u, v: hl(u, v, .010), lin(0, 1, 16), lin(0, 1, 3), 'lens', flip=sx < 0)
    patch(lambda u, v: hl(lerp(.70, .97, u), lerp(.18, .42, v), .007), lin(0, 1, 4), [0, 1], 'ind', flip=sx < 0)
# rear: full-width light bar + C-shaped ends, diffuser, quad exhaust
def tl(u, v, off):
    x = u * .86; z = .845 + .008 * abs(u) ** 2 + lerp(-.010, .010, v); return hit(x, z, False, off)
patch(lambda u, v: tl(u, lerp(-1.8, 1.8, v), .002), lin(-1, 1, 48), lin(0, 1, 3), 'black')
patch(lambda u, v: tl(u, v, .005), lin(-1, 1, 48), [0, 1], 'tail')
for sx in (1, -1):
    patch(lambda u, v, sx=sx: hit(sx * lerp(.70, .86, u), lerp(.845, .735, v), False, .004), lin(0, 1, 6), lin(0, 1, 5), 'black', flip=sx < 0)
    patch(lambda u, v, sx=sx: hit(sx * lerp(.82, .855, u), lerp(.835, .745, v), False, .007), [0, 1], lin(0, 1, 5), 'tail', flip=sx < 0)
    patch(lambda u, v, sx=sx: hit(sx * lerp(.72, .80, u), lerp(.762, .748, v), False, .007), lin(0, 1, 4), [0, 1], 'tail', flip=sx < 0)
    patch(lambda u, v, sx=sx: hit(sx * lerp(.72, .79, u), lerp(.80, .78, v), False, .007), lin(0, 1, 3), [0, 1], 'ind', flip=sx < 0)
patch(lambda u, v: tl(u, lerp(-1.8, 1.8, v), .010), lin(-1, 1, 48), lin(0, 1, 3), 'lensred')
patch(lambda u, v: hit(u * lerp(.84, .78, v), lerp(.47, .345, v), False, .004), lin(-1, 1, 36), lin(0, 1, 4), 'trim')                     # lower rear valance (satin black, houses the quad exhaust)
patch(lambda u, v: hit(u * .82, lerp(.475, .465, v), False, .005), lin(-1, 1, 36), [0, 1], 'chrome')
patch(lambda u, v: hit(u * .26, lerp(.66, .54, v), False, .003), lin(-1, 1, 8), lin(0, 1, 3), 'black')                                   # licence-plate recess (blank)
for sx in (1, -1):                                                                                  # rear haunch crease light catcher
    patch(lambda u, v, sx=sx: hit(sx * lerp(.30, .78, u), lerp(.735, .728, v) + .012 * u, False, .002), lin(0, 1, 16), [0, 1], 'black', flip=sx < 0)
for xf in (-.42, -.14, .14, .42):                                                                   # diffuser strakes
    Vs = [(xf - .004, 2.0, .132), (xf + .004, 2.0, .132), (xf + .004, YT - .05, .22), (xf - .004, YT - .05, .22), (xf - .004, 2.0, .16), (xf + .004, 2.0, .16), (xf + .004, YT - .05, .33), (xf - .004, YT - .05, .33)]
    n0 = len(G['V']); G['V'] += Vs
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)): G['F'].append(tuple(n0 + i for i in f)); G['T'].append('carbon')
for cx in (-.64, -.53, .53, .64):                                                                   # quad exhaust
    seg = 20; r1, r2 = .036, .030; p = hit(cx, .40, False); yo = p.y + .012 if p else YT; yi = yo - .14
    for (ra, rb, ya, yb, t) in ((r1, r1, yi, yo, 'chrome'), (r1, r2, yo, yo, 'chrome'), (r2, r2, yo, yi + .03, 'trim')):
        A = [(cx + ra * math.cos(2 * math.pi * k / seg), ya, .40 + ra * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
        B = [(cx + rb * math.cos(2 * math.pi * k / seg), yb, .40 + rb * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
        n0 = len(G['V']); G['V'] += A + B
        for k in range(seg): G['F'].append((n0 + k, n0 + (k + 1) % seg, n0 + seg + (k + 1) % seg, n0 + seg + k)); G['T'].append(t)
# side details: front-fender vent (aero) + side sill blade + door shut lines + flush handles
for sx in (1, -1):
    patch(lambda u, v, sx=sx: hit_side(sx, lerp(-.92, -.70, u) + .05 * v, lerp(.50, .66, v), .003), lin(0, 1, 6), lin(0, 1, 4), 'black', flip=sx > 0)
    for zz in (.545, .585, .625):
        patch(lambda u, v, sx=sx, zz=zz: hit_side(sx, lerp(-.90, -.715, u) + .05 * (zz - .5) / .16, zz + lerp(-.006, .006, v), .006), lin(0, 1, 6), [0, 1], 'chrome', flip=sx > 0)
    patch(lambda u, v, sx=sx: hit_side(sx, lerp(-.88, 1.0, u), lerp(.245, .275, v), .004), lin(0, 1, 30), [0, 1], 'carbon', flip=sx > 0)
    for yy in (-.88, .62):                                                                          # door shut lines
        patch(lambda u, v, sx=sx, yy=yy: hit_side(sx, yy + lerp(-.0035, .0035, u) + .03 * v, lerp(.30, .90, v), .001), [0, 1], lin(0, 1, 12), 'black', flip=sx > 0)
    patch(lambda u, v, sx=sx: hit_side(sx, lerp(.28, .43, u), lerp(.745, .765, v), .002), lin(0, 1, 4), [0, 1], 'chrome', flip=sx > 0)
# hood power bulge lines / bonnet shut line
for sx in (1, -1):
    patch(lambda u, v, sx=sx: hit_top(sx * lerp(.66, .672, v) - sx * .04 * (1 - u), lerp(-2.10, -.66, u), .001), lin(0, 1, 30), [0, 1], 'black', flip=sx < 0)
details = obj('Details', G['V'], G['F'], G['T'])
bm = bmesh.new(); bm.from_mesh(details.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6); bm.to_mesh(details.data); bm.free(); details.data.shade_smooth(); details.data.set_sharp_from_angle(angle=math.radians(35))
# mirrors (door-mounted, on short carbon stalks)
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=20, v_segments=12, radius=1.0)
    bmesh.ops.scale(bmm, vec=(.10, .065, .052), verts=bmm.verts); bmesh.ops.translate(bmm, vec=(sx * .995, -.40, .985), verts=bmm.verts)
    for v in bmm.verts:
        if v.co.y < -.40: v.co.y = -.40 + (v.co.y + .40) * .55
    me = bpy.data.meshes.new('Mirror'); bmm.to_mesh(me); bmm.free(); mo = bpy.data.objects.new('Mirror_L' if sx > 0 else 'Mirror_R', me); CAR.objects.link(mo); me.materials.append(MAT['paint']); me.shade_smooth()
    st = bpy.data.objects.new('MirrorStalk', None)
    Vs = [(sx * .835, -.44, .905), (sx * .835, -.36, .905), (sx * .915, -.385, .955), (sx * .915, -.425, .955)]
    so = obj('MirrorStalk_' + ('L' if sx > 0 else 'R'), Vs + [(x, y, z + .035) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], ['paint'] * 6)
    bm = bmesh.new(); bm.from_mesh(so.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(so.data); bm.free()
# ================================================================ wheels (revolved tire + 5 twin-spoke rim + brake disc + caliper)
def revolve(profile, seg, x_sign):
    """profile: list of (axial x offset, radius); revolved about the X axis."""
    Vs, Fs = [], []; n = len(profile)
    for k in range(seg):
        a = 2 * math.pi * k / seg
        for (dx, r) in profile: Vs.append((x_sign * dx, r * math.cos(a), r * math.sin(a)))
    for k in range(seg):
        for i in range(n - 1):
            a0, b0 = k * n + i, k * n + i + 1; a1, b1 = ((k + 1) % seg) * n + i, ((k + 1) % seg) * n + i + 1
            Fs.append((a0, a1, b1, b0) if x_sign > 0 else (a0, b0, b1, a1))
    return Vs, Fs
def wheel(name, y, z, R, W, sx, rim_r):
    o = bpy.data.objects.new(name, None); CAR.objects.link(o); o.location = (sx * (XF if y < 0 else XR), y, z)
    hw = W / 2
    tire = [(-hw * .80, rim_r + .005), (-hw * .97, rim_r + .03), (-hw, R * .80), (-hw * .96, R * .94), (-hw * .80, R * .995), (0, R), (hw * .80, R * .995), (hw * .96, R * .94), (hw, R * .80), (hw * .97, rim_r + .03), (hw * .80, rim_r + .005)]
    Vt, Ft = revolve(tire, 64, sx); t = obj(name.replace('Wheel', 'Tire'), Vt, Ft, ['tire'] * len(Ft), o)
    lip = [(hw * .80, rim_r - .025), (hw * .86, rim_r + .004), (hw * .70, rim_r + .010), (hw * .60, rim_r - .012), (-hw * .70, rim_r - .015), (-hw * .80, rim_r + .004)]
    Vr, Fr = revolve(lip, 64, sx); r = obj(name.replace('Wheel', 'RimBarrel'), Vr, Fr, ['rim'] * len(Fr), o)
    Gs = {'V': [], 'F': [], 'T': []}
    def box(c, size, rot, mat):
        hx, hy, hz = size; Vb = [Vector((x, yy, zz)) for x in (-hx, hx) for yy in (-hy, hy) for zz in (-hz, hz)]
        n0 = len(Gs['V']); Gs['V'] += [tuple(rot @ v + Vector(c)) for v in Vb]
        for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): Gs['F'].append(tuple(n0 + i for i in f)); Gs['T'].append(mat)
    xo = sx * hw * .62
    for k in range(5):
        for d in (-.12, .12):
            a = 2 * math.pi * k / 5 + d; rot = Matrix.Rotation(a, 3, 'X')
            L = rim_r - .065; c = rot @ Vector((0, 0, .06 + L / 2))
            box((xo + sx * .012 + c.x, c.y, c.z), (.012, .016, L / 2 + .01), rot @ Matrix.Rotation(sx * .0, 3, 'Y'), 'rim')
    hub = [(hw * .62 + .02, 0.0), (hw * .62 + .02, .05), (hw * .62, .07), (hw * .62 - .02, .075)]
    Vh, Fh = revolve(hub, 32, sx); n0 = len(Gs['V']); Gs['V'] += Vh; Gs['F'] += [tuple(n0 + i for i in f) for f in Fh]; Gs['T'] += ['rim_dark'] * len(Fh)
    sp = obj(name.replace('Wheel', 'Spokes'), Gs['V'], Gs['F'], Gs['T'], o)
    disc = [(hw * .15, .10), (hw * .15, rim_r - .035), (-hw * .02, rim_r - .035), (-hw * .02, .10)]
    Vd, Fd = revolve(disc, 48, sx); d = obj(name.replace('Wheel', 'BrakeDisc'), Vd, Fd, ['rotor'] * len(Fd), o)
    Gc = {'V': [], 'F': [], 'T': []}
    for k in range(9):                                                                              # caliper arc (rear-upper quadrant)
        a = math.radians(60 + 9 * k); a2 = math.radians(60 + 9 * (k + 1)); rr0, rr1 = rim_r - .085, rim_r - .022
        pts = [(rr0, a), (rr1, a), (rr1, a2), (rr0, a2)]; Vs = []
        for xx in (sx * hw * .30, -sx * hw * .10):
            Vs += [(xx, r_ * math.cos(aa) * (1 if y < 0 else -1), r_ * math.sin(aa)) for r_, aa in pts]
        n0 = len(Gc['V']); Gc['V'] += Vs
        for f in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)): Gc['F'].append(tuple(n0 + i for i in f)); Gc['T'].append('caliper')
    cal = obj(name.replace('Wheel', 'Caliper'), Gc['V'], Gc['F'], Gc['T'], o)
    for x in (t, r, sp, d, cal): x.data.shade_smooth(); x.data.set_sharp_from_angle(angle=math.radians(40))
    bm = bmesh.new(); bm.from_mesh(cal.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(cal.data); bm.free()
    bm = bmesh.new(); bm.from_mesh(sp.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(sp.data); bm.free()
    return o
for c, (y, R, W) in {'FL': (YF, RF, WF), 'FR': (YF, RF, WF), 'RL': (YR, RR, WR), 'RR': (YR, RR, WR)}.items():
    sx = 1 if c[1] == 'L' else -1; wheel(f'Wheel_{c}', y, R, R, W, sx, .254 if y < 0 else .267)
# ================================================================ interior silhouette (seen through the glass)
GI = {'V': [], 'F': [], 'T': []}
def ibox(c, s, mat, tilt=0.0):
    rot = Matrix.Rotation(tilt, 3, 'X'); hx, hy, hz = s
    Vb = [Vector((x, y, z)) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]; n0 = len(GI['V']); GI['V'] += [tuple(rot @ v + Vector(c)) for v in Vb]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)): GI['F'].append(tuple(n0 + i for i in f)); GI['T'].append(mat)
for sx in (1, -1):
    ibox((sx * .37, .30, .42), (.24, .26, .07), 'interior'); ibox((sx * .37, .52, .72), (.23, .07, .30), 'interior', -.22); ibox((sx * .37, .60, 1.02), (.12, .05, .08), 'interior', -.22)
ibox((0, -.38, .80), (.80, .16, .09), 'int_dark'); ibox((0, -.10, .45), (.10, .55, .10), 'int_dark'); ibox((.37, -.20, .78), (.18, .03, .14), 'int_dark', .35)
ibox((0, .78, .82), (.72, .25, .04), 'int_dark')
interior = obj('Interior_Blockout', GI['V'], GI['F'], GI['T'])
bm = bmesh.new(); sub_ = interior.modifiers.new('b', 'BEVEL'); sub_.width = .025; sub_.segments = 2
with bpy.context.temp_override(object=interior, active_object=interior): bpy.ops.object.modifier_apply(modifier='b')
bm.free(); interior.data.shade_smooth(); interior.data.set_sharp_from_angle(angle=math.radians(40))
# floor tray
obj('Floor', [(-.80, -2.0, .13), (.80, -2.0, .13), (.80, 2.05, .13), (-.80, 2.05, .13)], [(3, 2, 1, 0)], ['trim'])
# ================================================================ report
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons) if o.type == 'MESH' else 0
allm = [o for o in CAR.objects if o.type == 'MESH']; pts = np.array([(o.matrix_world @ v.co)[:] for o in allm for v in o.data.vertices])
dims = dict(length=round(float(np.ptp(pts[:, 1])), 3), width=round(float(np.ptp(pts[:, 0])), 3), height=round(float(pts[:, 2].max()), 3))
bp = np.array([(body.matrix_world @ v.co)[:] for v in body.data.vertices]); dims['width_body'] = round(float(np.ptp(bp[:, 0])), 3)
os.makedirs(P('reports'), exist_ok=True)
json.dump(dict(stage='01 blockout', design=DIM, measured=dims, triangles_total=sum(tris(o) for o in allm), objects={o.name: tris(o) for o in allm}),
          open(os.path.join(SCR or P('reports'), 'TG_blockout_stats.json'), 'w'), indent=1)
print('DIMS', dims, 'TRIS', sum(tris(o) for o in allm))
path = CKP('titangt_01_blockout.blend'); assert SCR or not os.path.exists(path), path
bpy.ops.wm.save_as_mainfile(filepath=path); print('SAVED', path)
