"""Exterior production pass from the existing 03 checkpoint, Blender only.
Run with -- --review for quick review images; no UV/LOD/export production.
"""
import bpy
import bmesh
import ast
import math
import sys
from pathlib import Path
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'racing_car_03_realistic_body.blend'
WORK=ROOT/'racing_car_04_exterior_working.blend'
FINAL=ROOT/'racing_car_04_exterior_final.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene
COL={n:bpy.data.collections[n] for n in ['CAR','WHEELS','BRAKES','INTERIOR','GLASS','LIGHTS','COLLIDERS','LODS','REFERENCES','PRESENTATION']}
paint=bpy.data.materials['MAT_CarPaint']
dark=bpy.data.materials['MAT_BlackPlastic']
aero=bpy.data.materials['MAT_Aero_Review']
tiremat=bpy.data.materials['MAT_Tire']
alloy=bpy.data.materials['MAT_Wheel_Alloy']
chrome=bpy.data.materials['MAT_Chrome']
disc=bpy.data.materials['MAT_BrakeDisc']
calipermat=bpy.data.materials['MAT_BrakeCaliper']
glass=bpy.data.materials['MAT_Glass']
slotmat=bpy.data.materials['MAT_Recess_Depth']
# Reuse established modeling functions and surface definitions, without
# executing the previous builder or opening/rebuilding the old blockout.
tree=ast.parse((ROOT/'scripts'/'refine_realistic_body.py').read_text())
constants={'width_points','center_points','roof_points','cabin_width'}
for node in tree.body:
    if isinstance(node,ast.FunctionDef) or (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in constants for t in node.targets)):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<existing_surface_helpers>','exec'),globals())
paint=bpy.data.materials['MAT_CarPaint']
dark=bpy.data.materials['MAT_BlackPlastic']
aero=bpy.data.materials['MAT_Aero_Review']
tiremat=bpy.data.materials['MAT_Tire']
alloy=bpy.data.materials['MAT_Wheel_Alloy']
chrome=bpy.data.materials['MAT_Chrome']
disc=bpy.data.materials['MAT_BrakeDisc']
calipermat=bpy.data.materials['MAT_BrakeCaliper']
glass=bpy.data.materials['MAT_Glass']
slotmat=bpy.data.materials['MAT_Recess_Depth']

def remove(name):
    obj=bpy.data.objects.get(name)
    if obj: bpy.data.objects.remove(obj,do_unlink=True)

def remove_prefix(prefix):
    for obj in list(bpy.data.objects):
        if obj.name.startswith(prefix): bpy.data.objects.remove(obj,do_unlink=True)

def emission(name,color,strength):
    m=material(name,color,.05,.2,.2)
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Emission Color'].default_value=(*color,1)
    p.inputs['Emission Strength'].default_value=strength
    m['independent_light_channel']=name
    return m

drlmat=emission('MAT_DRL',(.72,.86,1),5)
headmat=emission('MAT_Headlight',(.76,.88,1),3)
tailmat=emission('MAT_Taillight',(.90,.008,.015),6)
brakemat=emission('MAT_BrakeLight',(.90,.004,.009),2.5)
indicator=emission('MAT_Indicator',(.85,.20,.005),.1)
reverse=emission('MAT_ReverseLight',(.77,.88,1),.15)
lightglass=material('MAT_HeadlightLens',(.92,.97,1),0,.035,.1,.98)
lightglass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.46
tailglass=material('MAT_TaillightLens',(.38,.43,.48),0,.045,.15,.97)
tailglass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.46
projectglass=material('MAT_ProjectorLens',(.39,.55,.73),.1,.06,.2,.60)
sealmat=material('MAT_WindowSeal',(.008,.010,.012),0,.5)
accent=material('MAT_Wheel_DarkAccent',(.055,.065,.079),.82,.24)
emboss=material('MAT_Tire_Emboss',(.014,.016,.018),0,.72)
ductmat=material('MAT_IntakeDuct',(.025,.029,.034),.1,.38)
heatmat=material('MAT_ExhaustInner',(.047,.042,.036),.8,.42)
floor=bpy.data.objects['Studio_Floor']
floor.location.z=-.025

# First correct the base arch geometry rather than hiding it with trim.
old_arch_bottom=arch_bottom
def arch_bottom(y):
    result=.175
    for c,r,h in [(-1.35,.393,.345),(1.35,.414,.365)]:
        d=abs(y-c)
        start=r-.012
        finish=r+.033
        if d<=start:
            z=h+math.sqrt(max(0,r*r-d*d))
        elif d<finish:
            z0=h+math.sqrt(r*r-start*start)
            slope=-start/math.sqrt(r*r-start*start)
            t=(d-start)/(finish-start)
            z=(2*t**3-3*t*t+1)*z0+(t**3-2*t*t+t)*slope*(finish-start)+(-2*t**3+3*t*t)*.175
        else:
            z=.175
        result=max(result,z)
    return result

body=bpy.data.objects['Car_Body']
for v in body.data.vertices:
    x,y,z=v.co
    top=top_z(1,y); oldbot=old_arch_bottom(y)
    if x>.76 and z<top-.0005 and top-oldbot>.005:
        t=max(0,min(1,(top-z)/(top-oldbot)))
        newbot=arch_bottom(y)
        v.co.z=lerp(top,newbot,t)
        strength=min(1,gauss(y,-1.35,.46)+gauss(y,1.35,.48))
        v.co.x+=.039*strength*t**6
clean_normals(body.data)
body['topology_pass']='Smooth tangent arch endings, rolled shoulder width, separate door panels, inset headlight openings'

