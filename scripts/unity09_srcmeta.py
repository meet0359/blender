import bpy,json,os
O=bpy.data.objects
names=[o.name for o in O if o.name.endswith('LOD0') or o.name.startswith(('Collision_','WheelColliderRef','CenterOfMass','Car_Root')) ]
exp=set()
def walk(o):
    exp.add(o.name);[walk(c) for c in o.children if not (o.name=='Car_Root' and c.name.startswith('LOD'))]
walk(O['Car_Root'])
for n in ['Collision','Front_Axle_Reference']:exp.discard(n)
d={}
for n in exp:
    o=O[n];d[n]=dict(type=o.type,parent=o.parent.name if o.parent else None,mats=[m.name if m else None for m in o.data.materials] if o.type=='MESH' else [],uv=[u.name for u in o.data.uv_layers] if o.type=='MESH' else [],world=[list(map(float,o.matrix_world.translation))])
json.dump(d,open(os.environ['TMPDIR']+'/unity09_srcmeta.json','w'));print(len(d),sorted(n for n in d if d[n]['parent'] not in(None,) and d[n]['parent']=='Car_Root'))
