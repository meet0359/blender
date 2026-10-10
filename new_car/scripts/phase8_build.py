# Phase 8: colliders + final hierarchy + pivots. Opens hypercar_06_optimized_lods.blend, saves hypercar_07_colliders_hierarchy.blend.
# Render geometry is never edited; only empties/parenting/collections are added and colliders created.
import bpy, bmesh, os, json, math
from mathutils import Vector, Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hypercar_07_colliders_hierarchy.blend")
sc = bpy.context.scene
car_root = bpy.data.objects["Car_Root"]
ID = Matrix.Identity(4)

def world(o):
    """World matrix from the parent chain (exact; avoids depsgraph updates, no constraints in this rig)."""
    return (world(o.parent) @ o.matrix_parent_inverse if o.parent else ID) @ o.matrix_basis

def reparent(child, parent):
    """Re-parent keeping the world transform exactly."""
    mw = world(child)
    child.parent = parent; child.matrix_parent_inverse = world(parent).inverted() if parent else ID.copy()
    child.matrix_basis = child.matrix_parent_inverse.inverted() @ (world(parent).inverted() if parent else ID) @ mw

def empty(name, loc, col, parent, kind='PLAIN_AXES', size=0.15):
    o = bpy.data.objects.new(name, None); o.empty_display_type = kind; o.empty_display_size = size
    col.objects.link(o); o.location = loc
    if parent: reparent(o, parent)
    return o

# ---------------------------------------------------------------- 1. master isolation: nothing of REFERENCE_Master hangs off Car_Root
lc_ref = bpy.context.view_layer.layer_collection.children["REFERENCE_Master"]
lc_ref.exclude = False                                   # read master objects while re-parenting
_cut = bpy.data.objects["Body_Shell"].modifiers["Cutters"]; _cut_vis = _cut.show_viewport
_cut.show_viewport = False                               # park the 27 s Exact boolean (restored before saving)
ref = bpy.data.collections["REFERENCE_Master"]
ref_root = empty("REFERENCE_Master_Root", (0, 0, 0), ref, None, 'ARROWS', 0.4)
for o in ref.all_objects:
    if o.parent == car_root:
        reparent(o, ref_root)
ref["role"] = "REFERENCE_ONLY - never export"; ref.color_tag = 'COLOR_01'

# ---------------------------------------------------------------- 2. LOD roots + front steering pivots
for lod in range(4):
    r = bpy.data.objects[f"Car_LOD{lod}"]; r.name = f"LOD{lod}_Root"; r.empty_display_type = 'ARROWS'
    col = bpy.data.collections[f"Car_LOD{lod}"]
    for k in ("FL", "FR"):
        w = bpy.data.objects[f"Wheel_{k}_LOD{lod}"]
        sp = empty(f"SteerPivot_{k}_LOD{lod}", w.matrix_world.translation.copy(), bpy.data.collections[f"LOD{lod}_Wheels"],
                   r, 'CIRCLE', 0.42)
        sp.rotation_euler = (0, 0, 0)
        reparent(w, sp)                                  # wheel rolls (local X) under the yawing steer pivot
        reparent(bpy.data.objects[f"Caliper_{k}_LOD{lod}"], sp)   # caliper steers, never rolls

# ---------------------------------------------------------------- 3. colliders (compound convex pieces, low poly)
COL = bpy.data.collections.new("COLLIDERS"); sc.collection.children.link(COL)
coll_root = empty("Collision", (0, 0, 0), COL, car_root, 'CUBE', 0.25)
bpy.context.view_layer.update()
body = bpy.data.objects["Body_LOD2"]                      # simplified body surface as the fitting reference
bpts = [body.matrix_world @ v.co for v in body.data.vertices]
X1 = max(p.x for p in bpts)
PIECES = {   # name: (point filter, target max tris, debug colour)
    "Collision_Front":  (lambda p: p.y < -0.80,                                     90, (0.95, 0.35, 0.10)),
    "Collision_Body":   (lambda p: -0.80 <= p.y <= 0.62 and abs(p.x) <= 0.66 and p.z <= 0.80, 60, (0.20, 0.60, 0.95)),
    "Collision_Side_L": (lambda p: -0.95 <= p.y <= 1.00 and p.x >= 0.45 and p.z <= 0.82,  70, (0.20, 0.85, 0.35)),
    "Collision_Side_R": (lambda p: -0.95 <= p.y <= 1.00 and p.x <= -0.45 and p.z <= 0.82, 70, (0.85, 0.85, 0.20)),
    "Collision_Cabin":  (lambda p: -0.75 <= p.y <= 0.62 and p.z >= 0.76,                 60, (0.70, 0.30, 0.90)),
    "Collision_Rear":   (lambda p: p.y > 0.62,                                          90, (0.95, 0.20, 0.45)),
}
INSET = 0.015
def hull_tris(pts):
    bm = bmesh.new(); vs = [bm.verts.new(p) for p in pts]
    res = bmesh.ops.convex_hull(bm, input=vs)
    bmesh.ops.delete(bm, geom=list(set(res["geom_interior"] + res["geom_unused"])), context='VERTS')
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges[:])
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    ctr = sum((v.co for v in bm.verts), Vector()) / len(bm.verts)   # centroid is inside a convex hull:
    for f in bm.faces:                                                 # every normal must point away from it
        if f.normal.dot(f.calc_center_median() - ctr) < 0:
            f.normal_flip()
    bm.normal_update()
    return bm

