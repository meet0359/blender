# Design: Traffic_Bus_A — 12 m low-floor city bus (ORIGINAL fictional design). CLASS 'bus' (ts_vehicle_v2.py, one long box loft).
# Class references (published facts only): 12 m low-floor city buses (Citaro / Lion's City / 7900 class): ~12.0-12.2 m long, 2.55 m wide,
# ~3.0-3.3 m high incl. roof equipment, wheelbase ~5.9-6.0 m, 275/70 R22.5 tires. No manufacturer design copied.
# Construction: near-vertical sides, flat roof with rounded drip rail, tall flush-pillared window band, windshield and rear window IN the end faces,
# destination display, glass doors (front + middle) on the curb side (right side, x < 0: right-hand traffic), rear engine hatch, roof HVAC pod.
# Blockout limitations: single rear tires (real buses run duals), door glass is a surface panel (no door opening / steps modelled).
CLASS = 'bus'; VEH = 'Traffic_Bus_A'; PRE = 'TS_BusA'; CKP_ = 'trafficbusa'; COLL_NAME = 'TRAFFIC_BUS_A'; PAINT_RGB = (.50, .30, .04)   # review colour: transit amber
DIM = dict(length=12.0, width_body=2.55, height=2.95, wheelbase=6.0, track_f=2.10, track_r=1.90, overhang_f=2.70, overhang_r=3.30, ground_clearance=.32, tire='275/70 R22.5 (R 0.478, rim 22.5")', height_incl_hvac=3.21)
YF, YR = -3.30, 2.70; RW = .478; WT = .275; RIM = .2858; XF, XR = DIM['track_f'] / 2, DIM['track_r'] / 2
YN, YT = -6.0, 6.0; COWL = -5.75
_Y = [YN, -5.5, 0.0, 5.5, YT]
ZC = pchip(_Y, [2.90, 2.95, 2.95, 2.95, 2.92]); ZBELT = pchip(_Y, [1.15, 1.15, 1.15, 1.15, 1.18])
WBELT = pchip(_Y, [1.235, 1.250, 1.250, 1.250, 1.235]); WMAX = pchip(_Y, [1.260, 1.275, 1.275, 1.275, 1.260])     # 2.55 m
ZSH = pchip(_Y, [.60, .60, .60, .60, .60]); ZFLOOR = pchip(_Y, [.34, .32, .32, .32, .34]); WFLOOR = pchip(_Y, [1.15, 1.20, 1.20, 1.20, 1.15])
CAB = lambda y: 1.0                                                                                      # window band + roof the whole length
ROOFW = pchip([COWL, 0.0, 5.6], [1.170, 1.170, 1.170]); ROOF_END = 5.6
DECK_FADE = lambda y: 0.0; SK = lambda y: 0.0; HOOD_RIDGE = lambda y: 0.0
STAT = [round(v, 3) for v in np.linspace(-5.45, 5.40, 37)]
YC_F = pchip([.34, .45, .70, 1.00, 1.60, 2.20, 2.70, 2.95], [-5.94, -6.00, -6.00, -5.98, -5.95, -5.93, -5.92, -5.88])   # near-vertical front, slight rake
YC_R = pchip([.34, .60, 1.20, 2.00, 2.95], [5.94, 6.00, 5.99, 5.98, 5.95])
RS_F = pchip([.34, 1.0, 2.95], [.130, .140, .140]); RS_R = pchip([.34, 1.0, 2.95], [.100, .100, .100])
END = {'F': dict(ngon=True, sgn=-1, ysec=-5.55, Yc=YC_F, plan=.10, Rs=RS_F, Rt=.080, Rb=.050, d=(.12, .025), sc=(.982, .94, .84, .56, .22, .07)),
       'R': dict(ngon=True, sgn=1, ysec=5.55, Yc=YC_R, plan=.05, Rs=RS_R, Rt=.080, Rb=.050, d=(.12, .025), sc=(.982, .94, .84, .58, .24, .07))}
