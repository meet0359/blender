import bpy,bmesh,json,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;report={'errors':[],'warnings':[],'lods':{}}
build=json.loads((R/'lod_build_stats.json').read_text());report['master_categories']=build['master_categories'];report['master_total']=sum(build['master_categories'].values())
def check(ok,msg):
 if not ok:report['errors'].append(msg)
def evaluated(o):
 dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);return bpy.data.meshes.new_from_object(e,preserve_all_data_layers=True,depsgraph=dg)
def bounds(objs):
 p=[]
 for o in objs:
  p.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices)
 a=np.array(p);return a.min(0),a.max(0)
master=bpy.data.collections['REFERENCE_Master_06'];master.hide_viewport=False;bpy.context.view_layer.update()
masterme={}; mb=[]
for o in list(master.all_objects):
 if o.type not in ['MESH','CURVE','FONT']:continue
 me=evaluated(o);masterme[o.name]=me;mb.extend(tuple(o.matrix_world@v.co) for v in me.vertices)
a=np.array(mb);masterdims=a.max(0)-a.min(0);report['master_dimensions_xyz']=masterdims.tolist()
for lod in range(4):
 col=bpy.data.collections['Car_LOD'+str(lod)];col.hide_viewport=False;bpy.context.view_layer.update();objs=list(col.all_objects);cat={};top=[];deviation=[]
 for o in objs:
  me=o.data;me.calc_loop_triangles();c=o['lod_category'];cat[c]=cat.get(c,0)+len(me.loop_triangles)
  check(bool(me.uv_layers),o.name+' missing UV');check(bool(me.materials) and all(m for m in me.materials),o.name+' missing material')
  check(all(p.material_index<len(me.materials) for p in me.polygons),o.name+' invalid material index')
  bm=bmesh.new();bm.from_mesh(me);nonman=sum(not e.is_manifold for e in bm.edges);boundary=sum(e.is_boundary for e in bm.edges);wire=sum(e.is_wire for e in bm.edges);inconsistent=sum(e.is_manifold and not e.is_contiguous for e in bm.edges);deg=sum(f.calc_area()<1e-12 for f in bm.faces)
  src=masterme[o['source_object']];bs=bmesh.new();bs.from_mesh(src);srcbad=sum(not e.is_manifold for e in bs.edges);srcincon=sum(e.is_manifold and not e.is_contiguous for e in bs.edges)
  if not o.get('intentional_open_surface') and (wire or inconsistent>srcincon or (nonman>srcbad)):top.append(dict(object=o.name,boundary=boundary,nonmanifold=nonman,master_nonmanifold=srcbad,inconsistent=inconsistent,master_inconsistent=srcincon,wire=wire,degenerate=deg))
  bm.free();bs.free()
  # Bidirectional sampled surface distance for visible body/glass components.
  if c in ['Body','Glass']:
   hi=BVHTree.FromPolygons([v.co for v in src.vertices],[p.vertices[:] for p in src.polygons]);lo=BVHTree.FromPolygons([v.co for v in me.vertices],[p.vertices[:] for p in me.polygons]);dist=[]
   for mesh,bvh in [(src,lo),(me,hi)]:
    for v in list(mesh.vertices)[::max(1,len(mesh.vertices)//1000)]:
     hit=bvh.find_nearest(v.co)
     if hit[0] is not None:dist.append(hit[3])
   deviation.append({'object':o.name,'max_m':max(dist,default=0),'p95_m':float(np.percentile(dist,95)) if dist else 0})
 check(not top,f'LOD{lod} new topology defects: {top}')
 lo,hi=bounds(objs);dims=hi-lo;delta=dims-masterdims;check(bool(np.all(np.abs(delta)<=.010)),f'LOD{lod} dimensions differ by more than 10 mm: {delta}')
 wheels={}
 for key in ['FL','FR','RL','RR']:
  o=bpy.data.objects['Wheel_'+key+'_LOD'+str(lod)];src=bpy.data.objects['Wheel_'+key];err=(o.matrix_world.translation-src.matrix_world.translation).length;axis=o.matrix_world.to_3x3()@Vector((1,0,0));srcaxis=src.matrix_world.to_3x3()@Vector((1,0,0));check(err<1e-7 and (axis-srcaxis).length<1e-7,o.name+' wheel center/axis changed');wheels[key]=list(o.matrix_world.translation)
 report['lods'][str(lod)]={'categories':cat,'total':sum(cat.values()),'reduction_percent':100*(1-sum(cat.values())/report['master_total']),'dimensions_xyz':dims.tolist(),'dimension_delta_mm':(delta*1000).tolist(),'wheel_centers':wheels,'wheelbase_m':abs(wheels['FL'][1]-wheels['RL'][1]),'topology_review':top,'surface_deviation':deviation,'objects':len(objs)}
 print('LOD',lod,'TRIS',sum(cat.values()),'DIM DELTA mm',delta*1000,'TOPOLOGY FLAGS',len(top),flush=True)
 col.hide_viewport=lod!=0
check(hashlib.sha256((R/'racing_car_06_materials_uv.blend').read_bytes()).hexdigest()==S['master_06_sha256'],'Master file modified')
missing=[]
for im in bpy.data.images:
 if im.source=='FILE' and im.filepath and not Path(bpy.path.abspath(im.filepath)).exists():missing.append(im.filepath)
check(not missing,'Missing textures '+str(missing))
report['warnings']=['Intentional open/intersecting trim and panel surfaces inherited from master are not a watertight collision mesh.','Engine UV-to-meter attribute conversion and transmission setup remain required at later export.']
(R/'lod_validation.json').write_text(json.dumps(report,indent=2));print('ERRORS',report['errors'],flush=True)
