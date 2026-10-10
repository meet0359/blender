# Design: Traffic_Box_Truck_A — medium-duty cab-over box truck (ORIGINAL fictional design). CLASS 'box_truck' (ts_vehicle_v2.py, two shells).
# Class references (published facts only): Isuzu NPR-HD / Hino 155 / Fuso Canter class with a 16 ft box: ~6.8-7.2 m long, cab ~2.0 m wide, box ~2.3-2.4 m,
# ~3.3-3.4 m high, wheelbase ~3.8 m, 19.5" wheels. No manufacturer design copied.
# Shell 0 = cab-over cab: flat raked face carrying the windshield (FACE_GLASS), doors above the front wheel, flat roof, flat cab-back wall.
# Shell 1 = separate cargo box: flat front wall, crisp box edges, flat rear doors (centre split), box floor at 0.95 m above exposed chassis rails.
# Blockout limitations: single rear tires (builder has 4 wheels; real trucks run duals), no mud flaps.
CLASS = 'box_truck'; VEH = 'Traffic_Box_Truck_A'; PRE = 'TS_BoxTruckA'; CKP_ = 'trafficboxtrucka'; COLL_NAME = 'TRAFFIC_BOX_TRUCK_A'; PAINT_RGB = (.62, .62, .60)   # review colour: fleet white
DIM = dict(length=6.90, width_body=2.00, height=3.25, wheelbase=3.85, track_f=1.68, track_r=1.68, overhang_f=1.15, overhang_r=1.90, ground_clearance=.22, tire='225/70 R19.5 (R 0.405, rim 19.5")', box_width=2.34)
YF, YR = -2.30, 1.55; RW = .405; WT = .225; RIM = .2477; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -3.45, 3.45; COWL = -3.30; CB = -1.50; BF = -1.42                                               # CB: cab-back wall, BF: box front wall (80 mm gap)
# ---------------- shell 0: cab-over cab (also the global curves for doors, belt trim, mirrors, interior)
ZC_C = pchip([YN, -3.30, -2.90, -2.00, CB], [2.30, 2.36, 2.38, 2.38, 2.375])
_YC = [YN, -3.20, -2.60, -2.00, CB]
ZBELT_C = pchip(_YC, [1.58, 1.62, 1.62, 1.62, 1.62]); WBELT_C = pchip(_YC, [.960, .975, .975, .975, .975]); WMAX_C = pchip(_YC, [.985, 1.000, 1.000, 1.000, 1.000])
ZSH_C = pchip(_YC, [.95, .95, .95, .95, .95]); ZFLOOR_C = pchip(_YC, [.62, .60, .60, .60, .60]); WFLOOR_C = pchip(_YC, [.92, .95, .95, .95, .95])
ZC = lambda y: ZC_C(y) if y < (CB + BF) / 2 else 3.250
ZBELT = lambda y: ZBELT_C(y) if y < (CB + BF) / 2 else 3.24
WBELT = lambda y: WBELT_C(y) if y < (CB + BF) / 2 else 1.17
WMAX = lambda y: WMAX_C(y) if y < (CB + BF) / 2 else 1.02                                                 # rear: mudguard width for the arch liner
ZSH = lambda y: ZSH_C(y) if y < (CB + BF) / 2 else 1.00
ZFLOOR = lambda y: ZFLOOR_C(y) if y < (CB + BF) / 2 else .95
WFLOOR = lambda y: WFLOOR_C(y) if y < (CB + BF) / 2 else 1.10
CAB = lambda y: 1 - ss(CB + .03, CB + .06, y)                                                             # greenhouse over the whole cab
ROOFW = pchip([COWL, -2.60, CB], [.935, .935, .935]); ROOF_END = CB - .05                                # upright cab glass
DECK_FADE = lambda y: 0.0; SK = lambda y: 0.0; HOOD_RIDGE = lambda y: 0.0
STAT = [round(v, 3) for v in np.linspace(-2.74, -1.78, 7)]   # first station behind the raked-face blend ring (-2.86 folded)
YC_F = pchip([.40, .55, .75, .90, 1.30, 1.55, 1.90, 2.20, 2.32, 2.38], [-3.40, -3.45, -3.45, -3.43, -3.42, -3.40, -3.34, -3.27, -3.22, -3.18])   # bumper, grille, raked windshield face
RS_F = pchip([.40, 1.0, 1.6, 2.38], [.080, .090, .110, .120])
YC_CB = pchip([.55, 1.50, 2.40], [CB, CB, CB - .005]); RS_CB = pchip([.55, 2.40], [.045, .045])
END = {'F': dict(sgn=-1, ysec=-2.92, Yc=YC_F, plan=.05, Rs=RS_F, Rt=.090, Rb=.060, d=(.12, .025), sc=(.982, .94, .84, .56, .22)),
       'R': dict(sgn=1, ysec=CB - .20, Yc=YC_CB, plan=.0, Rs=RS_CB, Rt=.045, Rb=.045, d=(.10, .025), sc=(.982, .94, .84, .58, .24))}
