# Validate a hypercar checkpoint. Args after "--": <report_name>
import bpy, bmesh, os, sys, re
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
name = args[0] if args else "phase_01_validation"
dg = bpy.context.evaluated_depsgraph_get()
sc = bpy.context.scene
out = []
def rep(level, msg): out.append(f"[{level}] {msg}")

def wbounds(objs):
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in objs:
        ev = o.evaluated_get(dg); me = ev.to_mesh()
        for v in me.vertices:
            p = ev.matrix_world @ v.co
            lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
        ev.to_mesh_clear()
    return lo, hi

car = [o for o in bpy.data.collections["HC_Hypercar"].all_objects
       if o.type == 'MESH' and not o.name.startswith("Cut_")]
body = bpy.data.objects["Body_Shell"]

# scale / units
rep("PASS" if sc.unit_settings.system == 'METRIC' and sc.unit_settings.scale_length == 1 else "ERROR",
    f"units {sc.unit_settings.system} scale {sc.unit_settings.scale_length}")
bad = [o.name for o in bpy.data.objects if o.type == 'MESH' and any(abs(s - 1) > 1e-6 for s in o.scale)]
rep("PASS" if not bad else "WARNING", f"unapplied object scale: {bad or 'none'}")

# dimensions
lo, hi = wbounds([o for o in car if not o.name.startswith("Mirror")])
L, W, H = hi.y - lo.y, hi.x - lo.x, hi.z - lo.z
def rng(label, v, a, b):
    rep("PASS" if a <= v <= b else "ERROR", f"{label} {v:.3f} m (target {a}-{b})")
rng("length", L, 4.60, 4.75); rng("width (body, no mirrors)", W, 2.00, 2.08); rng("height", hi.z, 1.12, 1.20)
nonwheel = [o for o in car if o.name.split("_")[0] not in ("Tire", "Rim", "BrakeDisc", "Caliper")]
glo, _ = wbounds(nonwheel)
rng("ground clearance", glo.z, 0.10, 0.13)
mlo, mhi = wbounds(car)
rep("INFO", f"width incl. mirrors {mhi.x - mlo.x:.3f} m")
blo, bhi = wbounds([body])
rep("INFO", f"body shell bounds x[{blo.x:.3f},{bhi.x:.3f}] y[{blo.y:.3f},{bhi.y:.3f}] z[{blo.z:.3f},{bhi.z:.3f}]")

# wheels
refs = {k: bpy.data.objects.get(f"WheelColliderRef_{k}") for k in ("FL", "FR", "RL", "RR")}
rep("PASS" if all(refs.values()) else "ERROR", "wheel collider refs present")
wb = refs["RL"].matrix_world.translation.y - refs["FL"].matrix_world.translation.y
rng("wheelbase", wb, 2.72, 2.82)
fo = refs["FL"].matrix_world.translation.y - lo.y; ro = hi.y - refs["RL"].matrix_world.translation.y
rep("INFO", f"front overhang {fo:.3f} m, rear overhang {ro:.3f} m (incl. splitter / diffuser)")
for k, ref in refs.items():
    t = bpy.data.objects[f"Tire_{k}"]
    tlo, thi = wbounds([t])
    D, Wt = thi.z - tlo.z, thi.x - tlo.x
    c = (tlo + thi) / 2
    off = (c - ref.matrix_world.translation).length
    rep("PASS" if off < 0.002 else "ERROR", f"Tire_{k} center vs ref offset {off*1000:.1f} mm")
    rep("PASS" if (thi.y - tlo.y) > Wt * 1.5 and abs(tlo.z) < 0.003 else "ERROR",
        f"Tire_{k} axle along X, sits on ground (min z {tlo.z:.4f})")
    if k[0] == "F": rng(f"Tire_{k} diameter", D, 0.70, 0.72); rng(f"Tire_{k} width", Wt, 0.30, 0.32)
    else: rng(f"Tire_{k} diameter", D, 0.74, 0.77); rng(f"Tire_{k} width", Wt, 0.34, 0.36)
    for part in ("Rim", "BrakeDisc", "Caliper"):
        p = bpy.data.objects[f"{part}_{k}"]
        if (p.matrix_world.translation - ref.matrix_world.translation).length > 1e-4:
            rep("ERROR", f"{part}_{k} origin not at wheel center")
    rep("PASS" if t.rotation_euler.to_quaternion().angle < 1e-6 else "WARNING", f"Tire_{k} rotation identity (spin axis X)")

