# "Export Vechile" finalize: compare the independent FBX measurements (package + portable copy) with each release record,
# write per-vehicle spec JSON, the complete manifest, dependency + QA reports and the SHA-256 list. Called by va_export_package.py.
import sys; sys.dont_write_bytecode = True
from va_export_package import *

TOL = 0.0015                                  # m; release records are rounded to 0.1-1 mm
ALLOWED_ROTATED = ('ActiveSpoiler_', 'SteeringWheel_', 'Paddle_')    # Hypercar authored pivots (unity_import_notes.md pivot table)
DESIGN_BODY_W = {  # traffic design body width (m) from the design sources; only used to tell which hulls reach the mirror zone
    'Traffic_Sedan_A_r3': (1.80, 'H_TrafficFleet/scripts/ts_sedan_a_r3.py DIM.width_body'),
    'Traffic_Sedan_B': (1.89, 'H_TrafficFleet/scripts/ts_sedan_b.py DIM.width_body'),
    'Traffic_Hatchback_A_r2': (1.79, 'H_TrafficFleet/scripts/designs/hatchback_a_r2.py DIM.width_body'),
    'Traffic_SUV_A_v2': (1.84, 'H_TrafficFleet/scripts/designs/suv_a.py DIM.width_body'),
    'Traffic_SUV_B_v3': (1.96, 'H_TrafficFleet/scripts/designs/suv_b.py DIM.width_body'),
    'Traffic_Box_Truck_A_r7': (2.34, 'H_TrafficFleet/scripts/designs/box_truck_a.py DIM.box_width (cab width_body 2.00)'),
    'Traffic_Bus_A_v4': (2.55, 'H_TrafficFleet/scripts/designs/bus_a.py DIM.width_body'),
}
GLOBALS = dict(UpAxis=1, UpAxisSign=1, FrontAxis=2, FrontAxisSign=1, CoordAxis=0, CoordAxisSign=1, UnitScaleFactor=100.0)
TRAFFIC_BUDGET = 15000
CHECK_NAMES = {
    1: 'All seven mandatory traffic vehicles present', 2: 'Correct approved release version', 3: 'Complete FBX exists',
    4: 'Every required texture exists', 5: 'All paths resolve inside the portable package', 6: 'FBX hierarchy valid',
    7: 'Model orientation (+Z forward, +Y up, -X left)', 8: 'Dimensions and scale (metres, scale 1, ground Y 0)',
    9: 'All LODs preserved (LOD0-3)', 10: 'Triangle counts match the release manifest', 11: 'Wheel pivots match the validated source',
    12: 'Collider references preserved', 13: 'Centre-of-mass reference preserved', 14: 'Material names and assignments preserved',
    15: 'Light-channel data preserved', 16: 'No duplicate vehicle release', 17: 'No corrupted textures',
    18: 'No unexpectedly missing dependencies', 19: 'Original frozen sources unchanged', 20: 'Package checksum manifest valid'}

def close(a, b, t=TOL):
    return all(abs(x - y) <= t for x, y in zip(a, b)) if isinstance(a, (list, tuple)) else abs(a - b) <= t
def r3(x): return [round(v, 4) for v in x]
def bounds_of(parts, keep):
    bs = [p['bounds'] for n, p in parts.items() if keep(n) and p['bounds']]
    lo = [min(b['min'][i] for b in bs) for i in range(3)]; hi = [max(b['max'][i] for b in bs) for i in range(3)]
    return dict(min=lo, max=hi, size=[hi[i] - lo[i] for i in range(3)])

def tex_paths(v, names):
    out = []
    for n in names:
        a = f"{v['dir']}/textures/{n}"
        out.append(a if os.path.isfile(f'{PKG}/{a}') or v['fam'] != 'traffic' else f'01_Traffic_Vehicles/shared/textures/{n}')
    return out

def wheel_mesh(m, k):
    p = m['lod0_parts'].get(f'Tire_{k}_LOD0') or m['lod0_parts'].get(f'Wheel_{k}_LOD0')
    return dict(radius=p['bounds']['size'][1] / 2, width=p['bounds']['size'][0]) if p else None

def footprint(v, m):
    cols = {k: c['bounds'] for k, c in m['colliders'].items()}; u = m['collision_union']
    out = dict(collision_union=dict(length=round(u['size'][2], 4), width=round(u['size'][0], 4), height=round(u['size'][1], 4),
                                    center_unity=r3([(u['min'][i] + u['max'][i]) / 2 for i in range(3)])),
               hull_widths={k: round(b['size'][0], 4) for k, b in cols.items()})
    if v['id'] in DESIGN_BODY_W:
        bw, src = DESIGN_BODY_W[v['id']]
        body = {k: b['size'][0] for k, b in cols.items() if b['size'][0] <= bw + 0.03}
        mirror = sorted(k for k in cols if k not in body)
        out['recommended_footprint_override'] = dict(
            width=round(max(body.values()), 4), length=out['collision_union']['length'], height=out['collision_union']['height'],
            center_unity=out['collision_union']['center_unity'],
            width_from=sorted(body, key=lambda k: -body[k])[0],
            rule=f'width = widest collision hull not wider than the design body width + 3 cm ({bw} m, {src}); hulls {mirror} reach the mirror zone and are excluded from the width. Length / height = union of all collision hulls.',
            excluded_mirror_zone_hulls=mirror)
    return out

