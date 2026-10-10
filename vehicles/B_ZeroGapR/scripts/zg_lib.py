# Zero Gap R (Phase B) — shared library. Source: racing_car_09 (read-only). Convention: +Z up, nose -Y, vehicle left +X, 1 BU = 1 m.
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, re, json, math, zlib
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
WS = '/Users/meetshah/Documents/blender'; ROOT = WS + '/vehicles/B_ZeroGapR'; P = lambda *a: os.path.join(ROOT, *a)
SRC = WS + '/racing_car_09_unity_export_ready.blend'
P0_BLEND = WS + '/environment/P0_RoadFoundation/blend/road_05_export_ready.blend'
HYPER = WS + '/new_car/hypercar_08_unity_export.blend'
SCR = os.environ.get('ZG_SCRATCH')
def CKP(n):
    d = SCR or P('blend'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def EXP(n):
    d = os.path.join(SCR, 'exports') if SCR else P('exports'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def TEX(n):
    d = os.path.join(SCR, 'textures') if SCR else P('textures'); os.makedirs(d, exist_ok=True); return os.path.join(d, n)
def save_ckp(name):
    path = CKP(name); assert SCR or not os.path.exists(path), 'checkpoint exists: ' + path
    bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=path, copy=True, relative_remap=True); print('SAVED', path, flush=True)
def ss(a, b, x): t = min(1.0, max(0.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t
def tris(o):
    me = o.data; return sum(len(p.vertices) - 2 for p in me.polygons)
def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if not c: c = bpy.data.collections.new(name); (parent or bpy.context.scene.collection).children.link(c)
    return c
def link_only(o, c):
    for x in list(o.users_collection): x.objects.unlink(o)
    c.objects.link(o)
def empty(name, c, loc=(0, 0, 0), parent=None, kind='PLAIN_AXES', size=.25):
    e = bpy.data.objects.new(name, None); e.empty_display_type = kind; e.empty_display_size = size; c.objects.link(e)
    if parent: e.parent = parent
    e.location = loc; return e

# ---------------------------------------------------------------- materials
LIGHTS = ['ZG_LED_DRL', 'ZG_LED_Headlamp', 'ZG_LED_Tail', 'ZG_LED_Brake', 'ZG_LED_Indicator_L', 'ZG_LED_Indicator_R', 'ZG_LED_Reverse']
MATS = ['ZG_Paint', 'ZG_Palette', 'ZG_Carbon', 'ZG_Tire', 'ZG_Glass', 'ZG_LensClear', 'ZG_LensRed', 'ZG_Display'] + LIGHTS
EMIT = {'ZG_LED_DRL': ((.80, .90, 1.0), 9.0), 'ZG_LED_Headlamp': ((.95, .97, 1.0), 2.5), 'ZG_LED_Tail': ((1.0, .015, .02), 7.0), 'ZG_LED_Brake': ((1.0, .01, .015), 1.2),
        'ZG_LED_Indicator_L': ((1.0, .32, .0), .6), 'ZG_LED_Indicator_R': ((1.0, .32, .0), .6), 'ZG_LED_Reverse': ((1.0, 1.0, 1.0), .25), 'ZG_Display': ((.10, .35, .60), 1.4)}
# palette swatches: name -> (source material whose textures give the average colour, or explicit linear rgb), metallic, roughness
SWATCH = ['black_plastic', 'gloss_black', 'housing', 'chrome', 'brushed', 'wheel_metal', 'wheel_dark', 'caliper', 'rotor', 'leather', 'alcantara', 'int_plastic', 'int_metal',
          'seat_accent', 'speaker', 'mirror', 'grille', 'exhaust_inner', 'reflector']
SRC2SW = {'MAT_BlackPlastic_Engine': 'black_plastic', 'MAT_HeadlightHousing_Engine': 'housing', 'MAT_Chrome_Engine': 'chrome', 'MAT_BrushedMetal_Engine': 'brushed',
          'MAT_WheelMetal_Engine': 'wheel_metal', 'MAT_WheelDark_Engine': 'wheel_dark', 'MAT_BrakeCaliper_Engine': 'caliper', 'MAT_BrakeDisc_Engine': 'rotor',
          'MAT_InteriorLeather_LOD_Detail_Engine': 'leather', 'MAT_InteriorAlcantara_LOD_Detail_Engine': 'alcantara', 'MAT_InteriorPlastic_LOD_Detail_Engine': 'int_plastic',
          'MAT_InteriorMetal_LOD_Detail_Engine': 'int_metal', 'MAT_SeatAccent_LOD_Detail_Engine': 'seat_accent', 'MAT_Speaker_LOD_Detail_Engine': 'speaker', 'MAT_InteriorMirror_LOD_Detail_Engine': 'mirror'}
SRC2MAT = {'MAT_CarPaint_BrightRed': 'ZG_Paint', 'MAT_CarbonFiber_Engine': 'ZG_Carbon', 'MAT_InteriorCarbon_LOD_Detail_Engine': 'ZG_Carbon', 'MAT_Glass_LOD_Thin_Engine': 'ZG_Glass',
           'MAT_HeadlightLens_Engine': 'ZG_LensClear', 'MAT_ProjectorLens_Engine': 'ZG_LensClear', 'MAT_TaillightLens_Engine': 'ZG_LensRed', 'MAT_Display_LOD_Detail_Engine': 'ZG_Display',
           'MAT_Tire_LOD_Detail_Engine': 'ZG_Tire', 'MAT_EmissiveRed_Engine': 'ZG_LED_Tail', 'MAT_EmissiveAmber_Engine': 'ZG_LED_Indicator_L', 'MAT_EmissiveWhite_Engine': 'ZG_LED_DRL'}
GRID, CELL = 8, 32                                                                              # 8 x 8 swatch grid, 32 px cells -> 256 px palette
def swatch_uv(name):
    i = SWATCH.index(name); return ((i % GRID) + .5) / GRID, 1 - ((i // GRID) + .5) / GRID
def s2l(c): return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
def fresh(img):
    """independent, loaded copy of a source image (source images load lazily)."""
    im = bpy.data.images.load(bpy.path.abspath(img.filepath, library=img.library), check_existing=False); im.pixels[0]; return im
def img_mean(img, srgb):
    im = fresh(img); im.scale(32, 32); a = np.array(im.pixels[:], np.float32).reshape(-1, 4)[:, :3].mean(0); bpy.data.images.remove(im)
    return [s2l(float(v)) for v in a] if srgb else [float(v) for v in a]
def measure_source_swatches():
    """average colour / roughness / metallic of each source material (from its BaseColor + ORM textures, or its constant inputs)."""
    out = {}
    for src, sw in SRC2SW.items():
        m = bpy.data.materials.get(src)
        if not m: continue
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None); base, rough, metal = None, None, None
        for n in m.node_tree.nodes:
            if n.type != 'TEX_IMAGE' or not n.image: continue
            nm = n.image.name
            if 'BaseColor' in nm: base = img_mean(n.image, True)
            elif 'ORM' in nm: orm = img_mean(n.image, False); rough, metal = orm[1], orm[2]
        if base is None and b and not b.inputs['Base Color'].is_linked: base = list(b.inputs['Base Color'].default_value)[:3]
        if rough is None and b and not b.inputs['Roughness'].is_linked: rough = b.inputs['Roughness'].default_value
        if metal is None and b and not b.inputs['Metallic'].is_linked: metal = b.inputs['Metallic'].default_value
        out[sw] = dict(base=base or [.05, .05, .05], rough=.5 if rough is None else rough, metal=0.0 if metal is None else metal)
    out['gloss_black'] = dict(base=[.012, .012, .013], rough=.12, metal=0.0)                   # blacked-out pillars / bezels
    out['grille'] = dict(base=[.018, .018, .02], rough=.55, metal=.1)
    out['exhaust_inner'] = dict(base=[.035, .028, .022], rough=.7, metal=.6)
    out['reflector'] = dict(base=[.55, .55, .56], rough=.18, metal=1.0)
    out['mirror'] = dict(base=[.68, .72, .76], rough=.04, metal=1.0)
    for k in SWATCH: out.setdefault(k, dict(base=[.05, .05, .05], rough=.5, metal=0.0))
    return out
def write_palette(sw):
    N = GRID * CELL; bc = np.zeros((N, N, 4), np.float32); mr = np.zeros((N, N, 4), np.float32); ro = np.zeros((N, N, 4), np.float32); me = np.zeros((N, N, 4), np.float32)
    l2s = lambda c: 12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055
    for i, k in enumerate(SWATCH):
        r, c = divmod(i, GRID); y0 = N - (r + 1) * CELL; x0 = c * CELL; d = sw[k]
        bc[y0:y0 + CELL, x0:x0 + CELL] = [*(l2s(v) for v in d['base']), 1]; mr[y0:y0 + CELL, x0:x0 + CELL] = [d['metal'], 0, 0, 1 - d['rough']]
        ro[y0:y0 + CELL, x0:x0 + CELL] = [d['rough']] * 3 + [1]; me[y0:y0 + CELL, x0:x0 + CELL] = [d['metal']] * 3 + [1]
    paths = {}
    for nm, a, data in (('ZG_Palette_BaseColor', bc, False), ('ZG_Palette_MetallicSmoothness', mr, True), ('ZG_Palette_Roughness', ro, True), ('ZG_Palette_Metallic', me, True)):
        im = bpy.data.images.new(nm, N, N, alpha=True); im.pixels.foreach_set(a.ravel())
        if data: im.colorspace_settings.name = 'Non-Color'
        p = TEX(nm + '.png'); im.filepath_raw = p; im.file_format = 'PNG'; im.save(); paths[nm] = p
    return paths
def resave(img, name, size, data):
    im = fresh(img); im.scale(size, size); px = np.array(im.pixels[:], np.float32); bpy.data.images.remove(im)
    out = bpy.data.images.new(name, size, size, alpha=True)
    if data: out.colorspace_settings.name = 'Non-Color'
    out.pixels.foreach_set(px); p = TEX(name + '.png'); out.filepath_raw = p; out.file_format = 'PNG'; out.save(); bpy.data.images.remove(out); return p
def _img(nt, path, data, closest=False):
    n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(path, check_existing=True)
    if data: n.image.colorspace_settings.name = 'Non-Color'
    if closest: n.interpolation = 'Closest'
    return n
def build_materials(sw, tex):
    """15 engine materials. Opaque flat parts share ZG_Palette (one draw call); light channels are separate so Unity can drive them independently."""
    M = {}
    for name in MATS:
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled'); nt.links.new(b.outputs[0], out.inputs[0]); M[name] = m
        if name == 'ZG_Paint':
            b.inputs['Base Color'].default_value = (*sw['paint'], 1); b.inputs['Metallic'].default_value = .55; b.inputs['Roughness'].default_value = .28
            b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = .03
            m['unity'] = 'car paint (clear coat). Colour is runtime-swappable; no texture.'
        elif name == 'ZG_Palette':
            c = _img(nt, tex['ZG_Palette_BaseColor'], False, True); r = _img(nt, tex['ZG_Palette_Roughness'], True, True); mt = _img(nt, tex['ZG_Palette_Metallic'], True, True)
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(r.outputs[0], b.inputs['Roughness']); nt.links.new(mt.outputs[0], b.inputs['Metallic'])
            m['unity'] = 'Lit opaque; BaseMap ZG_Palette_BaseColor, MetallicGloss ZG_Palette_MetallicSmoothness (R metal, A smoothness); point filtering or no mips recommended'
        elif name == 'ZG_Carbon':
            c = _img(nt, tex['ZG_Carbon_BaseColor'], False); n = _img(nt, tex['ZG_Carbon_Normal'], True); nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = .6
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(n.outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], b.inputs['Normal'])
            b.inputs['Roughness'].default_value = .3; b.inputs['Coat Weight'].default_value = .6
        elif name == 'ZG_Tire':
            c = _img(nt, tex['ZG_Tire_BaseColor'], False); n = _img(nt, tex['ZG_Tire_Normal'], True); nm = nt.nodes.new('ShaderNodeNormalMap')
            nt.links.new(c.outputs[0], b.inputs['Base Color']); nt.links.new(n.outputs[0], nm.inputs['Color']); nt.links.new(nm.outputs[0], b.inputs['Normal']); b.inputs['Roughness'].default_value = .82
        elif name in ('ZG_Glass', 'ZG_LensClear', 'ZG_LensRed'):
            col, a = {'ZG_Glass': ((.015, .02, .025), .42), 'ZG_LensClear': ((.85, .88, .9), .12), 'ZG_LensRed': ((.22, .004, .008), .55)}[name]
            b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = .02; b.inputs['Alpha'].default_value = a; b.inputs['Coat Weight'].default_value = .3
            if hasattr(m, 'surface_render_method'): m.surface_render_method = 'BLENDED'
            m.use_backface_culling = False; m['unity'] = f'Lit transparent, alpha {a}, smoothness 0.98 (thin single sheet; no refraction)'
        elif name in EMIT:
            col, st = EMIT[name]; b.inputs['Base Color'].default_value = (*[c * .6 for c in col], 1); b.inputs['Roughness'].default_value = .3
            b.inputs['Emission Color'].default_value = (*col, 1); b.inputs['Emission Strength'].default_value = st
            m['unity'] = f'Lit opaque + emission {col} x{st} (runtime channel; drive _EmissionColor intensity)'
    return M

# ---------------------------------------------------------------- geometry helpers
def mk(name, V, F, FM, c, mats):
    """mesh from verts / faces / per-face material names ('ZG_Palette:<swatch>' sets the palette swatch)."""
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in V], [], [tuple(f) for f in F]); me.update()
    base = [m.split(':')[0] for m in FM]; order = list(dict.fromkeys(base))
    for m in order: me.materials.append(mats[m])
    me.polygons.foreach_set('material_index', [order.index(m) for m in base])
    a = me.attributes.new('swatch', 'INT', 'FACE'); a.data.foreach_set('value', [SWATCH.index(m.split(':')[1]) if ':' in m else 0 for m in FM]); me.update()
    o = bpy.data.objects.new(name, me); c.objects.link(o); return o
class Geo:
    def __init__(s): s.V, s.F, s.FM = [], [], []
    def quad_strip(s, A, B, mat, closed=False, flip=False):
        """faces between two equal-length point rows A and B."""
        n0 = len(s.V); s.V += [tuple(p) for p in A] + [tuple(p) for p in B]; n = len(A)
        for i in range(n - (0 if closed else 1)):
            j = (i + 1) % n; f = (n0 + i, n0 + j, n0 + n + j, n0 + n + i); s.F.append(f[::-1] if flip else f); s.FM.append(mat)
    def grid(s, rows, mat, flip=False):
        n0 = len(s.V); nr, nc = len(rows), len(rows[0])
        for r in rows: s.V += [tuple(p) for p in r]
        for i in range(nr - 1):
            for j in range(nc - 1):
                f = (n0 + i * nc + j, n0 + i * nc + j + 1, n0 + (i + 1) * nc + j + 1, n0 + (i + 1) * nc + j); s.F.append(f[::-1] if flip else f); s.FM.append(mat)
    def fan(s, ring, centre, mat, flip=False):
        n0 = len(s.V); s.V += [tuple(p) for p in ring] + [tuple(centre)]; n = len(ring)
        for i in range(n):
            f = (n0 + i, n0 + (i + 1) % n, n0 + n); s.F.append(f[::-1] if flip else f); s.FM.append(mat)
def rounded_poly(pts, r, seg=5):
    """closed 2D polygon with rounded corners (radius r, or per-corner list)."""
    out = []; n = len(pts); rs = r if isinstance(r, (list, tuple)) else [r] * n
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n]); d1 = (p0 - p1).normalized(); d2 = (p2 - p1).normalized()
        rr = min(rs[i], (p0 - p1).length * .45, (p2 - p1).length * .45); a = p1 + d1 * rr; b = p1 + d2 * rr
        for k in range(seg + 1):
            t = k / seg; q = (1 - t) ** 2 * a + 2 * (1 - t) * t * p1 + t * t * b; out.append((q.x, q.y))
    return out
