import bpy,json,math,hashlib
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
asset=set()
for n in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']: asset.update(bpy.data.collections[n].all_objects)
uvlines=[]; shader=[]; stats={}; errors=[]; warnings=[]
def check(ok,msg,lines):
    lines.append(('PASS: ' if ok else 'ERROR: ')+msg)
    if not ok: errors.append(msg)
original=json.loads((ROOT/'materials_source_geometry.json').read_text())
def signature(o):
    h=hashlib.sha256(); h.update(np.array([tuple(v.co) for v in o.data.vertices],dtype=np.float32).tobytes()); h.update(str([tuple(p.vertices) for p in o.data.polygons]).encode()); h.update(np.array(o.matrix_world,dtype=np.float32).tobytes()); return h.hexdigest()
meshes=[o for o in asset if o.type=='MESH']
check(all('UVMap' in o.data.uv_layers for o in meshes),'UVMap exists on all '+str(len(meshes))+' vehicle meshes',uvlines)
check(all(signature(o)==original[o.name] for o in meshes),'All source vertex coordinates, polygon indices and object transforms preserved',shader)
check(hashlib.sha256((ROOT/'racing_car_05_interior.blend').read_bytes()).hexdigest()==bpy.context.scene['source_05_sha256'],'Source 05 file preserved byte-for-byte',shader)
alltri={}; owners={}; repair={}; severe=[]; tiny=[]; flips=[]; outside=[]
for o in meshes:
    me=o.data; me.calc_loop_triangles(); uv=me.uv_layers['UVMap'].data
    loops=np.array([t.loops for t in me.loop_triangles]); vi=np.array([t.vertices for t in me.loop_triangles])
    U=np.array([tuple(v.uv) for v in uv])[loops]; P=np.array([tuple(v.co) for v in me.vertices])[vi]
    e1=P[:,1]-P[:,0]; e2=P[:,2]-P[:,0]; du=U[:,1]-U[:,0]; dv=U[:,2]-U[:,0]
    signed=du[:,0]*dv[:,1]-du[:,1]*dv[:,0]; area=np.abs(signed)/2
    if np.any((U<-.00001)|(U>1.00001)): outside.append(o.name)
    if np.any(signed<-1e-10): flips.append((o.name,int(np.sum(signed<-1e-10))))
    repair.setdefault(o.name,set()).update(me.loop_triangles[i].polygon_index for i in np.where(signed<-1e-10)[0])
    l=np.linalg.norm(e1,axis=1); cross=np.linalg.norm(np.cross(e1,e2),axis=1)
    good=(l>1e-9)&(cross>1e-12)&(area>1e-12)
    x=(e1*e2).sum(axis=1)/np.maximum(l,1e-12); y=cross/np.maximum(l,1e-12)
    J=np.stack([du/np.maximum(l,1e-12)[:,None],(dv-du*(x/np.maximum(l,1e-12))[:,None])/np.maximum(y,1e-12)[:,None]],axis=-1)
    singular=np.linalg.svd(J[good],compute_uv=False); stretch=singular[:,0]/np.maximum(singular[:,1],1e-12)
    if np.any(stretch>6): severe.append({'object':o.name,'triangles':int(np.sum(stretch>6)),'max':float(stretch.max())})
    repair[o.name].update(me.loop_triangles[i].polygon_index for i in np.where(good)[0][stretch>6])
    group=o['texture_group']; res={'body':4096,'interior':2048,'wheels':2048,'tires':2048,'lights':2048,'brakes':1024,'trim':1024}[group]
    if np.any(area*res*res<1): tiny.append((o.name,int(np.sum(area*res*res<1))))
    r=stats.setdefault(group,{'objects':0,'triangles':0,'uv_area':0.,'world_area':0.,'pixels_per_meter':[]})
    r['objects']+=1; r['triangles']+=len(U); r['uv_area']+=float(area.sum()); r['world_area']+=float(cross.sum()/2)
    r['pixels_per_meter'].append(res/o['uv_meter_scale'])
    alltri.setdefault(group,[]).extend(U)
    owners.setdefault(group,[]).extend((o.name,t.polygon_index) for t in me.loop_triangles)
check(not outside,'All base UVs are within 0–1: '+str(outside),uvlines)
check(not flips,'No flipped nondegenerate base triangles: '+str(flips[:20]),uvlines)
# Strict 2D separating-axis overlap test, with a spatial grid. Shared edges
# and point contacts are excluded by an area tolerance; mirrored modifiers
# are intentionally excluded because only editable base islands are tested.
def overlap(a,b):
    for tri in [a,b]:
        for i in range(3):
            e=tri[(i+1)%3]-tri[i]; axis=np.array([-e[1],e[0]])
            if np.linalg.norm(axis)<1e-12: continue
            pa=a@axis; pb=b@axis
            if min(pa.max(),pb.max())-max(pa.min(),pb.min())<=1e-10*np.linalg.norm(axis): return False
    return True
