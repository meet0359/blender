"""Refine the EXISTING Phase 2 checkpoint in Blender; preserve axle locations.
No final interior, lighting internals, UV production, textures, or LODs.
"""
import bpy
import bmesh
import math
import json
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'racing_car_01_blockout.blend'
DEST=ROOT/'racing_car_03_realistic_body.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene
scene['source_checkpoint']=str(SOURCE)
scene['milestone']='Realistic body / greenhouse / wheels / brakes; downstream production deferred'
scene.render.engine='CYCLES'
scene.cycles.samples=48
scene.cycles.use_denoising=True
scene.render.resolution_x=1920
scene.render.resolution_y=1080
scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
COL={n:bpy.data.collections[n] for n in ['CAR','WHEELS','BRAKES','INTERIOR','GLASS','LIGHTS','COLLIDERS','LODS','REFERENCES','PRESENTATION']}

def material(name,color,metal=0,rough=.3,coat=0,trans=0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal
    p.inputs['Roughness'].default_value=rough
    p.inputs['Coat Weight'].default_value=coat
    p.inputs['Coat Roughness'].default_value=.16
    p.inputs['Transmission Weight'].default_value=trans
    m.diffuse_color=(*color,1)
    return m

paint=material('MAT_CarPaint',(.22,.009,.015),.72,.235,.38)
dark=material('MAT_BlackPlastic',(.012,.016,.021),.12,.32)
aero=material('MAT_Aero_Review',(.022,.028,.034),.42,.25,.25)
tiremat=material('MAT_Tire',(.009,.011,.013),0,.68)
tiremat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.24
alloy=material('MAT_Wheel_Alloy',(.31,.35,.40),.92,.22)
chrome=material('MAT_Chrome',(.48,.54,.60),.97,.16)
disc=material('MAT_BrakeDisc',(.23,.25,.27),.86,.38)
calipermat=material('MAT_BrakeCaliper',(.72,.25,.013),.5,.26,.3)
glass=material('MAT_Glass',(.027,.046,.059),.14,.085,.35,.30)
glass.node_tree.nodes.get('Principled BSDF').inputs['IOR'].default_value=1.46
lens=material('MAT_Light_Recess_Review',(.031,.046,.066),.48,.13,.4)
floor_mat=material('MAT_Studio_Floor',(.12,.135,.15),.08,.32)
slotmat=material('MAT_Recess_Depth',(.003,.004,.005),0,.72)
slotmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.08

def assign(o,m):
    o.data.materials.clear()
    o.data.materials.append(m)
    o.color=m.diffuse_color

def link(o,coll):
    for c in list(o.users_collection): c.objects.unlink(o)
    COL[coll].objects.link(o)
    return o

def clean_normals(data):
    bm=bmesh.new()
    bm.from_mesh(data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(data)
    bm.free()
    data.update()

def make_mesh(name,verts,faces,mat=paint,coll='CAR',smooth=True,reuse=True):
    data=bpy.data.meshes.new(name+'_Surface')
    data.from_pydata(verts,[],faces)
    data.update()
    o=bpy.data.objects.get(name) if reuse else None
    if o and o.type=='MESH':
        old=o.data
        o.modifiers.clear()
        o.data=data
        if old.users==0: bpy.data.meshes.remove(old)
    else:
        o=bpy.data.objects.new(name,data)
        COL[coll].objects.link(o)
    o.location=(0,0,0)
    o.rotation_euler=(0,0,0)
    o.scale=(1,1,1)
    assign(o,mat)
    clean_normals(data)
    for p in data.polygons: p.use_smooth=smooth
    return o

def sub(o,level=1):
    m=o.modifiers.new('Controlled surface refinement','SUBSURF')
    m.levels=level
    m.render_levels=level
    m.subdivision_type='CATMULL_CLARK'
    return m

def shell(o,thickness=.006):
    m=o.modifiers.new('Panel thickness','SOLIDIFY')
    m.thickness=thickness
    m.offset=-1

def bevel(o,width=.008,segments=3):
    m=o.modifiers.new('Controlled edge radius','BEVEL')
    m.width=width
    m.segments=segments
    m=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    m.keep_sharp=True

def patch(name,fn,nu,nv,mat=paint,coll='CAR',subdiv=0,thickness=.006):
    verts=[fn(i/nu,j/nv) for j in range(nv+1) for i in range(nu+1)]
    faces=[]
    for j in range(nv):
        for i in range(nu):
            a=j*(nu+1)+i
            faces.append((a,a+1,a+nu+2,a+nu+1))
    o=make_mesh(name,verts,faces,mat,coll)
    if subdiv: sub(o,subdiv)
    if thickness: shell(o,thickness)
    return o

def box(name,loc,dims,mat=dark,coll='CAR',radius=.012):
    # Existing names are replaced in place by mesh() when useful.
    x,y,z=[a/2 for a in dims]
    vs=[(loc[0]+sx*x,loc[1]+sy*y,loc[2]+sz*z) for sx,sy,sz in
        [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    o=make_mesh(name,vs,fs,mat,coll,False)
    if radius: bevel(o,radius)
    return o

def tube(name,points,radius,mat=paint,coll='CAR',cyclic=False,res=3):
    data=bpy.data.curves.new(name+'_Path','CURVE')
    data.dimensions='3D'
    data.resolution_u=1
    data.bevel_depth=radius
    data.bevel_resolution=res
    sp=data.splines.new('POLY')
    sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points): p.co=(*co,1)
    sp.use_cyclic_u=cyclic
    o=bpy.data.objects.new(name,data)
    COL[coll].objects.link(o)
    assign(o,mat)
    return o

def cylinder(name,loc,radius,depth,mat=alloy,coll='WHEELS',axis='X',vertices=64,edge=.003):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    o=link(bpy.context.object,coll)
    o.name=name
    o.data.name=name+'_Mesh'
    if axis=='X': o.rotation_euler.y=math.pi/2
    if axis=='Y': o.rotation_euler.x=math.pi/2
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    assign(o,mat)
    for p in o.data.polygons: p.use_smooth=len(p.vertices)==4
    if edge: bevel(o,edge,2)
    return o

def parent_world(child,parent):
    mat=child.matrix_world.copy()
    child.parent=parent
    child.matrix_world=mat

def lerp(a,b,t): return a+(b-a)*t
def smooth(t): return t*t*(3-2*t)
def gauss(x,c,w): return math.exp(-((x-c)/w)**2)

# Smooth monotonic cubic interpolation avoids the blockout's station kinks.
def interp(points,y):
    if y<=points[0][0]: return points[0][1]
    if y>=points[-1][0]: return points[-1][1]
    for k in range(len(points)-1):
        a,v=points[k]; b,w=points[k+1]
        if a<=y<=b:
            t=(y-a)/(b-a)
            m0=(w-points[max(0,k-1)][1])/(b-points[max(0,k-1)][0])
            m1=(points[min(len(points)-1,k+2)][1]-v)/(points[min(len(points)-1,k+2)][0]-a)
            return (2*t**3-3*t*t+1)*v+(t**3-2*t*t+t)*m0*(b-a)+(-2*t**3+3*t*t)*w+(t**3-t*t)*m1*(b-a)

width_points=[(-2.23,.84),(-2.0,.94),(-1.35,.985),(-.73,.92),(-.1,.90),(.50,.94),(1.35,.997),(1.86,.965),(2.23,.89)]
center_points=[(-2.23,.535),(-1.92,.59),(-1.35,.67),(-.94,.735),(-.45,.75),(.6,.77),(1.12,.80),(1.70,.79),(2.23,.70)]

def width(y): return interp(width_points,y)
def top_z(u,y):
    center=interp(center_points,y)
    shoulder=.078+.075*gauss(y,-1.35,.50)+.087*gauss(y,1.35,.62)
    # Fender volume rises beside, rather than across, the center hood.
    ridge=shoulder*math.exp(-((u-.80)/.31)**2)
    outer_drop=.046*(max(0,(u-.83)/.17)**2)
    hood_valley=.018*gauss(u,.48,.17)*gauss(y,-1.35,.65)
    tail_lift=.058*smooth(max(0,min(1,(y-2.015)/.215)))*(1-.05*u*u)
    return center+ridge-outer_drop-hood_valley+tail_lift

# Replace existing body data while retaining the original body object's identity.
ys=sorted(set([round(-2.23+4.46*i/100,7) for i in range(101)]+[-2.08,-.94,1.12,2.08,
    -1.745,-1.743,-1.742,-.958,-.957,-.955,.933,.936,.937,1.763,1.764,1.767,-.89,.46,.84]+[round(.34+.04*i,7) for i in range(16)]))
us=[i/20 for i in range(21)]
def body_y(u,y):
    return y+.15*u*u*gauss(y,-2.23,.27)-.13*u*u*gauss(y,2.23,.27)
tv=[(u*width(body_y(u,y)),body_y(u,y),top_z(u,body_y(u,y))) for y in ys for u in us]
groups={'Car_Body':[],'Hood':[],'Rear_Engine_Cover':[],'Cabin_Lower_Deck':[]}
for j in range(len(ys)-1):
    ym=(ys[j]+ys[j+1])/2
    for i in range(len(us)-1):
        um=(us[i]+us[i+1])/2
        name='Cabin_Lower_Deck' if -.94<ym<1.12 and um<.70 else ('Hood' if -2.08<ym<-.94 and um<.665 else ('Rear_Engine_Cover' if 1.12<ym<2.08 and um<.625 else 'Car_Body'))
        row=len(us)
        a=j*row+i
        groups[name].append((a,a+1,a+row+1,a+row))
for name,faces in groups.items():
    ids=sorted({a for f in faces for a in f}); remap={a:i for i,a in enumerate(ids)}
    o=make_mesh(name,[tv[a] for a in ids],[tuple(remap[a] for a in f) for f in faces],dark if name=='Cabin_Lower_Deck' else paint,'INTERIOR' if name=='Cabin_Lower_Deck' else 'CAR')
    m=o.modifiers.new('Preserved X symmetry','MIRROR'); m.use_clip=True
    if name=='Cabin_Lower_Deck':
        o.data.materials.append(paint)
        for p in o.data.polygons:
            p.material_index=1 if any(abs(o.data.vertices[i].co.x)>.47 for i in p.vertices) else 0
    else:
        sub(o,1); shell(o)

# Main side surfaces sculpt into the wheel arch contour; no extruded lip tubes.
def arch_bottom(y):
    bottom=.175
    for c,r,h in [(-1.35,.393,.345),(1.35,.414,.365)]:
        d=abs(y-c)
        if d<r: bottom=max(bottom,h+math.sqrt(max(0,r*r-d*d)))
    return bottom

side_ys=ys
def side_surface(base_y,t,s=1):
    y=body_y(1,base_y)
    fade=math.sin(math.pi*t)**.4
    y+=fade*((.36+.22*t-.46)*gauss(base_y,.46,.16)+(.92-.10*t-.84)*gauss(base_y,.84,.15))
    w=width(y); top=top_z(1,y); bottom=arch_bottom(y)
    z=lerp(top,bottom,t)
    arch=gauss(y,-1.35,.48)+gauss(y,1.35,.49)
    waist=.075*(1-min(1,arch))*(math.sin(math.pi*t)**1.3)
    x=w-.045*t-waist+.016*math.sin(math.pi*t)*min(1,arch)
    return s*x,y,z
sv=[]
for base_y in side_ys:
    for j in range(13):
        t=j/12
        sv.append(side_surface(base_y,t))
sf=[]
for i in range(len(side_ys)-1):
    ym=(side_ys[i]+side_ys[i+1])/2
    for j in range(12):
        # A genuine opening in the side mesh, with a recessed intake duct added below.
        if 3<=j<=9 and .46<ym<.84: continue
        a=i*13+j; sf.append((a,a+13,a+14,a+1))
# Weld the upper fender and side shoulder before subdivision, so their normals
# and curvature are continuous rather than two unrelated edge strips.
body=bpy.data.objects['Car_Body']
bv=[tuple(v.co) for v in body.data.vertices]
bf=[tuple(p.vertices) for p in body.data.polygons]
offset=len(bv)
o=make_mesh('Car_Body',bv+sv,bf+[tuple(a+offset for a in f) for f in sf])
m=o.modifiers.new('Preserved X symmetry','MIRROR'); m.use_clip=True
sub(o,1); shell(o,.007)

# Keep useful chassis; resculpt the exposed lower platform to the original clearance.
box('Chassis_Blockout',(0,0,.198),(1.47,3.68,.136),dark,radius=.055)
for name in ['Cabin_Roof_Blockout','Rear_Engine_Cover_Blockout']+[o.name for o in bpy.data.objects if o.name.startswith('Wheel_Arch_') or o.name.startswith('Wheel_Center_Placeholder_')]:
    o=bpy.data.objects.get(name)
    if o: bpy.data.objects.remove(o,do_unlink=True)

# Greenhouse. Roof is a crowned longitudinal spline, not a rounded box.
roof_points=[(-1.025,.735),(-.70,.895),(-.34,1.123),(-.10,1.184),(.22,1.200),(.48,1.166),(.70,1.09),(1.15,.817)]
cabin_width=[(-1.025,.746),(-.70,.689),(-.34,.605),(-.10,.575),(.22,.570),(.48,.580),(.70,.621),(1.15,.730)]

def greenhouse(u,y):
    w=interp(cabin_width,y)
    z=interp(roof_points,y)-(.074+.012*gauss(y,.2,.5))*u*u
    return (u*w,y,z)

def green_patch(name,y0,y1,mat):
    return patch(name,lambda u,v:greenhouse(2*u-1,lerp(y0,y1,v)),20,16,mat,'GLASS' if mat==glass else 'CAR',1,.004)

green_patch('Windshield',-1.012,-.298,glass)
roof=green_patch('Roof_Panel',-.29,.525,paint)
green_patch('Rear_Glass',.535,1.137,glass)
for name,y in [('Windshield_Cowl_Seal',-1.02),('Windshield_Header_Seal',-.295),('Rear_Glass_Header_Seal',.529),('Rear_Glass_Deck_Seal',1.142)]:
    tube(name,[greenhouse(-1+2*i/64,y) for i in range(65)],.009,dark,cyclic=False)
for s,label in [(-1,'L'),(1,'R')]:
    tube('Roof_Rail_'+label,[greenhouse(s,-1.018+2.165*i/100) for i in range(101)],.022,paint,res=4)
    # Main side glazing interpolates from the swept lower sill to the roof rail.
    def sideglass(u,v,s=s):
        # Coons surface uses exactly the same curved A/C pillars as the roof.
        a=Vector(greenhouse(s,lerp(-.87,-.298,v)))
        b=Vector(greenhouse(s,lerp(1.105,.72,v)))
        c=Vector(greenhouse(s,lerp(-.298,.72,u)))
        p00=Vector(greenhouse(s,-.87)); p10=Vector(greenhouse(s,1.105))
        p01=Vector(greenhouse(s,-.298)); p11=Vector(greenhouse(s,.72))
        d=p00.lerp(p10,u)
        d.z+=.018*math.sin(math.pi*u)
        blend=p00*(1-u)*(1-v)+p10*u*(1-v)+p01*(1-u)*v+p11*u*v
        p=a*(1-u)+b*u+d*(1-v)+c*v-blend
        p.x+=s*.009*math.sin(math.pi*u)*math.sin(math.pi*v)
        return tuple(p)
    patch('Window_F'+label,lambda u,v:sideglass(.77*u,v),30,14,glass,'GLASS',1,.003)
    patch('Window_R'+label,lambda u,v:sideglass(.79+.21*u,v),12,14,glass,'GLASS',1,.003)
    tube('Window_Belt_Seal_'+label,[sideglass(i/80,0) for i in range(81)],.013,dark)
    tube('Window_B_Pillar_'+label,[sideglass(.78,i/24) for i in range(25)],.014,paint)
    tube('A_Pillar_'+label,[greenhouse(s,lerp(-1.018,-.298,i/48)) for i in range(49)],.024,paint,res=4)
    tube('Rear_Cabin_Buttress_'+label,[sideglass(1,i/40) for i in range(41)],.031,paint,res=4)
    # A broad sculpted flying-buttress volume ties cabin to the shoulder.
    def buttress(u,v,s=s):
        y=lerp(.68,1.42,u)
        x=lerp(interp(cabin_width,min(y,1.15)),width(y)*.85,v)
        z=lerp(interp(roof_points,min(y,1.15))-.075,top_z(.85,y),v)
        z+=.022*math.sin(math.pi*v)*math.sin(math.pi*u)
        return s*x,y,z
    patch('Rear_Buttress_Surface_'+label,buttress,24,8,paint,'CAR',1,.007)

# A simple dark cavity keeps tinted windows readable without building an interior.
box('Cabin_Shadow_Tray',(0,.08,.685),(1.42,1.87,.12),slotmat,'INTERIOR',.08)

# Wrapped bumper ribbons expose physical negative-space apertures.
def front_y(x): return -2.245+.19*(abs(x)/.98)**2
def front_band(u,v):
    q=2*u-1
    upper_y=body_y(abs(q),-2.23)
    x=q*width(upper_y)
    z=lerp(.438+.020*q*q,top_z(abs(q),upper_y),v)
    y=lerp(front_y(x),upper_y,v)
    return x,y,z
patch('Front_Bumper',front_band,64,8,paint,'CAR',1,.010)

def fascia_loop(name,coords,front=True,depth=.14,mat=paint):
    # Rounded 2D opening. Four support rings connect painted surface to a black throat.
    # coords sampled from Bezier outline; aperture geometry remains editable quads.
    center=Vector((sum(p[0] for p in coords)/len(coords),sum(p[1] for p in coords)/len(coords)))
    verts=[]
    for offset,zoff,yd in [(1.13,0,0),(1.035,0,-.003),(1,0,.018),(.96,0,depth)]:
        for x,z in coords:
            dx,dz=Vector((x,z))-center
            xx=center.x+dx*offset; zz=center.y+dz*offset
            yy=(front_y(xx) if front else 2.23-.12*(abs(xx)/.98)**2)+(yd if front else -yd)
            verts.append((xx,yy,zz))
    n=len(coords)
    faces=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
    o=make_mesh(name,verts,faces,mat)
    sub(o,1); shell(o,.004)
    # Flat black inset at depth is intentionally simplified, not a grille mesh.
    inner=verts[3*n:]
    make_mesh(name+'_Depth',inner,[tuple(range(n))],slotmat,smooth=False)
    return o

def rounded_polygon(points,r=.15,steps=6):
    pts=[]
    for i,p in enumerate(points):
        a=Vector(points[i-1]); b=Vector(p); c=Vector(points[(i+1)%len(points)])
        left=b+(a-b)*r; right=b+(c-b)*r
        for j in range(steps):
            t=j/steps
            q=(1-t)**2*left+2*(1-t)*t*b+t*t*right
            pts.append(tuple(q))
    return pts

fascia_loop('Front_Central_Intake',rounded_polygon([(-.535,.407),(.535,.407),(.46,.215),(-.46,.215)],.16),True,.17)
for s,label in [(-1,'L'),(1,'R')]:
    pts=[(s*.605,.431),(s*.906,.477),(s*.893,.249),(s*.574,.230)]
    fascia_loop('Front_Cooling_Duct_'+label,rounded_polygon(pts,.20),True,.18)
    # The primary body's welded side surface now wraps around the front corner.

def splitter(u,v):
    x=lerp(-.978,.978,u)
    y=lerp(-2.29+.12*(abs(x)/.978)**2,-2.045+.13*(abs(x)/.978)**2,v)
    return x,y,.142+.013*(abs(x)/.978)**2+.008*v
patch('Front_Splitter',splitter,64,8,aero,'CAR',1,.021)
# Nose/bumper shut line just under hood crown.
tube('Front_Nose_Shutline',[(lerp(-.86,.86,i/80),-2.092,top_z(abs(lerp(-.86,.86,i/80))/width(-2.092),-2.092)+.002) for i in range(81)],.0017,dark,res=1)

# Narrow swept headlight recesses lie flush with each fender, not on top of it.
for s,label in [(-1,'L'),(1,'R')]:
    def headlight(u,v,s=s):
        y=lerp(-2.048,-1.695,v)+.035*(u-.5)
        q=lerp(.715,.875,u)-.022*v
        return s*q*width(y),y,top_z(q,y)+.006
    patch('Headlight_'+label,headlight,10,24,lens,'LIGHTS',1,.004)
    boundary=[headlight(i/24,0) for i in range(25)]+[headlight(1,i/24) for i in range(1,25)]+[headlight(1-i/24,1) for i in range(1,25)]+[headlight(0,1-i/24) for i in range(1,24)]
    tube('Headlight_Recess_Rim_'+label,boundary,.006,dark,'LIGHTS',True,2)

# Door shutlines run across a compound concave flank.
def side_at(y,z,s):
    top=top_z(1,y); bot=arch_bottom(y)
    t=max(0,min(1,(top-z)/(top-bot)))
    arch=gauss(y,-1.35,.48)+gauss(y,1.35,.49)
    x=width(y)-.045*t-.075*(1-min(1,arch))*math.sin(math.pi*t)**1.3+.016*math.sin(math.pi*t)*min(1,arch)
    return s*(x+.003),y,z

for s,label in [(-1,'L'),(1,'R')]:
    outline=[]
    for i in range(32):
        t=i/31; y=lerp(-.865,.46,t)
        outline.append(side_at(y,top_z(1,y)-.045,s))
    for i in range(1,24):
        t=i/23; outline.append(side_at(.46-.11*t,lerp(top_z(1,.46)-.045,.258,t),s))
    for i in range(1,32):
        t=i/31; outline.append(side_at(lerp(.35,-.77,t),.258-.018*math.sin(math.pi*t),s))
    for i in range(1,24):
        t=i/23; outline.append(side_at(lerp(-.77,-.865,t),lerp(.258,top_z(1,-.865)-.045,t),s))
    tube('Door_Panel_Gap_'+label,outline,.0016,dark,cyclic=True,res=1)
    # Deep intake throat built into the opening, with a swept upper scoop.
    # Opening edges and duct rim share the exact side-surface parameterization.
    coords=[side_surface(lerp(.46,.84,i/24),.25,s) for i in range(25)]
    coords += [side_surface(.84,lerp(.25,10/12,i/24),s) for i in range(1,25)]
    coords += [side_surface(lerp(.84,.46,i/24),10/12,s) for i in range(1,25)]
    coords += [side_surface(.46,lerp(10/12,.25,i/24),s) for i in range(1,24)]
    inner=[(s*.79,y+.05,z) for x,y,z in coords]
    n=len(coords)
    fs=[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]+[tuple(range(n,2*n))]
    throat=make_mesh('Side_Intake_Throat_'+label,coords+inner,fs,slotmat)
    tube('Side_Intake_Trim_'+label,coords,.0035,dark,cyclic=True,res=2)
    def scoop(u,v,s=s):
        y=lerp(.30,.95,u)
        upper=.718+.05*u
        lower=.275+.10*u
        z=lerp(lower,upper,v)
        x=lerp(.884,.985,u)-.035*math.sin(math.pi*v)
        # lower and outer surround creates the negative space leading into haunch.
        return s*x,y,z
    def sill(u,v,s=s):
        y=lerp(-.905,.921,u)
        x=s*(.857+.074*v+.018*math.sin(math.pi*u))
        return x,y,.149+.065*math.sin(math.pi*v/2)+.022*math.sin(math.pi*u)
    patch('Side_Skirt_'+label,sill,48,8,aero,'CAR',1,.014)
    # Flush handle is only a broad design cue, no mechanical detail.
    tube('Door_Handle_Recess_'+label,[side_at(.16+i*.14/12,.67,s) for i in range(13)],.005,dark,res=2)

# Rear deck rolls up into a subtle ducktail; center rear has a deep physical recess.
def rear_y(x): return 2.245-.13*(abs(x)/.96)**2
def rearband(u,v):
    q=2*u-1
    upper_y=body_y(abs(q),2.23)
    x=q*width(upper_y)
    z=lerp(.575+.02*q*q,top_z(abs(q),upper_y),v)
    return x,lerp(rear_y(x),upper_y,v),z
patch('Rear_Bumper',rearband,64,10,paint,'CAR',1,.01)
fascia_loop('Rear_Center_Recess',rounded_polygon([(-.85,.544),(.85,.544),(.78,.34),(-.78,.34)],.1),False,.165,aero)
for s,label in [(-1,'L'),(1,'R')]:
    # A single smoked placeholder blade; no LED or projector internals.
    patch('Taillight_'+label,lambda u,v,s=s:(s*lerp(.16,.873,u),rear_y(lerp(.16,.873,u))+.008,
        .624+.023*v+.045*u*u),40,4,lens,'LIGHTS',1,.004)

def ducktail(u,v):
    x=lerp(-.902,.902,u)
    y=lerp(2.032,2.225,v)-.041*(abs(x)/.902)**2
    q=abs(x)/width(y)
    return x,y,top_z(q,y)+.004
patch('Rear_Wing',ducktail,48,12,paint,'CAR',1,.01)

def diffuser(u,v):
    x=lerp(-.865,.865,u)
    return x,lerp(1.70,2.258,v),.14+.169*smooth(v)+.012*abs(x)
patch('Rear_Diffuser',diffuser,24,12,aero,'CAR',0,.012)
for i,x in enumerate([-.66,-.40,-.16,.16,.40,.66]):
    # Upright swept fins, modest height and lift angle.
    verts=[(x-.006,1.80,.145),(x-.006,2.24,.155),(x-.006,2.24,.319),(x-.006,1.86,.219),
           (x+.006,1.80,.145),(x+.006,2.24,.155),(x+.006,2.24,.319),(x+.006,1.86,.219)]
    faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    o=make_mesh('Diffuser_Fin_'+str(i+1),verts,faces,aero,smooth=False); bevel(o,.003,2)

# A pair of hollow outlets provides scale and depth, without exhaust hardware.
def axial_ring(name,center,profile,mat,coll='WHEELS',axis='X',segments=96):
    verts=[]
    for ax,r in profile:
        for i in range(segments):
            a=2*math.pi*i/segments
            p=(ax,r*math.cos(a),r*math.sin(a)) if axis=='X' else (r*math.cos(a),ax,r*math.sin(a))
            verts.append(p)
    faces=[]
    for j in range(len(profile)):
        for i in range(segments):
            a=j*segments+i; b=j*segments+(i+1)%segments
            c=((j+1)%len(profile))*segments+(i+1)%segments; d=((j+1)%len(profile))*segments+i
            faces.append((a,b,c,d))
    o=make_mesh(name,verts,faces,mat,coll)
    o.location=center
    bpy.context.view_layer.update()
    return o

for s,label in [(-1,'L'),(1,'R')]:
    axial_ring('Exhaust_'+label,(s*.63,2.155,.385),[(-.07,.062),(.093,.062),(.10,.056),(.085,.048),(-.07,.048)],chrome,'CAR','Y',48)
    cylinder('Exhaust_Depth_'+label,(s*.63,2.105,.385),.048,.005,slotmat,'CAR','Y',48,0)

# Engine ventilation concept: two broad recessed regions, not dozens of tiny slats.
for s,label in [(-1,'L'),(1,'R')]:
    patch('Engine_Vent_Region_'+label,lambda u,v,s=s:(s*lerp(.20,.47,u),lerp(1.33,1.92,v),
        top_z(lerp(.20,.47,u)/width(lerp(1.33,1.92,v)),lerp(1.33,1.92,v))+.004),12,22,aero,'CAR',1,.003)

# Preserve wheel objects/origins; replace their mesh data with sculpted tires.
for key,x,y,r,w,rim_r in [('FL',-.825,-1.35,.345,.29,.254),('FR',.825,-1.35,.345,.29,.254),
                         ('RL',-.835,1.35,.365,.33,.267),('RR',.835,1.35,.365,.33,.267)]:
    old=bpy.data.objects['Wheel_'+key]
    center=old.location.copy()
    s=-1 if x<0 else 1
    # Profile loops incorporate two circumferential tread grooves.
    profile=[(-w/2+.015,rim_r-.006),(-w/2,rim_r+.01),(-w/2-.003,r-.045),
             (-w/2+.014,r-.013),(-w/2+.036,r-.002),(-.065,r),(-.058,r-.004),(-.050,r-.004),(-.043,r),
             (.043,r),(.050,r-.004),(.058,r-.004),(.065,r),(w/2-.036,r-.002),(w/2-.014,r-.013),
             (w/2+.003,r-.045),(w/2,rim_r+.01),(w/2-.015,rim_r-.006),(.0,rim_r-.009)]
    n=112
    verts=[]
    for ax,rr in profile:
        for i in range(n):
            a=2*math.pi*i/n
            zz=rr*math.sin(a)
            # Very subtle contact flattening: 1.5 mm, axle height unchanged.
            zz=max(zz,-r+.0015)
            verts.append((ax,rr*math.cos(a),zz))
    faces=[]
    for j in range(len(profile)):
        for i in range(n):
            faces.append((j*n+i,j*n+(i+1)%n,((j+1)%len(profile))*n+(i+1)%n,((j+1)%len(profile))*n+i))
    wheel=make_mesh('Wheel_'+key,verts,faces,tiremat,'WHEELS')
    wheel.location=center
    wheel['diameter_m']=2*r
    wheel['axle_axis']='X'
    wheel['description']='Tire master with wheel components parented; brake caliper intentionally independent'
    # Real shallow wheel wells eliminate see-through gaps behind the arch.
    patch('Wheel_Well_'+key,lambda u,v,x=x,y=y,r=r,w=w,s=s:(
        lerp(x-s*(w/2+.02),x+s*(w/2-.006),u),
        y+(r+.027)*math.cos(lerp(-.46,math.pi+.46,v)),
        r+(r+.027)*math.sin(lerp(-.46,math.pi+.46,v))),4,48,slotmat,'CAR',0,.003)
    # All rotating components use parented separate objects and stay editable.
    face=x+s*(w/2-.009)
    rim=axial_ring('Rim_Barrel_'+key,(x,y,r),[(-w/2+.015,rim_r),(-w/2+.015,rim_r-.011),
        (w/2-.015,rim_r-.011),(w/2-.015,rim_r)],alloy)
    parent_world(rim,wheel)
    lip=axial_ring('Rim_Outer_Lip_'+key,(face,y,r),[(-.012,rim_r),(.004,rim_r),(.009,rim_r-.009),
        (.001,rim_r-.018),(-.012,rim_r-.018)],chrome)
    parent_world(lip,wheel)
    hub=cylinder('Wheel_Hub_'+key,(face-s*.032,y,r),.059,.047,alloy)
    parent_world(hub,wheel)
    cap=cylinder('Wheel_Center_Cap_'+key,(face+s*.002,y,r),.031,.009,aero,vertices=48)
    parent_world(cap,wheel)
    # Five split pairs form a light concave ten-spoke wheel.
    for k in range(5):
        for branch in [-1,1]:
            angle=2*math.pi*k/5+branch*.09
            vs=[]
            for radius,tanwidth,bend,depth in [(.050,.012,0,-.040),(.12,.010,branch*.06,-.026),
                    (.205,.008,branch*.095,-.004),(.238,.009,branch*.11,0)]:
                aa=angle+bend
                for axoff,ts in [(-.009,-1),(-.009,1),(.009,1),(.009,-1)]:
                    yy=y+radius*math.cos(aa)-ts*tanwidth*math.sin(aa)
                    zz=r+radius*math.sin(aa)+ts*tanwidth*math.cos(aa)
                    vs.append((face+s*(depth+axoff),yy,zz))
            fs=[]
            for j in range(3):
                for q in range(4): fs.append((j*4+q,j*4+(q+1)%4,(j+1)*4+(q+1)%4,(j+1)*4+q))
            fs.extend([(3,2,1,0),(12,13,14,15)])
            spoke=make_mesh('Wheel_Spoke_'+key+'_'+str(k+1)+('_A' if branch<0 else '_B'),vs,fs,alloy,'WHEELS',False)
            bevel(spoke,.003,3); parent_world(spoke,wheel)
    for k in range(5):
        a=2*math.pi*k/5
        lug=cylinder('Wheel_Lug_'+key+'_'+str(k+1),(face+s*.003,y+.043*math.cos(a),r+.043*math.sin(a)),.006,.012,chrome,vertices=12,edge=.001)
        parent_world(lug,wheel)
    # Disc, central hat and caliper remain independent of the tire parent.
    rotor_x=face-s*.060
    rotor=axial_ring('BrakeDisc_'+key,(rotor_x,y,r),[(-.012,.216),(.012,.216),(.012,.092),(-.012,.092)],disc,'BRAKES',segments=96)
    rotor['axle_axis']='X'; rotor['component']='Ventilated rotor; independent of wheel master'
    cylinder('Brake_Hat_'+key,(rotor_x+s*.004,y,r),.093,.034,aero,'BRAKES',vertices=64)
    # Visible radial slots are deliberately moderate, with generic geometry.
    for k in range(18):
        a=2*math.pi*k/18
        pts=[]
        for j in range(7):
            rr=lerp(.146,.199,j/6)
            aa=a+.065*j/6
            pts.append((rotor_x+s*.013,y+rr*math.cos(aa),r+rr*math.sin(aa)))
        tube('Brake_Radial_Slot_'+key+'_'+str(k+1),pts,.0012,slotmat,'BRAKES',False,1)
    for k in range(18):
        a=2*math.pi*k/18
        # Internal black separator blocks indicate disc ventilation around edge.
        o=box('Brake_Vent_'+key+'_'+str(k+1),(rotor_x,y+.215*math.cos(a),r+.215*math.sin(a)),(.012,.009,.009),slotmat,'BRAKES',.001)
    cal=box('Caliper_'+key,(rotor_x+s*.016,y+.164,r+.055),(.067,.079,.183),calipermat,'BRAKES',.026)
    cal['stationary_when_wheel_rotates']=True
    box('Caliper_Bridge_'+key,(rotor_x+s*.052,y+.166,r+.055),(.023,.071,.100),calipermat,'BRAKES',.01)

# Small mirrors are broad primary exterior volumes, without mechanical internals.
for s,label in [(-1,'L'),(1,'R')]:
    tube('Mirror_Stem_'+label,[(s*.754,-.68,.80),(s*.853,-.63,.824),(s*.915,-.61,.845)],.016,aero)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=(s*.925,-.605,.859))
    o=link(bpy.context.object,'CAR'); o.name='Mirror_'+label
    o.scale=(.075,.132,.043)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    assign(o,paint)
    for p in o.data.polygons: p.use_smooth=True
    patch('Mirror_Glass_'+label,lambda u,v,s=s:(s*(.883+.08*u),-.481,.84+.034*v),12,6,chrome,'GLASS',1,.002)

# Studio uses large emitter cards, revealing curvature without external textures.
floor=bpy.data.objects['Blockout_Review_Floor']
floor.hide_set(False)
assign(floor,floor_mat)
floor.name='Studio_Floor'
floor.location.z=-.025
world=scene.world
world.use_nodes=True
world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.19,.22,.27,1)
world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.25

def area(name,loc,target,power,size,size_y,color=(1,1,1)):
    data=bpy.data.lights.new(name,'AREA')
    data.energy=power; data.shape='RECTANGLE'; data.size=size; data.size_y=size_y; data.color=color
    o=bpy.data.objects.new(name,data); COL['PRESENTATION'].objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o

area('Studio_Key_Softbox',(2.0,-2.3,5.7),(0,0,.3),1400,5.0,2.2,(1.0,.91,.84))
area('Studio_Fill_Softbox',(-4,-1,3.0),(0,0,.6),900,4.0,2.6,(.81,.89,1))
area('Studio_Rear_Rim',(1.0,4.0,3.8),(0,.6,.5),1400,4.0,1.0)
area('Studio_Side_Strip',(4,.1,2.1),(0,0,.6),700,4.8,.65)
area('Studio_Front_Strip',(0,-4,2.8),(0,-1,.5),600,3.5,.6)

def camera(name,loc,target,scale=5.8):
    o=bpy.data.objects.get(name)
    if not o:
        data=bpy.data.cameras.new(name); o=bpy.data.objects.new(name,data); COL['PRESENTATION'].objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.type='ORTHO'; o.data.ortho_scale=scale; o.data.lens=55
    return o

cameras={
    'realistic_front':camera('Camera_Front',(0,-8,1.70),(0,-.2,.58),4.1),
    'realistic_side':camera('Camera_Side',(12,0,1.755),(0,0,.57),5.50),
    'realistic_rear':camera('Camera_Rear',(0,8,1.65),(0,.2,.59),4.1),
    'realistic_front_3q':camera('Camera_Presentation',(6,-8,3.8),(0,0,.55),5.85),
    'realistic_rear_3q':camera('Camera_Rear_ThreeQuarter',(6,8,3.4),(0,.1,.55),5.85),
}
scene.camera=cameras['realistic_front_3q']
for key,name in [('FL','Front_Axle_Reference'),('RL','Rear_Axle_Reference')]:
    bpy.data.objects[name].location.z=bpy.data.objects['Wheel_'+key].location.z
scene.render.filepath=str(ROOT/'previews'/'realistic_front_3q.png')
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            space=a.spaces.active
            space.region_3d.view_rotation=scene.camera.rotation_euler.to_quaternion()
            space.region_3d.view_location=(0,0,.55); space.region_3d.view_distance=6.4
            space.shading.type='MATERIAL'; space.overlay.show_extras=False; space.overlay.show_floor=False
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Car_Body'].select_set(True); bpy.context.view_layer.objects.active=bpy.data.objects['Car_Body']

text=bpy.data.texts.new('READ_ME_Realistic_Body')
text.write('REFINED FROM racing_car_01_blockout.blend\nMetric, front -Y, up +Z, wheel axle local X.\nAll four wheel origins and the 2.70 m wheelbase are retained.\nWheel geometry: tires + child alloy components. Brakes are independent.\nLive Mirror, Subdivision, Solidify and Bevel retained where useful.\nStudio materials are temporary surface-review shaders, not final textures.\nGlass and light recesses are broad design placeholders.\nNo detailed interior, LEDs, final UVs/textures, collider or LODs.\nOriginal source checkpoint is unchanged.\n')
# Purge only unused mesh datablocks produced during replacements.
for data in list(bpy.data.meshes):
    if data.users==0: bpy.data.meshes.remove(data)
bpy.ops.wm.save_as_mainfile(filepath=str(DEST))

import os
selected=os.environ.get('CAR_RENDER_VIEWS','realistic_front_3q,realistic_side,realistic_rear_3q,realistic_front,realistic_rear').split(',')
for key in selected:
    if key not in cameras: continue
    scene.camera=cameras[key]
    scene.render.filepath=str(ROOT/'previews'/(key+'.png'))
    bpy.ops.render.render(write_still=True)
