import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
master=bpy.data.collections['REFERENCE_Master_06'];master.hide_viewport=False
validation=json.loads((R/'lod_validation.json').read_text())
def evalmesh(o):
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();return bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
def replace(o,me):
 old=o.data;o.data=me
 if old.users==0:bpy.data.meshes.remove(old)
def clean(me):
 bm=bmesh.new();bm.from_mesh(me);w=[e for e in bm.edges if e.is_wire]
 if w:bmesh.ops.delete(bm,geom=w,context='EDGES')
 lone=[v for v in bm.verts if not v.link_faces]
 if lone:bmesh.ops.delete(bm,geom=lone,context='VERTS')
 bm.to_mesh(me);bm.free();me.update()
def bad(me):
 bm=bmesh.new();bm.from_mesh(me);n=sum(not e.is_manifold for e in bm.edges);bm.free();return n
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];col.hide_viewport=False
 for o in list(col.all_objects):
  src=bpy.data.objects[o['source_object']]
  if src.name.startswith('Wheel_Well_'):
   key=src.name[-2:];wheel=bpy.data.objects['Wheel_'+key];x,y,z=wheel.location;s=-1 if x<0 else 1;r=.345 if key[0]=='F' else .365;w=.29 if key[0]=='F' else .33;N=[32,24,16,10][lod]
   vs=[];fs=[]
   for u in [0,1]:
    for i in range(N+1):
     a=-.46+(math.pi+.92)*i/N;vs.append((x-s*(w/2+.02)+s*(w+.014)*u,y+(r+.027)*math.cos(a),r+(r+.027)*math.sin(a)))
   for i in range(N):fs.append((i,i+1,N+2+i,N+1+i))
   me=bpy.data.meshes.new(o.name+'_retopo');me.from_pydata(vs,[],fs);me.materials.append(src.data.materials[0]);uv=me.uv_layers.new(name='UVMap')
   for l in me.loops:
    v=me.vertices[l.vertex_index].co;uv.data[l.index].uv=(v.y*.2,v.z*.2)
   for p in me.polygons:p.use_smooth=True
   replace(o,me);o.matrix_world.identity();o['uv_meter_scale']=5
   m=o.modifiers.new('Thin closed well liner','SOLIDIFY');m.thickness=.003;me=evalmesh(o);o.modifiers.clear();replace(o,me)
  elif src.name=='Front_Intake_Grille':
   me=evalmesh(src);bm=bmesh.new();bm.from_mesh(me)
   # Retain only the outward face of each tiny grille bar. Intentional sheet surface.
   remove=[f for f in bm.faces if f.normal.y>-.9];bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(me);bm.free();clean(me);replace(o,me);o['intentional_open_surface']='Grille bar front sheets; dark intake behind prevents see-through cabin'
  else:
   clean(o.data)
   flag=next((row for row in validation['lods'][str(lod)]['topology_review'] if row['object']==o.name),None)
   if flag and bad(o.data)>flag['master_nonmanifold']:
    o.data.calc_loop_triangles();target=len(o.data.loop_triangles)*2
    for trial in range(5):
     me=evalmesh(src);me.calc_loop_triangles();n=len(me.loop_triangles);replace(o,me)
     d=o.modifiers.new('Topology-safe increased component budget','DECIMATE');d.ratio=min(1,target/n)
     me=evalmesh(o);o.modifiers.clear();clean(me);replace(o,me)
     if bad(me)<=flag['master_nonmanifold']:break
     target*=2
  # Keep QEM overshoots inside each reference component's bounding box.
  ref=evalmesh(src);mins=[min(v.co[j] for v in ref.vertices) for j in range(3)];maxs=[max(v.co[j] for v in ref.vertices) for j in range(3)]
  if not src.name.startswith('Wheel_Well_'):
   for v in o.data.vertices:
    for j in range(3):v.co[j]=max(mins[j],min(maxs[j],v.co[j]))
  bpy.data.meshes.remove(ref)
 col.hide_viewport=lod!=0
master.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
