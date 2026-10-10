import sys,os;sys.path.insert(0,'/Users/meetshah/Documents/blender/scripts')
from unity09_common import *
T=os.environ['TMPDIR'];fbx=sys.argv[sys.argv.index('--')+1];tag=sys.argv[sys.argv.index('--')+2];O=bpy.data.objects
L=lambda s:print(s,flush=True)
bpy.ops.wm.read_factory_settings(use_empty=True);O=bpy.data.objects
RAW=tag=='true';C=np.array([[1,0,0],[0,0,1],[0,-1,0]],np.float32)  # Blender->file Y-up (x,z,-y)
bpy.ops.import_scene.fbx(filepath=fbx,axis_forward='-Y' if RAW else '-Z',axis_up='Z' if RAW else 'Y',global_scale=1.0)
bpy.context.view_layer.update()
meta=json.load(open(T+'/unity09_srcmeta.json'));src=np.load(T+'/unity09_src.npz');prep=json.load(open('/Users/meetshah/Documents/blender/unity09_prepare.json'))
rep={'fbx':fbx}
# names / hierarchy
missing=[n for n in meta if n not in O];extra=[o.name for o in O if o.name not in meta]
badpar=[n for n,m in meta.items() if n in O and (O[n].parent.name if O[n].parent else None)!=m['parent']]
rep['hierarchy']=dict(expected=len(meta),imported=len(O),missing=missing[:10],extra=extra[:10],wrong_parent=badpar[:10])
rep['root']=dict(rot=[round(math.degrees(x),4) for x in O['Car_Root'].rotation_euler],scale=list(map(lambda x:round(x,5),O['Car_Root'].scale)),loc=list(O['Car_Root'].location))
# materials / uv
ms=[];uvb=[];msh=[o for o in O if o.type=='MESH']
for o in msh:
    m=meta[o.name];nm=[x.name if x else None for x in o.data.materials]
    if [n.split('.')[0] if n else n for n in nm]!=m['mats']:ms.append((o.name,m['mats'][:2],nm[:2]))
    if [u.name for u in o.data.uv_layers]!=m['uv']:uvb.append((o.name,m['uv'],[u.name for u in o.data.uv_layers]))
rep['materials']=dict(meshes=len(msh),mismatch=len(ms),examples=ms[:3],slots_total=sum(len(o.data.materials) for o in msh))
rep['uv_layers']=dict(mismatch=len(uvb),examples=uvb[:3])
# dimensions: render LOD0 meshes (exclude collision/refs)
rm=[o for o in msh if o.name.endswith('LOD0')]
mn,mx=bbox(rm);d=mx-mn
sp=np.vstack([src[k].reshape(-1,3) for k in src.files if k.endswith('|pos')]);sp=sp@C.T if RAW else sp;sd=sp.max(0)-sp.min(0)
rep['dims_m']=dict(src=sd.round(6).tolist(),fbx=d.round(6).tolist(),diff_mm=((d-sd)*1e3).round(4).tolist())
rep['bbox_min_diff_mm']=((mn-sp.min(0))*1e3).round(4).tolist()
# wheels
w={}
for k in WH:
    wo=O[f'Wheel_{k}_LOD0'];o=np.array(wo.matrix_world.translation);mnw,mxw=bbox([wo]);c=(mnw+mxw)/2;s=np.array(prep['pivots'][k]['origin']);s=C@s if RAW else s
    w[k]=dict(origin=o.round(6).tolist(),err_mm=float(np.abs(o-s).max())*1e3,tire_center_offset_mm=((c-o)*1e3).round(3).tolist())
