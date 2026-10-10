# Phase 5: separate glazing + interior. Exec'd from build_interior.py after exterior_parts_p5.py
# (shares its globals: body, BODY_BVH, F, helpers sweep/strip/cyl/sect/finish/project/surf_z, materials ...).
# Phase 6: LEFT-HAND DRIVE. Forward -Y, up +Z: a driver facing -Y has +X on the left, so the driver sits at +X.
# Only asymmetric interior parts follow DRV_X / PSX; the steering wheel is translated (not mirrored) so its
# controls stay correct for the driver's hands.
DRV_X = 0.36
PSX = -1.0 if DRV_X > 0 else 1.0          # unit direction from the driver toward the passenger / tunnel

C_GLASS = coll("HC_Glass", C_CAR)
C_INT = coll("HC_Interior", C_CAR)

# ---------------------------------------------------------------- review materials (final = phase 6)
def glass_review():
    m = bpy.data.materials.new("MAT_Glass_Review"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.80, 0.83, 0.84, 1); b.inputs["Roughness"].default_value = 0.0
    b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = 1.45
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (0.86, 0.88, 0.89, 1)
    lp = nt.nodes.new("ShaderNodeLightPath"); mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs[0])      # glass doesn't black out the cabin
    nt.links.new(b.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], nt.nodes["Material Output"].inputs[0])
    m.diffuse_color = (0.7, 0.75, 0.78, 0.3)
    return m

M_GLASS_REV = glass_review()
MI_LEATHER = mat("MAT_InteriorLeather", (0.018, 0.018, 0.019), rough=0.45, coat=0.1)
MI_ALC = mat("MAT_InteriorAlcantara", (0.045, 0.045, 0.048), rough=0.95)
MI_CARBON = mat("MAT_InteriorCarbon", (0.03, 0.03, 0.033), rough=0.25, coat=0.8)
MI_PLASTIC = mat("MAT_InteriorPlastic", (0.03, 0.03, 0.032), rough=0.6)
MI_METAL = mat("MAT_InteriorMetal", (0.32, 0.32, 0.34), metal=1.0, rough=0.28)
MI_DISPLAY = emit_mat("MAT_Display", (0.01, 0.014, 0.025), 0.6)
MI_UI = emit_mat("MAT_DisplayGraphics", (0.75, 0.85, 1.0), 1.4)
MI_UI_RED = emit_mat("MAT_DisplayGraphics_Red", (1.0, 0.05, 0.03), 3.0)
MI_ACCENT = mat("MAT_SeatAccent", (0.82, 0.018, 0.015), rough=0.35, coat=0.4)
MI_SPEAKER = mat("MAT_Speaker", (0.05, 0.05, 0.055), metal=0.6, rough=0.5)
MI_MIRROR = mat("MAT_InteriorMirror", (0.9, 0.9, 0.9), metal=1.0, rough=0.02)
MI_AMBIENT = emit_mat("MAT_AmbientLight", (1.0, 0.03, 0.02), 2.0)

def ifinish(bm, name, mats, smooth=True, subsurf=0, parent=None, origin=None, col=None):
    o = finish(bm, name, col or C_INT, mats, smooth=smooth, subsurf=subsurf)
    if origin is not None:
        o.data.transform(Matrix.Translation(-Vector(origin))); o.location = origin
    if parent:
        o.parent = parent; o.matrix_parent_inverse = parent.matrix_world.inverted()
    return o

def loft(bm, sections, mi=0, mi_edge=None, cap=True):
    """Closed sections (same vertex count) bridged in order."""
    rings = [[bm.verts.new(p) for p in sec] for sec in sections]
    m = len(rings[0])
    for a, b in zip(rings, rings[1:]):
        for j in range(m):
            bm.faces.new((a[j], a[(j + 1) % m], b[(j + 1) % m], b[j])).material_index = mi_edge(j) if mi_edge else mi
    if cap:
        for f in (bm.faces.new(rings[0][::-1]), bm.faces.new(rings[-1])):
            f.material_index = mi
    return rings

def rbox(bm, lo, hi, mi=0):
    r = box_bm(bm, lo, hi)
    for f in {f for v in r["verts"] for f in v.link_faces}:
        f.material_index = mi

# ---------------------------------------------------------------- 1. glazing: split out of Body_Shell
cut_mod = body.modifiers["Cutters"]; cut_mod.show_viewport = False
bpy.context.view_layer.update()
_ev = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
gbm = bmesh.new(); gbm.from_mesh(_ev.to_mesh()); _ev.to_mesh_clear()
cut_mod.show_viewport = True
bmesh.ops.delete(gbm, geom=[f for f in gbm.faces if f.material_index != 1], context='FACES')
gbm.faces.ensure_lookup_table()
seen, islands = set(), []
for f in gbm.faces:
    if f.index in seen:
        continue
    stack, isl = [f], []
    seen.add(f.index)
    while stack:
        g = stack.pop(); isl.append(g.index)
        for e in g.edges:
            for h in e.link_faces:
                if h.index not in seen:
                    seen.add(h.index); stack.append(h)
    islands.append(isl)

def glass_name(c):
    if abs(c.x) < 0.2:
        return "Windshield" if c.y < 0 else "Rear_Glass" if c.y < 0.80 else "EngineGlass"
    side = "R" if c.x < 0 else "L"                  # vehicle left = +X
    return f"Window_F{side}" if c.y < 0.62 else f"QuarterGlass_{side}"

