# Material merge review (pre-Phase 7)

39 materials (36 assigned + 3 unassigned paint variants). Nothing merged yet.

Key point: after export, every opaque part samples its **atlas** texture set (BaseColor/Roughness/Metallic/Normal/AO
per atlas). So most opaque materials inside one atlas become one engine material automatically. The ones that must stay
separate are those with special shading (clearcoat paint, transparency, emission) or that the game drives at runtime.

## KEEP_SEPARATE

| Material(s) | Reason |
|---|---|
| MAT_CarPaint_RacingRed (+ ElectricBlue / PearlWhite / SatinBlack, unassigned) | clear-coat car-paint shader; colour swapping at runtime |
| MAT_Windshield, MAT_SideGlass, MAT_RearGlass, MAT_EngineGlass | transparent pass (could become 1 later, see below) |
| MAT_HeadlightLens, MAT_TaillightLens | transparent lens; taillight is red-tinted |
| MAT_LED_White (DRL) | independent light channel |
| MAT_ProjectorLens | low/high beam toggle (emission only at night) |
| MAT_LED_Red (tail) | independent light channel |
| MAT_LED_Brake | brake must switch independently of tail |
| MAT_LED_Amber | indicators blink independently L/R |
| MAT_LED_Reverse | independent light channel |
| MAT_AmbientLight | cabin ambient on/off, colour option |
| MAT_Display + MAT_DisplayGraphics + MAT_DisplayGraphics_Red | keep while the UI may be driven live by the game |
| MAT_Tire | dedicated tire map (shared lettering band, intentional overlap) |
| MAT_BrakeCaliper | colour option (yellow default) |

## CAN_MERGE_LATER (no visual change, values live in the atlas maps)

| Merge into | Materials | Notes |
|---|---|---|
| WHEELS atlas material | MAT_Wheel_Machined, MAT_Wheel_Graphite, MAT_Wheel_DarkBarrel | duplicate metals; roughness/metallic baked per texel |
| BRAKES atlas material | MAT_BrakeRotor (+ hat/hole slots already shared) | caliper stays separate only for colour options |
| INTERIOR atlas material | MAT_InteriorLeather, MAT_InteriorAlcantara, MAT_InteriorCarbon, MAT_InteriorPlastic, MAT_InteriorMetal, MAT_SeatAccent, MAT_Speaker | carbon weave, grain, stitching, perforation all baked |
| TRIM atlas material | MAT_CarbonExterior, MAT_BlackTrim, MAT_ExhaustMetal | duplicate black plastic + carbon + metal |
| LIGHTS atlas material | MAT_HeadlightHousing, MAT_ProjectorMetal | black plastic / chrome duplicates |
| one black-plastic material (if not atlas-merged) | MAT_BlackTrim, MAT_HeadlightHousing, MAT_InteriorPlastic | near-identical satin blacks |
| one metal material (if not atlas-merged) | MAT_ExhaustMetal, MAT_ProjectorMetal, MAT_InteriorMetal, MAT_Wheel_Machined | colour/roughness differ only slightly |
| one carbon material | MAT_CarbonExterior, MAT_CarbonInterior | same shader, 4 mm vs 2 mm weave tiling (baked) |
| one glass material | 4 glass materials | tint from GLASS atlas BaseColor |
| one mirror material | MAT_InteriorMirror (already shared by interior + exterior mirrors) | done |
| display (only if UI becomes a static texture) | MAT_Display, MAT_DisplayGraphics, MAT_DisplayGraphics_Red | otherwise keep separate |

Do NOT merge: MAT_LED_Red with MAT_LED_Brake, or MAT_LED_Amber left/right usage (game-controlled channels).

Estimated engine material count after consolidation: ~20 (8 atlas materials incl. paint, 1-2 glass, 1 lens set,
6 light channels, ambient, display, tire, caliper).

## Body UV decision

The body atlas stays at 4096 (no 8K). The body is uniform metallic paint plus tiled micro-detail, so 4K is enough.
If a unique livery, racing decals or close-up body graphics are needed later, use two 4K body atlases or a separate
decal/livery atlas, not a single 8K texture.