fl=np.array(O['Wheel_FL_LOD0'].matrix_world.translation);rl=np.array(O['Wheel_RL_LOD0'].matrix_world.translation)
rep['wheels']=w;ax=2 if RAW else 1;rep['wheelbase_m']=dict(src=2.7,fbx=float(abs(rl[ax]-fl[ax])),fbx_RR_FR=float(abs(O['Wheel_RR_LOD0'].matrix_world.translation[ax]-O['Wheel_FR_LOD0'].matrix_world.translation[ax])))
rep['refs']={n:dict(world=np.array(O[n].matrix_world.translation).round(6).tolist(),err_mm=float(np.abs(np.array(O[n].matrix_world.translation)-(C@np.array(prep['reference_world'][n]) if RAW else np.array(prep['reference_world'][n]))).max())*1e3) for n in prep['reference_world']}
rep['child_rotations_nonzero']=[o.name for o in O if o.name!='Car_Root' and any(abs(x)>1e-5 for x in o.rotation_euler)][:10];rep['roll']=roll_test(lambda n:O[n],L,'fbx ')
# shading/uv compare per object
def cmp(name):
    o=O[name];me=o.data;n=len(me.loops)
    if n%3 or n//3!=len(src[name+'|mat']):return dict(error=f'tri count {n//3} vs {len(src[name+"|mat"])}')
    M=np.array(o.matrix_world);v=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',v);vi=np.empty(n,np.int32);me.loops.foreach_get('vertex_index',vi)
    pos=(v.reshape(-1,3)[vi]@M[:3,:3].T+M[:3,3]).reshape(-1,3,3);nr=(np.array([l.vector for l in me.corner_normals],np.float32)@M[:3,:3].T).reshape(-1,3,3)
    uv=np.empty(n*2,np.float32);me.uv_layers[0].data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2)
    sp_,sn,su=src[name+'|pos'],src[name+'|nrm'],src[name+'|uv']
    if RAW:sp_=sp_@C.T;sn=sn@C.T
    # per corner nearest match inside triangle
    dd=np.linalg.norm(pos[:,:,None,:]-sp_[:,None,:,:],axis=3);j=dd.argmin(2)
    r=np.arange(len(pos))[:,None]
    pe=dd.min(2).max();ni=np.take_along_axis(sn,j[:,:,None],1)
    nd=np.degrees(np.arccos(np.clip((nr*ni).sum(2)/np.maximum(np.linalg.norm(nr,axis=2)*np.linalg.norm(ni,axis=2),1e-9),-1,1)))
    ui=np.take_along_axis(su,j[:,:,None],1);ue=np.abs(uv-ui).max()
    mi=np.array([p.material_index for p in me.polygons]);
    # geometric flip: normal vs face normal
    fn=np.cross(pos[:,1]-pos[:,0],pos[:,2]-pos[:,0]);flip=float(((nr*fn[:,None,:]).sum(2)<0).mean())
    sfn=np.cross(sp_[:,1]-sp_[:,0],sp_[:,2]-sp_[:,0]);sflip=float(((sn*sfn[:,None,:]).sum(2)<0).mean())
    return dict(tris=len(pos),pos_err_mm=float(pe)*1e3,nrm_max_deg=float(nd.max()),nrm_mean_deg=float(nd.mean()),uv_err=float(ue),mat_mismatch=int((mi!=src[name+'|mat']).sum()),flip_frac=flip,src_flip_frac=sflip)
res={}
for n in [k.split('|')[0] for k in src.files if k.endswith('|mat')]:
    if n in O and O[n].type=='MESH':res[n]=cmp(n)
bad=[n for n,r in res.items() if 'error' in r]
ok={n:r for n,r in res.items() if 'error' not in r}
agg=lambda k,f=max:f(r[k] for r in ok.values())
rep['compare']=dict(objects=len(ok),errors=bad[:10],pos_err_mm_max=agg('pos_err_mm'),nrm_max_deg=agg('nrm_max_deg'),nrm_mean_deg_max=agg('nrm_mean_deg'),uv_err_max=agg('uv_err'),mat_mismatch=sum(r['mat_mismatch'] for r in ok.values()),flip_frac_max=agg('flip_frac'),src_flip_frac_max=agg('src_flip_frac'))
rep['worst_normals']=sorted(((r['nrm_max_deg'],n) for n,r in ok.items()),reverse=True)[:5]
keys=['hood','roof','fender','arch','door','headlight','shoulder','wheel_fl','tire']
focus={}
for n,r in ok.items():
    for k in keys:
        if k in n.lower():focus.setdefault(k,[]).append((n,r['nrm_max_deg'],r['flip_frac']));break
rep['shading_focus']={k:dict(n=len(v),max_normal_deg=max(x[1] for x in v),max_flip=max(x[2] for x in v),names=[x[0] for x in v][:4]) for k,v in focus.items()}
json.dump(rep,open(f'{T}/val_{tag}.json','w'),indent=1,default=float)
L('VALIDATION '+tag+' '+json.dumps({k:rep[k] for k in ['hierarchy','root','materials','uv_layers','dims_m','wheelbase_m','compare']},default=float))
if tag=='final':
    bpy.ops.wm.save_as_mainfile(filepath='/Users/meetshah/Documents/blender/exports/validation_unity_test.blend')
