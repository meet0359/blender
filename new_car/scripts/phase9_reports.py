# Phase 9 reports (plain python3): combines fbx_validation_*.txt and writes the Unity notes, material mapping and manifest.
import json, os, hashlib, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(ROOT, "reports", *p)
J = lambda n: json.load(open(R(n)))
sha = lambda p: hashlib.sha1(open(p, "rb").read()).hexdigest()

exp, vc, v0 = J("fbx_export_settings.json"), J("fbx_validation_complete.json"), J("fbx_validation_lod0.json")
wref, cst, piv = J("wheel_reference_points.json"), J("collider_stats.json"), J("pivot_validation.json")
txt = {t: open(R(f"fbx_validation_{t}.txt")).read() for t in ("lod0", "complete")}
summ = {t: [l for l in txt[t].splitlines() if l.startswith("SUMMARY")][0] for t in txt}
errs = sum(txt[t].count("[ERROR]") for t in txt); warns = sum(txt[t].count("[WARNING]") for t in txt)
assert errs == 0, "validation has errors - fix before writing reports"
U = lambda p: [-p[0], p[2], -p[1]]           # Blender (x, y, z) -> Unity (-x, z, -y) after FBX import
r4 = lambda v: [round(c, 4) + 0.0 for c in v]
dup = exp["duplicate_triangles_removed"]

# ---------------------------------------------------------------- fbx_export_validation.txt
hdr = f"""PHASE 9 FBX EXPORT VALIDATION   ({datetime.date.today()})
Source checkpoint: hypercar_07_colliders_hierarchy.blend (unchanged, sha1 {sha(os.path.join(ROOT, 'hypercar_07_colliders_hierarchy.blend'))})
Export checkpoint: hypercar_08_unity_export.blend
Method: each FBX re-imported into a CLEAN factory scene (pass 1, Blender-frame round trip) and again with NO axis
conversion (pass 2 = the raw coordinates Unity reads). Mesh normals compared to the source meshes.

RESULT: {errs} ERROR, {warns} WARNING
  {summ['lod0']}
  {summ['complete']}

Preset history (the re-import test decided):
  1st try  axis -Z fwd / Y up + 'Apply Transform' (bake_space_transform=True): 20 ERRORS. Child meshes kept a
           residual Lcl Rotation 90 deg X on already-converted geometry (double rotation: H 2.27 m, wheels ~2 m off).
  final    axis -Z fwd / Y up, Apply Transform OFF, axis conversion baked explicitly in the export session
           (objects + mesh data, residual 1.8e-7) -> Car_Root identity in FBX, geometry/pivots in Unity axes.
Export-session-only changes (never saved to any .blend):
  - 5+-gons triangulated with bmesh (exact n-2 triangles; Blender's Triangulate modifier drops duplicates)
  - {sum(dup.values())} coincident duplicate triangles removed (same 3 vertices as an existing face; importers collapse
    them, Unity would z-fight): {json.dumps(dup)}
  - Phase 8 QA viewport materials stripped from the 6 colliders (physics only)
Shader differences (documented, not errors): Blender Principled -> Unity Lit is approximate; see
unity_material_mapping.md (smoothness = 1 - roughness, AO + clear-coat must be hooked up by hand).

"""
open(R("fbx_export_validation.txt"), "w").write(hdr + "\n".join(txt[t] for t in ("lod0", "complete")))

