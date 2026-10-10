# Titan GT revision r1: rebuild Body_LOD1..3 from a groove-free body (Vortex R method). Fixes the frozen release's LOD1 panel-gap shading tears.
#   Blender -b --factory-startup --python tg_r1_lods.py -- <scratch dir>
# 1. Re-runs the FROZEN tg_build.py stages 02-06 in memory with only the three panel-gap groove cutters disabled (tg_lib writes go to <scratch>).
# 2. Decimates that body to the frozen LOD1..3 body triangle counts; skin faces take KD-tree smooth normals from the high-res reference.
# 3. Opens the frozen titangt_08 (never saved), swaps ONLY the Body_LOD1..3 mesh data, saves C_TitanGT_r1/blend/titangt_r1_08_colliders_hierarchy.blend.
# 4. Trim_LOD3: arch liners taken from Trim_LOD2 (LOD3 liners were chord triangles through the fenders); Body_LOD3 gives back the extra triangles.
# 5. Trim_LOD1: own smooth normals (38 deg) instead of transferred LOD0 normals (rocker blotches). Normals only.
# LOD0, glass, trim geometry, lights, interior, wheels, rig, colliders, materials and orientation are the frozen data, untouched.
import sys, os, json
FROZEN = '/Users/meetshah/Documents/blender/vehicles/C_TitanGT'; R1 = '/Users/meetshah/Documents/blender/vehicles/C_TitanGT_r1'
SCRW = sys.argv[sys.argv.index('--') + 1]; os.makedirs(SCRW, exist_ok=True)
os.environ['TG_SCRATCH'] = SCRW                                                    # frozen tg_lib writes (textures) land in scratch, never in C_TitanGT
sys.path.insert(0, FROZEN + '/scripts'); sys.dont_write_bytecode = True
import tg_lib; tg_lib.save_ckp = lambda *a, **k: None                              # no checkpoints from the re-run
src = open(FROZEN + '/scripts/tg_build.py').read().split('# ================================================================ 07 LODs')[0]
for s in ("fence('gap_hood'", "fence('gap_trunk'", "fence(f'gap_door_{sx}'"):
    assert src.count(s) == 1, s; src = src.replace(s, 'None and ' + s)           # groove-free body: openings, pockets, arches, handles, vents stay
s = 'bpy.data.objects.remove(hi, do_unlink=True)'; assert src.count(s) == 1; src = src.replace(s, 'pass')   # keep the high-res reference for normals
sys.argv = [sys.argv[0], '--', '6']; G = {'__file__': FROZEN + '/scripts/tg_build.py', '__name__': '__tg_build__'}
exec(compile(src, G['__file__'], 'exec'), G)
bpy, bmesh, math, Vector, SWATCH = G['bpy'], G['bmesh'], G['math'], G['Vector'], G['SWATCH']
O = bpy.data.objects; ng = O['Body_LOD0']; hi = O['REF_HiRes']; ng.name = 'Body_NoGap'
from mathutils.kdtree import KDTree
hi.data.shade_smooth(); HN = [v.normal.copy() for v in hi.data.vertices]; KD = KDTree(len(hi.data.vertices))
for v in hi.data.vertices: KD.insert(v.co, v.index)
KD.balance()
def smooth_normal(co, fn):
    acc = Vector(); wsum = 0.0
    for c_, i_, d_ in KD.find_n(co, 8):
        n_ = HN[i_]
        if n_.dot(fn) < .35 or d_ > .03: continue
        w_ = 1.0 / (d_ + 1e-4); acc += n_ * w_; wsum += w_
    return acc.normalized() if wsum > 0 else None
def skin_normals(o, skin_names=('TG_Paint', 'TG_Glass'), skin_swatches=('gloss_black',)):
    me = o.data; me.shade_smooth(); sw = me.attributes.get('swatch'); out = []
    for p in me.polygons:
        m = me.materials[p.material_index].name if me.materials[p.material_index] else ''
        skin = m in skin_names or (m == 'TG_Palette' and sw and SWATCH[sw.data[p.index].value] in skin_swatches)
        for li in p.loop_indices:
            n = smooth_normal(me.vertices[me.loops[li].vertex_index].co.lerp(p.center, .08), p.normal) if skin else None
            out.append(tuple(n) if n is not None else tuple(p.normal))
    me.normals_split_custom_set(out)
BVH = G['BVH']; HIM = [m.name if m else '' for m in hi.data.materials]
def fix_slivers(o):
    """collapsed opening-wall slivers lying flat on the outer paint skin (all verts on the skin, facing out) -> paint. Real walls keep a vertex at depth."""
    me = o.data; names = [m.name if m else '' for m in me.materials]; paint = names.index('TG_Paint'); n = 0
    for p in me.polygons:
        if p.material_index == paint: continue
        hits = [BVH.find_nearest(me.vertices[vi].co) for vi in p.vertices]
        if all(h[0] is not None and h[3] < .003 and HIM[hi.data.polygons[h[2]].material_index] == 'TG_Paint' and abs(h[1].dot(p.normal)) > .9 for h in hits):
            p.material_index = paint; n += 1
    return n
geo = json.load(open(FROZEN + '/reports/TG_geometry.json'))['lods']
T_NG = G['tris'](ng); NEW = {}; SLIV = {}
# ---- Trim_LOD3: the four arch liners collapse to 12-tri chords that slice through the fenders -> take the liners from the clean Trim_LOD2, keep every other LOD3 trim part
FZ8 = FROZEN + '/blend/titangt_08_colliders_hierarchy.blend'
with bpy.data.libraries.load(FZ8) as (s_, d_): d_.meshes = ['Trim_LOD2', 'Trim_LOD3']   # appended copies; the frozen file is only read
def liner_faces(me):
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table(); seen = set(); out = set()
    for f in bm.faces:
        if f.index in seen: continue
        st = [f]; seen.add(f.index); fs = []
        while st:
            g = st.pop(); fs.append(g.index)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen: seen.add(h.index); st.append(h)
        vs = {v.co.copy().freeze() for i in fs for v in bm.faces[i].verts}
        if min(abs(v.x) for v in vs) > .45 and max(v.z for v in vs) > .7 and max(v.y for v in vs) - min(v.y for v in vs) > .6: out |= set(fs)
    bm.free(); return out
