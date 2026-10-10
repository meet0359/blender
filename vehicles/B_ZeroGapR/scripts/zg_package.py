# Zero Gap R packaging: comparison sheets, UnityTransfer (FBX, textures, README), integrity check, freeze record. Blender -b --factory-startup --python zg_package.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from zg_lib import *
import hashlib, shutil, glob, time
PV = P('previews'); A = WS + '/vehicles/A_Discovery/previews'; U = P('UnityTransfer')
def sheet(rows, cols, out, W=560, H=315, G=6):
    canvas = np.full((len(rows) * (H + G) - G, len(cols) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
    for r, (folder, pre) in enumerate(rows):
        for c, v in enumerate(cols):
            f = os.path.join(folder, f'{pre}_{v}.png')
            if not os.path.exists(f): continue
            im = bpy.data.images.load(f); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
            y0 = (len(rows) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
    img = bpy.data.images.new('sheet', canvas.shape[1], canvas.shape[0], alpha=False); img.pixels.foreach_set(canvas.ravel()); img.filepath_raw = out; img.file_format = 'JPEG'; img.save(); print('SHEET', out)
COLS = ['front34', 'rear34', 'front', 'rear', 'left', 'chase']
sheet([(A, 'VA_racing_car_09'), (PV, 'ZG'), (A, 'VA_hypercar_08')], COLS, os.path.join(PV, 'ZG_compare_source_remaster_hypercar.jpg'))
sheet([(A, 'VA_racing_car_09'), (PV, 'ZG')], ['front_close' if False else 'front34', 'interior', 'wheel', 'top'], os.path.join(PV, 'ZG_compare_details_before_after.jpg'))
# UnityTransfer
for d in ('FBX', 'Textures', 'Reports', 'README'): os.makedirs(os.path.join(U, d), exist_ok=True)
for f in glob.glob(P('exports', '*.fbx')): shutil.copy2(f, os.path.join(U, 'FBX'))
for f in glob.glob(P('textures', '*.png')): shutil.copy2(f, os.path.join(U, 'Textures'))
for f in ('ZG_validation.txt', 'ZG_geometry.json', 'ZG_export_manifest.json', 'ZG_build_log.json'): shutil.copy2(P('reports', f), os.path.join(U, 'Reports'))
geo = json.load(open(P('reports', 'ZG_geometry.json'))); L = geo['lods']; wr = geo['wheel_refs']; com = geo['center_of_mass']
u = lambda p: [round(-p[0], 4), round(p[2], 4), round(-p[1], 4)]
mm = []
for n in MATS:
    m = bpy.data.materials.get(n)
mat_rows = {'ZG_Paint': 'Car paint, clear coat. Linear base (0.58, 0.018, 0.024), metallic 0.55, smoothness 0.72, coat 1.0 / coat smoothness 0.97. No texture: colour is runtime-swappable.',
            'ZG_Palette': 'Lit opaque. BaseMap ZG_Palette_BaseColor; Metallic/Smoothness map ZG_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps (256 px swatch atlas: trim, black plastic, chrome, wheel metal, caliper, rotor, interior leather / alcantara / plastic / metal, grille, mirror, exhaust).',
            'ZG_Carbon': 'Lit opaque. ZG_Carbon_BaseColor + ZG_Carbon_Normal (OpenGL, no flip), smoothness 0.7, clear coat 0.6. UVs are world-scale (0.25 m tile).',
            'ZG_Tire': 'Lit opaque. ZG_Tire_BaseColor + ZG_Tire_Normal (sidewall lettering baked), smoothness 0.18.',
            'ZG_Glass': 'Lit transparent, alpha 0.42, near-black tint (0.015, 0.02, 0.025), smoothness 0.98. Single thin sheet: no refraction, no double-sided darkening.',
            'ZG_LensClear': 'Lit transparent, alpha 0.12, smoothness 0.98 (headlight outer lens).', 'ZG_LensRed': 'Lit transparent, alpha 0.55, smoked red (0.22, 0.004, 0.008) (tail-light outer lens).',
            'ZG_Display': 'Lit + emission (0.10, 0.35, 0.60) x1.4 (cluster / screen); swap for a RenderTexture to drive live gauges.'}
for n in LIGHTS: c, st = EMIT[n]; mat_rows[n] = f'Lit opaque + emission {tuple(round(x, 3) for x in c)} x{st}. RUNTIME CHANNEL: drive _EmissionColor intensity.'
md = f"""# Zero Gap R — Unity import notes

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/ZeroGapR_complete_unity.fbx`: LOD0-3 + colliders + references ({json.load(open(P('reports', 'ZG_export_manifest.json')))['files']['ZeroGapR_complete_unity.fbx']['count']} objects).
- `FBX/ZeroGapR_LOD0_unity_test.fbx`: LOD0 only (quick check).
- `Textures/`: 7 PNGs (palette 256 px x 3, carbon 1 K x 2, tire 1 K x 2). Copy next to the FBX folder structure or reassign by name.

## Importer
Scale Factor 1, Convert Units ON, **Bake Axis Conversion OFF** (axes are baked in the file; Car_Root identity). Normals Import, Tangents Import / Calculate (MikkTSpace). Animation Type None. Generate Colliders OFF.

| | Blender | Unity |
|---|---|---|
| forward | -Y | **+Z** |
| up | +Z | **+Y** |
| vehicle left | +X | **-X** |
| point | (x, y, z) | (-x, z, -y) |

## Dimensions
L x W x H {L['LOD0']['dims_m'][1]:.3f} x {L['LOD0']['dims_m'][0]:.3f} x {L['LOD0']['dims_m'][2]:.3f} m (mirrors incl.). Wheelbase 2.70 m, track 1.65 m front / 1.67 m rear.

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root      Body, Door_L, Door_R, Trim, Lights, Glass, Interior, SteeringWheel (LOD0-2)
 │   ├─ SteerPivot_FL / FR      yaw on local Y about the wheel centre (±25°)
 │   │   ├─ Wheel_FL / FR       roll on local X  → Tire, BrakeDisc (children, roll)   Caliper (child of the SteerPivot, steers, does not roll)
 │   ├─ Wheel_RL / RR           roll on local X  → Tire, BrakeDisc;  Caliper (sibling, static)
 ├─ Collision                   Collision_Front / Body / Cabin / Rear (convex)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
LOD3 has no separate brake hardware (a rotor disc is part of each wheel mesh). Door_L / Door_R pivots sit on the front (hinge) edge.
Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

## LODs
| LOD | triangles | ratio | objects | materials |
|---|---|---|---|---|
""" + '\n'.join(f"| {k} | {v['triangles']:,} | {v['ratio']:.0%} | {v['objects']} | {v['materials']} |" for k, v in L.items()) + f"""

## Wheels (WheelCollider positions)
| Ref | Blender | Unity (local to Car_Root) | radius m | width m |
|---|---|---|---|---|
""" + '\n'.join(f"| {c} | {tuple(wr[c])} | {tuple(u(wr[c]))} | {.3445 if c[0] == 'F' else .3645} | {.296 if c[0] == 'F' else .336} |" for c in ('FL', 'FR', 'RL', 'RR')) + f"""

Drive visual wheels from `WheelCollider.GetWorldPose` (Unity mirrors X on import).

## Centre of mass
`CenterOfMass` Blender {tuple(com)} → Unity local {tuple(u(com))}. Assign `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Colliders
""" + '\n'.join(f"- `{n}`: {d['tris']} tris, closed, convex" for n, d in geo['colliders'].items()) + """
MeshCollider with **Convex ON**, renderers off, vehicle physics layer.

## Materials (15)
| Material | Unity setup |
|---|---|
""" + '\n'.join(f'| `{n}` | {mat_rows[n]} |' for n in MATS) + """

Smoothness = 1 - roughness. Normal maps are OpenGL (+Y): Texture Type Normal map, no flip.
Light channels: `ZG_LED_DRL` (daytime running, front blades + headlamp DRL), `ZG_LED_Headlamp` (projectors, low / high beam), `ZG_LED_Tail` (tail bars), `ZG_LED_Brake` (brake segments, raise to ~8 when braking), `ZG_LED_Indicator_L` / `_R` (vehicle left / right, front + rear, blink independently), `ZG_LED_Reverse`.
"""
open(os.path.join(U, 'README', 'ZG_UNITY_IMPORT_NOTES.md'), 'w').write(md)
# integrity
base = json.load(open(WS + '/vehicles/A_Discovery/reports/VA_workspace_baseline.json'))['files']
sh = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()
changed = [k for k, v in base.items() if not os.path.exists(os.path.join(WS, k)) or sh(os.path.join(WS, k)) != v['sha1']]
now = set()
for d, dirs, fs in os.walk(WS):
    rel = os.path.relpath(d, WS)
    if rel == 'vehicles' or rel.startswith('vehicles' + os.sep): dirs[:] = []; continue
    now |= {os.path.relpath(os.path.join(d, f), WS) for f in fs if f != '.DS_Store'}
added = sorted(now - set(base)); ok = not changed and not added
src_ok = sh(WS + '/racing_car_09_unity_export_ready.blend') == base['racing_car_09_unity_export_ready.blend']['sha1']
open(P('reports', 'ZG_source_integrity_check.md'), 'w').write('\n'.join([
    '# Zero Gap R — protected-file integrity check', '', f"Re-hashed {time.strftime('%Y-%m-%d %H:%M:%S')} against the Phase A baseline (`vehicles/A_Discovery/reports/VA_workspace_baseline.json`, {len(base)} files outside `vehicles/`).", '',
    f'- Original source `racing_car_09_unity_export_ready.blend`: **{"UNCHANGED" if src_ok else "CHANGED"}** (read-only; a read-only copy sits in `source_import/`).',
    f'- Frozen environment P0–P3, frozen Hypercar, racing_car_00…09 and all other files: changed **{len(changed)}**, added outside `vehicles/` **{len(added)}**.', '', f"Result: **{'PASS' if ok and src_ok else 'FAIL'}**"]) + '\n')
print('INTEGRITY', 'PASS' if ok and src_ok else 'FAIL', changed[:3], added[:3])
shutil.copy2(P('reports', 'ZG_source_integrity_check.md'), os.path.join(U, 'Reports'))
files = sorted(glob.glob(P('blend', '*.blend')) + glob.glob(P('exports', '*.fbx')) + glob.glob(P('textures', '*.png')))
val = open(P('reports', 'ZG_validation.txt')).read().strip().splitlines()[-1]
open(P('reports', 'ZG_FREEZE_CANDIDATE.md'), 'w').write('\n'.join(['# Zero Gap R — freeze candidate (awaiting visual approval)', '', f"Date {time.strftime('%Y-%m-%d')}. Validation: **{val}**. Integrity: **{'PASS' if ok and src_ok else 'FAIL'}**.",
    'Status: **COMPLETE, PENDING APPROVAL** — becomes FROZEN once approved; nothing in this folder is edited after that.', '', '| File | SHA-1 |', '|---|---|'] +
    [f'| `{os.path.relpath(f, ROOT)}` | `{sh(f)}` |' for f in files]) + '\n')
print('PACKAGED', len(files))
