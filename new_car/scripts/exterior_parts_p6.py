# Phase 5 exterior parts (Phase 4 parts + cleanup: lens clearance, softened rear vents, forged spokes). Exec'd from build_exterior.py after the body exists:
# shares its globals (F, BODY_BVH, cutters collection, materials, catmull, smoothstep, lo_e/hi_e, ARCH, WHEELS ...).

# ---------------------------------------------------------------- preview materials (final materials = phase 6)
def emit_mat(name, color, strength):
    m = mat(name, color, rough=0.3)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = (*color, 1)
    b.inputs["Emission Strength"].default_value = strength
    return m

def glass_mat(name, color, rough):
    m = mat(name, color, rough=rough)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = 1.5
    return m

M_LED_W = emit_mat("PRE_LED_DRL_White", (1.0, 0.97, 0.92), 8.0)
M_LED_R = emit_mat("PRE_LED_Tail_Red", (1.0, 0.02, 0.01), 6.0)
M_LED_BRAKE = emit_mat("PRE_LED_Brake_Red", (0.9, 0.01, 0.01), 1.5)
M_LED_AMB = emit_mat("PRE_LED_Indicator_Amber", (1.0, 0.35, 0.0), 1.0)
M_LED_REV = emit_mat("PRE_LED_Reverse_White", (1.0, 1.0, 1.0), 0.3)
M_LENS = glass_mat("PRE_Lens_Clear", (1.0, 1.0, 1.0), 0.0)
M_LENS_SMOKE = glass_mat("PRE_Lens_Smoked", (0.25, 0.20, 0.20), 0.02)
M_BEZEL = mat("PRE_Bezel_Metal", (0.80, 0.80, 0.82), metal=1.0, rough=0.12)
M_HOUSING = mat("PRE_Light_Housing", (0.015, 0.015, 0.017), rough=0.35)
M_MIRROR = mat("PRE_Mirror_Glass", (0.9, 0.9, 0.9), metal=1.0, rough=0.02)
M_RIM_FACE = mat("PRE_Rim_Forged_Graphite", (0.10, 0.10, 0.11), metal=1.0, rough=0.28)
M_RIM_LIP = mat("PRE_Rim_Machined_Lip", (0.75, 0.76, 0.78), metal=1.0, rough=0.15)
M_EXH_IN = mat("PRE_Exhaust_Inner_Dark", (0.03, 0.028, 0.026), metal=0.6, rough=0.5)
M_PROJ = mat("PRE_Projector_Lens", (0.02, 0.022, 0.03), rough=0.02, coat=1.0)
M_HAT = mat("PRE_Brake_Hat", (0.25, 0.25, 0.27), metal=1.0, rough=0.3)

# ---------------------------------------------------------------- surface projection helpers
def _hit(o, d):
    return BODY_BVH.ray_cast(Vector(o), Vector(d))[0]

def surf_x(y, z, s):
    h = _hit((s * 3, y, z), (-s, 0, 0)); return h.x if h else None

def surf_z(x, y):
    h = _hit((x, y, 3), (0, 0, -1)); return h.z if h else None

AX = {'x': 0, 'y': 1, 'z': 2}

def _to3(axis, uv, w):
    a, b = uv
    return Vector((w, a, b)) if axis == 'x' else Vector((a, w, b)) if axis == 'y' else Vector((a, b, w))

def project(axis, pts, s=0):
    """Project 2D points onto the body along an axis -> [(surface point, inward dir)].
    axis 'x': (y,z) seen from side s; 'y': (x,z) from front (s=-1) / rear (s=+1); 'z': (x,y) from above."""
    if axis == 'x':
        o = lambda uv: (s * 3, *uv); d = Vector((-s, 0, 0))
    elif axis == 'y':
        o = lambda uv: (uv[0], (Y1 + 2) if s > 0 else (Y0 - 2), uv[1]); d = Vector((0, -s, 0))
    else:
        o = lambda uv: (*uv, 3); d = Vector((0, 0, -1))
    hits = [_hit(o(uv), d) for uv in pts]
    good = [i for i, h in enumerate(hits) if h is not None]
    assert good, ("no surface hits", pts[:2])
    out = []
    for i, uv in enumerate(pts):
        h = hits[i] if hits[i] is not None else hits[min(good, key=lambda g: abs(g - i))]
        out.append((_to3(axis, uv, h[AX[axis]]), d))
    return out

def densify(poly, step=0.015, closed=True):
    out = []; n = len(poly)
    for i in range(n if closed else n - 1):
        a, b = Vector(poly[i]), Vector(poly[(i + 1) % n])
        k = max(1, int((b - a).length / step))
        out += [tuple(a + (b - a) * j / k) for j in range(k)]
    if not closed:
        out.append(tuple(poly[-1]))
    return out

def offset_poly(poly, d):
    """Inward miter offset of a closed 2D polygon."""
    n = len(poly)
    area = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    sg = 1 if area > 0 else -1
    def nrm(a, b):
        e = (Vector(b) - Vector(a)).normalized(); return Vector((-e.y, e.x)) * sg
    out = []
    for i in range(n):
        n1, n2 = nrm(poly[i - 1], poly[i]), nrm(poly[i], poly[(i + 1) % n])
        m = (n1 + n2).normalized()
        out.append(tuple(Vector(poly[i]) + m * d / max(m.dot(n1), 0.3)))
    return out

def line_poly(pts, w):
    """Closed thin polygon around an open 2D polyline (for panel-gap lines)."""
    pts = [Vector(p) for p in pts]; L, Rr = [], []
    for i, p in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        e = (b - a).normalized(); nn = Vector((-e.y, e.x)) * (w / 2)
        L.append(tuple(p + nn)); Rr.append(tuple(p - nn))
    return L + Rr[::-1]

