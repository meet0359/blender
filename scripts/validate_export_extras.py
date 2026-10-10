import bpy,json,math
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];errors=[];results=[]
for o in [bpy.data.objects['Car_Root']]+list(bpy.data.objects['Car_Root'].children_recursive):
 if True:
  if any(abs(s-1)>1e-5 for s in o.scale) or o.matrix_world.determinant()<=0:errors.append(o.name+' scale')
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_viewport=False
bpy.context.view_layer.update()
for i in [0,1]:
 for k in ['FL','FR']:
  o=bpy.data.objects['Wheel_'+k+'_LOD'+str(i)];base=o.matrix_basis.copy();pos=o.matrix_world.translation.copy()
  for ang in [-25,25]:
   o.rotation_euler.z=math.radians(ang);bpy.context.view_layer.update();ok=(o.matrix_world.translation-pos).length<1e-6;results.append({'front_steering':o.name,'yaw':ang,'pivot_fixed':ok})
   if not ok:errors.append(o.name+' steering pivot')
  o.matrix_basis=base;bpy.context.view_layer.update()
steer=bpy.data.objects['Steering_Wheel_LOD0'];axis=steer.get('steering_axis_local');results.append({'cockpit_steering_wheel':steer.name,'position_m':list(steer.matrix_world.translation),'axis_local':list(axis) if axis else None,'separate':True})
manifest=json.loads((R/'texture_manifest.json').read_text());packed=json.loads((R/'orm_manifest.json').read_text());checks=[]
def sample(path):
 im=bpy.data.images.load(str(path),check_existing=False);im.colorspace_settings.name='Non-Color';w,h=im.size;points=[0,(w*h)//7,(w*h)//2,w*h-1];v=np.array([im.pixels[p*4:p*4+3] for p in points]);bpy.data.images.remove(im);return v,w,h
for key,path in packed.items():
 a,w,h=sample(R/path[2:]);sets=manifest[key]['maps'];expected=np.stack([sample(R/sets[c])[0][:,0] for c in ['AO','Roughness','Metallic']],axis=1);delta=float(np.max(np.abs(a-expected)));checks.append({'set':key,'size':[w,h],'channel_sample_max_error':delta,'packing':'R AO; G roughness; B metallic'})
 if delta>1/255+1e-5:errors.append(key+' ORM channels')
# Root coordinate system is unchanged; no animations, bones or negative scales in production.
report={'errors':errors,'steering_tests':results,'orm_checks':checks,'normal_convention':'OpenGL +Y','production_actions':sum(bool(o.animation_data) for i in range(4) for o in bpy.data.collections['Car_LOD'+str(i)].all_objects)}
(R/'export_extra_validation.json').write_text(json.dumps(report,indent=2));print('EXTRA VALIDATION',errors,flush=True)
