# Traffic-fleet visual QA renders (read-only: opens the blend, never saves). Cycles (Metal GPU when available) + OIDN denoise.
#   Blender -b --factory-startup --python ts_render.py -- <blend> <tag> <outdir> <mode> [views...]
#   mode studio : neutral automotive studio (grey cyclorama, overhead + side softboxes, rim strip) — front34 rear34 front rear side top wheel interior
#   mode daylight: physical sky + sun over the frozen P0 road (linked read-only)                   — day_front34 day_rear34 day_side
#   mode game   : frozen P0 highway, follow camera behind / near traffic at gameplay distances      — game_close game_normal game_far (+ LOD forced via env TS_LOD)
# Env: TS_LOD=<k> renders LODk (default LOD0); TS_PAINT=r,g,b overrides the paint base colour (paint-variant sheet); TS_SAMPLES (default 64); TS_RES (default 1280).
# No lighting tricks: no bloom, no motion blur, no vignette, neutral AgX (Medium High Contrast), real exposure.
import sys; sys.dont_write_bytecode = True
import bpy, os, math, re
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; SRC, TAG, OUT, MODE = a[0], a[1], a[2], a[3]; ONLY = set(a[4:]); os.makedirs(OUT, exist_ok=True)
LK = int(os.environ.get('TS_LOD', 0)); SAMP = int(os.environ.get('TS_SAMPLES', 64)); RES = int(os.environ.get('TS_RES', 1280))
P0 = '/Users/meetshah/Documents/blender/environment/P0_RoadFoundation/blend/road_05_export_ready.blend'
bpy.ops.wm.open_mainfile(filepath=SRC); sc = bpy.context.scene; O = bpy.data.objects
def under(o, root):
    p = o
    while p:
        if p.name == root: return True
        p = p.parent
    return False
rigged = f'LOD{LK}_Root' in O
for o in O:
    if o.type in ('CAMERA', 'LIGHT'): o.hide_render = True; continue
    if o.type not in ('MESH', 'CURVE'): continue
    if o.name.startswith(('Collision', 'REF_', 'QA_')): o.hide_render = True; continue
    o.hide_render = (not under(o, f'LOD{LK}_Root')) if rigged else False
if os.environ.get('TS_ONLY'):                                                                    # diagnosis: one mesh only (e.g. REF_Master in a stage-02 file)
    for o in O:
        if o.type == 'MESH': o.hide_render = o.name != os.environ['TS_ONLY']
if os.environ.get('TS_NONORMAL'):                                                                # diagnosis: paint without the baked normal map
    for m in bpy.data.materials:
        if m.use_nodes and '_Paint' in m.name:
            for l in list(m.node_tree.links):
                if l.to_socket.name in ('Normal', 'Coat Normal') and l.to_node.type == 'BSDF_PRINCIPLED': m.node_tree.links.remove(l)
if os.environ.get('TS_PAINT'):
    col = [float(v) for v in os.environ['TS_PAINT'].split(',')]
    for m in bpy.data.materials:
        if m.name.endswith('_Paint') and m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type == 'BSDF_PRINCIPLED': n.inputs['Base Color'].default_value = (*col, 1)
                if n.type == 'RGB' and n.label == 'PaintColour': n.outputs[0].default_value = (*col, 1)
if 'TS_LIGHTS' in os.environ and bpy.data.images.get('TS_Lights_State'):                         # review light state (which channels glow)
    CH = ['DRL', 'Headlamp', 'Tail', 'Brake', 'Indicator_L', 'Indicator_R', 'Reverse', 'Marker']; on = {x.strip() for x in os.environ['TS_LIGHTS'].split(',') if x.strip()}; px = []
    for r in range(3, -1, -1):
        for c in range(4):
            i = r * 4 + c; v = 1.0 if i < len(CH) and CH[i] in on else 0.0; px += [v, v, v, 1]
    im = bpy.data.images['TS_Lights_State']; im.unpack(method='REMOVE') if im.packed_file else None; im.source = 'GENERATED'; im.generated_width = im.generated_height = 4; im.pixels.foreach_set(px); im.update()
