# Phase 7: build Car_LOD0..3 from the master (hypercar_05a_pre_lod_cleanup.blend), component by component.
# Each LOD mesh = the master object evaluated with reduced settings (subdiv levels, bevel segments, cutter set,
# glass thickness) -> static mesh, then an optional per-component collapse decimate. Origins/pivots/UVs carry over.
# Saves hypercar_06_optimized_lods.blend; the master file is only read.
import bpy, bmesh, os, json, math
from mathutils import Matrix, Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "hypercar_06_optimized_lods.blend")
TEX = os.path.join(ROOT, "textures", "hypercar")
sc = bpy.context.scene
LODS = range(4)
CAT = {"BODY": "Body", "WHEELS": "Wheels", "TIRES": "Tires", "BRAKES": "Brakes", "INTERIOR": "Interior",
       "GLASS": "Glass", "LIGHTS": "Lights", "TRIM": "Aero_Trim"}
MASTER = [o for o in bpy.data.collections["HC_Hypercar"].all_objects
          if o.type == 'MESH' and not o.name.startswith("Cut_") and o.get("atlas") not in (None, "CUTTER")]

# ---------------------------------------------------------------- cutter subsets for distant body LODs
def cut_subset(name, exclude):
    c = bpy.data.collections.new(name); sc.collection.children.link(c)
    for o in bpy.data.collections["HC_Cutters"].objects:
        if not o.name.startswith(exclude):
            c.objects.link(o)
    c.hide_render = True; bpy.context.view_layer.layer_collection.children[name].hide_viewport = False
    return c
CUT2 = cut_subset("HC_Cutters_LOD2", ("Cut_Gap_", "Cut_DoorHandle_", "Cut_MirrorPad_"))
CUT3 = cut_subset("HC_Cutters_LOD3", ("Cut_Gap_", "Cut_DoorHandle_", "Cut_MirrorPad_", "Cut_EngineVent_"))

# ---------------------------------------------------------------- per-component plan
SMALL_INT = ("Pedal_", "Paddle_", "SteeringColumn", "RearViewMirror")
LOD3_INT_KEEP = {"Dashboard", "Seat_Driver", "Seat_Passenger", "SteeringWheel", "Interior_Tub", "CenterTunnel"}
SMALL_TRIM_LOD3 = ("EngineVents", "FrontIntakeVanes", "RearVent_", "RearFascia_Trim", "SideIntakeVane_",
                   "ActiveSpoilerHinge", "Exhaust_", "Chassis_EngineBay")
def plan(o, lod):
    """-> dict(sub=subsurf level or None, r=decimate ratio, drop, solid, bevel, holes)"""
    n, a = o.name, o["atlas"]
    p = dict(sub=None, r=1.0, drop=False, solid=True, bevel=None, holes=True)
    pick = lambda seq: seq[lod]
    if n == "Body_Shell":            p.update(sub=pick([1, 1, 0, 0]), r=pick([1, .55, 1, .45]))
    elif n == "Body_Buttress":       p.update(sub=pick([1, 0, 0, 0]), r=pick([1, 1, .6, .3]))
    elif n.startswith("Mirror_"):    p.update(sub=pick([1, 0, 0, 0]), r=pick([1, 1, .5, .2]))
    elif n.startswith("ArchLip_"):   p.update(r=pick([.4, .2, .1, 1]), drop=lod == 3)
    elif n.startswith("DoorHandle_"): p.update(drop=lod >= 2)
    elif n.startswith("Tire_"):      p.update(sub=0, r=pick([1, .55, .3, .1]))
    elif n.startswith("Rim_"):       p.update(r=pick([1, .55, .35, .12]))
    elif n.startswith("BrakeDisc_"): p.update(r=pick([.75, .5, .25, .08]), holes=lod == 0)
    elif n.startswith("Caliper_"):   p.update(bevel=pick([2, 1, 0, 0]), r=pick([1, .6, .35, .15]))
    elif a == "GLASS":
        if n.startswith("MirrorGlass"): p.update(drop=lod == 3)
        else: p.update(solid=lod < 2, r=pick([.5, .3, .25, .06]))
    elif a == "LIGHTS":
        if "Lens" in n: p.update(r=pick([1, .6, .4, 1]), drop=lod == 3)
        else: p.update(r=pick([1, .55, .3, .12]))
    elif a == "INTERIOR":
        if n.startswith("Seat_"):      p.update(sub=pick([1, 0, 0, 0]), r=pick([.5, 1, .45, .08]))
        elif n == "Dashboard":         p.update(sub=pick([1, 0, 0, 0]), r=pick([1, 1, .6, .5]))
        elif n == "SteeringWheel":     p.update(r=pick([1, .5, .25, .1]))
        elif n.startswith(SMALL_INT):  p.update(drop=lod >= 2)
        else: p.update(r=pick([{"Dashboard_Vents": .6, "EngineBay_Detail": .5, "PillarTrim": .6}.get(n, 1), .5, .2, .3]))
        if lod == 3 and n not in LOD3_INT_KEEP:
            p["drop"] = True
    elif a == "TRIM":
        p.update(r=pick([.9, .55, .3, .12]))
        if n.startswith("ActiveSpoilerHinge") and lod >= 2: p["drop"] = True
        if lod == 3 and n.startswith(SMALL_TRIM_LOD3): p["drop"] = True
    return p

