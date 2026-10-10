# Design: Traffic_SUV_B — premium large family SUV, three-row (ORIGINAL fictional design; not a stretched SUV A).
# Class references (published, facts only): Volvo XC90 ~4950 x 1958 x 1776, WB 2984; BMW X5 G05 ~4935 x 2004 x 1753, WB ~2934; Genesis GV80 ~4940 x 1975 x 1715, WB ~2954 (mm).
# Proportions: long premium hood with a high, flat leading edge, longitudinal-engine dash-to-axle (0.80 m), long flat roof over three rows, near-vertical
# liftgate glass, wide stable stance (1.96 m, 21" wheels, wide tracks), strong crisp shoulder, chrome DLO, tall vertical-vane grille, slim twin lamps,
# connected tail strip, twin exhaust finishers, flush roof rails, body-colour arches (premium, no cladding).
VEH = 'Traffic_SUV_B'; PRE = 'TS_SUVB'; CKP_ = 'trafficsuvb'; COLL_NAME = 'TRAFFIC_SUV_B'; PAINT_RGB = (.62, .62, .60)   # review colour: pearl white
DIM = dict(length=4.98, width_body=1.96, height=1.76, wheelbase=2.98, track_f=1.68, track_r=1.69, overhang_f=.94, overhang_r=1.06, ground_clearance=.21, tire='275/45 R21 (R 0.391, rim 21")')
YF, YR = -1.55, 1.43; RW = .391; WT = .275; RIM = .2667; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -2.49, 2.49; COWL = -.75
ZC = pchip([YN, -2.40, -2.15, -1.80, -1.55, -1.10, COWL, -.35, .10, .45, 1.20, 1.90, 2.18, 2.34, 2.40, YT], [.86, 1.060, 1.100, 1.130, 1.145, 1.165, 1.190, 1.470, 1.730, 1.755, 1.760, 1.750, 1.735, 1.300, 1.270, 1.200])
_YS = [YN, -2.35, -2.05, -1.55, COWL, 0, .90, 1.43, 1.95, 2.25, 2.38, YT]
ZBELT = pchip(_YS, [1.02, 1.100, 1.140, 1.160, 1.180, 1.195, 1.210, 1.220, 1.230, 1.220, 1.200, 1.140])
WBELT = pchip(_YS, [.86, .900, .925, .935, .930, .925, .925, .930, .932, .920, .900, .860])
WMAX = pchip(_YS, [.90, .945, .970, .980, .972, .970, .970, .978, .980, .965, .945, .900])            # 1.96 m body
ZSH = pchip([YN, YF, 0, YR, YT], [.66, .80, .84, .85, .78])
ZFLOOR = pchip([YN, -2.28, -2.08, 1.95, 2.25, YT], [.44, .33, .225, .225, .33, .44])
WFLOOR = pchip([YN, -2.2, 0, 2.2, YT], [.70, .86, .90, .86, .72])
CAB = lambda y: ss(COWL - .14, COWL + .06, y) * (1 - ss(2.32, 2.42, y))
ROOFW = pchip([COWL, -.30, .30, 1.20, 1.90, 2.25], [.780, .755, .745, .740, .725, .690]); ROOF_END = 2.25
DECK_FADE = lambda y: ss(2.25, 2.45, y)
SK = lambda y: .020 * ss(-1.00, -.80, y) * (1 - ss(1.00, 1.20, y))
HOOD_RIDGE = lambda y: E_('TS_HOODRIDGE', .008) * ss(-2.25, -2.10, y) * (1 - ss(COWL - .30, COWL - .06, y))
STAT = [round(v, 3) for v in np.linspace(-2.02, 2.10, 21)]
YC_F = pchip([.34, .42, .52, .64, .76, .88, .98, 1.04, 1.08], [-2.33, -2.42, -2.465, -2.485, -2.49, -2.485, -2.47, -2.45, -2.425])
YC_R = pchip([.36, .44, .54, .66, .78, .84, .90, 1.02, 1.16, 1.26, 1.30], [2.36, 2.43, 2.465, 2.485, 2.483, 2.475, 2.455, 2.455, 2.45, 2.43, 2.40])
RS_F = pchip([.34, .50, .65, .80, .95, 1.08], [.080, .085, .090, .100, .110, .115])
RS_R = pchip([.36, .54, .72, .90, 1.10, 1.30], [.080, .085, .090, .095, .100, .105])
END = {'R': dict(sgn=1, ysec=2.32, Yc=YC_R, plan=.05, Rs=RS_R, Rt=.030, Rb=.080, d=(.12, .025), sc=(.982, .94, .84, .58, .24)),
       'F': dict(sgn=-1, ysec=-2.28, Yc=YC_F, plan=.08, Rs=RS_F, Rt=.028, Rb=.075, d=(.12, .025), sc=(.982, .94, .84, .56, .22))}
