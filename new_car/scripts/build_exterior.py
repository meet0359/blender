# Phase 4: final exterior design + production detailing (body recipe from Phase 3, details in exterior_parts.py).
# Run: Blender -b --factory-startup -P scripts/build_exterior.py
import bpy, bmesh, math, os
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hypercar_03_exterior_final.blend")

# ---------------------------------------------------------------- dimensions
WB = 2.78                       # wheelbase
YF, YR = -WB / 2, WB / 2        # front / rear axle (forward = -Y)
Y0, Y1 = -2.38, 2.25            # body nose / tail
TRACK_X = 0.835                 # wheel center |x|
FRONT = dict(R=0.355, W=0.31, RIM=0.2667, ROTOR=0.200)    # 21"
REAR = dict(R=0.3775, W=0.35, RIM=0.2794, ROTOR=0.195)    # 22"
CLEAR = 0.105                   # ground clearance (floor / splitter)

# ---------------------------------------------------------------- scene
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'
sc.unit_settings.scale_length = 1.0
sc.unit_settings.length_unit = 'METERS'

def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or sc.collection).children.link(c)
    return c

C_CAR = coll("HC_Hypercar")
C_RIG = coll("HC_Rig", C_CAR)
C_BODY = coll("HC_Body", C_CAR)
C_CHASSIS = coll("HC_Chassis", C_CAR)
C_WHEELS = coll("HC_Wheels", C_CAR)
C_CUT = coll("HC_Cutters", C_CAR)
C_STUDIO = coll("HC_Studio")

def mat(name, color, metal=0.0, rough=0.4, coat=0.0, emit=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.08
    m.diffuse_color = (*color, 1)
    return m

# Blockout preview shaders only (real materials are phase 6).
M_CLAY = mat("PRE_Clay_Body", (0.11, 0.115, 0.12), rough=0.28, coat=0.6)
M_GLASS = mat("PRE_Glass_Dark", (0.01, 0.012, 0.015), rough=0.05, coat=1.0)
M_DARK = mat("PRE_Dark_Intake", (0.012, 0.012, 0.013), rough=0.55)
M_CARBON = mat("PRE_Carbon_Dark", (0.025, 0.025, 0.028), rough=0.3, coat=0.5)
M_TIRE = mat("PRE_Tire", (0.022, 0.022, 0.022), rough=0.75)
M_RIM = mat("PRE_Rim_Metal", (0.55, 0.56, 0.58), metal=1.0, rough=0.22)
M_RIM_DARK = mat("PRE_Rim_Barrel", (0.08, 0.08, 0.09), metal=1.0, rough=0.35)
M_ROTOR = mat("PRE_Rotor", (0.18, 0.18, 0.19), metal=0.8, rough=0.45)
M_CALIPER = mat("PRE_Caliper", (0.85, 0.62, 0.02), rough=0.3, coat=0.5)
M_EXH = mat("PRE_Exhaust_Metal", (0.45, 0.42, 0.40), metal=1.0, rough=0.25)
M_FLOOR = mat("PRE_Studio_Floor", (0.17, 0.17, 0.18), rough=0.55)

def new_obj(name, me, col, parent=None):
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    if parent:
        o.parent = parent
    return o

def empty(name, loc, col, parent=None, kind='PLAIN_AXES', size=0.15):
    o = bpy.data.objects.new(name, None)
    o.empty_display_type = kind
    o.empty_display_size = size
    o.location = loc
    col.objects.link(o)
    if parent:
        o.parent = parent
    return o

def bm_to_obj(bm, name, col, mats, parent=None, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    if smooth:
        me.shade_smooth()
    return new_obj(name, me, col, parent)

# ---------------------------------------------------------------- rig
ROOT_OBJ = empty("Car_Root", (0, 0, 0), C_RIG, kind='ARROWS', size=0.6)
WHEELS = {
    "FL": (-TRACK_X, YF, FRONT["R"], FRONT, -1),
    "FR": (TRACK_X, YF, FRONT["R"], FRONT, 1),
    "RL": (-TRACK_X, YR, REAR["R"], REAR, -1),
    "RR": (TRACK_X, YR, REAR["R"], REAR, 1),
}
for k, (x, y, z, _, _) in WHEELS.items():
    empty(f"WheelColliderRef_{k}", (x, y, z), C_RIG, ROOT_OBJ, kind='SPHERE', size=0.08)
empty("CenterOfMass", (0, 0.12, 0.35), C_RIG, ROOT_OBJ, kind='SPHERE', size=0.1)

# ---------------------------------------------------------------- body loft
def pchip(keys):
    xs = [k[0] for k in keys]; ys = [k[1] for k in keys]; n = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    d = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]
    m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, n - 1):
        if d[i - 1] * d[i] > 0:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    def f(x):
        if x <= xs[0]: return ys[0]
        if x >= xs[-1]: return ys[-1]
        i = max(j for j in range(n - 1) if xs[j] <= x)
        t = (x - xs[i]) / h[i]; t2, t3 = t * t, t * t * t
        return ((2*t3 - 3*t2 + 1) * ys[i] + (t3 - 2*t2 + t) * h[i] * m[i]
                + (-2*t3 + 3*t2) * ys[i + 1] + (t3 - t2) * h[i] * m[i + 1])
    return f

