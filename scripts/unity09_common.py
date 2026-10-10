import bpy,math,json
import mathutils as mu
import numpy as np
WH=['FL','FR','RL','RR']
def wmat(o): return o.matrix_world
def verts_world(o,step=1):
    M=np.array(o.matrix_world);co=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',co);co=co.reshape(-1,3)[::step]
    return co@M[:3,:3].T+M[:3,3]
def bbox(objs):
    pts=np.vstack([verts_world(o) for o in objs]);return pts.min(0),pts.max(0)
def roll_test(get,log,tag='',axis_name='x'):
    """get(name)->object. Rotate each wheel +-30 deg on local X; verify pivots, axis, fixed calipers."""
    res={}
    cal=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Caliper') and o.name.endswith('LOD0') and (o.parent is None or not o.parent.name.startswith('Wheel'))]
    for w in WH:
        wo=get(f'Wheel_{w}_LOD0');kids=[wo]+list(wo.children_recursive);meshes=[k for k in kids if k.type=='MESH']
        bpy.context.view_layer.update()
        base=[verts_world(m,7) for m in meshes];cbase=[verts_world(c,3) for c in cal if c.name.split('_')[-2]==w]
        c0=np.array(wo.matrix_world.translation);rest=tuple(wo.rotation_euler)
        out={}
        for deg in (30,-30):
            wo.rotation_euler[0]=rest[0]+math.radians(deg);bpy.context.view_layer.update()
            now=[verts_world(m,7) for m in meshes]
            dx=max(float(np.abs(a[:,0]-b[:,0]).max()) for a,b in zip(base,now))
            dr=0;ang=[]
            for a,b in zip(base,now):
                ra=np.hypot(a[:,1]-c0[1],a[:,2]-c0[2]);rb=np.hypot(b[:,1]-c0[1],b[:,2]-c0[2]);dr=max(dr,float(np.abs(ra-rb).max()))
                m=ra>0.05;aa=np.arctan2(b[m,2]-c0[2],b[m,1]-c0[1])-np.arctan2(a[m,2]-c0[2],a[m,1]-c0[1]);aa=(aa+np.pi)%(2*np.pi)-np.pi;ang+=list(np.degrees(aa))
            cn=[verts_world(c,3) for c in cal if c.name.split('_')[-2]==w]
            dc=max((float(np.abs(a-b).max()) for a,b in zip(cbase,cn)),default=0)
            out[deg]=dict(axle_x_shift_mm=dx*1e3,radius_change_mm=dr*1e3,mean_angle_deg=float(np.mean(ang)),angle_spread_deg=float(np.ptp(ang)) if ang else 0,caliper_shift_mm=dc*1e3,origin_shift_mm=float(np.abs(np.array(wo.matrix_world.translation)-c0).max())*1e3,calipers=len(cbase))
        wo.rotation_euler=rest;bpy.context.view_layer.update()
        res[w]=out;log(f'{tag}roll {w}: '+json.dumps(out))
    return res
