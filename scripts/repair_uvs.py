import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
repair=json.loads((ROOT/'uv_repair_faces.json').read_text())
count=0
for name,faces in repair.items():
    o=bpy.data.objects[name]; me=o.data; me.calc_loop_triangles(); uv=me.uv_layers['UVMap'].data
    for index in faces:
        p=me.polygons[index]; loops=list(p.loop_indices); n=len(loops)
        # Unfold existing loop triangles without altering geometry. This keeps
        # edge lengths on narrow/non-planar quads instead of squaring them.
        tris=[list(t.loops) for t in me.loop_triangles if t.polygon_index==index]
        P={l:me.vertices[me.loops[l].vertex_index].co.copy() for l in loops}; placed={}
        a,b,c=tris[0]; length=(P[b]-P[a]).length
        placed[a]=Vector((0,0)); placed[b]=Vector((max(length,1e-10),0))
        pending=list(tris)
        for _ in range(len(tris)+2):
            progress=False
            for tri in list(pending):
                missing=[l for l in tri if l not in placed]
                if not missing: pending.remove(tri); continue
                if len(missing)!=1: continue
                c=missing[0]; k=tri.index(c); a=tri[(k+1)%3]; b=tri[(k+2)%3]
                edge=placed[b]-placed[a]; length=max(edge.length,1e-10); direction=edge/length
                ra=(P[c]-P[a]).length; rb=(P[c]-P[b]).length
                along=(ra*ra-rb*rb+length*length)/(2*length)
                height=math.sqrt(max(0,ra*ra-along*along))
                placed[c]=placed[a]+direction*along+Vector((-direction.y,direction.x))*height
                pending.remove(tri); progress=True
            if not pending or not progress: break
        if len(placed)!=n:
            r=math.sqrt(max(p.area,1e-10)/(n*.5*math.sin(2*math.pi/n)))
            placed={l:Vector((r*math.cos(2*math.pi*k/n),r*math.sin(2*math.pi*k/n))) for k,l in enumerate(loops)}
        for l in loops: uv[l].uv=placed[l]+Vector((10+count*.01,10))
        count+=1
    o['uv_isolated_repair_faces']=len(faces)
groups={}
for o in bpy.data.objects:
    if o.type!='MESH' or 'texture_group' not in o: continue
    # Correct the wheel/tire grouping by semantic names, without changing mesh.
    if o['texture_group'] in ['wheels','tires']:
        o['texture_group']='tires' if o.name in ['Wheel_FL','Wheel_FR','Wheel_RL','Wheel_RR'] or o.name.startswith('Tire_') else 'wheels'
    groups.setdefault(o['texture_group'],[]).append(o)
for group,objs in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.average_islands_scale(); bpy.ops.uv.pack_islands(rotate=True,margin=.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    for o in objs:
        me=o.data; me.calc_loop_triangles(); uv=me.uv_layers.active.data; area=0
        for t in me.loop_triangles:
            a,b,c=[uv[i].uv for i in t.loops]; area+=abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))*.5
        o['uv_meter_scale']=math.sqrt(sum(p.area for p in me.polygons)/max(area,1e-12))
print('ISOLATED UV FACE CHARTS',count,flush=True)
# UV-independent circular wear coordinates for existing X-axis rotor faces.
m=bpy.data.materials['MAT_BrakeDisc']; nd=m.node_tree.nodes; links=m.node_tree.links
tc=nd.new('ShaderNodeTexCoord'); sep=nd.new('ShaderNodeSeparateXYZ'); links.new(tc.outputs['Object'],sep.inputs[0])
yy=nd.new('ShaderNodeMath'); yy.operation='MULTIPLY'; zz=nd.new('ShaderNodeMath'); zz.operation='MULTIPLY'
for node,axis in [(yy,'Y'),(zz,'Z')]: links.new(sep.outputs[axis],node.inputs[0]); links.new(sep.outputs[axis],node.inputs[1])
add=nd.new('ShaderNodeMath'); add.operation='ADD'; links.new(yy.outputs[0],add.inputs[0]); links.new(zz.outputs[0],add.inputs[1])
root=nd.new('ShaderNodeMath'); root.operation='SQRT'; links.new(add.outputs[0],root.inputs[0])
mul=nd.new('ShaderNodeMath'); mul.operation='MULTIPLY'; mul.inputs[1].default_value=8; links.new(root.outputs[0],mul.inputs[0])
vec=nd.new('ShaderNodeCombineXYZ'); links.new(mul.outputs[0],vec.inputs['Y'])
for node in nd:
    if node.type=='TEX_IMAGE' and node.label in ['Roughness','BaseColor']: links.new(vec.outputs[0],node.inputs['Vector'])
m['game_conversion']='Bake object-space concentric rotor wear into the brakes atlas before engine export'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_06_materials_uv_working.blend'))