def resample(pts, step, closed=True):
    P_ = [Vector(p) for p in pts] + ([Vector(pts[0])] if closed else []); L = [0.0]
    for a, b in zip(P_, P_[1:]): L.append(L[-1] + (b - a).length)
    n = max(4, int(L[-1] / step)); out = []
    for k in range(n if closed else n + 1):
        t = L[-1] * k / n; i = max(0, min(len(L) - 2, next((j for j in range(len(L) - 1) if L[j + 1] >= t), len(L) - 2))); seg = L[i + 1] - L[i]
        out.append(tuple(P_[i].lerp(P_[i + 1], 0 if seg < 1e-12 else (t - L[i]) / seg)))
    return out
def offset2d(poly, d):
    n = len(poly); out = []; area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n)); sgn = 1 if area > 0 else -1
    for i in range(n):
        p0, p1, p2 = Vector(poly[i - 1]), Vector(poly[i]), Vector(poly[(i + 1) % n]); e1 = (p1 - p0).normalized(); e2 = (p2 - p1).normalized()
        n1 = Vector((e1.y, -e1.x)) * sgn; n2 = Vector((e2.y, -e2.x)) * sgn; nn = (n1 + n2); nn = nn.normalized() if nn.length > 1e-9 else n1
        out.append(tuple(p1 + nn * d / max(.35, nn.dot(n1))))
    return out
