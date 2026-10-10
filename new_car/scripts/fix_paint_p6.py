# Apply the tuned Racing Red to the saved Phase-6 file (same values as lookdev_p6.PAINT_RED).
import bpy
b = bpy.data.materials["MAT_CarPaint_RacingRed"].node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.80, 0.010, 0.024, 1)
bpy.data.materials["MAT_CarPaint_RacingRed"].diffuse_color = (0.80, 0.010, 0.024, 1)
bpy.ops.wm.save_mainfile()
