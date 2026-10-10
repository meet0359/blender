# Traffic fleet — DESIGN-DRIVEN vehicle builder v2 (class-aware). v1 = ts_vehicle.py (unchanged; snapshotted in the v1 blockout folders).
# v2: vehicle CLASS presets (ts_classes.py), multi-shell bodies (ts_loft.py per shell: pickup cab + separate bed), class greenhouse profile, flush structural pillars, closed box-section roof rails, lower cladding panels.
#   Blender -b --factory-startup --python ts_vehicle_v2.py -- <design> [<last stage 2..8>]   env TS_BLOCKOUT=1 [TS_BLOCKOUT_TAG=_v2] -> blend/<ckp>_01_blockout<tag>.blend only
# Generic parts derived from each design's outlines: matrix headlamp internals, LED tail-lamp internals, grille vanes / bars, intake blades, plates,
# trims, roof rails, arch cladding, sculpted seats, mirrors.  Sedan B's own production script (ts_sedan_b.py) is unchanged.
#  02 body (master, game body, bake)  03 exterior parts + lights + glass  04 wheels  05 interior  06 merge, UVs, AO / grime bake  07 LODs (+ LOD1 bake)  08 rig
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from ts_lib import *
ARGS = sys.argv[sys.argv.index('--') + 1:]; DESIGN = ARGS[0]; LAST = int(ARGS[1]) if len(ARGS) > 1 else 8
E_ = lambda k, d: float(os.environ.get(k, d))
def rounded(pts, r, seg=3):
    out = []; n = len(pts); rs = r if isinstance(r, (list, tuple)) else [r] * n
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n]); d1 = (p0 - p1).normalized(); d2 = (p2 - p1).normalized()
        rr = min(rs[i], (p0 - p1).length * .45, (p2 - p1).length * .45); a_ = p1 + d1 * rr; b_ = p1 + d2 * rr
        for k in range(seg + 1): t = k / seg; q = (1 - t) ** 2 * a_ + 2 * (1 - t) * t * p1 + t * t * b_; out.append((q.x, q.y))
    return out
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'designs', DESIGN + '.py')).read(), DESIGN + '.py', 'exec'), globals())   # the design
from ts_classes import apply_class; apply_class(globals())                                         # v2: class defaults (design values win)
ROOT = vroot(VEH)
GH_TOP = globals().get('GH_TOP', (.065, .92)); RW_COL = globals().get('RW_COL', 11); GRILLE_FRAME = globals().get('GRILLE_FRAME', 'TS_Atlas:chrome')   # design defaults (Sedan B)
def OUTD(*a):
    d = os.path.join(SCR, *a[:-1]) if SCR else os.path.join(ROOT, *a[:-1]); os.makedirs(d, exist_ok=True); return os.path.join(d, a[-1])
BLOCKOUT = bool(os.environ.get('TS_BLOCKOUT'))
def save_ckp(name):
    if os.environ.get('TS_NOCKP') or BLOCKOUT: return
    path = OUTD('blend', name); assert SCR or not os.path.exists(path), 'checkpoint exists: ' + path
    bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=path, copy=True, relative_remap=True); print('SAVED', path, flush=True)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'
REPORT = {}
E_ = lambda k, d: float(os.environ.get(k, d))
# ================================================================ materials
TEX = make_shared_textures()
M = build_library(TEX, PRE, PAINT_RGB)
TMP = {}
def tmp(n):
    if n not in TMP: m = bpy.data.materials.new('TMP_' + n); m.diffuse_color = (.02, .02, .02, 1); TMP[n] = m
    return TMP[n]
MM = dict(M); MM.update({'TMP_' + k: tmp(k) for k in ('seal', 'pocket', 'housing', 'grille', 'plastic', 'arch', 'plate', 'clad')}); M['TMP_clad'] = MM['TMP_clad']
WORK = coll('TS_WORK'); CUT = coll('TS_CUTTERS'); CUT_G = coll('TS_GROOVES')
COFF = set(os.environ.get('TS_CREASE_OFF', '').split(','))                                               # diagnosis only
LOFT_SRC = compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ts_loft.py')).read(), 'ts_loft.py', 'exec')
SHELL_NS = []
for ov_ in (globals().get('SHELLS') or [{}]):                                                       # v2: one loft per body shell (own curves, ends, tags, creases)
    G_ = dict(globals()); G_.update(ov_); exec(LOFT_SRC, G_); SHELL_NS.append(G_)
REPORT['shells'] = len(SHELL_NS)
def cage_obj(name):
    objs = [G_['cage_obj'](f'{name}_s{k}') for k, G_ in enumerate(SHELL_NS)]
    if len(objs) == 1: objs[0].name = name; objs[0].data.name = name; return objs[0]
    return join(objs, name, WORK)
if len(SHELL_NS) == 1: globals().update({k: SHELL_NS[0][k] for k in ('RINGS', 'NR', 'NS', 'TAGS', 'FT', 'VB', 'F', 'I_FRONTFACE', 'I_REARFACE')})
def subdiv(o, lv):
    m = o.modifiers.new('s', 'SUBSURF'); m.levels = m.render_levels = lv; m.boundary_smooth = 'ALL'
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='s')
def untear(o, lim=45.0):
    """loops > lim deg off their own face (smooth average across a degenerate fan after heavy dissolve) take the face normal: no dark smear (S1), other loops unchanged."""
    me = o.data; c_ = math.cos(math.radians(lim)); cn = [l.vector.copy() for l in me.corner_normals]; n = 0
    for p in me.polygons:
        for li in p.loop_indices:
            if cn[li].dot(p.normal) < c_: cn[li] = p.normal.copy(); n += 1
    if n: me.normals_split_custom_set(cn)
    REPORT.setdefault('untear', {})[o.name] = n; return n
# ================================================================ 02 body
REF = cage_obj('REF_Skin'); subdiv(REF, 3)                                                              # uncut limit surface: projection reference (cutters, lenses, parts)
BVH = BVHTree.FromObject(REF, bpy.context.evaluated_depsgraph_get())
def ray(o, d):
    loc, nrm, i, dist = BVH.ray_cast(Vector(o), Vector(d))
    if loc is None: return None, None
    if nrm.dot(Vector(d)) > 0: nrm = -nrm
    return loc, nrm
RAY_Y = max(abs(YN), abs(YT), 3.5) + 1.0; RAY_Z = max(v[2] for G_ in SHELL_NS for v in G_['VB']) + 1.5                                   # v2: ray origins from the vehicle's own size (bus 12 m, truck 3.3 m tall)
fhit = lambda x, z: ray((x, -RAY_Y, z), (0, 1, 0)); rhit = lambda x, z: ray((x, RAY_Y, z), (0, -1, 0))
shit = lambda sx, y, z: ray((sx * 3, y, z), (-sx, 0, 0)); thit = lambda x, y: ray((x, y, RAY_Z), (0, 0, -1))
def solid(name, outer, inner, mat, c=None):
    bm = bmesh.new(); a = [bm.verts.new(p) for p in outer]; b = [bm.verts.new(p) for p in inner]; n = len(a)
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(n): j = (i + 1) % n; bm.faces.new((a[i], b[i], b[j], a[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(1), verts=bm.verts, edges=bm.edges)                  # v2: flat outer cap back to ONE n-gon (its sliver fan made the n-ary EXACT boolean ADD the SUV B headlamp cutter)
    if bm.calc_volume(signed=True) < 0: bmesh.ops.reverse_faces(bm, faces=bm.faces); REPORT.setdefault('cutters_flipped', []).append(name)   # guard: never subtract an inside-out cutter
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_' + mat]); o = bpy.data.objects.new(name, me); (c or CUT).objects.link(o); return o
def rounded(pts, r, seg=3):
    out = []; n = len(pts); rs = r if isinstance(r, (list, tuple)) else [r] * n
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n]); d1 = (p0 - p1).normalized(); d2 = (p2 - p1).normalized()
        rr = min(rs[i], (p0 - p1).length * .45, (p2 - p1).length * .45); a_ = p1 + d1 * rr; b_ = p1 + d2 * rr
        for k in range(seg + 1): t = k / seg; q = (1 - t) ** 2 * a_ + 2 * (1 - t) * t * p1 + t * t * b_; out.append((q.x, q.y))
    return out
def mirror_x(poly): return [(-x, z) for x, z in poly][::-1]
def front_pocket(name, poly, depth, mat, rear=False, c=None):
    hitf = rhit if rear else fhit; s = 1 if rear else -1; outer, inner = [], []
    for x, z in poly:
        p, n = hitf(x, z)
        if p is None: print('CUT MISS', name, x, z); return None
        outer.append((x, s * (RAY_Y - .5), z)); inner.append((p.x, p.y - s * depth, p.z))
    return solid(name, outer, inner, mat, c)
def side_pocket(name, poly, depth, mat, sx, c=None):
    outer, inner = [], []
    for y, z in poly:
        p, n = shit(sx, y, z)
        if p is None: print('CUT MISS', name, y, z); return None
        outer.append((sx * 2.0, y, z)); inner.append((p.x - sx * depth, p.y, p.z))
    return solid(name, outer, inner, mat, c)
def top_pocket(name, poly, depth, mat, c=None):
    outer, inner = [], []
    for x, y in poly:
        p, n = thit(x, y)
        if p is None: print('CUT MISS', name, x, y); return None
        outer.append((x, y, RAY_Z - .2)); inner.append((p.x, p.y, p.z - depth))
    return solid(name, outer, inner, mat, c)
def sample_poly(poly, step=.015, closed=True):
    out = []; pairs = list(zip(poly, poly[1:] + (poly[:1] if closed else [])))
    for a_, b_ in pairs:
        a_, b_ = Vector(a_), Vector(b_); n = max(1, int((b_ - a_).length / step)); out += [tuple(a_.lerp(b_, k / n)) for k in range(n)]
    return out
