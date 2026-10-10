# Start here: project context restore (2026-10-10)

The owner lost the earlier ChatGPT conversation. This document restores the context. The other files in this folder hold the detail.

## 1. How the work is organised

| Role | Who | What they do |
|---|---|---|
| Owner | Meet | Approves, freezes and decides. Relays between ChatGPT and Claude Code. |
| Planner | ChatGPT | Writes phase **work orders**: goals, restrictions, deliverables, final report. |
| Executor | Claude Code | Runs the work orders on the **Blender Mac** (Blender 5.2.2, fully script-driven pipeline). Reports back with Markdown reports and render images. |
| Unity integration | Separate **Unity machine** (Unity 6000.6.0f1, URP 17.6) | Not this Mac. Unity must not be installed on the Blender Mac. |

ChatGPT cannot open `.blend` or `.fbx` files. It works from these reports and from images the owner sends.

## 2. The project

The game is a mobile highway racing game in Unity. Blender produces the vehicles. All paths below are relative to `/Users/meetshah/Documents/blender/vehicles/`.

| Area | Status |
|---|---|
| Environment phases P0–P3 | Complete and frozen. On 2026-10-09 the folder was archived to the external drive `Denish` (`/Volumes/Denish/Assets/environment.zip`), then removed from the Mac. The owner decided **not to restore it** for now. Unity integration of the environment is under way on the Unity machine. Full environment context: the sibling folder `CHATGPT_CONTEXT_RESTORE_ENVIRONMENT_20261010/`. |
| Player cars | **FROZEN:** Zero Gap R (`B_ZeroGapR`), Titan GT + r1, Vortex R + r1, Raven XR. **Pulse EV postponed** (blockout untouched). For Unity, use the r1 revisions. |
| **Traffic fleet**, the current focus | **All 7 priority vehicles FROZEN** on 2026-10-10. **Unity FBX export and handoff package DONE** on 2026-10-10. |
| Postponed traffic | Pickup A (the builder needs a separate cab-volume feature first), Van A |

## 3. Traffic fleet: released versions (export only these)

| # | Vehicle | Released version | LOD0 triangles | Folder (`H_TrafficFleet/`) |
|---|---|---|---|---|
| 1 | Sedan A | r3 | 14,961 | `Traffic_Sedan_A_r3/` |
| 2 | Sedan B | production | 17,987 | `Traffic_Sedan_B/` |
| 3 | Hatchback A | **r2** | 17,174 | `Traffic_Hatchback_A_r2/` |
| 4 | SUV A | v2 | 17,998 | `Traffic_SUV_A/` |
| 5 | SUV B | v3 | 19,840 | `Traffic_SUV_B/` |
| 6 | Box Truck A | r7 | 20,063 | `Traffic_Box_Truck_A/` |
| 7 | Bus A | **v4** | 34,506 | `Traffic_Bus_A/` |

Not released, kept as history only:
- the original Hatchback A (`Traffic_Hatchback_A/`), which stays frozen;
- Bus A v3 (`_rollback_v3`).

## 4. What has been done (work-order history, latest last)

1. **Box Truck A final realism pass:**
   - truck wheels (8 studs, drums, deep-dish duals);
   - marker lamps;
   - cargo-box detail.

   Result: r6, then r7.
2. **Final fleet QA of the 7 vehicles:**
   - the truck and bus windshield "X" artefact fixed (structured glass grid);
   - end-cap fold cracks fixed (n-gon end caps);
   - SUV B plate fixed.

   The owner accepted the SUV A hood zebra stepping.
3. **Release:**
   - SUV A v2, SUV B v3 and Box Truck A r7 frozen;
   - a corrected Hatchback A r2 created (plate recess and rear cracks);
   - a Bus A v4 louvre fix;
   - **night review rig v2.** The root cause of black-looking paint at night was a black sky reflection; the fix is in the preview rig only.
4. **Final approval:** Hatchback A r2 and Bus A v4 frozen, so all 7 are frozen.
5. **Unity export and handoff (latest):**
   - FBX exported for all 7 from isolated copies of the frozen files;
   - clean re-import validation and an extra FBX audit;
   - handoff package built;
   - all vehicles pass.

   See `02_UNITY_FLEET_HANDOFF_REPORT.md`.

**Unity handoff package:** `H_TrafficFleet/UNITY_HANDOFF_20261010/` (48 MB, 94 files).
- 7 vehicle folders, each with:
  - the FBX with LOD0–3, colliders, wheel refs and CenterOfMass;
  - textures and reports.
- Shared textures.
- `README_UNITY_IMPORT.md`, the fleet manifest and `SHA1SUMS.txt`.

## 5. Owner rules: keep them in every future work order

- **Frozen means frozen.**
  - Never modify a frozen `.blend` or any file listed in a `*_FINAL_FREEZE.md` manifest.
  - Changes go into a new revision folder, for example `_r2`.
  - Never edit a manifest to hide a failure.
