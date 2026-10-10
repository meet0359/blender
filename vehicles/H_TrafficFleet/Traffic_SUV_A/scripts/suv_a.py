# Design: Traffic_SUV_A — compact crossover SUV (ORIGINAL fictional design).
# Class references (published, facts only): VW Tiguan ~4539 x 1842 x 1658, WB ~2679; Hyundai Tucson 4630 x 1865 x 1665, WB 2755, GC 181-192 (mm).
# Proportions: high hood leading edge (~1.0 m), upright face, raised ride (0.19 m), tall greenhouse with a flat roof to a roof spoiler, near-vertical
# liftgate glass, short rear overhang, dark wheel-arch + rocker cladding, roof rails, 18" wheels with tall sidewalls. Rugged-practical, not premium.
VEH = 'Traffic_SUV_A'; PRE = 'TS_SUVA'; CKP_ = 'trafficsuva'; COLL_NAME = 'TRAFFIC_SUV_A'; PAINT_RGB = (.30, .28, .24)   # review colour: warm grey metallic
DIM = dict(length=4.48, width_body=1.84, height=1.66, wheelbase=2.68, track_f=1.60, track_r=1.61, overhang_f=.92, overhang_r=.88, ground_clearance=.19, tire='235/60 R18 (R 0.370, rim 18")')
YF, YR = -1.32, 1.36; RW = .370; WT = .235; RIM = .2286; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.24, 2.24; COWL = -.90                                                                        # v2: FWD crossover dash-to-axle 0.42 m
ZC = pchip([YN, -2.15, -1.90, -1.50, -1.32, COWL, -.50, -.10, .30, 1.00, 1.60, 1.95, 2.10, 2.15, YT], [.80, .985, 1.020, 1.050, 1.060, 1.085, 1.360, 1.615, 1.650, 1.655, 1.645, 1.635, 1.230, 1.215, 1.150])
_YS = [YN, -2.10, -1.85, -1.32, COWL, 0, .90, 1.36, 1.75, 2.05, 2.15, YT]
ZBELT = pchip(_YS, [.95, .990, 1.030, 1.060, 1.080, 1.100, 1.120, 1.140, 1.150, 1.140, 1.120, 1.080])
WBELT = pchip(_YS, [.82, .860, .875, .880, .875, .870, .870, .875, .875, .860, .840, .800])
WMAX = pchip(_YS, [.86, .895, .915, .920, .915, .912, .912, .920, .920, .905, .890, .860])            # 1.84 m body
ZSH = pchip([YN, YF, 0, YR, YT], [.62, .74, .78, .78, .72])
ZFLOOR = pchip([YN, -2.05, -1.85, 1.80, 2.02, YT], [.40, .30, .205, .205, .30, .40])
WFLOOR = pchip([YN, -2.0, 0, 2.0, YT], [.66, .82, .86, .82, .68])
CAB = lambda y: ss(COWL - .14, COWL + .06, y) * (1 - ss(2.10, 2.20, y))
ROOFW = pchip([COWL, -.30, .30, 1.00, 1.60, 2.00], [.740, .715, .705, .700, .690, .660]); ROOF_END = 2.00
DECK_FADE = lambda y: ss(2.00, 2.20, y)
SK = lambda y: .015 * ss(-.90, -.70, y) * (1 - ss(.90, 1.10, y))
HOOD_RIDGE = lambda y: E_('TS_HOODRIDGE', .006) * ss(-2.00, -1.85, y) * (1 - ss(COWL - .25, COWL - .05, y))
STAT = [round(v, 3) for v in np.linspace(-1.80, 1.90, 19)]
YC_F = pchip([.30, .38, .48, .60, .72, .82, .90, .96, 1.00], [-2.08, -2.17, -2.215, -2.235, -2.24, -2.235, -2.22, -2.195, -2.165])
YC_R = pchip([.30, .38, .48, .60, .70, .76, .82, .95, 1.08, 1.18, 1.22], [2.12, 2.19, 2.225, 2.24, 2.238, 2.23, 2.215, 2.215, 2.21, 2.195, 2.17])
RS_F = pchip([.30, .45, .60, .75, .90, 1.00], [.075, .078, .085, .095, .105, .110])
RS_R = pchip([.30, .48, .66, .82, 1.00, 1.20], [.075, .078, .085, .090, .095, .100])
END = {'R': dict(sgn=1, ysec=2.10, Yc=YC_R, plan=.05, Rs=RS_R, Rt=.035, Rb=.075, d=(.12, .025), sc=(.982, .94, .84, .58, .24)),
       'F': dict(sgn=-1, ysec=-2.05, Yc=YC_F, plan=.10, Rs=RS_F, Rt=.030, Rb=.070, d=(.12, .025), sc=(.982, .94, .84, .56, .22))}
