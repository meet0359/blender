# REVISION r1 copy: ROOT -> C_TitanGT_r1 (the frozen C_TitanGT is only ever read). # Titan GT (Phase C) production library. Design curves are copied VERBATIM from the approved blockout (tg_blockout.py lines 14-79).
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, re, json, math, zlib
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
WS = '/Users/meetshah/Documents/blender'; ROOT = WS + '/vehicles/C_TitanGT_r1'; P = lambda *a: os.path.join(ROOT, *a)
P0_BLEND = WS + '/environment/P0_RoadFoundation/blend/road_05_export_ready.blend'
SCR = os.environ.get('TG_SCRATCH')
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
    bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=path, copy=True, relative_remap=True); print('SAVED', path, flush=True)
# ---------------------------------------------------------------- approved design (verbatim from the blockout)
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
CAGE_V, CAGE_F, CAGE_FT = V, F, FT
# caps + face tags (as the blockout)
def cage_mesh_data():
    V_, F_, FT_ = list(CAGE_V), list(CAGE_F), list(CAGE_FT)
    for ri, flip in ((0, False), (len(rings) - 1, True)):
        r = rings[ri]; cidx = len(V_); V_.append(tuple(np.mean(np.array(r), axis=0)))
        for j in range(NR):
            f = (ri * NR + j, ri * NR + (j + 1) % NR, cidx); F_.append(f[::-1] if not flip else f); FT_.append(('cap', 0, 0))
    def tag(t):
        if t[0] == 'cap': return 'paint'
        y, a, b = t
        if CAB(y) < .5: return 'paint'
        if a >= I_ROOF[0] and -.50 < y < .03: return 'glass'
        if a >= I_ROOF[0] and .68 < y < 1.36: return 'glass'
        if (a, b) == (12, 13) and -.43 < y < 1.12: return 'glass'
        if (a, b) in ((11, 12), (13, 14)) and -.40 < y < 1.15: return 'gloss_black'
        return 'paint'
    return V_, F_, [tag(t) for t in FT_]

# ---------------------------------------------------------------- materials (15, Zero Gap R convention)
LIGHTS = ['TG_LED_DRL', 'TG_LED_Headlamp', 'TG_LED_Tail', 'TG_LED_Brake', 'TG_LED_Indicator_L', 'TG_LED_Indicator_R', 'TG_LED_Reverse']
MATS = ['TG_Paint', 'TG_Palette', 'TG_Carbon', 'TG_Tire', 'TG_Glass', 'TG_LensClear', 'TG_LensRed', 'TG_Display'] + LIGHTS
EMIT = {'TG_LED_DRL': ((.82, .92, 1.0), 10.0), 'TG_LED_Headlamp': ((.95, .97, 1.0), 3.0), 'TG_LED_Tail': ((1.0, .012, .015), 7.0), 'TG_LED_Brake': ((1.0, .01, .012), 1.5),
        'TG_LED_Indicator_L': ((1.0, .32, .0), .7), 'TG_LED_Indicator_R': ((1.0, .32, .0), .7), 'TG_LED_Reverse': ((1.0, 1.0, 1.0), .3), 'TG_Display': ((.55, .62, .70), 1.2)}