def subset_mesh(name,data,faces,mat=paint,coll='CAR',mirror=False):
    used=sorted({i for f in faces for i in f})
    lookup={i:j for j,i in enumerate(used)}
    o=make_mesh(name,[tuple(data.vertices[i].co) for i in used],[tuple(lookup[i] for i in f) for f in faces],mat,coll)
    if mirror:
        m=o.modifiers.new('Original X symmetry','MIRROR'); m.use_clip=True
    return o

def boundary_loops(data):
    counts={}
    for p in data.polygons:
        ids=list(p.vertices)
        for a,b in zip(ids,ids[1:]+ids[:1]):
            key=tuple(sorted((a,b))); counts[key]=counts.get(key,0)+1
    edges=[e for e,n in counts.items() if n==1]
    adjacency={}
    for a,b in edges:
        adjacency.setdefault(a,[]).append(b); adjacency.setdefault(b,[]).append(a)
    unvisited=set(adjacency); loops=[]
    while unvisited:
        start=min(unvisited); cur=start; prev=None; loop=[]
        for _ in range(len(adjacency)+1):
            loop.append(cur); unvisited.discard(cur)
            options=[i for i in adjacency[cur] if i!=prev]
            if not options: break
            nxt=options[0]
            if nxt==start: break
            if nxt not in unvisited: break
            prev,cur=cur,nxt
        loops.append(loop)
    return loops

def delete_faces(obj,selected):
    bm=bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in selected],context='FACES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(obj.data); bm.free(); obj.data.update()

def recover_side_base(y,t):
    a,b=-2.23,2.23
    for _ in range(28):
        m=(a+b)/2
        if side_surface(m,t)[1]<y: a=m
        else: b=m
    return (a+b)/2

# Actual door meshes are extracted from the original continuous quad flank.
selected=[]
for p in body.data.polygons:
    c=p.center; top=top_z(1,c.y); bot=arch_bottom(c.y)
    if -.95<c.y<.57 and c.x>.78 and c.z<top-.010 and top-bot>.15:
        t=(top-c.z)/(top-bot)
        base_y=recover_side_base(c.y,t)
        if -.89<base_y<.46 and .065<t<.94: selected.append(p.index)
doorfaces=[tuple(body.data.polygons[i].vertices) for i in selected]
door_r=subset_mesh('Car_Door_R',body.data,doorfaces)
delete_faces(body,selected)
loops=boundary_loops(door_r.data)
edge_ids=set(i for loop in loops for i in loop)
center=sum((v.co for v in door_r.data.vertices),Vector())/len(door_r.data.vertices)
for v in door_r.data.vertices:
    if v.index in edge_ids:
        d=center-v.co
        d.x=0
        if d.length: v.co+=d.normalized()*.0035
clean_normals(door_r.data)
for s,label in [(1,'R'),(-1,'L')]:
    if s==1:
        door=door_r
    else:
        door=make_mesh('Car_Door_L',[(-v.co.x,v.co.y,v.co.z) for v in door_r.data.vertices],
            [tuple(p.vertices) for p in door_r.data.polygons])
    sub(door,1); shell(door,.006)
    door['panel_gap_m']=.0035
    for loop in boundary_loops(door.data):
        coords=[tuple(door.data.vertices[i].co+Vector((-s*.0015,0,0))) for i in loop]
        tube('Door_Shutline_Seal_'+label,coords,.0013,sealmat,cyclic=True,res=2)
    remove('Door_Panel_Gap_'+label)
    remove('Door_Handle_Recess_'+label)
    # Two millimetre recessed flush handle, with a thin painted center blade.
    y0=.13; z0=.685
    x0=abs(side_at(y0,z0,s)[0])
    o=box('Door_Handle_Recess_'+label,(s*(x0+.0005),y0,z0),(.005,.137,.020),slotmat,radius=.006)
    box('Door_Handle_FlushBlade_'+label,(s*(x0+.003),y0-.004,z0),(.004,.112,.012),paint,radius=.004)

# Replace inconsistent glazing with shared curved boundaries and fitted seals.
for prefix in ['Roof_Rail_','A_Pillar_','Rear_Cabin_Buttress_','Rear_Buttress_Surface_',
               'Window_Belt_Seal_','Window_B_Pillar_','Windshield_Cowl_Seal',
               'Windshield_Header_Seal','Rear_Glass_Header_Seal','Rear_Glass_Deck_Seal']:
    remove_prefix(prefix)

def wind_surface(u,v):
    by=-1.012+.165*u*u
    bx=u*.717
    bz=top_z(abs(bx)/width(by),by)+.007
    top=Vector(greenhouse(u,-.298+.015*u*u))
    p=Vector((bx,by,bz)).lerp(top,v)
    p.z+=.030*math.sin(math.pi*v)*(1-.35*u*u)
    return tuple(p)

def rear_surface(u,v):
    top=Vector(greenhouse(u,.535+.018*u*u))
    by=1.132-.160*u*u; bx=u*.680
    bz=top_z(abs(bx)/width(by),by)+.007
    p=top.lerp(Vector((bx,by,bz)),v)
    p.z+=.018*math.sin(math.pi*v)*(1-.25*u*u)
    return tuple(p)

patch('Windshield',lambda u,v:wind_surface(2*u-1,v),32,24,glass,'GLASS',1,.004)
patch('Roof_Panel',lambda u,v:greenhouse(2*u-1,lerp(-.290+.015*(2*u-1)**2,.525+.018*(2*u-1)**2,v)),
      28,28,paint,'CAR',1,.006)
