# Vortex R (Phase D) production build. Blender -b --factory-startup --python vx_build.py [-- <last stage 2..8>]
# Starts from the APPROVED blockout design (identical design code via vx_lib); writes vortexr_02 .. 08 (never overwrites 01_blockout).
#  02 body (cage + crest crease + subdivision, real openings, panel gaps, diffuser tunnel)  03 exterior details + lights  04 wheels  05 interior
#  06 merge + UVs  07 LODs  08 colliders, hierarchy, pivots, references
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from vx_lib import *
# ---- generic production helpers (copied from the frozen Titan GT build; read-only source, renamed TG -> VX)
def subdiv(o, lv):
    m = o.modifiers.new('s', 'SUBSURF'); m.levels = m.render_levels = lv
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='s')

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

def split_by_material(o, names, new_name):
    me2 = o.data.copy(); n = bpy.data.objects.new(new_name, me2); o.users_collection[0].objects.link(n)
    for ob, keep in ((o, lambda m: m not in names), (n, lambda m: m in names)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(mats[f.material_index].name if mats[f.material_index] else '')], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    return n

def remap_tmp(o):
    """TMP_<swatch> -> VX_Palette + swatch attribute."""
    me = o.data; names = [m.name for m in me.materials]; idx = [p.material_index for p in me.polygons]
    tg = [(n[4:] if n.startswith('TMP_') else None) for n in names]; final = [('VX_Palette' if t else n) for n, t in zip(names, tg)]
    order = list(dict.fromkeys(final)); me.materials.clear()
    for n in order: me.materials.append(M[n])
    me.polygons.foreach_set('material_index', [order.index(final[i]) for i in idx])
    a = me.attributes.get('swatch') or me.attributes.new('swatch', 'INT', 'FACE')
    a.data.foreach_set('value', [SWATCH.index('pocket' if tg[i] == 'arch' else tg[i]) if tg[i] else 0 for i in idx])
    if any(t == 'arch' for t in tg):
        for p in me.polygons:
            if tg[idx[p.index]] == 'arch': a.data[p.index].value = SWATCH.index('satin_black')

def skin_normals(o, skin_names=('VX_Paint', 'VX_Glass'), skin_swatches=('gloss_black',)):
    """loop normals: skin faces take the smooth high-resolution body normal; cut / pocket / gap faces stay flat (crisp edges)."""
    me = o.data; me.shade_smooth(); sw = me.attributes.get('swatch'); out = []
    for p in me.polygons:
        m = me.materials[p.material_index].name if me.materials[p.material_index] else ''
        skin = m in skin_names or (m == 'VX_Palette' and sw and SWATCH[sw.data[p.index].value] in skin_swatches)
        for li in p.loop_indices:
            if skin:
                co = me.vertices[me.loops[li].vertex_index].co.lerp(p.center, .08)                       # probe slightly inside the face: correct side of a crease
                n = smooth_normal(co, p.normal); out.append(tuple(n) if n is not None else tuple(p.normal))
            else: out.append(tuple(p.normal))
    me.normals_split_custom_set(out)

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

def bezel(g, poly, hitf, w, off, t):
    """thin frame on the surface around an opening (outline -> offset outline)."""
    ring = sample_poly(poly, .01); c = Vector((sum(x for x, _ in ring) / len(ring), sum(z for _, z in ring) / len(ring)))
    A, B = [], []
    for x, z in ring:
        q = Vector((x, z)); d = (q - c).normalized(); p0, n0 = hitf(q.x, q.y); q1 = q + d * w; p1, n1 = hitf(q1.x, q1.y)
        if p0 is None or p1 is None: print('BEZEL MISS', t); return
        A.append(p0 + n0 * off - (n0 * .006)); B.append(p1 + n1 * off)
    g.strip(A, B, t, closed=True)

def rbox(g, c, half, t, bev=.02, rot=None, seg=2):
    """rounded box (bevelled) built from a cube: inset corners by `bev`."""
    hx, hy, hz = half; R = rot or Matrix.Identity(3)
    bmx = bmesh.new(); bmesh.ops.create_cube(bmx, size=1.0); bmesh.ops.scale(bmx, vec=(2 * hx, 2 * hy, 2 * hz), verts=bmx.verts)
    bmesh.ops.bevel(bmx, geom=list(bmx.edges), offset=min(bev, hx * .9, hy * .9, hz * .9), segments=3, affect='EDGES', profile=.5)
    for v in bmx.verts: v.co = R @ v.co + Vector(c)
    g.add([tuple(v.co) for v in bmx.verts], [tuple(v.index for v in f.verts) for f in bmx.faces], t); bmx.free()

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

def hull(name, verts):
    cell = .05
    while True:
        pts = list({(round(v.x / cell), round(v.y / cell), round(v.z / cell)): v for v in verts}.values())
        pts += [max(verts, key=lambda v: v[i] * sg) for i in range(3) for sg in (1, -1)]                        # keep the 6 extreme points (bounds stay exact)
        bm = bmesh.new(); vv = [bm.verts.new(v) for v in pts]; bmesh.ops.convex_hull(bm, input=vv)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bmesh.ops.triangulate(bm, faces=bm.faces); bm.normal_update()
        convex = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 5e-4 for v in bm.verts) for f in bm.faces)
        if (len(bm.faces) <= 200 and convex) or cell > .4: break
        bm.free(); cell *= 1.3
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); COLL.objects.link(o); o.display_type = 'WIRE'; return o