def inside(poly, x, y):
    c = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1: c = not c
    return c
class Surf:
    """ray-projection onto a fascia surface: (x, z) -> surface point + outward normal, rays along -Y (front, out = -Y) or +Y (rear)."""
    def __init__(s, obj, front):
        bm = bmesh.new(); bm.from_mesh(obj.data); bm.transform(obj.matrix_world); s.bvh = BVHTree.FromBMesh(bm); bm.free(); s.front = front
    def at(s, x, z, off=0.0):
        o = Vector((x, -4.0 if s.front else 4.0, z)); d = Vector((0, 1 if s.front else -1, 0))
        loc, nrm, i, dist = s.bvh.ray_cast(o, d)
        if loc is None: return None, None
        out = Vector((0, -1 if s.front else 1, 0))
        if nrm.dot(out) < 0: nrm = -nrm
        return loc + nrm * off, nrm
def ribbon(g, surf, x0, x1, zb, zt, off, mat, nx=24, nz=3, wall=0.0, wall_mat=None):
    """surface-conforming patch over x in [x0, x1], z from zb(x) to zt(x), lifted `off` along the normal; optional side walls down to the surface."""
    rows = []; flip = None
    for k in range(nz + 1):
        row = []
        for i in range(nx + 1):
            x = lerp(x0, x1, i / nx); z = lerp(zb(x), zt(x), k / nz); p, n = surf.at(x, z, off); row.append(p)
        rows.append(row)
    if any(p is None for r in rows for p in r): return False
    # orientation: first face normal must point outward
    a, b, c = Vector(rows[0][0]), Vector(rows[0][1]), Vector(rows[1][0]); fn = (b - a).cross(c - a); flip = (fn.y > 0) if surf.front else (fn.y < 0)
    g.grid(rows, mat, flip)
    if wall > 0:
        ring = rows[0] + [rows[k][-1] for k in range(1, nz + 1)] + rows[-1][::-1][1:] + [rows[k][0] for k in range(nz - 1, 0, -1)]
        base = []
        for p in ring:
            q = Vector(p); _, n = surf.at(q.x, q.z, 0); base.append(q - n * off)
        g.quad_strip(ring, base, wall_mat or mat, closed=True, flip=not flip)
    return True