# Section key points, each (half-width, height) as a function of y.
# A floor-center, B floor-edge, C sill, D side-mid (side scoop), E shoulder,
# F fender/haunch crown, G valley/beltline, H roof-edge/buttress, I centerline.
K = {
 "zb":  [(Y0, .15), (-2.15, .13), (1.40, .13), (Y1, .36)],
 "wf":  [(Y0, .55), (-2.05, .80), (1.6, .78), (Y1, .68)],
 "ws":  [(Y0, .72), (-2.1, .93), (YF, .955), (YR, .975), (Y1, .95)],
 "zs":  [(Y0, .17), (-2.0, .21), (1.5, .21), (Y1, .21)],
 "wm":  [(Y0, .73), (-2.15, .93), (YF, .975), (-.9, .94), (-.4, .93), (.15, .925), (.55, .87),
         (.95, .92), (YR, 1.01), (1.9, 1.0), (Y1, .975)],
 "zm":  [(Y0, .26), (-2.15, .40), (YF, .46), (YR, .46), (Y1, .52)],
 "wsh": [(Y0, .76), (-2.2, .95), (YF, 1.0), (-.6, .93), (0, .90), (.45, .92), (.95, 1.0),
         (YR, 1.028), (1.9, 1.015), (Y1, .975)],
 "zsh": [(Y0, .30), (-2.15, .52), (YF, .68), (0, .70), (YR, .74), (Y1, .73)],
 "wfc": [(Y0, .70), (-2.2, .85), (YF, .885), (-.6, .845), (0, .835), (.6, .87), (1.25, .905), (Y1, .88)],
 "zfc": [(Y0, .33), (-2.2, .53), (-1.85, .71), (-1.6, .79), (YF, .83), (-.7, .81), (0, .83), (.6, .89),
         (1.25, .985), (1.75, .96), (Y1, .87)],
 "wv":  [(Y0, .55), (-2.2, .62), (YF, .63), (-.75, .655), (-.3, .64), (.3, .625), (.75, .63),
         (1.1, .62), (YR, .62), (Y1, .64)],
 "zv":  [(Y0, .335), (-2.2, .52), (YF, .775), (-.75, .765), (-.3, .84), (.2, .865), (.55, .87),
         (.85, .80), (1.6, .80), (Y1, .82)],
 "wr":  [(Y0, .30), (-2.2, .36), (YF, .40), (-.75, .55), (-.4, .50), (0, .46), (.35, .455),
         (.6, .46), (.85, .40), (YR, .40), (Y1, .42)],
 "zr":  [(Y0, .348), (-2.25, .438), (-2.0, .528), (YF, .673), (-.95, .743), (-.75, .775), (-.4, .95), (0, 1.10), (.3, 1.135),
         (.55, 1.10), (.75, .97), (.95, .91), (YR, .90), (1.9, .87), (Y1, .83)],
 "zt":  [(Y0, .34), (-2.25, .43), (-2.0, .52), (YF, .665), (-.95, .735), (-.75, .77), (-.4, .96), (0, 1.13), (.3, 1.16),
         (.55, 1.125), (.75, 1.0), (.95, .935), (YR, .92), (1.9, .88), (Y1, .83)],
}

