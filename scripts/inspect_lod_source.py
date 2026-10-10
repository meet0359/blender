import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]; dg=bpy.context.evaluated_depsgraph_get(); rows=[]
for cn in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']:
 for o in bpy.data.collections[cn].all_objects:
  if o.type not in ['MESH','CURVE','FONT']: continue
  e=o.evaluated_get(dg); me=e.to_mesh(); me.calc_loop_triangles()
  rows.append(dict(name=o.name,collection=cn,type=o.type,base=len(o.data.polygons) if o.type=='MESH' else 0,tris=len(me.loop_triangles),location=list(o.location),dimensions=list(o.dimensions),parent=o.parent.name if o.parent else None,mods=[dict(name=m.name,type=m.type,level=getattr(m,'levels',None),render=getattr(m,'render_levels',None),segments=getattr(m,'segments',None)) for m in o.modifiers],curve_res=getattr(o.data,'resolution_u',None),bevel_res=getattr(o.data,'bevel_resolution',None)))
  e.to_mesh_clear()
(R/'lod_source_inventory.json').write_text(json.dumps(rows,indent=2))
for cn in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']:
 a=[r for r in rows if r['collection']==cn];print(cn,len(a),sum(r['tris'] for r in a))
for r in sorted(rows,key=lambda r:-r['tris'])[:55]: print(r['name'],r['tris'],r['mods'],r['curve_res'],r['bevel_res'])