GLASS = {}
for isl in islands:
    keep = set(isl); bmi = gbm.copy(); bmi.faces.ensure_lookup_table()
    bmesh.ops.delete(bmi, geom=[f for f in bmi.faces if f.index not in keep], context='FACES')
    lo = Vector([min(v.co[i] for v in bmi.verts) for i in range(3)])
    hi = Vector([max(v.co[i] for v in bmi.verts) for i in range(3)])
    name = glass_name((lo + hi) / 2)
    bnd = [v for v in bmi.verts if any(e.is_boundary for e in v.link_edges)]
    moves = {}
    for v in bnd:                                   # 1.5 mm clearance to the seal frame, along the surface
        inner = [e.other_vert(v).co for e in v.link_edges if not e.is_boundary]
        if inner:
            corner = len(inner) == 1                 # pane corner: the subdivided seal rounds inward most here
            moves[v] = (sum(inner, Vector()) / len(inner) - v.co).normalized() * (0.006 if corner else 0.003)
    for v, mv in moves.items():
        v.co += mv
    bmi.transform(body.matrix_world)
    o = finish(bmi, name, C_GLASS, [M_GLASS_REV])
    o.data.transform(Matrix.Translation(-(lo + hi) / 2)); o.location = (lo + hi) / 2      # origin at pane centre
    so = o.modifiers.new("Thickness", 'SOLIDIFY'); so.thickness = 0.005; so.offset = -1.0
    GLASS[name] = o
gbm.free()

# body keeps its seal frames; the panes are removed procedurally (last modifier, fully editable)
ng = bpy.data.node_groups.new("HC_DeleteGlassFaces", 'GeometryNodeTree')
ng.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
gi, go = ng.nodes.new("NodeGroupInput"), ng.nodes.new("NodeGroupOutput")
mid = ng.nodes.new("GeometryNodeInputMaterialIndex")
cmp = ng.nodes.new("FunctionNodeCompare"); cmp.data_type = 'INT'; cmp.operation = 'EQUAL'
ia = next(sk for sk in cmp.inputs if sk.name == "A" and sk.type == 'INT')
ib = next(sk for sk in cmp.inputs if sk.name == "B" and sk.type == 'INT'); ib.default_value = 1
dg_ = ng.nodes.new("GeometryNodeDeleteGeometry"); dg_.domain = 'FACE'
ng.links.new(gi.outputs[0], dg_.inputs["Geometry"]); ng.links.new(mid.outputs[0], ia)
ng.links.new(cmp.outputs[0], dg_.inputs["Selection"])
# Manifold boolean flat-shades some faces it re-triangulates; re-smooth paint (0) + carbon (3), keep cut walls flat
smooth = ng.nodes.new("GeometryNodeSetShadeSmooth"); smooth.domain = 'FACE'
orn = ng.nodes.new("FunctionNodeBooleanMath"); orn.operation = 'OR'
for idx, sock in ((0, 0), (3, 1)):
    c2 = ng.nodes.new("FunctionNodeCompare"); c2.data_type = 'INT'; c2.operation = 'EQUAL'
    ng.links.new(mid.outputs[0], next(sk for sk in c2.inputs if sk.name == "A" and sk.type == 'INT'))
    next(sk for sk in c2.inputs if sk.name == "B" and sk.type == 'INT').default_value = idx
    ng.links.new(c2.outputs[0], orn.inputs[sock])
ng.links.new(dg_.outputs[0], smooth.inputs["Geometry"]); ng.links.new(orn.outputs[0], smooth.inputs["Selection"])
smooth.inputs["Shade Smooth"].default_value = True
ng.links.new(smooth.outputs[0], go.inputs[0])
body.modifiers.new("DeleteGlassFaces", 'NODES').node_group = ng

# door hinge empties: future dihedral/butterfly pivot; door glass + trim parented to them
DOOR = {}
for s, n in SIDES:
    d = empty(f"Door_{n}", (s * 0.90, -0.95, 0.80), C_INT, ROOT_OBJ, kind='SINGLE_ARROW', size=0.25)
    DOOR[n] = d
    bpy.context.view_layer.update()                     # parent world matrix must exist before re-parenting
    for child in (GLASS[f"Window_F{n}"], bpy.data.objects[f"DoorHandle_{n}"]):
        mw = child.matrix_world.copy(); child.parent = d; child.matrix_world = mw

# ---------------------------------------------------------------- 2. cabin tub, firewall, footwells
FLOOR = 0.16
bm = bmesh.new()
rbox(bm, (-0.60, -1.02, FLOOR - 0.015), (0.60, 0.64, FLOOR), mi=0)                    # floor tub
toe = [Vector((x, -1.02, FLOOR)) for x in (-0.60, 0.60)]
strip(bm, toe, [p + Vector((0, 0.10, 0.30)) for p in toe], 0.012, Vector((0, -0.95, 0.31)), mi=0)   # toe board / firewall
rbox(bm, (-0.60, -0.92, 0.435), (0.60, -0.74, 0.45), mi=0)                            # under-dash closeout
for s, n in SIDES:
    rbox(bm, (s * 0.60 - 0.006, -1.02, FLOOR), (s * 0.60 + 0.006, -0.40, 0.46), mi=0)  # footwell side walls
    lo_, hi_ = sorted((s * 0.585, s * 0.625))
    rbox(bm, (lo_, -0.40, FLOOR), (hi_, 0.64, 0.30), mi=1)                             # carbon tub sills
ifinish(bm, "Interior_Tub", [MI_ALC, MI_CARBON], smooth=False)

# ---------------------------------------------------------------- 3. centre tunnel + console
tun_top = pchip([(-1.0, 0.30), (-0.75, 0.37), (-0.45, 0.44), (-0.30, 0.42), (-0.10, 0.40), (0.15, 0.43),
                 (0.40, 0.44), (0.62, 0.45)])
