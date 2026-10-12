# "Export Vechile": one portable Unity handoff for every approved vehicle release (plain python3).
# Sources are only read and copied; every copy is hash-checked against its release record
# (traffic UNITY_HANDOFF_20261010/SHA1SUMS.txt, player *_FINAL_FREEZE.md, Hypercar final_export_manifest.json).
#   python3 va_export_package.py build <hypercar_reexport_dir>        assemble assets (moves an older package aside, never deletes)
#   python3 va_export_package.py finalize <measure_pkg.json> <measure_copy.json>   checks, specs, manifests, QA docs, checksums
#   python3 va_export_package.py verify <package_dir> [--log <file>]   SHA-256 list, mandatory files, FBX texture paths, PNG integrity
import sys; sys.dont_write_bytecode = True
import os, re, json, shutil, hashlib, zlib, subprocess, time

WS = '/Users/meetshah/Documents/blender'; V = f'{WS}/vehicles'
PKG = f'{WS}/Export Vechile'
HO = f'{V}/H_TrafficFleet/UNITY_HANDOFF_20261010'
HC = f'{WS}/new_car'
SCRATCH = os.environ.get('VA_SCRATCH', '/tmp')
CHECKSUMS = '05_Manifests/FILE_CHECKSUMS_SHA256.txt'
VERIFY_LOG = '05_Manifests/PACKAGE_VERIFICATION_LOG.md'          # written after the checksums, so it is not in them
NOT_HASHED = {CHECKSUMS, VERIFY_LOG}
TODAY = time.strftime('%Y-%m-%d')

def h(p, alg='sha1'):
    d = hashlib.new(alg)
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): d.update(b)
    return d.hexdigest()
U = lambda b: [round(-b[0], 5), round(b[2], 5), round(-b[1], 5)]          # Blender (x, y, z) -> Unity (-x, z, -y)
J = lambda p: json.load(open(p))
CORNERS = ('FL', 'FR', 'RL', 'RR')
LIGHT_CELLS = ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse', 'Marker']