GLASS_WS = (9.0, 9.0); GLASS_RW = (9.0, 9.0); GLASS_SIDE = (-2.88, -1.78); SEAL_Y = (-2.90, -1.76); RAIL_Y = (COWL, CB - .08)
CREST = lambda y: .50; J3_F = (2.95, 3.30); J3_R = (CB - .25, CB - .05); ROCKER_CREASE = lambda y: 0.0
# ---------------- shell 1: cargo box
_YB = [BF, 0.0, 2.0, YT]
BOX_SHELL = dict(ZC=lambda y: 3.250, ZBELT=lambda y: 3.245,   # flat box roof (5 mm crown: LOD planar dissolve keeps the height)
                  WBELT=lambda y: 1.17, WMAX=lambda y: 1.17, ZSH=lambda y: 1.00, ZFLOOR=lambda y: .95, WFLOOR=lambda y: 1.10,
                 CAB=lambda y: 0.0, CREST=lambda y: .95, ROCKER_CREASE=lambda y: 0.0, STAT=[round(v, 3) for v in np.linspace(-1.05, 3.05, 12)],
                 END={'F': dict(ngon=True, sgn=-1, ysec=BF + .22, Yc=pchip([.95, 2.0, 3.28], [BF, BF, BF]), plan=.0, Rs=pchip([.95, 3.28], [.035, .035]), Rt=.035, Rb=.035, d=(.12, .025), sc=(.982, .94, .84, .56, .22)),
                      'R': dict(ngon=True, sgn=1, ysec=YT - .22, Yc=pchip([.95, 2.0, 3.28], [YT, YT, YT]), plan=.0, Rs=pchip([.95, 3.28], [.035, .035]), Rt=.035, Rb=.035, d=(.12, .025), sc=(.982, .94, .84, .58, .24))},
                 J3_F=(-BF - .30, -BF - .05), J3_R=(3.05, 3.40))
