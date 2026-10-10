# Phase 9: re-import an exported FBX into factory-clean scenes and validate it independently of the source scene.
# Args after "--": <fbx file name in exports/> <tag>. Pass 1 = normal round-trip import (Blender space);
# pass 2 = raw import with NO axis conversion = exactly the coordinates Unity reads.
import bpy, os, sys, json, math
from mathutils import Vector, Matrix
from mathutils.kdtree import KDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda f: os.path.join(ROOT, "reports", f)
fname, tag = sys.argv[sys.argv.index("--") + 1:][:2]
FBXP = os.path.join(ROOT, "exports", fname)
SRC = os.path.join(ROOT, "hypercar_08_unity_export.blend")
out = []; data = {"file": fname}
def rep(lv, msg): out.append(f"[{lv}] {msg}")
ID = Matrix.Identity(4)
def world(o): return (world(o.parent) @ o.matrix_parent_inverse if o.parent else ID) @ o.matrix_basis
def ob(n): return bpy.data.objects.get(n)
def wpts(o, n=40):
    vs = o.data.vertices; st = max(1, len(vs) // n); W = world(o); return [W @ vs[i].co for i in range(0, len(vs), st)]
def rot_about(p, c, ax, a): return c + Matrix.Rotation(a, 3, ax) @ (p - c)
def tris(o): return sum(len(p.vertices) - 2 for p in o.data.polygons)

wref = json.load(open(R("wheel_reference_points.json"))); piv = json.load(open(R("pivot_validation.json")))
cst = json.load(open(R("collider_stats.json"))); p7 = json.load(open(R("phase_07_lod_counts.json")))
EXPSET = json.load(open(R("fbx_export_settings.json")))
LODS = [0] if "LOD0" in fname else [0, 1, 2, 3]

# ================================================================ pass 1: round-trip import
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBXP, use_custom_normals=True, use_image_search=False)
objs = list(bpy.data.objects)
rep("PASS", f"imported {len(objs)} objects into a clean scene ({sum(o.type == 'MESH' for o in objs)} meshes, {sum(o.type == 'EMPTY' for o in objs)} empties)")
dup = [o.name for o in objs if o.name[-4:-3] == "." and o.name[-3:].isdigit()]
rep("PASS" if not dup else "ERROR", f"no .001-style or duplicate names: {dup or 'ok'}")
bad = [o.name for o in objs if o.name.startswith(("Cut_", "Cam_", "Studio", "Light_", "QC_", "REFERENCE")) or o.type in ('CAMERA', 'LIGHT')]
master = [o.name for o in objs if o.type == 'MESH' and "_LOD" not in o.name and not o.name.startswith("Collision")]
rep("PASS" if not bad and not master else "ERROR", f"no master/studio/cutter leakage: {bad + master or 'clean'}")
cr = ob("Car_Root")
neg = [o.name for o in objs if any(s < 0 for s in o.scale)]
odd = [o.name for o in objs if any(abs(s - 1) > 1e-4 for s in o.scale)]
rep("PASS" if cr and not neg and not odd else "ERROR", f"scales: Car_Root {tuple(round(s, 4) for s in cr.scale)}, negative {neg or 'none'}, non-1 {odd[:5] or 'none'}")
rep("PASS" if (world(cr).translation.length < 1e-6) else "ERROR", f"Car_Root position {tuple(round(c, 5) for c in world(cr).translation)}")
for i in LODS:
    r = ob(f"LOD{i}_Root")
    rep("PASS" if r and r.parent == cr and (world(r).translation - world(cr).translation).length < 1e-6 else "ERROR",
        f"LOD{i}_Root under Car_Root, offset {(world(r).translation - world(cr).translation).length * 1000:.3f} mm")

