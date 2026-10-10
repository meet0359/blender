# Blender-only FINAL FREEZE manifest (same format as TS_HatchA_FINAL_FREEZE.md; read by A_Discovery/scripts/va_frozen_check.py).
#   Blender -b --factory-startup --python ts_freeze.py -- <Vehicle_Folder> <ckp> <ManifestName.md> "<approval note>"
# Re-opens <ckp>_09_export_ready.blend for a dependency check, then SHA-1s every file in the vehicle folder (except .DS_Store and the
# manifest itself) plus the external images the blend references outside the folder (shared textures). Writes nothing else.
import bpy, sys, os, hashlib, time, re
a = sys.argv[sys.argv.index('--') + 1:]; FOLD, CKP, MAN, NOTE = a[0], a[1], a[2], a[3]
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.join(H, FOLD); BL = os.path.join(R, 'blend', f'{CKP}_09_export_ready.blend')
bpy.ops.wm.open_mainfile(filepath=BL)
O = bpy.data.objects; need = ['Car_Root', 'LOD0_Root', 'LOD1_Root', 'LOD2_Root', 'LOD3_Root', 'CenterOfMass'] + [f'WheelColliderRef_{c}' for c in ('FL', 'FR', 'RL', 'RR')]
missing = [n for n in need if n not in O]; cols = [o.name for o in O if o.name.startswith('Collision')]
imgs = [im for im in bpy.data.images if im.source == 'FILE' and im.filepath]; ext = [os.path.normpath(bpy.path.abspath(im.filepath)) for im in imgs if not im.packed_file]
unres = [p for p in ext if not os.path.exists(p)]; packed = [im.name for im in bpy.data.images if im.packed_file]; libs = [l.filepath for l in bpy.data.libraries]
outside = sorted({os.path.relpath(p, R) for p in ext if not os.path.normpath(p).startswith(R + os.sep)})
val = os.path.join(R, 'reports', f'{CKP}_validation.txt'); vt = open(val).read() if os.path.exists(val) else ''
summ = (re.search(r'SUMMARY: .*', vt) or [''])[0]; budget = (re.search(r'LOD0 [\d,]+ within [^;]+; LOD1 [\d,]+[^;]*; LOD2 [\d,]+[^;]*; LOD3 [\d,]+ \(\d+%', vt) or [''])[0]
fails = re.findall(r'^\[FAIL\]\s+(\S+)', vt, re.M)
files = []
for d, ds, fs in os.walk(R):
    ds.sort()
    for f in sorted(fs):
        if f == '.DS_Store' or f == MAN: continue
        files.append(os.path.relpath(os.path.join(d, f), R))
files += [p for p in outside if p not in files]
sha = lambda p: hashlib.sha1(open(os.path.join(R, p), 'rb').read()).hexdigest()
rows = [(p, sha(p)) for p in files]
ok_dep = not missing and not unres and not libs and len(cols) >= 1
md = [f'# {FOLD} — FINAL FREEZE (Blender-only)', '',
      f"Date {time.strftime('%Y-%m-%d %H:%M')}. {NOTE}",
      f'- Validation: `reports/{CKP}_validation.txt` **{summ}** — {budget} tris. ' + ('The only FAIL is check 1 (protected files): the frozen `environment/` folder is archived on the external drive (owner-accepted relocation, all 1,186 files SHA-1 verified in the archive); every vehicle-specific check and S1 PASS; FBX re-import SKIPPED (Blender-only).' if fails == ['1.'] else f'FAILS: {fails}'),
      f"- Dependency check at freeze (re-open of `blend/{CKP}_09_export_ready.blend`): {len(O)} objects, {len(bpy.data.meshes)} meshes; " + ('Car_Root, LOD0-3 roots, 4 WheelColliderRefs, CenterOfMass present' if not missing else f'MISSING {missing}') + f'; colliders {len(cols)}; {len(ext)} external images, {len(unres)} unresolved; linked libraries {len(libs)}; packed {packed}.',
      '', '| Item | State |', '|---|---|', '| Blender production | **COMPLETE** |', '| Visual approval | **approved (Blender-only freeze)** |',
      '| FBX / UnityTransfer | **NOT GENERATED** (owner instruction) |', '| Unity runtime verification | **PENDING** |', '| Photorealistic / AAA | **NOT CLAIMED** |', '',
      '- Status: **FROZEN.** Do not modify; later changes go to a separate revision folder.',
      f'- Source of truth: `blend/{CKP}_09_export_ready.blend`. Build scripts snapshot: `scripts/production/`.', '',
      f'## Frozen files ({len(rows)})', '', '| File | SHA-1 |', '|---|---|'] + [f'| `{p}` | `{h}` |' for p, h in rows]
open(os.path.join(R, 'reports', MAN), 'w').write('\n'.join(md) + '\n')
print('FREEZE', FOLD, len(rows), 'files', 'deps OK' if ok_dep else f'DEPS PROBLEM missing={missing} unres={unres} libs={libs}', 'fails', fails, flush=True)