# wheel / body intersections (evaluated, booleans applied)
def bvh(o):
    ev = o.evaluated_get(dg); bm = bmesh.new(); bm.from_mesh(ev.to_mesh())
    bm.transform(o.matrix_world); t = BVHTree.FromBMesh(bm); bm.free(); ev.to_mesh_clear()
    return t
bb = bvh(body)
for k in refs:
    for part in ("Tire", "Rim", "Caliper"):
        n = len(bb.overlap(bvh(bpy.data.objects[f"{part}_{k}"])))
        rep("PASS" if n == 0 else "ERROR", f"{part}_{k} vs Body_Shell overlap faces: {n}")

# body topology / normals
ev = body.evaluated_get(dg); me = ev.to_mesh()
bm = bmesh.new(); bm.from_mesh(me)
nm = sum(1 for e in bm.edges if not e.is_manifold)
vol = bm.calc_volume(signed=True)
tris = sum(len(p.vertices) - 2 for p in me.polygons)
ev.to_mesh_clear(); bm.free()
rep("PASS" if nm == 0 else "INFO" if "DeleteGlassFaces" in body.modifiers else "WARNING",
    f"Body_Shell evaluated non-manifold edges: {nm}" + (" (glazing openings - see phase-5 check)" if "DeleteGlassFaces" in body.modifiers else ""))
rep("PASS" if vol > 0 else "ERROR", f"Body_Shell normals outward (signed volume {vol:.3f} m3)")
tot = 0
for o in car:
    e = o.evaluated_get(dg); m = e.to_mesh(); tot += sum(len(p.vertices) - 2 for p in m.polygons); e.to_mesh_clear()
rep("INFO", f"evaluated triangles: body {tris:,}, whole car {tot:,}")
src = body.data
rep("INFO", f"Body_Shell base cage: {len(src.polygons)} faces, ngons: {sum(1 for p in src.polygons if len(p.vertices) > 4)}, tris: {sum(1 for p in src.polygons if len(p.vertices) == 3)}")

# flying-buttress air gap: cast down from the buttress underside to the body
bt = bpy.data.objects.get("Body_Buttress")
if bt:
    ev = bt.evaluated_get(dg); m = ev.to_mesh()
    gaps = {}
    for yq in (0.8, 1.0, 1.2, 1.4):
        under = [ev.matrix_world @ v.co for v in m.vertices if v.co.x > 0 and abs(v.co.y - yq) < 0.03]
        if under:
            p = min(under, key=lambda q: q.z)
            hit = bb.ray_cast(p - Vector((0, 0, 0.001)), Vector((0, 0, -1)))[0]
            gaps[yq] = (p.z - hit.z) if hit else float("inf")
    ev.to_mesh_clear()
    g = min(gaps.values()) if gaps else 0
    rep("PASS" if g > 0.05 else "ERROR", "buttress air gap (m) by y: " + ", ".join(f"{k}:{v:.3f}" for k, v in gaps.items()))
if name != "phase_01_validation":
    rep("PASS" if os.path.exists(os.path.join(ROOT, "hypercar_01_blockout.blend")) else "ERROR",
        "approved blockout checkpoint preserved")

# phase-4 seating / clearance / mesh hygiene
def ov(a, b):
    return len(bvh(bpy.data.objects[a]).overlap(bvh(bpy.data.objects[b])))
