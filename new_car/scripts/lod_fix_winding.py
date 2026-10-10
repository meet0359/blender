# One-off on hypercar_06: same non-manifold repair as lod_build.clean() (drop sliver faces on 3+-face edges).
import bpy, bmesh
fixed = {}
for o in bpy.data.objects:
    if o.type != 'MESH' or "lod" not in o: continue
    bm = bmesh.new(); bm.from_mesh(o.data); n = 0
    for _ in range(8):
        bad = [e for e in bm.edges if len(e.link_faces) > 2]
        if not bad: break
        fs = list({min(e.link_faces, key=lambda f: f.calc_area()) for e in bad}); n += len(fs)
        bmesh.ops.delete(bm, geom=fs, context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    if n: bm.to_mesh(o.data); fixed[o.name] = n
    bm.free()
print("FIXED", fixed); bpy.ops.wm.save_mainfile()