# ---------------------------------------------------------------- evaluation helpers
def eval_mesh(o, p, lod):
    saved = []
    def setv(obj, attr, val):
        saved.append((obj, attr, getattr(obj, attr))); setattr(obj, attr, val)
    for md in o.modifiers:
        if md.type == 'SUBSURF' and p["sub"] is not None:
            setv(md, "levels", p["sub"])
        if md.type == 'BEVEL' and p["bevel"] is not None:
            if p["bevel"] == 0: setv(md, "show_viewport", False)
            else: setv(md, "segments", p["bevel"])
        if md.type == 'SOLIDIFY' and o["atlas"] == "GLASS" and not p["solid"]:
            setv(md, "show_viewport", False)
        if md.type == 'BOOLEAN' and lod >= 2:
            setv(md, "collection", CUT2 if lod == 2 else CUT3)
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    me = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    for obj, attr, val in reversed(saved):
        setattr(obj, attr, val)
    return me

def strip_holes(me):
    bm = bmesh.new(); bm.from_mesh(me)
    idx = [i for i, m in enumerate(me.materials) if m and m.name == "MAT_BlackTrim"]
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in idx], context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(me); bm.free()

def decimate(me, ratio, sym):
    if ratio >= 0.999 or len(me.polygons) < 40:
        return me
    tmp = bpy.data.objects.new("tmp_dec", me); sc.collection.objects.link(tmp)
    d = tmp.modifiers.new("Dec", 'DECIMATE'); d.decimate_type = 'COLLAPSE'; d.ratio = ratio
    d.use_symmetry = sym; d.symmetry_axis = 'X'
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    out = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    bpy.data.objects.remove(tmp)
    if me.users == 0: bpy.data.meshes.remove(me)
    return out

def clean(me):
    """Remove boolean slivers / decimation leftovers: degenerate faces+edges, edges with 3+ faces, loose verts."""
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-6, edges=bm.edges[:])
    for _ in range(8):                                   # edges with 3+ faces: drop the sliver face, repeat
        bad = [e for e in bm.edges if len(e.link_faces) > 2]
        if not bad: break
        bmesh.ops.delete(bm, geom=list({min(e.link_faces, key=lambda f: f.calc_area()) for e in bad}), context='FACES')
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.calc_area() < 1e-10], context='FACES')
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context='EDGES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(me); bm.free()

def tris(me):
    return sum(len(p.vertices) - 2 for p in me.polygons)

# ---------------------------------------------------------------- LOD materials (atlas texture sets + kept channels)
def img(atlas, ch):
    sub = {"BODY": "body", "INTERIOR": "interior", "WHEELS": "wheels", "TIRES": "tires", "LIGHTS": "lights",
           "BRAKES": "brakes", "GLASS": "glass", "TRIM": "trim"}[atlas]
    im = bpy.data.images.load(os.path.join(TEX, sub, f"{atlas}_{ch}.png"), check_existing=True)
    if ch != "BaseColor": im.colorspace_settings.name = 'Non-Color'
    return im

def atlas_mat(name, atlas, coat=0.0, glass=False):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    def tex(ch):
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = img(atlas, ch); return t
    nt.links.new(tex("BaseColor").outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex("Roughness").outputs["Color"], b.inputs["Roughness"])
    nt.links.new(tex("Metallic").outputs["Color"], b.inputs["Metallic"])
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.space = 'TANGENT'; nm.uv_map = "UVMap"
    nt.links.new(tex("Normal").outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs[0], b.inputs["Normal"])
    ao = tex("AO"); ao.label = "AO (engine occlusion slot; not wired in Cycles preview)"
    b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.1
    if glass:
        b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = 1.46
        out = nt.nodes["Material Output"]; tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        lp = nt.nodes.new("ShaderNodeLightPath"); mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs[0]); nt.links.new(b.outputs[0], mx.inputs[1])
        nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    m["lod_atlas"] = atlas
    return m