LOOK = os.environ.get('TS_LOOK')                                                                  # QA looks (studio views): clay | wire | normal — baked body normal kept connected
if LOOK:
    for m in {m for o in O if o.type == 'MESH' and not o.hide_render for m in o.data.materials if m and m.use_nodes}:
        nt_ = m.node_tree; out_ = next((n for n in nt_.nodes if n.type == 'OUTPUT_MATERIAL'), None); b_ = next((n for n in nt_.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        nsock = b_.inputs['Normal'].links[0].from_socket if b_ and b_.inputs['Normal'].links else None
        if LOOK == 'normal':
            g_ = nt_.nodes.new('ShaderNodeNewGeometry'); vm = nt_.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'; vm.inputs[1].default_value = (.5, .5, .5); vm.inputs[2].default_value = (.5, .5, .5)
            nt_.links.new(nsock or g_.outputs['Normal'], vm.inputs[0]); e_ = nt_.nodes.new('ShaderNodeEmission'); nt_.links.new(vm.outputs[0], e_.inputs[0]); nt_.links.new(e_.outputs[0], out_.inputs[0])
        else:
            c_ = nt_.nodes.new('ShaderNodeBsdfPrincipled'); c_.inputs['Base Color'].default_value = (.42, .42, .43, 1); c_.inputs['Roughness'].default_value = .38
            if nsock: nt_.links.new(nsock, c_.inputs['Normal'])
            sh_ = c_.outputs[0]
            if LOOK == 'wire':
                w_ = nt_.nodes.new('ShaderNodeWireframe'); w_.use_pixel_size = True; w_.inputs[0].default_value = 1.0; d_ = nt_.nodes.new('ShaderNodeBsdfDiffuse'); d_.inputs[0].default_value = (.01, .01, .012, 1)
                mx = nt_.nodes.new('ShaderNodeMixShader'); nt_.links.new(w_.outputs[0], mx.inputs[0]); nt_.links.new(c_.outputs[0], mx.inputs[1]); nt_.links.new(d_.outputs[0], mx.inputs[2]); sh_ = mx.outputs[0]
            nt_.links.new(sh_, out_.inputs[0])
        if hasattr(m, 'surface_render_method'): m.surface_render_method = 'DITHERED'
sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.samples = SAMP; cy.use_denoising = True; cy.use_adaptive_sampling = True
try:
    pr = bpy.context.preferences.addons['cycles'].preferences; pr.compute_device_type = 'METAL'; pr.get_devices()
    for d in pr.devices: d.use = True
    cy.device = 'GPU'
except Exception as e: print('CPU render', e)
cy.max_bounces = 8; cy.glossy_bounces = 4; cy.transmission_bounces = 8; cy.transparent_max_bounces = 16
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = RES, RES * 9 // 16, 100
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
S = bpy.data.collections.new('TS_SESSION'); sc.collection.children.link(S)
def plane(name, w, h, loc, rot, mat):
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)]); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); S.objects.link(o); o.location = loc; o.rotation_euler = rot; return o
def emit(name, strength, col=(1, 1, 1)):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); e = nt.nodes.new('ShaderNodeEmission'); o = nt.nodes.new('ShaderNodeOutputMaterial')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength; nt.links.new(e.outputs[0], o.inputs[0]); return m
def diffuse(name, col, rough=.6):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; return m
w = bpy.data.worlds.new('TS_World'); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes['Background']
cd = bpy.data.cameras.new('TS_Cam'); cam = bpy.data.objects.new('TS_Cam', cd); S.objects.link(cam); sc.camera = cam; cd.clip_start = .05; cd.clip_end = 2000
CAMK = float(os.environ.get('TS_CAM_SCALE', 1.0))                                                 # pull studio cameras back along their view line (longer vehicles; same factor for both cars in a comparison)
SHIFT = {'F': float(os.environ.get('TS_SHIFT_F', 0)), 'R': float(os.environ.get('TS_SHIFT_R', 0)), 'W': float(os.environ.get('TS_SHIFT_W', 0)), 'I': float(os.environ.get('TS_SHIFT_I', 0))}   # per-vehicle close-up framing (y shift, m)
LIFT = {k: float(os.environ.get('TS_LIFT_' + k, 0)) for k in 'FRWI'}                                # per-vehicle close-up height (z shift, m): SUV lamps sit higher
LALL = float(os.environ.get('TS_LIFT_ALL', 0))
VGRP = {'front_detail': 'F', 'bumper_front': 'F', 'lamp_front': 'F', 'lamp_front_R': 'F', 'rear_detail': 'R', 'bumper_rear': 'R', 'lamp_rear': 'R', 'plate_rear': 'R', 'quarter_rear_L': 'R', 'quarter_rear_R': 'R', 'wheel': 'W', 'interior': 'I'}
def shot(name, loc, tgt, lens):
    if ONLY and name not in ONLY: return
    if MODE == 'studio' and name in VGRP and (SHIFT[VGRP[name]] or LIFT[VGRP[name]]):
        dy, dz = SHIFT[VGRP[name]], LIFT[VGRP[name]]; loc = (loc[0], loc[1] + dy, loc[2] + dz); tgt = (tgt[0], tgt[1] + dy, tgt[2] + dz)
    if MODE == 'studio' and LALL: loc = (loc[0], loc[1], loc[2] + LALL); tgt = (tgt[0], tgt[1], tgt[2] + LALL)   # tall vehicles (truck, bus): lift every studio camera + target
    if CAMK != 1.0 and MODE == 'studio' and cd.type == 'PERSP': loc = tuple(Vector(tgt) + (Vector(loc) - Vector(tgt)) * CAMK)
    cd.lens = lens; cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    if 'Cyc' in bpy.data.objects: bpy.data.objects['Cyc'].rotation_euler = (0, 0, 0 if loc[1] < 0 else math.pi)        # backdrop always behind the car
    sc.render.filepath = os.path.join(OUT, f'{TAG}_{name}.png'); bpy.ops.render.render(write_still=True); print('RENDERED', sc.render.filepath, flush=True)
