"""Phase 1–2 only. Run with Blender --background --python this_file.py."""
import bpy
import math
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.unit_settings.length_unit = 'METERS'
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.display.shading.light = 'STUDIO'
scene.display.shading.studiolight_rotate_z = 0.35
scene.display.shading.color_type = 'OBJECT'
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = 'BOTH'
scene.display.shading.show_object_outline = False
scene.display.shading.background_type = 'WORLD'
scene.world.color = (0.055, 0.055, 0.055)
collections = {}
for name in ['CAR', 'WHEELS', 'BRAKES', 'INTERIOR', 'GLASS', 'LIGHTS', 'COLLIDERS', 'LODS', 'REFERENCES', 'PRESENTATION']:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    collections[name] = c

PAINT = (0.38, 0.075, 0.055, 1)
CHARCOAL = (0.055, 0.065, 0.075, 1)

def link(obj, coll):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collections[coll].objects.link(obj)
    return obj

def mesh(name, verts, faces, coll='CAR', color=PAINT):
    data = bpy.data.meshes.new(name + '_Mesh')
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    collections[coll].objects.link(obj)
    obj.color = color
    return obj

def normals(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

def bevel(obj, width=0.025, segments=3):
    mod = obj.modifiers.new('Blockout edge radius', 'BEVEL')
    mod.width = width
    mod.segments = segments
    mod = obj.modifiers.new('Area weighted normals', 'WEIGHTED_NORMAL')
    mod.keep_sharp = True

def box(name, center, dims, color=PAINT, coll='CAR', radius=0.025):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = link(bpy.context.object, coll)
    obj.name = name
    obj.data.name = name + '_Mesh'
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.color = color
    if radius:
        bevel(obj, radius)
    return obj

ref = bpy.data.objects.new('Vehicle_Dimensions_Reference', None)
collections['REFERENCES'].objects.link(ref)
ref.empty_display_type = 'CUBE'
ref.empty_display_size = 1
ref.location = (0, 0, 0.60)
ref.scale = (1.0, 2.29, 0.60)
ref.hide_render = True
ref.hide_set(True)
ref['description'] = 'Envelope: 4.58 m length × 2.00 m width × 1.20 m height. Front = -Y; up = +Z.'
for label, y in [('Front_Axle_Reference', -1.35), ('Rear_Axle_Reference', 1.35)]:
    o = bpy.data.objects.new(label, None)
    collections['REFERENCES'].objects.link(o)
    o.location = (0, y, 0.35 if y < 0 else 0.365)
    o.empty_display_type = 'ARROWS'
    o.empty_display_size = 0.35
    o.hide_render = True
    o.hide_set(True)
scene['milestone'] = 'PHASE 1 + PHASE 2 ONLY — proportions blockout; no detailed materials, lights, interior, or LODs'
scene['forward_axis'] = '-Y'
scene['wheel_rotation_axis'] = 'Local X; left/right wheel meshes use identical axis convention'
scene['wheelbase_m'] = 2.70
scene['target_length_m'] = 4.58
scene['target_width_m'] = 2.00
scene['target_height_m'] = 1.20
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'racing_car_00_scene_setup.blend'))

# Cross sections create a symmetric low-resolution shell. The sidewall lower
# edge follows circular arch cutouts rather than covering the tires with boxes.
stations = [(-2.29,.82,.54),(-2.12,.91,.62),(-1.85,.96,.71),
            (-1.35,.99,.79),(-.90,.96,.78),(-.50,.93,.76),
            (0,.93,.75),(.60,.96,.79),(1.05,.99,.85),
            (1.35,1.0,.87),(1.75,.99,.83),(2.05,.94,.75),(2.29,.89,.68)]

def section(y):
    for (a,w,z),(b,w2,z2) in zip(stations,stations[1:]):
        if a <= y <= b:
            t=(y-a)/(b-a)
            return w*(1-t)+w2*t, z*(1-t)+z2*t
    return stations[-1][1:]

