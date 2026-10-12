# Export validation report

Package `Export Vechile/`, generated 2026-10-11 on the Blender Mac. Blender 5.2.2 LTS. **Nothing in this package was opened in Unity**: Unity import, prefabs, shaders, materials, gameplay, lighting and Android performance are **NOT RUN** (task P0-05 on the Unity machine).

## Required checks

| # | Check | Result | Detail |
|---|---|---|---|
| 01 | All seven mandatory traffic vehicles present | PASS | 7 / 7: Sedan A r3, Sedan B, Hatchback A r2, SUV A v2, SUV B v3, Box Truck A r7, Bus A v4 |
| 02 | Correct approved release version | PASS | 12 / 12 vehicles (details: 06_QA) |
| 03 | Complete FBX exists | PASS | 12 / 12 vehicles (details: 06_QA) |
| 04 | Every required texture exists | PASS | 12 / 12 vehicles (details: 06_QA) |
| 05 | All paths resolve inside the portable package | PASS | 12 / 12 vehicles (details: 06_QA) |
| 06 | FBX hierarchy valid | PASS | 12 / 12 vehicles (details: 06_QA) |
| 07 | Model orientation (+Z forward, +Y up, -X left) | PASS | 12 / 12 vehicles (details: 06_QA) |
| 08 | Dimensions and scale (metres, scale 1, ground Y 0) | PASS | 12 / 12 vehicles (details: 06_QA) |
| 09 | All LODs preserved (LOD0-3) | PASS | 12 / 12 vehicles (details: 06_QA) |
| 10 | Triangle counts match the release manifest | PASS | 12 / 12 vehicles (details: 06_QA) |
| 11 | Wheel pivots match the validated source | PASS | 12 / 12 vehicles (details: 06_QA) |
| 12 | Collider references preserved | PASS | 12 / 12 vehicles (details: 06_QA) |
| 13 | Centre-of-mass reference preserved | PASS | 12 / 12 vehicles (details: 06_QA) |
| 14 | Material names and assignments preserved | PASS | 12 / 12 vehicles (details: 06_QA) |
| 15 | Light-channel data preserved | PASS | 12 / 12 vehicles (details: 06_QA) |
| 16 | No duplicate vehicle release | PASS | 12 FBX files for 12 vehicles, unique ids / releases / SHA-256; no LOD0 test FBX; Titan GT and Vortex R FBX are the r1 revisions (differ from the superseded originals) |
| 17 | No corrupted textures | PASS | 12 / 12 vehicles (details: 06_QA) |
| 18 | No unexpectedly missing dependencies | PASS | 12 / 12 vehicles (details: 06_QA) |
| 19 | Original frozen sources unchanged | PASS | va_frozen_check 14 releases unchanged; UNITY_HANDOFF_20261010 93 files match SHA1SUMS.txt; Hypercar 50 source files match its manifest; va_integrity: changed 0 |
| 20 | Package checksum manifest valid | see log | checked after the list is written: `05_Manifests/PACKAGE_VERIFICATION_LOG.md` (this folder + an independent copy) and again on the extracted ZIP |

Per-vehicle Blender-side result: Sedan A r3 PASS, Sedan B PASS, Hatchback A r2 PASS, SUV A v2 PASS, SUV B v3 PASS, Box Truck A r7 PASS, Bus A v4 PASS, Hypercar PASS, Zero Gap R PASS, Titan GT r1 PASS, Vortex R r1 PASS, Raven XR PASS

## Portability

The package was copied to a separate temporary folder outside the Blender project and every FBX re-measured there: the measurements are identical to the in-place run, all relative texture paths resolve inside the copy, and Blender's importer loaded every linked image from the copy (not from the original Blender folders). The stored absolute paths are informational only (see `05_Manifests/DEPENDENCY_REPORT.md`).

## Source integrity

- `va_frozen_check.py`: FROZEN CHECK PASS (14 frozen releases, run at packaging time).
- `UNITY_HANDOFF_20261010/SHA1SUMS.txt`: 93 files, mismatched 0.
- Hypercar `new_car/`: 50 source files (2 checkpoints + 48 textures) match `final_export_manifest.json`. new_car/exports/ (original 2026-10-06 FBX) is not on disk; FBX re-exported, see REEXPORT_PROVENANCE.md.
- Workspace baseline (`va_integrity.py`, run read-only): changed **0**; removed 1186 under `environment/`; added outside `vehicles/` by top-level folder: {'.git': 21, '.gitignore': 1, 'Export Vechile': 231}.

## Known separate item (not a vehicle export failure)

The frozen environment P0-P3 (`environment/`, 1186 baseline files) was moved off this Mac by the owner on 2026-10-09 and archived at `/Volumes/Denish/Assets/environment.zip`. `va_integrity.py` therefore reports FAIL for those files. This is owner-acknowledged and unrelated to the vehicles; the check was not weakened. Re-verifying the archive needs the `Denish` drive (`A_Discovery/scripts/va_verify_env_archive.py`): **NOT RUN** (drive not mounted). The new `Export Vechile/` folder (and the ZIP) also appear as 'added' outside `vehicles/`; that is expected.

## Known exceptions and limits

- **Hypercar FBX re-exported**: the 2026-10-06 FBX was no longer on disk. Re-exported with the unchanged pipeline from the hash-verified source; validator 85 PASS / 0 / 0, data identical to the frozen validation (see `02_Player_Vehicles/Hypercar/REEXPORT_PROVENANCE.md`). New SHA-1, by design (the FBX stores the export folder path).
- **Hypercar triangle counts** (LOD0 206,327) are far above the mobile player budget (60-120k LOD0). Use LOD1+ or treat as a showroom / high-tier asset; decide in Unity.
- **Traffic LOD0 above the existing 15,000 validation budget**: Sedan B 17,987, Hatchback A r2 17,174, SUV A v2 17,998, SUV B v3 19,840, Box Truck A r7 20,063, Bus A v4 34,506. These are the approved releases; the budget was not weakened here (decide in Unity: raise the budget per class or start these at LOD1).
- **Hypercar lights**: one amber material drives both indicators (no left/right split) and one white material is DRL + headlamp.
- **Player FBX texture folder case**: the player FBX files reference `../textures/`; the old UnityTransfer folders used `Textures/`. This package uses `textures/`, which resolves on case-sensitive file systems too.
- **Zero Gap R PB-1** (non-blocking): slightly pink daytime tail-lens; review in the Unity material pass.

## Not run here

- Unity import / prefab / LOD Group / material / shader / lighting / gameplay / Android performance: NOT RUN (no Unity on this Mac).
- Environment archive re-verification: NOT RUN (Denish drive not mounted).
- Visual (render) review: not repeated; every vehicle carries its frozen visual approval.