bm = bmesh.new()
secs = []
for i in range(25):
    y = -1.0 + 1.62 * i / 24; t = tun_top(y)
    secs.append([(-0.115, y, FLOOR), (0.115, y, FLOOR), (0.105, y, t - 0.03), (0.085, y, t), (-0.085, y, t),
                 (-0.105, y, t - 0.03)])
loft(bm, secs, mi=0, mi_edge=lambda j: 1 if j in (2, 3, 4) else 0)
ifinish(bm, "CenterTunnel", [MI_CARBON, MI_LEATHER], smooth=False)

bm = bmesh.new()
top = lambda y: tun_top(y) + 0.002
cyl(bm, Vector((0, -0.33, top(-0.33) + 0.004)), (0, 0, 1), 0.021, 0.008, segs=32, mi=1)          # start ring
cyl(bm, Vector((0, -0.33, top(-0.33) + 0.010)), (0, 0, 1), 0.014, 0.010, segs=32, mi=3)          # START button
for x in (-0.032, 0.0, 0.032):                                                                   # R / N / D toggles
    rbox(bm, (x - 0.008, -0.26, top(-0.25)), (x + 0.008, -0.235, top(-0.25) + 0.014), mi=1)
cyl(bm, Vector((0, -0.165, top(-0.165) + 0.009)), (0, 0, 1), 0.023, 0.018, segs=24, mi=1)         # mode rotary
cyl(bm, Vector((0, -0.165, top(-0.165) + 0.0185)), (0, 0, 1), 0.016, 0.002, segs=24, mi=0)
for x in (-0.05, 0.05):                                                                          # 2 guarded switches
    rbox(bm, (x - 0.011, -0.115, top(-0.11)), (x + 0.011, -0.085, top(-0.11) + 0.01), mi=0)
    rbox(bm, (x - 0.004, -0.106, top(-0.11) + 0.01), (x + 0.004, -0.094, top(-0.11) + 0.02), mi=3)
rbox(bm, (-0.07, -0.045, top(0.0) - 0.004), (0.07, 0.065, top(0.0) + 0.002), mi=2)                 # shallow storage tray
sweep(bm, [(0, 0.10, top(0.10) + 0.022), (0, 0.26, top(0.26) + 0.026), (0, 0.42, top(0.42) + 0.022)], 16,
      lambda t: sect(0.072, 0.024, 16, 0.5), ref=Vector((1, 0, 0)), mi=4)                          # armrest
ifinish(bm, "CenterConsole", [MI_PLASTIC, MI_METAL, MI_ALC, MI_ACCENT, MI_LEATHER])

# ---------------------------------------------------------------- 4. dashboard: low crown, driver shroud, flowing passenger side
DASH = [(-0.745, 0.705), (-0.62, 0.742), (-0.50, 0.735), (-0.43, 0.70), (-0.405, 0.62), (-0.43, 0.50),
        (-0.50, 0.44), (-0.745, 0.44)]
bm = bmesh.new(); secs = []
for i in range(25):
    x = -0.60 + 1.20 * i / 24
    fwd = -0.045 * smoothstep(0.10, 0.40, PSX * x) - 0.05 * smoothstep(0.48, 0.60, abs(x))     # passenger side flows forward
    secs.append([(x, y + (fwd if j in (3, 4, 5) else fwd * 0.5 if j in (2, 6) else 0),
                  z - (0.012 * smoothstep(0.10, 0.40, PSX * x) if j in (1, 2) else 0)) for j, (y, z) in enumerate(DASH)])
loft(bm, secs, mi=2, mi_edge=lambda j: 0 if j in (0, 1, 2) else 1 if j in (3, 4) else 2)
ifinish(bm, "Dashboard", [MI_ALC, MI_LEATHER, MI_PLASTIC], subsurf=1)

bm = bmesh.new()                                    # slim horizontal vents (2 outer + 1 centre), ambient strip
for xc, w in ((-0.48, 0.13), (0.50, 0.13), (0.0, 0.20)):
    yf = -0.405 - 0.045 * smoothstep(0.10, 0.40, PSX * xc) - 0.05 * smoothstep(0.48, 0.60, abs(xc)) - 0.004
    zc = 0.665 if xc else 0.705
    rbox(bm, (xc - w / 2, yf - 0.012, zc - 0.018), (xc + w / 2, yf + 0.01, zc + 0.018), mi=0)
    for dz in (-0.009, 0.0, 0.009):
        ea = [Vector((xc - w / 2 + 0.006 + (w - 0.012) * k / 4, yf - 0.014, zc + dz)) for k in range(5)]
        strip(bm, ea, [p + Vector((0, 0.012, -0.003)) for p in ea], 0.002, Vector((0, 0.25, 1)), mi=1)
amb = [Vector((-0.58 + 1.16 * k / 30, -0.432 - 0.045 * smoothstep(0.10, 0.40, PSX * (-0.58 + 1.16 * k / 30)), 0.697))
       for k in range(31)]
sweep(bm, amb, 60, lambda t: sect(0.0022, 0.0022, 8, 0.8), ref=Vector((0, 1, 0)), mi=2)
ifinish(bm, "Dashboard_Vents", [MI_PLASTIC, MI_METAL, MI_AMBIENT])

# ---------------------------------------------------------------- 5. instrument cluster (hooded) + centre screen

