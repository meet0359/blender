import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.samples=16
s.render.bake.margin=12; s.render.bake.use_clear=True
groups={}
for o in bpy.data.objects:
    if o.type=='MESH' and 'texture_group' in o: groups.setdefault(o['texture_group'],[]).append(o)
manifest=json.loads((ROOT/'texture_manifest.json').read_text())
for group,objs in groups.items():
    res=2048 if group in ['body','interior'] else 1024
    img=bpy.data.images.new('Atlas_'+group+'_CavityAO',res,res,alpha=False)
    img.colorspace_settings.name='Non-Color'; img.generated_color=(1,1,1,1)
    path=ROOT/'textures/racing_car'/group/(group+'_Atlas_CavityAO.png'); path.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT'); materials=set(); mods=[]
    for o in objs:
        o.select_set(True)
        for m in o.modifiers:
            if m.type in ['MIRROR','SOLIDIFY']:
                mods.append((m,m.show_render,m.show_viewport)); m.show_render=False; m.show_viewport=False
        materials.update(m for m in o.data.materials if m)
    for m in materials:
        for node in m.node_tree.nodes: node.select=False
        node=m.node_tree.nodes.new('ShaderNodeTexImage'); node.image=img; node.name='BakeTarget_'+group; node.label='Unique atlas cavity AO — '+group; node.location=(-1200,-1100)
        m.node_tree.nodes.active=node; node.select=True
    bpy.context.view_layer.objects.active=objs[0]
    print('BAKE AO',group,res,len(objs),flush=True)
    bpy.ops.object.bake(type='AO')
    img.filepath_raw=str(path); img.file_format='PNG'; img.save(); img.filepath='//'+str(path.relative_to(ROOT))
    for m,render,view in mods: m.show_render=render; m.show_viewport=view
    manifest['atlas_'+group]={'resolution':res,'maps':{'AO':str(path.relative_to(ROOT))},'scope':'Canonical base skin AO; Mirror/Solidify temporarily disabled to avoid conflicting backface UV writes; live modifiers restored'}
(ROOT/'texture_manifest.json').write_text(json.dumps(manifest,indent=2))
s.cycles.samples=48
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_06_materials_uv_working.blend'))
print('AO BAKES COMPLETE',flush=True)
