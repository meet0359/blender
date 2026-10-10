# Design: Traffic_Pickup_A — mid-size crew-cab pickup (ORIGINAL fictional design). v3 = two-shell PICKUP construction (ts_vehicle_v2.py, CLASS 'pickup').
# Class (approximate, mid-size crew cab): ~5.3-5.4 m long, ~1.9 m wide, ~1.85 m high, wheelbase ~3.25 m, ground clearance ~0.23 m.
# Shell 0 = engine compartment + upright crew cab, closed by a real flat CAB-BACK WALL (designed end surface, rear window in the wall).
# Shell 1 = separate open cargo bed: bed front wall, bedsides, tailgate face, step bumper; 35 mm gap to the cab. Real bed cavity (top-down cutter).
# v1 / v2 single-loft trials (car-based ute reading) kept in scratch as references.
CLASS = 'pickup'; VEH = 'Traffic_Pickup_A'; PRE = 'TS_PickupA'; CKP_ = 'trafficpickupa'; COLL_NAME = 'TRAFFIC_PICKUP_A'; PAINT_RGB = (.05, .14, .08)   # review colour: forest green metallic
DIM = dict(length=5.32, width_body=1.90, height=1.83, wheelbase=3.25, track_f=1.62, track_r=1.62, overhang_f=.92, overhang_r=1.15, ground_clearance=.23, tire='265/65 R17 (R 0.388, rim 17")')
YF, YR = -1.74, 1.51; RW = .388; WT = .265; RIM = .2159; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.66, 2.66; COWL = -1.00; CB = 1.000; BF = 1.035                                                # CB: cab-back wall, BF: bed front wall (35 mm gap)
# ---------------- shell 0: front + cab (these are also the global curves used by doors, belt trim, mirrors, interior)
ZC_CAB = pchip([YN, -2.58, -2.35, -1.74, -1.20, COWL, -.72, -.45, -.20, .40, .85, CB], [1.02, 1.215, 1.250, 1.270, 1.280, 1.290, 1.620, 1.810, 1.830, 1.830, 1.826, 1.822])   # tall flat hood, upright screen, flat roof
ZC_BED = pchip([BF, 1.12, 2.00, 2.50, YT], [1.268, 1.280, 1.282, 1.280, 1.262])
ZC = lambda y: ZC_CAB(y) if y < (CB + BF) / 2 else ZC_BED(y)
_YS = [YN, -2.50, -2.20, -1.74, COWL, 0, .60, CB]
ZBELT = pchip(_YS, [1.06, 1.160, 1.210, 1.240, 1.260, 1.270, 1.272, 1.270])                              # belt above the hood line
WBELT = pchip(_YS, [.86, .900, .925, .930, .925, .920, .920, .920])
WMAX = pchip(_YS, [.90, .930, .948, .950, .945, .940, .940, .940])                                       # 1.90 m body
ZSH = pchip([YN, YF, 0, CB], [.80, .88, .90, .90])
ZFLOOR = pchip([YN, -2.45, -2.20, CB], [.55, .45, .400, .400])
WFLOOR = pchip([YN, -2.3, 0, CB], [.70, .86, .88, .88])
CAB = lambda y: ss(COWL - .14, COWL + .06, y) * (1 - ss(CB + .03, CB + .06, y))                          # full greenhouse up to the cab-back wall
ROOFW = pchip([COWL, -.40, .30, CB], [.820, .815, .810, .805]); ROOF_END = CB - .06                       # boxy cab
DECK_FADE = lambda y: 0.0
SK = lambda y: .006 * ss(-1.20, -1.00, y) * (1 - ss(.60, .80, y))
HOOD_RIDGE = lambda y: E_('TS_HOODRIDGE', .012) * ss(-2.45, -2.30, y) * (1 - ss(COWL - .30, COWL - .08, y))
STAT = [round(v, 3) for v in np.linspace(-2.30, .74, 17)]
YC_F = pchip([.45, .52, .62, .75, .88, 1.00, 1.10, 1.18, 1.24, 1.28], [-2.52, -2.60, -2.64, -2.66, -2.66, -2.656, -2.648, -2.632, -2.610, -2.585])   # upright truck face
RS_F = pchip([.45, .62, .80, 1.00, 1.28], [.070, .070, .072, .075, .080])
YC_CABBACK = pchip([.40, .80, 1.20, 1.50, 1.85], [CB - .005, CB, CB, CB - .004, CB - .012])                  # flat, near-vertical cab-back wall
RS_CABBACK = pchip([.40, 1.00, 1.85], [.040, .040, .045])
END = {'R': dict(sgn=1, ysec=CB - .18, Yc=YC_CABBACK, plan=.0, Rs=RS_CABBACK, Rt=.030, Rb=.050, d=(.10, .025), sc=(.982, .94, .84, .58, .24)),
       'F': dict(sgn=-1, ysec=-2.45, Yc=YC_F, plan=.04, Rs=RS_F, Rt=.026, Rb=.070, d=(.12, .025), sc=(.982, .94, .84, .56, .22))}
