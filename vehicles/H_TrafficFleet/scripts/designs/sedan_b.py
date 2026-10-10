# Design: Traffic_Sedan_B (premium executive sedan) — values identical to ts_sedan_b.py (H2). Used as the ts_vehicle.py regression reference.
VEH = 'Traffic_Sedan_B'; PRE = 'TS_SedanB'; CKP_ = 'trafficsedanb'; COLL_NAME = 'TRAFFIC_SEDAN_B'; PAINT_RGB = (.150, .155, .165)
DIM = dict(length=4.98, width_body=1.89, height=1.47, wheelbase=2.97, track_f=1.625, track_r=1.640, overhang_f=.86, overhang_r=1.15, ground_clearance=.14, tire='245/40 R20 (R 0.352, rim 20")')
YF, YR = -1.62, 1.35; RW = .352; WT = .245; RIM = .254; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.48, 2.50; COWL = -.74
ZC = pchip([YN, -2.38, -2.25, -1.90, -1.62, -1.20, COWL, -.40, -.05, .25, .55, .85, 1.12, 1.45, 1.78, 2.10, 2.38, YT], [.60, .800, .835, .872, .898, .930, .975, 1.220, 1.425, 1.462, 1.468, 1.458, 1.420, 1.245, 1.085, 1.092, 1.100, 1.040])
_YS = [YN, -2.35, -1.95, -1.62, -1.10, -.40, .40, 1.10, 1.60, 2.05, 2.35, YT]
ZBELT = pchip(_YS, [.70, .800, .860, .885, .905, .925, .950, .975, .990, 1.000, .990, .950])
WBELT = pchip(_YS, [.80, .872, .893, .898, .890, .886, .888, .895, .898, .893, .878, .835])
WMAX = pchip(_YS, [.86, .915, .938, .946, .938, .936, .938, .944, .946, .940, .925, .885])
ZSH = pchip([YN, YF, 0, YR, YT], [.52, .64, .67, .68, .62])
ZFLOOR = pchip([YN, -2.30, -2.05, 1.90, 2.16, 2.34, YT], [.30, .23, .150, .150, .180, .236, .32])
WFLOOR = pchip([YN, -2.3, 0, 2.3, YT], [.64, .80, .84, .80, .68])
CAB = lambda y: ss(COWL - .14, COWL + .06, y) * (1 - ss(1.62, 1.84, y))
ROOFW = pchip([COWL, -.30, .20, .70, 1.10, 1.78], [.750, .715, .700, .690, .665, .635]); ROOF_END = 1.78
DECK_FADE = lambda y: ss(1.10, 1.70, y)
SK = lambda y: .030 * ss(-1.20, -1.00, y) * (1 - ss(.92, 1.12, y))
HOOD_RIDGE = lambda y: E_('TS_HOODRIDGE', .007) * ss(-2.22, -2.02, y) * (1 - ss(COWL - .28, COWL - .06, y))
STAT = [round(v, 3) for v in np.linspace(-1.96, 2.08, 21)]
YC_R = pchip([.20, .26, .34, .45, .58, .64, .69, .82, .95, 1.05, 1.10], [2.40, 2.45, 2.48, 2.495, 2.492, 2.486, 2.465, 2.468, 2.462, 2.448, 2.43])
YC_F = pchip([.16, .22, .30, .42, .55, .65, .72, .78, .82], [-2.36, -2.42, -2.455, -2.475, -2.48, -2.476, -2.464, -2.442, -2.418])
RS_R = pchip([.20, .34, .50, .66, .80, 1.10], [.075, .077, .080, .082, .085, .088])
RS_F = pchip([.16, .30, .48, .58, .70, .84], [.072, .074, .078, .082, .088, .095])
END = {'R': dict(sgn=1, ysec=2.32, Yc=YC_R, plan=.06, Rs=RS_R, Rt=.020, Rb=.080, d=(.12, .025), sc=(.982, .94, .84, .58, .24)),
       'F': dict(sgn=-1, ysec=-2.30, Yc=YC_F, plan=.08, Rs=RS_F, Rt=.022, Rb=.065, d=(.12, .025), sc=(.982, .94, .84, .56, .22))}
