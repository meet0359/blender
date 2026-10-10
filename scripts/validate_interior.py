import bpy,bmesh,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
dg=bpy.context.evaluated_depsgraph_get(); scene=bpy.context.scene
objects=list(bpy.data.collections['INTERIOR'].all_objects)
errors=[]; warnings=[]; lines=[]
def check(ok,msg):
    lines.append(('PASS: ' if ok else 'ERROR: ')+msg)
    if not ok: errors.append(msg)
def warn(msg): warnings.append(msg); lines.append('WARNING: '+msg)
required=['Dashboard','Steering_Wheel','Paddle_L','Paddle_R','InstrumentCluster','CenterScreen','CenterConsole','Seat_Driver','Seat_Passenger','DoorPanel_L','DoorPanel_R','Pedal_Brake','Pedal_Throttle','Floor','RearBulkhead','RearViewMirror','Headliner','TransmissionTunnel']
check(all(bpy.data.objects.get(n) in objects for n in required),'Required interior objects exist in INTERIOR hierarchy')
check(all(bpy.data.materials.get(n) for n in ['MAT_InteriorLeather','MAT_InteriorPlastic','MAT_InteriorAlcantara','MAT_InteriorCarbon','MAT_InteriorMetal','MAT_Display','MAT_SeatAccent','MAT_Speaker']),'All eight requested review material slots exist')
check(not any(o.name.startswith(('Cube','Plane','Cylinder','Sphere','Bezier','Text.')) for o in objects),'Meaningful object names')
check(all(min(o.scale)>0 and max(o.scale)-min(o.scale)<1e-6 for o in objects),'Positive uniform object scales')
check(all(not o.hide_render and not o.hide_viewport for o in objects),'No accidentally hidden interior parts')
check(not any(o.type=='LIGHT' for o in objects),'No functional light objects in interior asset')
check(hashlib.sha256((ROOT/'racing_car_04_exterior_final.blend').read_bytes()).hexdigest()==scene['exterior_04_sha256'],'Source 04 file preserved byte-for-byte')
base=[0,0,0]; evaluated=[0,0,0]; degenerate=[]; loose=[]; nonmanifold=[]; inverted=[]; geom={}; bounds={}; trees={}; categories={}
def evaluate(o):
    e=o.evaluated_get(dg); me=e.to_mesh(); me.calc_loop_triangles()
    coords=[e.matrix_world@v.co for v in me.vertices]; tris=[tuple(t.vertices) for t in me.loop_triangles]
    counts=[len(me.vertices),len(me.polygons),len(tris)]
    bm=bmesh.new(); bm.from_mesh(me)
    nm=sum(not e.is_manifold for e in bm.edges)
    volume=bm.calc_volume(signed=True) if not nm else 0
    bm.free(); e.to_mesh_clear()
    return coords,tris,counts,nm,volume
for o in objects:
    if o.type!='MESH': continue
    me=o.data; me.calc_loop_triangles(); b=[len(me.vertices),len(me.polygons),len(me.loop_triangles)]
    for i in range(3): base[i]+=b[i]
    bad=[p.index for p in me.polygons if p.area<1e-12]
    used={i for p in me.polygons for i in p.vertices}
    if bad: degenerate.append((o.name,len(bad)))
    if len(used)<len(me.vertices): loose.append(o.name)
    coords,tris,e,nm,vol=evaluate(o)
    for i in range(3): evaluated[i]+=e[i]
    if nm: nonmanifold.append((o.name,nm))
    if not nm and vol<-1e-10: inverted.append(o.name)
    geom[o.name]=(coords,tris); trees[o.name]=BVHTree.FromPolygons(coords,tris,all_triangles=True)
    bounds[o.name]=([min(p[i] for p in coords) for i in range(3)],[max(p[i] for p in coords) for i in range(3)])
    cat=next((c.name.replace('INTERIOR_','').title() for c in o.users_collection if c.name.startswith('INTERIOR_')),'Main')
    row=categories.setdefault(cat,{'base':[0,0,0],'evaluated':[0,0,0]})
    for i in range(3): row['base'][i]+=b[i]; row['evaluated'][i]+=e[i]