ys = sorted(set([round(-2.29+i*4.58/100,6) for i in range(101)] + [s[0] for s in stations] +
                [round(c+d,6) for c,r in [(-1.35,.395),(1.35,.415)] for d in [-r,-r+.004,0,r-.004,r]]))
verts=[]
for y in ys:
    w,z=section(y)
    bottom=.18
    for c,r in [(-1.35,.395),(1.35,.415)]:
        dy=abs(y-c)
        if dy < r:
            bottom=max(bottom,(.35 if c<0 else .365)+math.sqrt(max(0,r*r-dy*dy)))
    for x,h in [(0,z-.032),(.48*w,z-.018),(.78*w,z+.008),(w,z-.035),(w*.995,max(bottom,z-.12)),(w*.96,bottom)]:
        verts.append((x,y,h))
body_faces=[]
hood_faces=[]
for i in range(len(ys)-1):
    for j in range(5):
        face=(i*6+j,(i+1)*6+j,(i+1)*6+j+1,i*6+j+1)
        (hood_faces if ys[i+1]<=-.90 and j<2 else body_faces).append(face)
for name,faces in [('Car_Body',body_faces),('Hood',hood_faces)]:
    # Discard unreferenced vertices to keep edit-mode topology useful.
    used=sorted({v for f in faces for v in f})
    remap={old:new for new,old in enumerate(used)}
    obj=mesh(name,[verts[i] for i in used],[tuple(remap[i] for i in f) for f in faces])
    normals(obj)
    mod=obj.modifiers.new('Centerline symmetry','MIRROR')
    mod.use_clip=True
    mod.use_mirror_merge=True
    mod=obj.modifiers.new('Blockout panel thickness','SOLIDIFY')
    mod.thickness=.008
    mod.offset=-1
    for p in obj.data.polygons:
        p.use_smooth=True
    obj['phase']='2: provisional surface, refinement reserved for Phase 3'

box('Chassis_Blockout',(0,0,.275),(1.50,3.72,.29),CHARCOAL,radius=.055)
box('Front_Bumper',(0,-2.17,.35),(1.70,.24,.32),radius=.055)
box('Rear_Bumper',(0,2.16,.405),(1.78,.26,.40),radius=.055)

# Cabin silhouette: narrower roof, raked windshield and fastback rear deck.
cabin_sections=[(-.99,.71,.768),(-.40,.61,1.16),(-.20,.60,1.20),
                (.52,.595,1.20),(.70,.61,1.14),(1.12,.73,.84)]
cv=[]
for y,w,z in cabin_sections:
    base=section(y)[1]-.026
    cv.extend([(-.79,y,base),(-w,y,z),(w,y,z),(.79,y,base)])
cf=[]
for i in range(len(cabin_sections)-1):
    for j in range(3):
        cf.append((i*4+j,(i+1)*4+j,(i+1)*4+j+1,i*4+j+1))
cf.extend([(3,2,1,0),tuple(range(len(cv)-4,len(cv))),
           tuple([i*4 for i in range(len(cabin_sections))]+[i*4+3 for i in reversed(range(len(cabin_sections)))])])
cabin=mesh('Cabin_Roof_Blockout',cv,cf,color=(.20,.24,.28,1))
normals(cabin)
bevel(cabin,.025,3)
cabin['description']='Opaque cabin mass only; windshield, windows and interior deferred.'
box('Rear_Engine_Cover_Blockout',(0,1.63,.818),(1.20,.66,.045),radius=.03)

# Arch lips are explicit symmetric strips; still blockout geometry.
for axle,y,r,z in [('Front',-1.35,.395,.35),('Rear',1.35,.415,.365)]:
    for side,s in [('L',-1),('R',1)]:
        av=[]
        for i in range(33):
            t=math.pi*i/32
            yy=y+r*math.cos(t)
            w,_=section(yy)
            for rr in [r,r+.017]:
                av.append((s*(w+.002),y+rr*math.cos(t),z+rr*math.sin(t)))
        af=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(32)]
        o=mesh('Wheel_Arch_'+axle+'_'+side,av,af)
        normals(o)
        mod=o.modifiers.new('Arch lip thickness','SOLIDIFY')
        mod.thickness=.008

