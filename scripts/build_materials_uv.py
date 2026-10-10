import bpy,bmesh,math,json,hashlib,time
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; TEX=ROOT/'textures/racing_car'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'racing_car_05_interior.blend'))
s=bpy.context.scene
s['source_05_sha256']=hashlib.sha256((ROOT/'racing_car_05_interior.blend').read_bytes()).hexdigest()
asset=set()
for name in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']: asset.update(bpy.data.collections[name].all_objects)
def signature(o):
    h=hashlib.sha256()
    h.update(np.array([tuple(v.co) for v in o.data.vertices],dtype=np.float32).tobytes())
    h.update(str([tuple(p.vertices) for p in o.data.polygons]).encode())
    h.update(np.array(o.matrix_world,dtype=np.float32).tobytes())
    return h.hexdigest()
source_geometry={o.name:signature(o) for o in asset if o.type=='MESH'}
(ROOT/'materials_source_geometry.json').write_text(json.dumps(source_geometry,indent=2))
def category(o):
    cs={c.name for c in o.users_collection}
    if any(c.startswith('INTERIOR') for c in cs): return 'interior'
    if 'WHEELS' in cs: return 'tires' if o.name.startswith(('Wheel_','Tire_')) and o.type=='MESH' else 'wheels'
    if 'BRAKES' in cs: return 'brakes'
    if cs&{'LIGHTS','GLASS'}: return 'lights'
    if any(m and m.name=='MAT_CarPaint' for m in o.data.materials): return 'body'
    return 'trim'
groups={n:[] for n in ['body','interior','wheels','tires','lights','brakes','trim']}
for o in asset:
    if o.type=='MESH': groups[category(o)].append(o)
for group,objs in groups.items():
    print('UV ATLAS',group,len(objs),flush=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
        while len(o.data.uv_layers): o.data.uv_layers.remove(o.data.uv_layers[0])
        o.data.uv_layers.new(name='UVMap'); o['texture_group']=group
    bpy.context.view_layer.objects.active=objs[0]
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(72 if group=='body' else 66),island_margin=.003,area_weight=.35,correct_aspect=True,scale_to_bounds=False)
    bpy.ops.uv.average_islands_scale()
    bpy.ops.uv.pack_islands(rotate=True,margin=.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    for o in objs:
        me=o.data; me.calc_loop_triangles(); uv=me.uv_layers.active.data
        a3=sum(p.area for p in me.polygons); a2=0
        for tri in me.loop_triangles:
            a,b,c=[uv[i].uv for i in tri.loops]
            a2+=abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))*.5
        o['uv_meter_scale']=math.sqrt(a3/max(a2,1e-12))
        o['uv_overlap_policy']='Unique base islands within group atlas; live Mirror/Solidify reuse UVs intentionally'
        # Persist unwrap discontinuities as logical seam edges.
        bm=bmesh.new(); bm.from_mesh(me); layer=bm.loops.layers.uv.active
        for edge in bm.edges:
            if len(edge.link_loops)==2:
                a,b=edge.link_loops
                aa={l.vert.index:tuple(l[layer].uv) for l in [a,a.link_loop_next]}
                bb={l.vert.index:tuple(l[layer].uv) for l in [b,b.link_loop_next]}
                edge.seam=any(np.linalg.norm(np.array(aa[k])-np.array(bb[k]))>1e-5 for k in aa)
        bm.to_mesh(me); bm.free()