def fence(name, pts_normals, w=.0058, d_in=.009, d_out=.02):
    """closed groove cutter (panel gap, 4.5 mm wide) along a loop on the surface — high-res master only (baked into the normal map)."""
    n = len(pts_normals); bm = bmesh.new(); rr = []
    for i, (p, nr) in enumerate(pts_normals):
        q = pts_normals[(i + 1) % n][0]; r_ = pts_normals[i - 1][0]; tg = (q - r_).normalized(); b = tg.cross(nr).normalized()
        rr.append([bm.verts.new(p + b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 - nr * d_in), bm.verts.new(p + b * w / 2 - nr * d_in)])
    for i in range(n):
        A, B = rr[i], rr[(i + 1) % n]
        for k in range(4): bm.faces.new((A[k], A[(k + 1) % 4], B[(k + 1) % 4], B[k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_pocket'])
    o = bpy.data.objects.new(name, me); CUT_G.objects.link(o); return o
def slot(name, pts_normals, w=.0058, d_in=.009, d_out=.02):
    """open groove (bumper split line): a thin closed loop around a polyline (out and back)."""
    return fence(name, pts_normals + [(p + n * 0, n) for p, n in pts_normals[::-1][1:-1]], w, d_in, d_out)
def loop_top(pts): return [(p, n) for p, n in (thit(x, y) for x, y in pts) if p is not None]
def loop_side(sx, pts): return [(p, n) for p, n in (shit(sx, y, z) for y, z in pts) if p is not None]
def loop_front(pts, rear=False): return [(p, n) for p, n in ((rhit if rear else fhit)(x, z) for x, z in pts) if p is not None]
# ---- openings (cut into master AND game body)
for (y, sx) in ((YF, 1), (YF, -1), (YR, 1), (YR, -1)):                                                   # wheel arches: 55 mm tire clearance, centre 20 mm above the axle
    R_ = RW + .042; seg = 24; zc = RW + .014                                                       # the flared lip owns the visible arch edge
    outer = [(sx * 1.4, y + R_ * math.cos(2 * math.pi * k / seg), zc + R_ * math.sin(2 * math.pi * k / seg)) for k in range(seg)]
    solid(f'arch_{y}_{sx}', outer, [(sx * .56, py, pz) for _, py, pz in outer], 'arch')
for sx in (1, -1):
    front_pocket(f'headlamp_{sx}', HL(sx)[::-1] if sx > 0 else HL(sx), .095, 'housing')
    front_pocket(f'fog_{sx}', FOG(sx) if sx > 0 else FOG(sx)[::-1], .055, 'pocket')
    front_pocket(f'taillamp_{sx}', TL(sx) if sx < 0 else TL(sx)[::-1], .075, 'housing', rear=True)
    for (y0, y1) in HANDLES:                                                                         # door-handle recesses
        side_pocket(f'handle_{sx}_{y0}', rounded([(y0, HANDLE_Z + .014), (y1, HANDLE_Z + .018), (y1, HANDLE_Z - .010), (y0, HANDLE_Z - .014)], .01, 3), .018, 'pocket', sx)
    if EXH: front_pocket(f'exhaust_{sx}', EXH(sx) if sx < 0 else EXH(sx)[::-1], .07, 'plastic', rear=True)
front_pocket('grille', GRILLE[::-1], .075, 'grille'); front_pocket('lower', LOWER[::-1], .085, 'grille')
for k_, poly_ in enumerate(CLAD_F): front_pocket(f'clad_f{k_}', poly_[::-1], .006, 'clad')                     # v2: lower bumper cladding (SUV / pickup)
for k_, poly_ in enumerate(CLAD_R): front_pocket(f'clad_r{k_}', poly_[::-1], .006, 'clad', rear=True)
if globals().get('BED'): top_pocket('bed', BED[0], BED[1], 'plastic')                                      # pickup: open cargo bed (cavity + dark liner walls)
front_pocket('plate_r', (sample_poly(PLATE_R, PLATE_R_STEP) if globals().get('PLATE_R_STEP') else PLATE_R)[::-1], .018, 'plate', rear=True)   # PLATE_R_STEP: dense outline -> recess floor follows a convex rear at constant depth (corner-only outline read as a hexagonal frame); front_pocket('valance', VALANCE[::-1], .022, globals().get('VALANCE_POCKET', 'plastic'), rear=True)
WIN_D = globals().get('WIN_DEPTH', .05)                                                              # v2: real opening behind every GLASS patch in an end face / side panel (the patch alone floated
for k_, (end_, poly_, mat_) in enumerate(globals().get('FACE_GLASS', [])):                            #     4 mm over uncut paint: the paint showed through the glass - bus windshield lobes, door glass)
    if 'Glass' in mat_: front_pocket(f'faceglass_{k_}', poly_[::-1], WIN_D, 'seal', rear=end_ == 'R')
for k_, (sx_, poly_, mat_) in enumerate(globals().get('SIDE_PANELS', [])):
    if 'Glass' in mat_: side_pocket(f'sideglass_{k_}', poly_[::-1], WIN_D, 'seal', sx_)
def inpoly(u, v, poly):
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > v) != (y2 > v) and u < (x2 - x1) * (v - y1) / (y2 - y1) + x1: c = not c
    return c
def open_windows(o):
    """delete each glass pocket's FLOOR (faces facing out, inside the outline, at the pocket depth) -> see-through opening framed by the pocket walls (black reveal)."""
    bm = bmesh.new(); bm.from_mesh(o.data); bm.normal_update(); dead = set(); band = lambda d: WIN_D * .5 < d < WIN_D * 1.6
    for f in bm.faces:
        c = f.calc_center_median(); n = f.normal
        for end_, poly_, mat_ in globals().get('FACE_GLASS', []):
            if 'Glass' in mat_ and abs(n.y) > .9 and inpoly(c.x, c.z, poly_):
                p = (rhit if end_ == 'R' else fhit)(c.x, c.z)[0]
                if p is not None and band(abs(c.y - p.y)): dead.add(f)
        for sx_, poly_, mat_ in globals().get('SIDE_PANELS', []):
            if 'Glass' in mat_ and abs(n.x) > .9 and c.x * sx_ > 0 and inpoly(c.y, c.z, poly_):
                p = shit(sx_, c.y, c.z)[0]
                if p is not None and band(abs(c.x - p.x)): dead.add(f)
    bmesh.ops.delete(bm, geom=list(dead), context='FACES'); bm.to_mesh(o.data); bm.free(); REPORT.setdefault('window_floor_faces', []).append(len(dead)); print('OPEN WINDOWS', o.name, len(dead), flush=True)
# ---- panel gaps (master only -> baked): hood, trunk, 4 doors, fuel door, bumper splits (front + rear, both sides)
fence('gap_hood', loop_top(sample_poly(HOOD_LOOP))) if HOOD_LOOP else None                          # v2: no hood on cab-over trucks / buses
# trunk lid shut line: built below as one 3D path (surf_curve) once BVH paths exist   # trailing edge on the deck, clear of the crisp trunk edge
for sx in (1, -1):
    TOPZ = lambda y: ZBELT(y) + E_('TS_DOORTOP', .022)                                                # r3: door top shut line hidden under the belt seal (real-car); r2 ran it 18 mm under the crisp shoulder -> dashed bake
    if FDOOR: fence(f'gap_fdoor_{sx}', loop_side(sx, sample_poly(FDOOR(TOPZ))))
    if RDOOR: fence(f'gap_rdoor_{sx}', loop_side(sx, sample_poly(RDOOR(TOPZ))))                       # v2: optional (2-door cab, bus)
fence('gap_fuel', loop_side(-1, sample_poly(FUEL))) if FUEL else None   # fuel door (right rear quarter)
def groove_open(name, pn, w=.0055, d_in=.009, d_out=.02):
    """open groove cutter along a polyline on the surface (bumper shut line): square tube with end caps."""
    bm = bmesh.new(); rr = []; n = len(pn)
    for i, (p, nr) in enumerate(pn):
        q = pn[min(i + 1, n - 1)][0]; r_ = pn[max(i - 1, 0)][0]; tg = (q - r_).normalized(); b = tg.cross(nr).normalized()
        rr.append([bm.verts.new(p + b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 + nr * d_out), bm.verts.new(p - b * w / 2 - nr * d_in), bm.verts.new(p + b * w / 2 - nr * d_in)])
    for i in range(n - 1):
        A, B = rr[i], rr[i + 1]
        for k in range(4): bm.faces.new((A[k], A[(k + 1) % 4], B[(k + 1) % 4], B[k]))
    bm.faces.new(rr[0][::-1]); bm.faces.new(rr[-1]); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.materials.append(MM['TMP_pocket']); o = bpy.data.objects.new(name, me); CUT_G.objects.link(o); return o
def sweep_rear(z, c=None, a0=-86, a1=86, n=44):
    c = c or SWEEP_C
    out = []
    for a in np.linspace(math.radians(a0), math.radians(a1), n):
        d = Vector((math.sin(a), math.cos(a), 0)); loc, nrm, i_, dist = BVH.ray_cast(Vector((c[0], c[1], z)), d)
        if loc is not None: out.append((loc, (-nrm if nrm.dot(d) < 0 else nrm)))                     # outward normal
    return out
def surf_curve(guides, step=.005, iters=24):
    """r3: shut-line path = Catmull-Rom through 3D guide points, arc-length resampled every `step`, closest-point projected onto the skin,
    Laplacian-smoothed (ends fixed) with re-projection; frame normal = smoothed skin normal. No grazing ray casts, no twist."""
    G = [Vector(g) for g in guides]; G = [G[0] * 2 - G[1]] + G + [G[-1] * 2 - G[-2]]; dense = []
    for i in range(1, len(G) - 2):
        p0, p1, p2, p3 = G[i - 1], G[i], G[i + 1], G[i + 2]
        for k in range(40):
            t = k / 40; dense.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    dense.append(G[-2]); L = [0.0]
    for a_, b_ in zip(dense, dense[1:]): L.append(L[-1] + (b_ - a_).length)
    n = max(2, int(L[-1] / step)); P = []; j = 0
    for k in range(n + 1):
        s_ = L[-1] * k / n
        while j < len(L) - 2 and L[j + 1] < s_: j += 1
        t = (s_ - L[j]) / max(L[j + 1] - L[j], 1e-9); P.append(dense[j].lerp(dense[j + 1], t))
    proj = lambda p: BVH.find_nearest(p)[0]
    P = [proj(p) for p in P]
    for _ in range(iters):
        P = [P[0]] + [proj((P[i - 1] + 2 * P[i] + P[i + 1]) / 4) for i in range(1, len(P) - 1)] + [P[-1]]
    N = [BVH.find_nearest(p)[1].normalized() for p in P]
    for _ in range(6): N = [N[0]] + [(N[i - 1] + 2 * N[i] + N[i + 1]).normalized() for i in range(1, len(N) - 1)] + [N[-1]]
    return list(zip(P, N))
ARC = lambda y0, ang, r=RW + .042 + .020: (y0 + r * math.cos(math.radians(ang)), RW + .014 + r * math.sin(math.radians(ang)))   # point under the flared arch lip
def side_pt(sx, y, z): p, n = shit(sx, y, z); return p
# rear bumper shut line: under the RR arch lip -> quarter -> around the corner -> across the face -> quarter -> under the RL arch lip
if REAR_SHUT:                                                                                        # v2: optional (box truck / bus: no car bumper split)
  rs = [ARC(YR, 35)] + REAR_SHUT
  side_R = [side_pt(-1, y, z) for y, z in rs]; side_L = [side_pt(1, y, z) for y, z in rs]
  face_ = [p for p, n in sweep_rear(REAR_SHUT_Z, n=60) if p.y > REAR_SHUT_FACE_Y]                                            # corner + face (radial rays: never grazing)
  groove_open('shut_rear_bumper', surf_curve(side_R + face_[::4] + [face_[-1]] + side_L[::-1]))
def _tp(f, a, b): p = f(a, b)[0]; assert p is not None, ('trunk path miss', a, b); return p
HITF = {'r': lambda a, b: rhit(a, b), 't': lambda a, b: thit(a, b)}
if LID_SIDE:
  TLID = [[_tp(HITF[k], sx * a, b) for k, a, b in LID_SIDE] for sx in (-1, 1)]                          # trunk lid / tailgate shut line (design guides, sx = +1 side)
  lid_path = TLID[0] + [_tp(HITF[k], a, b) for k, a, b in LID_MID] + TLID[1][::-1]
  groove_open('shut_lid', surf_curve(lid_path))
for sx in ((1, -1) if FSHUT_LAMP else ()):                                                             # fascia / fender split: starts inside the headlamp opening, ends under the arch lip
    lamp = fhit(sx * FSHUT_LAMP[0], FSHUT_LAMP[1])[0]                                                                    # H2: start 4 mm outside the sharp lamp tip (under the 10 mm frame); inside the opening it grazed the cut wall
    yA, zA = ARC(YF, FSHUT_ARC)
    groove_open(f'shut_front_{sx}', surf_curve([lamp, side_pt(sx, lamp.y + .07, FSHUT_Z1)] + [side_pt(sx, y, z) for y, z in FSHUT_MID] + [side_pt(sx, yA, zA)]))
HITX = {'r': lambda a, b: rhit(a, b), 't': lambda a, b: thit(a, b), 'f': lambda a, b: fhit(a, b), 'sL': lambda a, b: shit(1, a, b), 'sR': lambda a, b: shit(-1, a, b)}
for k_, gd_ in enumerate(globals().get('EXTRA_GROOVES', [])):                                        # v2: extra shut lines from design guides, e.g. box-truck rear-door split
    groove_open(f'shut_extra_{k_}', surf_curve([_tp(HITX[k], a, b) for k, a, b in gd_]))
if globals().get('CAB_GAP'):                                                                          # pickup: separate cab / bed — shut line on each side (3D path, both ends hidden in the bed cut / sill)
    for sx in (1, -1): groove_open(f'cab_gap_{sx}', surf_curve([side_pt(sx, CAB_GAP[0], z) for z in np.linspace(CAB_GAP[1], CAB_GAP[2], 5)]), w=.008)
def apply_cuts(o, cc):
    """v2: VERIFIED boolean cascade. The EXACT boolean can ADD a cutter (SUV B headlamp / SUV A plate -> 0.6-1.3 m planks) or DESTROY the skin
    (hatchback master -> 496 tris). Every step is checked (nothing outside the uncut skin bounds + surface area >= 90 % of before) and restored on failure:
    1) all cutters at once (n-ary, v1 behaviour)  2) pockets at once, then grooves at once  3) one cutter at a time: plain -> hole-tolerant -> 0.1 % inflated -> skip + report."""
    lo_ = np.array([min(v.co[k] for v in REF.data.vertices) - .01 for k in range(3)]); hi_ = np.array([max(v.co[k] for v in REF.data.vertices) + .01 for k in range(3)])
    def area():
        ar = np.empty(len(o.data.polygons)); o.data.polygons.foreach_get('area', ar); return float(ar.sum())
    def bad(a0):
        co = np.empty(len(o.data.vertices) * 3); o.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        return int(((co < lo_) | (co > hi_)).any(1).sum()) > 0 or area() < .90 * a0
    def run(target, tol=False, self_=False):
        m_ = o.modifiers.new('cut', 'BOOLEAN'); m_.operation = 'DIFFERENCE'; m_.solver = 'EXACT'; m_.use_hole_tolerant = tol; m_.use_self = self_
        if isinstance(target, bpy.types.Collection): m_.operand_type = 'COLLECTION'; m_.collection = target
        else: m_.object = target
        if hasattr(m_, 'material_mode'): m_.material_mode = 'TRANSFER'
        with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='cut')
    def attempt(label, fn):
        keep = o.data.copy(); a0 = area(); fn()
        if not bad(a0): bpy.data.meshes.remove(keep); return True
        old = o.data; o.data = keep; bpy.data.meshes.remove(old); REPORT.setdefault('cut_retries', []).append(f'{o.name}:{label}'); return False
    def group(objs, name):
        c = bpy.data.collections.new(name); [c.objects.link(x) for x in objs]; return c
    allc = list(cc.objects)
    if attempt('all', lambda: run(cc)): REPORT.setdefault('cut_mode', {})[o.name] = 'n-ary'; return
    isg = lambda x: x.name.startswith(('gap_', 'shut_', 'cab_gap'))
    for gname, objs in (('pockets', [x for x in allc if not isg(x)]), ('grooves', [x for x in allc if isg(x)])):
        if not objs or attempt(gname, lambda: run(group(objs, 'TMPC_' + gname))): continue
        for c_ in sorted(objs, key=lambda x: x.name):
            ok = attempt(f'{c_.name}:plain', lambda: run(c_, self_=isg(c_))) or attempt(f'{c_.name}:hole_tolerant', lambda: run(c_, True, isg(c_)))
            if not ok:
                cen = sum((v.co for v in c_.data.vertices), Vector()) / len(c_.data.vertices)
                for v in c_.data.vertices: v.co = cen + (v.co - cen) * 1.001
                ok = attempt(f'{c_.name}:inflated', lambda: run(c_, True, isg(c_)))
            if not ok: REPORT.setdefault('cutters_skipped', []).append(f'{o.name}:{c_.name}'); print('CUTTER SKIPPED', o.name, c_.name, flush=True)
    REPORT.setdefault('cut_mode', {})[o.name] = 'cascade'
ALLC = coll('TS_ALLCUT')
for o in list(CUT.objects) + list(CUT_G.objects): ALLC.objects.link(o)
if os.environ.get('TS_SAVE_CUTTERS'): bpy.ops.wm.save_as_mainfile(filepath=os.environ['TS_SAVE_CUTTERS'], copy=True); sys.exit(0)   # diagnosis: cutters + skin before the boolean
HI = cage_obj('REF_Master'); subdiv(HI, 3); apply_cuts(HI, ALLC); open_windows(HI); HI.data.shade_smooth()
LO = cage_obj('Body_Game'); subdiv(LO, 1); apply_cuts(LO, CUT); open_windows(LO)
REPORT['master_tris'] = tris(HI); REPORT['cutters'] = sorted(o.name for o in CUT.objects); REPORT['grooves'] = sorted(o.name for o in CUT_G.objects)
for c_ in (ALLC, CUT, CUT_G):
    for o in list(c_.objects): bpy.data.objects.remove(o, do_unlink=True) if o.name in bpy.data.objects else None
clean(LO)
# game body = cage at subdivision level 1 (clean quads; material boundaries stay on cage lines - no decimation tears); smoothness comes from the bake
def split_by(o, pred, new_name):
    me2 = o.data.copy(); n = bpy.data.objects.new(new_name, me2); o.users_collection[0].objects.link(n)
    for ob, keep in ((o, lambda m: not pred(m)), (n, pred)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if not keep(mats[f.material_index].name if mats[f.material_index] else '')], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    purge_slots(n); purge_slots(o); return n
GLASS = split_by(LO, lambda m: m == 'TS_Glass', 'Glass_Shell')
BODYTRIM = split_by(LO, lambda m: m.startswith('TMP_'), 'BodyTrim')                                   # pocket walls, seals, arch walls -> atlas
REPORT['body_paint_tris'] = tris(LO); REPORT['bodytrim_tris'] = tris(BODYTRIM); REPORT['glass_tris'] = tris(GLASS)
# ---- body-colour mirror housings + roof antenna fin: part of the paint body (unique UVs, baked like the rest; copies added to the master)
MIRC = {sx: Vector((sx * MIRROR_POS[0], MIRROR_POS[1], MIRROR_POS[2])) for sx in (1, -1)}
def mirror_housing(sx):
    """tapered rounded-box housing: outboard end taller, flat rear face (glass sits there), rounded aero front."""
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=MIRROR_SIZE, verts=bm.verts)
    bmesh.ops.bevel(bm, geom=[e for e in bm.edges if not all(v.co.y > .03 for v in e.verts)], offset=.030, segments=3, affect='EDGES', profile=.55)
    for v in bm.verts:
        t = min(max((v.co.x * sx + .10) / .20, 0.0), 1.0); v.co.z *= lerp(.58, 1.0, t ** .8); v.co.y *= lerp(.75, 1.0, t)                          # H2 wing: thin at the door, tall outboard
        if v.co.z < 0: v.co.y += .018 * (-v.co.z / .049) * (1 if v.co.y < 0 else 0)                                            # swept-back lower edge
        if v.co.y < 0: v.co.y *= 1.0 + .45 * (1 - abs(v.co.z) / .055) * (1 - abs(v.co.x) / .11)                                 # aero front bulge
        v.co += MIRC[sx]
    me = bpy.data.meshes.new('MirH'); bm.to_mesh(me); bm.free(); me.materials.append(M[PRE + '_Paint']); o = bpy.data.objects.new(f'MirrorHousing_{sx}', me); WORK.objects.link(o); return o
def antenna_fin():
    prof = [(FIN_Y0 + d, h) for d, h in ((0, 0.0), (.10, .012), (.18, .045), (.22, .058), (.25, .040), (.265, 0.0))]; Vs = []; Fs = []
    for y, h in prof:
        p, n = thit(0, y); Vs += [(-.028 * (h > 0) - .006, y, p.z - .004), (.028 * (h > 0) + .006, y, p.z - .004), (0, y, p.z + h)]
    for i in range(len(prof) - 1):
        a0 = 3 * i; b0 = 3 * (i + 1); Fs += [(a0, b0, b0 + 2, a0 + 2), (a0 + 1, a0 + 2, b0 + 2, b0 + 1)]
    me = bpy.data.meshes.new('Fin'); me.from_pydata(Vs, [], Fs); me.materials.append(M[PRE + '_Paint']); o = bpy.data.objects.new('AntennaFin', me); WORK.objects.link(o)
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free(); return o
def arch_lip(y, sx, seg=20):
    Re = RW + .042; zc = RW + .014; a0, a1 = math.radians(-6), math.radians(186); rows = [[], [], []]
    for q in range(seg + 1):
        a = lerp(a0, a1, q / seg); ca, sa = math.cos(a), math.sin(a)
        p0, n0 = shit(sx, y + (Re + .036) * ca, zc + (Re + .036) * sa); p1, n1 = shit(sx, y + (Re + .006) * ca, zc + (Re + .006) * sa)
        if p0 is None or p1 is None: return None
        rows[0].append(p0 + n0 * .0015); rows[1].append(p1 + n1 * .009)
        rows[2].append(Vector((p1.x - sx * .032, y + (Re - .002) * ca, zc + (Re - .002) * sa)))
    LT = 'TMP_clad' if CLADDING else PRE + '_Paint'                                                  # SUV: dark arch cladding
    g = Geo(); g.strip(rows[0], rows[1], LT, flip=sx < 0); g.strip(rows[1], rows[2], LT, flip=sx < 0)
    o = mk(f'ArchLip_{y}_{sx}', g.V, g.F, g.T, WORK, M); orient_out(o, centre=(0, y, zc))
    fa = o.data.attributes.new('flatbake', 'INT', 'FACE'); fa.data.foreach_set('value', [1] * len(o.data.polygons)); return o