for key,x,y,r,width in [('FL',-.825,-1.35,.345,.29),('FR',.825,-1.35,.345,.29),
                         ('RL',-.835,1.35,.365,.33),('RR',.835,1.35,.365,.33)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=width,location=(x,y,r),rotation=(0,math.pi/2,0))
    o=link(bpy.context.object,'WHEELS')
    o.name='Wheel_'+key
    o.data.name=o.name+'_Mesh'
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    o.color=CHARCOAL
    bevel(o,.025,4)
    for p in o.data.polygons:
        p.use_smooth=len(p.vertices)==4
    o['axle_axis']='X'
    o['diameter_m']=2*r
    o['description']='Rounded cylinder placeholder; tire and rim separation deferred to Phase 7.'
    # Flat inset gives the placeholder a readable center without wheel detail.
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r*.70,depth=.012,
        location=(x+math.copysign(width/2+.002,x),y,r),rotation=(0,math.pi/2,0))
    hub=link(bpy.context.object,'WHEELS')
    hub.name='Wheel_Center_Placeholder_'+key
    hub.data.name=hub.name+'_Mesh'
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    hub.color=(.27,.29,.31,1)
    hub.parent=o
    hub.matrix_parent_inverse=o.matrix_world.inverted()
    bevel(hub,.006,2)

def camera(name,location,target):
    bpy.ops.object.camera_add(location=location)
    o=link(bpy.context.object,'PRESENTATION')
    o.name=name
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.type='ORTHO'
    o.data.ortho_scale=6.4
    return o
scene.camera=camera('Camera_Blockout_Review',(6,-8,4.3),(0,0,.55))
camera('Camera_Side_Blockout',(7,0,1.5),(0,0,.55))
camera('Camera_Rear_Blockout',(6,8,3.4),(0,0,.55))
floor=box('Blockout_Review_Floor',(0,0,-.045),(200,200,.05),(.16,.17,.19,1),'PRESENTATION',0)
floor.hide_set(True)

readme=bpy.data.texts.new('READ_ME_Phase_02')
readme.write('ORIGINAL SUPERCAR — PHASES 1 & 2\n\nMetric / 1 Blender unit = 1 metre\nFront: -Y. Up: +Z. Axles: X.\nEnvelope: 4.58 × 2.00 × 1.20 m\nWheelbase: 2.70 m; axle Y: -1.35 / +1.35\nFront placeholder: Ø0.690 m × 0.290 m\nRear placeholder: Ø0.730 m × 0.330 m\nChassis clearance: 0.130 m\n\nWheel origins are axle centers. Wheel center caps are parented.\nBody and hood use a live X Mirror. Body has real arch cutouts.\nColors are viewport colors, not finished materials. Cabin is an opaque mass.\nEmpty downstream collections are intentional. Hidden REFERENCES are intentional.\nPRESENTATION holds blockout review cameras and a render-only floor.\n\nNEXT: manual proportion approval and Phase 3 surface refinement.\nReview hood curvature, roof rake, rear haunches, arch transitions and overhangs.\nThis is a blockout, not a game-ready completed asset. No LODs, UVs, detailed\nlighting, glass, interior or final materials have been created.\n')

# Store a useful opening view and select the primary symmetric shell.
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Car_Body'].select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['Car_Body']
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            area.spaces.active.region_3d.view_rotation=scene.camera.rotation_euler.to_quaternion()
            area.spaces.active.region_3d.view_distance=7
            area.spaces.active.region_3d.view_location=(0,0,.55)
            area.spaces.active.clip_end=500
            area.spaces.active.shading.color_type='OBJECT'
            area.spaces.active.overlay.show_floor=False
            area.spaces.active.overlay.show_extras=False
scene.render.filepath=str(ROOT/'previews'/'blockout_front.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_01_blockout.blend'))
bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['Camera_Side_Blockout']
scene.render.filepath=str(ROOT/'previews'/'blockout_side.png')
bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['Camera_Rear_Blockout']
scene.render.filepath=str(ROOT/'previews'/'blockout_rear.png')
bpy.ops.render.render(write_still=True)

