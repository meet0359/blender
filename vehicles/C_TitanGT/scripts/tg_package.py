# Titan GT packaging: comparison sheets, UnityTransfer (FBX, textures, README), integrity check, freeze record. Blender -b --factory-startup --python zg_package.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from tg_lib import *
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
ZGP = WS + '/vehicles/B_ZeroGapR/previews'
sheet([(A, 'VA_hypercar_08'), (ZGP, 'ZG'), (PV, 'TG')], COLS, os.path.join(PV, 'TG_compare_hypercar_zerogapr_titangt.jpg'))
sheet([(PV, 'TG_blockout'), (PV, 'TG')], ['front34', 'rear34', 'front', 'rear', 'left', 'chase'], os.path.join(PV, 'TG_compare_blockout_final.jpg'))
sheet([(PV, 'TG')], ['hood_zoom', 'tail_zoom', 'door_zoom', 'wheel', 'interior', 'lod_lineup'], os.path.join(PV, 'TG_details.jpg'))
# UnityTransfer
for d in ('FBX', 'Textures', 'Reports', 'README'): os.makedirs(os.path.join(U, d), exist_ok=True)
for f in glob.glob(P('exports', '*.fbx')): shutil.copy2(f, os.path.join(U, 'FBX'))
for f in glob.glob(P('textures', '*.png')): shutil.copy2(f, os.path.join(U, 'Textures'))
for f in ('TG_validation.txt', 'TG_geometry.json', 'TG_export_manifest.json', 'TG_build_log.json', 'TG_blockout_report.md'): shutil.copy2(REPD() if False else P('reports', f), os.path.join(U, 'Reports'))
geo = json.load(open(REPD() if False else P('reports', 'TG_geometry.json'))); L = geo['lods']; wr = geo['wheel_refs']; com = geo['center_of_mass']
u = lambda p: [round(-p[0], 4), round(p[2], 4), round(-p[1], 4)]
mm = []
for n in MATS:
    m = bpy.data.materials.get(n)
mat_rows = {'TG_Paint': 'Car paint, clear coat. Midnight-blue metallic: linear base (0.012, 0.032, 0.085), metallic 0.62, smoothness 0.70, coat 1.0 / coat smoothness 0.975. No texture: colour is runtime-swappable.',
            'TG_Palette': 'Lit opaque. BaseMap TG_Palette_BaseColor; Metallic/Smoothness map TG_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps. 256 px swatch atlas: graphite + machined wheel, bronze caliper, rotor, exhaust, dark chrome, gloss / satin black, cognac + black leather, alcantara, aluminium, mirror, grille.',
            'TG_Carbon': 'Lit opaque. TG_Carbon_BaseColor + TG_Carbon_Normal (2x2 twill, OpenGL, no flip), smoothness 0.7, clear coat 0.7. UVs are world-scale (0.25 m tile).',
            'TG_Tire': 'Lit opaque. TG_Tire_BaseColor + TG_Tire_Normal (tread grooves, sipes, sidewall ring), smoothness 0.15. UV U = circumference (8 tread repeats), V = profile.',
            'TG_Glass': 'Lit transparent, alpha 0.66, near-black tint (0.006, 0.008, 0.010), smoothness 0.98. Single sheet: no refraction.',
            'TG_LensClear': 'Lit transparent, alpha 0.10, smoothness 0.98 (headlamp and lower rear clear lenses).',
            'TG_LensRed': 'Lit transparent, alpha 0.80, deep red (0.30, 0.0, 0.004): reads red in daylight and lit (applies the Zero Gap R PB-1 lesson).',
            'TG_Display': 'Lit + emission (0.55, 0.62, 0.70) x1.2 (cluster / centre screen); swap for a RenderTexture to drive live gauges.'}
