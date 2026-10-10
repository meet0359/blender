# Unity handoff FBX audit (read-only; supplements ts_validate's re-import check). Compares the PACKAGED FBX against the frozen 09 (an
# isolated, SHA-1-verified copy in the export workspace; never saved): FBX file globals + texture paths resolved from the package folder,
# per-LOD objects / triangles / materials, wheel pivots vs WheelColliderRefs, collider refs + CenterOfMass, light-channel faces, normals,
# duplicates, Unity-space transforms + dimensions. Also writes the material mapping (from the 09) for the Unity material setup.
#   Blender -b --factory-startup --python ts_fbx_audit.py -- <ws_vehicle_dir> <ckp_prefix> <FBX_base> <pkg_vehicle_dir>
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from ts_lib import *
from io_scene_fbx import parse_fbx
import hashlib
WSV, PFX, BASE, PKV = sys.argv[sys.argv.index('--') + 1:][:4]
SRC09 = os.path.join(WSV, 'blend', f'{PFX}_09_export_ready.blend'); MAN = json.load(open(os.path.join(WSV, 'reports', f'{PFX}_export_manifest.json')))
tris = lambda o: sum(len(p.vertices) - 2 for p in o.data.polygons)
CORNERS = ('FL', 'FR', 'RL', 'RR')
def channels(o):                                                                             # same decode as ts_validate check 10 (TS_Lights mask cell from UVs)
    me = o.data; uv = me.uv_layers['UVMap'].data; res = {}
    for p in me.polygons:
        m = me.materials[p.material_index]
        if not m or m.name.split('.')[0] != 'TS_Lights': continue
        u = sum(uv[li].uv.x for li in p.loop_indices) / len(p.loop_indices); v = sum(uv[li].uv.y for li in p.loop_indices) / len(p.loop_indices)
        i = int(min(3, max(0, (1 - v) // .25))) * 4 + int(min(3, max(0, u // .25)))
        if i < len(LIGHT_CELLS): res[LIGHT_CELLS[i]] = res.get(LIGHT_CELLS[i], 0) + 1
    return res
def tear_pct(o, lim=50.0):                                                                   # S1 metric (ts_validate)
    cn = o.data.corner_normals; b = t = 0
    for p in o.data.polygons:
        if p.area < 2e-6: continue
        for li in p.loop_indices: t += 1; b += cn[li].vector.angle(p.normal, 0) > math.radians(lim)
    return 100.0 * b / max(t, 1)
def facts():
    O = bpy.data.objects; F = {}
    for o in O:
        d = dict(type=o.type, parent=o.parent.name if o.parent else None, t=list(o.matrix_world.translation), lod=None)
        p = o
        while p and not (p.name.startswith('LOD') and p.name.endswith('_Root')): p = p.parent
        d['lod'] = int(p.name[3]) if p else None
        if o.type == 'MESH':
            me = o.data; d.update(tris=tris(o), mats=[m.name.split('.')[0] if m else None for m in me.materials], uv=[u.name for u in me.uv_layers], tear=round(tear_pct(o), 3) if len(me.polygons) else 0.0)
            co = np.array([v.co[:] for v in me.vertices]) if len(me.vertices) else np.zeros((0, 3)); cn = np.array([c.vector[:] for c in me.corner_normals]) if len(me.polygons) else np.zeros((0, 3))
            d['nan'] = int(np.isnan(co).sum() + np.isnan(cn).sum()); d['zero_normals'] = int((np.linalg.norm(cn, axis=1) < .5).sum()) if len(cn) else 0
            d['degenerate'] = sum(1 for q in me.polygons if q.area < 1e-10)
            seen, dup = set(), 0
            for q in me.polygons:
                k = frozenset(q.vertices); dup += k in seen; seen.add(k)
            d['dup_faces'] = dup
            if o.name.startswith('Lights_LOD'): d['channels'] = channels(o)
        if o.name.startswith('WheelColliderRef_'): d['props'] = {k: float(o[k]) for k in ('radius_m', 'width_m') if k in o}
        F[o.name] = d
    return F
def pyval(v):
    if hasattr(v, 'to_dict'): return v.to_dict()
    if hasattr(v, 'to_list'): return v.to_list()
    return v if isinstance(v, (int, float, str, bool)) or v is None else str(v)
def upstream_images(sock, depth=0):
    out = []
    for l in sock.links if depth < 8 else []:
        n = l.from_node
        if n.type == 'TEX_IMAGE' and n.image: out.append(os.path.basename(bpy.path.abspath(n.image.filepath)) if not n.image.packed_file else f'{n.image.name} (packed, Blender review only)')
        for s in n.inputs: out += upstream_images(s, depth + 1)
    return sorted(set(out))
# ---------------- source facts (frozen 09 copy; read-only)
bpy.ops.wm.open_mainfile(filepath=SRC09); SRC = facts(); used_by = {}
for o in bpy.data.objects:
    if o.type == 'MESH':
        for m in o.data.materials:
            if m: used_by.setdefault(m.name, []).append(o.name)
MATS = {}
for mn in sorted(used_by):
    m = bpy.data.materials[mn]; pb = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None) if m.use_nodes else None; ins = {}
    for k in ('Base Color', 'Metallic', 'Roughness', 'Alpha', 'Normal', 'Emission Color', 'Emission Strength', 'Coat Weight', 'Coat Roughness'):
        s = pb.inputs.get(k) if pb else None
        if s is None: continue
        dv = getattr(s, 'default_value', None); dv = [round(x, 4) for x in dv] if hasattr(dv, '__len__') else (round(dv, 4) if isinstance(dv, float) else None)
        ins[k] = dict(value=dv, linked=s.is_linked, textures=upstream_images(s))
    nm = [round(n.inputs['Strength'].default_value, 3) for n in m.node_tree.nodes if n.type == 'NORMAL_MAP'] if m.use_nodes else []
    rgb = {(n.label or n.name): [round(x, 4) for x in n.outputs[0].default_value[:3]] for n in m.node_tree.nodes if n.type == 'RGB'} if m.use_nodes else {}
    MATS[mn] = dict(custom={k: pyval(v) for k, v in m.items()}, surface_render_method=m.surface_render_method, principled=ins, normal_map_strengths=nm, rgb_nodes=rgb,
                    images=sorted({(os.path.basename(bpy.path.abspath(n.image.filepath)) if not n.image.packed_file else n.image.name + ' (packed)', n.image.colorspace_settings.name)
                                   for n in m.node_tree.nodes if n.type == 'TEX_IMAGE' and n.image} if m.use_nodes else set()),
                    used_by_lods=sorted({SRC[o]['lod'] for o in used_by[mn] if SRC[o]['lod'] is not None}), objects=len(used_by[mn]))
# ---------------- FBX file level (parse_fbx: what Unity reads)
def fbx_file(path):
    root, ver = parse_fbx.parse(path); E = lambda e, i: [c for c in e.elems if c.id == i]
    gs = {p.props[0].decode(): p.props[4] for p in E(E(E(root, b'GlobalSettings')[0], b'Properties70')[0], b'P') if len(p.props) > 4}
    objs = E(root, b'Objects')[0]; nm = {o.props[0]: (o.id.decode(), o.props[1].split(b'\x00\x01')[0].decode(errors='replace')) for o in objs.elems if o.props}
    tex = {}; vids = 0; tang = 0
    for o in objs.elems:
        if o.id == b'Texture':
            rel = (E(o, b'RelativeFilename') or [None])[0]; rel = rel.props[0].decode() if rel else ''
            tex[o.props[0]] = rel.replace('\\', '/')
        if o.id == b'Video' and E(o, b'Content') and len(E(o, b'Content')[0].props[0]) > 0: vids += 1
        if o.id == b'Geometry' and E(o, b'LayerElementTangent'): tang += 1
    m2t = {}
    for c in E(E(root, b'Connections')[0], b'C'):
        if c.props[0] == b'OP' and c.props[1] in tex and c.props[2] in nm: m2t.setdefault(nm[c.props[2]][1], {})[c.props[3].decode()] = tex[c.props[1]]
    kinds = {}
    for k, (t, _) in nm.items(): kinds[t] = kinds.get(t, 0) + 1
    pick = ('UpAxis', 'UpAxisSign', 'FrontAxis', 'FrontAxisSign', 'CoordAxis', 'CoordAxisSign', 'UnitScaleFactor', 'OriginalUnitScaleFactor')
    rels = sorted(set(tex.values())); unres = [r for r in rels if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), r)))]
    return dict(fbx_version=ver, globals={k: gs.get(k) for k in pick}, object_kinds=kinds, texture_relative_paths=rels, unresolved_from_package=unres,
                embedded_media=vids, geometries_with_tangents=tang, material_texture_slots=m2t)
