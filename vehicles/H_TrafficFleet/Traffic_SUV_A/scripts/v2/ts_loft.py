# Body loft (one SHELL): sections from the design curves, designed end surfaces, fairing, glass / seal / pillar tags, cage object with creases.
# Executed by ts_vehicle_v2.py once per body shell in its own namespace (a copy of the builder globals + that shell's design overrides).
# Sedan / hatchback / SUV = 1 shell. Pickup = 2 shells (front + cab with a real cab-back wall; separate cargo bed). Extracted from ts_vehicle.py v1.
def ring_half(y):
    zb, wf, wm, zs, zb_, wb, zc, c = ZFLOOR(y), WFLOOR(y), WMAX(y), ZSH(y), ZBELT(y), WBELT(y), ZC(y), CAB(y); sk = SK(y)
    side = [(0.0, zb), (.5 * wf, zb), (wf, zb + .006), (wm - .040 - sk * .3, zb + .075), (wm - .010 - sk, lerp(zb + .075, zs, .5)), (wm, zs), (lerp(wm, wb, .45), lerp(zs, zb_, .55)), (wb, zb_)]
    crown = lambda t: zb_ + (zc - zb_) * (1 - (1 - t) ** 2.2)
    rw = ROOFW(min(max(y, COWL), ROOF_END)); sw = wb - .05
    rd_, rm_, ln_ = GH_PROFILE[:3]; ri_ = GH_PROFILE[3] if len(GH_PROFILE) > 3 else 0   # v2 class greenhouse: roof-edge drop, mid-roof drop, side-glass lean, roof-edge inner point (box roof)
    gh = [(wb - .035, zb_ + .008), (sw, zb_ + .028), (lerp(sw, rw, ln_) + .008, lerp(zb_ + .028, zc - GH_TOP[0], GH_TOP[1])), (rw, zc - rd_)] + \
         ([(rw - ri_, zc - rd_ * .25)] if ri_ else []) + [(.50 * rw, zc - rm_), (0.0, zc)]   # extra point: subdivision no longer pulls a square roof edge 6-10 cm inboard
    w = DECK_FADE(y)                                                                                # Raven P0 rule: rear deck points at the greenhouse x (pure vertical fade)
    ts = [lerp(t, min(max(1 - g[0] / wb, 0.0), 1.0), w) for t, g in zip((.08, .26, .50, .74, .82, .90, 1.0) if ri_ else (.08, .26, .50, .74, .90, 1.0), gh)]
    deck = [(wb * (1 - t), crown(t)) for t in ts]
    hr_ = HOOD_RIDGE(y); deck[2] = (deck[2][0], deck[2][1] + hr_)
    top = [(lerp(d[0], g[0], c), lerp(d[1], g[1], c)) for d, g in zip(deck, gh)]
    return side + top
NS = len(ring_half(0.0)); I_ROOF = 11
def full_ring(y, scale=1.0, centre=None):
    h = ring_half(y); cz = centre if centre is not None else (h[0][1] + h[-1][1]) * .5
    pts = [(x * scale, y, cz + (z - cz) * scale) for x, z in h]
    return pts + [(-x, yy, z) for x, yy, z in pts[1:-1]][::-1]
NR = len(full_ring(0.0)); col_tag = lambda j: j if j < NS else NR - j
# ---- r2 END SURFACES. Each end = a designed face y = Yface(x, z) (side profile pchip + plan curvature), joined to the loft by a controlled-radius
#      corner (quarter circle, radius by outline direction: side / top / bottom), shallow inward-offset rings (corner), then rings scaled toward the
#      face centre, closed by a quad bridge (no fan pole, no folds).
CREASE_W = pchip([.020, .030, .050, .080, .120, .160], [.92, .85, .60, .36, .24, .20])                 # r3: continuous edge-ring crease weight from the (smoothed) corner radius
ENDR = {}
def outline_normals(ring):
    P = [Vector((x, z)) for x, _, z in ring]; n = len(P); c = sum(P, Vector((0, 0))) / n; out = []
    for i in range(n):
        tg = P[(i + 1) % n] - P[i - 1]; nn = Vector((tg.y, -tg.x)).normalized()
        if nn.dot(c - P[i]) < 0: nn = -nn
        out.append(nn)                                                                                  # inward 2D normal (x, z)
    return out
