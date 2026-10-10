import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for label,sign in [('L',-1),('R',1)]:
    for kind,shift in [('Brake',.029),('Indicator',.026)]:
        o=bpy.data.objects['Taillight_'+kind+'_'+label]
        for spline in o.data.splines:
            n=len(spline.points)
            for i,p in enumerate(spline.points):
                t=i/max(1,n-1)
                fade=max(0,min(1,(t-.78)/.22))
                fade=fade*fade*(3-2*fade)
                p.co.x-=sign*shift*fade
        o['outer_seating_fix']='Emitter endpoint inset from rounded lens boundary'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_04_exterior_final.blend'))
s=bpy.context.scene
for key,name in [('exterior_side','Camera_Side'),('exterior_rear_3q','Camera_Rear_ThreeQuarter'),('exterior_rear','Camera_Rear'),('exterior_taillight_closeup','Camera_Taillight_Closeup')]:
    s.camera=bpy.data.objects[name]; s.render.filepath=str(ROOT/'previews'/(key+'.png'))
    bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Camera_Presentation']; s.render.filepath=str(ROOT/'previews/exterior_front_3q.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_04_exterior_final.blend'))