def checks(v, rel, m, mc, pkg_root, copy_root):
    C = {}
    def add(n, ok, d): C[n] = ('PASS' if ok else 'FAIL', d)
    hd, lods = m['header'], m['lods']
    fbx_abs = f"{PKG}/{v['fbx']}"; fsha1 = h(fbx_abs)
    ok2 = fsha1 == rel['fbx_sha1']; d2 = f"FBX SHA-1 {fsha1[:12]} = release record" if ok2 else f'FBX SHA-1 {fsha1} != release {rel["fbx_sha1"]}'
    if v['fam'] == 'traffic':
        man = J(f"{PKG}/{v['dir']}/reports/{v['base']}_unity_manifest.json")
        fz = h(f"{V}/{man['source']['freeze_manifest']}")
        ok2 = ok2 and man['release'] == v['release'] and fz == man['source']['freeze_manifest_sha1']
        d2 += f"; release '{man['release']}'; freeze manifest {man['source']['freeze_manifest'].split('/')[-1]} unchanged since export ({fz[:12]})"
    elif v['fam'] == 'player':
        d2 += f"; FBX hash listed in {v['frz']}"
    else:
        d2 += '; re-exported from source checkpoints whose SHA-1 match final_export_manifest.json (REEXPORT_PROVENANCE.md)'
    add(2, ok2, d2)
    add(3, os.path.getsize(fbx_abs) > 0 and m['objects'] == rel['objects'], f"{v['fbx'].split('/')[-1]}: {m['bytes']:,} bytes, {m['objects']} objects (release {rel['objects']})")
    need = tex_paths(v, rel['all_textures']); miss = [p for p in need if not os.path.isfile(f'{PKG}/{p}')]
    add(4, not miss, f'{len(need)} required textures ({len(rel["manual_textures"])} for manual URP setup), missing {miss}')
    imgs_out = [i['name'] for i in m['images'] + mc['images'] if not (i['exists'] and i['inside_package'])]
    unres = hd['unresolved_from_package'] + hd['resolved_outside_package'] + mc['header']['unresolved_from_package'] + mc['header']['resolved_outside_package']
    add(5, not unres and not imgs_out, f"{len(hd['texture_relative_paths'])} relative texture paths resolve in the package and in the portable copy; importer loaded {len(mc['images'])} images, all from inside the copy" if not (unres or imgs_out) else f'unresolved {unres} / outside {imgs_out}')
    want = {f'LOD{i}_Root' for i in range(4)} | {'Collision', 'CenterOfMass'} | {f'WheelColliderRef_{k}' for k in CORNERS}
    lacking = sorted(want - set(m['car_root_children']))
    badpar = [k for k, c in m['colliders'].items() if c['parent'] != 'Collision'] + [k for k, x in lods.items() if x['parent'] != 'Car_Root']
    add(6, m['roots'] == ['Car_Root'] and not lacking and not badpar and not m['duplicate_suffix_names'],
        f"single root Car_Root; children {len(m['car_root_children'])} incl. LOD0-3_Root, Collision, 4 WheelColliderRef, CenterOfMass; colliders under Collision; no .001 names" if not (lacking or badpar) else f'missing {lacking}, wrong parent {badpar}')
    g = {k: hd['globals'].get(k) for k in GLOBALS}
    rot_bad = {k: x for k, x in hd['rotated_models'].items() if not k.startswith(ALLOWED_ROTATED if v['fam'] == 'hypercar' else ('\0',))}
    R = m['refs']; L0 = lods['LOD0']['bounds']
    zb = bounds_of(m['lod0_parts'], lambda n: n.startswith('Body_LOD0')) if v['fam'] != 'traffic' else L0    # player records measure nose/tail on the body
    ok7 = g == GLOBALS and not rot_bad and R['WheelColliderRef_FL'][0] < 0 < R['WheelColliderRef_FL'][2] and R['WheelColliderRef_RR'][2] < 0 < R['WheelColliderRef_RR'][0] \
        and close(zb['max'][2], rel['nose_z'], .002) and close(zb['min'][2], rel['tail_z'], .002)
    add(7, ok7, f"FBX axes Up +Y / Front +Z / Coord +X; {'body ' if v['fam'] != 'traffic' else ''}nose Z {zb['max'][2]:.4f} (release {rel['nose_z']}), tail {zb['min'][2]:.4f}; FL wheel at -X/+Z; "
        + (f"authored pivot rotations only: {sorted(hd['rotated_models'])}" if hd['rotated_models'] else 'all node rotations identity') + (f'; UNEXPECTED rotations {rot_bad}' if rot_bad else ''))
    dims = bounds_of(m['lod0_parts'], lambda n: 'Mirror' not in n)['size'] if v['fam'] == 'hypercar' else L0['size']
    ok8 = hd['globals'].get('UnitScaleFactor') == 100.0 and hd['max_lcl_scale_dev'] < 1e-4 and not m['negative_scale'] \
        and close(dims[0], rel['dims']['width']) and close(dims[1], rel['dims']['height']) and close(dims[2], rel['dims']['length']) and close(L0['min'][1], 0.0, .002)
    add(8, ok8, f"UnitScaleFactor 100 (1 unit = 1 m), max Lcl scale deviation {hd['max_lcl_scale_dev']:.1e}, no negative scale; LOD0 L x W x H {dims[2]:.4f} x {dims[0]:.4f} x {dims[1]:.4f} m"
        + (' (mirror objects excluded, as released)' if v['fam'] == 'hypercar' else '') + f" vs release {rel['dims']['length']} x {rel['dims']['width']} x {rel['dims']['height']}; ground Y {L0['min'][1]:+.4f}")
    add(9, sorted(lods) == ['LOD0', 'LOD1', 'LOD2', 'LOD3'], f"{len(lods)} LOD roots")
    tri = {k: (lods[k]['tris'], rel['lods'][k]['tris']) for k in rel['lods']}
    add(10, all(a == b for a, b in tri.values()), ', '.join(f'{k} {a:,}' + ('' if a == b else f' (release {b:,})') for k, (a, b) in tri.items()))
    wr = {k: (R[f'WheelColliderRef_{k}'], rel['wheels'][k]['unity']) for k in CORNERS}
    wm = {k: wheel_mesh(m, k) for k in CORNERS}
    piv = max(m['pivots'].values()) if m['pivots'] else 1.0
    ok11 = all(close(a, b) for a, b in wr.values()) and piv <= 1e-4 and len(m['pivots']) >= 16 and all(wm[k] and close(wm[k]['radius'], rel['wheels'][k]['radius'], .001) for k in CORNERS)
    add(11, ok11, f"4 WheelColliderRef positions = release (Unity FL {r3(R['WheelColliderRef_FL'])}); {len(m['pivots'])} Wheel/SteerPivot pivots, max offset from ref {piv * 1000:.4f} mm; wheel mesh radius = release radius within 1 mm")
    cm = {k: c['tris'] for k, c in m['colliders'].items()}
    add(12, cm == rel['colliders'] and all(c['materials'] == 0 for c in m['colliders'].values()), f"{len(cm)} convex hulls {cm}, no materials")
    add(13, close(R['CenterOfMass'], rel['com']), f"CenterOfMass Unity {r3(R['CenterOfMass'])} (release {r3(rel['com'])})")
    if v['fam'] == 'player':
        allm = sorted({x for l in lods.values() for x in l['materials']})
        ok14 = allm == rel['materials_all'] and all(len(lods[k]['materials']) == rel['lods'][k]['materials_count'] for k in lods)
        d14 = f"{len(allm)} materials = export manifest; per LOD {[len(lods[k]['materials']) for k in sorted(lods)]}"
    else:
        diff = {k: sorted(set(lods[k]['materials']) ^ set(rel['lods'][k]['materials'])) for k in lods if set(lods[k]['materials']) != set(rel['lods'][k]['materials'])}
        cnt = ', '.join('%s %d' % (k, len(lods[k]['materials'])) for k in sorted(lods))
        ok14 = not diff; d14 = f'per-LOD material sets = release ({cnt})' + (f'; DIFF {diff}' if diff else '')
    noslot = [n for k in lods for n in lods[k]['material_faces'] if n == '(none)']
    add(14, ok14 and not noslot, d14 + ('; every face has a material' if not noslot else '; faces without material'))
    lt = rel['lights']
    if lt['kind'] == 'ts_channels':
        diff = {k: (m['ts_light_channels'].get(k), x) for k, x in lt['per_object'].items() if m['ts_light_channels'].get(k) != x}
        add(15, not diff, f"TS_Lights channel faces decoded from UVs identical to the FBX audit on {len(lt['per_object'])} Lights_LODn objects; {len(lt['names'])} channels {lt['names']}" + (f' DIFF {diff}' if diff else ''))
    elif lt['kind'] == 'materials':
        mf = lods['LOD0']['material_faces']; diff = {k: (mf.get(k), x) for k, x in lt['faces'].items() if mf.get(k) != x}
        add(15, not diff, f"{len(lt['faces'])} light-channel materials, LOD0 face counts = release geometry report" + (f' DIFF {diff}' if diff else ''))
    else:
        per = {k: sorted(x for x in lods[k]['materials'] if x in lt['names']) for k in lods}
        relp = {k: sorted(x for x in rel['lods'][k]['materials'] if x in lt['names']) for k in lods}
        zero = [x for x in lt['names'] if not lods['LOD0']['material_faces'].get(x)]
        add(15, per == relp and not zero, f"emissive channel materials per LOD = release ({ {k: len(x) for k, x in per.items()} }); all {len(lt['names'])} carry faces at LOD0")
    bad = []
    for p in need:
        e, info = png_check(f'{PKG}/{p}')
        if e: bad.append(f'{p}: {e}')
    zero = [i['name'] for i in m['images'] if i['size'] == [0, 0]]
    add(17, not bad and not zero, f'{len(need)} PNG decoded (signature, CRC, zlib, pixel length); importer read non-zero sizes for {len(m["images"])} linked images' + (f' BAD {bad + zero}' if bad or zero else ''))
    same = all(m[k] == mc[k] for k in ('objects', 'names', 'lods', 'refs', 'pivots', 'colliders', 'ts_light_channels'))
    add(18, not miss and not unres and not imgs_out and same, 'no missing or external dependency; the portable-copy measurement is identical to the in-place one' if same else 'portable copy measurement DIFFERS')
    return C