def opening(g, surf, poly, depth, rim_w, mats, back='fan', grille=None):
    """recessed opening: gloss bezel ring on the surface, tunnel walls going in, back plate. Returns the expanded outline used to cut the skin."""
    inner = resample(poly, .012); outer = offset2d(inner, rim_w); dirin = Vector((0, 1 if surf.front else -1, 0))
    I = [surf.at(x, z, .0015)[0] for x, z in inner]; O = [surf.at(x, z, .0015)[0] for x, z in outer]
    if any(p is None for p in I + O): return None
    area = sum(inner[i][0] * inner[(i + 1) % len(inner)][1] - inner[(i + 1) % len(inner)][0] * inner[i][1] for i in range(len(inner)))
    fl = (area > 0) == surf.front
    g.quad_strip(O, I, mats[0], closed=True, flip=fl)
    D = [Vector(p) + dirin * depth for p in I]; g.quad_strip(I, D, mats[1], closed=True, flip=fl)
    if back == 'fan':
        c = sum((Vector(p) for p in D), Vector()) / len(D); g.fan(D, c, mats[1], flip=not fl)
    return offset2d(inner, rim_w * .5)
def cut_skin(obj, polys):
    """delete skin faces whose centre (x, z) lies inside any cut outline."""
    bm = bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
    dead = [f for f in bm.faces if any(inside(p, f.calc_center_median().x, f.calc_center_median().z) for p in polys)]
    bmesh.ops.delete(bm, geom=dead, context='FACES'); bm.to_mesh(obj.data); bm.free(); obj.data.update()

