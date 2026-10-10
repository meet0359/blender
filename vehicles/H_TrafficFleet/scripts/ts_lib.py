# Traffic fleet shared library (Phase H). Shared PBR material library + texture set (atlas, tire, paint flake, light mask), cage helpers, UV conventions.
# Shared textures live in H_TrafficFleet/shared/textures and are generated once (deterministic, seeded); every vehicle references them.
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, json, math
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
WS = '/Users/meetshah/Documents/blender'; FLEET = WS + '/vehicles/H_TrafficFleet'
SHARED_TEX = os.path.join(FLEET, 'shared', 'textures')
SCR = os.environ.get('TS_SCRATCH')
def vroot(v): return os.path.join(FLEET, v)
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
# ================================================================ shared atlas (2048, 8 x 8 cells of 256 px)
ATLAS_N, ATLAS_G = 2048, 8
CELLS = ['plastic_black', 'plastic_dark', 'gloss_black', 'chrome', 'alu_brushed', 'wheel_silver', 'wheel_dark', 'rubber',
         'fabric_dark', 'fabric_light', 'int_plastic', 'carpet', 'grille', 'lamp_housing', 'reflector', 'brake_disc',
         'caliper', 'lug', 'plate', 'badge', 'mirror_glass', 'reflector_red', 'exhaust', 'underbody',
         'frit', 'screen', 'leather', 'lamp_inner', 'reflector_amber', 'dark_chrome', 'arch_liner', 'wiper']
# cell: (linear base rgb, metallic, roughness, normal pattern, pattern strength)
CELL_SPEC = {
    'plastic_black': ((.018, .018, .019), 0, .62, 'grain', 1.0), 'plastic_dark': ((.045, .046, .048), 0, .58, 'grain', 1.0), 'gloss_black': ((.007, .007, .008), 0, .07, None, 0),
    'chrome': ((.90, .90, .92), 1, .045, None, 0), 'alu_brushed': ((.56, .57, .58), 1, .26, 'brushed', .6), 'wheel_silver': ((.55, .56, .58), .9, .26, None, 0),
    'wheel_dark': ((.07, .072, .078), .8, .34, None, 0), 'rubber': ((.018, .018, .018), 0, .80, 'fine', .06), 'fabric_dark': ((.028, .028, .030), 0, .90, 'weave', 1.0),
    'fabric_light': ((.22, .215, .20), 0, .92, 'weave', .7), 'int_plastic': ((.030, .030, .032), 0, .78, 'grain', 1.0), 'carpet': ((.02, .02, .021), 0, .96, 'fine', .3),
    'grille': ((.012, .012, .013), .2, .50, 'honeycomb', 1.0), 'lamp_housing': ((.030, .031, .034), .3, .45, None, 0), 'reflector': ((.86, .87, .88), 1, .08, 'facets', .5),
    'brake_disc': ((.36, .36, .37), 1, .40, 'radial', .8), 'caliper': ((.055, .056, .06), .3, .45, None, 0), 'lug': ((.62, .62, .63), 1, .20, None, 0),
    'plate': ((.80, .80, .78), 0, .35, None, 0), 'badge': ((.85, .86, .88), 1, .08, None, 0), 'mirror_glass': ((.90, .92, .94), 1, .01, None, 0),
    'reflector_red': ((.30, .0, .005), 0, .20, 'facets', 1.0), 'exhaust': ((.25, .24, .23), 1, .35, None, 0), 'underbody': ((.016, .016, .017), 0, .82, 'grain', .6),
    'frit': ((.006, .006, .007), 0, .10, None, 0), 'screen': ((.015, .017, .02), 0, .10, None, 0), 'leather': ((.025, .024, .024), 0, .55, 'grain', .8),
    'lamp_inner': ((.40, .41, .43), .6, .30, None, 0), 'reflector_amber': ((.40, .14, .0), 0, .20, 'facets', 1.0), 'dark_chrome': ((.24, .245, .25), 1, .15, None, 0),
    'arch_liner': ((.016, .016, .017), 0, .80, 'grain', 1.0), 'wiper': ((.015, .015, .016), 0, .55, 'grain', .5)}