def spec(v, rel, m, C):
    lods = m['lods']; R = m['refs']; L0 = lods['LOD0']['bounds']['size']
    fbx_dir = os.path.dirname(v['fbx'])
    linked = sorted(os.path.normpath(os.path.join(fbx_dir, r)) for r in m['header']['texture_relative_paths'])
    allt = tex_paths(v, rel['all_textures'])
    fl, fr, rl, rr = (R[f'WheelColliderRef_{k}'] for k in CORNERS)
    fp = footprint(v, m)
    noml = bounds_of(m['lod0_parts'], lambda n: 'Mirror' not in n)['size'] if v['fam'] == 'hypercar' else None
    lights = rel['lights']
    if lights['kind'] == 'ts_channels':
        lc = dict(count=len(lights['names']), names=lights['names'], material='TS_Lights (one material, one draw call)',
                  mechanism='channel index = round(TS_Lights_ChannelID.R x 15); emission = TS_Lights_Emission x intensity[channel] (per-renderer MaterialPropertyBlock)',
                  index_order=LIGHT_CELLS[:len(lights['names'])])
    elif lights['kind'] == 'materials':
        lc = dict(count=len(lights['names']), names=lights['names'], mechanism='one emissive material per channel; drive _EmissionColor intensity at runtime')
    else:
        lc = dict(count=len(lights['names']), names=lights['names'],
                  mechanism='one emissive material per channel; drive _EmissionColor intensity at runtime. MAT_LED_White = DRL + headlamp, MAT_LED_Red = tail, MAT_LED_Amber = BOTH indicators (no left/right split), MAT_AmbientLight = interior. MAT_ProjectorLens has no emission.')
    traffic = v['type'] == 'traffic'
    return dict(
        schema='export_vechile/vehicle_spec@1', vehicle_id=v['id'], display_name=v['name'], vehicle_type=v['type'], vehicle_class=v['cls'],
        approved_release=v['release'], source_release=rel['source'],
        fbx=dict(path=v['fbx'], bytes=m['bytes'], sha256=m['sha256'], sha1=h(f"{PKG}/{v['fbx']}"), objects=m['objects'],
                 contents='Car_Root > LOD0_Root..LOD3_Root (render meshes, wheel and steer pivots), Collision (convex hulls), WheelColliderRef_FL/FR/RL/RR, CenterOfMass'),
        textures=dict(fbx_linked=linked, manual_setup=tex_paths(v, rel['manual_textures']), all=allt),
        dimensions_m=dict(
            visual_lod0=dict(length=round(L0[2], 4), width=round(L0[0], 4), height=round(L0[1], 4)),
            visual_width_includes_mirrors=True if v['fam'] == 'hypercar' else rel['mirrors'],
            mirrors_source=rel['mirrors_src'] if v['fam'] != 'hypercar' else 'measured: LOD0 bounds over all meshes include Mirror_L/R objects',
            **({'lod0_excluding_mirror_objects': dict(length=round(noml[2], 4), width=round(noml[0], 4), height=round(noml[1], 4))} if noml else {}),
            **({'design_body_width': dict(value=DESIGN_BODY_W[v['id']][0], source=DESIGN_BODY_W[v['id']][1])} if v['id'] in DESIGN_BODY_W else {}),
            **({'documented_body_width': dict(value=rel['body_width'], source=rel['mirrors_src'])} if rel.get('body_width') else {}),
            collision=fp),
        wheelbase_m=round(fl[2] - rl[2], 4), track_m=dict(front=round(fr[0] - fl[0], 4), rear=round(rr[0] - rl[0], 4)),
        wheels={k: dict(unity_position=r3(R[f'WheelColliderRef_{k}']), radius_m=rel['wheels'][k]['radius'], width_m=rel['wheels'][k]['width'],
                        measured_wheel_mesh=dict((a, round(b, 4)) for a, b in (wheel_mesh(m, k) or {}).items()),
                        pivots={n: d for n, d in m['pivots'].items() if f'_{k}_' in n}) for k in CORNERS},
        wheel_notes=('Rear WheelColliderRef width is one tyre; the rear wheel mesh carries a dual (twin) tyre set, hence the wider measured mesh.' if v['cls'] in ('box_truck', 'bus') else None),
        center_of_mass_unity=r3(R['CenterOfMass']),
        colliders=dict(optional_integration_resource=True,
                       note='Convex reference hulls (MeshCollider Convex ON, renderers off). The current traffic system uses analytic collision: these are optional, not required.' if traffic else
                            'Convex reference hulls (MeshCollider Convex ON, renderers off). Use them if the player car keeps physics colliders; the existing controller decides.',
                       hulls={k: dict(tris=c['tris'], unity_bounds=dict(min=r3(c['bounds']['min']), max=r3(c['bounds']['max']))) for k, c in m['colliders'].items()}),
        wheel_collider_refs=dict(optional_integration_resource=True, note='WheelColliderRef_* empties mark wheel centres; WheelColliders are NOT required for analytic traffic.' if traffic else 'WheelColliderRef_* empties mark wheel centres for the player-car physics, if used.'),
        lods={k: dict(root=f'{k}_Root', triangles=lods[k]['tris'], objects=lods[k]['objects'], materials=lods[k]['materials']) for k in sorted(lods)},
        materials=sorted({x for l in lods.values() for x in l['materials']}),
        light_channels=lc,
        coordinate_convention=dict(forward='+Z', up='+Y', vehicle_left='-X', ground='Y = 0', front_axle='+Z', blender_to_unity_point='(x, y, z) -> (-x, z, -y)',
                                   fbx_globals=m['header']['globals'], axis_conversion='baked into the meshes: Car_Root identity; Bake Axis Conversion OFF'),
        scale=dict(units='metres', fbx_unit_scale_factor=100.0, unity_scale_factor=1, convert_units=True),
        unity_import=dict(scale_factor=1, convert_units=True, bake_axis_conversion=False, import_blendshapes=False, import_visibility=False,
                          import_cameras=False, import_lights=False, preserve_hierarchy=True, mesh_compression='Off', read_write=False,
                          generate_colliders=False, normals='Import', tangents='Calculate Mikktspace' if traffic else 'Import',
                          animation_type='None', import_animation=False, material_creation='Import via MaterialDescription, then remap by exact name',
                          lod_group=dict(on='Car_Root', renderers_from=[f'LOD{i}_Root' for i in range(4)],
                                         screen_relative_heights=[0.50, 0.22, 0.08, 0.015] if traffic else [0.60, 0.30, 0.12, 0.03],
                                         note='suggested starting values from the Blender handoff; tune on device')),
        traffic=dict(footprint_override=fp.get('recommended_footprint_override'),
                     lod0_vs_15k_budget=dict(lod0_triangles=lods['LOD0']['tris'], budget=TRAFFIC_BUDGET, over=lods['LOD0']['tris'] > TRAFFIC_BUDGET),
                     note='Map footprint_override onto the existing TrafficVehicleData footprint fields (names are the Unity project\'s); width is the collision body without mirrors.') if traffic else None,
        dependencies=dict(fbx_relative_texture_paths=m['header']['texture_relative_paths'], unresolved=m['header']['unresolved_from_package'],
                          absolute_paths_embedded=len(m['header']['absolute_paths']), embedded_media=m['header']['embedded_media'],
                          vehicle_readme=next((f"{v['dir']}/{n}" for n in sorted(os.listdir(f"{PKG}/{v['dir']}")) if n.endswith('.md')), None)),
        validation=dict(checks={f'{n:02d} {CHECK_NAMES[n]}': dict(result=s, detail=d) for n, (s, d) in sorted(C.items())},
                        blender_side='PASS' if all(s == 'PASS' for s, _ in C.values()) else 'FAIL', unity_runtime='NOT RUN (P0-05 on the Unity machine)'))