def text_mesh(bm, txt, size, basis, origin, mi):
    """Bake a text object into bm on a display plane (temporary UI)."""
    cu = bpy.data.curves.new("tmp_txt", 'FONT'); cu.body = txt; cu.size = size; cu.align_x = 'CENTER'
    ob = bpy.data.objects.new("tmp_txt", cu); sc.collection.objects.link(ob)
    bpy.context.view_layer.update()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    M = Matrix.Translation(origin) @ basis
    tmp = bmesh.new(); tmp.from_mesh(me); tmp.transform(M)
    vm = {v: bm.verts.new(v.co) for v in tmp.verts}
    for f in tmp.faces:
        bm.faces.new([vm[v] for v in f.verts]).material_index = mi
    tmp.free(); bpy.data.objects.remove(ob); bpy.data.curves.remove(cu); bpy.data.meshes.remove(me)

def screen_basis(normal):
    n = Vector(normal).normalized()
    right = Vector((0, 0, 1)).cross(n).normalized()          # viewer's right (= -X when facing -Y)
    up = n.cross(right).normalized()
    return Matrix((right, up, n)).transposed().to_4x4(), right, up, n

eye = Vector((DRV_X, 0.27, 0.955))
cc = Vector((DRV_X, -0.50, 0.745))            # pod on the dash top, seen over the wheel rim
B4, rt, up, nn = screen_basis(eye - cc)
bm = bmesh.new()
def quad(c, w, h, off, mi):
    vs = [bm.verts.new(c + rt * u + up * v + nn * off) for u, v in ((-w, -h), (w, -h), (w, h), (-w, h))]
    bm.faces.new(vs).material_index = mi
quad(cc, 0.13, 0.046, 0.0, 0)                                           # display surface
fr = [cc + rt * u + up * v - nn * 0.012 for u, v in ((-0.138, -0.054), (0.138, -0.054), (0.138, 0.054), (-0.138, 0.054))]
strip(bm, fr, [p + nn * 0.011 for p in fr], 0.004, up, mi=1)             # frame edges (bottom/top band)
for u in (-0.138, 0.138):
    e = [cc + rt * u + up * v - nn * 0.012 for v in (-0.054, 0.054)]
    strip(bm, e, [p + nn * 0.011 for p in e], 0.004, rt, mi=1)
vis = [Vector((DRV_X + 0.17 * math.sin(a), -0.475 - 0.02 * math.cos(a), 0.806 + 0.012 * math.cos(a)))
       for a in (math.pi * (k / 12 - 0.5) for k in range(13))]
strip(bm, vis, [p + Vector((0, -0.10, -0.004)) for p in vis], 0.007, Vector((0, 0.1, 1)), mi=2)  # visor
text_mesh(bm, "128", 0.040, B4, cc + up * -0.012 + nn * 0.0008, 3)
text_mesh(bm, "km/h", 0.011, B4, cc + up * -0.034 + nn * 0.0008, 3)
text_mesh(bm, "SPORT", 0.009, B4, cc + rt * -0.095 + up * -0.016 + nn * 0.0008, 4)
text_mesh(bm, "4", 0.034, B4, cc + rt * 0.095 + up * -0.016 + nn * 0.0008, 4)
for k in range(14):                                                     # rpm arc, red at the top end
    a = math.pi * (0.85 - 0.7 * k / 13); r0 = 0.055
    c = cc + rt * (r0 * math.cos(a) - 0.01) + up * (r0 * math.sin(a) - 0.035) + nn * 0.0008
    vs = [bm.verts.new(c + rt * u + up * v) for u, v in ((-0.004, -0.0025), (0.004, -0.0025), (0.004, 0.0025), (-0.004, 0.0025))]
    bm.faces.new(vs).material_index = 4 if k > 10 else 3
ifinish(bm, "InstrumentCluster", [MI_DISPLAY, MI_PLASTIC, MI_ALC, MI_UI, MI_UI_RED], smooth=False, origin=cc)

sc_c = Vector((0.0, -0.362, 0.615))
B4, rt, up, nn = screen_basis(Vector((DRV_X * 0.35, 0.94, 0.30)))
bm = bmesh.new()
quad(sc_c, 0.125, 0.06, 0.0, 0)
bz = [sc_c + rt * u + up * v - nn * 0.016 for u, v in ((-0.133, -0.068), (0.133, -0.068), (0.133, 0.068), (-0.133, 0.068))]
for a, b in zip(bz, bz[1:] + bz[:1]):
    strip(bm, [a, b], [a + nn * 0.015, b + nn * 0.015], 0.006, (b - a).cross(nn), mi=1)
for k, (u, v, w, h) in enumerate(((-0.07, 0.0, 0.028, 0.002), (0.06, 0.0, 0.04, 0.002), (0.0, -0.035, 0.10, 0.003))):
    c = sc_c + rt * u + up * v + nn * 0.0008
    vs = [bm.verts.new(c + rt * a + up * b) for a, b in ((-w, -h), (w, -h), (w, h), (-w, h))]
    bm.faces.new(vs).material_index = 3 if k < 2 else 4
text_mesh(bm, "DRIVE MODE", 0.008, B4, sc_c + up * 0.040 + nn * 0.001, 3)
text_mesh(bm, "SPORT", 0.022, B4, sc_c + rt * -0.045 + up * 0.008 + nn * 0.001, 4)
text_mesh(bm, "D", 0.040, B4, sc_c + rt * 0.075 + up * 0.002 + nn * 0.001, 3)
text_mesh(bm, "AERO  ACTIVE", 0.007, B4, sc_c + rt * -0.045 + up * -0.020 + nn * 0.001, 3)
ifinish(bm, "CenterScreen", [MI_DISPLAY, MI_METAL, MI_PLASTIC, MI_UI, MI_UI_RED], smooth=False, origin=sc_c)

