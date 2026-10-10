import bpy,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=24;S.cycles.use_denoising=True;S.render.resolution_x=1920;S.render.resolution_y=1080;S.render.resolution_percentage=100
review='--review' in sys.argv
if review:S.render.resolution_percentage=50;S.cycles.samples=12
cols=[bpy.data.collections['Car_LOD'+str(i)] for i in range(4)];master=bpy.data.collections['REFERENCE_Master_06'];master.hide_render=True
cam=bpy.data.objects.get('Camera_LOD0_ThroughGlass')
if not cam:
 cam=bpy.data.objects.new('Camera_LOD0_ThroughGlass',bpy.data.cameras.new('Camera_LOD0_ThroughGlass'));bpy.data.collections['PRESENTATION'].objects.link(cam)
cam.location=(1.8,-.78,1.28);target=Vector((-.24,-.13,.73));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=55;cam.data.clip_start=.01
views=[(0,'front_3q','Camera_Presentation'),(0,'rear_3q','Camera_Rear_ThreeQuarter'),(0,'side','Camera_Side'),(0,'wheel','Camera_Wheel_Closeup'),(0,'cockpit','Camera_LOD0_ThroughGlass')]
for i,dist in [(1,14),(2,28),(3,60)]:
 name='Camera_LOD'+str(i)+'_Distance';cam=bpy.data.objects.get(name)
 if not cam:
  cam=bpy.data.objects.new(name,bpy.data.cameras.new(name));bpy.data.collections['PRESENTATION'].objects.link(cam)
 target=Vector((0,0,.6));direction=Vector((.65,-.73,.20)).normalized();cam.location=target+direction*dist;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=50;cam['review_distance_m']=dist
 views.append((i,'distance',name))
if '--only' in sys.argv:
 wanted=sys.argv[sys.argv.index('--only')+1].split(',');views=[v for v in views if 'lod'+str(v[0])+'_'+v[1] in wanted]
for lod,key,cam in views:
 for i,c in enumerate(cols):c.hide_render=i!=lod;c.hide_viewport=i!=lod
 S.camera=bpy.data.objects[cam];name='lod'+str(lod)+'_'+key;S.render.filepath=str(R/'previews'/((('review_' if review else '')+name)+'.png'));print('RENDER',name,flush=True);bpy.ops.render.render(write_still=True)
for i,c in enumerate(cols):c.hide_render=i!=0;c.hide_viewport=i!=0
S.camera=bpy.data.objects['Camera_Presentation'];S.render.resolution_percentage=100
if '--save' in sys.argv:bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