# ---------------------------------------------------------------- material mapping
MAP = [  # (category, FBX material(s), Unity setup, Blender values -> Unity)
 ("Car Paint", "LODMAT_Body_Paint", "Lit Opaque; BaseMap BODY_BaseColor; Metallic+Smoothness from BODY_Metallic / 1-BODY_Roughness (pack: R=metal, A=1-rough); Normal BODY_Normal; Occlusion BODY_AO. HDRP: enable Clear Coat 0.58 / URP: use a clear-coat capable car-paint shader",
  "RacingRed base (0.80, 0.010, 0.024) linear, roughness 0.20 -> smoothness ~0.80, metallic 0.85, coat 0.58. Alt paints: ElectricBlue r0.20 m0.85, PearlWhite r0.25 (0.75) m0.30, SatinBlack r0.45 (0.55) m0.45"),
 ("Carbon (exterior)", "MAT_CarbonExterior", "Lit Opaque; BaseMap carbon_twill_BaseColor (tiling as authored); Normal carbon_twill_Normal; clear coat 1.0",
  "roughness 0.32 -> smoothness 0.68, metallic 0"),
 ("Metal / trim", "LODMAT_Trim, LODMAT_Wheels", "Lit Opaque; TRIM_* / WHEELS_* atlas (BaseColor, Metallic, Roughness->Smoothness, Normal, AO)",
  "machined 0.16 -> 0.84 (m1.0), graphite 0.30 -> 0.70 (m1.0), dark barrel 0.50 -> 0.50 (m0.8), exhaust 0.24 -> 0.76 (m1.0), black trim 0.45 -> 0.55"),
 ("Tire", "LODMAT_Tire", "Lit Opaque; TIRES_* atlas; sidewall detail already baked into TIRES_Normal",
  "base (0.032, 0.032, 0.034), roughness ~0.85 (baked map) -> smoothness ~0.15, metallic 0"),
 ("Brake Rotor", "LODMAT_Brakes", "Lit Opaque; BRAKES_* atlas", "roughness 0.45 -> 0.55, metallic 0.35"),
 ("Caliper", "MAT_BrakeCaliper", "Lit Opaque, solid colour (kept separate for colour option)",
  "base (0.80, 0.50, 0.015), roughness 0.32 -> 0.68, metallic 0, coat 0.6"),
 ("Glass", "LODMAT_Glass", "Lit Transparent (Alpha ~0.15-0.25, Preserve specular), double-sided off; GLASS_* atlas tint",
  "Blender uses transmission 1.0 / IOR 1.46, roughness 0.02 -> 0.98. Unity has no refraction in URP: use alpha"),
 ("Headlight Lens", "MAT_HeadlightLens", "Lit Transparent, Alpha ~0.1", "base 0.97, roughness 0.0 -> 1.0, transmission 1.0 / IOR 1.49"),
 ("Taillight Lens", "MAT_TaillightLens", "Lit Transparent, Alpha ~0.35, red tint", "base (0.42, 0.10, 0.10), roughness 0.03 -> 0.97, transmission 1.0"),
 ("Emission (light channels)", "MAT_LED_White, MAT_ProjectorLens, MAT_LED_Red, MAT_LED_Brake, MAT_LED_Amber, MAT_LED_Reverse, MAT_AmbientLight",
  "Lit Opaque + Emission ON; ONE material per channel so scripts can switch headlight/tail/brake/indicator/reverse independently (set _EmissionColor intensity at runtime)",
  "White em 6.0 (1,0.96,0.9), Red tail 5.0, Brake 1.2 (raise to ~8 when braking), Amber 0.8 (indicator), Reverse 0.25 (raise when reversing), Ambient 1.2; ProjectorLens r0.02 coat 1.0, no emission. Blender strength is not Unity nits/EV: re-tune with bloom"),
 ("Leather", "LODMAT_Interior (baked)", "Lit Opaque; INTERIOR_* atlas (leather, alcantara, plastic, metal, seat accent baked together); stitch/perforation detail baked into INTERIOR_Normal",
  "leather (0.020, 0.019, 0.019), roughness 0.42 -> 0.58"),
 ("Alcantara", "LODMAT_Interior (baked)", "same INTERIOR_* atlas", "(0.040, 0.040, 0.043), roughness 0.95 -> 0.05"),
 ("Interior Carbon", "MAT_InteriorCarbon", "Lit Opaque; carbon_twill_* textures; coat 0.8", "roughness 0.32 -> 0.68"),
 ("Display", "MAT_Display, MAT_DisplayGraphics, MAT_DisplayGraphics_Red", "Lit Opaque + Emission (or Unlit); swap BaseMap for a RenderTexture to drive live gauges",
  "screen base (0.006, 0.008, 0.012) r0.25 em 0.6; graphics em 1.4 (blue-white) / 1.6 (red)"),
 ("Interior mirror", "MAT_InteriorMirror", "Lit Opaque, metallic 1, smoothness 0.98 (or planar reflection)", "roughness 0.02 -> 0.98"),
]
md = ["# Unity material mapping (Phase 9)", "",
      "Smoothness rule: **Unity Smoothness ~= 1 - Blender Roughness** (paint 0.20 -> ~0.80). Unity Lit reads smoothness from "
      "the Metallic map's alpha: pack `R = Metallic`, `A = 1 - Roughness` (invert the *_Roughness.png). Normal maps are "
      "**OpenGL (+Y)**: set Texture Type = Normal map, no green flip needed in Unity. BaseColor = sRGB; Metallic, Roughness, "
      "Normal, AO = linear (sRGB off). AO (*_AO.png) is not referenced by the FBX: assign it to Occlusion by hand.", "",
      "| Category | FBX material | Unity setup | Blender values -> Unity |", "|---|---|---|---|"]