if MODE == 'studio':
    bg.inputs[0].default_value = (.035, .037, .04, 1); bg.inputs[1].default_value = 1.0
    # cyclorama: floor + curved cove + back wall (seamless), neutral 18 % grey, slightly glossy floor for contact reflections
    import bmesh
    bm = bmesh.new(); prof = [(y, 0.0) for y in (-14, 4)] + [(4 + 3 * math.sin(t * math.pi / 2), 3 - 3 * math.cos(t * math.pi / 2)) for t in [k / 8 for k in range(1, 9)]] + [(7, 9)]
    rows = [[bm.verts.new((x, y, z)) for y, z in prof] for x in (-16, 16)]
    for i in range(len(prof) - 1): bm.faces.new((rows[0][i], rows[1][i], rows[1][i + 1], rows[0][i + 1]))
    me = bpy.data.meshes.new('Cyc'); bm.to_mesh(me); bm.free(); cyc = bpy.data.objects.new('Cyc', me); S.objects.link(cyc); me.shade_smooth()
    me.materials.append(diffuse('TS_Cyc', (.16, .16, .165), .45)); cyc.rotation_euler = (0, 0, math.radians(180))
    plane('Soft_Top', 6.0, 3.0, (0, 0, 5.2), (0, 0, 0), emit('E1', 9.0)).rotation_euler = (math.pi, 0, 0)       # overhead key (the long highlight on hood / roof)
    plane('Soft_L', 4.0, 1.6, (6.5, -.5, 3.6), (0, math.radians(-60), 0), emit('E2', 6.0))                       # side strips (door / shoulder reflections)
    plane('Soft_R', 4.0, 1.6, (-6.5, .5, 3.6), (0, math.radians(60), 0), emit('E3', 3.5))
    plane('Soft_Rim', 5.0, 1.0, (0, 7.0, 4.2), (math.radians(55), 0, 0), emit('E4', 4.0))
    plane('Soft_Front', 3.0, 1.2, (0, -7.0, 4.0), (math.radians(-55), 0, 0), emit('E5', 2.5))
    KS = float(os.environ.get('TS_STUDIO_SCALE', 1.0))                                                # trucks / buses: whole studio (cyclorama + softboxes) scaled together, same look
    if KS != 1.0:
        for o_ in [cyc] + [o for o in bpy.data.objects if o.name.startswith('Soft_')]: o_.location = o_.location * KS; o_.scale = o_.scale * KS
    V = [('front34', (4.3, -5.9, 1.45), (0, -.2, .62), 55), ('rear34', (-4.4, 5.8, 1.6), (0, .2, .62), 55), ('front', (0, -8.4, 1.0), (0, 0, .70), 55),
         ('rear', (0, 8.4, 1.05), (0, 0, .72), 55), ('side', (9.0, 0, 1.0), (0, 0, .68), 50), ('top', (0, .01, 11.5), (0, 0, 0), 45),
         ('wheel', (2.3, -2.6, .55), (.80, -1.35, .34), 60), ('interior', (1.55, .05, 1.42), (0, -.05, .82), 26), ('front_detail', (1.4, -4.2, .85), (.45, -2.1, .62), 55), ('rear_detail', (-1.3, 4.3, .95), (-.45, 2.1, .72), 55)]
    V += [('bumper_front', (1.9, -4.0, .62), (.30, -2.10, .45), 45), ('bumper_rear', (-1.9, 4.1, .70), (-.30, 2.15, .52), 45), ('lamp_front', (1.30, -3.25, .85), (.66, -2.14, .66), 50),
          ('lamp_rear', (-1.25, 3.35, 1.02), (-.66, 2.25, .86), 50), ('plate_rear', (0, 3.4, .95), (0, 2.3, .73), 55), ('arch_rear', (2.6, 2.0, .75), (.85, 1.35, .45), 45)]
    V += [('quarter_rear_L', (1.9, 3.9, .75), (.70, 2.05, .55), 45), ('quarter_rear_R', (-1.9, 3.9, .75), (-.70, 2.05, .55), 45), ('lamp_front_R', (-1.30, -3.25, .85), (-.66, -2.14, .66), 50)]   # r3 artifact views (both sides)
    for v in V:
        if v[0] == 'interior':                                                                       # cabin shot: no softbox mirrored in the near glass; fills through windshield, far windows and a low near-side fill (below the reflection angle)
            for n_ in ('Soft_L', 'Soft_Top'): bpy.data.objects[n_].hide_render = True
            for nm, loc, rot, en, sz in (('Fill_WS', (0, -2.6, 1.7), (math.radians(-70), 0, 0), 900, 1.6), ('Fill_Far', (-2.6, 0, 1.25), (0, math.radians(-80), 0), 700, 1.6), ('Fill_Near', (3.2, -.2, .55), (0, math.radians(75), 0), 450, 2.0)):
                ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = en; ld.size = sz; lo = bpy.data.objects.new(nm, ld); S.objects.link(lo); lo.location = loc; lo.rotation_euler = rot
            shot('interior', (1.75, -.10, 1.18), (0, -.12, .86), 24)
            for n_ in ('Soft_L', 'Soft_Top'): bpy.data.objects[n_].hide_render = False
            for nm in ('Fill_WS', 'Fill_Far', 'Fill_Near'): bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
        else: shot(*v)
    for nm, loc, tgt, sz in (('ortho_front', (0, -9, .72), (0, 0, .72), 2.4), ('ortho_rear', (0, 9, .72), (0, 0, .72), 2.4), ('ortho_side', (9, 0, .72), (0, 0, .72), 5.0)):
        if ONLY and nm not in ONLY: continue
        cd.type = 'ORTHO'; cd.ortho_scale = sz * float(os.environ.get('TS_ORTHO_SCALE', 1.0)); shot(nm, loc, tgt, 50); cd.type = 'PERSP'   # TS_ORTHO_SCALE: same factor for both cars in a comparison
