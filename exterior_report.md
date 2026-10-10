# Exterior 04 review checkpoint

Source: `/Users/meetshah/Documents/blender/racing_car_03_realistic_body.blend` (preserved).

1. **Topology:** Kept the major skin predominantly quad based, welded the ducktail root into the body, added headlight opening support loops, cleaned normals and loose vertices. Kept symmetry, subdivision, panel thickness and curve weld modifiers editable. Base quad fraction: 84.4%.
2. **Wheel arches:** Replaced abrupt arch endings with tangent transitions and consistent rolled lips. Raised the front outer fender shoulder to remove inverted side strips above the tires. Corrected the discontinuous lip width and limited inner skin thickness to avoid folded offsets.
3. **Front fascia:** Slimmed painted intake frames, added cooling guide vanes and a central hex grille, refined the recessed headlight fit and splitter returns. Retained a separate bumper with a subtle manufacturing boundary.
4. **Rear fascia:** Inset the light assemblies into real bumper openings, cleaned face orientation, refined the lower recess and exhaust seating, and integrated the ducktail root.
5. **Side intakes:** Replaced the shallow throat with drafted curved duct surfaces leading inward toward the engine bay, including a dark depth cap. Retained the defining door-to-quarter sculpting.
6. **Doors and gaps:** Extracted separate left/right door panels from the body skin, inset boundaries by approximately 3.5 mm, added seals and minimal recessed flush handles. Hood and engine-cover seals define plausible shutlines. Small manufacturing gaps remain separate editable parts.
7. **Headlights:** Clear outer covers over dark cavities, two canted projector modules per side with metallic bezels and optical lenses, a swept angular DRL blade and a secondary LED element. Original generic design; no manufacturer branding.
8. **Taillights:** Neutral smoked covers, two staggered horizontal red strokes with an outer kick, independent brake, reverse and amber indicator regions/material channels. Separate left/right assemblies emphasize width.
9. **Aero and exhaust:** Restrained splitter side returns, connected skirt seams, four rounded diffuser fins, welded integrated ducktail, hollow double-wall metallic exhaust tips with darker inner sleeves. Engine-cover openings, seven louvers per side and rear fascia ribs add visible functional depth.
10. **Wheels and tires:** Preserved the original split spokes. Separated wheel metal, dark accents and center-cap materials; added lug counterbores. Added shallow shoulder sipes and generic embossed AERO SPORT/size lettering. No tire brand logos. Embossed lettering contributes substantial editable geometry and is a later optimization candidate.
11. **Brakes:** Flat annular rotor-face shading, small edge bevels, central hat rings, multi-piston caliper bosses and a bridge/spine. Four calipers stay stationary when their wheels rotate about the local X axle.
12. **Mirrors and glazing:** Sculpted teardrop housings, thin mounts and correctly rear-facing mirror glass. Refitted windshield, roof, rear glass and side/quarter glass with thin seals. Corrected window orientation and roof-edge seating; no intersections in the audited body/glass pairs.
13. **Base geometry:** 75,146 vertices; 74,012 polygons; 141,264 triangles. Counts include the retained minimal cabin shadow deck, not a new full interior.
14. **Evaluated geometry:** 271,984 vertices; 274,980 polygons; 539,824 triangles. Includes live subdivision, thickness and curve evaluation. No final game-budget reduction was performed.

| Category | Base vertices | Base polygons | Base triangles | Evaluated vertices | Evaluated polygons | Evaluated triangles |
|---|---:|---:|---:|---:|---:|---:|
| Body | 17,670 | 14,588 | 29,800 | 119,004 | 117,856 | 235,664 |
| Wheels | 7,392 | 6,680 | 14,512 | 14,944 | 14,392 | 29,616 |
| Tires | 31,120 | 36,612 | 62,080 | 37,168 | 42,884 | 73,728 |
| Brakes | 4,832 | 3,960 | 9,264 | 22,800 | 22,408 | 44,912 |
| Glass | 4,394 | 3,956 | 7,992 | 27,516 | 27,460 | 55,000 |
| Lights | 7,644 | 6,400 | 13,984 | 35,652 | 35,080 | 71,152 |
| Aero | 2,094 | 1,816 | 3,632 | 14,900 | 14,900 | 29,752 |

15. **Remaining weak areas:** This is an editable exterior review checkpoint rather than a certified shipping game asset. Tight arch/bumper transitions, optical cover boundaries and the dense physical tire lettering remain the highest-priority areas for human close-range review and later optimization. Fine manufacturing tolerances and mechanical opening/hinge behavior have not been engineered. Procedural review materials are temporary. The current model retains a broad, intentionally sculpted shoulder and fairly upright front/rear fascia.
16. **Validation:** PASS: required objects/collections, unique meaningful names, positive uniform unit scales, metric orientation, wheel centers/X axes, stationary calipers, no zero-area faces, no unused vertices, closed-surface signed-volume orientation, evaluated manifold surfaces, no audited primary body/glass overlaps and no nonadjacent primary self-overlap candidates. Base panels/curves may be open; 73 become capped/thickened through evaluation. **0 errors, 2 warnings:** final UVs/textures/interior/LODs/colliders/export remain deferred; assembly intersection checking is limited to primary surfaces, with intentional optical/trim/duct seating not globally unioned. Signed-volume checks do not prove every internal subassembly normal is correct. See `exterior_validation.txt` for exact scope.

Temporary high-gloss gray reflection renders were inspected from front 3/4, rear 3/4, side, top-front, low front and low rear. Dark flat silhouettes were inspected from side and both 3/4 views. These checks identified and led to the front shoulder/lip corrections. QA files use the `previews/qc_gloss_` and `previews/qc_silhouette_` prefixes. Final review uses the original temporary paint/material palette.

Envelope: length 4.5488 m, width 2.0073 m, height 1.1998 m. Wheelbase 2.7000 m. Front/rear tire nominal diameters remain 0.690/0.730 m; embossed detail adds negligible local protrusion.

17. **Saved Blender path:** `/Users/meetshah/Documents/blender/racing_car_04_exterior_final.blend`
18. **Final previews:** all nine are PNG, 1920 × 1080.

- `/Users/meetshah/Documents/blender/previews/exterior_front.png`
- `/Users/meetshah/Documents/blender/previews/exterior_front_3q.png`
- `/Users/meetshah/Documents/blender/previews/exterior_side.png`
- `/Users/meetshah/Documents/blender/previews/exterior_rear_3q.png`
- `/Users/meetshah/Documents/blender/previews/exterior_rear.png`
- `/Users/meetshah/Documents/blender/previews/exterior_top_3q.png`
- `/Users/meetshah/Documents/blender/previews/exterior_headlight_closeup.png`
- `/Users/meetshah/Documents/blender/previews/exterior_taillight_closeup.png`
- `/Users/meetshah/Documents/blender/previews/exterior_wheel_closeup.png`

Exterior scope stops here. No interior, UV/texturing, LOD, collider or export production was started.
