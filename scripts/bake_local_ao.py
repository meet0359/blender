"""Canonical atlas AO with finite distance, one temporary evaluated bake mesh per atlas."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.samples=16; s.render.bake.margin=8; s.render.bake.use_clear=True
groups={}
for o in bpy.data.objects:
    if o.type=='MESH' and 'texture_group' in o: groups.setdefault(o['texture_group'],[]).append(o)
manifest=json.loads((ROOT/'texture_manifest.json').read_text())
for group,objs in groups.items():
    res=2048 if group in ['body','interior'] else 1024
    mods=[]; states=[]
    for o in objs:
        states.append((o,o.hide_render))
        for m in o.modifiers:
            if m.type in ['MIRROR','SOLIDIFY']:
                mods.append((m,m.show_viewport,m.show_render)); m.show_viewport=False; m.show_render=False
    bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get()
    verts=[]; faces=[]; uvs=[]
    for o in objs:
        e=o.evaluated_get(dg); me=e.to_mesh(); offset=len(verts)
        verts.extend(tuple(e.matrix_world@v.co) for v in me.vertices)
        faces.extend(tuple(offset+i for i in p.vertices) for p in me.polygons)
        uv=me.uv_layers['UVMap']; uvs.extend(tuple(l.uv) for l in uv.data)
        e.to_mesh_clear(); o.hide_render=True
    mesh=bpy.data.meshes.new('QA_AO_BakeMesh'); mesh.from_pydata(verts,[],faces); mesh.update()
    layer=mesh.uv_layers.new(name='UVMap')
    for l,p in zip(layer.data,uvs): l.uv=p
    obj=bpy.data.objects.new('QA_AO_BakeTarget',mesh); bpy.context.scene.collection.objects.link(obj)
    mat=bpy.data.materials.new('QA_AO_BakeMaterial'); mat.use_nodes=True; nd=mat.node_tree.nodes; nd.clear(); lk=mat.node_tree.links
    ao=nd.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value=.12; ao.samples=16
    emit=nd.new('ShaderNodeEmission'); lk.new(ao.outputs['Color'],emit.inputs['Color'])
    out=nd.new('ShaderNodeOutputMaterial'); lk.new(emit.outputs[0],out.inputs['Surface'])
    img=bpy.data.images.new('Atlas_'+group+'_LocalAO',res,res,alpha=False); img.colorspace_settings.name='Non-Color'; img.use_fake_user=True
    node=nd.new('ShaderNodeTexImage'); node.image=img; nd.active=node; node.select=True; mesh.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
    bpy.context.view_layer.update(); print('LOCAL AO',group,res,flush=True); bpy.ops.object.bake(type='EMIT')
    path=ROOT/'textures/racing_car'/group/(group+'_Atlas_CavityAO.png'); path.parent.mkdir(parents=True,exist_ok=True)
    img.filepath_raw=str(path); img.file_format='PNG'; img.save(); img.filepath='//'+str(path.relative_to(ROOT))
    bpy.data.objects.remove(obj,do_unlink=True); bpy.data.meshes.remove(mesh); bpy.data.materials.remove(mat)
    for m,v,r in mods: m.show_viewport=v; m.show_render=r
    for o,h in states: o.hide_render=h
    manifest['atlas_'+group]={'resolution':res,'maps':{'AO':str(path.relative_to(ROOT))},'scope':'12 cm finite-distance cavity AO; evaluated canonical skin, mirrored and back surfaces excluded to avoid conflicting UV writes. Modifiers restored.'}
(ROOT/'texture_manifest.json').write_text(json.dumps(manifest,indent=2))
s.cycles.samples=48; bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_06_materials_uv_working.blend'))
print('FINITE-DISTANCE AO COMPLETE',flush=True)
