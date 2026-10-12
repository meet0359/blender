# Material setup guide (URP 17.6)

Blender shader graphs do **not** carry over to Unity. The FBX links only base colour and normal maps, plus two Blender slots (Metallic → ReflectionFactor, Roughness → ShininessExponent) that URP ignores or misreads. Create the URP materials once, name them **exactly** like the FBX materials, then remap them in each FBX's Materials tab (Search and Remap, Project-Wide).

This package contains **no Unity shaders or material scripts**. None existed in a verified state, so the configuration is documented here rather than invented. Everything below is the intended setup and is **not runtime-verified** (P0-05).

Exact per-vehicle values (paint colour, metallic, smoothness, alpha, clear coat, emission strengths) are in each vehicle's own notes, which carry the frozen source values:

| Vehicles | Notes file |
|---|---|
| Traffic | `01_Traffic_Vehicles/<Vehicle>/README_<Base>.md` (materials table), plus `reports/<Base>_unity_manifest.json` → `materials` |
| Zero Gap R, Titan GT r1, Vortex R r1, Raven XR | `02_Player_Vehicles/<Vehicle>/<PREFIX>_UNITY_IMPORT_NOTES.md` → "Materials (15)" |
| Hypercar | `02_Player_Vehicles/Hypercar/reports/unity_material_mapping.md` |

Every material name per LOD is listed in `04_Unity_Setup/Vehicle_Configuration/<vehicle>.json` → `lods.LODn.materials`, and the textures each vehicle needs by hand in `textures.manual_setup`.

## 1. Traffic fleet (7 vehicles; shared library in `01_Traffic_Vehicles/shared/textures/`)

**Shared materials, create once:** `TS_Atlas`, `TS_Tire`, `TS_Lens`, `TS_LensRed`, `TS_Lights`.

**Per-vehicle materials:**
- `<Paint>_Paint` (LOD0), `<Paint>_Paint_LOD1`, `<Paint>_Paint_Far` (LOD2–3);
- `<Paint>_Glass`, `<Paint>_Interior`;
- where `<Paint>` is `TS_SedanA`, `TS_SedanB`, `TS_HatchA`, `TS_SUVA`, `TS_SUVB`, `TS_BoxTruckA` or `TS_BusA`.

### Paint (`<Paint>_Paint`, `_Paint_LOD1`): the one that needs care

- **Shader:** Complex Lit (clear coat), or a Shader Graph.
- **BaseColor** = PaintColour × AO, where **AO is the R channel** of `<Paint>_Body_AO_Grime.png`.
- **Grime:** lerp towards (0.11, 0.10, 0.085) by **G × 0.55**. G is the road-grime mask.
- **Do not plug `_AO_Grime` into URP's Occlusion Map.** URP reads occlusion from **G**, so you would get grime as AO. Two options:
  - use a Shader Graph that samples R for AO and G for grime;
  - or make a repacked copy (R → G) used only as the Occlusion map, and drop the grime.
- **Normal** = `<Paint>_Body_Normal.png` (LOD0) or `<Paint>_Body_Normal_LOD1.png` (LOD1). MikkTSpace bakes.
- **Detail normal** = `TS_PaintFlake_Normal.png`, tiling 60, strength 0.15.
- **Metallic, smoothness, clear coat:** per vehicle README. Coat smoothness is about 0.955 (grime lowers it). The box truck has solid paint: metallic 0, coat 0.55.
- **`<Paint>_Paint_Far` (LOD2–3):** PaintColour only, with no normal or AO maps. Lit or Complex Lit.
- **Paint variants** are material instances only (linear RGB, metallic):

  | Variant | Linear RGB | Metallic |
  |---|---|---|
  | Arctic white | (0.80, 0.80, 0.78) | 0 |
  | Silver | (0.55, 0.57, 0.59) | 0.55 |
  | Graphite | (0.090, 0.095, 0.100) | 0.55 |
  | Black | (0.012, 0.012, 0.013) | 0 |
  | Deep red | (0.30, 0.012, 0.015) | 0.55 |
  | Steel blue | (0.060, 0.115, 0.220) | 0.55 |

### Lights (`TS_Lights`): one material, one draw call, 7 or 8 channels

- **Textures:**
  - BaseMap `TS_Lights_BaseColor.png` (lamps off);
  - Emission `TS_Lights_Emission.png`;
  - channel map `TS_Lights_ChannelID.png`, imported Point / no compression / no mip maps.
- **Channel index** = `round(ChannelID.R × 15)`:

  | Index | Channel |
  |---|---|
  | 0 | DRL |
  | 1 | Headlamp |
  | 2 | Tail |
  | 3 | Brake |
  | 4 | Indicator_L |
  | 5 | Indicator_R |
  | 6 | Reverse |
  | 7 | Marker (box truck and bus only) |

  Cars use channels 0–6; the box truck and bus use 0–7.
- **Emission** = `TS_Lights_Emission.rgb × intensity[index]`. Feed the 8 intensities per renderer (MaterialPropertyBlock), so pooled vehicles don't need material copies.
- **In Shader Graph:** 8 float properties and an index compare (or a small Custom Function). This is a description of the maths; no tested graph is included.
- **Suggested start intensities:**

  | Channel | Intensity |
  |---|---|
  | DRL | 12 |
  | Headlamp | 4 |
  | Tail | 5 |
  | Brake | 8 (on) |
  | Indicators | 1.2 (blink) |
  | Reverse | 0.5 |
  | Marker | about Tail level |

  Tune them with bloom.
