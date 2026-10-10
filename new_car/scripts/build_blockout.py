# Phase 1+2: scene setup + proportion blockout for the hypercar.
# Run: Blender -b --factory-startup -P scripts/build_blockout.py
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hypercar_01_blockout.blend")

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
 "zb":  [(Y0, .15), (-2.18, .13), (1.55, .13), (1.85, .19), (Y1, .34)],
 "wf":  [(Y0, .55), (-2.08, .80), (2.0, .82), (Y1, .70)],
 "ws":  [(Y0, .70), (-2.13, .93), (YF, .96), (0, .955), (YR, .98), (2.08, .97), (Y1, .88)],
 "zs":  [(Y0, .17), (-2.0, .21), (1.6, .22), (Y1, .42)],
 "wm":  [(Y0, .72), (-2.18, .92), (-1.7, .97), (YF, .975), (-1.0, .96), (-.6, .91), (-.1, .89),
         (.2, .86), (.45, .76), (.75, .80), (1.05, .95), (YR, 1.02), (1.9, 1.0), (Y1, .92)],
 "zm":  [(Y0, .26), (-2.18, .40), (YF, .46), (0, .44), (YR, .47), (Y1, .60)],
 "wsh": [(Y0, .78), (-2.23, .95), (-1.8, .995), (YF, 1.0), (-1.0, .975), (-.5, .92), (0, .90),
         (.4, .93), (.9, 1.0), (YR, 1.03), (1.9, 1.01), (Y1, .96)],
 "zsh": [(Y0, .30), (-2.18, .52), (YF, .67), (-.6, .66), (0, .70), (.6, .74), (YR, .74),
         (2.0, .76), (Y1, .74)],
 "wfc": [(Y0, .68), (-2.23, .82), (YF, .86), (-1.0, .86), (-.6, .84), (0, .84), (.6, .88),
         (1.2, .91), (1.6, .90), (Y1, .86)],
 "zfc": [(Y0, .33), (-2.23, .53), (-1.9, .72), (YF, .82), (-1.0, .80), (-.6, .81), (0, .83),
         (.6, .89), (1.2, .985), (1.6, .975), (2.0, .92), (Y1, .86)],
 "wv":  [(Y0, .55), (-2.18, .62), (YF, .63), (-.75, .655), (-.3, .64), (.2, .62), (.7, .64),
         (YR, .68), (Y1, .68)],
 "zv":  [(Y0, .335), (-2.18, .52), (YF, .775), (-.75, .76), (-.3, .84), (0, .86), (.6, .87),
         (YR, .86), (Y1, .80)],
 "wr":  [(Y0, .30), (-2.18, .36), (YF, .40), (-.75, .55), (-.4, .50), (0, .46), (.3, .45),
         (.6, .48), (1.0, .51), (YR, .52), (Y1, .52)],
 "zr":  [(Y0, .335), (-2.18, .44), (YF, .63), (-.75, .77), (-.4, .95), (0, 1.10), (.3, 1.135),
         (.6, 1.10), (.9, 1.02), (YR, .97), (1.9, .91), (Y1, .84)],
 "zt":  [(Y0, .34), (-2.18, .43), (YF, .60), (-.75, .77), (-.4, .96), (0, 1.13), (.3, 1.16),
         (.6, 1.12), (.9, .99), (YR, .92), (1.9, .86), (Y1, .82)],
}
F = {k: pchip(v) for k, v in K.items()}

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
    """0 clay, 1 glass. Windshield / side DLO / engine-cover glass between buttresses."""
    if seg == 7 and (-0.72 < y < -0.04 or 0.78 < y < 1.30):
        return 1
    if seg == 6 and -0.48 < y < 0.60 and SEG_START[6] < k < SEG_START[6] + SEGS[6] - 1:
        return 1
    return 0

bm = bmesh.new()
rows = []
for i in range(NS):
    y = station_y(i)
    rows.append([bm.verts.new((x, y, z)) for x, z in profile(y)])
for i in range(NS - 1):
    ym = (station_y(i) + station_y(i + 1)) / 2
    for k in range(NP - 1):
        f = bm.faces.new((rows[i][k], rows[i + 1][k], rows[i + 1][k + 1], rows[i][k + 1]))
        seg = max(s for s in range(len(SEGS)) if SEG_START[s] <= k)
        f.material_index = body_mat_index(ym, seg, k)
