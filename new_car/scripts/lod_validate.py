# Phase 7 validation: per-LOD triangle budgets, dimensions, pivots, UV/material/texture health, hierarchy, naming.
import bpy, bmesh, os, json, hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sc = bpy.context.scene
out, data = [], {}
def rep(level, msg): out.append(f"[{level}] {msg}")
CAT = {"BODY": "Body", "WHEELS": "Wheels", "TIRES": "Tires", "BRAKES": "Brakes", "INTERIOR": "Interior",
       "GLASS": "Glass", "LIGHTS": "Lights", "TRIM": "Aero/Trim"}
lc = bpy.context.view_layer.layer_collection.children["REFERENCE_Master"]
lc.exclude = False
dg = bpy.context.evaluated_depsgraph_get(); dg.update()

def tris_eval(o):
    e = o.evaluated_get(dg); m = e.to_mesh(); t = sum(len(p.vertices) - 2 for p in m.polygons); e.to_mesh_clear(); return t

def bounds(objs):
    lo = Vector((1e9,) * 3); hi = Vector((-1e9,) * 3)
    for o in objs:
        e = o.evaluated_get(dg); m = e.to_mesh()
        for v in m.vertices:
            p = e.matrix_world @ v.co; lo = Vector(map(min, lo, p)); hi = Vector(map(max, hi, p))
        e.to_mesh_clear()
    return lo, hi

def bvh(o):
    e = o.evaluated_get(dg); bm = bmesh.new(); bm.from_mesh(e.to_mesh()); bm.transform(o.matrix_world)
    t = BVHTree.FromBMesh(bm); bm.free(); e.to_mesh_clear(); return t

# master reference numbers
master = [o for o in bpy.data.collections["REFERENCE_Master"].all_objects
          if o.type == 'MESH' and o.get("atlas") not in (None, "CUTTER")]
mc = {c: 0 for c in CAT.values()}
for o in master: mc[CAT[o["atlas"]]] += tris_eval(o)
mlo, mhi = bounds([o for o in master if not o.name.startswith("Mirror")])
data["Master"] = mc
refs = {k: bpy.data.objects[f"WheelColliderRef_{k}"].matrix_world.translation.copy() for k in ("FL", "FR", "RL", "RR")}
LIGHTS = {"MAT_LED_White", "MAT_ProjectorLens", "MAT_LED_Red", "MAT_LED_Brake", "MAT_LED_Amber", "MAT_LED_Reverse"}
TARGET = {0: (180e3, 220e3), 1: (90e3, 120e3), 2: (40e3, 60e3), 3: (12e3, 20e3)}

