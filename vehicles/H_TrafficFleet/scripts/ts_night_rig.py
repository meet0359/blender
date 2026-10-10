# Night review rig v2 (2026-10-10). Executed by ts_render.py for MODE 'night' (REALISTIC HIGHWAY NIGHT) and 'night_qa' (NIGHT VISIBILITY QA).
# Blender PREVIEW rig only: no vehicle asset, material or geometry is touched.
# Root cause it fixes (measured on Sedan B, rig v1): the v1 night sky was almost black (strength 0.004), so clear-coated paint and glass
# mirrored black (paint median luminance 0.020, 51 % of body pixels < 0.02, vs 0.118 for white clay under the same light), plus only two
# side street lights and a high-contrast AgX look. Unity equivalent: a night skybox / reflection probe with horizon glow + ambient light,
# not per-vehicle realtime lights.
QA_ = MODE == 'night_qa'
# ---- world: deep-blue zenith, warm light-pollution glow at the horizon (something for glossy paint / glass to reflect), dim ground
for l_ in [l for l in nt.links if l.to_node == bg]: nt.links.remove(l_)
tc_ = nt.nodes.new('ShaderNodeTexCoord'); sx_ = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc_.outputs['Generated'], sx_.inputs[0])
rp_ = nt.nodes.new('ShaderNodeValToRGB'); nt.links.new(sx_.outputs['Z'], rp_.inputs['Fac']); nt.links.new(rp_.outputs['Color'], bg.inputs[0])
e0, e1 = rp_.color_ramp.elements[0], rp_.color_ramp.elements[1]
e0.position, e0.color = 0.0, (.050, .040, .032, 1)                                          # horizon: sodium / LED light-pollution glow
e1.position, e1.color = 1.0, (.0030, .0045, .0100, 1)                                       # zenith: deep night blue
em_ = rp_.color_ramp.elements.new(.10); em_.color = (.012, .013, .020, 1)                  # glow fades within ~6 deg of the horizon
bg.inputs[1].default_value = 1.0
# ---- moon: cool, soft, raking (shows body curvature without flattening it)
sd.energy = .35 if not QA_ else .50; sd.color = (.70, .80, 1.0); sd.angle = math.radians(.5); sun.rotation_euler = (math.radians(58), 0, math.radians(135))
# ---- road lighting: warm LED street lights along the road; the ones far ahead / behind give the natural rim on roof and edges
LXn_ = -1.8
for nm_, loc_, en_ in (('TS_SL_R1', (LXn_ + 6.0, -32.0, 9.0), 1800), ('TS_SL_R2', (LXn_ + 6.0, -8.0, 9.0), 1800), ('TS_SL_M1', (LXn_ - 6.7, -20.0, 9.0), 1400),
                       ('TS_SL_Ahead', (LXn_, -62.0, 9.0), 2500), ('TS_SL_Behind', (LXn_ + 2.0, 14.0, 9.0), 2000)):
    ld_ = bpy.data.lights.new(nm_, 'POINT'); ld_.energy = en_; ld_.color = (1.0, .84, .64); ld_.shadow_soft_size = .5
    lo_ = bpy.data.objects.new(nm_, ld_); S.objects.link(lo_); lo_.location = loc_
if QA_:                                                                                       # visibility QA only: controlled soft fills (NOT a gameplay condition)
    for nm_, loc_, rot_, en_, sz_ in (('TS_QA_Top', (LXn_, -20.0, 12.0), (0, 0, 0), 2200, 9.0), ('TS_QA_R', (LXn_ + 11.0, -20.0, 3.0), (0, math.radians(90), 0), 900, 7.0),
                                      ('TS_QA_L', (LXn_ - 11.0, -20.0, 3.0), (0, math.radians(-90), 0), 600, 7.0)):
        ld_ = bpy.data.lights.new(nm_, 'AREA'); ld_.energy = en_; ld_.size = sz_; ld_.color = (.90, .94, 1.0)
        lo_ = bpy.data.objects.new(nm_, ld_); S.objects.link(lo_); lo_.location = loc_; lo_.rotation_euler = rot_
# ---- tone: softer curve so dark paint is not crushed; realistic keeps real exposure, QA lifts slightly
try: sc.view_settings.look = 'AgX - Base Contrast' if not QA_ else 'AgX - Medium Low Contrast'
except TypeError: sc.view_settings.look = 'None'
sc.view_settings.exposure = 0.0 if not QA_ else .4
print('NIGHT RIG v2', 'VISIBILITY QA' if QA_ else 'REALISTIC HIGHWAY NIGHT', flush=True)