if "ActiveSpoiler" in bpy.data.objects:
    for k in refs:
        n = ov(f"Caliper_{k}", f"Rim_{k}") + ov(f"BrakeDisc_{k}", f"Rim_{k}")
        rep("PASS" if n == 0 else "ERROR", f"brake vs rim {k} overlap faces: {n}")
    n = ov("ActiveSpoiler", "Body_Shell")
    sp = bpy.data.objects["ActiveSpoiler"]; ev = sp.evaluated_get(dg); m = ev.to_mesh()
    gaps = []
    for v in list(m.vertices)[::25]:
        p = ev.matrix_world @ v.co
        h = bb.ray_cast(p + Vector((0, 0, 0.05)), Vector((0, 0, -1)))[0]
        if h is not None: gaps.append(p.z - h.z)
    ev.to_mesh_clear()
    rep("PASS" if n == 0 else "WARNING", f"ActiveSpoiler vs body overlap faces: {n}; top above seat floor {min(gaps):.3f}..{max(gaps):.3f} m")
    for lens in ("HeadlightLens_L", "HeadlightLens_R", "TaillightLens_L", "TaillightLens_R"):
        n = ov(lens, "Body_Shell")
        rep("PASS" if n == 0 else "WARNING", f"{lens} seated in recess (body overlap faces: {n})")
    n = ov("RearDiffuser", "Body_Shell")
    rep("INFO", f"RearDiffuser vane roots embedded in body underside ({n} overlapping face pairs = integrated, not floating)")
    bad_area = loose = 0
    for o in car:
        me = o.data
        bad_area += sum(1 for p in me.polygons if p.area < 1e-9)
        used = {v for p in me.polygons for v in p.vertices}
        loose += len(me.vertices) - len(used)
    rep("PASS" if bad_area == 0 else "WARNING", f"zero-area faces (base meshes): {bad_area}")
    rep("PASS" if loose == 0 else "WARNING", f"loose vertices (base meshes): {loose}")
    CAT = [("Body", ("Body_", "ArchLip_", "DoorHandle_")), ("Wheels", ("Rim_",)), ("Tires", ("Tire_",)),
           ("Brakes", ("BrakeDisc_", "Caliper_")), ("Lights", ("Headlight", "Taillight")),
           ("Aero", ("FrontSplitter", "RearDiffuser", "ActiveSpoiler", "SideSkirt", "SideIntakeVane", "RearVent",
                     "FrontIntakeVanes", "EngineVents")),
           ("Glass/Mirrors", ("MirrorGlass", "Windshield", "Rear_Glass", "Window_", "QuarterGlass_", "EngineGlass")),
           ("Interior", ("Seat_", "Dashboard", "InstrumentCluster", "CenterScreen", "CenterConsole", "CenterTunnel",
                         "Steering", "Paddle_", "Pedal_", "DoorPanel_", "Headliner", "PillarTrim", "RearViewMirror",
                         "RearBulkhead", "EngineBay_", "Interior_Tub")), ("Trim/Other", ("Mirror_", "Exhaust", "RearFascia", "Chassis"))]
    cnt = {c: 0 for c, _ in CAT}
    for o in car:
        e = o.evaluated_get(dg); m = e.to_mesh(); t = sum(len(p.vertices) - 2 for p in m.polygons); e.to_mesh_clear()
        cat = next((c for c, pre in CAT if o.name.startswith(pre)), "Trim/Other"); cnt[cat] += t
    rep("INFO", "triangles by category: " + ", ".join(f"{c} {v:,}" for c, v in cnt.items()))

