import bpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=bpy.context.scene
# FBX stores material slots; restore their corresponding engine shader assets for visual alignment review.
old={m.name:m for m in bpy.data.materials}
with bpy.data.libraries.load(str(R/'racing_car_08_export_ready.blend'),link=False) as (a,b):
 b.materials=[n for n in a.materials if n.endswith('_Engine')];b.objects=[n for n in a.objects if n.startswith(('Camera_','Studio_','Light_'))]
new={m.name.split('.00')[0]:m for m in b.materials if m}
for o in bpy.context.scene.objects:
 if o.type=='MESH':
  for slot in o.material_slots:
   if slot.material and slot.material.name in new:slot.material=new[slot.material.name]
for o in b.objects:
 if o:S.collection.objects.link(o)
for o in S.objects:
 if o.name.startswith('Collision_'):o.hide_render=True
S.world=bpy.data.worlds.new('Reimport QA World');S.world.use_nodes=True;S.world.node_tree.nodes['Background'].inputs[0].default_value=(.13,.16,.20,1);S.world.node_tree.nodes['Background'].inputs[1].default_value=.5
S.render.engine='CYCLES';S.cycles.samples=20;S.cycles.use_denoising=True;S.render.resolution_x=1600;S.render.resolution_y=900;S.render.resolution_percentage=100
for view,cam in [('front_3q','Camera_Presentation'),('rear_3q','Camera_Rear_ThreeQuarter'),('wheel','Camera_Wheel_Closeup')]:
 S.camera=bpy.data.objects[cam];S.render.filepath=str(R/'previews'/('fbx_reimport_'+view+'.png'));bpy.ops.render.render(write_still=True)