md += [f"| {a} | `{b}` | {c} | {d} |" for a, b, c, d in MAP]
md += ["", f"FBX material slots per LOD (LOD0): {len(vc['materials_LOD0'])} - " + ", ".join(f"`{m}`" for m in vc["materials_LOD0"]), ""]
open(R("unity_material_mapping.md"), "w").write("\n".join(md))

# ---------------------------------------------------------------- unity_import_notes.md
d0 = vc["dims_LOD0"]; ur = vc["unity_raw"]; com_u = ur["CenterOfMass_unity(x negated by Unity's FBX importer)"]
wr = "\n".join(f"| {k} | {'LEFT' if wref[k]['world_position'][0] > 0 else 'RIGHT'} | {tuple(r4(wref[k]['world_position']))} | "
               f"{tuple(r4(U(wref[k]['world_position'])))} | {wref[k]['radius_m']} | {wref[k]['width_m']} |" for k in ("FL", "FR", "RL", "RR"))
lods = "\n".join(f"| LOD{i} | {vc[f'tris_LOD{i}']:,} | {vc[f'dims_LOD{i}']['L']} x {vc[f'dims_LOD{i}']['W']} x {vc[f'dims_LOD{i}']['H']} | "
                 f"{len(vc[f'materials_LOD{i}'])} |" for i in range(4))
