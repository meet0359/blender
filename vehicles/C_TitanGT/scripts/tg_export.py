# Titan GT FBX export (Hypercar method). Opens titangt_08 (never re-saved), saves titangt_09_export_ready.blend (pre-bake production scene),
# then in memory only: duplicate-face removal + n-gon triangulation + axis bake G = Rot(-90 deg, X), and writes the two FBX files.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from tg_lib import *
import hashlib
bpy.ops.wm.open_mainfile(filepath=CKP('titangt_08_colliders_hierarchy.blend')); O = bpy.data.objects
FBX = dict(use_selection=True, object_types={'MESH', 'EMPTY'}, use_active_collection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
           axis_forward='-Z', axis_up='Y', bake_space_transform=False, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='FACE', use_subsurf=False,
           use_mesh_edges=False, use_tspace=True, use_triangles=False, use_custom_props=False, add_leaf_bones=False, bake_anim=False, path_mode='RELATIVE', embed_textures=False, batch_mode='OFF')
def subtree(o): return [o] + [c for c in o.children_recursive]
cr = O['Car_Root']; rig = [O[n] for n in ('WheelColliderRef_FL', 'WheelColliderRef_FR', 'WheelColliderRef_RL', 'WheelColliderRef_RR', 'CenterOfMass')]
colls = subtree(O['Collision']); lods = {i: subtree(O[f'LOD{i}_Root']) for i in range(4)}
SETS = {'TitanGT_LOD0_unity_test.fbx': [cr] + rig + colls + lods[0], 'TitanGT_complete_unity.fbx': [cr] + rig + colls + sum(lods.values(), [])}
allx = SETS['TitanGT_complete_unity.fbx']; master = set(bpy.data.collections['TITAN_GT'].all_objects)
assert set(allx) == master, sorted(o.name for o in master ^ set(allx))[:8]
save_ckp('titangt_09_export_ready.blend')
G = Matrix.Rotation(-math.pi / 2, 4, 'X'); Gi = G.inverted(); I4 = Matrix.Identity(4)
def world(o): return (world(o.parent) @ o.matrix_parent_inverse if o.parent else I4) @ o.matrix_basis
W = {o.name: world(o) for o in allx}
for o in allx:
    pw = (W[o.parent.name] @ Gi) if o.parent else I4; o.matrix_parent_inverse = I4.copy(); o.matrix_basis = pw.inverted() @ (W[o.name] @ Gi)
tri_ng, dup_removed = [], {}
for me in {o.data for o in allx if o.type == 'MESH'}:
    want = sum(len(p.vertices) - 2 for p in me.polygons); bm = bmesh.new(); bm.from_mesh(me)
    if any(len(f.verts) > 4 for f in bm.faces): bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4], quad_method='BEAUTY', ngon_method='BEAUTY'); tri_ng.append(me.name)
    seen, dups = set(), []
    for f in bm.faces:
        k = frozenset(v.index for v in f.verts); (dups.append(f) if k in seen else seen.add(k))
    lost = sum(len(f.verts) - 2 for f in dups)
    if dups: bmesh.ops.delete(bm, geom=dups, context='FACES_ONLY'); dup_removed[me.name] = lost
    bm.to_mesh(me); bm.free(); me.transform(G); me.update()
    assert sum(len(p.vertices) - 2 for p in me.polygons) == want - lost, me.name
bpy.context.view_layer.update()
err = max(abs(a - b) for o in allx for ra, rb in zip(W[o.name], world(o) @ G) for a, b in zip(ra, rb)); print('AXIS BAKE max residual', err); assert err < 2e-5
files = {}
for fname, objs in SETS.items():
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.hide_set(False); o.hide_select = False; o.select_set(True)
    bpy.context.view_layer.objects.active = cr; path = EXP(fname); bpy.ops.export_scene.fbx(filepath=path, **FBX)
    leaked = [o.name for o in bpy.context.selected_objects if o not in objs]
    files[fname] = dict(objects=[o.name for o in objs], count=len(objs), bytes=os.path.getsize(path), sha1=hashlib.sha1(open(path, 'rb').read()).hexdigest(), leaked_selection=leaked)
    print('EXPORTED', fname, len(objs), leaked, flush=True)
used = sorted({m.name for o in allx if o.type == 'MESH' for m in o.data.materials if m})
texfiles = sorted({os.path.normpath(bpy.path.abspath(n.image.filepath)) for m in used for n in bpy.data.materials[m].node_tree.nodes if n.type == 'TEX_IMAGE' and n.image})
json.dump(dict(asset='Titan GT', phase='C', source='original build from the approved blockout titangt_01_blockout.blend', source_checkpoint='titangt_08_colliders_hierarchy.blend', export_checkpoint='titangt_09_export_ready.blend',
               fbx_settings={k: sorted(v) if isinstance(v, set) else v for k, v in FBX.items()}, axis_bake='in-memory: world\' = world @ G^-1, mesh\' = G v, G = Rot(-90 deg, X); max residual %.2e' % err,
               export_session=dict(ngon_triangulated_meshes=sorted(tri_ng), duplicate_triangles_removed=dup_removed), files=files, materials=used, textures=[os.path.basename(t) for t in texfiles],
               unity=dict(forward='+Z', up='+Y', vehicle_left='-X', point_map='(x, y, z) Blender -> (-x, z, -y) Unity')),
          open(os.path.join(REPD(), 'TG_export_manifest.json'), 'w'), indent=1)
print('EXPORT DONE')