# ---------------------------------------------------------------- 6. steering wheel (origin on steering axis), column, paddles
SW_C = Vector((DRV_X, -0.20, 0.645))
tilt = math.radians(25)
ex, ey = Vector((-1, 0, 0)), Vector((0, -math.sin(tilt), math.cos(tilt)))
ez = ex.cross(ey)                                       # steering axis, pointing at the driver
SWB = Matrix((ex, ey, ez)).transposed().to_4x4()
def L(x, y, z):
    return Vector((x, y, z))
bm = bmesh.new()
rim = [L(0.172 * math.cos(a), 0.148 * max(-1, min(1, 1.18 * math.sin(a))), 0) for a in (2 * math.pi * k / 96 for k in range(96))]
grip = lambda i: smoothstep(0.55, 0.92, abs(math.cos(2 * math.pi * i / 96)))
sweep_closed(bm, rim, lambda t: sect(0.016 * (1 + 0.2 * grip(t * 96)), 0.019 * (1 + 0.12 * grip(t * 96)), 14, 0.75),
             Vector((0, 0, 1)), mi=lambda i, j: 3 if abs(i - 24) <= 1 else 1 if abs(math.sin(2 * math.pi * i / 96)) > 0.75 else 0)
hub = [L(0.078 * u, 0.058 * v, -0.032) for u, v in sect(1, 1, 24, 0.55)]
hub_f = [L(p.x, p.y, -0.004) for p in hub]
loft(bm, [hub, hub_f], mi=1)
for side in (-1, 1):                                     # 2 horizontal spokes
    ea = [L(side * (0.07 + 0.095 * k / 4), 0.014 - 0.012 * k / 4, -0.022 + 0.022 * k / 4) for k in range(5)]
    strip(bm, ea, [p + L(0, -0.042, 0) for p in ea], 0.014, L(0, 0, 1), mi=1)
ea = [L(0.024, -0.05 - 0.085 * k / 4, -0.022 + 0.022 * k / 4) for k in range(5)]               # lower spoke
strip(bm, ea, [p + L(-0.048, 0, 0) for p in ea], 0.014, L(0, 0, 1), mi=1)
def button(c, r, h, mi, segs=20, knurl=False):
    """Machined control: straight wall + chamfered cap, flat shaded (crisp, not a smooth dome)."""
    fs = set()
    for res in (cyl(bm, c + L(0, 0, h * 0.35), (0, 0, 1), r, h * 0.7, segs=segs, mi=mi),
                cyl(bm, c + L(0, 0, h * 0.85), (0, 0, 1), r * 0.97, h * 0.3, segs=segs, mi=mi, r2=r * 0.78)):
        fs |= {f for v in res["verts"] for f in v.link_faces}
    for f in fs:
        f.smooth = False
for side in (-1, 1):                                     # multifunction buttons
    for k in range(2):
        button(L(side * (0.10 + 0.028 * k), -0.006, -0.001), 0.0072, 0.006, 4, segs=16)
button(L(-0.125, -0.052, -0.002), 0.016, 0.013, 2, segs=24)                     # mode rotary (driver's right hand)
cyl(bm, L(-0.125, -0.052, 0.0115), (0, 0, 1), 0.0035, 0.002, segs=12, mi=3)      # rotary index mark
button(L(0.125, -0.052, -0.001), 0.011, 0.009, 3, segs=24)                      # START button
quad_pts = [L(u, v, 0.0005) for u, v in ((-0.035, 0.012), (0.035, 0.012), (0.035, 0.040), (-0.035, 0.040))]
bm.faces.new([bm.verts.new(p) for p in quad_pts]).material_index = 5             # hub display
sw = ifinish(bm, "SteeringWheel", [MI_LEATHER, MI_CARBON, MI_METAL, MI_ACCENT, MI_PLASTIC, MI_DISPLAY])
sw.matrix_world = Matrix.Translation(SW_C) @ SWB; sw["steering_axis"] = "local Z (points at driver)"

bm = bmesh.new()
cyl(bm, ez * -0.13, ez, 0.034, 0.20, segs=32, mi=0, r2=0.040)
o = finish(bm, "SteeringColumn", C_INT, [MI_PLASTIC]); o.location = SW_C
for side, n in ((1, "L"), (-1, "R")):                    # local +x = world -X = driver's left... paddle names follow world side
    bm = bmesh.new()
    outline = [(0.0, 0.0), (0.12, -0.015), (0.135, 0.02), (0.11, 0.06), (0.0, 0.035)]
    a = [bm.verts.new(L(side * (0.07 + u), 0.005 + v, -0.05)) for u, v in outline]
    b = [bm.verts.new(L(side * (0.07 + u), 0.005 + v, -0.056)) for u, v in outline]
    bm.faces.new(a); bm.faces.new(b[::-1])
    for j in range(len(a)):
        k = (j + 1) % len(a); bm.faces.new((a[j], a[k], b[k], b[j]))
    pl = L(side * 0.07, 0.022, -0.053)                   # pivot on the column side of the blade
    bm.transform(Matrix.Translation(-pl))
    nm = "Paddle_R" if (SW_C + SWB.to_3x3() @ L(side * 0.1, 0, 0)).x < SW_C.x else "Paddle_L"   # driver's hands
    o = finish(bm, nm, C_INT, [MI_CARBON], smooth=False)
    o.matrix_world = Matrix.Translation(SW_C + SWB.to_3x3() @ pl) @ SWB