for lod in range(4):
    col = bpy.data.collections[f"Car_LOD{lod}"]; root = bpy.data.objects[f"Car_LOD{lod}"]
    objs = [o for o in col.all_objects if o.type == 'MESH']
    cc = {c: 0 for c in CAT.values()}
    for o in objs: cc[CAT[o["atlas"]]] += tris_eval(o)
    tot = sum(cc.values()); data[f"LOD{lod}"] = cc
    a, b = TARGET[lod]
    rep("PASS" if a <= tot <= b else "WARNING", f"LOD{lod}: {tot:,} tris (target {int(a):,}-{int(b):,}), {100 * (1 - tot / sum(mc.values())):.1f}% below master")
    lo, hi = bounds([o for o in objs if not o.name.startswith("Mirror")])
    d = [(hi - lo)[i] - (mhi - mlo)[i] for i in range(3)]
    rep("PASS" if max(abs(x) for x in d) <= 0.010 else "ERROR",
        f"LOD{lod} dims L{hi.y - lo.y:.4f} W{hi.x - lo.x:.4f} H{hi.z:.4f} m (delta vs master mm: {d[1]*1000:+.1f}/{d[0]*1000:+.1f}/{d[2]*1000:+.1f})")
    for k, rp in refs.items():
        w = bpy.data.objects[f"Wheel_{k}_LOD{lod}"]
        off = (w.matrix_world.translation - rp).length
        rot = w.matrix_world.to_3x3().to_quaternion().angle
        rep("PASS" if off < 1e-5 and rot < 1e-6 else "ERROR", f"Wheel_{k}_LOD{lod} pivot offset {off*1000:.3f} mm, rotation {rot:.2e} rad (roll axis = local X)")
        for part in (f"Tire_{k}_LOD{lod}", f"BrakeDisc_{k}_LOD{lod}"):
            p = bpy.data.objects.get(part)
            if p and (p.parent != w or (p.matrix_world.translation - rp).length > 1e-5):
                rep("ERROR", f"{part} not riding on Wheel_{k}_LOD{lod} pivot")
    wb = (bpy.data.objects[f"Wheel_RL_LOD{lod}"].matrix_world.translation - bpy.data.objects[f"Wheel_FL_LOD{lod}"].matrix_world.translation).y
    rep("PASS" if abs(wb - 2.78) < 1e-4 else "ERROR", f"LOD{lod} wheelbase {wb:.4f} m")
    no_uv = [o.name for o in objs if "UVMap" not in o.data.uv_layers]
    empty = [o.name for o in objs if not o.data.materials or any(m is None for m in o.data.materials)]
    zero = sum(1 for o in objs for p in o.data.polygons if p.area < 1e-10)
    loose = sum(len(o.data.vertices) - len({v for p in o.data.polygons for v in p.vertices}) for o in objs)
    rep("PASS" if not no_uv else "ERROR", f"LOD{lod} UVMap on {len(objs) - len(no_uv)}/{len(objs)} meshes {no_uv[:3] or ''}")
    rep("PASS" if not empty else "ERROR", f"LOD{lod} empty material slots: {empty or 'none'}")
    rep("PASS" if zero == 0 else "WARNING", f"LOD{lod} zero-area faces: {zero}")
    rep("PASS" if loose == 0 else "WARNING", f"LOD{lod} loose vertices: {loose}")
    body = bpy.data.objects[f"Body_LOD{lod}"]
    me = body.data; ctr = sum((v.co for v in me.vertices), Vector()) / len(me.vertices)
    outward = sum(1 for p in me.polygons if p.normal.dot(p.center - ctr) > 0) / len(me.polygons)
    rep("PASS" if outward > 0.85 else "WARNING", f"Body_LOD{lod} normals outward: {outward * 100:.1f}% of faces")
    bm_ = bmesh.new(); bm_.from_mesh(me); nm = sum(1 for e in bm_.edges if not e.is_manifold and len(e.link_faces) != 1); bm_.free()
    rep("PASS" if nm == 0 else "WARNING", f"Body_LOD{lod} non-manifold (non-boundary) edges: {nm} (window openings are intentional boundaries)")
    bb = bvh(body)
    hits = [k for k in refs if len(bb.overlap(bvh(bpy.data.objects[f"Tire_{k}_LOD{lod}"]))) or len(bb.overlap(bvh(bpy.data.objects[f"Wheel_{k}_LOD{lod}"])))]
    rep("PASS" if not hits else "ERROR", f"LOD{lod} wheel/tire vs body intersections: {hits or 'none'}")
    def up_to_root(o):
        while o.parent and o.parent != root: o = o.parent
        return o.parent == root
    orphan = [o.name for o in col.all_objects if o != root and not up_to_root(o)]
    misplaced = [o.name for o in objs if not any(o.name in c.objects for c in col.children if c.name.endswith(CAT[o["atlas"]].replace("/", "_")))]
    rep("PASS" if not orphan and not misplaced else "ERROR", f"LOD{lod} hierarchy: orphans {orphan or 'none'}, wrong subcollection {misplaced or 'none'}")
    bad = []
    for o in col.all_objects:
        base = o.name.rsplit("_LOD", 1)[0]
        side = base[-1] if base[-2:-1] in ("_", "F", "R") and base[-1] in "LR" and not base.startswith("Paddle_") else None
        if side:
            x = (sum((o.matrix_world @ Vector(c) for c in o.bound_box), Vector()) / 8).x if o.type == 'MESH' else o.matrix_world.translation.x
            if (side == "L") != (x > 0): bad.append(o.name)
    rep("PASS" if not bad else "ERROR", f"LOD{lod} left(+X)/right(-X) naming: {bad or 'consistent'}")
    mats = sorted({m.name for o in objs for m in o.data.materials if m})
    keep = LIGHTS & set(mats)
    rep("PASS" if (lod == 3 or keep == LIGHTS) else "ERROR", f"LOD{lod} material groups: {len(mats)}; light channels separate: {sorted(keep)}")
    data[f"LOD{lod}_materials"] = mats

missing = [i.filepath for i in bpy.data.images if i.source == 'FILE' and not os.path.exists(bpy.path.abspath(i.filepath))]
rep("PASS" if not missing else "ERROR", f"texture links resolve: {len([i for i in bpy.data.images if i.source == 'FILE'])} images, missing {missing or 'none'}")
nm_bad = [m.name for m in bpy.data.materials if m.use_nodes for n in m.node_tree.nodes
          if n.type == 'NORMAL_MAP' and (n.space != 'TANGENT' or (n.inputs['Color'].links and n.inputs['Color'].links[0].from_node.image.colorspace_settings.name != 'Non-Color'))]
rep("PASS" if not nm_bad else "ERROR", f"normal maps tangent/OpenGL + Non-Color: {nm_bad or 'ok'}")
ref = bpy.data.collections["REFERENCE_Master"]
rep("PASS" if ref.hide_render else "ERROR", "REFERENCE_Master hidden from render (and excluded from view layer in the saved file)")
want = open(os.path.join(ROOT, "reports", "master_05a.sha")).read().split()[0]
got = hashlib.sha1(open(os.path.join(ROOT, "hypercar_05a_pre_lod_cleanup.blend"), "rb").read()).hexdigest()
rep("PASS" if want == got else "ERROR", f"master file unchanged (sha1 {got[:12]})")
lc.exclude = True
os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
open(os.path.join(ROOT, "reports", "phase_07_validation.txt"), "w").write("\n".join(out) + "\n")
json.dump(data, open(os.path.join(ROOT, "reports", "phase_07_lod_counts.json"), "w"), indent=1)
print("\n".join(out))