def corner_R(e, nin, z):
    """corner radius from the outline direction: side-facing -> Rs(z), top -> Rt, bottom -> Rb."""
    ax, az = abs(nin.x), nin.y; return e['Rs'](z) * ax + (e['Rt'] if az < 0 else e['Rb']) * abs(az)
def yplane(e, x, z): return e['Yc'](z) - e['sgn'] * e['plan'] * (x / .9) ** 2
def end_rings(e, edge):
    """edge = faired outline ring (NR pts, x, z). returns (d rings far->near, edge ring, cap rings near->inner) with designed y."""
    nin = outline_normals(edge); R = [corner_R(e, n, p[2]) for n, p in zip(nin, edge)]; sg = e['sgn']
    for _ in range(int(E_('TS_RSMOOTH', 8))): R = [(R[i - 1] + 2 * R[i] + R[(i + 1) % len(R)]) / 4 for i in range(len(R))]   # smooth radius changes along the outline (no lip ripple at the corners)
    ENDR[e['sgn']] = R                                                                                 # the crease weights use the same smoothed radius (r2 used the raw one -> steps)
    mk = lambda pts: [tuple(p) for p in pts]
    DW = {e['d'][0]: E_('TS_DW0', .25), e['d'][1]: E_('TS_DW1', .75)}                                 # r3: blend rings carry the loft section AT THEIR OWN y, eased toward the end outline
    def dpt(i, x, z, d):                                                                               # (r2 copied the end outline -> hood-corner / lower-corner bumps)
        y_ = yplane(e, x, z) - sg * (R[i] + d); xs, _, zs = full_ring(y_)[i]; w = DW[d]; xq, zq = lerp(xs, x, w), lerp(zs, z, w)
        return (xq, yplane(e, xq, zq) - sg * (R[i] + d), zq)
    drings = [mk([dpt(i, x, z, d) for i, (x, _, z) in enumerate(edge)]) for d in e['d']]
    ering = mk([(x, yplane(e, x, z) - sg * R[i], z) for i, (x, _, z) in enumerate(edge)])
    zs_ = [z for _, _, z in edge]; zc_ = (min(zs_) + max(zs_)) / 2; caps = []
    for s_ in e['sc']:                                                                                 # scale toward the face centre (star-shaped outline: cannot fold)
        r_ = []
        for i, (x, _, z) in enumerate(edge):
            d_ = (1 - s_) * math.hypot(x, z - zc_); pull = R[i] - math.sqrt(max(0.0, R[i] ** 2 - (R[i] - min(d_, R[i])) ** 2))
            xq, zq = x * s_, zc_ + (z - zc_) * s_; r_.append((xq, yplane(e, xq, zq) - sg * pull, zq))
        caps.append(r_)
    return drings, ering, caps
ef = full_ring(END['F']['ysec']); er = full_ring(END['R']['ysec'])
dF, eF, cF = end_rings(END['F'], ef); dR, eR, cR = end_rings(END['R'], er)
STAT_ = sorted(set(list(STAT) + ([round(v, 3) for p in [BPILLAR] + list(EXTRA_PILLARS) for v in p] if PILLARS_FLUSH else [])))   # v2: exact pillar edges
STAT_ = [v for i, v in enumerate(STAT_) if i == 0 or v - STAT_[i - 1] > .025]
RAW = [eF] + dF[::-1] + [full_ring(y) for y in STAT_] + dR + [eR]                                        # front edge ... loft ... rear edge
def fair_cage(rings, iters=30, lam=.5, mu=-.53, fixed=2):
    R = np.array(rings, float); n = len(R)
    for it in range(iters):
        for f in (lam, mu):
            L = np.zeros_like(R); L[1:-1] = (R[:-2] + R[2:]) * .5 - R[1:-1]; L[:fixed] = 0; L[n - fixed:] = 0; L[..., 1] = 0; R = R + f * L
    return [[tuple(p) for p in r] for r in R]
