# Pulse EV review renders (same rig as Phase A / Zero Gap R) (read-only: opens the blend, never saves). Identical camera rig + lighting for every vehicle.
#   Blender -b --factory-startup --python va_render.py -- <blend> <tag> <pct>
# LOD0 render geometry only; hidden reference masters, colliders, other LODs, file cameras / lights are excluded.
import sys; sys.dont_write_bytecode = True
import bpy, os, re, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; SRC, TAG, PCT, OUT = a[0], a[1], int(a[2]), a[3]; ONLY = set(a[4:])          # optional: render only these views
os.makedirs(OUT, exist_ok=True); LK = int(os.environ.get('PV_LOD', 0))                     # optional: render LODk (LOD1 close-up shading inspection)
P0 = '/Users/meetshah/Documents/blender/environment/P0_RoadFoundation/blend/road_05_export_ready.blend'
bpy.ops.wm.open_mainfile(filepath=SRC); sc = bpy.context.scene; O = bpy.data.objects
def in_coll(o, pat):
    cs = list(o.users_collection)
    while cs:
        c = cs.pop()
        if re.search(pat, c.name): return True
        cs += [p for p in bpy.data.collections if c.name in p.children]
    return False
def lod0(o):
    if 'LOD0_Root' not in O and ('PULSE_EV' in bpy.data.collections): return (in_coll(o, r'^(PULSE_EV|LOD0_PARTS)$') or (in_coll(o, r'^PV_WHEELS$') and o.name.endswith('_LOD0'))) and not o.name.startswith('REF_')
    if in_coll(o, r'^(REFERENCE|PRESENTATION|COLLI)') or o.name.startswith(('Collision', 'QA_')): return False
    if re.search(rf'_LOD{LK}(\.|$)', o.name): return True
    p = o
    while p:
        if p.name == f'LOD{LK}_Root': return True
        p = p.parent
    return in_coll(o, f'LOD{LK}')
for o in O: o.hide_render = not (o.type in ('MESH', 'CURVE') and lod0(o))
print('LOD0 render objects', sum(1 for o in O if not o.hide_render), flush=True)
items = sc.render.bl_rna.properties['engine'].enum_items.keys(); sc.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in items else 'BLENDER_EEVEE'
sc.eevee.taa_render_samples = 48; sc.eevee.use_raytracing = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 900, PCT
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
pc = bpy.data.collections.new('VA_SESSION'); sc.collection.children.link(pc)
w = bpy.data.worlds.new('VA_World'); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes['Background']
sky = nt.nodes.new('ShaderNodeTexSky'); kinds = [i.identifier for i in sky.bl_rna.properties['sky_type'].enum_items]; sky.sky_type = 'MULTIPLE_SCATTERING' if 'MULTIPLE_SCATTERING' in kinds else 'NISHITA'; sky.sun_disc = False
nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs['Strength'].default_value = .18
sd = bpy.data.lights.new('VA_Sun', 'SUN'); sd.energy = 3.4; sd.angle = math.radians(2); sun = bpy.data.objects.new('VA_Sun', sd); pc.objects.link(sun); sun.rotation_euler = (math.radians(50), 0, math.radians(140))
d = sun.rotation_euler.to_matrix() @ Vector((0, 0, 1)); sky.sun_elevation = math.asin(d.z); sky.sun_rotation = math.atan2(d.x, d.y) % (2 * math.pi)
me = bpy.data.meshes.new('VA_Ground'); me.from_pydata([(-60, -60, 0), (60, -60, 0), (60, 60, 0), (-60, 60, 0)], [], [(0, 1, 2, 3)]); gnd = bpy.data.objects.new('VA_Ground', me); pc.objects.link(gnd)
gm = bpy.data.materials.new('VA_Ground'); gm.use_nodes = True; b = gm.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (.16, .165, .17, 1); b.inputs['Roughness'].default_value = .55; me.materials.append(gm)
cd = bpy.data.cameras.new('VA_Cam'); cam = bpy.data.objects.new('VA_Cam', cd); pc.objects.link(cam); sc.camera = cam; cd.clip_start = .02
# rig: car centred on the origin, nose -Y, vehicle left +X (physical sides; independent of the file's wheel labels)
VIEWS = [('front', (0, -8.6, .8), (0, 0, .55), 50), ('rear', (0, 8.6, .95), (0, 0, .55), 50), ('left', (8.8, 0, .85), (0, 0, .55), 50), ('right', (-8.8, 0, .85), (0, 0, .55), 50),
         ('front34', (4.6, -6.2, 1.55), (0, -.25, .5), 50), ('rear34', (-4.8, 6.0, 1.9), (0, .2, .5), 50), ('top', (0, .01, 12.5), (0, 0, 0), 50),
         ('interior', (1.55, .25, 1.32), (.05, .0, .62), 28), ('hood_zoom', (1.1, -3.4, 1.2), (.3, -1.7, .6), 40), ('tail_zoom', (-1.2, 3.7, .95), (-.3, 2.25, .55), 40), ('door_zoom', (2.6, .9, .85), (.9, -.1, .55), 40), ('front_zoom', (.9, -3.6, .6), (.35, -2.1, .42), 40), ('wing_zoom', (-1.5, 3.3, 1.45), (0, 2.0, 1.05), 40), ('canopy_zoom', (1.9, -1.2, 1.75), (.2, .35, 1.1), 40), ('intake_zoom', (2.2, -1.55, .82), (.95, -.87, .58), 40), ('wheel', (2.25, -2.45, .42), (.83, -1.37, .33), 50)]
