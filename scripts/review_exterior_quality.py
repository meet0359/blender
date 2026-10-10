import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=bpy.context.scene
s.render.resolution_percentage=50
s.cycles.samples=16
p=bpy.data.materials['MAT_CarPaint'].node_tree.nodes.get('Principled BSDF')
p.inputs['Base Color'].default_value=(.22,.24,.27,1)
p.inputs['Metallic'].default_value=.75
p.inputs['Roughness'].default_value=.09
views=['Camera_Presentation','Camera_Rear_ThreeQuarter','Camera_Side','Camera_Top_ThreeQuarter','Camera_Low_Front','Camera_Low_Rear']
for name in views:
    s.camera=bpy.data.objects[name]
    s.render.filepath=str(ROOT/'previews'/('qc_gloss_'+name+'.png'))
    bpy.ops.render.render(write_still=True)
s.render.engine='BLENDER_WORKBENCH'
s.display.shading.light='FLAT'
s.display.shading.color_type='SINGLE'
s.display.shading.single_color=(.008,.008,.008)
s.display.shading.background_type='WORLD'
s.world.color=(.8,.8,.8)
s.display.shading.show_shadows=False
s.display.shading.show_cavity=False
bpy.data.objects['Studio_Floor'].hide_render=True
for name in ['Camera_Side','Camera_Presentation','Camera_Rear_ThreeQuarter']:
    s.camera=bpy.data.objects[name]
    s.render.filepath=str(ROOT/'previews'/('qc_silhouette_'+name+'.png'))
    bpy.ops.render.render(write_still=True)
