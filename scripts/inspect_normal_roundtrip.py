import bpy,numpy as np
from pathlib import Path
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parents[1];n='Wheel_Lug_FL_1_LOD0';o=bpy.data.objects[n];s=[tuple(x.vector) for x in o.data.corner_normals];print('SOURCE',s[:8]);source=[tuple(v.co) for v in o.data.vertices]
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(R/'exports/racing_car_LOD0.fbx'));o=bpy.data.objects[n];print('IMPORTED', [tuple(x.vector) for x in o.data.corner_normals][:8]);print('MATRIX',o.matrix_world);print('SMOOTH',[(p.use_smooth) for p in o.data.polygons][:4]);print('CUSTOM',o.data.has_custom_normals)
