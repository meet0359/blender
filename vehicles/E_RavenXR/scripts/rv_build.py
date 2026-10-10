# Raven XR (Phase E) production build. Blender -b --factory-startup --python rv_build.py [-- <last stage 2..8>]
# Starts from the APPROVED blockout design (identical design code via rv_lib) + the approved P0 refinements; writes ravenxr_02 .. 08 (never overwrites 01_blockout).
#  02 body (P0 cage, creases, subdivision, real openings, panel gaps, diffuser tunnel)  03 exterior details + lights  04 wheels  05 interior
#  06 merge + UVs  07 LODs (groove-free body source)  08 colliders, hierarchy, pivots, references
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from rv_lib import *
# ---- generic production helpers (copied from the frozen Titan GT build; read-only source, renamed TG -> VX -> RV)
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
    """TMP_<swatch> -> RV_Palette + swatch attribute."""
    me = o.data; names = [m.name for m in me.materials]; idx = [p.material_index for p in me.polygons]
    tg = [(n[4:] if n.startswith('TMP_') else None) for n in names]; final = [('RV_Palette' if t else n) for n, t in zip(names, tg)]
    order = list(dict.fromkeys(final)); me.materials.clear()
    for n in order: me.materials.append(M[n])
    me.polygons.foreach_set('material_index', [order.index(final[i]) for i in idx])
    a = me.attributes.get('swatch') or me.attributes.new('swatch', 'INT', 'FACE')
    a.data.foreach_set('value', [SWATCH.index('pocket' if tg[i] == 'arch' else tg[i]) if tg[i] else 0 for i in idx])
    if any(t == 'arch' for t in tg):
        for p in me.polygons:
            if tg[idx[p.index]] == 'arch': a.data[p.index].value = SWATCH.index('satin_black')

def skin_normals(o, skin_names=('RV_Paint', 'RV_Glass'), skin_swatches=('gloss_black',)):
    """loop normals: skin faces take the smooth high-resolution body normal; cut / pocket / gap faces stay flat (crisp edges)."""
    me = o.data; me.shade_smooth(); sw = me.attributes.get('swatch'); out = []
    for p in me.polygons:
        m = me.materials[p.material_index].name if me.materials[p.material_index] else ''
        skin = m in skin_names or (m == 'RV_Palette' and sw and SWATCH[sw.data[p.index].value] in skin_swatches)
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

# ================================================================ setup
LAST = int(sys.argv[sys.argv.index('--') + 1]) if '--' in sys.argv else 8
bpy.ops.wm.open_mainfile(filepath=P('blend', 'ravenxr_01_blockout.blend')); sc = bpy.context.scene; O = bpy.data.objects   # approved blockout (read; never saved back)
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
WORK = coll('RV_WORK'); CUT = coll('RV_CUTTERS')
# ================================================================ 02 body: approved cage + P0 refinements (sail-to-deck, sharpening creases), subdivision, real openings + panel gaps
R2 = fair_lateral(fair_cage(RAW_P0, fixed=2))                                                     # tail rings faired too (Vortex R tail-corner lesson)
R2 = [[(x, y, z + .008 * (1 - ss(.14, .22, z))) for x, y, z in r] for r in R2]                    # floor points +8 mm: subdivided underside stays >= 0.10 m
REPORT['cage_vs_blockout_max_shift_mm'] = round(float(np.abs(np.array(R2) - np.array(rings)).max() * 1000), 1)
VB = [p for r in R2 for p in r]
for ri in (0, len(R2) - 1): VB.append(tuple(np.mean(np.array(R2[ri]), axis=0)))
TAGS2 = []
for t, tg in zip(FT, TAGS):
    if tg == 'paint' and t[0] != 'cap' and (t[1], t[2]) == (10, 11) and CAB(t[0]) >= .5 and -.46 < t[0] < 1.48: tg = 'black'   # A-pillars + roof-rail trim: gloss black (roof stays body colour)
    TAGS2.append('RV_Paint' if tg == 'paint' else 'RV_Glass' if tg == 'glass' else 'TMP_gloss_black')