GLASS_WS = (COWL + .02, -.40); GLASS_RW = (9.0, 9.0); GLASS_SIDE = (COWL + .08, CB - .10); SEAL_Y = (COWL + .04, CB - .08); RAIL_Y = (COWL, CB - .08)
CREST = lambda y: .55 * ss(-2.85, -2.75, y) * (1 - ss(CB - .12, CB - .06, y))
J3_F = (2.20, 2.55); J3_R = (CB - .25, CB - .05)
ROCKER_CREASE = lambda y: .35 * ss(-1.20, -1.00, y) * (1 - ss(.60, .80, y))
# ---------------- shell 1: cargo bed (own curves and both designed ends; no greenhouse)
YC_BEDF = pchip([.50, .90, 1.28], [BF + .004, BF, BF + .002])                                             # bed front wall (faces the cab)
YC_R = pchip([.45, .52, .58, .64, .75, .90, 1.05, 1.15, 1.22, 1.27], [2.58, 2.635, 2.655, 2.64, 2.64, 2.638, 2.635, 2.630, 2.622, 2.610])   # step bumper (proud) + flat tailgate
RS_R = pchip([.45, .60, .80, 1.00, 1.27], [.038, .036, .036, .038, .040])   # crisp bed / tailgate corners (no tub)
_YB = [BF, 1.30, 2.00, 2.40, YT]
BED_SHELL = dict(YN=BF, YT=YT, ZC=ZC_BED,
                 ZBELT=pchip(_YB, [1.262, 1.268, 1.270, 1.268, 1.245]), WBELT=pchip(_YB, [.920, .925, .930, .925, .905]), WMAX=pchip(_YB, [.940, .945, .950, .945, .925]),
                 ZSH=pchip(_YB, [.90, .90, .90, .90, .86]), ZFLOOR=pchip([BF, 2.20, 2.45, YT], [.520, .520, .48, .52]), WFLOOR=pchip(_YB, [.86, .87, .87, .86, .74]),
                 CAB=lambda y: 0.0, DECK_FADE=lambda y: 0.0, SK=lambda y: 0.0, HOOD_RIDGE=lambda y: 0.0, ROCKER_CREASE=lambda y: 0.0,
                 STAT=[round(v, 3) for v in np.linspace(1.28, 2.32, 7)],
                 END={'R': dict(sgn=1, ysec=2.45, Yc=YC_R, plan=.015, Rs=RS_R, Rt=.020, Rb=.050, d=(.12, .025), sc=(.982, .94, .84, .58, .24)),
                      'F': dict(sgn=-1, ysec=BF + .17, Yc=YC_BEDF, plan=.0, Rs=pchip([.50, 1.28], [.035, .035]), Rt=.022, Rb=.050, d=(.10, .025), sc=(.982, .94, .84, .56, .22))},
                 CREST=lambda y: .55 * ss(BF + .05, BF + .12, y) * (1 - ss(2.50, 2.60, y)), J3_F=(-BF - .25, -BF - .05), J3_R=(2.25, 2.55))