def _hide_cutter(o, bevel):
    if bevel:
        b = o.modifiers.new("Bevel", 'BEVEL'); b.width = bevel; b.segments = 2
    o.display_type = 'WIRE'; o.hide_render = True
    return o

def surf_cutter(name, poly, axis, s, depth, out=0.06, ring=None, m=M_DARK, bevel=0.0, step=0.015):
    """Boolean cutter that follows the body: outline projected on the surface, cut `depth` inward.
    ring=w makes a thin panel-gap groove of width w along the outline instead of a pocket."""
    pts = densify(poly, step)
    bm = bmesh.new()
    def layer(pp, off):
        return [bm.verts.new(p + d * off) for p, d in project(axis, pp, s)]
    n = len(pts)
    if ring:
        inner = offset_poly(pts, ring)
        Ao, Ai, Bo, Bi = layer(pts, -out), layer(inner, -out), layer(pts, depth), layer(inner, depth)
        for j in range(n):
            k = (j + 1) % n
            for f in ((Ao[j], Ao[k], Bo[k], Bo[j]), (Ai[k], Ai[j], Bi[j], Bi[k]),
                      (Ao[k], Ao[j], Ai[j], Ai[k]), (Bo[j], Bo[k], Bi[k], Bi[j])):
                bm.faces.new(f)
    else:
        A, B = layer(pts, -out), layer(pts, depth)
        bm.faces.new(A); bm.faces.new(B[::-1])
        for j in range(n):
            k = (j + 1) % n; bm.faces.new((A[j], A[k], B[k], B[j]))
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _hide_cutter(bm_to_obj(bm, name, C_CUT, [m], ROOT_OBJ, smooth=False), bevel)

def groove(name, pts, axis, s=0, closed=False, w=0.0035, depth=0.010, out=0.04):
    """3-5 mm panel gap. Both walls hang off ONE projected centreline point, so the thin cutter can't
    self-intersect on steep/curved surfaces (independent wall projection caused non-manifold booleans)."""
    c2 = [Vector(p) for p in densify(pts, 0.012, closed=closed)]
    n = len(c2)
    hits = project(axis, [tuple(p) for p in c2], s)
    to3 = {'x': lambda v: Vector((0, v.x, v.y)), 'y': lambda v: Vector((v.x, 0, v.y)), 'z': lambda v: Vector((v.x, v.y, 0))}[axis]
    bm = bmesh.new(); rings = []
    for i, (p, d) in enumerate(hits):
        a_, b_ = (c2[i - 1] if (closed or i) else c2[i]), (c2[(i + 1) % n] if (closed or i < n - 1) else c2[i])
        e = (b_ - a_).normalized(); nv = to3(Vector((-e.y, e.x))).normalized() * (w / 2)
        rings.append([bm.verts.new(q) for q in (p + nv - d * out, p - nv - d * out, p - nv + d * depth, p + nv + d * depth)])
    for i in range(n if closed else n - 1):
        r0, r1 = rings[i], rings[(i + 1) % n]
        for j in range(4):
            bm.faces.new((r0[j], r0[(j + 1) % 4], r1[(j + 1) % 4], r1[j]))
    if not closed:
        bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _hide_cutter(bm_to_obj(bm, name, C_CUT, [M_DARK], ROOT_OBJ, smooth=False), 0)

def surf_patch(name, poly, axis, s, off, mats, col=C_BODY, thick=0.0, step=0.012):
    """Flush skin over an outline (lenses, handle flaps): filled, projected, pushed `off` inward."""
    pts = densify(poly, step)
    bm = bmesh.new()
    vs = [bm.verts.new((u, v, 0)) for u, v in pts]
    es = [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=es)
    proj = project(axis, [(v.co.x, v.co.y) for v in bm.verts], s)
    d = proj[0][1]
    for v, (p, dd) in zip(list(bm.verts), proj):
        v.co = p + dd * off
    bm.normal_update()
    for f in bm.faces:
        if f.normal.dot(d) > 0:
            f.normal_flip()
    o = bm_to_obj(bm, name, col, mats, ROOT_OBJ)
    if thick:
        so = o.modifiers.new("Solidify", 'SOLIDIFY'); so.thickness = thick; so.offset = -1
    return o

def sect(a, b, n=16, e=0.5):
    return [(a * math.copysign(abs(math.cos(t)) ** e, math.cos(t)), b * math.copysign(abs(math.sin(t)) ** e, math.sin(t)))
            for t in (2 * math.pi * j / n for j in range(n))]

def sweep(bm, ctrl, n, section, ref=Vector((0, 0, 1)), cap=True, bank=0.0, mi=0, mi_edge=None):
    """Swept solid along a Catmull-Rom path; section(t) -> [(u, v)] (u: side, v: up)."""
    ctrl = [Vector(c) for c in ctrl]; rings = []
    for i in range(n + 1):
        t = i / n; p = catmull(ctrl, t)
        tg = (catmull(ctrl, min(t + 1e-3, 1)) - catmull(ctrl, max(t - 1e-3, 0))).normalized()
        sd = tg.cross(ref)
        if sd.length < 1e-6:
            sd = tg.cross(Vector((1, 0, 0)))
        sd.normalize(); up = sd.cross(tg).normalized()
        if bank:
            rm = Matrix.Rotation(bank, 3, tg); sd, up = rm @ sd, rm @ up
        rings.append([bm.verts.new(p + sd * u + up * v) for u, v in section(t)])
    m = len(rings[0]); faces = []
    for a, b in zip(rings, rings[1:]):
        for j in range(m):
            f = bm.faces.new((a[j], a[(j + 1) % m], b[(j + 1) % m], b[j]))
            f.material_index = mi_edge(j) if mi_edge else mi; faces.append(f)
    if cap:
        for f in (bm.faces.new(rings[0][::-1]), bm.faces.new(rings[-1])):
            f.material_index = mi; faces.append(f)
    return faces