ATM = {"BODY": atlas_mat("LODMAT_Body_Paint", "BODY", coat=0.58), "INTERIOR": atlas_mat("LODMAT_Interior", "INTERIOR"),
       "WHEELS": atlas_mat("LODMAT_Wheels", "WHEELS"), "TIRES": atlas_mat("LODMAT_Tire", "TIRES"),
       "BRAKES": atlas_mat("LODMAT_Brakes", "BRAKES"), "LIGHTS": atlas_mat("LODMAT_Lights", "LIGHTS"),
       "TRIM": atlas_mat("LODMAT_Trim", "TRIM"), "GLASS": atlas_mat("LODMAT_Glass", "GLASS", glass=True)}
LIGHT_CHANNELS = {"MAT_LED_White", "MAT_ProjectorLens", "MAT_LED_Red", "MAT_LED_Brake", "MAT_LED_Amber", "MAT_LED_Reverse"}
def remap(mat, atlas, lod):
    n = mat.name if mat else ""
    if n in LIGHT_CHANNELS or n == "MAT_BrakeCaliper":
        return mat                                                   # gameplay-controlled / colour option
    if n in ("MAT_HeadlightLens", "MAT_TaillightLens", "MAT_InteriorMirror"):
        return mat
    if n in ("MAT_AmbientLight", "MAT_Display"):
        return mat if lod < 3 else ATM["INTERIOR"]
    if n in ("MAT_DisplayGraphics", "MAT_DisplayGraphics_Red"):
        return mat if lod < 2 else (bpy.data.materials["MAT_Display"] if lod == 2 else ATM["INTERIOR"])
    if n in ("MAT_CarbonExterior", "MAT_InteriorCarbon") and lod < 2:
        return mat                                                   # close-range weave kept at LOD0/1
    return ATM[atlas]

def merge_slots(me):
    """Collapse duplicate material slots after remapping (fewer draw calls)."""
    uniq = []
    for m in me.materials:
        if m not in uniq: uniq.append(m)
    if len(uniq) == len(me.materials): return
    remap_idx = [uniq.index(m) for m in me.materials]
    idx = [remap_idx[p.material_index] for p in me.polygons]
    me.materials.clear()
    for m in uniq: me.materials.append(m)
    for p, i in zip(me.polygons, idx): p.material_index = i

# ---------------------------------------------------------------- build
def lod_name(n, lod):
    return ("Body" if n == "Body_Shell" else "Wheel" + n[3:] if n.startswith("Rim_") else n) + f"_LOD{lod}"

car_root = bpy.data.objects["Car_Root"]
# Body LODs first, then park the master body's Exact boolean (27 s per re-eval; every temp decimate object would
# otherwise re-trigger it). Restored before saving, so REFERENCE_Master stays identical to the master file.
BODY_MESH = {}
_body = bpy.data.objects["Body_Shell"]
for lod in LODS:
    BODY_MESH[lod] = eval_mesh(_body, plan(_body, lod), lod)
    print("body LOD", lod, tris(BODY_MESH[lod]), flush=True)
