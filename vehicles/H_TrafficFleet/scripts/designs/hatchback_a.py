# Design: Traffic_Hatchback_A — modern five-door compact hatchback (ORIGINAL fictional design).
# Class references (published, facts only): VW Golf Mk8 4284 x 1789 x 1456, WB 2636; Hyundai i30 4340 x 1795 x 1455, WB 2650 (mm).
# Proportions: FWD short dash-to-axle (0.43 m), short rear overhang (0.75 m), compact hood, long roof ending in a roof spoiler, steep hatch glass
# (~52 deg), upright tailgate with split lamps, rising belt line, 17" wheels. Character: crisp but restrained (everyday car, not a hot hatch).
CLASS = 'hatchback'; VEH = 'Traffic_Hatchback_A'; PRE = 'TS_HatchA'; CKP_ = 'traffichatchbacka'; COLL_NAME = 'TRAFFIC_HATCHBACK_A'; PAINT_RGB = (.30, .018, .022)   # review colour: deep red metallic
DIM = dict(length=4.26, width_body=1.79, height=1.46, wheelbase=2.63, track_f=1.54, track_r=1.53, overhang_f=.88, overhang_r=.75, ground_clearance=.14, tire='225/45 R17 (R 0.317, rim 17")')
YF, YR = -1.25, 1.38; RW = .317; WT = .225; RIM = .2159; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.13, 2.13; COWL = -.82
ZC = pchip([YN, -2.05, -1.85, -1.55, -1.25, COWL, -.40, .02, .35, .80, 1.25, 1.62, 1.75, 1.79, 1.98, 2.02, YT], [.60, .785, .835, .864, .886, .962, 1.205, 1.425, 1.458, 1.458, 1.448, 1.436, 1.428, 1.400, 1.085, 1.068, 1.00])   # production: convex hood crown; v3: roof-spoiler lip at 1.75, ~62 deg hatch glass straight into the tailgate
_YS = [YN, -2.00, -1.75, -1.25, COWL, 0, .90, 1.40, 1.70, 1.92, 2.02, YT]
ZBELT = pchip(_YS, [.70, .780, .830, .860, .885, .915, .945, .975, .990, .985, .960, .900])         # rising belt (hatch wedge)
WBELT = pchip(_YS, [.78, .835, .852, .856, .850, .848, .852, .858, .852, .835, .815, .780])
WMAX = pchip(_YS, [.83, .872, .890, .895, .890, .888, .890, .895, .892, .880, .860, .830])            # 1.79 m body
ZSH = pchip([YN, YF, 0, YR, YT], [.50, .60, .62, .63, .58])
ZFLOOR = pchip([YN, -1.98, -1.75, 1.68, 1.92, YT], [.28, .21, .145, .145, .20, .30])
WFLOOR = pchip([YN, -1.9, 0, 1.9, YT], [.60, .76, .80, .76, .64])
CAB = lambda y: ss(COWL - .14, COWL + .06, y) * (1 - ss(1.99, 2.04, y))
ROOFW = pchip([COWL, -.30, .20, .80, 1.30, 1.95], [.720, .690, .675, .665, .650, .620]); ROOF_END = 1.95   # v3: wider roof end (square hatch, not a tapering sedan C-pillar)
DECK_FADE = lambda y: ss(1.97, 2.04, y)
SK = lambda y: .018 * ss(-.95, -.75, y) * (1 - ss(.85, 1.05, y))
HOOD_RIDGE = lambda y: 0.0
STAT = [round(v, 3) for v in np.linspace(-1.68, 1.72, 18)] + [1.765, 1.81]   # hatch-glass stations; must stay IN FRONT of the end blend rings (1.895 folded the hatch glass)
YC_F = pchip([.16, .22, .30, .42, .52, .60, .68, .74, .78], [-2.02, -2.08, -2.115, -2.13, -2.128, -2.12, -2.105, -2.085, -2.06])
YC_R = pchip([.20, .26, .34, .45, .58, .64, .675, .70, .80, .92, 1.02, 1.08], [2.06, 2.10, 2.128, 2.135, 2.133, 2.128, 2.112, 2.100, 2.098, 2.090, 2.073, 2.052])   # production: bumper 3 cm proud of the tailgate, defined ledge at .66-.70   # v3: compact bumper (ledge .66-.70) + near-vertical tailgate up to the glass
RS_F = pchip([.16, .30, .48, .60, .70, .78], [.070, .072, .078, .085, .095, .100])
RS_R = pchip([.20, .34, .50, .66, .85, 1.03], [.060, .058, .055, .055, .058, .062])   # v3: crisper hatch corners (no soap bar)
END = {'R': dict(sgn=1, ysec=2.00, Yc=YC_R, plan=.03, Rs=RS_R, Rt=.022, Rb=.075, d=(.12, .025), sc=(.982, .94, .84, .58, .24)),
       'F': dict(sgn=-1, ysec=-1.98, Yc=YC_F, plan=.10, Rs=RS_F, Rt=.025, Rb=.065, d=(.12, .025), sc=(.982, .94, .84, .56, .22))}