# ---------------------------------------------------------------- fascia (Coons patch filling the body opening)
def body_opening(body, front):
    """ordered front / rear opening edge of the body shell's lower boundary loop -> (top curve L->R, left side top->bottom, right side top->bottom)."""
    bm = bmesh.new(); bm.from_mesh(body.data); bm.transform(body.matrix_world); bm.verts.ensure_lookup_table()
    adj = {}
    for e in bm.edges:
        if len(e.link_faces) == 1:
            a, b = e.verts; adj.setdefault(a.index, []).append(b.index); adj.setdefault(b.index, []).append(a.index)
    comps, seen = [], set()
    for s0 in adj:
        if s0 in seen: continue
        c = []; st = [s0]
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); c.append(x); st += adj[x]
        comps.append(c)
    big = max(comps, key=len); start = big[0]; order = [start]; prev = None
    while True:
        nx = [n for n in adj[order[-1]] if n != prev]
        if not nx or nx[0] == start or len(order) > len(big): break
        prev = order[-1]; order.append(nx[0])
    pts = [bm.verts[i].co.copy() for i in order]; bm.free()
    sel = [(p.y < -2.0) if front else (p.y > 2.04) for p in pts]
    # rotate so the selected run is contiguous
    k = next(i for i in range(len(pts)) if not sel[i] and sel[(i + 1) % len(pts)])
    run = []; i = (k + 1) % len(pts)
    while sel[i]: run.append(pts[i]); i = (i + 1) % len(pts)
    run = [p for p in run if p.z > .2]
    if run[0].x > run[-1].x: run.reverse()                                                    # left (-x) ... right (+x)
    half = len(run) // 2
    il = max(range(half), key=lambda j: run[j].z); ir = max(range(half, len(run)), key=lambda j: run[j].z)
    top = run[il:ir + 1]; left = run[:il + 1][::-1]; right = run[ir:]
    return top, left, right
