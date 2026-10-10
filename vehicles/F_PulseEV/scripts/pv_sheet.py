# Pulse EV blockout sheets (reads previews only): 6-vehicle comparison + zebra comparison against the frozen references. Identical camera rig for all.
import sys; sys.dont_write_bytecode = True
import bpy, numpy as np, os
W_ = '/Users/meetshah/Documents/blender/vehicles/'; PV = W_ + 'F_PulseEV/previews/'
def sheet(rows, cols, out, W=480, H=270, G=6):
    canvas = np.full((len(rows) * (H + G) - G, len(cols) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
    for r, (d, pre) in enumerate(rows):
        for c, v in enumerate(cols):
            f = os.path.join(d, f'{pre}_{v}.png')
            if not os.path.exists(f): print('MISSING', f); continue
            im = bpy.data.images.load(f); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
            y0 = (len(rows) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
    o = bpy.data.images.new('s', canvas.shape[1], canvas.shape[0], alpha=False); o.pixels.foreach_set(canvas.ravel()); o.filepath_raw = out; o.file_format = 'JPEG'; o.save(); print('SHEET', out)
sheet([(W_ + 'A_Discovery/previews', 'VA_hypercar_08'), (W_ + 'B_ZeroGapR/previews', 'ZG'), (W_ + 'C_TitanGT_r1/previews', 'TG'), (W_ + 'D_VortexR_r1/previews', 'VX'), (W_ + 'E_RavenXR/previews', 'RV'), (PV, 'PV')],
      ['front34', 'rear34', 'front', 'rear', 'left', 'top', 'chase'], PV + 'PV_blockout_compare_6cars.jpg')
ZV = ['hood', 'roof', 'front_corner', 'door', 'door_r', 'side_full', 'quarter', 'quarter_r', 'deck', 'deck_r', 'tail_corner', 'tail_corner_r']
sheet([(PV + 'zebra_ref_TG_r1', 'zebra'), (PV + 'zebra_ref_VX_r1', 'zebra'), (PV + 'zebra_ref_RV', 'zebra'), (PV + 'zebra_PV', 'zebra')], ZV, PV + 'PV_zebra_compare_references.jpg', W=320, H=180)
