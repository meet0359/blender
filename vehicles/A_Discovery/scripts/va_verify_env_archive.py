# Verify the external environment archive (owner relocation 2026-10-09) against the Phase A baseline SHA-1s. Read-only. python3 va_verify_env_archive.py [zip path]
# Read-only: hash every environment/ member of the external archive and compare with the workspace baseline sha1s.
import zipfile, hashlib, json
base = json.load(open('/Users/meetshah/Documents/blender/vehicles/A_Discovery/reports/VA_workspace_baseline.json'))['files']
want = {k: v['sha1'] for k, v in base.items() if k.startswith('environment/')}
import sys, os; ZP = sys.argv[1] if len(sys.argv) > 1 else '/Volumes/Denish/Assets/environment.zip'
if not os.path.exists(ZP): print('ENV ZIP VERIFY: NOT RUN - archive not reachable:', ZP); sys.exit(2)
z = zipfile.ZipFile(ZP); ok = bad = 0; missing = set(want)
for n in z.namelist():
    if n in want:
        h = hashlib.sha1()
        with z.open(n) as f:
            for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
        missing.discard(n); ok += h.hexdigest() == want[n]; bad += h.hexdigest() != want[n]
print(f'ENV ZIP VERIFY: {ok} match, {bad} differ, {len(missing)} missing of {len(want)} baseline files', sorted(missing)[:5])