def sweep_closed(bm, pts, section, ref, mi=lambda i, j: 0):
    """Swept ring along a closed 3D point loop; mi(i, j) picks material per ring i / section edge j."""
    pts = [Vector(p) for p in pts]; n = len(pts); rings = []
    for i in range(n):
        tg = (pts[(i + 1) % n] - pts[i - 1]).normalized()
        sd = tg.cross(ref)
        if sd.length < 1e-6:
            sd = tg.cross(Vector((1, 0, 0)))
        sd.normalize(); up = sd.cross(tg).normalized()
        rings.append([bm.verts.new(pts[i] + sd * u + up * v) for u, v in section(i / n)])
    m = len(rings[0])
    for i in range(n):
        a, b = rings[i], rings[(i + 1) % n]
        for j in range(m):
            bm.faces.new((a[j], a[(j + 1) % m], b[(j + 1) % m], b[j])).material_index = mi(i, j)

def round_poly(poly, r, seg=5):
    """Fillet every corner of a closed 2D polygon (quadratic Bezier)."""
    out = []; n = len(poly)
    for i in range(n):
        p, a, b = Vector(poly[i]), Vector(poly[i - 1]), Vector(poly[(i + 1) % n])
        d1 = min(r, (a - p).length * 0.45); d2 = min(r, (b - p).length * 0.45)
        q0 = p + (a - p).normalized() * d1; q2 = p + (b - p).normalized() * d2
        out += [tuple((1 - t) ** 2 * q0 + 2 * (1 - t) * t * p + t * t * q2) for t in (k / seg for k in range(seg + 1))]
    return out

def strip(bm, edge_a, edge_b, thick, up, mi=0):
    """Thin plate between two 3D edge polylines (vanes, slats, skirts)."""
    h = up.normalized() * (thick / 2)
    T = [[bm.verts.new(p + h) for p in e] for e in (edge_a, edge_b)]
    B = [[bm.verts.new(p - h) for p in e] for e in (edge_a, edge_b)]
    n = len(edge_a); fs = []
    for j in range(n - 1):
        fs += [bm.faces.new((T[0][j], T[0][j + 1], T[1][j + 1], T[1][j])),
               bm.faces.new((B[0][j], B[1][j], B[1][j + 1], B[0][j + 1])),
               bm.faces.new((T[0][j], B[0][j], B[0][j + 1], T[0][j + 1])),
               bm.faces.new((T[1][j + 1], B[1][j + 1], B[1][j], T[1][j]))]
    for e in (0, n - 1):
        fs.append(bm.faces.new((T[0][e], T[1][e], B[1][e], B[0][e])))
    for f in fs:
        f.material_index = mi

def cyl(bm, center, axis, r, depth, segs=24, mi=0, r2=None):
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r2 or r, depth=depth)
    rot = Vector((0, 0, 1)).rotation_difference(Vector(axis)).to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation(center) @ rot, verts=res["verts"])
    for f in {f for v in res["verts"] for f in v.link_faces}:
        f.material_index = mi
    return res

def lathe_x(bm, prof, segs, closed, a0=0.0, a1=2 * math.pi, mi=lambda j: 0):
    """Revolve (x, r) profile around the X axis; partial sweeps get capped."""
    full = abs(a1 - a0 - 2 * math.pi) < 1e-6
    na = segs if full else segs + 1
    rings = [[bm.verts.new((x, r * math.cos(a0 + (a1 - a0) * i / segs), r * math.sin(a0 + (a1 - a0) * i / segs)))
              for x, r in prof] for i in range(na)]
    n = len(prof)
    for i in range(segs):
        r0, r1 = rings[i], rings[(i + 1) % na]
        for j in range(n if closed else n - 1):
            bm.faces.new((r0[j], r1[j], r1[(j + 1) % n], r0[(j + 1) % n])).material_index = mi(j)
    if not full and closed:
        bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])

def lathe_y(bm, prof, center, segs, mi=0):
    """Revolve closed (r, y) profile around a Y-parallel axis through center (x, z)."""
    cx, cz = center; n = len(prof)
    rings = [[bm.verts.new((cx + r * math.cos(2 * math.pi * i / segs), y, cz + r * math.sin(2 * math.pi * i / segs)))
              for r, y in prof] for i in range(segs)]
    for i in range(segs):
        r0, r1 = rings[i], rings[(i + 1) % segs]
        for j in range(n):
            bm.faces.new((r0[j], r1[j], r1[(j + 1) % n], r0[(j + 1) % n])).material_index = mi

def finish(bm, name, col, mats, smooth=True, subsurf=0):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = bm_to_obj(bm, name, col, mats, ROOT_OBJ, smooth=smooth)
    if subsurf:
        o.modifiers.new("Subsurf", 'SUBSURF').levels = subsurf
    return o

C_LIGHTS = coll("HC_Lights", C_CAR)
C_AERO = coll("HC_Aero", C_CAR)
C_TRIM = coll("HC_Trim", C_CAR)
SIDES = ((-1, "R"), (1, "L"))                  # forward -Y, up +Z: vehicle left = +X
lerp = lambda pts, x: next(p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0])
                           for p, q in zip(pts, pts[1:]) if min(p[0], q[0]) <= x <= max(p[0], q[0]))