def arclen_param(pts):
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + (b - a).length)
    return [l / L[-1] for l in L]
def curve_at(pts, prm, t):
    for j in range(len(prm) - 1):
        if prm[j + 1] >= t:
            s = (t - prm[j]) / max(1e-9, prm[j + 1] - prm[j]); return pts[j].lerp(pts[j + 1], s)
    return pts[-1].copy()
def fascia(body, front, NU, NV, chin_z, chin_y, bulge, c, mats, inset=.004):
    """skin that closes the body opening: top = body lip (tucked `inset` behind it -> shut line), sides = body opening edges, bottom = designed chin."""
    top, left, right = body_opening(body, front); sgn = -1 if front else 1
    tp, lp, rp = arclen_param(top), arclen_param(left), arclen_param(right)
    xe = right[-1].x; ze = right[-1].z; ye = right[-1].y
    def T(u): p = curve_at(top, tp, u); return p - Vector((0, sgn * inset, inset * .5))
    def SL(v): return curve_at(left, lp, v) - Vector((0, sgn * inset, 0))
    def SR(v): return curve_at(right, rp, v) - Vector((0, sgn * inset, 0))
    def Bm(u):
        x = lerp(left[-1].x, xe, u); a = abs(x) / abs(xe)
        return Vector((x, lerp(chin_y, ye, a ** 2.4) - sgn * inset, lerp(chin_z, ze, ss(.72, 1.0, a))))
    c00, c10, c01, c11 = T(0), T(1), Bm(0), Bm(1)
    rows = []
    for j in range(NV + 1):
        v = j / NV; row = []
        for i in range(NU + 1):
            u = i / NU
            p = (1 - v) * T(u) + v * Bm(u) + (1 - u) * SL(v) + u * SR(v) - ((1 - u) * (1 - v) * c00 + u * (1 - v) * c10 + (1 - u) * v * c01 + u * v * c11)
            p.y += sgn * bulge * math.sin(math.pi * v) ** 1.2 * (1 - abs(2 * u - 1) ** 4); row.append(p)
        rows.append(row)
    g = Geo(); a, b, d = rows[0][0], rows[0][1], rows[1][0]; fn = (b - a).cross(d - a); flip = (fn.y > 0) if front else (fn.y < 0)
    g.grid(rows, 'ZG_Paint', flip); o = mk(('Fascia_Front' if front else 'Fascia_Rear'), g.V, g.F, g.FM, c, mats)
    return o, rows