patch('Rear_Glass',lambda u,v:rear_surface(2*u-1,v),32,24,glass,'GLASS',1,.004)
for name,fn,t in [('Windshield_Cowl_Seal',wind_surface,0),('Windshield_Header_Seal',wind_surface,1),
                  ('Rear_Glass_Header_Seal',rear_surface,0),('Rear_Glass_Deck_Seal',rear_surface,1)]:
    tube(name,[fn(-1+2*i/80,t) for i in range(81)],.003,sealmat,cyclic=False,res=2)

for s,label in [(-1,'L'),(1,'R')]:
    def glazing(u,v,s=s):
        a=Vector(wind_surface(s,v)); b=Vector(rear_surface(s,1-v))
        top=Vector(greenhouse(s,lerp(-.283,.553,u)))
        p00=Vector(wind_surface(s,0)); p10=Vector(rear_surface(s,1))
        p01=Vector(wind_surface(s,1)); p11=Vector(rear_surface(s,0))
        low=p00.lerp(p10,u)
        low.x+=s*.014*math.sin(math.pi*u)
        low.z=top_z(abs(low.x)/width(low.y),low.y)+.007
        blend=p00*(1-u)*(1-v)+p10*u*(1-v)+p01*(1-u)*v+p11*u*v
        p=a*(1-u)+b*u+low*(1-v)+top*v-blend
        p.x+=s*.008*math.sin(math.pi*u)*math.sin(math.pi*v)
        return tuple(p)
    patch('Window_F'+label,lambda u,v:glazing(.77*u,v),28,16,glass,'GLASS',1,.003)
    patch('Window_R'+label,lambda u,v:glazing(.79+.21*u,v),14,16,glass,'GLASS',1,.003)
    tube('A_Pillar_'+label,[wind_surface(s,i/64) for i in range(65)],.019,paint,res=3)
    tube('Roof_Rail_'+label,[greenhouse(s,lerp(-.28,.55,i/80)) for i in range(81)],.018,paint,res=3)
    tube('Rear_Cabin_Pillar_'+label,[rear_surface(s,i/64) for i in range(65)],.025,paint,res=3)
    tube('Window_Belt_Seal_'+label,[glazing(i/100,0) for i in range(101)],.0035,sealmat,res=2)
    tube('Window_B_Pillar_'+label,[glazing(.78,i/40) for i in range(41)],.008,paint,res=2)
    tube('Side_Glass_Upper_Seal_'+label,[glazing(i/100,1) for i in range(101)],.003,sealmat,res=2)
    # A narrow C-pillar surface, fully supported by the rear shoulder.
    patch('Rear_Cabin_Pillar_Surface_'+label,lambda u,v,s=s:(
        rear_surface(s,u)[0]+s*.048*v,
        rear_surface(s,u)[1]+.04*v,
        rear_surface(s,u)[2]-.015*v),32,6,paint,'CAR',1,.006)

g=glass.node_tree.nodes.get('Principled BSDF')
g.inputs['Base Color'].default_value=(.09,.14,.18,1)
g.inputs['Metallic'].default_value=0
g.inputs['Roughness'].default_value=.055
g.inputs['Transmission Weight'].default_value=.75
g.inputs['IOR'].default_value=1.46
glass.diffuse_color=(.06,.10,.13,1)

# Headlight apertures are cut by deleting controlled quad patches; no boolean.
def base_y_from_top(q,y):
    base=y
    for _ in range(18): base=y-(body_y(q,base)-base)
    return base

lamp_selected=[]
for p in body.data.polygons:
    c=p.center
    if c.x>.60 and c.y<-1.60 and p.normal.z>.45:
        q=c.x/width(c.y); by=base_y_from_top(q,c.y)
        if .7001<q<.8999 and -2.070<by<-1.700: lamp_selected.append(p.index)
lampfaces=[tuple(body.data.polygons[i].vertices) for i in lamp_selected]
lamp_patch=subset_mesh('Headlight_Aperture_Template',body.data,lampfaces,dark,'LIGHTS')
lamp_loop=max(boundary_loops(lamp_patch.data),key=len)
lamp_boundary=[Vector(lamp_patch.data.vertices[i].co) for i in lamp_loop]
qmin=min(p.x/width(p.y) for p in lamp_boundary)
qmax=max(p.x/width(p.y) for p in lamp_boundary)
bmin=min(base_y_from_top(p.x/width(p.y),p.y) for p in lamp_boundary)
bmax=max(base_y_from_top(p.x/width(p.y),p.y) for p in lamp_boundary)
delete_faces(body,lamp_selected)
remove('Headlight_Aperture_Template')
# Paint support loops are welded into the surrounding skin. They keep the
# headlight aperture from pulling a broad dent into the subdivided fender.
vs=[tuple(v.co) for v in body.data.vertices]
fs=[tuple(p.vertices) for p in body.data.polygons]
lookup={tuple(round(c,6) for c in p):i for i,p in enumerate(vs)}
outer=[lookup[tuple(round(c,6) for c in p)] for p in lamp_boundary]
lamp_center=sum(lamp_boundary,Vector())/len(lamp_boundary)
for scale,dz in [(.978,-.0007),(.960,-.0035)]:
    inner=[]
    for p in lamp_boundary:
        q=lamp_center+(p-lamp_center)*scale
        q.z=top_z(q.x/width(q.y),q.y)+dz
        inner.append(len(vs)); vs.append(tuple(q))
    fs.extend((outer[i],outer[(i+1)%len(outer)],inner[(i+1)%len(inner)],inner[i]) for i in range(len(outer)))
    outer=inner
