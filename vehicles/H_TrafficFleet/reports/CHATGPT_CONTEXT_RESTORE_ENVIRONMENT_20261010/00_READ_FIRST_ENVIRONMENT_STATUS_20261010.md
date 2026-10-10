# Environment: current status, 2026-10-10 (read this before `00_START_HERE_environment_context.md`)

The owner lost the earlier ChatGPT conversation, and this folder restores the **environment** context. The owner reports that the environment is now being integrated in Unity, so the Unity side needs this background.

**What is in this folder:**
- The environment context bundle written on **2026-10-08**, copied unchanged: files `00_START_HERE…` to `11_…`, plus `images/`.
- This update, which lists what changed after that date.

**Where the bundle disagrees with this update, this update wins.**

The vehicle and traffic context is a separate folder: `CHATGPT_CONTEXT_RESTORE_20261010/`, next to this one.

## 1. What is still true

**The nine environment phases are complete and FROZEN**, and no environment work has been done since P3 was frozen on 2026-10-07:

| Phase | Area |
|---|---|
| P0 | Road |
| P1 | Props, terrain, vegetation, tunnel |
| P2 | Bridges, bridge terrain, city |
| P3 | Mountain and coastal |

Everything in the bundle about these still applies:
- the conventions (axes, FBX method, naming, vertex-data contracts, seams, the road corridor);
- the per-phase deliverables, the known limitations and the original specs.

**No new biome is planned.**

## 2. What changed since 2026-10-08

### 2.1 The environment is no longer on the Blender Mac

- **2026-10-09:**
  - The owner archived the whole `environment/` folder to the external drive **`Denish`**, as `/Volumes/Denish/Assets/environment.zip`, and removed it from the Mac.
  - All **1,186** baseline files were verified inside the archive by SHA-1.
- **The owner decided not to restore it for now.**
- Every `environment/<Phase>/…` path in the bundle, including each phase's `UnityTransfer/` package, now lives **inside that zip**.
- **2026-10-10:** re-verification was **NOT RUN**, because the drive was not connected. When it is, run:
  `python3 vehicles/A_Discovery/scripts/va_verify_env_archive.py`

**Effects on the Blender Mac** (reported openly, not hidden):
- `va_integrity.py` reports **FAIL**: 0 changed, **1,186 removed**, 0 added.
- Vehicle validator check 1 (protected files) FAILs for the same reason.
- Vehicle review renders use a **stand-in road** instead of the P0 road.
- New Blender work **cannot link the frozen phases read-only** until `environment/` is restored.

### 2.2 Unity integration has started (bundle §8 is out of date)

- The bundle says "Unity integration has not started". **That is no longer true.**
- The owner reports the environment is being integrated on the **Unity machine**, using each phase's `UnityTransfer/` package.
- **Target versions:** Unity 6000.6.0f1, URP 17.6. This matches the vehicle handoff.
- **Unity progress is not tracked from the Blender Mac.** Ask the owner for its status.
- **If the Unity team needs a phase package again:** it is in `environment.zip` on `Denish`. The bundle digests and the `UnityTransfer` READMEs quoted in them describe each package's contents and import settings.

### 2.3 The vehicle work listed as "next" in bundle §8 is done

**Player cars FROZEN:**
- Zero Gap R;
- Titan GT, and its r1 revision;
- Vortex R, and its r1 revision;
- Raven XR.

For Unity, use the r1 revisions. Pulse EV is postponed.

**Traffic fleet, 7 vehicles FROZEN** on 2026-10-10:
- Sedan A r3, Sedan B, Hatchback A r2;
- SUV A v2, SUV B v3;
- Box Truck A r7, Bus A v4.

**Traffic Unity FBX handoff DONE** on 2026-10-10:
- Package: `vehicles/H_TrafficFleet/UNITY_HANDOFF_20261010/`.
- Next step: **P0-05**, Unity runtime verification of the vehicles.

`handoff_vehicle_remaster/`, mentioned in the bundle, is **superseded** by `CHATGPT_CONTEXT_RESTORE_20261010/`.

## 3. How the traffic vehicles fit the environment in Unity

These are facts from both handoffs, useful when placing traffic on the road:

| Topic | Environment (P0 road) | Traffic vehicles | Result |
|---|---|---|---|
| Axes | Blender (x, y, z) → Unity (−x, z, −y), 1 unit = 1 m | Same mapping, same FBX method | Same space, no extra rotation or scale |
| Travel direction | Blender −Y = **Unity +Z** | Vehicle nose = **Unity +Z** | Vehicles drive along the road as imported |
| Left side | Median / driver-left = Unity −X | Vehicle left = Unity −X | Consistent |
| Lanes | 4 lanes, one direction, 3.60 m wide, centres at **x = ±1.8, ±5.4**, surface ≈ ±0.018 m (crown) | Width incl. mirrors: cars 2.06–2.30 m, truck 2.54 m, bus 2.98 m | Every class fits a lane. Spawn at lane centres, and let the WheelColliders settle onto the road collision. |
| Ground | Road surface ≈ 0 | Vehicle ground at Y = 0 | No offset needed |
| Night | City windows: night emission from `CityWindowData`. Tunnel lighting guide in digest 05. | One emissive light material with 8 independent channels. A black reflection environment makes paint look black at night. | Use a night skybox or reflection probe with a horizon glow (vehicle `README_UNITY_IMPORT.md` §7) |

## 4. Rules (unchanged; keep them in every work order)

**On the Blender Mac:**
- Frozen phases are never edited. New work only links them read-only, and even that needs `environment/` restored first.
- The road never changes: straight and level, 40 m and 20 m modules.
- No automatic deletion. Honest reporting: a check that could not run is reported as **NOT RUN**, never as a pass.
- **Unity is not installed on the Blender Mac.** All Unity results come from the Unity machine.

**Unity owns:** shaders, prefabs, LOD Group components, streaming, lighting, fog, weather, water, vegetation instancing and wind, quality tiers, and performance (bundle §3).

## 5. Files in this folder

| File | Content |
|---|---|
| `00_READ_FIRST_ENVIRONMENT_STATUS_20261010.md` | This update |
| `00_START_HERE_environment_context.md` | Full environment overview: rules, conventions, the 9 phases, dependencies, limitations. Written 2026-10-08. |
| `01_P0_RoadFoundation.md` … `09_P3_MountainCoastal.md` | One digest per phase: asset index (triangles per LOD, which FBX), Unity import notes and guides, materials, validation, freeze record |
| `10_original_specs_P0_P1.md`, `11_original_specs_P2_P3.md` | The owner's original phase instructions, verbatim (large) |
| `images/01 … 09_*_previews.jpg` | One preview contact sheet per phase (Blender QA renders, not the final Unity look) |

**Suggested upload order if ChatGPT limits the number of files:**
1. This file, `00_START_HERE…` and the 9 images.
2. The phase digests (01–09).
3. The original specs (10–11), only if requirements are in question.

Or upload `CHATGPT_CONTEXT_RESTORE_ENVIRONMENT_20261010.zip`, which contains all of these files.
