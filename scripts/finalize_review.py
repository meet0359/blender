"""Camera/floor framing correction and embedded documentation only."""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.context.scene
camera=bpy.data.objects['Camera_Side']
# Move backward along the same view ray: projection of the car is unchanged,
# but bottom rays begin above the studio floor instead of inside its thickness.
camera.location=(12,0,1.755)
camera.rotation_euler=(Vector((0,0,.57))-camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera=camera
scene.render.filepath=str(ROOT/'previews'/'realistic_side.png')
bpy.ops.render.render(write_still=True)
scene.camera=bpy.data.objects['Camera_Presentation']
scene.render.filepath=str(ROOT/'previews'/'realistic_front_3q.png')
old=bpy.data.texts.get('READ_ME_Phase_02')
if old: old.name='ARCHIVE_READ_ME_Phase_02'
for name,file in [('REPORT_Realistic_Body','realistic_body_report.md'),('VALIDATION_Realistic_Body','realistic_body_validation.txt')]:
    text=bpy.data.texts.get(name) or bpy.data.texts.new(name)
    text.clear()
    text.write((ROOT/file).read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_03_realistic_body.blend'))