# ---------------------------------------------------------------- UVs
def box_uv(me, tile, layer='UVMap'):
    uv = me.uv_layers.get(layer) or me.uv_layers.new(name=layer)
    for p in me.polygons:
        ax = max(range(3), key=lambda k: abs(p.normal[k]))
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = ((co.y / tile, co.z / tile), (co.x / tile, co.z / tile), (co.x / tile, co.y / tile))[ax]
def final_uvs(o, carbon_tile):
    """single UV0 'UVMap': palette faces -> swatch centre, tire -> source atlas UV, carbon -> box UV at the carbon tile size, everything else box UV 1 m."""
    me = o.data
    if not me.polygons: return
    src = me.uv_layers.get('UVMap'); keep_tire = None
    if src is not None: keep_tire = [tuple(d.uv) for d in src.data]
    for l in list(me.uv_layers): me.uv_layers.remove(l)
    box_uv(me, 1.0); uv = me.uv_layers['UVMap']; carb = me.uv_layers.new(name='_c'); box_uv(me, carbon_tile, '_c'); cd = carb.data
    key = me.attributes.get('swatch')
    for p in me.polygons:
        m = me.materials[p.material_index] if p.material_index < len(me.materials) else None; nm = m.name if m else ''
        if nm == 'ZG_Palette':
            s_ = SWATCH[key.data[p.index].value] if key else 'black_plastic'; u, v = swatch_uv(s_)
            for li in p.loop_indices: uv.data[li].uv = (u, v)
        elif nm == 'ZG_Tire' and keep_tire:
            for li in p.loop_indices: uv.data[li].uv = keep_tire[li]
        elif nm == 'ZG_Carbon':
            for li in p.loop_indices: uv.data[li].uv = tuple(cd[li].uv)
    me.uv_layers.remove(me.uv_layers['_c'])
def set_swatch(o, name, faces=None):
    """face attribute 'swatch' (index into SWATCH) for palette faces."""
    me = o.data; a = me.attributes.get('swatch') or me.attributes.new('swatch', 'INT', 'FACE'); idx = SWATCH.index(name)
    for p in (me.polygons if faces is None else faces): a.data[p.index].value = idx