cr_l = bm.edges.layers.float.new("crease_edge")
kE = SEG_START[4]
for i in range(NS - 1):
    bm.edges.get((rows[i][kE], rows[i + 1][kE]))[cr_l] = 0.6
for r in (rows[0], rows[-1]):
    for k in range(NP - 1):
        bm.edges.get((r[k], r[k + 1]))[cr_l] = 0.45
for r in (rows[0], rows[-1]):                    # ladder caps (quads, mirror-safe)
    for k in range(NP // 2 - 1):
        bm.faces.new((r[k], r[k + 1], r[NP - 2 - k], r[NP - 1 - k]))
for v in bm.verts:
    if v.co.y < -1.85:
        v.co.y += 0.22 * v.co.x ** 2 * ((-1.85 - v.co.y) / (-1.85 - Y0)) ** 1.5
    elif v.co.y > 1.9:
        v.co.y -= 0.16 * v.co.x ** 2 * ((v.co.y - 1.9) / (Y1 - 1.9)) ** 1.5
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
body = bm_to_obj(bm, "Body_Shell", C_BODY, [M_CLAY, M_GLASS], ROOT_OBJ)

mod = body.modifiers.new("Mirror", 'MIRROR')
mod.use_clip = True; mod.use_mirror_merge = True; mod.merge_threshold = 0.001
mod = body.modifiers.new("Subsurf", 'SUBSURF')
mod.levels = 2; mod.render_levels = 2
mod = body.modifiers.new("Cutters", 'BOOLEAN')
mod.operand_type = 'COLLECTION'; mod.collection = C_CUT
mod.solver = 'EXACT'; mod.material_mode = 'TRANSFER'

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

for k, (x, y, z, spec, side) in WHEELS.items():   # wheel arches (dark wheel-well liner)
    bm = bmesh.new()
    cyl_bm(bm, spec["R"] + 0.045, 0.7, 64)
    bm.transform(Matrix.Rotation(math.pi / 2, 4, 'Y'))
    o = bm_to_obj(bm, f"Cut_Arch_{k}", C_CUT, [M_DARK], ROOT_OBJ, smooth=False)
    o.location = (side * (0.655 + 0.35), y, z)
    o.display_type = 'WIRE'; o.hide_render = True

prism_y("Cut_FrontIntake_C", [(-0.44, 0.165), (0.44, 0.165), (0.36, 0.30), (-0.36, 0.30)], Y0 - 0.2, Y0 + 0.17)
for s, n in ((-1, "L"), (1, "R")):
    prism_y(f"Cut_FrontIntake_{n}", [(s * 0.52, 0.165), (s * 0.86, 0.165), (s * 0.84, 0.36), (s * 0.60, 0.31)][::s],
            Y0 - 0.2, Y0 + 0.30)
    prism(f"Cut_SideIntake_{n}", [(0.30, 0.40), (0.50, 0.67), (1.02, 0.71), (0.98, 0.40)],
          s * 0.66, s * 1.3)
prism_y("Cut_RearFascia", [(-0.80, 0.37), (0.80, 0.37), (0.74, 0.63), (-0.74, 0.63)], Y1 - 0.30, Y1 + 0.2)

# ---------------------------------------------------------------- chassis / aero volumes
bm = bmesh.new(); box_bm(bm, (-0.80, -2.05, CLEAR), (0.80, 1.56, 0.132))
o = bm_to_obj(bm, "Chassis_Floor", C_CHASSIS, [M_CARBON], ROOT_OBJ, smooth=False)

bm = bmesh.new(); box_bm(bm, (-0.86, Y0 - 0.05, CLEAR), (0.86, -2.05, 0.128))
o = bm_to_obj(bm, "Aero_Splitter", C_CHASSIS, [M_CARBON], ROOT_OBJ, smooth=False)
b = o.modifiers.new("Bevel", 'BEVEL'); b.width = 0.08; b.segments = 6
b.limit_method = 'ANGLE'; b.angle_limit = math.radians(60)

# Diffuser: ramp that follows the body underside + 5 fins + side strakes.
bm = bmesh.new()
ys = [1.55 + (Y1 - 1.55) * t / 12 for t in range(13)]
HW = 0.66
vs = [(bm.verts.new((-HW, y, F["zb"](y) - 0.012)), bm.verts.new((HW, y, F["zb"](y) - 0.012))) for y in ys]
for a, b2 in zip(vs, vs[1:]):
    bm.faces.new((a[0], a[1], b2[1], b2[0]))
for fx in (-0.62, -0.40, -0.20, 0.0, 0.20, 0.40, 0.62):
    t = 0.012 if abs(fx) < 0.6 else 0.02
    base = [(y, F["zb"](y) - 0.012) for y in ys]
    low = [(y, min(F["zb"](y) - 0.012, 0.135 + (y - 1.55) * 0.03)) for y in ys]
    top = [bm.verts.new((fx - t, y, z)) for y, z in base] + [bm.verts.new((fx + t, y, z)) for y, z in base]
    bot = [bm.verts.new((fx - t, y, z)) for y, z in low] + [bm.verts.new((fx + t, y, z)) for y, z in low]
    n = len(ys)
    for side in (0, n):
        for j in range(n - 1):
            bm.faces.new((top[side + j], top[side + j + 1], bot[side + j + 1], bot[side + j]))
    for j in range(n - 1):
        bm.faces.new((bot[j], bot[j + 1], bot[n + j + 1], bot[n + j]))
    bm.faces.new((top[n - 1], top[2 * n - 1], bot[2 * n - 1], bot[n - 1]))
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
o = bm_to_obj(bm, "Aero_Diffuser", C_CHASSIS, [M_CARBON], ROOT_OBJ, smooth=False)
o.modifiers.new("Solidify", 'SOLIDIFY').thickness = 0.008

# Exhaust placeholders: central high-mounted twin, sitting in the rear fascia recess.
bm = bmesh.new()
for ex in (-0.13, 0.13):
    r = bmesh.ops.create_cone(bm, cap_ends=False, segments=32, radius1=0.058, radius2=0.058, depth=0.26)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((ex, Y1 - 0.20, 0.52)) @ Matrix.Rotation(math.pi / 2, 4, 'X'),
                        verts=r["verts"])