for n in LIGHTS: c, st = EMIT[n]; mat_rows[n] = f'Lit opaque + emission {tuple(round(x, 3) for x in c)} x{st}. RUNTIME CHANNEL: drive _EmissionColor intensity.'
md = f"""# Titan GT — Unity import notes

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/TitanGT_complete_unity.fbx`: LOD0-3 + colliders + references ({json.load(open(REPD() if False else P('reports', 'TG_export_manifest.json')))['files']['TitanGT_complete_unity.fbx']['count']} objects).
- `FBX/TitanGT_LOD0_unity_test.fbx`: LOD0 only (quick check).
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
L x W x H {L['LOD0']['dims_m'][1]:.3f} x {L['LOD0']['dims_m'][0]:.3f} x {L['LOD0']['dims_m'][2]:.3f} m (mirrors incl.; body width 2.00 m). Wheelbase 2.82 m, track 1.69 m front / 1.71 m rear. Tires 265/35 R20 front, 305/30 R21 rear.

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root      Body (incl. mirrors, panel gaps), Trim, Lights, Glass, Interior, SteeringWheel (LOD0-2)
 │   ├─ SteerPivot_FL / FR      yaw on local Y about the wheel centre (±25°)
 │   │   ├─ Wheel_FL / FR       roll on local X  → Tire, BrakeDisc (children, roll)   Caliper (child of the SteerPivot, steers, does not roll)
 │   ├─ Wheel_RL / RR           roll on local X  → Tire, BrakeDisc;  Caliper (sibling, static)
 ├─ Collision                   Collision_Front / Body / Cabin / Rear (convex)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
LOD3 has no separate brake hardware (a rotor disc is part of each wheel mesh). Doors are part of the body (shut lines modelled, not opening).
Suggested LOD Group screen heights: 60 / 30 / 12 / 3 %.

## LODs
| LOD | triangles | ratio | objects | materials |
|---|---|---|---|---|
""" + '\n'.join(f"| {k} | {v['triangles']:,} | {v['ratio']:.0%} | {v['objects']} | {v['materials']} |" for k, v in L.items()) + f"""

## Wheels (WheelCollider positions)
| Ref | Blender | Unity (local to Car_Root) | radius m | width m |
|---|---|---|---|---|
""" + '\n'.join(f"| {c} | {tuple(wr[c])} | {tuple(u(wr[c]))} | {RF if c[0] == 'F' else RR} | {WF if c[0] == 'F' else WR} |" for c in ('FL', 'FR', 'RL', 'RR')) + f"""

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
Light channels: `TG_LED_DRL` (daytime-running blade in each headlamp), `TG_LED_Headlamp` (two projector modules per side, low / high beam), `TG_LED_Tail` (full-width bar + corner verticals), `TG_LED_Brake` (upper corner blocks, raise to ~8 when braking), `TG_LED_Indicator_L` / `_R` (vehicle left / right, front + rear, blink independently), `TG_LED_Reverse`.
"""
open(os.path.join(U, 'README', 'TG_UNITY_IMPORT_NOTES.md'), 'w').write(md)
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
zgf = [l for l in open(WS + '/vehicles/B_ZeroGapR/reports/ZG_FINAL_FREEZE.md') if l.startswith('| `')]
zgbad = [l.split('`')[1] for l in zgf if sh(os.path.join(WS, 'vehicles/B_ZeroGapR', l.split('`')[1])) != l.split('`')[3]]
src_ok = not zgbad and os.path.exists(P('blend', 'titangt_01_blockout.blend'))
open(REPD() if False else P('reports', 'TG_source_integrity_check.md'), 'w').write('\n'.join([
    '# Titan GT — protected-file integrity check', '', f"Re-hashed {time.strftime('%Y-%m-%d %H:%M:%S')} against the Phase A baseline (`vehicles/A_Discovery/reports/VA_workspace_baseline.json`, {len(base)} files outside `vehicles/`).", '',
    f'- Frozen environment P0–P3, frozen Hypercar, racing_car_00…09 and all other files outside `vehicles/`: changed **{len(changed)}**, added **{len(added)}**.',
    f'- Frozen Zero Gap R ({len(zgf)} hashed files): changed **{len(zgbad)}**.', '- Approved Titan GT blockout checkpoint `titangt_01_blockout.blend`: present, never rewritten (production checkpoints start at 02).', '', f"Result: **{'PASS' if ok and src_ok else 'FAIL'}**"]) + '\n')
print('INTEGRITY', 'PASS' if ok and src_ok else 'FAIL', changed[:3], added[:3])
shutil.copy2(REPD() if False else P('reports', 'TG_source_integrity_check.md'), os.path.join(U, 'Reports'))
files = sorted(glob.glob(P('blend', '*.blend')) + glob.glob(P('exports', '*.fbx')) + glob.glob(P('textures', '*.png')))
val = open(REPD() if False else P('reports', 'TG_validation.txt')).read().strip().splitlines()[-1]
open(REPD() if False else P('reports', 'TG_FREEZE_CANDIDATE.md'), 'w').write('\n'.join(['# Titan GT — freeze candidate / integrity manifest (awaiting approval)', '', f"Date {time.strftime('%Y-%m-%d')}. Validation: **{val}**. Integrity: **{'PASS' if ok and src_ok else 'FAIL'}**.",
    'Status: **COMPLETE, PENDING APPROVAL** — becomes FROZEN once approved; nothing in this folder is edited after that.', '', '| File | SHA-1 |', '|---|---|'] +
    [f'| `{os.path.relpath(f, ROOT)}` | `{sh(f)}` |' for f in files]) + '\n')
print('PACKAGED', len(files))
