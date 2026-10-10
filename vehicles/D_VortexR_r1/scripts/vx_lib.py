# REVISION r1 copy (paths -> D_VortexR_r1; the frozen D_VortexR is only ever read). # Vortex R (Phase D) production library. Design code (curves, cage, fairing, tags) is copied VERBATIM from the approved blockout (vx_blockout.py lines 18-111).
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, re, json, math, zlib
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
WS = '/Users/meetshah/Documents/blender'; ROOT = WS + '/vehicles/D_VortexR_r1'; P = lambda *a: os.path.join(ROOT, *a)
SCR = os.environ.get('VX_SCRATCH')
def CKP(n):
    d = SCR or P('blend'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def EXP(n):
    d = os.path.join(SCR, 'exports') if SCR else P('exports'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def TEX(n):
    d = os.path.join(SCR, 'textures') if SCR else P('textures'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def REPD():
    d = os.path.join(SCR, 'reports') if SCR else P('reports'); os.makedirs(d, exist_ok=True); return d
def save_ckp(name):
    path = CKP(name); assert SCR or not os.path.exists(path), 'checkpoint exists: ' + path
    bpy.ops.file.make_paths_relative()
    import time as _t
    for attempt in range(4):                                                                         # transient FS race on the temp-file rename ('File exists' / 'No such file')
        try: bpy.ops.wm.save_as_mainfile(filepath=path, copy=True, relative_remap=True); break
        except RuntimeError as e_:
            if attempt == 3: raise
            print('SAVE RETRY', attempt + 1, e_, flush=True); _t.sleep(2)
    print('SAVED', path, flush=True)
# ---------------------------------------------------------------- approved design (verbatim)
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
# ---------------------------------------------------------------- materials (15, Zero Gap R convention)
LIGHTS = ['VX_LED_DRL', 'VX_LED_Headlamp', 'VX_LED_Tail', 'VX_LED_Brake', 'VX_LED_Indicator_L', 'VX_LED_Indicator_R', 'VX_LED_Reverse']
MATS = ['VX_Paint', 'VX_Palette', 'VX_Carbon', 'VX_Tire', 'VX_Glass', 'VX_LensClear', 'VX_LensRed', 'VX_Display'] + LIGHTS
EMIT = {'VX_LED_DRL': ((.82, .92, 1.0), 10.0), 'VX_LED_Headlamp': ((.95, .97, 1.0), 3.0), 'VX_LED_Tail': ((1.0, .012, .015), 7.0), 'VX_LED_Brake': ((1.0, .01, .012), 1.5),
        'VX_LED_Indicator_L': ((1.0, .32, .0), .7), 'VX_LED_Indicator_R': ((1.0, .32, .0), .7), 'VX_LED_Reverse': ((1.0, 1.0, 1.0), .3), 'VX_Display': ((.55, .62, .70), 1.2)}
PAINT = (.075, .028, .155)                                                                             # deep violet (linear, approved blockout colour)
SW = {  # swatch: (linear base, metallic, roughness)
    'black_plastic': ((.014, .014, .015), 0.0, .55), 'gloss_black': ((.008, .008, .009), 0.0, .10), 'satin_black': ((.016, .016, .018), .2, .5), 'pocket': ((.005, .005, .006), 0.0, .7),
    'housing': ((.03, .031, .034), .6, .35), 'mesh': ((.010, .010, .011), .4, .5), 'dark_chrome': ((.30, .31, .33), 1.0, .14), 'exhaust': ((.36, .33, .30), 1.0, .22), 'exhaust_inner': ((.03, .025, .02), .6, .7),
    'wheel_forged': ((.035, .036, .040), 1.0, .32), 'wheel_lip': ((.22, .22, .23), 1.0, .25), 'caliper_green': ((.55, .75, .02), .1, .30), 'rotor': ((.32, .32, .33), 1.0, .35),
    'rotor_hat': ((.05, .05, .055), .8, .5), 'hub': ((.18, .18, .19), 1.0, .35), 'alcantara': ((.020, .020, .022), 0.0, .88), 'leather_black': ((.013, .012, .012), 0.0, .48),
    'accent_green': ((.55, .75, .02), 0.0, .40), 'int_trim': ((.025, .025, .027), .1, .45), 'aluminium': ((.50, .51, .52), 1.0, .28), 'grille': ((.010, .010, .011), .3, .4),
    'mirror': ((.70, .73, .76), 1.0, .03), 'reflector': ((.60, .61, .63), 1.0, .12), 'carpet': ((.011, .011, .012), 0.0, .95), 'harness': ((.03, .03, .032), 0.0, .6)}
SWATCH = list(SW)
GRID, CELL = 8, 32
def swatch_uv(name):
    i = SWATCH.index(name); return ((i % GRID) + .5) / GRID, 1 - ((i // GRID) + .5) / GRID
l2s = lambda c: 12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055
def save_img(name, arr, data):
    h, w = arr.shape[:2]; im = bpy.data.images.new(name, w, h, alpha=True)
    if data: im.colorspace_settings.name = 'Non-Color'
    a = np.dstack([arr, np.ones((h, w))]) if arr.shape[2] == 3 else arr
    im.pixels.foreach_set(a.astype(np.float32).ravel()); p = TEX(name + '.png'); im.filepath_raw = p; im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im); return p
def normal_from(h, k):
    gy, gx = np.gradient(h); n = np.dstack([-gx * k, -gy * k, np.ones_like(h)]); n /= np.linalg.norm(n, axis=2, keepdims=True); return n * .5 + .5
def make_textures():
    tex = {}; N = GRID * CELL; bc = np.zeros((N, N, 3)); ms = np.zeros((N, N, 4)); ro = np.zeros((N, N, 3)); me = np.zeros((N, N, 3))
    for i, k in enumerate(SWATCH):
        r, c = divmod(i, GRID); y0 = N - (r + 1) * CELL; x0 = c * CELL; col, m, rg = SW[k]
        bc[y0:y0 + CELL, x0:x0 + CELL] = [l2s(v) for v in col]; ms[y0:y0 + CELL, x0:x0 + CELL] = [m, 0, 0, 1 - rg]; ro[y0:y0 + CELL, x0:x0 + CELL] = rg; me[y0:y0 + CELL, x0:x0 + CELL] = m
    tex['pal_bc'] = save_img('VX_Palette_BaseColor', bc, False); tex['pal_ms'] = save_img('VX_Palette_MetallicSmoothness', ms, True)
    tex['pal_r'] = save_img('VX_Palette_Roughness', ro, True); tex['pal_m'] = save_img('VX_Palette_Metallic', me, True)
    # carbon twill 2x2 (512 px = one 0.25 m tile): tows alternate direction per cell, twill offset per row
    n = 512; yy, xx = np.mgrid[0:n, 0:n] / n; cells = 16; cx = (xx * cells); cy = (yy * cells); ix = np.floor(cx).astype(int); iy = np.floor(cy).astype(int)
    warp = ((ix + iy) // 2) % 2 == 0; fx = cx - ix; fy = cy - iy
    tow = np.where(warp, np.sin(np.pi * fx) ** .6, np.sin(np.pi * fy) ** .6); sheen = np.where(warp, .55 + .45 * np.cos(np.pi * fy * 2) ** 2, .55 + .45 * np.cos(np.pi * fx * 2) ** 2)
    v = .018 + .028 * tow * sheen; tex['carb_bc'] = save_img('VX_Carbon_BaseColor', np.dstack([v, v, v * 1.05]), False)
    tex['carb_n'] = save_img('VX_Carbon_Normal', normal_from(tow * .5, 6.0), True)
    # tire: U around the circumference (8 tread repeats per turn), V across the profile (0 inner bead .. .5 crown .. 1 inner bead)
    n = 1024; yy, xx = np.mgrid[0:n, 0:n] / n; v = yy; u = xx * 8
    tread = (np.abs(v - .5) < .23).astype(float)
    groove = np.zeros_like(v)
    for g in (-.13, -.04, .05, .14): groove = np.maximum(groove, (np.abs(v - .5 - g) < .010).astype(float))
    sipe = ((np.abs(((u * 6 + (v - .5) * 3) % 1) - .5) < .04) & (np.abs(v - .5) < .19) & (np.abs(v - .5) > .02)).astype(float)
    side_ring = (np.abs(np.abs(v - .5) - .36) < .006).astype(float)
    h = .5 - .5 * groove * tread - .3 * sipe * tread + .2 * side_ring
    base = .022 + .006 * (1 - tread) - .006 * groove * tread
    tex['tire_bc'] = save_img('VX_Tire_BaseColor', np.dstack([base, base, base * 1.03]), False); tex['tire_n'] = save_img('VX_Tire_Normal', normal_from(h, 12.0), True)
    return tex
def _img(nt, path, data, closest=False):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(path, check_existing=True)
    if data: n.image.colorspace_settings.name = 'Non-Color'
    if closest: n.interpolation = 'Closest'
    return n
def build_materials(tex):
    M = {}
    for name in MATS:
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled'); nt.links.new(b.outputs[0], out.inputs[0]); M[name] = m
        if name == 'VX_Paint':
            b.inputs['Base Color'].default_value = (*PAINT, 1); b.inputs['Metallic'].default_value = .80; b.inputs['Roughness'].default_value = .36
            b.inputs['Coat Weight'].default_value = .35; b.inputs['Coat Roughness'].default_value = .18                        # satin metallic
        elif name == 'VX_Palette':
            c = _img(nt, tex['pal_bc'], False, True); r = _img(nt, tex['pal_r'], True, True); mt = _img(nt, tex['pal_m'], True, True)
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(r.outputs[0], b.inputs['Roughness']); nt.links.new(mt.outputs[0], b.inputs['Metallic'])
        elif name in ('VX_Carbon', 'VX_Tire'):
            k = 'carb' if name == 'VX_Carbon' else 'tire'; c = _img(nt, tex[k + '_bc'], False); n = _img(nt, tex[k + '_n'], True); nm = nt.nodes.new('ShaderNodeNormalMap')
            nm.inputs['Strength'].default_value = .5 if k == 'carb' else 1.0
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(n.outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], b.inputs['Normal'])
            b.inputs['Roughness'].default_value = .3 if k == 'carb' else .85; b.inputs['Coat Weight'].default_value = .7 if k == 'carb' else 0
        elif name in ('VX_Glass', 'VX_LensClear', 'VX_LensRed'):
            col, a = {'VX_Glass': ((.006, .008, .010), .66), 'VX_LensClear': ((.85, .88, .9), .10), 'VX_LensRed': ((.30, .0, .004), .80)}[name]
            b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = .02; b.inputs['Alpha'].default_value = a; b.inputs['Coat Weight'].default_value = .4
            if hasattr(m, 'surface_render_method'): m.surface_render_method = 'BLENDED'
            m.use_backface_culling = False
        elif name in EMIT:
            col, st = EMIT[name]; b.inputs['Base Color'].default_value = (*[c * .6 for c in col], 1); b.inputs['Roughness'].default_value = .3
            b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = st
    return M

# ---------------------------------------------------------------- geometry helpers
def mk(name, V, F, FM, c, mats):
    """mesh from verts / faces / per-face material tags ('VX_Palette:<swatch>' or a material name)."""
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in V], [], [tuple(f) for f in F]); me.update()
    base = [m.split(':')[0] for m in FM]; order = list(dict.fromkeys(base))
    for m in order: me.materials.append(mats[m])
    me.polygons.foreach_set('material_index', [order.index(m) for m in base])
    a = me.attributes.new('swatch', 'INT', 'FACE'); a.data.foreach_set('value', [SWATCH.index(m.split(':')[1]) if ':' in m else 0 for m in FM]); me.update()
    o = bpy.data.objects.new(name, me); c.objects.link(o); return o
class Geo:
    def __init__(s): s.V, s.F, s.T = [], [], []
    def add(s, V, F, t):
        n = len(s.V); s.V += [tuple(v) for v in V]; s.F += [tuple(i + n for i in f) for f in F]; s.T += ([t] * len(F) if isinstance(t, str) else list(t))
    def grid(s, rows, t, flip=False):
        n0 = len(s.V); nr, nc = len(rows), len(rows[0])
        for r in rows: s.V += [tuple(p) for p in r]
        for i in range(nr - 1):
            for j in range(nc - 1):
                f = (n0 + i * nc + j, n0 + i * nc + j + 1, n0 + (i + 1) * nc + j + 1, n0 + (i + 1) * nc + j); s.F.append(f[::-1] if flip else f); s.T.append(t)
    def strip(s, A, B, t, closed=False, flip=False):
        n0 = len(s.V); s.V += [tuple(p) for p in A] + [tuple(p) for p in B]; n = len(A)
        for i in range(n - (0 if closed else 1)):
            j = (i + 1) % n; f = (n0 + i, n0 + j, n0 + n + j, n0 + n + i); s.F.append(f[::-1] if flip else f); s.T.append(t)
    def box(s, c, half, t, rot=None):
        hx, hy, hz = half; R = rot or Matrix.Identity(3); Vb = [R @ Vector((x, y, z)) + Vector(c) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
        s.add(Vb, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)], t)
    def tube(s, centre_fn, n_path, radius_fn, seg, t, closed_ends=True):
        """sweep a circle along a path (centre_fn(k) -> (p, tangent))."""
        rings_ = []
        for k in range(n_path):
            p, tg = centre_fn(k); tg = Vector(tg).normalized(); a = Vector((0, 0, 1)) if abs(tg.z) < .9 else Vector((1, 0, 0)); b1 = tg.cross(a).normalized(); b2 = tg.cross(b1)
            r = radius_fn(k); rings_.append([Vector(p) + (b1 * math.cos(2 * math.pi * q / seg) + b2 * math.sin(2 * math.pi * q / seg)) * r for q in range(seg)])
        for a_, b_ in zip(rings_, rings_[1:]): s.strip(a_, b_, t, closed=True)
def revolve(profile, seg, x_sign, a0=0.0):
    """profile: list of (axial offset, radius), revolved about +X; returns V, F and per-vertex (u, v) for UVs."""
    Vs, Fs, UV = [], [], []; n = len(profile)
    for k in range(seg + 1):
        a = a0 + 2 * math.pi * k / seg
        for i, (dx, r) in enumerate(profile): Vs.append((x_sign * dx, r * math.cos(a), r * math.sin(a))); UV.append((k / seg, i / (n - 1)))
    for k in range(seg):
        for i in range(n - 1):
            a_, b_ = k * n + i, k * n + i + 1; c_, d_ = (k + 1) * n + i + 1, (k + 1) * n + i
            Fs.append((a_, d_, c_, b_) if x_sign > 0 else (a_, b_, c_, d_))
    return Vs, Fs, UV
def ss_(a, b, x): return ss(a, b, x)
def set_origin(o, p):
    p = Vector(p); o.data.transform(Matrix.Translation(-p)); o.matrix_world = Matrix.Translation(p)
def link_only(o, c):
    for x in list(o.users_collection): x.objects.unlink(o)
    c.objects.link(o)
def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if not c: c = bpy.data.collections.new(name); (parent or bpy.context.scene.collection).children.link(c)
    return c
def empty(name, c, loc=(0, 0, 0), parent=None, kind='PLAIN_AXES', size=.25):
    e = bpy.data.objects.new(name, None); e.empty_display_type = kind; e.empty_display_size = size; c.objects.link(e)
    if parent: e.parent = parent
    e.location = loc; return e
def tris(o): return sum(len(p.vertices) - 2 for p in o.data.polygons)
def join(objs, name, c):
    objs = [o for o in objs if o and o.type == 'MESH']
    if not objs: return None
    for o in objs: link_only(o, c)
    a = objs[0]
    if len(objs) > 1:
        with bpy.context.temp_override(active_object=a, object=a, selected_objects=objs, selected_editable_objects=objs): bpy.ops.object.join()
    a.name = name; a.data.name = name; return a
def box_uv(me, tile, layer='UVMap'):
    uv = me.uv_layers.get(layer) or me.uv_layers.new(name=layer)
    for p in me.polygons:
        ax = max(range(3), key=lambda k: abs(p.normal[k]))
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co; uv.data[li].uv = ((co.y / tile, co.z / tile), (co.x / tile, co.z / tile), (co.x / tile, co.y / tile))[ax]
def final_uvs(o, keep_layer=None):
    """single UV0 'UVMap': palette faces -> swatch centre; tire faces keep their revolve UVs ('tireUV'); carbon -> box 0.25 m; others box 1 m."""
    me = o.data
    if not me.polygons: return
    tire = me.uv_layers.get('tireUV'); keep = [tuple(d.uv) for d in tire.data] if tire else None
    for l in list(me.uv_layers): me.uv_layers.remove(l)
    box_uv(me, 1.0); uv = me.uv_layers['UVMap']; cl = me.uv_layers.new(name='_c'); box_uv(me, .25, '_c'); cd = cl.data; key = me.attributes.get('swatch')
    for p in me.polygons:
        m = me.materials[p.material_index] if p.material_index < len(me.materials) else None; nm = m.name if m else ''
        if nm == 'VX_Palette':
            u, v = swatch_uv(SWATCH[key.data[p.index].value] if key else 'black_plastic')
            for li in p.loop_indices: uv.data[li].uv = (u, v)
        elif nm == 'VX_Tire' and keep:
            for li in p.loop_indices: uv.data[li].uv = keep[li]
        elif nm == 'VX_Carbon':
            for li in p.loop_indices: uv.data[li].uv = tuple(cd[li].uv)
    me.uv_layers.remove(me.uv_layers['_c'])
def clean(o, tri_dups=True):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    seen, dups = set(), []
    for f in bm.faces:
        k = frozenset(v.index for v in f.verts); (dups.append(f) if k in seen else seen.add(k))
    bmesh.ops.delete(bm, geom=dups, context='FACES_ONLY')
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=1e-5)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_area() < 2e-9], context='FACES_ONLY')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(o.data); bm.free(); o.data.update()

def purge_slots(o):
    """drop material slots no face uses (keeps per-face assignment)."""
    me = o.data; used = sorted({p.material_index for p in me.polygons}); mats = [me.materials[i] for i in used]; remap = {i: k for k, i in enumerate(used)}
    idx = [remap[p.material_index] for p in me.polygons]; me.materials.clear()
    for m in mats: me.materials.append(m)
    me.polygons.foreach_set('material_index', idx); me.update()
def orient_components(o, centre_z=.55):
    """consistent winding per connected component, then flip a whole component if it faces inward (away from the car centre)."""
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.faces.ensure_lookup_table(); seen = set()
    for f0 in bm.faces:
        if f0.index in seen: continue
        comp = []; st = [f0]
        while st:
            f = st.pop()
            if f.index in seen: continue
            seen.add(f.index); comp.append(f); st += [g for e in f.edges for g in e.link_faces if g.index not in seen]
        score = 0.0
        for f in comp:
            c = f.calc_center_median(); out = Vector((c.x * .6, c.y, c.z - centre_z))
            score += f.normal.dot(out.normalized()) * f.calc_area()
        if score < 0:
            for f in comp: f.normal_flip()
    bm.to_mesh(o.data); bm.free(); o.data.update()