# dimensions (world space of this Blender import, axis-converted back)
for i in LODS:
    meshes = [o for o in objs if o.type == 'MESH' and o.name.endswith(f"_LOD{i}")]
    pts = [world(o) @ v.co for o in meshes if not o.name.startswith("Mirror") for v in o.data.vertices]
    lo = Vector([min(p[k] for p in pts) for k in range(3)]); hi = Vector([max(p[k] for p in pts) for k in range(3)])
    L, W, H = hi.y - lo.y, hi.x - lo.x, hi.z
    ref = {0: (4.6950, 2.0523, 1.1726), 1: (4.6950, 2.0525, 1.1726), 2: (4.6950, 2.0528, 1.1741), 3: (4.6920, 2.0528, 1.1741)}[i]
    d = (L - ref[0], W - ref[1], H - ref[2])
    data[f"dims_LOD{i}"] = {"L": round(L, 5), "W": round(W, 5), "H": round(H, 5), "delta_mm": [round(x * 1000, 2) for x in d]}
    rep("PASS" if max(abs(x) for x in d) <= 0.002 else "ERROR", f"LOD{i} re-import dims L{L:.4f} W{W:.4f} H{H:.4f} m (delta mm {d[0]*1000:+.2f}/{d[1]*1000:+.2f}/{d[2]*1000:+.2f})")
    t = sum(tris(o) for o in meshes); dupr = {n: v for n, v in EXPSET["duplicate_triangles_removed"].items() if n.endswith(f"_LOD{i}")}
    want = sum(p7[f"LOD{i}"].values()) - sum(dupr.values())
    data[f"tris_LOD{i}"] = t
    rep("PASS" if t == want else "ERROR", f"LOD{i} triangles {t:,} (Phase 7 {want + sum(dupr.values()):,} - coincident duplicates removed at export {dupr or 0})")
    no_uv = [o.name for o in meshes if "UVMap" not in o.data.uv_layers]
    empt = [o.name for o in meshes if not o.data.materials or any(m is None for m in o.data.materials)]
    rep("PASS" if not no_uv else "ERROR", f"LOD{i} UVMap on {len(meshes) - len(no_uv)}/{len(meshes)} meshes {no_uv[:4] or ''}")
    rep("PASS" if not empt else "ERROR", f"LOD{i} material slots filled on all meshes {empt[:4] or ''}")
    mats = sorted({m.name for o in meshes for m in o.data.materials if m})
    data[f"materials_LOD{i}"] = mats
    lights = {"MAT_LED_White", "MAT_ProjectorLens", "MAT_LED_Red", "MAT_LED_Brake", "MAT_LED_Amber", "MAT_LED_Reverse"}
    rep("PASS" if lights <= set(mats) and {"LODMAT_Body_Paint", "LODMAT_Glass", "LODMAT_Tire", "MAT_BrakeCaliper"} <= set(mats) else "ERROR",
        f"LOD{i} {len(mats)} material groups survive; 6 light channels, paint, glass, tire, caliper distinct")

# wheels: pivots, axle, roll, steer
refs = {k: ob(f"WheelColliderRef_{k}") for k in ("FL", "FR", "RL", "RR")}
for k, r in refs.items():
    src = Vector(wref[k]["world_position"]); got = world(r).translation
    rep("PASS" if (got - src).length < 1e-3 else "ERROR", f"WheelColliderRef_{k} at {tuple(round(c, 4) for c in got)} (source delta {(got - src).length*1000:.3f} mm)")
