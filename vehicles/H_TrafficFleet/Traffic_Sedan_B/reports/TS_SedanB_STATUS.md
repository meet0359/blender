# Traffic Sedan B — STATUS: FROZEN (Blender-only), see TS_SedanB_FINAL_FREEZE.md

- Blender production complete (H2). **FROZEN (Blender-only) 2026-10-09** on owner approval. No UnityTransfer package and no new FBX.
- Final-review sheet: `previews/TrafficSedanB_sheet_FINAL_REVIEW.jpg`, made from existing renders; nothing was re-rendered.
  - Row 1: front¾, rear¾, side.
  - Row 2: front close-up, rear close-up, chase camera.
  - Row 3: LOD0, LOD1, LOD2 and LOD3, front¾.
- Validation (`reports/trafficsedanb_validation.txt`): **19 / 19 PASS, 0 FAIL.** This is 18 checks plus the S1 shading screen across all LODs.
- Geometry:

  | LOD | Triangles | Share of LOD0 | Materials |
  |---|---|---|---|
  | LOD0 | 17,987 | 100 % | 8 |
  | LOD1 | 8,739 | 49 % | 8 |
  | LOD2 | 4,012 | 22 % | 8 |
  | LOD3 | 1,746 | 10 % | 6 |

- External textures (`textures/`): `TS_SedanB_Body_Normal.png`, `TS_SedanB_Body_Normal_LOD1.png`, `TS_SedanB_Body_AO_Grime.png`, plus the shared library.
- Production files (blend, textures, exports) are unchanged since the start of the overnight sprint (checked 2026-10-09).
- Known: LOD3 wheels are octagonal at close range. That LOD only shows at distance; the close-up is in the LOD row of the sheet.
- UnityTransfer and Unity runtime profiling are not part of this freeze.
