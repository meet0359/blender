# Unity handoff driver (export + validation only; frozen releases are read-only). python3 ts_unity_handoff.py ws | run <Folder> | package | verify
#   ws       isolated export workspace: SHA-1-verified copies of each frozen 09 + its textures + shared textures (relative layout preserved)
#   run      ts_export (TS_FROM_09, workspace) -> ts_validate (FBX re-import on) -> copy FBX / textures into the package -> ts_fbx_audit
#   package  per-vehicle README + material mapping, fleet manifest (JSON + MD), SHA1SUMS
#   verify   workspace 09 copies still match the freeze manifests + frozen-release check
import sys, os, json, shutil, hashlib, subprocess, glob, time
SC = os.path.dirname(os.path.abspath(__file__)); FLEET = os.path.dirname(SC); VEH = os.path.dirname(FLEET)
WSR = os.path.join(FLEET, '_UNITY_EXPORT_WS_20261010'); PKG = os.path.join(FLEET, 'UNITY_HANDOFF_20261010'); B = '/Applications/Blender.app/Contents/MacOS/Blender'
HEAVY = {'TS_LOD_PCT': '.40,.60,.15,.30,.05,.15', 'TS_COM_Z': '.5,1.5'}             # truck / bus class targets (as used at freeze)
# folder, ckp, production preview base, FBX base, collection, paint prefix, budget lo, hi, validator env, release label, freeze manifest
SPEC = [('Traffic_Sedan_A_r3', 'trafficsedanar3', 'TrafficSedanA', 'TrafficSedanA_r3', 'TRAFFIC_SEDAN_A', 'TS_SedanA', 10000, 15000, {}, 'Sedan A r3', 'TS_SedanA_r3_FINAL_FREEZE.md'),
        ('Traffic_Sedan_B', 'trafficsedanb', 'TrafficSedanB', 'TrafficSedanB', 'TRAFFIC_SEDAN_B', 'TS_SedanB', 12000, 18000, {}, 'Sedan B', 'TS_SedanB_FINAL_FREEZE.md'),
        ('Traffic_Hatchback_A_r2', 'traffichatchbackar2', 'TrafficHatchbackA', 'TrafficHatchbackA_r2', 'TRAFFIC_HATCHBACK_A_R2', 'TS_HatchA', 12000, 18000, {}, 'Hatchback A r2', 'TS_HatchA_r2_FINAL_FREEZE.md'),
        ('Traffic_SUV_A', 'trafficsuva', 'TrafficSUVA', 'TrafficSUVA', 'TRAFFIC_SUV_A', 'TS_SUVA', 12000, 18000, {}, 'SUV A v2', 'TS_SUVA_FINAL_FREEZE.md'),
        ('Traffic_SUV_B', 'trafficsuvb', 'TrafficSUVB', 'TrafficSUVB', 'TRAFFIC_SUV_B', 'TS_SUVB', 13000, 20000, {}, 'SUV B v3', 'TS_SUVB_FINAL_FREEZE.md'),
        ('Traffic_Box_Truck_A', 'trafficboxtrucka', 'TrafficBoxTruckA', 'TrafficBoxTruckA', 'TRAFFIC_BOX_TRUCK_A', 'TS_BoxTruckA', 15000, 25000, HEAVY, 'Box Truck A r7', 'TS_BoxTruckA_FINAL_FREEZE.md'),
        ('Traffic_Bus_A', 'trafficbusa', 'TrafficBusA', 'TrafficBusA', 'TRAFFIC_BUS_A', 'TS_BusA', 20000, 35000, HEAVY, 'Bus A v4', 'TS_BusA_FINAL_FREEZE.md')]
sha = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()
pkgdir = lambda i, s: os.path.join(PKG, f'{i + 1:02d}_{s[0]}')
def frozen(s): return {r[1]: r[3] for r in (l.split('`') for l in open(os.path.join(FLEET, s[0], 'reports', s[10])) if l.startswith('| `'))}
def guard(what, floor_gb=2.0):
    free = shutil.disk_usage(FLEET).free / 2**30; print(f'DISK {what}: {free:.1f} GB free', flush=True)
    if free < floor_gb: sys.exit(f'DISK STOP: below {floor_gb} GB before {what}')
def check_copy(s):                                                                         # workspace copy == frozen manifest entry (09 + vehicle textures)
    man = frozen(s); w = os.path.join(WSR, s[0]); bad = []
    for rel in [f'blend/{s[1]}_09_export_ready.blend'] + [r for r in man if r.startswith('textures/')]:
        if not os.path.exists(os.path.join(w, rel)) or sha(os.path.join(w, rel)) != man[rel]: bad.append(rel)
    for rel, h in man.items():
        if rel.startswith('../shared/textures/') and sha(os.path.join(WSR, 'shared', 'textures', os.path.basename(rel))) != h: bad.append(rel)
    return bad
