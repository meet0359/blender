# Titan GT blockout comparison sheet: rows Hypercar (frozen), Zero Gap R (frozen), Titan GT blockout; identical camera rig. Reads previews only.
import sys; sys.dont_write_bytecode = True
import bpy, numpy as np, os
W_ = '/Users/meetshah/Documents/blender/vehicles/'
ROWS = [(W_ + 'A_Discovery/previews', 'VA_hypercar_08'), (W_ + 'B_ZeroGapR/previews', 'ZG'), (W_ + 'C_TitanGT/previews', 'TG')]
COLS = ['front34', 'rear34', 'front', 'rear', 'left', 'top', 'chase']; W, H, G = 520, 292, 6
canvas = np.full((len(ROWS) * (H + G) - G, len(COLS) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
for r, (d, pre) in enumerate(ROWS):
    for c, v in enumerate(COLS):
        im = bpy.data.images.load(os.path.join(d, f'{pre}_{v}.png')); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
        y0 = (len(ROWS) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
out = bpy.data.images.new('s', canvas.shape[1], canvas.shape[0], alpha=False); out.pixels.foreach_set(canvas.ravel())
out.filepath_raw = W_ + 'C_TitanGT/previews/TG_blockout_compare_hypercar_zerogapr.jpg'; out.file_format = 'JPEG'; out.save(); print('SHEET', out.filepath_raw)