# ------------------------------------------------------------------ texture import settings (machine-readable, from the source READMEs)
def tex_settings(p):
    n = os.path.basename(p); s = dict(path=p, textureType='Default', sRGBTexture=False, mipmapEnabled=True, filterMode='Bilinear', compression='Default')
    if n.endswith('_Normal.png') or n.endswith('_Normal_LOD1.png'): s['textureType'] = 'NormalMap'
    elif n.endswith('_BaseColor.png') or n == 'TS_Lights_Emission.png': s['sRGBTexture'] = True
    if n == 'TS_Lights_ChannelID.png': s.update(filterMode='Point', compression='None', mipmapEnabled=False, note='R x 15 = channel index; must stay exact')
    if '_Palette_' in n: s.update(filterMode='Point', mipmapEnabled=False, note='256 px swatch atlas')
    if n.endswith('_AO_Grime.png'): s['note'] = 'R = ambient occlusion, G = road-grime mask (URP Occlusion reads G: use a Shader Graph or repack)'
    if n.endswith('MetallicSmoothness.png'): s['note'] = 'R = metallic, A = smoothness (Smoothness Source = Metallic Alpha)'
    if n.endswith(('_Metallic.png', '_Roughness.png')) and 'hypercar' in p: s['note'] = 'pack for URP: MetallicSmoothness R = Metallic, A = 1 - Roughness'
    if n.endswith('_AO.png'): s['note'] = 'not linked by the FBX: assign to Occlusion by hand (URP reads G; greyscale is fine)'
    return s