- **Never write output files inside frozen vehicle folders.**
- **No automatic deletion.** The 494 MB staging folder `vehicles/_TO_DELETE_cleanup_20261009/` is kept until the owner deletes it.
- **Report honestly.**
  - Validator **check 1 (protected files)** FAILs on every vehicle only because `environment/` is archived off the Mac. Report it; never hide it.
  - Archive re-verification needs the `Denish` drive connected. On 2026-10-10 it was not connected, so the result is **NOT RUN**, not a pass.
- **Unity results are verified only on the Unity machine.** Never claim Unity runtime results from the Blender Mac.
- **Approvals:**
  - Ask the owner before freezing anything.
  - Do not ask for approval between normal, reversible steps.
- **Disk:** about 8.3 GB free, with a 1 GB emergency floor. Outputs must not exhaust the disk.
- **Process for any new vehicle:**
  1. Art direction first: published class dimensions as reference, but an original design.
  2. Blockout, with written self-critique.
  3. Same-camera comparison against an approved vehicle.
  4. Production.
  5. Validation.
  6. Owner approval.
  7. Freeze.

## 6. Technical conventions (short)

**Hierarchy:**
- `Car_Root` contains `LOD0_Root`–`LOD3_Root`, each holding Body, Glass, Trim, Lights, Interior, plus wheels under front `SteerPivot`s.
- `Car_Root` also contains `Collision` (4 convex hulls), `WheelColliderRef_FL/FR/RL/RR` (with `radius_m` and `width_m`) and `CenterOfMass`.

**Materials:** 8 per LOD, and 19–20 draw calls at LOD0.
- **Shared library:** `TS_Atlas` (8 × 8 material atlas), `TS_Tire`, `TS_Lens`, `TS_LensRed`, `TS_Lights`.
- **Per vehicle:** `_Paint` / `_Paint_LOD1` / `_Paint_Far`, `_Glass`, `_Interior`.

**Light channels:** one emissive material with 8 independent channels, selected by a channel-ID map:
- DRL, Headlamp, Tail, Brake;
- Indicator L, Indicator R, Reverse;
- Marker (truck and bus).

**Unity axes:**
- Point mapping: Blender (x, y, z) → Unity (−x, z, −y).
- Forward +Z, up +Y.
- Scale 1, 1 unit = 1 m.

**Triangle budgets (LOD0):**

| Class | LOD0 triangles |
|---|---|
| Cars | 10–18k |
| SUV B | 13–20k (approved) |
| Truck | 15–25k |
| Bus | 20–35k |

**Validation:**
- 16 checks, the S1 shading screen and the FBX re-import.
- The frozen-release hash check `va_frozen_check.py` currently passes for all 14 releases.

## 7. Open items: the next work order should come from here

1. **P0-05: Unity runtime verification on the Unity machine.** This is the main next step. The checklist is in `03_README_UNITY_IMPORT.md` §9:
   - import;
   - LOD Group;
   - convex colliders and WheelColliders;
   - centre of mass;
   - transparency;
   - light-channel shader;
   - night look;
   - mobile performance.

   Unity-side work needed:
   - a Shader Graph for the paint (AO is in the R channel; URP occlusion reads G);
   - a Shader Graph for the light-channel emission.

   FBX cannot carry these maps; the README lists them.
2. **Environment archive:** connect `Denish` and run `python3 vehicles/A_Discovery/scripts/va_verify_env_archive.py`. Also decide whether to restore `environment/` or formally accept the relocation.
3. **Cleanup decisions for the owner:**
   - delete the staging folder (494 MB);
   - delete the export workspace `H_TrafficFleet/_UNITY_EXPORT_WS_20261010/` (54 MB) after the package is accepted.
4. **Postponed:** Pickup A, Van A, Pulse EV.

## 8. Files in this folder

| File | What it is |
|---|---|
| `00_START_HERE_PROJECT_CONTEXT.md` | This summary |
| `01_FLEET_FINAL_RELEASE_20261010.md` | Release record: versions, frozen file paths, budgets, validation, freeze manifests, integrity |
| `02_UNITY_FLEET_HANDOFF_REPORT.md` | Latest phase report: FBX export, validation, LODs, materials, orientation, colliders, wheels, integrity, package, blockers |
| `03_README_UNITY_IMPORT.md` | Unity integration instructions: texture and model import settings, prefab assembly, material setup, light channels, P0-05 checklist |
| `04_UNITY_FLEET_MANIFEST.md` | Checksums and summary per vehicle: source release SHA-1, FBX SHA-1, LODs, materials, shared textures |
| `05_TRAFFIC_REALISM_STANDARDS.md` | The design and realism standard (H0) the traffic vehicles were built to |