def shot(name, loc, tgt, lens):
    cd.lens = lens; cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(OUT, f'{TAG}_{name}.png'); bpy.ops.render.render(write_still=True); print('RENDERED', sc.render.filepath, flush=True)
for v in VIEWS:
    if not ONLY or v[0] in ONLY: shot(*v)
if 'LOD0_Root' in O and (not ONLY or 'lod_lineup' in ONLY):                                          # LOD0..3 side by side (session-only offsets)
    for k in range(4):
        r = O[f'LOD{k}_Root']; r.location.x = (k - 1.5) * 2.6
        for o in r.children_recursive:
            if o.type == 'MESH': o.hide_render = False
    shot('lod_lineup', (2.0, -12.5, 3.2), (0, 0, .45), 40)
    for k in range(4): O[f'LOD{k}_Root'].location.x = 0
# chase view on the frozen P0 road (LINKED read-only); the car is moved to lane x -1.8 by a temporary parent, never saved
road = ['Road_4Lane_40m', 'Road_4Lane_40m_EdgeLines', 'Road_4Lane_40m_Dividers', 'Shoulder_Paved_R', 'Shoulder_Paved_L', 'Median_Concrete', 'Median_Barrier_LOD0']
with bpy.data.libraries.load(P0, link=True) as (src, dst): dst.meshes = [m for m in road if m in src.meshes]
for k in range(-1, 7):
    for m in dst.meshes: o = bpy.data.objects.new(f'VA_Road_{m.name}_{k}', m); o.location = (0, 40.0 - 40.0 * k, 0); pc.objects.link(o)
gnd.location.z = -.35
mover = bpy.data.objects.new('VA_Mover', None); pc.objects.link(mover)
tops = set()
for o in O:
    if o.hide_render or o.type not in ('MESH', 'CURVE') or o.name in pc.objects: continue
    p = o
    while p.parent: p = p.parent
    tops.add(p)
for t in tops: t.parent = mover                                                                        # move the whole car (top-most ancestors), session only
mover.location = (-1.8, -20.0, .018)
shot('chase', (-1.8, -20 + 7.6, 2.05), (-1.8, -20 - 30, .55), 35)