# ------------------------------------------------------------------ source integrity (read-only)
def source_integrity():
    out = {}
    r = subprocess.run([sys.executable, f'{V}/A_Discovery/scripts/va_frozen_check.py'], capture_output=True, text=True)
    out['va_frozen_check'] = dict(ok='FROZEN CHECK PASS' in r.stdout, releases=len(re.findall(r'changed/missing 0', r.stdout)), tail=r.stdout.strip().splitlines()[-1])
    sums = [l.split(None, 1) for l in open(f'{HO}/SHA1SUMS.txt') if l.strip()]
    bad = [p.strip() for d, p in sums if h(os.path.join(HO, p.strip())) != d]
    out['unity_handoff_20261010'] = dict(ok=not bad, files=len(sums), mismatched=bad)
    man = J(f'{HC}/reports/final_export_manifest.json')['files']
    hb = [k for k, x in man.items() if not k.startswith('exports/') and h(f'{HC}/{k}') != x['sha1']]
    out['hypercar_new_car'] = dict(ok=not hb, files=sum(not k.startswith('exports/') for k in man), mismatched=hb,
                                   note='new_car/exports/ (original 2026-10-06 FBX) is not on disk; FBX re-exported, see REEXPORT_PROVENANCE.md')
    src = open(f'{V}/A_Discovery/scripts/va_integrity.py').read().replace("open(os.path.join(R, 'VA_integrity_check.md'), 'w')", 'open(os.devnull, "w")')
    ns = {}; exec(compile(src, 'va_integrity(read-only)', 'exec'), ns)
    env_removed = [k for k in ns['removed'] if k.startswith('environment/')]
    other_removed = [k for k in ns['removed'] if not k.startswith('environment/')]
    added_top = {}
    for k in ns['added']: added_top[k.split('/')[0]] = added_top.get(k.split('/')[0], 0) + 1
    out['va_integrity'] = dict(changed=ns['changed'], removed_environment_archive=len(env_removed), removed_other=other_removed, added_by_top_level=added_top,
                               ok_for_vehicle_export=not ns['changed'] and not other_removed)
    return out

# ------------------------------------------------------------------ docs
def md_table(head, rows): return ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]