# ---------------------------------------------------------------- headlights: swept blade along the fender peak
HL_TOP = [(0.44, 0.378), (0.52, 0.41), (0.66, 0.452), (0.80, 0.497), (0.90, 0.537), (0.935, 0.553)]
HL_BOT = [(0.93, 0.522), (0.86, 0.478), (0.74, 0.425), (0.60, 0.385), (0.50, 0.362), (0.455, 0.345)]
hl_top = lambda x: lerp(HL_TOP, x); hl_bot = lambda x: lerp(HL_BOT[::-1], x)
for s, n in SIDES:
    poly = [(s * x, z) for x, z in HL_TOP + HL_BOT][::s]
    surf_cutter(f"Cut_Headlight_{n}", poly, 'y', -1, 0.065, m=M_HOUSING, bevel=0.004)
    surf_patch(f"HeadlightLens_{n}", offset_poly(poly, 0.0015), 'y', -1, 0.002, [M_LENS], col=C_LIGHTS)
    bm = bmesh.new()
    def inside(x, z, dep):
        p, d = project('y', [(s * x, z)], -1)[0]; return p + d * dep
    # main DRL blade: hugs the upper edge, turns in and down at the nose
    drl = [inside(x, hl_top(x) - 0.008, 0.022) for x in (0.47, 0.56, 0.66, 0.76, 0.85, 0.915)]
    sweep(bm, drl, 40, lambda t: sect(0.0042, 0.006, 12, 0.6), ref=Vector((0, 1, 0)), mi=1)
    # short inner light element along the lower inner edge
    inner = [inside(x, hl_bot(x) + 0.010, 0.026) for x in (0.475, 0.53, 0.60)]
    sweep(bm, inner, 16, lambda t: sect(0.0035, 0.005, 12, 0.6), ref=Vector((0, 1, 0)), mi=1)
    # two primary projector modules + one secondary, with metal bezels
    for x, r in ((0.69, 0.0125), (0.80, 0.0125), (0.585, 0.009)):
        zc = hl_top(x) - 0.029 if r > 0.01 else (hl_top(x) + hl_bot(x)) / 2 - 0.006
        f = inside(x, zc, 0.0)
        cyl(bm, f + Vector((0, 0.0215, 0)), (0, 1, 0), r + 0.0045, 0.004, mi=2)
        res = cyl(bm, f + Vector((0, 0.036, 0)), (0, 1, 0), r, 0.03, mi=0)
        front = min((fc for fc in {fc for v in res["verts"] for fc in v.link_faces}), key=lambda fc: fc.calc_center_median().y)
        front.material_index = 3
    finish(bm, f"Headlight_{n}", C_LIGHTS, [M_HOUSING, M_LED_W, M_BEZEL, M_PROJ])

# ---------------------------------------------------------------- taillights: two floating blades, dark centre zone
zlo = lambda x: lerp(lo_e, x); zhi = lambda x: lerp(hi_e[::-1], x)
zc_t = lambda x: (zlo(x) + zhi(x)) / 2
for s, n in SIDES:
    lens = ([(0.24, zlo(0.24))] + [p for p in lo_e if 0.24 < p[0] < 0.94] + [(0.94, zlo(0.94)), (0.94, zhi(0.94))]
            + [p for p in hi_e if 0.24 < p[0] < 0.94] + [(0.24, zhi(0.24))])          # stops short of the corner wrap
    surf_patch(f"TaillightLens_{n}", offset_poly([(s * x, z) for x, z in lens][::s], 0.003), 'y', 1, 0.002,
               [M_LENS_SMOKE], col=C_LIGHTS)
    bm = bmesh.new()
    def tl(x0, x1, dz, hh, mi, k=8):
        pts = []
        for i in range(k):
            x = x0 + (x1 - x0) * i / (k - 1)
            p, d = project('y', [(s * x, zc_t(x) + dz)], 1)[0]; pts.append(p + d * 0.02)
        sweep(bm, pts, 6 * k, lambda t: sect(0.004, hh, 12, 0.6), ref=Vector((0, 1, 0)), mi=mi)
    tl(0.33, 0.84, 0.006, 0.0045, 1)       # primary red blade
    tl(0.40, 0.80, -0.009, 0.004, 2)       # brake bar
    tl(0.865, 0.928, 0.0, 0.006, 3, 4)     # amber indicator tip (rises with the corner)
    tl(0.26, 0.31, 0.0, 0.007, 4, 3)       # reverse light, inner end
    finish(bm, f"Taillight_{n}", C_LIGHTS, [M_HOUSING, M_LED_R, M_LED_BRAKE, M_LED_AMB, M_LED_REV])

# ---------------------------------------------------------------- active rear spoiler: flush blade in a recessed seat
SP_Y0, SP_Y1 = 1.884, 2.136
sp_hw = lambda y: 0.596 + 0.02 * (y - SP_Y0) / (SP_Y1 - SP_Y0)
seat = [(-sp_hw(SP_Y0) - 0.004, SP_Y0 - 0.004), (sp_hw(SP_Y0) + 0.004, SP_Y0 - 0.004),
        (sp_hw(SP_Y1) + 0.004, SP_Y1 + 0.004), (-sp_hw(SP_Y1) - 0.004, SP_Y1 + 0.004)]
