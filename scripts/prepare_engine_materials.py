import bpy,json,math
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];T=R/'textures/racing_car';G=T/'game';G.mkdir(exist_ok=True)
manifest=json.loads((R/'texture_manifest.json').read_text());materials={};notes={};cache={}
objs=list(bpy.data.collections['Car_LOD0'].all_objects)
def read(path,rgb=True):
 im=bpy.data.images.load(str(path),check_existing=True);arr=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(arr);arr=arr.reshape(im.size[1],im.size[0],4);out=arr[:,:,:3].copy() if rgb else arr[:,:,0].copy();im.buffers_free()
 if rgb and path.name.endswith('BaseColor.png'):out=np.where(out<=.04045,out/12.92,((out+.055)/1.055)**2.4)
 return out

def save(name,arr,color=False):
 if color:arr=np.where(arr<=.0031308,arr*12.92,1.055*np.power(np.maximum(arr,0),1/2.4)-.055)
 h,w=arr.shape[:2];a=np.ones((h,w,4),dtype=np.float32)
 if arr.ndim==2:a[:,:,:3]=arr[:,:,None]
 else:a[:,:,:3]=arr
 im=bpy.data.images.new(name,w,h,alpha=False);im.colorspace_settings.name='sRGB' if color else 'Non-Color';im.pixels.foreach_set(a.ravel());im.filepath_raw=str(G/(name+'.png'));im.file_format='PNG';im.save();bpy.data.images.remove(im);return G/(name+'.png')

def image(path,color=False):
 im=bpy.data.images.load(str(path),check_existing=True);im.colorspace_settings.name='sRGB' if color else 'Non-Color';im.filepath='//'+str(path.relative_to(R));return im

def sample(arr,u,v):
 h,w=arr.shape[:2];x=(u*w-.5)%w;y=(v*h-.5)%h;x0=np.floor(x).astype(int);y0=np.floor(y).astype(int);x1=(x0+1)%w;y1=(y0+1)%h;fx=x-x0;fy=y-y0
 if arr.ndim==3:fx=fx[...,None];fy=fy[...,None]
 return (arr[y0,x0]*(1-fx)+arr[y0,x1]*fx)*(1-fy)+(arr[y1,x0]*(1-fx)+arr[y1,x1]*fx)*fy
# Original maps remain untouched. R/G/B packing is literal data, not color transformed.
orm={}
for key,d in manifest.items():
 if key.startswith('atlas_'):continue
 ao=read(R/d['maps']['AO'],False);rough=read(R/d['maps']['Roughness'],False);metal=read(R/d['maps']['Metallic'],False)
 path=save(key+'_ORM',np.stack([ao,rough,metal],-1));orm[key]=path;print('ORM',key,flush=True)
# For each detail material, bake the existing micro + detail normal arithmetic into one atlas.
def atlas_normal(m,key):
 tile=read(R/manifest[key]['maps']['Normal']);detail=read(T/('tires' if key=='rubber' else 'interior')/'lod_detail_Normal.png');res=4096
 own=[o for o in objs if any(s.material==m for s in o.material_slots)];coef=float(np.median([o.get('uv_meter_scale',1)/m['tile_m'] for o in own]));out=np.empty((res,res,3),dtype=np.float32)
 for y in range(0,res,128):
  u=np.arange(res,dtype=np.float32)[None,:]/res+.5/res;v=np.arange(y,min(res,y+128),dtype=np.float32)[:,None]/res+.5/res
  out[y:y+128]=sample(tile,u*coef,v*coef)+detail[y:y+128]-np.array([.5,.5,1],dtype=np.float32)
 # Refine each object's chart using its exact stored meter scale. Uniform mirrored UV reuse is intentional.
 for o in own:
  exact=float(o.get('uv_meter_scale',1)/m['tile_m'])
  if abs(exact-coef)<1e-5:continue
  me=o.data;me.calc_loop_triangles();uv=me.uv_layers['UVMap'].data
  for tri in me.loop_triangles:
   if me.materials[me.polygons[tri.polygon_index].material_index]!=m:continue
   p=np.array([tuple(uv[i].uv) for i in tri.loops],dtype=np.float32)*res
   x0=max(0,int(np.floor(p[:,0].min())));x1=min(res,int(np.ceil(p[:,0].max())));y0=max(0,int(np.floor(p[:,1].min())));y1=min(res,int(np.ceil(p[:,1].max())))
   if x1<=x0 or y1<=y0:continue
   xx=np.arange(x0,x1,dtype=np.float32)[None,:]+.5;yy=np.arange(y0,y1,dtype=np.float32)[:,None]+.5
   a=p[1]-p[0];b=p[2]-p[0];det=a[0]*b[1]-a[1]*b[0]
   if abs(det)<1e-8:continue
   s=((xx-p[0,0])*b[1]-(yy-p[0,1])*b[0])/det;t=(a[0]*(yy-p[0,1])-a[1]*(xx-p[0,0]))/det;mask=(s>=-1e-5)&(t>=-1e-5)&(s+t<=1.00001)
   val=sample(tile,xx/res*exact,yy/res*exact)+detail[y0:y1,x0:x1]-np.array([.5,.5,1],dtype=np.float32);part=out[y0:y1,x0:x1];part[mask]=val[mask]
 return save(m.name+'_Normal',np.clip(out,0,1))

