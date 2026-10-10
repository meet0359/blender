# Vortex R r1 — LOD1 normals repair revision: QA report

**Status: VALIDATED and FROZEN — corrected revision of Vortex R, preferred Unity import candidate** (2026-10-08).
- The original release `vehicles/D_VortexR/` is kept frozen and byte-identical; it was only read.
- Approved by the project owner as "Vortex R — approve revision r1".

## 1. Result

| Gate | Result |
|---|---|
| Validation (`reports/VX_validation.txt`) | **19 checks (18 + S1 LOD1/LOD2 torn-normal check): 0 errors, 0 warnings** |
| Full shading QA, LOD0–LOD3 (`reports/VX_r1_shading_qa.json`) | **79 of 79 render meshes PASS.** The original release had 3 FAIL and 1 WARN |
| FBX clean re-import | 2 of 2 files pass, 37 and 103 objects. Bounds deviate by 3.0e-7 m and pivots by 1.5e-7 m. Raw Unity space was checked |
| Scope check | All 103 objects were diffed between the original and r1 export-ready files. **Only 4 meshes differ, and only in their normals**; no geometry differs. Everything else is identical in geometry, normals, materials, transform and parent |
| Triangle counts | Unchanged: 73,665 / 34,060 / 15,026 / 6,146 |
| Protected files | **PASS**: baseline 1,554 files; frozen Zero Gap R, Titan GT original, Titan GT r1, Vortex R original and Raven XR are all byte-identical |

## 2. Defect and fix

- **Defect:** the original build transferred LOD0 custom normals onto the decimated LOD1 hard-surface parts. On the reduced geometry those normals tear.
- **Visible symptoms (all confirmed):**
  - silvery, blotchy carbon wing and endplates;
  - smeared rocker blade;
  - silver streaks on the diffuser fins.
- **Repair (normals only, `scripts/vx_r1_normals.py`):**
  - Custom normals are cleared, the parts are shaded smooth, and sharp edges are set from the **same angle each part uses at LOD0**: 35° for trim and lights, 40° for interior and steering wheel.
  - This keeps the intended smoothing boundaries.
  - Geometry, UVs, materials, light channels, pivots, colliders, hierarchy and orientation are untouched.
- **Re-run check:** re-running the script reproduces the committed file's normals exactly.

| Mesh | Torn loop normals before | After |
|---|---|---|
| `Trim_LOD1` (wing, pylons, endplates, rocker, diffuser, splitter) | **23.04 %** | 0.00 % |
| `Interior_LOD1` | 2.36 % | 0.00 % |
| `Lights_LOD1` | 1.22 % | 0.00 % |
| `SteeringWheel_LOD1` | 0.91 % | 0.08 % |

- **LOD2 and LOD3** were checked as well, using the full shading QA and the LOD2 render rows. They have no equivalent defect; those LODs already used their own normals. They were not changed.
- **Considered and rejected:** a hybrid that keeps plausible transferred normals. It rendered identically. The LOD1 exhaust tips lose the chrome glint they had in the original, but LOD0 renders them the same dark way, so that glint was itself part of the artifact.

## 3. Evidence

- **`previews/VX_r1_lod_compare_original_vs_repaired.jpg`.** Rows: original LOD1, r1 LOD1, original LOD2, r1 LOD2. Columns: front ¾, rear ¾, side, wing, rocker/door, rear and diffuser.
- **`previews/lod_compare/`:** the 24 individual renders behind the sheet.
- **`previews/VX_*.png`:** the 18 review renders, identical to the original at LOD0, plus the lineup.

## 4. Unity

- **Use `D_VortexR_r1/UnityTransfer/`.**
- FBX names are unchanged (`VortexR_complete_unity.fbx`, `VortexR_LOD0_unity_test.fbx`), so r1 drops in as a replacement for the original.

## 5. Known limitations (unchanged from the original release)

These are listed in `D_VortexR/reports/VX_FINAL_REPORT.md` §6:
- doors don't open;
- the interior isn't built for hero close-ups;
- emission needs tuning in Unity with bloom;
- no Unity runtime testing was done.
