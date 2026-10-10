# Hypercar (frozen flagship): reference scripts

These are reference implementations from the hypercar pipeline (Blender 5.2, run headless). Reuse the patterns: LOD build, colliders + hierarchy + pivots, axis-baked FBX export, and independent FBX re-import validation. Copy and adapt the code; never import or edit these files.


---

## `new_car/scripts/phase8_build.py`

_Phase 8: colliders, Car_Root / LODn_Root hierarchy, wheel + steer pivots, WheelColliderRef_*, CenterOfMass_

```python
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
```

---

## `new_car/scripts/export_fbx.py`

_Phase 9: Unity FBX export with explicit in-memory axis bake (G = Rot(-90, X)), manifest, never saves the source_

```python
# Phase 9: Unity FBX export. Opens hypercar_07_colliders_hierarchy.blend (never saved), writes
# exports/hypercar_LOD0_unity_test.fbx + exports/hypercar_complete_unity.fbx, saves hypercar_08_unity_export.blend.
import bpy, bmesh, os, json, hashlib
from mathutils import Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "exports"); os.makedirs(EXP, exist_ok=True)
CKPT = os.path.join(ROOT, "hypercar_08_unity_export.blend")
sc = bpy.context.scene

# Unity preset (documented in reports/unity_import_notes.md)
FBX = dict(use_selection=True, object_types={'MESH', 'EMPTY'}, use_active_collection=False,
           global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
           axis_forward='-Z', axis_up='Y', bake_space_transform=False,      # Blender -Y fwd -> FBX/Unity +Z, +Z up -> +Y
           # (exporter's experimental Apply Transform mis-handles >1-level hierarchies; the axis bake is done
           #  explicitly below on the export session instead)
           use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='FACE',
           use_subsurf=False, use_mesh_edges=False, use_tspace=True, use_triangles=False,
           use_custom_props=False, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X',
           use_armature_deform_only=False, bake_anim=False, path_mode='RELATIVE', embed_textures=False,
           batch_mode='OFF', axis_forward_note=None)
FBX.pop("axis_forward_note")

def subtree(o, acc):
    acc.append(o)
    for c in o.children:
        subtree(c, acc)
    return acc

cr = bpy.data.objects["Car_Root"]
rig = [bpy.data.objects[n] for n in ("WheelColliderRef_FL", "WheelColliderRef_FR", "WheelColliderRef_RL",
                                      "WheelColliderRef_RR", "CenterOfMass")]
coll = subtree(bpy.data.objects["Collision"], [])
lods = {i: subtree(bpy.data.objects[f"LOD{i}_Root"], []) for i in range(4)}
sets = {"hypercar_LOD0_unity_test.fbx": [cr] + rig + coll + lods[0],
        "hypercar_complete_unity.fbx": [cr] + rig + coll + sum(lods.values(), [])}

sc["phase9_export_prep"] = "export-time only (in memory, not saved): 5+-gon triangulation for tangents + axis bake"
bpy.ops.wm.save_as_mainfile(filepath=CKPT)                       # checkpoint = production scene, pre-axis-bake
print("SAVED", CKPT)

# ---- explicit axis bake for the export session (never saved): world'(o) = world(o) @ G^-1, mesh data' = G v.
# Exporter then writes root = G @ G^-1 = identity, children = G L G^-1, geometry in Unity/FBX axes.
G = Matrix.Rotation(-1.5707963267948966, 4, 'X')          # Blender (fwd -Y, up +Z) -> FBX (fwd +Z, up +Y)
Gi = G.inverted()
export_objs = sets["hypercar_complete_unity.fbx"]
I4 = Matrix.Identity(4)
def world(o): return (world(o.parent) @ o.matrix_parent_inverse if o.parent else I4) @ o.matrix_basis
W = {o.name: world(o) for o in export_objs}
for o in export_objs:
    wn = W[o.name] @ Gi
    pw = (W[o.parent.name] @ Gi) if o.parent else I4
    o.matrix_parent_inverse = I4.copy()
    o.matrix_basis = pw.inverted() @ wn
# tangents need tris/quads: triangulate 5+-gons with bmesh (the Triangulate modifier drops duplicate tris and
# would change triangle counts); each mesh datablock once, even if shared
# Coincident duplicate faces (same vertex set) are removed: importers collapse them and in Unity they z-fight.
tri_mod = []; dup_removed = {}
for me in {o.data for o in export_objs if o.type == 'MESH'}:
    want = sum(len(p.vertices) - 2 for p in me.polygons)
    bm = bmesh.new(); bm.from_mesh(me)
    if any(len(f.verts) > 4 for f in bm.faces):
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4], quad_method='BEAUTY', ngon_method='BEAUTY')
        tri_mod.append(me.name)
    seen, dups = set(), []
    for f in bm.faces:
        k = frozenset(v.index for v in f.verts)
        (dups.append(f) if k in seen else seen.add(k))
    lost = sum(len(f.verts) - 2 for f in dups)
    if dups:
        bmesh.ops.delete(bm, geom=dups, context='FACES_ONLY')
        for o in export_objs:
            if o.data == me: dup_removed[o.name] = lost
    bm.to_mesh(me); bm.free()
    me.transform(G); me.update()
    assert sum(len(p.vertices) - 2 for p in me.polygons) == want - lost, me.name
print("DUPLICATE TRIS REMOVED", dup_removed)
for o in export_objs:                                   # colliders: physics only, drop Phase 8 QA viewport materials
    if o.type == 'MESH' and o.name.startswith("Collision_"):
        o.data.materials.clear()
err = max((W[o.name] - (world(o) @ G)).length_squared if False else max(abs(a - b) for ra, rb in zip(W[o.name], world(o) @ G) for a, b in zip(ra, rb)) for o in export_objs)
print("AXIS BAKE max matrix residual", err)
assert err < 1e-6

ref_lc = bpy.context.view_layer.layer_collection.children["REFERENCE_Master"]
assert ref_lc.exclude, "reference master must stay excluded"
out = {}
for fname, objs in sets.items():
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.hide_set(False); o.hide_select = False; o.select_set(True)
    bpy.context.view_layer.objects.active = cr
    path = os.path.join(EXP, fname)
    bpy.ops.export_scene.fbx(filepath=path, **FBX)
    leaked = [o.name for o in bpy.context.selected_objects if o not in objs]
    out[fname] = {"objects": len(objs), "bytes": os.path.getsize(path), "leaked_selection": leaked,
                  "sha1": hashlib.sha1(open(path, "rb").read()).hexdigest()}
    print("EXPORTED", fname, out[fname], flush=True)

settings = {k: (sorted(v) if isinstance(v, set) else v) for k, v in FBX.items()}
json.dump({"settings": settings, "files": out, "export_time_ngon_triangulated_meshes": sorted(tri_mod),
           "duplicate_triangles_removed": dup_removed},
          open(os.path.join(ROOT, "reports", "fbx_export_settings.json"), "w"), indent=1)
print("ngon-triangulated objects:", len(tri_mod))
```

