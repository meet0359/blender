import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.render.resolution_x=1280
s.render.resolution_y=720
s.display.shading.light='STUDIO'
s.display.shading.studiolight_rotate_z=.4
s.display.shading.color_type='MATERIAL'
s.display.shading.show_shadows=True
s.display.shading.show_cavity=True
s.display.shading.cavity_type='BOTH'
s.display.shading.show_object_outline=False
for name,cam in [('surface_check_front','Camera_Presentation'),('surface_check_side','Camera_Side'),('surface_check_rear','Camera_Rear_ThreeQuarter')]:
    s.camera=bpy.data.objects[cam]
    s.render.filepath=str(ROOT/'previews'/(name+'.png'))
    bpy.ops.render.render(write_still=True)