def smoothed(f, sigma, step=0.005):
    """Gaussian-smooth a PCHIP curve so curvature is continuous (no highlight kinks at keys).
    Kernel narrows toward nose/tail; odd-reflection padding keeps end slopes."""
    n = int(round((Y1 - Y0) / step)) + 1
    ys = [f(Y0 + i * step) for i in range(n)]
    def at(i):
        if i < 0: return 2 * ys[0] - ys[-i]
        if i >= n: return 2 * ys[-1] - ys[2 * (n - 1) - i]
        return ys[i]
    out = []
    for i in range(n):
        d = min(i, n - 1 - i) * step
        sg = sigma * min(1.0, max(0.12, d / 0.35))
        r = int(3 * sg / step)
        acc = wsum = 0.0
        for j in range(-r, r + 1):
            w = math.exp(-0.5 * (j * step / sg) ** 2); acc += w * at(i + j); wsum += w
        out.append(acc / wsum)
    def g(y):
        t = min(max((y - Y0) / step, 0), n - 1.000001); i = int(t); u = t - i
        return out[i] * (1 - u) + out[i + 1] * u
    return g

SIGMA = {"zb": .12, "wf": .12, "ws": .14, "zs": .12, "wm": .22, "zm": .14, "wsh": .12, "zsh": .14,
         "wfc": .12, "zfc": .10, "wv": .10, "zv": .07, "wr": .07, "zr": .06, "zt": .06}
F = {k: smoothed(pchip(v), SIGMA[k]) for k, v in K.items()}

SEGS = [4, 3, 4, 4, 3, 4, 6, 5]                  # faces per profile segment A-B ... H-I
SEG_START = [sum(SEGS[:i]) for i in range(len(SEGS))]
NP = sum(SEGS) + 1

def section(y):
    g = {k: f(y) for k, f in F.items()}
    return [(0, g["zb"]), (g["wf"], g["zb"]), (g["ws"], g["zs"]), (g["wm"], g["zm"]),
            (g["wsh"], g["zsh"]), (g["wfc"], g["zfc"]), (g["wv"], g["zv"]),
            (g["wr"], g["zr"]), (0, g["zt"])]

def cr(p0, p1, p2, p3, u, alpha=0.5):          # centripetal Catmull-Rom
    def tj(ti, a, b):
        return ti + max(math.dist(a, b), 1e-6) ** alpha
    t0 = 0; t1 = tj(t0, p0, p1); t2 = tj(t1, p1, p2); t3 = tj(t2, p2, p3)
    t = t1 + (t2 - t1) * u
    L = lambda a, b, ta, tb: tuple(((tb - t) * a[i] + (t - ta) * b[i]) / (tb - ta) for i in range(2))
    A1, A2, A3 = L(p0, p1, t0, t1), L(p1, p2, t1, t2), L(p2, p3, t2, t3)
    return L(L(A1, A2, t0, t2), L(A2, A3, t1, t3), t1, t2)

def profile(y):
    P = section(y)
    ext = [(-P[1][0], P[1][1])] + P + [(-P[-2][0], P[-2][1])]   # mirrored phantoms
    out = []
    for s, n in enumerate(SEGS):
        for j in range(n):
            u = j / n
            if s == 0:   # floor stays flat
                out.append((P[0][0] + (P[1][0] - P[0][0]) * u, P[0][1]))
            else:
                out.append(cr(ext[s], ext[s + 1], ext[s + 2], ext[s + 3], u))
    out.append(P[-1])
    return out

NS = 110
def station_y(i):
    s = i / (NS - 1)
    return Y0 + (Y1 - Y0) * (s - 0.6 * math.sin(2 * math.pi * s) / (2 * math.pi))

def body_mat_index(y, seg, k):
    """0 clay, 1 glass. Every glass edge runs along a mesh row (A-pillar = H row) or station,
    so subdivision gives smooth, unstepped DLO outlines."""
    if seg == 7 and (-0.73 < y < -0.03 or 0.82 < y < 1.32):     # windshield / engine glass
        return 1
    if seg == 6 and -0.70 < y < 0.60 and SEG_START[6] < k < SEG_START[7] - 1:   # side DLO
        return 1
    return 0