SHELLS = [{}, BOX_SHELL]
# ---------------- face, lamps, doors, trim
FACE_GLASS = [('F', rounded([(-.90, 2.200), (.90, 2.200), (.92, 1.560), (-.92, 1.560)], [.10, .10, .06, .06], 4), 'TS_Glass')]   # windshield in the raked face
HL = lambda sx: rounded([(sx * .60, 1.200), (sx * .82, 1.200), (sx * .84, .990), (sx * .60, .990)], [.03, .04, .04, .03], 3)
GRILLE = rounded([(-.54, 1.520), (.54, 1.520), (.54, 1.000), (-.54, 1.000)], [.04, .04, .04, .04], 3)    # production: tall cab-over grille panel up to the windshield base (covers the face-centre cap pinch at z ~1.5)
LOWER = rounded([(-.55, .790), (.55, .790), (.52, .680), (-.52, .680)], [.03, .03, .03, .03], 3)   # bumper zone: the cab underside is at .60
FOG = lambda sx: rounded([(sx * .66, .790), (sx * .80, .790), (sx * .80, .700), (sx * .66, .700)], .02, 2)
TL = lambda sx: rounded([(sx * .90, 1.340), (sx * 1.08, 1.340), (sx * 1.08, 1.060), (sx * .90, 1.060)], [.015, .02, .02, .015], 3)   # tall lamps on the box rear corners
PLATE_R = rounded([(-.26, 1.150), (.26, 1.150), (.26, 1.040), (-.26, 1.040)], .012, 3)
VALANCE = rounded([(-1.04, 1.012), (1.04, 1.012), (1.04, .992), (-1.04, .992)], .006, 2)               # rear sill rail recess
EXH = None
HANDLES = ((-2.24, -2.12),); HANDLE_Z = 1.420
HOOD_LOOP = None
FDOOR = lambda TOPZ: rounded([(-2.86, .97), (-2.04, .97), (-2.04, TOPZ(-2.04)), (-2.84, TOPZ(-2.84))], [.04, .03, .01, .02], 5)   # door above the front wheel
RDOOR = None
FUEL = None
SWEEP_C = (0, 3.0); REAR_SHUT = None; REAR_SHUT_Z = None; REAR_SHUT_FACE_Y = None
LID_SIDE = [('r', 1.08, 1.025), ('r', 1.08, 2.10), ('r', 1.08, 3.165)]                                 # rear doors: outline
LID_MID = [('r', -.60, 3.165), ('r', 0.0, 3.165), ('r', .60, 3.165)]; LID_X = None
EXTRA_GROOVES = [[('r', 0.0, 1.025), ('r', 0.0, 2.10), ('r', 0.0, 3.165)]] + \
                [[(s_, y, 1.03), (s_, y, 2.10), (s_, y, 3.17)] for s_ in ('sL', 'sR') for y in (-.25, .95, 2.15)]   # door centre split + box side panel seams
FSHUT_LAMP = None; FSHUT_Z1 = None; FSHUT_MID = []; FSHUT_ARC = 150
MIRROR_POS = (1.20, -3.02, 1.95); MIRROR_SIZE = (.10, .070, .300); MIRROR_BASE_Z = 1.78; MIRROR_DETECT = (1.10, 1.70)
FIN_Y0 = None; CLADDING = True; UNDER_Y = 2.0
HL_CELLS = 2; HL_DRL_SEGS = 4; INTAKE_BLADES = (0.0,)
REVERSE = (.70, .84, 1.090, 1.130); REFLECTOR = (.92, 1.06, 1.000, 1.020); REPEATER = (-3.00, -2.94, 1.100, 1.125)
LINER_XI = .70; GRILLE_STYLE = 'horizontal'; GRILLE_BARS = 6; GRILLE_BAR_MAT = 'TS_Atlas:dark_chrome'; CHIN_Z = .650; CHIN_W = .80
PLATE_F = (.840, .940); REAR_STRIP = None; VALANCE_TRIM = 'TS_Atlas:gloss_black'; BADGE_F = 1.300; BADGE_R = 2.40
TRAY = (.600, .90, -3.20, -1.60); HMSL = ('r', .25, 3.100, 3.130)
BPILLAR = (-2.12, -2.04); EXTRA_PILLARS = []; BELT_Y1 = -1.85; BELT_TRIM = 'TS_Atlas:gloss_black'
ROCKER = None; ROOF_RAILS = None
SPOKES = dict(n=8, dish=.060, twin=0, curve=0.0, w0=.026, w1=.072); DISC_R = .200                       # steel wheel: spokes widen to the rim -> 8 small hand holes (production r2; .030 read as a car alloy)
INT = dict(drv=.50, dz=.62, half=.95, rows=[-2.62], dash=-3.12, parcel=None, two_tone=False, dark=True)
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -2.6], 'Collision_Body': [p for p in pts if -2.8 < p.y < -1.4 and p.z < 1.6],
                         'Collision_Cabin': [p for p in pts if -3.3 < p.y < -1.5 and p.z > 1.5], 'Collision_Rear': [p for p in pts if p.y > -1.45]}
COM = (0, -.40, 1.10)
GH_TOP = (.060, .95); RW_COL = 10; GRILLE_FRAME = 'TS_Atlas:plastic_dark'
FRAME = (-1.55, 3.30, .62, .82, .42)                                                                    # exposed chassis rails under the box
BOXES = [((0, 3.36, .56), (1.02, .045, .065), 'TS_Atlas:dark_chrome')] + \
        [((sx * .70, 3.30, .76), (.035, .035, .19), 'TS_Atlas:underbody') for sx in (1, -1)] + \
        [((sx * 1.06, .05, .76), (.015, 1.10, .075), 'TS_Atlas:wheel_silver') for sx in (1, -1)] + \
        [((-.82, -.95, .70), (.20, .42, .17), 'TS_Atlas:wheel_silver')] + \
        [((sx * .96, -2.45, .64), (.08, .24, .018), 'TS_Atlas:plastic_dark') for sx in (1, -1)]           # underride bar + uprights, side guards, fuel tank, cab steps