wb = world(refs["RL"]).translation.y - world(refs["FL"]).translation.y
rep("PASS" if abs(wb - wref["_wheelbase_m"]) < 1e-3 else "ERROR", f"wheelbase {wb:.5f} m (delta {(wb - wref['_wheelbase_m'])*1000:+.3f} mm)")
for i in LODS:
    for k, r in refs.items():
        w = ob(f"Wheel_{k}_LOD{i}"); c = world(r).translation; off = (world(w).translation - c).length
        ax = world(w).to_3x3().col[0].normalized()
        kids = [o for o in (w, ob(f"Tire_{k}_LOD{i}"), ob(f"BrakeDisc_{k}_LOD{i}")) if o]
        cal = ob(f"Caliper_{k}_LOD{i}"); cb = wpts(cal); b0 = w.matrix_basis.copy(); worst = 0.0; calm = 0.0
        for a in (math.radians(30), math.radians(-30)):
            before = [(o, wpts(o)) for o in kids]
            w.matrix_basis = b0 @ Matrix.Rotation(a, 4, 'X')
            worst = max([worst, (world(w).translation - c).length] + [max((p - rot_about(q, c, ax, a)).length for p, q in zip(wpts(o), b)) for o, b in before])
            calm = max(calm, max((p - q).length for p, q in zip(wpts(cal), cb)))
            w.matrix_basis = b0
        rep("PASS" if off < 1e-3 and worst < 1e-4 and calm < 1e-6 and abs(abs(ax.x) - 1) < 1e-6 else "ERROR",
            f"Wheel_{k}_LOD{i}: pivot {off*1000:.3f} mm, roll +/-30 rigid (err {worst*1000:.4f} mm), tire+rotor follow, caliper static, axle along vehicle X")
    for k in ("FL", "FR"):
        sp = ob(f"SteerPivot_{k}_LOD{i}"); w = ob(f"Wheel_{k}_LOD{i}"); cal = ob(f"Caliper_{k}_LOD{i}")
        c = world(refs[k]).translation; up = Vector((0, 0, 1));   # world up; Unity-baked local yaw axis = +Y
        s0 = sp.matrix_basis.copy(); w0 = w.matrix_basis.copy()
        worst = 0.0; rollcal = 0.0
        for a in (math.radians(-25), 0.0, math.radians(25)):
            parts = [w, cal]; before = [(o, wpts(o)) for o in parts]
            sp.matrix_basis = s0 @ Matrix.Rotation(a, 4, 'Y')
            worst = max([worst, (world(w).translation - c).length] + [max((p - rot_about(q, c, up, a)).length for p, q in zip(wpts(o), b)) for o, b in before])
            cb2 = wpts(cal); w.matrix_basis = w0 @ Matrix.Rotation(math.radians(30), 4, 'X')
            rollcal = max(rollcal, max((p - q).length for p, q in zip(wpts(cal), cb2))); w.matrix_basis = w0
            sp.matrix_basis = s0
        rep("PASS" if worst < 1e-4 and rollcal < 1e-6 else "ERROR",
            f"SteerPivot_{k}_LOD{i}: -25/0/+25 deg yaw about wheel centre (err {worst*1000:.4f} mm), caliper steers but not rolls, roll works while steered")

for i in [l for l in LODS if l <= 2]:
    s = ob(f"SteeringWheel_LOD{i}"); M = world(s); c = M.translation.copy(); ax = M.to_3x3().col[1].normalized()   # shaft = local +Y after Unity axis bake
    src = piv["steering_wheel"][f"LOD{i}"]; b0 = s.matrix_basis.copy(); before = wpts(s, 80); worst = 0.0
    for a in (math.radians(30), math.radians(-30)):
        s.matrix_basis = b0 @ Matrix.Rotation(a, 4, 'Y')
        worst = max(worst, max((p - rot_about(q, c, ax, a)).length for p, q in zip(wpts(s, 80), before))); s.matrix_basis = b0
    oerr = (c - Vector(src["origin"])).length; aerr = math.degrees(ax.angle(Vector(src["axis"])))
    rep("PASS" if worst < 1e-4 and oerr < 1e-3 and aerr < 0.05 else "ERROR",
        f"SteeringWheel_LOD{i}: origin delta {oerr*1000:.3f} mm, shaft axis delta {aerr:.4f} deg, wobble {worst*1000:.4f} mm")

for i in [l for l in LODS if l <= 1]:
    for sd in ("L", "R"):
        d = ob(f"Door_{sd}_LOD{i}"); c = world(d).translation.copy(); src = Vector(piv["doors"][f"{sd}_LOD{i}"]["hinge_world"])
        kids = list(d.children); before = [(o, wpts(o)) for o in kids]; b0 = d.matrix_basis.copy(); ax = world(d).to_3x3().col[0].normalized()
        d.matrix_basis = b0 @ Matrix.Rotation(math.radians(18), 4, 'X')
        err = max(max((p - rot_about(q, c, ax, math.radians(18))).length for p, q in zip(wpts(o), b)) for o, b in before)
        d.matrix_basis = b0
        names = sorted(o.name for o in kids)
        rep("PASS" if err < 1e-4 and (c - src).length < 1e-3 and len(kids) == 3 else "ERROR",
            f"Door_{sd}_LOD{i}: hinge delta {(c - src).length*1000:.3f} mm, 18 deg open, {names} follow (err {err*1000:.4f} mm)")