# ---------------- per FBX: clean re-import vs source
OUT = dict(asset=os.path.basename(WSV), source=SRC09, source_sha1=hashlib.sha1(open(SRC09, 'rb').read()).hexdigest(), files={}, materials=MATS)
allok = True
for fname, d in MAN['files'].items():
    path = os.path.join(PKV, 'FBX', fname); pr = []; R = dict(sha1=hashlib.sha1(open(path, 'rb').read()).hexdigest(), bytes=os.path.getsize(path))
    if R['sha1'] != d['sha1']: pr.append('packaged FBX differs from the exported FBX')
    R['file'] = fl = fbx_file(path)
    g = fl['globals']
    if (g['UpAxis'], g['UpAxisSign']) != (1, 1): pr.append(f'axis globals {g}')                     # Y up; forward / handedness proven by the raw Unity-space test below
    if abs(g['UnitScaleFactor'] - 100.0) > 1e-6: pr.append(f"UnitScaleFactor {g['UnitScaleFactor']} (expected 100 = metres)")
    if fl['unresolved_from_package']: pr.append(f"texture paths unresolved from package: {fl['unresolved_from_package']}")
    if fl['embedded_media']: pr.append('embedded media present')
    want = set(d['objects'])
    # default import (Blender space, compared to the 09)
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=path); bpy.context.view_layer.update(); GOT = facts()
    if set(GOT) != want: pr.append(f'objects: missing {sorted(want - set(GOT))[:4]} extra {sorted(set(GOT) - want)[:4]}')
    dupm = sorted(m.name for m in bpy.data.materials if '.' in m.name); dupo = sorted(n for n in GOT if '.0' in n)
    if dupm or dupo: pr.append(f'duplicate names: materials {dupm[:4]} objects {dupo[:4]}')
    lods = {}; mdev = pdev = 0.0
    for k in range(4):
        s_ = [n for n in want if SRC[n]['lod'] == k]
        if not s_: continue
        g_ = [n for n in s_ if n in GOT]
        lods[f'LOD{k}'] = dict(objects=len(g_), source_objects=len(s_), tris=sum(GOT[n].get('tris', 0) for n in g_), source_tris=sum(SRC[n].get('tris', 0) for n in s_),
                               materials=sorted({m for n in g_ for m in GOT[n].get('mats', []) if m}), source_materials=sorted({m for n in s_ for m in SRC[n].get('mats', []) if m}))
        L = lods[f'LOD{k}']
        if L['objects'] != L['source_objects'] or L['materials'] != L['source_materials'] or not (L['source_tris'] - 30 <= L['tris'] <= L['source_tris']): pr.append(f'LOD{k} {L}')
    for n in want & set(GOT):
        a, b = SRC[n], GOT[n]; pdev = max(pdev, (Vector(a['t']) - Vector(b['t'])).length)
        if a['parent'] != b['parent']: pr.append(f'{n} parent {b["parent"]} vs {a["parent"]}')
        if a['type'] == 'MESH' and (a['mats'] != b['mats'] or a['uv'] != b['uv']): pr.append(f'{n} materials / UV')
    wheels = {}
    for c in CORNERS:
        ref = Vector(GOT[f'WheelColliderRef_{c}']['t']); ws_ = [n for n in GOT if n.startswith((f'Wheel_{c}_LOD', f'SteerPivot_{c}_LOD', f'Caliper_{c}_LOD'))]
        dv = max((Vector(GOT[n]['t']) - ref).length for n in ws_); wl = sorted({GOT[n]['lod'] for n in ws_ if n.startswith('Wheel_')})
        wheels[c] = dict(ref_blender=[round(x, 4) for x in ref], ref_unity=[round(-ref.x, 4), round(ref.z, 4), round(-ref.y, 4)], wheel_lods=wl, pivots=len(ws_), max_pivot_vs_ref_m=dv,
                         props=GOT[f'WheelColliderRef_{c}'].get('props'), source_props=SRC[f'WheelColliderRef_{c}'].get('props'))
        exp_l = sorted({SRC[n]['lod'] for n in want if n.startswith(f'Wheel_{c}_LOD')})
        if wl != exp_l or dv > 1e-4: pr.append(f'wheel {c}: LODs {wl} vs {exp_l}, pivot dev {dv:.1e}')
        if wheels[c]['props'] != wheels[c]['source_props'] or not wheels[c]['props']: pr.append(f'wheel {c} custom props {wheels[c]["props"]}')
    com = Vector(GOT['CenterOfMass']['t']); cols = sorted(n for n in GOT if n.startswith('Collision_'))
    colinfo = {n: dict(tris=GOT[n]['tris'], materials=len([m for m in GOT[n]['mats'] if m])) for n in cols}
    if len(cols) < 4 or any(v['tris'] > 255 or v['materials'] for v in colinfo.values()) or (com - Vector(SRC['CenterOfMass']['t'])).length > 1e-4: pr.append(f'colliders / COM {colinfo}')
    light = {n: dict(fbx=GOT[n]['channels'], source=SRC[n]['channels']) for n in sorted(GOT) if 'channels' in GOT[n]}
    if any(v['fbx'] != v['source'] for v in light.values()): pr.append('light channel faces differ')
    meshes = [n for n in GOT if GOT[n]['type'] == 'MESH']
    nrm = dict(nan_values=sum(GOT[n]['nan'] for n in meshes), zero_length_normals=sum(GOT[n]['zero_normals'] for n in meshes), degenerate_faces=sum(GOT[n]['degenerate'] for n in meshes),
               source_degenerate_faces=sum(SRC[n]['degenerate'] for n in meshes if n in SRC), duplicate_faces=sum(GOT[n]['dup_faces'] for n in meshes),
               s1_worst_fbx=sorted(((n, GOT[n]['tear']) for n in meshes if not n.startswith('Collision')), key=lambda t: -t[1])[:3])
    if nrm['nan_values'] or nrm['zero_length_normals'] or nrm['duplicate_faces'] or nrm['s1_worst_fbx'][0][1] > 1.0: pr.append(f'normals / duplicates {nrm}')
    # raw import = FBX file space as Unity reads it (Unity position = (-x, y, z)); no axis conversion applied
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=path, use_manual_orientation=True, axis_forward='Y', axis_up='Z'); bpy.context.view_layer.update()
    O = bpy.data.objects; I3 = Matrix.Identity(3)
    rot = max(max(abs(a - b) for ra, rb in zip(o.matrix_world.to_3x3().normalized(), I3) for a, b in zip(ra, rb)) for o in O)
    scl = max(abs(s - 1) for o in O for s in o.matrix_world.to_scale()); neg = [o.name for o in O if o.matrix_world.determinant() < 0]
    pts = np.vstack([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in O if o.type == 'MESH' and o.name.endswith('_LOD0')]); pts[:, 0] *= -1
    mn, mx = pts.min(0), pts.max(0); dims_u = dict(width_x=round(float(mx[0] - mn[0]), 4), height_y=round(float(mx[1] - mn[1]), 4), length_z=round(float(mx[2] - mn[2]), 4))
    unity = dict(car_root_identity=max(abs(a - b) for ra, rb in zip(O['Car_Root'].matrix_world, Matrix.Identity(4)) for a, b in zip(ra, rb)), max_rotation_dev=rot, max_scale_dev=scl, negative_scale=neg,
                 lod0_dims_m=dims_u, nose_z=round(float(mx[2]), 4), tail_z=round(float(mn[2]), 4), roof_y=round(float(mx[1]), 4), ground_y=round(float(mn[1]), 4),
                 center_of_mass=[round(-O['CenterOfMass'].matrix_world.translation.x, 4), round(O['CenterOfMass'].matrix_world.translation.y, 4), round(O['CenterOfMass'].matrix_world.translation.z, 4)])
    if unity['car_root_identity'] > 1e-5 or rot > 1e-5 or scl > 1e-5 or neg: pr.append(f'transforms {unity}')
    fl_ = O['WheelColliderRef_FL'].matrix_world.translation
    if not (unity['nose_z'] > 0 > unity['tail_z'] and abs(unity['ground_y']) < .01 and -fl_.x < 0 and fl_.z > 0): pr.append(f'unity orientation {unity}')
    R.update(lods=lods, wheels=wheels, max_pivot_dev_vs_source_m=pdev, center_of_mass_blender=[round(x, 4) for x in com], colliders=colinfo, light_channels=light, normals=nrm, unity_space=unity, problems=pr, ok=not pr)
    OUT['files'][fname] = R; allok &= not pr
    print('AUDIT', fname, 'PASS' if not pr else 'FAIL', '; '.join(pr)[:600], flush=True)
OUT['ok'] = allok
json.dump(OUT, open(os.path.join(WSV, 'reports', f'{PFX}_fbx_audit.json'), 'w'), indent=1, default=str)
print('AUDIT RESULT', 'PASS' if allok else 'FAIL', flush=True)
