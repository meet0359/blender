# Consolidated fleet comparison sheet (read-only): one row per vehicle, same cameras / lights / samples; last column = orthographic side at ONE shared scale.
#   Blender -b --factory-startup --python ts_fleet_sheet.py -- <image_dir> <out.jpg> <tag1,tag2,...> [view1,view2,...]
#   or explicit cells (paths relative to image_dir):  ... -- <image_dir> <out.jpg> "a.png,b.png,c.png;d.png,e.png"
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; D, OUT, TAGS = a[0], a[1], a[2].split(',')
VIEWS = a[3].split(',') if len(a) > 3 else ['front34', 'side', 'rear34', 'ortho_side']
W, H, G = 640, 360, 6
ROWS = [r.split(',') for r in a[2].split(';')] if '.png' in a[2] else [[f'{t}_{v}.png' for v in VIEWS] for t in TAGS]
NC = max(len(r) for r in ROWS)
canvas = np.full((len(ROWS) * (H + G) - G, NC * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
for r, row in enumerate(ROWS):                                                # row 0 = top of the sheet
    for c, fn in enumerate(row):
        f = os.path.join(D, fn)
        if not os.path.exists(f): print('MISSING', f); continue
        im = bpy.data.images.load(f); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
        y0 = (len(ROWS) - 1 - r) * (H + G); canvas[y0:y0 + H, c * (W + G):c * (W + G) + W] = px; bpy.data.images.remove(im)
img = bpy.data.images.new('sheet', canvas.shape[1], canvas.shape[0], alpha=False); img.pixels.foreach_set(canvas.ravel())
img.filepath_raw = OUT; img.file_format = 'JPEG'; img.save(); print('SHEET', OUT, f'{len(ROWS)} rows x {NC} cols')
