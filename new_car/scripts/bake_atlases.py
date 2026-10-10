# Bake per-atlas PBR texture sets for export: BaseColor / Roughness / Metallic / Normal (tangent, OpenGL +Y) / AO.
# Run on hypercar_05_materials_uv.blend; writes textures/hypercar/<group>/<ATLAS>_<map>.png, does not save the .blend.
# Optional args after "--": atlas names to bake (default all).
import bpy, os, sys, time
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, "textures", "hypercar")
SUB = {"BODY": "body", "INTERIOR": "interior", "WHEELS": "wheels", "TIRES": "tires", "LIGHTS": "lights",
       "BRAKES": "brakes", "GLASS": "glass", "TRIM": "trim"}
sc = bpy.context.scene
RES = dict(sc["atlas_resolution"])
only = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "METAL"; prefs.get_devices()
for d in prefs.devices: d.use = True
sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU'
# Bake session only (file is never saved): freeze Body_Shell's modifier stack into a plain mesh. Its Exact boolean
# costs ~27 s and re-runs on every scene edit (node add, hide toggle) -> ~8 re-evals per bake otherwise.
_body = bpy.data.objects["Body_Shell"]
_frozen = bpy.data.meshes.new_from_object(_body.evaluated_get(bpy.context.evaluated_depsgraph_get()))
_body.modifiers.clear(); _body.data = _frozen
sc.render.bake.margin = 8; sc.render.bake.use_clear = True; sc.render.bake.target = 'IMAGE_TEXTURES'
sc.cycles.use_denoising = False

def principled(m):
    return next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)

def rewire(m, sockets):
    """Temporarily drive the output with Emission = Principled input(s): exact-value bake.
    sockets = ["Base Color"] or ["Roughness", "Metallic"] (packed into R, G)."""
    nt = m.node_tree; b = principled(m)
    out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
    old = out.inputs["Surface"].links[0].from_socket if out.inputs["Surface"].links else None
    em = nt.nodes.new("ShaderNodeEmission"); added = [em]
    if len(sockets) == 1:
        src = b.inputs[sockets[0]]
        if src.links:
            nt.links.new(src.links[0].from_socket, em.inputs["Color"])
        else:
            em.inputs["Color"].default_value = tuple(src.default_value)
    else:
        cmb = nt.nodes.new("ShaderNodeCombineColor"); added.append(cmb)
        for i, sk in enumerate(sockets):
            src = b.inputs[sk]
            if src.links:
                nt.links.new(src.links[0].from_socket, cmb.inputs[i])
            else:
                cmb.inputs[i].default_value = src.default_value
        nt.links.new(cmb.outputs[0], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    def undo():
        if old:
            nt.links.new(old, out.inputs["Surface"])
        for n in added:
            nt.nodes.remove(n)
    return undo

# BaseColor and packed Roughness(R)/Metallic(G) are exact emission bakes; Normal = tangent OpenGL; AO = real occlusion
CH = [("BaseColor", "EMIT", ["Base Color"], False), ("RM", "EMIT", ["Roughness", "Metallic"], True),
      ("Normal", "NORMAL", None, True), ("AO", "AO", None, True)]
meshes = [o for o in sc.objects if o.type == 'MESH' and o.get("atlas") and o["atlas"] != "CUTTER" and not o.hide_render]
everything = [o for o in sc.objects if o.type in ('MESH', 'CURVE') and not o.hide_render]

def save(img, grp, name):
    path = os.path.join(TEX, SUB[grp], f"{grp}_{name}.png")
    img.filepath_raw = path; img.file_format = 'PNG'; img.save()

report = []
for grp, res in RES.items():
    if only and grp not in only:
        continue
    objs = [o for o in meshes if o["atlas"] == grp]
    mats = {s.material for o in objs for s in o.material_slots if s.material and principled(s.material)}
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.hide_set(False); o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    for ch, kind, socks, noncolor in CH:
        t0 = time.time()
        img = bpy.data.images.new(f"{grp}_{ch}", res, res, alpha=False, float_buffer=(ch == "RM"))
        if noncolor:
            img.colorspace_settings.name = 'Non-Color'
        nodes = []
        for m in mats:
            n = m.node_tree.nodes.new("ShaderNodeTexImage"); n.image = img
            m.node_tree.nodes.active = n; nodes.append((m, n))
        undo = [rewire(m, socks) for m in mats] if kind == "EMIT" else []
        for o in everything:                       # per-bake scene sync dominates: keep only what the pass needs
            o.hide_render = (kind != "AO") and o not in objs
        sc.cycles.samples = 16 if kind == "AO" else 1
        if kind == "NORMAL":
            sc.render.bake.normal_space = 'TANGENT'
            sc.render.bake.normal_r, sc.render.bake.normal_g, sc.render.bake.normal_b = 'POS_X', 'POS_Y', 'POS_Z'
        bpy.ops.object.bake(type=kind)
        for o in everything:
            o.hide_render = False
        for u in undo:
            u()
        for m, n in nodes:
            m.node_tree.nodes.remove(n)
        if ch == "RM":                              # split packed bake -> Roughness / Metallic
            px = np.empty(res * res * 4, np.float32); img.pixels.foreach_get(px); px = px.reshape(-1, 4)
            for name, c in (("Roughness", 0), ("Metallic", 1)):
                o_img = bpy.data.images.new(f"{grp}_{name}", res, res, alpha=False)
                o_img.colorspace_settings.name = 'Non-Color'
                g = np.repeat(px[:, c:c + 1], 3, 1)
                o_img.pixels.foreach_set(np.hstack([g, np.ones((len(g), 1), np.float32)]).ravel())
                save(o_img, grp, name)
        else:
            save(img, grp, ch)
        report.append(f"{grp}_{ch} {res}px {time.time() - t0:.0f}s")
        print("BAKED", report[-1], flush=True)
os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
open(os.path.join(ROOT, "reports", "phase_06_bake_log.txt"), "a").write("\n".join(report) + "\n")
