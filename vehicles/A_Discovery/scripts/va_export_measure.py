# Export Vechile package: measure every *_complete_unity.fbx inside a package copy (read-only; never saves).
# FBX level = what Unity reads (globals, Lcl transforms, texture paths resolved from the package, absolute paths).
# Re-import level = factory-clean scene per FBX: hierarchy, per-LOD tris/materials, bounds, wheel refs + pivots,
# CenterOfMass, colliders, light channels, UVs, custom normals, which image files the importer actually loaded.
#   Blender -b --factory-startup --python va_export_measure.py -- <package_dir> <out.json>
import bpy, os, sys, json, hashlib
import numpy as np
from io_scene_fbx import parse_fbx

PKG, OUT = sys.argv[sys.argv.index('--') + 1:][:2]
PKG = os.path.realpath(PKG)
LIGHT_CELLS = ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse', 'Marker']   # = ts_lib.LIGHT_CELLS
U = lambda v: [round(-v[0], 5), round(v[2], 5), round(-v[1], 5)]          # Blender (x, y, z) -> Unity (-x, z, -y)
base = lambda n: n.split('.')[0]


def fbx_file(path):                                     # after ts_fbx_audit.fbx_file, plus Lcl transforms + absolute paths
    root, ver = parse_fbx.parse(path); E = lambda e, i: [c for c in e.elems if c.id == i]
    gs = {p.props[0].decode(): p.props[4] for p in E(E(E(root, b'GlobalSettings')[0], b'Properties70')[0], b'P') if len(p.props) > 4}
    objs = E(root, b'Objects')[0]
    rel, absp, kinds, rot, scl, vids, tang = set(), set(), {}, {}, 0.0, 0, 0
    for o in objs.elems:
        k = o.id.decode(); kinds[k] = kinds.get(k, 0) + 1
        if o.id in (b'Texture', b'Video'):
            for tag, acc in ((b'RelativeFilename', rel), (b'FileName', absp), (b'Filename', absp)):
                for e in E(o, tag):
                    s = e.props[0].decode(errors='replace').replace('\\', '/')
                    if s: acc.add(s)
        if o.id == b'Video' and E(o, b'Content') and len(E(o, b'Content')[0].props[0]) > 0: vids += 1
        if o.id == b'Geometry' and E(o, b'LayerElementTangent'): tang += 1
        if o.id == b'Model':
            for p in (E(E(o, b'Properties70')[0], b'P') if E(o, b'Properties70') else []):
                n = p.props[0]
                if n == b'Lcl Rotation' and max(abs(x) for x in p.props[4:7]) > 1e-3:
                    rot[o.props[1].split(b'\x00\x01')[0].decode()] = [round(x, 4) for x in p.props[4:7]]
                if n == b'Lcl Scaling': scl = max(scl, *(abs(x - 1) for x in p.props[4:7]))
                if n == b'Lcl Scaling' and min(p.props[4:7]) < 0: scl = max(scl, 99.0)
    rel = sorted(r for r in rel if not r.startswith('/'))
    d = os.path.dirname(path)
    return dict(fbx_version=ver, globals={k: gs.get(k) for k in ('UpAxis', 'UpAxisSign', 'FrontAxis', 'FrontAxisSign', 'CoordAxis',
                'CoordAxisSign', 'UnitScaleFactor', 'OriginalUnitScaleFactor')}, object_kinds=kinds,
                texture_relative_paths=rel, unresolved_from_package=[r for r in rel if not os.path.isfile(os.path.normpath(os.path.join(d, r)))],
                resolved_outside_package=[r for r in rel if not os.path.normpath(os.path.join(d, r)).startswith(PKG + os.sep)],
                absolute_paths=sorted(absp), embedded_media=vids, geometries_with_tangents=tang,
                rotated_models=rot, max_lcl_scale_dev=scl)


def world_verts(o):
    me = o.data; n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float64); me.vertices.foreach_get('co', co); co = co.reshape(n, 3)
    M = np.array(o.matrix_world)
    return co @ M[:3, :3].T + M[:3, 3]


def ubounds(o_list):
    pts = [world_verts(o) for o in o_list if o.type == 'MESH' and len(o.data.vertices)]
    if not pts: return None
    p = np.concatenate(pts); p = np.stack([-p[:, 0], p[:, 2], -p[:, 1]], axis=1)          # Unity space
    lo, hi = p.min(0), p.max(0)
    return dict(min=[round(float(x), 5) for x in lo], max=[round(float(x), 5) for x in hi], size=[round(float(x), 5) for x in hi - lo])


def tris(o): return sum(len(p.vertices) - 2 for p in o.data.polygons)


def subtree(o):
    out = [o]
    for c in o.children: out += subtree(c)
    return out