# Tileable PBR image library. Authored inside Blender; no geometry microdetail.
sets={
'paint':('body',4096,(.24,.006,.014),.27,1,'paint',.20),
'carbon':('trim',1024,(.018,.022,.026),.32,.48,'carbon',.128),
'plastic':('trim',1024,(.012,.016,.022),.49,0,'grain',.16),
'chrome':('trim',1024,(.62,.67,.72),.16,1,'metal',.16),
'metal':('wheels',2048,(.32,.36,.40),.28,1,'metal',.20),
'rubber':('tires',2048,(.021,.024,.028),.78,0,'grain',.18),
'rotor':('brakes',1024,(.35,.37,.39),.43,1,'metal',.12),
'caliper':('brakes',1024,(.62,.22,.008),.29,.62,'paint',.15),
'leather':('interior',2048,(.015,.02,.026),.43,0,'leather',.16),
'alcantara':('interior',2048,(.029,.035,.043),.83,0,'grain',.10),
'speaker':('interior',1024,(.011,.015,.019),.65,.1,'speaker',.096),
'lens':('lights',2048,(.94,.97,1),.035,0,'lens',.25)}
images={}; manifest={}
def save_image(path,rgb,noncolor=True):
    h,w=rgb.shape[:2]; a=np.ones((h,w,4),dtype=np.float32)
    a[:,:,:3]=rgb if rgb.ndim==3 else rgb[:,:,None]
    im=bpy.data.images.new(path.stem,w,h,alpha=False,float_buffer=False)
    im.colorspace_settings.name='Non-Color'
    im.pixels.foreach_set(a.reshape(-1)); im.filepath_raw=str(path); im.file_format='PNG'; im.save()
    im.colorspace_settings.name='Non-Color' if noncolor else 'sRGB'
    im.filepath='//'+str(path.relative_to(ROOT))
    return im
for key,(folder,res,color,rough,metal,kind,meters) in sets.items():
    print('TEXTURE SET',key,res,flush=True)
    directory=TEX/folder; directory.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(317+sum(map(ord,key)))
    Y,X=np.mgrid[0:res,0:res].astype(np.float32)/res
    noise=rng.random((res,res),dtype=np.float32)-.5
    fine=(noise+np.roll(noise,1,0)+np.roll(noise,1,1))/3
    if kind=='carbon':
        a=np.floor(X*32).astype(int); b=np.floor(Y*32).astype(int)
        weave=((a+b)%4<2)
        ht=np.where(weave,np.sin(2*np.pi*X*32),np.sin(2*np.pi*Y*32))*.25
        ht+=np.where(weave,np.sin(2*np.pi*X*256),np.sin(2*np.pi*Y*256))*.07
        tint=1+ht*.3; variation=ht*.04
    elif kind=='speaker':
        xx=(X*24)%1-.5; yy=(Y*24)%1-.5
        hole=(xx*xx+yy*yy<.115).astype(np.float32)
        ht=-hole*.65; tint=1-hole*.72; variation=hole*.10
    elif kind=='metal':
        ht=.05*np.sin(2*np.pi*Y*320)+.018*np.sin(2*np.pi*Y*127)+fine*.015
        tint=1+ht*.12; variation=ht*.25
    elif kind=='leather':
        ht=.18*np.sin(2*np.pi*X*97+np.sin(2*np.pi*Y*31))*.5+.16*np.sin(2*np.pi*Y*113)+fine*.22
        tint=1+ht*.12; variation=ht*.16
    else:
        ht=fine*(.04 if kind in ['paint','lens'] else .20)
        tint=1+ht*.08; variation=ht*(.025 if kind=='lens' else .14)
    base=np.clip(np.array(color,dtype=np.float32)[None,None,:]*tint[:,:,None],0,1)
    base=np.where(base<=.0031308,base*12.92,1.055*np.power(base,1/2.4)-.055)
    gx=(np.roll(ht,-1,1)-np.roll(ht,1,1))*.25; gy=(np.roll(ht,-1,0)-np.roll(ht,1,0))*.25
    normal=np.stack([-gx,-gy,np.ones_like(ht)],axis=-1)
    normal/=np.linalg.norm(normal,axis=-1)[:,:,None]; normal=normal*.5+.5
    maps={'BaseColor':base,'Roughness':np.clip(rough+variation,.015,.98),'Metallic':np.full((res,res),metal,dtype=np.float32),'Normal':normal,'AO':np.ones((res,res),dtype=np.float32)}
    if kind=='speaker': maps['AO']=1-hole*.35
    images[key]={}; paths={}
    for channel,data in maps.items():
        path=directory/(key+'_'+channel+'.png')
        images[key][channel]=save_image(path,data,channel!='BaseColor'); paths[channel]=str(path.relative_to(ROOT))
    manifest[key]={'resolution':res,'tile_m':meters,'maps':paths,'AO_scope':'Material micro-occlusion only; white for unoccluded tile, not vehicle cavity AO'}
    del maps,base,normal,X,Y,noise,fine,ht,tint,variation