GLASS_WS = (99.0, 99.0); GLASS_RW = (99.0, 99.0); GLASS_SIDE = (-5.70, 5.50); SEAL_Y = (-5.72, 5.52); RAIL_Y = (COWL, 5.5)
CREST = lambda y: .40; J3_F = (5.2, 5.9); J3_R = (5.2, 5.9); ROCKER_CREASE = lambda y: 0.0
PILLAR_Y = [-4.50, -3.10, -1.80, -.62, .72, 1.95, 3.20, 4.45]
BPILLAR = (PILLAR_Y[0] - .045, PILLAR_Y[0] + .045); EXTRA_PILLARS = [(y - .045, y + .045) for y in PILLAR_Y[1:]]   # flush window pillars
# ---------------- faces, lamps, doors, trim
FACE_GLASS = [('F', rounded([(-1.10, 2.680), (1.10, 2.680), (1.12, 1.000), (-1.12, 1.000)], [.10, .10, .08, .08], 4), 'TS_Glass'),   # windshield
              ('R', rounded([(-1.00, 2.560), (1.00, 2.560), (1.00, 1.580), (-1.00, 1.580)], [.08, .08, .06, .06], 4), 'TS_Glass')]   # rear window (production: down to 1.58, covers the rear-face cap pinch at z ~1.65)
FACE_TRIMS = [('F', 2.815, 1.02, .170, 'TS_Atlas:screen'), ('R', 2.680, .62, .110, 'TS_Atlas:screen')]   # destination / route displays
SIDE_PANELS = [(-1, rounded([(-5.64, .430), (-4.56, .430), (-4.56, 2.580), (-5.64, 2.580)], .03, 2), 'TS_Glass'),   # front door glass, full height (curb side)
               (-1, rounded([(-.53, .430), (.63, .430), (.63, 2.580), (-.53, 2.580)], .03, 2), 'TS_Glass')]       # middle door glass, full height
EXTRA_GROOVES = [[('sR', y, .40), ('sR', y, .78), ('sR', y, 1.13)] for y in (-5.66, -5.10, -4.54, -.55, .05, .65)]   # door edges + centre splits
HL = lambda sx: rounded([(sx * .74, .740), (sx * 1.02, .740), (sx * 1.02, .580), (sx * .74, .580)], [.03, .04, .04, .03], 3)
GRILLE = rounded([(-.45, .950), (.45, .950), (.45, .820), (-.45, .820)], [.03, .03, .03, .03], 3)        # front vent below the windshield
LOWER = rounded([(-.60, .520), (.60, .520), (.58, .410), (-.58, .410)], [.03, .03, .03, .03], 3)
FOG = lambda sx: rounded([(sx * .80, .520), (sx * .96, .520), (sx * .96, .440), (sx * .80, .440)], .02, 2)
TL = lambda sx: rounded([(sx * .90, 1.200), (sx * 1.10, 1.200), (sx * 1.10, .560), (sx * .90, .560)], [.02, .03, .03, .02], 3)   # tall corner lamps
PLATE_R = rounded([(-.26, .650), (.26, .650), (.26, .540), (-.26, .540)], .012, 3)
VALANCE = rounded([(-.70, 1.450), (.70, 1.450), (.70, .780), (-.70, .780)], .03, 3)                     # rear engine louvre panel
EXH = None
HANDLES = (); HANDLE_Z = 1.0
HOOD_LOOP = None; FDOOR = None; RDOOR = None; FUEL = None
SWEEP_C = (0, 5.0); REAR_SHUT = None; REAR_SHUT_Z = None; REAR_SHUT_FACE_Y = None
LID_SIDE = [('r', .76, .700), ('r', .76, 1.10), ('r', .76, 1.520)]                                    # engine hatch outline
LID_MID = [('r', -.40, 1.520), ('r', 0.0, 1.520), ('r', .40, 1.520)]; LID_X = None
FSHUT_LAMP = None; FSHUT_Z1 = None; FSHUT_MID = []; FSHUT_ARC = 150
MIRROR_POS = (1.42, -5.80, 2.30); MIRROR_SIZE = (.10, .070, .320); MIRROR_BASE_Z = 2.10; MIRROR_DETECT = (1.30, 2.00)
FIN_Y0 = 4.80; CLADDING = False; UNDER_Y = 5.6
HL_CELLS = 2; HL_DRL_SEGS = 5; INTAKE_BLADES = (0.0,)
REVERSE = (.55, .70, .700, .750); REFLECTOR = (.70, .85, .400, .430); REPEATER = (-5.00, -4.90, .900, .930)
LINER_XI = .90; GRILLE_STYLE = 'horizontal'; GRILLE_BARS = 2; GRILLE_BAR_MAT = 'TS_Atlas:dark_chrome'; CHIN_Z = .360; CHIN_W = 1.00
PLATE_F = (.590, .690); REAR_STRIP = None; VALANCE_TRIM = 'TS_Atlas:gloss_black'; BADGE_F = .770; BADGE_R = 1.600
TRAY = (.320, 1.15, -5.60, 5.60); HMSL = ('r', .30, 2.770, 2.790)
BELT_Y1 = 5.30; BELT_TRIM = 'TS_Atlas:gloss_black'
ROCKER = (.400, .060, 'TS_Atlas:plastic_dark'); ROOF_RAILS = None
SPOKES = dict(n=10, dish=.080, twin=0, curve=0.0, w0=.022, w1=.065); DISC_R = .220                     # steel bus wheel: spokes widen to the rim -> 10 small hand holes
INT = dict(drv=.75, dz=.45, half=1.20, rows=[-5.35, -3.90, -3.10, -2.30, 1.40, 2.20, 3.00, 3.80, 4.60], dash=-5.75, parcel=None, two_tone=False, dark=True,
           rear_x=(-.95, -.50, .50, .95), bench=False)                                                  # 2 + 2 seating, centre aisle, door / standing zones kept clear