LIPS = [l_ for l_ in (arch_lip(y, sx) for y in (YF, YR) for sx in (1, -1)) if l_]
REPORT['arch_lips'] = len(LIPS)
FIN_YR = (FIN_Y0 - .02, FIN_Y0 + .30) if FIN_Y0 is not None else (1e9, -1e9)                         # fin face band for the LOD keep-rules (empty when there is no fin)
EXTRA = [mirror_housing(1), mirror_housing(-1)] + ([antenna_fin()] if FIN_Y0 is not None else []) + LIPS   # FIN_Y0 = None: no car shark-fin (commercial cabs)
for e_ in EXTRA:
    c_ = e_.copy(); c_.data = e_.data.copy(); WORK.objects.link(c_); HI = join([HI, c_], 'REF_Master', WORK)
def master_normals(o, tol=.0005, agree=.82):
    """r3: loops on the skin get the uncut skin's interpolated smooth normal (boolean slivers no longer shade themselves);
    loops of faces that disagree (groove / pocket walls) get their flat face normal; everything off the skin keeps its own."""
    from mathutils.interpolate import poly_3d_calc
    rme = REF.data; RV = [v.co.copy() for v in rme.vertices]; RN = [v.normal.copy() for v in rme.vertices]; RP = [tuple(p.vertices) for p in rme.polygons]
    bvp = BVHTree.FromPolygons(RV, RP); me = o.data; cn = [c.vector.copy() for c in me.corner_normals]; vmap = {}
    for v in me.vertices:
        loc, nrm, fi, d = bvp.find_nearest(v.co)
        if loc is None or d > tol: continue
        ids = RP[fi]; w = poly_3d_calc([RV[i] for i in ids], v.co); vmap[v.index] = sum((RN[i] * wi for i, wi in zip(ids, w)), Vector()).normalized()
    nrep = nflat = 0
    for p in me.polygons:
        for li in p.loop_indices:
            vi = me.loops[li].vertex_index
            if vi not in vmap: continue
            if p.normal.dot(vmap[vi]) > agree: cn[li] = vmap[vi]; nrep += 1
            else: cn[li] = p.normal.copy(); nflat += 1
    me.normals_split_custom_set(cn); REPORT['master_normals'] = dict(skin_loops=nrep, wall_loops_flat=nflat, verts_on_skin=len(vmap)); print('MASTER NORMALS', nrep, nflat, len(vmap), flush=True)
master_normals(HI)
LO = join([LO] + EXTRA, 'Body_Game', WORK)
_t0 = tris(LO); bm = bmesh.new(); bm.from_mesh(LO.data); bm.faces.ensure_lookup_table()
near_cut = {v for e in bm.edges if e.is_boundary for v in e.verts}                                     # vertices on any opening / arch edge
okf = lambda f: not any(v in near_cut for v in f.verts)
bm.normal_update(); top_ = lambda f: f.normal.z > E_('TS_TOP_NZ', .55)                              # r3: hood / roof / deck keep a finer mesh (long slivers forced big 8-bit normal-map
ed = [e for e in bm.edges if len(e.link_faces) == 2 and all(okf(f) for f in e.link_faces)]             #     corrections -> stair-stepped highlight on the hood)
dn_ = lambda f: f.normal.z < -.70 and f.calc_center_median().z < .34                                  # r3: under-bumper / underside faces (never seen from any game camera): coarse dissolve, surface stays closed
edd = [e for e in ed if all(dn_(f) for f in e.link_faces)]; ed = [e for e in ed if not all(dn_(f) for f in e.link_faces)]
bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(E_('TS_PLANAR_DOWN_DEG', 12.0)), use_dissolve_boundaries=False, edges=edd, verts=[], delimit={'MATERIAL'})
ed = [e for e in ed if e.is_valid]
edt = [e for e in ed if all(top_(f) for f in e.link_faces)]; eds = [e for e in ed if not all(top_(f) for f in e.link_faces)]
bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(float(os.environ.get('TS_PLANAR_DEG', 3.0))), use_dissolve_boundaries=False, edges=eds, verts=[], delimit={'MATERIAL'})
edt = [e for e in edt if e.is_valid]
if E_('TS_PLANAR_TOP_DEG', 0.5) > 0: bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(E_('TS_PLANAR_TOP_DEG', 0.5)), use_dissolve_boundaries=False, edges=edt, verts=[], delimit={'MATERIAL'})
bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4], quad_method='BEAUTY', ngon_method='BEAUTY'); bm.to_mesh(LO.data); bm.free(); clean(LO)
inv_ = 0
for p_ in LO.data.polygons:
    loc_, nrm_, i_, d_ = BVH.find_nearest(p_.center)
    if loc_ is not None and d_ < .05 and nrm_.dot(p_.normal) < -.2: inv_ += 1
REPORT['body_inverted_faces'] = inv_; print('INVERTED', inv_, flush=True)
REPORT['body_planar_dissolve'] = dict(before=_t0, after=tris(LO)); print('PLANAR', _t0, '->', tris(LO), flush=True)   # flat regions: fewer triangles, the baked normal map carries the shading
bm = bmesh.new(); bm.from_mesh(LO.data); bm.normal_update()
bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.normal.z < -.75 and f.calc_center_median().z < .26 and abs(f.calc_center_median().y) < UNDER_Y], context='FACES'); bm.to_mesh(LO.data); bm.free()   # hidden underside (underbody tray covers it)
# ---- shading of the game body: smooth, hard edges only at real breaks (opening rims), then UV unwrap + normal bake from the master
LO.data.shade_smooth(); LO.data.set_sharp_from_angle(angle=math.radians(48))
if globals().get('FLAT_PLANAR'):   # truck / bus: large flat panels shade with their own face normal - the rim normal averaged with the rounded box corners streaked across the long planar-dissolve slivers ("cracks" on the rear doors)
    me_ = LO.data; P_ = me_.polygons; cn_ = [c.vector.copy() for c in me_.corner_normals]; adj_ = {}; seen_ = set(); nfl_ = 0; cos1 = math.cos(math.radians(1.0))
    for p_ in P_:
        for ek in p_.edge_keys: adj_.setdefault(ek, []).append(p_.index)
    for p_ in P_:
        if p_.index in seen_: continue
        n0 = p_.normal.copy(); reg = [p_.index]; seen_.add(p_.index); q_ = [p_.index]
        while q_:                                                                                       # grow against the SEED normal (no drift along gentle curves)
            for ek in P_[q_.pop()].edge_keys:
                for g_ in adj_[ek]:
                    if g_ not in seen_ and P_[g_].normal.dot(n0) > cos1: seen_.add(g_); reg.append(g_); q_.append(g_)
        if sum(P_[i].area for i in reg) >= FLAT_PLANAR:
            for i in reg:
                for li in P_[i].loop_indices: cn_[li] = P_[i].normal.copy(); nfl_ += 1
    me_.normals_split_custom_set(cn_); REPORT['flat_planar_loops'] = nfl_; print('FLAT PLANAR loops', nfl_, flush=True)
bpy.context.view_layer.objects.active = LO
for o in bpy.context.view_layer.objects: o.select_set(o == LO)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(float(os.environ.get('TS_UV_ANGLE', 58))), island_margin=.006, area_weight=.3, correct_aspect=True, scale_to_bounds=False)
bpy.ops.uv.pack_islands(margin=.006, rotate=True)
bpy.ops.object.mode_set(mode='OBJECT')
def bake_normal(low, high, img_name, res, path):
    SS = int(E_('TS_BAKE_SS', 2)); out_res = res; res = res * SS                                     # r3: supersampled bake (2x, box-filtered down): 5.8 mm panel gaps were ~2.4 texels -> dashed / beaded
    img = bpy.data.images.new(img_name + '_ss', res, res, alpha=False, float_buffer=True); img.colorspace_settings.name = 'Non-Color'
    bm_ = bpy.data.materials.new('BAKE_TMP'); bm_.use_nodes = True; tn = bm_.node_tree.nodes.new('ShaderNodeTexImage'); tn.image = img; bm_.node_tree.nodes.active = tn
    saved = [m for m in low.data.materials]; low.data.materials.clear(); low.data.materials.append(bm_)
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 1
    try:
        pr = bpy.context.preferences.addons['cycles'].preferences; pr.compute_device_type = 'METAL'; pr.get_devices(); [setattr(d, 'use', True) for d in pr.devices]; sc.cycles.device = 'GPU'
    except Exception as e: print('bake on CPU', e)
    hr, hv = high.hide_render, high.hide_viewport; high.hide_render = False; high.hide_viewport = False
    for o in bpy.context.view_layer.objects: o.select_set(o in (low, high))
    bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(type='NORMAL', normal_space='TANGENT', use_selected_to_active=True, cage_extrusion=float(os.environ.get('TS_CAGE', .03)), max_ray_distance=float(os.environ.get('TS_RAY', .07)), margin=8 * SS, use_clear=True)
    high.hide_render, high.hide_viewport = hr, hv
    fl = low.data.attributes.get('flatbake')                                                         # thin rolled parts (arch lips): flat tangent normal (own smooth geometry shades them)
    if fl:
        W_ = img.size[0]; px = np.array(img.pixels[:], np.float32).reshape(W_, W_, 4); uvd = low.data.uv_layers.active.data; nflat = 0
        for p_ in low.data.polygons:
            if not fl.data[p_.index].value: continue
            P = np.array([uvd[li].uv[:] for li in p_.loop_indices]) * W_; c_ = P.mean(0); P = c_ + (P - c_) * 1.0 + np.sign(P - c_) * 3.0   # 3 px dilation
            for k_ in range(1, len(P) - 1):
                T_ = np.array([P[0], P[k_], P[k_ + 1]]); x0, y0 = np.floor(T_.min(0)).astype(int); x1, y1 = np.ceil(T_.max(0)).astype(int)
                x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W_ - 1), min(y1, W_ - 1)
                if x1 < x0 or y1 < y0: continue
                yy, xx = np.mgrid[y0:y1 + 1, x0:x1 + 1] + .5; a_, b_, c2 = T_
                den = (b_[1] - c2[1]) * (a_[0] - c2[0]) + (c2[0] - b_[0]) * (a_[1] - c2[1])
                if abs(den) < 1e-9: continue
                l1 = ((b_[1] - c2[1]) * (xx - c2[0]) + (c2[0] - b_[0]) * (yy - c2[1])) / den; l2 = ((c2[1] - a_[1]) * (xx - c2[0]) + (a_[0] - c2[0]) * (yy - c2[1])) / den
                m_ = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1); sub = px[y0:y1 + 1, x0:x1 + 1]; sub[m_] = (.5, .5, 1.0, 1.0); nflat += int(m_.sum())
        img.pixels.foreach_set(px.ravel()); print('FLATBAKE texels', nflat, flush=True)
    if SS > 1:
        px = np.array(img.pixels[:], np.float32).reshape(res, res, 4); n_ = px[..., :3] * 2 - 1
        n_ = n_.reshape(out_res, SS, out_res, SS, 3).mean((1, 3)); n_ /= np.maximum(np.linalg.norm(n_, axis=2, keepdims=True), 1e-6)
        o_ = np.dstack([n_ * .5 + .5, np.ones((out_res, out_res, 1), np.float32)]); bpy.data.images.remove(img)
        if E_('TS_BAKE_DITHER', 0) or globals().get('BAKE_DITHER'): o_[..., :3] += (np.random.default_rng(7).random((out_res, out_res, 3), np.float32) - .5) / 255.0   # opt-in: +-0.5 LSB dither breaks 8-bit banding (stair-stepped zebra on gentle hoods)
        img = bpy.data.images.new(img_name, out_res, out_res, alpha=False, float_buffer=False); img.colorspace_settings.name = 'Non-Color'; img.pixels.foreach_set(o_.ravel())
    img.filepath_raw = path; img.file_format = 'PNG'; img.save(); low.data.materials.clear()
    for m in saved: low.data.materials.append(m)
    bpy.data.materials.remove(bm_); return path
if os.environ.get('TS_NOBAKE'): assert SCR; save_ckp(CKP_ + '_02_body.blend'); sys.exit(0)                     # geometry trials only (scratch)
NORMAL0 = None if BLOCKOUT else bake_normal(LO, HI,f'{PRE}_Body_Normal', int(os.environ.get('TS_BAKE_RES', 2048)), OUTD('textures', f'{PRE}_Body_Normal.png'))
M.update(paint_material(PRE + '_Paint', PAINT_RGB, dict(normal=NORMAL0) if NORMAL0 else None, TEX, finish=globals().get('PAINT_FINISH')))
REPORT['body_normal'] = os.path.basename(NORMAL0) if NORMAL0 else None
HI.hide_render = True; HI.hide_viewport = True
save_ckp(CKP_ + '_02_body.blend') if LAST >= 2 else None
if LAST <= 2: sys.exit(0)
# ================================================================ 03 exterior parts, lamps, glass (real depth; nothing painted-on)
TR, LI = Geo(), Geo()
def grow(poly, d):
    c = centroid2(poly); return [tuple(c + (Vector(p) - c) * (1 + d / max((Vector(p) - c).length, 1e-6))) for p in poly]
def rim_band(g, poly, hitf, w_out, w_in, off, t, step=.030):
    """thin frame on the skin across an opening outline (outline grown by w_out .. shrunk by w_in), `off` above the skin."""
    ring = sample_poly(poly, step); c = centroid2(ring); A, B = [], []; n_ = len(ring)
    for i_, (x, z) in enumerate(ring):                                                                # v2: offset along the outline's own normal (radial-from-centroid made long frames lens-shaped)
        q = Vector((x, z)); tg = Vector(ring[(i_ + 1) % n_]) - Vector(ring[i_ - 1]); dv = Vector((tg.y, -tg.x)).normalized()
        if dv.dot(q - c) < 0: dv = -dv
        pa, na = hitf(*(q + dv * w_out)); pb, nb = hitf(*(q - dv * w_in))
        if pa is None or pb is None: print('RIM MISS', t); return
        A.append(pa + na * off); B.append(pb + nb * off)
    g.strip(A, B, t, closed=True)
def ptat(hitf, a, b, depth):
    p, n = hitf(a, b); return None if p is None else p - n * depth
def centroid2(poly): return Vector((sum(x for x, _ in poly) / len(poly), sum(z for _, z in poly) / len(poly)))
def surf_patch(g, poly, hitf, off, t, step=.026, shrink=1.0):
    """surface-following panel / lens over a closed outline (polar fan from the outline centroid; exact outline), offset `off` along the skin normal."""
    ring = sample_poly(poly, step); c = centroid2(ring); rows = []
    for k in (shrink, shrink * .5):
        row = []
        for x, z in ring:
            q = c.lerp(Vector((x, z)), k); p, n = hitf(q.x, q.y); row.append(p + n * off if p is not None else None)
        rows.append(row)
    if any(p is None for r in rows for p in r): print('PATCH MISS', t); return
    pc, nc = hitf(c.x, c.y); n0 = len(g.V); nr = len(ring)
    for r in rows: g.V += [tuple(p) for p in r]
    g.V.append(tuple(pc + nc * off))
    for i in range(1):
        for j in range(nr): g.F.append((n0 + i * nr + j, n0 + i * nr + (j + 1) % nr, n0 + (i + 1) * nr + (j + 1) % nr, n0 + (i + 1) * nr + j)); g.T.append(t)
    for j in range(nr): g.F.append((n0 + nr + j, n0 + nr + (j + 1) % nr, n0 + 2 * nr)); g.T.append(t)
def surf_grid(g, poly, hitf, off, t, nu=24, nv=8):
    """structured surface-following panel for large curved glass: nu columns across u (cosine-spaced, dense at the rounded ends) x nv rows along v,
    every point on the skin + off along its normal. The polar fan (surf_patch) made 76:1 slivers around one valence-99 centre -> an X in reflections."""
    us_ = [p[0] for p in poly]; u0, u1 = min(us_) + .004, max(us_) - .004; cols = []; nrm_ = None
    for i in range(nu + 1):
        u = u0 + (u1 - u0) * (.5 - .5 * math.cos(math.pi * i / nu)); vb, vt = edge_z(poly, u)
        if vb is None or vt - vb < .004: return surf_patch(g, poly, hitf, off, t)
        col = []
        for j in range(nv + 1):
            p, n = hitf(u, lerp(vb, vt, j / nv))
            if p is None: return surf_patch(g, poly, hitf, off, t)
            col.append(p + n * off); nrm_ = nrm_ or n
        cols.append(col)
    rev = (cols[1][0] - cols[0][0]).cross(cols[0][1] - cols[0][0]).dot(nrm_) < 0                  # wind every quad to face out along the skin normal
    for i in range(nu):
        A, B = cols[i], cols[i + 1]
        for j in range(nv):
            q = [A[j], B[j], B[j + 1], A[j + 1]]; g.add(q[::-1] if rev else q, [(0, 1, 2, 3)], t)
