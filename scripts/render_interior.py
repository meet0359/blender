"""Presentation-only cutaways and intact through-glass/cockpit review."""
import bpy,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene; review='--review' in sys.argv
s.render.resolution_percentage=50 if review else 100
s.cycles.samples=16 if review else 48
state={o.name:o.hide_render for o in bpy.data.objects}
exposure=s.view_settings.exposure
interior=set(bpy.data.collections['INTERIOR'].all_objects)
vehicle=set()
for n in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']:
    vehicle.update(bpy.data.collections[n].all_objects)
def reset():
    for name,hidden in state.items():
        o=bpy.data.objects.get(name)
        if o: o.hide_render=hidden
def light(name,loc,power,size,target):
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.shape='DISK'; d.size=size
    o=bpy.data.objects.new(name,d); bpy.data.collections['PRESENTATION'].objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
key=light('QA_Interior_Softbox',(0,-.1,2.1),110,1.8,(0,0,.5))
fill=light('QA_Interior_Fill',(1.4,.8,1.5),55,1.2,(0,-.3,.6))
views=[('interior_driver','Camera_Interior_Driver','cutaway'),
('interior_passenger','Camera_Interior_Passenger','cutaway'),
('interior_dashboard','Camera_Interior_Dashboard','dashboard'),
('interior_seats','Camera_Interior_Seats','seats'),
('interior_cockpit','Camera_Cockpit_QA','intact'),
('interior_through_front_3q','Camera_Presentation','intact'),
('interior_through_side','Camera_Side','intact'),
('interior_through_rear_3q','Camera_Rear_ThreeQuarter','intact')]
if '--only' in sys.argv:
    selected=sys.argv[sys.argv.index('--only')+1].split(',')
    views=[v for v in views if v[0] in selected]
for keyname,cam,mode in views:
    reset(); key.hide_render=mode=='intact'; fill.hide_render=mode=='intact'
    s.view_settings.exposure=exposure if mode=='intact' else exposure-.65
    if mode!='intact':
        for o in vehicle-interior: o.hide_render=True
        for o in interior:
            if o.name.startswith(('Headliner','RoofRail_Liner','A_Pillar_Liner','SunVisor','OverheadConsole','DomeLight','RearViewMirror')): o.hide_render=True
        if mode=='dashboard':
            for o in interior:
                if o.name.startswith(('Seat_','Seatbelt_','RearBulkhead','DoorPanel_')): o.hide_render=True
        if mode=='seats':
            for o in interior:
                if not o.name.startswith(('Seat_','Seatbelt_','Floor','Seat_Rail','RearBulkhead')): o.hide_render=True
    s.camera=bpy.data.objects[cam]
    s.render.filepath=str(ROOT/'previews'/(('review_' if review else '')+keyname+'.png'))
    print('RENDER',keyname,mode,flush=True)
    bpy.ops.render.render(write_still=True)
reset()
s.view_settings.exposure=exposure
for o in [key,fill]: bpy.data.objects.remove(o,do_unlink=True)
s.camera=bpy.data.objects['Camera_Presentation']
s.render.resolution_percentage=100; s.cycles.samples=48
if '--save-final' in sys.argv:
    s.render.filepath=str(ROOT/'previews/interior_through_front_3q.png')
    for fn,name in [('interior_report.md','READ_ME_Interior_05'),('interior_validation.txt','VALIDATION_Interior_05')]:
        if (ROOT/fn).exists():
            t=bpy.data.texts.get(name) or bpy.data.texts.new(name); t.clear(); t.write((ROOT/fn).read_text())
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_05_interior.blend'))
