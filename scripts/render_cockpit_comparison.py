import bpy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=24;S.cycles.use_denoising=True;S.render.resolution_x=1920;S.render.resolution_y=1080;S.render.resolution_percentage=100
for o in bpy.data.objects:
 if o.type=='LIGHT':o.visible_glossy=False
fill=bpy.data.objects.new('QA_CockpitFill',bpy.data.lights.new('QA_CockpitFill','AREA'));S.collection.objects.link(fill);fill.location=(0,-.05,1.08);fill.data.energy=20;fill.data.size=.6;fill.rotation_euler=(Vector((0,-.4,.5))-fill.location).to_track_quat('-Z','Y').to_euler();fill.visible_glossy=False
master=bpy.data.collections['REFERENCE_Master_06'];cols=[bpy.data.collections['Car_LOD'+str(i)] for i in range(4)]
for mode in ['master','lod0']:
 master.hide_render=mode!='master';master.hide_viewport=mode!='master'
 for i,c in enumerate(cols):c.hide_render=mode!='lod0' or i!=0;c.hide_viewport=c.hide_render
 S.camera=bpy.data.objects['Camera_LOD0_ThroughGlass'];S.render.filepath=str(R/'previews'/('master_cockpit_through_glass.png' if mode=='master' else 'lod0_cockpit.png'));print('COCKPIT',mode,flush=True);bpy.ops.render.render(write_still=True)
# Read-only preview process: QA light settings are not saved.
