# Reflection-line (zebra) QA: paint replaced by a mirror, world = horizontal stripes. Read-only (never saves).
#   Blender -b --factory-startup --python vx_zebra.py -- <blend> <outdir>
import sys; sys.dont_write_bytecode = True
import bpy, os, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; SRC, OUT = a[0], a[1]; os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=SRC); sc = bpy.context.scene; O = bpy.data.objects
def under(o, root):
    p = o
    while p:
        if p.name == root: return True
        p = p.parent
    return False
for o in O:
    if o.type in ('CAMERA', 'LIGHT'): o.hide_render = True
    if 'LOD0_Root' in O and o.type == 'MESH': o.hide_render = not under(o, 'LOD0_Root')            # rigged files: LOD0 only (overlapping LODs z-fight)
    if 'LOD0_Root' not in O and 'Body_Shell' in O and o.type == 'MESH': o.hide_render = o.name not in ('Body_Shell', 'Glass_Shell')   # stage-02 body check (no work / reference meshes)
for m in bpy.data.materials:
    if m.name.endswith('_Paint') and m.use_nodes:
        b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'); b.inputs['Base Color'].default_value = (.9, .9, .9, 1); b.inputs['Metallic'].default_value = 1; b.inputs['Roughness'].default_value = .02; b.inputs['Coat Weight'].default_value = 0
w = bpy.data.worlds.new('Z'); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes['Background']
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 28.0
sn = nt.nodes.new('ShaderNodeMath'); sn.operation = 'SINE'; gt = nt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.0
nt.links.new(tc.outputs['Generated'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], mul.inputs[0]); nt.links.new(mul.outputs[0], sn.inputs[0]); nt.links.new(sn.outputs[0], gt.inputs[0]); nt.links.new(gt.outputs[0], bg.inputs['Color'])
bg.inputs['Strength'].default_value = 1.0
items = sc.render.bl_rna.properties['engine'].enum_items.keys(); sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in items else 'BLENDER_EEVEE'
sc.eevee.taa_render_samples = 16; sc.render.resolution_x, sc.render.resolution_y = 1200, 675; sc.view_settings.view_transform = 'Standard'
cd = bpy.data.cameras.new('ZC'); cam = bpy.data.objects.new('ZC', cd); sc.collection.objects.link(cam); sc.camera = cam
for nm, loc, tgt, lens in (('hood', (1.6, -4.2, 1.9), (0, -1.5, .7), 40), ('roof', (2.4, -1.6, 2.2), (0, .1, 1.0), 40), ('deck', (-1.8, 4.2, 2.1), (0, 1.5, .85), 40),
                           ('door', (3.4, -.6, .9), (.9, -.2, .55), 40), ('side_full', (6.5, 0, 1.2), (0, 0, .6), 40), ('tail_corner', (-1.9, 3.3, 1.35), (-.85, 2.1, .78), 45), ('quarter', (3.0, 3.1, 1.45), (.85, 1.25, .72), 40),
                           ('deck_r', (1.8, 4.2, 2.1), (0, 1.5, .85), 40), ('front_corner', (2.0, -3.4, 1.2), (.85, -2.0, .62), 45), ('door_r', (-3.4, -.4, .9), (-.9, .1, .62), 40), ('quarter_r', (-3.0, 3.1, 1.45), (-.85, 1.25, .72), 40), ('tail_corner_r', (1.9, 3.3, 1.35), (.85, 2.1, .78), 45)):   # both sides
    cd.lens = lens; cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, f'zebra_{nm}.png'); bpy.ops.render.render(write_still=True); print('ZEBRA', nm, flush=True)