def cell_rect(name):
    i = CELLS.index(name); r, c = divmod(i, ATLAS_G); s = 1.0 / ATLAS_G
    return c * s, 1 - (r + 1) * s, s                                                                    # u0, v0, size (UV space, v up)
L2S = np.vectorize(lambda c: 12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055)
def _height(pattern, n, rng):
    yy, xx = np.mgrid[0:n, 0:n] / n
    if pattern == 'grain': return rng.random((n, n)) * .6 + .4 * np.sin(xx * 300 + rng.random() * 6) * np.sin(yy * 280)
    if pattern == 'fine': return rng.random((n, n))
    if pattern == 'brushed': return np.repeat(rng.random((n, 1)), n, 1) * .8 + rng.random((n, n)) * .2
    if pattern == 'weave': return (np.sin(xx * 2 * np.pi * 48) * np.sign(np.sin(yy * 2 * np.pi * 24)) + np.sin(yy * 2 * np.pi * 48) * np.sign(np.sin(xx * 2 * np.pi * 24))) * .5
    if pattern == 'honeycomb':
        u = xx * 14; v = yy * 14 / .866; rows = np.floor(v); u = u + (rows % 2) * .5
        du = (u % 1) - .5; dv = (v % 1) - .5; d = np.maximum(np.abs(du) * 1.0, np.abs(du) * .5 + np.abs(dv) * .866)
        return np.clip((.42 - d) * 8, 0, 1)                                                             # 1 = cell hole (deep), 0 = web
    if pattern == 'radial':
        a = np.arctan2(yy - .5, xx - .5); return np.sin(a * 220 + rng.random((n, n)) * .3) * .3 + rng.random((n, n)) * .2
    if pattern == 'facets': return ((np.floor(xx * 24) + np.floor(yy * 24)) % 2) * .5 + ((xx * 24) % 1) * .5
    if pattern == 'dots':
        u = (xx * 32) % 1 - .5; v = (yy * 32) % 1 - .5; return np.clip(.3 - np.sqrt(u * u + v * v), 0, 1) * 3
    return np.zeros((n, n))
def _blur(h, r):
    k = 2 * r + 1; p = np.pad(h, r, mode='wrap'); c = np.cumsum(np.cumsum(p, 0), 1); c = np.pad(c, ((1, 0), (1, 0)))
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)
def _normal(h, k):
    gy, gx = np.gradient(h); nrm = np.dstack([-gx * k, -gy * k, np.ones_like(h)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True); return nrm * .5 + .5
def _save(name, arr, data, folder):
    os.makedirs(folder, exist_ok=True); h, w = arr.shape[:2]; im = bpy.data.images.new(name, w, h, alpha=True)
    if data: im.colorspace_settings.name = 'Non-Color'
    a = np.dstack([arr, np.ones((h, w))]) if arr.shape[2] == 3 else arr
    im.pixels.foreach_set(a.astype(np.float32).ravel()); p = os.path.join(folder, name + '.png'); im.filepath_raw = p; im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im); return p
def plate_pattern(n, rng):
    img = np.ones((n, n)) * 1.0; band = np.zeros((n, n)); yy, xx = np.mgrid[0:n, 0:n] / n
    band[(xx < .12)] = 1                                                                                  # blue strip (fictional, no country code)
    glyph = np.zeros((n, n))
    for k in range(6):                                                                                    # six blocky glyphs "AB 123"-like (fictional)
        x0 = .18 + k * .13; seg = rng.integers(1, 6, size=5)
        for j, s_ in enumerate(seg):
            glyph[(xx > x0) & (xx < x0 + .09) & (yy > .25 + j * .1) & (yy < .25 + j * .1 + .05 * s_ / 3)] = 1
        glyph[(xx > x0) & (xx < x0 + .02) & (yy > .25) & (yy < .75)] = 1
    return band, glyph
