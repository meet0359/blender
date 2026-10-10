# Phase 8 QA previews: ghosted LOD0 + collider overlay, and a pivot/hierarchy reference. Never saves the .blend.
import bpy, bmesh, os, math
from mathutils import Vector, Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, "previews")
sc = bpy.context.scene
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for d in prefs.devices: d.use = True
sc.cycles.device = "GPU"; sc.render.use_persistent_data = False; sc.cycles.samples = 48
sc.render.resolution_x, sc.render.resolution_y = 1600, 900

def mat(name, rgb, alpha=1.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Alpha"].default_value = alpha
    b.inputs["Roughness"].default_value = 0.6
    if emit:
        b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = emit
    return m
ghost = mat("QA_Ghost", (0.75, 0.75, 0.78), alpha=0.16)
for o in bpy.data.collections["Car_LOD0"].all_objects:      # ghost LOD0 (in memory only)
    if o.type == 'MESH':
        for i in range(len(o.data.materials)): o.data.materials[i] = ghost
for o in bpy.data.collections["COLLIDERS"].objects:
    o.hide_render = False

def render(cam, name):
    sc.camera = bpy.data.objects[cam]; sc.render.filepath = os.path.join(PRE, name)
    bpy.ops.render.render(write_still=True); print("RENDERED", sc.render.filepath, flush=True)
import sys
if "pivot_only" not in sys.argv:
    for cam, name in (("Cam_front_3q", "collider_front_3q.png"), ("Cam_side", "collider_side.png"),
                      ("Cam_top", "collider_top.png"), ("Cam_rear_3q", "collider_rear_3q.png")):
        render(cam, name)

# ---- pivot reference: colliders off, fainter ghost, bright emissive markers
for o in bpy.data.collections["COLLIDERS"].objects: o.hide_render = True
ghost.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.07
for n in ("Cam_front_3q", "Cam_side", "Cam_top", "Cam_rear_3q"):
    pass
MK = bpy.data.collections.new("QA_Markers"); sc.collection.children.link(MK)
def world(o):
    I = Matrix.Identity(4); return (world(o.parent) @ o.matrix_parent_inverse if o.parent else I) @ o.matrix_basis
def marker(name, m, build):
    bm = bmesh.new(); build(bm); me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    me.materials.append(m); o = bpy.data.objects.new(name, me); MK.objects.link(o); return o
def rod(bm, a, b, r):
    a, b = Vector(a), Vector(b); d = b - a
    res = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=r, depth=d.length)
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_matrix().to_4x4()
    bmesh.ops.transform(bm, matrix=Matrix.Translation((a + b) / 2) @ rot, verts=res["verts"])
def ball(bm, c, r):
    res = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=r)
    bmesh.ops.translate(bm, vec=Vector(c), verts=res["verts"])
ORANGE, YELLOW, MAG, CYAN, GREEN, RED, BLUE, WHITE = ((1, .35, 0), (1, .9, .1), (1, .1, .8), (.1, .9, 1),
                                                      (.2, 1, .3), (1, .1, .1), (.2, .4, 1), (1, 1, 1))
for k in ("FL", "FR", "RL", "RR"):
    c = world(bpy.data.objects[f"WheelColliderRef_{k}"]).translation
    marker(f"mk_ref_{k}", mat("m_ref", ORANGE, emit=18), lambda bm, c=c: ball(bm, c, 0.05))
    marker(f"mk_axle_{k}", mat("m_axle", YELLOW, emit=15), lambda bm, c=c: rod(bm, c - Vector((0.32, 0, 0)), c + Vector((0.32, 0, 0)), 0.012))
    if k[0] == "F":
        marker(f"mk_steer_{k}", mat("m_steer", GREEN, emit=15), lambda bm, c=c: rod(bm, c - Vector((0, 0, 0.45)), c + Vector((0, 0, 0.45)), 0.009))
com = world(bpy.data.objects["CenterOfMass"]).translation
marker("mk_com", mat("m_com", MAG, emit=18), lambda bm: (ball(bm, com, 0.07), rod(bm, com, (com.x, com.y, 0.0), 0.008)))
for v, colr in (((0.9, 0, 0), RED), ((0, -0.9, 0), GREEN), ((0, 0, 0.9), BLUE)):   # Car_Root: right(+X) red, forward(-Y) green, up(+Z) blue
    marker("mk_root", mat("m_root", colr, emit=18), lambda bm, v=v: (rod(bm, (0, 0, 0.002), Vector(v) + Vector((0, 0, 0.002)), 0.015), ball(bm, v, 0.03)))
for s in ("L", "R"):
    h = world(bpy.data.objects[f"Door_{s}_LOD0"]).translation
    marker(f"mk_door_{s}", mat("m_door", CYAN, emit=18), lambda bm, h=h: (ball(bm, h, 0.045), rod(bm, h - Vector((0.25, 0, 0)), h + Vector((0.25, 0, 0)), 0.01)))
sp = world(bpy.data.objects["ActiveSpoiler_LOD0"]).translation
marker("mk_spoiler", mat("m_spoiler", CYAN, emit=18), lambda bm: (ball(bm, sp, 0.04), rod(bm, sp - Vector((0.7, 0, 0)), sp + Vector((0.7, 0, 0)), 0.01)))
sw = world(bpy.data.objects["SteeringWheel_LOD0"]); a = sw.to_3x3().col[2].normalized(); c = sw.translation
marker("mk_sw", mat("m_sw", WHITE, emit=18), lambda bm: rod(bm, c - a * 0.35, c + a * 0.25, 0.008))
render("Cam_top_3q", "hierarchy_pivot_reference.png")