lamp_boundary=[Vector(vs[i]) for i in outer]
body=make_mesh('Car_Body',vs,fs)
m=body.modifiers.new('Original X symmetry','MIRROR'); m.use_clip=True
sub(body,1); shell(body,.007)

def lamp_point(q,b,s=1,dz=0):
    y=body_y(q,b)
    return (s*q*width(y),y,top_z(q,y)+dz)

def frame_ring(name,boundary,mat,coll='LIGHTS',depth=.070):
    center=sum(boundary,Vector())/len(boundary)
    vs=[]
    for scale,dz in [(1.0,0),(.985,-.004),(.975,-.013),(.970,-depth)]:
        for p in boundary:
            q=center+(p-center)*scale
            q.z=p.z+dz
            vs.append(tuple(q))
    n=len(boundary)
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
    o=make_mesh(name,vs,fs,mat,coll)
    sub(o,1); shell(o,.003)
    return o

def orient_axis(obj,axis):
    obj.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)

for s,label in [(-1,'L'),(1,'R')]:
    remove('Headlight_Recess_Rim_'+label)
    boundary=[Vector((s*p.x,p.y,p.z)) for p in lamp_boundary]
    frame_ring('Headlight_Housing_'+label,boundary,dark,depth=.070)
    patch('Headlight_Cavity_'+label,lambda u,v,s=s:lamp_point(lerp(qmin+.005,qmax-.005,u),lerp(bmin+.005,bmax-.005,v),s,-.069),
          12,20,slotmat,'LIGHTS',0,.004)
    lens_obj=patch('Headlight_'+label,lambda u,v,s=s:lamp_point(lerp(qmin+.009,qmax-.009,u),lerp(bmin+.008,bmax-.008,v),s,-.003),
          18,28,lightglass,'LIGHTS',1,.003)
    lens_obj['assembly']='Clear outer lens; independent dark cavity, bent-blade DRL, two canted projector modules'
    # Original continuous grazing blade, with a short transverse front return.
    pts=[lamp_point(lerp(qmin+.023,qmin+.13,i/16),bmin+.031,s,-.010) for i in range(17)]
    pts.reverse()
    pts += [lamp_point(qmin+.023+.012*smooth(i/64),lerp(bmin+.031,bmax-.026,i/64),s,-.010) for i in range(1,65)]
    tube('Headlight_DRL_'+label,pts,.0028,drlmat,'LIGHTS',False,3)
    # Short secondary blade makes the housing readable from the front.
    tube('Headlight_SecondaryLED_'+label,[lamp_point(qmax-.025,lerp(bmin+.075,bmin+.152,i/24),s,-.013) for i in range(25)],
         .0017,drlmat,'LIGHTS',False,2)
    for idx,b in enumerate([bmin+.105,bmin+.238],1):
        p=Vector(lamp_point((qmin+qmax)/2+.010,b,s,-.044))
        axis=Vector((0,-.8,.6))
        o=cylinder('Headlight_Projector_Shroud_'+label+'_'+str(idx),p,.032,.041,dark,'LIGHTS','Z',64,.003)
        orient_axis(o,axis)
        o=cylinder('Headlight_Projector_Bezel_'+label+'_'+str(idx),p+axis*.022,.029,.004,chrome,'LIGHTS','Z',64,.001)
        orient_axis(o,axis)
        o=cylinder('Headlight_Projector_Emitter_'+label+'_'+str(idx),p+axis*.024,.025,.002,headmat,'LIGHTS','Z',64,0)
        orient_axis(o,axis)
        # Optical convex lens, not a flat glowing disc.
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=p+axis*.027)
        o=link(bpy.context.object,'LIGHTS'); o.name='Headlight_Projector_Lens_'+label+'_'+str(idx)
        o.scale=(.025,.025,.008); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        orient_axis(o,axis); assign(o,projectglass)
        for poly in o.data.polygons: poly.use_smooth=True

# Engine cover openings: functional recessed slotted vent wells with moderate ribs.
engine=bpy.data.objects['Rear_Engine_Cover']
vent_ids=[]
for p in engine.data.polygons:
    c=p.center
    if 1.34<c.y<1.93 and .23<c.x<.49: vent_ids.append(p.index)
delete_faces(engine,vent_ids)
for s,label in [(-1,'L'),(1,'R')]:
    remove('Engine_Vent_Region_'+label)
    patch('Engine_Vent_Duct_'+label,lambda u,v,s=s:(s*lerp(.215,.505,u),lerp(1.32,1.95,v),
          top_z(lerp(.215,.505,u)/width(lerp(1.32,1.95,v)),lerp(1.32,1.95,v))-.035),
          10,18,slotmat,'CAR',0,.004)
    for i in range(7):
        y=1.365+i*.080
        patch('Engine_Vent_Louver_'+label+'_'+str(i+1),lambda u,v,y=y,s=s:(s*lerp(.215,.505,u),y+.024*v,
              top_z(lerp(.215,.505,u)/width(y+.024*v),y+.024*v)-.010+.010*v),
              10,3,aero,'CAR',0,.005)