def ws():
    guard('workspace'); os.makedirs(os.path.join(WSR, 'shared', 'textures'), exist_ok=True)
    for f in sorted(os.listdir(os.path.join(FLEET, 'shared', 'textures'))):
        if f.endswith('.png'): shutil.copy2(os.path.join(FLEET, 'shared', 'textures', f), os.path.join(WSR, 'shared', 'textures', f))
    for s in SPEC:
        src, w = os.path.join(FLEET, s[0]), os.path.join(WSR, s[0])
        for d in ('blend', 'textures', 'reports', 'exports', 'logs'): os.makedirs(os.path.join(w, d), exist_ok=True)
        shutil.copy2(os.path.join(src, 'blend', f'{s[1]}_09_export_ready.blend'), os.path.join(w, 'blend'))
        for f in glob.glob(os.path.join(src, 'textures', '*.png')): shutil.copy2(f, os.path.join(w, 'textures'))
        pv = os.path.join(w, 'previews')                                                    # validator check 16 reads QA renders: link to the frozen previews (read-only)
        if not os.path.lexists(pv):
            if s[2] == s[3]: os.symlink(os.path.join(src, 'previews'), pv)
            else:
                os.makedirs(pv)
                for f in glob.glob(os.path.join(src, 'previews', f'{s[2]}_*.png')): os.symlink(f, os.path.join(pv, s[3] + os.path.basename(f)[len(s[2]):]))
        bad = check_copy(s); print('WS', s[0], 'copies verified against', s[10] if not bad else f'MISMATCH {bad}', flush=True)
        if bad: sys.exit(1)
