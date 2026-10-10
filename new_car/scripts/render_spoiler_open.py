# QA only: render the active spoiler deployed (not saved; default stays closed).
import bpy, math, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for d in prefs.devices: d.use = True
sc = bpy.context.scene; sc.cycles.device = "GPU"
sp = bpy.data.objects["ActiveSpoiler"]; sp.rotation_euler.x = math.radians(sp["open_test_deg"])
sc.camera = bpy.data.objects["Cam_spoiler"]
sc.render.filepath = os.path.join(ROOT, "previews", "exterior_spoiler_open_test.png")
bpy.ops.render.render(write_still=True)
print("RENDERED", sc.render.filepath)