# Add broad panel seals derived from actual panel edges rather than arbitrary cuts.
for name,seal_name in [('Hood','Hood_Shutline'),('Rear_Engine_Cover','EngineCover_Shutline')]:
    obj=bpy.data.objects[name]
    for k,loop in enumerate(boundary_loops(obj.data)):
        # Do not draw an artificial center seam on a mirrored panel.
        paths=[]; path=[]
        for i in loop+loop[:1]:
            p=obj.data.vertices[i].co
            if abs(p.x)<.001:
                if len(path)>1: paths.append(path)
                path=[]
            else:
                path.append(tuple(p+Vector((0,0,-.002))))
        if len(path)>1: paths.append(path)
        for j,path in enumerate(paths):
            for s,label in [(-1,'L'),(1,'R')]:
                tube(seal_name+'_'+label+'_'+str(k)+'_'+str(j),[(s*x,y,z) for x,y,z in path],.0017,sealmat,res=2)

# Fascia openings: slimmer painted edges and inner cooling surfaces.
for name in ['Front_Central_Intake','Front_Cooling_Duct_L','Front_Cooling_Duct_R']:
    obj=bpy.data.objects[name]
    n=len(obj.data.vertices)//4
    center=sum((v.co for v in obj.data.vertices[:n]),Vector())/n
    for v in obj.data.vertices[:n]:
        v.co.x=center.x+(v.co.x-center.x)*.953
        v.co.z=center.z+(v.co.z-center.z)*.953
    clean_normals(obj.data)
    obj['edge_refinement']='Thinner radiused surround; inner duct surfaces and functional grille'

for s,label in [(-1,'L'),(1,'R')]:
    # Two curved vanes inside each brake cooling duct, behind the opening.
    for i in range(2):
        x=s*(.678+.093*i)
        patch('Front_Duct_Guide_'+label+'_'+str(i+1),lambda u,v,x=x:(x+.008*math.sin(math.pi*v),
              front_y(x)+.055+.12*u,lerp(.261,.430,v)),4,12,aero,'CAR',0,.003)

def hex_grille(name,xrange,zrange,plane_y,mat,coll='CAR',r=.024):
    vs=[]; fs=[]
    row=0; z=zrange[0]+r
    while z<zrange[1]-r/2:
        x=xrange[0]+r+(row%2)*r*.87
        while x<xrange[1]-r:
            if abs(x)<.47-(.385-z)*.32:
                points=[Vector((x+r*math.cos(math.pi/6+k*math.pi/3),plane_y,z+r*math.sin(math.pi/6+k*math.pi/3))) for k in range(6)]
                for a,b in zip(points,points[1:]+points[:1]):
                    direction=(b-a).normalized(); across=Vector((-direction.z,0,direction.x))*.0008
                    depth=Vector((0,.0008,0)); start=len(vs)
                    for p in [a,b]:
                        vs.extend([tuple(p-across-depth),tuple(p+across-depth),tuple(p+across+depth),tuple(p-across+depth)])
                    fs.extend([(start+i,start+(i+1)%4,start+4+(i+1)%4,start+4+i) for i in range(4)])
                    fs.extend([(start+3,start+2,start+1,start),(start+4,start+5,start+6,start+7)])
            x+=r*1.74
        z+=r*1.5; row+=1
    return make_mesh(name,vs,fs,mat,coll,False)
hex_grille('Front_Intake_Grille',(-.48,.48),(.235,.389),-2.12,aero)

# Smooth drafted intake walls turn toward the mid-engine bay, rather than
# ending at a flat black plate immediately behind the outer opening.
for s,label in [(-1,'L'),(1,'R')]:
    throat=bpy.data.objects['Side_Intake_Throat_'+label]
    n=len(throat.data.vertices)//2
    mouth=[Vector(v.co) for v in throat.data.vertices[:n]]
    c=sum(mouth,Vector())/n
    vs=[]
    for depth,scale,turn in [(0,1,0),(.085,.95,.035),(.17,.78,.13),(.22,.64,.22)]:
        for p in mouth:
            q=c+(p-c)*scale
            q.x=p.x-s*depth; q.y+=turn
            vs.append(tuple(q))
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
    fs.append(tuple(range(3*n,4*n)))
    throat=make_mesh('Side_Intake_Throat_'+label,vs,fs,ductmat)
    sub(throat,1); shell(throat,.003)

# Rear lighting holes follow the existing fascia's quad grid.
rear=bpy.data.objects['Rear_Bumper']
def fascia_uv(p):
    lo,hi=0,1
    for _ in range(24):
        t=(lo+hi)/2
        if rearband(t,.5)[0]<p.x: lo=t
        else: hi=t
    u=(lo+hi)/2
    bottom=rearband(u,0)[2]; top=rearband(u,1)[2]
    return u,(p.z-bottom)/(top-bottom)
rear_selected=[]
for p in rear.data.polygons:
    u,v=fascia_uv(p.center)
    if (.035<u<.410 or .590<u<.965) and .205<v<.495: rear_selected.append(p.index)