def smoothstep(a, b, x):
    t = min(max((x - a) / (b - a), 0), 1); return t * t * (3 - 2 * t)

bm = bmesh.new()
rows = []
for i in range(NS):
    y = station_y(i)
    pr = profile(y)
    # subtle double-bubble roof: lift the roof between centerline and roof rail
    wroof = smoothstep(-0.02, 0.15, y) * (1 - smoothstep(0.40, 0.62, y))
    xr = max(pr[-2 - SEGS[7] + 1][0], 0.3)
    pr = [(x, z + (0.007 * math.sin(math.pi * min(x / xr, 1)) ** 2 * wroof if k >= SEG_START[7] else 0))
          for k, (x, z) in enumerate(pr)]
    rows.append([bm.verts.new((x, y, z)) for x, z in pr])
glass = []
for i in range(NS - 1):
    ym = (station_y(i) + station_y(i + 1)) / 2
    for k in range(NP - 1):
        f = bm.faces.new((rows[i][k], rows[i + 1][k], rows[i + 1][k + 1], rows[i][k + 1]))
        seg = max(s for s in range(len(SEGS)) if SEG_START[s] <= k)
        f.material_index = body_mat_index(ym, seg, k)
        if f.material_index == 1:
            glass.append(f)
        elif 0.80 < ym < 1.86 and k in (SEG_START[6] - 1, SEG_START[6]):
            f.material_index = 3
cr_l = bm.edges.layers.float.new("crease_edge")
kE, kF = SEG_START[4], SEG_START[5]
for i in range(NS - 1):
    y = station_y(i)
    bm.edges.get((rows[i][kE], rows[i + 1][kE]))[cr_l] = 0.55       # one dominant shoulder line
    # tensioned blade along the front fender peak, fading out over the door
    bm.edges.get((rows[i][kF], rows[i + 1][kF]))[cr_l] = 0.3 * (1 - smoothstep(-1.2, -0.5, y))
for r in (rows[0], rows[-1]):
    for k in range(NP - 1):
        bm.edges.get((r[k], r[k + 1]))[cr_l] = 0.45
for r in (rows[0], rows[-1]):                    # ladder caps (quads, mirror-safe)
    for k in range(NP // 2 - 1):
        bm.faces.new((r[k], r[k + 1], r[NP - 2 - k], r[NP - 1 - k]))
for v in bm.verts:
    if v.co.y < -1.85:                           # arrow-shaped nose in plan
        v.co.y += 0.22 * v.co.x ** 2 * ((-1.85 - v.co.y) / (-1.85 - Y0)) ** 1.5
    elif v.co.y > 1.9:                           # rounded tail plan
        v.co.y -= 0.16 * v.co.x ** 2 * ((v.co.y - 1.9) / (Y1 - 1.9)) ** 1.5
for v in rows[0]:                                # nose leading edge leans forward over the fascia
    v.co.y += (v.co.z - 0.24) * -0.2
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
# Glass sits inside the body: inset + recess with a dark seal reveal.
ins = bmesh.ops.inset_region(bm, faces=glass, thickness=0.010, depth=-0.006,
                             use_boundary=False, use_even_offset=True)
for f in ins["faces"]:
    f.material_index = 2
body = bm_to_obj(bm, "Body_Shell", C_BODY, [M_CLAY, M_GLASS, M_DARK, M_CARBON], ROOT_OBJ)

mod = body.modifiers.new("Mirror", 'MIRROR')
mod.use_clip = True; mod.use_mirror_merge = True; mod.merge_threshold = 0.001
mod = body.modifiers.new("Subsurf", 'SUBSURF')
mod.levels = 2; mod.render_levels = 2

bpy.context.view_layer.update()
BODY_BVH = BVHTree.FromObject(body, bpy.context.evaluated_depsgraph_get())

def surf_y(x, z, rear=False):
    """Body surface Y at (x, z), hit from the front (or rear)."""
    o, d = ((x, Y1 + 2, z), (0, -1, 0)) if rear else ((x, Y0 - 2, z), (0, 1, 0))
    hit = BODY_BVH.ray_cast(Vector(o), Vector(d))[0]
    assert hit is not None, (x, z, rear)
    return hit.y

# ---------------------------------------------------------------- cutters
def box_bm(bm, lo, hi):
    r = bmesh.ops.create_cube(bm, size=1.0)
    c = [(lo[i] + hi[i]) / 2 for i in range(3)]
    s = [hi[i] - lo[i] for i in range(3)]
    for v in r["verts"]:
        v.co = Vector((c[0] + v.co.x * s[0], c[1] + v.co.y * s[1], c[2] + v.co.z * s[2]))
    return r

def cutter(name, lo, hi, m=M_DARK, bevel=0.02, rot=None):
    bm = bmesh.new()
    box_bm(bm, lo, hi)
    o = bm_to_obj(bm, name, C_CUT, [m], ROOT_OBJ, smooth=False)
    if rot:
        c = Vector([(lo[i] + hi[i]) / 2 for i in range(3)])
        o.data.transform(Matrix.Translation(-c))
        o.matrix_basis = Matrix.Translation(c) @ rot
    if bevel:
        b = o.modifiers.new("Bevel", 'BEVEL'); b.width = bevel; b.segments = 3
    o.display_type = 'WIRE'; o.hide_render = True
    return o

def cyl_bm(bm, r, length, segs=48):
    return bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=length)

