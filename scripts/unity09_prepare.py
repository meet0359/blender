import sys;sys.path.insert(0,'/Users/meetshah/Documents/blender/scripts')
from unity09_common import *
R='/Users/meetshah/Documents/blender/';O=bpy.data.objects;rep={}
L=lambda s:print(s,flush=True)
root=O['Car_Root']
# --- hierarchy: flatten LOD0 group under Car_Root, no transform changes (all identity, verified)
ren={'LOD0_Body':'Body_LOD0','LOD0_Interior':'Interior_LOD0','LOD0_Glass':'Glass_LOD0','LOD0_Lights':'Lights_LOD0','LOD0_Aero':'Aero_LOD0','LOD0_Brakes':'Brakes_LOD0'}
def reparent(o,p):
    mw=o.matrix_world.copy();o.parent=p;o.matrix_parent_inverse=p.matrix_world.inverted();o.matrix_world=mw
for old,new in ren.items():
    o=O[old];o.name=new;reparent(o,root)
for n in ['Wheel_FL_LOD0','Wheel_FR_LOD0','Wheel_RL_LOD0','Wheel_RR_LOD0','Steering_Wheel_LOD0']:reparent(O[n],root)
for n in ['Collision_Body','Collision_Front','Collision_Rear','Collision_Roof']:reparent(O[n],root)
lod0=O['LOD0'];assert not lod0.children,[c.name for c in lod0.children];bpy.data.objects.remove(lod0)
bpy.context.view_layer.update()
# --- transforms check (every exported object)
exp=[o for o in O if o.name.endswith('LOD0') and o.name!='LOD0']
exp=[o for o in exp if o.type=='MESH' or o.name in ren.values()]
bad=[o.name for o in exp if min(o.scale)<=0 or max(o.scale)-min(o.scale)>1e-6 or o.matrix_world.determinant()<=0]
rot=[o.name for o in exp if any(abs(x)>1e-6 for x in o.rotation_euler)]
rep['transforms']=dict(objects=len(exp),negative_or_nonuniform=bad,nonzero_rotation=rot)
L(f'transforms {rep["transforms"]}')
# --- wheel pivots: tire/rim bbox center vs origin
piv={}
for w in WH:
    wo=O[f'Wheel_{w}_LOD0'];t=[k for k in [wo]+list(wo.children_recursive) if k.type=='MESH' and (k is wo or k.name.startswith(('Rim_','Wheel_Spoke','Wheel_Hub')))]
    mn,mx=bbox([wo]);c=(mn+mx)/2;o=np.array(wo.matrix_world.translation)
    piv[w]=dict(origin=o.round(6).tolist(),tire_bbox_center_offset_mm=((c-o)*1e3).round(3).tolist(),radius=float((mx[2]-mn[2])/2),width=float(mx[0]-mn[0]))
    # hub center from Wheel_Hub (axle-aligned) 
    hb=O[f'Wheel_Hub_{w}_LOD0'];hmn,hmx=bbox([hb]);piv[w]['hub_center_offset_yz_mm']=(((hmn+hmx)/2-o)*1e3)[1:].round(3).tolist()
rep['pivots']=piv;L(json.dumps(piv))
# --- roll test + steering pivot test
rep['roll_source']=roll_test(lambda n:O[n],L,'src ')
st={}
for w in ['FL','FR']:
    wo=O[f'Wheel_{w}_LOD0'];meshes=[wo]+[c for c in wo.children_recursive if c.type=='MESH'];bpy.context.view_layer.update()
    b=[verts_world(m,7) for m in meshes];c0=np.array(wo.matrix_world.translation);rest=tuple(wo.rotation_euler);r={}
    for deg in (20,-20):
        wo.rotation_euler[2]=math.radians(deg);bpy.context.view_layer.update()
        n=[verts_world(m,7) for m in meshes];dz=max(float(np.abs(a[:,2]-x[:,2]).max()) for a,x in zip(b,n))
        dr=max(float(np.abs(np.hypot(a[:,0]-c0[0],a[:,1]-c0[1])-np.hypot(x[:,0]-c0[0],x[:,1]-c0[1])).max()) for a,x in zip(b,n))
        r[deg]=dict(height_shift_mm=dz*1e3,radius_about_Z_change_mm=dr*1e3,origin_shift_mm=float(np.abs(np.array(wo.matrix_world.translation)-c0).max())*1e3)
    wo.rotation_euler=rest;bpy.context.view_layer.update();st[w]=r
rep['steer_pivot_test']=st;L('steer '+json.dumps(st))
assert all(tuple(O[f'Wheel_{w}_LOD0'].rotation_euler)==(0,0,0) for w in WH)
# --- steering wheel axis
sw=O['Steering_Wheel_LOD0'];p=verts_world(sw);cen=p.mean(0);u,s,vt=np.linalg.svd(p-cen);ax=vt[2]
if ax[1]<0:ax=-ax
org=np.array(sw.matrix_world.translation);rel=org-cen;perp=rel-ax*rel.dot(ax)
hub=O['Steering_Hub_LOD0'];hp=verts_world(hub);hc=(hp.min(0)+hp.max(0))/2
hrel=org-hc;hperp=hrel-ax*hrel.dot(ax)
rep['steering']=dict(origin=org.tolist(),axis_pca_world=ax.round(4).tolist(),rim_centroid=cen.round(4).tolist(),origin_dist_to_rim_axis_mm=float(np.linalg.norm(perp))*1e3,origin_dist_to_hub_axis_mm=float(np.linalg.norm(hperp))*1e3,tilt_deg_from_Y=float(np.degrees(np.arccos(abs(ax[1])))))
L('steering '+json.dumps(rep['steering']))
# --- relative texture paths
nonrel=[i.filepath for i in bpy.data.images if i.filepath and not i.filepath.startswith('//') and i.source=='FILE']
rep['absolute_image_paths']=nonrel
rep['reference_world']={n:np.array(O[n].matrix_world.translation).round(6).tolist() for n in ['CenterOfMass']+[f'WheelColliderRef_{w}' for w in WH]}
json.dump(rep,open(R+'unity09_prepare.json','w'),indent=1,default=float)
bpy.ops.wm.save_as_mainfile(filepath=R+'racing_car_09_unity_export_ready.blend');L('PREP DONE')
