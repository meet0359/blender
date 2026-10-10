# Design-blockout review sheets (read-only): new vehicle blockout + side-by-side against the approved previous vehicle (same cameras / lighting).
#   Blender -b --factory-startup --python ts_blockout_sheets.py -- <Vehicle_Folder> <tag> <reference_folder> <reference_tag>
#   e.g. Traffic_Sedan_B SedanB Traffic_Sedan_A_r3 SedanA   (row 1 = reference, row 2 = new vehicle)
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.dont_write_bytecode = True
from ts_lib import *
VEH, TAG, REF, RTAG = sys.argv[sys.argv.index('--') + 1:][:4]
P = os.path.join(vroot(VEH), 'previews', 'blockout'); C = os.path.join(P, 'compare_' + RTAG[-1]); RP = os.path.join(vroot(REF), 'previews')
def sheet(rows, cols, out, W=640, H=360, G=6):
    canvas = np.full((len(rows) * (H + G) - G, len(cols) * (W + G) - G, 4), .08, np.float32); canvas[..., 3] = 1
    for r, (folder, pre) in enumerate(rows):
        for c, v in enumerate(cols):
            f = os.path.join(folder, f'{pre}_{v}.png')
            if not os.path.exists(f): print('MISSING', f); continue
            im = bpy.data.images.load(f); im.scale(W, H); px = np.array(im.pixels[:], np.float32).reshape(H, W, 4)
            canvas[(len(rows) - 1 - r) * (H + G):(len(rows) - 1 - r) * (H + G) + H, c * (W + G):c * (W + G) + W] = px; bpy.data.images.remove(im)
    img = bpy.data.images.new('sheet', canvas.shape[1], canvas.shape[0], alpha=False); img.pixels.foreach_set(canvas.ravel()); img.filepath_raw = out; img.file_format = 'JPEG'; img.save(); bpy.data.images.remove(img); print('SHEET', out)
S_ = lambda n: os.path.join(P, f'{TAG}_blockout_sheet_{n}.jpg')
sheet([(P, TAG)] * 2, ['front34', 'rear34', 'side'], S_('studio_a'), W=800, H=450) if False else None
sheet([(P, TAG)], ['front34', 'rear34', 'side'], S_('studio_1'), W=800, H=450); sheet([(P, TAG)], ['front', 'rear', 'top'], S_('studio_2'), W=800, H=450)
sheet([(P, TAG)], ['game_close', 'game_normal', 'game_far'], S_('chase_camera'), W=800, H=450)
sheet([(P, TAG)], ['day_front34', 'day_rear34', 'day_side'], S_('daylight'), W=800, H=450)
sheet([(os.path.join(P, 'clay'), 'clay')], ['front34', 'rear34', 'side', 'front', 'rear'], S_('clay'), W=640, H=360)
ZV = ['hood', 'roof', 'deck', 'deck_r', 'door', 'side_full', 'quarter', 'quarter_r', 'tail_corner', 'tail_corner_r']
sheet([(os.path.join(RP, 'zebra_master'), 'zebra'), (os.path.join(P, 'zebra'), 'zebra')], ZV, S_(f'zebra_{RTAG}_vs_{TAG}'), W=360, H=203)
# side by side: row 1 = reference (approved), row 2 = new design — identical cameras, lights, samples
sheet([(C, RTAG), (P, TAG)], ['front34', 'rear34', 'side'], S_(f'{RTAG}_vs_{TAG}_threequarter_side'), W=800, H=450)
sheet([(C, RTAG), (P, TAG)], ['front', 'rear', 'top'], S_(f'{RTAG}_vs_{TAG}_front_rear_top'), W=800, H=450)
sheet([(C, RTAG), (P, TAG)], ['ortho_side', 'ortho_front', 'ortho_rear'], S_(f'{RTAG}_vs_{TAG}_orthographic_same_scale'), W=800, H=450)
sheet([(C, 'clayA'), (os.path.join(P, 'clay'), 'clay')], ['front34', 'rear34', 'side'], S_(f'{RTAG}_vs_{TAG}_clay'), W=800, H=450)
sheet([(RP, 'TrafficSedanA'), (P, TAG)], ['game_close', 'game_normal', 'game_far'], S_(f'{RTAG}_vs_{TAG}_chase'), W=800, H=450)
print('SHEETS DONE')