def prism(name, yz, x0, x1, m=M_DARK, bevel=0.035):
    """Side-view polygon extruded along X (for raked, swept openings)."""
    bm = bmesh.new()
    a = [bm.verts.new((x0, y, z)) for y, z in yz]
    b = [bm.verts.new((x1, y, z)) for y, z in yz]
    bm.faces.new(a); bm.faces.new(b[::-1])
    n = len(yz)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, name, C_CUT, [m], ROOT_OBJ, smooth=False)
    bv = o.modifiers.new("Bevel", 'BEVEL'); bv.width = bevel; bv.segments = 3
    o.display_type = 'WIRE'; o.hide_render = True
    return o

def prism_y(name, xz, y0, y1, m=M_DARK, bevel=0.025):
    """Front-view polygon extruded along Y (intakes / fascia recesses)."""
    bm = bmesh.new()
    a = [bm.verts.new((x, y0, z)) for x, z in xz]
    b = [bm.verts.new((x, y1, z)) for x, z in xz]
    bm.faces.new(a); bm.faces.new(b[::-1])
    n = len(xz)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, name, C_CUT, [m], ROOT_OBJ, smooth=False)
    bv = o.modifiers.new("Bevel", 'BEVEL'); bv.width = bevel; bv.segments = 3
    o.display_type = 'WIRE'; o.hide_render = True
    return o

def prism_depth(name, xz, depth, rear=False, m=M_DARK, bevel=0.012, out=0.25):
    """Front/rear-view outline cut a constant depth into the surface (per-vertex raycast)."""
    bm = bmesh.new(); sgn = -1 if rear else 1
    ya = [surf_y(x, z, rear) for x, z in xz]
    a = [bm.verts.new((x, y - sgn * out, z)) for (x, z), y in zip(xz, ya)]
    b = [bm.verts.new((x, y + sgn * depth, z)) for (x, z), y in zip(xz, ya)]
    bm.faces.new(a); bm.faces.new(b[::-1])
    n = len(xz)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, name, C_CUT, [m], ROOT_OBJ, smooth=False)
    if bevel:
        bv = o.modifiers.new("Bevel", 'BEVEL'); bv.width = bevel; bv.segments = 2
    o.display_type = 'WIRE'; o.hide_render = True
    return o

def loft_cutter(name, outer, inner, x0, x1, m=M_DARK):
    """Side-view duct: outer outline at x1 tapering to a smaller, rearward inner outline at x0."""
    bm = bmesh.new()
    a = [bm.verts.new((x1, y, z)) for y, z in outer]
    b = [bm.verts.new((x0, y, z)) for y, z in inner]
    bm.faces.new(a); bm.faces.new(b[::-1])
    n = len(outer)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, name, C_CUT, [m], ROOT_OBJ, smooth=False)
    bv = o.modifiers.new("Bevel", 'BEVEL'); bv.width = 0.03; bv.segments = 4
    o.display_type = 'WIRE'; o.hide_render = True
    return o

