import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];rows=[]
for i in range(4):
 for o in bpy.data.collections['Car_LOD'+str(i)].all_objects:
  rows.append(dict(name=o.name,lod=i,loc=list(o.location),rot=list(o.rotation_euler),scale=list(o.scale),matrix=[list(x) for x in o.matrix_world],parent=o.parent.name if o.parent else None,texture_group=o.get('texture_group'),uv_meter_scale=o.get('uv_meter_scale'),mats=[s.material.name for s in o.material_slots],uvs=[l.name for l in o.data.uv_layers]))
(R/'export_source_inventory.json').write_text(json.dumps(rows,indent=2));print('nonunit',[(r['name'],r['scale']) for r in rows if any(abs(s-1)>1e-6 for s in r['scale'])]);print('rotated',[(r['name'],r['rot']) for r in rows if any(abs(s)>1e-6 for s in r['rot'])][:25]);print('steer',[(r['name'],r['loc'],r['rot']) for r in rows if r['name'].startswith('Steering_Wheel')])
for m in sorted({s.material for o in bpy.data.collections['Car_LOD0'].all_objects for s in o.material_slots},key=lambda m:m.name):
 print(m.name,m.get('texture_set'),m.get('tile_m'),[(n.label,tuple(n.inputs[2].default_value)) for n in m.node_tree.nodes if n.type=='MIX_RGB' and n.blend_type=='MULTIPLY'])
