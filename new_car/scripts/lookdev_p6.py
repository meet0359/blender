# Phase 6: tile textures, production materials, UV atlases, studio/day/night rigs.
# Exec'd at the end of build_materials.py (shares its globals: sc, coll, materials, objects ...).
import numpy as np

TEX = os.path.join(ROOT, "textures", "hypercar")
SUBS = ("body", "interior", "wheels", "tires", "lights", "brakes", "glass", "trim")
for d in SUBS:
    os.makedirs(os.path.join(TEX, d), exist_ok=True)

# ================================================================ 1. generated tile textures (numpy)
def save_img(name, arr, sub, noncolor=False):
    """arr: HxW or HxWx3 floats 0-1, row 0 = bottom (Blender order). Saved as PNG under textures/hypercar/sub."""
    h, w = arr.shape[:2]
    if arr.ndim == 2:
        arr = np.dstack([arr] * 3)
    rgba = np.dstack([np.clip(arr[..., :3], 0, 1), np.ones((h, w))]).astype(np.float32)
    path = os.path.join(TEX, sub, name + ".png")
    img = bpy.data.images.new(name, w, h, alpha=False)
    img.pixels.foreach_set(rgba.ravel())
    img.filepath_raw = path; img.file_format = 'PNG'; img.save()
    img.source = 'FILE'; img.filepath = path; img.reload()
    if noncolor:
        img.colorspace_settings.name = 'Non-Color'
    return img