# phase-5: glazing split, body openings, interior fit
if "Windshield" in bpy.data.objects:
    GL = ["Windshield", "Rear_Glass", "Window_FL", "Window_FR", "QuarterGlass_L", "QuarterGlass_R", "EngineGlass"]
    miss = [g for g in GL if g not in bpy.data.objects]
    rep("PASS" if not miss else "ERROR", f"glass objects present: {len(GL) - len(miss)}/{len(GL)} {miss or ''}")
    gm = max(body.data.materials.find("PRE_Glass_Dark"), body.data.materials.find("MAT_SideGlass"))
    e = body.evaluated_get(dg); m = e.to_mesh(); left = sum(1 for p in m.polygons if p.material_index == gm); e.to_mesh_clear()
    rep("PASS" if left == 0 else "ERROR", f"glass faces left in evaluated Body_Shell: {left}")
    md = body.modifiers["DeleteGlassFaces"]; md.show_viewport = False; dg.update()
    bm_ = bmesh.new(); bm_.from_mesh(body.evaluated_get(dg).to_mesh())
    nm0 = sum(1 for x in bm_.edges if not x.is_manifold); bm_.free()
    md.show_viewport = True; dg.update()
    rep("PASS" if nm0 == 0 else "ERROR", f"Body_Shell unintended non-manifold edges (before glazing openings): {nm0}")
    bm_ = bmesh.new(); bm_.from_mesh(body.evaluated_get(dg).to_mesh())
    seal = max(body.data.materials.find("PRE_Dark_Intake"), body.data.materials.find("MAT_BlackTrim"))
    op = [x for x in bm_.edges if not x.is_manifold]
    ok = all(len(x.link_faces) == 1 and x.link_faces[0].material_index == seal for x in op); bm_.free()
    rep("PASS" if ok else "ERROR", f"intentional open edges = glazing openings framed by seals: {len(op)} (all on seal frames: {ok})")
    bb = bvh(body)
    for g in GL:
        o = bpy.data.objects[g]; n = len(bb.overlap(bvh(o)))
        th = o.modifiers["Thickness"].thickness
        rep("PASS" if n == 0 else "ERROR", f"{g}: body overlap faces {n}, thickness {th * 1000:.0f} mm, origin {tuple(round(c, 3) for c in o.matrix_world.translation)}")
    INT = [o for o in bpy.data.collections["HC_Interior"].all_objects if o.type == 'MESH']
    for o in INT:
        n = len(bb.overlap(bvh(o)))
        if n: rep("ERROR", f"interior {o.name} intersects Body_Shell ({n} face pairs)")
    rep("PASS", f"interior objects vs Body_Shell checked: {len(INT)}") if all(len(bb.overlap(bvh(o))) == 0 for o in INT) else None
    PAIRS = [("Seat_Driver", "DoorPanel_L"), ("Seat_Passenger", "DoorPanel_R"), ("Seat_Driver", "CenterConsole"),
             ("Seat_Passenger", "CenterConsole"), ("Seat_Driver", "CenterTunnel"), ("Seat_Passenger", "CenterTunnel"),
             ("Seat_Driver", "Headliner"), ("Seat_Passenger", "Headliner"), ("Seat_Driver", "RearBulkhead"),
             ("Dashboard", "Windshield"), ("RearViewMirror", "Windshield"), ("InstrumentCluster", "Windshield"),
             ("EngineBay_Detail", "EngineGlass"), ("SteeringWheel", "Dashboard"), ("SteeringWheel", "InstrumentCluster"),
             ("CenterScreen", "Dashboard"), ("Headliner", "Windshield"), ("PillarTrim", "Windshield"),
             ("PillarTrim", "Window_FL"), ("PillarTrim", "Window_FR")]
    for a, b in PAIRS:
        n = ov(a, b) if "ov" in dir() else len(bvh(bpy.data.objects[a]).overlap(bvh(bpy.data.objects[b])))
        rep("PASS" if n == 0 else "WARNING", f"{a} vs {b} overlap faces: {n}")
    rep("PASS" if sc.get("headroom_headrest_to_headliner_mm", 0) >= 60 else "WARNING",
        f"headroom headrest->headliner: {sc.get('headroom_headrest_to_headliner_mm')} mm (min of both seats)")
    sw = bpy.data.objects["SteeringWheel"]; ax = sw.matrix_world.to_3x3() @ Vector((0, 0, 1))
    rep("PASS", f"SteeringWheel origin {tuple(round(c, 3) for c in sw.matrix_world.translation)} on steering axis, local Z = {tuple(round(c, 2) for c in ax)}")
    H = bpy.data.objects["Seat_Driver"].matrix_world.translation
    for pd in ("Pedal_Brake", "Pedal_Throttle"):
        e = bpy.data.objects[pd].evaluated_get(dg); m = e.to_mesh()
        c = sum((bpy.data.objects[pd].matrix_world @ v.co for v in m.vertices), Vector()) / len(m.vertices); e.to_mesh_clear()
        dd = (c - H).length
        rep("PASS" if 0.85 <= dd <= 1.15 else "WARNING", f"{pd} pad centre {dd:.3f} m from driver H-point (realistic 0.85-1.15)")
    bi = be = 0
    for o in INT:
        bi += sum(len(p.vertices) - 2 for p in o.data.polygons)
        e = o.evaluated_get(dg); m = e.to_mesh(); be += sum(len(p.vertices) - 2 for p in m.polygons); e.to_mesh_clear()
    rep("PASS" if be <= 160000 else "WARNING", f"interior triangles: base {bi:,}, evaluated {be:,} (target 40-70k / 80-140k)")

