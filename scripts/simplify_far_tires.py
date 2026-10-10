import bpy,bmesh,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];col=bpy.data.collections['Car_LOD3'];col.hide_viewport=False;bpy.data.collections['REFERENCE_Master_06'].hide_viewport=False
for key in ['FL','FR','RL','RR']:
 o=bpy.data.objects['Wheel_'+key+'_LOD3'];src=bpy.data.objects['Wheel_'+key];r=.345 if key[0]=='F' else .365;w=.29 if key[0]=='F' else .33;ri=.254 if key[0]=='F' else .267
 profile=[(-w/2+.015,ri-.006),(-w/2,ri+.01),(-w/2-.003,r-.045),(-w/2+.028,r),(w/2-.028,r),(w/2+.003,r-.045),(w/2,ri+.01),(w/2-.015,ri-.006)]
 N=32;vs=[(x,rr*math.cos(i*2*math.pi/N),max(-r+.0015,rr*math.sin(i*2*math.pi/N))) for x,rr in profile for i in range(N)];fs=[(j*N+i,j*N+(i+1)%N,((j+1)%8)*N+(i+1)%N,((j+1)%8)*N+i) for j in range(8) for i in range(N)]
 me=bpy.data.meshes.new(o.name+'_smooth');me.from_pydata(vs,[],fs);me.materials.append(o.data.materials[0]);me.uv_layers.new(name='UVMap');bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for p in me.polygons:p.use_smooth=True
 old=o.data;o.data=me;bpy.data.meshes.remove(old);dt=o.modifiers.new('Preserve tire atlas coordinates','DATA_TRANSFER');dt.object=src;dt.use_loop_data=True;dt.data_types_loops={'UV'};dt.loop_mapping='POLYINTERP_NEAREST';bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();new=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg);o.modifiers.clear();o.data=new;bpy.data.meshes.remove(me)
 o['far_tire']='32 radial segments, eight smooth profile rings, no physical tread'
col.hide_viewport=True;bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_07_optimized_lods.blend'))