COLLIDERS = lambda pts: {'Collision_Front': [p for p in pts if p.y < -4.0], 'Collision_Body': [p for p in pts if -4.5 < p.y < 4.5 and p.z < 1.2],
                         'Collision_Cabin': [p for p in pts if -5.8 < p.y < 5.8 and p.z > 1.1], 'Collision_Rear': [p for p in pts if p.y > 4.0]}
COM = (0, .30, 1.10)
GH_TOP = (.200, .90); RW_COL = 10; GRILLE_FRAME = 'TS_Atlas:plastic_dark'
ROOF_BOXES = [(0.0, -.80, (.85, 1.30, .13), 'TS_Atlas:lamp_inner'), (0.0, 3.60, (.40, .40, .05), 'TS_Atlas:lamp_housing')]   # HVAC pod + roof hatch
# ---------------- production detail (approved blockout -> detailed production)
DUAL_REAR = .030; LINER_XI = .55                                                                        # dual rear tires, mudguard liner spans both
GRILLE_FRAME = 'TS_Atlas:plastic_dark'
FACE_WIPERS = (1.05, [(-.10, -.95, 2.30), (.10, .85, 2.25)])                                           # two long wiper arms from the centre pivots
FACE_PARTS = [('sR', 'rod', y, .44, 2.56, .010, 'TS_Atlas:rubber') for y in (-5.64, -5.10, -4.56, -.53, .05, .63)] + \
             [('sR', 'box', y, 1.25, (.020, .012, .060), 'TS_Atlas:wheel_silver') for y in (-5.16, -5.04, -.01, .11)]   # door edge / centre-seal rubbers + door grips
FACE_PARTS = [(k_, kind_) + tuple(a_) for k_, kind_, *a_ in [(e[0], e[1], *e[2:]) for e in FACE_PARTS]]
BOXES = [((-1.05, y, 1.45), (.016, .016, 1.05), 'TS_Atlas:wheel_silver') for y in (-5.70, -4.50, -.60, .70)] + \
        [((sx * .32, y, 1.45), (.016, .016, 1.05), 'TS_Atlas:wheel_silver') for sx in (1, -1) for y in (-3.50, -1.10, 1.80, 3.40)]   # entry grab poles + aisle stanchions