for i in LODS:
    sp = ob(f"ActiveSpoiler_LOD{i}"); c = world(sp).translation.copy(); src = Vector(piv["spoiler"][f"LOD{i}"]["hinge_world"])
    ax = world(sp).to_3x3().col[0].normalized(); b0 = sp.matrix_basis.copy(); before = wpts(sp, 60)
    ang = math.radians(15)                                   # 3 -> 18 deg
    sp.matrix_basis = b0 @ Matrix.Rotation(ang, 4, 'X')
    err = max((p - rot_about(q, c, ax, ang)).length for p, q in zip(wpts(sp, 60), before)); rise = max(p.z for p in wpts(sp, 60)) - max(p.z for p in before)
    sp.matrix_basis = b0
    rep("PASS" if err < 1e-4 and (c - src).length < 1e-3 and rise > 0.02 else "ERROR",
        f"ActiveSpoiler_LOD{i}: hinge delta {(c - src).length*1000:.3f} mm, 3->18 deg rise {rise*100:.1f} cm, err {err*1000:.4f} mm")

# colliders
COLS = ["Collision_Front", "Collision_Body", "Collision_Side_L", "Collision_Side_R", "Collision_Cabin", "Collision_Rear"]
tot = 0
for n in COLS:
    o = ob(n); W = world(o); vs = [W @ v.co for v in o.data.vertices]; t = tris(o); tot += t
    viol = max((v - W @ p.center).dot((W.to_3x3() @ p.normal).normalized()) for p in o.data.polygons for v in vs)
    lo = [round(min(v[k] for v in vs), 3) for k in range(3)]; srclo = [round(x, 3) for x in cst[n]["bbox_min"]]
    pos = max(abs(a - b) for a, b in zip(lo, srclo))
    rep("PASS" if t == cst[n]["triangles"] and viol <= 1e-3 and pos <= 0.002 and o.parent == ob("Collision") else "ERROR",
        f"{n}: {t} tris, convex (viol {viol*1000:.3f} mm), normals outward, placement delta {pos*1000:.1f} mm")
rep("PASS" if tot == cst["_total_triangles"] else "ERROR", f"collider total {tot} triangles (source {cst['_total_triangles']})")
com = world(ob("CenterOfMass")).translation
rep("PASS" if (com - Vector((0, 0.12, 0.35))).length < 1e-3 else "ERROR", f"CenterOfMass physical position (Blender frame) {tuple(round(c, 4) for c in com)}")
data["CenterOfMass_blender"] = [round(c, 5) for c in com]

# normals: imported split normals vs source corner normals (nearest vertex), sample hero meshes
with bpy.data.libraries.load(SRC, link=False) as (src_d, dst_d):
    hero = ["Body_LOD0", "Body_Buttress_LOD0", "Mirror_L_LOD0", "Wheel_FL_LOD0", "Headlight_L_LOD0", "Tire_FL_LOD0"]
    dst_d.meshes = [n for n in hero if n in src_d.meshes]
srcmesh = {m.name.split(".")[0]: m for m in dst_d.meshes}
worst_flip = 0; angles = []
for n in hero:
    o = ob(n)
    if not o or n not in srcmesh: continue
    sm = srcmesh[n]; kd = KDTree(len(sm.vertices))
    for v in sm.vertices: kd.insert(v.co, v.index)
    kd.balance()
    vnorm = {}
    for li, l in enumerate(sm.loops): vnorm.setdefault(l.vertex_index, []).append(Vector(sm.corner_normals[li].vector))
    im = o.data; step = max(1, len(im.loops) // 3000)
    for li in range(0, len(im.loops), step):
        co = im.vertices[im.loops[li].vertex_index].co; nn = Vector(im.corner_normals[li].vector)
        _, idx, dist = kd.find(co)
        if dist < 1e-4:
            a = min(math.degrees(nn.angle(s, 0)) for s in vnorm[idx]); angles.append(a)
            if a > 90: worst_flip += 1
angles.sort()
p99 = angles[int(len(angles) * 0.99)] if angles else 0
data["normals_p99_deg"] = round(p99, 3)
rep("PASS" if worst_flip == 0 and p99 < 2.0 else "ERROR", f"shading normals vs source on hero meshes ({len(angles)} samples): 99th pct {p99:.3f} deg, flipped {worst_flip}")
cols = [o for o in objs if o.type == 'MESH' and o.name.startswith("Collision_")]
rep("PASS" if all("UVMap" in o.data.uv_layers for o in objs if o.type == 'MESH' and o not in cols) else "ERROR", "UVMap present on every imported render mesh")
rep("PASS" if all(not o.data.materials or all(m is None for m in o.data.materials) for o in cols) else "ERROR", f"{len(cols)} colliders: physics-only (no UVs / materials required)")

# ================================================================ pass 2: raw import = Unity's view of the file
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBXP, use_manual_orientation=True, axis_forward='Y', axis_up='Z', global_scale=1.0,
                         bake_space_transform=False, use_custom_normals=True, use_image_search=False)
