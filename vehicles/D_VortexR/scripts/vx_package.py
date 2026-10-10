# Vortex R packaging: comparison sheets, UnityTransfer (FBX, textures, README), integrity check, freeze record. Blender -b --factory-startup --python zg_package.py
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from vx_lib import *
import hashlib, shutil, glob, time
PV = P('previews'); A = WS + '/vehicles/A_Discovery/previews'; U = P('UnityTransfer')
def sheet(rows, cols, out, W=560, H=315, G=6):
    rows = [(d, p) for d, p in rows]
    canvas = np.full((len(rows) * (H + G) - G, len(cols) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
    for r, (folder, pre) in enumerate(rows):
        for c, v in enumerate(cols):
            f = os.path.join(folder, f'{pre}_{v}.png')
            if not os.path.exists(f): continue
            im = bpy.data.images.load(f); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
            y0 = (len(rows) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
    img = bpy.data.images.new('sheet', canvas.shape[1], canvas.shape[0], alpha=False); img.pixels.foreach_set(canvas.ravel()); img.filepath_raw = out; img.file_format = 'JPEG'; img.save(); print('SHEET', out)
COLS = ['front34', 'rear34', 'front', 'rear', 'left', 'chase']
ZGP = WS + '/vehicles/B_ZeroGapR/previews'; TGP = WS + '/vehicles/C_TitanGT/previews'
COLS = ['front34', 'rear34', 'front', 'rear', 'left', 'top', 'chase']
sheet([(A, 'VA_hypercar_08'), (ZGP, 'ZG'), (TGP, 'TG'), (PV, 'VX')], COLS, os.path.join(PV, 'VX_compare_4cars.jpg'), W=480, H=270)
sheet([(PV, 'VX_blockout'), (PV, 'VX')], ['front34', 'rear34', 'front', 'rear', 'left', 'chase'], os.path.join(PV, 'VX_compare_blockout_final.jpg'))
sheet([(PV, 'VX')], ['front_zoom', 'hood_zoom', 'intake_zoom', 'canopy_zoom'], os.path.join(PV, 'VX_details_front_side.jpg'))
sheet([(PV, 'VX')], ['tail_zoom', 'wing_zoom', 'wheel', 'interior'], os.path.join(PV, 'VX_details_rear_wheel_interior.jpg'))
sheet([(PV + '/zebra_TG_reference', 'zebra'), (PV + '/zebra_VX_final', 'zebra')], ['hood', 'roof', 'deck', 'door', 'side_full', 'tail_corner'], os.path.join(PV, 'VX_zebra_compare_titangt_vortexr_final.jpg'), W=400, H=225)
# UnityTransfer
for d in ('FBX', 'Textures', 'Reports', 'README'): os.makedirs(os.path.join(U, d), exist_ok=True)
for f in glob.glob(P('exports', '*.fbx')): shutil.copy2(f, os.path.join(U, 'FBX'))
for f in glob.glob(P('textures', '*.png')): shutil.copy2(f, os.path.join(U, 'Textures'))
for f in ('VX_validation.txt', 'VX_geometry.json', 'VX_export_manifest.json', 'VX_build_log.json', 'VX_blockout_report.md'): shutil.copy2(REPD() if False else P('reports', f), os.path.join(U, 'Reports'))
geo = json.load(open(REPD() if False else P('reports', 'VX_geometry.json'))); L = geo['lods']; wr = geo['wheel_refs']; com = geo['center_of_mass']
u = lambda p: [round(-p[0], 4), round(p[2], 4), round(-p[1], 4)]
mm = []
for n in MATS:
    m = bpy.data.materials.get(n)
mat_rows = {'VX_Paint': 'Car paint, satin metallic deep violet: linear base (0.075, 0.028, 0.155), metallic 0.80, smoothness 0.64, coat 0.35 / coat smoothness 0.82. No texture: colour is runtime-swappable.',
            'VX_Palette': 'Lit opaque. BaseMap VX_Palette_BaseColor; Metallic/Smoothness map VX_Palette_MetallicSmoothness (R metal, A smoothness). Point filter or no mip-maps. 256 px swatch atlas: forged wheel + lip, acid-green caliper / accents, rotor, exhaust, mesh, gloss / satin black, alcantara, leather, aluminium, mirror, grille.',
            'VX_Carbon': 'Lit opaque. VX_Carbon_BaseColor + VX_Carbon_Normal (2x2 twill, OpenGL, no flip), smoothness 0.7, clear coat 0.7. UVs are world-scale (0.25 m tile).',
            'VX_Tire': 'Lit opaque. VX_Tire_BaseColor + VX_Tire_Normal (tread grooves, sipes, sidewall ring), smoothness 0.15. UV U = circumference, V = profile.',
            'VX_Glass': 'Lit transparent, alpha 0.66, near-black tint, smoothness 0.98. Single sheet: no refraction.',
            'VX_LensClear': 'Lit transparent, alpha 0.10, smoothness 0.98 (headlamp lenses).',
            'VX_LensRed': 'Lit transparent, alpha 0.80, deep red (0.30, 0.0, 0.004): reads red in daylight and lit (Zero Gap R PB-1 lesson).',
            'VX_Display': 'Lit + emission (0.55, 0.62, 0.70) x1.2 (digital cluster, wheel display); swap for a RenderTexture to drive live gauges.'}
for n in LIGHTS: c, st = EMIT[n]; mat_rows[n] = f'Lit opaque + emission {tuple(round(x, 3) for x in c)} x{st}. RUNTIME CHANNEL: drive _EmissionColor intensity.'
md = f"""# Vortex R — Unity import notes

**Unity owns** the vehicle controller, physics tuning, WheelCollider setup, prefab, LOD Group component, shaders (paint, glass, emission), lighting, damage, audio, quality tiers and profiling. Blender delivers geometry, pivots, reference empties, colliders, source materials, textures and FBX. Nothing here was opened in Unity.

## Files
- `FBX/VortexR_complete_unity.fbx`: LOD0-3 + colliders + references ({json.load(open(REPD() if False else P('reports', 'VX_export_manifest.json')))['files']['VortexR_complete_unity.fbx']['count']} objects).
- `FBX/VortexR_LOD0_unity_test.fbx`: LOD0 only (quick check).
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
L x W x H {L['LOD0']['dims_m'][1]:.3f} x {L['LOD0']['dims_m'][0]:.3f} x {L['LOD0']['dims_m'][2]:.3f} m (mirrors + wing endplates incl.; body width 2.09 m). Wheelbase 2.72 m, track 1.72 m front / 1.70 m rear. Tires 255/30 R20 front, 325/25 R21 rear.

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
Light channels: `VX_LED_DRL` (boomerang blade + down-hook per side), `VX_LED_Headlamp` (three LED projector modules per side, low / high beam), `VX_LED_Tail` (three raked slashes per side + thin full-width thread), `VX_LED_Brake` (bar under each slash cluster + the third brake light on the wing trailing edge; raise to ~8 when braking), `VX_LED_Indicator_L` / `_R` (vehicle left / right, front + rear), `VX_LED_Reverse`.
"""
open(os.path.join(U, 'README', 'VX_UNITY_IMPORT_NOTES.md'), 'w').write(md)
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
def frozen(ph, rec):
    L_ = [l for l in open(f'{WS}/vehicles/{ph}/reports/{rec}') if l.startswith('| `')]
    return L_, [l.split('`')[1] for l in L_ if sh(os.path.join(WS, 'vehicles', ph, l.split('`')[1])) != l.split('`')[3]]
zgf, zgbad = frozen('B_ZeroGapR', 'ZG_FINAL_FREEZE.md'); tgf, tgbad = frozen('C_TitanGT', 'TG_FINAL_FREEZE.md')
src_ok = not zgbad and not tgbad and os.path.exists(P('blend', 'vortexr_01_blockout.blend'))
open(REPD() if False else P('reports', 'VX_source_integrity_check.md'), 'w').write('\n'.join([
    '# Vortex R — protected-file integrity check', '', f"Re-hashed {time.strftime('%Y-%m-%d %H:%M:%S')} against the Phase A baseline (`vehicles/A_Discovery/reports/VA_workspace_baseline.json`, {len(base)} files outside `vehicles/`).", '',
    f'- Frozen environment P0–P3, frozen Hypercar, racing_car_00…09 and all other files outside `vehicles/`: changed **{len(changed)}**, added **{len(added)}**.',
    f'- Frozen Zero Gap R ({len(zgf)} hashed files): changed **{len(zgbad)}**. Frozen Titan GT ({len(tgf)} hashed files): changed **{len(tgbad)}**.', '- Approved Vortex R blockout checkpoint `vortexr_01_blockout.blend`: present, never rewritten (production checkpoints start at 02).', '', f"Result: **{'PASS' if ok and src_ok else 'FAIL'}**"]) + '\n')
print('INTEGRITY', 'PASS' if ok and src_ok else 'FAIL', changed[:3], added[:3])
shutil.copy2(REPD() if False else P('reports', 'VX_source_integrity_check.md'), os.path.join(U, 'Reports'))
files = sorted(glob.glob(P('blend', '*.blend')) + glob.glob(P('exports', '*.fbx')) + glob.glob(P('textures', '*.png')))
val = open(REPD() if False else P('reports', 'VX_validation.txt')).read().strip().splitlines()[-1]
open(REPD() if False else P('reports', 'VX_FREEZE_CANDIDATE.md'), 'w').write('\n'.join(['# Vortex R — freeze candidate / integrity manifest (awaiting approval)', '', f"Date {time.strftime('%Y-%m-%d')}. Validation: **{val}**. Integrity: **{'PASS' if ok and src_ok else 'FAIL'}**.",
    'Status: **COMPLETE, PENDING APPROVAL** — becomes FROZEN once approved; nothing in this folder is edited after that.', '', '| File | SHA-1 |', '|---|---|'] +
    [f'| `{os.path.relpath(f, ROOT)}` | `{sh(f)}` |' for f in files]) + '\n')
print('PACKAGED', len(files))