PAINT = (.012, .032, .085)                                                                             # midnight blue (linear)
SW = {  # swatch: (linear base, metallic, roughness)
    'black_plastic': ((.014, .014, .015), 0.0, .55), 'gloss_black': ((.008, .008, .009), 0.0, .10), 'satin_black': ((.018, .018, .02), .2, .45), 'pocket': ((.006, .006, .007), 0.0, .7),
    'housing': ((.035, .036, .038), .6, .35), 'dark_chrome': ((.32, .33, .35), 1.0, .14), 'chrome': ((.62, .63, .65), 1.0, .08), 'exhaust': ((.45, .42, .40), 1.0, .22), 'exhaust_inner': ((.03, .025, .02), .6, .7),
    'wheel_graphite': ((.11, .115, .12), 1.0, .32), 'wheel_machined': ((.40, .41, .43), 1.0, .2), 'caliper_bronze': ((.48, .30, .14), 1.0, .30), 'rotor': ((.28, .28, .29), 1.0, .42),
    'rotor_hat': ((.06, .06, .065), .8, .5), 'hub': ((.20, .20, .21), 1.0, .35), 'leather_cognac': ((.115, .045, .018), 0.0, .48), 'leather_black': ((.014, .013, .013), 0.0, .5),
    'alcantara': ((.022, .022, .024), 0.0, .9), 'int_trim': ((.03, .03, .032), .1, .45), 'aluminium': ((.50, .51, .52), 1.0, .28), 'grille': ((.010, .010, .011), .3, .4),
    'mirror': ((.70, .73, .76), 1.0, .03), 'reflector': ((.60, .61, .63), 1.0, .12), 'carpet': ((.012, .012, .013), 0.0, .95), 'stitch': ((.25, .14, .06), 0.0, .5)}
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
    tex['pal_bc'] = save_img('TG_Palette_BaseColor', bc, False); tex['pal_ms'] = save_img('TG_Palette_MetallicSmoothness', ms, True)
    tex['pal_r'] = save_img('TG_Palette_Roughness', ro, True); tex['pal_m'] = save_img('TG_Palette_Metallic', me, True)
    # carbon twill 2x2 (512 px = one 0.25 m tile): tows alternate direction per cell, twill offset per row
    n = 512; yy, xx = np.mgrid[0:n, 0:n] / n; cells = 16; cx = (xx * cells); cy = (yy * cells); ix = np.floor(cx).astype(int); iy = np.floor(cy).astype(int)
    warp = ((ix + iy) // 2) % 2 == 0; fx = cx - ix; fy = cy - iy
    tow = np.where(warp, np.sin(np.pi * fx) ** .6, np.sin(np.pi * fy) ** .6); sheen = np.where(warp, .55 + .45 * np.cos(np.pi * fy * 2) ** 2, .55 + .45 * np.cos(np.pi * fx * 2) ** 2)
    v = .018 + .028 * tow * sheen; tex['carb_bc'] = save_img('TG_Carbon_BaseColor', np.dstack([v, v, v * 1.05]), False)
    tex['carb_n'] = save_img('TG_Carbon_Normal', normal_from(tow * .5, 6.0), True)
    # tire: U around the circumference (8 tread repeats per turn), V across the profile (0 inner bead .. .5 crown .. 1 inner bead)
    n = 1024; yy, xx = np.mgrid[0:n, 0:n] / n; v = yy; u = xx * 8
    tread = (np.abs(v - .5) < .23).astype(float)
    groove = np.zeros_like(v)
    for g in (-.13, -.04, .05, .14): groove = np.maximum(groove, (np.abs(v - .5 - g) < .010).astype(float))
    sipe = ((np.abs(((u * 6 + (v - .5) * 3) % 1) - .5) < .04) & (np.abs(v - .5) < .19) & (np.abs(v - .5) > .02)).astype(float)
    side_ring = (np.abs(np.abs(v - .5) - .36) < .006).astype(float)
    h = .5 - .5 * groove * tread - .3 * sipe * tread + .2 * side_ring
    base = .022 + .006 * (1 - tread) - .006 * groove * tread
    tex['tire_bc'] = save_img('TG_Tire_BaseColor', np.dstack([base, base, base * 1.03]), False); tex['tire_n'] = save_img('TG_Tire_Normal', normal_from(h, 12.0), True)
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
        if name == 'TG_Paint':
            b.inputs['Base Color'].default_value = (*PAINT, 1); b.inputs['Metallic'].default_value = .62; b.inputs['Roughness'].default_value = .30
            b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = .025
        elif name == 'TG_Palette':
            c = _img(nt, tex['pal_bc'], False, True); r = _img(nt, tex['pal_r'], True, True); mt = _img(nt, tex['pal_m'], True, True)
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(r.outputs[0], b.inputs['Roughness']); nt.links.new(mt.outputs[0], b.inputs['Metallic'])
        elif name in ('TG_Carbon', 'TG_Tire'):
            k = 'carb' if name == 'TG_Carbon' else 'tire'; c = _img(nt, tex[k + '_bc'], False); n = _img(nt, tex[k + '_n'], True); nm = nt.nodes.new('ShaderNodeNormalMap')
            nm.inputs['Strength'].default_value = .5 if k == 'carb' else 1.0
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(n.outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], b.inputs['Normal'])
            b.inputs['Roughness'].default_value = .3 if k == 'carb' else .85; b.inputs['Coat Weight'].default_value = .7 if k == 'carb' else 0
        elif name in ('TG_Glass', 'TG_LensClear', 'TG_LensRed'):
            col, a = {'TG_Glass': ((.006, .008, .010), .66), 'TG_LensClear': ((.85, .88, .9), .10), 'TG_LensRed': ((.30, .0, .004), .80)}[name]
            b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = .02; b.inputs['Alpha'].default_value = a; b.inputs['Coat Weight'].default_value = .4
            if hasattr(m, 'surface_render_method'): m.surface_render_method = 'BLENDED'
            m.use_backface_culling = False
        elif name in EMIT:
            col, st = EMIT[name]; b.inputs['Base Color'].default_value = (*[c * .6 for c in col], 1); b.inputs['Roughness'].default_value = .3
            b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = st
    return M

# ---------------------------------------------------------------- geometry helpers
def mk(name, V, F, FM, c, mats):
    """mesh from verts / faces / per-face material tags ('TG_Palette:<swatch>' or a material name)."""
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
        if nm == 'TG_Palette':
            u, v = swatch_uv(SWATCH[key.data[p.index].value] if key else 'black_plastic')
            for li in p.loop_indices: uv.data[li].uv = (u, v)
        elif nm == 'TG_Tire' and keep:
            for li in p.loop_indices: uv.data[li].uv = keep[li]
        elif nm == 'TG_Carbon':
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
