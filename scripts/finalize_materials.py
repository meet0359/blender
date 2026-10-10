import bpy,json,hashlib,runpy,struct
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
original=json.loads((ROOT/'materials_source_geometry.json').read_text())
for name,sig in original.items():
 o=bpy.data.objects[name]; h=hashlib.sha256(); h.update(np.array([tuple(v.co) for v in o.data.vertices],dtype=np.float32).tobytes()); h.update(str([tuple(p.vertices) for p in o.data.polygons]).encode()); h.update(np.array(o.matrix_world,dtype=np.float32).tobytes()); assert h.hexdigest()==sig,name
 uv=o.data.uv_layers['UVMap'].data; edges={}
 for p in o.data.polygons:
  ids=list(p.loop_indices)
  for i,l in enumerate(ids):
   nxt=ids[(i+1)%len(ids)]; a=o.data.loops[l].vertex_index; b=o.data.loops[nxt].vertex_index
   edges.setdefault(o.data.loops[l].edge_index,[]).append({a:tuple(uv[l].uv),b:tuple(uv[nxt].uv)})
 for idx,rows in edges.items(): o.data.edges[idx].use_seam=len(rows)!=2 or rows[0]!=rows[1]
assert hashlib.sha256((ROOT/'racing_car_05_interior.blend').read_bytes()).hexdigest()==bpy.context.scene['source_05_sha256']
for m in bpy.data.materials:
 if m.use_nodes:
  for n in list(m.node_tree.nodes):
   if n.name.startswith('BakeTarget_'): m.node_tree.nodes.remove(n)
for path in (ROOT/'textures/racing_car').rglob('*_Atlas_CavityAO.png'):
 img=bpy.data.images.load(str(path),check_existing=True); img.reload(); img.use_fake_user=True; img.colorspace_settings.name='Non-Color'; img.filepath='//'+str(path.relative_to(ROOT))
for kind,folder in [('leather','interior'),('plastic','trim'),('rubber','tires')]:
 img=bpy.data.images.load(str(ROOT/'textures/racing_car'/folder/(kind+'_Metallic.png')),check_existing=True)
 values=np.empty(len(img.pixels),dtype=np.float32); img.pixels.foreach_get(values); assert values[::4].max()<0.001,kind
for img in bpy.data.images:
 if img.source=='FILE' and img.filepath:
  path=Path(bpy.path.abspath(img.filepath)); assert path.exists(),str(path)
  if path.is_relative_to(ROOT): img.filepath='//'+str(path.relative_to(ROOT))
for p in (ROOT/'previews').glob('materials_*.png'):
 if 'checker' not in p.name: assert struct.unpack('>II',p.read_bytes()[16:24])==(1920,1080),p.name
assert len(list((ROOT/'previews').glob('materials_*.png')))==19
stats=json.loads((ROOT/'materials_stats.json').read_text()); stats['texture_count']=len(list((ROOT/'textures/racing_car').rglob('*.png'))); (ROOT/'materials_stats.json').write_text(json.dumps(stats,indent=2))
runpy.run_path(str(ROOT/'scripts/write_materials_report.py'))
for fn,n in [('materials_report.md','READ_ME_Materials_UV_06'),('uv_validation.txt','VALIDATION_UV_06'),('shader_validation.txt','VALIDATION_Shader_06')]:
 t=bpy.data.texts.get(n) or bpy.data.texts.new(n); t.clear(); t.write((ROOT/fn).read_text())
bpy.context.scene.camera=bpy.data.objects['Camera_Presentation']
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_06_materials_uv.blend'))
print('FINAL CHECKS PASSED: geometry preserved, relative texture links resolved, 17 full-resolution previews')