delete_faces(rear,rear_selected)
for s,label in [(-1,'L'),(1,'R')]:
    def tail_point(u,v,s=s,depth=0):
        uu=lerp(.59375,.96875,u)
        x,y,z=rearband(uu,lerp(.20,.50,v))
        return s*x,y-depth,z
    boundary=[Vector(tail_point(i/40,0)) for i in range(41)]+[Vector(tail_point(1,i/10)) for i in range(1,11)]+[Vector(tail_point(1-i/40,1)) for i in range(1,41)]+[Vector(tail_point(0,1-i/10)) for i in range(1,10)]
    # Fascia normal is +Y; support loops are recessed toward -Y.
    verts=[]
    center=sum(boundary,Vector())/len(boundary)
    for scale,depth in [(1,0),(.989,.005),(.981,.014),(.981,.055)]:
        for p in boundary:
            q=center+(p-center)*scale; q.y=p.y-depth; verts.append(tuple(q))
    n=len(boundary)
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
    housing=make_mesh('Taillight_Housing_'+label,verts,fs,dark,'LIGHTS'); sub(housing,1); shell(housing,.003)
    patch('Taillight_Cavity_'+label,lambda u,v:tail_point(u,v,depth=.054),40,8,slotmat,'LIGHTS',0,.003)
    patch('Taillight_'+label,lambda u,v:tail_point(lerp(.015,.985,u),lerp(.06,.94,v),depth=.003),
          40,8,tailglass,'LIGHTS',1,.003)
    # Two staggered strokes with an outer kick: original separated rear signature.
    for name,v,u0,u1,mat,rad in [('Signature',.72,.025,.91,tailmat,.0025),
                                ('Brake',.33,.115,.985,brakemat,.0030)]:
        points=[tail_point(lerp(u0,u1,i/80),v+.07*smooth(i/80),depth=.011) for i in range(81)]
        tube('Taillight_'+name+'_'+label,points,rad,mat,'LIGHTS',False,3)
    tube('Taillight_OuterKick_'+label,[tail_point(.935,lerp(.50,.79,i/14),depth=.011) for i in range(15)],.0025,tailmat,'LIGHTS',False,2)
    tube('Taillight_Reverse_'+label,[tail_point(lerp(.035,.12,i/16),.27,depth=.012) for i in range(17)],.0020,reverse,'LIGHTS',False,2)
    tube('Taillight_Indicator_'+label,[tail_point(lerp(.74,.94,i/28),.31,depth=.012) for i in range(29)],.0020,indicator,'LIGHTS',False,2)

# Refine the diffuser to four restrained, thickened swept fins.
remove_prefix('Diffuser_Fin_')
for i,x in enumerate([-.54,-.18,.18,.54],1):
    vs=[(x-.004,1.82,.146),(x-.004,2.23,.190),(x-.004,2.23,.309),(x-.004,1.88,.184),
        (x+.004,1.82,.146),(x+.004,2.23,.190),(x+.004,2.23,.309),(x+.004,1.88,.184)]
    fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    o=make_mesh('Diffuser_Fin_'+str(i),vs,fs,aero,smooth=False); bevel(o,.003,3)
for s,label in [(-1,'L'),(1,'R')]:
    # A restrained return at each splitter end, no oversized canards.
    patch('Splitter_Side_Return_'+label,lambda u,v,s=s:(s*lerp(.88,.972,u),
          lerp(-2.12,-1.86,v),.156+.013*u+.016*math.sin(math.pi*v)),8,14,aero,'CAR',1,.008)
    tube('Side_Skirt_Upper_Shutline_'+label,[(s*(.895+.010*math.sin(math.pi*i/60)),lerp(-.89,.90,i/60),.202) for i in range(61)],.0015,sealmat,res=2)
    # Hollow two-wall outlets with a recessed inner sleeve and pipe hint.
    remove('Exhaust_'+label); remove('Exhaust_Depth_'+label)
    axial_ring('Exhaust_'+label,(s*.63,2.155,.385),[(-.13,.061),(.094,.061),(.100,.058),(.095,.055),(-.13,.055)],chrome,'CAR','Y',80)
    axial_ring('Exhaust_InnerSleeve_'+label,(s*.63,2.145,.385),[(-.16,.054),(.071,.054),(.071,.051),(-.16,.051)],heatmat,'CAR','Y',64)
    cylinder('Exhaust_Depth_'+label,(s*.63,1.975,.385),.050,.004,slotmat,'CAR','Y',64,0)

# Remove redundant spoiler overlay: the main body already contains the lift.
# A separate engineered ducktail panel is extracted from the real body surface.
remove('Rear_Wing')
tail_ids=[p.index for p in body.data.polygons if p.center.y>2.08 and p.normal.z>.40 and p.center.z>.65]
tail_faces=[tuple(body.data.polygons[i].vertices) for i in tail_ids]
wing=subset_mesh('Rear_Wing',body.data,tail_faces,paint,mirror=True)
delete_faces(body,tail_ids)
sub(wing,1); shell(wing,.006)
wing['integrated_aero']='Extracted from existing raised rear deck; no floating overlay'
# Weld the matching panel boundary back into one continuous stamped surface.
# Retain a named assembly anchor and a vertex group for easy aero selection.
vs=[tuple(v.co) for v in body.data.vertices]
fs=[tuple(p.vertices) for p in body.data.polygons]
offset=len(vs)
vs.extend(tuple(v.co) for v in wing.data.vertices)
fs.extend(tuple(i+offset for i in p.vertices) for p in wing.data.polygons)
remove('Rear_Wing')
body=make_mesh('Car_Body',vs,fs)
m=body.modifiers.new('Original X symmetry','MIRROR'); m.use_clip=True
sub(body,1); shell(body,.007)
group=body.vertex_groups.get('Integrated_Ducktail') or body.vertex_groups.new(name='Integrated_Ducktail')
group.add([v.index for v in body.data.vertices if v.co.y>2.075 and v.co.z>.65],1,'REPLACE')
wing=bpy.data.objects.new('Rear_Wing',None); COL['CAR'].objects.link(wing)
wing.empty_display_type='PLAIN_AXES'; wing.empty_display_size=.03; wing.location=(0,2.08,.77)
wing['integrated_into']='Car_Body / Integrated_Ducktail vertex group'