GLASS_WS = (COWL + .02, .08); GLASS_RW = (2.20, 2.33); GLASS_SIDE = (COWL + .08, 2.10); SEAL_Y = (COWL + .04, 2.14); RAIL_Y = (COWL, 2.22)
CREST = lambda y: .80 * ss(-2.65, -2.55, y) * (1 - ss(2.36, 2.46, y))
J3_F = (2.02, 2.40); J3_R = (2.05, 2.42)
ROCKER_CREASE = lambda y: .55 * ss(-1.00, -.80, y) * (1 - ss(1.00, 1.20, y))
HL = lambda sx: rounded([(sx * .50, 1.005), (sx * .68, 1.015), (sx * .82, 1.035), (sx * .875, 1.048), (sx * .882, 1.005), (sx * .84, .965), (sx * .68, .955), (sx * .52, .965)], [.010, .03, .03, .012, .014, .02, .03, .010], 3)
GRILLE = rounded([(-.46, .985), (.46, .985), (.46, .660), (.40, .600), (-.40, .600), (-.46, .660)], [.035, .035, .04, .05, .05, .04], 3)   # tall premium grille
LOWER = rounded([(-.58, .520), (.58, .520), (.52, .380), (-.52, .380)], [.04, .04, .05, .05], 3)
FOG = lambda sx: rounded([(sx * .68, .620), (sx * .80, .640), (sx * .83, .420), (sx * .72, .390)], .025, 2)
TL = lambda sx: rounded([(sx * .52, 1.170), (sx * .78, 1.185), (sx * .875, 1.170), (sx * .882, 1.080), (sx * .82, 1.050), (sx * .54, 1.100)], [.010, .02, .02, .016, .02, .012], 3)
PLATE_R = rounded([(-.27, 1.000), (.27, 1.000), (.27, .890), (-.27, .890)], .014, 3)
VALANCE = rounded([(-.80, .500), (.80, .500), (.74, .370), (-.74, .370)], .02, 3)
EXH = lambda sx: rounded([(sx * .48, .470), (sx * .70, .470), (sx * .68, .400), (sx * .50, .400)], .02, 3)
HANDLES = ((-.08, .06), (1.10, 1.24)); HANDLE_Z = 1.135
HOOD_LOOP = rounded([(.76, COWL - .03), (.84, -1.50), (.80, -2.36), (-.80, -2.36), (-.84, -1.50), (-.76, COWL - .03)], [.02, .3, .08, .08, .3, .02], 6)
FDOOR = lambda TOPZ: rounded([(-1.05, .46), (.33, .46), (.33, TOPZ(.33)), (-.99, TOPZ(-.99))], [.04, .02, .01, .02], 5)
RDOOR = lambda TOPZ: rounded([(.39, .46), (.91, .46), (.932, .470), (.997, .655), (1.143, .815), (1.62, TOPZ(1.62)), (.39, TOPZ(.39))], [.02, .03, .03, .06, .06, .02, .01], 5)
FUEL = rounded([(1.80, 1.03), (1.96, 1.03), (1.96, 1.16), (1.80, 1.16)], .025, 4)
SWEEP_C = (0, 2.15); REAR_SHUT = [(1.98, .820), (2.18, .860), (2.34, .880)]; REAR_SHUT_Z = .885; REAR_SHUT_FACE_Y = 2.38
LID_SIDE = [('r', .70, .890), ('r', .70, 1.02), ('r', .705, 1.15), ('r', .71, 1.26), ('t', .72, 2.32), ('t', .73, 2.26), ('t', .72, 2.20)]
LID_MID = [('t', -.42, 2.17), ('t', -.14, 2.17), ('t', .14, 2.17), ('t', .42, 2.17)]; LID_X = .70
FSHUT_LAMP = (.888, .995); FSHUT_Z1 = .980; FSHUT_MID = [(-2.12, .880)]; FSHUT_ARC = 150
MIRROR_POS = (1.04, COWL + .14, ZBELT(COWL + .14) + .12); MIRROR_SIZE = (.22, .085, .115); MIRROR_BASE_Z = ZBELT(COWL + .14) + .025; MIRROR_DETECT = (1.00, 1.22)
FIN_Y0 = 1.80; CLADDING = False; UNDER_Y = 2.10
HL_CELLS = 5; HL_DRL_SEGS = 8; INTAKE_BLADES = (-.02, .02)
REVERSE = (.44, .58, .700, .720); REFLECTOR = (.70, .82, .560, .580); REPEATER = (-2.20, -2.13, .980, .995)
LINER_XI = .62; GRILLE_STYLE = 'vertical'; GRILLE_BARS = 13; GRILLE_BAR_MAT = 'TS_Atlas:chrome'; CHIN_Z = .360; CHIN_W = .70
PLATE_F = (.470, .580); REAR_STRIP = (1.115, .50); VALANCE_TRIM = 'TS_Atlas:alu_brushed'; BADGE_F = .800; BADGE_R = 1.050
TRAY = (.235, .86, -2.10, 2.15); HMSL = ('t', .24, 2.160, 2.175)
BPILLAR = (.33, .43); EXTRA_PILLARS = [(1.64, 1.72)]; BELT_Y1 = 2.08; BELT_TRIM = 'TS_Atlas:alu_brushed'
ROCKER = (.380, .030, 'TS_Atlas:dark_chrome'); ROOF_RAILS = (-.40, 1.95, .10, .040)          # (y0, y1, inset from the roof edge, height)
SPOKES = dict(n=12, dish=.030, twin=0, curve=.06, w0=.010, w1=.007); DISC_R = .190
INT = dict(drv=.40, dz=.20, half=.88, rows=[.15, 1.02, 1.80], dash=-.48, parcel=None, two_tone=True)
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -1.30 and p.z < 1.25], 'Collision_Body': [p for p in pts if -1.50 < p.y < 1.30 and p.z < 1.24],
                         'Collision_Cabin': [p for p in pts if COWL - .05 < p.y < 2.35 and p.z > 1.15], 'Collision_Rear': [p for p in pts if p.y > 1.10 and p.z < 1.35]}
COM = (0, -.10, .70)
GH_TOP = (.045, .95); RW_COL = 10                                                                      # v2: taller DLO, wide liftgate glass