SHELLS = [{}, BED_SHELL]
# ---------------- openings, lamps, trim (global; rear items land on the bed / tailgate)
HL = lambda sx: rounded([(sx * .50, 1.150), (sx * .70, 1.158), (sx * .82, 1.162), (sx * .845, 1.150), (sx * .848, 1.065), (sx * .80, 1.050), (sx * .62, 1.055), (sx * .50, 1.065)], [.012, .03, .03, .012, .014, .02, .03, .012], 3)
GRILLE = rounded([(-.48, 1.150), (.48, 1.150), (.48, .860), (.42, .800), (-.42, .800), (-.48, .860)], [.03, .03, .04, .04, .04, .04], 3)   # big upright truck grille
LOWER = rounded([(-.55, .690), (.55, .690), (.50, .550), (-.50, .550)], [.03, .03, .03, .03], 3)
FOG = lambda sx: rounded([(sx * .64, .760), (sx * .78, .780), (sx * .80, .620), (sx * .68, .600)], .025, 2)
TL = lambda sx: rounded([(sx * .780, 1.200), (sx * .842, 1.200), (sx * .845, .880), (sx * .780, .880)], [.015, .02, .02, .015], 3)   # vertical truck lamps
PLATE_R = rounded([(-.26, .790), (.26, .790), (.26, .680), (-.26, .680)], .012, 3)                    # plate on the tailgate (step bumper below)
VALANCE = rounded([(-.75, .475), (.75, .475), (.72, .455), (-.72, .455)], .008, 3)
EXH = None
HANDLES = ((-.35, -.22), (.62, .75)); HANDLE_Z = 1.190
HOOD_LOOP = rounded([(.78, COWL - .03), (.86, -1.80), (.82, -2.52), (-.82, -2.52), (-.86, -1.80), (-.78, COWL - .03)], [.02, .3, .08, .08, .3, .02], 6)
FDOOR = lambda TOPZ: rounded([(-1.24, .50), (-.10, .50), (-.10, TOPZ(-.10)), (-1.18, TOPZ(-1.18))], [.04, .02, .01, .02], 5)
RDOOR = lambda TOPZ: rounded([(-.04, .50), (.90, .50), (.92, TOPZ(.92)), (-.04, TOPZ(-.04))], [.02, .03, .02, .01], 5)
FUEL = rounded([(1.25, .95), (1.40, .95), (1.40, 1.07), (1.25, 1.07)], .025, 4)
SWEEP_C = (0, 2.40); REAR_SHUT = [(2.10, .620), (2.30, .610), (2.48, .605)]; REAR_SHUT_Z = .605; REAR_SHUT_FACE_Y = 2.52
LID_SIDE = [('r', .74, 1.20), ('r', .74, .90), ('r', .74, .630)]                                          # tailgate: verticals + bottom edge
LID_MID = [('r', -.40, .628), ('r', 0.0, .628), ('r', .40, .628)]; LID_X = None
FSHUT_LAMP = (.854, 1.100); FSHUT_Z1 = 1.090; FSHUT_MID = [(-2.40, .950)]; FSHUT_ARC = 150
MIRROR_POS = (1.07, COWL + .16, ZBELT(COWL + .16) + .14); MIRROR_SIZE = (.24, .090, .140); MIRROR_BASE_Z = ZBELT(COWL + .16) + .025; MIRROR_DETECT = (1.00, 1.30)
FIN_Y0 = .45; CLADDING = True; UNDER_Y = 2.45
HL_CELLS = 3; HL_DRL_SEGS = 6; INTAKE_BLADES = (0.0,)
REVERSE = (.790, .835, .895, .930); REFLECTOR = (.60, .72, .645, .660); REPEATER = (-2.40, -2.33, 1.040, 1.055)   # reverse in the tail-lamp stack (bumper covers .455-.625)
LINER_XI = .62; GRILLE_STYLE = 'horizontal'; GRILLE_BARS = 3; GRILLE_BAR_MAT = 'TS_Atlas:dark_chrome'; CHIN_Z = .470; CHIN_W = .58
PLATE_F = (.585, .685); REAR_STRIP = None; VALANCE_TRIM = 'TS_Atlas:gloss_black'; BADGE_F = .990; BADGE_R = 1.000
TRAY = (.400, .86, -2.40, 2.40); HMSL = ('t', .20, CB - .065, CB - .055)
BPILLAR = (-.14, -.02); EXTRA_PILLARS = []; BELT_Y1 = .92; BELT_TRIM = 'TS_Atlas:gloss_black'
ROCKER = (.470, .050, 'TS_Atlas:plastic_dark'); ROOF_RAILS = None
SPOKES = dict(n=6, dish=.025, twin=0, curve=0.0, w0=.018, w1=.015); DISC_R = .170
INT = dict(drv=.40, dz=.30, half=.86, rows=[-.12, .62], dash=-.76, parcel=None, two_tone=False, dark=True)
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -1.40 and p.z < 1.30], 'Collision_Body': [p for p in pts if -1.60 < p.y < 1.20 and p.z < 1.25],
                         'Collision_Cabin': [p for p in pts if COWL - .05 < p.y < 1.05 and p.z > 1.15], 'Collision_Rear': [p for p in pts if p.y > 1.00 and p.z < 1.30]}
COM = (0, -.30, .75)
GH_TOP = (.040, .96); RW_COL = 10; GRILLE_FRAME = 'TS_Atlas:plastic_dark'
BED = (rounded([(-.83, 1.085), (.83, 1.085), (.83, 2.565), (-.83, 2.565)], .03, 3), .43)                 # open cargo bed: 1.66 x 1.48 m, 0.43 m deep; bedside top rails ~0.10 m
CAB_BACK_GLASS = (rounded([(-.52, 1.700), (.52, 1.700), (.56, 1.420), (-.56, 1.420)], .04, 3), CB + .018)   # rear window in the cab-back wall
CLAD_F = [rounded([(-.84, .530), (.84, .530), (.80, .450), (-.80, .450)], .02, 3)]                          # dark lower front bumper
CLAD_R = []
BUMPER_R = (.455, .625, .905, .075, 'TS_Atlas:dark_chrome')                                              # separate step bumper: z .455-.625, 7.5 cm proud
