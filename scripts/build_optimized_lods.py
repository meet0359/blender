import bpy,bmesh,json,math,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]; S=bpy.context.scene
inventory=json.loads((R/'lod_source_inventory.json').read_text()); lookup={r['name']:r for r in inventory}; savings=json.loads((R/'detail_bake_savings.json').read_text())
sourcehash=hashlib.sha256((R/'racing_car_06_materials_uv.blend').read_bytes()).hexdigest()
master=bpy.data.collections.new('REFERENCE_Master_06'); S.collection.children.link(master)
source=[]
for cn in ['CAR','WHEELS','BRAKES','GLASS','LIGHTS','INTERIOR']:
 col=bpy.data.collections[cn]; source+=list(col.all_objects)
 for parent in [S.collection]:
  if col.name in parent.children: parent.children.unlink(col)
 master.children.link(col)
source=list(set(source)); geom=[o for o in source if o.type in ['MESH','CURVE','FONT']]
def category(o):
 c=lookup[o.name]['collection']; n=o.name
 if c=='WHEELS':return 'Tires' if n.startswith(('Tire_','Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR')) else 'Wheels'
 if c=='CAR':return 'Body' if n in ['Car_Body','Hood','Roof_Panel','Front_Bumper','Rear_Bumper','Rear_Engine_Cover','Car_Door_L','Car_Door_R','Mirror_L','Mirror_R'] or 'Pillar_Surface' in n else 'Aero_Trim'
 return {'BRAKES':'Brakes','GLASS':'Glass','LIGHTS':'Lights','INTERIOR':'Interior'}[c]
def omit(n,lod):
 if n in savings:return True
 if n.startswith('Brake_Vent_'):return True
 if lod>=1 and (n.startswith(('Pedal_','DeadPedal','Seat_Rail','Footwell_Mat','Paddle_Attachment','Steering_Button','Console_Switch','DoorPanel_')) and any(w in n for w in ['Slit','Switch','Pedal','Rail','Mat','Button','Attachment'])):return True
 if lod>=1 and n.startswith(('Tire_Shoulder_Sipe','Wheel_Lug_Recess','Caliper_PistonBoss')):return True
 if lod>=2:
  if n.startswith(('Wheel_Lug','Brake_Radial_Slot','Brake_Hat_Rim','Caliper_Bridge','Caliper_Spine','Headlight_Projector_Shroud','Headlight_Projector_Bezel','Headlight_Secondary','Mirror_Rear_Seal','Mirror_Glass_Center','Exhaust_InnerSleeve')):return True
  if lookup[n]['collection']=='INTERIOR':
   return not(n in ['Floor','Dashboard','CenterConsole','TransmissionTunnel','RearBulkhead','Headliner','Steering_Wheel','Steering_Hub','DoorPanel_L','DoorPanel_R','InstrumentCluster','InstrumentCluster_Screen'] or n.startswith(('Seat_Driver','Seat_Passenger')) and not any(x in n for x in ['Accent']))
 if lod>=3:
  if n.startswith(('Diffuser_Fin','Front_Duct_Guide','Engine_Vent_Louver','Rear_Vent_Rib','Wheel_Center_Cap','Brake_Hat','Headlight_Projector_Lens','Headlight_Cavity','Taillight_Cavity','Mirror_Stem')):return True
 return False
# Per-component budgets preserve high-curvature body, split spokes and light signatures.
def budget(o,lod):
 n=o.name; c=category(o); t=lookup[n]['tris']
 hero={'Car_Body':24000,'Hood':3800,'Roof_Panel':4300,'Front_Bumper':2600,'Rear_Bumper':2700,'Rear_Engine_Cover':2300,'Car_Door_L':1800,'Car_Door_R':1800,'Mirror_L':900,'Mirror_R':900,'Dashboard':4100,'Seat_Driver':3900,'Seat_Passenger':3900,'Windshield':2700,'Rear_Glass':2200,'Front_Splitter':1800}
 base=hero.get(n,t*{'Body':.34,'Wheels':.72,'Tires':.82,'Brakes':.31,'Interior':.36,'Glass':.24,'Lights':.25,'Aero_Trim':.28}[c])
 if 'Spoke' in n:base=t*.88
 if 'Shutline' in n or 'Seal' in n:base=t*.28
 if n.startswith('Brake_Radial_Slot'):base=24
 if n.startswith('Tire_Shoulder_Sipe'):base=24
 scale={'Body':[1,.57,.29,.09],'Wheels':[1,.6,.29,.11],'Tires':[1,.64,.38,.16],'Brakes':[1,.65,.3,.12],'Interior':[1,.53,.27,.12],'Glass':[1,.6,.34,.14],'Lights':[1,.55,.28,.12],'Aero_Trim':[1,.52,.26,.10]}[c][lod]
 return max(12,int(base*scale))