GLASS_WS = (COWL + .02, -.03); GLASS_RW = (1.14, 1.74); GLASS_SIDE = (COWL + .08, 1.50); SEAL_Y = (COWL + .04, 1.54); RAIL_Y = (COWL, 1.74)
CREST = lambda y: .80 * ss(E_('TS_CRF0', -2.70), E_('TS_CRF1', -2.60), y) * (1 - ss(2.42, 2.55, y))
J3_F = (1.96, 2.36); J3_R = (2.08, 2.40)
ROCKER_CREASE = lambda y: .65 * ss(-1.25, -1.02, y) * (1 - ss(.98, 1.20, y))
HL = lambda sx: rounded([(sx * .43, .704), (sx * .62, .720), (sx * .78, .750), (sx * .85, .772), (sx * .862, .726), (sx * .82, .682), (sx * .64, .664), (sx * .45, .672)], [.010, .03, .03, .012, .014, .02, .03, .010], 3)
GRILLE = rounded([(-.40, .705), (.40, .705), (.34, .480), (-.34, .480)], [.03, .03, .05, .05], 3)
LOWER = rounded([(-.56, .345), (.56, .345), (.50, .210), (-.50, .210)], [.03, .03, .04, .04], 3)
FOG = lambda sx: rounded([(sx * .64, .520), (sx * .770, .535), (sx * .785, .300), (sx * .70, .265)], .025, 2)
TL = lambda sx: rounded([(sx * .40, .950), (sx * .70, .965), (sx * .845, .955), (sx * .852, .880), (sx * .76, .855), (sx * .42, .880)], [.010, .02, .02, .016, .02, .012], 3)
PLATE_R = rounded([(-.265, .835), (.265, .835), (.265, .722), (-.265, .722)], .014, 3)
VALANCE = rounded([(-.76, .360), (.76, .360), (.70, .205), (-.70, .205)], .02, 3)
EXH = lambda sx: rounded([(sx * .46, .312), (sx * .66, .312), (sx * .64, .246), (sx * .48, .246)], .02, 3)
HANDLES = ((-.05, .09), (.99, 1.13)); HANDLE_Z = .872
HOOD_LOOP = rounded([(.72, COWL - .03), (.80, -1.30), (.76, -2.30), (-.76, -2.30), (-.80, -1.30), (-.72, COWL - .03)], [.02, .3, .08, .08, .3, .02], 6)
FDOOR = lambda TOPZ: rounded([(-1.14, .33), (.33, .33), (.33, TOPZ(.33)), (-1.06, TOPZ(-1.06))], [.04, .02, .01, .02], 5)
RDOOR = lambda TOPZ: rounded([(.39, .33), (.86, .33), (.887, .406), (.947, .598), (1.083, .746), (1.50, TOPZ(1.50)), (.39, TOPZ(.39))], [.02, .03, .03, .06, .06, .02, .01], 5)
FUEL = rounded([(1.62, .80), (1.78, .80), (1.78, .93), (1.62, .93)], .025, 4)
SWEEP_C = (0, 2.12); REAR_SHUT = [(1.95, .640), (2.12, .668), (2.28, .684)]; REAR_SHUT_Z = .686; REAR_SHUT_FACE_Y = 2.34
LID_SIDE = [('r', .62, .690), ('r', .62, .80), ('r', .62, .93), ('r', .625, 1.035), ('t', .645, 2.385), ('t', .675, 2.20), ('t', .68, 2.00), ('t', .665, 1.85), ('t', .63, 1.805)]
LID_MID = [('t', -.40, 1.80), ('t', -.15, 1.80), ('t', .15, 1.80), ('t', .40, 1.80)]; LID_X = .62
FSHUT_LAMP = (.866, .728); FSHUT_Z1 = .715; FSHUT_MID = [(-2.10, .660)]; FSHUT_ARC = 150
MIRROR_POS = (.99, COWL + .09, 1.03); MIRROR_SIZE = (.20, .072, .098); MIRROR_BASE_Z = .955; MIRROR_DETECT = (.93, .92)
FIN_Y0 = .80; CLADDING = False; UNDER_Y = 2.12
HL_CELLS = 4; HL_DRL_SEGS = 7; INTAKE_BLADES = (-.019, .018)
REVERSE = (.44, .58, .500, .520); REFLECTOR = (.66, .78, .500, .520); REPEATER = (-2.10, -2.03, .700, .716)
LINER_XI = .58; GRILLE_STYLE = 'vertical'; GRILLE_BARS = 11; GRILLE_BAR_MAT = 'TS_Atlas:chrome'; CHIN_Z = .205; CHIN_W = .66
PLATE_F = (.360, .470); REAR_STRIP = (.921, .41); VALANCE_TRIM = 'TS_Atlas:alu_brushed'; BADGE_F = .600; BADGE_R = .985
TRAY = (.158, .80, -2.10, 2.15); HMSL = ('r', .24, 1.062, 1.072)
BPILLAR = (.31, .41); EXTRA_PILLARS = []; BELT_Y1 = 1.47; BELT_TRIM = 'TS_Atlas:alu_brushed'
ROCKER = (.300, .024, 'TS_Atlas:dark_chrome'); ROOF_RAILS = None
SPOKES = dict(n=10, dish=.034, twin=0, curve=0.0, w0=.0115, w1=.0075); DISC_R = .172
INT = dict(drv=.38, dz=0.0, half=.84, rows=[.14, 1.04], dash=-.56, parcel=1.56, two_tone=True)
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -1.20 and p.z < .98], 'Collision_Body': [p for p in pts if -1.40 < p.y < 1.15 and p.z < .97],
                         'Collision_Cabin': [p for p in pts if COWL - .05 < p.y < 1.80 and p.z > .90], 'Collision_Rear': [p for p in pts if p.y > .95 and p.z < 1.12]}
COM = (0, -.08, .53)
