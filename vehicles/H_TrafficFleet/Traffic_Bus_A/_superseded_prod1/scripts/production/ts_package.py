# Traffic fleet packaging (read-only on the model): review sheets, UnityTransfer (FBX, textures, reports, README), integrity check, freeze-candidate manifest.
#   Blender -b --factory-startup --python ts_package.py -- <Vehicle_Folder> <ckp_prefix> <FBX_base> <PaintPrefix>
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from ts_lib import *
import hashlib, shutil, glob, time
VEH, PFX, BASE, PP = sys.argv[sys.argv.index('--') + 1:][:4]; ROOT = vroot(VEH); P_ = lambda *a: os.path.join(ROOT, *a); PV = P_('previews'); U = P_('UnityTransfer')
def sheet(rows, cols, out, W=560, H=315, G=6):
    canvas = np.full((len(rows) * (H + G) - G, len(cols) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
    for r, (folder, pre) in enumerate(rows):
        for c, v in enumerate(cols):
            f = os.path.join(folder, f'{pre}_{v}.png')
            if not os.path.exists(f): print('MISSING', f); continue
            im = bpy.data.images.load(f); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
            y0 = (len(rows) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
    img = bpy.data.images.new('sheet', canvas.shape[1], canvas.shape[0], alpha=False); img.pixels.foreach_set(canvas.ravel()); img.filepath_raw = out; img.file_format = 'JPEG'; img.save(); bpy.data.images.remove(img); print('SHEET', out)
S_ = lambda n: os.path.join(PV, f'{BASE}_{n}.jpg')
sheet([(PV, BASE)] * 2, ['front34', 'rear34', 'front'], S_('sheet_studio_a'), W=640, H=360) if False else None
sheet([(PV, BASE)], ['front34', 'rear34', 'front', 'rear'], S_('sheet_studio_1')); sheet([(PV, BASE)], ['side', 'top', 'wheel', 'interior'], S_('sheet_studio_2'))
sheet([(PV, BASE)], ['front_detail', 'rear_detail', 'wheel', 'interior'], S_('sheet_details'))
sheet([(PV, BASE)], ['day_front34', 'day_rear34', 'day_side'], S_('sheet_daylight')); sheet([(PV, BASE)], ['game_close', 'game_normal', 'game_far'], S_('sheet_game_camera'))
sheet([(os.path.join(PV, 'lod'), f'LOD{k}') for k in range(4)], ['front34', 'side', 'game_close', 'game_normal'], S_('sheet_lod_comparison'), W=480, H=270)
sheet([(os.path.join(PV, 'variants'), n) for n in ('white', 'silver', 'graphite')], ['front34'], S_('sheet_paint_variants_a'), W=640, H=360)
sheet([(os.path.join(PV, 'variants'), n) for n in ('black', 'red', 'blue')], ['front34'], S_('sheet_paint_variants_b'), W=640, H=360)
sheet([(os.path.join(PV, 'lights'), 'off'), (os.path.join(PV, 'lights'), 'on')], ['front_detail', 'rear_detail'], S_('sheet_lights_off_on'), W=640, H=360)
ZV = ['hood', 'roof', 'deck', 'deck_r', 'door', 'side_full', 'quarter', 'quarter_r', 'tail_corner', 'tail_corner_r']
sheet([(os.path.join(PV, 'zebra_master'), 'zebra'), (os.path.join(PV, 'zebra_game'), 'zebra')], ZV, S_('sheet_zebra_master_vs_game'), W=360, H=203)
HC = os.path.join(PV, 'h1_compare')
if os.path.isdir(HC):                                                                                 # revision: original vs revision, identical cameras + lighting
    sheet([(HC, 'H1'), (HC, 'R2')], ['front34', 'rear34', 'side'], S_('sheet_H1_vs_r2_overall'), W=640, H=360)
    sheet([(HC, 'H1'), (HC, 'R2')], ['rear', 'bumper_rear', 'lamp_rear'], S_('sheet_H1_vs_r2_rear'), W=640, H=360)
    sheet([(HC, 'H1'), (HC, 'R2')], ['front', 'bumper_front', 'arch_rear'], S_('sheet_H1_vs_r2_front_arch'), W=640, H=360)
    sheet([(HC, 'H1'), (HC, 'R2')], ['wheel', 'interior', 'day_rear34', 'game_close'], S_('sheet_H1_vs_r2_wheel_interior_day_game'), W=560, H=315)
    sheet([(PV, BASE)], ['bumper_front', 'bumper_rear', 'lamp_front', 'lamp_rear'], S_('sheet_closeups_bumpers_lamps'))
    sheet([(PV, BASE)], ['plate_rear', 'arch_rear', 'wheel', 'interior'], S_('sheet_closeups_plate_arch_wheel_interior'))
    sheet([(PV, BASE)], ['ortho_front', 'ortho_rear', 'ortho_side'], S_('sheet_orthographic'), W=640, H=360)
    sheet([(os.path.join(PV, 'lod'), f'LOD{k}') for k in range(4)], ['front34', 'rear34', 'side', 'game_close', 'game_normal'], S_('sheet_lod_comparison'), W=440, H=248)
    sheet([(os.path.join(PV, 'lights'), 'off'), (os.path.join(PV, 'lights'), 'on')], ['lamp_front', 'lamp_rear'], S_('sheet_lights_off_on'), W=640, H=360)
RC = os.path.join(PV, 'r2_compare')
if os.path.isdir(RC):                                                                                 # r3: r2 vs r3, identical cameras + lighting (r2 rendered read-only from its own export file)
    sheet([(RC, 'R2'), (RC, 'R3')], ['lamp_front', 'lamp_front_R'], S_('sheet_r2_vs_r3_front_fender'), W=800, H=450)
    sheet([(RC, 'R2'), (RC, 'R3')], ['quarter_rear_L', 'quarter_rear_R'], S_('sheet_r2_vs_r3_rear_quarter'), W=800, H=450)
    sheet([(RC, 'R2'), (RC, 'R3')], ['bumper_front', 'bumper_rear'], S_('sheet_r2_vs_r3_bumper_corners'), W=800, H=450)
    sheet([(RC, 'R2'), (RC, 'R3')], ['front34', 'rear34', 'side'], S_('sheet_r2_vs_r3_overall'), W=640, H=360)
    sheet([(RC, 'R2'), (RC, 'R3')], ['interior', 'day_glass'], S_('sheet_r2_vs_r3_glass_interior'), W=800, H=450)
    R2Z = os.path.join(FLEET, 'Traffic_Sedan_A_r2', 'previews', 'zebra_game')
    sheet([(R2Z, 'zebra'), (os.path.join(PV, 'zebra_game'), 'zebra'), (os.path.join(PV, 'zebra_master'), 'zebra')], ZV, S_('sheet_zebra_r2game_r3game_r3master'), W=360, H=203)
    sheet([(os.path.join(PV, 'zebra_diag'), n) for n in ('R2', 'R3')], ['fender_L', 'fender_R', 'quarter_L', 'quarter_R'], S_('sheet_zebra_artifact_zones_r2_vs_r3'), W=500, H=350)
    sheet([(os.path.join(PV, 'lod'), f'LOD{k}') for k in range(4)], ['front34', 'rear34', 'side', 'game_close', 'game_normal'], S_('sheet_lod_comparison'), W=440, H=248)
QA = os.path.join(PV, 'qa')
if os.path.isdir(QA):                                                                                 # generic QA looks + close-ups (any vehicle rendered with the r3+ set)
    for look in ('clay', 'wire', 'normal'): sheet([(QA, look)], ['front34', 'rear34', 'lamp_front', 'bumper_rear'], S_(f'sheet_qa_{look}'))
    sheet([(QA, 'clay'), (QA, 'wire')], ['bumper_front', 'bumper_rear', 'arch_rear', 'side'], S_('sheet_qa_clay_wire_details'))
    sheet([(PV, BASE)], ['wheel', 'interior', 'day_glass', 'plate_rear'], S_('sheet_closeups_wheel_glass_plate'))
    sheet([(PV, BASE)], ['bumper_front', 'bumper_rear', 'lamp_front', 'lamp_rear'], S_('sheet_closeups_bumpers_lamps'))
    sheet([(PV, BASE)], ['ortho_front', 'ortho_rear', 'ortho_side'], S_('sheet_orthographic'), W=640, H=360)
    sheet([(os.path.join(PV, 'lod'), f'LOD{k}') for k in (2, 3)], ['game_normal', 'game_far'], S_('sheet_distant_lods_plates'), W=800, H=450)
    sheet([(os.path.join(PV, 'lod'), f'LOD{k}') for k in range(4)], ['front34', 'rear34', 'side', 'game_close', 'game_normal'], S_('sheet_lod_comparison'), W=440, H=248)
ZD = os.path.join(PV, 'zebra_diag')
if os.path.isfile(os.path.join(ZD, 'A_Blamp.png')):                                                    # master (A) vs baked game mesh (C) in the critical zones
    sheet([(ZD, 'A'), (ZD, 'C')], ['Blamp', 'Bfront', 'Bhood', 'Bquarter_L', 'Bquarter_R', 'Btail'], S_('sheet_zebra_zones_master_vs_game'), W=420, H=294)
CA = os.path.join(PV, 'blockout', 'compare_A'); RA = os.path.join(FLEET, 'Traffic_Sedan_A_r3', 'previews')
if os.path.isdir(CA):                                                                                 # frozen Sedan A r3 vs this vehicle: identical cameras, lights, samples (row 1 = A)
    sheet([(CA, 'SedanA'), (PV, BASE)], ['front34', 'rear34', 'side'], S_('sheet_SedanA_r3_vs_SedanB_threequarter_side'), W=800, H=450)
    sheet([(CA, 'SedanA'), (PV, BASE)], ['front', 'rear', 'top'], S_('sheet_SedanA_r3_vs_SedanB_front_rear_top'), W=800, H=450)
    sheet([(CA, 'clayA'), (QA, 'clay')], ['front34', 'rear34', 'side'], S_('sheet_SedanA_r3_vs_SedanB_clay'), W=800, H=450)
    sheet([(RA, 'TrafficSedanA'), (PV, BASE)], ['game_close', 'game_normal', 'game_far'], S_('sheet_SedanA_r3_vs_SedanB_chase'), W=800, H=450)
    sheet([(os.path.join(RA, 'zebra_game'), 'zebra'), (os.path.join(PV, 'zebra_game'), 'zebra')], ZV, S_('sheet_zebra_SedanA_r3_vs_SedanB_game'), W=360, H=203)
H0 = os.path.join(FLEET, 'previews', 'h0_audit')
sheet([(H0, 'VXr1'), (PV, BASE)], ['front34', 'wheel', 'rear_detail'], S_('sheet_realism_vs_h0_audit'), W=640, H=360)
# ---- UnityTransfer (skipped with TS_NO_UNITY=1: sheets + integrity + candidate manifest only)
NO_UNITY = bool(os.environ.get('TS_NO_UNITY'))
if not NO_UNITY:
    for d in ('FBX', 'Textures', 'Textures/Shared', 'Reports', 'README'): os.makedirs(os.path.join(U, d), exist_ok=True)
if not NO_UNITY:
    for f in glob.glob(P_('exports', '*.fbx')): shutil.copy2(f, os.path.join(U, 'FBX'))
if not NO_UNITY:
    for f in glob.glob(P_('textures', '*.png')): shutil.copy2(f, os.path.join(U, 'Textures'))
man = json.load(open(P_('reports', f'{PFX}_export_manifest.json'))); shared = [t for t in man['textures'] if t.startswith('TS_') and os.path.exists(os.path.join(SHARED_TEX, t))]
if not NO_UNITY:
    for t in shared: shutil.copy2(os.path.join(SHARED_TEX, t), os.path.join(U, 'Textures', 'Shared'))
if not NO_UNITY:
    for t in ('TS_Atlas_MetallicSmoothness.png', 'TS_Lights_ChannelID.png', 'TS_PaintFlake_Normal.png'): shutil.copy2(os.path.join(SHARED_TEX, t), os.path.join(U, 'Textures', 'Shared'))   # Unity-side maps
for f in glob.glob(P_('reports', '*')) if not NO_UNITY else []:
    if not os.path.basename(f).endswith('_FREEZE_CANDIDATE.md'): shutil.copy2(f, os.path.join(U, 'Reports'))
geo = json.load(open(P_('reports', f'{PFX}_geometry.json'))); L = geo['lods']; wr = geo['wheel_refs']; com = geo['center_of_mass']
u = lambda p: [round(-p[0], 4), round(p[2], 4), round(-p[1], 4)]
md = f"""# {VEH} — Unity import notes

**Unity owns** controller, physics, WheelColliders, prefab, LOD Group, shaders, lighting, audio and profiling. Blender delivers geometry, pivots, reference empties, colliders, materials, textures and FBX. **Nothing here was opened in Unity; no frame-rate claims.**

## Files
- `FBX/{BASE}_complete_unity.fbx` (LOD0-3 + colliders + references, {man['files'][f'{BASE}_complete_unity.fbx']['count']} objects); `FBX/{BASE}_LOD0_unity_test.fbx` (LOD0 only).
- `Textures/` — vehicle bakes: `{PP}_Body_Normal` (2048, tangent / MikkTSpace, LOD0), `{PP}_Body_Normal_LOD1` (1024), `{PP}_Body_AO_Grime` (1024; R = ambient occlusion, G = road-grime mask).
- `Textures/Shared/` — fleet library (reused by every traffic vehicle): `TS_Atlas_*` (2048 8x8 material atlas), `TS_Tire_*`, `TS_PaintFlake_Normal`, `TS_Lights_*` (light mask).

## Importer
Scale 1, Convert Units ON, **Bake Axis Conversion OFF** (axes baked; Car_Root identity). Normals: Import. Tangents: Calculate (MikkTSpace — required for the baked body normal map). Animation None. Generate Colliders OFF.
Blender (x, y, z) -> Unity (-x, z, -y): forward -Y -> +Z, up +Z -> +Y, vehicle left +X -> -X.

## Hierarchy
```
Car_Root
 ├─ LOD0_Root … LOD3_Root     Body (paint shell incl. mirrors + antenna), Glass, Trim (atlas), Lights (emitters + lenses), Interior
 │   ├─ SteerPivot_FL / FR     yaw on local Y (±25°) → Wheel_FL / FR (rim + tire + disc, roll on local X), Caliper_FL / FR (steers, does not roll)
 │   ├─ Wheel_RL / RR          roll on local X;  Caliper_RL / RR static
 ├─ Collision                  Collision_Front / Body / Cabin / Rear (convex MeshColliders, renderers off)
 ├─ WheelColliderRef_FL / FR / RL / RR   (custom props radius_m, width_m)
 └─ CenterOfMass
```
Suggested LOD Group screen heights: 50 / 22 / 8 / 1.5 %.

## LODs
| LOD | triangles | ratio | materials | draw calls |
|---|---|---|---|---|
""" + '\n'.join(f"| {k} | {v['triangles']:,} | {v['ratio']:.0%} | {v['materials']} | {v['draw_calls']} |" for k, v in L.items()) + f"""

## Wheels / centre of mass
| Ref | Blender | Unity | radius m | width m |
|---|---|---|---|---|
""" + '\n'.join(f"| {c} | {tuple(wr[c])} | {tuple(u(wr[c]))} | 0.316 | 0.205 |" for c in ('FL', 'FR', 'RL', 'RR')) + f"""

`CenterOfMass` Blender {tuple(com)} → Unity {tuple(u(com))} (front-engine FWD bias). `rigidbody.centerOfMass = CenterOfMass.localPosition`.

## Materials ({L['LOD0']['materials']} at LOD0; paint is one instance per colour)
| Material | Unity setup |
|---|---|
| `{PP}_Paint` | Lit clear-coat (or URP Complex Lit): BaseColor = paint colour × AO (R of `{PP}_Body_AO_Grime`), lerp to grime colour (0.11, 0.10, 0.085) by G × 0.55; Normal = `{PP}_Body_Normal`; detail normal `TS_PaintFlake_Normal` tiling 60, strength 0.15; Metallic 0.55, Smoothness 0.64; Clear coat 1.0, coat smoothness 0.955 (grime lowers it). |
| `{PP}_Paint_LOD1` | same, Normal = `{PP}_Body_Normal_LOD1` |
| `{PP}_Paint_Far` | same without normal / AO maps (LOD2-3) |
| `TS_Atlas` | Lit opaque. BaseMap `TS_Atlas_BaseColor`; Metallic/Smoothness `TS_Atlas_MetallicSmoothness` (R metal, A smoothness); Normal `TS_Atlas_Normal`. Bilinear, mip-maps on, **no texture wrap across cells** (UVs are inset 6 %). |
| `TS_Tire` | Lit opaque. `TS_Tire_BaseColor` + `TS_Tire_Normal` (tread blocks, sipes, sidewall rings, fictional lettering band); smoothness 1 - `TS_Tire_Roughness`. UV U wraps around the tire (repeat). |
| `TS_Glass` | Lit transparent, base (0.50, 0.58, 0.56) **alpha 0.35**, smoothness 1.0 — tinted, see-through. |
""" + ('\n'.join(x for x in (f"| `{PP}_Glass` | **Instance of `TS_Glass`** (used instead of it on this vehicle): Lit transparent, base (0.78, 0.84, 0.82) **alpha 0.22**, smoothness 1.0 — light green automotive tint (~75 % visible transmission), cabin readable. |" if f'{PP}_Glass' in man['materials'] else '',
       f"| `{PP}_Interior` | **Instance of `TS_Atlas`** (same textures and UVs) on the Interior meshes: normal scale **0.12** (seat weave reads as fabric at cabin scale, not crumpled). |" if f'{PP}_Interior' in man['materials'] else '') if x) + '\n' if any(m in man['materials'] for m in (f'{PP}_Glass', f'{PP}_Interior')) else '') + f"""| `TS_Lens` / `TS_LensRed` | Lit transparent: clear alpha 0.10; red (0.42, 0, 0.006) alpha 0.55 — reads red in daylight. |
| `TS_Lights` | **One emissive material for all channels.** BaseMap `TS_Lights_BaseColor` (off look), Emission `TS_Lights_Emission`; channel = `TS_Lights_ChannelID` R × 15 → 0 DRL, 1 Headlamp, 2 Tail, 3 Brake, 4 Indicator_L, 5 Indicator_R, 6 Reverse, 7 Marker. Drive a per-channel intensity array (MaterialPropertyBlock / small shader): one draw call, independent channels. Suggested intensities: DRL 12, Headlamp 4, Tail 5, Brake 8 (on), Indicators 1.2 (blink), Reverse 0.5. |

## Paint variants (material instances, no extra meshes)
| Variant | Linear base RGB | Metallic |
|---|---|---|
| Arctic white (solid) | (0.80, 0.80, 0.78) | 0.0 |
| Silver metallic | (0.55, 0.57, 0.59) | 0.55 |
| Graphite metallic | (0.090, 0.095, 0.100) | 0.55 |
| Black (solid) | (0.012, 0.012, 0.013) | 0.0 |
| Deep red metallic | (0.30, 0.012, 0.015) | 0.55 |
| Steel blue metallic (review) | (0.060, 0.115, 0.220) | 0.55 |
"""
if not NO_UNITY: open(os.path.join(U, 'README', f'{BASE}_UNITY_IMPORT_NOTES.md'), 'w').write(md)
# ---- integrity
sh = lambda p: hashlib.sha1(open(p, 'rb').read()).hexdigest()
base = json.load(open(WS + '/vehicles/A_Discovery/reports/VA_workspace_baseline.json'))['files']
changed = [k for k, v in base.items() if not os.path.exists(os.path.join(WS, k)) or sh(os.path.join(WS, k)) != v['sha1']]
now = set()
for d, dirs, fs in os.walk(WS):
    rel = os.path.relpath(d, WS)
    if rel == 'vehicles' or rel.startswith('vehicles' + os.sep): dirs[:] = []; continue
    now |= {os.path.relpath(os.path.join(d, f), WS) for f in fs if f != '.DS_Store'}
added = sorted(now - set(base)); FR = {}
for man_ in sorted(glob.glob(os.path.join(WS, 'vehicles', '*', 'reports', '*_FINAL_FREEZE.md')) + [m for m in glob.glob(os.path.join(WS, 'vehicles', '*', '*', 'reports', '*_FINAL_FREEZE.md')) if 'UnityTransfer' not in m]):
    r = os.path.dirname(os.path.dirname(man_)); rows = [l.split('`') for l in open(man_) if l.startswith('| `')]
    FR[os.path.basename(r)] = (len(rows), [x[1] for x in rows if not os.path.exists(os.path.join(r, x[1])) or sh(os.path.join(r, x[1])) != x[3]])
pulse_ok = sh(os.path.join(WS, 'vehicles/F_PulseEV/blend/pulseev_01_blockout.blend')) == '18af7277976ab32e89c103f81c4e9c941c367f4d'
CAND = {}                                                                                             # earlier traffic revisions (H1, r2 ...) stay byte-identical to their candidate manifests
for man_ in sorted(glob.glob(os.path.join(FLEET, '*', 'reports', '*_FREEZE_CANDIDATE.md'))):
    if os.path.dirname(os.path.dirname(man_)) == ROOT: continue
    rows = [l.split('`') for l in open(man_) if l.startswith('| `')]; CAND[os.path.basename(os.path.dirname(os.path.dirname(man_)))] = (len(rows), [x[1] for x in rows if not os.path.exists(os.path.join(FLEET, x[1])) or sh(os.path.join(FLEET, x[1])) != x[3]])
ok = not changed and not added and not any(b for _, b in FR.values()) and pulse_ok and not any(b for _, b in CAND.values())
open(P_('reports', f'{PFX}_integrity_check.md'), 'w').write('\n'.join([f'# {VEH} — protected-file integrity check', '', f"Re-hashed {time.strftime('%Y-%m-%d %H:%M:%S')}.", '',
    f'- Phase A baseline ({len(base)} files outside `vehicles/`: frozen P0–P3, Hypercar, racing_car sources): changed **{len(changed)}**, added **{len(added)}**.'] +
    [f'- Frozen {k} ({n} hashed files): changed **{len(b)}**.' for k, (n, b) in FR.items()] +
    [f'- Earlier traffic revision {k} ({n} files in its candidate manifest): changed / missing **{len(b)}**.' for k, (n, b) in CAND.items()] +
    [f"- Postponed Pulse EV blockout `pulseev_01_blockout.blend`: {'unchanged' if pulse_ok else '**CHANGED**'}.", '', f"Result: **{'PASS' if ok else 'FAIL'}**"]) + '\n')
(None if NO_UNITY else shutil.copy2(P_('reports', f'{PFX}_integrity_check.md'), os.path.join(U, 'Reports'))); print('INTEGRITY', 'PASS' if ok else 'FAIL')
files = sorted(glob.glob(P_('blend', '*.blend')) + glob.glob(P_('exports', '*.fbx')) + glob.glob(P_('textures', '*.png')) + [os.path.join(SHARED_TEX, t) for t in sorted(os.listdir(SHARED_TEX))])
val = open(P_('reports', f'{PFX}_validation.txt')).read().strip().splitlines()[-1]
open(P_('reports', f'{PFX}_FREEZE_CANDIDATE.md'), 'w').write('\n'.join([f'# {VEH} — candidate manifest (awaiting visual + technical approval)', '', f"Date {time.strftime('%Y-%m-%d')}. Validation: **{val}**. Integrity: **{'PASS' if ok else 'FAIL'}**.", '',
    '| File | SHA-1 |', '|---|---|'] + [f'| `{os.path.relpath(f, FLEET)}` | `{sh(f)}` |' for f in files]) + '\n')
print('PACKAGED', len(files))