# ---------------- production detail (approved blockout -> detailed production)
DUAL_REAR = .030                                                                                        # dual rear tires, 30 mm gap (same pivot / WheelColliderRef)
LINER_XI = .50                                                                                          # rear mudguard liner spans both tires
GRILLE_FRAME = 'TS_Atlas:chrome'
FACE_WIPERS = (1.585, [(-.82, -.10, 1.80), (.06, .78, 1.80)])                                           # two wiper arms on the windshield base
_HZ = (1.30, 2.10, 2.90)
FACE_PARTS = [('R', 'box', sx * 1.095, z, (.035, .018, .055), 'TS_Atlas:dark_chrome') for sx in (1, -1) for z in _HZ] + \
             [('R', 'rod', x, 1.06, 3.10, .013, 'TS_Atlas:wheel_silver') for x in (-.80, -.32, .32, .80)] + \
             [('R', 'box', x + (.06 if x > 0 else -.06), 1.60, (.060, .016, .012), 'TS_Atlas:dark_chrome') for x in (-.80, -.32, .32, .80)] + \
             [('R', 'box', x, z, (.030, .014, .020), 'TS_Atlas:dark_chrome') for x in (-.80, -.32, .32, .80) for z in (1.05, 3.11)] + \
             [('R', 'box', sx * 1.135, 2.10, (.028, .015, 1.10), 'TS_Atlas:wheel_silver') for sx in (1, -1)] + \
             [('R', 'box', 0.0, 1.000, (1.10, .015, .030), 'TS_Atlas:wheel_silver'), ('R', 'box', 0.0, 3.205, (1.10, .015, .025), 'TS_Atlas:wheel_silver')]   # hinges, locking bars + handles + keepers, corner posts, sill / header
BOXES += [((0, -3.505, .560), (1.000, .060, .090), 'TS_Atlas:dark_chrome'), ((0, -3.470, .655), (.960, .030, .012), 'TS_Atlas:plastic_dark')]   # front bumper bar + step
BOXES += [((sx * .42, y, .58), (.040, .52, .030), 'TS_Atlas:underbody') for sx in (1, -1) for y in (YF, YR)] + \
         [((0, y, RW), (.70 if y == YR else .74, .055, .055), 'TS_Atlas:underbody') for y in (YF, YR)]   # leaf springs + axle beams
BOXES += [((sx * .80, YR + .62, .40), (.17, .008, .22), 'TS_Atlas:plastic_black') for sx in (1, -1)]    # rear mud flaps
LOD_KEEP_LARGE_TRIM = .30                                                                               # structural trim kept whole at every LOD (chassis / guards / bumpers / posts)
LOD_BODY_MODE = 'planar'                                                                               # boxy commercial body: planar LOD dissolve (flat panels stay whole)
LOD_PLANAR_DEG = {1: 3.0, 2: 9.0, 3: 24.0}                                                             # stronger planar dissolve at distance (flat panels stay exact)
LOD_RK = {1: dict(Trim=.28, Interior=.32), 2: dict(Trim=.10, Interior=.12), 3: dict(Trim=.04, Interior=.08)}
LOD_PLANAR_COLLAPSE = {3: .55}
# production r2 (2026-10-09): alu_brushed -> wheel_silver on long trims (brushed normal pattern magnified into dents); FIN_Y0 None (car shark-fin removed)
# FLAT_PLANAR removed (r4): it did not fix the rear 'cracks' (the n-gon end cap did) and its custom normals tore the LOD1-3 bodies (S1 3.0 %)
# production r3: box ends closed by a planar n-gon (END ngon=True) - the quad bridge folded at the inner ring's top corners (rear-door 'cracks', inverted skin faces at x +-0.28, z 2.35)
