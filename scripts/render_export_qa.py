import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.samples=16;S.cycles.use_denoising=True;S.render.resolution_x=1600;S.render.resolution_y=1000;S.render.resolution_percentage=100
for i in range(4):bpy.data.collections['Car_LOD'+str(i)].hide_render=i!=0
bpy.data.collections['REFERENCE_Master_06'].hide_render=True
for o in bpy.data.collections['Car_LOD0'].all_objects:
 m=bpy.data.materials.get('QA_Transparent')
 if not m:
  m=bpy.data.materials.new('QA_Transparent');m.use_nodes=True;n=m.node_tree.nodes;n.clear();a=n.new('ShaderNodeBsdfTransparent');b=n.new('ShaderNodeBsdfDiffuse');b.inputs['Color'].default_value=(.22,.25,.3,1);c=n.new('ShaderNodeMixShader');c.inputs[0].default_value=.24;out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(a.outputs[0],c.inputs[1]);m.node_tree.links.new(b.outputs[0],c.inputs[2]);m.node_tree.links.new(c.outputs[0],out.inputs[0])
 for slot in o.material_slots:slot.material=m
 o.visible_shadow=False
for o in bpy.data.objects:
 if o.type=='MESH' and ('Floor' in o.name or 'Ground' in o.name):o.hide_render=True
def material(name,col):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.5;return m
cyan=material('QA_Collider',(.01,.48,.64));dark=material('QA_Edges',(.005,.04,.06));yellow=material('QA_Wheels',(.95,.4,.015));pink=material('QA_COM',(.85,.02,.15))
colliders=[o for o in bpy.data.collections['COLLISION'].all_objects if o.type=='MESH'];helpers=[]
for o in colliders:
 o.hide_render=False;o.data.materials.clear();o.data.materials.append(cyan)
 dup=o.copy();dup.data=o.data.copy();S.collection.objects.link(dup);dup.data.materials.clear();dup.data.materials.append(dark);mod=dup.modifiers.new('Overlay edges','WIREFRAME');mod.thickness=.009;helpers.append(dup)
def camera(name,pos,target,ortho=None):
 c=bpy.data.objects.new(name,bpy.data.cameras.new(name));S.collection.objects.link(c);c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=ortho or 6;return c
def render(name,c):
 S.camera=c;S.render.filepath=str(R/'previews'/name);print('QA RENDER',name,flush=True);bpy.ops.render.render(write_still=True)
render('collider_overlay_front_3q.png',camera('QA_front',(5,-6,3.5),(0,0,.5),6.2))
render('collider_overlay_side.png',camera('QA_side',(7,0,.7),(0,0,.6),5.8))
render('collider_overlay_top.png',camera('QA_top',(0,0,8),(0,0,0),8.4))
for o in colliders+helpers:o.hide_render=True
bpy.data.materials['QA_Transparent'].node_tree.nodes.get('Mix Shader').inputs[0].default_value=.035
for mat,col in [(yellow,(1,.45,.005)),(pink,(1,.005,.1))]:
 n=mat.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*col,1);e.inputs[1].default_value=.8;out=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(e.outputs[0],out.inputs[0])
def line(a,b,r,mat):
 d=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat)
def dot(pos,mat,r=.055):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=r,location=pos);bpy.context.object.data.materials.append(mat)
for k in ['FL','FR','RL','RR']:
 pos=bpy.data.objects['WheelColliderRef_'+k].matrix_world.translation;dot(pos,yellow);line(pos+Vector((-.23,0,0)),pos+Vector((.23,0,0)),.012,yellow)
 for axis in [Vector((0,.13,0)),Vector((0,0,.13))]:line(pos-axis,pos+axis,.008,yellow)
 label=bpy.data.curves.new('Label_'+k,'FONT');label.body=k;label.size=.15;o=bpy.data.objects.new('Label_'+k,label);S.collection.objects.link(o);o.location=pos+Vector((-.08,-.17,.13));label.materials.append(yellow)
for a,b in [('FL','FR'),('RL','RR')]:line(bpy.data.objects['WheelColliderRef_'+a].location,bpy.data.objects['WheelColliderRef_'+b].location,.012,yellow)
dot(bpy.data.objects['CenterOfMass'].location,pink,.075)
label=bpy.data.curves.new('COM label','FONT');label.body='COM  (0, +0.22, 0.37 m)';label.size=.12;o=bpy.data.objects.new('COM label',label);S.collection.objects.link(o);o.location=(-.52,.38,.5);label.materials.append(pink)
render('export_reference_points.png',camera('QA_refs',(0,-3.8,7),(0,0,.2),8.1))