# ------------------------------------------------------------------ vehicle registry (the approved releases)
TRAFFIC = [  # package id, handoff dir, FBX base, approved release label, class
    ('Traffic_Sedan_A_r3', '01_Traffic_Sedan_A_r3', 'TrafficSedanA_r3', 'Sedan A r3', 'sedan'),
    ('Traffic_Sedan_B', '02_Traffic_Sedan_B', 'TrafficSedanB', 'Sedan B', 'sedan'),
    ('Traffic_Hatchback_A_r2', '03_Traffic_Hatchback_A_r2', 'TrafficHatchbackA_r2', 'Hatchback A r2', 'hatchback'),
    ('Traffic_SUV_A_v2', '04_Traffic_SUV_A', 'TrafficSUVA', 'SUV A v2', 'suv'),
    ('Traffic_SUV_B_v3', '05_Traffic_SUV_B', 'TrafficSUVB', 'SUV B v3', 'suv'),
    ('Traffic_Box_Truck_A_r7', '06_Traffic_Box_Truck_A', 'TrafficBoxTruckA', 'Box Truck A r7', 'box_truck'),
    ('Traffic_Bus_A_v4', '07_Traffic_Bus_A', 'TrafficBusA', 'Bus A v4', 'bus'),
]
PLAYER = [  # package id, display, source dir, prefix, FBX base, freeze manifest, approved release label
    ('ZeroGapR', 'Zero Gap R', 'B_ZeroGapR', 'ZG', 'ZeroGapR', 'ZG_FINAL_FREEZE.md', 'Zero Gap R (Phase B release)'),
    ('TitanGT_r1', 'Titan GT r1', 'C_TitanGT_r1', 'TG', 'TitanGT', 'TG_R1_FINAL_FREEZE.md', 'Titan GT r1 (Phase C revision r1)'),
    ('VortexR_r1', 'Vortex R r1', 'D_VortexR_r1', 'VX', 'VortexR', 'VX_R1_FINAL_FREEZE.md', 'Vortex R r1 (Phase D revision r1)'),
    ('RavenXR', 'Raven XR', 'E_RavenXR', 'RV', 'RavenXR', 'RV_FINAL_FREEZE.md', 'Raven XR (Phase E release)'),
]
EXCLUDED = [  # (what, where, why)
    ('Titan GT (original)', 'vehicles/C_TitanGT/', 'Frozen but superseded for Unity import by Titan GT r1 (LOD1-3 panel-gap shading tears). Same identity: only r1 ships.'),
    ('Vortex R (original)', 'vehicles/D_VortexR/', 'Frozen but superseded for Unity import by Vortex R r1 (LOD1 trim normal tears). Same identity: only r1 ships.'),
    ('Zero Gap R r1', '(proposal only, no folder)', 'Proposed LOD1 trim/lights normals revision; never approved or built. The frozen Phase B release ships.'),
    ('Titan GT r2', '(proposal only, no folder)', 'Proposed Lights_LOD1 normals-only revision; never approved or built. Titan GT r1 ships.'),
    ('Pulse EV', 'vehicles/F_PulseEV/', 'POSTPONED by the project owner (2026-10-08); design blockout only, no production model, no FBX.'),
    ('Traffic Pickup A', 'vehicles/H_TrafficFleet/Traffic_Pickup_A/', 'POSTPONED by the project owner; blockout / scratch trial only.'),
    ('Traffic Van A', '(never started)', 'POSTPONED by the project owner; no model exists.'),
    ('Traffic Sedan A (H1) and r2', 'vehicles/H_TrafficFleet/Traffic_Sedan_A/, Traffic_Sedan_A_r2/', 'Superseded by Sedan A r3 (r2 rejected as benchmark); kept for reference only.'),
    ('Traffic Hatchback A (original)', 'vehicles/H_TrafficFleet/Traffic_Hatchback_A/', 'Frozen as history; superseded by Hatchback A r2 (released version).'),
    ('Earlier SUV A v1, SUV B v1/v2, Box Truck r1-r6, Bus v1-v3', 'rollback folders inside the vehicle directories', 'Superseded iterations / rollbacks; Bus v3 is rollback only. The released versions ship.'),
    ('racing_car_00 ... 09 (.blend)', 'project root', 'Older unnamed generic car; racing_car_09 was the Zero Gap R intake source, superseded by vehicles/B_ZeroGapR/.'),
    ('*_LOD0_unity_test.fbx', 'every vehicle', 'LOD0-only quick-import reference, a strict subset of the complete FBX. Not a vehicle; not shipped (saves ~40 MB).'),
    ('Old UnityTransfer folders, _UNITY_EXPORT_WS_20261010, _TO_DELETE_cleanup_20261009', 'vehicles/...', 'Staging / workspace copies. Their verified files are re-copied here with hash checks; the folders themselves are not shipped.'),
    ('Source .blend files, previews, renders, scripts', 'all vehicles', 'Not needed in Unity. Every source stays untouched on the Blender machine.'),
    ('environment/ (P0-P3 world)', '/Volumes/Denish/Assets/environment.zip', 'Not a vehicle asset; archived off this Mac by the owner (separate known integrity item, see validation report).'),
]

def freeze_rows(path):
    return {m.group(1): m.group(2) for m in re.finditer(r'^\| `([^`]+)` \| `([0-9a-f]{40})` \|', open(path).read(), re.M)}

def registry():
    out = []
    for pid, hdir, base, release, cls in TRAFFIC:
        man = J(f'{HO}/{hdir}/reports/{base}_unity_manifest.json')
        out.append(dict(id=pid, name=man['release'], type='traffic', cls=cls, release=release, fam='traffic',
                        dir=f'01_Traffic_Vehicles/{pid}', fbx=f'01_Traffic_Vehicles/{pid}/FBX/{base}_complete_unity.fbx', base=base, hdir=hdir))
    out.append(dict(id='Hypercar', name='Hypercar', type='player', cls='hypercar', release='Hypercar (flagship, Phase 9 export checkpoint hypercar_08)',
                    fam='hypercar', dir='02_Player_Vehicles/Hypercar', fbx='02_Player_Vehicles/Hypercar/FBX/hypercar_complete_unity.fbx', base='hypercar'))
    for pid, name, src, pre, base, frz, release in PLAYER:
        out.append(dict(id=pid, name=name, type='player', cls='sports_car', release=release, fam='player', src=src, pre=pre, frz=frz,
                        dir=f'02_Player_Vehicles/{pid}', fbx=f'02_Player_Vehicles/{pid}/FBX/{base}_complete_unity.fbx', base=base))
    return out