# Premium mirror housings with a true rear-facing mirror aperture.
for s,label in [(-1,'L'),(1,'R')]:
    remove('Mirror_Stem_'+label); remove('Mirror_Glass_'+label)
    center=Vector((s*.914,-.635,.856))
    profiles=[(-.125,.018,.014),(-.100,.055,.033),(-.044,.082,.041),(.065,.080,.041),(.100,.069,.033),(.101,.065,.029),(.082,.065,.029)]
    vs=[]; segments=64
    for y,rx,rz in profiles:
        for i in range(segments):
            a=2*math.pi*i/segments
            vs.append(tuple(center+Vector((rx*math.cos(a),y,rz*math.sin(a)))))
    fs=[(j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i) for j in range(len(profiles)-1) for i in range(segments)]
    fs.append(tuple(reversed(range(segments))))
    o=make_mesh('Mirror_'+label,vs,fs,paint); sub(o,1); shell(o,.003)
    tube('Mirror_Stem_'+label,[(s*.749,-.688,.817),(s*.810,-.646,.845),(s*.861,-.628,.856)],.011,aero,res=3)
    def mirrorface(u,v):
        # Elliptical disk in a grid; polar center is a small capped ring.
        a=2*math.pi*u; r=.012+.986*v
        return (center.x+.063*r*math.cos(a),center.y+.101+.002*(1-r*r),center.z+.028*r*math.sin(a))
    m=patch('Mirror_Glass_'+label,mirrorface,64,8,chrome,'GLASS',0,.002)
    clean_normals(m.data)
    cylinder('Mirror_Glass_Center_'+label,(center.x,center.y+.103,center.z),.00085,.002,chrome,'GLASS','Y',24,0)
    tube('Mirror_Rear_Seal_'+label,[(center.x+.065*math.cos(2*math.pi*i/64),center.y+.101,center.z+.030*math.sin(2*math.pi*i/64)) for i in range(64)],.002,sealmat,'GLASS',True,2)

# Original wheel design retained: material separation, concavity and lug pockets.
for key in ['FL','FR','RL','RR']:
    wheel=bpy.data.objects['Wheel_'+key]
    x,y,z=wheel.location; s=-1 if x<0 else 1
    w=.29 if key.startswith('F') else .33
    radius=.345 if key.startswith('F') else .365
    face=x+s*(w/2-.009)
    for obj in COL['WHEELS'].objects:
        if obj.name.startswith('Wheel_Spoke_'+key):
            obj.data.materials.clear(); obj.data.materials.append(alloy); obj.data.materials.append(accent)
            for p in obj.data.polygons:
                p.material_index=1 if abs(p.normal.x)<.5 else 0
            obj['profile']='Retained original split-spoke geometry; machined face / dark sidewalls'
    hub=bpy.data.objects['Wheel_Hub_'+key]
    hub.data.materials.append(accent)
    for p in hub.data.polygons:
        if abs(p.normal.x)<.5: p.material_index=1
    # Shallow counterbores around the existing lugs.
    for k in range(5):
        a=2*math.pi*k/5
        o=axial_ring('Wheel_Lug_Recess_'+key+'_'+str(k+1),(face-s*.003,y+.043*math.cos(a),z+.043*math.sin(a)),
                     [(-.003,.010),(.002,.010),(.003,.007),(-.003,.007)],accent,segments=24)
        parent_world(o,wheel)
    # Sparse alternating shoulder sipes, modeled as shallow dark inlays.
    for k in range(28):
        angle=2*math.pi*k/28
        points=[]
        for j in range(9):
            ax=lerp(-w*.30,w*.30,j/8)
            aa=angle+.11*(j/8-.5)
            rr=radius-.0016
            points.append((x+ax,y+rr*math.cos(aa),z+rr*math.sin(aa)))
        o=tube('Tire_Shoulder_Sipe_'+key+'_'+str(k+1),points,.0007,slotmat,'WHEELS',False,1)
        parent_world(o,wheel)
    # Curved, generic embossed sidewall lettering: no real brands/logos.
    glyphs=[]
    for text,base_angle in [('AERO SPORT',1.57+.18*s),('295/30 ZR20' if key.startswith('F') else '335/30 ZR21',4.72+.18*s)]:
        for k,char in enumerate(text):
            if char==' ': continue
            a=base_angle-s*k*.040
            rr=radius-.041
            data=bpy.data.curves.new('Tire_Emboss_Glyph','FONT')
            data.body=char; data.size=.010; data.extrude=.00035; data.bevel_depth=.0001; data.bevel_resolution=0
            o=bpy.data.objects.new('Tire_Emboss_Glyph',data); COL['WHEELS'].objects.link(o)
            normal=Vector((s,0,0)); tx=Vector((0,s*math.sin(a),-s*math.cos(a))); ty=normal.cross(tx)
            o.matrix_world=Matrix(((tx.x,ty.x,normal.x,x+s*(w/2+.0032)),
                                  (tx.y,ty.y,normal.y,y+rr*math.cos(a)),
                                  (tx.z,ty.z,normal.z,z+rr*math.sin(a)),(0,0,0,1)))
            assign(o,emboss)
            bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
            bpy.ops.object.convert(target='MESH')
            glyphs.append(bpy.context.object)
    bpy.ops.object.select_all(action='DESELECT')
    for o in glyphs: o.select_set(True)
    bpy.context.view_layer.objects.active=glyphs[0]; bpy.ops.object.join()
    markings=bpy.context.object; markings.name='Tire_Sidewall_Markings_'+key
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    parent_world(markings,wheel)
    # Multi-piston sculpted caliper details without logos or redundant hardware.
    cal=bpy.data.objects['Caliper_'+key]
    cx,cy,cz=cal.data.vertices[0].co # existing caliper is modeled in world coordinates
    center=sum((v.co for v in cal.data.vertices),Vector())/len(cal.data.vertices)
    for i,offset in enumerate([-.057,0,.057],1):
        o=cylinder('Caliper_PistonBoss_'+key+'_'+str(i),(center.x+s*.031,center.y-.012,center.z+offset),.026,.010,calipermat,'BRAKES','X',40,.003)
    box('Caliper_Spine_'+key,(center.x+s*.037,center.y+.019,center.z),(.008,.022,.122),calipermat,'BRAKES',.007)
    # Hat attachment ring and geometric heat-relief scallops are visible through spokes.
    hat=bpy.data.objects['Brake_Hat_'+key]
    axial_ring('Brake_Hat_Rim_'+key,hat.location,[(-.018,.093),(.018,.093),(.018,.084),(-.018,.084)],accent,'BRAKES',segments=72)
    cal['stationary_when_wheel_rotates']=True
    rotor=bpy.data.objects['BrakeDisc_'+key]
    for p in rotor.data.polygons:
        p.use_smooth=abs(p.normal.x)<.8
    bevel(rotor,.0012,3)