def groove_z(name, poly, z0, z1, w=0.004):
    """Thin panel-gap ring (plan outline) cut from above: future spoiler / mirror-mount panels."""
    bm = bmesh.new(); n = len(poly)
    cx = sum(p[0] for p in poly) / n; cy = sum(p[1] for p in poly) / n
    def shrink(p, d):
        v = Vector((p[0] - cx, p[1] - cy)); L = v.length
        return (cx + v.x * (L - d) / L, cy + v.y * (L - d) / L)
    rings = [[bm.verts.new((*q, z)) for q in pts] for z in (z0, z1)
             for pts in (poly, [shrink(p, w) for p in poly])]
    o0, i0, o1, i1 = rings
    for j in range(n):
        k = (j + 1) % n
        for f in ((o0[j], o0[k], o1[k], o1[j]), (i0[k], i0[j], i1[j], i1[k]),
                  (o0[k], o0[j], i0[j], i0[k]), (o1[j], o1[k], i1[k], i1[j])):
            bm.faces.new(f)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, name, C_CUT, [M_DARK], ROOT_OBJ, smooth=False)
    o.display_type = 'WIRE'; o.hide_render = True
    return o

ARCH = {"F": (0.050, 0.038, 2.6), "R": (0.075, 0.046, 2.4)}   # extra rx, extra rz, superellipse n
for k, (x, y, z, spec, side) in WHEELS.items():   # squared-off arches (dark wheel-well liner)
    ex, ez, n = ARCH[k[0]]
    rx, rz = spec["R"] + ex, spec["R"] + ez
    bm = bmesh.new()
    prof = []
    for j in range(72):
        t = 2 * math.pi * j / 72; c, s_ = math.cos(t), math.sin(t)
        prof.append((rx * math.copysign(abs(c) ** (2 / n), c), rz * math.copysign(abs(s_) ** (2 / n), s_)))
    a = [bm.verts.new((side * 0.655, y + py, z + pz)) for py, pz in prof]
    b = [bm.verts.new((side * 1.35, y + py, z + pz)) for py, pz in prof]
    bm.faces.new(a); bm.faces.new(b[::-1])
    for j in range(72):
        bm.faces.new((a[j], a[(j + 1) % 72], b[(j + 1) % 72], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, f"Cut_Arch_{k}", C_CUT, [M_DARK], ROOT_OBJ, smooth=False)
    o.display_type = 'WIRE'; o.hide_render = True

# front: trapezoid main intake, raked corner channels, future headlight blade recesses
prism_depth("Cut_FrontIntake_C", [(-0.44, 0.165), (0.44, 0.165), (0.36, 0.30), (-0.36, 0.30)], 0.30, bevel=0.02)
for s, n in ((-1, "L"), (1, "R")):
    side_in = [(s * 0.52, 0.165), (s * 0.84, 0.165), (s * 0.82, 0.35), (s * 0.60, 0.30)]
    prism_depth(f"Cut_FrontIntake_{n}", side_in[::s], 0.35, bevel=0.02)
    # side intake: tapered duct, entry follows the door shutline, throat narrows inward + rearward
    outer = [(0.28, 0.41), (0.47, 0.645), (1.0, 0.685), (1.02, 0.64), (0.96, 0.41)]
    inner = [(0.48, 0.46), (0.60, 0.61), (0.96, 0.64), (0.99, 0.60), (0.96, 0.47)]
    loft_cutter(f"Cut_SideIntake_{n}", outer, inner, s * 0.62, s * 1.3)
    # future mirror mounting pad on the shoulder at the A-pillar base
    groove_z(f"Cut_MirrorPad_{n}", [(s * x, y) for x, y in
             [(0.69, -0.64), (0.84, -0.60), (0.84, -0.44), (0.70, -0.40)]][::s], 0.70, 1.0)

# rear: taillight band, central exhaust cavity (layered over the lower bumper + diffuser)
lo_e = [(0.0, 0.675), (0.55, 0.68), (0.85, 0.70), (0.965, 0.735)]     # slim blade, rising at the corners
hi_e = [(0.955, 0.76), (0.85, 0.735), (0.55, 0.715), (0.0, 0.712)]
band = ([(-x, z) for x, z in reversed(lo_e[1:])] + lo_e + hi_e + [(-x, z) for x, z in reversed(hi_e[:-1])])
prism_depth("Cut_TaillightBand", band, 0.05, rear=True)
prism_depth("Cut_RearCavity", [(-0.44, 0.43), (0.44, 0.43), (0.38, 0.62), (-0.38, 0.62)], 0.28, rear=True,
            bevel=0.02)

mod = body.modifiers.new("Cutters", 'BOOLEAN')
mod.operand_type = 'COLLECTION'; mod.collection = C_CUT
mod.solver = 'EXACT'; mod.material_mode = 'TRANSFER'

# ---------------------------------------------------------------- flying buttresses
def catmull(pts, t):
    n = len(pts) - 1; f = min(t * n, n - 1e-6); i = int(f); u = f - i
    p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n)]
    return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u
                  + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)

