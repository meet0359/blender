# Phase A comparison sheet: rows = vehicles, columns = views (identical rig). Reads previews only.
import sys; sys.dont_write_bytecode = True
import bpy, numpy as np, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PV = os.path.join(HERE, 'previews')
ROWS = ['racing_car_09', 'hypercar_08']; COLS = ['front34', 'rear34', 'front', 'left', 'chase']; W, H, G = 640, 360, 6
canvas = np.full((len(ROWS) * (H + G) - G, len(COLS) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
for r, t in enumerate(ROWS):
    for c, v in enumerate(COLS):
        im = bpy.data.images.load(os.path.join(PV, f'VA_{t}_{v}.png')); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
        y0 = (len(ROWS) - 1 - r) * (H + G); x0 = c * (W + G); canvas[y0:y0 + H, x0:x0 + W] = px; bpy.data.images.remove(im)
out = bpy.data.images.new('VA_compare', canvas.shape[1], canvas.shape[0], alpha=False); out.pixels.foreach_set(canvas.ravel())
out.filepath_raw = os.path.join(PV, 'VA_compare_racingcar_vs_hypercar.jpg'); out.file_format = 'JPEG'; out.save(); print('SHEET', out.filepath_raw)