GLASS_WS = (COWL + .02, -.02); GLASS_RW = (1.76, 1.86); GLASS_SIDE = (COWL + .08, 1.56); SEAL_Y = (COWL + .04, 1.60); RAIL_Y = (COWL, 1.95)   # glass stops before the tailgate end-blend zone (glass in the blend rings folded / tore)
CREST = lambda y: .55 * ss(-2.20, -2.10, y) * (1 - ss(1.95, 2.08, y))
J3_F = (1.68, 2.05); J3_R = (1.75, 2.06)
ROCKER_CREASE = lambda y: .40 * ss(-.95, -.75, y) * (1 - ss(.85, 1.05, y))
HL = lambda sx: rounded([(sx * .40, .700), (sx * .58, .712), (sx * .74, .735), (sx * .800, .752), (sx * .808, .712), (sx * .76, .672), (sx * .58, .658), (sx * .42, .668)], [.010, .03, .03, .012, .014, .02, .03, .010], 3)
GRILLE = rounded([(-.36, .665), (.36, .665), (.32, .585), (-.32, .585)], [.02, .02, .03, .03], 3)          # slim upper grille between the lamps
LOWER = rounded([(-.50, .470), (.50, .470), (.43, .270), (-.43, .270)], [.06, .06, .05, .05], 3)          # large trapezoid lower intake
FOG = lambda sx: rounded([(sx * .56, .440), (sx * .69, .465), (sx * .72, .320), (sx * .60, .290)], .025, 2)
TL = lambda sx: rounded([(sx * .36, 1.035), (sx * .64, 1.048), (sx * .785, 1.040), (sx * .805, .950), (sx * .785, .820), (sx * .70, .825), (sx * .58, .915), (sx * .36, .945)], [.010, .02, .02, .025, .016, .02, .03, .010], 3)   # v3: large lamps (22 cm at the corner) across the tailgate split   # v3: large boomerang lamps across the tailgate split
PLATE_R = rounded([(-.26, .845), (.26, .845), (.26, .735), (-.26, .735)], .014, 3)
VALANCE = rounded([(-.70, .395), (.70, .395), (.64, .200), (-.64, .200)], [.03, .03, .02, .02], 3)   # v3: black diffuser = defined compact lower bumper
EXH = None
HANDLES = ((-.12, .01), (.94, 1.06)); HANDLE_Z = .868
HOOD_LOOP = rounded([(.66, COWL - .03), (.74, -1.35), (.70, -1.94), (-.70, -1.94), (-.74, -1.35), (-.66, COWL - .03)], [.02, .25, .07, .07, .25, .02], 6)
FDOOR = lambda TOPZ: rounded([(-.82, .30), (.16, .30), (.16, TOPZ(.16)), (-.76, TOPZ(-.76))], [.04, .02, .01, .02], 5)
RDOOR = lambda TOPZ: rounded([(.22, .30), (.93, .30), (.957, .368), (1.012, .544), (1.136, .679), (1.48, TOPZ(1.48)), (.22, TOPZ(.22))], [.02, .03, .03, .06, .06, .02, .01], 5)
FUEL = rounded([(1.55, .80), (1.69, .80), (1.69, .92), (1.55, .92)], .025, 4)
SWEEP_C = (0, 1.82); REAR_SHUT = [(1.82, .640), (1.95, .662)]; REAR_SHUT_Z = .665; REAR_SHUT_FACE_Y = 1.99
LID_SIDE = [('r', .62, .680), ('r', .62, .85), ('r', .625, 1.00), ('t', .64, 1.96), ('t', .65, 1.88), ('t', .65, 1.80), ('t', .63, 1.74)]   # v3: hatch opening (full-width glass + tailgate)   # tailgate: rear face -> D-pillar edge -> roof header
LID_MID = [('t', -.35, 1.725), ('t', -.12, 1.725), ('t', .12, 1.725), ('t', .35, 1.725)]; LID_X = .62
FSHUT_LAMP = (.812, .712); FSHUT_Z1 = .700; FSHUT_MID = [(-1.72, .630)]; FSHUT_ARC = 150
MIRROR_POS = (.95, COWL + .12, ZBELT(COWL + .12) + .10); MIRROR_SIZE = (.18, .068, .092); MIRROR_BASE_Z = ZBELT(COWL + .12) + .025; MIRROR_DETECT = (.90, .90)
FIN_Y0 = 1.18; CLADDING = False; UNDER_Y = 1.75
HL_CELLS = 3; HL_DRL_SEGS = 5; INTAKE_BLADES = (0.0,)
REVERSE = (.40, .52, .540, .558); REFLECTOR = (.60, .72, .450, .468); REPEATER = (-1.80, -1.74, .660, .676)
LINER_XI = .55; GRILLE_STYLE = 'horizontal'; GRILLE_BARS = 3; GRILLE_BAR_MAT = 'TS_Atlas:dark_chrome'; CHIN_Z = .200; CHIN_W = .60
PLATE_F = (.335, .445); REAR_STRIP = None; VALANCE_TRIM = 'TS_Atlas:gloss_black'; BADGE_F = .625; BADGE_R = .985
TRAY = (.150, .76, -1.75, 1.80); HMSL = ('t', .20, 1.745, 1.760)
BPILLAR = (.12, .22); EXTRA_PILLARS = []; BELT_Y1 = 1.50; BELT_TRIM = 'TS_Atlas:gloss_black'
ROCKER = None; ROOF_RAILS = None
SPOKES = dict(n=10, dish=.040, twin=.40, curve=0.0, w0=.012, w1=.009); DISC_R = .150
INT = dict(drv=.36, dz=0.0, half=.80, rows=[.04, .90], dash=-.56, parcel=None, two_tone=False, dark=True)
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -1.0 and p.z < .95], 'Collision_Body': [p for p in pts if -1.15 < p.y < 1.15 and p.z < .95],
                         'Collision_Cabin': [p for p in pts if COWL - .05 < p.y < 1.95 and p.z > .88], 'Collision_Rear': [p for p in pts if p.y > .95 and p.z < 1.10]}
COM = (0, -.18, .50)
RW_COL = 10                                                                                            # v2: full-width hatch glass
FACE_TRIMS = [('R', .405, .64, .010, 'TS_Atlas:gloss_black')]                                       # production: bumper / diffuser split trim