def fair_lateral(rings, iters=12, lam=.45, mu=-.48, lock=3):
    out = []
    for r in rings:
        R = np.array(r, float); n = len(R); fix = set(range(lock)) | set(range(n - lock + 1, n)) | {7, n - 7}
        if CAB(r[0][1]) > .05: fix |= set(range(8, n - 7))
        if HOOD_RIDGE(r[0][1]) > 1e-4: fix |= {10, n - 10}                                                # keep the designed hood ridge                                               # designed greenhouse stays exact (Pulse EV lesson)
        for it in range(iters):
            for f in (lam, mu):
                L = (np.roll(R, 1, 0) + np.roll(R, -1, 0)) * .5 - R; L[list(fix)] = 0; L[:, 1] = 0; R = R + f * L
        R[NS - 1, 0] = 0.0; out.append([tuple(p) for p in R])
    return out
FAIRED = fair_lateral(fair_cage(RAW))
dF, eF, cF = end_rings(END['F'], [(x, 0, z) for x, _, z in FAIRED[0]]); dR, eR, cR = end_rings(END['R'], [(x, 0, z) for x, _, z in FAIRED[-1]])   # end surfaces from the faired outline
FAIRED = [eF] + dF[::-1] + FAIRED[1 + len(dF):len(FAIRED) - 1 - len(dR)] + dR + [eR]
RINGS = cF[::-1] + FAIRED + cR
I_FRONTFACE = len(cF); I_REARFACE = len(cF) + len(FAIRED) - 1
def fair_columns(rings, idx, iters=int(E_('TS_CFAIR', 40)), lam=.5, mu=-.53):
    """r3: chord-weighted Taubin fairing of x, z ALONG each cage column across the end transition (faired loft rings -> designed blend rings).
    r2 had 3-7 mm kinks there (e.g. lower bumper side x .848 -> .851 -> .844) = zebra rings on the corners. y (designed) and the face edge ring stay fixed."""
    R = np.array(rings, float)
    for _ in range(iters):
        for f in (lam, mu):
            L = np.zeros_like(R)
            for i in idx:
                wp = 1 / np.maximum(np.abs(R[i, :, 1] - R[i - 1, :, 1]), 1e-3); wn = 1 / np.maximum(np.abs(R[i + 1, :, 1] - R[i, :, 1]), 1e-3)
                L[i] = (wp[:, None] * R[i - 1] + wn[:, None] * R[i + 1]) / (wp + wn)[:, None] - R[i]
            L[..., 1] = 0; R = R + f * L
    return [[tuple(p) for p in r] for r in R]
_nd = len(dF); RINGS = fair_columns(RINGS, list(range(I_FRONTFACE + 1, I_FRONTFACE + _nd + 2)) + list(range(I_REARFACE - _nd - 1, I_REARFACE)))
if os.environ.get('TS_DUMP'): json.dump(dict(rings=RINGS, ff=len(cF), rf=len(cF) + len(FAIRED) - 1, ns=NS, nr=NR), open(os.environ['TS_DUMP'], 'w')); sys.exit(0)   # diagnosis
LIFT = (E_('TS_LIFT_A', .10), E_('TS_LIFT_B', .34))                                                     # r3: lift eased over a wider band (r2 .15-.24 put a 6 mm step on the lower corners)
RINGS = [[(x, y, z + .006 * (1 - ss(LIFT[0], LIFT[1], z))) for x, y, z in r] for r in RINGS]            # floor lift: subdivided underside >= clearance
VB = [p for r in RINGS for p in r]; F = []; FT = []
for i in range(len(RINGS) - 1):
    for j in range(NR):
        a = i * NR + j; b = i * NR + (j + 1) % NR; cc = (i + 1) * NR + (j + 1) % NR; d = (i + 1) * NR + j
        endf = i < I_FRONTFACE or i >= I_REARFACE
        F.append((a, d, cc, b)); ym = (RINGS[i][0][1] + RINGS[i + 1][0][1]) / 2; h0, h1 = col_tag(j), col_tag((j + 1) % NR); FT.append(('cap', 0, 0) if endf else (ym, min(h0, h1), max(h0, h1)))