---

## `new_car/scripts/fbx_validate.py`

_Phase 9: re-import each FBX into a clean scene and validate (names, hierarchy, tris, bounds, pivots, Unity-space coordinates)_

```python
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
```

---

## `new_car/scripts/lod_build.py`

_Phase 7: per-component LOD0-3 generation from the master (reduced modifier settings + collapse decimate)_

```python
# Phase 7: build Car_LOD0..3 from the master (hypercar_05a_pre_lod_cleanup.blend), component by component.
# Each LOD mesh = the master object evaluated with reduced settings (subdiv levels, bevel segments, cutter set,
# glass thickness) -> static mesh, then an optional per-component collapse decimate. Origins/pivots/UVs carry over.
# Saves hypercar_06_optimized_lods.blend; the master file is only read.
import bpy, bmesh, os, json, math
from mathutils import Matrix, Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hypercar_06_optimized_lods.blend")
TEX = os.path.join(ROOT, "textures", "hypercar")
sc = bpy.context.scene
LODS = range(4)
CAT = {"BODY": "Body", "WHEELS": "Wheels", "TIRES": "Tires", "BRAKES": "Brakes", "INTERIOR": "Interior",
       "GLASS": "Glass", "LIGHTS": "Lights", "TRIM": "Aero_Trim"}
MASTER = [o for o in bpy.data.collections["HC_Hypercar"].all_objects
          if o.type == 'MESH' and not o.name.startswith("Cut_") and o.get("atlas") not in (None, "CUTTER")]

# ---------------------------------------------------------------- cutter subsets for distant body LODs
def cut_subset(name, exclude):
    c = bpy.data.collections.new(name); sc.collection.children.link(c)
    for o in bpy.data.collections["HC_Cutters"].objects:
        if not o.name.startswith(exclude):
            c.objects.link(o)
    c.hide_render = True; bpy.context.view_layer.layer_collection.children[name].hide_viewport = False
    return c
CUT2 = cut_subset("HC_Cutters_LOD2", ("Cut_Gap_", "Cut_DoorHandle_", "Cut_MirrorPad_"))
CUT3 = cut_subset("HC_Cutters_LOD3", ("Cut_Gap_", "Cut_DoorHandle_", "Cut_MirrorPad_", "Cut_EngineVent_"))

# ---------------------------------------------------------------- per-component plan
SMALL_INT = ("Pedal_", "Paddle_", "SteeringColumn", "RearViewMirror")
LOD3_INT_KEEP = {"Dashboard", "Seat_Driver", "Seat_Passenger", "SteeringWheel", "Interior_Tub", "CenterTunnel"}
SMALL_TRIM_LOD3 = ("EngineVents", "FrontIntakeVanes", "RearVent_", "RearFascia_Trim", "SideIntakeVane_",
                   "ActiveSpoilerHinge", "Exhaust_", "Chassis_EngineBay")
def plan(o, lod):
    """-> dict(sub=subsurf level or None, r=decimate ratio, drop, solid, bevel, holes)"""
    n, a = o.name, o["atlas"]
    p = dict(sub=None, r=1.0, drop=False, solid=True, bevel=None, holes=True)
    pick = lambda seq: seq[lod]
    if n == "Body_Shell":            p.update(sub=pick([1, 1, 0, 0]), r=pick([1, .55, 1, .45]))
    elif n == "Body_Buttress":       p.update(sub=pick([1, 0, 0, 0]), r=pick([1, 1, .6, .3]))
    elif n.startswith("Mirror_"):    p.update(sub=pick([1, 0, 0, 0]), r=pick([1, 1, .5, .2]))
    elif n.startswith("ArchLip_"):   p.update(r=pick([.4, .2, .1, 1]), drop=lod == 3)
    elif n.startswith("DoorHandle_"): p.update(drop=lod >= 2)
    elif n.startswith("Tire_"):      p.update(sub=0, r=pick([1, .55, .3, .1]))
    elif n.startswith("Rim_"):       p.update(r=pick([1, .55, .35, .12]))
    elif n.startswith("BrakeDisc_"): p.update(r=pick([.75, .5, .25, .08]), holes=lod == 0)
    elif n.startswith("Caliper_"):   p.update(bevel=pick([2, 1, 0, 0]), r=pick([1, .6, .35, .15]))
    elif a == "GLASS":
        if n.startswith("MirrorGlass"): p.update(drop=lod == 3)
        else: p.update(solid=lod < 2, r=pick([.5, .3, .25, .06]))
    elif a == "LIGHTS":
        if "Lens" in n: p.update(r=pick([1, .6, .4, 1]), drop=lod == 3)
        else: p.update(r=pick([1, .55, .3, .12]))
    elif a == "INTERIOR":
        if n.startswith("Seat_"):      p.update(sub=pick([1, 0, 0, 0]), r=pick([.5, 1, .45, .08]))
        elif n == "Dashboard":         p.update(sub=pick([1, 0, 0, 0]), r=pick([1, 1, .6, .5]))
        elif n == "SteeringWheel":     p.update(r=pick([1, .5, .25, .1]))
        elif n.startswith(SMALL_INT):  p.update(drop=lod >= 2)
        else: p.update(r=pick([{"Dashboard_Vents": .6, "EngineBay_Detail": .5, "PillarTrim": .6}.get(n, 1), .5, .2, .3]))
        if lod == 3 and n not in LOD3_INT_KEEP:
            p["drop"] = True
    elif a == "TRIM":
        p.update(r=pick([.9, .55, .3, .12]))
        if n.startswith("ActiveSpoilerHinge") and lod >= 2: p["drop"] = True
        if lod == 3 and n.startswith(SMALL_TRIM_LOD3): p["drop"] = True
    return p

# ---------------------------------------------------------------- evaluation helpers
def eval_mesh(o, p, lod):
    saved = []
    def setv(obj, attr, val):
        saved.append((obj, attr, getattr(obj, attr))); setattr(obj, attr, val)
    for md in o.modifiers:
        if md.type == 'SUBSURF' and p["sub"] is not None:
            setv(md, "levels", p["sub"])
        if md.type == 'BEVEL' and p["bevel"] is not None:
            if p["bevel"] == 0: setv(md, "show_viewport", False)
            else: setv(md, "segments", p["bevel"])
        if md.type == 'SOLIDIFY' and o["atlas"] == "GLASS" and not p["solid"]:
            setv(md, "show_viewport", False)
        if md.type == 'BOOLEAN' and lod >= 2:
            setv(md, "collection", CUT2 if lod == 2 else CUT3)
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    me = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    for obj, attr, val in reversed(saved):
        setattr(obj, attr, val)
    return me

def strip_holes(me):
    bm = bmesh.new(); bm.from_mesh(me)
    idx = [i for i, m in enumerate(me.materials) if m and m.name == "MAT_BlackTrim"]
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in idx], context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(me); bm.free()

def decimate(me, ratio, sym):
    if ratio >= 0.999 or len(me.polygons) < 40:
        return me
    tmp = bpy.data.objects.new("tmp_dec", me); sc.collection.objects.link(tmp)
    d = tmp.modifiers.new("Dec", 'DECIMATE'); d.decimate_type = 'COLLAPSE'; d.ratio = ratio
    d.use_symmetry = sym; d.symmetry_axis = 'X'
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    out = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    bpy.data.objects.remove(tmp)
    if me.users == 0: bpy.data.meshes.remove(me)
    return out

def clean(me):
    """Remove boolean slivers / decimation leftovers: degenerate faces+edges, edges with 3+ faces, loose verts."""
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-6, edges=bm.edges[:])
    for _ in range(8):                                   # edges with 3+ faces: drop the sliver face, repeat
        bad = [e for e in bm.edges if len(e.link_faces) > 2]
        if not bad: break
        bmesh.ops.delete(bm, geom=list({min(e.link_faces, key=lambda f: f.calc_area()) for e in bad}), context='FACES')
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_area() < 1e-10], context='FACES')
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context='EDGES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(me); bm.free()

def tris(me):
    return sum(len(p.vertices) - 2 for p in me.polygons)

# ---------------------------------------------------------------- LOD materials (atlas texture sets + kept channels)
def img(atlas, ch):
    sub = {"BODY": "body", "INTERIOR": "interior", "WHEELS": "wheels", "TIRES": "tires", "LIGHTS": "lights",
           "BRAKES": "brakes", "GLASS": "glass", "TRIM": "trim"}[atlas]
    im = bpy.data.images.load(os.path.join(TEX, sub, f"{atlas}_{ch}.png"), check_existing=True)
    if ch != "BaseColor": im.colorspace_settings.name = 'Non-Color'
    return im

def atlas_mat(name, atlas, coat=0.0, glass=False):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    def tex(ch):
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = img(atlas, ch); return t
    nt.links.new(tex("BaseColor").outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex("Roughness").outputs["Color"], b.inputs["Roughness"])
    nt.links.new(tex("Metallic").outputs["Color"], b.inputs["Metallic"])
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.space = 'TANGENT'; nm.uv_map = "UVMap"
    nt.links.new(tex("Normal").outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs[0], b.inputs["Normal"])
    ao = tex("AO"); ao.label = "AO (engine occlusion slot; not wired in Cycles preview)"
    b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.1
    if glass:
        b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = 1.46
        out = nt.nodes["Material Output"]; tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        lp = nt.nodes.new("ShaderNodeLightPath"); mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs[0]); nt.links.new(b.outputs[0], mx.inputs[1])
        nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    m["lod_atlas"] = atlas
    return m

ATM = {"BODY": atlas_mat("LODMAT_Body_Paint", "BODY", coat=0.58), "INTERIOR": atlas_mat("LODMAT_Interior", "INTERIOR"),
       "WHEELS": atlas_mat("LODMAT_Wheels", "WHEELS"), "TIRES": atlas_mat("LODMAT_Tire", "TIRES"),
       "BRAKES": atlas_mat("LODMAT_Brakes", "BRAKES"), "LIGHTS": atlas_mat("LODMAT_Lights", "LIGHTS"),
       "TRIM": atlas_mat("LODMAT_Trim", "TRIM"), "GLASS": atlas_mat("LODMAT_Glass", "GLASS", glass=True)}
LIGHT_CHANNELS = {"MAT_LED_White", "MAT_ProjectorLens", "MAT_LED_Red", "MAT_LED_Brake", "MAT_LED_Amber", "MAT_LED_Reverse"}
def remap(mat, atlas, lod):
    n = mat.name if mat else ""
    if n in LIGHT_CHANNELS or n == "MAT_BrakeCaliper":
        return mat                                                   # gameplay-controlled / colour option
    if n in ("MAT_HeadlightLens", "MAT_TaillightLens", "MAT_InteriorMirror"):
        return mat
    if n in ("MAT_AmbientLight", "MAT_Display"):
        return mat if lod < 3 else ATM["INTERIOR"]
    if n in ("MAT_DisplayGraphics", "MAT_DisplayGraphics_Red"):
        return mat if lod < 2 else (bpy.data.materials["MAT_Display"] if lod == 2 else ATM["INTERIOR"])
    if n in ("MAT_CarbonExterior", "MAT_InteriorCarbon") and lod < 2:
        return mat                                                   # close-range weave kept at LOD0/1
    return ATM[atlas]

def merge_slots(me):
    """Collapse duplicate material slots after remapping (fewer draw calls)."""
    uniq = []
    for m in me.materials:
        if m not in uniq: uniq.append(m)
    if len(uniq) == len(me.materials): return
    remap_idx = [uniq.index(m) for m in me.materials]
    idx = [remap_idx[p.material_index] for p in me.polygons]
    me.materials.clear()
    for m in uniq: me.materials.append(m)
    for p, i in zip(me.polygons, idx): p.material_index = i

# ---------------------------------------------------------------- build
def lod_name(n, lod):
    return ("Body" if n == "Body_Shell" else "Wheel" + n[3:] if n.startswith("Rim_") else n) + f"_LOD{lod}"

car_root = bpy.data.objects["Car_Root"]
# Body LODs first, then park the master body's Exact boolean (27 s per re-eval; every temp decimate object would
# otherwise re-trigger it). Restored before saving, so REFERENCE_Master stays identical to the master file.
BODY_MESH = {}
_body = bpy.data.objects["Body_Shell"]
for lod in LODS:
    BODY_MESH[lod] = eval_mesh(_body, plan(_body, lod), lod)
    print("body LOD", lod, tris(BODY_MESH[lod]), flush=True)
_cut = _body.modifiers["Cutters"]; _cut_vis = _cut.show_viewport; _cut.show_viewport = False
report = {"master": {}, "lods": {}}
bpy.context.view_layer.update()
for lod in LODS:
    col = bpy.data.collections.new(f"Car_LOD{lod}"); sc.collection.children.link(col)
    sub = {}
    for cat in CAT.values():
        c = bpy.data.collections.new(f"LOD{lod}_{cat}"); col.children.link(c); sub[cat] = c
    root = bpy.data.objects.new(f"Car_LOD{lod}", None); col.objects.link(root)
    root.parent = car_root; root.empty_display_size = 0.5
    bpy.context.view_layer.update()
    made = {}
    for o in MASTER:
        p = plan(o, lod)
        if p["drop"]:
            continue
        me = BODY_MESH[lod] if o.name == "Body_Shell" else eval_mesh(o, p, lod)
        if not p["holes"] and o.name.startswith("BrakeDisc_"):
            strip_holes(me)
        sym = abs(sum((Vector(c) for c in o.bound_box), Vector()).x / 8 + o.matrix_world.translation.x) < 0.05
        me = decimate(me, p["r"], sym)
        clean(me)
        for i, m in enumerate(me.materials):
            me.materials[i] = remap(m, o["atlas"], lod)
        merge_slots(me)
        nm = lod_name(o.name, lod); me.name = nm
        ob = bpy.data.objects.new(nm, me); sub[CAT[o["atlas"]]].objects.link(ob)
        ob.parent = root; ob.matrix_parent_inverse = root.matrix_world.inverted(); ob.matrix_basis = o.matrix_world.copy()
        ob["atlas"] = o["atlas"]; ob["lod"] = lod; ob["master"] = o.name
        made[o.name] = ob
    bpy.context.view_layer.update()
    # rolling assemblies: tire + rotor ride on the wheel (rim) pivot; calipers stay on the root (steer, don't roll)
    for k in ("FL", "FR", "RL", "RR"):
        w = made[f"Rim_{k}"]
        for part in (f"Tire_{k}", f"BrakeDisc_{k}"):
            if part in made:
                c = made[part]; mw = c.matrix_world.copy()
                c.parent = w; c.matrix_parent_inverse = w.matrix_world.inverted(); c.matrix_basis = mw
    # door hinge empties (LOD0/1) keep the opening-door hierarchy
    if lod <= 1:
        for s in ("L", "R"):
            src = bpy.data.objects[f"Door_{s}"]
            d = bpy.data.objects.new(f"Door_{s}_LOD{lod}", None); sub["Body"].objects.link(d)
            d.empty_display_type = 'SINGLE_ARROW'; d.parent = root; d.matrix_basis = src.matrix_world.copy()
            bpy.context.view_layer.update()
            for ch in (f"DoorPanel_{s}", f"Window_F{s}", f"DoorHandle_{s}"):
                if ch in made:
                    c = made[ch]; mw = c.matrix_world.copy()
                    c.parent = d; c.matrix_parent_inverse = d.matrix_world.inverted(); c.matrix_basis = mw
    # LOD3: one lightweight cockpit shell
    if lod == 3:
        parts = [made[n] for n in LOD3_INT_KEEP if n in made]
        bm = bmesh.new(); mats = []
        for ob in parts:
            t = bmesh.new(); t.from_mesh(ob.data); t.transform(ob.matrix_world)
            base = len(mats); mats += list(ob.data.materials)
            for f in t.faces: f.material_index += base
            tmpme = bpy.data.meshes.new("tmp"); t.to_mesh(tmpme); bm.from_mesh(tmpme); bpy.data.meshes.remove(tmpme); t.free()
        me = bpy.data.meshes.new("Interior_LOD3"); bm.to_mesh(me); bm.free()
        for m in mats: me.materials.append(m)
        merge_slots(me)
        ob = bpy.data.objects.new("Interior_LOD3", me); sub["Interior"].objects.link(ob)
        ob.parent = root; ob.matrix_parent_inverse = root.matrix_world.inverted()
        ob["atlas"] = "INTERIOR"; ob["lod"] = 3; ob["master"] = ",".join(sorted(LOD3_INT_KEEP))
        for p_ in parts:
            bpy.data.objects.remove(p_)
    col.hide_render = lod != 0
    print("LOD", lod, "built", sum(tris(o.data) for o in col.all_objects if o.type == 'MESH'), flush=True)

_cut.show_viewport = _cut_vis
# ---------------------------------------------------------------- master -> hidden, render-excluded reference
ref = bpy.data.collections.new("REFERENCE_Master"); sc.collection.children.link(ref)
for c in list(bpy.data.collections["HC_Hypercar"].children):
    if c.name != "HC_Rig":
        bpy.data.collections["HC_Hypercar"].children.unlink(c); ref.children.link(c)
ref.hide_render = True
bpy.context.view_layer.layer_collection.children["REFERENCE_Master"].exclude = True
for n in ("HC_Cutters_LOD2", "HC_Cutters_LOD3"):
    bpy.context.view_layer.layer_collection.children[n].exclude = True
sc["lod_build"] = "lod_build.py from hypercar_05a_pre_lod_cleanup.blend"
bpy.ops.wm.save_as_mainfile(filepath=OUT)
bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_mainfile()
print("SAVED", OUT)
```