# ---------------------------------------------------------------- 7. pedals (driver footwell)
def pedal(name, x, p0, p1, w, mi_pad, pivot):
    bm = bmesh.new()
    nrm = (Vector((0, *p1)) - Vector((0, *p0))).normalized(); fwd = Vector((1, 0, 0)).cross(nrm)   # along pad / pad normal
    ea = [Vector((x - w / 2, *p0)), Vector((x - w / 2, *p1))]
    strip(bm, ea, [p + Vector((w, 0, 0)) for p in ea], 0.008, fwd, mi=0)
    for k in range(3):                                   # rubber grip strips
        c = Vector((x, *p0)).lerp(Vector((x, *p1)), (k + 1) / 4) + fwd * 0.005
        strip(bm, [c - Vector((w * 0.4, 0, 0)), c + Vector((w * 0.4, 0, 0))],
              [c - Vector((w * 0.4, 0, 0)) + nrm * 0.008, c + Vector((w * 0.4, 0, 0)) + nrm * 0.008], 0.003, fwd, mi=1)
    return ifinish(bm, name, [MI_METAL, MI_PLASTIC], smooth=False, origin=pivot)
XT, XB, XD = DRV_X + PSX * 0.085, DRV_X - PSX * 0.045, DRV_X - PSX * 0.17
pedal("Pedal_Throttle", XT, (-0.958, 0.19), (-0.885, 0.36), 0.06, 1, (XT, -0.958, 0.19))
pedal("Pedal_Dead", XD, (-0.985, 0.215), (-0.935, 0.37), 0.075, 1, (XD, -0.985, 0.215))
o = pedal("Pedal_Brake", XB, (-0.875, 0.255), (-0.845, 0.33), 0.085, 1, (XB, -0.80, 0.43))
bm = bmesh.new()                                         # hanging brake arm to the under-dash pivot
sweep(bm, [(XB, -0.80, 0.43), (XB, -0.83, 0.37), (XB, -0.855, 0.30)], 10,
      lambda t: sect(0.006, 0.012, 8, 0.6), ref=Vector((1, 0, 0)))
ifinish(bm, "Pedal_Brake_Arm", [MI_METAL], origin=(XB, -0.80, 0.43))

# ---------------------------------------------------------------- 8. carbon-shell bucket seats
SPINE = [(-0.44, 0.07), (-0.22, 0.02), (0.0, 0.0), (0.13, 0.09), (0.25, 0.36), (0.315, 0.56), (0.355, 0.685)]
wk = pchip([(0, 0.19), (0.3, 0.205), (0.5, 0.21), (0.7, 0.22), (0.85, 0.20), (0.93, 0.125), (1.0, 0.112)])
hk = pchip([(0, 0.05), (0.25, 0.075), (0.42, 0.03), (0.55, 0.10), (0.75, 0.11), (0.88, 0.06), (1.0, 0.025)])
def seat(name, xc):
    H = Vector((xc, 0.12, 0.31))
    ctrl = [H + Vector((0, y, z)) for y, z in SPINE]
    def shell(t):
        w, h = wk(t), hk(t)
        top = [(-w - 0.012, h - 0.008), (-w, h), (-w + 0.022, h * 0.5), (-w + 0.06, 0.012), (-w * 0.45, 0.003), (0, 0),
               (w * 0.45, 0.003), (w - 0.06, 0.012), (w - 0.022, h * 0.5), (w, h), (w + 0.012, h - 0.008)]
        back = [(v * 1.03, n - 0.024) for v, n in top[::-1]]
        return [(-n, v) for v, n in top + back]
    bm = bmesh.new()
    sweep(bm, ctrl, 44, shell, ref=Vector((1, 0, 0)), mi=0)
    def sub(t0, t1):
        return [catmull([Vector(c) for c in ctrl], t0 + (t1 - t0) * k / 6) for k in range(7)]
    for t0, t1 in ((0.02, 0.37), (0.45, 0.86), (0.905, 0.985)):                     # alcantara centre inserts
        sweep(bm, sub(t0, t1), 18, lambda t: [(-n, v) for v, n in
                                             [(-0.095, 0.004), (0.095, 0.004), (0.095, 0.026), (-0.095, 0.026)]],
              ref=Vector((1, 0, 0)), mi=1)
        for sv in (-1, 1):                                                          # leather side pads + red seam
            sweep(bm, sub(t0, t1), 18, lambda t, sv=sv: [(-n, sv * v) for v, n in
                                                       [(0.101, 0.004), (0.165, 0.008), (0.165, 0.030), (0.101, 0.024)]],
                  ref=Vector((1, 0, 0)), mi=2)
            sweep(bm, sub(t0, t1), 18, lambda t, sv=sv: [(-0.027 + u, sv * 0.098 + v) for u, v in sect(0.003, 0.003, 6, 1)],
                  ref=Vector((1, 0, 0)), mi=3)
    for sv in (-1, 1):                                                              # harness openings
        p = catmull([Vector(c) for c in ctrl], 0.875)
        rbox(bm, (p.x + sv * 0.07 - 0.012, p.y - 0.004, p.z - 0.022), (p.x + sv * 0.07 + 0.012, p.y + 0.03, p.z + 0.022), mi=5)
        rbox(bm, (xc + sv * 0.12 - 0.012, -0.32, FLOOR), (xc + sv * 0.12 + 0.012, 0.14, FLOOR + 0.03), mi=4)   # rails
        for yy in (-0.24, 0.06):
            zt_ = catmull([Vector(c) for c in ctrl], 0.18 if yy < 0 else 0.38).z - 0.02
            rbox(bm, (xc + sv * 0.12 - 0.008, yy - 0.012, FLOOR + 0.03), (xc + sv * 0.12 + 0.008, yy + 0.012, zt_), mi=4)
    return ifinish(bm, name, [MI_CARBON, MI_ALC, MI_LEATHER, MI_ACCENT, MI_METAL, MI_PLASTIC], subsurf=1, origin=H)
