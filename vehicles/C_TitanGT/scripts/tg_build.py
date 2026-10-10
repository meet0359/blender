# Titan GT (Phase C) production build. Blender -b --factory-startup --python tg_build.py [-- <last stage 2..8>]
# Starts from the APPROVED blockout design (identical design curves, tg_lib); writes titangt_02 .. 08 (never overwrites 01_blockout).
#  02 body panels (shell, arches, panel gaps, openings)  03 exterior details + lights  04 wheels / tires / brakes  05 interior
#  06 merge + materials + UVs + shading  07 LODs  08 colliders, hierarchy, pivots, references
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from tg_lib import *
LAST = int(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else 8
bpy.ops.wm.open_mainfile(filepath=P('blend', 'titangt_01_blockout.blend')); sc = bpy.context.scene; O = bpy.data.objects
BLOCKOUT_BODY = {k: v for k, v in (('dims', None),)}
for o in list(O): bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d): d.remove(x)
REPORT = {}
tex = make_textures(); M = build_materials(tex)
TMP = {}
def tmp(name):
    if name not in TMP: m = bpy.data.materials.new('TMP_' + name); m.diffuse_color = (.02, .02, .02, 1); TMP[name] = m
    return TMP[name]
MM = dict(M); MM.update({'TMP_' + k: tmp(k) for k in ('gloss_black', 'pocket', 'housing', 'satin_black', 'arch')})
WORK = coll('TG_WORK'); CUT = coll('TG_CUTTERS')
# ================================================================ 02 body shell
V0, F0, T0 = cage_mesh_data()
T0 = ['TG_Paint' if t == 'paint' else 'TG_Glass' if t == 'glass' else 'TMP_gloss_black' for t in T0]
def cage_obj(name):
    o = mk(name, V0, F0, T0, WORK, MM); bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); return o
def subdiv(o, lv):
    sm = o.modifiers.new('fair', 'LAPLACIANSMOOTH'); sm.lambda_factor = .5; sm.lambda_border = 0.0; sm.iterations = 14; sm.use_volume_preserve = True; sm.use_normalized = True   # fair the lofted cage (removes station ripples)
    m = o.modifiers.new('s', 'SUBSURF'); m.levels = m.render_levels = lv
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='fair')
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='s')
hi = cage_obj('REF_HiRes'); subdiv(hi, 3)
BVH = BVHTree.FromObject(hi, bpy.context.evaluated_depsgraph_get())
def ray(o, d):
    loc, nrm, i, dist = BVH.ray_cast(Vector(o), Vector(d))
    if loc is None: return None, None
    if nrm.dot(Vector(d)) > 0: nrm = -nrm
    return loc, nrm
