import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];maps=json.loads((R/'lod_bake_manifest.json').read_text());images={}
for key,path in maps.items():
 im=bpy.data.images.load(str(R/path),check_existing=True);im.colorspace_settings.name='Non-Color';im.filepath='//'+path;im.use_fake_user=True;images[key]=im
mask=bpy.data.images.load(str(R/'textures/racing_car/tires/lod_detail_Mask.png'),check_existing=True);mask.colorspace_settings.name='Non-Color';mask.filepath='//textures/racing_car/tires/lod_detail_Mask.png'
variants={}
for lod in range(4):
 for o in list(bpy.data.collections['Car_LOD'+str(lod)].all_objects):
  group='tires' if o['source_object'] in ['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR'] else 'interior' if o['lod_category']=='Interior' else None
  if not group:continue
  for slot in o.material_slots:
   src=slot.material
   if not src or not src.use_nodes:continue
   key=(src.name,group)
   if key not in variants:
    m=src.copy();m.name=src.name+'_LOD_Detail';ns=m.node_tree.nodes;links=m.node_tree.links
    bs=next((n for n in ns if n.type=='BSDF_PRINCIPLED'),None)
    if not bs:variants[key]=src;continue
    uv=ns.new('ShaderNodeUVMap');uv.uv_map='UVMap';uv.label='Preserved unique atlas UVs'
    tex=ns.new('ShaderNodeTexImage');tex.image=images[group+'_Normal'];tex.label='Master-to-canonical tangent detail bake';links.new(uv.outputs['UV'],tex.inputs['Vector'])
    normal=next((n for n in ns if n.type=='NORMAL_MAP'),None)
    if normal and normal.inputs['Color'].is_linked:
     prev=normal.inputs['Color'].links[0].from_socket;add=ns.new('ShaderNodeVectorMath');add.operation='ADD';links.new(prev,add.inputs[0]);links.new(tex.outputs['Color'],add.inputs[1]);sub=ns.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=(.5,.5,1.);links.new(add.outputs[0],sub.inputs[0]);links.new(sub.outputs[0],normal.inputs['Color'])
    else:
     normal=ns.new('ShaderNodeNormalMap');links.new(tex.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs[0],bs.inputs['Normal'])
    normal.uv_map='UVMap'
    if group=='tires':
     mt=ns.new('ShaderNodeTexImage');mt.image=mask;links.new(uv.outputs['UV'],mt.inputs['Vector'])
     mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.inputs[2].default_value=(.07,.073,.078,1);links.new(mt.outputs['Color'],mix.inputs[0])
     if bs.inputs['Base Color'].is_linked:links.new(bs.inputs['Base Color'].links[0].from_socket,mix.inputs[1])
     else:mix.inputs[1].default_value=bs.inputs['Base Color'].default_value
     links.new(mix.outputs[0],bs.inputs['Base Color'])
    m['detail_bake']='Shared across all four LODs; original material parameters retained';variants[key]=m
   slot.material=variants[key]
report={'new_shared_variants':[m.name for m in variants.values()],'normal_space':'Tangent +Y','images':maps,'letter_mask':mask.filepath,'note':'AO provided separately, not multiplied into Cycles lighting. Normal detail adds to existing tangent micro-normal; gross shape kept in mesh.'}
(R/'lod_material_changes.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
