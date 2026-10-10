import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.samples=48; s.cycles.use_denoising=True
s.render.resolution_x=1920; s.render.resolution_y=1080; s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
views={
'exterior_front':'Camera_Front',
'exterior_front_3q':'Camera_Presentation',
'exterior_side':'Camera_Side',
'exterior_rear_3q':'Camera_Rear_ThreeQuarter',
'exterior_rear':'Camera_Rear',
'exterior_top_3q':'Camera_Top_ThreeQuarter',
'exterior_headlight_closeup':'Camera_Headlight_Closeup',
'exterior_taillight_closeup':'Camera_Taillight_Closeup',
'exterior_wheel_closeup':'Camera_Wheel_Closeup'}
for key,name in views.items():
    s.camera=bpy.data.objects[name]
    s.render.filepath=str(ROOT/'previews'/(key+'.png'))
    print('FINAL PREVIEW',key,flush=True)
    bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Camera_Presentation']
s.render.filepath=str(ROOT/'previews/exterior_front_3q.png')
for filename,textname in [('exterior_report.md','READ_ME_Exterior_04'),('exterior_validation.txt','VALIDATION_Exterior_04')]:
    path=ROOT/filename
    if path.exists():
        t=bpy.data.texts.get(textname) or bpy.data.texts.new(textname)
        t.clear(); t.write(path.read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_04_exterior_final.blend'))
