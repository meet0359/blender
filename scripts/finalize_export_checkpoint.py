import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=bpy.context.scene
for i in range(4):
 c=bpy.data.collections['Car_LOD'+str(i)];c.hide_render=i!=0;c.hide_viewport=i!=0
bpy.data.collections['REFERENCE_Master_06'].hide_render=True;bpy.data.collections['REFERENCE_Master_06'].hide_viewport=True
for o in bpy.data.collections['COLLISION'].all_objects:
 if o.type=='MESH':o.hide_render=True;o.display_type='WIRE';o.color=(.01,.6,.8,1)
for n in ['export_report.md','material_export_notes.md','export_validation.txt']:
 t=bpy.data.texts.get(n) or bpy.data.texts.new(n);t.clear();t.write((R/n).read_text())
S['export_phase']='08 — colliders, explicit UVs, ORM, validated FBX and GLB';S['export_validation_errors']=0;S['reimport_validation_errors']=0;S['export_report']='//export_report.md';S['export_script']='//scripts/export_test_assets.py'
S.camera=bpy.data.objects['Camera_Presentation'];bpy.ops.object.select_all(action='DESELECT');root=bpy.data.objects['Car_Root'];root.select_set(True);bpy.context.view_layer.objects.active=root
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_extras=True
bpy.ops.wm.save_as_mainfile(filepath=str(R/'racing_car_08_export_ready.blend'));print('FINAL CHECKPOINT SAVED',flush=True)
