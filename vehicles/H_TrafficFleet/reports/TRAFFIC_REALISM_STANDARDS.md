# Traffic fleet — realism standard (Phase H0)

The visual-quality standard for every traffic vehicle (H1–H9). **Technical validation never overrides visual rejection.**

## 1. Audit: why the current player cars look procedural

**Method.**
- Read-only inspection of the frozen player cars (meshes, materials, build scripts).
- The existing Eevee review renders.
- A new **Cycles studio** render of the frozen Vortex R r1 (`previews/h0_audit/VXr1_*.png`), to separate *rendering* problems from *asset* problems.
- **Finding:** even under proper studio lighting, Vortex R still reads as plastic and simplified. Better rendering helps reflections a little; **most of the problem is in the asset.**

| # | Symptom (seen in the renders) | Root cause | Category |
|---|---|---|---|
| 1 | Headlights, tail lights and vents look **pasted on** | Details were built as thin patches projected onto the skin (`quad_patch`). There is no housing depth, no lens volume and no internal reflector or projector. Tail lights are flat emissive bars | Geometry |
| 2 | Intakes and grilles look like **flat dark panels** | Openings are shallow prism pockets with one flat back plate in a single palette colour. There are no layered vanes or mesh with depth, no AO in the cavity, and no edge thickness | Geometry + texturing |
| 3 | **Bumpers read as part of a soap bar** | The whole body is one lofted shell. Nose and tail are scaled-down rings (rounded "pillow" ends). There is no crisp front or rear face, no bumper-to-fender split, no bumper lip thickness and no lower-valance step | Geometry |
| 4 | **Wheels look like toys** | Spokes are extruded quads with no window chamfer or rim dish. The rim lip has no depth. The tire is a smooth revolve with weak shoulder and sidewall bulge, uniform black, with no lettering, wear or tread readability. One flat swatch colour per part | Geometry + materials |
| 5 | Wing supports and exhausts look **artificial** | Pylons are square tubes; exhaust tips are two thin rings with no tip wall, inner pipe or heat tint | Geometry + materials |
| 6 | **Windows read as black painted surfaces** | Glass is a single sheet in the same surface as the body (no inset, seal or frit band), with alpha 0.66 near-black tint, so the cabin reads as a black cavity | Geometry + materials |
| 7 | **Paint looks like plastic** | Satin paint (roughness 0.36, coat 0.35) has no flake, no orange-peel and no sharp clear-coat reflection. The old Eevee renders had nothing to reflect: a grey plane plus one sun | Materials + rendering |
| 8 | **Uniform, untextured surfaces** | A 256 px *flat-colour* palette atlas: no grain on plastics, no brushed metal, no rubber texture, no AO, no grime. Every part has one roughness value | Texturing |
| 9 | Parts look **floating** | No ambient occlusion anywhere (no baked AO, no contact darkening), so trim and wheels don't sit *in* the body | Texturing |
| 10 | **No sense of scale** | Missing small real-world items: wipers, license plates, badges, washer and sensor details, door-handle recesses, fuel door, side markers, antenna, seals. Without them a 4.6 m car reads like a 30 cm toy | Geometry |
| 11 | **Exaggerated proportions** | The player cars are deliberately stylised (wedge, canopy, huge wings). That's fine for hero cars, but it makes the fleet look like concept toys. **Traffic must be built to real-world class proportions** | Design |
| 12 | Presentation | The previous review renders used Eevee, a grey ground plane, one sun and a sky. No studio softboxes, so no automotive highlight lines | Rendering |

**What does *not* fix it:** more polygons. Vortex R is 73k triangles and still looks procedural; the missing ingredients are construction, depth, material response and small-scale detail. Traffic must look *more* real at **10–15k triangles**.

## 2. Production method for traffic