BPATH = [Vector(p) for p in ((0.405, 0.30, 1.098), (0.52, 0.85, 1.068), (0.63, 1.30, 1.008),
                             (0.74, 1.65, 0.955), (0.82, 1.93, 0.895))]   # roof -> lands on haunch crown
bm = bmesh.new(); NSEC, NRING = 40, 16
ringsB = []
for i in range(NSEC + 1):
    t = i / NSEC
    p = catmull(BPATH, t); tg = (catmull(BPATH, min(t + 1e-3, 1)) - catmull(BPATH, max(t - 1e-3, 0))).normalized()
    sd = tg.cross(Vector((0, 0, 1))).normalized(); up = sd.cross(tg).normalized()
    bank = Matrix.Rotation(math.radians(-15), 3, tg)       # sail banks outward with the body
    sd, up = bank @ sd, bank @ up
    a = 0.125 - 0.06 * t + 0.035 * smoothstep(0.75, 1.0, t)     # broad root, slim waist, stronger landing
    b = 0.030 + 0.012 * t                                          # thickens toward the trailing landing
    ring = []
    for j in range(NRING):
        th = 2 * math.pi * j / NRING; c, s_ = math.cos(th), math.sin(th)
        ring.append(bm.verts.new(p + sd * a * math.copysign(abs(c) ** 0.5, c) + up * b * math.copysign(abs(s_) ** 0.5, s_)))
    ringsB.append(ring)
for i in range(NSEC):
    for j in range(NRING):
        bm.faces.new((ringsB[i][j], ringsB[i][(j + 1) % NRING], ringsB[i + 1][(j + 1) % NRING], ringsB[i + 1][j]))
for ring, rev in ((ringsB[0], True), (ringsB[-1], False)):   # buried end caps
    c = bm.verts.new(sum((v.co for v in ring), Vector()) / NRING)
    for j in range(NRING):
        f = (ring[j], ring[(j + 1) % NRING], c)
        bm.faces.new(f[::-1] if rev else f)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
o = bm_to_obj(bm, "Body_Buttress", C_BODY, [M_CLAY], ROOT_OBJ)
mm = o.modifiers.new("Mirror", 'MIRROR'); mm.use_mirror_merge = False
o.modifiers.new("Subsurf", 'SUBSURF').levels = 2

bm = bmesh.new(); box_bm(bm, (-0.80, -2.05, CLEAR), (0.80, 1.42, 0.132))
o = bm_to_obj(bm, "Chassis_Floor", C_CHASSIS, [M_CARBON], ROOT_OBJ, smooth=False)

# Engine-bay floor under the rear glass so it doesn't read as a hole.
bm = bmesh.new(); box_bm(bm, (-0.38, 0.80, 0.70), (0.38, 1.36, 0.80))
bm_to_obj(bm, "Chassis_EngineBay", C_CHASSIS, [M_DARK], ROOT_OBJ, smooth=False)

exec(open(os.path.join(ROOT, "scripts", "exterior_parts.py")).read())