SEAT_D = seat("Seat_Driver", DRV_X)
SEAT_P = seat("Seat_Passenger", -DRV_X)

# ---------------------------------------------------------------- 9. door panels (follow the door skin; parented to door hinge)
DP = [(0.655, 0.755), (0.695, 0.735), (0.725, 0.69), (0.765, 0.575), (0.79, 0.43), (0.80, 0.30), (0.80, 0.27),
      (0.825, 0.27), (0.825, 0.43), (0.80, 0.58), (0.755, 0.705), (0.715, 0.755)]
for s, n in SIDES:
    bm = bmesh.new()
    secs = [[(s * x, -0.88 + 1.08 * i / 18, z) for x, z in DP] for i in range(19)]
    loft(bm, secs if s > 0 else [sec[::-1] for sec in secs], mi=1,
         mi_edge=lambda j: (0 if j in (0, 1) else 1 if j in (2, 3) else 2) if s > 0 else (0 if j in (9, 10) else 1 if j in (7, 8) else 2))
    sweep(bm, [(s * 0.735, -0.48, 0.60), (s * 0.738, -0.20, 0.605), (s * 0.735, 0.06, 0.60)], 18,
          lambda t: sect(0.024, 0.036, 14, 0.5), ref=Vector((0, 0, 1)), mi=1)                    # armrest
    sweep(bm, [(s * 0.735, -0.33, 0.632), (s * 0.70, -0.25, 0.648), (s * 0.735, -0.17, 0.632)], 12,
          lambda t: sect(0.007, 0.014, 8, 0.6), ref=Vector((1, 0, 0)), mi=0)                     # carbon pull strap
    rbox(bm, sorted((s * 0.705, s * 0.75))[:1] + [-0.47, 0.622], sorted((s * 0.705, s * 0.75))[1:] + [-0.39, 0.628], mi=3)
    for yy in (-0.455, -0.425, -0.405):
        cyl(bm, Vector((s * 0.722, yy, 0.63)), (0, 0, 1), 0.0055, 0.004, segs=12, mi=3)          # window / lock switches
    cyl(bm, Vector((s * 0.790, -0.68, 0.40)), (s, 0, 0), 0.062, 0.004, segs=32, mi=3)            # speaker ring
    cyl(bm, Vector((s * 0.787, -0.68, 0.40)), (s, 0, 0), 0.055, 0.004, segs=32, mi=4)            # speaker grille
    sweep(bm, [(s * 0.704, -0.84 + 1.0 * k / 6, 0.728) for k in range(7)], 36,
          lambda t: sect(0.0022, 0.0022, 8, 0.8), ref=Vector((0, 0, 1)), mi=5)                    # ambient strip
    ifinish(bm, f"DoorPanel_{n}", [MI_CARBON, MI_LEATHER, MI_ALC, MI_METAL, MI_SPEAKER, MI_AMBIENT], parent=DOOR[n])

# ---------------------------------------------------------------- 10. headliner, pillar liners, overhead console, rear-view mirror
bm = bmesh.new(); NXh, NYh = 16, 12
grid = [[Vector((-0.40 + 0.80 * u / NXh, -0.02 + 0.58 * v / NYh, 0)) for u in range(NXh + 1)] for v in range(NYh + 1)]
for row in grid:
    for p in row:
        p.z = surf_z(p.x, p.y) - 0.022
vs = [[bm.verts.new(p) for p in row] for row in grid]
for v in range(NYh):
    for u in range(NXh):
        bm.faces.new((vs[v][u], vs[v + 1][u], vs[v + 1][u + 1], vs[v][u + 1]))
hl = ifinish(bm, "Headliner", [MI_ALC])
hl.modifiers.new("Thickness", 'SOLIDIFY').thickness = 0.008
bm = bmesh.new()
for s, n in SIDES:
    ap = [Vector((s * (F["wr"](y) - 0.025), y, F["zr"](y) - 0.035)) for y in (-0.68, -0.52, -0.36, -0.20, -0.05)]
    sweep(bm, ap, 24, lambda t: sect(0.022, 0.008, 10, 0.6), ref=Vector((0, 1, 0)), mi=0)        # A-pillar liner
    bp = [Vector((s * 0.56, 0.62, 0.84)), Vector((s * 0.49, 0.615, 0.96)), Vector((s * 0.41, 0.61, 1.05))]
    sweep(bm, bp, 12, lambda t: sect(0.018, 0.008, 10, 0.6), ref=Vector((0, 1, 0)), mi=0)        # B/C pillar liner
zc_ = surf_z(0, 0.07) - 0.03
rbox(bm, (-0.07, 0.02, zc_ - 0.022), (0.07, 0.12, zc_), mi=1)                                    # overhead console
for x in (-0.03, 0.03):
    rbox(bm, (x - 0.012, 0.05, zc_ - 0.026), (x + 0.012, 0.075, zc_ - 0.022), mi=2)
ifinish(bm, "PillarTrim", [MI_ALC, MI_PLASTIC, MI_METAL])
bm = bmesh.new()
cyl(bm, Vector((0, -0.045, 1.085)), (0, -0.6, -1), 0.008, 0.05, segs=12, mi=1)
sweep(bm, [(-0.11, -0.072, 1.045), (0, -0.075, 1.047), (0.11, -0.072, 1.045)], 18,
      lambda t: sect(0.026 * (1 - 0.6 * smoothstep(0.85, 1, abs(2 * t - 1))), 0.021, 14, 0.45), ref=Vector((0, 0, 1)), mi=0)