surf_cutter("Cut_SpoilerSeat", seat, 'z', 0, 0.03, m=M_DARK, bevel=0.003)
NU, NV = 30, 8
bm = bmesh.new(); top, bot = [], []
for v in range(NV + 1):
    y = SP_Y0 + (SP_Y1 - SP_Y0) * v / NV; hw = sp_hw(y)
    rowt, rowb = [], []
    for u in range(NU + 1):
        x = -hw + 2 * hw * u / NU; z = surf_z(x, y)
        lip = 0.005 * smoothstep(0.75, 1.0, v / NV)          # subtle trailing-edge kick
        rowt.append(bm.verts.new((x, y, z + 0.0005 + lip))); rowb.append(bm.verts.new((x, y, z - 0.016)))
    top.append(rowt); bot.append(rowb)
for v in range(NV):
    for u in range(NU):
        bm.faces.new((top[v][u], top[v][u + 1], top[v + 1][u + 1], top[v + 1][u]))
        bm.faces.new((bot[v][u], bot[v + 1][u], bot[v + 1][u + 1], bot[v][u + 1]))
ring_t = top[0] + [r[-1] for r in top[1:]] + top[-1][::-1][1:] + [r[0] for r in top[::-1][1:-1]]
ring_b = bot[0] + [r[-1] for r in bot[1:]] + bot[-1][::-1][1:] + [r[0] for r in bot[::-1][1:-1]]
for j in range(len(ring_t)):
    k = (j + 1) % len(ring_t)
    bm.faces.new((ring_t[j], ring_b[j], ring_b[k], ring_t[k]))
hinge = Vector((0, SP_Y0, surf_z(0, SP_Y0) - 0.008))
bm.transform(Matrix.Translation(-hinge))
spoiler = finish(bm, "ActiveSpoiler", C_AERO, [M_CARBON], smooth=True)
spoiler.location = hinge
spoiler.rotation_euler.x = math.radians(3)          # default: very slightly raised; pivot = front hinge line
spoiler["open_test_deg"] = 18.0
bm = bmesh.new()
for hx in (-0.38, 0.38):
    zf = surf_z(hx, 1.91)
    box_bm(bm, (hx - 0.012, SP_Y0 + 0.006, zf - 0.03), (hx + 0.012, SP_Y0 + 0.05, zf - 0.012))
finish(bm, "ActiveSpoilerHinge", C_AERO, [M_DARK], smooth=False)

# ---------------------------------------------------------------- mirrors: blade housing on a buttress-style sail stem
for s, n in SIDES:
    bm = bmesh.new()
    def mshape(t):
        k = (0.62 + 0.38 * math.sin(math.pi / 2 * min(t * 1.7, 1))) * (1 - 0.8 * smoothstep(0.72, 1.0, t))
        return sect(0.066 * k, 0.040 * max(k, 0.35), 16, 0.45)
    sweep(bm, [(s * 0.905, -0.508, 0.872), (s * 0.98, -0.502, 0.882), (s * 1.05, -0.495, 0.888), (s * 1.105, -0.488, 0.890)],
          24, mshape, ref=Vector((0, 0, 1)), mi=0)
    sweep(bm, [(s * 0.775, -0.535, 0.790), (s * 0.84, -0.525, 0.828), (s * 0.935, -0.508, 0.868)], 14,
          lambda t: sect(0.040 - 0.010 * t, 0.011, 12, 0.5), ref=Vector((0, 0, 1)), mi=1)
    finish(bm, f"Mirror_{n}", C_TRIM, [M_CLAY, M_CARBON], subsurf=1)
    bm = bmesh.new()
    g = [bm.verts.new((s * (0.995 + 0.075 * u), -0.441, 0.883 + 0.030 * v)) for u, v in sect(1, 1, 20, 0.45)]
    bm.faces.new(g)
    finish(bm, f"MirrorGlass_{n}", C_TRIM, [M_MIRROR])

# ---------------------------------------------------------------- flush door handles
for s, n in SIDES:
    slot = [(0.02, 0.752), (0.155, 0.758), (0.155, 0.778), (0.02, 0.772)]
    surf_cutter(f"Cut_DoorHandle_{n}", slot, 'x', s, 0.016, bevel=0.003)
    surf_patch(f"DoorHandle_{n}", offset_poly(slot, 0.003), 'x', s, 0.0015, [M_CLAY], col=C_TRIM, thick=0.004)

# ---------------------------------------------------------------- panel gaps (3.5 mm)
for s, n in SIDES:
    groove(f"Cut_Gap_Door_{n}", [(-0.915, 0.78), (-0.935, 0.55), (-0.935, 0.27), (0.235, 0.27), (0.25, 0.45),
                                 (0.215, 0.78)], 'x', s)
    groove(f"Cut_Gap_FrontBumper_{n}", [(-2.03, 0.56), (-1.93, 0.48), (-1.83, 0.40), (-1.80, 0.32)], 'x', s)
    groove(f"Cut_Gap_RearBumperSide_{n}", [(1.86, 0.40), (2.07, 0.40)], 'x', s)
groove("Cut_Gap_Hood", [(-0.55, -2.17), (0.55, -2.17), (0.585, -2.0), (0.585, -0.84), (-0.585, -0.84), (-0.585, -2.0)],
       'z', closed=True)
groove("Cut_Gap_EngineCover", [(-0.44, 0.84), (0.44, 0.84), (0.45, 1.84), (-0.45, 1.84)], 'z', closed=True)
groove("Cut_Gap_RearBumper", [(-0.70, 0.405), (0.70, 0.405)], 'y', 1)

# ---------------------------------------------------------------- engine cover heat extraction: 4 broad louvers per side
bm = bmesh.new()
for s, n in SIDES:
    surf_cutter(f"Cut_EngineVent_{n}", [(s * 0.13, 1.40), (s * 0.35, 1.40), (s * 0.35, 1.76), (s * 0.13, 1.76)][::s],
                'z', 0, 0.035, bevel=0.012)
    for yv in (1.445, 1.525, 1.605, 1.685):
        xs_ = [s * (0.145 + 0.19 * i / 6) for i in range(7)]
        ea = [Vector((x, yv - 0.022, surf_z(x, yv) - 0.016)) for x in xs_]
        eb = [Vector((x, yv + 0.022, surf_z(x, yv) - 0.004)) for x in xs_]
        strip(bm, ea, eb, 0.007, Vector((0, -0.45, 1)))
