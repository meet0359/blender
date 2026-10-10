"""Editable original two-seat cockpit, built inside exterior checkpoint 04."""
import bpy,bmesh,math,json,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'racing_car_04_exterior_final.blend'))
s=bpy.context.scene
source_hash=hashlib.sha256((ROOT/'racing_car_04_exterior_final.blend').read_bytes()).hexdigest()
interior=bpy.data.collections['INTERIOR']
COL={}
for short in ['MAIN','SEATS','CONTROLS','TRIM']:
    name='INTERIOR_'+short
    c=bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in interior.children: interior.children.link(c)
    COL[short]=c
for o in list(interior.all_objects): bpy.data.objects.remove(o,do_unlink=True)

def material(name,color,metal=0,rough=.45):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
    m.diffuse_color=(*color,1)
    return m
leather=material('MAT_InteriorLeather',(.008,.011,.015),0,.4)
plastic=material('MAT_InteriorPlastic',(.005,.008,.011),0,.52)
alcantara=material('MAT_InteriorAlcantara',(.028,.033,.04),0,.8)
carbon=material('MAT_InteriorCarbon',(.008,.011,.014),.25,.28)
metal=material('MAT_InteriorMetal',(.075,.095,.11),.78,.3)
display=material('MAT_Display',(.008,.018,.025),.05,.15)
accent=material('MAT_SeatAccent',(.34,.018,.025),0,.52)
speaker=material('MAT_Speaker',(.016,.02,.023),.1,.7)
glassmat=bpy.data.materials['MAT_Glass']
p=glassmat.node_tree.nodes.get('Principled BSDF')
p.inputs['Base Color'].default_value=(.72,.80,.86,1)
p.inputs['Transmission Weight'].default_value=1
p.inputs['Roughness'].default_value=.025
glassmat['interior_review_change']='Reduced tint and full transmission for cabin visibility; geometry preserved'

def mesh(name,verts,faces,mat=plastic,coll='MAIN',smooth=True):
    me=bpy.data.meshes.new(name+'_Mesh'); me.from_pydata(verts,[],faces); me.update()
    bm=bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new(name,me); COL[coll].objects.link(o)
    me.materials.append(mat)
    for p in me.polygons: p.use_smooth=smooth
    o.color=mat.diffuse_color
    return o
def bevel(o,w=.004,n=3):
    m=o.modifiers.new('Soft manufactured edges','BEVEL'); m.width=w; m.segments=n
    m.harden_normals=True
    for p in o.data.polygons: p.use_smooth=True
    m=o.modifiers.new('Weighted panel normals','WEIGHTED_NORMAL'); m.keep_sharp=True
    return o
def sub(o):
    m=o.modifiers.new('Surface refinement','SUBSURF'); m.levels=1; m.render_levels=1
    return o
def solid(o,t=.004):
    m=o.modifiers.new('Physical panel thickness','SOLIDIFY'); m.thickness=t; m.offset=-1
    return o
def origin(o,pt):
    delta=Vector(pt)
    bpy.context.view_layer.update()
    o.data.transform(Matrix.Translation(-delta)@o.matrix_world)
    o.matrix_world=Matrix.Translation(delta)
    return o
def parent(o,root):
    bpy.context.view_layer.update(); mat=o.matrix_world.copy(); o.parent=root; o.matrix_world=mat
    return o