o = bm_to_obj(bm, "Exhaust_Blockout", C_CHASSIS, [M_EXH], ROOT_OBJ)
o.modifiers.new("Solidify", 'SOLIDIFY').thickness = 0.006

# Engine-bay floor under the rear glass so it doesn't read as a hole.
bm = bmesh.new(); box_bm(bm, (-0.5, 0.75, 0.70), (0.5, 1.35, 0.74))
bm_to_obj(bm, "Chassis_EngineBay", C_CHASSIS, [M_DARK], ROOT_OBJ, smooth=False)

# ---------------------------------------------------------------- wheels
def lathe(bm, prof, segs, closed):
    rings = []
    for a in range(segs):
        th = 2 * math.pi * a / segs
        rings.append([bm.verts.new((x, r * math.cos(th), r * math.sin(th))) for x, r in prof])
    n = len(prof)
    for a in range(segs):
        r0, r1 = rings[a], rings[(a + 1) % segs]
        for j in range(n if closed else n - 1):
            j1 = (j + 1) % n
            bm.faces.new((r0[j], r1[j], r1[j1], r0[j1]))

def box_between(bm, p0, p1, w, t):
    d = (p1 - p0).normalized()
    ax = Vector((1, 0, 0))
    side = d.cross(ax).normalized() * (w / 2)
    up = ax * (t / 2)
    vs = [bm.verts.new(p + sv + uv) for p in (p0, p1) for sv in (-side, side) for uv in (-up, up)]
    for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
        bm.faces.new([vs[i] for i in f])

