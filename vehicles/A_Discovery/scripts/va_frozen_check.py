# Re-hash every frozen vehicle release against its *_FINAL_FREEZE.md manifest (read-only). python3 va_frozen_check.py
import glob, hashlib, os, sys
V = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad_total = 0
for man in sorted(glob.glob(os.path.join(V, '*', 'reports', '*_FINAL_FREEZE.md')) + [m for m in glob.glob(os.path.join(V, '*', '*', 'reports', '*_FINAL_FREEZE.md')) if 'UnityTransfer' not in m]):   # + nested fleets (H_TrafficFleet/<vehicle>)
    root = os.path.dirname(os.path.dirname(man)); rows = [l.split('`') for l in open(man) if l.startswith('| `')]
    bad = [r[1] for r in rows if not os.path.exists(os.path.join(root, r[1])) or hashlib.sha1(open(os.path.join(root, r[1]), 'rb').read()).hexdigest() != r[3]]
    bad_total += len(bad); print(f'{os.path.basename(root):16s} {len(rows):4d} files  changed/missing {len(bad)}', bad[:5])
print('FROZEN CHECK', 'PASS' if not bad_total else 'FAIL'); sys.exit(1 if bad_total else 0)
