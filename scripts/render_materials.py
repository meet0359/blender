import bpy,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]; s=bpy.context.scene
review='--review' in sys.argv
s.render.resolution_percentage=50 if review else 100; s.cycles.samples=16 if review else 48
pres=bpy.data.collections['PRESENTATION']
def camera(name,loc,target,lens):
    o=bpy.data.objects.get(name)
    if not o: o=bpy.data.objects.new(name,bpy.data.cameras.new(name)); pres.objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); o.data.lens=lens; o.data.clip_start=.008
    return o
camera('Camera_Materials_Carbon',(1.35,-3.5,.72),(.54,-2.19,.185),65)
camera('Camera_Materials_Steering',(-.49,.17,.91),(-.36,-.445,.736),52)
views=[('materials_front_3q','Camera_Presentation','intact'),('materials_rear_3q','Camera_Rear_ThreeQuarter','intact'),('materials_side','Camera_Side','intact'),('materials_front','Camera_Front','intact'),('materials_rear','Camera_Rear','intact'),('materials_headlight','Camera_Headlight_Closeup','intact'),('materials_taillight','Camera_Taillight_Closeup','intact'),('materials_wheel_brake','Camera_Wheel_Closeup','intact'),('materials_carbon','Camera_Materials_Carbon','intact'),('materials_interior_cockpit','Camera_Cockpit_QA','intact'),('materials_interior_dashboard','Camera_Interior_Dashboard','dashboard'),('materials_interior_seats','Camera_Interior_Seats','seats'),('materials_steering','Camera_Materials_Steering','dashboard'),('materials_daylight','Camera_Presentation','day'),('materials_night_front','Camera_Presentation','night'),('materials_night_rear','Camera_Rear_ThreeQuarter','night'),('materials_night_cockpit','Camera_Cockpit_QA','night')]
if '--only' in sys.argv:
    wanted=sys.argv[sys.argv.index('--only')+1].split(','); views=[v for v in views if v[0] in wanted]
interior=set(bpy.data.collections['INTERIOR'].all_objects); asset=set()
for n in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']: asset.update(bpy.data.collections[n].all_objects)
visibility={o.name:o.hide_render for o in bpy.data.objects}
energy={o.name:o.data.energy for o in bpy.data.objects if o.type=='LIGHT'}
world=s.world; world.use_nodes=True; bg=world.node_tree.nodes.get('Background'); bgold=bg.inputs['Strength'].default_value
exposure=s.view_settings.exposure
def area(name,loc,power,size,target):
    o=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA')); pres.objects.link(o)
    o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); return o
fill=area('QA_Material_Interior',(0,0,2),95,1.8,(0,0,.5))
sun=bpy.data.objects.new('QA_Material_Daylight',bpy.data.lights.new('QA_Material_Daylight','SUN')); pres.objects.link(sun); sun.data.energy=2; sun.data.angle=.15; sun.rotation_euler=(.48,-.55,-.7)
for key,cam,mode in views:
    for name,h in visibility.items(): bpy.data.objects[name].hide_render=h
    for name,e in energy.items(): bpy.data.objects[name].data.energy=e*(.045 if mode=='night' else .4 if mode=='day' else 1)
    bg.inputs['Strength'].default_value=.035 if mode=='night' else .55 if mode=='day' else bgold
    fill.hide_render=mode not in ['dashboard','seats']; sun.hide_render=mode!='day'
    s.view_settings.exposure=exposure-.4 if mode in ['dashboard','seats'] else exposure
    if mode in ['dashboard','seats']:
        for o in asset-interior: o.hide_render=True
        for o in interior:
            if o.name.startswith(('Headliner','RoofRail_Liner','A_Pillar_Liner','SunVisor','OverheadConsole','DomeLight','RearViewMirror')): o.hide_render=True
            if mode=='dashboard' and o.name.startswith(('Seat_','Seatbelt_','RearBulkhead','DoorPanel_')): o.hide_render=True
            if mode=='seats' and not o.name.startswith(('Seat_','Seatbelt_','Floor','Seat_Rail','RearBulkhead')): o.hide_render=True
    s.camera=bpy.data.objects[cam]; s.render.filepath=str(ROOT/'previews'/(('review_' if review else '')+key+'.png'))
    print('RENDER',key,flush=True); bpy.ops.render.render(write_still=True)
for name,h in visibility.items(): bpy.data.objects[name].hide_render=h
for name,e in energy.items(): bpy.data.objects[name].data.energy=e
bg.inputs['Strength'].default_value=bgold; s.view_settings.exposure=exposure
for o in [fill,sun]: bpy.data.objects.remove(o,do_unlink=True)
s.camera=bpy.data.objects['Camera_Presentation']; s.render.resolution_percentage=100; s.cycles.samples=48
if '--save-final' in sys.argv:
    for fn,n in [('materials_report.md','READ_ME_Materials_UV_06'),('uv_validation.txt','VALIDATION_UV_06'),('shader_validation.txt','VALIDATION_Shader_06')]:
        if (ROOT/fn).exists():
            t=bpy.data.texts.get(n) or bpy.data.texts.new(n); t.clear(); t.write((ROOT/fn).read_text())
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_06_materials_uv.blend'))