def box(name,loc,dim,mat=plastic,coll='MAIN',radius=.008,basis=None):
    B=basis or Matrix.Identity(3)
    vs=[Vector(loc)+B@Vector((x*dim[0]/2,y*dim[1]/2,z*dim[2]/2)) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    o=mesh(name,vs,fs,mat,coll,False); origin(o,loc)
    if radius: bevel(o,radius,3)
    return o
def patch(name,fn,nu,nv,mat,coll='MAIN',thick=.004,refine=True):
    vs=[fn(i/nu,j/nv) for j in range(nv+1) for i in range(nu+1)]
    fs=[]
    for j in range(nv):
        for i in range(nu):
            a=j*(nu+1)+i; fs.append((a,a+1,a+nu+2,a+nu+1))
    o=mesh(name,vs,fs,mat,coll)
    if refine: sub(o)
    if thick: solid(o,thick)
    return o
def tube(name,pts,r,mat=accent,coll='TRIM',closed=False,sides=8):
    vs=[]; P=[Vector(p) for p in pts]; N=len(P)
    for i,p in enumerate(P):
        tangent=(P[(i+1)%N]-P[(i-1)%N]).normalized() if closed else (P[min(i+1,N-1)]-P[max(0,i-1)]).normalized()
        ref=Vector((0,0,1)) if abs(tangent.z)<.93 else Vector((1,0,0))
        a=tangent.cross(ref).normalized(); b=tangent.cross(a).normalized()
        for k in range(sides):
            q=2*math.pi*k/sides; vs.append(p+r*(math.cos(q)*a+math.sin(q)*b))
    fs=[]
    for i in range(N if closed else N-1):
        j=(i+1)%N
        for k in range(sides): fs.append((i*sides+k,i*sides+(k+1)%sides,j*sides+(k+1)%sides,j*sides+k))
    if not closed: fs.extend([tuple(range(sides-1,-1,-1)),tuple((N-1)*sides+k for k in range(sides))])
    return mesh(name,vs,fs,mat,coll)
def cyl(name,center,r,depth,mat=metal,coll='CONTROLS',axis=(0,0,1),n=32):
    normal=Vector(axis).normalized(); ref=Vector((1,0,0)) if abs(normal.x)<.9 else Vector((0,1,0))
    a=normal.cross(ref).normalized(); b=normal.cross(a).normalized(); C=Vector(center)
    vs=[C+normal*z+ r*(math.cos(2*math.pi*i/n)*a+math.sin(2*math.pi*i/n)*b) for z in [-depth/2,depth/2] for i in range(n)]
    fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    o=mesh(name,vs,fs,mat,coll)
    for p in o.data.polygons:
        if len(p.vertices)>4: p.use_smooth=False
    origin(o,center); bevel(o,min(.0015,depth*.15),2)
    return o
def lerp(a,b,t): return a+(b-a)*t
def smooth(t): return t*t*(3-2*t)
def profile(points,t):
    for (a,b),(c,d) in zip(points,points[1:]):
        if a<=t<=c: return lerp(b,d,smooth((t-a)/(c-a)))
    return points[0][1] if t<points[0][0] else points[-1][1]
def rounded_outline(w,h,r,n=6):
    pts=[]
    for cx,cy,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
        for i in range(n):
            a=math.radians(start+90*i/(n-1)); pts.append((cx+r*math.sin(a),cy+r*math.cos(a)))
    # Traverse corners clockwise with a standard parameterization instead.
    pts=[]
    for cx,cy,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
        for i in range(n):
            a=math.radians(start+90*i/(n-1)); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts

# Sculpted floor tub with two recessed footwells, rising rear shelf and firewall.
def floor_surface(u,v):
    x=lerp(-.70,.70,u); y=lerp(-1.12,.73,v)
    z=.255+.032*math.exp(-((y-.65)/.17)**2)+.040*(abs(x)/.70)**8
    return x,y,z
floor=patch('Floor',floor_surface,28,32,plastic,thick=.012)
box('LowerFirewall',(0,-1.10,.46),(1.34,.035,.39),plastic,radius=.025)
box('RearBulkhead',(0,.76,.58),(1.16,.065,.60),alcantara,radius=.045)
box('RearBulkhead_UpperShelf',(0,.87,.823),(1.20,.20,.04),leather,radius=.018)
for sx in [-1,1]:
    x=sx*.36
    box('Footwell_Mat_'+('L' if sx<0 else 'R'),(x,-.53,.269),(.46,.70,.013),alcantara,radius=.035)
    box('Seat_Rail_Inner_'+str(sx),(x-sx*.14,.20,.289),(.026,.56,.029),metal,radius=.005)
    box('Seat_Rail_Outer_'+str(sx),(x+sx*.14,.20,.289),(.026,.56,.029),metal,radius=.005)
    box('InnerSill_'+('L' if sx<0 else 'R'),(sx*.742,-.21,.36),(.08,1.30,.20),carbon,radius=.025)

# Continuous tunnel: broad forward support, narrow controls, rear shoulder.
stations=[(-1.08,.15,.43),(-.85,.15,.49),(-.59,.135,.60),(-.39,.115,.59),(-.1,.105,.51),(.25,.11,.48),(.63,.14,.54),(.75,.145,.59)]
vs=[]
for y,w,z in stations:
    for x,zz in [(-w,.265),(-w,z-.035),(-w+.025,z),(w-.025,z),(w,z-.035),(w,.265)]: vs.append((x,y,zz))
fs=[]
for j in range(len(stations)-1):
    for k in range(6): fs.append((j*6+k,j*6+(k+1)%6,(j+1)*6+(k+1)%6,(j+1)*6+k))
fs.extend([tuple(range(5,-1,-1)),tuple((len(stations)-1)*6+k for k in range(6))])
tunnel=mesh('TransmissionTunnel',vs,fs,plastic); bevel(tunnel,.014,4)
console=box('CenterConsole',(0,-.045,.514),(.19,.58,.039),carbon,radius=.028)
box('CenterConsole_Armrest',(0,.44,.542),(.215,.30,.095),leather,radius=.036)
for sx in [-1,1]:
    tube('Console_Red_Seam_'+str(sx),[(sx*.097,lerp(-.30,.28,i/40),.535-.008*math.sin(math.pi*i/40)) for i in range(41)],.0012)

# Seat shells and upholstered grids. Front is -Y; recline moves upward sections aft.
def back_params(v):
    z=lerp(.385,1.035,v); y=.18+.335*v
    w=profile([(0,.175),(.17,.205),(.56,.222),(.70,.223),(.78,.145),(.88,.128),(1,.121)],v)
    return y,z,w
for label,xc in [('Driver',-.36),('Passenger',.36)]:
    def shellfn(u,v):
        q=2*u-1; y,z,w=back_params(v)
        return xc+q*w,y+.044-.084*abs(q)**3*(math.sin(math.pi*v)*.55+.45),z
    seat=patch('Seat_'+label,shellfn,24,32,carbon,'SEATS',.012,True)
    origin(seat,(xc,.21,.335)); seat['seat_recline_degrees']=27.25
    def backpad(u,v):
        q=2*u-1; vv=.055+.735*v; y,z,w=back_params(vv)
        return xc+q*w*.71,y-.014-.012*(1-q*q)*math.sin(math.pi*v),z
    pad=patch('Seat_'+label+'_BackrestPad',backpad,18,24,alcantara,'SEATS',.031,True); parent(pad,seat)
    def cushion(u,v):
        q=2*u-1; y=lerp(-.25,.245,v)
        z=.342+.032*(1-v)**2+.035*abs(q)**3-.012*math.sin(math.pi*v)*(1-q*q)
        return xc+q*(.197+.012*math.sin(math.pi*v)),y,z
    cushionobj=patch('Seat_'+label+'_Cushion',cushion,24,26,leather,'SEATS',.045,True); parent(cushionobj,seat)
    def centerpad(u,v):
        q=2*u-1; y=lerp(-.218,.206,v)
        return xc+q*.133,y,.350+.029*(1-v)**2-.013*math.sin(math.pi*v)*(1-q*q)
    pad=patch('Seat_'+label+'_CushionInsert',centerpad,14,22,alcantara,'SEATS',.012,True); parent(pad,seat)
    # Well-padded bolsters: oval sections following the seat shell.
    for side in [-1,1]:
        vs=[]; N=32; R=14
        for i in range(N+1):
            t=i/N; v=.025+.745*t; y,z,w=back_params(v)
            rx=.032+.016*math.sin(math.pi*t); ry=.025+.040*math.sin(math.pi*t)
            cap=.18+.82*math.sin(math.pi*(.02+.96*t))**.35
            for k in range(R):
                a=2*math.pi*k/R
                vs.append((xc+side*(w*.89+rx*math.cos(a)*cap),y-.024+ry*math.sin(a)*cap,z))
        fs=[(i*R+k,i*R+(k+1)%R,(i+1)*R+(k+1)%R,(i+1)*R+k) for i in range(N) for k in range(R)]
        fs.extend([tuple(range(R-1,-1,-1)),tuple(N*R+k for k in range(R))])
        bolster=mesh('Seat_'+label+'_Bolster_'+str(side),vs,fs,leather,'SEATS'); parent(bolster,seat)
        pts=[]
        for i in range(48):
            v=.065+.69*i/47; y,z,w=back_params(v)
            t=(v-.025)/.745; cap=.18+.82*math.sin(math.pi*(.02+.96*t))**.35
            ry=.025+.040*math.sin(math.pi*t)
            pts.append((xc+side*w*.89,y-.024-ry*cap-.001,z))
        parent(tube('Seat_'+label+'_BackrestSeam_'+str(side),pts,.00125),seat)
        parent(tube('Seat_'+label+'_CushionSeam_'+str(side),[(xc+side*.149,lerp(-.21,.20,i/32),.358+.030*(1-i/32)**2) for i in range(33)],.00125),seat)
        parent(box('Seat_'+label+'_ThighBolster_'+str(side),(xc+side*.173,-.07,.375),(.069,.35,.088),leather,'SEATS',.03),seat)
    head=box('Seat_'+label+'_Headrest',(xc,.471,.971),(.229,.075,.123),leather,'SEATS',.032); parent(head,seat)
    parent(box('Seat_'+label+'_HeadrestAccent',(xc,.429,.955),(.154,.004,.024),accent,'SEATS',.008),seat)
    for k in range(3):
        v=.16+k*.18; y,z,w=back_params(v)
        parent(tube('Seat_'+label+'_PadDivision_'+str(k),[(xc+lerp(-.13,.13,i/24),y-.031,z) for i in range(25)],.0008,plastic),seat)
    # Belt webbing and buckle, separate from the future moving seat shell.
    buckle=box('Seatbelt_Buckle_'+label,(xc-math.copysign(.242,xc),.23,.409),(.029,.047,.057),plastic,'SEATS',.005)
    box('Seatbelt_Release_'+label,(buckle.location.x,.205,.424),(.020,.005,.021),accent,'SEATS',.002)
    sx=1 if xc>0 else -1
    patch('Seatbelt_Webbing_'+label,lambda u,v,xc=xc,sx=sx:(xc+sx*(.225-.015*v)+.017*(u-.5),.61-.35*v,.97-.58*v),2,18,plastic,'TRIM',.0015,False)

# Dashboard top is a smooth swept pad, with a lower fascia and knee protection.
def dash_top(u,v):
    x=lerp(-.675,.675,u)
    y=lerp(-.925+.095*(abs(x)/.675)**2,-.47+.05*(abs(x)/.675)**2,v)
    z=.735+.036*math.sin(math.pi*v)+.018*(abs(x)/.675)**2-.018*v
    return x,y,z
dash=patch('Dashboard',dash_top,44,18,leather,thick=.023)
# Close the cowl below the windshield seat after removing the solid blockout
# deck. The forward edge tucks under the body opening without touching glass.
windedge=[v.co.copy() for v in bpy.data.objects['Windshield'].data.vertices[:33]]
def cowl_surface(u,v):
    x=lerp(-.665,.665,u); q=(x/.717+1)*16; i=min(31,int(q))
    a=windedge[i].lerp(windedge[i+1],q-i)
    a.y+=.025; a.z-=.033
    b=Vector(dash_top((x+.675)/1.35,0)); b.y+=.006; b.z-=.004
    return tuple(a.lerp(b,v))
patch('Dashboard_CowlClosure',cowl_surface,32,4,plastic,thick=.006,refine=False)
def dash_face(u,v):
    x=lerp(-.662,.662,u); y=-.47+.050*(abs(x)/.675)**2+.014*math.sin(math.pi*v)
    return x,y,lerp(.711,.559,v)+.014*(abs(x)/.675)**2
patch('Dashboard_LowerFascia',dash_face,40,12,plastic,thick=.013)
for side in [-1,1]:
    box('KneePad_'+str(side),(side*.385,-.516,.531),(.43,.12,.077),alcantara,radius=.028)
    tube('Dashboard_Seam_'+str(side),[dash_top(lerp(.03,.44,i/48) if side<0 else lerp(.56,.97,i/48),.89) for i in range(49)],.0011)
box('Passenger_Glovebox',(.365,-.449,.616),(.36,.014,.10),leather,radius=.018)
box('Passenger_Glovebox_Latch',(.365,-.435,.657),(.06,.009,.008),metal,'CONTROLS',.003)

# Discrete HVAC blades, modest geometry and dark real cavities.
for label,xc in [('Driver',-.572),('Center',.07),('Passenger',.545)]:
    w=.13 if label!='Center' else .18
    box('HVAC_'+label+'_Housing',(xc,-.435,.692),(w,.035,.041),metal,'CONTROLS',.010)
    box('HVAC_'+label+'_Cavity',(xc,-.413,.692),(w-.013,.008,.028),speaker,'CONTROLS',.006)
    for k in range(3): box('HVAC_'+label+'_Blade_'+str(k),(xc,-.405,.683+.008*k),(w-.02,.014,.0025),plastic,'CONTROLS',.001)
    box('HVAC_'+label+'_Tab',(xc+.021,-.395,.692),(.018,.008,.009),metal,'CONTROLS',.003)

# Displays have black physical surfaces and a visor; no baked dashboard UI.
N=Vector((0,.94,.342)); N.normalize(); X=Vector((1,0,0)); U=X.cross(N).normalized()
B=Matrix((X,N,U)).transposed()
clusterC=Vector((-.36,-.678,.834))
cluster=box('InstrumentCluster',clusterC,(.316,.040,.100),plastic,'CONTROLS',.024,B)
parent(box('InstrumentCluster_Screen',clusterC+N*.024,(.282,.007,.085),display,'CONTROLS',.013,B),cluster)
patch('InstrumentCluster_Visor',lambda u,v:(-.36+lerp(-.175,.175,u),lerp(-.795,-.63,v),lerp(.758,.895,smooth(v))+.012*math.sin(math.pi*u)*math.sin(math.pi*v)),24,8,alcantara,'CONTROLS',.008)
for side in [-1,1]:
    patch('InstrumentCluster_ShroudSide_'+str(side),lambda u,v,side=side:(-.36+side*.173,lerp(-.792,-.638,u),lerp(.765,lerp(.761,.891,smooth(u)),v)),16,3,plastic,'CONTROLS',.004,False)
box('InstrumentCluster_Base',(-.36,-.679,.772),(.30,.09,.018),plastic,'CONTROLS',.006)
screenN=Vector((-.16,.955,.25)).normalized(); screenX=Vector((screenN.y,-screenN.x,0)).normalized(); screenU=screenX.cross(screenN).normalized(); SB=Matrix((screenX,screenN,screenU)).transposed()
screenC=Vector((.16,-.435,.621))
screen=box('CenterScreen',screenC,(.266,.037,.118),metal,'CONTROLS',.014,SB)
parent(box('CenterScreen_Display',screenC+screenN*.023,(.242,.007,.092),display,'CONTROLS',.009,SB),screen)
box('CenterScreen_DashSupport',(.16,-.478,.614),(.20,.07,.103),plastic,'CONTROLS',.02)
for o in list(interior.all_objects):
    if o.name.startswith('HVAC_Center_'): o.location.z+=.022

# Original compact steering wheel with restrained three-spoke layout.
C=Vector((-.36,-.405,.718)); radius=.156
vs=[]; seg=112; ring=16
for i in range(seg):
    a=2*math.pi*i/seg
    xx=radius*math.cos(a); zz=max(-.124,radius*math.sin(a))
    outward=(X*math.cos(a)+U*math.sin(a)).normalized()
    grip=.0155+.006*math.exp(-((abs(math.cos(a))-.97)/.18)**2)
    for k in range(ring):
        t=2*math.pi*k/ring
        vs.append(C+X*xx+U*zz+grip*math.cos(t)*outward+.018*math.sin(t)*N)
fs=[(i*ring+k,i*ring+(k+1)%ring,((i+1)%seg)*ring+(k+1)%ring,((i+1)%seg)*ring+k) for i in range(seg) for k in range(ring)]
wheel=mesh('Steering_Wheel',vs,fs,leather,'CONTROLS'); sub(wheel); origin(wheel,C)
wheel['steering_axis_local']=list(N); wheel['driver_seat_center_x']=-.36
hub=box('Steering_Hub',C+N*.016,(.112,.070,.085),plastic,'CONTROLS',.025,B); parent(hub,wheel)
parent(box('Steering_Hub_Badge',C+N*.054,(.038,.0025,.011),metal,'CONTROLS',.004,B),wheel)
for side in [-1,1]:
    parent(box('Steering_Spoke_'+str(side),C+X*(side*.09)-N*.003,(.107,.021,.035),carbon,'CONTROLS',.012,B),wheel)
    parent(box('Steering_GripInsert_'+str(side),C+X*(side*.145)+N*.014,(.024,.009,.070),alcantara,'CONTROLS',.01,B),wheel)
    for j in range(2):
        parent(cyl('Steering_Button_'+str(side)+'_'+str(j),C+X*(side*(.074+.026*j))+N*.017,.0085,.007,metal,'CONTROLS',N,24),wheel)
    pc=C+X*(side*.118)-N*.042+U*.016
    paddle=box('Paddle_'+('L' if side<0 else 'R'),pc,(.026,.007,.103),metal,'CONTROLS',.009,B)
    pivot=C+X*(side*.085)-N*.034; origin(paddle,pivot)
    paddle['pivot_purpose']='Attachment pivot; no rig'
    box('Paddle_Attachment_'+str(side),C+X*(side*.084)-N*.041,(.067,.014,.018),plastic,'CONTROLS',.004,B)
    tube('Steering_Stalk_'+str(side),[tuple(C-N*.09),tuple(C-N*.115+X*(side*.12))],.006,plastic,'CONTROLS')
parent(box('Steering_LowerSpoke',C-U*.077-N*.005,(.037,.022,.088),metal,'CONTROLS',.01,B),wheel)
parent(box('Steering_CenterMarker',C+U*.157+N*.002,(.010,.039,.012),accent,'CONTROLS',.003,B),wheel)
column_start=C-N*.042; column_end=Vector((-.36,-.67,.648))
column=cyl('Steering_Column',(column_start+column_end)/2,.031,(column_start-column_end).length,plastic,'CONTROLS',column_start-column_end,40)
box('Steering_Column_DashBoot',(-.36,-.64,.66),(.109,.115,.079),plastic,'CONTROLS',.027)

# Compact controls sit on the supported console, not on floating plates.
selector=box('DriveSelector',(0,-.10,.561),(.061,.11,.058),metal,'CONTROLS',.016)
box('DriveSelector_Grip',(0,-.087,.588),(.046,.064,.023),leather,'CONTROLS',.01)
cyl('StartStop_Button',(-.041,-.245,.553),.017,.009,accent,n=40)
cyl('DriveMode_Rotary',(.041,-.239,.556),.022,.018,metal,n=48)
cyl('DriveMode_Cap',(.041,-.239,.568),.017,.007,plastic,n=40)
for i in range(3): box('Console_Switch_'+str(i),(-.058+.058*i,.082,.544),(.038,.025,.009),metal,'CONTROLS',.004)
box('Console_StorageTray',(0,.214,.534),(.15,.127,.024),plastic,'CONTROLS',.021)
box('Console_StorageInset',(0,.214,.549),(.125,.102,.008),speaker,'CONTROLS',.016)

# Door panels are self-contained and stop inside their exterior door boundaries.
for side,label in [(-1,'L'),(1,'R')]:
    def doorfn(u,v):
        y=lerp(-.82,.455,u); z=lerp(.34,.718,v)
        x=side*(.775-.055*math.sin(math.pi*v)-.015*math.sin(math.pi*u))
        return x,y,z
    door=patch('DoorPanel_'+label,doorfn,30,16,leather,thick=.012)
    origin(door,(side*.78,-.80,.48)); door['future_door_parent']='Car_Door_'+label
    arm=box('DoorPanel_'+label+'_Armrest',(side*.702,-.12,.564),(.11,.64,.069),alcantara,'TRIM',.027); parent(arm,door)
    trim=patch('DoorPanel_'+label+'_CarbonInsert',lambda u,v:(side*(.731-.005*math.sin(math.pi*v)),lerp(-.57,.32,u),lerp(.601,.683,v)),24,6,carbon,'TRIM',.004); parent(trim,door)
    pts=[]
    for i in range(65):
        y=lerp(-.64,.37,i/64); z=.698+.009*math.sin(math.pi*i/64)
        u=(y+.82)/1.275; v=(z-.34)/.378
        pts.append((side*(.775-.055*math.sin(math.pi*v)-.015*math.sin(math.pi*u)-.0015),y,z))
    parent(tube('DoorPanel_'+label+'_Seam',pts,.0013),door)
    parent(tube('DoorPanel_'+label+'_Pull',[(side*.674,-.33,.589),(side*.657,-.26,.623),(side*.662,-.12,.628),(side*.70,-.04,.597)],.009,metal),door)
    parent(box('DoorPanel_'+label+'_SwitchPad',(side*.681,-.41,.601),(.063,.088,.018),plastic,'CONTROLS',.012),door)
    for k in range(2): parent(box('DoorPanel_'+label+'_WindowSwitch_'+str(k),(side*(.666+.026*k),-.41,.614),(.018,.045,.006),metal,'CONTROLS',.003),door)
    parent(box('DoorPanel_'+label+'_Speaker',(side*.722,.18,.440),(.019,.23,.12),speaker,'TRIM',.032),door)
    for k in range(7):
        parent(box('DoorPanel_'+label+'_SpeakerSlit_'+str(k),(side*.708,.096+.027*k,.44),(.003,.005,.078),plastic,'TRIM',.002),door)

# Pedals use independent hinge origins and substantial metal/rubber faces.
pedalB=Matrix.Rotation(math.radians(-18),3,'X')
for name,x,w,y in [('Pedal_Brake',-.393,.094,-.91),('Pedal_Throttle',-.244,.043,-.947),('DeadPedal',-.548,.065,-.91)]:
    loc=(x,y,.393); pedal=box(name,loc,(w,.020,.127),metal,'CONTROLS',.01,pedalB)
    origin(pedal,(x,y+.026,.316)); pedal['hinge_axis']='local X'
    for k in range(4):
        zz=-.04+k*.027; pt=Vector(loc)+pedalB@Vector((0,.014,zz))
        parent(box(name+'_Rubber_'+str(k),pt,(w*.72,.004,.009),plastic,'CONTROLS',.003,pedalB),pedal)
    if name!='DeadPedal': box(name+'_Arm',(x,y-.022,.343),(.018,.028,.11),plastic,'CONTROLS',.005)

# Roof liner follows the actual roof, offset inward. Pillar liners track seals.
roof=bpy.data.objects['Roof_Panel']
me=roof.data.copy(); liner=bpy.data.objects.new('Headliner',me); COL['TRIM'].objects.link(liner)
for v in me.vertices: v.co.z-=.018; v.co.x*=.978
me.materials.clear(); me.materials.append(alcantara); sub(liner); solid(liner,.005)
for label,side in [('L',-1),('R',1)]:
    source=bpy.data.objects['A_Pillar_'+label]
    pts=[source.matrix_world@Vector(p.co[:3]) for p in source.data.splines[0].points]
    pts=[(p.x-side*.032,p.y+.025,p.z-.015) for p in pts[5:]]
    tube('A_Pillar_Liner_'+label,pts,.012,alcantara)
    source=bpy.data.objects['Roof_Rail_'+label]
    pts=[source.matrix_world@Vector(p.co[:3]) for p in source.data.splines[0].points]
    tube('RoofRail_Liner_'+label,[(p.x-side*.017,p.y,p.z-.018) for p in pts],.012,alcantara)
box('OverheadConsole',(0,-.04,1.158),(.095,.155,.015),plastic,'TRIM',.013)
box('DomeLight_Lens',(0,-.024,1.147),(.049,.055,.004),metal,'TRIM',.008)
for side in [-1,1]: box('SunVisor_'+str(side),(side*.305,-.239,1.083),(.235,.102,.016),alcantara,'TRIM',.012)
mirror=box('RearViewMirror',(0,-.435,1.037),(.214,.029,.069),plastic,'TRIM',.017)
mirrormat=material('MAT_InteriorMirror',(.55,.60,.63),1,.06)
parent(box('RearViewMirror_Glass',(0,-.417,1.037),(.191,.004,.052),mirrormat,'TRIM',.012),mirror)
bpy.context.view_layer.update()
wind=bpy.data.objects['Windshield'].evaluated_get(bpy.context.evaluated_depsgraph_get())
hit,point,normal,index=wind.ray_cast(Vector((0,-.37,.90)),Vector((0,0,1)))
assert hit,'Mirror mount must locate inner windshield surface'
mount_z=point.z-.009
tube('RearViewMirror_Mount',[(0,-.435,1.056),(0,-.405,1.064),(0,-.37,mount_z)],.005,plastic)
box('RearViewMirror_BondPad',(0,-.37,mount_z+.003),(.028,.021,.003),plastic,'TRIM',.004)

# Dense visible base grids already support smooth shading. Keep subdivision
# only where it materially improves the dash crown and seat shell silhouette.
for o in interior.all_objects:
    if o.name not in ['Dashboard','Seat_Driver','Seat_Passenger']:
        for m in list(o.modifiers):
            if m.type=='SUBSURF': o.modifiers.remove(m)

# Review camera collection remains outside the vehicle asset.
pres=bpy.data.collections['PRESENTATION']
def camera(name,loc,target,lens=35):
    o=bpy.data.objects.get(name)
    if not o:
        o=bpy.data.objects.new(name,bpy.data.cameras.new(name)); pres.objects.link(o)
    o.location=loc; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    o.data.type='PERSP'; o.data.lens=lens; o.data.clip_start=.008; o.data.clip_end=100
    return o
camera('Camera_Interior_Driver',(-1.30,.64,1.47),(-.14,-.30,.61),36)
camera('Camera_Interior_Passenger',(1.30,.78,1.48),(.12,-.28,.61),36)
camera('Camera_Interior_Dashboard',(.06,.49,1.02),(0,-.63,.70),29)
camera('Camera_Interior_Seats',(1.18,-1.56,1.25),(0,.26,.65),48)
camera('Camera_Cockpit_QA',(-.36,.15,1.027),(-.31,-1.50,.56),18)
s['milestone']='05: original two-seat interior, exterior 04 preserved'
s['exterior_04_sha256']=source_hash
s['interior_driver_eye_m']=(-.36,.15,1.027)
s['interior_review_notes']='Black/charcoal with restrained red seams. No final UI, UV, textures, animation, export or game optimization. Separate moving components have local pivots.'
s.camera=bpy.data.objects['Camera_Presentation']
s.render.engine='CYCLES'; s.cycles.samples=40; s.cycles.use_denoising=True
s.cycles.max_bounces=12; s.cycles.transmission_bounces=8
s.render.resolution_x=1920; s.render.resolution_y=1080; s.render.resolution_percentage=100
bpy.ops.object.select_all(action='DESELECT'); wheel.select_set(True); bpy.context.view_layer.objects.active=wheel
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_05_interior_working.blend'))
print('INTERIOR BUILD COMPLETE',len(interior.all_objects),'objects',flush=True)