BUMPER_R = (.360, .500, 1.200, .050, 'TS_Atlas:plastic_dark')                                          # rear bumper
REFLECTOR = (.30, .45, .700, .720)
LOD_KEEP_LARGE_TRIM = .30                                                                               # structural trim kept whole at every LOD (chassis / guards / bumpers / posts)
LOD_BODY_MODE = 'planar'                                                                               # boxy commercial body: planar LOD dissolve (flat panels stay whole)
LOD_PLANAR_DEG = {1: 3.0, 2: 9.0, 3: 24.0}                                                             # stronger planar dissolve at distance (flat panels stay exact)
LOD_RK = {1: dict(Trim=.28, Interior=.32), 2: dict(Trim=.10, Interior=.12), 3: dict(Trim=.04, Interior=.08)}
LOD_PLANAR_COLLAPSE = {3: .55}
# production (2026-10-09): alu_brushed -> wheel_silver on poles / grips (brushed normal pattern magnifies on long parts)
# production: row -1.50 dropped -> wheelchair / standing bay opposite the middle door (LOD0 35,359 -> under the 35k ceiling)
LINER_X = 9.0; LINER_ZMIN = lambda y: ZFLOOR(y) + .06; LINER_DISSOLVE = 25.0   # production: interior liner on every cabin wall above the floor (blockout showed bare yellow shell + jagged liner edge through the windshield)
FLAT_PLANAR = .25   # m2: flat panels >= this shade with their face normal (rear-face cap-pinch streaks; see ts_vehicle_v2 game-body shading)
# production: HVAC pod was body paint on a trim part (sampled random body-map UVs -> yellow/black stripes) -> satin grey atlas cell; hatch -> pattern-free dark cell
# production: both ends closed by an n-gon (END ngon=True) - the quad bridge folded at the inner ring corners (170 inverted skin faces per end; windshield glass projected onto the fold reflected the yellow body)
# ================================================================ final QA v3 (2026-10-10): commercial lamp set + night tail glow + smaller cap pole
# extra inner cap ring (sc + .07): the n-gon pole behind the windshield made the horizon reflection wave
TAIL_FILL = (.20, .62)                                                                                  # tall corner lamps glow over the lens (thin strip alone read weak at night)
_SX = (1, -1)
MARKER_LAMPS = [((sx * 1.00, -5.781, 2.83), (.040, .010, .018), 'TS_Lights:Marker', (0, -1, 0)) for sx in _SX] + \
               [((sx * 1.00, 5.898, 2.83), (.040, .010, .018), 'TS_Lights:Tail', (0, 1, 0)) for sx in _SX] + \
               [((x, y, 2.83), (.028, .010, .016), 'TS_Lights:Tail', (0, 1, 0)) for x, y in ((-.30, 5.950), (0.0, 5.956), (.30, 5.950))] + \
               [((sx * 1.278, y, .72), (.010, .040, .016), 'TS_Lights:Marker', (sx, 0, 0)) for sx in _SX for y in (-4.20, 1.50)] + \
               [((sx * 1.278, 5.50, .72), (.010, .040, .016), 'TS_Lights:Tail', (sx, 0, 0)) for sx in _SX]
# amber front clearance, red rear clearance + 3 red ID lamps (above the high-mount brake lamp), amber front + mid side markers, red rear side markers (surfaces measured on the v2 body)
PLAIN_BOXES = [((sx * 1.272, -4.05, .72), (.004, .030, .014), 'TS_Atlas:reflector_amber') for sx in _SX] + \
              [((sx * 1.272, 5.35, .72), (.004, .030, .014), 'TS_Atlas:reflector_red') for sx in _SX]
# final release v4 (2026-10-10): rear engine louvre. The 1.4 x 0.67 m recess used the grain-patterned plastic cell, magnified into a crumpled
# swirl in the close follow view -> pattern-free gloss-black recess + 8 real horizontal louvre slats (dark satin) bridging it
VALANCE_POCKET = 'seal'
FACE_PARTS += [('R', 'box', 0.0, z, (.66, .012, .014), 'TS_Atlas:lamp_housing') for z in (.845, .923, 1.001, 1.079, 1.157, 1.235, 1.313, 1.391)]
