# Hypercar (frozen flagship): reference reports

These are the delivered reports of the finished, frozen hypercar. Every new vehicle must follow the same conventions: axes, hierarchy, pivots, colliders, centre of mass, LODs, material channels and FBX validation. They are copied verbatim from `new_car/reports/`.


---

## `new_car/reports/unity_import_notes.md`

_Unity import contract: axes, dimensions, wheel refs, centre of mass, LOD table, material groups, colliders, pivots, suggested Unity hierarchy_

# Unity import notes: hypercar

Files: `exports/hypercar_complete_unity.fbx` (LOD0-3 + colliders + refs, 308 objects) and
`exports/hypercar_LOD0_unity_test.fbx` (LOD0 only, 102 objects). Textures are external (not embedded), referenced
relatively as `../textures/hypercar/<group>/*.png`. Copy `textures/hypercar/` into the Unity project with the FBX.

## Importer settings (Model tab)
- Scale Factor **1**, Convert Units **ON** (file unit = 1 m, UnitScaleFactor 100 cm). Result: 1 unit = 1 m, root scale 1.
- Bake Axis Conversion **OFF** (not needed: axes are already baked; Car_Root rotation is identity in the file).
- Import Normals: **Import**; Tangents: **Import** (MikkTSpace, exported); Smoothing source: from file.
- Materials: Location "Use External Materials (Legacy)" or extract, then set them up per `unity_material_mapping.md`.
- Animation: none in the file (Animation Type None). No cameras or lights.