finish(bm, "EngineVents", C_AERO, [M_CARBON], smooth=False)

# ---------------------------------------------------------------- rear corner extraction vents with directional vanes
for s, n in SIDES:
    rv = round_poly([(0.64, 0.255), (0.855, 0.255), (0.875, 0.485), (0.745, 0.505)], 0.035)
    surf_cutter(f"Cut_RearVent_{n}", [(s * x, z) for x, z in rv][::s], 'y', 1, 0.07)
    bm = bmesh.new()
    lip = [p + d * -0.0015 for p, d in project('y', [(s * x, z) for x, z in offset_poly(rv, -0.004)], 1)]
    sweep_closed(bm, lip, lambda t: sect(0.0055, 0.004, 8, 0.7), Vector((0, 1, 0)), mi=lambda i, j: 1)
    for zv in (0.31, 0.375, 0.44):
        x0 = 0.64 + 0.105 * (zv - 0.255) / 0.25 + 0.008; x1 = 0.855 + 0.02 * (zv - 0.255) / 0.23 - 0.008
        xs_ = [x0 + (x1 - x0) * i / 5 for i in range(6)]
        pa = [p + d * 0.02 for p, d in project('y', [(s * x, zv) for x in xs_], 1)]
        strip(bm, pa, [p + Vector((0, -0.045, -0.02)) for p in pa], 0.006, Vector((0, 0.4, 1)))
    finish(bm, f"RearVent_{n}", C_AERO, [M_CARBON, M_CLAY], smooth=True)

# ---------------------------------------------------------------- rear diffuser: ramp + 2 structural vanes + 2 channel walls
DY0, DY1 = 1.50, Y1 + 0.02
ramp = lambda y: F["zb"](y) - 0.006
bm = bmesh.new()
ysd = [DY0 + (DY1 - DY0) * i / 20 for i in range(21)]
xr = [-0.70 + 1.40 * i / 14 for i in range(15)]
T_ = [[bm.verts.new((x, y, ramp(y))) for x in xr] for y in ysd]
B_ = [[bm.verts.new((x, y, ramp(y) - 0.008)) for x in xr] for y in ysd]
for i in range(len(ysd) - 1):
    for j in range(len(xr) - 1):
        bm.faces.new((T_[i][j], T_[i + 1][j], T_[i + 1][j + 1], T_[i][j + 1]))
        bm.faces.new((B_[i][j], B_[i][j + 1], B_[i + 1][j + 1], B_[i + 1][j]))
for i in range(len(ysd) - 1):
    for j in (0, len(xr) - 1):
        bm.faces.new((T_[i][j], B_[i][j], B_[i + 1][j], T_[i + 1][j]))
for i in (0, len(ysd) - 1):
    for j in range(len(xr) - 1):
        bm.faces.new((T_[i][j], T_[i][j + 1], B_[i][j + 1], B_[i][j]))
def vane(xc, wr, wt, hmax, diverge):
    rings = []
    for i in range(3, len(ysd)):
        y = ysd[i]; t = (y - DY0) / (DY1 - DY0)
        x0 = xc + diverge * t * t; zr = ramp(y) - 0.008; tip = zr - hmax * t ** 1.3
        sec = [(-wr / 2 - 0.014, zr + 0.03), (-wr / 2, zr - 0.012), (-wt / 2, tip + 0.008), (0, tip),
               (wt / 2, tip + 0.008), (wr / 2, zr - 0.012), (wr / 2 + 0.014, zr + 0.03)]
        rings.append([bm.verts.new((x0 + u, y, z)) for u, z in sec])
    m = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for j in range(m):
            bm.faces.new((a[j], b[j], b[(j + 1) % m], a[(j + 1) % m]))
    bm.faces.new(rings[0]); bm.faces.new(rings[-1][::-1])
for sx_ in (-1, 1):
    vane(sx_ * 0.30, 0.055, 0.020, 0.17, sx_ * 0.03)      # structural vanes framing the central tunnel
    vane(sx_ * 0.67, 0.050, 0.030, 0.16, 0.0)             # side-channel walls under the bumper
finish(bm, "RearDiffuser", C_AERO, [M_CARBON], smooth=False)

# ---------------------------------------------------------------- front splitter: thin blade, raised outer edges, side returns
bm = bmesh.new()
xs_ = [-0.86 + 1.72 * i / 34 for i in range(35)]
yf = lambda x: Y0 - 0.045 + 0.20 * x * x
zt_ = lambda x: 0.117 + 0.010 * smoothstep(0.55, 0.86, abs(x))
ea = [Vector((x, yf(x), zt_(x) - 0.006)) for x in xs_]
eb = [Vector((x, -2.02, zt_(x) - 0.006)) for x in xs_]
strip(bm, ea, eb, 0.012, Vector((0, 0, 1)))
for sx_ in (-1, 1):
    x = sx_ * 0.85
    pa = [Vector((x, yf(x) + 0.01 + (-2.03 - yf(x) - 0.01) * i / 4, zt_(x))) for i in range(5)]
    pb = [p + Vector((0, 0, 0.045 + 0.04 * i / 4)) for i, p in enumerate(pa)]
    strip(bm, pa, pb, 0.012, Vector((1, 0, 0)))
