# Diagnostic: per-object random colours (front / rear close-ups) of LOD0. Read-only.
import sys; sys.dont_write_bytecode = True
import bpy, math, random, re, os, zlib
from mathutils import Vector
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'previews', '_diag')
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/Users/meetshah/Documents/blender/racing_car_09_unity_export_ready.blend'); sc = bpy.context.scene; O = bpy.data.objects
for n in ('Steering_Wheel_LOD0', 'Seat_Driver_LOD0', 'InstrumentCluster_LOD0', 'Pedal_Accelerator_LOD0'):
    if n in O: print('POS', n, [round(v, 3) for v in O[n].matrix_world.translation])
l0 = [o for o in O if re.search(r'_LOD0$', o.name) and o.type == 'MESH' and any(c.name.startswith('LOD0_') for c in o.users_collection)]
HIDE = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
for o in O: o.hide_render = o not in l0 or any(re.search(h, o.name) for h in HIDE)
cache = {}
for o in l0:
    r = random.Random(zlib.crc32(o.name.encode())); m = bpy.data.materials.new('D_' + o.name); m.diffuse_color = (r.random(), r.random(), r.random(), 1); o.data.materials.clear(); o.data.materials.append(m)
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'; sc.display.shading.show_object_outline = True
sc.render.resolution_x, sc.render.resolution_y = 1400, 900
cd = bpy.data.cameras.new('C'); cam = bpy.data.objects.new('C', cd); sc.collection.objects.link(cam); sc.camera = cam
for nm, loc, tgt, lens in (('front_low34', (1.9, -4.3, .55), (0, -2.0, .45), 45), ('front_straight', (0, -5.5, .5), (0, -2, .48), 50), ('rear_low34', (-1.9, 4.4, .6), (0, 2.0, .45), 45),
                           ('side_front', (3.6, -1.9, .5), (0, -1.9, .45), 50), ('top_front', (0, -1.6, 4.2), (0, -1.6, .4), 50)):
    cd.lens = lens; cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, f'diag_{nm}{"_bare" if HIDE else ""}.png'); bpy.ops.render.render(write_still=True); print('R', nm)
