# Phase A vehicle audit (read-only: opens the blend, measures, never saves).
#   Blender -b --factory-startup --python va_audit.py -- <blend> <tag>
# Writes vehicles/A_Discovery/reports/VA_audit_<tag>.json and prints a summary.
import sys; sys.dont_write_bytecode = True
import bpy, bmesh, os, re, json, math
from collections import Counter, defaultdict
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; SRC, TAG = a[0], a[1]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports', f'VA_audit_{TAG}.json')
bpy.ops.wm.open_mainfile(filepath=SRC); O = bpy.data.objects; dg = bpy.context.evaluated_depsgraph_get()
LODRE = re.compile(r'_LOD(\d)(?:$|\.)')
def lod_of(o):
    m = LODRE.search(o.name)
    if m: return int(m.group(1))
    for c in o.users_collection:
        m = re.search(r'LOD(\d)', c.name)
        if m: return int(m.group(1))
    return None
def collider(o): return o.name.startswith(('Collision', 'Collider')) or any(c.name.upper().startswith('COLLI') for c in o.users_collection)
def hidden_ref(o):
    cs = list(o.users_collection)
    while cs:
        c = cs.pop()
        if c.name.startswith('REFERENCE') or c.name.startswith('PRESENTATION'): return True
        cs += [p for p in bpy.data.collections if c.name in p.children]
    return False
def tri_mesh(o):
    ev = o.evaluated_get(dg); me = ev.to_mesh(); me.calc_loop_triangles(); return ev, me
geo = [o for o in O if o.type in ('MESH', 'CURVE', 'SURFACE', 'META', 'FONT')]
per = {}
for o in geo:
    ev, me = tri_mesh(o); per[o.name] = dict(tris=len(me.loop_triangles), verts=len(me.vertices), lod=lod_of(o), collider=collider(o), ref=hidden_ref(o), type=o.type,
                                              mats=sorted({s.material.name for s in o.material_slots if s.material}), uv=len(getattr(o.data, 'uv_layers', []) or []),
                                              scale=[round(v, 4) for v in o.scale], neg=any(v < 0 for v in o.scale), mods=[m.type for m in getattr(o, 'modifiers', [])])
    ev.to_mesh_clear()
lods = sorted({v['lod'] for v in per.values() if v['lod'] is not None and not v['collider'] and not v['ref']})
lod_stats = {}
for L in lods:
    names = [n for n, v in per.items() if v['lod'] == L and not v['collider'] and not v['ref']]
    mats = sorted({m for n in names for m in per[n]['mats']})
    imgs = sorted({nd.image.name for m in mats for nd in (bpy.data.materials[m].node_tree.nodes if bpy.data.materials[m].use_nodes else []) if nd.type == 'TEX_IMAGE' and nd.image})
    lod_stats[f'LOD{L}'] = dict(objects=len(names), tris=sum(per[n]['tris'] for n in names), materials=len(mats), material_names=mats, images=len(imgs),
                                curves=sum(1 for n in names if per[n]['type'] != 'MESH'), largest=sorted(((per[n]['tris'], n) for n in names), reverse=True)[:6])
ref_tris = sum(v['tris'] for v in per.values() if v['ref']); unl = [n for n, v in per.items() if v['lod'] is None and not v['collider'] and not v['ref']]
# bounds of LOD0 (vehicle dims)
def bounds(names):
    pts = [O[n].matrix_world @ Vector(c) for n in names for c in O[n].bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)]); return lo, hi
