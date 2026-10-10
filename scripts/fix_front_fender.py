import bpy, ast, math, bmesh
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
env=globals()
tree=ast.parse((ROOT/'scripts/refine_realistic_body.py').read_text())
for n in tree.body:
    if isinstance(n,ast.FunctionDef) and n.name in ['gauss','smooth','lerp','interp','width','top_z','arch_bottom'] or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['width_points','center_points'] for t in n.targets):
        exec(compile(ast.Module(body=[n],type_ignores=[]),'helpers','exec'),env)
old_bottom=arch_bottom
tree=ast.parse((ROOT/'scripts/build_exterior.py').read_text())
for n in tree.body:
    if isinstance(n,ast.FunctionDef) and n.name=='arch_bottom': exec(compile(ast.Module(body=[n],type_ignores=[]),'helpers','exec'),env)
def lift(u,y):
    d=abs(y+1.35)/.32
    return .075*(.5+.5*math.cos(math.pi*d))**2*smooth(max(0,min(1,(u-.70)/.30))) if d<1 else 0
o=bpy.data.objects['Car_Body']; counts=[0,0]
for v in o.data.vertices:
    x,y,z=v.co
    if abs(y+1.35)>=.32: continue
    top=top_z(1,y); old=old_bottom(y); modified=top-old>.005
    bot=arch_bottom(y) if modified else old
    matched=False
    for j in range(13):
        t=j/12; a=min(1,gauss(y,-1.35,.48)+gauss(y,1.35,.49))
        xx=width(y)-.045*t-.075*(1-a)*math.sin(math.pi*t)**1.3+.016*math.sin(math.pi*t)*a
        if modified and j>0: xx+=.039*min(1,gauss(y,-1.35,.46)+gauss(y,1.35,.48))*t**6
        if abs(x-xx)<.0001 and abs(z-lerp(top,bot,t))<.0001:
            v.co.z=lerp(top+lift(1,y),arch_bottom(y),t)
            counts[0]+=1; matched=True; break
    if not matched:
        u=x/width(y)
        if abs(z-top_z(u,y))<.0001:
            v.co.z+=lift(u,y); counts[1]+=1
bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(o.data); bm.free(); o.data.update()
o['front_fender_fix']='Raised outer shoulder to remove inverted side strips over front arches; preserved opening and stance'
print('FENDER CORRECTION',counts,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_04_exterior_working.blend'))