def bezel(g, poly, hitf, d0, d1, k1, t, step=.04):
    """depth ring inside an opening: outline at depth d0 -> outline shrunk to k1 at depth d1 (gives a lamp / grille real inner wall)."""
    ring = sample_poly(poly, step); c = centroid2(ring); A, B = [], []
    for x, z in ring:
        p0 = ptat(hitf, x, z, d0); q = c.lerp(Vector((x, z)), k1); p1 = ptat(hitf, q.x, q.y, d1)
        if p0 is None or p1 is None: print('BEZEL MISS', t); return
        A.append(p0); B.append(p1)
    g.strip(A, B, t, closed=True)
def ribbon(g, hitf, pts, h, depth, t):
    """light guide / trim ribbon of height h along a polyline of (x, z) points, `depth` behind the skin."""
    A = [ptat(hitf, x, z - h / 2, depth) for x, z in pts]; B = [ptat(hitf, x, z + h / 2, depth) for x, z in pts]
    if any(p is None for p in A + B): print('RIBBON MISS', t); return
    g.strip(A, B, t)
def cup(g, centre, axis, r, depth, seg, t_rim, t_core=None, rc=.010):
    """reflector bowl: rim ring -> apex along -axis; optional emitter disc at the bottom."""
    axis = Vector(axis).normalized(); a = Vector((1, 0, 0)) if abs(axis.x) < .9 else Vector((0, 0, 1)); b1 = axis.cross(a).normalized(); b2 = axis.cross(b1)
    ring = lambda rr, d: [Vector(centre) - axis * d + (b1 * math.cos(2 * math.pi * k / seg) + b2 * math.sin(2 * math.pi * k / seg)) * rr for k in range(seg)]
    g.strip(ring(r, 0), ring(rc + .004, depth), t_rim, closed=True)
    if t_core: g.cap(ring(rc + .004, depth), t_core, centre=Vector(centre) - axis * (depth - .004))
def tube(g, p0, p1, r, seg, t, cap_end=True):
    p0, p1 = Vector(p0), Vector(p1); ax = (p1 - p0).normalized(); a = Vector((1, 0, 0)) if abs(ax.x) < .9 else Vector((0, 0, 1)); b1 = ax.cross(a).normalized(); b2 = ax.cross(b1)
    ring = lambda p: [p + (b1 * math.cos(2 * math.pi * k / seg) + b2 * math.sin(2 * math.pi * k / seg)) * r for k in range(seg)]
    g.strip(ring(p0), ring(p1), t, closed=True)
    if cap_end: g.cap(ring(p1), t, centre=p1)
def box_rail(g, top, w, h, t):
    """v2 roof rail: closed rectangular section swept along the top line (one closed component; ends capped)."""
    S = [[p + Vector((-w / 2, 0, 0)), p + Vector((w / 2, 0, 0)), p + Vector((w / 2, 0, -h)), p + Vector((-w / 2, 0, -h))] for p in top]
    n0 = len(g.V); g.V += [tuple(q) for s_ in S for q in s_]; n = len(S)
    for i in range(n - 1):
        for k in range(4): g.F.append((n0 + 4 * i + k, n0 + 4 * i + (k + 1) % 4, n0 + 4 * (i + 1) + (k + 1) % 4, n0 + 4 * (i + 1) + k)); g.T.append(t)
    g.F.append(tuple(n0 + k for k in range(4))); g.T.append(t); g.F.append(tuple(n0 + 4 * (n - 1) + k for k in (3, 2, 1, 0))); g.T.append(t)
def vane(xc, z0, z1, d0, d1, w, front, side, n=3, hit=None):
    """real bar: front face of width 2w (faces the viewer) + two side walls running d0 -> d1 deep (no edge-on invisible planes)."""
    hit = hit or fhit; zs_ = np.linspace(z0, z1, n)
    F0 = [ptat(hit, xc - w, z, d0) for z in zs_]; F1 = [ptat(hit, xc + w, z, d0) for z in zs_]; B0 = [ptat(hit, xc - w, z, d1) for z in zs_]; B1 = [ptat(hit, xc + w, z, d1) for z in zs_]
    if any(p is None for p in F0 + F1 + B0 + B1): return
    TR.strip(F0, F1, front); TR.strip(F0, B0, side); TR.strip(F1, B1, side)
def edge_z(poly, x):
    """(z_bottom, z_top) of a closed (x, z) outline at abscissa x."""
    zs = [z1 + (x - x1) / (x2 - x1) * (z2 - z1) for (x1, z1), (x2, z2) in zip(poly, poly[1:] + poly[:1]) if (x1 - x) * (x2 - x) <= 0 and abs(x2 - x1) > 1e-9]
    return (min(zs), max(zs)) if zs else (None, None)
def along(poly, xa, xb, dz, side, n=4):
    """points following the top (side=+1) or bottom (side=-1) edge of an outline, dz inside."""
    out = []
    for x in np.linspace(xa, xb, n):
        zb, zt = edge_z(poly, x)
        if zb is None: continue
        out.append((x, zt - dz) if side > 0 else (x, zb + dz))
    return out