## Coordinate conversion (verified by re-import)
| | Blender | FBX file | Unity |
|---|---|---|---|
| forward | -Y | +Z | **+Z** |
| up | +Z | +Y | **+Y** |
| vehicle left | +X | +X | **-X** (Unity's importer negates FBX X) |
| point (x, y, z) | (x, y, z) | (x, z, -y) | (-x, z, -y) |

The car faces +Z, upright, and the LHD driver seat sits on the vehicle's left (Unity -X). Car_Root: position 0, rotation 0, scale 1.
Unity view checks: nose z 2.3967, tail z -2.249, roof y 1.1726.

## Dimensions (LOD0 re-import, mirrors excluded)
Length 4.695 m, width 2.05233 m, height 1.17258 m (all within 0.05 mm of Phase 7).
Wheelbase 2.78 m, track front 1.67 m / rear 1.67 m.

## Wheels (WheelColliderRef_* empties = wheel centres)
| Ref | Side | Blender | Unity local to Car_Root | radius m | width m |
|---|---|---|---|---|---|
| FL | LEFT | (0.835, -1.39, 0.355) | (-0.835, 0.355, 1.39) | 0.355 | 0.31 |
| FR | RIGHT | (-0.835, -1.39, 0.355) | (0.835, 0.355, 1.39) | 0.355 | 0.31 |
| RL | LEFT | (0.835, 1.39, 0.3775) | (-0.835, 0.3775, -1.39) | 0.3775 | 0.35 |
| RR | RIGHT | (-0.835, 1.39, 0.3775) | (0.835, 0.3775, -1.39) | 0.3775 | 0.35 |

Use the refs to position WheelColliders (radius as above; suspension distance tuned in Unity).
Visual wheels: `Wheel_<k>_LODn` rotates on **local X** (axle; tire + rotor are children, calipers do not roll).
Front steering: `SteerPivot_FL/FR_LODn` yaws on **local Y** (= car up) about the wheel centre, carrying wheel and caliper.
Because Unity mirrors X on import, drive the visual wheels from `WheelCollider.GetWorldPose` rather than accumulating
local Euler angles; if spinning by hand, verify the sign once per side.

## Center of mass
`CenterOfMass` empty: Blender (0, 0.12, 0.35) -> Unity local **(0.0, 0.35, -0.12)**
(0.35 m high, 0.12 m behind mid-wheelbase). Assign `rigidbody.centerOfMass = CenterOfMass.localPosition` in a script.

## LODs (one FBX, four roots)
| LOD | triangles | L x W x H (m) | material slots |
|---|---|---|---|
| LOD0 | 206,327 | 4.695 x 2.05233 x 1.17258 | 24 |
| LOD1 | 107,210 | 4.695 x 2.05252 x 1.17258 | 24 |
| LOD2 | 53,786 | 4.695 x 2.05275 x 1.1741 | 20 |
| LOD3 | 17,747 | 4.69201 x 2.05275 x 1.1741 | 15 |

Triangles are Phase 7 counts minus 57 coincident duplicate triangles removed at export ({"Caliper_FL_LOD3": 3, "InstrumentCluster_LOD1": 2, "Caliper_FR_LOD3": 2, "CenterConsole_LOD2": 6, "InstrumentCluster_LOD2": 2, "Body_LOD2": 7, "Body_LOD0": 2, "Interior_LOD3": 21, "Interior_Tub_LOD2": 6, "Caliper_RL_LOD3": 5, "Caliper_RR_LOD3": 1}).
Set up a LOD Group on Car_Root: LOD0_Root ... LOD3_Root renderers (suggested 60 / 30 / 12 / 3 % screen height).
Colliders, refs and CenterOfMass are outside the LOD roots and shared by all LODs.

## Material groups
24 materials per LOD: 8 baked atlases (`LODMAT_Body_Paint`, `Brakes`, `Glass`, `Interior`, `Lights`, `Tire`,
`Trim`, `Wheels`) + carbon (exterior/interior) + caliper + lenses + displays + interior mirror + **6 light channels kept
separate**: `MAT_LED_White`, `MAT_ProjectorLens`, `MAT_LED_Red`, `MAT_LED_Brake`, `MAT_LED_Amber`, `MAT_LED_Reverse` (+ `MAT_AmbientLight`).
Full mapping: `reports/unity_material_mapping.md`.

## Textures (48 files, PNG)
Atlases: BODY 4096, INTERIOR 4096, WHEELS / TIRES / LIGHTS 2048, BRAKES / GLASS / TRIM 1024; each has BaseColor, Metallic,
Roughness, Normal, AO. **Normal maps are OpenGL (+Y up green)**, which is Unity's convention: import as Normal map, no flip.
Roughness must be inverted to smoothness (see mapping). AO is not linked by the FBX; assign it manually.
- `textures/hypercar/body/BODY_AO.png`
- `textures/hypercar/body/BODY_BaseColor.png`
- `textures/hypercar/body/BODY_Metallic.png`
- `textures/hypercar/body/BODY_Normal.png`
- `textures/hypercar/body/BODY_Roughness.png`
- `textures/hypercar/brakes/BRAKES_AO.png`
- `textures/hypercar/brakes/BRAKES_BaseColor.png`
- `textures/hypercar/brakes/BRAKES_Metallic.png`
- `textures/hypercar/brakes/BRAKES_Normal.png`
- `textures/hypercar/brakes/BRAKES_Roughness.png`
- `textures/hypercar/glass/GLASS_AO.png`
- `textures/hypercar/glass/GLASS_BaseColor.png`
- `textures/hypercar/glass/GLASS_Metallic.png`
- `textures/hypercar/glass/GLASS_Normal.png`
- `textures/hypercar/glass/GLASS_Roughness.png`
- `textures/hypercar/interior/INTERIOR_AO.png`
- `textures/hypercar/interior/INTERIOR_BaseColor.png`
- `textures/hypercar/interior/INTERIOR_Metallic.png`
- `textures/hypercar/interior/INTERIOR_Normal.png`
- `textures/hypercar/interior/INTERIOR_Roughness.png`
- `textures/hypercar/interior/speaker_perforation_Mask.png`
- `textures/hypercar/interior/speaker_perforation_Normal.png`
- `textures/hypercar/interior/stitch_Mask.png`
- `textures/hypercar/interior/stitch_Normal.png`
- `textures/hypercar/lights/LIGHTS_AO.png`
- `textures/hypercar/lights/LIGHTS_BaseColor.png`
- `textures/hypercar/lights/LIGHTS_Metallic.png`
- `textures/hypercar/lights/LIGHTS_Normal.png`
- `textures/hypercar/lights/LIGHTS_Roughness.png`
- `textures/hypercar/tires/TIRES_AO.png`
- `textures/hypercar/tires/TIRES_BaseColor.png`
- `textures/hypercar/tires/TIRES_Metallic.png`
- `textures/hypercar/tires/TIRES_Normal.png`
- `textures/hypercar/tires/TIRES_Roughness.png`
- `textures/hypercar/tires/tire_sidewall_Mask.png`
- `textures/hypercar/tires/tire_sidewall_Normal.png`
- `textures/hypercar/trim/TRIM_AO.png`
- `textures/hypercar/trim/TRIM_BaseColor.png`
- `textures/hypercar/trim/TRIM_Metallic.png`
- `textures/hypercar/trim/TRIM_Normal.png`
- `textures/hypercar/trim/TRIM_Roughness.png`
- `textures/hypercar/trim/carbon_twill_BaseColor.png`
- `textures/hypercar/trim/carbon_twill_Normal.png`
- `textures/hypercar/wheels/WHEELS_AO.png`
- `textures/hypercar/wheels/WHEELS_BaseColor.png`
- `textures/hypercar/wheels/WHEELS_Metallic.png`
- `textures/hypercar/wheels/WHEELS_Normal.png`
- `textures/hypercar/wheels/WHEELS_Roughness.png`

## Colliders (`Collision` empty, 6 convex meshes, 392 triangles total)
| Collider | tris | verts |
|---|---|---|
| Collision_Front | 74 | 39 |
| Collision_Body | 52 | 28 |
| Collision_Side_L | 64 | 34 |
| Collision_Side_R | 66 | 35 |
| Collision_Cabin | 60 | 32 |
| Collision_Rear | 76 | 40 |

All convex (<= 255 triangles each), closed, outward normals: add MeshCollider with **Convex ON** to each, disable their
MeshRenderers (they carry no material and no UVs), and put them on a vehicle physics layer.

## Animated / pivot objects (no animation data exported, pivots only)
| Object | Pivot | Axis (Unity local) | Range |
|---|---|---|---|
| `Wheel_FL/FR/RL/RR_LOD0-3` | wheel centre | X (roll) | continuous |
| `SteerPivot_FL/FR_LOD0-3` | wheel centre | Y (yaw) | -25 .. +25 deg |
| `SteeringWheel_LOD0-2` | column hub, Blender (0.36, -0.2, 0.645) | Y (shaft) | ~ +/-270 deg (ratio to taste) |
| `Paddle_L/R_LOD0-1` | paddle hinge | as authored | small pull |
| `Door_L/R_LOD0-1` (+ panel, window, handle) | hinge, Blender (+/-0.9, -0.95, 0.8) | X | 0 .. 15-20 deg (validated 18) |
| `ActiveSpoiler_LOD0-3` | hinge, Blender (0, 1.884, 0.8735) | X | 3 deg rest .. 18 deg deployed |

## Suggested Unity hierarchy (not built: Unity work starts after approval)
```
Hypercar (prefab root) = Car_Root   [Rigidbody, LOD Group, vehicle controller]
 |- LOD0_Root .. LOD3_Root          [render meshes; animated pivots inside]
 |- Collision                       [6 x MeshCollider convex, renderers off]
 |- WheelColliders (new)            [4 x WheelCollider placed at WheelColliderRef_*]
 |- WheelColliderRef_FL/FR/RL/RR    [position references, can be removed after setup]
 '- CenterOfMass                    [read by script -> rigidbody.centerOfMass]
```

---

## `new_car/reports/unity_material_mapping.md`

_Material categories mapped to Unity setup (paint, glass, lenses, light channels, interior, tire, brakes)_

# Unity material mapping (Phase 9)

Smoothness rule: **Unity Smoothness ~= 1 - Blender Roughness** (paint 0.20 -> ~0.80). Unity Lit reads smoothness from the Metallic map's alpha: pack `R = Metallic`, `A = 1 - Roughness` (invert the *_Roughness.png). Normal maps are **OpenGL (+Y)**: set Texture Type = Normal map, no green flip needed in Unity. BaseColor = sRGB; Metallic, Roughness, Normal, AO = linear (sRGB off). AO (*_AO.png) is not referenced by the FBX: assign it to Occlusion by hand.

| Category | FBX material | Unity setup | Blender values -> Unity |
|---|---|---|---|
| Car Paint | `LODMAT_Body_Paint` | Lit Opaque; BaseMap BODY_BaseColor; Metallic+Smoothness from BODY_Metallic / 1-BODY_Roughness (pack: R=metal, A=1-rough); Normal BODY_Normal; Occlusion BODY_AO. HDRP: enable Clear Coat 0.58 / URP: use a clear-coat capable car-paint shader | RacingRed base (0.80, 0.010, 0.024) linear, roughness 0.20 -> smoothness ~0.80, metallic 0.85, coat 0.58. Alt paints: ElectricBlue r0.20 m0.85, PearlWhite r0.25 (0.75) m0.30, SatinBlack r0.45 (0.55) m0.45 |
| Carbon (exterior) | `MAT_CarbonExterior` | Lit Opaque; BaseMap carbon_twill_BaseColor (tiling as authored); Normal carbon_twill_Normal; clear coat 1.0 | roughness 0.32 -> smoothness 0.68, metallic 0 |
| Metal / trim | `LODMAT_Trim, LODMAT_Wheels` | Lit Opaque; TRIM_* / WHEELS_* atlas (BaseColor, Metallic, Roughness->Smoothness, Normal, AO) | machined 0.16 -> 0.84 (m1.0), graphite 0.30 -> 0.70 (m1.0), dark barrel 0.50 -> 0.50 (m0.8), exhaust 0.24 -> 0.76 (m1.0), black trim 0.45 -> 0.55 |
| Tire | `LODMAT_Tire` | Lit Opaque; TIRES_* atlas; sidewall detail already baked into TIRES_Normal | base (0.032, 0.032, 0.034), roughness ~0.85 (baked map) -> smoothness ~0.15, metallic 0 |
| Brake Rotor | `LODMAT_Brakes` | Lit Opaque; BRAKES_* atlas | roughness 0.45 -> 0.55, metallic 0.35 |
| Caliper | `MAT_BrakeCaliper` | Lit Opaque, solid colour (kept separate for colour option) | base (0.80, 0.50, 0.015), roughness 0.32 -> 0.68, metallic 0, coat 0.6 |
| Glass | `LODMAT_Glass` | Lit Transparent (Alpha ~0.15-0.25, Preserve specular), double-sided off; GLASS_* atlas tint | Blender uses transmission 1.0 / IOR 1.46, roughness 0.02 -> 0.98. Unity has no refraction in URP: use alpha |
| Headlight Lens | `MAT_HeadlightLens` | Lit Transparent, Alpha ~0.1 | base 0.97, roughness 0.0 -> 1.0, transmission 1.0 / IOR 1.49 |
| Taillight Lens | `MAT_TaillightLens` | Lit Transparent, Alpha ~0.35, red tint | base (0.42, 0.10, 0.10), roughness 0.03 -> 0.97, transmission 1.0 |
| Emission (light channels) | `MAT_LED_White, MAT_ProjectorLens, MAT_LED_Red, MAT_LED_Brake, MAT_LED_Amber, MAT_LED_Reverse, MAT_AmbientLight` | Lit Opaque + Emission ON; ONE material per channel so scripts can switch headlight/tail/brake/indicator/reverse independently (set _EmissionColor intensity at runtime) | White em 6.0 (1,0.96,0.9), Red tail 5.0, Brake 1.2 (raise to ~8 when braking), Amber 0.8 (indicator), Reverse 0.25 (raise when reversing), Ambient 1.2; ProjectorLens r0.02 coat 1.0, no emission. Blender strength is not Unity nits/EV: re-tune with bloom |
| Leather | `LODMAT_Interior (baked)` | Lit Opaque; INTERIOR_* atlas (leather, alcantara, plastic, metal, seat accent baked together); stitch/perforation detail baked into INTERIOR_Normal | leather (0.020, 0.019, 0.019), roughness 0.42 -> 0.58 |
| Alcantara | `LODMAT_Interior (baked)` | same INTERIOR_* atlas | (0.040, 0.040, 0.043), roughness 0.95 -> 0.05 |
| Interior Carbon | `MAT_InteriorCarbon` | Lit Opaque; carbon_twill_* textures; coat 0.8 | roughness 0.32 -> 0.68 |
| Display | `MAT_Display, MAT_DisplayGraphics, MAT_DisplayGraphics_Red` | Lit Opaque + Emission (or Unlit); swap BaseMap for a RenderTexture to drive live gauges | screen base (0.006, 0.008, 0.012) r0.25 em 0.6; graphics em 1.4 (blue-white) / 1.6 (red) |
| Interior mirror | `MAT_InteriorMirror` | Lit Opaque, metallic 1, smoothness 0.98 (or planar reflection) | roughness 0.02 -> 0.98 |

FBX material slots per LOD (LOD0): 24 - `LODMAT_Body_Paint`, `LODMAT_Brakes`, `LODMAT_Glass`, `LODMAT_Interior`, `LODMAT_Lights`, `LODMAT_Tire`, `LODMAT_Trim`, `LODMAT_Wheels`, `MAT_AmbientLight`, `MAT_BrakeCaliper`, `MAT_CarbonExterior`, `MAT_Display`, `MAT_DisplayGraphics`, `MAT_DisplayGraphics_Red`, `MAT_HeadlightLens`, `MAT_InteriorCarbon`, `MAT_InteriorMirror`, `MAT_LED_Amber`, `MAT_LED_Brake`, `MAT_LED_Red`, `MAT_LED_Reverse`, `MAT_LED_White`, `MAT_ProjectorLens`, `MAT_TaillightLens`

---

## `new_car/reports/material_merge_review.md`

_Which materials stay separate (runtime-driven light channels, paint, glass) and which merge into atlases_

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

---

## `new_car/reports/static_merge_review.md`

_Which parts were merged into static meshes and which stay separate (pivots, animated parts)_

# Static merge review (Phase 8): nothing merged yet

Goal: cut draw calls later without losing gameplay control. Objects are listed per LOD (same pattern LOD0-LOD3
unless noted).

## KEEP_SEPARATE (functional transforms or runtime control)

| Objects | Why |
|---|---|
| `Wheel_FL/FR/RL/RR_LODn` (+ child `Tire_*`, `BrakeDisc_*`) | roll on local X; tire + rotor ride on the wheel |
| `SteerPivot_FL/FR_LODn` (+ `Caliper_FL/FR`) | front steering yaw; calipers steer but never roll |
| `Caliper_RL/RR_LODn` | static, but keep separate for the caliper colour option (MAT_BrakeCaliper) |
| `SteeringWheel_LOD0/1/2` | rotates on its column axis (local Z) |
| `Paddle_L/R_LOD0/1` | separate pivots (paddle pull animation) |
| `Door_L/R_LOD0/1` + `DoorPanel_*`, `Window_F*`, `DoorHandle_*` | opening doors (hinge empties) |
| `ActiveSpoiler_LODn` | rotates about its hinge (default 3 deg) |
| `Headlight_*`, `Taillight_*` (MAT_LED_White / ProjectorLens / LED_Red / LED_Brake / LED_Amber / LED_Reverse) | independently switched light channels |
| `HeadlightLens_*`, `TaillightLens_*`, all glass | transparent pass; side windows move with doors |
| `InstrumentCluster`, `CenterScreen` (displays) | may be driven live by the game |
| `COLLIDERS` pieces | physics only, never merged with render meshes |

## SAFE_TO_MERGE_LATER (static, same LOD, no runtime control)

| Merge group | Members | Expected saving |
|---|---|---|
| Body static | `Body`, `Body_Buttress`, `ArchLip_*`, `Mirror_*` (+ `MirrorGlass_*` as a 2nd material) | ~8 objects -> 1 |
| Aero / trim static | `FrontSplitter`, `RearDiffuser`, `SideSkirt_*`, `SideIntakeVane_*`, `FrontIntakeVanes`, `RearVent_*`, `EngineVents`, `RearFascia_Trim`, `Exhaust_*`, `Chassis_*`, `ActiveSpoilerHinge` | ~14 objects -> 1 (1 trim atlas material + carbon) |
| Interior static | `Dashboard`, `Dashboard_Vents`, `CenterTunnel`, `CenterConsole`, `Seat_*`, `RearBulkhead`, `Headliner`, `PillarTrim`, `Interior_Tub`, `EngineBay_Detail`, `RearViewMirror`, `SteeringColumn`, `Pedal_*` | ~16 objects -> 1-2 (atlas + carbon + emissive strips) |
| Static light housings | housing/bezel parts of `Headlight_*` / `Taillight_*` | only if emitters are split into their own objects first |

Rule: merge per LOD, keep each merged object's origin at Car_Root / LOD root, and re-check UVs + material slots after
joining (all members already share their atlas UV layout, so no repack is needed).

---

## `new_car/reports/phase_07_validation.txt`

_LOD validation (triangle targets, silhouette, materials per LOD)_

```text
[PASS] LOD0: 206,329 tris (target 180,000-220,000), 57.1% below master
[PASS] LOD0 dims L4.6950 W2.0523 H1.1726 m (delta vs master mm: +0.0/+0.1/+0.4)
[PASS] Wheel_FL_LOD0 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_FR_LOD0 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RL_LOD0 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RR_LOD0 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] LOD0 wheelbase 2.7800 m
[PASS] LOD0 UVMap on 84/84 meshes 
[PASS] LOD0 empty material slots: none
[PASS] LOD0 zero-area faces: 0
[PASS] LOD0 loose vertices: 0
[PASS] Body_LOD0 normals outward: 88.4% of faces
[PASS] Body_LOD0 non-manifold (non-boundary) edges: 0 (window openings are intentional boundaries)
[PASS] LOD0 wheel/tire vs body intersections: none
[PASS] LOD0 hierarchy: orphans none, wrong subcollection none
[PASS] LOD0 left(+X)/right(-X) naming: consistent
[PASS] LOD0 material groups: 24; light channels separate: ['MAT_LED_Amber', 'MAT_LED_Brake', 'MAT_LED_Red', 'MAT_LED_Reverse', 'MAT_LED_White', 'MAT_ProjectorLens']
[PASS] LOD1: 107,212 tris (target 90,000-120,000), 77.7% below master
[PASS] LOD1 dims L4.6950 W2.0525 H1.1726 m (delta vs master mm: +0.0/+0.3/+0.4)
[PASS] Wheel_FL_LOD1 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_FR_LOD1 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RL_LOD1 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RR_LOD1 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] LOD1 wheelbase 2.7800 m
[PASS] LOD1 UVMap on 84/84 meshes 
[PASS] LOD1 empty material slots: none
[PASS] LOD1 zero-area faces: 0
[PASS] LOD1 loose vertices: 0
[PASS] Body_LOD1 normals outward: 87.3% of faces
[PASS] Body_LOD1 non-manifold (non-boundary) edges: 0 (window openings are intentional boundaries)
[PASS] LOD1 wheel/tire vs body intersections: none
[PASS] LOD1 hierarchy: orphans none, wrong subcollection none
[PASS] LOD1 left(+X)/right(-X) naming: consistent
[PASS] LOD1 material groups: 24; light channels separate: ['MAT_LED_Amber', 'MAT_LED_Brake', 'MAT_LED_Red', 'MAT_LED_Reverse', 'MAT_LED_White', 'MAT_ProjectorLens']
[PASS] LOD2: 53,807 tris (target 40,000-60,000), 88.8% below master
[PASS] LOD2 dims L4.6950 W2.0528 H1.1741 m (delta vs master mm: +0.0/+0.5/+2.8)
[PASS] Wheel_FL_LOD2 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_FR_LOD2 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RL_LOD2 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RR_LOD2 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] LOD2 wheelbase 2.7800 m
[PASS] LOD2 UVMap on 73/73 meshes 
[PASS] LOD2 empty material slots: none
[PASS] LOD2 zero-area faces: 0
[PASS] LOD2 loose vertices: 0
[PASS] Body_LOD2 normals outward: 85.6% of faces
[PASS] Body_LOD2 non-manifold (non-boundary) edges: 0 (window openings are intentional boundaries)
[PASS] LOD2 wheel/tire vs body intersections: none
[PASS] LOD2 hierarchy: orphans none, wrong subcollection none
[PASS] LOD2 left(+X)/right(-X) naming: consistent
[PASS] LOD2 material groups: 20; light channels separate: ['MAT_LED_Amber', 'MAT_LED_Brake', 'MAT_LED_Red', 'MAT_LED_Reverse', 'MAT_LED_White', 'MAT_ProjectorLens']
[PASS] LOD3: 17,779 tris (target 12,000-20,000), 96.3% below master
[PASS] LOD3 dims L4.6920 W2.0528 H1.1741 m (delta vs master mm: -3.0/+0.5/+0.9)
[PASS] Wheel_FL_LOD3 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_FR_LOD3 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RL_LOD3 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] Wheel_RR_LOD3 pivot offset 0.000 mm, rotation 0.00e+00 rad (roll axis = local X)
[PASS] LOD3 wheelbase 2.7800 m
[PASS] LOD3 UVMap on 38/38 meshes 
[PASS] LOD3 empty material slots: none
[PASS] LOD3 zero-area faces: 0
[PASS] LOD3 loose vertices: 0
[PASS] Body_LOD3 normals outward: 86.0% of faces
[PASS] Body_LOD3 non-manifold (non-boundary) edges: 0 (window openings are intentional boundaries)
[PASS] LOD3 wheel/tire vs body intersections: none
[PASS] LOD3 hierarchy: orphans none, wrong subcollection none
[PASS] LOD3 left(+X)/right(-X) naming: consistent
[PASS] LOD3 material groups: 15; light channels separate: ['MAT_LED_Amber', 'MAT_LED_Brake', 'MAT_LED_Red', 'MAT_LED_Reverse', 'MAT_LED_White', 'MAT_ProjectorLens']
[PASS] texture links resolve: 47 images, missing none
[PASS] normal maps tangent/OpenGL + Non-Color: ok
[PASS] REFERENCE_Master hidden from render (and excluded from view layer in the saved file)
[PASS] master file unchanged (sha1 eaf334d81404)
```

---

## `new_car/reports/phase_07_lod_counts.json`

_Triangles per category per LOD and material lists per LOD_

```json
{
 "Master": {
  "Body": 279090,
  "Wheels": 13840,
  "Tires": 73728,
  "Brakes": 10760,
  "Interior": 58781,
  "Glass": 25860,
  "Lights": 11050,
  "Aero/Trim": 8212
 },
 "LOD0": {
  "Body": 96140,
  "Wheels": 13840,
  "Tires": 18432,
  "Brakes": 8768,
  "Interior": 37759,
  "Glass": 12946,
  "Lights": 11050,
  "Aero/Trim": 7394
 },
 "LOD0_materials": [
  "LODMAT_Body_Paint",
  "LODMAT_Brakes",
  "LODMAT_Glass",
  "LODMAT_Interior",
  "LODMAT_Lights",
  "LODMAT_Tire",
  "LODMAT_Trim",
  "LODMAT_Wheels",
  "MAT_AmbientLight",
  "MAT_BrakeCaliper",
  "MAT_CarbonExterior",
  "MAT_Display",
  "MAT_DisplayGraphics",
  "MAT_DisplayGraphics_Red",
  "MAT_HeadlightLens",
  "MAT_InteriorCarbon",
  "MAT_InteriorMirror",
  "MAT_LED_Amber",
  "MAT_LED_Brake",
  "MAT_LED_Red",
  "MAT_LED_Reverse",
  "MAT_LED_White",
  "MAT_ProjectorLens",
  "MAT_TaillightLens"
 ],
 "LOD1": {
  "Body": 46768,
  "Wheels": 7608,
  "Tires": 10136,
  "Brakes": 4112,
  "Interior": 20142,
  "Glass": 7776,
  "Lights": 6092,
  "Aero/Trim": 4578
 },
 "LOD1_materials": [
  "LODMAT_Body_Paint",
  "LODMAT_Brakes",
  "LODMAT_Glass",
  "LODMAT_Interior",
  "LODMAT_Lights",
  "LODMAT_Tire",
  "LODMAT_Trim",
  "LODMAT_Wheels",
  "MAT_AmbientLight",
  "MAT_BrakeCaliper",
  "MAT_CarbonExterior",
  "MAT_Display",
  "MAT_DisplayGraphics",
  "MAT_DisplayGraphics_Red",
  "MAT_HeadlightLens",
  "MAT_InteriorCarbon",
  "MAT_InteriorMirror",
  "MAT_LED_Amber",
  "MAT_LED_Brake",
  "MAT_LED_Red",
  "MAT_LED_Reverse",
  "MAT_LED_White",
  "MAT_ProjectorLens",
  "MAT_TaillightLens"
 ],
 "LOD2": {
  "Body": 24502,
  "Wheels": 4840,
  "Tires": 5528,
  "Brakes": 1656,
  "Interior": 8342,
  "Glass": 3037,
  "Lights": 3348,
  "Aero/Trim": 2554
 },
 "LOD2_materials": [
  "LODMAT_Body_Paint",
  "LODMAT_Brakes",
  "LODMAT_Glass",
  "LODMAT_Interior",
  "LODMAT_Lights",
  "LODMAT_Tire",
  "LODMAT_Trim",
  "LODMAT_Wheels",
  "MAT_AmbientLight",
  "MAT_BrakeCaliper",
  "MAT_Display",
  "MAT_HeadlightLens",
  "MAT_InteriorMirror",
  "MAT_LED_Amber",
  "MAT_LED_Brake",
  "MAT_LED_Red",
  "MAT_LED_Reverse",
  "MAT_LED_White",
  "MAT_ProjectorLens",
  "MAT_TaillightLens"
 ],
 "LOD3": {
  "Body": 9802,
  "Wheels": 1656,
  "Tires": 1840,
  "Brakes": 580,
  "Interior": 1420,
  "Glass": 713,
  "Lights": 1276,
  "Aero/Trim": 492
 },
 "LOD3_materials": [
  "LODMAT_Body_Paint",
  "LODMAT_Brakes",
  "LODMAT_Glass",
  "LODMAT_Interior",
  "LODMAT_Lights",
  "LODMAT_Tire",
  "LODMAT_Trim",
  "LODMAT_Wheels",
  "MAT_BrakeCaliper",
  "MAT_LED_Amber",
  "MAT_LED_Brake",
  "MAT_LED_Red",
  "MAT_LED_Reverse",
  "MAT_LED_White",
  "MAT_ProjectorLens"
 ]
}
```

---

## `new_car/reports/phase_07_silhouette_iou.json`

_LOD silhouette IoU against LOD0_

```json
{
 "LOD0_vs_Master": {
  "side": 99.93,
  "front": 99.9,
  "rear": 99.87,
  "front_3q": 99.92,
  "rear_3q": 99.91
 },
 "LOD1_vs_LOD0": {
  "side": 99.94,
  "front": 99.9,
  "rear": 99.89,
  "front_3q": 99.93,
  "rear_3q": 99.92
 },
 "LOD2_vs_LOD0": {
  "side": 99.69,
  "front": 99.71,
  "rear": 99.67,
  "front_3q": 99.72,
  "rear_3q": 99.62
 },
 "LOD3_vs_LOD0": {
  "side": 99.57,
  "front": 99.45,
  "rear": 99.54,
  "front_3q": 99.51,
  "rear_3q": 99.47
 }
}
```

---

## `new_car/reports/phase_08_validation.txt`

_Colliders, hierarchy and pivot validation (wheel roll and steer tests, doors, spoiler)_

```text
[PASS] Car_Root at origin, rotation 0, scale 1, top level
[PASS] LOD0_Root under Car_Root with identity transform (LODs overlap exactly)
[PASS] LOD1_Root under Car_Root with identity transform (LODs overlap exactly)
[PASS] LOD2_Root under Car_Root with identity transform (LODs overlap exactly)
[PASS] LOD3_Root under Car_Root with identity transform (LODs overlap exactly)
[PASS] COLLIDERS collection + Collision root + 6 pieces parented
[PASS] CenterOfMass at (0.0, 0.12, 0.35) (centreline, rear-biased, low)
[PASS] WheelColliderRef_FL LEFT (+X) at [0.835, -1.39, 0.355], r=0.355 w=0.31
[PASS] WheelColliderRef_FR RIGHT (-X) at [-0.835, -1.39, 0.355], r=0.355 w=0.31
[PASS] WheelColliderRef_RL LEFT (+X) at [0.835, 1.39, 0.3775], r=0.3775 w=0.35
[PASS] WheelColliderRef_RR RIGHT (-X) at [-0.835, 1.39, 0.3775], r=0.3775 w=0.35
[PASS] Wheel_FL_LOD0: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_FR_LOD0: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_RL_LOD0: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] Wheel_RR_LOD0: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] SteerPivot_FL_LOD0: +/-25 deg yaw about wheel centre (err 0.0001 mm); caliper steers, does not roll
[PASS] SteerPivot_FR_LOD0: +/-25 deg yaw about wheel centre (err 0.0001 mm); caliper steers, does not roll
[PASS] Wheel_FL_LOD1: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_FR_LOD1: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_RL_LOD1: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] Wheel_RR_LOD1: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] SteerPivot_FL_LOD1: +/-25 deg yaw about wheel centre (err 0.0001 mm); caliper steers, does not roll
[PASS] SteerPivot_FR_LOD1: +/-25 deg yaw about wheel centre (err 0.0001 mm); caliper steers, does not roll
[PASS] Wheel_FL_LOD2: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_FR_LOD2: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_RL_LOD2: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] Wheel_RR_LOD2: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] SteerPivot_FL_LOD2: +/-25 deg yaw about wheel centre (err 0.0002 mm); caliper steers, does not roll
[PASS] SteerPivot_FR_LOD2: +/-25 deg yaw about wheel centre (err 0.0002 mm); caliper steers, does not roll
[PASS] Wheel_FL_LOD3: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_FR_LOD3: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0002 mm), axle X, caliper static on roll
[PASS] Wheel_RL_LOD3: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] Wheel_RR_LOD3: offset 0.0000 mm, roll +/-30 deg rigid (err 0.0001 mm), axle X, caliper static on roll
[PASS] SteerPivot_FL_LOD3: +/-25 deg yaw about wheel centre (err 0.0001 mm); caliper steers, does not roll
[PASS] SteerPivot_FR_LOD3: +/-25 deg yaw about wheel centre (err 0.0002 mm); caliper steers, does not roll
[PASS] SteeringWheel_LOD0: +/-30 deg about local Z (column axis (0.0, 0.91, 0.42)), wobble 0.0001 mm
[PASS] SteeringWheel_LOD1: +/-30 deg about local Z (column axis (0.0, 0.91, 0.42)), wobble 0.0001 mm
[PASS] SteeringWheel_LOD2: +/-30 deg about local Z (column axis (0.0, 0.91, 0.42)), wobble 0.0001 mm
[PASS] Door_L_LOD0 hinge [0.9, -0.95, 0.8]: 18 deg opening, 3 children follow rigidly
[PASS] Door_R_LOD0 hinge [-0.9, -0.95, 0.8]: 18 deg opening, 3 children follow rigidly
[PASS] Door_L_LOD1 hinge [0.9, -0.95, 0.8]: 18 deg opening, 3 children follow rigidly
[PASS] Door_R_LOD1 hinge [-0.9, -0.95, 0.8]: 18 deg opening, 3 children follow rigidly
[PASS] ActiveSpoiler_LOD0: 3 -> 18 deg about hinge, rise 4.9 cm, no translation, brackets static
[PASS] ActiveSpoiler_LOD1: 3 -> 18 deg about hinge, rise 4.9 cm, no translation, brackets static
[PASS] ActiveSpoiler_LOD2: 3 -> 18 deg about hinge, rise 4.9 cm, no translation, brackets static
[PASS] ActiveSpoiler_LOD3: 3 -> 18 deg about hinge, rise 4.9 cm, no translation, brackets static
[PASS] negative scales: none
[PASS] non-unit / non-uniform scales: none
[INFO] intentional rotations (11): ['ActiveSpoiler_LOD0', 'ActiveSpoiler_LOD1', 'ActiveSpoiler_LOD2', 'ActiveSpoiler_LOD3', 'Paddle_L_LOD0', 'Paddle_L_LOD1', 'Paddle_R_LOD0', 'Paddle_R_LOD1', 'SteeringWheel_LOD0', 'SteeringWheel_LOD1', 'SteeringWheel_LOD2']
[PASS] duplicate-suffixed names: none
[PASS] left(+X)/right(-X) naming across production objects: consistent
[PASS] Collision_Front: 74 tris, convex True, closed True, normals outward True
[PASS] Collision_Front fit: 9/39 verts outside LOD0 skin, max 7.4 mm
[PASS] Collision_Body: 52 tris, convex True, closed True, normals outward True
[PASS] Collision_Body fit: 0/28 verts outside LOD0 skin, max 0.0 mm
[PASS] Collision_Side_L: 64 tris, convex True, closed True, normals outward True
[PASS] Collision_Side_L fit: 11/34 verts outside LOD0 skin, max 2.8 mm
[PASS] Collision_Side_R: 66 tris, convex True, closed True, normals outward True
[PASS] Collision_Side_R fit: 10/35 verts outside LOD0 skin, max 2.8 mm
[PASS] Collision_Cabin: 60 tris, convex True, closed True, normals outward True
[PASS] Collision_Cabin fit: 4/32 verts outside LOD0 skin, max 4.8 mm
[PASS] Collision_Rear: 76 tris, convex True, closed True, normals outward True
[PASS] Collision_Rear fit: 11/40 verts outside LOD0 skin, max 8.2 mm
[PASS] collider total 392 triangles (target ~100-500)
[PASS] LOD0: 206,329 tris (phase 7: 206,329); L4.6950 W2.0523 H1.1726 m
[PASS] LOD0 UVMap + material slots on all 84 meshes
[PASS] LOD0 independent light channels present: 6/6; material groups 24
[PASS] LOD1: 107,212 tris (phase 7: 107,212); L4.6950 W2.0525 H1.1726 m
[PASS] LOD1 UVMap + material slots on all 84 meshes
[PASS] LOD1 independent light channels present: 6/6; material groups 24
[PASS] LOD2: 53,807 tris (phase 7: 53,807); L4.6950 W2.0528 H1.1741 m
[PASS] LOD2 UVMap + material slots on all 73 meshes
[PASS] LOD2 independent light channels present: 6/6; material groups 20
[PASS] LOD3: 17,779 tris (phase 7: 17,779); L4.6920 W2.0528 H1.1741 m
[PASS] LOD3 UVMap + material slots on all 38 meshes
[PASS] LOD3 independent light channels present: 6/6; material groups 15
[PASS] side glass rides on the door hinges (LOD0/LOD1)
[PASS] textures: missing none, absolute paths none
[PASS] every object under Car_Root is in GAME_ASSET (308 objects)
[PASS] GAME_ASSET objects outside Car_Root hierarchy: none
[PASS] REFERENCE_Master excluded (view layer + render), not in GAME_ASSET, no master object under Car_Root
[PASS] no studio/camera/cutter helpers in GAME_ASSET: none
[PASS] checkpoint 06 unchanged (sha1 875e57736aab)
[INFO] export manifest: 308 objects, roles {'body': 32, 'brakes': 32, 'center_of_mass': 1, 'collider': 6, 'collider_root': 1, 'door_hinge_pivot': 4, 'glass': 34, 'interior': 65, 'lights': 28, 'lod_root': 4, 'root': 1, 'spoiler (pivot = hinge)': 4, 'steering_pivot': 8, 'tires': 16, 'trim': 52, 'wheel (rolls local X)': 16, 'wheel_collider_reference': 4}
SUMMARY: 82 PASS, 0 WARNING, 0 ERROR
```

---

## `new_car/reports/collider_stats.json`

_Collider pieces and triangle counts_

```json
{
 "Collision_Front": {
  "triangles": 74,
  "vertices": 39,
  "grid_cell_m": 0.435,
  "bbox_min": [
   -0.9777,
   -2.38,
   0.1338
  ],
  "bbox_max": [
   0.9778,
   -0.8363,
   0.7666
  ],
  "max_convexity_violation_mm": 0.0001,
  "convex": true,
  "closed_manifold": true,
  "outward_normals": true,
  "verts_outside_LOD0_body": 9,
  "max_outside_mm": 7.4
 },
 "Collision_Body": {
  "triangles": 52,
  "vertices": 28,
  "grid_cell_m": 0.04,
  "bbox_min": [
   -0.6439,
   -0.7526,
   0.1344
  ],
  "bbox_max": [
   0.6439,
   0.6072,
   0.7926
  ],
  "max_convexity_violation_mm": 0.1052,
  "convex": true,
  "closed_manifold": true,
  "outward_normals": true,
  "verts_outside_LOD0_body": 0,
  "max_outside_mm": 0
 },
 "Collision_Side_L": {
  "triangles": 64,
  "vertices": 34,
  "grid_cell_m": 0.074,
  "bbox_min": [
   0.4643,
   -0.9349,
   0.1346
  ],
  "bbox_max": [
   0.9998,
   0.9822,
   0.814
  ],
  "max_convexity_violation_mm": 0.8303,
  "convex": true,
  "closed_manifold": true,
  "outward_normals": true,
  "verts_outside_LOD0_body": 11,
  "max_outside_mm": 2.8
 },
 "Collision_Side_R": {
  "triangles": 66,
  "vertices": 35,
  "grid_cell_m": 0.074,
  "bbox_min": [
   -0.9997,
   -0.9348,
   0.1346
  ],
  "bbox_max": [
   -0.4642,
   0.9823,
   0.8142
  ],
  "max_convexity_violation_mm": 0.0475,
  "convex": true,
  "closed_manifold": true,
  "outward_normals": true,
  "verts_outside_LOD0_body": 10,
  "max_outside_mm": 2.8
 },
 "Collision_Cabin": {
  "triangles": 60,
  "vertices": 32,
  "grid_cell_m": 0.217,
  "bbox_min": [
   -0.9139,
   -0.6899,
   0.7684
  ],
  "bbox_max": [
   0.9139,
   0.5606,
   1.1668
  ],
  "max_convexity_violation_mm": 0.0672,
  "convex": true,
  "closed_manifold": true,
  "outward_normals": true,
  "verts_outside_LOD0_body": 4,
  "max_outside_mm": 4.8
 },
 "Collision_Rear": {
  "triangles": 76,
  "vertices": 40,
  "grid_cell_m": 0.403,
  "bbox_min": [
   -1.0008,
   0.6431,
   0.1361
  ],
  "bbox_max": [
   1.0009,
   2.2328,
   1.0767
  ],
  "max_convexity_violation_mm": 0.0002,
  "convex": true,
  "closed_manifold": true,
  "outward_normals": true,
  "verts_outside_LOD0_body": 11,
  "max_outside_mm": 8.2
 },
 "_total_triangles": 392,
 "_method": "convex hull of representative Body_LOD2 surface points per region, 15 mm inset, re-hulled (convex by construction)"
}
```

---

## `new_car/reports/wheel_reference_points.json`

_Wheel centres, radii and widths_

```json
{
 "FL": {
  "world_position": [
   0.835,
   -1.39,
   0.355
  ],
  "local_to_Car_Root": [
   0.835,
   -1.39,
   0.355
  ],
  "radius_m": 0.355,
  "diameter_m": 0.71,
  "width_m": 0.31,
  "axle_direction_world": [
   1.0,
   0.0,
   0.0
  ],
  "side": "LEFT (+X)"
 },
 "FR": {
  "world_position": [
   -0.835,
   -1.39,
   0.355
  ],
  "local_to_Car_Root": [
   -0.835,
   -1.39,
   0.355
  ],
  "radius_m": 0.355,
  "diameter_m": 0.71,
  "width_m": 0.31,
  "axle_direction_world": [
   1.0,
   0.0,
   0.0
  ],
  "side": "RIGHT (-X)"
 },
 "RL": {
  "world_position": [
   0.835,
   1.39,
   0.3775
  ],
  "local_to_Car_Root": [
   0.835,
   1.39,
   0.3775
  ],
  "radius_m": 0.3775,
  "diameter_m": 0.755,
  "width_m": 0.35,
  "axle_direction_world": [
   1.0,
   0.0,
   0.0
  ],
  "side": "LEFT (+X)"
 },
 "RR": {
  "world_position": [
   -0.835,
   1.39,
   0.3775
  ],
  "local_to_Car_Root": [
   -0.835,
   1.39,
   0.3775
  ],
  "radius_m": 0.3775,
  "diameter_m": 0.755,
  "width_m": 0.35,
  "axle_direction_world": [
   1.0,
   0.0,
   0.0
  ],
  "side": "RIGHT (-X)"
 },
 "_wheelbase_m": 2.78,
 "_track_m": {
  "front": 1.67,
  "rear": 1.67
 }
}
```

---

## `new_car/reports/fbx_export_settings.json`

_Exact FBX exporter settings used_

```json
{
 "settings": {
  "use_selection": true,
  "object_types": [
   "EMPTY",
   "MESH"
  ],
  "use_active_collection": false,
  "global_scale": 1.0,
  "apply_unit_scale": true,
  "apply_scale_options": "FBX_SCALE_ALL",
  "axis_forward": "-Z",
  "axis_up": "Y",
  "bake_space_transform": false,
  "use_mesh_modifiers": true,
  "use_mesh_modifiers_render": true,
  "mesh_smooth_type": "FACE",
  "use_subsurf": false,
  "use_mesh_edges": false,
  "use_tspace": true,
  "use_triangles": false,
  "use_custom_props": false,
  "add_leaf_bones": false,
  "primary_bone_axis": "Y",
  "secondary_bone_axis": "X",
  "use_armature_deform_only": false,
  "bake_anim": false,
  "path_mode": "RELATIVE",
  "embed_textures": false,
  "batch_mode": "OFF"
 },
 "files": {
  "hypercar_LOD0_unity_test.fbx": {
   "objects": 102,
   "bytes": 10928972,
   "leaked_selection": [],
   "sha1": "18a281c3dea09a7b0b42cd4dc9d7c6af940b153d"
  },
  "hypercar_complete_unity.fbx": {
   "objects": 308,
   "bytes": 22078332,
   "leaked_selection": [],
   "sha1": "58f0edbf6fe59d297df902e11f0ab4bb92252463"
  }
 },
 "export_time_ngon_triangulated_meshes": [
  "ArchLip_FL_LOD0",
  "ArchLip_FL_LOD1",
  "ArchLip_FR_LOD0",
  "ArchLip_FR_LOD1",
  "ArchLip_RL_LOD0",
  "ArchLip_RL_LOD1",
  "ArchLip_RR_LOD0",
  "ArchLip_RR_LOD1",
  "Body_LOD0",
  "Body_LOD1",
  "Body_LOD2",
  "Body_LOD3",
  "BrakeDisc_FL_LOD0",
  "BrakeDisc_FR_LOD0",
  "BrakeDisc_RL_LOD0",
  "BrakeDisc_RR_LOD0",
  "Caliper_FL_LOD0",
  "Caliper_FL_LOD1",
  "Caliper_FL_LOD2",
  "Caliper_FL_LOD3",
  "Caliper_FR_LOD0",
  "Caliper_FR_LOD1",
  "Caliper_FR_LOD2",
  "Caliper_FR_LOD3",
  "Caliper_RL_LOD0",
  "Caliper_RL_LOD1",
  "Caliper_RL_LOD2",
  "Caliper_RL_LOD3",
  "Caliper_RR_LOD0",
  "Caliper_RR_LOD1",
  "Caliper_RR_LOD2",
  "Caliper_RR_LOD3",
  "CenterConsole_LOD0",
  "CenterConsole_LOD1",
  "CenterConsole_LOD2",
  "CenterTunnel_LOD0",
  "CenterTunnel_LOD1",
  "CenterTunnel_LOD2",
  "Dashboard_LOD1",
  "Dashboard_LOD2",
  "Dashboard_Vents_LOD0",
  "Dashboard_Vents_LOD1",
  "Dashboard_Vents_LOD2",
  "DoorPanel_L_LOD0",
  "DoorPanel_L_LOD1",
  "DoorPanel_L_LOD2",
  "DoorPanel_R_LOD0",
  "DoorPanel_R_LOD1",
  "DoorPanel_R_LOD2",
  "EngineBay_Detail_LOD0",
  "EngineBay_Detail_LOD1",
  "EngineBay_Detail_LOD2",
  "Exhaust_L_LOD0",
  "Exhaust_L_LOD1",
  "Exhaust_L_LOD2",
  "Exhaust_R_LOD0",
  "Exhaust_R_LOD1",
  "Exhaust_R_LOD2",
  "Headlight_L_LOD0",
  "Headlight_L_LOD1",
  "Headlight_L_LOD2",
  "Headlight_L_LOD3",
  "Headlight_R_LOD0",
  "Headlight_R_LOD1",
  "Headlight_R_LOD2",
  "Headlight_R_LOD3",
  "InstrumentCluster_LOD0",
  "InstrumentCluster_LOD1",
  "InstrumentCluster_LOD2",
  "Interior_LOD3",
  "MirrorGlass_L_LOD0",
  "MirrorGlass_L_LOD1",
  "MirrorGlass_L_LOD2",
  "MirrorGlass_R_LOD0",
  "MirrorGlass_R_LOD1",
  "MirrorGlass_R_LOD2",
  "Mirror_L_LOD1",
  "Mirror_L_LOD2",
  "Mirror_L_LOD3",
  "Mirror_R_LOD1",
  "Mirror_R_LOD2",
  "Mirror_R_LOD3",
  "Paddle_L_LOD0",
  "Paddle_L_LOD1",
  "Paddle_R_LOD0",
  "Paddle_R_LOD1",
  "Pedal_Brake_Arm_LOD0",
  "Pedal_Brake_Arm_LOD1",
  "PillarTrim_LOD0",
  "PillarTrim_LOD1",
  "PillarTrim_LOD2",
  "RearBulkhead_LOD0",
  "RearBulkhead_LOD1",
  "RearBulkhead_LOD2",
  "RearDiffuser_LOD0",
  "RearDiffuser_LOD1",
  "RearDiffuser_LOD2",
  "RearDiffuser_LOD3",
  "RearViewMirror_LOD0",
  "RearViewMirror_LOD1",
  "Seat_Driver_LOD1",
  "Seat_Driver_LOD2",
  "Seat_Passenger_LOD1",
  "Seat_Passenger_LOD2",
  "SteeringColumn_LOD0",
  "SteeringColumn_LOD1",
  "SteeringWheel_LOD0",
  "SteeringWheel_LOD1",
  "SteeringWheel_LOD2",
  "Taillight_L_LOD0",
  "Taillight_L_LOD1",
  "Taillight_L_LOD2",
  "Taillight_L_LOD3",
  "Taillight_R_LOD0",
  "Taillight_R_LOD1",
  "Taillight_R_LOD2",
  "Taillight_R_LOD3",
  "Wheel_FL_LOD0",
  "Wheel_FL_LOD1",
  "Wheel_FL_LOD2",
  "Wheel_FL_LOD3",
  "Wheel_FR_LOD0",
  "Wheel_FR_LOD1",
  "Wheel_FR_LOD2",
  "Wheel_FR_LOD3",
  "Wheel_RL_LOD0",
  "Wheel_RL_LOD1",
  "Wheel_RL_LOD2",
  "Wheel_RL_LOD3",
  "Wheel_RR_LOD0",
  "Wheel_RR_LOD1",
  "Wheel_RR_LOD2",
  "Wheel_RR_LOD3"
 ],
 "duplicate_triangles_removed": {
  "Caliper_FL_LOD3": 3,
  "InstrumentCluster_LOD1": 2,
  "Caliper_FR_LOD3": 2,
  "CenterConsole_LOD2": 6,
  "InstrumentCluster_LOD2": 2,
  "Body_LOD2": 7,
  "Body_LOD0": 2,
  "Interior_LOD3": 21,
  "Interior_Tub_LOD2": 6,
  "Caliper_RL_LOD3": 5,
  "Caliper_RR_LOD3": 1
 }
}
```

---

## `new_car/reports/fbx_validation_complete.txt`

_Clean re-import validation of the complete FBX (Blender space + raw Unity space)_

```text
== hypercar_complete_unity.fbx (complete) ==
[PASS] imported 308 objects into a clean scene (285 meshes, 23 empties)
[PASS] no .001-style or duplicate names: ok
[PASS] no master/studio/cutter leakage: clean
[PASS] scales: Car_Root (1.0, 1.0, 1.0), negative none, non-1 none
[PASS] Car_Root position (0.0, 0.0, 0.0)
[PASS] LOD0_Root under Car_Root, offset 0.000 mm
[PASS] LOD1_Root under Car_Root, offset 0.000 mm
[PASS] LOD2_Root under Car_Root, offset 0.000 mm
[PASS] LOD3_Root under Car_Root, offset 0.000 mm
[PASS] LOD0 re-import dims L4.6950 W2.0523 H1.1726 m (delta mm -0.00/+0.03/-0.02)
[PASS] LOD0 triangles 206,327 (Phase 7 206,329 - coincident duplicates removed at export {'Body_LOD0': 2})
[PASS] LOD0 UVMap on 84/84 meshes 
[PASS] LOD0 material slots filled on all meshes 
[PASS] LOD0 24 material groups survive; 6 light channels, paint, glass, tire, caliper distinct
[PASS] LOD1 re-import dims L4.6950 W2.0525 H1.1726 m (delta mm -0.00/+0.02/-0.02)
[PASS] LOD1 triangles 107,210 (Phase 7 107,212 - coincident duplicates removed at export {'InstrumentCluster_LOD1': 2})
[PASS] LOD1 UVMap on 84/84 meshes 
[PASS] LOD1 material slots filled on all meshes 
[PASS] LOD1 24 material groups survive; 6 light channels, paint, glass, tire, caliper distinct
[PASS] LOD2 re-import dims L4.6950 W2.0528 H1.1741 m (delta mm -0.00/-0.05/+0.00)
[PASS] LOD2 triangles 53,786 (Phase 7 53,807 - coincident duplicates removed at export {'CenterConsole_LOD2': 6, 'InstrumentCluster_LOD2': 2, 'Body_LOD2': 7, 'Interior_Tub_LOD2': 6})
[PASS] LOD2 UVMap on 73/73 meshes 
[PASS] LOD2 material slots filled on all meshes 
[PASS] LOD2 20 material groups survive; 6 light channels, paint, glass, tire, caliper distinct
[PASS] LOD3 re-import dims L4.6920 W2.0528 H1.1741 m (delta mm +0.01/-0.05/+0.00)
[PASS] LOD3 triangles 17,747 (Phase 7 17,779 - coincident duplicates removed at export {'Caliper_FL_LOD3': 3, 'Caliper_FR_LOD3': 2, 'Interior_LOD3': 21, 'Caliper_RL_LOD3': 5, 'Caliper_RR_LOD3': 1})
[PASS] LOD3 UVMap on 38/38 meshes 
[PASS] LOD3 material slots filled on all meshes 
[PASS] LOD3 15 material groups survive; 6 light channels, paint, glass, tire, caliper distinct
[PASS] WheelColliderRef_FL at (0.835, -1.39, 0.355) (source delta 0.000 mm)
[PASS] WheelColliderRef_FR at (-0.835, -1.39, 0.355) (source delta 0.000 mm)
[PASS] WheelColliderRef_RL at (0.835, 1.39, 0.3775) (source delta 0.000 mm)
[PASS] WheelColliderRef_RR at (-0.835, 1.39, 0.3775) (source delta 0.000 mm)
[PASS] wheelbase 2.78000 m (delta -0.000 mm)
[PASS] Wheel_FL_LOD0: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_FR_LOD0: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RL_LOD0: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RR_LOD0: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] SteerPivot_FL_LOD0: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] SteerPivot_FR_LOD0: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] Wheel_FL_LOD1: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_FR_LOD1: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RL_LOD1: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RR_LOD1: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] SteerPivot_FL_LOD1: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] SteerPivot_FR_LOD1: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] Wheel_FL_LOD2: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_FR_LOD2: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RL_LOD2: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RR_LOD2: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] SteerPivot_FL_LOD2: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] SteerPivot_FR_LOD2: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] Wheel_FL_LOD3: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_FR_LOD3: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RL_LOD3: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] Wheel_RR_LOD3: pivot 0.000 mm, roll +/-30 rigid (err 0.0001 mm), tire+rotor follow, caliper static, axle along vehicle X
[PASS] SteerPivot_FL_LOD3: -25/0/+25 deg yaw about wheel centre (err 0.0002 mm), caliper steers but not rolls, roll works while steered
[PASS] SteerPivot_FR_LOD3: -25/0/+25 deg yaw about wheel centre (err 0.0001 mm), caliper steers but not rolls, roll works while steered
[PASS] SteeringWheel_LOD0: origin delta 0.000 mm, shaft axis delta 0.0000 deg, wobble 0.0001 mm
[PASS] SteeringWheel_LOD1: origin delta 0.000 mm, shaft axis delta 0.0000 deg, wobble 0.0001 mm
[PASS] SteeringWheel_LOD2: origin delta 0.000 mm, shaft axis delta 0.0000 deg, wobble 0.0001 mm
[PASS] Door_L_LOD0: hinge delta 0.000 mm, 18 deg open, ['DoorHandle_L_LOD0', 'DoorPanel_L_LOD0', 'Window_FL_LOD0'] follow (err 0.0002 mm)
[PASS] Door_R_LOD0: hinge delta 0.000 mm, 18 deg open, ['DoorHandle_R_LOD0', 'DoorPanel_R_LOD0', 'Window_FR_LOD0'] follow (err 0.0002 mm)
[PASS] Door_L_LOD1: hinge delta 0.000 mm, 18 deg open, ['DoorHandle_L_LOD1', 'DoorPanel_L_LOD1', 'Window_FL_LOD1'] follow (err 0.0002 mm)
[PASS] Door_R_LOD1: hinge delta 0.000 mm, 18 deg open, ['DoorHandle_R_LOD1', 'DoorPanel_R_LOD1', 'Window_FR_LOD1'] follow (err 0.0003 mm)
[PASS] ActiveSpoiler_LOD0: hinge delta 0.019 mm, 3->18 deg rise 4.9 cm, err 0.0002 mm
[PASS] ActiveSpoiler_LOD1: hinge delta 0.019 mm, 3->18 deg rise 4.9 cm, err 0.0002 mm
[PASS] ActiveSpoiler_LOD2: hinge delta 0.019 mm, 3->18 deg rise 4.9 cm, err 0.0002 mm
[PASS] ActiveSpoiler_LOD3: hinge delta 0.019 mm, 3->18 deg rise 4.9 cm, err 0.0002 mm
[PASS] Collision_Front: 74 tris, convex (viol 0.000 mm), normals outward, placement delta 0.0 mm
[PASS] Collision_Body: 52 tris, convex (viol 0.105 mm), normals outward, placement delta 0.0 mm
[PASS] Collision_Side_L: 64 tris, convex (viol 0.830 mm), normals outward, placement delta 0.0 mm
[PASS] Collision_Side_R: 66 tris, convex (viol 0.047 mm), normals outward, placement delta 0.0 mm
[PASS] Collision_Cabin: 60 tris, convex (viol 0.067 mm), normals outward, placement delta 0.0 mm
[PASS] Collision_Rear: 76 tris, convex (viol 0.000 mm), normals outward, placement delta 0.0 mm
[PASS] collider total 392 triangles (source 392)
[PASS] CenterOfMass physical position (Blender frame) (0.0, 0.12, 0.35)
[PASS] shading normals vs source on hero meshes (5314 samples): 99th pct 0.000 deg, flipped 0
[PASS] UVMap present on every imported render mesh
[PASS] 6 colliders: physics-only (no UVs / materials required)
[PASS] Unity view: Car_Root rotation [-0.0, -0.0, 0.0] scale [1.0, 1.0, 1.0] (no 90 deg / 100x)
[PASS] Unity view: nose at +Z (2.397), tail -2.249, roof +Y (1.173) -> car faces +Z, upright
[PASS] Unity view: driver seat FBX x +0.360, front-left wheel FBX (+0.835, 0.355, +1.390); Unity negates FBX x -> vehicle left = Unity -X, LHD driver on the left
[PASS] Unity view: CenterOfMass FBX [0.0, 0.35, -0.12] -> Unity (0, 0.35, -0.12): low, 0.12 m behind mid-wheelbase
[PASS] Unity view local pivot axes: wheel roll = local X, steer yaw = local Y (= world up), steering shaft = local Y (max err 1.99e-05)
SUMMARY hypercar_complete_unity.fbx: 85 PASS, 0 WARNING, 0 ERROR
```