mvs = [bm.verts.new((0.095 * u, -0.0525, 1.046 + 0.019 * v)) for u, v in sect(1, 1, 20, 0.45)]
bm.faces.new(mvs).material_index = 2
ifinish(bm, "RearViewMirror", [MI_PLASTIC, MI_METAL, MI_MIRROR], origin=(0, -0.045, 1.10))

# ---------------------------------------------------------------- 11. rear bulkhead + engine-view area
bm = bmesh.new()
bh = [(-0.58, FLOOR), (0.58, FLOOR), (0.58, 0.78), (0.46, 0.90), (-0.46, 0.90), (-0.58, 0.78)]
loft(bm, [[(x, 0.66, z) for x, z in bh], [(x, 0.635, z) for x, z in bh]], mi=0)
sweep(bm, [(-0.30, 0.625, 0.62), (0.0, 0.62, 0.625), (0.30, 0.625, 0.62)], 14,
      lambda t: sect(0.20, 0.016, 16, 0.4), ref=Vector((0, 1, 0)), mi=1)                        # padded centre section
fr_ = [Vector((x, 0.632, z)) for x, z in ((-0.58, 0.78), (-0.46, 0.90), (0.46, 0.90), (0.58, 0.78))]
sweep(bm, fr_, 24, lambda t: sect(0.012, 0.012, 8, 0.6), ref=Vector((0, 1, 0)), mi=2)            # engine-glass frame
for x in (-0.42, 0.42):
    rbox(bm, (x - 0.02, 0.625, 0.30), (x + 0.02, 0.635, 0.76), mi=2)                             # carbon uprights
ifinish(bm, "RearBulkhead", [MI_PLASTIC, MI_ALC, MI_CARBON])

bm = bmesh.new()
rbox(bm, (-0.55, 0.70, 0.58), (0.55, 1.80, 0.60), mi=0)                                          # bay floor
for x in (-0.55, 0.55):
    rbox(bm, (x - 0.008, 0.70, 0.60), (x + 0.008, 1.80, 0.80), mi=0)
for x in (-0.17, 0.17):                                                                          # intake plenums
    sweep(bm, [(x, 0.86, 0.80), (x, 1.10, 0.815), (x, 1.34, 0.80)], 16,
          lambda t: sect(0.095, 0.042, 16, 0.45), ref=Vector((0, 0, 1)), mi=1)
    for k in range(4):                                                                           # runners
        cyl(bm, Vector((x * 1.9, 0.92 + 0.12 * k, 0.78)), (1, 0, 0.3), 0.022, 0.12, segs=16, mi=2)
sweep(bm, [(-0.43, 1.00, 0.855), (0.0, 1.00, 0.862), (0.43, 1.00, 0.855)], 16,
      lambda t: sect(0.016, 0.016, 12, 1), ref=Vector((0, 1, 0)), mi=2)                         # cross brace
ifinish(bm, "EngineBay_Detail", [MI_PLASTIC, MI_CARBON, MI_METAL])

# ---------------------------------------------------------------- 12. cabin QA light + cameras
C_IQA = coll("HC_Interior_QA")
l = bpy.data.lights.new("Light_CabinFill", 'AREA'); l.energy = 14; l.size = 0.7; l.size_y = 0.45
o = bpy.data.objects.new("Light_CabinFill", l); C_IQA.objects.link(o); o.location = (0, 0.12, 1.03)
INT_CAMS = {
    "Camera_Cockpit_QA": ((DRV_X, 0.27, 0.955), 22, (DRV_X, -1.2, 0.84)),
    "Cam_int_driver": ((PSX * 0.38, 0.30, 1.00), 18, (DRV_X, -0.25, 0.62)),
    "Cam_int_passenger": ((-PSX * 0.38, 0.30, 1.00), 18, (-DRV_X, -0.30, 0.60)),
    "Cam_int_dashboard": ((0.0, 0.47, 1.03), 20, (0.0, -0.55, 0.66)),
    "Cam_int_seats": ((0.0, -0.40, 0.86), 18, (0.0, 0.30, 0.48)),
    "Cam_int_steering": ((DRV_X + 0.05, 0.10, 0.90), 32, (DRV_X, -0.22, 0.66)),
    "Cam_int_cockpit": ((PSX * 0.05, 0.56, 1.06), 16, (-PSX * 0.10, -0.45, 0.62)),
    "Cam_glass_fit_front_3q": ((-1.65, -1.75, 1.32), 38, (-0.45, -0.40, 0.95)),
    "Cam_glass_fit_side": ((-2.7, -0.05, 1.0), 38, (-0.70, 0.0, 0.95)),
}
for n, (loc, lens, tgt) in INT_CAMS.items():
    cd = bpy.data.cameras.new(n); cd.lens = lens; cd.clip_start = 0.01
    co = bpy.data.objects.new(n, cd); C_STUDIO.objects.link(co); co.location = loc
    c = co.constraints.new('TRACK_TO'); c.target = empty(f"Target_{n}", tgt, C_STUDIO)
    c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'

# headroom: headrest tops vs headliner / roof directly above
hr = []
for st in (SEAT_D, SEAT_P):
    e = st.evaluated_get(bpy.context.evaluated_depsgraph_get()); m = e.to_mesh()
    tp = max((st.matrix_world @ v.co for v in m.vertices), key=lambda p: p.z); e.to_mesh_clear()
    hr.append(surf_z(tp.x, tp.y) - 0.022 - 0.008 - tp.z)
sc["headroom_headrest_to_headliner_mm"] = round(min(hr) * 1000, 1)
print("HEADROOM mm", [round(h * 1000, 1) for h in hr])