for sx in (1, -1):
    IND = 'TS_Lights:Indicator_L' if sx > 0 else 'TS_Lights:Indicator_R'
    P = HL(1); X0, X1 = min(p[0] for p in P), max(p[0] for p in P); W_ = X1 - X0
    # ---- headlamp (generic): inner bezel, housing back with depth, N projector modules, segmented LED DRL along the top edge, amber indicator along the bottom, clear lens, frame
    bezel(LI, HL(sx), fhit, .004, .030, .90, 'TS_Atlas:lamp_inner', step=.06)
    surf_patch(LI, HL(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .048, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:lamp_housing', step=.05, shrink=.94)
    for i_ in range(HL_CELLS):
        x_ = lerp(X0 + .06, X1 - .08, i_ / max(HL_CELLS - 1, 1)); zb, zt = edge_z(P, x_)
        if zb is None: continue
        p, n = fhit(sx * x_, (zb + zt) / 2 - .002); r_ = min(.017, (zt - zb) * .32)
        if p is not None: cup(LI, p - n * .022, -n, r_, .028, 7, 'TS_Atlas:reflector', 'TS_Lights:Headlamp', rc=r_ * .45)
    for k_ in range(HL_DRL_SEGS):
        t0, t1 = k_ / HL_DRL_SEGS + .012, (k_ + 1) / HL_DRL_SEGS - .012
        pts_ = along(P, lerp(X0 + .02, X1 - .015, t0), lerp(X0 + .02, X1 - .015, t1), .010, +1, 3)
        if len(pts_) >= 2: ribbon(LI, fhit, [(sx * x, z) for x, z in pts_], .008, .016, 'TS_Lights:DRL')
    pts_ = along(P, X0 + .62 * W_, X1 - .02, .010, -1, 3)
    if len(pts_) >= 2: ribbon(LI, fhit, [(sx * x, z) for x, z in pts_], .008, .020, IND)
    surf_patch(LI, HL(sx), fhit, .004, 'TS_Lens', step=.032)
    rim_band(TR, HL(sx), fhit, .010, .004, .0058, 'TS_Atlas:gloss_black')
    # ---- side intake (generic): honeycomb back, frame, aero blades
    if FOG:
        surf_patch(TR, FOG(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .050, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:grille', step=.05)
        rim_band(TR, FOG(sx), fhit, .008, .003, .004, 'TS_Atlas:gloss_black')
        Q = FOG(1); qx = sum(p[0] for p in Q) / len(Q); qz0, qz1 = min(p[1] for p in Q) + .03, max(p[1] for p in Q) - .02
        for dx in INTAKE_BLADES: vane(sx * (qx + dx), qz0, qz1, .010, .044, .004, 'TS_Atlas:dark_chrome', 'TS_Atlas:gloss_black')
    # ---- tail lamp (generic): housing field, bezel depth, LED tail guide along the top, brake block, indicator, red lens, frame; split at the lid line
    T = TL(1); U0, U1 = min(p[0] for p in T), max(p[0] for p in T); WT_ = U1 - U0
    surf_patch(LI, TL(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .040, pn[1]) if pn[0] is not None else pn)(rhit(a, b)), 0.0, 'TS_Atlas:lamp_housing', step=.05, shrink=.97)
    bezel(LI, TL(sx), rhit, .004, .035, .97, 'TS_Atlas:lamp_housing', step=.05)
    pts_ = along(T, U0 + .03, U1 - .012, .013, +1, 5)
    if len(pts_) >= 2: ribbon(LI, rhit, [(sx * x, z) for x, z in pts_], .007, .016, 'TS_Lights:Tail')
    xb_ = np.linspace(U0 + .10 * WT_, U0 + .72 * WT_, 5); zc_ = [sum(edge_z(T, x)) / 2 for x in xb_]
    LI.grid([[ptat(rhit, sx * x, z + dz, .022) for x, z in zip(xb_, zc_)] for dz in (-.006, .006)], 'TS_Lights:Brake')
    xi_ = np.linspace(U0 + .55 * WT_, U1 - .06, 4); zi_ = [edge_z(T, x)[0] + .013 for x in xi_]
    LI.grid([[ptat(rhit, sx * x, z + dz, .022) for x, z in zip(xi_, zi_)] for dz in (-.005, .005)], IND)
    if globals().get('TAIL_FILL'):                                                                       # v2 truck: combination lamp glows over most of the lens (the thin car LED guide alone read as two red lines at night)
        zt0_, zt1_ = min(p[1] for p in T), max(p[1] for p in T); f0_, f1_ = TAIL_FILL
        LI.grid([[ptat(rhit, sx * x, lerp(zt0_, zt1_, f), .026) for x in np.linspace(U0 + .018, U1 - .018, 4)] for f in (f0_, f1_)], 'TS_Lights:Tail')
    surf_patch(LI, TL(sx), rhit, .004, 'TS_LensRed', step=.032)
    rim_band(TR, TL(sx), rhit, .010, .004, .0058, 'TS_Atlas:gloss_black')
    if LID_X and U0 < LID_X < U1:
        zb, zt = edge_z(T, LID_X); TR.grid([[ptat(rhit, sx * x, z, -.0065) for x in (LID_X - .0035, LID_X + .0035)] for z in np.linspace(zb - .006, zt + .006, 4)], 'TS_Atlas:gloss_black', flip=sx < 0)
    # ---- exhaust finisher, reverse lamp, reflector, side repeater, handle grips, mirror arm + glass
    if EXH:
        rim_band(TR, EXH(sx), rhit, .008, .004, .003, 'TS_Atlas:chrome'); bezel(TR, EXH(sx), rhit, .004, .030, .90, 'TS_Atlas:chrome', step=.04)
        surf_patch(TR, EXH(sx), lambda a, b: (lambda pn: (pn[0] - pn[1] * .060, pn[1]) if pn[0] is not None else pn)(rhit(a, b)), 0.0, 'TS_Atlas:underbody', step=.05)
    (rx0, rx1, rz0, rz1) = REVERSE
    LI.grid([[ptat(rhit, sx * x, z, .004) for x in np.linspace(rx0, rx1, 4)] for z in (rz0, rz1)], 'TS_Lights:Reverse')
    LI.grid([[ptat(rhit, sx * x, z, -.0015) for x in np.linspace(rx0 - .005, rx1 + .005, 4)] for z in (rz0 - .004, rz1 + .004)], 'TS_Lens')
    (fx0, fx1, fz0, fz1) = REFLECTOR
    TR.grid([[ptat(rhit, sx * x, z, -.002) for x in np.linspace(fx0, fx1, 3)] for z in (fz0, fz1)], 'TS_Atlas:reflector_red')
    (py0, py1, pz0, pz1) = REPEATER
    LI.grid([[ptat(lambda y_, z_: shit(sx, y_, z_), y, z, -.002) for y in np.linspace(py0, py1, 3)] for z in (pz0, pz1)], IND)
    for (y0, y1) in HANDLES:
        TR.grid([[ptat(lambda y_, z_: shit(sx, y_, z_), y, z, d) for y in np.linspace(y0 + .01, y1 - .01, 4)] for z, d in ((HANDLE_Z - .010, .002), (HANDLE_Z + .001, -.006), (HANDLE_Z + .010, .002))], 'TS_Atlas:dark_chrome')
    mc = MIRC[sx]; base = shit(sx, mc.y, MIRROR_BASE_Z)[0]
    TR.rbox(((base.x + mc.x - sx * .07) / 2, mc.y, (MIRROR_BASE_Z + .005 + mc.z - .02) / 2), (abs(mc.x - sx * .07 - base.x) / 2 + .012, .030, .020), 'TS_Atlas:plastic_black', .008)
    TR.add([(mc.x - sx * .072, mc.y + .046, mc.z - .043), (mc.x + sx * .072, mc.y + .046, mc.z - .040), (mc.x + sx * .072, mc.y + .046, mc.z + .046), (mc.x - sx * .072, mc.y + .046, mc.z + .038)], [(0, 1, 2, 3) if sx < 0 else (3, 2, 1, 0)], 'TS_Atlas:mirror_glass')
for (y, sx) in ((YF, 1), (YF, -1), (YR, 1), (YR, -1)):
    R_ = RW + .045; zc = RW + .014; seg = 10; a0, a1 = math.radians(-12), math.radians(192)
    arc = [(y + R_ * math.cos(lerp(a0, a1, q / seg)), zc + R_ * math.sin(lerp(a0, a1, q / seg))) for q in range(seg + 1)]
    xi, xo = sx * LINER_XI, sx * (WMAX(y) - .02)
    TR.strip([Vector((xi, yy, zz)) for yy, zz in arc], [Vector((xo, yy, zz)) for yy, zz in arc], 'TS_Atlas:arch_liner', flip=sx > 0)
    TR.cap([Vector((xi, yy, zz)) for yy, zz in arc], 'TS_Atlas:arch_liner', centre=Vector((xi, y, zc - .05)), flip=sx < 0)
# ---- grille: chrome frame, five gloss-black bars with depth, dark mesh back plate deep in shadow; lower intake + bar; front plate; badges; rear light strip
bezel(TR, GRILLE, fhit, .002, .014, .955, GRILLE_FRAME)
surf_patch(TR, GRILLE, lambda a, b: (lambda pn: (pn[0] - pn[1] * .070, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:grille', step=.06)
rim_band(TR, GRILLE, fhit, .016, .004, .004, GRILLE_FRAME)                                                                   # H2: distinct grille surround on the skin
G_ = GRILLE; gx = min(max(p[0] for p in G_ if p[1] < min(q[1] for q in G_) + .03), .6); gz0, gz1 = min(p[1] for p in G_) + .015, max(p[1] for p in G_) - .015
if GRILLE_STYLE == 'vertical':
    for xv in np.linspace(-(gx - .04), gx - .04, GRILLE_BARS): vane(xv, gz0, gz1, .016, .056, .0045, 'TS_Atlas:chrome', 'TS_Atlas:gloss_black')
elif GRILLE_STYLE == 'horizontal':                                                                     # horizontal bars (front face + walls)
    for zv in np.linspace(gz0 + .01, gz1 - .01, GRILLE_BARS):
        hw_ = (edge_z([(z, x) for x, z in G_], zv)[1] or gx) - .03; xs_ = np.linspace(-hw_, hw_, 7)
        F0 = [ptat(fhit, x, zv - .006, .016) for x in xs_]; F1 = [ptat(fhit, x, zv + .006, .016) for x in xs_]; B0 = [ptat(fhit, x, zv - .006, .052) for x in xs_]; B1 = [ptat(fhit, x, zv + .006, .052) for x in xs_]
        if all(p is not None for p in F0 + F1 + B0 + B1): TR.strip(F0, F1, GRILLE_BAR_MAT); TR.strip(F1, B1, 'TS_Atlas:gloss_black'); TR.strip(F0, B0, 'TS_Atlas:gloss_black')
if CHIN_Z: ribbon(TR, fhit, [(x, CHIN_Z) for x in np.linspace(-CHIN_W, CHIN_W, 13)], .016, -.004, 'TS_Atlas:gloss_black')     # lower lip
for (end_, zt_, hw_, ht_, mt_) in globals().get('FACE_TRIMS', []):                                    # v2: horizontal bumper / fascia trim bars on the front ('F') or rear ('R') face
    ribbon(TR, fhit if end_ == 'F' else rhit, [(x, zt_) for x in np.linspace(-hw_, hw_, 17)], ht_, -.005, mt_)
surf_patch(TR, LOWER, lambda a, b: (lambda pn: (pn[0] - pn[1] * .060, pn[1]) if pn[0] is not None else pn)(fhit(a, b)), 0.0, 'TS_Atlas:grille', step=.06)
bezel(TR, LOWER, fhit, .003, .03, .965, 'TS_Atlas:plastic_black')
lz_ = (min(p[1] for p in LOWER) + max(p[1] for p in LOWER)) / 2; lw_ = max(p[0] for p in LOWER) - .07
A = [ptat(fhit, x, lz_, .030) for x in np.linspace(-lw_, lw_, 11)]
if all(p is not None for p in A): TR.strip([p - Vector((0, 0, .006)) for p in A], [p + Vector((0, 0, .006)) for p in A], 'TS_Atlas:gloss_black')
TR.grid([[ptat(fhit, x, z, -.006) for x in np.linspace(-.26, .26, 4)] for z in PLATE_F], 'TS_Atlas:plate')                         # front plate (fictional)
TR.grid([[ptat(fhit, x, z, -.002) for x in np.linspace(-.28, .28, 4)] for z in (PLATE_F[0] - .010, PLATE_F[1] + .010)], 'TS_Atlas:plastic_black')   # plate holder
pz0_, pz1_ = min(p[1] for p in PLATE_R) + .010, max(p[1] for p in PLATE_R) - .010
TR.grid([[ptat(rhit, x, z, .010) for x in np.linspace(-.25, .25, 4)] for z in (pz0_, pz1_)], 'TS_Atlas:plate')                         # rear plate in the recess
rim_band(TR, PLATE_R, rhit, .014, .004, .004, 'TS_Atlas:plastic_black')
if REAR_STRIP: ribbon(TR, rhit, [(x, REAR_STRIP[0]) for x in np.linspace(-REAR_STRIP[1], REAR_STRIP[1], 9)], .010, -.002, 'TS_Atlas:dark_chrome')
vz_ = max(p[1] for p in VALANCE) + .014; vw_ = max(p[0] for p in VALANCE) - .06
ribbon(TR, rhit, [(x, vz_) for x in np.linspace(-vw_, vw_, 13)], .008, -.002, VALANCE_TRIM)                     # satin trim over the valance                               # connecting trim strip across the trunk (unlit)
p, n = fhit(0, BADGE_F); TR.cap([p - n * .012 + Vector((.034 * math.cos(2 * math.pi * k / 12), 0, .026 * math.sin(2 * math.pi * k / 12))) for k in range(12)], 'TS_Atlas:badge', flip=True)
p, n = rhit(0, BADGE_R); TR.cap([p + n * .002 + Vector((.030 * math.cos(2 * math.pi * k / 12), 0, .022 * math.sin(2 * math.pi * k / 12))) for k in range(12)], 'TS_Atlas:badge')
# ---- underbody tray, high-mount brake light integrated in the trunk lip, wipers
TR.grid([[Vector((x, y, TRAY[0])) for x in np.linspace(-TRAY[1], TRAY[1], 3)] for y in np.linspace(TRAY[2], TRAY[3], 4)], 'TS_Atlas:underbody', flip=True)
if HMSL[0] == 'r': LI.grid([[ptat(rhit, x, z, -.001) for x in np.linspace(-HMSL[1], HMSL[1], 4)] for z in (HMSL[2], HMSL[3])], 'TS_Lights:Brake')   # high-mount brake light
else: LI.grid([[thit(x, y)[0] + Vector((0, 0, .004)) for x in np.linspace(-HMSL[1], HMSL[1], 4)] for y in (HMSL[2], HMSL[3])], 'TS_Lights:Brake')
for x0, x1 in (((-.64, -.06), (.02, .58)) if globals().get('WIPERS', True) else ()):           # v2: car wipers (cab-over / bus: omitted at blockout)
    pts = [thit(x, COWL + .05)[0] + Vector((0, 0, .012)) for x in np.linspace(x0, x1, 5)]
    TR.strip([p - Vector((0, .006, 0)) for p in pts], [p + Vector((0, .006, .004)) for p in pts], 'TS_Atlas:wiper'); TR.strip([p + Vector((0, .006, .004)) for p in pts], [p + Vector((0, .006, .016)) for p in pts], 'TS_Atlas:wiper')
for side_, bb_ in (('R', globals().get('BUMPER_R')), ('F', globals().get('BUMPER_F'))):              # v2: separate bumper construction (pickup step bumper, off-road bars)
    if bb_:
        z0_, z1_, hw_, pr_, mt_ = bb_; sg_ = 1 if side_ == 'R' else -1; p_ = (rhit if side_ == 'R' else fhit)(0, (z0_ + z1_) / 2)[0]
        TR.rbox((0, p_.y + sg_ * (pr_ - .03) / 2, (z0_ + z1_) / 2), (hw_, (pr_ + .03) / 2, (z1_ - z0_) / 2), mt_, .012, seg=2)
for end_, poly_, mat_ in globals().get('FACE_GLASS', []):                                          # v2: glass in an END FACE (cab-over / bus windshield, bus rear window)
    hf_ = fhit if end_ == 'F' else rhit; surf_grid(TR, poly_, hf_, .004, mat_); rim_band(TR, poly_, hf_, .016, .002, .003, 'TS_Atlas:rubber')   # structured glass (no fan X)
for sx_, poly_, mat_ in globals().get('SIDE_PANELS', []):                                           # v2: side panels, e.g. bus door glass to the floor (poly in (y, z))
    hs_ = lambda a, b, sx_=sx_: shit(sx_, a, b); surf_patch(TR, poly_, hs_, .004, mat_, step=.05); rim_band(TR, poly_, hs_, .014, .002, .003, 'TS_Atlas:rubber')
for (bx_, by_, bh_, bmt_) in globals().get('ROOF_BOXES', []):                                         # v2: roof equipment (bus HVAC pod) seated on the roof
    p_ = thit(bx_, by_)[0]; TR.rbox((bx_, by_, p_.z + bh_[2] - .01), bh_, bmt_, .04, seg=2)
for (bc_, bh_, bmt_) in globals().get('BOXES', []): TR.rbox(bc_, bh_, bmt_, min(.015, min(bh_) * .5), seg=2)   # v2: free-standing parts (underride bar, side guards, tank, steps)
if globals().get('FRAME'):                                                                            # v2: visible chassis rails (box truck)
    fy0, fy1, fz0, fz1, fx = FRAME
    for sx in (1, -1): TR.rbox((sx * fx, (fy0 + fy1) / 2, (fz0 + fz1) / 2), (.045, (fy1 - fy0) / 2, (fz1 - fz0) / 2), 'TS_Atlas:underbody', .008)
def pbox(g, c, h, t):
    """plain 12-tri box (crisp, cheap): cargo-body rails, subframe, crossmembers, marker lamps."""
    x, y, z = c; hx, hy, hz = h; V = [(x + i * hx, y + j * hy, z + k * hz) for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)]
    g.add(V, [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)], t)
for c_, h_, t_ in globals().get('PLAIN_BOXES', []): pbox(TR, c_, h_, t_)                              # v2: commercial body structure (corner caps, top / bottom rails, subframe, crossmembers, reflectors)
for c_, h_, ch_, d_ in globals().get('MARKER_LAMPS', []):                                            # v2: clearance / identification / side marker lamps: dark housing (trim) + proud emitter on a light channel
    pbox(TR, c_, h_, 'TS_Atlas:lamp_housing'); d_ = Vector(d_); off_ = abs(d_.x) * h_[0] + abs(d_.y) * h_[1] + abs(d_.z) * h_[2]
    pbox(LI, tuple(Vector(c_) + d_ * (off_ + .002)), tuple(hh * (.5 if abs(dd) > .5 else .78) for hh, dd in zip(h_, d_)), ch_)
HITP = {'F': lambda a, b: fhit(a, b), 'R': lambda a, b: rhit(a, b), 'sL': lambda a, b: shit(1, a, b), 'sR': lambda a, b: shit(-1, a, b)}
if globals().get('FACE_WIPERS'):                                                                       # v2: wipers on a flat windshield face (cab-over, bus): blade + arm lying on the glass
    fz_, blades_ = FACE_WIPERS
    for x0_, x1_, z1_ in blades_:
        pts_ = [fhit(lerp(x0_, x1_, t), lerp(fz_, z1_, t))[0] for t in np.linspace(0, 1, 6)]
        if all(p is not None for p in pts_):
            pts_ = [p + Vector((0, -.014, 0)) for p in pts_]; TR.strip([p - Vector((0, 0, .008)) for p in pts_], [p + Vector((0, 0, .008)) for p in pts_], 'TS_Atlas:wiper')
            TR.strip([p + Vector((0, -.006, 0)) for p in pts_], [p + Vector((0, .004, 0)) for p in pts_], 'TS_Atlas:wiper')
for key_, kind_, *a_ in globals().get('FACE_PARTS', []):                                               # v2: parts seated on a face: hinges / latches / handles ('box'), locking bars / poles ('rod')
    hf_ = HITP[key_]
    if kind_ == 'box':
        u_, v_, half_, mt_ = a_; p_, n_ = hf_(u_, v_)
        if p_ is not None: TR.rbox(tuple(p_ + n_ * (half_[1] - .002)), half_ if abs(n_.y) > .5 else (half_[1], half_[0], half_[2]), mt_, min(.006, min(half_) * .5), seg=1)
    elif kind_ == 'rod':
        u_, v0_, v1_, r_, mt_ = a_; p0_, n0_ = hf_(u_, v0_); p1_, n1_ = hf_(u_, v1_)
        if p0_ is not None and p1_ is not None: tube(TR, p0_ + n0_ * (r_ + .012), p1_ + n1_ * (r_ + .012), r_, 8, mt_)
if globals().get('CAB_BACK_GLASS'):                                                                   # v2 pickup: rear window in the cab-back WALL (rays from inside the cab / bed gap)
    cbp_, cby_ = CAB_BACK_GLASS; chit_ = lambda a, b: ray((a, cby_, b), (0, -1, 0))
    surf_patch(TR, cbp_, chit_, .003, 'TS_Glass', step=.04); rim_band(TR, cbp_, chit_, .012, .002, .002, 'TS_Atlas:rubber')
# ---- glass: inset 6 mm with a rubber seal wall, black frit band on the windshield / rear window, B-pillar applique + quarter-light divider
gme = GLASS.data; bmg = bmesh.new(); bmg.from_mesh(gme); bmg.verts.ensure_lookup_table(); bmg.normal_update()
orig = {v.index: v.co.copy() for v in bmg.verts}
for v in bmg.verts: v.co -= v.normal * .006
bnd = [e for e in bmg.edges if e.is_boundary]
for e in bnd:
    a_, b_ = e.verts; TR.add([orig[a_.index], orig[b_.index], b_.co.copy(), a_.co.copy()], [(0, 1, 2, 3)], 'TS_Atlas:rubber')
isl = {}; seen = set()
for f0 in bmg.faces:
    if f0.index in seen: continue
    st = [f0]; comp = []
    while st:
        f = st.pop()
        if f.index in seen: continue
        seen.add(f.index); comp.append(f); st += [g for e in f.edges for g in e.link_faces if g.index not in seen]
    cen = sum((f.calc_center_median() for f in comp), Vector()) / len(comp)
    for f in comp: isl[f.index] = cen
frit_faces = [f for f in bmg.faces if abs(isl[f.index].x) < .30]                                    # windshield + rear window
res_ = bmesh.ops.inset_region(bmg, faces=frit_faces, thickness=.045, depth=0.0, use_even_offset=True, use_boundary=True)
gme.materials.append(M['TS_Atlas']); FRIT_SLOT = len(gme.materials) - 1
for f in res_['faces']: f.material_index = FRIT_SLOT
bmesh.ops.dissolve_limit(bmg, angle_limit=math.radians(3.0), use_dissolve_boundaries=False, edges=[e for e in bmg.edges if len(e.link_faces) == 2], verts=[], delimit={'MATERIAL'})   # window glass is near-planar
bmesh.ops.triangulate(bmg, faces=[f for f in bmg.faces if len(f.verts) > 4])
bmg.to_mesh(gme); bmg.free(); gme.update()
fa = gme.attributes.get('cell') or gme.attributes.new('cell', 'INT', 'FACE'); fa.data.foreach_set('value', [CELLS.index('frit') if p.material_index == FRIT_SLOT else -1 for p in gme.polygons])
for sx in (1, -1):
    sh_ = lambda y, z: shit(sx, y, z)
    for (ya, yb, t) in ([] if PILLARS_FLUSH else [(BPILLAR[0], BPILLAR[1], 'TS_Atlas:gloss_black')] + [(a_, b_, 'TS_Atlas:gloss_black') for a_, b_ in EXTRA_PILLARS]):   # v2: flush pillars are in the skin                                         # B-pillar applique (no quarter divider)
        rows = []
        for z_ in np.linspace(0, 1, 5):
            row = []
            for y in (ya, yb):
                z0 = ZBELT(y) + .04; z1 = lerp(ZBELT(y) + .028, ZC(y) - GH_TOP[0], GH_TOP[1]) - .028; p = ptat(sh_, y, lerp(z0, z1, z_), -.003); row.append(p)
            rows.append(row)
        if all(p is not None for r in rows for p in r): TR.grid(rows, t, flip=sx > 0)
    ys_ = np.linspace(COWL + .12, BELT_Y1, 18)                                                              # satin aluminium belt trim (premium DLO line)
    ribbon(TR, lambda y_, z_: shit(sx, y_, z_), [(y, ZBELT(y) + .016) for y in ys_], .009, -.003, BELT_TRIM)
    if ROCKER: ribbon(TR, lambda y_, z_: shit(sx, y_, z_), [(y, ROCKER[0]) for y in np.linspace(YF + .48, YR - .48, 12)], ROCKER[1], -.002, ROCKER[2])   # rocker trim / cladding
    if ROOF_RAILS:                                                                                     # roof rails: constant-height bar on two (+ mid) feet, ends ramped down
        ry0, ry1, rx_, rh_ = ROOF_RAILS; ysr = np.linspace(ry0, ry1, 12)   # 12 sections: straight box rail (quadratic top line) needs no more (LOD0 budget)
        base_ = [thit(sx * (ROOFW(min(max(y, COWL), ROOF_END)) - rx_), y)[0] for y in ysr]          # follows the roof edge at a fixed inset (a constant x fell off the narrowing roof)
        if all(p is not None for p in base_):
            hgt = [rh_ * (.35 + .65 * ss(0, .10, (y - ry0) / (ry1 - ry0)) * (1 - ss(.90, 1.0, (y - ry0) / (ry1 - ry0)))) for y in ysr]
            raw_ = np.array([p.z + h for p, h in zip(base_, hgt)]); zt_ = np.maximum(np.polyval(np.polyfit(ysr, raw_, 2), ysr), np.array([p.z for p in base_]) + .028)   # rail = straight extrusion (quadratic top line) that always CLEARS the roof (else paint pokes through as dashes)
            top_ = [Vector((p.x, p.y, z)) for p, z in zip(base_, zt_)]
            box_rail(TR, top_, RAIL_W, RAIL_H, RAIL_MAT)
            for i in (1, len(ysr) // 2, len(ysr) - 2): TR.rbox(tuple((base_[i] + top_[i]) / 2 - Vector((0, 0, .004))), (.014, .035, max(.008, (top_[i].z - base_[i].z) / 2)), 'TS_Atlas:plastic_black', 0)   # plain feet (12 tris each)
trim = mk('Trim_Parts', TR.V, TR.F, TR.T, WORK, M); lights = mk('Lights_LOD0', LI.V, LI.F, LI.T, WORK, M)
for o in (trim, lights):
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges); bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bm.to_mesh(o.data); bm.free()   # zero-area slivers from coincident ray hits; v2: + verts orphaned by the dissolve
    clean(o); orient_out(o); o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(35))
REPORT['trim_parts_tris'], REPORT['lights_tris'] = tris(trim), tris(lights)
save_ckp(CKP_ + '_03_parts_lights.blend') if LAST >= 3 else None
if LAST <= 3: sys.exit(0)
# ================================================================ 04 wheels: 205/55 R16 on a 16" 10-spoke alloy (5 double spokes), lug nuts, centre cap, ventilated disc, caliper
WREF = {'FL': Vector((XF, YF, RW)), 'FR': Vector((-XF, YF, RW)), 'RL': Vector((XR, YR, RW)), 'RR': Vector((-XR, YR, RW))}
WSEG = {0: (24, 20), 1: (14, 12), 2: (10, 8), 3: (8, 6)}                                                 # LOD0: round silhouette (24) with a 7-point profile = same triangles as 18 x 9                                                 # (tire, rim) segments per LOD
def build_wheel(c, k, coll_):
    sx = 1 if c[1] == 'L' else -1; hw = WT / 2; st, sr = WSEG[k]; g = Geo(); out = {}
    TW = globals().get('TRUCK_WHEEL')                                                                   # v2 truck: steel disc wheel (mounting face + studs, hand holes, hub cap, drum brake, deep-dished rear duals)
    # tire: bead -> sidewall bulge (max section at 45 % height) -> shoulder radius -> slightly crowned tread (real 55-series profile)
    prof = [(-hw * .80, RIM + .006), (-hw * .96, RIM + .020), (-hw * 1.0, RW - .072), (-hw * .985, RW - .040), (-hw * .90, RW - .012), (-hw * .70, RW - .002), (0, RW),
            (hw * .70, RW - .002), (hw * .90, RW - .012), (hw * .985, RW - .040), (hw * 1.0, RW - .072), (hw * .96, RIM + .020), (hw * .80, RIM + .006)]
    prof = [prof[i] for i in ((0, 2, 3, 4, 6, 8, 9, 10, 12) if k == 1 else (0, 2, 4, 6, 8, 10, 12))]
    Vt, Ft, UVt = revolve(prof, st, sx, a0=-math.pi / 2); n0 = len(g.V); g.add(Vt, Ft, 'TS_Tire'); tire_uv = UVt          # vertex at the contact patch at every LOD
    DUAL = globals().get('DUAL_REAR') if (c[0] == 'R' and k <= 2) else None   # LOD3: inner tire hidden at distance;                                        # v2: dual rear wheels (truck / bus): inner tire + rim on the same pivot
    if DUAL:
        dx_ = -sx * (WT + DUAL); Vt2 = [(v[0] + dx_, v[1], v[2]) for v in Vt]; g.add(Vt2, Ft, 'TS_Tire'); tire_uv = list(UVt) + list(UVt)
        if k <= 2:
            V_, F_, _ = revolve([(hw * .80, RIM + .006), (hw * .55, RIM - .020), (-hw * .80, RIM - .028), (-hw * .80, RIM + .006)], max(8, sr // 2 + 4), sx); g.add([(v[0] + dx_, v[1], v[2]) for v in V_], F_, 'TS_Atlas:wheel_dark')
        xd_ = (hw * .48 - TW['dish_r'] - .008) if TW else (hw * .40 + dx_ * sx)                                 # truck: inner wheel disc back-to-back with the outer one (seen through the hand holes)
        V_, F_, _ = revolve([(xd_, 0.0), (xd_, RIM - .025)], 8, sx); g.add(V_, F_, 'TS_Atlas:wheel_dark')   # inner disc (closes the gap)
    face = hw * .48
    lip = [(hw * .80, RIM + .006), (hw * .86, RIM - .004), (hw * .55, RIM - .020)]
    if k <= 2: V_, F_, _ = revolve(lip, sr, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')                      # machined rim lip
    barrel = [(hw * .55, RIM - .020), (-hw * .80, RIM - .028), (-hw * .80, RIM + .006)]
    if k <= 2: V_, F_, _ = revolve(barrel, max(8, sr // 2 + 4), sx); g.add(V_, F_, 'TS_Atlas:wheel_dark')
    if k <= 2:
        nsp = SPOKES['n'] if k <= 1 else max(5, SPOKES['n'] // 2); DISH = (TW['dish_r'] if c[0] == 'R' else TW['dish_f']) if TW else SPOKES['dish']
        for s_ in range(nsp):                                                                               # curved twin spokes, concave dish, machined (bright) front face, dark painted sides
            a_ = (2 * math.pi * (s_ // 2 * 2 + (s_ % 2) * SPOKES['twin']) / nsp) if (SPOKES['twin'] and nsp == SPOKES['n']) else 2 * math.pi * s_ / nsp
            secs = []
            for t in ((0.0, .5, 1.0) if k == 0 else (0.0, 1.0)):
                r_ = lerp(TW['r_mount'] if TW else .066, RIM - .016, t); w = lerp(SPOKES['w0'], SPOKES['w1'], t) * (1.0 if nsp == SPOKES['n'] else 1.6); xx = face - DISH * (1 - t) ** 1.6 + .006
                Rm = Matrix.Rotation(a_ + SPOKES['curve'] * t * t * (1 if s_ % 2 == 0 else -1), 3, 'X')
                secs.append([Rm @ Vector((sx * xx, -w, r_)), Rm @ Vector((sx * xx, w, r_)), Rm @ Vector((sx * (xx - .026), w * 1.25, r_)), Rm @ Vector((sx * (xx - .026), -w * 1.25, r_))])
            for A, B in zip(secs, secs[1:]):
                for q in range(4):
                    f = [A[q], A[(q + 1) % 4], B[(q + 1) % 4], B[q]]; g.add(f, [(0, 1, 2, 3) if sx > 0 else (3, 2, 1, 0)], 'TS_Atlas:wheel_silver' if q == 0 else 'TS_Atlas:wheel_dark')
        if TW:                                                                                              # truck: flat mounting face, hub cap (front dome / rear axle hub), studs on the bolt circle
            m_ = face - DISH
            V_, F_, _ = revolve([(m_ - .001, TW['r_mount'] + .006), (m_, .072)], 16 if k <= 1 else 8, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')
            hc_ = [(m_, .092), (m_ + .030, .086), (m_ + .060, .062), (m_ + .072, 0.0)] if c[0] == 'F' else [(m_, .086), (m_ + .038, .080), (m_ + .046, 0.0)]
            V_, F_, _ = revolve(hc_, 12 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:dark_chrome' if c[0] == 'F' else 'TS_Atlas:wheel_dark')
            if k == 0:
                R_ = TW['pcd'] / 2; nr_ = TW['nut']
                for s_ in range(TW['studs']):                                                               # wheel nuts (hex, closed end) on the ISO bolt circle
                    a_ = 2 * math.pi * (s_ + .5) / TW['studs']; cy, cz = R_ * math.cos(a_), R_ * math.sin(a_); hx = [(cy + nr_ * math.cos(2 * math.pi * q / 6), cz + nr_ * math.sin(2 * math.pi * q / 6)) for q in range(6)]
                    A = [Vector((sx * (m_ - .002), y, z)) for y, z in hx]; Bv = [Vector((sx * (m_ + .024), y, z)) for y, z in hx]
                    g.strip(A, Bv, 'TS_Atlas:lug', closed=True, flip=sx < 0); g.add(Bv if sx > 0 else Bv[::-1], [tuple(range(6))], 'TS_Atlas:lug')
        else:
            hub = [(face - DISH - .002, .070), (face - DISH + .004, .042), (face - DISH + .008, .030)]
            V_, F_, _ = revolve(hub, 10 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')
            V_, F_, _ = revolve([(face - DISH + .010, .030), (face - DISH + .014, .022), (face - DISH + .015, 0.0)], 10 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:badge')     # centre cap
            if k == 0:
                for s_ in range(5):                                                                             # lug nuts (5 x 114.3 PCD)
                    a_ = 2 * math.pi * (s_ + .5) / 5; cy, cz = .0572 * math.cos(a_), .0572 * math.sin(a_); hx = [(cy + .0095 * math.cos(2 * math.pi * q / 6), cz + .0095 * math.sin(2 * math.pi * q / 6)) for q in range(6)]
                    A = [Vector((sx * (face - DISH - .002), y, z)) for y, z in hx]; Bv = [Vector((sx * (face - DISH + .012), y, z)) for y, z in hx]
                    g.strip(A, Bv, 'TS_Atlas:lug', closed=True, flip=sx < 0)
    else:
        V_, F_, _ = revolve([(face - .03, 0.0), (face - .03, RIM - .02)], 8, sx); g.add(V_, F_, 'TS_Atlas:wheel_silver')   # LOD3: flat face disc
    if k <= 2:                                                                                              # ventilated disc (280 mm) with hat (rotates with the wheel)
        rd = DISC_R
        if TW:                                                                                              # truck: brake drum behind the mounting face (rotates), seen through the hand holes
            m_ = face - DISH; V_, F_, _ = revolve([(m_ - .20, TW['drum_r']), (m_ - .008, TW['drum_r']), (m_ - .008, .09)], 14 if k <= 1 else 8, sx); g.add(V_, F_, 'TS_Atlas:wheel_dark')
        else:
            V_, F_, _ = revolve([(-hw * .25, rd * .61), (-hw * .25, rd), (-hw * .55, rd)], 12 if k <= 1 else 8, sx); g.add(V_, F_, 'TS_Atlas:brake_disc')
            V_, F_, _ = revolve([(face - .030, rd * .52), (-hw * .25, rd * .61)], 10 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:caliper')
    o = mk(f'Wheel_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    uvl = o.data.uv_layers.new(name='tireUV')
    for p in o.data.polygons:
        for li in p.loop_indices:
            vi = o.data.loops[li].vertex_index; uvl.data[li].uv = tire_uv[vi] if vi < len(tire_uv) else (0, 0)
    out['Wheel'] = o
    if k <= 2:                                                                                              # floating caliper (static / steers, does not roll)
        g = Geo()
        if TW:                                                                                              # truck: drum-brake backing plate (static; steers with the front wheel) instead of a car caliper
            V_, F_, _ = revolve([(face - DISH - .215, TW['drum_r'] + .012), (face - DISH - .215, .075)], 12 if k <= 1 else 6, sx); g.add(V_, F_, 'TS_Atlas:caliper')
        else:
            front = c[0] == 'F'; a0, a1 = (math.radians(20), math.radians(70)) if front else (math.radians(110), math.radians(160)); n_ = 6 if k <= 1 else 3
            secs = []
            for q in range(n_ + 1):
                a = lerp(a0, a1, q / n_); ca, sa = math.cos(a) * (1 if front else -1), math.sin(a)
                pts = [(rd - .044, sx * (-hw * .10)), (rd + .018, sx * (-hw * .10)), (rd + .018, -sx * hw * .62), (rd - .044, -sx * hw * .62)]
                secs.append([Vector((xx, rr * ca, rr * sa)) for rr, xx in pts])
            for A, B in zip(secs, secs[1:]): g.strip(A, B, 'TS_Atlas:caliper', closed=True)
            g.add(secs[0], [(0, 1, 2, 3)], 'TS_Atlas:caliper'); g.add(secs[-1], [(3, 2, 1, 0)], 'TS_Atlas:caliper')
        out['Caliper'] = mk(f'Caliper_{c}_LOD{k}', g.V, g.F, g.T, coll_, M)
    for key, o in out.items():
        clean(o); orient_out(o, centre=(0, 0, 0)) if key == 'Caliper' else None
        o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(40 if key != 'Wheel' else 50))
        o.data.transform(Matrix.Translation(WREF[c])); set_origin(o, WREF[c])
    return out
WH = coll('TS_WHEELS'); ASM = {}
for k in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key, o in build_wheel(c, k, WH).items(): ASM[(k, c, key)] = o
save_ckp(CKP_ + '_04_wheels.blend') if LAST >= 4 else None
# ================================================================ 05 interior (visible through the glass): seats + headrests, rear bench, dashboard, cluster, wheel, console, door cards, headliner
IN = Geo(); DRV = INT['drv']; DZ = INT['dz']; XH = INT['half']                                         # seat rows / dash from the design (DZ: H-point height vs sedan)
CR, DK, AL = 'TS_Atlas:fabric_light', 'TS_Atlas:int_plastic', 'TS_Atlas:alu_brushed'
if INT.get('dark'): CR = 'TS_Atlas:fabric_dark'
def seat(x, y, rear=False, w=None):
    w = w or (.23 if not rear else .21); tilt_ = Matrix.Rotation(-.28 if not rear else -.32, 3, 'X')
    IN.rbox((x, y - .02, .405 + DZ), (w - .03, .245, .045), CR, .035)
    for s_ in (-1, 1): IN.rbox((x + s_ * (w - .025), y - .03, .44 + DZ), (.035, .22, .045), CR, .028)
    IN.rbox((x, y + .27, .74 + DZ), (w - (.06 if not rear else .01), .05, .25), CR, .035, tilt_)
    if not rear:
        for s_ in (-1, 1): IN.rbox((x + s_ * (w - .03), y + .265, .72 + DZ), (.045, .07, .26), CR, .03, tilt_)
        IN.rbox((x, y + .36, 1.12 + DZ), (.115, .045, .075), CR, .035, Matrix.Rotation(-.16, 3, 'X'))
        for s_ in (-1, 1): IN.rbox((x + s_ * .065, y + .345, 1.02 + DZ), (.006, .006, .045), AL, 0)
    else: IN.rbox((x, y + .30, 1.07 + DZ), (.11, .045, .07), CR, .03, Matrix.Rotation(-.22, 3, 'X'))
YS = INT['rows']; YD = INT['dash']; ylo, yhi = YD + .10, YS[-1] + .40
for sx in (1, -1):
    seat(sx * DRV, YS[0])
    IN.rbox((sx * XH, (ylo + yhi) / 2, .58 + DZ), (.03, (yhi - ylo) / 2, .25), DK, .01)
    IN.rbox((sx * (XH - .015), (ylo + yhi) / 2, .80 + DZ), (.02, (yhi - ylo) / 2 - .02, .055), CR, .01)
    IN.rbox((sx * (XH - .02), (ylo + yhi) / 2, .755 + DZ), (.010, (yhi - ylo) / 2 - .05, .006), AL, 0)
for yr_ in YS[1:]:
    for xr in INT.get('rear_x', (-.37, .37)): seat(xr, yr_, rear=True)                                  # v2: bus = 2 + 2 with a centre aisle
    if INT.get('bench', True): IN.rbox((0, yr_ - .02, .43 + DZ), (.14, .24, .05), CR, .03); IN.rbox((0, yr_ + .24, .74 + DZ), (.14, .05, .24), CR, .03, Matrix.Rotation(-.32, 3, 'X'))
IN.rbox((0, YD, .87 + DZ), (XH - .05, .16, .065), DK, .04)
IN.rbox((0, YD + .13, .74 + DZ), (XH - .07, .07, .07), CR if INT.get('two_tone', True) else DK, .03)
IN.rbox((0, YD + .175, .815 + DZ), (XH - .07, .006, .010), AL, 0)
for xv in (-.62, -.20, .20, .62): IN.rbox((xv * XH / .84, YD + .145, .835 + DZ), (.06, .006, .014), 'TS_Atlas:gloss_black', .002)
IN.rbox((DRV, YD + .14, .93 + DZ), (.16, .05, .03), DK, .02); IN.rbox((DRV, YD + .185, .905 + DZ), (.14, .004, .038), 'TS_Atlas:screen', .002)
IN.rbox((0, YD + .11, .91 + DZ), (.17, .012, .07), 'TS_Atlas:screen', .006, Matrix.Rotation(.22, 3, 'X'))
IN.rbox((0, (YD + YS[0]) / 2 + .10, .44 + DZ), (.11, max(.2, (YS[0] - YD) / 2), .11), DK, .02); IN.rbox((0, YS[0] + .18, .565 + DZ), (.095, .16, .025), CR, .02)
IN.rbox((0, YS[0] - .44, .58 + DZ), (.035, .045, .028), 'TS_Atlas:leather', .015)
if INT.get('parcel'): IN.rbox((0, INT['parcel'], 1.00 + DZ), (.70, .20, .02), 'TS_Atlas:fabric_dark', 0)
hub = Vector((DRV, YD + .35, .86 + DZ)); tilt = Matrix.Rotation(math.radians(-62), 3, 'X'); seg, sg2 = 12, 4
for q in range(seg):
    a0, a1 = 2 * math.pi * q / seg, 2 * math.pi * (q + 1) / seg
    ring = lambda a: [hub + tilt @ Vector((.185 * math.cos(a) + .016 * math.cos(2 * math.pi * k / sg2) * math.cos(a), .016 * math.sin(2 * math.pi * k / sg2), .185 * math.sin(a) + .016 * math.cos(2 * math.pi * k / sg2) * math.sin(a))) for k in range(sg2)]
    IN.strip(ring(a0), ring(a1), 'TS_Atlas:leather', closed=True)
IN.rbox(tuple(hub + tilt @ Vector((0, .02, 0))), (.06, .03, .05), 'TS_Atlas:leather', .02, tilt)
for a in (0, math.pi, -math.pi / 2): IN.rbox(tuple(hub + tilt @ Vector((.10 * math.cos(a), .01, .10 * math.sin(a)))), (.06 if a != -math.pi / 2 else .014, .01, .014 if a != -math.pi / 2 else .05), 'TS_Atlas:int_plastic', .004, tilt)
interior = mk('Interior_LOD0', IN.V, IN.F, IN.T, WORK, M); clean(interior); interior.data.shade_smooth(); interior.data.set_sharp_from_angle(angle=math.radians(52))   # chamfered seat parts shade round
liner = LO.copy(); liner.data = LO.data.copy(); WORK.objects.link(liner); bm = bmesh.new(); bm.from_mesh(liner.data); bm.normal_update()
LZ_ = globals().get('LINER_ZMIN') or (lambda y: ZBELT(y) + .02); LX_ = globals().get('LINER_X', .95)                  # car: headliner band above the belt; bus: full-height, full-width walls (no bare paint through the glass)
bmesh.ops.delete(bm, geom=[f for f in bm.faces if not (f.calc_center_median().z > LZ_(f.calc_center_median().y) and CAB(f.calc_center_median().y) > .5 and abs(f.calc_center_median().x) < LX_)], context='FACES')
for v in bm.verts: v.co -= v.normal * .018
bmesh.ops.reverse_faces(bm, faces=bm.faces); bm.to_mesh(liner.data); bm.free()
liner.data.materials.clear(); liner.data.materials.append(M['TS_Atlas']); la = liner.data.attributes.get('cell') or liner.data.attributes.new('cell', 'INT', 'FACE'); la.data.foreach_set('value', [CELLS.index('carpet')] * len(liner.data.polygons))   # anthracite headliner / pillar trim (unique cell: dropped at LOD2+)
if globals().get('LINER_DISSOLVE'):                                                                   # bus: planar dissolve keeps every window-opening edge exact (collapse tore the full-width liner into spikes / gaps)
    bm = bmesh.new(); bm.from_mesh(liner.data); bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(LINER_DISSOLVE), use_dissolve_boundaries=False, verts=bm.verts, edges=bm.edges)
    bmesh.ops.triangulate(bm, faces=bm.faces); bm.to_mesh(liner.data); bm.free()
else:
    decim_ = liner.modifiers.new('d', 'DECIMATE'); decim_.ratio = .16; decim_.use_symmetry = True
    with bpy.context.temp_override(object=liner, active_object=liner): bpy.ops.object.modifier_apply(modifier='d')
for l_ in list(liner.data.uv_layers): liner.data.uv_layers.remove(l_)
interior = join([interior, liner], 'Interior_LOD0', WORK); clean(interior)
interior.data.shade_smooth(); interior.data.set_sharp_from_angle(angle=math.radians(52))
if globals().get('LINER_DISSOLVE'): untear(interior)                                                   # bus: dissolved liner n-gon fans tore smooth normals (S1 1.2 %)
REPORT['interior_tris'] = tris(interior)
save_ckp(CKP_ + '_05_interior.blend') if LAST >= 5 else None
# ================================================================ 06 merge, UVs, AO + grime bake (all LOD0 parts in place -> real contact occlusion)
TMAP = {'TMP_clad': 'plastic_dark', 'TMP_seal': 'gloss_black', 'TMP_pocket': 'plastic_black', 'TMP_housing': 'lamp_housing', 'TMP_grille': 'grille', 'TMP_plastic': 'plastic_black', 'TMP_arch': 'arch_liner', 'TMP_plate': 'plastic_black'}
def tmp_to_atlas(o):
    me = o.data; names = [m.name for m in me.materials]; idx = [p.material_index for p in me.polygons]
    a = me.attributes.get('cell') or me.attributes.new('cell', 'INT', 'FACE'); vals = [CELLS.index(TMAP[names[i]]) if names[i] in TMAP else -1 for i in idx]
    me.materials.clear(); me.materials.append(M['TS_Atlas']); me.polygons.foreach_set('material_index', [0] * len(idx)); a.data.foreach_set('value', vals)
tmp_to_atlas(BODYTRIM)
d_ = BODYTRIM.modifiers.new('d', 'DECIMATE'); d_.decimate_type = 'DISSOLVE'; d_.angle_limit = math.radians(4.0); d_.delimit = {'MATERIAL', 'NORMAL'}
with bpy.context.temp_override(object=BODYTRIM, active_object=BODYTRIM): bpy.ops.object.modifier_apply(modifier='d')
bm = bmesh.new(); bm.from_mesh(BODYTRIM.data); bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4]); bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges); bm.to_mesh(BODYTRIM.data); bm.free()   # + no zero-area slivers (plate-recess wall)   # planar cut walls: dissolve flat facets
L0 = coll('LOD0_PARTS')
trim0 = join([BODYTRIM, trim], 'Trim_LOD0', L0)
for g_ in [GLASS]:
    g_.name = g_.data.name = 'Glass_LOD0'; link_only(g_, L0)
LO.name = LO.data.name = 'Body_LOD0'; link_only(LO, L0); link_only(lights, L0); link_only(interior, L0)
for o in (trim0, lights, interior, GLASS): atlas_uvs(o)
for k_ in range(4):
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key in ('Wheel', 'Caliper'):
            o = ASM.get((k_, c, key))
            if o: atlas_uvs(o)
trim0.data.shade_smooth(); trim0.data.set_sharp_from_angle(angle=math.radians(35)); GLASS.data.shade_smooth(); GLASS.data.set_sharp_from_angle(angle=math.radians(45))   # v2: glass folds (hatch glass wrapping the corner) -> split normals, not torn
for o in [x for x in bpy.data.objects if x.type == 'MESH']: purge_slots(o)
if BLOCKOUT:                                                                                           # design blockout: master body (smooth, real openings + gaps) + glass, lamps, trim, LOD0 wheels, interior
    for n_ in [o.name for o in bpy.data.objects if o.type == 'MESH' and (o.name in ('Body_LOD0', 'REF_Skin') or (('_LOD' in o.name) and not o.name.endswith('_LOD0')))]: bpy.data.objects.remove(bpy.data.objects[n_], do_unlink=True)
    HI.hide_render = HI.hide_viewport = False; HI.name = 'Body_Blockout'; link_only(HI, L0)
    bm = bmesh.new(); bm.from_mesh(HI.data); mats = HI.data.materials
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if mats[f.material_index] and mats[f.material_index].name == 'TS_Glass'], context='FACES'); bm.to_mesh(HI.data); bm.free(); purge_slots(HI)
    for m in HI.data.materials:
        if m and m.name.startswith('TMP_'):
            m.use_nodes = True; b_ = m.node_tree.nodes['Principled BSDF']; b_.inputs['Base Color'].default_value = (.015, .015, .016, 1); b_.inputs['Roughness'].default_value = .5
    def _inst(src, name, **kw):
        m = bpy.data.materials[src].copy(); m.name = name; m['instance_of'] = src; nt = m.node_tree
        if 'col' in kw: next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED').inputs['Base Color'].default_value = (*kw['col'], 1)
        if 'ns' in kw:
            for n in nt.nodes:
                if n.type == 'NORMAL_MAP': n.inputs['Strength'].default_value = kw['ns']
        return m
    GLb, INb = _inst('TS_Glass', PRE + '_Glass', col=(.78, .84, .82)), _inst('TS_Atlas', PRE + '_Interior', ns=.12)
    for o in bpy.data.objects:
        if o.type != 'MESH': continue
        for i, m in enumerate(o.data.materials):
            if m and m.name == 'TS_Glass' and o.name.startswith(('Glass', 'Trim')): o.data.materials[i] = GLb
            if m and m.name == 'TS_Atlas' and o.name.startswith('Interior'): o.data.materials[i] = INb
    for o_ in [o for o in bpy.data.objects if o.type == 'MESH']:                                    # v2: final orphan-vertex sweep (geometry joined after the trim cleanup)
        bm_ = bmesh.new(); bm_.from_mesh(o_.data); lv_ = [v for v in bm_.verts if not v.link_faces]
        if lv_: bmesh.ops.delete(bm_, geom=lv_, context='VERTS'); bm_.to_mesh(o_.data); REPORT.setdefault('orphan_verts_removed', {})[o_.name] = len(lv_)
        bm_.free()
    bb = [HI.matrix_world @ Vector(c) for c in HI.bound_box]
    REPORT['blockout'] = dict(master_tris=tris(HI), length=round(max(v.y for v in bb) - min(v.y for v in bb), 3), width_body=round(max(v.x for v in bb) - min(v.x for v in bb), 3),
                              height=round(max(v.z for v in bb), 3), min_z=round(min(v.z for v in bb), 3), lod0_parts_tris={o.name: tris(o) for o in bpy.data.objects if o.type == 'MESH'})
    os.makedirs(OUTD('reports', 'x') and os.path.dirname(OUTD('reports', 'x')), exist_ok=True)
    json.dump(dict(DIM=DIM, wheel_centres=dict(YF=YF, YR=YR, RW=RW), cowl=COWL, dash_to_axle=round(COWL - YF, 3), **REPORT), open(OUTD('reports', PRE + '_blockout_stats' + os.environ.get('TS_BLOCKOUT_TAG', '') + '.json'), 'w'), indent=1)
    p_ = OUTD('blend', CKP_ + '_01_blockout' + os.environ.get('TS_BLOCKOUT_TAG', '') + '.blend'); assert SCR or not os.path.exists(p_)
    bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=p_, copy=True, relative_remap=True); print('SAVED BLOCKOUT', p_, REPORT['blockout'], flush=True); sys.exit(0)
def bake_ao_grime(body, res, path):
    """AO with every LOD0 part in place (wheels, trim, interior occlude) + road-grime mask (low on the body, in cavities). R = AO, G = grime."""
    for o in bpy.data.objects:
        if o.type == 'MESH': o.hide_render = not (o.name in L0.objects or (o.name.endswith('_LOD0') and o.name.startswith(('Wheel', 'Caliper'))))
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 96
    imgs = {}
    for kind in ('AO', 'EMIT'):
        img = bpy.data.images.new(f'bake_{kind}', res, res, alpha=False); img.colorspace_settings.name = 'Non-Color'; imgs[kind] = img
        bm_ = bpy.data.materials.new('BAKE_TMP'); bm_.use_nodes = True; nt = bm_.node_tree; tn = nt.nodes.new('ShaderNodeTexImage'); tn.image = img; nt.nodes.active = tn
        if kind == 'EMIT':
            em = nt.nodes.new('ShaderNodeEmission'); tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); mr = nt.nodes.new('ShaderNodeMapRange')
            mr.inputs['From Min'].default_value = .18; mr.inputs['From Max'].default_value = .62; mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
            nt.links.new(tc.outputs['Object'], sp.inputs[0]); nt.links.new(sp.outputs['Z'], mr.inputs['Value']); nt.links.new(mr.outputs[0], em.inputs['Color'])
            nt.links.new(em.outputs[0], nt.nodes['Material Output'].inputs[0])
        saved = [m for m in body.data.materials]; body.data.materials.clear(); body.data.materials.append(bm_)
        for o in bpy.context.view_layer.objects: o.select_set(o == body)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.bake(type=kind, margin=8, use_clear=True); body.data.materials.clear()
        for m in saved: body.data.materials.append(m)
        bpy.data.materials.remove(bm_)
    ao = np.array(imgs['AO'].pixels[:]).reshape(res, res, 4)[..., 0]; low = np.array(imgs['EMIT'].pixels[:]).reshape(res, res, 4)[..., 0]
    grime = np.clip(.75 * low ** 1.6 + .45 * np.clip(.85 - ao, 0, 1), 0, 1) * .8
    out = np.dstack([ao, grime, np.zeros_like(ao), np.ones_like(ao)])
    im = bpy.data.images.new(os.path.basename(path)[:-4], res, res, alpha=True); im.colorspace_settings.name = 'Non-Color'; im.pixels.foreach_set(out.astype(np.float32).ravel())
    im.filepath_raw = path; im.file_format = 'PNG'; im.save()
    for o in bpy.data.objects:
        if o.type == 'MESH': o.hide_render = False
    HI.hide_render = True; REF.hide_render = True; return path
AOMASK = bake_ao_grime(LO, int(os.environ.get('TS_AO_RES', 1024)), OUTD('textures', f'{PRE}_Body_AO_Grime.png'))
M.update(paint_material(PRE + '_Paint', PAINT_RGB, dict(normal=NORMAL0, aomask=AOMASK), TEX, finish=globals().get('PAINT_FINISH')))
T0_ = {o.name: tris(o) for o in bpy.data.objects if o.type == 'MESH' and o.name.endswith('_LOD0')}; REPORT['lod0_parts'] = T0_; REPORT['lod0_total'] = sum(T0_.values())
print('LOD0', REPORT['lod0_total'], T0_, flush=True)
save_ckp(CKP_ + '_06_materials_uv.blend') if LAST >= 6 else None
# ================================================================ 07 LODs: body re-baked at LOD1 (1024); own normals (sharp 35-40 deg) on every hard-surface part; LOD3 drops the interior detail + lenses
def boxify(o):
    """v2: every connected component -> oriented-to-axes bounding box (12 tris) carrying the component's material, atlas cell and a UV inside that cell."""
    bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table(); uvl = bm.loops.layers.uv.active; cl = bm.faces.layers.int.get('cell'); seen = set(); comps = []
    for f0 in bm.faces:
        if f0.index in seen: continue
        comp = []; st = [f0]
        while st:
            f = st.pop()
            if f.index in seen: continue
            seen.add(f.index); comp.append(f); st += [g for e in f.edges for g in e.link_faces if g.index not in seen]
        vs = {v for f in comp for v in f.verts}; lo = Vector([min(v.co[i] for v in vs) for i in range(3)]); hi = Vector([max(v.co[i] for v in vs) for i in range(3)])
        comps.append((lo, hi, comp[0].material_index, comp[0][cl] if cl else 0, comp[0].loops[0][uvl].uv.copy() if uvl else None))
    bmesh.ops.delete(bm, geom=list(bm.faces), context='FACES'); bmesh.ops.delete(bm, geom=[v for v in bm.verts], context='VERTS')
    for lo, hi, mi, ce, uv in comps:
        vv = [bm.verts.new((hi.x if i & 1 else lo.x, hi.y if i & 2 else lo.y, hi.z if i & 4 else lo.z)) for i in range(8)]
        for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
            f = bm.faces.new([vv[i] for i in q]); f.material_index = mi
            if cl: f[cl] = ce
            if uvl and uv is not None:
                for l in f.loops: l[uvl].uv = uv
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bmesh.ops.triangulate(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free(); o.data.update()
def decim(o, ratio):
    if ratio >= .999: return o
    m = o.modifiers.new('dec', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = ratio; m.use_symmetry = True; m.symmetry_axis = 'X'; m.use_collapse_triangulate = True
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.object.modifier_apply(modifier='dec')
    clean(o); return o
RK = {1: dict(Body=.44, Glass=.8, Trim=.36, Lights=1.0, Interior=.40), 2: dict(Body=.17, Glass=.5, Trim=.13, Lights=.55, Interior=.15), 3: dict(Body=.065, Glass=.25, Trim=.05, Lights=1.0, Interior=.12)}
if os.environ.get('TS_RK'): RK = {int(k): v for k, v in json.loads(os.environ['TS_RK']).items()}
for k_, ov_ in globals().get('LOD_RK', {}).items(): RK[k_].update(ov_)                                   # v2: per-design LOD ratios (commercial vehicles)
for k in (1, 2, 3):
    Lk = coll(f'LOD{k}_PARTS')
    for kind in ('Body', 'Glass', 'Trim', 'Lights', 'Interior'):
        o0 = bpy.data.objects[f'{kind}_LOD0']; d = o0.copy(); d.data = o0.data.copy(); Lk.objects.link(d); d.name = d.data.name = f'{kind}_LOD{k}'
        if kind == 'Lights':                                                                             # deterministic light LODs: drop detail, never emitters
            DROP = {1: {'lamp_inner', 'lamp_housing'}, 2: {'lamp_inner', 'reflector', 'lamp_housing'}, 3: {'lamp_inner', 'reflector', 'lamp_housing', 'LENS'}}[k]
            bm = bmesh.new(); bm.from_mesh(d.data); mats = d.data.materials; cl = bm.faces.layers.int.get('cell')
            def drop(f):
                mn = mats[f.material_index].name
                if mn in ('TS_Lens', 'TS_LensRed'): return 'LENS' in DROP
                return mn == 'TS_Atlas' and 0 <= f[cl] < 100 and CELLS[f[cl]] in DROP
            bmesh.ops.delete(bm, geom=[f for f in bm.faces if drop(f)], context='FACES'); bm.to_mesh(d.data); bm.free(); purge_slots(d)
        if kind == 'Body':                                                                               # mirrors + fin decimated gently (silhouette width / height kept)
            bm = bmesh.new(); bm.from_mesh(d.data); bm.verts.ensure_lookup_table()
            ext = [f for f in bm.faces if (abs(f.calc_center_median().x) > MIRROR_DETECT[0] and f.calc_center_median().z > MIRROR_DETECT[1]) or (abs(f.calc_center_median().x) < .045 and f.calc_center_median().z > ZC(f.calc_center_median().y) - .005 and FIN_YR[0] < f.calc_center_median().y < FIN_YR[1])]
            sub_ = bmesh.ops.split(bm, geom=ext); bm.to_mesh(d.data); bm.free()
            ex = d.copy(); ex.data = d.data.copy(); Lk.objects.link(ex)
            for ob, keep_ext in ((d, False), (ex, True)):
                bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
                isx = lambda f: (abs(f.calc_center_median().x) > MIRROR_DETECT[0] and f.calc_center_median().z > MIRROR_DETECT[1]) or (abs(f.calc_center_median().x) < .045 and f.calc_center_median().z > ZC(f.calc_center_median().y) - .005 and FIN_YR[0] < f.calc_center_median().y < FIN_YR[1])
                bmesh.ops.delete(bm, geom=[f for f in bm.faces if isx(f) != keep_ext], context='FACES'); bm.to_mesh(ob.data); bm.free()
            if globals().get('LOD_BODY_MODE') == 'planar':                                               # v2 (opt-in, boxy commercial bodies): planar dissolve keeps flat panels whole (collapse tore the cargo box)
                bm = bmesh.new(); bm.from_mesh(d.data); bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(globals().get('LOD_PLANAR_DEG', {1: 2.0, 2: 6.0, 3: 12.0})[k]), use_dissolve_boundaries=False, verts=bm.verts, edges=bm.edges, delimit={'MATERIAL', 'SEAM', 'UV'})
                bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4], quad_method='BEAUTY', ngon_method='BEAUTY'); bm.to_mesh(d.data); bm.free()
                if globals().get('LOD_PLANAR_COLLAPSE', {}).get(k): decim(d, LOD_PLANAR_COLLAPSE[k])          # optional gentle collapse after the planar pass (far LOD)
                d.vertex_groups.new(name='keep_extremes')
            else:
                vg_ = d.vertex_groups.new(name='keep_extremes'); ys_ = [v.co.y for v in d.data.vertices]; ymin_, ymax_ = min(ys_), max(ys_)
                vg_.add([v.index for v in d.data.vertices if v.co.y > ymax_ - .006 or v.co.y < ymin_ + .006], 1.0, 'REPLACE')     # bumper crowns define the length: keep them
                m_ = d.modifiers.new('dec', 'DECIMATE'); m_.decimate_type = 'COLLAPSE'; m_.ratio = RK[k][kind]; m_.use_symmetry = True; m_.symmetry_axis = 'X'; m_.use_collapse_triangulate = True
                m_.vertex_group = 'keep_extremes'; m_.invert_vertex_group = True; m_.vertex_group_factor = 1.0
                with bpy.context.temp_override(object=d, active_object=d): bpy.ops.object.modifier_apply(modifier='dec')
            clean(d); d.vertex_groups.remove(d.vertex_groups['keep_extremes']); d = join([d, ex], f'Body_LOD{k}', Lk); clean(d)                              # mirrors + fin kept whole (tiny; exact silhouette)
            uvl_ = d.data.uv_layers.get('UVMap')
            if uvl_:
                for u_ in uvl_.data: u_.uv = (min(max(u_.uv.x, 0.0), 1.0), min(max(u_.uv.y, 0.0), 1.0))          # collapse can push seam UVs a hair outside 0-1
        else:
            if kind == 'Interior' and k >= 2:                                                           # mid / far: seats + dash only (the thin pillar liner spikes under heavy collapse)
                bm = bmesh.new(); bm.from_mesh(d.data); cl = bm.faces.layers.int.get('cell')
                bmesh.ops.delete(bm, geom=[f for f in bm.faces if cl and f[cl] == CELLS.index('carpet')], context='FACES'); bm.to_mesh(d.data); bm.free()
            pl_ = None
            if kind == 'Trim' and k >= 2:                                                               # r3: plate quads kept out of the collapse (it merged half of each plate into the holder)
                pl_ = d.copy(); pl_.data = d.data.copy(); Lk.objects.link(pl_)
                for ob, keep in ((pl_, True), (d, False)):
                    bm = bmesh.new(); bm.from_mesh(ob.data); cl = bm.faces.layers.int.get('cell')
                    bmesh.ops.delete(bm, geom=[f for f in bm.faces if (f[cl] == CELLS.index('plate')) != keep], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
            big_ = None
            if kind == 'Trim' and globals().get('LOD_KEEP_LARGE_TRIM'):                                 # v2 (opt-in, trucks / buses): structural trim (chassis rails, guards, bumpers, posts) kept whole
                bm = bmesh.new(); bm.from_mesh(d.data); bm.faces.ensure_lookup_table(); seen_ = set(); bigf_ = []
                cs_ = [v.co for v in bm.verts]; XE_ = max(abs(c.x) for c in cs_) - .005; Y0E_ = min(c.y for c in cs_) + .005; Y1E_ = max(c.y for c in cs_) - .005; ZE_ = max(c.z for c in cs_) - .005
                for f0 in bm.faces:
                    if f0.index in seen_: continue
                    comp_ = []; st_ = [f0]
                    while st_:
                        f = st_.pop()
                        if f.index in seen_: continue
                        seen_.add(f.index); comp_.append(f); st_ += [g for e in f.edges for g in e.link_faces if g.index not in seen_]
                    vs_ = {v for f in comp_ for v in f.verts}; ext_ = max(max(v.co[i] for v in vs_) - min(v.co[i] for v in vs_) for i in range(3))
                    sz_ = sorted(max(v.co[i] for v in vs_) - min(v.co[i] for v in vs_) for i in range(3))
                    if sz_[2] > LOD_KEEP_LARGE_TRIM and sz_[0] > .02 and len(comp_) <= 120: bigf_ += [f.index for f in comp_]   # bulky solid parts only (not flat ribbons / strips)
                    elif len(comp_) <= 120 and any(abs(v.co.x) > XE_ or v.co.y < Y0E_ or v.co.y > Y1E_ or v.co.z > ZE_ for v in vs_): bigf_ += [f.index for f in comp_]   # silhouette extremes (mirror glass, end lamps) kept: LOD bounds stay within 10 mm
                bm.free(); bigs_ = set(bigf_)
                if bigs_:
                    big_ = d.copy(); big_.data = d.data.copy(); Lk.objects.link(big_); BIGC_ = []
                    for ob, keep in ((big_, True), (d, False)):
                        bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
                        bmesh.ops.delete(bm, geom=[f for f in bm.faces if (f.index in bigs_) != keep], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
                    if k >= 2: boxify(big_)                                                                    # mid / far: each kept part -> its plain bounding box (12 tris), same material / cell / UV
            decim(d, RK[k][kind])
            if big_: d = join([d, big_], f'Trim_LOD{k}', Lk); clean(d)
            if pl_: d = join([d, pl_], f'Trim_LOD{k}', Lk); clean(d)
            if kind == 'Trim' and k >= 2:                                                               # r3: distant plates = clean plate (blue band kept, glyph rows avoided)
                me_ = d.data; cl_ = me_.attributes.get('cell'); uv_ = me_.uv_layers['UVMap'].data; u0, v0, s_ = cell_rect('plate'); npl = 0
                for p_ in me_.polygons:
                    if cl_ and cl_.data[p_.index].value == CELLS.index('plate'):
                        npl += 1
                        for li in p_.loop_indices:
                            u, v = uv_[li].uv; uv_[li].uv = (u, v0 + s_ * (.88 + .06 * min(max((v - v0) / s_, 0.0), 1.0)))
                REPORT.setdefault('distant_plate_faces', {})[k] = npl
        if kind == 'Body':
            d.data.shade_smooth(); d.data.set_sharp_from_angle(angle=math.radians(48))
            if k >= 2 and globals().get('LOD_BODY_MODE') == 'planar': untear(d)                          # far planar LODs (no per-LOD bake): 24 deg dissolve fans tore normals (bus LOD3 S1 1.9 %)
        else:
            with bpy.context.temp_override(object=d, active_object=d): bpy.ops.mesh.customdata_custom_splitnormals_clear()
            d.data.shade_smooth(); d.data.set_sharp_from_angle(angle=math.radians(35 if kind != 'Glass' else 60))
    for c in ('FL', 'FR', 'RL', 'RR'):
        for key in ('Wheel', 'Caliper'):
            o = ASM.get((k, c, key))
            if o: link_only(o, Lk)
NORMAL1 = bake_normal(bpy.data.objects['Body_LOD1'], HI, f'{PRE}_Body_Normal_LOD1', 1024, OUTD('textures', f'{PRE}_Body_Normal_LOD1.png'))
M.update(paint_material(PRE + '_Paint_LOD1', PAINT_RGB, dict(normal=NORMAL1, aomask=AOMASK), TEX, finish=globals().get('PAINT_FINISH')))
M.update(paint_material(PRE + '_Paint_Far', PAINT_RGB, dict(normal=None, aomask=None), TEX, finish=globals().get('PAINT_FINISH')) if False else paint_material(PRE + '_Paint_Far', PAINT_RGB, None, TEX, finish=globals().get('PAINT_FINISH')))
for k, mname in ((1, PRE + '_Paint_LOD1'), (2, PRE + '_Paint_Far'), (3, PRE + '_Paint_Far')):
    me = bpy.data.objects[f'Body_LOD{k}'].data
    for i, m in enumerate(me.materials):
        if m.name == PRE + '_Paint': me.materials[i] = M[mname]
bpy.data.objects.remove(HI, do_unlink=True); bpy.data.objects.remove(REF, do_unlink=True)
def move_atlas(src, dst):
    cp = src.copy(); cp.data = src.data.copy(); dst.users_collection[0].objects.link(cp)
    for ob, keep in ((cp, True), (src, False)):
        bm = bmesh.new(); bm.from_mesh(ob.data); mats = ob.data.materials
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if (mats[f.material_index].name == 'TS_Atlas') != keep], context='FACES'); bm.to_mesh(ob.data); bm.free(); ob.data.update()
    purge_slots(src); purge_slots(cp)
    if not cp.data.polygons: bpy.data.objects.remove(cp, do_unlink=True); return dst
    nm = dst.name; return join([dst, cp], nm, dst.users_collection[0])
for k in range(4):
    for kind in ('Lights', 'Glass'): move_atlas(bpy.data.objects[f'{kind}_LOD{k}'], bpy.data.objects[f'Trim_LOD{k}'])
REPORT['submesh_merge'] = 'TS_Atlas faces of Lights_LODk and Glass_LODk (reflectors, housings, frit) moved into Trim_LODk'
REPORT['lod_ratios'] = RK
save_ckp(CKP_ + '_07_lods.blend') if LAST >= 7 else None
# ================================================================ 08 hierarchy, pivots, colliders, references
FIN = coll(COLL_NAME); COLL = coll('TS_COLLIDERS', FIN)
root = empty('Car_Root', FIN, (0, 0, 0), None, 'PLAIN_AXES', .5)
for k in range(4):
    lr = empty(f'LOD{k}_Root', FIN, (0, 0, 0), root, 'PLAIN_AXES', .3)
    for n in ('Body', 'Glass', 'Trim', 'Lights', 'Interior'):
        o = bpy.data.objects.get(f'{n}_LOD{k}')
        if not o: continue
        link_only(o, FIN); set_origin(o, (0, 0, 0)); mw = o.matrix_world.copy(); o.parent = lr; o.matrix_world = mw
    for c in ('FL', 'FR', 'RL', 'RR'):
        w = ASM[(k, c, 'Wheel')]; cal = ASM.get((k, c, 'Caliper')); parent = lr
        if c in ('FL', 'FR'): parent = empty(f'SteerPivot_{c}_LOD{k}', FIN, WREF[c], lr, 'ARROWS', .15); bpy.context.view_layer.update()
        local = Matrix.Identity(4) if parent is not lr else Matrix.Translation(WREF[c])
        link_only(w, FIN); w.parent = parent; w.matrix_parent_inverse = Matrix.Identity(4); w.matrix_basis = local
        if cal: link_only(cal, FIN); cal.parent = parent; cal.matrix_parent_inverse = Matrix.Identity(4); cal.matrix_basis = local
        bpy.context.view_layer.update()
def hull(name, verts):
    cell = .05
    while True:
        pts = list({(round(v.x / cell), round(v.y / cell), round(v.z / cell)): v for v in verts}.values())
        pts += [max(verts, key=lambda v: v[i] * sg) for i in range(3) for sg in (1, -1)]
        bm = bmesh.new(); vv = [bm.verts.new(v) for v in pts]; bmesh.ops.convex_hull(bm, input=vv)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS'); bmesh.ops.triangulate(bm, faces=bm.faces); bm.normal_update()
        convex = all(all((v.co - f.calc_center_median()).dot(f.normal) <= 5e-4 for v in bm.verts) for f in bm.faces)
        if (len(bm.faces) <= 200 and convex) or cell > 1.5: break                                     # v2: large vehicles (7-12 m) need a coarser snap grid to come out convex
        bm.free(); cell *= 1.3
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); COLL.objects.link(o); o.display_type = 'WIRE'; return o
pts = [bpy.data.objects[f'{n}_LOD2'].matrix_world @ v.co for n in ('Body', 'Glass') for v in bpy.data.objects[f'{n}_LOD2'].data.vertices]
CL = COLLIDERS(pts)
cr = empty('Collision', FIN, (0, 0, 0), root, 'PLAIN_AXES', .2)
for n, vs in CL.items():
    if len(vs) > 8: h = hull(n, vs); h.parent = cr
for c in ('FL', 'FR', 'RL', 'RR'):
    e = empty(f'WheelColliderRef_{c}', FIN, WREF[c], root, 'SPHERE', .1); e['radius_m'] = RW; e['width_m'] = WT
empty('CenterOfMass', FIN, COM, root, 'SPHERE', .08)
for c in list(bpy.data.collections):
    if c.name not in (COLL_NAME, 'TS_COLLIDERS'):
        for o in list(c.objects):
            if o.name not in FIN.all_objects: bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
# r3: revision-specific material INSTANCES (shared library untouched): lighter, realistic side-glass tint; interior with a softer fabric normal
def instance(src, name, **kw):
    m = bpy.data.materials[src].copy(); m.name = name; m['instance_of'] = src; nt = m.node_tree
    if 'col' in kw:
        b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs['Base Color'].default_value = (*kw['col'], 1); m['unity_alpha'] = kw['alpha']
    if 'nstrength' in kw:
        for n in nt.nodes:
            if n.type == 'NORMAL_MAP': n.inputs['Strength'].default_value = kw['nstrength']
    m['unity'] = kw['unity']; return m
GL_ = instance('TS_Glass', PRE + '_Glass', col=(.78, .84, .82), alpha=.22, unity='instance of TS_Glass: Lit transparent, base (0.78, 0.84, 0.82) alpha 0.22, smoothness 1.0 (light green automotive tint, ~75 % visible transmission)')
IN_ = instance('TS_Atlas', PRE + '_Interior', nstrength=.12, unity='instance of TS_Atlas (same textures / UVs): normal scale 0.12 (seat weave reads as fabric, not crumpled at cabin scale)')
for o in FIN.all_objects:
    if o.type != 'MESH': continue
    for i, m in enumerate(o.data.materials):
        if m and m.name == 'TS_Glass' and o.name.startswith(('Glass_', 'Trim_')): o.data.materials[i] = GL_   # v2: glass patches in the trim (face windshield, door glass) use the vehicle glass instance too
        if m and m.name == 'TS_Atlas' and o.name.startswith('Interior_'): o.data.materials[i] = IN_
REPORT['material_instances'] = {GL_.name: dict(GL_.items()), IN_.name: dict(IN_.items())}
json.dump(REPORT, open(OUTD('reports', PRE + '_build_log.json'), 'w'), indent=1)
save_ckp(CKP_ + '_08_rig.blend') if LAST >= 8 else None
