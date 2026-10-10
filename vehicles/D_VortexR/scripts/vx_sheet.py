# Vortex R blockout sheets (reads previews only): 4-row comparison (Hypercar, Zero Gap R, Titan GT, Vortex R) + zebra comparison (Titan GT vs Vortex R).
import sys; sys.dont_write_bytecode = True
import bpy, numpy as np, os
W_ = '/Users/meetshah/Documents/blender/vehicles/'; PV = W_ + 'D_VortexR/previews/'
def sheet(rows, cols, out, W=480, H=270, G=6):
    canvas = np.full((len(rows) * (H + G) - G, len(cols) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
    for r, (d, pre) in enumerate(rows):
        for c, v in enumerate(cols):
            im = bpy.data.images.load(os.path.join(d, f'{pre}_{v}.png')); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
            y0 = (len(rows) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
    o = bpy.data.images.new('s', canvas.shape[1], canvas.shape[0], alpha=False); o.pixels.foreach_set(canvas.ravel()); o.filepath_raw = out; o.file_format = 'JPEG'; o.save(); print('SHEET', out)
sheet([(W_ + 'A_Discovery/previews', 'VA_hypercar_08'), (W_ + 'B_ZeroGapR/previews', 'ZG'), (W_ + 'C_TitanGT/previews', 'TG'), (PV, 'VX')],
      ['front34', 'rear34', 'front', 'rear', 'left', 'top', 'chase'], PV + 'VX_blockout_compare_4cars.jpg')
sheet([(PV + 'zebra_TG_reference', 'zebra'), (PV + 'zebra_VX', 'zebra')], ['hood', 'roof', 'deck', 'door', 'side_full'], PV + 'VX_zebra_compare_titangt_vortexr.jpg')