aliases={'MAT_Aero_Review':'MAT_CarbonFiber','MAT_Wheel_Alloy':'MAT_WheelMetal','MAT_Wheel_DarkAccent':'MAT_WheelDark',
'MAT_DRL':'MAT_EmissiveWhite','MAT_Headlight':'MAT_EmissiveWhite','MAT_ReverseLight':'MAT_EmissiveWhite','MAT_Taillight':'MAT_EmissiveRed','MAT_BrakeLight':'MAT_EmissiveRed','MAT_Indicator':'MAT_EmissiveAmber',
'MAT_Tire_Emboss':'MAT_Tire','MAT_ExhaustInner':'MAT_BrushedMetal','MAT_IntakeDuct':'MAT_BlackPlastic','MAT_Recess_Depth':'MAT_HeadlightHousing','MAT_WindowSeal':'MAT_BlackPlastic'}
spec={
'MAT_CarPaint':('paint',None),'MAT_CarbonFiber':('carbon',None),'MAT_BlackPlastic':('plastic',None),
'MAT_Chrome':('chrome',None),'MAT_BrushedMetal':('metal',(.33,.37,.4)),
'MAT_Glass':(None,(.78,.88,.93)),'MAT_HeadlightLens':('lens',None),'MAT_TaillightLens':('lens',(.47,.50,.53)),
'MAT_HeadlightHousing':('plastic',(.18,.22,.26)),
'MAT_EmissiveWhite':(None,(.76,.87,1)),'MAT_EmissiveRed':(None,(.65,.005,.009)),'MAT_EmissiveAmber':(None,(.8,.16,.002)),
'MAT_WheelMetal':('metal',None),'MAT_WheelDark':('metal',(.12,.16,.20)),
'MAT_Tire':('rubber',None),'MAT_BrakeDisc':('rotor',None),'MAT_BrakeCaliper':('caliper',None),
'MAT_InteriorLeather':('leather',None),'MAT_InteriorPlastic':('plastic',(.55,.6,.65)),
'MAT_InteriorAlcantara':('alcantara',None),'MAT_InteriorCarbon':('carbon',None),
'MAT_InteriorMetal':('metal',(.40,.46,.52)),'MAT_Display':(None,(.006,.016,.023)),
'MAT_SeatAccent':('leather',(.65,.05,.045)),'MAT_Speaker':('speaker',None),'MAT_InteriorMirror':(None,(.68,.72,.76)),
'MAT_ProjectorLens':('lens',(.60,.75,.91))}
materials={}
for name,(key,tint) in spec.items():
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes=True
    nodes=m.node_tree.nodes; links=m.node_tree.links; nodes.clear()
    out=nodes.new('ShaderNodeOutputMaterial'); out.location=(850,0)
    bs=nodes.new('ShaderNodeBsdfPrincipled'); bs.location=(550,0); links.new(bs.outputs['BSDF'],out.inputs['Surface'])
    if key:
        uv=nodes.new('ShaderNodeUVMap'); uv.uv_map='UVMap'; uv.location=(-900,200)
        attr=nodes.new('ShaderNodeAttribute'); attr.attribute_type='OBJECT'; attr.attribute_name='uv_meter_scale'; attr.location=(-900,-30)
        mult=nodes.new('ShaderNodeMath'); mult.operation='MULTIPLY'; mult.inputs[1].default_value=1/(sets[key][6]*(.5 if name=='MAT_InteriorCarbon' else 1)); mult.location=(-700,-30)
        links.new(attr.outputs['Fac'],mult.inputs[0])
        scale=nodes.new('ShaderNodeVectorMath'); scale.operation='SCALE'; scale.location=(-520,200)
        links.new(uv.outputs['UV'],scale.inputs[0]); links.new(mult.outputs[0],scale.inputs[3])
        for j,ch in enumerate(['BaseColor','Roughness','Metallic','Normal']):
            tex=nodes.new('ShaderNodeTexImage'); tex.image=images[key][ch]; tex.label=ch; tex.location=(-300,400-j*230)
            tex.interpolation='Linear'; tex.extension='REPEAT'; links.new(scale.outputs[0],tex.inputs['Vector'])
            if ch=='Normal':
                normal=nodes.new('ShaderNodeNormalMap'); normal.space='TANGENT'; normal.uv_map='UVMap'; normal.inputs['Strength'].default_value=.3 if key!='speaker' else .65; normal.location=(300,-350)
                links.new(tex.outputs['Color'],normal.inputs['Color']); links.new(normal.outputs['Normal'],bs.inputs['Normal'])
            elif ch=='BaseColor':
                mix=nodes.new('ShaderNodeMixRGB'); mix.blend_type='MULTIPLY'; mix.inputs[0].default_value=1; mix.inputs[2].default_value=(*(tint or (1,1,1)),1); mix.label='Color tint — neutral preserves texture'; mix.location=(80,350)
                links.new(tex.outputs['Color'],mix.inputs[1]); links.new(mix.outputs[0],bs.inputs['Base Color'])
            else: links.new(tex.outputs['Color'],bs.inputs[ch])
        m['texture_set']=key; m['tile_m']=sets[key][6]*(.5 if name=='MAT_InteriorCarbon' else 1)
    else: bs.inputs['Base Color'].default_value=(*(tint or (.02,.02,.02)),1)
    if name in ['MAT_CarPaint','MAT_BrakeCaliper']:
        bs.inputs['Coat Weight'].default_value=.42; bs.inputs['Coat Roughness'].default_value=.18
    if 'Carbon' in name: bs.inputs['Coat Weight'].default_value=.23; bs.inputs['Coat Roughness'].default_value=.24
    if name=='MAT_InteriorAlcantara': bs.inputs['Sheen Weight'].default_value=.3
    if name in ['MAT_Glass','MAT_HeadlightLens','MAT_TaillightLens','MAT_ProjectorLens']:
        bs.inputs['Transmission Weight'].default_value=1; bs.inputs['IOR'].default_value=1.46; bs.inputs['Roughness'].default_value=.035
    if name.startswith('MAT_Emissive'):
        bs.inputs['Emission Color'].default_value=(*tint,1); bs.inputs['Emission Strength'].default_value=2.0 if name.endswith('White') else 1.3
        bs.inputs['Roughness'].default_value=.28
    if name=='MAT_Display':
        bs.inputs['Roughness'].default_value=.19; bs.inputs['Emission Color'].default_value=(.014,.033,.05,1); bs.inputs['Emission Strength'].default_value=.35
    if name=='MAT_InteriorMirror': bs.inputs['Metallic'].default_value=1; bs.inputs['Roughness'].default_value=.045
    m['game_conversion']='Standard PBR maps; bake per-object UV-meter transform to atlas or carry equivalent UV tiling to engine'
    materials[name]=m