def tire_atlases(m):
 d=manifest['rubber'];base=read(R/d['maps']['BaseColor']);rough=read(R/d['maps']['Roughness'],False);metal=read(R/d['maps']['Metallic'],False);ao=read(T/'tires/lod_detail_AO.png',False);mask=read(T/'tires/lod_detail_Mask.png',False);res=4096
 own=[o for o in objs if any(s.material==m for s in o.material_slots)];coef=float(np.median([o['uv_meter_scale']/m['tile_m'] for o in own]));color=np.empty((res,res,3),np.float32);packed=np.empty((res,res,3),np.float32)
 for y in range(0,res,128):
  u=(np.arange(res,dtype=np.float32)[None,:]+.5)/res;v=(np.arange(y,min(res,y+128),dtype=np.float32)[:,None]+.5)/res;bm=sample(base,u*coef,v*coef);mk=mask[y:y+128,None] if False else mask[y:y+128,:,None]
  color[y:y+128]=bm*(1-mk)+np.array([.07,.073,.078],np.float32)*mk;packed[y:y+128,:,0]=ao[y:y+128];packed[y:y+128,:,1]=sample(rough,u*coef,v*coef);packed[y:y+128,:,2]=sample(metal,u*coef,v*coef)
 return save('tire_BaseColor',color,True),save('tire_ORM',packed)