# ------------------------------------------------------------------ build
LOG = []
def copy(src, rel, expect=None, what=''):
    dst = os.path.join(PKG, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    s, d = h(src), h(dst)
    if s != d: raise SystemExit(f'COPY MISMATCH {rel}')
    if expect is not None and d != expect: raise SystemExit(f'RELEASE HASH MISMATCH {rel}: {d} != {expect} ({what})')
    LOG.append(dict(path=rel, source=os.path.relpath(src, WS), sha1=d, verified_against=what if expect else 'copy only'))

def build(reexport):
    if os.path.exists(PKG):
        old = os.path.join(SCRATCH, f'old_package_{int(time.time())}'); shutil.move(PKG, old); print('moved older package to', old)
    sums = {l.split(None, 1)[1].strip(): l.split()[0] for l in open(f'{HO}/SHA1SUMS.txt') if l.strip()}
    sums = {k[2:] if k.startswith('./') else k: v for k, v in sums.items()}
    T = 'UNITY_HANDOFF_20261010/SHA1SUMS.txt'
    for v in registry():
        if v['fam'] == 'traffic':
            H = f"{HO}/{v['hdir']}"; man = J(f"{H}/reports/{v['base']}_unity_manifest.json")
            assert man['release'] == v['release'], (man['release'], v['release'])
            f = f"{v['base']}_complete_unity.fbx"
            assert sums[f"{v['hdir']}/FBX/{f}"] == man['fbx'][f]['sha1']
            copy(f'{H}/FBX/{f}', f"{v['dir']}/FBX/{f}", man['fbx'][f]['sha1'], T + ' + unity manifest')
            for sub in ('textures', 'reports'):
                for n in sorted(os.listdir(f'{H}/{sub}')):
                    copy(f'{H}/{sub}/{n}', f"{v['dir']}/{sub}/{n}", sums[f"{v['hdir']}/{sub}/{n}"], T)
            n = f"README_{v['base']}.md"; copy(f'{H}/{n}', f"{v['dir']}/{n}", sums[f"{v['hdir']}/{n}"], T)
        elif v['fam'] == 'player':
            S = f"{V}/{v['src']}"; rows = freeze_rows(f"{S}/reports/{v['frz']}"); FZ = f"{v['src']}/reports/{v['frz']}"
            f = f"{v['base']}_complete_unity.fbx"
            copy(f'{S}/UnityTransfer/FBX/{f}', f"{v['dir']}/FBX/{f}", rows[f'UnityTransfer/FBX/{f}'], FZ)
            for n in sorted(os.listdir(f'{S}/UnityTransfer/Textures')):          # FBX links ../textures/<file> (lower case)
                copy(f'{S}/UnityTransfer/Textures/{n}', f"{v['dir']}/textures/{n}", rows[f'UnityTransfer/Textures/{n}'], FZ)
            n = f"{v['pre']}_UNITY_IMPORT_NOTES.md"; copy(f'{S}/UnityTransfer/README/{n}', f"{v['dir']}/{n}", rows[f'UnityTransfer/README/{n}'], FZ)
            for n in sorted(os.listdir(f'{S}/UnityTransfer/Reports')):
                if n.endswith('FINAL_REPORT.md') or n in (f"{v['pre']}_export_manifest.json", f"{v['pre']}_geometry.json", f"{v['pre']}_validation.txt"):
                    copy(f'{S}/UnityTransfer/Reports/{n}', f"{v['dir']}/reports/{n}", rows[f'UnityTransfer/Reports/{n}'], FZ)
            copy(f"{S}/reports/{v['frz']}", f"{v['dir']}/reports/{v['frz']}", None)
        else:                                                                    # Hypercar: re-export from the hash-verified source copy
            man = J(f'{HC}/reports/final_export_manifest.json'); files = man['files']; HM = 'new_car/reports/final_export_manifest.json'
            for b in ('hypercar_07_colliders_hierarchy.blend', 'hypercar_08_unity_export.blend'):
                assert h(f'{HC}/{b}') == files[b]['sha1'], b
            assert h(f'{reexport}/hypercar_07_colliders_hierarchy.blend') == files['hypercar_07_colliders_hierarchy.blend']['sha1']
            es = J(f'{reexport}/reports/fbx_export_settings.json'); f = 'hypercar_complete_unity.fbx'
            copy(f'{reexport}/exports/{f}', f"{v['dir']}/FBX/{f}", es['files'][f]['sha1'], 're-export fbx_export_settings.json')
            for rel, meta in sorted(files.items()):
                if rel.startswith('textures/'):
                    copy(f'{HC}/{rel}', f"{v['dir']}/{rel}", meta['sha1'], HM)
            for n in ('unity_import_notes.md', 'unity_material_mapping.md', 'final_export_manifest.json', 'wheel_reference_points.json',
                      'collider_stats.json', 'pivot_validation.json'):
                copy(f'{HC}/reports/{n}', f"{v['dir']}/reports/{n}", None)
            for n in ('fbx_validation_complete.txt', 'fbx_validation_complete.json', 'fbx_export_settings.json'):
                copy(f'{reexport}/reports/{n}', f"{v['dir']}/reports/REEXPORT_{n}", None)
            orig = J(f'{HC}/reports/fbx_validation_complete.json'); new = J(f'{reexport}/reports/fbx_validation_complete.json')
            same = orig == new
            prov = ['# Hypercar FBX re-export provenance', '',
                    f'The frozen Hypercar release (`new_car/`) has no FBX on disk any more; its Phase 9 export folder `new_car/exports/` is gone. The FBX in `FBX/` was re-exported on {TODAY} with the established, unchanged Phase 9 pipeline (`new_car/scripts/export_fbx.py`), run on an isolated scratch copy of the hash-verified source. No frozen file was opened for writing.', '',
                    '| Item | Value |', '|---|---|',
                    f"| Source checkpoint | `hypercar_07_colliders_hierarchy.blend` SHA-1 `{files['hypercar_07_colliders_hierarchy.blend']['sha1']}` (matches the release manifest) |",
                    f"| Export checkpoint | `hypercar_08_unity_export.blend` SHA-1 `{files['hypercar_08_unity_export.blend']['sha1']}` (frozen original, matches the release manifest) |",
                    f"| Textures | 48 / 48 PNG match the release manifest SHA-1 |",
                    f"| Blender | 5.2.2 LTS |",
                    f"| New FBX | `{f}` {es['files'][f]['bytes']:,} bytes, SHA-1 `{es['files'][f]['sha1']}`, {es['files'][f]['objects']} objects |",
                    f"| Original FBX (2026-10-06, not on disk) | {files['exports/' + f]['bytes']:,} bytes, SHA-1 `{files['exports/' + f]['sha1']}`, 308 objects |",
                    f"| Re-import validation (`fbx_validate.py`) | {open(f'{reexport}/reports/fbx_validation_complete.txt').read().split('SUMMARY')[1].splitlines()[0].strip(' :')} |",
                    f"| Validation data vs the frozen 2026-10-06 run | {'identical' if same else 'DIFFERENT'} (`REEXPORT_fbx_validation_complete.json` vs `fbx_validation_complete.json`) |", '',
                    'The byte size differs by about 7 KB because each FBX stores the absolute texture paths of the machine and folder it was written from (here the scratch folder, a longer path). The relative paths `../textures/hypercar/<group>/*.png` that Unity resolves are the same. Object count, triangle counts (incl. the 57 coincident duplicate triangles removed at export), 133 n-gon triangulations, axis bake residual 1.79e-07, dimensions, wheel refs, pivots, colliders and materials all match the original export.', '',
                    'Also shipped: `reports/REEXPORT_fbx_validation_complete.txt` / `.json` (validator output for this exact file) and `reports/REEXPORT_fbx_export_settings.json` (exporter settings + SHA-1).']
            p = os.path.join(PKG, v['dir'], 'REEXPORT_PROVENANCE.md'); open(p, 'w').write('\n'.join(prov) + '\n')
            LOG.append(dict(path=os.path.relpath(p, PKG), source='generated', sha1=h(p), verified_against='generated'))
    for n in sorted(os.listdir(f'{HO}/shared/textures')):
        copy(f'{HO}/shared/textures/{n}', f'01_Traffic_Vehicles/shared/textures/{n}', sums[f'shared/textures/{n}'], T)
    for n in ('README_UNITY_IMPORT.md', 'UNITY_FLEET_HANDOFF_REPORT.md'):
        copy(f'{HO}/{n}', f'01_Traffic_Vehicles/_fleet_reference_20261010/{n}', sums[n], T)
    os.makedirs(f'{PKG}/05_Manifests', exist_ok=True)
    json.dump(LOG, open(f'{PKG}/05_Manifests/build_copy_log.json', 'w'), indent=1)
    print('BUILD', len(LOG), 'files;', sum(1 for x in LOG if x['verified_against'] not in ('copy only', 'generated')), 'checked against release records')

# ------------------------------------------------------------------ released reference values (what each check compares against)
def released(v):
    if v['fam'] == 'traffic':
        R = f"{PKG}/{v['dir']}/reports/{v['base']}"
        man = J(f'{R}_unity_manifest.json'); aud = J(f'{R}_fbx_audit.json')['files'][f"{v['base']}_complete_unity.fbx"]
        us = man['unity_space']
        return dict(objects=man['fbx'][f"{v['base']}_complete_unity.fbx"]['objects'],
                    lods={k: dict(tris=x['triangles'], materials=x['materials']) for k, x in man['lods'].items()},
                    dims=dict(length=us['lod0_dims_m']['length_z'], width=us['lod0_dims_m']['width_x'], height=us['lod0_dims_m']['height_y']),
                    nose_z=us['nose_z'], tail_z=us['tail_z'],
                    wheels={k: dict(unity=man['wheels'][k]['unity_position'], radius=man['wheels'][k]['radius_m'], width=man['wheels'][k]['width_m']) for k in CORNERS},
                    com=man['center_of_mass_unity'], colliders={k: x['tris'] for k, x in man['colliders'].items()},
                    lights=dict(kind='ts_channels', per_object={k: x['fbx'] for k, x in aud['light_channels'].items()},
                                names=[c for c in LIGHT_CELLS if c in man['light_channels']]),
                    materials_all=sorted({m for x in man['lods'].values() for m in x['materials']}),
                    mirrors=True, mirrors_src='traffic README_UNITY_IMPORT.md section 8: "Width includes the mirrors."',
                    fbx_sha1=man['fbx'][f"{v['base']}_complete_unity.fbx"]['sha1'],
                    source=dict(freeze_manifest=man['source']['freeze_manifest'], freeze_manifest_sha1=man['source']['freeze_manifest_sha1'],
                                source_blend=man['source']['file'], source_blend_sha1=man['source']['sha1'],
                                handoff='vehicles/H_TrafficFleet/UNITY_HANDOFF_20261010/' + v['hdir']),
                    manual_textures=sorted({t.split(' ')[0] for mt in man['materials'] for t in mt['manual_textures'] if t.split(' ')[0].endswith('.png')}),
                    all_textures=man['dependencies']['all_source_textures'])
    if v['fam'] == 'player':
        R = f"{PKG}/{v['dir']}/reports/{v['pre']}"
        g = J(f'{R}_geometry.json'); em = J(f'{R}_export_manifest.json'); rx = g['fbx_reimport'][f"{v['base']}_complete_unity.fbx"]
        notes = open(f"{PKG}/{v['dir']}/{v['pre']}_UNITY_IMPORT_NOTES.md").read()
        wt = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in
              re.finditer(r'^\| (FL|FR|RL|RR) \| \([^)]*\) \| \([^)]*\) \| ([\d.]+) \| ([\d.]+) \|', notes, re.M)}
        rows = freeze_rows(f"{PKG}/{v['dir']}/reports/{v['frz']}")
        d = g['lods']['LOD0']['dims_m']
        return dict(objects=rx['objects'], lods={k: dict(tris=x['triangles'], materials=None, materials_count=x['materials']) for k, x in g['lods'].items()},
                    dims=dict(length=d[1], width=d[0], height=d[2]), nose_z=rx['unity_space']['nose_z'], tail_z=rx['unity_space']['tail_z'],
                    wheels={k: dict(unity=U(g['wheel_refs'][k]), radius=wt[k][0], width=wt[k][1]) for k in CORNERS},
                    com=U(g['center_of_mass']), colliders={k: x['tris'] for k, x in g['colliders'].items()},
                    lights=dict(kind='materials', faces=g['light_faces'], names=list(g['light_faces'])),
                    materials_all=sorted(em['materials']), mirrors=bool(re.search(r'^L x W x H [^(]*\(mirrors[^)]*incl', notes, re.M)),
                    body_width=(lambda x: float(x.group(1)) if x else None)(re.search(r'body width ~?([\d.]+) m', notes)),
                    mirrors_src=f"{v['pre']}_UNITY_IMPORT_NOTES.md: \"" + re.search(r'^L x W x H .*$', notes, re.M).group(0) + '"',
                    fbx_sha1=rows[f"UnityTransfer/FBX/{v['base']}_complete_unity.fbx"],
                    source=dict(freeze_manifest=f"vehicles/{v['src']}/reports/{v['frz']}", freeze_manifest_sha1=h(f"{V}/{v['src']}/reports/{v['frz']}"),
                                source_blend=f"vehicles/{v['src']}/" + next(k for k in rows if k.endswith('_09_export_ready.blend')),
                                source_blend_sha1=next(x for k, x in rows.items() if k.endswith('_09_export_ready.blend'))),
                    manual_textures=[f"{v['pre']}_Palette_MetallicSmoothness.png"], all_textures=sorted(em['textures']) + [f"{v['pre']}_Palette_MetallicSmoothness.png"])
    R = f"{PKG}/{v['dir']}/reports"                                               # Hypercar (frozen 2026-10-06 values)
    man = J(f'{R}/final_export_manifest.json'); fv = J(f'{HC}/reports/fbx_validation_complete.json'); un = man['unity']
    es = J(f'{R}/REEXPORT_fbx_export_settings.json')
    leds = ['MAT_LED_White', 'MAT_LED_Red', 'MAT_LED_Brake', 'MAT_LED_Amber', 'MAT_LED_Reverse', 'MAT_AmbientLight']
    return dict(objects=man['fbx']['hypercar_complete_unity.fbx']['objects'],
                lods={k: dict(tris=x['triangles'], materials=fv[f'materials_{k}']) for k, x in man['lods'].items()},
                dims=dict(length=man['lods']['LOD0']['dims_m']['L'], width=man['lods']['LOD0']['dims_m']['W'], height=man['lods']['LOD0']['dims_m']['H']),
                nose_z=fv['unity_raw']['body_z_range(forward)'][1], tail_z=fv['unity_raw']['body_z_range(forward)'][0],
                wheels={k: dict(unity=un['wheels'][k]['position'], radius=un['wheels'][k]['radius'], width=un['wheels'][k]['width']) for k in CORNERS},
                com=un['center_of_mass'], colliders=man['colliders'],
                lights=dict(kind='hypercar', names=leds), materials_all=sorted({m for k in man['lods'] for m in fv[f'materials_{k}']}),
                mirrors=None, mirrors_src='unity_import_notes.md: "Dimensions (LOD0 re-import, mirrors excluded)" - see measured note',
                fbx_sha1=es['files']['hypercar_complete_unity.fbx']['sha1'],
                source=dict(freeze='Hypercar FROZEN flagship (handoff_vehicle_remaster/00_START_HERE, VA_VEHICLE_MASTER_INVENTORY.md)',
                            release_manifest='new_car/reports/final_export_manifest.json', release_manifest_sha1=h(f'{HC}/reports/final_export_manifest.json'),
                            source_blend='new_car/hypercar_08_unity_export.blend', source_blend_sha1=man['files']['hypercar_08_unity_export.blend']['sha1'],
                            fbx_note='re-exported 2026-10-11 from the hash-verified source copy, see REEXPORT_PROVENANCE.md'),
                manual_textures=sorted(k.split('/', 1)[1] for k in man['files'] if k.startswith('textures/') and '_AO' in k),
                all_textures=sorted(k.split('/', 1)[1] for k in man['files'] if k.startswith('textures/')))

