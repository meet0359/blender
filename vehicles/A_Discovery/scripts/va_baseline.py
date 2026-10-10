# Phase A: SHA-1 integrity baseline of every workspace file outside vehicles/ (plain python3, read-only).
import sys; sys.dont_write_bytecode = True
import os, json, hashlib, time
WS = '/Users/meetshah/Documents/blender'; OUT = os.path.join(WS, 'vehicles/A_Discovery/reports/VA_workspace_baseline.json')
files = {}
for d, dirs, fs in os.walk(WS):
    rel = os.path.relpath(d, WS)
    if rel == 'vehicles' or rel.startswith('vehicles' + os.sep): dirs[:] = []; continue
    for f in fs:
        if f == '.DS_Store': continue
        p = os.path.join(d, f); r = os.path.relpath(p, WS)
        files[r] = dict(sha1=hashlib.sha1(open(p, 'rb').read()).hexdigest(), bytes=os.path.getsize(p))
grp = lambda pre: sum(1 for k in files if k.startswith(pre))
groups = {'environment (P0-P3, frozen)': grp('environment/'), 'new_car (Hypercar, frozen)': grp('new_car/'), 'racing_car_*.blend (root)': grp('racing_car_'),
          'handoff bundles': grp('handoff_'), 'root scripts/': grp('scripts/'), 'root textures/': grp('textures/')}
groups['other root files'] = len(files) - sum(groups.values())
assert not os.path.exists(OUT), 'baseline already recorded: ' + OUT
json.dump(dict(taken=time.strftime('%Y-%m-%d %H:%M:%S'), scope='every workspace file outside vehicles/ (excl. .DS_Store)', file_count=len(files), groups=groups, files=files), open(OUT, 'w'), indent=1)
print('BASELINE', len(files), groups)
