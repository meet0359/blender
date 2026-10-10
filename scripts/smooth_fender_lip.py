import bpy, ast, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
env=globals()
tree=ast.parse((ROOT/'scripts/fix_front_fender.py').read_text())
for n in tree.body:
    if isinstance(n,(ast.Import,ast.ImportFrom,ast.Assign,ast.For,ast.FunctionDef)):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['o','counts'] for t in n.targets): break
        exec(compile(ast.Module(body=[n],type_ignores=[]),'helpers','exec'),env)
o=bpy.data.objects['Car_Body']; count=0
for v in o.data.vertices:
    x,y,z=v.co
    if abs(y+1.35)>=.32: continue
    top=top_z(1,y)+lift(1,y); bot=arch_bottom(y)
    if abs(bot-top)<1e-7: continue
    t=(z-top)/(bot-top)
    j=round(t*12)
    if not 0<=j<=12 or abs(t-j/12)>.001: continue
    t=j/12; a=min(1,gauss(y,-1.35,.48)+gauss(y,1.35,.49))
    xx=width(y)-.045*t-.075*(1-a)*math.sin(math.pi*t)**1.3+.016*math.sin(math.pi*t)*a
    roll=.039*min(1,gauss(y,-1.35,.46)+gauss(y,1.35,.48))*t**6
    if min(abs(x-xx),abs(x-xx-roll))<.00015:
        v.co.x=xx+roll; count+=1
for m in o.modifiers:
    if m.type=='SOLIDIFY': m.thickness=.0008; m.thickness_clamp=1
o.data.update()
print('CONSISTENT FRONT LIP',count)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'racing_car_04_exterior_working.blend'))