cols = "\n".join(f"| {n} | {s['triangles']} | {s['vertices']} |" for n, s in cst.items() if n.startswith("Collision_"))
tex = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "textures", "hypercar", "*", "*.png")))
tex_md = "\n".join(f"- `{t}`" for t in tex)
notes = f"""# Unity import notes: hypercar

Files: `exports/hypercar_complete_unity.fbx` (LOD0-3 + colliders + refs, 308 objects) and
`exports/hypercar_LOD0_unity_test.fbx` (LOD0 only, 102 objects). Textures are external (not embedded), referenced
relatively as `../textures/hypercar/<group>/*.png`. Copy `textures/hypercar/` into the Unity project with the FBX.

## Importer settings (Model tab)
- Scale Factor **1**, Convert Units **ON** (file unit = 1 m, UnitScaleFactor 100 cm). Result: 1 unit = 1 m, root scale 1.
- Bake Axis Conversion **OFF** (not needed: axes are already baked; Car_Root rotation is identity in the file).
- Import Normals: **Import**; Tangents: **Import** (MikkTSpace, exported); Smoothing source: from file.
- Materials: Location "Use External Materials (Legacy)" or extract, then set them up per `unity_material_mapping.md`.
- Animation: none in the file (Animation Type None). No cameras or lights.

## Coordinate conversion (verified by re-import)
| | Blender | FBX file | Unity |
|---|---|---|---|
| forward | -Y | +Z | **+Z** |
| up | +Z | +Y | **+Y** |
| vehicle left | +X | +X | **-X** (Unity's importer negates FBX X) |
| point (x, y, z) | (x, y, z) | (x, z, -y) | (-x, z, -y) |

The car faces +Z, upright, and the LHD driver seat sits on the vehicle's left (Unity -X). Car_Root: position 0, rotation 0, scale 1.
Unity view checks: nose z {ur['body_z_range(forward)'][1]}, tail z {ur['body_z_range(forward)'][0]}, roof y {ur['body_y_max(up)']}.

## Dimensions (LOD0 re-import, mirrors excluded)
Length {d0['L']} m, width {d0['W']} m, height {d0['H']} m (all within 0.05 mm of Phase 7).
Wheelbase {wref['_wheelbase_m']} m, track front {wref['_track_m']['front']} m / rear {wref['_track_m']['rear']} m.

## Wheels (WheelColliderRef_* empties = wheel centres)
| Ref | Side | Blender | Unity local to Car_Root | radius m | width m |
|---|---|---|---|---|---|
{wr}

Use the refs to position WheelColliders (radius as above; suspension distance tuned in Unity).
Visual wheels: `Wheel_<k>_LODn` rotates on **local X** (axle; tire + rotor are children, calipers do not roll).
Front steering: `SteerPivot_FL/FR_LODn` yaws on **local Y** (= car up) about the wheel centre, carrying wheel and caliper.
Because Unity mirrors X on import, drive the visual wheels from `WheelCollider.GetWorldPose` rather than accumulating
local Euler angles; if spinning by hand, verify the sign once per side.

## Center of mass
`CenterOfMass` empty: Blender (0, 0.12, 0.35) -> Unity local **{tuple(c + 0.0 for c in com_u)}**
(0.35 m high, 0.12 m behind mid-wheelbase). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition` in a script.

## LODs (one FBX, four roots)
| LOD | triangles | L x W x H (m) | material slots |
|---|---|---|---|
{lods}

Triangles are Phase 7 counts minus {sum(dup.values())} coincident duplicate triangles removed at export ({json.dumps(dup)}).
Set up a LOD Group on Car_Root: LOD0_Root ... LOD3_Root renderers (suggested 60 / 30 / 12 / 3 % screen height).
Colliders, refs and CenterOfMass are outside the LOD roots and shared by all LODs.

## Material groups
{len(vc['materials_LOD0'])} materials per LOD: 8 baked atlases (`LODMAT_Body_Paint`, `Brakes`, `Glass`, `Interior`, `Lights`, `Tire`,
`Trim`, `Wheels`) + carbon (exterior/interior) + caliper + lenses + displays + interior mirror + **6 light channels kept
separate**: `MAT_LED_White`, `MAT_ProjectorLens`, `MAT_LED_Red`, `MAT_LED_Brake`, `MAT_LED_Amber`, `MAT_LED_Reverse` (+ `MAT_AmbientLight`).
Full mapping: `reports/unity_material_mapping.md`.

## Textures ({len(tex)} files, PNG)
Atlases: BODY 4096, INTERIOR 4096, WHEELS / TIRES / LIGHTS 2048, BRAKES / GLASS / TRIM 1024; each has BaseColor, Metallic,
Roughness, Normal, AO. **Normal maps are OpenGL (+Y up green)**, which is Unity's convention: import as Normal map, no flip.
Roughness must be inverted to smoothness (see mapping). AO is not linked by the FBX; assign it manually.
{tex_md}

## Colliders (`Collision` empty, 6 convex meshes, {cst['_total_triangles']} triangles total)
| Collider | tris | verts |
|---|---|---|
{cols}

All convex (<= 255 triangles each), closed, outward normals: add MeshCollider with **Convex ON** to each, disable their
MeshRenderers (they carry no material and no UVs), and put them on a vehicle physics layer.

## Animated / pivot objects (no animation data exported, pivots only)
| Object | Pivot | Axis (Unity local) | Range |
|---|---|---|---|
| `Wheel_FL/FR/RL/RR_LOD0-3` | wheel centre | X (roll) | continuous |
| `SteerPivot_FL/FR_LOD0-3` | wheel centre | Y (yaw) | -25 .. +25 deg |
| `SteeringWheel_LOD0-2` | column hub, Blender {tuple(piv['steering_wheel']['LOD0']['origin'])} | Y (shaft) | ~ +/-270 deg (ratio to taste) |
| `Paddle_L/R_LOD0-1` | paddle hinge | as authored | small pull |
| `Door_L/R_LOD0-1` (+ panel, window, handle) | hinge, Blender (+/-0.9, -0.95, 0.8) | X | 0 .. 15-20 deg (validated 18) |
| `ActiveSpoiler_LOD0-3` | hinge, Blender (0, 1.884, 0.8735) | X | 3 deg rest .. 18 deg deployed |

## Suggested Unity hierarchy (not built: Unity work starts after approval)
```
Hypercar (prefab root) = Car_Root   [Rigidbody, LOD Group, vehicle controller]
 |- LOD0_Root .. LOD3_Root          [render meshes; animated pivots inside]
 |- Collision                       [6 x MeshCollider convex, renderers off]
 |- WheelColliders (new)            [4 x WheelCollider placed at WheelColliderRef_*]
 |- WheelColliderRef_FL/FR/RL/RR    [position references, can be removed after setup]
 '- CenterOfMass                    [read by script -> rigidbody.centerOfMass]
```
"""
open(R("unity_import_notes.md"), "w").write(notes)