cr = ob("Car_Root"); body = ob("Body_LOD0"); W = world(body)
pts = [W @ v.co for v in body.data.vertices]
zmin, zmax = min(p.z for p in pts), max(p.z for p in pts); ymax = max(p.y for p in pts); ymin = min(p.y for p in pts)
nose = max(pts, key=lambda p: p.z); seat = world(ob("Seat_Driver_LOD0")).translation
fl = world(ob("WheelColliderRef_FL")).translation; com = world(ob("CenterOfMass")).translation
q = cr.matrix_world.to_quaternion()
data["unity_raw"] = {"Car_Root_rotation_deg": [round(math.degrees(a), 4) for a in cr.matrix_world.to_euler()],
                     "Car_Root_scale": [round(s, 5) for s in cr.matrix_world.to_scale()],
                     "body_z_range(forward)": [round(zmin, 4), round(zmax, 4)], "body_y_max(up)": round(ymax, 4),
                     "driver_seat_fbx": [round(c, 4) for c in seat], "WheelColliderRef_FL_fbx": [round(c, 4) for c in fl],
                     "CenterOfMass_fbx": [round(c, 4) for c in com],
                     "CenterOfMass_unity(x negated by Unity's FBX importer)": [round(-com.x, 4), round(com.y, 4), round(com.z, 4)]}
rep("PASS" if q.angle < 1e-5 and max(abs(s - 1) for s in cr.matrix_world.to_scale()) < 1e-5 else "ERROR",
    f"Unity view: Car_Root rotation {data['unity_raw']['Car_Root_rotation_deg']} scale {data['unity_raw']['Car_Root_scale']} (no 90 deg / 100x)")
rep("PASS" if zmax > 2.3 and abs(zmin + 2.25) < 0.05 and ymax > 1.1 and min(p.y for p in pts) > 0.1 else "ERROR",
    f"Unity view: nose at +Z ({zmax:.3f}), tail {zmin:.3f}, roof +Y ({ymax:.3f}) -> car faces +Z, upright")
rep("PASS" if seat.x > 0 and fl.x > 0 and fl.z > 1.3 else "ERROR",
    f"Unity view: driver seat FBX x {seat.x:+.3f}, front-left wheel FBX ({fl.x:+.3f}, {fl.y:.3f}, {fl.z:+.3f}); Unity negates FBX x -> vehicle left = Unity -X, LHD driver on the left")
rep("PASS" if abs(com.x) < 1e-6 and abs(com.y - 0.35) < 1e-3 and abs(com.z + 0.12) < 1e-3 else "ERROR",
    f"Unity view: CenterOfMass FBX {data['unity_raw']['CenterOfMass_fbx']} -> Unity (0, 0.35, -0.12): low, 0.12 m behind mid-wheelbase")

Gb = Matrix.Rotation(-math.pi / 2, 3, 'X')                  # Blender -> FBX/Unity direction
ax_err = max([abs(abs(world(ob(f"Wheel_{k}_LOD0")).to_3x3().col[0].normalized().x) - 1) for k in ("FL", "FR", "RL", "RR")] +
             [(world(ob(f"SteerPivot_{k}_LOD0")).to_3x3().col[1].normalized() - Vector((0, 1, 0))).length for k in ("FL", "FR")] +
             [(world(ob("SteeringWheel_LOD0")).to_3x3().col[1].normalized() - Gb @ Vector(piv["steering_wheel"]["LOD0"]["axis"])).length])
rep("PASS" if ax_err < 1e-4 else "ERROR",
    f"Unity view local pivot axes: wheel roll = local X, steer yaw = local Y (= world up), steering shaft = local Y (max err {ax_err:.2e})")

errs = sum(l.startswith("[ERROR]") for l in out)
out.insert(0, f"== {fname} ({tag}) ==")
out.append(f"SUMMARY {fname}: {sum(l.startswith('[PASS]') for l in out)} PASS, {sum(l.startswith('[WARNING]') for l in out)} WARNING, {errs} ERROR")
open(R(f"fbx_validation_{tag}.txt"), "w").write("\n".join(out) + "\n")
json.dump(data, open(R(f"fbx_validation_{tag}.json"), "w"), indent=1)
print("\n".join(out))
