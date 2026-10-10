import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=8
S.render.bake.use_selected_to_active=True;S.render.bake.use_clear=True;S.render.bake.margin=8;S.render.bake.cage_extrusion=.018;S.render.bake.max_ray_distance=.035;S.render.bake.normal_space='TANGENT'
savings=json.loads((R/'detail_bake_savings.json').read_text()); manifest={}
for group in ['tires']:
 if group=='tires':
  base=[bpy.data.objects['Wheel_'+key] for key in ['FL','FR','RL','RR']];details=[bpy.data.objects['Tire_Sidewall_Markings_'+key] for key in ['FL','FR','RL','RR']]
 else:
  base=[o for o in bpy.data.collections['INTERIOR'].all_objects if o.type=='MESH' and o.name not in savings];details=[bpy.data.objects[n] for n in savings if not n.startswith('Tire_')]
 originals=list(set(base+details));verts=[];faces=[];uvs=[]
 for o in base:
  mods=[(m,m.show_viewport) for m in o.modifiers if m.type=='SOLIDIFY']
  for m,v in mods:m.show_viewport=False
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dg);me=e.to_mesh();off=len(verts)
  verts.extend(tuple(o.matrix_world@v.co) for v in me.vertices);faces.extend(tuple(off+i for i in p.vertices) for p in me.polygons);uvs.extend(tuple(l.uv) for l in me.uv_layers['UVMap'].data);e.to_mesh_clear()
  for m,v in mods:m.show_viewport=v
 mesh=bpy.data.meshes.new('Bake_Low_Canonical');mesh.from_pydata(verts,[],faces);mesh.update();uv=mesh.uv_layers.new(name='UVMap')
 for l,p in zip(uv.data,uvs):l.uv=p
 for p in mesh.polygons:p.use_smooth=True
 obj=bpy.data.objects.new('Bake_Low_Canonical',mesh);S.collection.objects.link(obj)
 mat=bpy.data.materials.new('Bake_Target');mat.use_nodes=True;mesh.materials.append(mat);node=mat.node_tree.nodes.new('ShaderNodeTexImage');mat.node_tree.nodes.active=node
 bpy.ops.object.select_all(action='DESELECT')
 for o in originals:o.select_set(True)
 obj.select_set(True);bpy.context.view_layer.objects.active=obj
 out=R/'textures/racing_car'/group;out.mkdir(parents=True,exist_ok=True)
 for kind in ['Mask']:
  img=bpy.data.images.new('LOD_'+group+'_'+kind,4096,4096,alpha=False);img.colorspace_settings.name='Non-Color';node.image=img
  restore=[];aomat=None
  if kind=='Mask':
   black=bpy.data.materials.new('Bake_Black');black.use_nodes=True
   white=bpy.data.materials.new('Bake_White');white.use_nodes=True
   for m,val in [(black,0.),(white,1.)]:
    ns=m.node_tree.nodes;ns.clear();em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(val,val,val,1);outnode=ns.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],outnode.inputs[0])
   for o in originals:
    restore.append((o,list(o.data.materials)))
    for i in range(len(o.data.materials)):o.data.materials[i]=white if o in details else black
  print('BAKE',group,kind,flush=True);bpy.ops.object.bake(type='NORMAL' if kind=='Normal' else 'EMIT')
  path=out/('lod_detail_'+kind+'.png');img.filepath_raw=str(path);img.file_format='PNG';img.save();manifest[group+'_'+kind]=str(path.relative_to(R))
  for o,mats in restore:
   for i,m in enumerate(mats):o.data.materials[i]=m
  if aomat:bpy.data.materials.remove(aomat)
 bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh);bpy.data.materials.remove(mat)
(R/'lod_mask_manifest.json').write_text(json.dumps(manifest,indent=2));print('DETAIL BAKES FINISHED',flush=True)