l0 = [n for n, v in per.items() if v['lod'] == (lods[0] if lods else None) and not v['collider'] and not v['ref']] or unl
lo, hi = bounds(l0); dims = dict(length_y=round(hi.y - lo.y, 4), width_x=round(hi.x - lo.x, 4), height_z=round(hi.z - lo.z, 4), min=[round(v, 4) for v in lo], max=[round(v, 4) for v in hi])
# topology on LOD0
topo = Counter(); worst = []
for n in l0:
    o = O[n]
    if o.type != 'MESH': continue
    ev, me = tri_mesh(o); bm = bmesh.new(); bm.from_mesh(me); ev.to_mesh_clear(); bm.faces.ensure_lookup_table(); bm.normal_update()
    za = sum(1 for f in bm.faces if f.calc_area() < 1e-9); ng = sum(1 for f in bm.faces if len(f.verts) > 4); lv = sum(1 for v in bm.verts if not v.link_edges)
    nm = sum(1 for e in bm.edges if len(e.link_faces) > 2); bd = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    wind = sum(1 for e in bm.edges if len(e.link_faces) == 2 and [l.vert for l in e.link_faces[0].loops if l.edge == e][0] == [l.vert for l in e.link_faces[1].loops if l.edge == e][0])
    dup = len(bm.verts) - len({tuple(round(c, 5) for c in v.co) for v in bm.verts})
    vol = sum(f.calc_center_median().dot(f.normal) * f.calc_area() for f in bm.faces) / 3.0 if not bd and bm.faces else None
    inv = vol is not None and vol < -1e-7
    bm.free()
    for k, v in (('zero_area_faces', za), ('ngons', ng), ('loose_verts', lv), ('nonmanifold_edges', nm), ('boundary_edges', bd), ('inconsistent_winding_edges', wind), ('duplicate_verts', dup), ('closed_inside_out', int(inv))):
        topo[k] += v
    score = za + wind + nm + int(inv) * 1000
    if score: worst.append((score, n, dict(zero_area=za, winding=wind, nonmanifold=nm, inside_out=inv)))
worst.sort(reverse=True)
# coincident duplicate objects in LOD0 (same tris + same world bounds)
sig = defaultdict(list)
for n in l0:
    b = [tuple(round(c, 3) for c in (O[n].matrix_world @ Vector(x))) for x in O[n].bound_box]
    sig[(per[n]['tris'], tuple(sorted(b)))].append(n)
dupobj = [v for v in sig.values() if len(v) > 1]
# wheels
wheels = {}
for k in ('FL', 'FR', 'RL', 'RR'):
    cand = [O[n] for n in (f'Wheel_{k}_LOD{lods[0] if lods else 0}', f'Wheel_{k}') if n in O and not hidden_ref(O[n])]
    ref = O.get(f'WheelColliderRef_{k}')
    if cand:
        w = cand[0]; kids = [w] + [c for c in w.children_recursive if re.search(r'Tire|Tyre|Rim|Wheel', c.name) and not re.search(r'Brake|Caliper|Disc|Rotor', c.name)]
        pts = [c.matrix_world @ Vector(x) for c in kids if c.type == 'MESH' for x in c.bound_box]
        if pts:
            blo = Vector([min(p[i] for p in pts) for i in range(3)]); bhi = Vector([max(p[i] for p in pts) for i in range(3)]); ctr = (blo + bhi) / 2
            wheels[k] = dict(object=w.name, origin=[round(v, 4) for v in w.matrix_world.translation], bbox_centre_offset_mm=[round((ctr[i] - w.matrix_world.translation[i]) * 1000, 2) for i in range(3)],
                             radius=round((bhi.z - blo.z) / 2, 4), width=round(bhi.x - blo.x, 4), ref=[round(v, 4) for v in ref.matrix_world.translation] if ref else None,
                             side_by_convention=('LEFT(+X)' if w.matrix_world.translation.x > 0 else 'RIGHT(-X)'), front=w.matrix_world.translation.y < 0)