def blender(script, args, env, log):
    with open(log, 'w') as fh: return subprocess.run([B, '-b', '--factory-startup', '--python', script, '--'] + args, cwd=SC, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
def run(folder):
    i, s = next((i, s) for i, s in enumerate(SPEC) if s[0] == folder); w = os.path.join(WSR, s[0]); L = os.path.join(w, 'logs')
    bad = check_copy(s)
    if bad: sys.exit(f'{folder}: workspace copy does not match the freeze manifest {bad}')
    env = {k: v for k, v in os.environ.items() if k not in ('TS_NO_FBX', 'TS_NO_UNITY')}; env.update(s[8]); env.update(TS_SCRATCH=w, TS_FROM_09='1')
    guard(f'export {folder}'); rc = blender('ts_export.py', [s[0], s[1], s[3], s[4]], env, os.path.join(L, 'export.log'))
    if rc or 'EXPORT DONE' not in open(os.path.join(L, 'export.log')).read(): sys.exit(f'{folder}: EXPORT FAILED (see {L}/export.log)')
    guard(f'validate {folder}'); blender('ts_validate.py', [s[0], s[1], s[3], s[4], str(s[6]), str(s[7]), '.12'], env, os.path.join(L, 'validate.log'))
    val = open(os.path.join(w, 'reports', f'{s[1]}_validation.txt')).read()
    p = pkgdir(i, s); man = json.load(open(os.path.join(w, 'reports', f'{s[1]}_export_manifest.json')))
    for d in ('FBX', 'textures', 'reports'): os.makedirs(os.path.join(p, d), exist_ok=True)
    os.makedirs(os.path.join(PKG, 'shared', 'textures'), exist_ok=True)
    for f in man['files']: shutil.copy2(os.path.join(w, 'exports', f), os.path.join(p, 'FBX', f))
    for t in man['textures']:
        if os.path.exists(os.path.join(w, 'textures', t)): shutil.copy2(os.path.join(w, 'textures', t), os.path.join(p, 'textures', t))
    for t in os.listdir(os.path.join(WSR, 'shared', 'textures')): shutil.copy2(os.path.join(WSR, 'shared', 'textures', t), os.path.join(PKG, 'shared', 'textures', t))
    guard(f'audit {folder}'); blender('ts_fbx_audit.py', [w, s[1], s[3], p], env, os.path.join(L, 'audit.log'))
    for f in ('export_manifest.json', 'validation.txt', 'geometry.json', 'fbx_audit.json'): shutil.copy2(os.path.join(w, 'reports', f'{s[1]}_{f}'), os.path.join(p, 'reports', f'{s[3]}_{f}'))
    au = json.load(open(os.path.join(w, 'reports', f'{s[1]}_fbx_audit.json'))); post = check_copy(s)
    fails = [l[:160] for l in val.splitlines() if l.startswith('[FAIL]')]
    print('RUN', folder, '|', [l for l in val.splitlines() if l.startswith('SUMMARY')][0], '| validator FAIL lines:', fails, '| audit', 'PASS' if au['ok'] else 'FAIL',
          {f: r['problems'] for f, r in au['files'].items() if r['problems']}, '| workspace 09 after:', 'unchanged' if not post else f'CHANGED {post}', flush=True)
def verify():
    for s in SPEC: print('WS09', s[0], 'matches freeze manifest' if not check_copy(s) else f'MISMATCH {check_copy(s)}')
    return subprocess.run(['python3', os.path.join(VEH, 'A_Discovery', 'scripts', 'va_frozen_check.py')]).returncode
def shader(m, d):
    c = d['custom']; p = d['principled']
    if '_Paint' in m: return 'URP Complex Lit (clear coat)' if (p.get('Coat Weight') or {}).get('value') else 'URP Lit (opaque)'
    if m.endswith('_Glass') or m.startswith('TS_Lens'): return 'URP Lit, Surface Transparent'
    if m == 'TS_Lights': return 'Emissive light-channel shader (Shader Graph; see README)'
    return 'URP Lit (opaque)'
EXTRA = {'TS_Atlas': ['TS_Atlas_MetallicSmoothness.png (R metal, A smoothness; replaces Metallic + Roughness)'], 'TS_Lights': ['TS_Lights_Emission.png', 'TS_Lights_ChannelID.png (R x 15 = channel; point filter, no compression)'],
         'TS_Tire': ['smoothness = 1 - TS_Tire_Roughness (pack into a map alpha, or use the constant)']}
def mat_rows(au, fb):
    slots = au['files'][fb]['file']['material_texture_slots']; rows = []
    for m, d in au['materials'].items():
        p = d['principled']; bc = p['Base Color']; c = d['custom']; a = c.get('unity_alpha', p['Alpha']['value'])
        pc = d.get('rgb_nodes', {}).get('PaintColour')
        base = (f"PaintColour {tuple(pc)}" + (' x AO (R of AO_Grime), grime by G' if bc['textures'] else '')) if pc else ', '.join(bc['textures']) if bc['linked'] else str(tuple(bc['value'][:3]))
        carried = {os.path.basename(v) for v in slots.get(m, {}).values()}
        extra = [t for t in sorted({i[0] for i in d['images']}) if t not in carried and '(packed)' not in t]
        key = 'TS_Atlas' if c.get('instance_of') == 'TS_Atlas' else m
        extra += EXTRA.get(key, []) + (['TS_PaintFlake_Normal.png (detail normal, tiling 60, strength 0.15)'] if '_Paint' in m and not m.endswith('_Far') else [])
        extra = [t for t in dict.fromkeys(extra) if not any(e != t and e.startswith(t) for e in extra)]                  # keep the annotated entry when a texture is listed twice
        rows.append(dict(material=m, lods=d['used_by_lods'], shader=shader(m, d), base=base, metallic=p['Metallic']['value'], smoothness=round(1 - p['Roughness']['value'], 3), alpha=a,
                         coat=(p.get('Coat Weight') or {}).get('value'), normal_strength=d['normal_map_strengths'], fbx_slots=slots.get(m, {}), manual_textures=extra, note=c.get('unity', '')))
    return rows
def package():
    guard('package'); fleet = dict(package=os.path.relpath(PKG, VEH), created=time.strftime('%Y-%m-%d %H:%M'), blender='5.2.2', unity_target='Unity 6000.6.0f1 / URP 17.6 (not run on this machine)',
                                   unity_runtime_verification='NOT DONE - belongs to P0-05 on the Unity machine', vehicles=[], shared_textures={})
    for t in sorted(os.listdir(os.path.join(PKG, 'shared', 'textures'))): fleet['shared_textures'][t] = sha(os.path.join(PKG, 'shared', 'textures', t))
    md = ['# Unity fleet manifest (traffic, 7 vehicles)', '', f"Created {fleet['created']}. Package `{fleet['package']}`. Unity runtime verification: **not done** (P0-05, Unity machine).", '',
          '| # | Release | Folder | Source 09 SHA-1 (= freeze manifest) | Complete FBX | SHA-1 | LOD0 / 1 / 2 / 3 tris | Materials per LOD | Validation | FBX audit |', '|---|---|---|---|---|---|---|---|---|---|']
    for i, s in enumerate(SPEC):
        w = os.path.join(WSR, s[0], 'reports'); p = pkgdir(i, s); man = frozen(s); src = f'blend/{s[1]}_09_export_ready.blend'
        em = json.load(open(os.path.join(w, f'{s[1]}_export_manifest.json'))); au = json.load(open(os.path.join(w, f'{s[1]}_fbx_audit.json'))); val = open(os.path.join(w, f'{s[1]}_validation.txt')).read()
        fb = f'{s[3]}_complete_unity.fbx'; r = au['files'][fb]; L = r['lods']; summ = [l for l in val.splitlines() if l.startswith('SUMMARY')][0]
        fails = [l.split('.')[0].replace('[FAIL]', '').strip() for l in val.splitlines() if l.startswith('[FAIL]')]
        assert au['source_sha1'] == man[src], s[0]
        rows = mat_rows(au, fb)
        v = dict(release=s[9], folder=s[0], package_dir=os.path.basename(p), source=dict(file=f'H_TrafficFleet/{s[0]}/{src}', sha1=man[src], freeze_manifest=f'H_TrafficFleet/{s[0]}/reports/{s[10]}',
                 freeze_manifest_sha1=sha(os.path.join(FLEET, s[0], 'reports', s[10]))),
                 fbx={f: dict(sha1=sha(os.path.join(p, 'FBX', f)), bytes=os.path.getsize(os.path.join(p, 'FBX', f)), objects=d['count']) for f, d in em['files'].items()},
                 textures={t: sha(os.path.join(p, 'textures', t)) for t in sorted(os.listdir(os.path.join(p, 'textures')))},
                 dependencies=dict(fbx_relative_texture_paths=r['file']['texture_relative_paths'], unresolved=r['file']['unresolved_from_package'], all_source_textures=em['textures'],
                                   blender_only=em.get('blender_only'), linked_libraries=0),
                 lods={k: dict(triangles=x['tris'], objects=x['objects'], materials=x['materials']) for k, x in L.items()}, materials=rows,
                 wheels={c: dict(unity_position=x['ref_unity'], radius_m=x['props']['radius_m'], width_m=x['props']['width_m'], lods_with_wheel=x['wheel_lods'], pivot_dev_m=x['max_pivot_vs_ref_m']) for c, x in r['wheels'].items()},
                 center_of_mass_unity=r['unity_space']['center_of_mass'], colliders=r['colliders'], light_channels=sorted(r['light_channels']['Lights_LOD0']['fbx']),
                 unity_space=r['unity_space'], fbx_globals=r['file']['globals'], validation=dict(summary=summ, failed_checks=fails, report=f'reports/{s[3]}_validation.txt'),
                 fbx_audit=dict(ok=au['ok'], problems={f: x['problems'] for f, x in au['files'].items()}, report=f'reports/{s[3]}_fbx_audit.json'))
        fleet['vehicles'].append(v); json.dump(v, open(os.path.join(p, 'reports', f'{s[3]}_unity_manifest.json'), 'w'), indent=1)
        tri_s = ' / '.join(format(L[k]['tris'], ',') for k in L)
        md.append(f"| {i + 1} | **{s[9]}** | `{os.path.basename(p)}` | `{man[src]}` | `FBX/{fb}` | `{v['fbx'][fb]['sha1']}` | {tri_s} | {' / '.join(str(len(L[k]['materials'])) for k in L)} | "
                  f"{summ.replace('SUMMARY: ', '')} (check {', '.join(fails)} = environment archive)" + f" | {'PASS' if au['ok'] else 'FAIL'} |")
        u = r['unity_space']; dm = u['lod0_dims_m']
        rd = [f'# {s[9]}: Unity import notes (`{s[3]}`)', '', f"Release **{s[9]}**, exported from the frozen `{v['source']['file']}` (SHA-1 `{man[src]}`, verified against `{s[10]}`). Exported {fleet['created']} with `ts_export.py` (unchanged FBX settings; source opened read-only, never saved).",
              '**Not opened in Unity.** Runtime verification is P0-05 on the Unity machine. Follow `../README_UNITY_IMPORT.md` for importer and material setup.', '',
              '## Files', '', '| File | Objects | Bytes | SHA-1 |', '|---|---|---|---|'] + [f"| `FBX/{f}` | {d['objects']} | {d['bytes']:,} | `{d['sha1']}` |" for f, d in v['fbx'].items()] + [
              '', f"Vehicle textures (`textures/`): {', '.join(f'`{t}`' for t in v['textures'])}. Shared textures: `../shared/textures/`. The FBX references textures by relative path (`../textures/`, `../../shared/textures/`); all {len(r['file']['texture_relative_paths'])} resolve inside this package.", '',
              '## Size and orientation (Unity space, LOD0 incl. mirrors)', '', f"Length (Z) **{dm['length_z']} m**, width (X) **{dm['width_x']} m**, height (Y) **{dm['height_y']} m**. Nose at +Z {u['nose_z']}, tail {u['tail_z']}, ground Y {u['ground_y']}. Car_Root identity; all node rotations identity, scale 1, no negative scale.", '',
              '## LODs', '', '| LOD | Triangles | Objects | Materials |', '|---|---|---|---|'] + [f"| {k} | {x['tris']:,} | {x['objects']} | {len(x['materials'])} |" for k, x in L.items()] + [
              '', 'Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 % (tune in P0-05).', '',
              '## Wheels and centre of mass (Unity local space under Car_Root)', '', '| Wheel | WheelColliderRef position | radius m | width m | Wheel pivots (all LODs) |', '|---|---|---|---|---|'] + [
              f"| {c} | {tuple(x['unity_position'])} | {x['radius_m']} | {x['width_m']} | on the ref (max dev {x['pivot_dev_m']:.1e} m), LODs {x['lods_with_wheel']} |" for c, x in v['wheels'].items()] + [
              '', f"`CenterOfMass` {tuple(v['center_of_mass_unity'])}. Front wheels steer on `SteerPivot_FL/FR_LOD*` (yaw about local Y); wheels roll about local X.", '',
              '## Colliders', '', '| Collider | Triangles | Materials |', '|---|---|---|'] + [f"| `{n}` | {x['tris']} | {x['materials']} |" for n, x in v['colliders'].items()] + [
              '', f"Light channels on `Lights_LOD*`: {', '.join(v['light_channels'])}.", '',
              '## Materials (values from the frozen source; smoothness = 1 - roughness; colours linear)', '',
              '| Material | LODs | Unity shader | Base | Metallic | Smoothness | Alpha | Coat | Carried by the FBX | Set manually |', '|---|---|---|---|---|---|---|---|---|---|'] + [
              f"| `{x['material']}` | {x['lods']} | {x['shader']} | {x['base']} | {x['metallic']} | {x['smoothness']} | {x['alpha']} | {x['coat']} | {'; '.join(f'{k}: {os.path.basename(t)}' for k, t in x['fbx_slots'].items()) or '-'} | {'; '.join(x['manual_textures']) or '-'} |" for x in rows] + [
              '', f"Validation: {summ} (`reports/{s[3]}_validation.txt`; the only failure, check {', '.join(fails)}, is the archived `environment/` folder, not this vehicle). FBX audit: {'PASS' if au['ok'] else 'FAIL'} (`reports/{s[3]}_fbx_audit.json`)."]
        open(os.path.join(p, f'README_{s[3]}.md'), 'w').write('\n'.join(rd) + '\n')
    md += ['', '## Shared textures (`shared/textures/`)', '', '| File | SHA-1 |', '|---|---|'] + [f'| `{t}` | `{h}` |' for t, h in fleet['shared_textures'].items()]
    json.dump(fleet, open(os.path.join(PKG, 'UNITY_FLEET_MANIFEST.json'), 'w'), indent=1); open(os.path.join(PKG, 'UNITY_FLEET_MANIFEST.md'), 'w').write('\n'.join(md) + '\n')
    sums = []
    for d, ds, fs in os.walk(PKG):
        ds.sort()
        for f in sorted(fs):
            if f not in ('SHA1SUMS.txt', '.DS_Store'): sums.append(f'{sha(os.path.join(d, f))}  {os.path.relpath(os.path.join(d, f), PKG)}')
    open(os.path.join(PKG, 'SHA1SUMS.txt'), 'w').write('\n'.join(sums) + '\n'); print('PACKAGE', len(sums), 'files hashed')
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ws': ws()
    elif cmd == 'run': [run(f) for f in (sys.argv[2:] if sys.argv[2:] != ['all'] else [s[0] for s in SPEC])]
    elif cmd == 'verify': sys.exit(verify())
    elif cmd == 'audit':                                                                       # re-run only the FBX audit on the packaged FBX (no re-export)
        for i, s in enumerate(SPEC):
            w = os.path.join(WSR, s[0]); p = pkgdir(i, s); blender('ts_fbx_audit.py', [w, s[1], s[3], p], dict(os.environ), os.path.join(w, 'logs', 'audit.log'))
            shutil.copy2(os.path.join(w, 'reports', f'{s[1]}_fbx_audit.json'), os.path.join(p, 'reports', f'{s[3]}_fbx_audit.json')); print('AUDIT', s[0], [l for l in open(os.path.join(w, 'logs', 'audit.log')) if l.startswith('AUDIT RESULT')], flush=True)
    elif cmd == 'package': package()