GLASS_WS = (COWL + .02, -.06); GLASS_RW = (1.97, 2.09); GLASS_SIDE = (COWL + .08, 1.82); SEAL_Y = (COWL + .04, 1.86); RAIL_Y = (COWL, 1.98)
CREST = lambda y: .60 * ss(-2.40, -2.30, y) * (1 - ss(2.10, 2.20, y))
J3_F = (1.80, 2.15); J3_R = (1.84, 2.16)
ROCKER_CREASE = lambda y: .45 * ss(-.90, -.70, y) * (1 - ss(.90, 1.10, y))
HL = lambda sx: rounded([(sx * .44, .905), (sx * .62, .915), (sx * .78, .935), (sx * .835, .950), (sx * .842, .905), (sx * .80, .865), (sx * .62, .855), (sx * .46, .865)], [.010, .03, .03, .012, .014, .02, .03, .010], 3)
GRILLE = rounded([(-.42, .880), (.42, .880), (.46, .720), (.38, .580), (-.38, .580), (-.46, .720)], [.03, .03, .04, .05, .05, .04], 3)   # wide hexagonal grille
LOWER = rounded([(-.50, .500), (.50, .500), (.46, .360), (-.46, .360)], [.04, .04, .04, .04], 3)
FOG = lambda sx: rounded([(sx * .62, .560), (sx * .74, .580), (sx * .76, .400), (sx * .66, .370)], .025, 2)
TL = lambda sx: rounded([(sx * .50, 1.100), (sx * .74, 1.130), (sx * .835, 1.110), (sx * .842, 1.000), (sx * .80, .950), (sx * .62, 1.020), (sx * .50, 1.040)], [.010, .02, .02, .016, .02, .02, .012], 3)   # L-shaped corner lamps
PLATE_R = rounded([(-.26, .970), (.26, .970), (.26, .860), (-.26, .860)], .014, 3)
VALANCE = rounded([(-.72, .440), (.72, .440), (.66, .310), (-.66, .310)], .02, 3)
EXH = None
HANDLES = ((-.10, .03), (1.00, 1.12)); HANDLE_Z = 1.035
HOOD_LOOP = rounded([(.70, COWL - .03), (.78, -1.40), (.74, -2.08), (-.74, -2.08), (-.78, -1.40), (-.70, COWL - .03)], [.02, .25, .07, .07, .25, .02], 6)
FDOOR = lambda TOPZ: rounded([(-.84, .42), (.20, .42), (.20, TOPZ(.20)), (-.78, TOPZ(-.78))], [.04, .02, .01, .02], 5)
RDOOR = lambda TOPZ: rounded([(.26, .42), (.86, .42), (.882, .450), (.944, .624), (1.085, .777), (1.62, TOPZ(1.62)), (.26, TOPZ(.26))], [.02, .03, .03, .06, .06, .02, .01], 5)
FUEL = rounded([(1.70, .98), (1.84, .98), (1.84, 1.10), (1.70, 1.10)], .025, 4)
SWEEP_C = (0, 1.92); REAR_SHUT = [(1.85, .720), (2.00, .750), (2.12, .765)]; REAR_SHUT_Z = .765; REAR_SHUT_FACE_Y = 2.16
LID_SIDE = [('r', .66, .770), ('r', .66, .90), ('r', .665, 1.05), ('r', .67, 1.17), ('t', .68, 2.08), ('t', .69, 2.02), ('t', .68, 1.96)]   # liftgate
LID_MID = [('t', -.40, 1.935), ('t', -.13, 1.935), ('t', .13, 1.935), ('t', .40, 1.935)]; LID_X = .66
FSHUT_LAMP = (.848, .900); FSHUT_Z1 = .890; FSHUT_MID = [(-1.85, .800)]; FSHUT_ARC = 150
MIRROR_POS = (.99, COWL + .14, ZBELT(COWL + .14) + .11); MIRROR_SIZE = (.21, .080, .110); MIRROR_BASE_Z = ZBELT(COWL + .14) + .025; MIRROR_DETECT = (.94, 1.08)
FIN_Y0 = 1.50; CLADDING = True; UNDER_Y = 1.85
HL_CELLS = 3; HL_DRL_SEGS = 6; INTAKE_BLADES = (0.0,)
REVERSE = (.40, .52, .640, .660); REFLECTOR = (.66, .78, .500, .520); REPEATER = (-1.98, -1.92, .860, .876)
LINER_XI = .58; GRILLE_STYLE = 'horizontal'; GRILLE_BARS = 4; GRILLE_BAR_MAT = 'TS_Atlas:dark_chrome'; CHIN_Z = .330; CHIN_W = .55
PLATE_F = (.385, .495); REAR_STRIP = None; VALANCE_TRIM = 'TS_Atlas:alu_brushed'; BADGE_F = .730; BADGE_R = 1.050
TRAY = (.215, .80, -1.85, 1.85); HMSL = ('t', .22, 1.930, 1.945)
BPILLAR = (.17, .29); EXTRA_PILLARS = [(1.60, 1.68)]; BELT_Y1 = 1.80; BELT_TRIM = 'TS_Atlas:gloss_black'
ROCKER = (.330, .090, 'TS_Atlas:plastic_dark'); ROOF_RAILS = (-.45, 1.65, .10, .045)          # (y0, y1, inset from the roof edge, height)
SPOKES = dict(n=10, dish=.020, twin=.35, curve=0.0, w0=.014, w1=.011); DISC_R = .165
INT = dict(drv=.38, dz=.16, half=.82, rows=[-.04, .92], dash=-.64, parcel=None, two_tone=False, dark=True)
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -1.15 and p.z < 1.15], 'Collision_Body': [p for p in pts if -1.30 < p.y < 1.20 and p.z < 1.12],
                         'Collision_Cabin': [p for p in pts if COWL - .05 < p.y < 2.05 and p.z > 1.05], 'Collision_Rear': [p for p in pts if p.y > .95 and p.z < 1.25]}
COM = (0, -.12, .62)
GH_TOP = (.045, .95); RW_COL = 10; GRILLE_FRAME = 'TS_Atlas:gloss_black'                                   # v2: taller DLO, wide liftgate glass, black grille frame (own identity)