finish(bm, "FrontSplitter", C_AERO, [M_CARBON], smooth=False)

# ---------------------------------------------------------------- front intake vanes (centre blades + directional corner vanes)
bm = bmesh.new()
for zb_, hw in ((0.205, 0.40), (0.255, 0.37)):
    xs_ = [-hw + 2 * hw * i / 16 for i in range(17)]
    pa = [p + d * 0.03 for p, d in project('y', [(x, zb_) for x in xs_], -1)]
    strip(bm, pa, [p + Vector((0, 0.07, -0.012)) for p in pa], 0.007, Vector((0, 0.17, 1)))
for s, n in SIDES:
    zs_ = [0.175 + 0.13 * i / 5 for i in range(6)]
    pa = [p + d * 0.035 for p, d in project('y', [(s * (0.66 + 0.06 * (z - 0.175) / 0.13), z) for z in zs_], -1)]
    strip(bm, pa, [p + Vector((s * 0.03, 0.075, 0)) for p in pa], 0.007, Vector((1, -s * 0.4, 0)))
finish(bm, "FrontIntakeVanes", C_AERO, [M_CARBON], smooth=False)

# ---------------------------------------------------------------- side intake vane + carbon side skirts
for s, n in SIDES:
    bm = bmesh.new()
    ysv = [0.43 + 0.54 * i / 8 for i in range(9)]
    pa = [Vector((surf_x(y, 0.53 + 0.03 * (y - 0.43) / 0.54, s) - s * 0.008, y, 0.53 + 0.03 * (y - 0.43) / 0.54)) for y in ysv]
    strip(bm, pa, [p + Vector((-s * 0.17, 0.03, 0)) for p in pa], 0.008, Vector((0, -0.2, 1)))
    finish(bm, f"SideIntakeVane_{n}", C_AERO, [M_CARBON], smooth=False)
    bm = bmesh.new()
    ysk = [-0.93 + 1.83 * i / 24 for i in range(25)]
    xo = lambda y: 0.935 + 0.05 * math.sin(math.pi * (y + 0.93) / 1.83) ** 0.35
    strip(bm, [Vector((s * 0.84, y, 0.146)) for y in ysk], [Vector((s * xo(y), y, 0.146)) for y in ysk],
          0.012, Vector((0, 0, 1)))
    finish(bm, f"SideSkirt_{n}", C_AERO, [M_CARBON], smooth=False)

# ---------------------------------------------------------------- rolled wheel-arch lips
for k, (x, y, z, spec, side) in WHEELS.items():
    ex, ez, ne = ARCH[k[0]]
    rx, rz = spec["R"] + ex + 0.004, spec["R"] + ez + 0.004
    pts = []
    for j in range(61):
        t = math.radians(-20 + 220 * j / 60); c, s_ = math.cos(t), math.sin(t)
        py = rx * math.copysign(abs(c) ** (2 / ne), c); pz = rz * math.copysign(abs(s_) ** (2 / ne), s_)
        if z + pz < 0.20:
            continue
        sxv = surf_x(y + py, z + pz, side)
        if sxv is not None and abs(sxv) > 0.7:
            pts.append(Vector((sxv - side * 0.004, y + py, z + pz)))
    bm = bmesh.new()
    sweep(bm, pts, 3 * len(pts), lambda t: sect(0.009, 0.006, 10, 0.7), ref=Vector((1, 0, 0)))
    finish(bm, f"ArchLip_{k}", C_BODY, [M_CLAY])

# ---------------------------------------------------------------- exhaust: double-wall tips in the designed cavity
for s, n in SIDES:
    bm = bmesh.new(); c = (s * 0.13, 0.525)
    lathe_y(bm, [(0.054, 1.98), (0.064, 1.98), (0.064, 2.214), (0.0615, 2.223), (0.057, 2.224), (0.054, 2.216)], c, 40, mi=0)
    lathe_y(bm, [(0.040, 1.99), (0.046, 1.99), (0.046, 2.200), (0.040, 2.200)], c, 40, mi=1)
    cyl(bm, Vector((c[0], 2.0, c[1])), (0, 1, 0), 0.046, 0.004, segs=40, mi=1)
    finish(bm, f"Exhaust_{n}", C_CHASSIS, [M_EXH, M_EXH_IN])
bm = bmesh.new()
for s, n in SIDES:
    for zv in (0.47, 0.525, 0.58):
        pa = [p + d * 0.06 for p, d in project('y', [(s * (0.22 + 0.18 * i / 4), zv) for i in range(5)], 1)]
        strip(bm, pa, [p + Vector((0, -0.05, 0)) for p in pa], 0.008, Vector((0, 0, 1)))
finish(bm, "RearFascia_Trim", C_TRIM, [M_CARBON], smooth=False)

