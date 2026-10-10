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
