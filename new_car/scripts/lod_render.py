# Phase 7 QA renders: LOD0 close-ups, distance views, master/LOD comparison montages, silhouette IoU.
# Args after "--": stages to run (sil, lod0, dist, compare); default all. Never saves the .blend.
import bpy, os, sys, json
import numpy as np
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = os.path.join(ROOT, "previews"); TMP = os.path.join(ROOT, "previews", "_lodqa"); os.makedirs(TMP, exist_ok=True)
stages = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["sil", "lod0", "dist", "compare"]
sc = bpy.context.scene
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for d in prefs.devices: d.use = True
sc.cycles.device = "GPU"
sc.render.use_persistent_data = False      # persistent data ignores collection visibility switches between renders
SETS = ["Master", "LOD0", "LOD1", "LOD2", "LOD3"]
lcs = bpy.context.view_layer.layer_collection.children

def show(which):
    # only toggle 'exclude' when it changes: re-excluding an excluded collection records its children as
    # excluded, and they then stay hidden when the parent is re-included.
    for name, key in [("REFERENCE_Master", "Master")] + [(f"Car_LOD{i}", f"LOD{i}") for i in range(4)]:
        ex = which != key
        if lcs[name].exclude != ex:
            lcs[name].exclude = ex
        bpy.data.collections[name].hide_render = ex

def render(cam, path, res=(1600, 900), samples=32):
    sc.camera = bpy.data.objects[cam]; sc.render.resolution_x, sc.render.resolution_y = res
    sc.cycles.samples = samples; sc.render.filepath = path
    bpy.ops.render.render(write_still=True); print("RENDERED", path, flush=True)

def load(path):
    im = bpy.data.images.load(path); a = np.array(im.pixels[:], np.float32).reshape(im.size[1], im.size[0], 4)
    bpy.data.images.remove(im); return a

def save(arr, path):
    h, w = arr.shape[:2]; im = bpy.data.images.new("comp", w, h, alpha=False)
    im.pixels.foreach_set(arr.astype(np.float32).ravel()); im.filepath_raw = path; im.file_format = 'PNG'; im.save()
    bpy.data.images.remove(im)

def cam(name, loc, lens, tgt=(0, 0, 0.5)):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    co = bpy.data.objects.new(name, cd); sc.collection.objects.link(co); co.location = loc
    co.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return name

VIEWS = ["side", "front", "rear", "front_3q", "rear_3q"]
if "sil" in stages:                     # silhouette masks -> IoU
    floor = bpy.data.objects["Studio_Floor"]; floor.hide_render = True
    bg = sc.world.node_tree.nodes["Background"]; old_bg = tuple(bg.inputs[0].default_value), bg.inputs[1].default_value
    bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = 1
    blk = bpy.data.materials.new("SIL"); blk.use_nodes = True; nt = blk.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (0, 0, 0, 1)
    nt.links.new(e.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs[0])
    bpy.context.view_layer.material_override = blk
    vt = sc.view_settings.view_transform; sc.view_settings.view_transform = "Standard"
    masks = {}
    for s in SETS:
        show(s)
        for v in VIEWS:
            p = os.path.join(TMP, f"sil_{s}_{v}.png"); render(f"Cam_{v}", p, (1280, 720), 4)
            masks[(s, v)] = load(p)[..., 0] < 0.5
    iou = {}
    for a, b in (("LOD0", "Master"), ("LOD1", "LOD0"), ("LOD2", "LOD0"), ("LOD3", "LOD0")):
        iou[f"{a}_vs_{b}"] = {v: round(float((masks[(a, v)] & masks[(b, v)]).sum() / (masks[(a, v)] | masks[(b, v)]).sum()) * 100, 2) for v in VIEWS}
    json.dump(iou, open(os.path.join(ROOT, "reports", "phase_07_silhouette_iou.json"), "w"), indent=1)
    print("IOU", json.dumps(iou))
    bpy.context.view_layer.material_override = None; floor.hide_render = False
    bg.inputs[0].default_value, bg.inputs[1].default_value = old_bg; sc.view_settings.view_transform = vt

if "lod0" in stages:                    # hero LOD0 close-ups
    show("LOD0")
    for v in ("front_3q", "rear_3q", "side", "wheel"):
        render(f"Cam_{v}", os.path.join(PRE, f"lod0_{v}.png"))
    cf = bpy.data.objects["Light_CabinFill"].data; e0 = cf.energy; cf.energy = 40
    glossy = [(o, o.visible_glossy) for o in bpy.data.collections["HC_Studio"].objects if o.type == 'LIGHT']
    for o, _ in glossy: o.visible_glossy = False
    render("Cam_int_cockpit", os.path.join(PRE, "lod0_cockpit.png"), samples=64)
    cf.energy = e0
    for o, g in glossy: o.visible_glossy = g

if "dist" in stages:                    # inspection distances 15 / 30 / 60 m, 50 mm lens (~40 deg hfov)
    d3 = Vector((-0.67, -0.74, 0.0)).normalized()
    for lod, dist in ((1, 15), (2, 30), (3, 60)):
        show(f"LOD{lod}")
        c = cam(f"Cam_dist_{dist}", tuple(d3 * dist + Vector((0, 0, 1.6))), 50)
        render(c, os.path.join(PRE, f"lod{lod}_distance.png"))

if "compare" in stages:                 # 3x2 montage: Master, LOD0, LOD1 / LOD2, LOD3, blank
    for v in ("side", "front_3q", "rear_3q"):
        tiles = []
        for s in SETS:
            show(s); p = os.path.join(TMP, f"cmp_{s}_{v}.png"); render(f"Cam_{v}", p, (800, 450), 24); tiles.append(load(p))
        tiles.append(np.ones_like(tiles[0]) * np.array([0.12, 0.12, 0.13, 1.0], np.float32))
        top = np.concatenate(tiles[3:6], axis=1); bot = np.concatenate(tiles[0:3], axis=1)   # Blender rows go bottom-up
        save(np.concatenate([top, bot], axis=0), os.path.join(PRE, f"lod_comparison_{v}.png"))
        print("MONTAGE", v, flush=True)
show("LOD0")