for ri in (0, len(RINGS) - 1):                                                                       # quad bridge of the innermost ring (top row <-> bottom row, each half)
    o_ = ri * NR
    for half in (0, 1):
        idx = list(range(0, NS)) if half == 0 else [0] + list(range(NR - 1, NS - 2, -1))
        for k in range(NS // 2 - 1):
            a, b, c2, d2 = idx[k], idx[k + 1], idx[NS - 2 - k], idx[NS - 1 - k]
            f = (o_ + a, o_ + b, o_ + c2, o_ + d2); F.append(f); FT.append(('cap', 0, 0))
def tag(t):
    if t[0] == 'cap': return 'paint'
    y, a, b = t
    if CAB(y) < .5: return 'paint'
    if a >= I_ROOF and GLASS_WS[0] < y < GLASS_WS[1]: return 'glass'                                                  # windshield
    if a >= RW_COL and GLASS_RW[0] < y < GLASS_RW[1]: return 'glass'                                                   # rear window
    if (a, b) == (9, 10) and PILLARS_FLUSH and any(p0 < y < p1 for p0, p1 in [BPILLAR] + list(EXTRA_PILLARS)): return 'seal'   # v2: flush body pillar (gloss black), part of the skin
    if (a, b) == (9, 10) and GLASS_SIDE[0] < y < GLASS_SIDE[1]: return 'glass'                                            # side glass (front door, rear door, quarter light)
    if (a, b) == (8, 9) and SEAL_Y[0] < y < SEAL_Y[1]: return 'seal'                                              # belt / DLO seal
    return 'paint'
TAGS = [tag(t) for t in FT]
def cage_obj(name):
    tags = [PRE + '_Paint' if t == 'paint' else 'TS_Glass' if t == 'glass' else 'TMP_seal' for t in TAGS]
    me = bpy.data.meshes.new(name); me.from_pydata(VB, [], F); me.update(); order = list(dict.fromkeys(tags))
    for m in order: me.materials.append(MM[m])
    me.polygons.foreach_set('material_index', [order.index(t) for t in tags]); o = bpy.data.objects.new(name, me); WORK.objects.link(o)
    bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    cr = me.attributes.new('crease_edge', 'FLOAT', 'EDGE'); n_ = len(RINGS)
    crest = {i * NR + j for i in range(n_) for j in (7, NR - 7)}
    rail = {i * NR + j for i in range(n_) if RAIL_Y[0] < RINGS[i][0][1] < RAIL_Y[1] for j in (I_ROOF, NR - I_ROOF)}
    for e in me.edges:
        a_, b_ = e.vertices
        if a_ >= n_ * NR or b_ >= n_ * NR: continue
        ia, ja = divmod(a_, NR); ib, jb = divmod(b_, NR); ym_ = (VB[a_][1] + VB[b_][1]) / 2
        endz = min(ia, ib) < I_FRONTFACE or max(ia, ib) > I_REARFACE
        if ia == ib and ia in (I_FRONTFACE, I_REARFACE) and 'face' in COFF: continue
        if ia == ib and ia in (I_FRONTFACE, I_REARFACE):                                                                    # face edge ring: crisp where the corner radius is small (trunk lip, hood edge)
            Rl = ENDR[-1 if ia == I_FRONTFACE else 1]; cr.data[e.index].value = float(CREASE_W((Rl[ja] + Rl[jb]) / 2))   # continuous (r3)
            continue
        if endz: continue
        if ia != ib and ja == jb:
            if ja in (3, NR - 3) and 'j3' in COFF: continue
            if a_ in crest and b_ in crest and 'crest' in COFF: continue
            if a_ in crest and b_ in crest: cr.data[e.index].value = CREST(ym_)   # strong shoulder, lamp to lamp   # shoulder line (crisp, real-car)
            elif a_ in rail and b_ in rail: cr.data[e.index].value = .55                                                    # roof drip rail
            elif ja in (3, NR - 3):                                                                                         # sill / bumper lower edge: hands over to the face edge weight (r3)
                sg_ = -1 if ym_ < 0 else 1; w_end = float(CREASE_W(ENDR[sg_][ja])); t_ = ss(J3_F[0], J3_F[1], -ym_) if sg_ < 0 else ss(J3_R[0], J3_R[1], ym_)
                cr.data[e.index].value = lerp(.30, w_end, t_)
            elif ja in (10, NR - 10) and HOOD_RIDGE(ym_) > 1e-4 and CAB(ym_) < .05: cr.data[e.index].value = .30 * HOOD_RIDGE(ym_) / max(E_('TS_HOODRIDGE', .007), 1e-6)   # hood ridge
            elif ja in (4, NR - 4): cr.data[e.index].value = ROCKER_CREASE(ym_)        # lower rocker sculpt line (doors only)
    return o
COFF = set(os.environ.get('TS_CREASE_OFF', '').split(','))                                               # diagnosis only
