# Render previews of a checkpoint. Args after "--": <prefix> <mode: std|qc|sil> [cam ...]
#   qc  = high-gloss black body under long strip reflection cards
#   sil = black silhouette on white
import bpy, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
prefix = args[0] if args else "body"
mode = args[1] if len(args) > 1 else "std"
cams = args[2:] or ["front", "side", "rear", "front_3q", "rear_3q"]
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for d in prefs.devices: d.use = True
sc = bpy.context.scene; sc.cycles.device = "GPU"
bg = sc.world.node_tree.nodes["Background"]
if mode == "qc":
    for o in bpy.data.collections["HC_Studio"].objects:
        if o.type == 'LIGHT': o.hide_render = True
    for o in bpy.data.collections["HC_QC_Reflection"].objects: o.hide_render = False
    b = bpy.data.materials["PRE_Clay_Body"].node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.004, 0.004, 0.005, 1)
    b.inputs["Roughness"].default_value = 0.02; b.inputs["Coat Weight"].default_value = 1.0
    bg.inputs[1].default_value = 0.03
    sc.cycles.samples = 48
elif mode == "int":                     # cabin close-ups: stronger cabin fill, more samples
    if "Light_CabinFill" in bpy.data.objects:
        bpy.data.objects["Light_CabinFill"].data.energy = 40
    for o in bpy.data.collections["HC_Studio"].objects:     # no softbox mirror-images in the glass for cabin QA
        if o.type == 'LIGHT': o.visible_glossy = False
    sc.cycles.samples = 64
elif mode in ("day", "night"):
    for o in bpy.data.collections["HC_Studio"].objects:
        if o.type == 'LIGHT': o.hide_render = True
    flm = bpy.data.objects["Studio_Floor"].active_material.node_tree.nodes["Principled BSDF"]
    if mode == "day":
        for o in bpy.data.collections["HC_Daylight"].objects: o.hide_render = False
        bg.inputs[0].default_value = (0.42, 0.56, 0.85, 1); bg.inputs[1].default_value = 0.9
        flm.inputs["Base Color"].default_value = (0.32, 0.31, 0.30, 1); flm.inputs["Roughness"].default_value = 0.85
    else:
        for o in bpy.data.collections["HC_Night"].objects: o.hide_render = False
        bg.inputs[0].default_value = (0.02, 0.025, 0.04, 1); bg.inputs[1].default_value = 0.08
        flm.inputs["Base Color"].default_value = (0.05, 0.05, 0.055, 1); flm.inputs["Roughness"].default_value = 0.35
        pl = bpy.data.materials["MAT_ProjectorLens"].node_tree.nodes["Principled BSDF"]
        pl.inputs["Emission Strength"].default_value = 6.0                       # low beams on
        bpy.data.materials["MAT_LED_Brake"].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.5
    sc.cycles.samples = 64
elif mode == "uvcheck":
    bpy.context.view_layer.material_override = bpy.data.materials["QA_UV_Checker"]
    sc.cycles.samples = 24
elif mode == "sil":
    m = bpy.data.materials.new("SIL"); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (0, 0, 0, 1)
    nt.links.new(e.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs[0])
    bpy.context.view_layer.material_override = m
    bpy.data.objects["Studio_Floor"].hide_render = True
    bg.inputs[0].default_value = (1, 1, 1, 1); bg.inputs[1].default_value = 1
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    sc.cycles.samples = 4
os.makedirs(os.path.join(ROOT, "previews"), exist_ok=True)
for c in cams:
    sc.camera = bpy.data.objects.get(f"Cam_{c}") or bpy.data.objects[c]
    name = f"{prefix}_daylight" if mode == "day" else f"{prefix}_{c}"        # daylight never overwrites studio shots
    sc.render.filepath = os.path.join(ROOT, "previews", name + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", sc.render.filepath)