# Subtle rear fascia breathing ribs behind the main recess, no engine modeled.
for i in range(9):
    x=lerp(-.78,.78,i/8)
    box('Rear_Vent_Rib_'+str(i+1),(x,2.115,.490),(.012,.055,.060),aero,'CAR',.004)

# All finite trim curves have caps; no accidental open tube ends.
for obj in bpy.data.objects:
    if obj.type=='CURVE': obj.data.use_fill_caps=True
for c in COL.values():
    for obj in c.objects:
        if obj.type=='MESH': clean_normals(obj.data)

scene['source_checkpoint']=str(SOURCE)
scene['milestone']='Exterior final design / topology pass; no interior, UV, LOD, collider or export production'
scene['panel_gap_nominal_m']=.0035
scene['exterior_light_signature']='Front bent grazing blade / rear separated staggered double strokes'
scene['main_vehicle_origin']='Car_Body at chassis XY center; wheels retain original local-X axle centers'

# Review cameras, including optical module and wheel closeups.
views={
 'exterior_front':camera('Camera_Front',(0,-8,1.70),(0,-.2,.58),4.1),
 'exterior_front_3q':camera('Camera_Presentation',(6,-8,3.65),(0,0,.55),5.85),
 'exterior_side':camera('Camera_Side',(12,0,1.755),(0,0,.57),5.5),
 'exterior_rear_3q':camera('Camera_Rear_ThreeQuarter',(6,8,3.25),(0,.1,.55),5.85),
 'exterior_rear':camera('Camera_Rear',(0,8,1.65),(0,.2,.59),4.1),
 'exterior_top_3q':camera('Camera_Top_ThreeQuarter',(5,-6,8),(0,0,.50),5.85),
 'exterior_headlight_closeup':camera('Camera_Headlight_Closeup',(2.25,-3.45,2.1),(.75,-1.88,.74),.95),
 'exterior_taillight_closeup':camera('Camera_Taillight_Closeup',(2.1,4.5,1.48),(.56,2.22,.68),1.10),
 'exterior_wheel_closeup':camera('Camera_Wheel_Closeup',(3.2,-2.3,1.10),(.825,-1.35,.345),1.03),
 'exterior_low_front':camera('Camera_Low_Front',(4,-7,1.25),(0,-.25,.45),5.65),
 'exterior_low_rear':camera('Camera_Low_Rear',(4,7,1.15),(0,.2,.45),5.65),
}
scene.render.engine='CYCLES'; scene.cycles.samples=48; scene.cycles.use_denoising=True
scene.render.resolution_x=1920; scene.render.resolution_y=1080; scene.render.resolution_percentage=100
scene.camera=views['exterior_front_3q']; scene.render.filepath=str(ROOT/'previews'/'exterior_front_3q.png')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.region_3d.view_rotation=scene.camera.rotation_euler.to_quaternion()
            space.region_3d.view_location=(0,0,.55); space.region_3d.view_distance=6.5
            space.shading.type='MATERIAL'; space.overlay.show_extras=False; space.overlay.show_floor=False
bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); bpy.context.view_layer.objects.active=body
for data in list(bpy.data.meshes):
    if data.users==0: bpy.data.meshes.remove(data)
notes=bpy.data.texts.new('READ_ME_Exterior_04')
notes.write('EXTERIOR PRODUCTION PASS — SOURCE 03 PRESERVED\n\nMetric; front -Y, up +Z. Original wheel centers and local X axles retained.\nActual separate door panels, smoothed arch endings, inset optical assemblies.\nLight materials have independent channels. Calipers remain stationary.\nMirrors/glazing/seals use consistent fitted surfaces. Four diffuser fins.\nLive modifiers retained. No final UV/textures, interior, LODs, collider or export.\nValidation and reflection/silhouette previews must be reviewed before approval.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(WORK))
review='--review' in sys.argv
if review:
    scene.render.resolution_percentage=67; scene.cycles.samples=24
    keys=['exterior_front_3q','exterior_rear_3q','exterior_side','exterior_headlight_closeup','exterior_taillight_closeup','exterior_wheel_closeup']
else:
    keys=list(views)[:9]
for key in keys:
    scene.camera=views[key]
    filename=('review_'+key if review else key)+'.png'
    scene.render.filepath=str(ROOT/'previews'/filename)
    bpy.ops.render.render(write_still=True)