# Explicit glTF AO input node. Cycles lighting is not double-multiplied by AO.
group=bpy.data.node_groups.get('glTF Material Output') or bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree')
if not group.interface.items_tree:group.interface.new_socket(name='Occlusion',in_out='INPUT',socket_type='NodeSocketFloat')
used=sorted({s.material for o in objs for s in o.material_slots},key=lambda m:m.name)
for src in used:
 key=src.get('texture_set');oldbs=next((n for n in src.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
 vals={i.name:tuple(i.default_value) if hasattr(i.default_value,'__len__') else i.default_value for i in oldbs.inputs if hasattr(i,'default_value')} if oldbs else {}
 m=bpy.data.materials.new(src.name+'_Engine');m.use_nodes=True;m.diffuse_color=src.diffuse_color;ns=m.node_tree.nodes;ns.clear();lk=m.node_tree.links;bs=ns.new('ShaderNodeBsdfPrincipled');out=ns.new('ShaderNodeOutputMaterial');lk.new(bs.outputs[0],out.inputs[0])
 for name,val in vals.items():
  if name in bs.inputs and name!='Normal':
   try:bs.inputs[name].default_value=val
   except:pass
 uv=ns.new('ShaderNodeUVMap');uv.uv_map='UV_Game';atlas=ns.new('ShaderNodeUVMap');atlas.uv_map='UVMap';radial=ns.new('ShaderNodeUVMap');radial.uv_map='UV_Rotor'
 info={'source_material':src.name,'texture_set':key,'uv_tile_channel':'UV_Game','detail_channel':'UVMap','rotor_channel':'UV_Rotor','attributes_required':[],'images':{}}
 def tex(path,color,coord):
  n=ns.new('ShaderNodeTexImage');n.image=image(path,color);lk.new(coord.outputs[0],n.inputs['Vector']);info['images'][path.stem]='//'+str(path.relative_to(R));return n
 if key:
  d=manifest[key];tint=next((tuple(n.inputs[2].default_value)[:3] for n in src.node_tree.nodes if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY'),(1,1,1))
  basepath=R/d['maps']['BaseColor'];ormpath=orm[key];normalpath=R/d['maps']['Normal'];baseuv=radial if src.name=='MAT_BrakeDisc' else uv;ormuv=baseuv;normaluv=uv
  if tint!=(1,1,1):basepath=save(src.name+'_BaseColor',read(basepath)*np.array(tint,np.float32),True)
  if src.name=='MAT_Tire_LOD_Detail':basepath,ormpath=tire_atlases(src);baseuv=atlas;ormuv=atlas
  if src.name.endswith('_LOD_Detail'):normalpath=atlas_normal(src,key);normaluv=atlas
  n=tex(basepath,True,baseuv);lk.new(n.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Base Color'].default_value=(1,1,1,1)
  n=tex(ormpath,False,ormuv);sep=ns.new('ShaderNodeSeparateColor');lk.new(n.outputs['Color'],sep.inputs[0]);lk.new(sep.outputs['Green'],bs.inputs['Roughness']);lk.new(sep.outputs['Blue'],bs.inputs['Metallic']);ao=ns.new('ShaderNodeGroup');ao.node_tree=group;lk.new(sep.outputs['Red'],ao.inputs['Occlusion'])
  n=tex(normalpath,False,normaluv);normal=ns.new('ShaderNodeNormalMap');normal.uv_map=normaluv.uv_map;original=next((n for n in src.node_tree.nodes if n.type=='NORMAL_MAP'),None);normal.inputs['Strength'].default_value=original.inputs['Strength'].default_value if original else .3;lk.new(n.outputs['Color'],normal.inputs['Color']);lk.new(normal.outputs[0],bs.inputs['Normal'])
 elif src.name.endswith('_LOD_Detail'):
  path=T/'interior/lod_detail_Normal.png';n=tex(path,False,atlas);normal=ns.new('ShaderNodeNormalMap');normal.uv_map='UVMap';lk.new(n.outputs[0],normal.inputs[1]);lk.new(normal.outputs[0],bs.inputs['Normal'])
 if src.name=='MAT_Glass_LOD_Thin':
  bs.inputs['Base Color'].default_value=(.83,.91,.95,1);bs.inputs['Roughness'].default_value=.025;bs.inputs['Metallic'].default_value=0;bs.inputs['Transmission Weight'].default_value=1;bs.inputs['IOR'].default_value=1.46;bs.inputs['Alpha'].default_value=.18;m.surface_render_method='DITHERED'
  info['glass']={'tint_linear':[.83,.91,.95],'roughness':.025,'alpha':.18,'transmission':1,'ior':1.46,'note':'Portable Principled approximation. Recreate original thin Fresnel reflection/straight-through model in the target engine; FBX transparency is approximate.'}
 if src.name.startswith('MAT_Emissive') or src.name.startswith('MAT_Display'):info['emission']={'color_linear':list(bs.inputs['Emission Color'].default_value)[:3],'strength':bs.inputs['Emission Strength'].default_value}
 materials[src]=m;notes[m.name]=info;print('ENGINE MATERIAL',src.name,flush=True)
for lod in range(4):
 for o in bpy.data.collections['Car_LOD'+str(lod)].all_objects:
  for slot in o.material_slots:slot.material=materials[slot.material]
(R/'engine_material_manifest.json').write_text(json.dumps(notes,indent=2));(R/'orm_manifest.json').write_text(json.dumps({k:'//'+str(p.relative_to(R)) for k,p in orm.items()},indent=2))
bpy.context.scene['engine_material_policy']='UV_Game realizes physical tiling; UV_Rotor realizes radial wear; UVMap retains atlas detail. No shader object attributes remain in production materials.'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_08_export_ready.blend'));print('ENGINE MATERIALS COMPLETE',flush=True)