for k, (x, y, z, sp, s) in WHEELS.items():
    R, hw, rr = sp["R"], sp["W"] / 2, sp["RIM"]
    loc = Vector((x, y, z))
    # tire: closed, rounded-shoulder low-profile section
    prof = [(-hw * .86, rr + .004), (-hw, rr + .03), (-hw, R - .04), (-hw + .012, R - .012),
            (-hw + .045, R), (hw - .045, R), (hw - .012, R - .012), (hw, R - .04),
            (hw, rr + .03), (hw * .86, rr + .004)]
    bm = bmesh.new(); lathe(bm, prof, 96, True)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    t = bm_to_obj(bm, f"Tire_{k}", C_WHEELS, [M_TIRE], ROOT_OBJ)
    t.location = loc
    t.modifiers.new("Subsurf", 'SUBSURF').levels = 1

    # rim: barrel + machined lip (outboard = s), 5 double spokes, center-lock hub
    xf = s * hw * 0.92
    bm = bmesh.new()
    prof = [(s * -hw * .86, rr + .012), (s * -hw * .86, rr - .012), (s * hw * .70, rr - .012),
            (s * hw * .80, rr - .03), (s * hw * .92, rr - .022), (s * hw * .95, rr + .012),
            (s * hw * .86, rr + .016)]
    lathe(bm, prof, 96, False)
    for i in range(5):
        base = 2 * math.pi * i / 5
        for sgn in (-1, 1):
            a0, a1 = base + sgn * math.radians(4), base + sgn * math.radians(10)
            p0 = Vector((xf - s * 0.075, 0.085 * math.cos(a0), 0.085 * math.sin(a0)))
            p1 = Vector((xf - s * 0.012, (rr - .022) * math.cos(a1), (rr - .022) * math.sin(a1)))
            box_between(bm, p0, p1, 0.024, 0.032)
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=0.095, radius2=0.075, depth=0.05)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((xf - s * 0.075, 0, 0)) @ Matrix.Rotation(s * math.pi / 2, 4, 'Y'), verts=r["verts"])
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.05, radius2=0.042, depth=0.04)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((xf - s * 0.04, 0, 0)) @ Matrix.Rotation(s * math.pi / 2, 4, 'Y'), verts=r["verts"])
    o = bm_to_obj(bm, f"Rim_{k}", C_WHEELS, [M_RIM], ROOT_OBJ)
    o.location = loc

    # carbon-ceramic rotor placeholder + caliper block (calipers trail the axle: +Y)
    bm = bmesh.new()
    r = bmesh.ops.create_cone(bm, cap_ends=True, segments=64, radius1=sp["ROTOR"], radius2=sp["ROTOR"], depth=0.034)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((s * -0.01, 0, 0)) @ Matrix.Rotation(math.pi / 2, 4, 'Y'), verts=r["verts"])
    o = bm_to_obj(bm, f"BrakeDisc_{k}", C_WHEELS, [M_ROTOR], ROOT_OBJ)
    o.location = loc
    bm = bmesh.new()
    box_bm(bm, (-0.06 if s > 0 else -0.045, -0.10, sp["ROTOR"] - 0.055),
           (0.045 if s > 0 else 0.06, 0.10, sp["ROTOR"] + 0.04))
    bm.transform(Matrix.Rotation(math.radians(-70), 4, 'X'))
    o = bm_to_obj(bm, f"Caliper_{k}", C_WHEELS, [M_CALIPER], ROOT_OBJ, smooth=False)
    o.location = loc
    b = o.modifiers.new("Bevel", 'BEVEL'); b.width = 0.015; b.segments = 2

# ---------------------------------------------------------------- studio
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=40)
fl = bm_to_obj(bm, "Studio_Floor", C_STUDIO, [M_FLOOR], smooth=False)

w = bpy.data.worlds.new("Studio_World"); sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.32, 0.33, 0.35, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.35

def area(name, loc, size, energy, rot, shape='RECTANGLE', size_y=None):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.shape = shape
    l.size = size; l.size_y = size_y or size
    o = bpy.data.objects.new(name, l); C_STUDIO.objects.link(o)
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
}
for n, (loc, lens) in CAMS.items():
    cd = bpy.data.cameras.new(f"Cam_{n}"); cd.lens = lens
    co = bpy.data.objects.new(f"Cam_{n}", cd); C_STUDIO.objects.link(co)
    co.location = loc
    c = co.constraints.new('TRACK_TO'); c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
sc.camera = bpy.data.objects["Cam_front_3q"]

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