- **Check:** channel faces in every FBX were verified identical to the source on all LODs. Brake and tail are separate channels, and the indicators are split left and right.

### Other traffic materials

| Material | URP setup |
|---|---|
| `TS_Atlas` | Lit, opaque. BaseMap `TS_Atlas_BaseColor`; **Metallic Map `TS_Atlas_MetallicSmoothness`** with Smoothness Source = Metallic Alpha; Normal `TS_Atlas_Normal`. Atlas UVs are inset 6 % per cell, so bilinear filtering does not bleed. `TS_Atlas_Metallic` / `_Roughness` are the Blender-side pair; the MetallicSmoothness map replaces them. |
| `<Paint>_Interior` | Same as `TS_Atlas` (an instance of it), with **normal scale 0.12** |
| `TS_Tire` | Lit, opaque. BaseMap `TS_Tire_BaseColor`, Normal `TS_Tire_Normal`. Smoothness = 1 − `TS_Tire_Roughness`: pack it into an alpha, or use a constant of about 0.5. U wraps around the tyre (repeat). |
| `<Paint>_Glass` | Lit, Transparent. Base (0.78, 0.84, 0.82), **alpha 0.22**, smoothness 1.0 |
| `TS_Lens` | Lit, Transparent. Base (0.92, 0.94, 0.96), alpha 0.10, smoothness 0.99 |
| `TS_LensRed` | Lit, Transparent. Base (0.42, 0, 0.006), alpha 0.55, smoothness 0.98 |

## 2. Player cars: Zero Gap R, Titan GT r1, Vortex R r1, Raven XR (15 materials each)

The prefix is `ZG_`, `TG_`, `VX_` or `RV_`.

| Material | URP setup |
|---|---|
| `<P>_Paint` | Complex Lit (clear coat). No texture, so the colour is runtime-swappable. Colour, metallic, smoothness and coat values are in the notes. |
| `<P>_Palette` | Lit, opaque. BaseMap `<P>_Palette_BaseColor`; **Metallic Map `<P>_Palette_MetallicSmoothness`** (R metal, A smoothness). Filter Point or mip maps off: it is a 256 px swatch atlas. |
| `<P>_Carbon` | Lit, opaque. `<P>_Carbon_BaseColor` + `<P>_Carbon_Normal`. Smoothness about 0.7, clear coat about 0.6. UVs are world-scale (0.25 m tile). |
| `<P>_Tire` | Lit, opaque. `<P>_Tire_BaseColor` + `<P>_Tire_Normal` (sidewall lettering baked in). Smoothness about 0.18. |
| `<P>_Glass`, `<P>_LensClear`, `<P>_LensRed` | Lit, Transparent. Alpha and tint per notes (single thin sheets, no refraction). |
| `<P>_Display` | Lit + emission. Swap for a RenderTexture to drive live gauges. |
| `<P>_LED_DRL`, `_Headlamp`, `_Tail`, `_Brake`, `_Indicator_L`, `_Indicator_R`, `_Reverse` | Lit, opaque + emission. **One material per light channel (7 channels)**: drive `_EmissionColor` intensity at runtime. Start strengths are in the notes. |

Zero Gap R has an open polish item, **PB-1**: its daytime tail-lens reads slightly pink. Review it in this pass. The other three use the corrected deep red, alpha 0.80.

## 3. Hypercar (24 materials at LOD0; 8 baked atlases in `textures/hypercar/<group>/`)

- **Atlases:** `LODMAT_Body_Paint`, `_Brakes`, `_Glass`, `_Interior`, `_Lights`, `_Tire`, `_Trim`, `_Wheels`.
  - Each has BaseColor, Metallic, Roughness, Normal and AO.
  - Sizes: BODY and INTERIOR 4096; WHEELS, TIRES and LIGHTS 2048; BRAKES, GLASS and TRIM 1024.
- **URP needs packing:** `MetallicSmoothness` = R ← `*_Metallic`, A ← 1 − `*_Roughness`. **This package ships the unpacked maps** (the frozen release). Pack them in Unity, or with a texture tool, before assigning them.
- **AO:** `*_AO.png` is not linked by the FBX. Assign it to Occlusion by hand; greyscale works with URP's G read.
- **Paint (`LODMAT_Body_Paint`):** RacingRed (0.80, 0.010, 0.024) linear, metallic 0.85, smoothness about 0.80, clear coat 0.58. Use Complex Lit or a clear-coat paint shader.
- **Light channels, one material each** (6 emissive):
  - `MAT_LED_White`: DRL + headlamp;
  - `MAT_LED_Red`: tail;
  - `MAT_LED_Brake`;
  - `MAT_LED_Amber`: **both indicators; there is no left/right split**;
  - `MAT_LED_Reverse`;
  - `MAT_AmbientLight`: interior.

  `MAT_ProjectorLens` has no emission. If the game needs independent left and right indicators on the Hypercar, that is a Blender-side revision; it is not part of this package.
- **Other materials:** carbon (`MAT_CarbonExterior` / `MAT_InteriorCarbon`), caliper, lenses, displays and interior mirror. See `unity_material_mapping.md`.

## 4. Night lighting (from the Blender night review; not verified in Unity)

- **Avoid** a black reflection environment. Clear-coat paint and glass then read black at night.
- **Use** a night skybox or reflection probe with a warm horizon glow and a deep-blue zenith, plus low ambient light.
- **Lamp light** comes from the emissive channels. Traffic needs no per-vehicle real-time lights.