fhit = lambda x, z: ray((x, -4, z), (0, 1, 0)); rhit = lambda x, z: ray((x, 4, z), (0, -1, 0))
shit = lambda sx, y, z: ray((sx * 3, y, z), (-sx, 0, 0)); thit = lambda x, y: ray((x, y, 3), (0, 0, -1))
body = cage_obj('Body_Shell'); subdiv(body, 2)
dm = body.modifiers.new('d', 'DECIMATE'); dm.decimate_type = 'COLLAPSE'; dm.ratio = .44; dm.use_symmetry = True; dm.symmetry_axis = 'X'; dm.use_collapse_triangulate = True   # curvature-adaptive density (silhouette, arches, nose) before cutting
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='d')
# ---- cutters
def solid(name, outer, inner, mat):
    """closed prism between two equal-length rings (outer outside the body, inner = pocket floor)."""
    bm = bmesh.new(); a = [bm.verts.new(p) for p in outer]; b = [bm.verts.new(p) for p in inner]; n = len(a)
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(n): j = (i + 1) % n; bm.faces.new((a[i], b[i], b[j], a[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bmesh.ops.triangulate(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_' + mat]); o = bpy.data.objects.new(name, me); CUT.objects.link(o); return o
def rounded(pts, r, seg=4):
    out = []; n = len(pts); rs = r if isinstance(r, (list, tuple)) else [r] * n
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n]); d1 = (p0 - p1).normalized(); d2 = (p2 - p1).normalized()
        rr = min(rs[i], (p0 - p1).length * .45, (p2 - p1).length * .45); a = p1 + d1 * rr; b = p1 + d2 * rr
        for k in range(seg + 1): t = k / seg; q = (1 - t) ** 2 * a + 2 * (1 - t) * t * p1 + t * t * b; out.append((q.x, q.y))
    return out
def front_pocket(name, poly, depth, mat, rear=False):
    hitf = rhit if rear else fhit; s = 1 if rear else -1; outer, inner = [], []
    for x, z in poly:
        p, n = hitf(x, z)
        if p is None: print('CUT MISS', name, x, z); return None
        outer.append((x, s * 3.5, z)); inner.append((p.x, p.y - s * depth, p.z))
    return solid(name, outer, inner, mat)
def side_pocket(name, poly, depth, mat, sx):
    outer, inner = [], []
    for y, z in poly:
        p, n = shit(sx, y, z)
        if p is None: print('CUT MISS', name, y, z); return None
        outer.append((sx * 2.0, y, z)); inner.append((p.x - sx * depth, p.y, p.z))
    return solid(name, outer, inner, mat)
def fence(name, pts_normals, w=.0045, d_in=.011, d_out=.02, mat='pocket'):
    """closed groove cutter along a closed loop on the surface (panel gap)."""
    n = len(pts_normals); bm = bmesh.new(); rings_ = []
    for i, (p, nr) in enumerate(pts_normals):
        q = pts_normals[(i + 1) % n][0]; r_ = pts_normals[i - 1][0]; tg = (q - r_).normalized(); b = tg.cross(nr).normalized()
        rings_.append([bm.verts.new(p + b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 - nr * d_in), bm.verts.new(p + b * w / 2 - nr * d_in)])
    for i in range(n):
        A, B = rings_[i], rings_[(i + 1) % n]
        for k in range(4): bm.faces.new((A[k], A[(k + 1) % 4], B[(k + 1) % 4], B[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_' + mat])
    o = bpy.data.objects.new(name, me); CUT.objects.link(o); return o
def loop_top(pts):
    out = []
    for x, y in pts:
        p, n = thit(x, y)
        if p is None: print('GAP MISS', x, y); continue
        out.append((p, n))
    return out
def loop_side(sx, pts):
    out = []
    for y, z in pts:
        p, n = shit(sx, y, z)
        if p is None: print('GAP MISS', y, z); continue
        out.append((p, n))
    return out
def sample_poly(poly, step=.02):
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        a, b = Vector(a), Vector(b); n = max(1, int((b - a).length / step))
        out += [tuple(a.lerp(b, k / n)) for k in range(n)]
    return out
# wheel arches
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    R_ = r + .052; seg = 64; zc = r + .012
    outer = [(sx * 1.4, y + R_ * math.cos(2 * math.pi * k / seg), zc + R_ * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    solid(f'arch_{y}_{sx}', outer, [(sx * .52, py, pz) for _, py, pz in outer], 'arch')
# panel gaps (hood, trunk, doors)
HOOD = [(x, y) for x, y in rounded([(.655, -.66), (.705, -1.40), (.60, -2.17), (-.60, -2.17), (-.705, -1.40), (-.655, -.66)], [.0, .3, .12, .12, .3, .0], 6)]
fence('gap_hood', loop_top(sample_poly(HOOD, .02)))
TRUNK = rounded([(.58, 1.42), (.62, 1.9), (.52, 2.31), (-.52, 2.31), (-.62, 1.9), (-.58, 1.42)], [.05, .2, .1, .1, .2, .05], 6)
fence('gap_trunk', loop_top(sample_poly(TRUNK, .02)))
for sx in (1, -1):
    DOOR = rounded([(-.90, .315), (.61, .315), (.63, ZBELT(.6) - .012), (-.88, ZBELT(-.9) - .015)], [.05, .05, .02, .02], 5)
    fence(f'gap_door_{sx}', loop_side(sx, sample_poly(DOOR, .02)))
    side_pocket(f'handle_{sx}', rounded([(.27, .748), (.44, .748), (.44, .772), (.27, .772)], .008, 3), .012, 'pocket', sx)
    side_pocket(f'vent_{sx}', rounded([(-.93, .505), (-.73, .505), (-.69, .655), (-.89, .655)], .02, 3), .032, 'pocket', sx)
# front openings
def grille_x(v): return lerp(.44, .54, v)
GZ0, GZ1 = .245, .495
GRILLE = rounded([(grille_x(0), GZ1), (-grille_x(0), GZ1), (-grille_x(1), GZ0), (grille_x(1), GZ0)], [.045, .045, .03, .03], 6)
front_pocket('grille', GRILLE, .095, 'pocket')
for sx in (1, -1):
    INT = rounded([(sx * .62, .36), (sx * .84, .39), (sx * .84, .24), (sx * .62, .21)], .025, 4)
    front_pocket(f'intake_{sx}', INT if sx > 0 else INT[::-1], .07, 'pocket')
    HL = rounded([(sx * .585, .525), (sx * .862, .575), (sx * .862, .672), (sx * .585, .600)], [.02, .03, .03, .02], 4)
    front_pocket(f'headlamp_{sx}', HL if sx > 0 else HL[::-1], .07, 'housing')
# rear light channel (full-width bar + C-shaped corners)
TL = [(.866, .857), (-.866, .857), (-.866, .728), (-.70, .728), (-.70, .833), (.70, .833), (.70, .728), (.866, .728)]
TL = rounded(TL, [.02, .02, .015, .01, .006, .006, .01, .015], 3)
front_pocket('taillight', TL, .05, 'housing', rear=True)
# boolean (all cutters in one exact boolean, cutter materials transferred to the new faces)
bm_ = body.modifiers.new('cuts', 'BOOLEAN'); bm_.operation = 'DIFFERENCE'; bm_.solver = 'EXACT'; bm_.operand_type = 'COLLECTION'; bm_.collection = CUT
if hasattr(bm_, 'material_mode'): bm_.material_mode = 'TRANSFER'
with bpy.context.temp_override(object=body, active_object=body): bpy.ops.object.modifier_apply(modifier='cuts')
REPORT['cutters'] = sorted(o.name for o in CUT.objects)
for o in list(CUT.objects): bpy.data.objects.remove(o, do_unlink=True)
clean(body)
def split_by_material(o, names, new_name):
    me2 = o.data.copy(); n = bpy.data.objects.new(new_name, me2); o.users_collection[0].objects.link(n)
    for ob, keep in ((o, lambda m: m not in names), (n, lambda m: m in names)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(mats[f.material_index].name if mats[f.material_index] else '')], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    return n
glass = split_by_material(body, {'TG_Glass'}, 'Glass_Shell'); clean(glass); clean(body)
def remap_tmp(o):
    """TMP_<swatch> -> TG_Palette + swatch attribute."""
    me = o.data; names = [m.name for m in me.materials]; idx = [p.material_index for p in me.polygons]
    tg = [(n[4:] if n.startswith('TMP_') else None) for n in names]; final = [('TG_Palette' if t else n) for n, t in zip(names, tg)]
    order = list(dict.fromkeys(final)); me.materials.clear()
    for n in order: me.materials.append(M[n])
    me.polygons.foreach_set('material_index', [order.index(final[i]) for i in idx])
    a = me.attributes.get('swatch') or me.attributes.new('swatch', 'INT', 'FACE')
    a.data.foreach_set('value', [SWATCH.index('pocket' if tg[i] == 'arch' else tg[i]) if tg[i] else 0 for i in idx])
    if any(t == 'arch' for t in tg):
        for p in me.polygons:
            if tg[idx[p.index]] == 'arch': a.data[p.index].value = SWATCH.index('satin_black')
def skin_normals(o, skin_names=('TG_Paint', 'TG_Glass'), skin_swatches=('gloss_black',)):
    """loop normals: skin faces take the smooth high-resolution body normal; cut / pocket / gap faces stay flat (crisp edges)."""
    me = o.data; me.shade_smooth(); sw = me.attributes.get('swatch'); out = []
    for p in me.polygons:
        m = me.materials[p.material_index].name if me.materials[p.material_index] else ''
        skin = m in skin_names or (m == 'TG_Palette' and sw and SWATCH[sw.data[p.index].value] in skin_swatches)
        for li in p.loop_indices:
            if skin:
                co = me.vertices[me.loops[li].vertex_index].co; loc, nrm, i, d = BVH.find_nearest(co)
                n = nrm if nrm.dot(p.normal) > 0 else -nrm
                out.append(tuple(n) if d < .006 and n.dot(p.normal) > .5 else tuple(p.normal))
            else: out.append(tuple(p.normal))
    me.normals_split_custom_set(out)
remap_tmp(body); remap_tmp(glass); purge_slots(body); purge_slots(glass); skin_normals(body); skin_normals(glass)
REPORT['body_lod0_tris'] = tris(body)
save_ckp('titangt_02_body_panels.blend') if LAST >= 2 else None
if LAST <= 2: sys.exit(0)
# ================================================================ 03 exterior details + lights (Trim / Lights / mirrors)
TR, LI = Geo(), Geo()
def surf_patch(g, poly, hitf, off, t, step=.008, flip=None):
    """conforming lens / panel over a closed outline: polar fan from the outline centroid (keeps the exact outline)."""
    ring = sample_poly(poly, step); c = Vector((sum(x for x, _ in ring) / len(ring), sum(z for _, z in ring) / len(ring)))
    pts = []
    for k in (1.0, .66, .33):
        row = []
        for x, z in ring:
            q = c.lerp(Vector((x, z)), k); p, n = hitf(q.x, q.y); row.append(p + n * off if p is not None else None)
        pts.append(row)
    if any(p is None for r in pts for p in r): print('PATCH MISS', t); return
    pc, nc = hitf(c.x, c.y); n0 = len(g.V)
    for r in pts: g.V += [tuple(p) for p in r]
    g.V.append(tuple(pc + nc * off)); nr = len(ring)
    fl = flip if flip is not None else False
    for i in range(2):
        for j in range(nr):
            f = (n0 + i * nr + j, n0 + i * nr + (j + 1) % nr, n0 + (i + 1) * nr + (j + 1) % nr, n0 + (i + 1) * nr + j); g.F.append(f[::-1] if fl else f); g.T.append(t)
    for j in range(nr):
        f = (n0 + 2 * nr + j, n0 + 2 * nr + (j + 1) % nr, n0 + 3 * nr); g.F.append(f[::-1] if fl else f); g.T.append(t)
def orient(g_from, outward):
    """flip faces added since g_from so their normals point along `outward(face centre)`."""
    for i in range(g_from, len(TR.F)): pass
def bezel(g, poly, hitf, w, off, t):
    """thin frame on the surface around an opening (outline -> offset outline)."""
    ring = sample_poly(poly, .01); c = Vector((sum(x for x, _ in ring) / len(ring), sum(z for _, z in ring) / len(ring)))
    A, B = [], []
    for x, z in ring:
        q = Vector((x, z)); d = (q - c).normalized(); p0, n0 = hitf(q.x, q.y); q1 = q + d * w; p1, n1 = hitf(q1.x, q1.y)
        if p0 is None or p1 is None: print('BEZEL MISS', t); return
        A.append(p0 + n0 * off - (n0 * .006)); B.append(p1 + n1 * off)
    g.strip(A, B, t, closed=True)
# ---- front: grille bezel + slats, intake fins, splitter
bezel(TR, GRILLE, fhit, .016, .0015, 'TG_Palette:dark_chrome')
for k in range(7):
    z = lerp(GZ0 + .03, GZ1 - .03, k / 6); v = (GZ1 - z) / (GZ1 - GZ0); hw = grille_x(v) - .012; xs = np.linspace(-hw, hw, 25); F_, B_ = [], []
    for x in xs:
        p, n = fhit(x, z); F_.append(Vector((x, p.y + .014, z))); B_.append(Vector((x, p.y + .05, z)))
    top_f = [q + Vector((0, 0, .004)) for q in F_]; bot_f = [q - Vector((0, 0, .004)) for q in F_]; top_b = [q + Vector((0, 0, .004)) for q in B_]; bot_b = [q - Vector((0, 0, .004)) for q in B_]
    TR.strip(bot_f, top_f, 'TG_Palette:dark_chrome', flip=True); TR.strip(top_f, top_b, 'TG_Palette:grille', flip=True); TR.strip(bot_b, bot_f, 'TG_Palette:grille', flip=True)
for sx in (1, -1):
    for zf in (.27, .32):
        xs = np.linspace(.64, .82, 9); F_ = []
        for x in xs:
            p, n = fhit(sx * x, zf + .03 * (x - .62) / .22); F_.append(Vector((sx * x, p.y + .012, zf + .03 * (x - .62) / .22)))
        TR.strip([q - Vector((0, 0, .003)) for q in F_], [q + Vector((0, 0, .003)) for q in F_], 'TG_Carbon', flip=sx > 0)
        TR.strip([q + Vector((0, 0, .003)) for q in F_], [q + Vector((0, .04, .003)) for q in F_], 'TG_Carbon', flip=sx > 0)
xs = np.linspace(-.88, .88, 45); front = []
for x in xs:
    p, n = fhit(x, .20); front.append(Vector((x, (p.y if p else -2.25) - .03, .172)))
back = [Vector((x, -1.95, .172)) for x in xs]
TR.strip(back, front, 'TG_Carbon'); TR.strip([q - Vector((0, 0, .013)) for q in front], [q - Vector((0, 0, .013)) for q in back], 'TG_Carbon')
TR.strip(front, [q - Vector((0, 0, .013)) for q in front], 'TG_Carbon', flip=True)
# ---- headlights (in the recess): DRL blade, two projector modules, amber indicator, clear outer lens
for sx in (1, -1):
    xin, xout = .585, .862
    def hl_pt(u, zf, depth):                                                                      # u 0 inner .. 1 outer; zf 0 bottom .. 1 top of the outline
        x = lerp(xin, xout, u); zb = lerp(.525, .575, u); zt = lerp(.600, .672, u); z = lerp(zb, zt, zf); p, n = fhit(sx * x, z); return Vector((p.x, p.y + depth, p.z))
    us = np.linspace(.04, .96, 22)
    A = [hl_pt(u, .80, .018) for u in us]; B = [hl_pt(u, .92, .018) for u in us]
    LI.strip(A, B, 'TG_LED_DRL', flip=sx < 0)
    A = [hl_pt(u, .20, .022) for u in np.linspace(.74, .96, 6)]; B = [hl_pt(u, .34, .022) for u in np.linspace(.74, .96, 6)]
    LI.strip(A, B, 'TG_LED_Indicator_L' if sx > 0 else 'TG_LED_Indicator_R', flip=sx < 0)
    for u in (.22, .50):                                                                            # projector modules
        c0 = hl_pt(u, .46, .0); seg = 20; r = .024
        ring = lambda dy, rr: [Vector((c0.x + rr * math.cos(2 * math.pi * q / seg), c0.y + dy, c0.z + rr * math.sin(2 * math.pi * q / seg))) for q in range(seg)]
        LI.strip(ring(.055, r), ring(.016, r), 'TG_Palette:housing', closed=True); LI.strip(ring(.016, r), ring(.012, r * .8), 'TG_Palette:reflector', closed=True)
        n0 = len(LI.V); LI.V += [tuple(v) for v in ring(.012, r * .8)] + [(c0.x, c0.y + .010, c0.z)]
        for q in range(seg): LI.F.append((n0 + q, n0 + (q + 1) % seg, n0 + seg)); LI.T.append('TG_LED_Headlamp')
    surf_patch(LI, HL_ := rounded([(sx * .585, .525), (sx * .862, .575), (sx * .862, .672), (sx * .585, .600)], [.02, .03, .03, .02], 4), fhit, .0012, 'TG_LensClear')
# ---- rear lights (in the channel): full-width tail bar, corner tail verticals, brake / indicator / reverse blocks, red + clear lenses
def rl_pt(x, z, depth): p, n = rhit(x, z); return Vector((p.x, p.y - depth, p.z))
xs = np.linspace(-.69, .69, 60)
LI.strip([rl_pt(x, .840, .016) for x in xs], [rl_pt(x, .850, .016) for x in xs], 'TG_LED_Tail')
for sx in (1, -1):
    zs = np.linspace(.742, .852, 8)
    LI.strip([rl_pt(sx * .838, z, .016) for z in zs], [rl_pt(sx * .855, z, .016) for z in zs], 'TG_LED_Tail', flip=sx > 0)
    for (z0, z1, mat) in ((.802, .826, 'TG_LED_Brake'), (.770, .792, 'TG_LED_Indicator_L' if sx > 0 else 'TG_LED_Indicator_R'), (.738, .760, 'TG_LED_Reverse')):
        xs2 = np.linspace(.712, .826, 8)
        LI.strip([rl_pt(sx * x, z0, .02) for x in xs2], [rl_pt(sx * x, z1, .02) for x in xs2], mat, flip=sx < 0)
RED = rounded([(.866, .857), (-.866, .857), (-.866, .795), (-.70, .795), (-.70, .833), (.70, .833), (.70, .795), (.866, .795)], [.02, .02, .0, .0, .006, .006, .0, .0], 3)
surf_patch(LI, RED[:len(RED) // 2 + 1] if False else RED, rhit, .0012, 'TG_LensRed') if False else None
# red lens: bar + upper corners; clear lens over indicator / reverse (lower corners)
xs = np.linspace(-.866, .866, 70); zs = np.linspace(.833, .857, 3)
LI.grid([[rl_pt(x, z, -.0012) for x in xs] for z in zs], 'TG_LensRed')
for sx in (1, -1):
    xs2 = np.linspace(.70, .866, 10)
    LI.grid([[rl_pt(sx * x, z, -.0012) for x in xs2] for z in np.linspace(.795, .833, 3)], 'TG_LensRed', flip=sx < 0)
    LI.grid([[rl_pt(sx * x, z, -.0012) for x in xs2] for z in np.linspace(.728, .795, 4)], 'TG_LensClear', flip=sx < 0)
# ---- rear valance (satin black) + chrome accent, plate recess, quad exhaust, diffuser + strakes
def rpatch(g, x_fn, z0, z1, nz, t, off, nx=40, flip=False):
    g.grid([[rl_pt(x_fn(v) * u, lerp(z0, z1, v), -off) for u in np.linspace(-1, 1, nx)] for v in np.linspace(0, 1, nz)], t, flip)
rpatch(TR, lambda v: lerp(.84, .78, v), .470, .345, 5, 'TG_Palette:satin_black', .002, flip=True)
rpatch(TR, lambda v: .82, .474, .468, 2, 'TG_Palette:dark_chrome', .0028, flip=True)
rpatch(TR, lambda v: .255, .665, .545, 4, 'TG_Palette:gloss_black', .0015, nx=12, flip=True)
for cx in (-.64, -.53, .53, .64):
    seg = 24; p, n = rhit(cx, .405); y0 = p.y + .002; cz = .405
    circ = lambda r, y: [Vector((cx + r * math.cos(2 * math.pi * k / seg), y, cz + r * math.sin(2 * math.pi * k / seg))) for k in range(seg)]
    TR.strip(circ(.040, y0 - .02), circ(.040, y0 + .022), 'TG_Palette:exhaust', closed=True); TR.strip(circ(.040, y0 + .022), circ(.034, y0 + .022), 'TG_Palette:exhaust', closed=True)
    TR.strip(circ(.034, y0 + .022), circ(.034, y0 - .06), 'TG_Palette:exhaust_inner', closed=True)
    n0 = len(TR.V); TR.V += [tuple(v) for v in circ(.034, y0 - .06)] + [(cx, y0 - .06, cz)]
    for k in range(seg): TR.F.append((n0 + (k + 1) % seg, n0 + k, n0 + seg)); TR.T.append('TG_Palette:exhaust_inner')
xs = np.linspace(-.62, .62, 33); ys = np.linspace(1.80, 2.37, 12)
def diff_z(y): return lerp(.130, .330, ss(1.80, 2.37, y) ** 1.2)
TR.grid([[Vector((x, y, diff_z(y))) for x in xs] for y in ys], 'TG_Carbon', flip=True)
for xf in (-.62, -.40, -.14, .14, .40, .62):
    top = [Vector((xf, y, diff_z(y))) for y in ys]; bot = [Vector((xf, y, max(.142, diff_z(y) - .045))) for y in ys]
    for off in (-.0035, .0035): TR.strip([q + Vector((off, 0, 0)) for q in top], [q + Vector((off, 0, 0)) for q in bot], 'TG_Carbon', flip=off > 0)
    TR.strip([q - Vector((.0035, 0, 0)) for q in bot], [q + Vector((.0035, 0, 0)) for q in bot], 'TG_Carbon')
# ---- side: vent fins, handle bars, sill blades, chrome belt line
for sx in (1, -1):
    for k in range(3):
        z = .535 + .045 * k; ys2 = np.linspace(-.905 + .04 * (z - .505) / .15, -.715 + .04 * (z - .505) / .15, 8); A = []
        for y in ys2:
            p, n = shit(sx, y, z); A.append(Vector((p.x - sx * .008, y, z)))
        TR.strip([q - Vector((0, 0, .005)) for q in A], [q + Vector((0, 0, .005)) for q in A], 'TG_Palette:dark_chrome', flip=sx > 0)
        TR.strip([q + Vector((0, 0, .005)) for q in A], [q + Vector((-sx * .02, 0, .005)) for q in A], 'TG_Palette:dark_chrome', flip=sx > 0)
    ys2 = np.linspace(.285, .425, 8); A = []
    for y in ys2:
        p, n = shit(sx, y, .760); A.append(Vector((p.x - sx * .004, y, .760)))
    TR.strip([q - Vector((0, 0, .005)) for q in A], [q + Vector((0, 0, .005)) for q in A], 'TG_Palette:chrome', flip=sx > 0)
    ys2 = np.linspace(-.86, .96, 40); A, B = [], []
    for y in ys2:
        p, n = shit(sx, y, .262); A.append(p + n * .006 + Vector((0, 0, -.016))); B.append(p + n * .006 + Vector((0, 0, .016)))
    TR.strip(A, B, 'TG_Carbon', flip=sx > 0); TR.strip(B, [q - Vector((sx * .02, 0, 0)) for q in B], 'TG_Carbon', flip=sx > 0); TR.strip([q - Vector((sx * .02, 0, 0)) for q in A], A, 'TG_Carbon', flip=sx > 0)
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):                          # wheel-well liners: drum + inner wall (no see-through arches)
    R_ = r + .05; zc = r + .012; seg = 28; a0, a1 = math.radians(-25), math.radians(205)
    xin_ = .52
    arc = [(y + R_ * math.cos(lerp(a0, a1, q / seg)), zc + R_ * math.sin(lerp(a0, a1, q / seg))) for q in range(seg + 1)]
    xi, xo = sx * .52, sx * (WMAX(y) - .012)                                                         # liner stays inside the body side
    A = [Vector((xi, yy, zz)) for yy, zz in arc]; B = [Vector((xo, yy, zz)) for yy, zz in arc]
    TR.strip(A, B, 'TG_Palette:satin_black', flip=sx > 0)
    inner = [Vector((xi, yy, zz)) for yy, zz in arc] + [Vector((xi, y + R_ * math.cos(a0), .13)), Vector((xi, y + R_ * math.cos(a1), .13))][::-1]
    n0 = len(TR.V); TR.V += [tuple(v) for v in A] + [(xi, y, .14)]
    for q in range(seg): f = (n0 + q, n0 + q + 1, n0 + seg + 1); TR.F.append(f if sx < 0 else f[::-1]); TR.T.append('TG_Palette:satin_black')
trim = mk('Trim_LOD0', TR.V, TR.F, TR.T, WORK, M); lights = mk('Lights_LOD0', LI.V, LI.F, LI.T, WORK, M)
# orient: every trim / light face looks away from the car centre (or down for underside parts)
for o in (trim, lights):
    clean(o); orient_components(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(35))
# ---- mirrors (teardrop housing, glass on the rear face, stalk) -> part of the body
MI = Geo()
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=24, v_segments=14, radius=1.0)
    for v in bmm.verts:
        x, y, z = v.co; y = y * (1.0 if y < 0 else .45); z = z * (1 - .25 * max(0, -y))                 # tapered nose (front, -Y), flat glass face (rear)
        v.co = Vector((x * .115, y * .085, z * .048)) + Vector((sx * 1.0, -.40, .985))
    vs = [tuple(v.co) for v in bmm.verts]; fs = [tuple(v.index for v in f.verts) for f in bmm.faces]
    ts = ['TG_Palette:mirror' if f.normal.y > .7 else 'TG_Paint' for f in bmm.faces]; bmm.free(); MI.add(vs, fs, ts)
    Vs = [(sx * .835, -.44, .905), (sx * .835, -.36, .905), (sx * .915, -.385, .955), (sx * .915, -.425, .955)]
    MI.add(Vs + [(x, y, z + .035) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'TG_Paint')
mirrors = mk('Mirrors', MI.V, MI.F, MI.T, WORK, M)
bm = bmesh.new(); bm.from_mesh(mirrors.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(mirrors.data); bm.free(); mirrors.data.shade_smooth()
REPORT['trim_tris'], REPORT['lights_tris'] = tris(trim), tris(lights)
save_ckp('titangt_03_details_lights.blend') if LAST >= 3 else None
# ================================================================ 04 wheels (parametric per LOD: tire, rim, brake disc, caliper)
WREF = {'FL': Vector((XF, YF, RF)), 'FR': Vector((-XF, YF, RF)), 'RL': Vector((XR, YR, RR)), 'RR': Vector((-XR, YR, RR))}
WSPEC = {'FL': (RF, WF, .254), 'FR': (RF, WF, .254), 'RL': (RR, WR, .267), 'RR': (RR, WR, .267)}
LOD_SEG = {0: (96, 64), 1: (48, 36), 2: (28, 20), 3: (16, 12)}
def build_wheel(c, k, coll_):
    R, W, rr = WSPEC[c]; sx = 1 if c[1] == 'L' else -1; hw = W / 2; seg_t, seg_r = LOD_SEG[k]; out = {}
    # tire (revolve with UVs for the tread texture)
    prof = [(-hw * .80, rr + .006), (-hw * .96, rr + .03), (-hw, R * .80), (-hw * .985, R * .90), (-hw * .93, R * .965), (-hw * .80, R * .995), (-hw * .40, R), (0, R),
            (hw * .40, R), (hw * .80, R * .995), (hw * .93, R * .965), (hw * .985, R * .90), (hw, R * .80), (hw * .96, rr + .03), (hw * .80, rr + .006)]
    if k >= 2: prof = [prof[i] for i in (0, 2, 4, 6, 8, 10, 12, 14)]
    Vt, Ft, UVt = revolve(prof, seg_t, sx); g = Geo(); g.add(Vt, Ft, 'TG_Tire'); tire = mk(f'Tire_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    uvl = tire.data.uv_layers.new(name='tireUV')
    for p in tire.data.polygons:
        for li in p.loop_indices: uvl.data[li].uv = UVt[tire.data.loops[li].vertex_index]
    out['Tire'] = tire
    # rim: outer lip + barrel + 5 twin spokes + hub + lug nuts + centre cap
    g = Geo(); face = hw * .55
    lip = [(hw * .84, rr - .028), (hw * .90, rr + .005), (hw * .80, rr + .012), (hw * .70, rr - .008), (hw * .66, rr - .020)]
    Vl, Fl, _ = revolve(lip, seg_r, sx); g.add(Vl, Fl, 'TG_Palette:wheel_machined')
    barrel = [(hw * .66, rr - .020), (hw * .20, rr - .030), (-hw * .70, rr - .032), (-hw * .82, rr + .004)]
    Vb, Fb, _ = revolve(barrel, seg_r, sx); g.add(Vb, Fb, 'TG_Palette:wheel_graphite')
    nsp = 5
    for s_ in range(nsp):
        for d in (-.105, .105):
            a = 2 * math.pi * s_ / nsp + d; R_ = Matrix.Rotation(a, 3, 'X')
            prof_s = []                                                                            # tapered, concave spoke: (radius, axial x, half-width)
            for t in np.linspace(0, 1, 9 if k == 0 else 4 if k == 1 else 3):
                r_ = lerp(.062, rr - .022, t); xx = face - .028 * math.sin(math.pi * t) * (1 - .4 * t) - .012 * t; w = lerp(.016, .011, t); prof_s.append((r_, xx, w))
            secs = []
            for r_, xx, w in prof_s:
                th = .012
                pts = [Vector((sx * (xx + .004), -w, r_)), Vector((sx * (xx + .004), w, r_)), Vector((sx * (xx - th), w * 1.15, r_)), Vector((sx * (xx - th), -w * 1.15, r_))]
                secs.append([R_ @ p for p in pts])
            for A, B in zip(secs, secs[1:]): g.strip(A, B, 'TG_Palette:wheel_graphite', closed=True, flip=sx < 0)
            g.add(secs[-1], [(0, 1, 2, 3) if sx > 0 else (3, 2, 1, 0)], 'TG_Palette:wheel_graphite')
    hub = [(face + .006, 0.0), (face + .006, .032), (face + .002, .048), (face - .004, .068), (face - .02, .07)]
    Vh, Fh, _ = revolve(hub, max(12, seg_r // 2), sx); g.add(Vh, Fh, 'TG_Palette:wheel_graphite')
    if k <= 1:
        for s_ in range(5):                                                                        # lug nuts
            a = 2 * math.pi * (s_ + .5) / 5; cy, cz = .042 * math.cos(a), .042 * math.sin(a); hx = []
            for q in range(6): b = 2 * math.pi * q / 6; hx.append((cy + .0075 * math.cos(b), cz + .0075 * math.sin(b)))
            A = [Vector((sx * (face + .004), y, z)) for y, z in hx]; B = [Vector((sx * (face + .016), y, z)) for y, z in hx]
            g.strip(A, B, 'TG_Palette:wheel_machined', closed=True, flip=sx < 0); g.add(B, [tuple(range(6)) if sx > 0 else tuple(range(5, -1, -1))], 'TG_Palette:wheel_machined')
        cap = [(face + .010, 0.0), (face + .010, .020), (face + .006, .026)]
        Vc, Fc, _ = revolve(cap, 16, sx); g.add(Vc, Fc, 'TG_Palette:dark_chrome')
    if k == 3:                                                                                     # LOD3: rotor disc inside the wheel replaces the brake hardware
        Vd, Fd, _ = revolve([(-hw * .1, .06), (-hw * .1, rr - .05)], 12, sx); g.add(Vd, Fd, 'TG_Palette:rotor')
    out['Wheel'] = mk(f'Wheel_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    if k <= 2:
        g = Geo(); rd = rr - .045
        disc = [(hw * .05, .085), (hw * .05, rd), (-hw * .10, rd), (-hw * .10, .085)]
        Vd, Fd, _ = revolve(disc, seg_r, sx); g.add(Vd, Fd, 'TG_Palette:rotor')
        hat = [(hw * .30, .0), (hw * .30, .085), (hw * .05, .085)]
        Vh, Fh, _ = revolve(hat, max(12, seg_r // 2), sx); g.add(Vh, Fh, 'TG_Palette:rotor_hat')
        out['BrakeDisc'] = mk(f'BrakeDisc_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
        g = Geo(); n_ = {0: 12, 1: 8, 2: 4}[k]; r0, r1 = rd - .055, rd + .012; front = c[0] == 'F'
        a0, a1 = (math.radians(35), math.radians(105)) if front else (math.radians(75), math.radians(145))
        secs = []
        for q in range(n_ + 1):
            a = lerp(a0, a1, q / n_); ca, sa = math.cos(a) * (1 if front else -1), math.sin(a); bul = .006 * math.sin(math.pi * q / n_)
            pts = [(r0, sx * (hw * .22 + bul)), (r1, sx * (hw * .22 + bul)), (r1 + .006, sx * (hw * .05)), (r1, -sx * (hw * .30 + bul)), (r0, -sx * (hw * .30 + bul)), (r0 - .006, sx * (-hw * .05))]
            secs.append([Vector((xx, rr_ * ca, rr_ * sa)) for rr_, xx in pts])
        for A, B in zip(secs, secs[1:]): g.strip(A, B, 'TG_Palette:caliper_bronze', closed=True)
        g.add(secs[0], [tuple(range(6))], 'TG_Palette:caliper_bronze'); g.add(secs[-1], [tuple(range(5, -1, -1))], 'TG_Palette:caliper_bronze')
        out['Caliper'] = mk(f'Caliper_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    for key, o in out.items():
        bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
        if key in ('Caliper',): bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(o.data); bm.free(); clean(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40 if key != 'Tire' else 60))
        o.data.transform(Matrix.Translation(WREF[c])); set_origin(o, WREF[c])
    return out
WH = coll('TG_WHEELS'); ASM = {}
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key, o in build_wheel(c, k, WH).items(): ASM[(k, c, key)] = o
save_ckp('titangt_04_wheels.blend') if LAST >= 4 else None
# ================================================================ 05 interior (sport-luxury GT: cognac leather, black trim, aluminium accents)
IN, ST = Geo(), Geo()
def rbox(g, c, half, t, bev=.02, rot=None, seg=2):
    """rounded box (bevelled) built from a cube: inset corners by `bev`."""
    hx, hy, hz = half; R = rot or Matrix.Identity(3)
    bmx = bmesh.new(); bmesh.ops.create_cube(bmx, size=1.0); bmesh.ops.scale(bmx, vec=(2 * hx, 2 * hy, 2 * hz), verts=bmx.verts)
    bmesh.ops.bevel(bmx, geom=list(bmx.edges), offset=min(bev, hx * .9, hy * .9, hz * .9), segments=3, affect='EDGES', profile=.5)
    for v in bmx.verts: v.co = R @ v.co + Vector(c)
    g.add([tuple(v.co) for v in bmx.verts], [tuple(v.index for v in f.verts) for f in bmx.faces], t); bmx.free()
for sx in (1, -1):
    xs_ = sx * .372; tilt = Matrix.Rotation(-.30, 3, 'X')
    rbox(IN, (xs_, .30, .315), (.235, .245, .055), 'TG_Palette:leather_cognac', .03)                   # cushion
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .205, .30, .36), (.035, .24, .055), 'TG_Palette:leather_black', .018)      # cushion bolsters
    rbox(IN, (xs_, .56, .67), (.215, .055, .30), 'TG_Palette:leather_cognac', .035, tilt)              # backrest
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .20, .53, .66), (.04, .07, .27), 'TG_Palette:leather_black', .02, tilt)     # backrest bolsters
    rbox(IN, (xs_, .66, 1.03), (.12, .045, .085), 'TG_Palette:leather_black', .03, tilt)               # head restraint
    rbox(IN, (sx * .765, -.05, .56), (.025, .55, .215), 'TG_Palette:leather_black', .02)                # door card (inside the door skin, below the belt)
    rbox(IN, (sx * .735, -.05, .64), (.025, .36, .025), 'TG_Palette:leather_cognac', .012)             # armrest
    rbox(IN, (sx * .738, -.42, .48), (.012, .08, .055), 'TG_Palette:aluminium', .006)                  # speaker trim
rbox(IN, (0, -.40, .755), (.70, .11, .055), 'TG_Palette:leather_black', .045)                           # dashboard top (stays below the cowl / belt line)
rbox(IN, (0, -.33, .62), (.70, .06, .08), 'TG_Palette:int_trim', .03)                                  # dashboard lower
rbox(IN, (0, -.29, .70), (.68, .012, .010), 'TG_Palette:aluminium', .005)                              # aluminium accent bar
rbox(IN, (.372, -.38, .835), (.17, .06, .03), 'TG_Palette:leather_black', .025)                        # cluster hood (LHD: driver on +X)
rbox(IN, (.372, -.325, .785), (.15, .008, .04), 'TG_Display', .006)                                   # instrument cluster display
rbox(IN, (0, -.285, .735), (.11, .008, .05), 'TG_Display', .006)                                       # centre screen
rbox(IN, (0, -.05, .46), (.10, .55, .10), 'TG_Palette:leather_black', .03)                             # centre console
rbox(IN, (0, .08, .565), (.09, .30, .012), 'TG_Palette:aluminium', .01)                               # console top plate
rbox(IN, (0, -.18, .60), (.022, .022, .04), 'TG_Palette:leather_cognac', .015)                         # selector
rbox(IN, (0, .20, .17), (.82, 1.0, .03), 'TG_Palette:carpet', .01)                                     # floor
rbox(IN, (0, .86, .84), (.70, .22, .02), 'TG_Palette:alcantara', .01)                                 # parcel shelf
# headliner: the roof's inner surface (offset of the high-res body under the roof), so the cabin ceiling is not the paint backface
hl_rows = []
for y in np.linspace(-.40, 1.30, 18):
    row = []
    for x in np.linspace(-.52, .52, 15):
        p, n = thit(x, y); row.append((p - n * .012) if p is not None and p.z > 1.0 else None)
    hl_rows.append(row)
hl_rows = [r for r in hl_rows if all(p is not None for p in r)]
IN.grid(hl_rows, 'TG_Palette:alcantara', flip=True)
interior = mk('Interior_LOD0', IN.V, IN.F, IN.T, WORK, M)
# steering wheel: rim torus + three spokes + hub (pivot at the hub, tilted 22 deg)
hubc = Vector((.372, -.255, .785)); tilt = Matrix.Rotation(math.radians(-68), 3, 'X'); seg, sg2 = 36, 10
for q in range(seg):
    a0, a1 = 2 * math.pi * q / seg, 2 * math.pi * (q + 1) / seg
    ring = lambda a: [hubc + tilt @ Vector((.18 * math.cos(a) + .016 * math.cos(2 * math.pi * k / sg2) * math.cos(a), .016 * math.sin(2 * math.pi * k / sg2), .18 * math.sin(a) + .016 * math.cos(2 * math.pi * k / sg2) * math.sin(a))) for k in range(sg2)]
    ST.strip(ring(a0), ring(a1), 'TG_Palette:leather_black', closed=True)
for a in (0, math.pi, -math.pi / 2):
    rbox(ST, tuple(hubc + tilt @ Vector((.10 * math.cos(a), 0, .10 * math.sin(a)))), (.075 if a != -math.pi / 2 else .018, .012, .018 if a != -math.pi / 2 else .07), 'TG_Palette:aluminium', .008, tilt)
rbox(ST, tuple(hubc + tilt @ Vector((0, .012, 0))), (.055, .025, .045), 'TG_Palette:leather_black', .02, tilt)
steer = mk('SteeringWheel_LOD0', ST.V, ST.F, ST.T, WORK, M); set_origin(steer, hubc)
for o in (interior, steer):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); clean(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40))
REPORT['interior_tris'] = tris(interior) + tris(steer)
save_ckp('titangt_05_interior.blend') if LAST >= 5 else None
# ================================================================ 06 merge + UVs
L0 = coll('LOD0_PARTS')
bpy.data.objects.remove(hi, do_unlink=True)
body_final = join([body, mirrors], 'Body_LOD0', L0); skin_normals(body_final) if False else None
glass.name = glass.data.name = 'Glass_LOD0'; link_only(glass, L0)
for o in (trim, lights, interior, steer): link_only(o, L0)
FINAL0 = {n: O[n] for n in ('Body_LOD0', 'Glass_LOD0', 'Trim_LOD0', 'Lights_LOD0', 'Interior_LOD0')}
for o in [x for x in O if x.type == 'MESH']: purge_slots(o); final_uvs(o)
T0_ = {o.name: tris(o) for o in O if o.type == 'MESH' and o.name.endswith('_LOD0')}; REPORT['lod0_parts'] = T0_; REPORT['lod0_total'] = sum(T0_.values())
print('LOD0', REPORT['lod0_total'], T0_, flush=True)
save_ckp('titangt_06_materials_uv.blend') if LAST >= 6 else None
# ================================================================ 07 LODs (collapse with LOD0 normals at LOD1; own smooth normals + 38 deg hard edges at LOD2/3)
def decimate(o, ratio, ref=None, transfer=True, sym=True):
    if ratio >= .999: return o
    m = o.modifiers.new('dec', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = ratio; m.use_symmetry = sym; m.symmetry_axis = 'X'; m.use_collapse_triangulate = True
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='dec')
    if transfer and ref:
        o.data.shade_smooth(); dt = o.modifiers.new('nt', 'DATA_TRANSFER'); dt.object = ref; dt.use_loop_data = True; dt.data_types_loops = {'CUSTOM_NORMAL'}; dt.loop_mapping = 'POLYINTERP_NEAREST'
        with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='nt')
    else:
        with bpy.context.temp_override(object=o, active_object=o): bpy.ops.mesh.customdata_custom_splitnormals_clear()
        o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(38))
    clean(o); return o
RK = {1: {'Body': .52, 'Glass': .7, 'Trim': .45, 'Lights': .5, 'Interior': .45, 'SteeringWheel': .5},
      2: {'Body': .26, 'Glass': .45, 'Trim': .18, 'Lights': .22, 'Interior': .18, 'SteeringWheel': .2},
      3: {'Body': .10, 'Glass': .18, 'Trim': .06, 'Lights': .08, 'Interior': .04}}
for k in (1, 2, 3):
    Lk = coll(f'LOD{k}_PARTS')
    for n0, o0 in list(FINAL0.items()) + [('SteeringWheel_LOD0', steer)]:
        kind = n0.split('_')[0]
        if kind not in RK[k]: continue
        d = o0.copy(); d.data = o0.data.copy(); Lk.objects.link(d); d.name = n0.replace('LOD0', f'LOD{k}'); d.data.name = d.name
        decimate(d, RK[k][kind], ref=o0, transfer=k <= 1)
        final_uvs(d)
REPORT['lod_ratios'] = RK
save_ckp('titangt_07_lods.blend') if LAST >= 7 else None
# ================================================================ 08 colliders, hierarchy, pivots, references
FIN = coll('TITAN_GT'); COLL = coll('TG_COLLIDERS', FIN)
root = empty('Car_Root', FIN, (0, 0, 0), None, 'PLAIN_AXES', .5)
for k in range(4):
    lr = empty(f'LOD{k}_Root', FIN, (0, 0, 0), root, 'PLAIN_AXES', .3)
    for n in ('Body', 'Glass', 'Trim', 'Lights', 'Interior', 'SteeringWheel'):
        o = O.get(f'{n}_LOD{k}')
        if not o: continue
        link_only(o, FIN)
        if n != 'SteeringWheel': set_origin(o, (0, 0, 0))
        mw = o.matrix_world.copy(); o.parent = lr; o.matrix_world = mw
    for c in ('FL', 'FR', 'RL', 'RR'):
        w = ASM.get((k, c, 'Wheel')); parent = lr
        if c in ('FL', 'FR'): parent = empty(f'SteerPivot_{c}_LOD{k}', FIN, WREF[c], lr, 'ARROWS', .15); bpy.context.view_layer.update()
        for key in ('Wheel', 'Tire', 'BrakeDisc', 'Caliper'):
            o = ASM.get((k, c, key))
            if o: link_only(o, FIN)
        local = Matrix.Identity(4) if parent is not lr else Matrix.Translation(WREF[c])
        w.parent = parent; w.matrix_parent_inverse = Matrix.Identity(4); w.matrix_basis = local
        for key in ('Tire', 'BrakeDisc'):
            o = ASM.get((k, c, key))
            if o: o.parent = w; o.matrix_parent_inverse = Matrix.Identity(4); o.matrix_basis = Matrix.Identity(4)
        cal = ASM.get((k, c, 'Caliper'))
        if cal: cal.parent = parent; cal.matrix_parent_inverse = Matrix.Identity(4); cal.matrix_basis = local
        bpy.context.view_layer.update()
def hull(name, verts):
    cell = .05
    while True:
        pts = list({(round(v.x / cell), round(v.y / cell), round(v.z / cell)): v for v in verts}.values())
        bm = bmesh.new(); vv = [bm.verts.new(v) for v in pts]; bmesh.ops.convex_hull(bm, input=vv)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bmesh.ops.triangulate(bm, faces=bm.faces); bm.normal_update()
        convex = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 5e-4 for v in bm.verts) for f in bm.faces)
        if (len(bm.faces) <= 200 and convex) or cell > .4: break
        bm.free(); cell *= 1.3
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); COLL.objects.link(o); o.display_type = 'WIRE'; return o
pts = [O[f'{n}_LOD2'].matrix_world @ v.co for n in ('Body', 'Glass') for v in O[f'{n}_LOD2'].data.vertices]
CL = {'Collision_Front': [p for p in pts if p.y < -1.0 and p.z < .95], 'Collision_Body': [p for p in pts if -1.15 < p.y < 1.25 and p.z < .82],
      'Collision_Cabin': [p for p in pts if -.62 < p.y < 1.55 and p.z > .74], 'Collision_Rear': [p for p in pts if p.y > 1.05 and p.z < 1.02]}
cr = empty('Collision', FIN, (0, 0, 0), root, 'PLAIN_AXES', .2)
for n, vs in CL.items():
    if len(vs) > 8: h = hull(n, vs); h.parent = cr
for c in ('FL', 'FR', 'RL', 'RR'):
    e = empty(f'WheelColliderRef_{c}', FIN, WREF[c], root, 'SPHERE', .1); e['radius_m'] = WSPEC[c][0]; e['width_m'] = WF if c[0] == 'F' else WR
empty('CenterOfMass', FIN, (0, .15, .42), root, 'SPHERE', .08)                                   # front-mid engine GT: centreline, low, slightly behind mid-wheelbase
for c in list(bpy.data.collections):
    if c.name not in ('TITAN_GT', 'TG_COLLIDERS'):
        for o in list(c.objects):
            if o.name not in FIN.all_objects: bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
json.dump(REPORT, open(os.path.join(REPD(), 'TG_build_log.json'), 'w'), indent=1)
save_ckp('titangt_08_colliders_hierarchy.blend') if LAST >= 8 else None