def cage_obj(name):
    o = mk(name, VB, F, TAGS2, WORK, MM); bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free()
    cr = o.data.attributes.new('crease_edge', 'FLOAT', 'EDGE'); n_ = len(R2)
    crest = {i * NR + j for i in range(n_) for j in (7, NR - 7)}
    rail = {i * NR + j for i in range(n_) if -.42 < R2[i][0][1] < 1.42 for j in (I_ROOF, NR - I_ROOF)}
    for e in o.data.edges:
        a_, b_ = e.vertices
        if a_ >= n_ * NR or b_ >= n_ * NR: continue
        ia, ja = divmod(a_, NR); ib, jb = divmod(b_, NR); ym_ = (VB[a_][1] + VB[b_][1]) / 2
        if ia != ib and ja == jb:                                                                   # longitudinal edge
            if a_ in crest and b_ in crest: cr.data[e.index].value = CREASE_P0['fender_crest'] * ss(-2.14, -1.84, ym_) * (1 - ss(1.62, 2.02, ym_))
            elif a_ in rail and b_ in rail: cr.data[e.index].value = CREASE_P0['roof_rail']
        elif ia == ib and EDGE_COLS(ja) and EDGE_COLS(jb):                                          # transverse edge on the hood leading edge / rear deck edge
            tp = ss(7.5, 10.5, min(col_tag(ja), col_tag(jb)))                                      # taper to 0 toward the fender crest (no crease-end knot at the corners)
            if ia == I_HOODEDGE: cr.data[e.index].value = CREASE_P0['hood_leading_edge'] * tp
            elif ia == I_DECKEDGE: cr.data[e.index].value = CREASE_P0['deck_edge'] * tp
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
# wheel arches (approved radii)
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    R_ = r + .048; seg = 64; zc = r + .012
    outer = [(sx * 1.4, y + R_ * math.cos(2 * math.pi * k / seg), zc + R_ * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    solid(f'arch_{y}_{sx}', outer, [(sx * .55, py, pz) for _, py, pz in outer], 'arch')
# panel gaps: hood (inboard of the fender crests, so the crests stay on the fenders), deck lid, doors
fence('gap_hood', loop_top(sample_poly(rounded([(.64, -.60), (.70, -1.35), (.60, -2.10), (-.60, -2.10), (-.70, -1.35), (-.64, -.60)], [.03, .30, .10, .10, .30, .03], 6), .02)))
fence('gap_deck', loop_top(sample_poly(rounded([(.50, 1.54), (.58, 1.85), (.55, 2.165), (-.55, 2.165), (-.58, 1.85), (-.50, 1.54)], [.03, .20, .06, .06, .20, .03], 6), .02)))
for sx in (1, -1):
    DOOR = rounded([(-.42, .30), (.74, .30), (.74, ZBELT(.74) - .02), (-.40, ZBELT(-.40) - .018)], [.04, .04, .02, .02], 5)
    fence(f'gap_door_{sx}', loop_side(sx, sample_poly(DOOR, .02)))
    side_pocket(f'handle_{sx}', rounded([(.40, .795), (.56, .795), (.56, .815), (.40, .815)], .008, 3), .012, 'pocket', sx)
# front: wide inverted-trapezoid grille, upper slot, corner air curtains, angular headlamp housings with the fang
GR = rounded([(-.54, .42), (.54, .42), (.40, .20), (-.40, .20)], [.03, .03, .045, .045], 4)
front_pocket('grille', GR[::-1], .10, 'pocket')
SLOT = rounded([(-.34, .535), (.34, .535), (.33, .515), (-.33, .515)], .008, 2)
front_pocket('slot', SLOT[::-1], .035, 'pocket')
def AC(sx): return rounded([(sx * .70, .45), (sx * .755, .47), (sx * .76, .24), (sx * .705, .22)], .012, 3)
def HLP(sx): return rounded([(sx * .455, .590), (sx * .86, .658), (sx * .878, .598), (sx * .525, .548), (sx * .515, .468), (sx * .494, .468)], [.008, .012, .012, .006, .004, .004], 3)
for sx in (1, -1):
    front_pocket(f'aircurtain_{sx}', AC(sx) if sx > 0 else AC(sx)[::-1], .08, 'pocket')
    front_pocket(f'headlamp_{sx}', HLP(sx)[::-1] if sx > 0 else HLP(sx), .065, 'housing')
# hood heat-extractor vents
def HV(sx): return rounded([(sx * .18, -1.18), (sx * .36, -1.14), (sx * .36, -.92), (sx * .20, -.96)], .02, 4)
for sx in (1, -1): top_pocket(f'hoodvent_{sx}', HV(sx) if sx > 0 else HV(sx)[::-1], .05, 'pocket')
# side: front-fender gills
def GILL(): return rounded([(-.93, .66), (-.80, .67), (-.82, .50), (-.93, .55)], .015, 3)
for sx in (1, -1): side_pocket(f'gill_{sx}', GILL(), .03, 'pocket', sx)
# rear: chevron lamp housings, reverse lamps, plate recess, black valance (frames the exhausts), diffuser tunnel
def TLH(sx): return rounded([(sx * .50, .878), (sx * .89, .812), (sx * .89, .758), (sx * .54, .700)], [.01, .015, .015, .01], 3)
def REV(sx): return rounded([(sx * .65, .49), (sx * .81, .49), (sx * .81, .458), (sx * .65, .458)], .008, 2)
for sx in (1, -1):
    front_pocket(f'taillamp_{sx}', TLH(sx) if sx < 0 else TLH(sx)[::-1], .05, 'housing', rear=True)
    front_pocket(f'reverse_{sx}', REV(sx) if sx < 0 else REV(sx)[::-1], .015, 'housing', rear=True)
front_pocket('plate', rounded([(-.25, .66), (.25, .66), (.25, .54), (-.25, .54)], .015, 3)[::-1], .02, 'satin_black', rear=True)
VAL = rounded([(-.80, .425), (.80, .425), (.74, .27), (-.74, .27)], [.03, .03, .02, .02], 3)
front_pocket('valance', VAL[::-1], .04, 'satin_black', rear=True)
def diff_z(y): return lerp(.125, .262, ss(1.70, 2.22, y) ** 1.3)
DY = [lerp(1.68, 2.40, k / 16) for k in range(17)]
outer = [(.78, y, diff_z(min(y, 2.22))) for y in DY] + [(-.78, y, diff_z(min(y, 2.22))) for y in DY[::-1]]
bmx = bmesh.new(); top_ = [bmx.verts.new(p) for p in outer]; bot_ = [bmx.verts.new((p[0], p[1], -.5)) for p in outer]; n_ = len(outer)
bmx.faces.new(top_); bmx.faces.new(bot_[::-1])
for i in range(n_): j = (i + 1) % n_; bmx.faces.new((top_[i], bot_[i], bot_[j], top_[j]))
bmesh.ops.recalc_face_normals(bmx, faces=bmx.faces); bmesh.ops.triangulate(bmx, faces=bmx.faces); me_ = bpy.data.meshes.new('diffcut'); bmx.to_mesh(me_); bmx.free(); me_.materials.append(MM['TMP_satin_black'])
CUT.objects.link(bpy.data.objects.new('diffuser_tunnel', me_))
def apply_cuts(o, cc):
    m_ = o.modifiers.new('cuts', 'BOOLEAN'); m_.operation = 'DIFFERENCE'; m_.solver = 'EXACT'; m_.operand_type = 'COLLECTION'; m_.collection = cc
    if hasattr(m_, 'material_mode'): m_.material_mode = 'TRANSFER'
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='cuts')
CUT_NG = coll('RV_CUTTERS_NOGAP')                                                                  # LOD source: same openings, NO panel-gap grooves (Titan GT r1 lesson)
for o in CUT.objects:
    if not o.name.startswith('gap_'): CUT_NG.objects.link(o)
body_ng = cage_obj('Body_NoGap'); subdiv(body_ng, 2); apply_cuts(body_ng, CUT_NG)
for o in list(CUT_NG.objects): CUT_NG.objects.unlink(o)
apply_cuts(body, CUT)
REPORT['cutters'] = sorted(o.name for o in CUT.objects)
for o in list(CUT.objects): bpy.data.objects.remove(o, do_unlink=True)
clean(body)
glass = split_by_material(body, {'RV_Glass'}, 'Glass_Shell'); clean(glass); clean(body)
remap_tmp(body); remap_tmp(glass); purge_slots(body); purge_slots(glass); skin_normals(body); skin_normals(glass)
g_ng = split_by_material(body_ng, {'RV_Glass'}, 'Glass_NoGap'); bpy.data.objects.remove(g_ng, do_unlink=True); clean(body_ng); remap_tmp(body_ng); purge_slots(body_ng)
REPORT['body_lod0_tris'] = tris(body)
save_ckp('ravenxr_02_body_panels.blend') if LAST >= 2 else None
if LAST <= 2: sys.exit(0)
# ================================================================ 03 exterior details + lights
TR, LI = Geo(), Geo()
def ptat(hitf, a, b, depth):
    p, n = hitf(a, b); return None if p is None else p - n * depth
def bars(hitf, pts2, depth, w, t, flip=False, axis='x'):
    """thin bar strip through projected points (x, z) at `depth` behind the skin."""
    A = [ptat(hitf, a, b, depth) for a, b in pts2]
    if any(p is None for p in A) or len(A) < 2: return
    d = Vector((w, 0, 0)) if axis == 'x' else Vector((0, 0, w))
    TR.strip([q - d for q in A], [q + d for q in A], t, flip=flip)
# ---- front: honeycomb grille (back plate + diagonal lattice), gloss-black brow, air-curtain vanes, splitter
surf_patch(TR, GR, lambda a, b: (lambda pn: (pn[0] + Vector((0, .092, 0)), pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'RV_Palette:mesh', flip=True)
for k in range(-13, 14):
    for d_ in (1, -1):
        pts = []
        for t in np.linspace(0, 1, 7):
            x = k * .055 + d_ * lerp(-.11, .11, t); z = lerp(.205, .415, t)
            if abs(x) < lerp(.40, .54, (z - .20) / .22) - .02: pts.append((x, z))
        if len(pts) >= 2: bars(fhit, pts, .05, .0035, 'RV_Palette:grille')
bezel(TR, GR, fhit, .014, .001, 'RV_Palette:gloss_black')
for sx in (1, -1):
    for xf in (.722, .740):
        zs = np.linspace(.235, .455, 6); bars(fhit, [(sx * (xf + .004 * (z - .24) / .2), z) for z in zs], .03, .0025, 'RV_Palette:gloss_black', flip=sx < 0)
xs = np.linspace(-.84, .84, 41); front = []
for x in xs:
    p, n = fhit(x, .19); front.append(Vector((x, (p.y if p else -2.2) - .035 - .015 * (1 - (x / .84) ** 2), .165)))
back = [Vector((x, -1.92, .165)) for x in xs]
TR.strip(back, front, 'RV_Carbon'); TR.strip([q - Vector((0, 0, .012)) for q in front], [q - Vector((0, 0, .012)) for q in back], 'RV_Carbon'); TR.strip(front, [q - Vector((0, 0, .012)) for q in front], 'RV_Carbon', flip=True)
for sx in (1, -1):
    x = sx * .84; p, n = fhit(x, .21); yf = p.y - .03
    TR.box((x, yf + .10, .195), (.004, .10, .035), 'RV_Carbon')
# ---- hood heat-extractor slats, fender-gill slats
for sx in (1, -1):
    for k in range(5):
        y = lerp(-1.13, -.97, k / 4); xs_ = np.linspace(.19 + .004 * k, .355, 7); A = []
        for x in xs_:
            p, n = thit(sx * x, y); A.append(Vector((sx * x, y, p.z - .010)))
        TR.strip([q - Vector((0, .006, 0)) for q in A], [q + Vector((0, .006, 0)) for q in A], 'RV_Palette:gloss_black', flip=sx < 0)
        TR.strip([q + Vector((0, .006, 0)) for q in A], [q + Vector((0, .006, -.028)) for q in A], 'RV_Palette:gloss_black', flip=sx < 0)
    for k in range(3):
        z0 = .545 + .04 * k; ys = np.linspace(-.92, -.82, 5); A = []
        for y in ys:
            p, n = shit(sx, y, z0 + .02 * (y + .92) / .10); A.append(p - n * .012)
        TR.strip([q - Vector((0, 0, .005)) for q in A], [q + Vector((0, 0, .005)) for q in A], 'RV_Palette:gloss_black', flip=sx > 0)
# ---- side: sculpted gloss-black side-skirt blade (rises toward the rear), B-pillar applique on the side glass
for sx in (1, -1):
    ys = np.linspace(-.92, .98, 40); A, B = [], []
    for y in ys:
        zc_ = lerp(.23, .26, (y + .92) / 1.9); p, n = shit(sx, y, zc_)
        if p is None: continue
        A.append(p + n * .008 + Vector((0, 0, -.022))); B.append(p + n * .008 + Vector((0, 0, .016)))
    TR.strip(A, B, 'RV_Palette:gloss_black', flip=sx > 0); TR.strip(B, [q + Vector((sx * .028, 0, -.010)) for q in B], 'RV_Palette:gloss_black', flip=sx > 0)
    TR.strip([q + Vector((sx * .028, 0, -.010)) for q in B], A, 'RV_Palette:gloss_black', flip=sx > 0)
    rows = []
    for z in np.linspace(0, 1, 5):
        row = []
        for y in (.70, .76):
            zz = lerp(ZBELT(y) + .035, lerp(ZBELT(y) + .03, ZC(y) - .06, .90) - .01, z); p, n = shit(sx, y, zz); row.append(p + n * .004 if p is not None else None)
        rows.append(row)
    if all(p is not None for r in rows for p in r): TR.grid(rows, 'RV_Palette:gloss_black', flip=sx > 0)
# ---- rear: diffuser surface + 5 strakes + side plates, oval exhausts in the valance, deck spoiler on two pylons
xs = list(np.linspace(-.78, .78, 25)); ys = list(np.linspace(1.70, 2.22, 12))
TR.grid([[Vector((x, y, diff_z(y))) for x in xs] for y in ys], 'RV_Carbon', flip=True)
for xf in (-.40, -.20, 0.0, .20, .40, -.78, .78):
    top = [Vector((xf, y, diff_z(y) - .001)) for y in ys]; bot = [Vector((xf, y, min(diff_z(y) - .006, lerp(.13, .205, ss(1.80, 2.22, y))))) for y in ys]   # strakes taper to ~6 cm at the tail (integrated, no comb below the valance)
    w = .005 if abs(xf) < .7 else .008
    for off in (-w, w): TR.strip([q + Vector((off, 0, 0)) for q in top], [q + Vector((off, 0, 0)) for q in bot], 'RV_Carbon', flip=off > 0)
    TR.strip([q - Vector((w, 0, 0)) for q in bot], [q + Vector((w, 0, 0)) for q in bot], 'RV_Carbon')
for cx in (-.62, .62):
    seg = 28; p, n = rhit(cx, .34); y0 = p.y - .04; cz = .34
    ell = lambda rx, rz, y: [Vector((cx + rx * math.cos(2 * math.pi * k / seg), y, cz + rz * math.sin(2 * math.pi * k / seg))) for k in range(seg)]
    TR.strip(ell(.07, .04, y0 - .10), ell(.07, .04, y0 + .045), 'RV_Palette:exhaust', closed=True); TR.strip(ell(.07, .04, y0 + .045), ell(.061, .031, y0 + .045), 'RV_Palette:exhaust', closed=True)
    TR.strip(ell(.061, .031, y0 + .045), ell(.061, .031, y0 - .06), 'RV_Palette:exhaust_inner', closed=True)
    n0 = len(TR.V); TR.V += [tuple(v) for v in ell(.061, .031, y0 - .06)] + [(cx, y0 - .06, cz)]
    for k in range(seg): TR.F.append((n0 + k, n0 + (k + 1) % seg, n0 + seg)); TR.T.append('RV_Palette:exhaust_inner')
SP_Y = 2.04; SP_Z = thit(0, SP_Y)[0].z + .075
af = [(0.0, 0.0), (.03, .010), (.07, .015), (.12, .016), (.17, .010), (.20, .002), (.17, -.001), (.12, -.004), (.07, -.004), (.03, -.003)]
ring_s = []
for x in np.linspace(-.76, .76, 25):
    zb0 = thit(x, SP_Y)[0].z; ring_s.append([Vector((x, SP_Y - .10 + c, max(SP_Z, zb0 + .055) + z)) for c, z in af])
for A, B in zip(ring_s, ring_s[1:]): TR.strip(A, B, 'RV_Carbon', closed=True)
for R_ in (ring_s[0], ring_s[-1]): TR.add(R_, [tuple(range(len(R_))) if R_ is ring_s[-1] else tuple(range(len(R_) - 1, -1, -1))], 'RV_Carbon')
for sx in (1, -1):
    b0 = thit(sx * .46, SP_Y - .03)[0]; secs = []
    for t in np.linspace(0, 1, 4):
        z = lerp(b0.z - .01, SP_Z + .006, t); ch = lerp(.10, .08, t)
        secs.append([Vector((sx * .46 - .008, SP_Y - .07, z)), Vector((sx * .46 + .008, SP_Y - .07, z)), Vector((sx * .46 + .008, SP_Y - .07 + ch, z)), Vector((sx * .46 - .008, SP_Y - .07 + ch, z))])
    for A, B in zip(secs, secs[1:]): TR.strip(A, B, 'RV_Carbon', closed=True)
# ---- wheel-well liners
for (y, r, sx) in ((YF, RF, 1), (YF, RF, -1), (YR, RR, 1), (YR, RR, -1)):
    R_ = r + .046; zc = r + .012; seg = 28; a0, a1 = math.radians(-25), math.radians(205)
    arc = [(y + R_ * math.cos(lerp(a0, a1, q / seg)), zc + R_ * math.sin(lerp(a0, a1, q / seg))) for q in range(seg + 1)]
    xi, xo = sx * .55, sx * (WMAX(y) - .015)
    TR.strip([Vector((xi, yy, zz)) for yy, zz in arc], [Vector((xo, yy, zz)) for yy, zz in arc], 'RV_Palette:satin_black', flip=sx > 0)
    n0 = len(TR.V); TR.V += [(xi, yy, zz) for yy, zz in arc] + [(xi, y, .15)]
    for q in range(seg): f = (n0 + q, n0 + q + 1, n0 + seg + 1); TR.F.append(f if sx < 0 else f[::-1]); TR.T.append('RV_Palette:satin_black')
# ---- LIGHTS front: upper DRL blade + inboard fang (DRL), two projector modules (Headlamp), amber indicator, clear lens
def hz(x, top):                                                                                     # housing top / bottom edge height at x (outer, angular part)
    t = (x - .455) / (.86 - .455); return lerp(.590, .658, t) if top else lerp(.548, .598, (x - .525) / (.878 - .525))
for sx in (1, -1):
    fl = sx < 0; IND = 'RV_LED_Indicator_L' if sx > 0 else 'RV_LED_Indicator_R'
    LI.grid([[ptat(fhit, sx * x, hz(x, True) - dz, .012) for x in np.linspace(.475, .85, 22)] for dz in (.016, .006)], 'RV_LED_DRL', flip=fl)        # upper DRL blade
    LI.grid([[ptat(fhit, sx * lerp(x0, x1, v), lerp(.575, .478, v), .012) for x0, x1 in ((.466, .498), (.478, .508))] for v in np.linspace(0, 1, 6)], 'RV_LED_DRL', flip=fl)    # fang
    LI.grid([[ptat(fhit, sx * x, hz(x, False) + dz, .012) for x in np.linspace(.78, .866, 6)] for dz in (.006, .015)], IND, flip=fl)
    for x0 in (.62, .725):                                                                          # projector modules
        zc_ = (hz(x0, True) + hz(x0, False)) / 2 - .002; c0 = ptat(fhit, sx * x0, zc_, .0); seg = 16; r = .015
        ring = lambda dy, rr: [Vector((c0.x + rr * math.cos(2 * math.pi * q / seg), c0.y + dy, c0.z + rr * math.sin(2 * math.pi * q / seg))) for q in range(seg)]
        LI.strip(ring(.05, r), ring(.014, r), 'RV_Palette:housing', closed=True); LI.strip(ring(.014, r), ring(.011, r * .75), 'RV_Palette:reflector', closed=True)
        n0 = len(LI.V); LI.V += [tuple(v) for v in ring(.011, r * .75)] + [(c0.x, c0.y + .009, c0.z)]
        for q in range(seg): LI.F.append((n0 + q, n0 + (q + 1) % seg, n0 + seg)); LI.T.append('RV_LED_Headlamp')
    surf_patch(LI, HLP(sx), fhit, .0012, 'RV_LensClear', flip=None)
# ---- LIGHTS rear: chevron (upper + lower blade + tip) = Tail; inner fill = Brake; amber segment = Indicator; lower lamp = Reverse; red lens; third brake light
def ub(u): return lerp(.52, .87, u), lerp(.857, .799, u)                                          # upper blade centreline
def lb(u): return lerp(.555, .87, u), lerp(.721, .779, u)                                         # lower blade centreline
for sx in (1, -1):
    fl = sx < 0; IND = 'RV_LED_Indicator_L' if sx > 0 else 'RV_LED_Indicator_R'
    for fn in (ub, lb):
        LI.grid([[ptat(rhit, sx * fn(u)[0], fn(u)[1] + dz, .016) for u in np.linspace(0, 1, 14)] for dz in (-.008, .008)], 'RV_LED_Tail', flip=fl)
    LI.grid([[ptat(rhit, sx * x, z, .016) for x in (.838, .866)] for z in np.linspace(.778, .806, 3)], 'RV_LED_Tail', flip=fl)
    LI.grid([[ptat(rhit, sx * lerp(ub(u)[0], lb(u)[0], v), lerp(ub(u)[1] - .013, lb(u)[1] + .013, v), .024) for u in np.linspace(.04, .42, 6)] for v in np.linspace(0, 1, 4)], 'RV_LED_Brake', flip=fl)
    LI.grid([[ptat(rhit, sx * lerp(ub(u)[0], lb(u)[0], v), lerp(ub(u)[1] - .013, lb(u)[1] + .013, v), .022) for u in np.linspace(.55, .74, 4)] for v in np.linspace(.15, .85, 3)], IND, flip=fl)
    surf_patch(LI, TLH(sx), rhit, -.0012, 'RV_LensRed', flip=None)
    LI.grid([[ptat(rhit, sx * x, z, .006) for x in np.linspace(.665, .795, 6)] for z in (.464, .484)], 'RV_LED_Reverse', flip=fl)
    surf_patch(LI, REV(sx), rhit, -.0012, 'RV_LensClear', flip=None)
LI.grid([[Vector((x, SP_Y + .101, SP_Z + z)) for x in np.linspace(-.14, .14, 9)] for z in (.0, .008)], 'RV_LED_Brake')          # third brake light: deck-spoiler trailing edge
trim = mk('Trim_LOD0', TR.V, TR.F, TR.T, WORK, M); lights = mk('Lights_LOD0', LI.V, LI.F, LI.T, WORK, M)
for o in (trim, lights): clean(o); orient_components(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(35))
# ---- mirrors: body-colour pod (flat glass face to the rear) on a gloss-black arm -> part of the body
MI = Geo()
for sx in (1, -1):
    bmm = bmesh.new(); bmesh.ops.create_uvsphere(bmm, u_segments=24, v_segments=14, radius=1.0)
    for v in bmm.verts:
        x, y, z = v.co; y = y * (1.0 if y < 0 else .42); z = z * (1 - .25 * max(0, -y))
        v.co = Vector((x * .088, y * .082, z * .050)) + Vector((sx * .935, -.32, .975))
    bmm.normal_update(); vs = [tuple(v.co) for v in bmm.verts]; fs = [tuple(v.index for v in f.verts) for f in bmm.faces]
    ts = ['RV_Palette:mirror' if f.normal.y > .7 else 'RV_Paint' for f in bmm.faces]; bmm.free(); MI.add(vs, fs, ts)
    Vs = [(sx * .80, -.38, .905), (sx * .80, -.31, .905), (sx * .89, -.30, .955), (sx * .89, -.35, .955)]
    MI.add(Vs + [(x, y, z + .014) for x, y, z in Vs], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)], 'RV_Palette:gloss_black')
mirrors = mk('Mirrors', MI.V, MI.F, MI.T, WORK, M)
bm = bmesh.new(); bm.from_mesh(mirrors.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(mirrors.data); bm.free(); mirrors.data.shade_smooth()
REPORT['trim_tris'], REPORT['lights_tris'] = tris(trim), tris(lights)
save_ckp('ravenxr_03_details_lights.blend') if LAST >= 3 else None
if LAST <= 3: sys.exit(0)
# ================================================================ 04 wheels: dark forged 14-spoke (7 pairs), 19", hub + 5 lug nuts, drilled-look rotors, red calipers
WREF = {'FL': Vector((XF, YF, RF)), 'FR': Vector((-XF, YF, RF)), 'RL': Vector((XR, YR, RR)), 'RR': Vector((-XR, YR, RR))}
WSPEC = {'FL': (RF, WF, .2413), 'FR': (RF, WF, .2413), 'RL': (RR, WR, .2413), 'RR': (RR, WR, .2413)}
LOD_SEG = {0: (96, 64), 1: (48, 36), 2: (28, 20), 3: (16, 12)}
def build_wheel(c, k, coll_):
    R, W, rr = WSPEC[c]; sx = 1 if c[1] == 'L' else -1; hw = W / 2; seg_t, seg_r = LOD_SEG[k]; out = {}
    prof = [(-hw * .80, rr + .006), (-hw * .96, rr + .026), (-hw, R * .80), (-hw * .985, R * .90), (-hw * .93, R * .965), (-hw * .80, R * .997), (-hw * .40, R), (0, R),
            (hw * .40, R), (hw * .80, R * .997), (hw * .93, R * .965), (hw * .985, R * .90), (hw, R * .80), (hw * .96, rr + .026), (hw * .80, rr + .006)]
    if k >= 2: prof = [prof[i] for i in (0, 2, 4, 6, 8, 10, 12, 14)]
    Vt, Ft, UVt = revolve(prof, seg_t, sx); g = Geo(); g.add(Vt, Ft, 'RV_Tire'); tire = mk(f'Tire_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    uvl = tire.data.uv_layers.new(name='tireUV')
    for p in tire.data.polygons:
        for li in p.loop_indices: uvl.data[li].uv = UVt[tire.data.loops[li].vertex_index]
    out['Tire'] = tire
    g = Geo(); face = hw * .58
    lip = [(hw * .84, rr - .024), (hw * .90, rr + .004), (hw * .78, rr + .010), (hw * .68, rr - .016)]
    Vl, Fl, _ = revolve(lip, seg_r, sx); g.add(Vl, Fl, 'RV_Palette:wheel_lip')
    barrel = [(hw * .68, rr - .016), (hw * .20, rr - .028), (-hw * .70, rr - .030), (-hw * .82, rr + .004)]
    Vb, Fb, _ = revolve(barrel, seg_r, sx); g.add(Vb, Fb, 'RV_Palette:wheel_forged')
    nt_ = 7 if k == 0 else 4 if k == 1 else 2
    nspk = 7 if k <= 2 else 7
    for s_ in range(nspk):
        for side_ in ((-1, 1) if k <= 2 else (0,)):
            a_in = 2 * math.pi * s_ / nspk; a_out = a_in + side_ * .17; secs = []
            for t in np.linspace(0, 1, nt_):
                r_ = lerp(.075, rr - .02, t); a = lerp(a_in + side_ * .025, a_out, t ** 1.2); w = lerp(.018, .011, t) * (1.6 if side_ == 0 else 1); xx = face - .024 * math.sin(math.pi * t)
                Rm = Matrix.Rotation(a, 3, 'X')
                secs.append([Rm @ Vector((sx * (xx + .004), -w, r_)), Rm @ Vector((sx * (xx + .004), w, r_)), Rm @ Vector((sx * (xx - .018), w * 1.12, r_)), Rm @ Vector((sx * (xx - .018), -w * 1.12, r_))])
            for A, B in zip(secs, secs[1:]): g.strip(A, B, 'RV_Palette:wheel_forged', closed=True, flip=sx < 0)
            g.add(secs[-1], [(0, 1, 2, 3) if sx > 0 else (3, 2, 1, 0)], 'RV_Palette:wheel_forged')
    hub = [(face + .006, 0.0), (face + .006, .030), (face + .002, .050), (face - .006, .075), (face - .02, .077)]
    Vh, Fh, _ = revolve(hub, max(12, seg_r // 2), sx); g.add(Vh, Fh, 'RV_Palette:wheel_forged')
    if k <= 1:
        for s_ in range(5):                                                                         # 5 lug nuts
            a = 2 * math.pi * (s_ + .5) / 5; cy, cz = .044 * math.cos(a), .044 * math.sin(a); hx = [(cy + .0075 * math.cos(2 * math.pi * q / 6), cz + .0075 * math.sin(2 * math.pi * q / 6)) for q in range(6)]
            A = [Vector((sx * (face + .004), y, z)) for y, z in hx]; B = [Vector((sx * (face + .016), y, z)) for y, z in hx]
            g.strip(A, B, 'RV_Palette:lug', closed=True, flip=sx < 0); g.add(B, [tuple(range(6)) if sx > 0 else tuple(range(5, -1, -1))], 'RV_Palette:lug')
        Vc, Fc, _ = revolve([(face + .010, 0.0), (face + .010, .020), (face + .006, .026)], 16, sx); g.add(Vc, Fc, 'RV_Palette:accent_red')
    if k == 3:
        Vd, Fd, _ = revolve([(-hw * .1, .06), (-hw * .1, rr - .05)], 12, sx); g.add(Vd, Fd, 'RV_Palette:rotor')
    out['Wheel'] = mk(f'Wheel_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    if k <= 2:
        g = Geo(); rd = rr - .045
        Vd, Fd, _ = revolve([(hw * .05, .085), (hw * .05, rd), (-hw * .10, rd), (-hw * .10, .085)], seg_r, sx); g.add(Vd, Fd, 'RV_Palette:rotor')
        Vh, Fh, _ = revolve([(hw * .28, .0), (hw * .28, .085), (hw * .05, .085)], max(12, seg_r // 2), sx); g.add(Vh, Fh, 'RV_Palette:rotor_hat')
        out['BrakeDisc'] = mk(f'BrakeDisc_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
        g = Geo(); n_ = {0: 12, 1: 8, 2: 4}[k]; r0, r1 = rd - .055, rd + .008; front = c[0] == 'F'
        a0, a1 = (math.radians(32), math.radians(104)) if front else (math.radians(76), math.radians(148))
        secs = []
        for q in range(n_ + 1):
            a = lerp(a0, a1, q / n_); ca, sa = math.cos(a) * (1 if front else -1), math.sin(a); bul = .005 * math.sin(math.pi * q / n_)
            pts = [(r0, sx * (hw * .16 + bul)), (r1, sx * (hw * .16 + bul)), (r1 + .005, sx * (hw * .03)), (r1, -sx * (hw * .30 + bul)), (r0, -sx * (hw * .30 + bul)), (r0 - .006, sx * (-hw * .06))]
            secs.append([Vector((xx, rr_ * ca, rr_ * sa)) for rr_, xx in pts])
        for A, B in zip(secs, secs[1:]): g.strip(A, B, 'RV_Palette:caliper_red', closed=True)
        g.add(secs[0], [tuple(range(6))], 'RV_Palette:caliper_red'); g.add(secs[-1], [tuple(range(5, -1, -1))], 'RV_Palette:caliper_red')
        out['Caliper'] = mk(f'Caliper_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    for key, o in out.items():
        bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
        if key == 'Caliper': bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(o.data); bm.free(); clean(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40 if key != 'Tire' else 60))
        o.data.transform(Matrix.Translation(WREF[c])); set_origin(o, WREF[c])
    return out
WH = coll('RV_WHEELS'); ASM = {}
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key, o in build_wheel(c, k, WH).items(): ASM[(k, c, key)] = o
save_ckp('ravenxr_04_wheels.blend') if LAST >= 4 else None
# ================================================================ 05 interior: lightweight premium driver-focused cockpit (LHD, driver on +X), red accents
IN, ST = Geo(), Geo()
for sx in (1, -1):
    xs_ = sx * .37; tilt = Matrix.Rotation(-.30, 3, 'X')
    rbox(IN, (xs_, .32, .30), (.20, .23, .05), 'RV_Palette:alcantara', .025)                         # sport bucket: cushion
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .18, .32, .36), (.04, .22, .075), 'RV_Palette:leather_black', .025)
    rbox(IN, (xs_, .58, .64), (.19, .055, .30), 'RV_Palette:alcantara', .03, tilt)                    # backrest
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .18, .55, .63), (.045, .075, .29), 'RV_Palette:leather_black', .02, tilt)
    for bx in (-1, 1): rbox(IN, (xs_ + bx * .12, .52, .62), (.004, .058, .26), 'RV_Palette:accent_red', .002, tilt)   # red stitching lines
    rbox(IN, (xs_, .60, .98), (.11, .05, .07), 'RV_Palette:leather_black', .03, tilt)                 # integrated headrest
    rbox(IN, (sx * .77, .10, .55), (.022, .48, .17), 'RV_Palette:leather_black', .02)                  # door trim
    rbox(IN, (sx * .745, .12, .62), (.03, .30, .02), 'RV_Palette:alcantara', .01)                     # armrest
    rbox(IN, (sx * .752, .12, .645), (.004, .30, .003), 'RV_Palette:accent_red', .001)                # red stitching on the armrest
    rbox(IN, (sx * .748, -.18, .70), (.006, .04, .02), 'RV_Palette:aluminium', .004)                  # door release
rbox(IN, (0, -.40, .70), (.70, .13, .07), 'RV_Palette:leather_black', .04)                            # dashboard
rbox(IN, (0, -.32, .645), (.68, .04, .05), 'RV_Palette:int_trim', .02)
rbox(IN, (0, -.315, .69), (.68, .004, .003), 'RV_Palette:accent_red', .001)                           # red stitching across the dash
rbox(IN, (.37, -.32, .80), (.15, .06, .035), 'RV_Palette:leather_black', .025)                        # cluster hood over the driver
rbox(IN, (.37, -.272, .765), (.125, .006, .038), 'RV_Display', .004)                                  # instrument cluster
rbox(IN, (.09, -.33, .74), (.095, .006, .055), 'RV_Display', .004, Matrix.Rotation(-.20, 3, 'Z'))    # centre screen angled to the driver
rbox(IN, (.06, -.02, .40), (.11, .42, .12), 'RV_Palette:int_trim', .03, Matrix.Rotation(-.06, 3, 'Z'))   # centre console, angled toward the driver
rbox(IN, (.06, .02, .525), (.07, .10, .01), 'RV_Palette:aluminium', .006)                             # shifter plate
rbox(IN, (.06, .03, .57), (.018, .018, .04), 'RV_Palette:leather_black', .012)                        # shifter
rbox(IN, (0, .25, .14), (.78, .75, .02), 'RV_Palette:carpet', .01)                                    # floor
rbox(IN, (0, .98, .80), (.68, .25, .02), 'RV_Palette:int_trim', .01)                                  # parcel shelf under the fastback glass
rbox(IN, (0, 1.12, .52), (.68, .03, .27), 'RV_Palette:int_trim', .02)                                 # luggage bulkhead
hl_rows = []
for y in np.linspace(-.30, .95, 16):
    row = []
    for x in np.linspace(-.48, .48, 13):
        p, n = thit(x, y); row.append((p - n * .014) if p is not None and p.z > 1.10 else None)
    hl_rows.append(row)
hl_rows = [r for r in hl_rows if all(p is not None for p in r)]
IN.grid(hl_rows, 'RV_Palette:alcantara', flip=True)                                                  # headliner
interior = mk('Interior_LOD0', IN.V, IN.F, IN.T, WORK, M)
hubc = Vector((.37, -.10, .72)); tilt = Matrix.Rotation(math.radians(-68), 3, 'X'); seg, sg2 = 32, 10
for q in range(seg):                                                                                  # sport wheel, flat bottom
    a0, a1 = 2 * math.pi * q / seg, 2 * math.pi * (q + 1) / seg
    def ring(a):
        rx = .17; cx_, cz_ = rx * math.cos(a), max(rx * math.sin(a), -.125)
        return [hubc + tilt @ Vector((cx_ + .017 * math.cos(2 * math.pi * k / sg2) * math.cos(a), .017 * math.sin(2 * math.pi * k / sg2), cz_ + .017 * math.cos(2 * math.pi * k / sg2) * math.sin(a))) for k in range(sg2)]
    ST.strip(ring(a0), ring(a1), 'RV_Palette:leather_black', closed=True)
rbox(ST, tuple(hubc + tilt @ Vector((0, 0, .162))), (.012, .021, .013), 'RV_Palette:accent_red', .005, tilt)    # 12-o'clock marker
for a in (0, math.pi, -math.pi / 2):
    rbox(ST, tuple(hubc + tilt @ Vector((.095 * math.cos(a), 0, .095 * math.sin(a)))), (.07 if a != -math.pi / 2 else .016, .012, .016 if a != -math.pi / 2 else .06), 'RV_Palette:int_trim', .006, tilt)
rbox(ST, tuple(hubc + tilt @ Vector((0, .014, 0))), (.058, .026, .045), 'RV_Palette:leather_black', .02, tilt)
for sxp in (1, -1): rbox(ST, tuple(hubc + tilt @ Vector((sxp * .11, .03, .03))), (.004, .02, .03), 'RV_Palette:aluminium', .002, tilt)   # shift paddles
steer = mk('SteeringWheel_LOD0', ST.V, ST.F, ST.T, WORK, M); set_origin(steer, hubc)
for o in (interior, steer):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); clean(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40))
REPORT['interior_tris'] = tris(interior) + tris(steer)
save_ckp('ravenxr_05_interior.blend') if LAST >= 5 else None
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
save_ckp('ravenxr_06_materials_uv.blend') if LAST >= 6 else None
# ================================================================ 07 LODs: body from the groove-free source + smooth-reference normals; Trim LOD1 own normals (Titan r1 lesson)
RK = {1: {'Body': .54, 'Glass': .7, 'Trim': .45, 'Lights': .5, 'Interior': .45, 'SteeringWheel': .5},
      2: {'Body': .26, 'Glass': .45, 'Trim': .18, 'Lights': .22, 'Interior': .18, 'SteeringWheel': .2},
      3: {'Body': .095, 'Glass': .18, 'Trim': .06, 'Lights': .08, 'Interior': .04}}
if os.environ.get('RV_RK'): RK = json.loads(os.environ['RV_RK'], object_hook=lambda d: {int(k) if k.isdigit() else k: v for k, v in d.items()})
for k in (1, 2, 3):
    Lk = coll(f'LOD{k}_PARTS')
    for n0, o0 in list(FINAL0.items()) + [('SteeringWheel_LOD0', steer)]:
        kind = n0.split('_')[0]
        if kind not in RK[k]: continue
        src_ = body_lodsrc if kind == 'Body' else o0
        d = src_.copy(); d.data = src_.data.copy(); Lk.objects.link(d); d.name = n0.replace('LOD0', f'LOD{k}'); d.data.name = d.name
        if kind == 'Body':
            decimate(d, RK[k][kind], transfer=False); skin_normals(d)
        else: decimate(d, RK[k][kind], ref=o0, transfer=(k <= 1 and kind == 'Glass'))                 # LOD0-normal transfer only for the smooth glass sheet; hard-surface parts get own normals (no tears)
        final_uvs(d)
bpy.data.objects.remove(body_lodsrc, do_unlink=True); bpy.data.objects.remove(hi, do_unlink=True)
REPORT['lod_ratios'] = RK
save_ckp('ravenxr_07_lods.blend') if LAST >= 7 else None
# ================================================================ 08 colliders, hierarchy, pivots, references
FIN = coll('RAVEN_XR'); COLL = coll('RV_COLLIDERS', FIN)
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
tr2 = [O['Trim_LOD2'].matrix_world @ v.co for v in O['Trim_LOD2'].data.vertices]
CL = {'Collision_Front': [p for p in pts if p.y < -.95 and p.z < .90], 'Collision_Body': [p for p in pts if -1.10 < p.y < 1.20 and p.z < .86],
      'Collision_Cabin': [p for p in pts if -.75 < p.y < 1.55 and p.z > .80], 'Collision_Rear': [p for p in pts if p.y > 1.0 and p.z < 1.12] + [p for p in tr2 if p.y > 1.85 and p.z > .95]}   # rear incl. the deck spoiler
cr = empty('Collision', FIN, (0, 0, 0), root, 'PLAIN_AXES', .2)
for n, vs in CL.items():
    if len(vs) > 8: h = hull(n, vs); h.parent = cr
for c in ('FL', 'FR', 'RL', 'RR'):
    e = empty(f'WheelColliderRef_{c}', FIN, WREF[c], root, 'SPHERE', .1); e['radius_m'] = WSPEC[c][0]; e['width_m'] = WF if c[0] == 'F' else WR
empty('CenterOfMass', FIN, (0, -.08, .44), root, 'SPHERE', .08)                                   # front-mid engine coupe: centreline, low, slightly ahead of mid-wheelbase
for c in list(bpy.data.collections):
    if c.name not in ('RAVEN_XR', 'RV_COLLIDERS'):
        for o in list(c.objects):
            if o.name not in FIN.all_objects: bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
json.dump(REPORT, open(os.path.join(REPD(), 'RV_build_log.json'), 'w'), indent=1)
save_ckp('ravenxr_08_colliders_hierarchy.blend') if LAST >= 8 else None
