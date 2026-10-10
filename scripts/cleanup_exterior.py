"""Targeted non-destructive shell/trim/glazing cleanup, on loaded 04 only."""
import bpy
import bmesh
import math
from mathutils import Vector

# Realistic shell thickness also avoids hidden folded offsets at tight returns.
for o in bpy.data.collections['CAR'].objects:
    if o.type!='MESH': continue
    if o.name in ['Car_Body','Hood','Car_Door_L','Car_Door_R','Roof_Panel','Rear_Engine_Cover']:
        for m in o.modifiers:
            if m.type=='SOLIDIFY': m.thickness=.0025
    elif o.name in ['Front_Bumper','Rear_Bumper']:
        for m in o.modifiers:
            if m.type=='SOLIDIFY': m.thickness=.0035

# Capped bevel curves have coincident cap/side vertices in Blender's evaluated
# tessellation. A live Weld makes those trim meshes topologically connected.
for o in bpy.data.objects:
    if o.type=='CURVE':
        if not any(m.type=='WELD' for m in o.modifiers):
            m=o.modifiers.new('Connect capped trim seams','WELD')
            m.merge_threshold=.000001
            m.mode='ALL'

# Source intake depth plates were single faces; close them with live thickness.
for name in ['Front_Central_Intake_Depth','Front_Cooling_Duct_L_Depth','Front_Cooling_Duct_R_Depth','Rear_Center_Recess_Depth','Cabin_Lower_Deck']:
    o=bpy.data.objects[name]
    if not any(m.type=='SOLIDIFY' for m in o.modifiers):
        m=o.modifiers.new('Close depth plate','SOLIDIFY'); m.thickness=.002; m.offset=-1

# Recess the side-glass roof seat below the roof's inner skin. Painted rails
# cover the 3–6 mm seat; transparent surfaces no longer cross the roof panel.
for name in ['Window_FL','Window_FR','Window_RL','Window_RR']:
    o=bpy.data.objects[name]
    heights=[v.co.z for v in o.data.vertices]
    # Rows were generated in ascending v order, with 17 rows.
    columns=len(o.data.vertices)//17
    for v in o.data.vertices:
        row=v.index//columns
        t=row/16
        fade=t**7
        v.co.z-=.007*fade
        v.co.x-=math.copysign(.0025*fade,v.co.x)
    o.data.update()

def flip_if(o,component,desired):
    average=sum(p.normal[component]*p.area for p in o.data.polygons)
    if average*desired<0:
        bm=bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
        bm.to_mesh(o.data); bm.free(); o.data.update()

for name in ['Rear_Bumper','Taillight_L','Taillight_R','Taillight_Cavity_L','Taillight_Cavity_R']:
    flip_if(bpy.data.objects[name],1,1)
for name in ['Window_FL','Window_RL']: flip_if(bpy.data.objects[name],0,-1)
for name in ['Window_FR','Window_RR']: flip_if(bpy.data.objects[name],0,1)

# Thin three-millimetre exhaust walls, with dark independent inner sleeves.
for name in ['Exhaust_L','Exhaust_R']:
    o=bpy.data.objects[name]
    for v in o.data.vertices:
        r=math.hypot(v.co.x,v.co.z)
        if abs(r-.055)<.00001:
            v.co.x*=.058/r; v.co.z*=.058/r
    o.data.update()

for o in bpy.data.objects:
    if o.type=='MESH':
        o.data.update()