wb = None
if all(k in wheels for k in ('FL', 'RL')): wb = round(abs(wheels['RL']['origin'][1] - wheels['FL']['origin'][1]), 4)
fr = O.get('WheelColliderRef_FL') or O.get('WheelColliderRef_FR')
facing = ('-Y (project convention)' if fr.matrix_world.translation.y < 0 else '+Y') if fr else 'unknown'
lr = {k: ('+X' if O[f'WheelColliderRef_{k}'].matrix_world.translation.x > 0 else '-X') for k in ('FL', 'FR', 'RL', 'RR') if f'WheelColliderRef_{k}' in O}
left_right = dict(refs=lr, convention_ok=(lr.get('FL') == '+X' and lr.get('RL') == '+X') if lr else None, note='project convention: vehicle left = Blender +X (forward -Y, up +Z)')
# colliders
cols = {}
for n, v in per.items():
    if not v['collider'] or O[n].type != 'MESH': continue
    me = O[n].data; bm = bmesh.new(); bm.from_mesh(me); bm.normal_update()
    closed = all(len(e.link_faces) == 2 for e in bm.edges); conv = all(all((v_.co - f.calc_center_median()).dot(f.normal) <= 1e-3 for v_ in bm.verts) for f in bm.faces)
    cols[n] = dict(tris=v['tris'], closed=closed, convex=conv, materials=v['mats']); bm.free()   # convex: every vertex behind every face plane (1 mm)
refs = {o.name: [round(c, 4) for c in o.matrix_world.translation] for o in O if o.type == 'EMPTY' and any(k in o.name for k in ('WheelColliderRef', 'CenterOfMass', 'Axle', 'Car_Root', 'LOD0_Root'))}
# materials / images
imgs = []
for im in bpy.data.images:
    if im.source != 'FILE': continue
    p = bpy.path.abspath(im.filepath, library=im.library); imgs.append(dict(name=im.name, size=list(im.size), packed=bool(im.packed_file), exists=os.path.exists(p), path=im.filepath))
miss = [i['name'] for i in imgs if not i['exists'] and not i['packed']]
rep = dict(source=SRC, tag=TAG, objects=dict(Counter(o.type for o in O)), collections=len(bpy.data.collections), materials_total=len(bpy.data.materials), images_total=len(imgs), missing_images=miss,
           lods=lod_stats, hidden_reference_tris=ref_tris, left_right=left_right, unlodded_render_objects=len(unl), dims_lod0=dims, facing=facing, wheels=wheels, wheelbase=wb,
           track=round(abs(wheels['FL']['origin'][0] - wheels['FR']['origin'][0]), 4) if 'FL' in wheels and 'FR' in wheels else None,
           topology_lod0=dict(topo), worst_lod0_objects=[(n, d) for _, n, d in worst[:12]], duplicate_object_groups_lod0=len(dupobj), duplicate_object_examples=dupobj[:6],
           colliders=cols, references=refs, negative_scale=[n for n, v in per.items() if v['neg']], cameras=[o.name for o in O if o.type == 'CAMERA'], lights=[o.name for o in O if o.type == 'LIGHT'],
           modifiers_lod0=dict(Counter(m for n in l0 for m in per[n]['mods'])), objects_without_uv_lod0=[n for n in l0 if O[n].type == 'MESH' and per[n]['uv'] == 0][:20])
json.dump(rep, open(OUT, 'w'), indent=1)
print('AUDIT', TAG, json.dumps({k: rep[k] for k in ('objects', 'materials_total', 'images_total', 'dims_lod0', 'facing', 'left_right', 'wheelbase', 'track', 'hidden_reference_tris', 'topology_lod0', 'duplicate_object_groups_lod0')}))
for L, s in lod_stats.items(): print(' ', L, {k: s[k] for k in ('objects', 'tris', 'materials', 'images', 'curves')})
for k, w in wheels.items(): print('  wheel', k, w)
print('  colliders', cols); print('  refs', refs); print('  missing images', miss[:10]); print('  cameras', len(rep['cameras']), 'lights', len(rep['lights']), 'neg scale', rep['negative_scale'][:5])
print('  worst', rep['worst_lod0_objects'][:6]); print('  dup objects', rep['duplicate_object_examples'][:3])