else:
    sky = nt.nodes.new('ShaderNodeTexSky'); kinds = [i.identifier for i in sky.bl_rna.properties['sky_type'].enum_items]; sky.sky_type = 'MULTIPLE_SCATTERING' if 'MULTIPLE_SCATTERING' in kinds else 'NISHITA'
    sky.sun_disc = False; nt.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = .30
    sd = bpy.data.lights.new('TS_Sun', 'SUN'); sd.energy = 4.0; sd.angle = math.radians(1.2); sun = bpy.data.objects.new('TS_Sun', sd); S.objects.link(sun); sun.rotation_euler = (math.radians(52), 0, math.radians(135))
    d = sun.rotation_euler.to_matrix() @ Vector((0, 0, 1)); sky.sun_elevation = math.asin(d.z); sky.sun_rotation = math.atan2(d.x, d.y) % (2 * math.pi)
    g = plane('Ground', 400, 400, (0, 0, -.35), (0, 0, 0), diffuse('TS_Ground', (.10, .11, .08), .9))
    road = ['Road_4Lane_40m', 'Road_4Lane_40m_EdgeLines', 'Road_4Lane_40m_Dividers', 'Shoulder_Paved_R', 'Shoulder_Paved_L', 'Median_Concrete', 'Median_Barrier_LOD0']
    with bpy.data.libraries.load(P0, link=True) as (src, dst): dst.meshes = [m for m in road if m in src.meshes]
    for k in range(-2, 9):
        for m in dst.meshes: o = bpy.data.objects.new(f'TS_Road_{m.name}_{k}', m); o.location = (0, 40.0 - 40.0 * k, 0); S.objects.link(o)
    mover = bpy.data.objects.new('TS_Mover', None); S.objects.link(mover); tops = set()
    for o in O:
        if o.hide_render or o.type not in ('MESH', 'CURVE') or o.name in S.objects: continue
        p = o
        while p.parent: p = p.parent
        tops.add(p)
    for t in tops: t.parent = mover
    LX = -1.8; mover.location = (LX, -20.0, .018)                                                           # car in the right-hand lane of the P0 road
    if MODE == 'daylight':
        for v in [('day_front34', (LX + 4.2, -26.0, 1.35), (LX, -20.2, .6), 50), ('day_rear34', (LX - 4.0, -13.8, 1.5), (LX, -19.8, .65), 50), ('day_side', (LX + 8.0, -20.0, 1.0), (LX, -20.0, .7), 45),
                  ('day_glass', (LX + 2.6, -20.6, 1.30), (LX, -20.05, .95), 35)]: shot(*v)                    # r3: side glass / cabin in neutral daylight
    else:   # game: the camera follows behind a player car (camera height 1.9-2.4 m, lens 50 mm-equivalent on a 16:9 mobile frame) looking at this traffic car ahead
        for v in [('game_close', (LX, -20.0 + 7.5, 2.0), (LX, -20.0 - 20, .7), 35), ('game_normal', (LX + .4, -20.0 + 22.0, 2.2), (LX, -20.0 - 30, .8), 35), ('game_far', (LX + .6, -20.0 + 60.0, 2.4), (LX, -20.0 - 60, .9), 35)]: shot(*v)