1. **High-poly → low-poly bake (new).**
   - Each body is built as a high-resolution master: cage at subdivision level 3 with real panel-gap grooves, recessed openings and creases.
   - The game mesh is a decimated, uniquely unwrapped low-poly body.
   - **Tangent-space normals (MikkTSpace) and AO are baked** from the master. The low-poly shades like the high-poly; panel gaps, shut lines, bumper splits and crisp creases come from the normal map, not from triangles. This also removes the decimation shading-tear problem.
2. **Real-world proportions first.**
   - Dimensions, overhangs, wheelbase, tire size, glass angles and greenhouse share follow the vehicle class (§4).
   - Designs stay original and fictional; no licensed shapes, logos or plates.
3. **Constructed ends.**
   - The front and rear faces get defined planes and creases: hood leading edge, bumper upper crease, corner radius.
   - No scaled-ring "pillow" ends.
4. **Depth everywhere a real car has it.**
   - Grilles: frame, mesh with real offset, back plate in shadow.
   - Lamps: housing, chrome reflector bowls and projector, LED light guides, then a lens that follows the original body surface.
   - Glass: inset 5–8 mm with a rubber seal and a black frit band.
   - Arches: dark liners.
   - Door handles: in recesses.
5. **Scale cues on every vehicle.** License plates (fictional), wipers, badges, mirrors with glass, side markers or reflectors, antenna or fin, door handles, fuel door (baked), and a visible interior.
6. **Reusable traffic system.** Shared material library (§3), atlas and light-mask conventions, scripts, validation and render rig. Vehicle-specific geometry and body bakes only.

## 3. Material standard (PBR, ≤ 8 slots at LOD0, shared across the fleet)

| Slot | Use | Physical targets |
|---|---|---|
| `TS_Paint` (per vehicle, colour = instance parameter) | Body paint | Base layer metallic 0.45–0.65 (solid colours 0.0) and roughness 0.30–0.40 (flake), **clear coat 1.0 with coat roughness 0.03–0.06**. Fine flake detail normal (tiling). Baked normal + AO (+ grime mask) per vehicle |
| `TS_Atlas` (shared 2048) | Every opaque non-paint part | One cell per material class, each with **texture variation**:<br>• grained black plastic (rough 0.55–0.7, grain normal)<br>• gloss black (0.08)<br>• chrome (metal 1, 0.05)<br>• brushed aluminium (metal 1, 0.25, directional)<br>• silver and dark wheel paint (metal 0.8, 0.3)<br>• rubber seals (0.9)<br>• fabric (weave normal, 0.85)<br>• interior plastic (0.6)<br>• carpet<br>• grille mesh<br>• lamp housing and chrome reflector<br>• brake disc (metal, radial)<br>• caliper<br>• lug nut<br>• fictional plate<br>• badge<br>• mirror glass<br>• red reflector |
| `TS_Tire` (shared) | Tires | Rubber base ≈ 0.03 linear, rough 0.85–0.92. Tread and sidewall normal (blocks, sipes, sidewall rings, fictional lettering band). Mild tread wear (lighter, rougher crown) |
| `TS_Glass` (shared) | Window glass | Tinted transmissive (green-grey), rough 0.02, **alpha ≈ 0.35 for Unity, never opaque black** |
| `TS_Lens` / `TS_LensRed` (shared) | Lamp lenses | Clear and red lenses, rough 0.02. Red reads **red in daylight**, with no pink cast |
| `TS_Lights` (shared) | All light emitters | One emissive material. **Channel = atlas cell** (DRL, Headlamp, Tail, Brake, Indicator_L, Indicator_R, Reverse, Marker). Unity drives per-channel intensity through a channel-ID mask (one draw call) |

- **Wear:** restrained only. Slight lower-body road grime from the baked mask, light dust in cavities via AO, mild tire wear. No rust, damage or noise.
- **Paint variants:** 5–6 believable factory colours per vehicle (solid white, silver metallic, dark grey metallic, black, deep blue or red metallic, …). These are material instances only; no duplicate meshes.

## 4. Proportion standard (real-world class ranges)