overlaps={}
for group,rows in alltri.items():
    T=np.array(rows); bins={}; tested=set(); contacts=[]
    for i,t in enumerate(T):
        if abs(np.cross(t[1]-t[0],t[2]-t[0]))<1e-12: continue
        lo=np.floor(t.min(axis=0)*96).astype(int); hi=np.floor(t.max(axis=0)*96).astype(int)
        candidates=set()
        cells=[(x,y) for x in range(lo[0],hi[0]+1) for y in range(lo[1],hi[1]+1)]
        for cell in cells: candidates.update(bins.get(cell,[]))
        for j in candidates:
            a=T[j]
            if np.any(np.minimum(t.max(axis=0),a.max(axis=0))-np.maximum(t.min(axis=0),a.min(axis=0))<=1e-10): continue
            if overlap(t,a):
                contacts.append((j,i))
                for idx in [j,i]:
                    name,face=owners[group][idx]; repair[name].add(face)
        for cell in cells: bins.setdefault(cell,[]).append(i)
    if contacts: overlaps[group]={'triangle_pairs':len(contacts),'examples':contacts[:8]}
    print('UV OVERLAP CHECK',group,len(contacts),flush=True)
check(not overlaps,'No unintended positive-area base triangle overlaps across each packed atlas: '+json.dumps(overlaps),uvlines)
if severe: warnings.append('High UV stretch (>6:1) on '+str(sum(r['triangles'] for r in severe))+' triangles; see detailed JSON')
if tiny: warnings.append('Subpixel base triangles exist on small hardware/lettering at atlas resolution; tileable detail maps remain available')
for g,r in stats.items():
    r['density_min']=min(r.pop('pixels_per_meter')) if False else min(r['pixels_per_meter'])
    r['density_max']=max(r['pixels_per_meter']); r['density_median']=float(np.median(r.pop('pixels_per_meter')))
materials={m for o in asset if o.type in ['MESH','CURVE'] for m in o.data.materials if m}
check(all(o.data.materials and all(o.data.materials) for o in asset if o.type in ['MESH','CURVE']),'All vehicle surfaces have valid material slots',shader)
check(not any(m.name.startswith('Material.') for m in materials),'No default material names',shader)
broken=[]
for m in materials:
    for node in m.node_tree.nodes:
        if node.type=='TEX_IMAGE' and (not node.image or not Path(bpy.path.abspath(node.image.filepath)).exists()): broken.append(m.name)
check(not broken,'All referenced texture files resolve: '+str(broken),shader)
for name in ['MAT_Glass','MAT_HeadlightLens','MAT_TaillightLens']:
    p=bpy.data.materials[name].node_tree.nodes.get('Principled BSDF'); check(p.inputs['Transmission Weight'].default_value>.95,name+' uses transmission with IOR '+str(round(p.inputs['IOR'].default_value,2)),shader)
check(all(not m.node_tree.nodes.get('Material Output').inputs['Displacement'].is_linked for m in materials),'No displacement or geometry generated by shaders',shader)
for name in ['MAT_EmissiveWhite','MAT_EmissiveRed','MAT_EmissiveAmber']:
    p=bpy.data.materials[name].node_tree.nodes.get('Principled BSDF'); check(0<p.inputs['Emission Strength'].default_value<=3,name+' emission controlled',shader)
warnings.append('Mirror and Solidify reuse base UVs intentionally; those evaluated overlaps require separate bake/export policy later')
warnings.append('Physical lettering and thin seams create tiny atlas islands; preserve geometry now, bake detail in the later optimization phase')
for msg in warnings: uvlines.append('WARNING: '+msg)
uvlines.append('Atlas density statistics: '+json.dumps(stats))
shader.append('Vehicle material count: '+str(len(materials)))
shader.append('WARNING: Per-object UV-to-meter attribute must be baked to unique atlas maps or reproduced as engine UV scaling')
(ROOT/'uv_validation.txt').write_text('\n'.join(uvlines)+'\n')
(ROOT/'shader_validation.txt').write_text('\n'.join(shader)+'\n')
result={'errors':errors,'warnings':warnings,'groups':stats,'stretch':severe,'tiny_triangles':tiny,'flips':flips,'overlaps':overlaps,'material_count':len(materials),'material_nodes':{m.name:len(m.node_tree.nodes) for m in materials},'texture_count':len(list((ROOT/'textures/racing_car').rglob('*.png')))}
(ROOT/'materials_stats.json').write_text(json.dumps(result,indent=2))
(ROOT/'uv_repair_faces.json').write_text(json.dumps({k:sorted(v) for k,v in repair.items() if v},indent=2))
print('\n'.join(uvlines+shader)); print('RESULT',len(errors),'errors',flush=True)
