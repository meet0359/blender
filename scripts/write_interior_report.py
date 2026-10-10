import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'interior_stats.json').read_text())
text='''# Interior 05 checkpoint

Original two-seat supercar cockpit, built in Blender from `racing_car_04_exterior_final.blend`. Source checkpoint 04 is preserved byte-for-byte. Exterior meshes, transforms and live modifiers were retained. The window material alone was changed to lighter tint/full transmission to make the cabin visible; window geometry was preserved. The two obsolete solid interior placeholder decks were removed.

1. **Dashboard design:** A low swept leather crown, separate lower fascia, knee pads, passenger glovebox and a fitted cowl closure. Three compact HVAC outlets use real dark cavities and restrained horizontal blades. A charcoal instrument shroud rises smoothly from the crown.
2. **Steering wheel:** Original compact three-spoke wheel with flattened lower rim, shaped grips, a restrained red center marker, four small buttons and a plain hub. A column and dash boot physically support it. Independent metal paddles and stalks sit behind it. Its origin is on the steering axis at `(-0.36, -0.405, 0.718)` m; no animation rig was created.
3. **Seats:** Two bucket seats with substantial shells, reclined backrests, integrated headrest profiles, separate pads, shoulder/side bolsters, thigh support and selective seam curves. Seat centers are at X ±0.36 m. Recline is approximately 27 degrees from vertical. Headrest-to-exterior-roof clearance is about 83 mm. Rails, belt webbing and buckles complete the visible assembly. Headroom is a geometric check, not an anthropometric fit certification.
4. **Center console:** A supported tunnel connects firewall/dashboard to rear bulkhead. A compact selector, red start/stop button, mode rotary, three small switches, shallow storage tray and rear armrest keep the layout simple.
5. **Instrument cluster:** A physical dark screen and frame sit behind the steering wheel, inside a tapered visor/shroud. The driver's seat, steering wheel and cluster share the same lateral center. UI artwork remains intentionally absent.
6. **Infotainment/display:** A modest landscape screen angles toward the driver and sits in a physical metallic housing with a dashboard support. Its position was corrected so it is visible in front of the fascia and clear of the center vent. No final graphics were baked.
7. **Door panels:** Separate left/right leather panels with armrests, carbon-like inserts, metal pulls, window switches and efficient slotted speaker areas. Each panel stays within the exterior door's longitudinal span; trim is parented to its panel. Future hinge origins are prepared, but the exterior door and window opening mechanics remain a later rigging task.
8. **Pedals:** Separate brake, accelerator and dead pedal with metal faces and four rubber grip strips each. Brake and throttle use low hinge origins inside the driver's footwell. The floor tub, mats, firewall and tunnel close the lower cabin.
9. **Rear bulkhead:** A padded structural bulkhead and upper shelf sit behind the seats. No engine or character was created. A fitted headliner, pillar liners, simple visors, overhead housing and mounted rear-view mirror finish the upper cabin; the overhead housing contains no functional light.
10. **Material slots:** `MAT_InteriorLeather`, `MAT_InteriorPlastic`, `MAT_InteriorAlcantara`, `MAT_InteriorCarbon`, `MAT_InteriorMetal`, `MAT_Display`, `MAT_SeatAccent`, `MAT_Speaker`. A separate `MAT_InteriorMirror` supplies the reflective mirror surface. Palette: charcoal/dark gray, restrained red accents and dark metal. All are temporary review materials without final textures.
'''
b=d['base']; e=d['evaluated']; allv=d['complete_vehicle_evaluated']
text+=f'''11. **Interior base geometry:** {b[0]:,} vertices, {b[1]:,} polygons, **{b[2]:,} triangles**. Within the 30,000–60,000 triangle target.
12. **Interior evaluated geometry:** {e[0]:,} vertices, {e[1]:,} polygons, **{e[2]:,} triangles**. Within the 60,000–120,000 triangle target. Subdivision is retained on the dashboard crown and seat shells; sufficiently dense base grids elsewhere use smooth shading and live thickness.
13. **Complete vehicle evaluated geometry:** {allv[0]:,} vertices, {allv[1]:,} polygons, **{allv[2]:,} triangles**. The complete vehicle count replaces, rather than adds to, the old cabin placeholder decks. Studio floor, cameras and lights are excluded.

| Interior group | Base vertices | Base polygons | Base triangles | Evaluated vertices | Evaluated polygons | Evaluated triangles |
|---|---:|---:|---:|---:|---:|---:|
'''
for name,row in d['categories'].items(): text+='| '+name+' | '+' | '.join(f'{v:,}' for v in row['base']+row['evaluated'])+' |\n'
text+='''
14. **Fit corrections:** Removed the blocking placeholder decks; reduced interior-only subdivision to meet the requested budget; corrected pedal/paddle origins; inset A-pillar liners; seated the mirror mount below the inner windshield; lifted and reshaped the instrument housing to clear the dashboard; brought the center display forward and separated it from its vent; seated seam paths on their host surfaces; closed the lower windshield cowl; shortened both inner sills and narrowed the rear bulkhead to clear the side-intake ducts. The duct envelopes are included in the final intersection audit. No exterior geometry redesign was required.
15. **Remaining weak areas:** This is an editable interior review checkpoint. Temporary untextured surfaces do not yet carry leather grain, carbon weave, screen UI or final stitch detail. Small assemblies intentionally overlap at their seats and attachments. Door opening mechanics, occupant ergonomics across body sizes, belt routing under motion, and real manufacturing tolerances need later specialist review. The blank cluster's placement can be assessed from the cockpit view; UI legibility awaits graphics. Physical material/shading quality will improve during the separate texturing phase.
16. **Validation:** **0 errors, 2 warnings.** PASS: required objects/materials, meaningful names, positive uniform scales, no accidental hidden parts, no asset lights, source-file preservation, no zero-area faces or loose vertices, manifold evaluated thickness, consistent closed-surface signed volume, both triangle budgets, no audited cabin/exterior/glass intersections, no primary interior assembly crossings, steering origin/alignment, pedals in the footwell, seat clearance and door-panel span. Warnings: downstream production phases remain deferred; seated upholstery/trim/fastener assemblies are not globally boolean-unioned and mechanical tolerances are outside this audit. Signed-volume checks are not a per-face normal proof for every detail. Exact results are in `interior_validation.txt`.

The five interior detail images use presentation cutaways where useful: the driver/passenger views temporarily hide the exterior and upper liner; the dashboard view additionally hides the seats/doors; the seat view isolates seats, floor and bulkhead. `interior_cockpit.png` and all three through-window images retain the intact vehicle and glass. Temporary cutaway lights/visibility changes are removed/restored before saving. `Camera_Cockpit_QA` is positioned at an approximate driver eye point `(-0.36, 0.15, 1.027)` m and retained for Blender review only.

17. **Saved checkpoint:** `/Users/meetshah/Documents/blender/racing_car_05_interior.blend`
18. **Previews:** PNG files at 1920 × 1080:

'''
for name in ['driver','passenger','dashboard','seats','cockpit','through_front_3q','through_side','through_rear_3q']:
    text+=f'- `/Users/meetshah/Documents/blender/previews/interior_{name}.png`\n'
text+='\nWork stops at this interior checkpoint. No final UVs/textures, gameplay, LODs, colliders, vehicle optimization or export were started.\n'
(ROOT/'interior_report.md').write_text(text)
