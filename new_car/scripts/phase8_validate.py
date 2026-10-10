# Phase 8 validation + pivot tests (rotations are temporary; the file is never saved).
import bpy, bmesh, os, json, math, hashlib
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda f: os.path.join(ROOT, "reports", f)
sc = bpy.context.scene; ID = Matrix.Identity(4)
out = []
def rep(lv, msg): out.append(f"[{lv}] {msg}")
def world(o): return (world(o.parent) @ o.matrix_parent_inverse if o.parent else ID) @ o.matrix_basis
def ob(n): return bpy.data.objects.get(n)
def wpts(o, n=40):
    vs = o.data.vertices; step = max(1, len(vs) // n); W = world(o)
    return [W @ vs[i].co for i in range(0, len(vs), step)]
def rot_about(p, c, axis, ang): return c + Matrix.Rotation(ang, 3, axis) @ (p - c)

# ---------------------------------------------------------------- roots
cr = ob("Car_Root")
rep("PASS" if cr and world(cr) == ID and cr.parent is None else "ERROR", f"Car_Root at origin, rotation 0, scale 1, top level")
for lod in range(4):
    r = ob(f"LOD{lod}_Root")
    rep("PASS" if r and r.parent == cr and world(r) == ID else "ERROR", f"LOD{lod}_Root under Car_Root with identity transform (LODs overlap exactly)")
col = bpy.data.collections.get("COLLIDERS"); croot = ob("Collision")
NEED = ["Collision_Front", "Collision_Body", "Collision_Side_L", "Collision_Side_R", "Collision_Cabin", "Collision_Rear"]
rep("PASS" if col and croot and croot.parent == cr and all(ob(n) and ob(n).parent == croot for n in NEED) else "ERROR",
    f"COLLIDERS collection + Collision root + {len(NEED)} pieces parented")
com = ob("CenterOfMass"); com_w = world(com).translation
rep("PASS" if com.parent == cr and abs(com_w.x) < 1e-6 and 0.30 <= com_w.z <= 0.40 and com_w.y > 0 else "ERROR",
    f"CenterOfMass at {tuple(round(c, 3) for c in com_w)} (centreline, rear-biased, low)")

# ---------------------------------------------------------------- wheel references
refs = {k: ob(f"WheelColliderRef_{k}") for k in ("FL", "FR", "RL", "RR")}
wheel_data = {}
for k, r in refs.items():
    rw = world(r).translation
    side_ok = (k[1] == "L") == (rw.x > 0)
    t = ob(f"Tire_{k}_LOD0"); tw = world(t); pts = [tw @ v.co for v in t.data.vertices]
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
    wheel_data[k] = {"world_position": [round(c, 5) for c in rw], "local_to_Car_Root": [round(c, 5) for c in (world(cr).inverted() @ rw)],
                     "radius_m": round((hi.z - lo.z) / 2, 4), "diameter_m": round(hi.z - lo.z, 4), "width_m": round(hi.x - lo.x, 4),
                     "axle_direction_world": [round(c, 4) for c in world(ob(f"Wheel_{k}_LOD0")).to_3x3().col[0]],
                     "side": "LEFT (+X)" if rw.x > 0 else "RIGHT (-X)"}
    rep("PASS" if side_ok and r.parent == cr else "ERROR", f"WheelColliderRef_{k} {wheel_data[k]['side']} at {wheel_data[k]['world_position']}, r={wheel_data[k]['radius_m']} w={wheel_data[k]['width_m']}")
wheel_data["_wheelbase_m"] = round(world(refs["RL"]).translation.y - world(refs["FL"]).translation.y, 5)
wheel_data["_track_m"] = {"front": round(world(refs["FL"]).translation.x - world(refs["FR"]).translation.x, 5),
                          "rear": round(world(refs["RL"]).translation.x - world(refs["RR"]).translation.x, 5)}
json.dump(wheel_data, open(R("wheel_reference_points.json"), "w"), indent=1)

# ---------------------------------------------------------------- pivot tests
piv = {"wheel_offsets_mm": {}, "roll": {}, "steer": {}, "steering_wheel": {}, "doors": {}, "spoiler": {}}
def max_err(objs_before, fn):
    e = 0.0
    for o, before in objs_before:
        after = [world(o) @ v for v in [world(o).inverted() @ p for p in before]] if False else wpts(o)
        e = max(e, max((a - fn(b)).length for a, b in zip(after, before)))
    return e
for lod in range(4):
    for k, r in refs.items():
        w = ob(f"Wheel_{k}_LOD{lod}"); c = world(r).translation
        off = (world(w).translation - c).length * 1000; piv["wheel_offsets_mm"][f"{k}_LOD{lod}"] = round(off, 4)
        ax = world(w).to_3x3().col[0].normalized()
        kids = [ob(n) for n in (f"Wheel_{k}_LOD{lod}", f"Tire_{k}_LOD{lod}", f"BrakeDisc_{k}_LOD{lod}") if ob(n)]
        cal = ob(f"Caliper_{k}_LOD{lod}"); cal_before = wpts(cal)
        worst = 0.0; b0 = w.matrix_basis.copy()
        for ang in (math.radians(30), math.radians(-30)):
            before = [(o, wpts(o)) for o in kids]
            w.matrix_basis = b0 @ Matrix.Rotation(ang, 4, 'X')
            worst = max(worst, max_err(before, lambda p: rot_about(p, c, ax, ang)), (world(w).translation - c).length)
            cal_move = max((a - b).length for a, b in zip(wpts(cal), cal_before))
            w.matrix_basis = b0
        piv["roll"][f"{k}_LOD{lod}"] = {"max_vertex_error_mm": round(worst * 1000, 5), "caliper_moved_mm": round(cal_move * 1000, 5)}
        ok = off < 0.5 and worst < 1e-5 and cal_move < 1e-6 and abs(ax.x) > 0.999999
        rep("PASS" if ok else "ERROR", f"Wheel_{k}_LOD{lod}: offset {off:.4f} mm, roll +/-30 deg rigid (err {worst*1000:.4f} mm), axle X, caliper static on roll")
    for k in ("FL", "FR"):
        sp = ob(f"SteerPivot_{k}_LOD{lod}"); w = ob(f"Wheel_{k}_LOD{lod}"); cal = ob(f"Caliper_{k}_LOD{lod}")
        c = world(refs[k]).translation; s0 = sp.matrix_basis.copy(); w0 = w.matrix_basis.copy(); worst = 0.0
        for ang in (math.radians(25), math.radians(-25)):
            parts = [w, cal] + [o for o in (ob(f"Tire_{k}_LOD{lod}"), ob(f"BrakeDisc_{k}_LOD{lod}")) if o]
            before = [(o, wpts(o)) for o in parts]
            sp.matrix_basis = s0 @ Matrix.Rotation(ang, 4, 'Z')
            worst = max(worst, max_err(before, lambda p: rot_about(p, c, Vector((0, 0, 1)), ang)), (world(w).translation - c).length)
            cb = wpts(cal); w.matrix_basis = w0 @ Matrix.Rotation(math.radians(30), 4, 'X')    # roll while steered
            roll_cal = max((a - b).length for a, b in zip(wpts(cal), cb)); centre = (world(w).translation - c).length
            w.matrix_basis = w0; sp.matrix_basis = s0
        piv["steer"][f"{k}_LOD{lod}"] = {"max_vertex_error_mm": round(worst * 1000, 5), "caliper_moves_on_roll_mm": round(roll_cal * 1000, 5),
                                         "centre_shift_mm": round(centre * 1000, 5), "parent_chain": f"{sp.name} > {w.name} (+ {cal.name})"}
        rep("PASS" if worst < 1e-5 and roll_cal < 1e-6 and centre < 1e-6 else "ERROR",
            f"SteerPivot_{k}_LOD{lod}: +/-25 deg yaw about wheel centre (err {worst*1000:.4f} mm); caliper steers, does not roll")

for lod in (0, 1, 2):
    s = ob(f"SteeringWheel_LOD{lod}")
    if not s: continue
    M = world(s); c = M.translation.copy(); ax = M.to_3x3().col[2].normalized(); b0 = s.matrix_basis.copy(); worst = 0.0
    before = wpts(s, 80)
    for ang in (math.radians(30), math.radians(-30)):
        s.matrix_basis = b0 @ Matrix.Rotation(ang, 4, 'Z')
        worst = max(worst, max((a - rot_about(b, c, ax, ang)).length for a, b in zip(wpts(s, 80), before)))
        s.matrix_basis = b0
    piv["steering_wheel"][f"LOD{lod}"] = {"origin": [round(x, 4) for x in c], "axis": [round(x, 4) for x in ax], "wobble_mm": round(worst * 1000, 5)}
    rep("PASS" if worst < 1e-5 else "ERROR", f"SteeringWheel_LOD{lod}: +/-30 deg about local Z (column axis {tuple(round(x, 2) for x in ax)}), wobble {worst*1000:.4f} mm")

for lod in (0, 1):
    for sd in ("L", "R"):
        d = ob(f"Door_{sd}_LOD{lod}"); c = world(d).translation.copy(); b0 = d.matrix_basis.copy()
        kids = [k for k in d.children]; before = [(o, wpts(o)) for o in kids]
        ang = math.radians(18); d.matrix_basis = b0 @ Matrix.Rotation(ang, 4, 'X')       # rear edge swings up (dihedral/scissor test)
        err = max_err(before, lambda p: rot_about(p, c, Vector((1, 0, 0)), ang))
        rise = max(world(o).translation.z for o in kids if o.type == 'MESH') if False else max(p.z for o in kids for p in wpts(o)) - max(p.z for _, b in before for p in b)
        d.matrix_basis = b0
        piv["doors"][f"{sd}_LOD{lod}"] = {"hinge_world": [round(x, 4) for x in c], "children": sorted(k.name for k in kids),
                                          "follow_error_mm": round(err * 1000, 5), "top_rise_m_at_18deg": round(rise, 4)}
        side_ok = (sd == "L") == (c.x > 0)
        rep("PASS" if err < 1e-5 and len(kids) == 3 and side_ok else "ERROR",
            f"Door_{sd}_LOD{lod} hinge {piv['doors'][f'{sd}_LOD{lod}']['hinge_world']}: 18 deg opening, {len(kids)} children follow rigidly")

for lod in range(4):
    sp = ob(f"ActiveSpoiler_LOD{lod}"); hg = ob(f"ActiveSpoilerHinge_LOD{lod}")
    c = world(sp).translation.copy(); ax = world(sp).to_3x3().col[0].normalized(); b0 = sp.matrix_basis.copy()
    cur = sp.rotation_euler.x; before = wpts(sp, 60); hb = wpts(hg) if hg else []
    ang = math.radians(18) - cur
    sp.rotation_euler.x = math.radians(18)
    err = max((a - rot_about(b, c, ax, ang)).length for a, b in zip(wpts(sp, 60), before))
    shift = (world(sp).translation - c).length; te = max(p.z for p in wpts(sp, 60)) - max(p.z for p in before)
    hg_move = max(((a - b).length for a, b in zip(wpts(hg), hb)), default=0) if hg else 0.0   # bracket dropped at LOD2/3
    sp.matrix_basis = b0
    piv["spoiler"][f"LOD{lod}"] = {"hinge_world": [round(x, 4) for x in c], "default_deg": round(math.degrees(cur), 2),
                                   "open_test_deg": 18, "error_mm": round(err * 1000, 5), "trailing_edge_rise_m": round(te, 4),
                                   "hinge_bracket_moved_mm": round(hg_move * 1000, 5)}
    rep("PASS" if err < 1e-5 and shift < 1e-9 and te > 0.02 and hg_move < 1e-6 else "ERROR",
        f"ActiveSpoiler_LOD{lod}: {math.degrees(cur):.0f} -> 18 deg about hinge, rise {te*100:.1f} cm, no translation, brackets static")
json.dump(piv, open(R("pivot_validation.json"), "w"), indent=1)

# ---------------------------------------------------------------- transforms, naming, duplicates
GA = bpy.data.collections["GAME_ASSET"]; prod = list(GA.all_objects)
neg = [o.name for o in prod if any(s < 0 for s in o.scale)]
nonu = [o.name for o in prod if max(o.scale) - min(o.scale) > 1e-6 or abs(o.scale[0] - 1) > 1e-6]
rotd = sorted(o.name for o in prod if o.rotation_euler.to_quaternion().angle > 1e-6)
rep("PASS" if not neg else "ERROR", f"negative scales: {neg or 'none'}")
rep("PASS" if not nonu else "WARNING", f"non-unit / non-uniform scales: {nonu or 'none'}")
rep("INFO", f"intentional rotations ({len(rotd)}): {rotd}")
dups = [o.name for o in bpy.data.objects if o.name[-4:-3] == "." and o.name[-3:].isdigit()]
rep("PASS" if not dups else "ERROR", f"duplicate-suffixed names: {dups or 'none'}")
bad = []
for o in prod:
    base = o.name.rsplit("_LOD", 1)[0]
    if base.startswith("Paddle_") or not (base.endswith(("_L", "_R"))): continue
    x = (sum((world(o) @ Vector(c) for c in o.bound_box), Vector()) / 8).x if o.type == 'MESH' else world(o).translation.x
    if (base[-1] == "L") != (x > 0): bad.append(o.name)
rep("PASS" if not bad else "ERROR", f"left(+X)/right(-X) naming across production objects: {bad or 'consistent'}")

# ---------------------------------------------------------------- colliders
body0 = ob("Body_LOD0"); bm = bmesh.new(); bm.from_mesh(body0.data); bm.transform(world(body0)); bt = BVHTree.FromBMesh(bm); bm.free()
cstats = json.load(open(R("collider_stats.json"))); tot = 0
for n in NEED:
    o = ob(n); me = o.data; W = world(o); vs = [W @ v.co for v in me.vertices]
    tris = sum(len(p.vertices) - 2 for p in me.polygons); tot += tris
    viol = max((v - W @ p.center).dot((W.to_3x3() @ p.normal).normalized()) for p in me.polygons for v in vs)
    convex = viol <= 1e-3                                  # 1 mm: float noise on near-coplanar hull triangles
    cstats[n]["max_convexity_violation_mm"] = round(viol * 1000, 4)
    b2 = bmesh.new(); b2.from_mesh(me); vol = b2.calc_volume(signed=True); manifold = all(e.is_manifold for e in b2.edges); b2.free()
    outside = []
    for v in vs:
        loc, nrm, _, _ = bt.find_nearest(v)
        if loc is not None and (v - loc).dot(nrm) > 0: outside.append((v - loc).length)
    mo = max(outside, default=0)
    cstats[n].update({"convex": convex, "closed_manifold": manifold, "outward_normals": vol > 0,
                      "verts_outside_LOD0_body": len(outside), "max_outside_mm": round(mo * 1000, 1)})
    rep("PASS" if convex and manifold and vol > 0 and tris <= 120 else "ERROR",
        f"{n}: {tris} tris, convex {convex}, closed {manifold}, normals outward {vol > 0}")
    rep("PASS" if mo <= 0.03 else "WARNING", f"{n} fit: {len(outside)}/{len(vs)} verts outside LOD0 skin, max {mo*1000:.1f} mm")
    if any(m and not m.name.startswith("QA_") for m in me.materials): rep("ERROR", f"{n} carries a production material")
cstats["_total_triangles"] = tot
json.dump(cstats, open(R("collider_stats.json"), "w"), indent=1)
rep("PASS" if 100 <= tot <= 600 else "WARNING", f"collider total {tot} triangles (target ~100-500)")

# ---------------------------------------------------------------- LOD geometry unchanged
p7 = json.load(open(R("phase_07_lod_counts.json")))
CAT = {"BODY": "Body", "WHEELS": "Wheels", "TIRES": "Tires", "BRAKES": "Brakes", "INTERIOR": "Interior", "GLASS": "Glass", "LIGHTS": "Lights", "TRIM": "Aero/Trim"}
for lod in range(4):
    objs = [o for o in bpy.data.collections[f"Car_LOD{lod}"].all_objects if o.type == 'MESH']
    t = sum(len(p.vertices) - 2 for o in objs for p in o.data.polygons)
    pts = [world(o) @ v.co for o in objs if not o.name.startswith("Mirror") for v in o.data.vertices]
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
    want = sum(p7[f"LOD{lod}"].values())
    rep("PASS" if t == want else "ERROR", f"LOD{lod}: {t:,} tris (phase 7: {want:,}); L{hi.y-lo.y:.4f} W{hi.x-lo.x:.4f} H{hi.z:.4f} m")
    no_uv = [o.name for o in objs if "UVMap" not in o.data.uv_layers]
    empty_slot = [o.name for o in objs if not o.data.materials or any(m is None for m in o.data.materials)]
    rep("PASS" if not no_uv and not empty_slot else "ERROR", f"LOD{lod} UVMap + material slots on all {len(objs)} meshes")
    mats = {m.name for o in objs for m in o.data.materials if m}
    L = {"MAT_LED_White", "MAT_ProjectorLens", "MAT_LED_Red", "MAT_LED_Brake", "MAT_LED_Amber", "MAT_LED_Reverse"}
    rep("PASS" if L <= mats else "ERROR", f"LOD{lod} independent light channels present: {len(L & mats)}/6; material groups {len(mats)}")
rep("PASS" if ob("Window_FL_LOD0").parent == ob("Door_L_LOD0") and ob("Window_FR_LOD0").parent == ob("Door_R_LOD0") else "ERROR",
    "side glass rides on the door hinges (LOD0/LOD1)")
miss = [i.filepath for i in bpy.data.images if i.source == 'FILE' and not os.path.exists(bpy.path.abspath(i.filepath))]
absp = [i.name for i in bpy.data.images if i.source == 'FILE' and not i.filepath.startswith("//")]
rep("PASS" if not miss and not absp else "ERROR", f"textures: missing {miss or 'none'}, absolute paths {absp or 'none'}")

# ---------------------------------------------------------------- production membership / master exclusion
under_root = set()
def walk(o):
    under_root.add(o.name)
    for c in o.children: walk(c)
walk(cr)
ga_names = {o.name for o in prod}
rep("PASS" if under_root <= ga_names else "ERROR", f"every object under Car_Root is in GAME_ASSET ({len(under_root)} objects)")
stray = sorted(ga_names - under_root)
rep("PASS" if not stray else "ERROR", f"GAME_ASSET objects outside Car_Root hierarchy: {stray or 'none'}")
refc = bpy.data.collections["REFERENCE_Master"]
leak = [o.name for o in refc.all_objects if o.name in under_root]
in_ga = refc.name in {c.name for c in GA.children_recursive}
rep("PASS" if not leak and not in_ga and refc.hide_render and bpy.context.view_layer.layer_collection.children["REFERENCE_Master"].exclude
    else "ERROR", f"REFERENCE_Master excluded (view layer + render), not in GAME_ASSET, no master object under Car_Root")
helpers = [o.name for o in prod if o.type in ('CAMERA', 'LIGHT') or o.name.startswith(("Cut_", "Cam_", "Studio", "QC_", "Light_"))]
rep("PASS" if not helpers else "ERROR", f"no studio/camera/cutter helpers in GAME_ASSET: {helpers or 'none'}")
want = open(R("lods_06.sha")).read().split()[0]
got = hashlib.sha1(open(os.path.join(ROOT, "hypercar_06_optimized_lods.blend"), "rb").read()).hexdigest()
rep("PASS" if want == got else "ERROR", f"checkpoint 06 unchanged (sha1 {got[:12]})")

# ---------------------------------------------------------------- export manifest
def role(o):
    n = o.name
    if n == "Car_Root": return "root"
    if n.endswith("_Root"): return "lod_root"
    if n.startswith("Collision"): return "collider" if o.type == 'MESH' else "collider_root"
    if n.startswith("WheelColliderRef_"): return "wheel_collider_reference"
    if n == "CenterOfMass": return "center_of_mass"
    if n.startswith("SteerPivot_"): return "steering_pivot"
    if n.startswith("Door_"): return "door_hinge_pivot"
    if n.startswith("ActiveSpoiler_"): return "spoiler (pivot = hinge)"
    if n.startswith("Wheel_"): return "wheel (rolls local X)"
    return o.get("atlas", o.type).lower()
man = {"root": "Car_Root", "forward": "-Y", "up": "+Z", "vehicle_left": "+X", "driver_side": "+X (LHD)",
       "objects": [{"name": o.name, "type": o.type, "parent": o.parent.name if o.parent else None, "role": role(o),
                    "lod": o.get("lod"), "collection": o.users_collection[0].name,
                    "materials": [m.name for m in o.data.materials] if o.type == 'MESH' else []} for o in sorted(prod, key=lambda o: o.name)],
       "exclude": ["REFERENCE_Master (REFERENCE_ONLY)", "HC_Studio / cameras / lights", "HC_Cutters*", "HC_QC_Reflection",
                   "HC_Daylight / HC_Night", "HC_Interior_QA"],
       "notes": ["Colliders carry QA_* debug materials only: strip renderers on import, keep MeshCollider(convex)",
                 "Normal maps are OpenGL (+Y) tangent space", "AO maps are in textures/hypercar/<atlas>/<ATLAS>_AO.png"]}
man["counts"] = {r_: sum(1 for x in man["objects"] if x["role"] == r_) for r_ in sorted({x["role"] for x in man["objects"]})}
json.dump(man, open(R("export_manifest.json"), "w"), indent=1)
rep("INFO", f"export manifest: {len(prod)} objects, roles {man['counts']}")

errs = sum(1 for l in out if l.startswith("[ERROR]")); warns = sum(1 for l in out if l.startswith("[WARNING]"))
out.append(f"SUMMARY: {sum(1 for l in out if l.startswith('[PASS]'))} PASS, {warns} WARNING, {errs} ERROR")
open(R("phase_08_validation.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