for o in asset:
    if o.type not in ['MESH','CURVE']: continue
    for i,old in enumerate(list(o.data.materials)):
        if not old: continue
        name=aliases.get(old.name,old.name)
        if name in materials: o.data.materials[i]=materials[name]
    if o.name.startswith(('Headlight_Housing','Headlight_Cavity','Taillight_Housing','Taillight_Cavity')):
        for i in range(len(o.data.materials)): o.data.materials[i]=materials['MAT_HeadlightHousing']
for m in list(bpy.data.materials):
    if m.users==0: bpy.data.materials.remove(m)
for o in asset:
    if o.type=='MESH': assert signature(o)==source_geometry[o.name],o.name+' geometry changed'
(ROOT/'texture_manifest.json').write_text(json.dumps(manifest,indent=2))
s['milestone']='06 UV and texture-backed PBR review; downstream production deferred'
s['uv_strategy']='Seven packed atlas groups, unique base islands, intentional live modifier UV reuse; UVMap only'
s.render.engine='CYCLES'; s.cycles.samples=48; s.cycles.use_denoising=True
s.render.resolution_x=1920; s.render.resolution_y=1080; s.render.resolution_percentage=100
s.camera=bpy.data.objects['Camera_Presentation']
bpy.ops.object.select_all(action='DESELECT'); bpy.data.objects['Car_Body'].select_set(True); bpy.context.view_layer.objects.active=bpy.data.objects['Car_Body']
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_06_materials_uv_working.blend'))
print('MATERIAL AND UV BUILD COMPLETE',flush=True)