check(not degenerate,'No zero-area faces: '+str(degenerate))
check(not loose,'No loose vertices: '+str(loose))
check(not nonmanifold,'Evaluated panels have manifold thickness: '+str(nonmanifold))
check(not inverted,'Closed evaluated surfaces have consistent signed-volume orientation: '+str(inverted))
if not 30000<=base[2]<=60000: warn('Interior base budget outside target: '+str(base[2]))
else: check(True,'Interior base budget 30,000–60,000 triangles: '+str(base[2]))
if not 60000<=evaluated[2]<=120000: warn('Interior evaluated budget outside target: '+str(evaluated[2]))
else: check(True,'Interior evaluated budget 60,000–120,000 triangles: '+str(evaluated[2]))
exterior_names=['Car_Body','Hood','Rear_Engine_Cover','Car_Door_L','Car_Door_R','Roof_Panel','Windshield','Rear_Glass','Window_FL','Window_FR','Window_RL','Window_RR','Side_Intake_Throat_L','Side_Intake_Throat_R']
for name in exterior_names:
    coords,tris,_,_,_=evaluate(bpy.data.objects[name]); geom[name]=(coords,tris)
    trees[name]=BVHTree.FromPolygons(coords,tris,all_triangles=True)
    bounds[name]=([min(p[i] for p in coords) for i in range(3)],[max(p[i] for p in coords) for i in range(3)])
def bbox_contact(a,b):
    aa,ab=bounds[a]; ba,bb=bounds[b]
    return all(aa[i]<=bb[i] and ab[i]>=ba[i] for i in range(3))
contacts=[]
for o in objects:
    if o.type!='MESH': continue
    for name in exterior_names:
        if bbox_contact(o.name,name):
            pairs=trees[o.name].overlap(trees[name])
            if pairs: contacts.append({'interior':o.name,'exterior':name,'triangle_pairs':len(pairs)})
check(not contacts,'No interior/exterior or glass intersections in audited envelope: '+json.dumps(contacts))
# Primary separate assemblies should not cross one another. Fitted pads/seams
# and their host shells are intentional seated assemblies, audited visually.
primary=['Seat_Driver','Seat_Passenger','Dashboard','DoorPanel_L','DoorPanel_R','RearBulkhead','Steering_Wheel','InstrumentCluster','CenterScreen']
primary_contacts=[]
for k,a in enumerate(primary):
    for b in primary[k+1:]:
        if bbox_contact(a,b):
            pairs=trees[a].overlap(trees[b])
            if pairs: primary_contacts.append((a,b,len(pairs)))
check(not primary_contacts,'No primary interior assembly crossings: '+str(primary_contacts))
wheel=bpy.data.objects['Steering_Wheel']
check((wheel.matrix_world.translation-Vector((-.36,-.405,.718))).length<1e-5,'Steering origin centered on designed steering axis')
check(abs(wheel.location.x-bpy.data.objects['Seat_Driver'].location.x)<1e-5,'Driver seat / steering / instrument lateral alignment')
for n in ['Pedal_Brake','Pedal_Throttle']:
    lo,hi=bounds[n]
    check(-.66<lo[0]<hi[0]<-.16 and -1.1<lo[1]<hi[1]<-.7 and .27<lo[2]<hi[2]<.55,n+' inside driver footwell; hinge origin prepared')
headroom={}
for name,x in [('Seat_Driver',-.36),('Seat_Passenger',.36)]:
    top=max(p.z for p in geom[name][0]); ray=Vector((x,.515,top))
    hit,normal,idx,dist=trees['Roof_Panel'].ray_cast(ray,Vector((0,0,1)),1)
    headroom[name]=dist
    check(dist is not None and dist>.06,name+' headrest-to-roof clearance '+str(round(dist,4) if dist else dist)+' m')
check(all(bounds['DoorPanel_'+c][0][1]>-.88 and bounds['DoorPanel_'+c][1][1]<.52 for c in ['L','R']),'Door inner panels stay inside future opening door span')
full=[0,0,0]
asset=set()
for n in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']:
    asset.update(bpy.data.collections[n].all_objects)
for o in asset:
    if o.type not in ['MESH','CURVE','FONT','SURFACE']: continue
    e=o.evaluated_get(dg); me=e.to_mesh(); me.calc_loop_triangles()
    for i,v in enumerate([len(me.vertices),len(me.polygons),len(me.loop_triangles)]): full[i]+=v
    e.to_mesh_clear()
warn('No final UI graphics, UVs/textures, animation, LODs, colliders, optimization or export checks in this phase.')
warn('Seated upholstery/trim/fastener assemblies are not globally boolean-unioned; close-range mechanical tolerance remains a later review task.')
lines.append('BASE INTERIOR V/P/T: '+str(base)); lines.append('EVALUATED INTERIOR V/P/T: '+str(evaluated)); lines.append('COMPLETE VEHICLE EVALUATED V/P/T: '+str(full))
lines.append(f'RESULT: {len(errors)} errors / {len(warnings)} warnings')
report='\n'.join(lines)+'\n'; print(report)
(ROOT/'interior_validation.txt').write_text(report)
(ROOT/'interior_stats.json').write_text(json.dumps({'base':base,'evaluated':evaluated,'complete_vehicle_evaluated':full,'categories':categories,'objects':len(objects),'errors':errors,'warnings':warnings,'contacts':contacts,'primary_contacts':primary_contacts,'headrest_roof_clearances_m':headroom,'bounds':bounds},indent=2))