def representative(pts, cell):
    """One surface point per grid cell (the one farthest from the centroid): fewer hull verts, still on the body."""
    c = sum(pts, Vector()) / len(pts); best = {}
    for p in pts:
        key = (round(p.x / cell), round(p.y / cell), round(p.z / cell))
        if key not in best or (p - c).length > (best[key] - c).length:
            best[key] = p
    return list(best.values()), c

import random
def violation(bm):
    return max(((v.co - f.calc_center_median()).dot(f.normal) for f in bm.faces for v in bm.verts), default=1.0)

stats = {}
for name, (flt, target, colr) in PIECES.items():
    pts = [p for p in bpts if flt(p)]
    cell = 0.04; rng = random.Random(1); tries = 0
    while True:
        rep, c = representative(pts, cell)
        inset = [c + (p - c) * max(0.0, ((p - c).length - INSET) / (p - c).length) for p in rep]
        if tries:   # break exact coplanarity that trips bmesh.convex_hull (0.1 mm jitter)
            inset = [p + Vector([rng.uniform(-1e-4, 1e-4) for _ in range(3)]) for p in inset]
        bm = hull_tris(inset)
        ok_convex = violation(bm) <= 1e-3
        if (len(bm.faces) <= target and ok_convex) or cell > 0.6 or tries > 40:
            break
        bm.free(); tries += 1
        if len(bm.faces) > target if False else True: cell *= 1.08
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    m = bpy.data.materials.new(f"QA_{name}"); m.diffuse_color = (*colr, 0.55); m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]; bsdf.inputs["Base Color"].default_value = (*colr, 1)
    bsdf.inputs["Alpha"].default_value = 0.55; m["debug_only"] = True
    me.materials.append(m)
    o = bpy.data.objects.new(name, me); COL.objects.link(o); reparent(o, coll_root)
    o.display_type = 'SOLID'; o.color = (*colr, 0.55); o.hide_render = True; o["collider"] = "convex"
    stats[name] = {"triangles": len(me.polygons), "vertices": len(me.vertices), "grid_cell_m": round(cell, 3),
                   "bbox_min": [round(min(v.co[i] for v in me.vertices), 4) for i in range(3)],
                   "bbox_max": [round(max(v.co[i] for v in me.vertices), 4) for i in range(3)]}
stats["_total_triangles"] = sum(v["triangles"] for k, v in stats.items() if not k.startswith("_"))
stats["_method"] = "convex hull of representative Body_LOD2 surface points per region, 15 mm inset, re-hulled (convex by construction)"
json.dump(stats, open(os.path.join(ROOT, "reports", "collider_stats.json"), "w"), indent=1)
print("COLLIDERS", {k: v["triangles"] for k, v in stats.items() if not k.startswith("_")}, stats["_total_triangles"])

# ---------------------------------------------------------------- 4. production collection (links only, no duplicated geometry)
GA = bpy.data.collections.new("GAME_ASSET"); sc.collection.children.link(GA)
GA.children.link(bpy.data.collections["HC_Rig"])
for lod in range(4):
    GA.children.link(bpy.data.collections[f"Car_LOD{lod}"])
GA.children.link(COL)
GA["role"] = "export selection: everything below Car_Root in these collections"
for n in ("HC_Cutters_LOD2", "HC_Cutters_LOD3"):
    sc.collection.children[n]["role"] = "build helper, not exported"

_cut.show_viewport = _cut_vis
lc_ref.exclude = True
bpy.data.collections["REFERENCE_Master"].hide_render = True
sc["phase8"] = "phase8_build.py from hypercar_06_optimized_lods.blend"
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT)