def make_shared_textures(force=False):
    """deterministic shared texture set; regenerated only if missing (fleet-wide reuse)."""
    names = ['TS_Atlas_BaseColor', 'TS_Atlas_Normal', 'TS_Atlas_Roughness', 'TS_Atlas_Metallic', 'TS_Atlas_MetallicSmoothness', 'TS_Tire_BaseColor', 'TS_Tire_Normal', 'TS_Tire_Roughness',
             'TS_PaintFlake_Normal', 'TS_Lights_BaseColor', 'TS_Lights_Emission', 'TS_Lights_ChannelID']
    paths = {n: os.path.join(SHARED_TEX, n + '.png') for n in names}
    if not force and all(os.path.exists(p) for p in paths.values()): return paths
    rng = np.random.default_rng(20261008); N, G = ATLAS_N, ATLAS_G; C = N // G
    bc = np.zeros((N, N, 3)); nm = np.zeros((N, N, 3)); ro = np.zeros((N, N, 3)); me = np.zeros((N, N, 3)); ms = np.zeros((N, N, 4))
    for i, k in enumerate(CELLS):
        r, c = divmod(i, G); y0 = N - (r + 1) * C; x0 = c * C; col, m, rg, pat, st = CELL_SPEC[k]
        h = _height(pat, C, rng) if pat else np.zeros((C, C)); var = (rng.random((C, C)) - .5) * .06          # subtle albedo variation (no flat swatches)
        base = np.dstack([np.full((C, C), v) for v in col]) * (1 + var[..., None])
        rough = np.clip(rg + (h - h.mean()) * .06 + var * .5, .02, 1)
        if k == 'grille': base *= (1 - .7 * h[..., None]); rough = np.clip(rg + .3 * h, 0, 1)                 # holes darker / rougher
        if k == 'plate':
            band, glyph = plate_pattern(C, rng); base[band > 0] = (.02, .05, .30); base[glyph > 0] = (.015, .015, .02); h = glyph * .6
        if k == 'badge': yy, xx = np.mgrid[0:C, 0:C] / C; ring = np.abs(np.sqrt((xx - .5) ** 2 + (yy - .5) ** 2) - .32) < .05; base[~ring] *= .25; h = ring * 1.0
        if k == 'brake_disc': yy, xx = np.mgrid[0:C, 0:C] / C; rr = np.sqrt((xx - .5) ** 2 + (yy - .5) ** 2); base *= np.where(rr > .46, .55, 1)[..., None]   # darker outer rim (no rust)
        bc[y0:y0 + C, x0:x0 + C] = L2S(np.clip(base, 0, 1)); nm[y0:y0 + C, x0:x0 + C] = _normal(h, 3.0 * st) if pat or k in ('plate', 'badge') else (.5, .5, 1)
        ro[y0:y0 + C, x0:x0 + C] = rough[..., None]; me[y0:y0 + C, x0:x0 + C] = m
        ms[y0:y0 + C, x0:x0 + C] = np.dstack([np.full((C, C), m), np.zeros((C, C)), np.zeros((C, C)), 1 - rough])
    _save('TS_Atlas_BaseColor', bc, False, SHARED_TEX); _save('TS_Atlas_Normal', nm, True, SHARED_TEX); _save('TS_Atlas_Roughness', ro, True, SHARED_TEX)
    _save('TS_Atlas_Metallic', me, True, SHARED_TEX); _save('TS_Atlas_MetallicSmoothness', ms, True, SHARED_TEX)
    # tire: U = circumference (texture repeats 4x around the wheel -> UV u spans 0..4), V = profile 0 (inner bead) .. 1 (outer bead); crown at v .5
    W_, H_ = 1024, 512; yy, xx = np.mgrid[0:H_, 0:W_]; v = yy / H_; u = xx / W_ * 6                       # 6 tread pitches per texture repeat (24 around)
    crown = np.abs(v - .5) < .21; shoulder = (np.abs(v - .5) >= .21) & (np.abs(v - .5) < .27)
    groove = np.zeros_like(v)
    for g in (-.12, -.04, .04, .12): groove = np.maximum(groove, (np.abs(v - .5 - g) < .011).astype(float))
    lateral = ((np.abs(((u + (v - .5) * 1.6) % 1) - .5) < .10) & crown).astype(float)                   # angled lateral grooves -> tread blocks
    sipe = ((np.abs(((u * 3 + (v - .5) * 2) % 1) - .5) < .02) & crown & (groove == 0)).astype(float)
    shoulder_blk = (shoulder & (np.abs((u * 4 % 1) - .5) < .08)).astype(float)
    side = np.abs(v - .5) >= .27; ring = (np.abs(np.abs(v - .5) - .40) < .004).astype(float) + (np.abs(np.abs(v - .5) - .33) < .003).astype(float)
    letters = np.zeros_like(v); band = side & (np.abs(np.abs(v - .5) - .365) < .022)
    for k in range(10):                                                                                   # fictional raised lettering blocks (brand-less) on the sidewall band
        x0 = .05 + k * .085; letters[band & (xx / W_ > x0) & (xx / W_ < x0 + .05) & ((np.floor(xx / W_ * 160) % 3) != 1)] = 1
    hgt = .5 - .45 * groove * crown - .35 * lateral - .15 * sipe - .3 * shoulder_blk + .25 * ring + .2 * letters
    hgt = _blur(_blur(hgt, 3), 2)                                                                       # rounded block edges (depth, not hairlines)
    base = np.where(crown, .040, .026) + .006 * letters - .01 * groove * crown + (np.random.default_rng(7).random(v.shape) - .5) * .006
    rgh = np.where(crown, .80, .90) - .05 * letters
    _save('TS_Tire_BaseColor', L2S(np.dstack([base, base, base * 1.02])), False, SHARED_TEX); _save('TS_Tire_Normal', _normal(hgt, 22.0), True, SHARED_TEX)
    _save('TS_Tire_Roughness', np.dstack([rgh] * 3), True, SHARED_TEX)
    n = 256; flake = rng.random((n, n, 2)) - .5; f = np.dstack([.5 + flake[..., 0] * .35, .5 + flake[..., 1] * .35, np.ones((n, n))])   # metallic flake micro-normal (tiling)
    _save('TS_PaintFlake_Normal', f, True, SHARED_TEX)
    # lights: 4 x 4 cells of 64 px. off-state base colour, emission colour, channel id (R = id / 15)
    LB, LE, LI = np.zeros((256, 256, 3)), np.zeros((256, 256, 3)), np.zeros((256, 256, 3))
    for i, ch in enumerate(LIGHT_CELLS):
        r, c = divmod(i, 4); y0 = 256 - (r + 1) * 64; x0 = c * 64; off, on = LIGHT_COL[ch]
        LB[y0:y0 + 64, x0:x0 + 64] = L2S(np.array(off)); LE[y0:y0 + 64, x0:x0 + 64] = L2S(np.array(on)); LI[y0:y0 + 64, x0:x0 + 64] = i / 15.0
    _save('TS_Lights_BaseColor', LB, False, SHARED_TEX); _save('TS_Lights_Emission', LE, False, SHARED_TEX); _save('TS_Lights_ChannelID', LI, True, SHARED_TEX)
    return paths
