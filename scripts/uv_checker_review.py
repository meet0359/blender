import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; s=bpy.context.scene
m=bpy.data.materials.new('QA_UV_Checker'); m.use_nodes=True
nodes=m.node_tree.nodes; links=m.node_tree.links; p=nodes.get('Principled BSDF')
p.inputs['Roughness'].default_value=.65
uv=nodes.new('ShaderNodeUVMap'); uv.uv_map='UVMap'; checker=nodes.new('ShaderNodeTexChecker'); checker.inputs['Scale'].default_value=48
checker.inputs['Color1'].default_value=(.12,.29,.5,1); checker.inputs['Color2'].default_value=(.75,.75,.75,1)
links.new(uv.outputs[0],checker.inputs['Vector']); links.new(checker.outputs['Color'],p.inputs['Base Color'])
for o in bpy.data.objects:
    if o.type=='MESH' and 'texture_group' in o:
        for i in range(len(o.data.materials)): o.data.materials[i]=m
s.render.resolution_percentage=67; s.cycles.samples=16
for key,cam in [('materials_uv_checker_body','Camera_Presentation'),('materials_uv_checker_seats','Camera_Interior_Seats')]:
    if key.endswith('seats'):
        inside=set(bpy.data.collections['INTERIOR'].all_objects)
        for name in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS']:
            for o in bpy.data.collections[name].all_objects: o.hide_render=True
        for o in inside: o.hide_render=not o.name.startswith(('Seat_','Seatbelt_','Floor','Seat_Rail','RearBulkhead'))
    s.camera=bpy.data.objects[cam]; s.render.filepath=str(ROOT/'previews'/(key+'.png'))
    bpy.ops.render.render(write_still=True)
