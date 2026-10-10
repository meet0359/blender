# Vortex R revision r1: LOD1 hard-surface normal repair (NORMALS ONLY). Blender -b --factory-startup --python vx_r1_normals.py
# Frozen Vortex R decimated Trim / Lights / Interior / SteeringWheel to LOD1 and then transferred LOD0 custom normals onto them; on the reduced
# geometry those normals tear (Trim_LOD1 23 % torn loops: silvery blotchy carbon wing, smeared rocker blade + diffuser fins). r1 replaces them with
# locally computed normals: custom normals cleared, smooth shading, sharp edges from the SAME angle each part uses at LOD0 (trim / lights 35 deg,
# interior / steering 40 deg) so the intended smoothing boundaries are kept. Geometry, UVs, materials, rig, colliders, names are untouched.
# Opens the frozen vortexr_08 (never saved back) and writes D_VortexR_r1/blend/vortexr_r1_08_colliders_hierarchy.blend.
import bpy, os, math, json
FROZEN = '/Users/meetshah/Documents/blender/vehicles/D_VortexR'; R1 = '/Users/meetshah/Documents/blender/vehicles/D_VortexR_r1'
out = os.path.join(R1, 'blend', 'vortexr_r1_08_colliders_hierarchy.blend'); assert not os.path.exists(out), out
bpy.ops.wm.open_mainfile(filepath=FROZEN + '/blend/vortexr_08_colliders_hierarchy.blend'); O = bpy.data.objects
ANG = {'Trim_LOD1': 35, 'Lights_LOD1': 35, 'Interior_LOD1': 40, 'SteeringWheel_LOD1': 40}
def torn(o):
    cn = o.data.corner_normals; b = t = 0
    for p in o.data.polygons:
        if p.area < 2e-6: continue
        for li in p.loop_indices: t += 1; b += cn[li].vector.angle(p.normal, 0) > math.radians(50)
    return round(100 * b / max(t, 1), 3)
LOG = {}
for n, ang in ANG.items():
    o = O[n]; before = torn(o); tris_ = sum(len(p.vertices) - 2 for p in o.data.polygons)
    with bpy.context.temp_override(object=o, active_object=o): bpy.ops.mesh.customdata_custom_splitnormals_clear()
    o.data.shade_smooth(); o.data.set_sharp_from_angle(angle=math.radians(ang))
    LOG[n] = dict(torn_pct_before=before, torn_pct_after=torn(o), sharp_angle_deg=ang, tris=tris_, tris_after=sum(len(p.vertices) - 2 for p in o.data.polygons))
    print('R1', n, LOG[n], flush=True)
for im in bpy.data.images:                                                        # textures resolve to the r1 copies (byte-identical)
    if im.filepath: im.filepath = os.path.join(R1, 'textures', os.path.basename(bpy.path.abspath(im.filepath)))
bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_as_mainfile(filepath=out, copy=True, relative_remap=True); print('SAVED', out, flush=True)
json.dump({'revision': 'r1', 'base': 'D_VortexR/blend/vortexr_08_colliders_hierarchy.blend (frozen, read only)', 'change': 'normals only on LOD1 hard-surface parts', 'parts': LOG},
          open(os.path.join(R1, 'reports', 'VX_r1_normals_log.json'), 'w'), indent=1)