# ---------------------------------------------------------------- final_export_manifest.json
files = {}
for p in ["hypercar_07_colliders_hierarchy.blend", "hypercar_08_unity_export.blend",
          "exports/hypercar_LOD0_unity_test.fbx", "exports/hypercar_complete_unity.fbx"] + tex:
    fp = os.path.join(ROOT, p); files[p] = {"bytes": os.path.getsize(fp), "sha1": sha(fp)}
for f, e in exp["files"].items():
    assert files["exports/" + f]["sha1"] == e["sha1"], f
man = {"asset": "hypercar", "phase": 9, "date": str(datetime.date.today()), "source_checkpoint": "hypercar_07_colliders_hierarchy.blend",
       "export_checkpoint": "hypercar_08_unity_export.blend", "fbx_settings": exp["settings"],
       "axis_bake": "explicit in export session: world' = world @ G^-1, mesh' = G v, G = Rot(-90 deg, X)",
       "export_session_changes": {"ngon_triangulated_meshes": len(exp["export_time_ngon_triangulated_meshes"]),
                                  "duplicate_triangles_removed": dup, "collider_qa_materials_stripped": 6},
       "fbx": {f: {"objects": e["objects"], "validation": summ['lod0' if 'LOD0' in f else 'complete']} for f, e in exp["files"].items()},
       "unity": {"forward": "+Z", "up": "+Y", "vehicle_left": "-X", "units": "m", "root_rotation": [0, 0, 0], "root_scale": [1, 1, 1],
                 "center_of_mass": ur["CenterOfMass_unity(x negated by Unity's FBX importer)"],
                 "wheels": {k: {"position": r4(U(wref[k]["world_position"])), "radius": wref[k]["radius_m"], "width": wref[k]["width_m"]} for k in ("FL", "FR", "RL", "RR")},
                 "wheelbase": wref["_wheelbase_m"], "track": wref["_track_m"]},
       "lods": {f"LOD{i}": {"triangles": vc[f"tris_LOD{i}"], "dims_m": vc[f"dims_LOD{i}"], "materials": len(vc[f"materials_LOD{i}"])} for i in range(4)},
       "colliders": {n: s["triangles"] for n, s in cst.items() if n.startswith("Collision_")}, "collider_triangles": cst["_total_triangles"],
       "validation": {"errors": errs, "warnings": warns},
       "reports": ["reports/fbx_export_validation.txt", "reports/unity_import_notes.md", "reports/unity_material_mapping.md",
                   "reports/fbx_validation_lod0.txt", "reports/fbx_validation_complete.txt", "reports/fbx_export_settings.json"],
       "files": files}
json.dump(man, open(R("final_export_manifest.json"), "w"), indent=1)
print("REPORTS OK", errs, "errors", warns, "warnings,", len(tex), "textures")
