# Pre-Phase-7 cleanup on hypercar_05_materials_uv.blend -> hypercar_05a_pre_lod_cleanup.blend
# 1) side names from world X (forward -Y, up +Z: vehicle LEFT = +X)  2) windshield seal relief
import bpy, re, os, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hypercar_05a_pre_lod_cleanup.blend")
PAT = re.compile(r"^(.*_)([FR]?)([LR])$")

def world_x(o):
    if o.type == 'MESH' and len(o.data.vertices):
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        return sum(p.x for p in bb) / 8
    return o.matrix_world.translation.x

plan = []
for o in bpy.data.objects:
    m = PAT.match(o.name)
    if not m or o.name.startswith("Paddle_"):       # paddles = driver's hands (documented), already +X = left
        continue
    x = world_x(o)
    if abs(x) < 0.02:
        continue
    want = "L" if x > 0 else "R"
    if m.group(3) != want:
        plan.append((o, m.group(1) + m.group(2) + want))
for o, _ in plan:                                    # two-phase rename: no name collisions
    o.name = o.name + "__tmp"
renames = []
for o, new in plan:
    old = o.name[:-5]; o.name = new
    if o.data is not None and hasattr(o.data, "name") and o.data.users == 1:
        o.data.name = new
    renames.append((old, new))
assert all(o.name == n for o, n in plan), "rename collision"

exec(open(os.path.join(ROOT, "scripts", "seal_relief.py")).read())
add_seal_relief(bpy.data.node_groups["HC_DeleteGlassFaces"])

dg = bpy.context.evaluated_depsgraph_get(); dg.update()
def tree(n):
    o = bpy.data.objects[n]; return BVHTree.FromObject(o, dg), o
B, body = tree("Body_Shell"); W, ws = tree("Windshield")
ov = len(W.overlap(B))
gap = []
for sx in (1, -1):
    c = Vector((sx * 0.5203, -0.6741, 0.8030))
    gap.append(round(W.find_nearest(B.find_nearest(c)[0])[3] * 1000, 2))
paddles = {n: round(bpy.data.objects[n].matrix_world.translation.x, 3) for n in ("Paddle_L", "Paddle_R")}
json.dump({"renames": renames, "windshield_overlap_faces": ov, "corner_clearance_mm_+X_-X": gap, "paddles_x": paddles},
          open(os.path.join(ROOT, "reports", "cleanup_05a.json"), "w"), indent=1)
print("RENAMES", len(renames)); print("OVERLAP", ov, "CLEARANCE_MM", gap, "PADDLES", paddles)
bpy.ops.wm.save_as_mainfile(filepath=OUT, copy=False)
print("SAVED", OUT)