# ---------------------------------------------------------------- wheels: forged 5 double-spoke, center lock, carbon-ceramic brakes
for k, (x, y, z, sp, s) in WHEELS.items():
    R, hw, rr = sp["R"], sp["W"] / 2, sp["RIM"]
    loc = Vector((x, y, z)); rear = k[0] == "R"
    # tire: rounded shoulder, 3 circumferential grooves (sidewall text -> baked normal map later)
    tread = []
    for g in (-0.5 * hw, -0.1 * hw, 0.3 * hw):
        tread += [(g - 0.007, R), (g - 0.004, R - 0.007), (g + 0.004, R - 0.007), (g + 0.007, R)]
    prof = ([(-hw * .86, rr + .004), (-hw, rr + .03), (-hw, R - .05), (-hw + .004, R - .02), (-hw + .02, R - .006),
             (-hw + .05, R)] + tread +
            [(hw - .05, R), (hw - .02, R - .006), (hw - .004, R - .02), (hw, R - .05), (hw, rr + .03), (hw * .86, rr + .004)])
    bm = bmesh.new(); lathe_x(bm, prof, 96, True)
    t_ = finish(bm, f"Tire_{k}", C_WHEELS, [M_TIRE]); t_.location = loc
    t_.modifiers.new("Subsurf", 'SUBSURF').levels = 1

    # rim: inner flange, drop centre (inboard, clear of the caliper), barrel, machined outer lip
    bm = bmesh.new()
    prof = [(s * -hw * .86, rr + .014), (s * -hw * .86, rr - .004), (s * -hw * .80, rr - .010), (s * -hw * .70, rr - .030),
            (s * -hw * .48, rr - .030), (s * -hw * .40, rr - .012), (s * hw * .70, rr - .012), (s * hw * .88, rr - .012),
            (s * hw * .95, rr + .004), (s * hw * .95, rr + .016), (s * hw * .88, rr + .019)]
    lathe_x(bm, prof, 96, False, mi=lambda j: 1 if j >= 7 else 3)        # lip machined, barrel dark
    xf = s * hw * 0.90; conc = 0.10 if rear else 0.085
    for i in range(5):
        base = 2 * math.pi * i / 5 + math.pi / 2
        for sg in (-1, 1):
            a0, a1 = base + sg * math.radians(3.5), base + sg * math.radians(10.5)
            am, rm_ = (a0 + a1) / 2, (0.078 + rr) / 2
            ctrl = [(s * 0.069, 0.078 * math.cos(a0), 0.078 * math.sin(a0)),     # root anchored in the hub
                    (xf - s * conc * 0.42, rm_ * math.cos(am), rm_ * math.sin(am)),
                    (xf - s * 0.008, (rr - 0.016) * math.cos(a1), (rr - 0.016) * math.sin(a1))]
            def spoke_sec(t):
                w = 0.046 - 0.024 * t; d = 0.030 - 0.012 * t; c = 0.0035   # broad root -> slim outer
                sec = [(-w / 2, d / 2 - c), (-w / 2 + c, d / 2), (w / 2 - c, d / 2), (w / 2, d / 2 - c),
                       (w * 0.30, -d / 2), (-w * 0.30, -d / 2)]
                return [(u, v * s) for u, v in sec]          # machined face always outboard
            fs = sweep(bm, ctrl, 10, spoke_sec, ref=Vector((1, 0, 0)), mi=0,
                       mi_edge=lambda j: {1: 0, 0: 1, 2: 1}.get(j, 2))   # face silver, chamfers machined, sides graphite
            for f in fs:
                f.smooth = False
    hub_x = s * 0.047          # 2 mm clear of the rotor hat face
    cyl(bm, Vector((hub_x + s * 0.0225, 0, 0)), (s, 0, 0), 0.088, 0.045, segs=40, mi=2, r2=0.074)
    cyl(bm, Vector((hub_x + s * 0.052, 0, 0)), (s, 0, 0), 0.050, 0.016, segs=12, mi=1, r2=0.044)
    cyl(bm, Vector((hub_x + s * 0.064, 0, 0)), (s, 0, 0), 0.013, 0.012, segs=16, mi=1)
    o = finish(bm, f"Rim_{k}", C_WHEELS, [M_RIM, M_RIM_LIP, M_RIM_FACE, M_RIM_DARK]); o.location = loc

    # rotor + hat + drilled pattern
    bm = bmesh.new(); RO = sp["ROTOR"]
    lathe_x(bm, [(s * -0.027, 0.125), (s * 0.007, 0.125), (s * 0.007, RO), (s * -0.027, RO)], 72, True)
    lathe_x(bm, [(s * 0.0, 0.128), (s * 0.045, 0.120), (s * 0.045, 0.050), (s * 0.038, 0.050), (s * 0.038, 0.112),
                 (s * 0.0, 0.118)], 48, True, mi=lambda j: 1)
    for ri, rad in enumerate((0.150, 0.168, 0.186)):
        for j in range(30):
            a = 2 * math.pi * (j + ri / 3) / 30
            ring = [bm.verts.new((s * 0.0075, rad * math.cos(a) + 0.0035 * math.cos(b), rad * math.sin(a) + 0.0035 * math.sin(b)))
                    for b in (2 * math.pi * q / 6 for q in range(6))]
            bm.faces.new(ring).material_index = 2
    o = finish(bm, f"BrakeDisc_{k}", C_WHEELS, [M_ROTOR, M_HAT, M_DARK], smooth=False); o.location = loc

    # monoblock caliper: arc body straddling the rotor, trailing the axle, piston bosses (6-pot front / 4-pot rear)
    bm = bmesh.new(); tc = math.radians(20); span = math.radians(32)
    lo_x, hi_x = sorted((s * -0.066, s * 0.052))
    lathe_x(bm, [(lo_x, 0.150), (hi_x, 0.150), (hi_x, 0.243), (lo_x, 0.243)], 16, True, a0=tc - span, a1=tc + span)
    for da in ((-20, 0, 20) if not rear else (-12, 12)):
        a = tc + math.radians(da)
        cyl(bm, Vector((s * 0.0535, 0.197 * math.cos(a), 0.197 * math.sin(a))), (s, 0, 0), 0.024, 0.004, segs=24, r2=0.021)
    o = finish(bm, f"Caliper_{k}", C_WHEELS, [M_CALIPER], smooth=False); o.location = loc
    b = o.modifiers.new("Bevel", 'BEVEL'); b.width = 0.006; b.segments = 2; b.limit_method = 'ANGLE'