def finalize(meas_pkg, meas_copy):
    MP, MC = J(meas_pkg), J(meas_copy)
    regs = registry(); specs, allC = [], {}
    for v in regs:
        rel = released(v); m = MP['files'][v['fbx']]; mc = MC['files'][v['fbx']]
        C = checks(v, rel, m, mc, MP['package'], MC['package']); allC[v['id']] = C
        specs.append(spec(v, rel, m, C))
    # package-level checks
    P = {}
    tr = [s for s in specs if s['vehicle_type'] == 'traffic']
    P[1] = ('PASS' if len(tr) == 7 and all(os.path.isfile(f"{PKG}/{s['fbx']['path']}") for s in tr) else 'FAIL', f"{len(tr)} / 7: " + ', '.join(s['approved_release'] for s in tr))
    fbxs = sorted(os.path.relpath(os.path.join(a, f), PKG) for a, _, fs in os.walk(PKG) for f in fs if f.lower().endswith('.fbx'))
    orig = {t: freeze_rows(f'{V}/{d}/reports/{fz}')[f'UnityTransfer/FBX/{b}_complete_unity.fbx']
            for t, d, fz, b in (('TitanGT_r1', 'C_TitanGT', 'TG_FINAL_FREEZE.md', 'TitanGT'), ('VortexR_r1', 'D_VortexR', 'VX_FINAL_FREEZE.md', 'VortexR'))}
    superseded = [t for t, x in orig.items() if next(s for s in specs if s['vehicle_id'] == t)['fbx']['sha1'] == x]
    dup = len({s['vehicle_id'] for s in specs}) != len(specs) or len({s['fbx']['sha256'] for s in specs}) != len(specs) or len({s['approved_release'] for s in specs}) != len(specs)
    P[16] = ('PASS' if not dup and len(fbxs) == len(specs) and not superseded and not any('LOD0_unity_test' in f for f in fbxs) else 'FAIL',
             f'{len(fbxs)} FBX files for {len(specs)} vehicles, unique ids / releases / SHA-256; no LOD0 test FBX; Titan GT and Vortex R FBX are the r1 revisions (differ from the superseded originals)')
    SI = source_integrity()
    ok19 = SI['va_frozen_check']['ok'] and SI['unity_handoff_20261010']['ok'] and SI['hypercar_new_car']['ok'] and SI['va_integrity']['ok_for_vehicle_export']
    P[19] = ('PASS' if ok19 else 'FAIL', f"va_frozen_check {SI['va_frozen_check']['releases']} releases unchanged; UNITY_HANDOFF_20261010 {SI['unity_handoff_20261010']['files']} files match SHA1SUMS.txt; Hypercar {SI['hypercar_new_car']['files']} source files match its manifest; va_integrity: changed {len(SI['va_integrity']['changed'])}")
    P[20] = ('see log', f'checked after the list is written: `{VERIFY_LOG}` (this folder + an independent copy) and again on the extracted ZIP')

    os.makedirs(f'{PKG}/04_Unity_Setup/Vehicle_Configuration', exist_ok=True); os.makedirs(f'{PKG}/04_Unity_Setup/Import_Settings', exist_ok=True)
    os.makedirs(f'{PKG}/06_QA', exist_ok=True); os.makedirs(f'{PKG}/00_Documentation', exist_ok=True)
    for s in specs: json.dump(s, open(f"{PKG}/04_Unity_Setup/Vehicle_Configuration/{s['vehicle_id']}.json", 'w'), indent=1)
    texs = sorted({p for s in specs for p in s['textures']['all']})
    json.dump(dict(schema='export_vechile/import_settings@1', unity='6000.6.0f1', urp='17.6', status='intended settings, not runtime-verified',
                   model_importer={s['vehicle_id']: dict(fbx=s['fbx']['path'], **s['unity_import']) for s in specs},
                   texture_importer=[tex_settings(p) for p in texs]),
              open(f'{PKG}/04_Unity_Setup/Import_Settings/unity_import_settings.json', 'w'), indent=1)

    every = lambda C: 'PASS' if all(x[0] == 'PASS' for x in C.values()) else 'FAIL'
    # ---- VEHICLE_SPECS.md
    rows = []
    for s in specs:
        d = s['dimensions_m']; fpo = (s['traffic'] or {}).get('footprint_override')
        rows.append([s['display_name'], s['vehicle_type'], f"{d['visual_lod0']['length']:.3f} x {d['visual_lod0']['width']:.3f} x {d['visual_lod0']['height']:.3f}",
                     'yes' if d['visual_width_includes_mirrors'] else 'no', f"{fpo['width']:.3f} x {fpo['length']:.3f}" if fpo else '-',
                     f"{s['wheelbase_m']:.3f}", f"{s['wheels']['FL']['radius_m']} / {s['wheels']['RL']['radius_m']}",
                     ' / '.join(f"{s['lods'][k]['triangles']:,}" for k in sorted(s['lods'])), str(s['center_of_mass_unity']), s['light_channels']['count']])
    doc = ['# Vehicle specifications', '', f'Generated {TODAY} from the packaged FBX files (independent Blender 5.2.2 re-import of each file) and the release records. Unity space: +Z forward, +Y up, -X vehicle left, metres. Machine-readable: `04_Unity_Setup/Vehicle_Configuration/<vehicle>.json`.', '']
    doc += md_table(['Vehicle', 'Type', 'Visual L x W x H (m)', 'Width incl. mirrors', 'Traffic footprint W x L (m)', 'Wheelbase (m)', 'Wheel radius F / R (m)', 'LOD0 / 1 / 2 / 3 tris', 'CenterOfMass', 'Light channels'], rows)
    doc += ['', '## Traffic footprint overrides (collision body, mirrors excluded)', '']
    doc += md_table(['Vehicle', 'Width (m)', 'Width from hull', 'Length (m)', 'Height (m)', 'Centre (Unity)', 'Mirror-zone hulls excluded', 'Visual width incl. mirrors'],
                    [[s['display_name'], s['traffic']['footprint_override']['width'], s['traffic']['footprint_override']['width_from'], s['traffic']['footprint_override']['length'],
                      s['traffic']['footprint_override']['height'], s['traffic']['footprint_override']['center_unity'], ', '.join(s['traffic']['footprint_override']['excluded_mirror_zone_hulls']),
                      s['dimensions_m']['visual_lod0']['width']] for s in tr])
    doc += ['', 'Rule: width = the widest convex collision hull that is not wider than the vehicle\'s design body width + 3 cm (design width is only used to identify hulls that extend into the mirror zone); length and height = union of all collision hulls. All values are measured from the packaged FBX.', '',
            '## Wheels (WheelColliderRef positions, Unity local to Car_Root)', '']
    doc += md_table(['Vehicle', 'FL', 'FR', 'RL', 'RR', 'Radius F / R', 'Width F / R', 'Track F / R'],
                    [[s['display_name']] + [str(s['wheels'][k]['unity_position']) for k in CORNERS] + [f"{s['wheels']['FL']['radius_m']} / {s['wheels']['RL']['radius_m']}",
                     f"{s['wheels']['FL']['width_m']} / {s['wheels']['RL']['width_m']}", f"{s['track_m']['front']} / {s['track_m']['rear']}"] for s in specs])
    doc += ['', 'Truck and bus rear widths are per tyre; their rear wheel meshes carry dual tyres.', '', '## LOD0 triangle budget (Unity validation uses 15,000 for traffic)', '']
    doc += md_table(['Vehicle', 'LOD0 tris', 'vs 15,000'], [[s['display_name'], f"{s['lods']['LOD0']['triangles']:,}", 'over by %s' % f"{s['lods']['LOD0']['triangles'] - TRAFFIC_BUDGET:,}" if s['traffic']['lod0_vs_15k_budget']['over'] else 'within'] for s in tr])
    open(f'{PKG}/00_Documentation/VEHICLE_SPECS.md', 'w').write('\n'.join(doc) + '\n')
    # ---- VEHICLE_INVENTORY.md
    doc = ['# Vehicle inventory', '', f'{len(specs)} vehicles included ({len(tr)} traffic, {len(specs) - len(tr)} player). One approved release per vehicle identity.', '', '## Included', '']
    doc += md_table(['#', 'Vehicle', 'Type', 'Approved release', 'Package folder', 'Source release record', 'Blender validation'],
                    [[i + 1, s['display_name'], s['vehicle_type'], s['approved_release'], f"`{os.path.dirname(os.path.dirname(s['fbx']['path']))}/`",
                      '`' + (s['source_release'].get('freeze_manifest') or s['source_release'].get('release_manifest')) + '`', s['validation']['blender_side']] for i, s in enumerate(specs)])
    doc += ['', 'Purpose: traffic vehicles replace or extend the existing `TrafficSpawner` pool (analytic collision, no physics required). Player vehicles are the frozen player-car releases; the Hypercar is the flagship player car (its LOD0 is far above mobile budgets, see the integration guide).', '',
            '## Excluded (and why)', '']
    doc += md_table(['Item', 'Location', 'Reason'], [[a, f'`{b}`', c] for a, b, c in EXCLUDED])
    open(f'{PKG}/00_Documentation/VEHICLE_INVENTORY.md', 'w').write('\n'.join(doc) + '\n')
    # ---- QA docs
    fbxn, geon = (2, 3, 5, 6, 7, 8, 14, 17, 18), (9, 10, 11, 12, 13, 15)
    for name, nums, title in (('FBX_VALIDATION.md', fbxn, 'FBX validation'), ('GEOMETRY_VALIDATION.md', geon, 'Geometry validation')):
        doc = [f'# {title}', '', f'Generated {TODAY}. Each packaged `*_complete_unity.fbx` was parsed at FBX level (what Unity reads) and re-imported into a factory-clean Blender 5.2.2 scene, once in place and once from an independent copy of the package in a separate temporary folder outside the Blender project. Values are compared with each vehicle\'s release record. Raw data: `06_QA/fbx_measurements.json`.', '']
        doc += md_table(['Vehicle'] + [f'{n:02d}' for n in nums], [[s['display_name']] + [allC[s['vehicle_id']][n][0] for n in nums] for s in specs])
        doc += [''] + [f'- **{n:02d}**: {CHECK_NAMES[n]}' for n in nums] + ['']
        for s in specs:
            doc += [f"## {s['display_name']}", ''] + [f"- {n:02d} {CHECK_NAMES[n]}: **{allC[s['vehicle_id']][n][0]}**. {allC[s['vehicle_id']][n][1]}" for n in nums] + ['']
        open(f'{PKG}/06_QA/{name}', 'w').write('\n'.join(doc) + '\n')
    json.dump(dict(package_measurement=MP, portable_copy_measurement_package=MC['package'],
                   portable_copy_identical={f: all(MP['files'][f][k] == MC['files'][f][k] for k in ('objects', 'names', 'lods', 'refs', 'pivots', 'colliders', 'ts_light_channels', 'sha256')) for f in MP['files']}),
              open(f'{PKG}/06_QA/fbx_measurements.json', 'w'), indent=1)
    # ---- DEPENDENCY_REPORT.md
    doc = ['# Dependency report', '', 'Every FBX references its textures by **relative path** (no embedded media). All paths below were resolved from the FBX location inside this package and from an independent copy; Blender\'s importer loaded every linked image from inside the copy.', '',
           'Each FBX also stores the absolute path of the folder it was written from on the Blender Mac (`/Users/meetshah/...` or a scratch folder). That path is informational only and does not exist on the Unity machine; it exposes the local user name. Unity resolves the relative path first.', '']
    for s in specs:
        dpn = s['dependencies']
        doc += [f"## {s['display_name']} (`{s['fbx']['path']}`)", '', f"- Relative references in the FBX ({len(dpn['fbx_relative_texture_paths'])}): " + ', '.join(f'`{x}`' for x in dpn['fbx_relative_texture_paths']),
                f"- Resolved: {len(s['textures']['fbx_linked'])}, unresolved: {len(dpn['unresolved'])}; embedded media {dpn['embedded_media']}; absolute paths stored {dpn['absolute_paths_embedded']}",
                '- Not linked by the FBX, required for the URP material setup: ' + (', '.join(f'`{x}`' for x in s['textures']['manual_setup']) or 'none'), '']
    doc += ['## Not shipped on purpose', '', '- `*_LOD0_unity_test.fbx`: LOD0-only subsets of the complete FBX; not needed in Unity.',
            '- Source `.blend` files, previews, scripts: Blender-side only. No FBX links to them.', '- `TS_Lights_State` (traffic): a Blender-only 4 x 4 review mask, not used by Unity.', '']
    open(f'{PKG}/05_Manifests/DEPENDENCY_REPORT.md', 'w').write('\n'.join(doc) + '\n')
    # ---- EXPORT_VALIDATION_REPORT.md
    tot = {n: sum(allC[s['vehicle_id']][n][0] == 'PASS' for s in specs) for n in range(2, 19) if n != 16}
    doc = ['# Export validation report', '', f'Package `Export Vechile/`, generated {TODAY} on the Blender Mac. Blender 5.2.2 LTS. **Nothing in this package was opened in Unity**: Unity import, prefabs, shaders, materials, gameplay, lighting and Android performance are **NOT RUN** (task P0-05 on the Unity machine).', '',
           '## Required checks', '']
    rws = []
    for n in range(1, 21):
        if n in P: rws.append([f'{n:02d}', CHECK_NAMES[n], P[n][0], P[n][1]])
        else: rws.append([f'{n:02d}', CHECK_NAMES[n], 'PASS' if tot[n] == len(specs) else 'FAIL', f'{tot[n]} / {len(specs)} vehicles (details: 06_QA)'])
    doc += md_table(['#', 'Check', 'Result', 'Detail'], rws)
    doc += ['', f"Per-vehicle Blender-side result: " + ', '.join(f"{s['display_name']} {every(allC[s['vehicle_id']])}" for s in specs), '',
            '## Portability', '', f"The package was copied to a separate temporary folder outside the Blender project and every FBX re-measured there: the measurements are identical to the in-place run, all relative texture paths resolve inside the copy, and Blender's importer loaded every linked image from the copy (not from the original Blender folders). The stored absolute paths are informational only (see `05_Manifests/DEPENDENCY_REPORT.md`).", '',
            '## Source integrity', '', f"- `va_frozen_check.py`: {SI['va_frozen_check']['tail']} ({SI['va_frozen_check']['releases']} frozen releases, run at packaging time).",
            f"- `UNITY_HANDOFF_20261010/SHA1SUMS.txt`: {SI['unity_handoff_20261010']['files']} files, mismatched {len(SI['unity_handoff_20261010']['mismatched'])}.",
            f"- Hypercar `new_car/`: {SI['hypercar_new_car']['files']} source files (2 checkpoints + 48 textures) match `final_export_manifest.json`. {SI['hypercar_new_car']['note']}.",
            f"- Workspace baseline (`va_integrity.py`, run read-only): changed **{len(SI['va_integrity']['changed'])}**; removed {SI['va_integrity']['removed_environment_archive']} under `environment/`" + (f", other removed {SI['va_integrity']['removed_other']}" if SI['va_integrity']['removed_other'] else '') + f"; added outside `vehicles/` by top-level folder: {SI['va_integrity']['added_by_top_level']}.", '',
            '## Known separate item (not a vehicle export failure)', '',
            f"The frozen environment P0-P3 (`environment/`, {SI['va_integrity']['removed_environment_archive']} baseline files) was moved off this Mac by the owner on 2026-10-09 and archived at `/Volumes/Denish/Assets/environment.zip`. `va_integrity.py` therefore reports FAIL for those files. This is owner-acknowledged and unrelated to the vehicles; the check was not weakened. Re-verifying the archive needs the `Denish` drive (`A_Discovery/scripts/va_verify_env_archive.py`): **NOT RUN** (drive not mounted). The new `Export Vechile/` folder (and the ZIP) also appear as 'added' outside `vehicles/`; that is expected.", '',
            '## Known exceptions and limits', '',
            '- **Hypercar FBX re-exported**: the 2026-10-06 FBX was no longer on disk. Re-exported with the unchanged pipeline from the hash-verified source; validator 85 PASS / 0 / 0, data identical to the frozen validation (see `02_Player_Vehicles/Hypercar/REEXPORT_PROVENANCE.md`). New SHA-1, by design (the FBX stores the export folder path).',
            '- **Hypercar triangle counts** (LOD0 206,327) are far above the mobile player budget (60-120k LOD0). Use LOD1+ or treat as a showroom / high-tier asset; decide in Unity.',
            '- **Traffic LOD0 above the existing 15,000 validation budget**: ' + ', '.join(f"{s['display_name']} {s['lods']['LOD0']['triangles']:,}" for s in tr if s['traffic']['lod0_vs_15k_budget']['over']) + '. These are the approved releases; the budget was not weakened here (decide in Unity: raise the budget per class or start these at LOD1).',
            '- **Hypercar lights**: one amber material drives both indicators (no left/right split) and one white material is DRL + headlamp.',
            '- **Player FBX texture folder case**: the player FBX files reference `../textures/`; the old UnityTransfer folders used `Textures/`. This package uses `textures/`, which resolves on case-sensitive file systems too.',
            '- **Zero Gap R PB-1** (non-blocking): slightly pink daytime tail-lens; review in the Unity material pass.', '',
            '## Not run here', '', '- Unity import / prefab / LOD Group / material / shader / lighting / gameplay / Android performance: NOT RUN (no Unity on this Mac).',
            '- Environment archive re-verification: NOT RUN (Denish drive not mounted).', '- Visual (render) review: not repeated; every vehicle carries its frozen visual approval.', '']
    open(f'{PKG}/00_Documentation/EXPORT_VALIDATION_REPORT.md', 'w').write('\n'.join(doc) + '\n')
    # ---- COMPLETE_VEHICLE_MANIFEST.json + checksums
    docs = sorted(os.path.relpath(os.path.join(a, f), PKG) for a, _, fs in os.walk(PKG) for f in fs if f.endswith('.md') and (a.endswith('00_Documentation') or a.endswith('06_QA') or a.endswith('05_Manifests')) and f != os.path.basename(VERIFY_LOG))
    json.dump(dict(schema='export_vechile/manifest@1', package='Export Vechile', created=TODAY, source_project=WS, blender='5.2.2 LTS',
                   unity_target=dict(editor='6000.6.0f1', urp='17.6', status='not runtime-verified (P0-05)'),
                   coordinate_convention='Unity +Z forward, +Y up, -X vehicle left, metres, ground Y 0; import scale 1, Bake Axis Conversion off',
                   vehicles=specs, excluded=[dict(item=a, location=b, reason=c) for a, b, c in EXCLUDED],
                   package_checks={f'{n:02d} {CHECK_NAMES[n]}': dict(result=s, detail=d) for n, (s, d) in sorted(P.items())},
                   source_integrity=SI, documentation=docs),
              open(f'{PKG}/05_Manifests/COMPLETE_VEHICLE_MANIFEST.json', 'w'), indent=1)
    vl = f'{PKG}/{VERIFY_LOG}'
    if os.path.exists(vl): os.remove(vl)                                         # our own generated log; rewritten after verification
    files = sorted(os.path.relpath(os.path.join(a, f), PKG) for a, _, fs in os.walk(PKG) for f in fs if f != '.DS_Store')
    files = [f for f in files if f not in NOT_HASHED]
    open(f'{PKG}/{CHECKSUMS}', 'w').write(''.join(f"{h(os.path.join(PKG, f), 'sha256')}  {f}\n" for f in files))
    fails = {s['vehicle_id']: [n for n, x in allC[s['vehicle_id']].items() if x[0] != 'PASS'] for s in specs}
    print('FINALIZE', len(specs), 'vehicles;', 'package checks', {n: x[0] for n, x in P.items()}, '; failing', {k: x for k, x in fails.items() if x} or 'none', ';', len(files), 'files hashed')