def keep_faces(me, keep, name):
    o = bpy.data.objects.new(name, me.copy()); bpy.context.scene.collection.objects.link(o); bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.index not in keep], context='FACES'); bm.to_mesh(o.data); bm.free(); return o
m2, m3 = d_.meshes; L2, L3 = liner_faces(m2), liner_faces(m3)
t3 = keep_faces(m3, set(range(len(m3.polygons))) - L3, 'Trim_LOD3_r1'); lin = keep_faces(m2, L2, 'liners')
with bpy.context.temp_override(active_object=t3, object=t3, selected_editable_objects=[t3, lin], selected_objects=[t3, lin]): bpy.ops.object.join()
t3.data.name = 'Trim_LOD3_r1'; G['clean'](t3)
TRIM_DELTA = G['tris'](t3) - sum(len(p.vertices) - 2 for p in m3.polygons)
print('R1 Trim_LOD3 liner faces', len(L3), '->', len(L2), 'delta tris', TRIM_DELTA, flush=True)
assert len(L2) and len(L3), 'liner islands not found'
for k in (1, 2, 3):
    target = geo[f'LOD{k}']['parts'][f'Body_LOD{k}'] - (TRIM_DELTA if k == 3 else 0)   # LOD3 total stays at the frozen count
    d = ng.copy(); d.data = ng.data.copy(); ng.users_collection[0].objects.link(d); d.name = d.data.name = f'Body_LOD{k}'
    m = d.modifiers.new('dec', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = target / T_NG; m.use_symmetry = True; m.symmetry_axis = 'X'; m.use_collapse_triangulate = True
    with bpy.context.temp_override(object=d, active_object=d): bpy.ops.object.modifier_apply(modifier='dec')
    G['clean'](d); SLIV[k] = fix_slivers(d); skin_normals(d); G['final_uvs'](d); NEW[k] = d
    print('R1 Body_LOD%d' % k, G['tris'](d), 'frozen', target, 'slivers->paint', SLIV[k], flush=True)
lib = os.path.join(SCRW, 'r1_body_lods.blend'); bpy.data.libraries.write(lib, {o.data for o in NEW.values()} | {t3.data}, fake_user=True)
# ---- swap into the frozen 08 checkpoint (opened, never saved back)
out = os.path.join(R1, 'blend', 'titangt_r1_08_colliders_hierarchy.blend'); assert not os.path.exists(out), out
bpy.ops.wm.open_mainfile(filepath=FROZEN + '/blend/titangt_08_colliders_hierarchy.blend'); O = bpy.data.objects; MAT = bpy.data.materials
with bpy.data.libraries.load(lib) as (s_, d_): d_.meshes = [f'Body_LOD{k}' for k in (1, 2, 3)] + ['Trim_LOD3_r1']
LOG = {}
for me in d_.meshes:
    base = me.name.split('.')[0].replace('_r1', ''); o = O[base]; old = o.data; before = len(old.polygons)
    for i, m in enumerate(me.materials): me.materials[i] = MAT[m.name.split('.')[0]]   # frozen materials (TG_Paint.001 -> TG_Paint)
    me.use_fake_user = False; o.data = me; bpy.data.meshes.remove(old); me.name = base
    LOG[base] = {'tris_frozen': before, 'tris_r1': sum(len(p.vertices) - 2 for p in me.polygons)}
t = O['Trim_LOD1']                                                                 # rocker chrome blotches: transferred LOD0 normals -> own smooth normals + 38 deg edges (as LOD2/3)
with bpy.context.temp_override(object=t, active_object=t): bpy.ops.mesh.customdata_custom_splitnormals_clear()
t.data.shade_smooth(); t.data.set_sharp_from_angle(angle=math.radians(38)); LOG['Trim_LOD1'] = 'normals only: custom normals cleared, smooth + 38 deg sharp edges; geometry unchanged'
for d in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
    for x in list(d):
        if x.users == 0: d.remove(x)
for im in bpy.data.images:                                                        # textures resolve to the r1 copies (byte-identical to the frozen ones)
    if im.filepath: im.filepath = os.path.join(R1, 'textures', os.path.basename(bpy.path.abspath(im.filepath)))
for lb in list(bpy.data.libraries): bpy.data.libraries.remove(lb)
assert all(m.name in {'TG_Carbon', 'TG_Display', 'TG_Glass', 'TG_Paint', 'TG_Palette', 'TG_Tire', 'TG_LensClear', 'TG_LensRed'} or m.name.startswith('TG_LED_') for m in MAT), [m.name for m in MAT]
bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, relative_remap=True); print('SAVED', out, flush=True)
json.dump({'revision': 'r1', 'base': 'C_TitanGT/blend/titangt_08_colliders_hierarchy.blend (frozen, read only)', 'nogap_body_tris': T_NG, 'slivers_to_paint': SLIV, 'swapped': LOG,
           'method': 'groove-free body (panel-gap cutters disabled), collapse decimate to the frozen per-LOD body triangle count, KD-tree smooth-reference normals on skin faces, flat on openings'},
          open(os.path.join(R1, 'reports', 'TG_r1_lod_rebuild_log.json'), 'w'), indent=1)