# ---------------------------------------------------------------- studio
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=40)
fl = bm_to_obj(bm, "Studio_Floor", C_STUDIO, [M_FLOOR], smooth=False)

w = bpy.data.worlds.new("Studio_World"); sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.32, 0.33, 0.35, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.35

def area(name, loc, size, energy, rot, shape='RECTANGLE', size_y=None, col=None):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.shape = shape
    l.size = size; l.size_y = size_y or size
    o = bpy.data.objects.new(name, l); (col or C_STUDIO).objects.link(o)
    o.location = loc; o.rotation_euler = rot
    return o

area("Light_Top", (0, 0, 6.5), 7, 700, (0, 0, 0), size_y=3.5)
area("Light_StripL", (-5.5, 0, 2.6), 9, 450, (0, math.radians(-65), 0), size_y=0.5)
area("Light_StripR", (5.5, 0, 2.6), 9, 450, (0, math.radians(65), 0), size_y=0.5)
area("Light_Front", (0, -7, 2.5), 4, 250, (math.radians(70), 0, 0), size_y=2)
area("Light_Rear", (0, 7, 2.5), 4, 250, (math.radians(-70), 0, 0), size_y=2)

target = empty("Cam_Target", (0, 0, 0.5), C_STUDIO)
CAMS = {
    "front": ((0, -8.2, 0.75), 70),
    "side": ((13.5, 0, 0.62), 85),
    "rear": ((0, 8.2, 0.85), 70),
    "front_3q": ((-6.0, -6.6, 1.35), 60),
    "rear_3q": ((6.0, 6.4, 1.65), 60),
    "top_3q": ((-5.6, -6.6, 6.2), 50),
    "low_3q": ((-5.4, -5.2, 0.42), 55),
    "top": ((0, 0, 14), 85),
}
for n, (loc, lens) in CAMS.items():
    cd = bpy.data.cameras.new(f"Cam_{n}"); cd.lens = lens
    co = bpy.data.objects.new(f"Cam_{n}", cd); C_STUDIO.objects.link(co)
    co.location = loc
    c = co.constraints.new('TRACK_TO'); c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
sc.camera = bpy.data.objects["Cam_front_3q"]
cam = bpy.data.objects["Cam_top"]; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 5.6
cam.constraints.clear(); cam.rotation_euler = (0, 0, math.radians(90))
CLOSE = {   # close-up review cameras: (location, lens, look-at)
    "headlight": ((-1.45, -3.35, 0.78), 60, (-0.70, -2.22, 0.45)),
    "taillight": ((-1.55, 3.55, 1.02), 60, (-0.55, 2.20, 0.70)),
    "diffuser": ((-1.25, 4.05, 0.38), 42, (0.0, 2.05, 0.27)),
    "side_intake": ((-3.3, -0.25, 0.85), 45, (-0.88, 0.65, 0.55)),
    "wheel": ((-2.55, -2.25, 0.52), 50, (-0.84, -1.39, 0.36)),
    "spoiler": ((-1.7, 3.75, 1.95), 42, (0.0, 2.0, 0.88)),
}
for n, (loc, lens, tgt) in CLOSE.items():
    cd = bpy.data.cameras.new(f"Cam_{n}"); cd.lens = lens
    co = bpy.data.objects.new(f"Cam_{n}", cd); C_STUDIO.objects.link(co)
    co.location = loc
    c = co.constraints.new('TRACK_TO'); c.target = empty(f"CamTarget_{n}", tgt, C_STUDIO)
    c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'

C_QC = coll("HC_QC_Reflection")          # long strip softboxes = reflection cards (QC renders only)
for i, deg in enumerate(range(-80, 81, 20)):      # arc of strips around the car's long axis
    th = math.radians(deg)
    area(f"QC_Strip_{i:02d}", (5.0 * math.sin(th), 0, 0.5 + 5.0 * math.cos(th)), 0.16, 260,
         (0, th, 0), size_y=12, col=C_QC)
for o in C_QC.objects:
    o.hide_render = True


sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.render.use_persistent_data = True
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1600, 900
sc.view_settings.look = 'AgX - Medium High Contrast'

for o in C_CUT.objects:
    o.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
