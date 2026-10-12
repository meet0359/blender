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