def ts_channels(o):                                     # same UV-cell decode as ts_fbx_audit.channels / ts_validate check 10
    me = o.data; uv = me.uv_layers[0].data if me.uv_layers else None; res = {}
    if uv is None: return res
    for p in me.polygons:
        m = me.materials[p.material_index] if p.material_index < len(me.materials) else None
        if not m or base(m.name) != 'TS_Lights': continue
        u = sum(uv[li].uv.x for li in p.loop_indices) / len(p.loop_indices); v = sum(uv[li].uv.y for li in p.loop_indices) / len(p.loop_indices)
        i = int(min(3, max(0, (1 - v) // .25))) * 4 + int(min(3, max(0, u // .25)))
        if i < len(LIGHT_CELLS): res[LIGHT_CELLS[i]] = res.get(LIGHT_CELLS[i], 0) + 1
    return res


def material_faces(objs):
    out = {}
    for o in objs:
        if o.type != 'MESH': continue
        mats = [base(m.name) if m else None for m in o.data.materials]
        for p in o.data.polygons:
            n = mats[p.material_index] if p.material_index < len(mats) else None
            out[n or '(none)'] = out.get(n or '(none)', 0) + 1
    return out


def measure(path):
    R = dict(file=os.path.relpath(path, PKG), bytes=os.path.getsize(path),
             sha256=hashlib.sha256(open(path, 'rb').read()).hexdigest(), header=fbx_file(path))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path, use_custom_normals=True, use_image_search=False)
    O = bpy.data.objects; bpy.context.view_layer.update()
    R['objects'] = len(O); R['names'] = sorted(o.name for o in O)
    R['roots'] = sorted(o.name for o in O if o.parent is None)
    R['duplicate_suffix_names'] = [o.name for o in O if o.name[-4:-3] == '.' and o.name[-3:].isdigit()]
    R['negative_scale'] = [o.name for o in O if min(o.matrix_world.to_scale()) < 0]
    cr = O.get('Car_Root')
    R['car_root_children'] = sorted(c.name for c in cr.children) if cr else []
    R['lods'] = {}
    for i in range(4):
        r = O.get(f'LOD{i}_Root')
        if not r: continue
        objs = [o for o in subtree(r) if o.type == 'MESH']
        R['lods'][f'LOD{i}'] = dict(parent=r.parent.name if r.parent else None, objects=len(objs), tris=sum(tris(o) for o in objs),
                                    materials=sorted({base(m.name) for o in objs for m in o.data.materials if m}),
                                    material_faces=material_faces(objs), bounds=ubounds(objs),
                                    meshes_without_uv=[o.name for o in objs if not o.data.uv_layers],
                                    meshes_without_custom_normals=[o.name for o in objs if not o.data.has_custom_normals])
    r0 = O.get('LOD0_Root')
    R['lod0_parts'] = {o.name: dict(tris=tris(o), bounds=ubounds([o])) for o in (subtree(r0) if r0 else []) if o.type == 'MESH'}
    R['refs'] = {n: U(O[n].matrix_world.translation) for n in ('WheelColliderRef_FL', 'WheelColliderRef_FR', 'WheelColliderRef_RL',
                                                                 'WheelColliderRef_RR', 'CenterOfMass') if n in O}
    R['pivots'] = {}
    for o in O:
        b = base(o.name)
        for k in ('FL', 'FR', 'RL', 'RR'):
            if (b.startswith(f'Wheel_{k}_LOD') or b.startswith(f'SteerPivot_{k}_LOD')) and f'WheelColliderRef_{k}' in O:
                R['pivots'][o.name] = round((o.matrix_world.translation - O[f'WheelColliderRef_{k}'].matrix_world.translation).length, 7)
    R['colliders'] = {o.name: dict(tris=tris(o), materials=len([m for m in o.data.materials if m]), bounds=ubounds([o]),
                                   parent=o.parent.name if o.parent else None)
                      for o in O if o.type == 'MESH' and o.name.startswith('Collision_')}
    cols = [o for o in O if o.type == 'MESH' and o.name.startswith('Collision_')]
    R['collision_union'] = ubounds(cols)
    R['ts_light_channels'] = {o.name: ts_channels(o) for o in O if o.type == 'MESH' and base(o.name).startswith('Lights_LOD')}
    imgs = []
    for im in bpy.data.images:
        fp = os.path.realpath(bpy.path.abspath(im.filepath)) if im.filepath else ''
        ok = bool(fp) and os.path.isfile(fp)
        try: size = list(im.size) if ok else [0, 0]
        except Exception: size = [0, 0]
        imgs.append(dict(name=im.name, loaded_from=fp, exists=ok, inside_package=fp.startswith(PKG + os.sep), size=size))
    R['images'] = sorted(imgs, key=lambda x: x['name'])
    return R


fbx = sorted(os.path.join(d, f) for d, _, fs in os.walk(PKG) for f in fs if f.endswith('_complete_unity.fbx'))
res = {}
for p in fbx:
    m = measure(p); res[m['file']] = m
    print('MEASURED', m['file'], m['objects'], {k: v['tris'] for k, v in m['lods'].items()}, flush=True)
json.dump(dict(package=PKG, blender=bpy.app.version_string, files=res), open(OUT, 'w'), indent=1)
print('WROTE', OUT, len(res))