LIGHT_CELLS = ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse', 'Marker']
LIGHT_COL = {'DRL': ((.55, .58, .62), (.82, .90, 1.0)), 'Headlamp': ((.60, .62, .65), (1.0, .97, .92)), 'Tail': ((.18, .0, .005), (1.0, .02, .02)), 'Brake': ((.20, .0, .005), (1.0, .01, .01)),
             'Indicator_L': ((.35, .14, .0), (1.0, .38, .0)), 'Indicator_R': ((.35, .14, .0), (1.0, .38, .0)), 'Reverse': ((.55, .56, .57), (1.0, 1.0, 1.0)), 'Marker': ((.35, .14, .0), (1.0, .38, .0))}
LIGHT_STRENGTH = {'DRL': 12, 'Headlamp': 4, 'Tail': 5, 'Brake': 2, 'Indicator_L': 1.2, 'Indicator_R': 1.2, 'Reverse': .5, 'Marker': 1.0}   # Blender review "parked, DRL + tail on" state
def light_cell_rect(ch):
    i = LIGHT_CELLS.index(ch); r, c = divmod(i, 4); return c * .25, 1 - (r + 1) * .25, .25
# ================================================================ materials (<= 8 slots at LOD0)
def _tex(nt, path, data, interp='Linear'):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(path, check_existing=True); n.interpolation = interp
    if data: n.image.colorspace_settings.name = 'Non-Color'
    return n
