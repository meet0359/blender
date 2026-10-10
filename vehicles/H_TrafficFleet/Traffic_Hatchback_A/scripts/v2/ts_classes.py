# v2 vehicle-class presets for ts_vehicle_v2.py. A design declares CLASS = '<name>'; these fill only what the design does not set.
# Structure per class (what the builder does differently), not body shapes: every coordinate still comes from the design file.
#   GH_PROFILE   (roof-edge drop, mid-roof drop, side-glass lean 0..1[, roof-edge inner point offset: box roof]) - sedan: crowned roof + strong tumblehome; SUV / van / pickup: flat roof, upright DLO
#   SHELLS       None = one body loft; pickup = [front + cab shell (real cab-back wall), cargo-bed shell] (each a full loft with its own designed ends)
#   PILLARS_FLUSH  B / C / D pillars are gloss-black faces of the skin (exact ring stations), not appliques laid over one glass strip
#   RAIL_*       roof rails: closed box section; CLAD_F / CLAD_R lower bumper cladding panels (front / rear outlines, dark plastic)
CLASSES = {
    'sedan':       dict(GH_PROFILE=(.032, .007, .82), PILLARS_FLUSH=True, RAIL_W=.026, RAIL_H=.020, RAIL_MAT='TS_Atlas:plastic_black', CLAD_F=[], CLAD_R=[], SHELLS=None),
    'hatchback':   dict(GH_PROFILE=(.030, .006, .80), PILLARS_FLUSH=True, RAIL_W=.026, RAIL_H=.020, RAIL_MAT='TS_Atlas:plastic_black', CLAD_F=[], CLAD_R=[], SHELLS=None),
    'suv_compact': dict(GH_PROFILE=(.024, .004, .70, .07), PILLARS_FLUSH=True, RAIL_W=.030, RAIL_H=.024, RAIL_MAT='TS_Atlas:plastic_black', CLAD_F=[], CLAD_R=[], SHELLS=None),
    'suv_full':    dict(GH_PROFILE=(.022, .004, .66, .07), PILLARS_FLUSH=True, RAIL_W=.030, RAIL_H=.022, RAIL_MAT='TS_Atlas:alu_brushed', CLAD_F=[], CLAD_R=[], SHELLS=None),
    'pickup':      dict(GH_PROFILE=(.020, .003, .62, .07), PILLARS_FLUSH=True, RAIL_W=.030, RAIL_H=.024, RAIL_MAT='TS_Atlas:plastic_black', CLAD_F=[], CLAD_R=[], SHELLS=None),
    'van':         dict(GH_PROFILE=(.018, .003, .55, .07), PILLARS_FLUSH=True, RAIL_W=.030, RAIL_H=.024, RAIL_MAT='TS_Atlas:plastic_black', CLAD_F=[], CLAD_R=[], SHELLS=None),   # future (not yet exercised)
}
def apply_class(G):
    c = G.get('CLASS', 'sedan'); assert c in CLASSES, ('unknown CLASS', c)
    for k, v in CLASSES[c].items(): G.setdefault(k, v)
    G['CLASS'] = c
if __name__ == '__main__':
    g = dict(CLASS='suv_full', GH_PROFILE=(1, 2, 3)); apply_class(g); assert g['GH_PROFILE'] == (1, 2, 3) and g['RAIL_MAT'] == 'TS_Atlas:alu_brushed'
    g = {}; apply_class(g); assert g['CLASS'] == 'sedan' and g['SHELLS'] is None; print('ts_classes ok')
