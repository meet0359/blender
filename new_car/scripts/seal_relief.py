# Windshield seal relief: lift the rubber seal up to 1.5 mm along its normal, fading out within 12 mm of
# each lower windshield corner, so the bonded glass never intersects it. Appended to the body's GN group.
def add_seal_relief(ng, corner=(0.519, -0.6745, 0.8028), radius=0.012, lift=0.0015):
    from mathutils import Vector
    go = next(n for n in ng.nodes if n.type == 'GROUP_OUTPUT')
    src = go.inputs[0].links[0].from_socket
    pos = ng.nodes.new("GeometryNodeInputPosition"); nrm = ng.nodes.new("GeometryNodeInputNormal")
    dists = []
    for sx in (1, -1):
        d = ng.nodes.new("ShaderNodeVectorMath"); d.operation = 'DISTANCE'
        d.inputs[1].default_value = (sx * corner[0], corner[1], corner[2])
        ng.links.new(pos.outputs[0], d.inputs[0]); dists.append(d)
    mn = ng.nodes.new("ShaderNodeMath"); mn.operation = 'MINIMUM'
    ng.links.new(dists[0].outputs["Value"], mn.inputs[0]); ng.links.new(dists[1].outputs["Value"], mn.inputs[1])
    fall = ng.nodes.new("ShaderNodeMapRange"); fall.clamp = True
    fall.inputs["From Min"].default_value = 0.0; fall.inputs["From Max"].default_value = radius
    fall.inputs["To Min"].default_value = lift; fall.inputs["To Max"].default_value = 0.0
    ng.links.new(mn.outputs[0], fall.inputs["Value"])
    sc_ = ng.nodes.new("ShaderNodeVectorMath"); sc_.operation = 'SCALE'
    ng.links.new(nrm.outputs[0], sc_.inputs[0]); ng.links.new(fall.outputs["Result"], sc_.inputs["Scale"])
    sp = ng.nodes.new("GeometryNodeSetPosition"); sp.name = "SealRelief"
    ng.links.new(src, sp.inputs["Geometry"]); ng.links.new(sc_.outputs[0], sp.inputs["Offset"])
    ng.links.new(sp.outputs[0], go.inputs[0])