def height_to_normal(hm, strength):
    """Tileable tangent-space normal, OpenGL convention (+Y = up in UV / green up)."""
    gx = (np.roll(hm, -1, 1) - np.roll(hm, 1, 1)) * 0.5 * strength
    gy = (np.roll(hm, -1, 0) - np.roll(hm, 1, 0)) * 0.5 * strength
    n = np.dstack([-gx, -gy, np.ones_like(hm)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return n * 0.5 + 0.5

def blur(a, r=1):
    for _ in range(r):
        a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5
    return a

rng = np.random.default_rng(7)
# --- carbon 2x2 twill: tile = 4 tows x 4 tows
N = 512; cell = N // 4
yy, xx = np.mgrid[0:N, 0:N]
ci, cj = yy // cell, xx // cell
fy, fx = (yy % cell) / cell, (xx % cell) / cell
horiz = ((ci - cj) % 4) < 2
prof = np.where(horiz, np.sin(np.pi * fy), np.sin(np.pi * fx)) ** 0.6
fib = blur(rng.random((N, N)), 1)
streak = np.where(horiz, np.roll(fib, 0, 1).mean(1, keepdims=True).repeat(N, 1), fib.mean(0, keepdims=True).repeat(N, 0))
cw_h = prof * 0.85 + 0.15 * streak
cw_col = np.where(horiz, 0.15, 0.085) * (0.75 + 0.35 * prof) + 0.02 * streak
IMG_CARBON_C = save_img("carbon_twill_BaseColor", cw_col, "trim")
IMG_CARBON_N = save_img("carbon_twill_Normal", height_to_normal(blur(cw_h, 2), 6.0), "trim", True)
# --- speaker perforation: staggered holes
N = 256; per = 32
yy, xx = np.mgrid[0:N, 0:N]
sx = (xx + (yy // per % 2) * per // 2) % per - per / 2; sy = yy % per - per / 2
holes = (np.hypot(sx, sy) < per * 0.28).astype(float)
IMG_SPK_C = save_img("speaker_perforation_Mask", 1 - holes, "interior")
IMG_SPK_N = save_img("speaker_perforation_Normal", height_to_normal(blur(1 - holes, 1), 4.0), "interior", True)
# --- saddle stitch: dashes along U
W, H = 256, 64
yy, xx = np.mgrid[0:H, 0:W]
dash = ((xx % 64) < 40) & (np.abs(yy - H / 2) < 7)
st_h = blur(dash.astype(float), 2)
IMG_STITCH_N = save_img("stitch_Normal", height_to_normal(st_h, 5.0), "interior", True)
IMG_STITCH_M = save_img("stitch_Mask", st_h, "interior", True)

# --- tire sidewall lettering: rasterised from Blender text meshes into the outboard-sidewall UV band
def raster_text(items, W, H, wm, hm):
    """items: (text, size_m, cx_m, cy_m) in a wm x hm metre strip -> HxW mask."""
    mask = np.zeros((H, W), np.float32)
    dg = bpy.context.evaluated_depsgraph_get()
    for txt, size, cx, cy in items:
        cu = bpy.data.curves.new("rt", 'FONT'); cu.body = txt; cu.size = size
        cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.space_character = 1.15
        ob = bpy.data.objects.new("rt", cu); sc.collection.objects.link(ob); bpy.context.view_layer.update()
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(bpy.context.evaluated_depsgraph_get()))
        me.calc_loop_triangles()
        co = np.array([(v.co.x + cx, v.co.y + cy) for v in me.vertices]) * [W / wm, H / hm]
        for tri in me.loop_triangles:
            p = co[list(tri.vertices)]
            x0, y0 = np.floor(p.min(0)).astype(int); x1, y1 = np.ceil(p.max(0)).astype(int)
            x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W - 1), min(y1, H - 1)
            if x1 < x0 or y1 < y0:
                continue
            gy, gx = np.mgrid[y0:y1 + 1, x0:x1 + 1] + 0.5
            (ax, ay), (bx, by), (cx_, cy_) = p
            d = (by - cy_) * (ax - cx_) + (cx_ - bx) * (ay - cy_)
            if abs(d) < 1e-12:
                continue
            l1 = ((by - cy_) * (gx - cx_) + (cx_ - bx) * (gy - cy_)) / d
            l2 = ((cy_ - ay) * (gx - cx_) + (ax - cx_) * (gy - cy_)) / d
            inside = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
            mask[y0:y1 + 1, x0:x1 + 1] = np.maximum(mask[y0:y1 + 1, x0:x1 + 1], inside)
        bpy.data.objects.remove(ob); bpy.data.curves.remove(cu); bpy.data.meshes.remove(me)
    return mask

def tire_profile_v(R, hw, rr):
    """Same profile as exterior_parts (tire lathe) -> cumulative normalised arc length per profile point."""
    tread = []
    for g in (-0.5 * hw, -0.1 * hw, 0.3 * hw):
        tread += [(g - 0.007, R), (g - 0.004, R - 0.007), (g + 0.004, R - 0.007), (g + 0.007, R)]
    prof = ([(-hw * .86, rr + .004), (-hw, rr + .03), (-hw, R - .05), (-hw + .004, R - .02), (-hw + .02, R - .006),
             (-hw + .05, R)] + tread +
            [(hw - .05, R), (hw - .02, R - .006), (hw - .004, R - .02), (hw, R - .05), (hw, rr + .03), (hw * .86, rr + .004)])
    acc = [0.0]
    for a, b in zip(prof, prof[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    return prof, [a / acc[-1] for a in acc], acc[-1]

TEXN = 2048
bands = []
for spec in (FRONT, REAR):
    prof, vv, total = tire_profile_v(spec["R"], spec["W"] / 2, spec["RIM"])
    bands.append((vv[-4], vv[-3], total, spec))          # outboard sidewall: (hw, R-.05) -> (hw, rr+.03)
va = max(b[0] for b in bands); vb = min(b[1] for b in bands)
total = sum(b[2] for b in bands) / 2
r_mid = sum(b[3]["RIM"] + (b[3]["R"] - b[3]["RIM"]) / 2 for b in bands) / 2
u_len = math.pi * r_mid                                  # UV u spans half the circumference (text repeats twice)
band_h = (vb - va) * total
H = int(round((vb - va) * TEXN))
items = [("AERO HYPER", band_h * 0.42, u_len * 0.25, band_h * 0.52),
         ("ZR PERFORMANCE", band_h * 0.22, u_len * 0.70, band_h * 0.60),
         ("TUBELESS RADIAL  -  EXTRA LOAD", band_h * 0.12, u_len * 0.70, band_h * 0.28),
         ("305/30 ZR21  -  345/30 ZR22", band_h * 0.11, u_len * 0.25, band_h * 0.16)]
strip = raster_text(items, TEXN, H, u_len, band_h)
strip = strip[::-1, ::-1]                                 # 180 deg: letter tops face the tread, reads clockwise
tire_mask = np.zeros((TEXN, TEXN), np.float32)
r0 = int(round(va * TEXN)); tire_mask[r0:r0 + H, :] = strip
tire_h = blur(tire_mask, 2)
IMG_TIRE_M = save_img("tire_sidewall_Mask", tire_h, "tires", True)
IMG_TIRE_N = save_img("tire_sidewall_Normal", height_to_normal(tire_h, 4.0), "tires", True)
sc["tire_letter_band_v"] = (round(va, 4), round(vb, 4))

# ================================================================ 2. production materials
def new_mat(name, base, metal=0.0, rough=0.5, coat=0.0, coat_rough=0.1, fake=False):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(b.outputs[0], out.inputs[0])
    b.inputs["Base Color"].default_value = (*base, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough; b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = coat_rough
    m.diffuse_color = (*base, 1); m.use_fake_user = fake
    return m, nt, b

def node(nt, kind, **kw):
    n = nt.nodes.new(kind)
    for k, v in kw.items():
        setattr(n, k, v)
    return n

def tex_box(nt, img, scale, noncolor=False):
    """Image tiled in world units via box projection on object coordinates (no UV dependence)."""
    tc = node(nt, "ShaderNodeTexCoord"); mp = node(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (scale, scale, scale)
    ti = node(nt, "ShaderNodeTexImage", image=img, projection='BOX', projection_blend=0.25)
    nt.links.new(tc.outputs["Object"], mp.inputs[0]); nt.links.new(mp.outputs[0], ti.inputs[0])
    return ti

def tex_uv(nt, img):
    tc = node(nt, "ShaderNodeTexCoord"); ti = node(nt, "ShaderNodeTexImage", image=img)
    nt.links.new(tc.outputs["UV"], ti.inputs[0])
    return ti

def normal_map(nt, b, img_node, strength):
    nm = node(nt, "ShaderNodeNormalMap", space='TANGENT', uv_map="UVMap")
    nm.inputs["Strength"].default_value = strength
    nt.links.new(img_node.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs[0], b.inputs["Normal"])
    return nm

def bump_noise(nt, b, scale, strength, distance, detail=4.0, voronoi=False, stretch=(1, 1, 1)):
    tc = node(nt, "ShaderNodeTexCoord"); mp = node(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = stretch
    t = node(nt, "ShaderNodeTexVoronoi" if voronoi else "ShaderNodeTexNoise")
    t.inputs["Scale"].default_value = scale
    if not voronoi:
        t.inputs["Detail"].default_value = detail
    bp = node(nt, "ShaderNodeBump"); bp.inputs["Strength"].default_value = strength
    bp.inputs["Distance"].default_value = distance
    nt.links.new(tc.outputs["Object"], mp.inputs[0]); nt.links.new(mp.outputs[0], t.inputs["Vector"])
    nt.links.new(t.outputs["Distance" if voronoi else "Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs[0], b.inputs["Normal"])
    return bp

def emissive(name, color, strength, base=(0.02, 0.02, 0.02)):
    m, nt, b = new_mat(name, base, rough=0.3)
    b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = strength
    return m

def glass(name, tint, rough=0.02, ior=1.46):
    m, nt, b = new_mat(name, tint, rough=rough)
    b.inputs["Transmission Weight"].default_value = 1.0; b.inputs["IOR"].default_value = ior
    out = nt.nodes["Material Output"]
    tr = node(nt, "ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = (*tint, 1)
    lp = node(nt, "ShaderNodeLightPath"); mx = node(nt, "ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs[0])          # cabin keeps its light through glass
    nt.links.new(b.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs[0])
    m.diffuse_color = (*tint, 0.25)
    return m

PAINT_RED = (0.80, 0.010, 0.024)          # brief: (0.82, 0.018, 0.015); nudged to crimson so AgX highlights stay red, not orange
def paint(name, base, metal, rough, coat, coat_rough, fake=False):
    m, nt, b = new_mat(name, base, metal, rough, coat, coat_rough, fake)
    b.inputs["Coat IOR"].default_value = 1.5
    tc = node(nt, "ShaderNodeTexCoord"); fl = node(nt, "ShaderNodeTexNoise")       # metallic flake micro-normal
    fl.inputs["Scale"].default_value = 2500.0; fl.inputs["Detail"].default_value = 1.0
    bp = node(nt, "ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.025; bp.inputs["Distance"].default_value = 0.0002
    nt.links.new(tc.outputs["Object"], fl.inputs["Vector"]); nt.links.new(fl.outputs["Fac"], bp.inputs["Height"])
    nt.links.new(bp.outputs[0], b.inputs["Normal"])
    return m

MAT = {}
MAT["paint"] = paint("MAT_CarPaint_RacingRed", PAINT_RED, 0.85, 0.20, 0.58, 0.10)
paint("MAT_CarPaint_ElectricBlue", (0.010, 0.090, 0.75), 0.85, 0.20, 0.60, 0.08, fake=True)
paint("MAT_CarPaint_PearlWhite", (0.86, 0.86, 0.83), 0.30, 0.25, 0.70, 0.06, fake=True)
paint("MAT_CarPaint_SatinBlack", (0.020, 0.020, 0.022), 0.45, 0.45, 0.25, 0.40, fake=True)

def carbon(name, tile_m, coat):
    m, nt, b = new_mat(name, (0.03, 0.03, 0.03), 0.0, 0.32, coat, 0.04)
    scale = 1.0 / tile_m
    c = tex_box(nt, IMG_CARBON_C, scale); nt.links.new(c.outputs["Color"], b.inputs["Base Color"])
    n = tex_box(nt, IMG_CARBON_N, scale); normal_map(nt, b, n, 0.35)
    return m
MAT["carbon_ext"] = carbon("MAT_CarbonExterior", 0.016, 1.0)       # 4 tows x 4 mm
MAT["carbon_int"] = carbon("MAT_CarbonInterior", 0.008, 0.8)       # 4 tows x 2 mm
MAT["blacktrim"] = new_mat("MAT_BlackTrim", (0.012, 0.012, 0.013), 0.0, 0.45)[0]
MAT["wheel_mach"] = new_mat("MAT_Wheel_Machined", (0.78, 0.78, 0.80), 1.0, 0.16)[0]
MAT["wheel_graph"] = new_mat("MAT_Wheel_Graphite", (0.085, 0.087, 0.095), 1.0, 0.30)[0]
MAT["wheel_barrel"] = new_mat("MAT_Wheel_DarkBarrel", (0.045, 0.045, 0.05), 0.8, 0.50)[0]

m, nt, b = new_mat("MAT_Tire", (0.032, 0.032, 0.034), 0.0, 0.80)
mk = tex_uv(nt, IMG_TIRE_M)
rr_ = node(nt, "ShaderNodeMapRange"); rr_.inputs[3].default_value = 0.80; rr_.inputs[4].default_value = 0.72
nt.links.new(mk.outputs["Color"], rr_.inputs[0]); nt.links.new(rr_.outputs[0], b.inputs["Roughness"])
nmn = tex_uv(nt, IMG_TIRE_N); nm = normal_map(nt, b, nmn, 1.0)
bp = node(nt, "ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.08; bp.inputs["Distance"].default_value = 0.0005
nz = node(nt, "ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 900.0
nt.links.new(nz.outputs["Fac"], bp.inputs["Height"]); nt.links.new(nm.outputs[0], bp.inputs["Normal"])
nt.links.new(bp.outputs[0], b.inputs["Normal"])
MAT["tire"] = m

m, nt, b = new_mat("MAT_BrakeRotor", (0.075, 0.072, 0.07), 0.35, 0.45)
mot = node(nt, "ShaderNodeTexNoise"); mot.inputs["Scale"].default_value = 180.0
ramp = node(nt, "ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1); ramp.color_ramp.elements[1].color = (0.11, 0.105, 0.10, 1)
nt.links.new(mot.outputs["Fac"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
MAT["rotor"] = m
MAT["caliper"] = new_mat("MAT_BrakeCaliper", (0.80, 0.50, 0.015), 0.0, 0.32, 0.6, 0.08)[0]
MAT["exhaust"] = new_mat("MAT_ExhaustMetal", (0.56, 0.52, 0.48), 1.0, 0.24)[0]

MAT["windshield"] = glass("MAT_Windshield", (0.92, 0.94, 0.94))
MAT["sideglass"] = glass("MAT_SideGlass", (0.84, 0.86, 0.87))
MAT["rearglass"] = glass("MAT_RearGlass", (0.70, 0.72, 0.74))
MAT["engineglass"] = glass("MAT_EngineGlass", (0.62, 0.62, 0.64))

MAT["hl_lens"] = glass("MAT_HeadlightLens", (0.97, 0.97, 0.97), rough=0.0, ior=1.49)
MAT["hl_housing"] = new_mat("MAT_HeadlightHousing", (0.018, 0.018, 0.02), 0.2, 0.30)[0]
MAT["led_white"] = emissive("MAT_LED_White", (1.0, 0.96, 0.90), 6.0, base=(0.9, 0.9, 0.9))
m, nt, b = new_mat("MAT_ProjectorLens", (0.02, 0.022, 0.03), 0.0, 0.02, 1.0, 0.02)
b.inputs["Emission Color"].default_value = (1.0, 0.97, 0.92, 1); b.inputs["Emission Strength"].default_value = 0.0
MAT["proj_lens"] = m                                                # night mode switches this on
MAT["proj_metal"] = new_mat("MAT_ProjectorMetal", (0.82, 0.82, 0.84), 1.0, 0.08)[0]
MAT["tl_lens"] = glass("MAT_TaillightLens", (0.42, 0.10, 0.10), rough=0.03, ior=1.49)
MAT["led_red"] = emissive("MAT_LED_Red", (1.0, 0.02, 0.01), 5.0, base=(0.5, 0.02, 0.02))
MAT["led_brake"] = emissive("MAT_LED_Brake", (0.9, 0.01, 0.01), 1.2, base=(0.35, 0.01, 0.01))
MAT["led_amber"] = emissive("MAT_LED_Amber", (1.0, 0.35, 0.0), 0.8, base=(0.6, 0.25, 0.0))
MAT["led_rev"] = emissive("MAT_LED_Reverse", (1.0, 1.0, 1.0), 0.25, base=(0.6, 0.6, 0.6))

# interior (refine the Phase-5 slots in place so every object keeps its assignment)
m, nt, b = new_mat("MAT_InteriorLeather", (0.020, 0.019, 0.019), 0.0, 0.42, 0.08, 0.3)
bump_noise(nt, b, 1400.0, 0.12, 0.0004, voronoi=True)                                 # restrained grain
m, nt, b = new_mat("MAT_InteriorAlcantara", (0.040, 0.040, 0.043), 0.0, 0.95)
b.inputs["Sheen Weight"].default_value = 0.35
bump_noise(nt, b, 3500.0, 0.06, 0.0003, detail=2.0, stretch=(1, 1, 3.5))             # directional nap
MAT["carbon_int_slot"] = carbon("MAT_InteriorCarbon", 0.008, 0.8)
m, nt, b = new_mat("MAT_InteriorPlastic", (0.028, 0.028, 0.030), 0.0, 0.55)
bump_noise(nt, b, 2200.0, 0.05, 0.0002)
m, nt, b = new_mat("MAT_InteriorMetal", (0.24, 0.24, 0.26), 1.0, 0.30)
bump_noise(nt, b, 900.0, 0.03, 0.0002, stretch=(1, 30, 1))                           # brushed titanium
m, nt, b = new_mat("MAT_Display", (0.006, 0.008, 0.012), 0.0, 0.25, 0.25, 0.05)      # anti-glare cover glass
b.inputs["Emission Color"].default_value = (0.008, 0.013, 0.025, 1); b.inputs["Emission Strength"].default_value = 0.6
emissive("MAT_DisplayGraphics", (0.75, 0.85, 1.0), 1.4)
emissive("MAT_DisplayGraphics_Red", (1.0, 0.06, 0.03), 1.6)
m, nt, b = new_mat("MAT_SeatAccent", PAINT_RED, 0.0, 0.40, 0.25, 0.3)
sn = tex_box(nt, IMG_STITCH_N, 1.0 / 0.008); normal_map(nt, b, sn, 0.6)                # baked saddle stitch
m, nt, b = new_mat("MAT_Speaker", (0.05, 0.05, 0.055), 0.6, 0.45)
pm = tex_box(nt, IMG_SPK_C, 1.0 / 0.006)
mix = node(nt, "ShaderNodeMix", data_type='RGBA'); mix.inputs[6].default_value = (0.0, 0.0, 0.0, 1)
mix.inputs[7].default_value = (0.06, 0.06, 0.065, 1)
nt.links.new(pm.outputs["Color"], mix.inputs[0]); nt.links.new(mix.outputs[2], b.inputs["Base Color"])
normal_map(nt, b, tex_box(nt, IMG_SPK_N, 1.0 / 0.006), 0.8)
new_mat("MAT_InteriorMirror", (0.92, 0.92, 0.92), 1.0, 0.02)
emissive("MAT_AmbientLight", (1.0, 0.03, 0.02), 1.2, base=(0.3, 0.01, 0.01))

REMAP = {
    "PRE_Clay_Body": MAT["paint"], "PRE_Glass_Dark": MAT["sideglass"], "PRE_Dark_Intake": MAT["blacktrim"],
    "PRE_Carbon_Dark": MAT["carbon_ext"], "PRE_Tire": MAT["tire"], "PRE_Rim_Metal": MAT["wheel_mach"],
    "PRE_Rim_Barrel": MAT["wheel_barrel"], "PRE_Rim_Machined_Lip": MAT["wheel_mach"],
    "PRE_Rim_Forged_Graphite": MAT["wheel_graph"], "PRE_Rotor": MAT["rotor"], "PRE_Caliper": MAT["caliper"],
    "PRE_Brake_Hat": MAT["wheel_graph"], "PRE_Exhaust_Metal": MAT["exhaust"], "PRE_Exhaust_Inner_Dark": MAT["wheel_barrel"],
    "PRE_Light_Housing": MAT["hl_housing"], "PRE_LED_DRL_White": MAT["led_white"], "PRE_LED_Tail_Red": MAT["led_red"],
    "PRE_LED_Brake_Red": MAT["led_brake"], "PRE_LED_Indicator_Amber": MAT["led_amber"],
    "PRE_LED_Reverse_White": MAT["led_rev"], "PRE_Lens_Clear": MAT["hl_lens"], "PRE_Lens_Smoked": MAT["tl_lens"],
    "PRE_Bezel_Metal": MAT["proj_metal"], "PRE_Projector_Lens": MAT["proj_lens"],
    "PRE_Mirror_Glass": bpy.data.materials["MAT_InteriorMirror"],
}
GLASSMAP = {"Windshield": MAT["windshield"], "Rear_Glass": MAT["rearglass"], "EngineGlass": MAT["engineglass"]}
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    for slot in o.material_slots:
        if slot.material is None:
            continue
        if slot.material.name == "MAT_Glass_Review":
            slot.material = GLASSMAP.get(o.name, MAT["sideglass"])
        elif slot.material.name in REMAP:
            slot.material = REMAP[slot.material.name]
for mname in [mm.name for mm in bpy.data.materials if mm.users == 0 and not mm.use_fake_user]:
    bpy.data.materials.remove(bpy.data.materials[mname])

# ================================================================ 3. UV atlases
CAR = [o for o in bpy.data.collections["HC_Hypercar"].all_objects if o.type == 'MESH']
INT_NAMES = {o.name for o in bpy.data.collections["HC_Interior"].all_objects}
GLASS_NAMES = {o.name for o in bpy.data.collections["HC_Glass"].all_objects}
def atlas_of(o):
    n = o.name
    if n.startswith("Cut_"): return None
    if n in INT_NAMES: return "INTERIOR"
    if n in GLASS_NAMES or n.startswith("MirrorGlass"): return "GLASS"
    if n.startswith(("Body_", "ArchLip_", "DoorHandle_", "Mirror_")): return "BODY"
    if n.startswith("Rim_"): return "WHEELS"
    if n.startswith("Tire_"): return "TIRES"
    if n.startswith(("BrakeDisc_", "Caliper_")): return "BRAKES"
    if n.startswith(("Headlight", "Taillight")): return "LIGHTS"
    return "TRIM"
ATLAS_RES = {"BODY": 4096, "INTERIOR": 4096, "WHEELS": 2048, "TIRES": 2048, "LIGHTS": 2048,
             "BRAKES": 1024, "GLASS": 1024, "TRIM": 1024}
WEIGHT = {"SteeringWheel": 2.0, "Seat_Driver": 1.5, "Seat_Passenger": 1.5, "Dashboard": 1.5, "CenterConsole": 1.5,
          "InstrumentCluster": 1.5, "CenterScreen": 1.5, "Paddle_L": 1.5, "Paddle_R": 1.5, "DoorPanel_L": 1.3,
          "DoorPanel_R": 1.3, "Interior_Tub": 0.4, "EngineBay_Detail": 0.4, "RearBulkhead": 0.7, "Headliner": 0.7,
          "CenterTunnel": 0.8, "SteeringColumn": 0.8, "Dashboard_Vents": 1.2, "ArchLip_FL": 0.5, "ArchLip_FR": 0.5,
          "ArchLip_RL": 0.5, "ArchLip_RR": 0.5, "DoorHandle_L": 0.6, "DoorHandle_R": 0.6,
          "Chassis_Floor": 0.25, "Chassis_EngineBay": 0.3, "ActiveSpoilerHinge": 0.5}         # hidden trim -> lower
for o in CAR:
    o["atlas"] = atlas_of(o) or "CUTTER"

def edit(objs, fn):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.hide_set(False); o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    fn()
    bpy.ops.object.mode_set(mode='OBJECT')

def uv_area_ratio(o):
    me = o.data; uv = me.uv_layers["UVMap"].data
    wa = ua = 0.0
    for p in me.polygons:
        wa += p.area
        pts = [uv[li].uv for li in p.loop_indices]
        ua += abs(sum(pts[i].x * pts[i - 1].y - pts[i - 1].x * pts[i].y for i in range(len(pts)))) / 2
    return wa, ua

def scale_uv(o, f):
    uv = o.data.uv_layers["UVMap"].data
    co = np.zeros(len(uv) * 2); uv.foreach_get("uv", co); uv.foreach_set("uv", co * f)

# tires: cylindrical sidewall mapping (lettering band), u = half circumference, rotated 180 deg on the left
for o in CAR:
    if not o.name.startswith("Tire_"):
        continue
    me = o.data; uvl = me.uv_layers.new(name="UVMap") if "UVMap" not in me.uv_layers else me.uv_layers["UVMap"]
    spec = FRONT if o.name[5] == "F" else REAR
    prof, vv, _ = tire_profile_v(spec["R"], spec["W"] / 2, spec["RIM"]); n = len(prof)
    left = o.matrix_world.translation.x < 0
    for p in me.polygons:
        us = []
        for li in p.loop_indices:
            vi = me.loops[li].vertex_index; c = me.vertices[vi].co
            th = math.atan2(c.z, c.y) % (2 * math.pi)
            us.append([(th % math.pi) / math.pi, vv[vi % n], vi % n])
        if {q[2] for q in us} == {0, n - 1}:                       # hidden bead face closing the profile loop
            for q in us: q[1] = 1.0                                 # collapse instead of a reversed full-height span
        us = [q[:2] for q in us]
        if max(u for u, _ in us) - min(u for u, _ in us) > 0.5:        # seam at 0 / pi
            for q in us:
                if q[0] < 0.5: q[0] += 1.0
        for li, (u, v) in zip(p.loop_indices, us):
            uvl.data[li].uv = (min(u, 1.0), v) if not left else (1.0 - min(u, 1.0), 1.0 - v)

# smart-project everything else (body loft already has its metric UV), normalise to metres, weight, pack
for grp in ("BODY", "INTERIOR", "WHEELS", "BRAKES", "LIGHTS", "GLASS", "TRIM"):
    objs = [o for o in CAR if o["atlas"] == grp]
    proj = [o for o in objs if o.name != "Body_Shell"]
    if proj:
        edit(proj, lambda: bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.0,
                                                   scale_to_bounds=False))
    for o in objs:
        wa, ua = uv_area_ratio(o)
        if ua > 0:
            scale_uv(o, math.sqrt(wa / ua) * WEIGHT.get(o.name, 1.0))
    edit(objs, lambda: bpy.ops.uv.pack_islands(rotate=True, margin=0.004))
    if grp == "BODY":                                  # reserve the top-right corner for boolean cut walls
        for o in objs:
            scale_uv(o, 0.965)
# cutters: their wall faces land in the reserved corner texel block of the BODY atlas
for o in bpy.data.collections["HC_Cutters"].objects:
    me = o.data; uvl = me.uv_layers.get("UVMap") or me.uv_layers.new(name="UVMap")
    co = np.full(len(uvl.data) * 2, 0.985); uvl.data.foreach_set("uv", co)

# texel density (median px/m per atlas, base cage faces)
dens = {}
for grp, res in ATLAS_RES.items():
    vals = []
    for o in CAR:
        if o["atlas"] != grp:
            continue
        me = o.data; uv = me.uv_layers["UVMap"].data
        for p in me.polygons:
            if p.area < 1e-8: continue
            pts = [uv[li].uv for li in p.loop_indices]
            ua = abs(sum(pts[i].x * pts[i - 1].y - pts[i - 1].x * pts[i].y for i in range(len(pts)))) / 2
            vals.append(math.sqrt(ua / p.area) * res)
    dens[grp] = round(float(np.median(vals)), 1) if vals else 0
sc["texel_density_px_per_m"] = dens
sc["atlas_resolution"] = ATLAS_RES
print("TEXEL DENSITY", dens)

# QA checker material (UV review renders only)
chk = bpy.data.images.new("QA_UV_Checker", 2048, 2048); chk.generated_type = 'COLOR_GRID'
m, nt, b = new_mat("QA_UV_Checker", (1, 1, 1), 0.0, 0.5, fake=True)
nt.links.new(tex_uv(nt, chk).outputs["Color"], b.inputs["Base Color"])

# ================================================================ 4. studio / daylight / night rigs, colour management
for o in [o for o in C_STUDIO.objects if o.type == 'LIGHT']:
    bpy.data.objects.remove(o)
def light(name, kind, loc, rot, energy, size=1.0, size_y=None, col=C_STUDIO, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, kind); l.energy = energy; l.color = color
    if kind == 'AREA':
        l.shape = 'RECTANGLE'; l.size = size; l.size_y = size_y or size
    o = bpy.data.objects.new(name, l); col.objects.link(o); o.location = loc; o.rotation_euler = rot
    o.visible_camera = False; o.visible_transmission = False
    return o
def aim(o, tgt=(0, 0, 0.5)):
    d = Vector(tgt) - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
k = light("Light_Key", 'AREA', (-4.2, -5.0, 4.4), (0, 0, 0), 1600, 4.5, 2.2); aim(k)
f = light("Light_Fill", 'AREA', (5.0, -2.5, 1.6), (0, 0, 0), 350, 4.0, 3.0); aim(f)
r = light("Light_Rim", 'AREA', (0.5, 6.5, 2.6), (0, 0, 0), 900, 6.0, 1.2); aim(r)
light("Light_OverheadStrip", 'AREA', (0, 0, 5.5), (0, 0, 0), 900, 0.7, 12.0)
light("Light_SideStrip", 'AREA', (-5.5, 0, 1.2), (0, math.radians(-90), 0), 260, 0.5, 10.0)
C_DAY = coll("HC_Daylight"); C_NIGHT = coll("HC_Night")
sun = light("Sun_Daylight", 'SUN', (0, 0, 10), (math.radians(42), 0, math.radians(-35)), 4.5, col=C_DAY, color=(1.0, 0.96, 0.9))
sun.data.angle = math.radians(1.2)
moon = light("Light_NightRim", 'AREA', (2.5, 5.5, 3.0), (0, 0, 0), 220, 5.0, 2.0, col=C_NIGHT, color=(0.6, 0.7, 1.0)); aim(moon)
moon2 = light("Light_NightKick", 'AREA', (-3.5, 4.5, 1.2), (0, 0, 0), 90, 4.0, 1.0, col=C_NIGHT, color=(0.6, 0.7, 1.0)); aim(moon2)
for o in list(C_DAY.objects) + list(C_NIGHT.objects):
    o.hide_render = True
bpy.data.objects["Light_CabinFill"].data.energy = 10
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Punchy'
sc.view_settings.exposure = 0.0
cd = bpy.data.cameras.new("Cam_carbon"); cd.lens = 45
co = bpy.data.objects.new("Cam_carbon", cd); C_STUDIO.objects.link(co); co.location = (-1.55, -3.05, 0.42)
c = co.constraints.new('TRACK_TO'); c.target = empty("CamTarget_carbon", (-0.62, -2.15, 0.16), C_STUDIO)
c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