def build_library(tex, prefix, paint_rgb, body_tex=None):
    """TS materials. body_tex: dict(normal=, aomask=) per-vehicle baked maps (None during the bake stage). Returns {name: material}."""
    M = {}
    def new(name):
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled'); nt.links.new(b.outputs[0], out.inputs[0]); M[name] = m; return m, nt, b
    M.update(paint_material(prefix + '_Paint', paint_rgb, body_tex, tex))
    m, nt, b = new('TS_Atlas')
    c = _tex(nt, tex['TS_Atlas_BaseColor'], False); r = _tex(nt, tex['TS_Atlas_Roughness'], True); mt = _tex(nt, tex['TS_Atlas_Metallic'], True); n = _tex(nt, tex['TS_Atlas_Normal'], True); nmap = nt.nodes.new('ShaderNodeNormalMap')
    nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(r.outputs[0], b.inputs['Roughness']); nt.links.new(mt.outputs[0], b.inputs['Metallic']); nt.links.new(n.outputs[0], nmap.inputs['Color']); nt.links.new(nmap.outputs[0], b.inputs['Normal'])
    m, nt, b = new('TS_Tire')
    c = _tex(nt, tex['TS_Tire_BaseColor'], False); r = _tex(nt, tex['TS_Tire_Roughness'], True); n = _tex(nt, tex['TS_Tire_Normal'], True); nmap = nt.nodes.new('ShaderNodeNormalMap'); nmap.inputs['Strength'].default_value = 1.0
    nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(r.outputs[0], b.inputs['Roughness']); nt.links.new(n.outputs[0], nmap.inputs['Color']); nt.links.new(nmap.outputs[0], b.inputs['Normal'])
    for name, col, alpha, rough in (('TS_Glass', (.50, .58, .56), .35, .0), ('TS_Lens', (.92, .94, .96), .10, .01), ('TS_LensRed', (.42, .0, .006), .55, .02)):
        m, nt, b = new(name); b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['IOR'].default_value = 1.5
        b.inputs['Transmission Weight'].default_value = 1.0 if name != 'TS_LensRed' else .85; b.inputs['Alpha'].default_value = 1.0      # Cycles: physical transmission; Unity: alpha below
        m['unity_alpha'] = alpha
        if hasattr(m, 'surface_render_method'): m.surface_render_method = 'BLENDED'
        m.use_backface_culling = False
    m, nt, b = new('TS_Lights')
    c = _tex(nt, tex['TS_Lights_BaseColor'], False, 'Closest'); e = _tex(nt, tex['TS_Lights_Emission'], False, 'Closest')
    nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(e.outputs[0], b.inputs['Emission Color']); b.inputs['Roughness'].default_value = .25
    st = _state_mask(os.environ.get('TS_LIGHTS', 'DRL,Tail')); sm = nt.nodes.new('ShaderNodeTexImage'); sm.image = st; sm.interpolation = 'Closest'
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs['Factor'].default_value = 1.0
    nt.links.new(e.outputs[0], mul.inputs['A']); nt.links.new(sm.outputs[0], mul.inputs['B']); nt.links.new(mul.outputs['Result'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = float(os.environ.get('TS_LIGHT_STRENGTH', 6.0))
    m['unity'] = 'one emissive material; channel = TS_Lights_ChannelID (R * 15 = index into DRL, Headlamp, Tail, Brake, Indicator_L, Indicator_R, Reverse, Marker); per-channel intensity array set at runtime (one draw call)'
    return M
def _state_mask(on):
    """Blender review only: which channels glow (default daytime driving: DRL + tail). Unity drives this at runtime."""
    on = {x.strip() for x in on.split(',') if x.strip()}; im = bpy.data.images.get('TS_Lights_State') or bpy.data.images.new('TS_Lights_State', 4, 4)
    px = []
    for r in range(3, -1, -1):
        for c in range(4):
            i = r * 4 + c; v = 1.0 if i < len(LIGHT_CELLS) and LIGHT_CELLS[i] in on else 0.0; px += [v, v, v, 1]
    im.pixels.foreach_set(px); im.pack(); return im
def paint_material(name, rgb, body_tex, tex, finish=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled'); nt.links.new(b.outputs[0], out.inputs[0])
    col = nt.nodes.new('ShaderNodeRGB'); col.label = 'PaintColour'; col.outputs[0].default_value = (*rgb, 1)
    F_ = dict(metallic=.55, roughness=.36, coat=1.0, coat_rough=.045); F_.update(finish or {})                  # finish: per-vehicle override (commercial solid paint)
    b.inputs['Metallic'].default_value = F_['metallic']; b.inputs['Roughness'].default_value = F_['roughness']; b.inputs['Coat Weight'].default_value = F_['coat']; b.inputs['Coat Roughness'].default_value = F_['coat_rough']; b.inputs['Coat IOR'].default_value = 1.5
    if body_tex:
        n = _tex(nt, body_tex['normal'], True); nmap = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(n.outputs[0], nmap.inputs['Color'])
        nt.links.new(nmap.outputs[0], b.inputs['Normal']); nt.links.new(nmap.outputs[0], b.inputs['Coat Normal'])
        if body_tex.get('aomask'):
            a = _tex(nt, body_tex['aomask'], True); sep = nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(a.outputs[0], sep.inputs[0])
            grime = nt.nodes.new('ShaderNodeMix'); grime.data_type = 'RGBA'; grime.inputs['B'].default_value = (.11, .10, .085, 1)          # restrained road grime colour
            gm = nt.nodes.new('ShaderNodeMath'); gm.operation = 'MULTIPLY'; gm.inputs[1].default_value = .55
            nt.links.new(sep.outputs['Green'], gm.inputs[0]); nt.links.new(gm.outputs[0], grime.inputs['Factor']); nt.links.new(col.outputs[0], grime.inputs['A'])
            ao = nt.nodes.new('ShaderNodeMix'); ao.data_type = 'RGBA'; ao.blend_type = 'MULTIPLY'; ao.inputs['Factor'].default_value = 1.0
            nt.links.new(grime.outputs['Result'], ao.inputs['A']); nt.links.new(sep.outputs['Red'], ao.inputs['B']); nt.links.new(ao.outputs['Result'], b.inputs['Base Color'])
            rgh = nt.nodes.new('ShaderNodeMath'); rgh.operation = 'MULTIPLY_ADD'; rgh.inputs[1].default_value = .30; rgh.inputs[2].default_value = F_['coat_rough']
            nt.links.new(sep.outputs['Green'], rgh.inputs[0]); nt.links.new(rgh.outputs[0], b.inputs['Coat Roughness'])                  # grime dulls the clear coat slightly
        else: nt.links.new(col.outputs[0], b.inputs['Base Color'])
    else: nt.links.new(col.outputs[0], b.inputs['Base Color'])
    m['unity'] = f"Lit (or clear-coat paint shader): BaseColor = PaintColour x AO (R of AO_Grime) blended to grime (G); Normal = baked body normal; detail normal TS_PaintFlake_Normal tiling 60; metallic {F_['metallic']:.2f}, smoothness {1 - F_['roughness']:.2f}, clear coat {F_['coat']:.2f} / coat smoothness {1 - F_['coat_rough']:.3f}"
    return {name: m}
# ================================================================ geometry helpers
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
    def cap(s, ring, t, centre=None, flip=False):
        n0 = len(s.V); s.V += [tuple(p) for p in ring]; c = centre if centre is not None else sum((Vector(p) for p in ring), Vector()) / len(ring); s.V.append(tuple(c)); n = len(ring)
        for i in range(n): f = (n0 + i, n0 + (i + 1) % n, n0 + n); s.F.append(f[::-1] if flip else f); s.T.append(t)
    def rbox(s, c, half, t, bev=.02, rot=None, seg=1):
        hx, hy, hz = half; R = rot or Matrix.Identity(3)
        bmx = bmesh.new(); bmesh.ops.create_cube(bmx, size=1.0); bmesh.ops.scale(bmx, vec=(2 * hx, 2 * hy, 2 * hz), verts=bmx.verts)
        if bev > 0: bmesh.ops.bevel(bmx, geom=list(bmx.edges), offset=min(bev, hx * .9, hy * .9, hz * .9), segments=seg, affect='EDGES', profile=.5)
        for v in bmx.verts: v.co = R @ v.co + Vector(c)
        s.add([tuple(v.co) for v in bmx.verts], [tuple(v.index for v in f.verts) for f in bmx.faces], t); bmx.free()
def revolve(profile, seg, x_sign, a0=0.0):
    """profile (axial offset, radius) revolved about +X; returns V, F, per-vertex (u, v)."""
    Vs, Fs, UV = [], [], []; n = len(profile)
    for k in range(seg + 1):
        a = a0 + 2 * math.pi * k / seg
        for i, (dx, r) in enumerate(profile): Vs.append((x_sign * dx, r * math.cos(a), r * math.sin(a))); UV.append((k / seg, i / (n - 1)))
    for k in range(seg):
        for i in range(n - 1):
            a_, b_ = k * n + i, k * n + i + 1; c_, d_ = (k + 1) * n + i + 1, (k + 1) * n + i
            Fs.append((a_, d_, c_, b_) if x_sign > 0 else (a_, b_, c_, d_))
    return Vs, Fs, UV
def mk(name, V, F, FM, coll_, mats):
    """mesh from per-face tags: 'TS_Atlas:<cell>', 'TS_Lights:<channel>' or a material name."""
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in V], [], [tuple(f) for f in F]); me.update()
    base = [t.split(':')[0] for t in FM]; order = list(dict.fromkeys(base))
    for m in order: me.materials.append(mats[m])
    me.polygons.foreach_set('material_index', [order.index(m) for m in base])
    a = me.attributes.new('cell', 'INT', 'FACE'); a.data.foreach_set('value', [cell_index(t) for t in FM]); me.update()
    o = bpy.data.objects.new(name, me); coll_.objects.link(o); return o
def cell_index(tag):
    if ':' not in tag: return -1
    m, c = tag.split(':'); return CELLS.index(c) if m == 'TS_Atlas' else 100 + LIGHT_CELLS.index(c)
def atlas_uvs(o, keep=('UVMap',), tire_layer='tireUV'):
    """UV0 'UVMap' for atlas / lights / tire faces (paint faces keep their unique unwrap if present).
    Atlas faces: box projection normalised into the face-group's cell (inset 6 %), so cell textures never wrap; lights: cell centre region; tire: revolve UVs."""
    me = o.data
    if not me.polygons: return
    uv = me.uv_layers.get('UVMap') or me.uv_layers.new(name='UVMap'); me.uv_layers.active = uv
    tire = me.uv_layers.get(tire_layer); tuv = [tuple(d.uv) for d in tire.data] if tire else None
    cell = me.attributes.get('cell'); mats = [m.name if m else '' for m in me.materials]
    groups = {}
    for p in me.polygons:
        nm = mats[p.material_index]; c = cell.data[p.index].value if cell else -1
        if nm == 'TS_Atlas' and c >= 0: groups.setdefault(c, []).append(p)
    STRETCH = {CELLS.index('plate'), CELLS.index('badge'), CELLS.index('mirror_glass')}                # decals fill their cell (per-axis stretch, upright)
    for c in [c for c in list(groups) if c in STRETCH]:                                                  # decals: one UV frame per connected island (front + rear plate each fill the cell)
        polys = groups.pop(c); left = {p.index: p for p in polys}; isl = 0
        while left:
            seed = left.pop(next(iter(left))); comp = [seed]; vset = set(seed.vertices); grew = True
            while grew:
                grew = False
                for k_, p_ in list(left.items()):
                    if vset & set(p_.vertices): comp.append(left.pop(k_)); vset |= set(p_.vertices); grew = True
            groups[(c, isl)] = comp; isl += 1
    for c, polys in groups.items():
        c = c[0] if isinstance(c, tuple) else c
        vs = [me.vertices[i].co for p in polys for i in p.vertices]; mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs))); mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
        ext = max(max(mx - mn), 1e-6); u0, v0, sz = cell_rect(CELLS[c]); pad = sz * .06; span = sz - 2 * pad
        for p in polys:
            ax = max(range(3), key=lambda k: abs(p.normal[k])); i1, i2 = [(1, 2), (0, 2), (0, 1)][ax]
            for li in p.loop_indices:
                co = me.vertices[me.loops[li].vertex_index].co - mn
                if c in STRETCH:                                                                            # x across (mirrored on rear-facing decals), z up
                    e1 = max(mx[0] - mn[0], 1e-6); e2 = max(mx[2] - mn[2], 1e-6); fu = co[0] / e1
                    if p.normal.y > 0: fu = 1 - fu
                    uv.data[li].uv = (u0 + sz * (.02 + .96 * fu), v0 + sz * (.02 + .96 * co[2] / e2))
                else: uv.data[li].uv = (u0 + pad + span * co[i1] / ext, v0 + pad + span * co[i2] / ext)
    for p in me.polygons:
        nm = mats[p.material_index]; c = cell.data[p.index].value if cell else -1
        if nm == 'TS_Lights' and c >= 100:
            u0, v0, sz = light_cell_rect(LIGHT_CELLS[c - 100])
            for k, li in enumerate(p.loop_indices): uv.data[li].uv = (u0 + sz * (.3 + .4 * (k % 2)), v0 + sz * (.3 + .4 * ((k // 2) % 2)))
        elif nm == 'TS_Tire' and tuv:
            for li in p.loop_indices: uv.data[li].uv = (tuv[li][0] * 4, tuv[li][1])                        # tire texture repeats 4x around
        elif nm in ('TS_Glass', 'TS_Lens', 'TS_LensRed'):
            for li in p.loop_indices: uv.data[li].uv = (.5, .5)
    for l in list(me.uv_layers):
        if l.name != 'UVMap': me.uv_layers.remove(l)
def clean(o):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    seen, dups = set(), []
    for f in bm.faces:
        k = frozenset(v.index for v in f.verts); (dups.append(f) if k in seen else seen.add(k))
    bmesh.ops.delete(bm, geom=dups, context='FACES_ONLY'); bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=1e-5)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_area() < 2e-9], context='FACES_ONLY')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bm.to_mesh(o.data); bm.free(); o.data.update()
def purge_slots(o):
    me = o.data; used = sorted({p.material_index for p in me.polygons}); mats = [me.materials[i] for i in used]; remap = {i: k for k, i in enumerate(used)}
    idx = [remap[p.material_index] for p in me.polygons]; me.materials.clear()
    for m in mats: me.materials.append(m)
    me.polygons.foreach_set('material_index', idx); me.update()
def tris(o): return sum(len(p.vertices) - 2 for p in o.data.polygons)
def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if not c: c = bpy.data.collections.new(name); (parent or bpy.context.scene.collection).children.link(c)
    return c
def link_only(o, c):
    for x in list(o.users_collection): x.objects.unlink(o)
    c.objects.link(o)
def join(objs, name, c):
    objs = [o for o in objs if o and o.type == 'MESH']
    for o in objs: link_only(o, c)
    a = objs[0]
    if len(objs) > 1:
        with bpy.context.temp_override(active_object=a, object=a, selected_objects=objs, selected_editable_objects=objs): bpy.ops.object.join()
    a.name = name; a.data.name = name; return a
def set_origin(o, p):
    p = Vector(p); o.data.transform(Matrix.Translation(-p)); o.matrix_world = Matrix.Translation(p)
def empty(name, c, loc=(0, 0, 0), parent=None, kind='PLAIN_AXES', size=.25):
    e = bpy.data.objects.new(name, None); e.empty_display_type = kind; e.empty_display_size = size; c.objects.link(e)
    if parent: e.parent = parent
    e.location = loc; return e
def orient_out(o, centre=(0, 0, .55)):
    """consistent winding per connected component, flipped outward (away from a centre) when the component's area-weighted normal points inward."""
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.faces.ensure_lookup_table(); seen = set(); C = Vector(centre)
    for f0 in bm.faces:
        if f0.index in seen: continue
        comp = []; st = [f0]
        while st:
            f = st.pop()
            if f.index in seen: continue
            seen.add(f.index); comp.append(f); st += [g for e in f.edges for g in e.link_faces if g.index not in seen]
        score = sum(f.normal.dot((f.calc_center_median() - C).normalized()) * f.calc_area() for f in comp)
        if score < 0:
            for f in comp: f.normal_flip()
    bm.to_mesh(o.data); bm.free(); o.data.update()
