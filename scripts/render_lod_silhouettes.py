import bpy,json
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=bpy.context.scene
S.render.engine='BLENDER_WORKBENCH';S.render.resolution_x=640;S.render.resolution_y=360;S.render.resolution_percentage=100;S.render.film_transparent=True
sh=S.display.shading;sh.light='FLAT';sh.color_type='SINGLE';sh.single_color=(.02,.02,.02);sh.show_shadows=False;sh.show_cavity=False;sh.show_specular_highlight=False
for o in bpy.data.collections['PRESENTATION'].all_objects:
 if o.type=='MESH':o.hide_render=True
cols=[bpy.data.collections['REFERENCE_Master_06']]+[bpy.data.collections['Car_LOD'+str(i)] for i in range(4)]
views={'side':'Camera_Side','front_3q':'Camera_Presentation','rear_3q':'Camera_Rear_ThreeQuarter','front':'Camera_Front','rear':'Camera_Rear'}
results={};out=R/'previews/lod_silhouettes';out.mkdir(exist_ok=True)
for view,cam in views.items():
 masks=[]
 for idx,col in enumerate(cols):
  for c in cols:c.hide_render=c!=col;c.hide_viewport=c!=col
  S.camera=bpy.data.objects[cam];path=out/(('master' if idx==0 else 'lod'+str(idx-1))+'_'+view+'.png');S.render.filepath=str(path);bpy.ops.render.render(write_still=True)
  im=bpy.data.images.load(str(path),check_existing=False);p=np.array(im.pixels[:]).reshape(360,640,4);masks.append(p[:,:,3]>.5);bpy.data.images.remove(im)
 results[view]={}
 # White board, five rows: master then LOD0..3. Overlay master/LOD0 outline disagreement in red.
 board=np.ones((360*5,640,4),dtype=np.float32)
 for idx,mask in enumerate(masks):
  ref=masks[0] if idx<=1 else masks[1];union=(mask|ref).sum();iou=(mask&ref).sum()/max(1,union)
  name='master' if idx==0 else 'LOD'+str(idx-1);results[view][name]={'iou_reference':float(iou),'different_pixels':int((mask^ref).sum()),'reference':'master' if idx<=1 else 'LOD0'}
  row=board[(4-idx)*360:(5-idx)*360];row[mask,:3]=.035;row[mask^ref,:3]=[.85,.10,.06]
 img=bpy.data.images.new('Silhouette comparison '+view,640,1800,alpha=True);img.pixels.foreach_set(board.ravel());img.filepath_raw=str(R/'previews'/('lod_comparison_'+view+'.png'));img.file_format='PNG';img.save()
 print('SILHOUETTE',view,results[view],flush=True)
(R/'lod_silhouette_metrics.json').write_text(json.dumps(results,indent=2))