_cut = _body.modifiers["Cutters"]; _cut_vis = _cut.show_viewport; _cut.show_viewport = False
report = {"master": {}, "lods": {}}
bpy.context.view_layer.update()
for lod in LODS:
    col = bpy.data.collections.new(f"Car_LOD{lod}"); sc.collection.children.link(col)
    sub = {}
    for cat in CAT.values():
        c = bpy.data.collections.new(f"LOD{lod}_{cat}"); col.children.link(c); sub[cat] = c
    root = bpy.data.objects.new(f"Car_LOD{lod}", None); col.objects.link(root)
    root.parent = car_root; root.empty_display_size = 0.5
    bpy.context.view_layer.update()
    made = {}
    for o in MASTER:
        p = plan(o, lod)
        if p["drop"]:
            continue
        me = BODY_MESH[lod] if o.name == "Body_Shell" else eval_mesh(o, p, lod)
        if not p["holes"] and o.name.startswith("BrakeDisc_"):
            strip_holes(me)
        sym = abs(sum((Vector(c) for c in o.bound_box), Vector()).x / 8 + o.matrix_world.translation.x) < 0.05
        me = decimate(me, p["r"], sym)
        clean(me)
        for i, m in enumerate(me.materials):
            me.materials[i] = remap(m, o["atlas"], lod)
        merge_slots(me)
        nm = lod_name(o.name, lod); me.name = nm
        ob = bpy.data.objects.new(nm, me); sub[CAT[o["atlas"]]].objects.link(ob)
        ob.parent = root; ob.matrix_parent_inverse = root.matrix_world.inverted(); ob.matrix_basis = o.matrix_world.copy()
        ob["atlas"] = o["atlas"]; ob["lod"] = lod; ob["master"] = o.name
        made[o.name] = ob
    bpy.context.view_layer.update()
    # rolling assemblies: tire + rotor ride on the wheel (rim) pivot; calipers stay on the root (steer, don't roll)
    for k in ("FL", "FR", "RL", "RR"):
        w = made[f"Rim_{k}"]
        for part in (f"Tire_{k}", f"BrakeDisc_{k}"):
            if part in made:
                c = made[part]; mw = c.matrix_world.copy()
                c.parent = w; c.matrix_parent_inverse = w.matrix_world.inverted(); c.matrix_basis = mw
    # door hinge empties (LOD0/1) keep the opening-door hierarchy
    if lod <= 1:
        for s in ("L", "R"):
            src = bpy.data.objects[f"Door_{s}"]
            d = bpy.data.objects.new(f"Door_{s}_LOD{lod}", None); sub["Body"].objects.link(d)
            d.empty_display_type = 'SINGLE_ARROW'; d.parent = root; d.matrix_basis = src.matrix_world.copy()
            bpy.context.view_layer.update()
            for ch in (f"DoorPanel_{s}", f"Window_F{s}", f"DoorHandle_{s}"):
                if ch in made:
                    c = made[ch]; mw = c.matrix_world.copy()
                    c.parent = d; c.matrix_parent_inverse = d.matrix_world.inverted(); c.matrix_basis = mw
    # LOD3: one lightweight cockpit shell
    if lod == 3:
        parts = [made[n] for n in LOD3_INT_KEEP if n in made]
        bm = bmesh.new(); mats = []
        for ob in parts:
            t = bmesh.new(); t.from_mesh(ob.data); t.transform(ob.matrix_world)
            base = len(mats); mats += list(ob.data.materials)
            for f in t.faces: f.material_index += base
            tmpme = bpy.data.meshes.new("tmp"); t.to_mesh(tmpme); bm.from_mesh(tmpme); bpy.data.meshes.remove(tmpme); t.free()
        me = bpy.data.meshes.new("Interior_LOD3"); bm.to_mesh(me); bm.free()
        for m in mats: me.materials.append(m)
        merge_slots(me)
        ob = bpy.data.objects.new("Interior_LOD3", me); sub["Interior"].objects.link(ob)
        ob.parent = root; ob.matrix_parent_inverse = root.matrix_world.inverted()
        ob["atlas"] = "INTERIOR"; ob["lod"] = 3; ob["master"] = ",".join(sorted(LOD3_INT_KEEP))
        for p_ in parts:
            bpy.data.objects.remove(p_)
    col.hide_render = lod != 0
    print("LOD", lod, "built", sum(tris(o.data) for o in col.all_objects if o.type == 'MESH'), flush=True)

_cut.show_viewport = _cut_vis
# ---------------------------------------------------------------- master -> hidden, render-excluded reference
ref = bpy.data.collections.new("REFERENCE_Master"); sc.collection.children.link(ref)
for c in list(bpy.data.collections["HC_Hypercar"].children):
    if c.name != "HC_Rig":
        bpy.data.collections["HC_Hypercar"].children.unlink(c); ref.children.link(c)
ref.hide_render = True
bpy.context.view_layer.layer_collection.children["REFERENCE_Master"].exclude = True
for n in ("HC_Cutters_LOD2", "HC_Cutters_LOD3"):
    bpy.context.view_layer.layer_collection.children[n].exclude = True
sc["lod_build"] = "lod_build.py from hypercar_05a_pre_lod_cleanup.blend"
bpy.ops.wm.save_as_mainfile(filepath=OUT)
bpy.ops.file.make_paths_relative(); bpy.ops.wm.save_mainfile()
print("SAVED", OUT)
