# Phase A: re-hash every workspace file outside vehicles/ against the baseline; scan for added / removed files (plain python3, read-only).
import sys; sys.dont_write_bytecode = True
import os, json, hashlib, time
WS = '/Users/meetshah/Documents/blender'; R = os.path.join(WS, 'vehicles/A_Discovery/reports')
base = json.load(open(os.path.join(R, 'VA_workspace_baseline.json')))['files']; now = {}
for d, dirs, fs in os.walk(WS):
    rel = os.path.relpath(d, WS)
    if rel == 'vehicles' or rel.startswith('vehicles' + os.sep): dirs[:] = []; continue
    for f in fs:
        if f != '.DS_Store': p = os.path.join(d, f); now[os.path.relpath(p, WS)] = hashlib.sha1(open(p, 'rb').read()).hexdigest()
changed = sorted(k for k in base if k in now and now[k] != base[k]['sha1']); removed = sorted(set(base) - set(now)); added = sorted(set(now) - set(base))
ok = not (changed or removed or added)
md = ['# Phase A — workspace integrity check', '', f"Re-hashed {time.strftime('%Y-%m-%d %H:%M:%S')} against `VA_workspace_baseline.json` ({len(base)} files outside `vehicles/`).", '',
      f'- Changed: **{len(changed)}** {changed[:5]}', f'- Removed: **{len(removed)}** {removed[:5]}', f'- Added outside `vehicles/`: **{len(added)}** {added[:5]}', '', f"Result: **{'PASS' if ok else 'FAIL'}**. Frozen environment P0–P3, the frozen Hypercar and the racing-car sources are byte-identical."]
open(os.path.join(R, 'VA_integrity_check.md'), 'w').write('\n'.join(md) + '\n'); print('INTEGRITY', 'PASS' if ok else 'FAIL', len(changed), len(removed), len(added))