def evaluate(o):
 bpy.context.view_layer.update(); e=o.evaluated_get(bpy.context.evaluated_depsgraph_get()); return bpy.data.meshes.new_from_object(e,preserve_all_data_layers=True,depsgraph=bpy.context.evaluated_depsgraph_get())
def tri(me):me.calc_loop_triangles();return len(me.loop_triangles)
# Cache evaluated surfaces; the live reference remains intact.
cache={}
for o in geom:cache[o.name]=evaluate(o)
report={'master_sha256':sourcehash,'master_categories':{},'lods':{},'decisions':[]}
for o in geom:
 c=category(o);report['master_categories'][c]=report['master_categories'].get(c,0)+tri(cache[o.name])
for lod in range(4):
 col=bpy.data.collections.new('Car_LOD'+str(lod));S.collection.children.link(col);cats={}
 for c in ['Body','Wheels','Tires','Brakes','Interior','Glass','Lights','Aero_Trim']:
  sub=bpy.data.collections.new('LOD'+str(lod)+'_'+c);col.children.link(sub);cats[c]=sub
 made={};counts={};decisions=[]
 for src in sorted(geom,key=lambda x:x.name):
  if omit(src.name,lod):continue
  c=category(src);o=bpy.data.objects.new(src.name+'_LOD'+str(lod),cache[src.name].copy());cats[c].objects.link(o);o.matrix_world=src.matrix_world
  for k in src.keys():
   if k!='_RNA_UI':o[k]=src[k]
  o['source_object']=src.name;o['lod_category']=c;o['lod_level']=lod
  # Curves acquire UVs only on converted production mesh; master remains editable.
  if not o.data.uv_layers:
   uv=o.data.uv_layers.new(name='UVMap')
   for p in o.data.polygons:
    for li in p.loop_indices:
     v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v.y*.2,v.z*.2)
   o['uv_meter_scale']=5.
  before=tri(o.data);target=budget(src,lod)
  # First dissolve nearly coplanar interiors, respecting material and UV seams.
  d=o.modifiers.new('Planar reduction; preserve UV and material boundaries','DECIMATE');d.decimate_type='DISSOLVE';d.angle_limit=math.radians([.12,.3,.65,1.2][lod]);d.delimit={'MATERIAL','UV','SEAM'}
  me=evaluate(o);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
  current=tri(me)
  if current>target:
   d=o.modifiers.new('Component budget: '+str(target)+' tris','DECIMATE');d.decimate_type='COLLAPSE';d.ratio=max(.005,target/current);d.use_collapse_triangulate=False
   me=evaluate(o);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
  # Preserve master corner normals on retained surfaces rather than flattening highlights.
  dt=o.modifiers.new('Master surface normal transfer','DATA_TRANSFER');dt.object=src;dt.use_loop_data=True;dt.data_types_loops={'CUSTOM_NORMAL'};dt.loop_mapping='POLYINTERP_NEAREST'
  try:
   me=evaluate(o);o.modifiers.clear();old=o.data;o.data=me;bpy.data.meshes.remove(old)
  except Exception as ex: print('NORMAL TRANSFER',o.name,str(ex),flush=True);o.modifiers.clear()
  made[src.name]=o;count=tri(o.data);counts[c]=counts.get(c,0)+count
  decisions.append({'source':src.name,'category':c,'master':before,'target':target,'actual':count})
 # Parent all rolling components to a clear wheel pivot at the original center; brakes stay separate.
 for key in ['FL','FR','RL','RR']:
  wheel=made['Wheel_'+key];wheel['rotation_axis']='X';wheel['wheel_center_world']=list(wheel.matrix_world.translation)
  for n,o in made.items():
   if o==wheel:continue
   if category(bpy.data.objects[n]) in ['Wheels','Tires'] and ('_'+key in n):
    mw=o.matrix_world.copy();o.parent=wheel;o.matrix_world=mw
 for n,o in made.items():
  if n.startswith(('Steering_','Paddle_')) and n!='Steering_Wheel' and 'Steering_Wheel' in made:
   mw=o.matrix_world.copy();o.parent=made['Steering_Wheel'];o.matrix_world=mw
 report['lods'][str(lod)]={'categories':counts,'total':sum(counts.values()),'objects':len(made),'decisions':decisions}
 print('LOD',lod,counts,'TOTAL',sum(counts.values()),flush=True)
 col.hide_render=lod!=0;col.hide_viewport=lod!=0
master.hide_render=True;master.hide_viewport=True
S['master_06_sha256']=sourcehash;S['lod_phase']='07 controlled component optimization'
(R/'lod_build_stats.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
