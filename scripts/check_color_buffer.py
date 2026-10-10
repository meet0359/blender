import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];bpy.ops.wm.read_factory_settings(use_empty=True);S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=1
bpy.ops.mesh.primitive_plane_add();o=bpy.context.object;o.data.uv_layers.active.data[0].uv=(0,0)
m=bpy.data.materials.new('test');m.use_nodes=True;o.data.materials.append(m);ns=m.node_tree.nodes;ns.clear();lk=m.node_tree.links
im=bpy.data.images.load(str(R/'textures/racing_car/body/paint_BaseColor.png'));im.colorspace_settings.name='sRGB';print('SOURCE_PIXELS',im.is_float,list(im.pixels[:3]),flush=True)
n=ns.new('ShaderNodeTexImage');n.image=im;xyz=ns.new('ShaderNodeCombineXYZ');xyz.inputs['X'].default_value=.5/im.size[0];xyz.inputs['Y'].default_value=.5/im.size[1];lk.new(xyz.outputs[0],n.inputs['Vector']);em=ns.new('ShaderNodeEmission');out=ns.new('ShaderNodeOutputMaterial');lk.new(n.outputs[0],em.inputs[0]);lk.new(em.outputs[0],out.inputs[0]);target=bpy.data.images.new('sample',8,8,float_buffer=True);active=ns.new('ShaderNodeTexImage');active.image=target;ns.active=active;bpy.ops.object.bake(type='EMIT');print('SHADER_LINEAR',list(target.pixels[4*36:4*36+3]),flush=True)