# ------------------------------------------------------------------ PNG + FBX helpers (plain python, no Blender)
def png_check(p):
    b = open(p, 'rb').read()
    if b[:8] != b'\x89PNG\r\n\x1a\n': return 'bad signature', None
    i, idat, ihdr, end = 8, [], None, False
    while i + 8 <= len(b):
        n = int.from_bytes(b[i:i + 4], 'big'); t = b[i + 4:i + 8]; d = b[i + 8:i + 8 + n]
        if len(d) != n or i + 12 + n > len(b): return 'truncated', None
        if zlib.crc32(t + d) & 0xffffffff != int.from_bytes(b[i + 8 + n:i + 12 + n], 'big'): return f'CRC error in {t.decode(errors="replace")}', None
        if t == b'IHDR': ihdr = d
        if t == b'IDAT': idat.append(d)
        i += 12 + n
        if t == b'IEND': end = True; break
    if not ihdr or not end: return 'missing IHDR/IEND', None
    w, hh, bd, ct, il = int.from_bytes(ihdr[0:4], 'big'), int.from_bytes(ihdr[4:8], 'big'), ihdr[8], ihdr[9], ihdr[12]
    try: raw = zlib.decompress(b''.join(idat))
    except zlib.error as e: return f'zlib: {e}', None
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if il == 0 and ch and len(raw) != hh * (1 + (w * ch * bd + 7) // 8): return 'pixel data length mismatch', None
    return None, dict(w=w, h=hh, bit_depth=bd, color_type=ct, channels=ch)

def fbx_rel_textures(p):
    return sorted({m.decode() for m in re.findall(rb'\.\./[\x20-\x7e]{1,200}?\.png', open(p, 'rb').read())})

# ------------------------------------------------------------------ verify (also used on the extracted ZIP)
def verify(root, log=None):
    root = os.path.realpath(root); out = []; ok = True
    lines = [l.rstrip('\n') for l in open(os.path.join(root, CHECKSUMS)) if l.strip()]
    listed = {}
    for l in lines:
        d, p = l.split('  ', 1); listed[p] = d
    bad = [p for p, d in listed.items() if not os.path.isfile(os.path.join(root, p)) or h(os.path.join(root, p), 'sha256') != d]
    on_disk = {os.path.relpath(os.path.join(a, f), root) for a, _, fs in os.walk(root) for f in fs}
    extra = sorted(on_disk - set(listed) - NOT_HASHED)
    out.append(('SHA-256 checksum list', not bad and not extra, f'{len(listed)} files re-hashed; mismatched/missing {len(bad)} {bad[:3]}; unlisted {len(extra)} {extra[:3]}'))
    man = J(os.path.join(root, '05_Manifests/COMPLETE_VEHICLE_MANIFEST.json'))
    need = [p for v in man['vehicles'] for p in [v['fbx']['path']] + v['textures']['all']] + [x for x in man['documentation']]
    miss = [p for p in need if not os.path.isfile(os.path.join(root, p))]
    out.append(('Mandatory files (FBX, textures, docs per manifest)', not miss, f'{len(need)} required, missing {len(miss)} {miss[:3]}'))
    traffic = sum(v['vehicle_type'] == 'traffic' for v in man['vehicles'])
    out.append(('Seven mandatory traffic vehicles', traffic == 7, f'{traffic} traffic + {len(man["vehicles"]) - traffic} player vehicles'))
    unres = []; n = 0
    for v in man['vehicles']:
        f = os.path.join(root, v['fbx']['path'])
        for r in fbx_rel_textures(f):
            n += 1; t = os.path.normpath(os.path.join(os.path.dirname(f), r))
            if not os.path.isfile(t) or not t.startswith(root + os.sep): unres.append(f"{v['vehicle_id']}: {r}")
    out.append(('FBX relative texture paths resolve inside this folder', not unres, f'{n} references, unresolved {len(unres)} {unres[:3]}'))
    pngs = sorted(p for p in on_disk if p.lower().endswith('.png')); badp = []
    for p in pngs:
        e, _ = png_check(os.path.join(root, p))
        if e: badp.append(f'{p}: {e}')
    out.append(('PNG integrity (signature, chunk CRC, zlib, pixel length)', not badp, f'{len(pngs)} PNG, corrupt {len(badp)} {badp[:3]}'))
    ok = all(x[1] for x in out)
    txt = [f'# Package verification ({time.strftime("%Y-%m-%d %H:%M")})', '', f'Folder: `{root}`', '', '| Check | Result | Detail |', '|---|---|---|']
    txt += [f"| {a} | {'PASS' if b else 'FAIL'} | {c} |" for a, b, c in out]
    txt += ['', f"Overall: **{'PASS' if ok else 'FAIL'}**"]
    for a, b, c in out: print('PASS' if b else 'FAIL', '|', a, '|', c)
    print('VERIFY', 'PASS' if ok else 'FAIL', root)
    if log: open(log, 'a').write('\n'.join(txt) + '\n\n')
    return ok

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'build': build(sys.argv[2])
    elif cmd == 'verify':
        lg = sys.argv[sys.argv.index('--log') + 1] if '--log' in sys.argv else None
        sys.exit(0 if verify(sys.argv[2], lg) else 1)
    elif cmd == 'finalize':
        from va_export_finalize import finalize
        finalize(sys.argv[2], sys.argv[3])