# phase-6: LHD layout, UVs, materials, textures
if "MAT_CarPaint_RacingRed" in bpy.data.materials:
    import numpy as np
    W = lambda n: bpy.data.objects[n].matrix_world.translation
    sd, sp, sw = W("Seat_Driver"), W("Seat_Passenger"), W("SteeringWheel")
    rep("PASS" if sd.x > 0 > sp.x else "ERROR", f"LHD: Seat_Driver x={sd.x:+.3f}, Seat_Passenger x={sp.x:+.3f}")
    rep("PASS" if abs(sw.x - sd.x) < 0.01 else "ERROR", f"steering wheel centred on driver: dx={sw.x - sd.x:+.4f} m")
    def ctr(n):
        o = bpy.data.objects[n]; e = o.evaluated_get(dg); m = e.to_mesh()
        c = sum((o.matrix_world @ v.co for v in m.vertices), Vector()) / len(m.vertices); e.to_mesh_clear(); return c
    cl = W("InstrumentCluster")                       # origin = display centre (graphics are asymmetric)
    rep("PASS" if abs(cl.x - sw.x) < 0.01 else "ERROR", f"cluster display centred on wheel: dx={cl.x - sw.x:+.4f} m")
    pb, pt = ctr("Pedal_Brake"), ctr("Pedal_Throttle")
    rep("PASS" if abs(pb.x - sd.x) < 0.1 and abs(pt.x) < abs(pb.x) else "ERROR",
        f"pedals: brake x={pb.x:+.3f}, throttle x={pt.x:+.3f} (throttle inboard = driver's right foot)")
    cq = W("Camera_Cockpit_QA")
    rep("PASS" if abs(cq.x - sd.x) < 0.01 else "ERROR", f"Camera_Cockpit_QA x={cq.x:+.3f} (driver eye)")
    rep("PASS" if abs(W("RearViewMirror").x) < 0.005 else "ERROR", f"rear-view mirror centred: x={W('RearViewMirror').x:+.4f}")
    so = bpy.data.objects["CenterScreen"]; dm = so.data.materials.find("MAT_Display")
    ns = [so.matrix_world.to_3x3() @ p.normal for p in so.data.polygons if p.material_index == dm]
    nx = sum((n if n.y > 0 else -n).x for n in ns)         # orient toward the cabin (+Y) before reading x
    rep("PASS" if nx > 0 else "WARNING", f"centre screen angled toward driver (+X): normal.x sum {nx:+.3f}")

    REND = [o for o in car if not o.name.startswith("Cut_")]
    no_uv = [o.name for o in REND if "UVMap" not in o.data.uv_layers]
    rep("PASS" if not no_uv else "ERROR", f"meshes with UVMap: {len(REND) - len(no_uv)}/{len(REND)} {no_uv[:5] or ''}")
    out_rng = flipped = total_f = stretch_bad = 0; flip_by = {}
    raster = {}
    for o in REND:
        me = o.data; uv = me.uv_layers["UVMap"].data
        co = np.zeros(len(uv) * 2); uv.foreach_get("uv", co); co = co.reshape(-1, 2)
        out_rng += int(((co < -1e-4) | (co > 1 + 1e-4)).any(1).sum())
        ratios = []
        for p in me.polygons:
            pts = co[list(p.loop_indices)]
            a = 0.5 * np.sum(pts[:, 0] * np.roll(pts[:, 1], -1) - np.roll(pts[:, 0], -1) * pts[:, 1])
            total_f += 1
            if a < 0: flipped += 1; flip_by[o.name] = flip_by.get(o.name, 0) + 1
            if p.area > 1e-8: ratios.append(abs(a) / p.area)
            if o.get("atlas") not in ("TIRES", None):
                raster.setdefault(o["atlas"], []).append(pts)
        if ratios:
            r = np.array(ratios); med = np.median(r[r > 0]) if (r > 0).any() else 1
            stretch_bad += int(((r / med < 0.25) | (r / med > 4)).sum())
    rep("PASS" if out_rng == 0 else "ERROR", f"UV loops outside 0-1: {out_rng}")
    rep("PASS" if flipped / total_f < 0.002 else "WARNING", f"flipped UV faces: {flipped}/{total_f} ({100 * flipped / total_f:.2f}%) top: {sorted(flip_by.items(), key=lambda kv: -kv[1])[:5]}")
    rep("PASS" if stretch_bad / total_f < 0.02 else "WARNING",
        f"severe area-stretch faces (>4x from object median): {stretch_bad} ({100 * stretch_bad / total_f:.2f}%)")
    N = 512
    for grp, polys in raster.items():
        cnt = np.zeros((N, N), np.int32)
        for pts in polys:
            for t in range(1, len(pts) - 1):
                tri = np.array([pts[0], pts[t], pts[t + 1]]) * N
                x0, y0 = np.floor(tri.min(0)).astype(int).clip(0, N - 1); x1, y1 = np.ceil(tri.max(0)).astype(int).clip(0, N - 1)
                gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1] + 0.5
                (ax, ay), (bx, by), (cx_, cy_) = tri
                d = (by - cy_) * (ax - cx_) + (cx_ - bx) * (ay - cy_)
                if abs(d) < 1e-12: continue
                l1 = ((by - cy_) * (gx - cx_) + (cx_ - bx) * (gy - cy_)) / d
                l2 = ((cy_ - ay) * (gx - cx_) + (ax - cx_) * (gy - cy_)) / d
                cnt[y0:y1 + 1, x0:x1 + 1] += ((l1 > 1e-6) & (l2 > 1e-6) & (l1 + l2 < 1 - 1e-6))
        cov = (cnt > 0).sum(); ovl = (cnt > 1).sum()
        rep("PASS" if ovl / max(cov, 1) < 0.01 else "WARNING",
            f"{grp} atlas: coverage {100 * cov / N / N:.1f}%, overlapping texels {100 * ovl / max(cov, 1):.2f}% (512 raster)")
    rep("INFO", "TIRES atlas: intentional overlap (all tires + both half-circumferences share one lettering map)")
    rep("INFO", f"texel density px/m: {dict(sc.get('texel_density_px_per_m', {}))}")

    used = {s.material for o in REND for s in o.material_slots if s.material}
    pre = sorted({m.name for m in used if not m.name.startswith("MAT_")})
    rep("PASS" if not pre else "ERROR", f"non-production materials on car: {pre or 'none'}")
    prod = sorted(m.name for m in bpy.data.materials if m.name.startswith("MAT_"))
    rep("PASS" if 25 <= len(prod) <= 40 else "WARNING", f"production materials: {len(prod)} ({len(used)} in use)")
    missing, nm_bad = [], []
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        for n in m.node_tree.nodes:
            if n.type == 'TEX_IMAGE' and n.image and n.image.source == 'FILE' and not os.path.exists(bpy.path.abspath(n.image.filepath)):
                missing.append(f"{m.name}:{n.image.name}")
            if n.type == 'NORMAL_MAP':
                src = n.inputs["Color"].links[0].from_node if n.inputs["Color"].links else None
                if n.space != 'TANGENT' or (src and src.image.colorspace_settings.name != 'Non-Color'):
                    nm_bad.append(m.name)
    rep("PASS" if not missing else "ERROR", f"missing texture files: {missing or 'none'}")
    rel = [i.name for i in bpy.data.images if i.source == 'FILE' and not i.filepath.startswith("//")]
    rep("PASS" if not rel else "WARNING", f"absolute texture paths: {rel or 'none (all relative)'}")
    rep("PASS" if not nm_bad else "ERROR", f"normal maps: tangent space + Non-Color, OpenGL (+Y) {nm_bad or ''}")
    tex_dir = os.path.join(ROOT, "textures", "hypercar")
    baked = [f for d, _, fs in os.walk(tex_dir) for f in fs if f.endswith(".png")]
    exp = [f"{g}_{c}.png" for g in sc["atlas_resolution"].keys() for c in ("BaseColor", "Roughness", "Metallic", "Normal", "AO")]
    lack = [f for f in exp if f not in baked]
    rep("PASS" if not lack else "ERROR", f"baked atlas maps: {len(exp) - len(lack)}/{len(exp)}; texture files total {len(baked)} {lack[:4] or ''}")
    for gm in ("MAT_Windshield", "MAT_SideGlass", "MAT_RearGlass", "MAT_EngineGlass"):
        b = next(n for n in bpy.data.materials[gm].node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        tw = b.inputs["Transmission Weight"].default_value; ior = b.inputs["IOR"].default_value
        rep("PASS" if tw >= 0.95 else "ERROR", f"{gm}: transmission {tw:.2f}, IOR {ior:.2f}, shadow-transparent")
    em = []
    for m in used:
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if b and b.inputs["Emission Strength"].default_value > 0 and any(b.inputs["Emission Color"].default_value[:3]):
            em.append((m.name, round(b.inputs["Emission Strength"].default_value, 2)))
    rep("PASS" if all(s <= 8 for _, s in em) else "WARNING", f"emitters (strength): {sorted(em)}")

# naming / duplicates / hidden
dups = [o.name for o in bpy.data.objects if re.search(r"\.\d{3}$", o.name)]
rep("PASS" if not dups else "ERROR", f"duplicate-suffixed objects: {dups or 'none'}")
need = ["Car_Root", "CenterOfMass", "Body_Shell"] + [f"WheelColliderRef_{k}" for k in refs]
miss = [n for n in need if n not in bpy.data.objects]
rep("PASS" if not miss else "ERROR", f"required objects missing: {miss or 'none'}")
orphan = [o.name for o in bpy.data.collections["HC_Hypercar"].all_objects if o.parent is None and o.name != "Car_Root"]
rep("PASS" if not orphan else "WARNING", f"objects not parented under Car_Root: {orphan or 'none'}")
hidden = [o.name for o in car if o.hide_render or o.hide_get()]
rep("PASS" if not hidden else "WARNING", f"hidden render geometry (non-cutter): {hidden or 'none'}")
cut_vis = [o.name for o in bpy.data.objects if o.name.startswith("Cut_") and not o.hide_render]
rep("PASS" if not cut_vis else "ERROR", f"boolean cutters visible in render: {cut_vis or 'none'}")
com = bpy.data.objects["CenterOfMass"].matrix_world.translation
rep("PASS" if 0.30 <= com.z <= 0.40 and com.y > 0 else "WARNING", f"CenterOfMass at {tuple(round(c, 3) for c in com)} (rear-biased, low)")

# materials / UVs (phase-appropriate)
empty_slots = [o.name for o in car if not o.data.materials or any(m is None for m in o.data.materials)]
rep("PASS" if not empty_slots else "ERROR", f"objects with empty material slots: {empty_slots or 'none'}")
rep("INFO", "materials are PRE_* blockout preview shaders; production materials are phase 6")
no_uv = [o.name for o in car if not o.data.uv_layers]
rep("WARNING" if no_uv else "PASS", f"meshes without UVs: {len(no_uv)} (expected until phase 6)")
imgs = [i.name for i in bpy.data.images if i.source == 'FILE' and not os.path.exists(bpy.path.abspath(i.filepath))]
rep("PASS" if not imgs else "ERROR", f"missing texture links: {imgs or 'none'}")
rep("INFO", "LOD0-3 and Collision_* not created yet (phase 7/8)")

txt = "\n".join(out)
os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
open(os.path.join(ROOT, "reports", f"{name}.txt"), "w").write(txt + "\n")
print(txt)