# ================================================================ setup
LAST = int(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else 8
bpy.ops.wm.open_mainfile(filepath=P('blend', 'vortexr_01_blockout.blend')); sc = bpy.context.scene; O = bpy.data.objects
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
MM = dict(M); MM.update({'TMP_' + k: tmp(k) for k in ('gloss_black', 'pocket', 'housing', 'satin_black', 'arch', 'mesh')})
WORK = coll('VX_WORK'); CUT = coll('VX_CUTTERS')
# ================================================================ 02 body: approved cage (tail-corner fairing refinement), crest crease, subdivision, real openings + panel gaps
TAIL_FIX = True                                                                                   # blockout tail-corner pinch: fair the last cage rings too (2 fixed instead of 4)
R2 = fair_lateral(fair_cage(RAW_RINGS, fixed=2)) if TAIL_FIX else rings
R2 = [[(x, y, z + .012 * (1 - ss(.13, .20, z))) for x, y, z in r] for r in R2]                    # floor points +12 mm: subdivided underside stays >= 0.10 m (road clearance)
REPORT['cage_tail_fairing'] = dict(max_shift_vs_blockout_mm=round(float(np.abs(np.array(R2) - np.array(rings)).max() * 1000), 1))
VB = [p for r in R2 for p in r]
for ri in (0, len(R2) - 1): VB.append(tuple(np.mean(np.array(R2[ri]), axis=0)))
TAGS2 = ['VX_Paint' if t == 'paint' else 'VX_Glass' if t == 'glass' else 'TMP_gloss_black' for t in TAGS]
def cage_obj(name):
    o = mk(name, VB, F, TAGS2, WORK, MM); bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free()
    cr = o.data.attributes.new('crease_edge', 'FLOAT', 'EDGE'); crest = set()
    for i in range(len(R2)):
        if -2.12 < R2[i][0][1] < 2.16:
            for j in (7, NR - 7): crest.add(i * NR + j)
    for e in o.data.edges:
        a_, b_ = e.vertices
        if a_ in crest and b_ in crest and abs(a_ - b_) == NR:
            ym_ = (VB[a_][1] + VB[b_][1]) / 2; cr.data[e.index].value = .62 * ss(-2.12, -1.80, ym_) * (1 - ss(1.40, 1.92, ym_))   # crease fades out at the nose / tail (no corner pinch)
    return o
hi = cage_obj('REF_HiRes'); subdiv(hi, 4)
BVH = BVHTree.FromObject(hi, bpy.context.evaluated_depsgraph_get())
from mathutils.kdtree import KDTree
hi.data.shade_smooth(); HN = [v.normal.copy() for v in hi.data.vertices]; KD = KDTree(len(hi.data.vertices))
for v in hi.data.vertices: KD.insert(v.co, v.index)
KD.balance()
def smooth_normal(co, fn):
    """interpolated smooth normal of the high-res limit surface near `co` (inverse-distance blend of the nearest vertex normals that face like `fn`)."""
    acc = Vector(); wsum = 0.0
    for c_, i_, d_ in KD.find_n(co, 8):
        n_ = HN[i_]
        if n_.dot(fn) < .35 or d_ > .03: continue
        w_ = 1.0 / (d_ + 1e-4); acc += n_ * w_; wsum += w_
    return acc.normalized() if wsum > 0 else None
def ray(o, d):
    loc, nrm, i, dist = BVH.ray_cast(Vector(o), Vector(d))
    if loc is None: return None, None
    if nrm.dot(Vector(d)) > 0: nrm = -nrm
    return loc, nrm
fhit = lambda x, z: ray((x, -4, z), (0, 1, 0)); rhit = lambda x, z: ray((x, 4, z), (0, -1, 0))
shit = lambda sx, y, z: ray((sx * 3, y, z), (-sx, 0, 0)); thit = lambda x, y: ray((x, y, 3), (0, 0, -1))
body = cage_obj('Body_Shell'); subdiv(body, 2)
def top_pocket(name, poly, depth, mat):
    outer, inner = [], []
    for x, y in poly:
        p, n = thit(x, y)
        if p is None: print('CUT MISS', name); return None
        outer.append((x, y, 3.0)); inner.append((p.x, p.y, p.z - depth))
    return solid(name, outer, inner, mat)
# wheel arches
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    R_ = r + .045; seg = 64; zc = r + .01
    outer = [(sx * 1.4, y + R_ * math.cos(2 * math.pi * k / seg), zc + R_ * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    solid(f'arch_{y}_{sx}', outer, [(sx * .55, py, pz) for _, py, pz in outer], 'arch')
# panel gaps: front lid (frunk), engine cover, doors
fence('gap_frunk', loop_top(sample_poly(rounded([(.56, -1.0), (.60, -1.55), (.50, -2.02), (-.50, -2.02), (-.60, -1.55), (-.56, -1.0)], [.03, .25, .10, .10, .25, .03], 6), .02)))
fence('gap_engine', loop_top(sample_poly(rounded([(.52, .80), (.60, 1.40), (.56, 2.06), (-.56, 2.06), (-.60, 1.40), (-.52, .80)], [.03, .25, .08, .08, .25, .03], 6), .02)))
for sx in (1, -1):
    DOOR = rounded([(-.93, .27), (.205, .27), (.205, ZBELT(.205) - .02), (-.86, ZBELT(-.86) - .018)], [.04, .03, .02, .02], 5)
    fence(f'gap_door_{sx}', loop_side(sx, sample_poly(DOOR, .02)))
# front openings: corner intakes, centre nose intake, boomerang headlamp housings
for sx in (1, -1):
    CI = rounded([(sx * .40, .43), (sx * .78, .50), (sx * .76, .20), (sx * .44, .19)], [.03, .04, .03, .03], 4)
    front_pocket(f'intake_{sx}', CI if sx > 0 else CI[::-1], .11, 'pocket')
    HL = rounded([(sx * .50, .528), (sx * .842, .604), (sx * .848, .515), (sx * .884, .518), (sx * .905, .668), (sx * .50, .562)], [.01, .006, .01, .01, .012, .01], 3)
    front_pocket(f'headlamp_{sx}', HL if sx > 0 else HL[::-1], .065, 'housing')
NOSEI = rounded([(-.30, .30), (.30, .30), (.24, .20), (-.24, .20)], .03, 4)
front_pocket('nose_intake', NOSEI[::-1], .09, 'pocket')
# hood vents (frunk extraction) + engine-cover louvre bay
for sx in (1, -1):
    HV = rounded([(sx * .14, -1.62), (sx * .40, -1.58), (sx * .42, -1.32), (sx * .18, -1.36)], .02, 4)
    top_pocket(f'hoodvent_{sx}', HV if sx > 0 else HV[::-1], .06, 'pocket')
top_pocket('louvres', rounded([(-.42, 1.0), (.42, 1.0), (.42, 1.62), (-.42, 1.62)], .03, 4), .05, 'pocket')
# side intakes: deep duct behind each door
for sx in (1, -1):
    SI = rounded([(.42, .60), (.90, .74), (.90, .33), (.48, .40)], [.03, .04, .04, .03], 4)
    side_pocket(f'sideintake_{sx}', SI, .13, 'pocket', sx)
# rear: light housings, connecting light channel, ventilation mesh bay, diffuser tunnel (opened from below)
for sx in (1, -1):
    TLH = rounded([(sx * .645, .835), (sx * .87, .84), (sx * .86, .63), (sx * .62, .63)], [.01, .02, .02, .01], 3)
    front_pocket(f'taillamp_{sx}', TLH if sx < 0 else TLH[::-1], .05, 'housing', rear=True)
front_pocket('tailthread', rounded([(-.62, .770), (.62, .770), (.62, .748), (-.62, .748)], .006, 2)[::-1], .02, 'housing', rear=True)
MESHP = rounded([(-.60, .725), (.60, .725), (.50, .43), (-.50, .43)], .03, 4)
front_pocket('rearmesh', MESHP[::-1], .09, 'pocket', rear=True)
def diff_z(y): return lerp(.108, .40, ss(1.62, 2.20, y) ** 1.25)
DY = [lerp(1.60, 2.40, k / 16) for k in range(17)]
outer = [(.80, y, diff_z(min(y, 2.2))) for y in DY] + [(-.80, y, diff_z(min(y, 2.2))) for y in DY[::-1]]
bmx = bmesh.new(); top_ = [bmx.verts.new(p) for p in outer]; bot_ = [bmx.verts.new((p[0], p[1], -.5)) for p in outer]; n_ = len(outer)
bmx.faces.new(top_); bmx.faces.new(bot_[::-1])
for i in range(n_): j = (i + 1) % n_; bmx.faces.new((top_[i], bot_[i], bot_[j], top_[j]))
bmesh.ops.recalc_face_normals(bmx, faces=bmx.faces); bmesh.ops.triangulate(bmx, faces=bmx.faces); me_ = bpy.data.meshes.new('diffcut'); bmx.to_mesh(me_); bmx.free(); me_.materials.append(MM['TMP_satin_black'])
CUT.objects.link(bpy.data.objects.new('diffuser_tunnel', me_))
def apply_cuts(o, cc):
    m_ = o.modifiers.new('cuts', 'BOOLEAN'); m_.operation = 'DIFFERENCE'; m_.solver = 'EXACT'; m_.operand_type = 'COLLECTION'; m_.collection = cc
    if hasattr(m_, 'material_mode'): m_.material_mode = 'TRANSFER'
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='cuts')
# LOD source without panel-gap grooves (decimating grooves smears their normals / leaves shards): same openings, no gaps
CUT_NG = coll('VX_CUTTERS_NOGAP')
for o in CUT.objects:
    if not o.name.startswith('gap_'): CUT_NG.objects.link(o)
body_ng = cage_obj('Body_NoGap'); subdiv(body_ng, 2); apply_cuts(body_ng, CUT_NG)
for o in list(CUT_NG.objects): CUT_NG.objects.unlink(o)
apply_cuts(body, CUT)
REPORT['cutters'] = sorted(o.name for o in CUT.objects)
for o in list(CUT.objects): bpy.data.objects.remove(o, do_unlink=True)
clean(body)
glass = split_by_material(body, {'VX_Glass'}, 'Glass_Shell'); clean(glass); clean(body)
remap_tmp(body); remap_tmp(glass); purge_slots(body); purge_slots(glass); skin_normals(body); skin_normals(glass)
g_ng = split_by_material(body_ng, {'VX_Glass'}, 'Glass_NoGap'); bpy.data.objects.remove(g_ng, do_unlink=True); clean(body_ng); remap_tmp(body_ng); purge_slots(body_ng)
REPORT['body_lod0_tris'] = tris(body)
save_ckp('vortexr_02_body_panels.blend') if LAST >= 2 else None
if LAST <= 2: sys.exit(0)
# ================================================================ 03 exterior details + lights
TR, LI = Geo(), Geo()
def ptat(hitf, a, b, depth):
    p, n = hitf(a, b); return None if p is None else p - n * depth
# ---- front: corner-intake carbon blades + vanes + inner mesh, nose-intake mesh, splitter with endplates + dive planes
for sx in (1, -1):
    for k in range(3):                                                                              # horizontal vanes across the corner intake
        z0 = .27 + .07 * k; xs = np.linspace(.45, .76, 10); A = []
        for x in xs:
            z = z0 + .07 * (x - .44) / .34 * .5; p, n = fhit(sx * x, z); A.append(Vector((sx * x, p.y + .02, z)))
        TR.strip([q - Vector((0, 0, .004)) for q in A], [q + Vector((0, 0, .004)) for q in A], 'VX_Carbon')
        TR.strip([q + Vector((0, 0, .004)) for q in A], [q + Vector((0, .05, .004)) for q in A], 'VX_Carbon')
    for xf in (.595,):                                                                              # vertical carbon blade
        zs = np.linspace(.20, .465, 8); A = []
        for z in zs:
            p, n = fhit(sx * xf, z); A.append(Vector((sx * xf, p.y + .004, z)))
        TR.strip([q - Vector((.004, 0, 0)) for q in A], [q + Vector((.004, 0, 0)) for q in A], 'VX_Carbon'); TR.strip([q + Vector((.004, 0, 0)) for q in A], [q + Vector((.004, .07, 0)) for q in A], 'VX_Carbon')
    # inner mesh back plate (diamond grid look via palette mesh swatch; the depth reads through the vanes)
    CI = rounded([(sx * .40, .43), (sx * .78, .50), (sx * .76, .20), (sx * .44, .19)], [.03, .04, .03, .03], 4)
    surf_patch(TR, CI, lambda a, b: (lambda pn: (pn[0] + Vector((0, .095, 0)), pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'VX_Palette:mesh', flip=sx < 0)
surf_patch(TR, NOSEI, lambda a, b: (lambda pn: (pn[0] + Vector((0, .075, 0)), pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'VX_Palette:mesh', flip=True)
for k in range(2):                                                                                  # nose-intake slats
    z = .235 + .035 * k; xs = np.linspace(-.25, .25, 13); A = []
    for x in xs:
        p, n = fhit(x, z); A.append(Vector((x, p.y + .012, z)))
    TR.strip([q - Vector((0, 0, .004)) for q in A], [q + Vector((0, 0, .004)) for q in A], 'VX_Carbon', flip=True)
xs = np.linspace(-.80, .80, 41); front = []
for x in xs:
    p, n = fhit(x, .175); front.append(Vector((x, (p.y if p else -2.2) - .035 - .02 * (1 - (x / .8) ** 2), .152)))
back = [Vector((x, -1.90, .152)) for x in xs]
TR.strip(back, front, 'VX_Carbon'); TR.strip([q - Vector((0, 0, .012)) for q in front], [q - Vector((0, 0, .012)) for q in back], 'VX_Carbon'); TR.strip(front, [q - Vector((0, 0, .012)) for q in front], 'VX_Carbon', flip=True)
for sx in (1, -1):
    x = sx * .80; p, n = fhit(x, .2); yf = p.y - .03                                              # splitter endplates
    TR.box((x, yf + .12, .19), (.004, .12, .04), 'VX_Carbon')
    p, n = shit(sx, -1.85, .30)                                                                     # dive plane on the front corner
    if p is not None:
        b0 = p + n * .002; TR.add([b0, b0 + Vector((sx * .055, -.03, .012)), b0 + Vector((sx * .055, .10, .02)), b0 + Vector((0, .14, .006))], [(0, 1, 2, 3) if sx > 0 else (3, 2, 1, 0)], 'VX_Carbon')
# ---- hood vents: carbon slats over the pocket
for sx in (1, -1):
    for k in range(4):
        y = lerp(-1.57, -1.39, k / 3); xs = np.linspace(.17 + .01 * k, .40 + .005 * k, 8); A = []
        for x in xs:
            p, n = thit(sx * x, y); A.append(Vector((sx * x, y, p.z - .012)))
        TR.strip([q - Vector((0, .007, 0)) for q in A], [q + Vector((0, .007, .0)) for q in A], 'VX_Carbon', flip=sx < 0)
        TR.strip([q + Vector((0, .007, 0)) for q in A], [q + Vector((0, .007, -.03)) for q in A], 'VX_Carbon', flip=sx < 0)
# ---- engine-cover louvres (6 gloss-black slats in the bay)
for k in range(6):
    y = 1.06 + .095 * k; xs = np.linspace(-.40, .40, 17); A = []
    for x in xs:
        p, n = thit(x, y); A.append(Vector((x, y, p.z - .01)))
    TR.strip([q - Vector((0, .02, 0)) for q in A], [q + Vector((0, .02, .0)) for q in A], 'VX_Palette:gloss_black')
    TR.strip([q + Vector((0, .02, 0)) for q in A], [q + Vector((0, .02, -.035)) for q in A], 'VX_Palette:gloss_black')
# ---- side: intake splitter blade + internal duct floor, carbon rocker blade
for sx in (1, -1):
    ys = np.linspace(.36, .46, 4); zs = np.linspace(.34, .62, 6)
    rows = [[(lambda p: p + Vector((-sx * .004, 0, 0)) if p is not None else None)(shit(sx, y + (.06 * (z - .34) / .28), z)[0]) for y in ys] for z in zs]
    if all(p is not None for r in rows for p in r): TR.grid(rows, 'VX_Carbon', flip=sx > 0)
    ys = np.linspace(-.92, .98, 40); A, B = [], []
    for y in ys:
        p, n = shit(sx, y, .24)
        if p is None: continue
        A.append(p + n * .006 + Vector((0, 0, -.018))); B.append(p + n * .006 + Vector((0, 0, .018)))
    TR.strip(A, B, 'VX_Carbon', flip=sx > 0); TR.strip(B, [q + Vector((sx * .03, 0, -.012)) for q in B], 'VX_Carbon', flip=sx > 0); TR.strip([q + Vector((sx * .03, 0, -.012)) for q in B], A, 'VX_Carbon', flip=sx > 0)
# ---- rear: ventilation mesh (diamond lattice bars), twin exhaust, diffuser + strakes, swan-neck wing
dpt = .085
for k in range(-9, 10):                                                                            # diagonal lattice in the mesh bay
    for d in (1, -1):
        pts = []
        for t in np.linspace(0, 1, 7):
            x = k * .065 + d * lerp(-.15, .15, t); z = lerp(.44, .715, t)
            if abs(x) > lerp(.50, .60, (z - .43) / .295) - .01: continue
            p, n = rhit(x, z); pts.append(Vector((x, p.y - dpt * .5, z)) if p is not None else None)
        pts = [p for p in pts if p is not None]
        if len(pts) >= 2: TR.strip([q - Vector((.0035, 0, 0)) for q in pts], [q + Vector((.0035, 0, 0)) for q in pts], 'VX_Palette:mesh')
for cx in (-.11, .11):
    seg = 24; p, n = rhit(cx, .52); y0 = p.y - .002; cz = .52
    ell = lambda rx, rz, y: [Vector((cx + rx * math.cos(2 * math.pi * k / seg), y, cz + rz * math.sin(2 * math.pi * k / seg))) for k in range(seg)]
    TR.strip(ell(.056, .046, y0 - .11), ell(.056, .046, y0 + .022), 'VX_Palette:exhaust', closed=True); TR.strip(ell(.056, .046, y0 + .022), ell(.047, .038, y0 + .022), 'VX_Palette:exhaust', closed=True)
    TR.strip(ell(.047, .038, y0 + .022), ell(.047, .038, y0 - .07), 'VX_Palette:exhaust_inner', closed=True)
    n0 = len(TR.V); TR.V += [tuple(v) for v in ell(.047, .038, y0 - .07)] + [(cx, y0 - .07, cz)]
    for k in range(seg): TR.F.append((n0 + k, n0 + (k + 1) % seg, n0 + seg)); TR.T.append('VX_Palette:exhaust_inner')
xs = list(np.linspace(-.80, .80, 25)); ys = list(np.linspace(1.62, 2.22, 12))
TR.grid([[Vector((x, y, diff_z(y))) for x in xs] for y in ys], 'VX_Carbon', flip=True)
for xf in (-.62, -.36, -.12, .12, .36, .62, -.80, .80):
    top = [Vector((xf, y, diff_z(y) - .001)) for y in ys]; bot = [Vector((xf, y, max(.115, ZFLOOR(y) - .005))) for y in ys]        # vertical plates down to the body underside (stay inside the silhouette)
    w = .005 if abs(xf) < .7 else .008
    for off in (-w, w): TR.strip([q + Vector((off, 0, 0)) for q in top], [q + Vector((off, 0, 0)) for q in bot], 'VX_Carbon', flip=off > 0)
    TR.strip([q - Vector((w, 0, 0)) for q in bot], [q + Vector((w, 0, 0)) for q in bot], 'VX_Carbon')
wing_y, wing_z = 1.98, 1.205
for sx in (1, -1):                                                                                  # swan-neck pylons: tapered blade sections, hook over the wing top
    base = thit(sx * .40, 1.80)[0]; secs = []
    for t in np.linspace(0, 1, 12):
        y = lerp(1.80, wing_y + .05, t); z = lerp(base.z - .01, wing_z + .045, ss(0, .82, t)) + .035 * math.sin(math.pi * t); ch = lerp(.08, .05, t); th = lerp(.016, .010, t)
        secs.append([Vector((sx * .40 - th, y - ch / 2, z)), Vector((sx * .40 + th, y - ch / 2, z)), Vector((sx * .40 + th, y + ch / 2, z)), Vector((sx * .40 - th, y + ch / 2, z))])
    for A, B in zip(secs, secs[1:]): TR.strip(A, B, 'VX_Carbon', closed=True)
af = [(0.0, 0.0), (.03, .014), (.08, .024), (.15, .028), (.23, .020), (.30, .004), (.23, -.002), (.15, -.006), (.08, -.006), (.03, -.004)]
xsw = list(np.linspace(-.86, .86, 31)); ring_w = []
for x in xsw:
    tip = ss(.70, .86, abs(x)); ring_w.append([Vector((x, wing_y - .14 + c, wing_z + z + .02 * tip)) for c, z in af])
for A, B in zip(ring_w, ring_w[1:]): TR.strip(A, B, 'VX_Carbon', closed=True)
for x in (-.86, .86):
    s_ = 1 if x > 0 else -1; plate = [Vector((x, wing_y - .21, wing_z - .075)), Vector((x, wing_y + .19, wing_z - .085)), Vector((x, wing_y + .21, wing_z + .07)), Vector((x, wing_y - .18, wing_z + .06))]
    TR.add(plate + [q + Vector((s_ * .006, 0, 0)) for q in plate], [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)] if s_ > 0 else [(3, 2, 1, 0), (4, 5, 6, 7), (1, 5, 4, 0), (2, 6, 5, 1), (3, 7, 6, 2), (0, 4, 7, 3)], 'VX_Carbon')
# ---- wheel-well liners
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    R_ = r + .043; zc = r + .01; seg = 28; a0, a1 = math.radians(-25), math.radians(205)
    arc = [(y + R_ * math.cos(lerp(a0, a1, q / seg)), zc + R_ * math.sin(lerp(a0, a1, q / seg))) for q in range(seg + 1)]
    xi, xo = sx * .55, sx * (WMAX(y) - .015)
    TR.strip([Vector((xi, yy, zz)) for yy, zz in arc], [Vector((xo, yy, zz)) for yy, zz in arc], 'VX_Palette:satin_black', flip=sx > 0)
    n0 = len(TR.V); TR.V += [(xi, yy, zz) for yy, zz in arc] + [(xi, y, .14)]
    for q in range(seg): f = (n0 + q, n0 + q + 1, n0 + seg + 1); TR.F.append(f if sx < 0 else f[::-1]); TR.T.append('VX_Palette:satin_black')
# ---- LIGHTS: boomerang headlamps (DRL blade + hook, 3 projector modules, amber indicator, clear lens)
for sx in (1, -1):
    fl = sx < 0
    def hb(u, v, d):                                                                               # blade: u 0 inner .. 1 outer, v 0 bottom .. 1 top
        x = lerp(.52, .88, u); zb = lerp(.535, .615, u); zt = lerp(.556, .652, u); return ptat(fhit, sx * x, lerp(zb, zt, v), -d)
    LI.grid([[hb(u, v, .012) for u in np.linspace(.0, 1, 24)] for v in (.62, .92)], 'VX_LED_DRL', flip=fl)
    LI.grid([[ptat(fhit, sx * lerp(.851, .876, u), lerp(.525, .62, v), -.012) for u in (0, 1)] for v in np.linspace(0, 1, 6)], 'VX_LED_DRL', flip=fl)
    LI.grid([[hb(u, v, .014) for u in np.linspace(.62, .80, 6)] for v in (.15, .48)], 'VX_LED_Indicator_L' if sx > 0 else 'VX_LED_Indicator_R', flip=fl)
    for u in (.12, .28, .44):                                                                       # compact LED projector modules
        c0 = hb(u, .30, .0); seg = 16; r = .013
        ring = lambda dy, rr: [Vector((c0.x + rr * math.cos(2 * math.pi * q / seg), c0.y + dy, c0.z + rr * math.sin(2 * math.pi * q / seg))) for q in range(seg)]
        LI.strip(ring(.045, r), ring(.012, r), 'VX_Palette:housing', closed=True); LI.strip(ring(.012, r), ring(.009, r * .75), 'VX_Palette:reflector', closed=True)
        n0 = len(LI.V); LI.V += [tuple(v) for v in ring(.009, r * .75)] + [(c0.x, c0.y + .007, c0.z)]
        for q in range(seg): LI.F.append((n0 + q, n0 + (q + 1) % seg, n0 + seg)); LI.T.append('VX_LED_Headlamp')
    HL = rounded([(sx * .50, .528), (sx * .842, .604), (sx * .848, .515), (sx * .884, .518), (sx * .905, .668), (sx * .50, .562)], [.01, .006, .01, .01, .012, .01], 3)
    surf_patch(LI, HL, fhit, .0012, 'VX_LensClear', flip=None)
# ---- LIGHTS: rear — three raked tail slashes per side, brake bar, amber indicator, reverse, thin connecting tail thread, smoked-red lens; third brake light on the wing
for sx in (1, -1):
    fl = sx < 0
    for k in range(3):
        x0 = .66 + .065 * k; z0 = .82 - .012 * k
        quad = [(sx * x0, z0), (sx * (x0 + .05), z0 + .012), (sx * (x0 + .02), z0 - .14), (sx * (x0 - .03), z0 - .152)]
        rows = [[ptat(rhit, lerp(lerp(quad[0][0], quad[1][0], u), lerp(quad[3][0], quad[2][0], u), v), lerp(lerp(quad[0][1], quad[1][1], u), lerp(quad[3][1], quad[2][1], u), v), .016) for u in (0, .5, 1)] for v in np.linspace(0, 1, 5)]
        LI.grid(rows, 'VX_LED_Tail', flip=fl)
    LI.grid([[ptat(rhit, sx * x, z, .018) for x in np.linspace(.64, .855, 8)] for z in (.648, .668)], 'VX_LED_Brake', flip=fl)
    LI.grid([[ptat(rhit, sx * x, z, .018) for x in np.linspace(.75, .855, 5)] for z in (.636, .646)], 'VX_LED_Indicator_L' if sx > 0 else 'VX_LED_Indicator_R', flip=fl)
    LI.grid([[ptat(rhit, sx * x, z, .018) for x in np.linspace(.64, .74, 4)] for z in (.636, .646)], 'VX_LED_Reverse', flip=fl)
    TLH = rounded([(sx * .645, .835), (sx * .87, .84), (sx * .86, .63), (sx * .62, .63)], [.01, .02, .02, .01], 3)
    surf_patch(LI, TLH, rhit, -.0012, 'VX_LensRed', flip=None)
LI.grid([[ptat(rhit, x, z, .012) for x in np.linspace(-.61, .61, 50)] for z in (.754, .764)], 'VX_LED_Tail')
LI.grid([[ptat(rhit, x, z, -.0012) for x in np.linspace(-.62, .62, 50)] for z in (.748, .770)], 'VX_LensRed')
LI.grid([[Vector((x, wing_y + .155, wing_z + z)) for x in np.linspace(-.13, .13, 7)] for z in (.002, .014)], 'VX_LED_Brake')     # third brake light (wing trailing edge)
trim = mk('Trim_LOD0', TR.V, TR.F, TR.T, WORK, M); lights = mk('Lights_LOD0', LI.V, LI.F, LI.T, WORK, M)
for o in (trim, lights): clean(o); orient_components(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(35))
# ---- mirrors: aero pod (teardrop, flat glass face) on a twin-blade carbon stalk -> part of the body
MI = Geo()
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=24, v_segments=14, radius=1.0)
    for v in bmm.verts:
        x, y, z = v.co; y = y * (1.0 if y < 0 else .40); z = z * (1 - .30 * max(0, -y))
        v.co = Vector((x * .10, y * .095, z * .044)) + Vector((sx * 1.035, -.62, .91))
    bmm.normal_update(); vs = [tuple(v.co) for v in bmm.verts]; fs = [tuple(v.index for v in f.verts) for f in bmm.faces]
    ts = ['VX_Palette:mirror' if f.normal.y > .7 else 'VX_Paint' for f in bmm.faces]; bmm.free(); MI.add(vs, fs, ts)
    for dz in (0.0, .028):
        Vs = [(sx * .88, -.70, .835 + dz), (sx * .88, -.62, .835 + dz), (sx * 1.0, -.60, .895 + dz * .5), (sx * 1.0, -.66, .895 + dz * .5)]
        MI.add(Vs + [(x, y, z + .008) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'VX_Carbon')
mirrors = mk('Mirrors', MI.V, MI.F, MI.T, WORK, M)
bm = bmesh.new(); bm.from_mesh(mirrors.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(mirrors.data); bm.free(); mirrors.data.shade_smooth()
REPORT['trim_tris'], REPORT['lights_tris'] = tris(trim), tris(lights)
save_ckp('vortexr_03_details_lights.blend') if LAST >= 3 else None
# ================================================================ 04 wheels: dark forged 10-spoke (5 swept Y-pairs), 20" / 21", big rotors, acid-green calipers
WREF = {'FL': Vector((XF, YF, RF)), 'FR': Vector((-XF, YF, RF)), 'RL': Vector((XR, YR, RR)), 'RR': Vector((-XR, YR, RR))}
WSPEC = {'FL': (RF, WF, .254), 'FR': (RF, WF, .254), 'RL': (RR, WR, .267), 'RR': (RR, WR, .267)}
LOD_SEG = {0: (96, 64), 1: (48, 36), 2: (28, 20), 3: (16, 12)}
def build_wheel(c, k, coll_):
    R, W, rr = WSPEC[c]; sx = 1 if c[1] == 'L' else -1; hw = W / 2; seg_t, seg_r = LOD_SEG[k]; out = {}
    prof = [(-hw * .80, rr + .006), (-hw * .96, rr + .028), (-hw, R * .82), (-hw * .985, R * .91), (-hw * .93, R * .97), (-hw * .80, R * .997), (-hw * .40, R), (0, R),
            (hw * .40, R), (hw * .80, R * .997), (hw * .93, R * .97), (hw * .985, R * .91), (hw, R * .82), (hw * .96, rr + .028), (hw * .80, rr + .006)]
    if k >= 2: prof = [prof[i] for i in (0, 2, 4, 6, 8, 10, 12, 14)]
    Vt, Ft, UVt = revolve(prof, seg_t, sx); g = Geo(); g.add(Vt, Ft, 'VX_Tire'); tire = mk(f'Tire_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    uvl = tire.data.uv_layers.new(name='tireUV')
    for p in tire.data.polygons:
        for li in p.loop_indices: uvl.data[li].uv = UVt[tire.data.loops[li].vertex_index]
    out['Tire'] = tire
    g = Geo(); face = hw * .58
    lip = [(hw * .84, rr - .024), (hw * .90, rr + .004), (hw * .78, rr + .010), (hw * .68, rr - .016)]
    Vl, Fl, _ = revolve(lip, seg_r, sx); g.add(Vl, Fl, 'VX_Palette:wheel_lip')
    barrel = [(hw * .68, rr - .016), (hw * .20, rr - .028), (-hw * .70, rr - .030), (-hw * .82, rr + .004)]
    Vb, Fb, _ = revolve(barrel, seg_r, sx); g.add(Vb, Fb, 'VX_Palette:wheel_forged')
    nt_ = 9 if k == 0 else 5 if k == 1 else 3
    for s_ in range(5):
        for side_ in (-1, 1):
            a_in = 2 * math.pi * s_ / 5; a_out = a_in + side_ * .30; secs = []
            for t in np.linspace(0, 1, nt_):
                r_ = lerp(.07, rr - .02, t); a = lerp(a_in + side_ * .03, a_out, t ** 1.4); w = lerp(.026, .016, t); xx = face - .022 * math.sin(math.pi * t)
                Rm = Matrix.Rotation(a, 3, 'X')
                secs.append([Rm @ Vector((sx * (xx + .004), -w, r_)), Rm @ Vector((sx * (xx + .004), w, r_)), Rm @ Vector((sx * (xx - .018), w * 1.12, r_)), Rm @ Vector((sx * (xx - .018), -w * 1.12, r_))])
            for A, B in zip(secs, secs[1:]): g.strip(A, B, 'VX_Palette:wheel_forged', closed=True, flip=sx < 0)
            g.add(secs[-1], [(0, 1, 2, 3) if sx > 0 else (3, 2, 1, 0)], 'VX_Palette:wheel_forged')
    hub = [(face + .006, 0.0), (face + .006, .030), (face + .002, .048), (face - .006, .07), (face - .02, .072)]
    Vh, Fh, _ = revolve(hub, max(12, seg_r // 2), sx); g.add(Vh, Fh, 'VX_Palette:wheel_forged')
    if k <= 1:
        for s_ in range(5):
            a = 2 * math.pi * (s_ + .5) / 5; cy, cz = .042 * math.cos(a), .042 * math.sin(a); hx = [(cy + .0075 * math.cos(2 * math.pi * q / 6), cz + .0075 * math.sin(2 * math.pi * q / 6)) for q in range(6)]
            A = [Vector((sx * (face + .004), y, z)) for y, z in hx]; B = [Vector((sx * (face + .016), y, z)) for y, z in hx]
            g.strip(A, B, 'VX_Palette:wheel_lip', closed=True, flip=sx < 0); g.add(B, [tuple(range(6)) if sx > 0 else tuple(range(5, -1, -1))], 'VX_Palette:wheel_lip')
        Vc, Fc, _ = revolve([(face + .010, 0.0), (face + .010, .020), (face + .006, .026)], 16, sx); g.add(Vc, Fc, 'VX_Palette:accent_green')
    if k == 3:
        Vd, Fd, _ = revolve([(-hw * .1, .06), (-hw * .1, rr - .05)], 12, sx); g.add(Vd, Fd, 'VX_Palette:rotor')
    out['Wheel'] = mk(f'Wheel_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    if k <= 2:
        g = Geo(); rd = rr - .035
        Vd, Fd, _ = revolve([(hw * .05, .085), (hw * .05, rd), (-hw * .10, rd), (-hw * .10, .085)], seg_r, sx); g.add(Vd, Fd, 'VX_Palette:rotor')
        Vh, Fh, _ = revolve([(hw * .30, .0), (hw * .30, .085), (hw * .05, .085)], max(12, seg_r // 2), sx); g.add(Vh, Fh, 'VX_Palette:rotor_hat')
        out['BrakeDisc'] = mk(f'BrakeDisc_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
        g = Geo(); n_ = {0: 12, 1: 8, 2: 4}[k]; r0, r1 = rd - .06, rd + .012; front = c[0] == 'F'
        a0, a1 = (math.radians(32), math.radians(108)) if front else (math.radians(72), math.radians(148))
        secs = []
        for q in range(n_ + 1):
            a = lerp(a0, a1, q / n_); ca, sa = math.cos(a) * (1 if front else -1), math.sin(a); bul = .006 * math.sin(math.pi * q / n_)
            pts = [(r0, sx * (hw * .22 + bul)), (r1, sx * (hw * .22 + bul)), (r1 + .006, sx * (hw * .05)), (r1, -sx * (hw * .30 + bul)), (r0, -sx * (hw * .30 + bul)), (r0 - .006, sx * (-hw * .05))]
            secs.append([Vector((xx, rr_ * ca, rr_ * sa)) for rr_, xx in pts])
        for A, B in zip(secs, secs[1:]): g.strip(A, B, 'VX_Palette:caliper_green', closed=True)
        g.add(secs[0], [tuple(range(6))], 'VX_Palette:caliper_green'); g.add(secs[-1], [tuple(range(5, -1, -1))], 'VX_Palette:caliper_green')
        out['Caliper'] = mk(f'Caliper_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    for key, o in out.items():
        bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
        if key == 'Caliper': bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(o.data); bm.free(); clean(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40 if key != 'Tire' else 60))
        o.data.transform(Matrix.Translation(WREF[c])); set_origin(o, WREF[c])
    return out
WH = coll('VX_WHEELS'); ASM = {}
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key, o in build_wheel(c, k, WH).items(): ASM[(k, c, key)] = o
save_ckp('vortexr_04_wheels.blend') if LAST >= 4 else None
# ================================================================ 05 interior: track cockpit (LHD, driver on +X)
IN, ST = Geo(), Geo()
for sx in (1, -1):
    xs_ = sx * .36; tilt = Matrix.Rotation(-.40, 3, 'X')
    rbox(IN, (xs_, .06, .27), (.20, .23, .045), 'VX_Palette:alcantara', .025)                         # race-seat cushion
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .185, .06, .33), (.035, .22, .07), 'VX_Palette:leather_black', .02)
    rbox(IN, (xs_, .30, .58), (.19, .05, .30), 'VX_Palette:alcantara', .03, tilt)                     # shell backrest
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .185, .27, .57), (.04, .07, .29), 'VX_Palette:leather_black', .02, tilt)
    rbox(IN, (xs_, .26, .56), (.045, .052, .27), 'VX_Palette:accent_green', .015, tilt)               # acid-green centre stripe
    for hx in (-.075, .075): rbox(IN, (xs_ + hx, .22, .56), (.022, .053, .28), 'VX_Palette:harness', .01, tilt)   # harness straps
    rbox(IN, (sx * .745, -.30, .52), (.022, .48, .17), 'VX_Palette:alcantara', .02)                    # door trim
    rbox(IN, (sx * .72, -.30, .62), (.02, .32, .018), 'VX_Palette:carbon' if False else 'VX_Palette:int_trim', .01)
    rbox(IN, (sx * .725, -.55, .50), (.006, .03, .03), 'VX_Palette:accent_green', .004)                  # door pull loop
rbox(IN, (0, -.62, .66), (.66, .12, .05), 'VX_Palette:alcantara', .04)                                # wraparound dash
rbox(IN, (0, -.54, .60), (.64, .05, .06), 'VX_Palette:int_trim', .025)
rbox(IN, (.36, -.53, .735), (.14, .05, .025), 'VX_Palette:leather_black', .02)                        # cluster binnacle
rbox(IN, (.36, -.488, .70), (.12, .006, .035), 'VX_Display', .004)                                    # digital instrument cluster
rbox(IN, (0, -.30, .40), (.11, .40, .11), 'VX_Palette:int_trim', .03)                                 # centre console (tunnel)
rbox(IN, (0, -.42, .52), (.08, .10, .012), 'VX_Palette:aluminium', .008)                              # switch panel
for k_ in range(4): rbox(IN, (-.045 + .03 * k_, -.40, .535), (.008, .01, .008), 'VX_Palette:accent_green' if k_ == 0 else 'VX_Palette:aluminium', .003)
rbox(IN, (0, .20, .12), (.80, .78, .02), 'VX_Palette:carpet', .01)                                    # floor
rbox(IN, (0, .50, .66), (.70, .03, .32), 'VX_Palette:int_trim', .02)                                   # rear engine bulkhead
rbox(IN, (0, .48, .80), (.24, .006, .10), 'VX_Glass' if False else 'VX_Palette:gloss_black', .004)   # bulkhead window frame
hl_rows = []
for y in np.linspace(-.75, .55, 16):
    row = []
    for x in np.linspace(-.42, .42, 13):
        p, n = thit(x, y); row.append((p - n * .012) if p is not None and p.z > .95 else None)
    hl_rows.append(row)
hl_rows = [r for r in hl_rows if all(p is not None for p in r)]
IN.grid(hl_rows, 'VX_Palette:alcantara', flip=True)                                                  # headliner
interior = mk('Interior_LOD0', IN.V, IN.F, IN.T, WORK, M)
hubc = Vector((.36, -.30, .66)); tilt = Matrix.Rotation(math.radians(-72), 3, 'X'); seg, sg2 = 32, 10
for q in range(seg):                                                                                  # flat-bottom race wheel
    a0, a1 = 2 * math.pi * q / seg, 2 * math.pi * (q + 1) / seg
    def ring(a):
        rx = .165; rz = .165 if math.sin(a) > -.55 else .165 * .55 / max(.55, -math.sin(a)) * 1.0
        cx_, cz_ = rx * math.cos(a), max(rz * math.sin(a), -.11)
        return [hubc + tilt @ Vector((cx_ + .016 * math.cos(2 * math.pi * k / sg2) * math.cos(a), .016 * math.sin(2 * math.pi * k / sg2), cz_ + .016 * math.cos(2 * math.pi * k / sg2) * math.sin(a))) for k in range(sg2)]
    ST.strip(ring(a0), ring(a1), 'VX_Palette:alcantara', closed=True)
rbox(ST, tuple(hubc + tilt @ Vector((0, 0, .158))), (.012, .02, .012), 'VX_Palette:accent_green', .005, tilt)    # 12-o'clock marker
for a in (0, math.pi, -math.pi / 2):
    rbox(ST, tuple(hubc + tilt @ Vector((.095 * math.cos(a), 0, .095 * math.sin(a)))), (.07 if a != -math.pi / 2 else .016, .012, .016 if a != -math.pi / 2 else .06), 'VX_Palette:int_trim', .006, tilt)
rbox(ST, tuple(hubc + tilt @ Vector((0, .014, 0))), (.06, .026, .045), 'VX_Palette:leather_black', .02, tilt)
rbox(ST, tuple(hubc + tilt @ Vector((0, .04, .02))), (.05, .004, .02), 'VX_Display', .003, tilt)                  # wheel display
steer = mk('SteeringWheel_LOD0', ST.V, ST.F, ST.T, WORK, M); set_origin(steer, hubc)
for o in (interior, steer):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); clean(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40))
REPORT['interior_tris'] = tris(interior) + tris(steer)
save_ckp('vortexr_05_interior.blend') if LAST >= 5 else None
# ================================================================ 06 merge + UVs
L0 = coll('LOD0_PARTS')
mir_ng = mirrors.copy(); mir_ng.data = mirrors.data.copy(); WORK.objects.link(mir_ng)
body_lodsrc = join([body_ng, mir_ng], 'Body_LODSource', WORK); final_uvs(body_lodsrc)
body_final = join([body, mirrors], 'Body_LOD0', L0)
glass.name = glass.data.name = 'Glass_LOD0'; link_only(glass, L0)
for o in (trim, lights, interior, steer): link_only(o, L0)
FINAL0 = {n: O[n] for n in ('Body_LOD0', 'Glass_LOD0', 'Trim_LOD0', 'Lights_LOD0', 'Interior_LOD0')}
for o in [x for x in O if x.type == 'MESH']: purge_slots(o); final_uvs(o)
T0_ = {o.name: tris(o) for o in O if o.type == 'MESH' and o.name.endswith('_LOD0')}; REPORT['lod0_parts'] = T0_; REPORT['lod0_total'] = sum(T0_.values())
print('LOD0', REPORT['lod0_total'], {k: v for k, v in T0_.items() if not k.startswith(('Tire', 'Wheel', 'Brake', 'Caliper'))}, flush=True)
save_ckp('vortexr_06_materials_uv.blend') if LAST >= 6 else None
# ================================================================ 07 LODs
RK = {1: {'Body': .50, 'Glass': .7, 'Trim': .45, 'Lights': .5, 'Interior': .45, 'SteeringWheel': .5},
      2: {'Body': .24, 'Glass': .45, 'Trim': .18, 'Lights': .22, 'Interior': .18, 'SteeringWheel': .2},
      3: {'Body': .09, 'Glass': .18, 'Trim': .06, 'Lights': .08, 'Interior': .04}}
RK[1]['Body'] = .54; RK[2]['Body'] = .26; RK[3]['Body'] = .095                                     # relative to the no-gap LOD source
for k in (1, 2, 3):
    Lk = coll(f'LOD{k}_PARTS')
    for n0, o0 in list(FINAL0.items()) + [('SteeringWheel_LOD0', steer)]:
        kind = n0.split('_')[0]
        if kind not in RK[k]: continue
        src_ = body_lodsrc if kind == 'Body' else o0
        d = src_.copy(); d.data = src_.data.copy(); Lk.objects.link(d); d.name = n0.replace('LOD0', f'LOD{k}'); d.data.name = d.name
        if kind == 'Body':
            decimate(d, RK[k][kind], transfer=False); skin_normals(d)                                  # smooth high-res body normals re-projected (crisp openings stay flat)
        else: decimate(d, RK[k][kind], ref=o0, transfer=k <= 1)
        final_uvs(d)
bpy.data.objects.remove(body_lodsrc, do_unlink=True); bpy.data.objects.remove(hi, do_unlink=True)
REPORT['lod_ratios'] = RK
save_ckp('vortexr_07_lods.blend') if LAST >= 7 else None
# ================================================================ 08 colliders, hierarchy, pivots, references
FIN = coll('VORTEX_R'); COLL = coll('VX_COLLIDERS', FIN)
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
pts = [O[f'{n}_LOD2'].matrix_world @ v.co for n in ('Body', 'Glass') for v in O[f'{n}_LOD2'].data.vertices]
CL = {'Collision_Front': [p for p in pts if p.y < -.95 and p.z < .90], 'Collision_Body': [p for p in pts if -1.10 < p.y < 1.20 and p.z < .80],
      'Collision_Cabin': [p for p in pts if -.95 < p.y < .80 and p.z > .74], 'Collision_Rear': [p for p in pts if p.y > 1.0 and p.z < 1.0]}
CL['Collision_Wing'] = [O['Trim_LOD2'].matrix_world @ v.co for v in O['Trim_LOD2'].data.vertices if (O['Trim_LOD2'].matrix_world @ v.co).z > 1.05]   # fixed rear wing
cr = empty('Collision', FIN, (0, 0, 0), root, 'PLAIN_AXES', .2)
for n, vs in CL.items():
    if len(vs) > 8: h = hull(n, vs); h.parent = cr
for c in ('FL', 'FR', 'RL', 'RR'):
    e = empty(f'WheelColliderRef_{c}', FIN, WREF[c], root, 'SPHERE', .1); e['radius_m'] = WSPEC[c][0]; e['width_m'] = WF if c[0] == 'F' else WR
empty('CenterOfMass', FIN, (0, .25, .38), root, 'SPHERE', .08)                                  # mid-engine: centreline, low, rear-biased
for c in list(bpy.data.collections):
    if c.name not in ('VORTEX_R', 'VX_COLLIDERS'):
        for o in list(c.objects):
            if o.name not in FIN.all_objects: bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
json.dump(REPORT, open(os.path.join(REPD(), 'VX_build_log.json'), 'w'), indent=1)
save_ckp('vortexr_08_colliders_hierarchy.blend') if LAST >= 8 else None