| Class | Length m | Width m (body) | Height m | Wheelbase m | Tire |
|---|---|---|---|---|---|
| Compact sedan | 4.55–4.70 | 1.78–1.82 | 1.42–1.48 | 2.65–2.72 | 205/55 R16 – 215/50 R17 |
| Premium sedan | 4.85–5.00 | 1.83–1.90 | 1.43–1.48 | 2.85–2.97 | 225/50 R18 |
| Compact hatchback | 4.00–4.30 | 1.72–1.80 | 1.43–1.50 | 2.50–2.62 | 195/60 R15 – 205/55 R16 |
| Compact SUV | 4.35–4.55 | 1.80–1.86 | 1.60–1.70 | 2.60–2.70 | 215/60 R17 |
| Large SUV | 4.85–5.10 | 1.93–2.00 | 1.72–1.80 | 2.90–3.00 | 255/55 R19 |
| Pickup | 5.30–5.90 | 1.95–2.05 | 1.80–1.95 | 3.20–3.70 | 265/70 R17 (all-terrain) |
| Van | 5.30–5.95 | 2.00–2.05 | 2.30–2.60 | 3.30–3.70 | 235/65 R16C |
| Box truck | 7.0–8.5 | 2.40–2.50 | 3.30–3.60 | 4.0–4.8 | 225/75 R17.5 (dual rear) |
| City bus | 12.0 | 2.50–2.55 | 3.0–3.3 | 5.9–6.2 | 275/70 R22.5 (dual rear) |

Commercial vehicles use steel or heavy-duty wheels and dual rears with the correct wheel count; never sports wheels.

## 5. Budget (initial targets, LOD0 triangles)

| Hatchback | Compact sedan | Premium sedan | Compact SUV | Large SUV | Pickup | Van | Box truck | Bus |
|---|---|---|---|---|---|---|---|---|
| 8–12k | 10–15k | 12–18k | 10–16k | 12–20k | 12–20k | 10–18k | 12–22k | 15–25k |

- **LOD1** is 40–55 % of LOD0, **LOD2** 15–25 %, **LOD3** 5–10 %.
- **Materials:** ≤ 8 effective slots at LOD0 and fewer at far LODs (LOD3 drops the interior and lens materials where possible).
- **Textures:** shared atlas, tire and lights sets across the fleet; per vehicle only the body normal and AO/grime bake (2048 at LOD0, 1024 at LOD1).
- **No frame-rate claims without Unity device profiling.**

## 6. Visual QA protocol (mandatory, rendered with `scripts/ts_render.py`)

| Environment | Renders |
|---|---|
| **A. Neutral studio** (Cycles; grey cyclorama; overhead key, side strips and rim softboxes; neutral AgX; no bloom, no motion blur) | Front ¾, rear ¾, front, rear, side, top, wheel close-up, interior through glass, front and rear detail |
| **B. Daylight** (physical sky and sun over the frozen P0 road) | Front ¾, rear ¾, side |
| **C. Game camera** (frozen P0 highway, follow camera height 2.0–2.4 m) | Close follow (~7.5 m), normal traffic (~22 m), far traffic (~60 m), plus LOD0–3 compared at matching camera positions |

- **Plus:** zebra on the high-res master and the baked low-poly; the numeric shading screen (`va_shading_qa.py`) on all LODs; a proportion check against §4; and a paint-variant sheet.
- **Reference comparison:** no licensed photographic references are bundled in this offline workspace. The realism comparison uses the class-dimension data in §4 and studio renders. Photographic side-by-sides should be added by the art director from licensed sources.

## 7. Rejection conditions (any one rejects the vehicle)

- It looks like a toy.
- Proportions are outside the §4 class range, or visibly wrong.
- The paint reads as plastic.
- The bumper or grille looks flat.
- Wheels look unrealistic.
- Windows look painted black.
- Lamps look pasted on.
- Panel transitions are broken.
- There is unintended reflection waviness.
- Shading tears appear at any gameplay LOD.
- Wheels or colliders are misaligned.
- Parts float or intersect.
- There is obvious LOD popping.

Every review must state honestly where the asset still falls short.
