# Phase A — Vehicle discovery and baseline

**Date:** 2026-10-08. **Status:** discovery complete; waiting for approval. No vehicle has been modified, nothing has been built, and nothing in a frozen folder was written.

## 1. Verdict

| Vehicle | Source on this workstation | Condition | Required work |
|---|---|---|---|
| **Hypercar** (flagship) | `new_car/hypercar_08_unity_export.blend` | Complete, FROZEN, meets every project convention | None. Read-only reference |
| **Unnamed racing car** | `racing_car_00 … 09.blend` (workspace root) + `textures/racing_car/` | Complete multi-LOD car with significant quality and pipeline defects (§3) | Probably the starter car you call **Zero Gap R**. Its defects match your Zero Gap R brief almost exactly. **Needs your confirmation** |
| **Zero Gap R** | **Not found** under that name | — | If the racing car is Zero Gap R: optimisation remaster of that file. Otherwise you must provide the source |
| **Titan GT** | **Not found** | — | A remaster needs the source from your Unity project. Without it, an original new build that keeps the "very stable GT" identity |
| **Vortex R** | **Not found** | — | Full original build (as planned) |
| **Raven XR** | **Not found** | — | Full original build (as planned) |
| **Pulse EV** | **Not found** | — | Full original build (as planned) |
| **Existing traffic vehicles** | **None found** | — | Phase G needs their source files; otherwise Phase H builds the whole fleet |
| Traffic fleet (9 archetypes) | None | — | Phase H: Sedan A/B, Hatchback A, SUV A/B, Pickup A, Van A, Box Truck A, Bus A |

## 2. How the search was done (read-only)

- **Workspace** `/Users/meetshah/Documents/blender`: every `.blend`, the root reports and scripts, `new_car/`, `textures/`, both handoff bundles.
- **Whole home folder**, by Spotlight name search (`zero gap`, `titan`, `vortex`, `raven`, `pulse`, `traffic`, `sedan`, `hatchback`, `pickup`, `boxtruck`) and by a direct filesystem scan for 3D/Unity asset extensions: `.fbx .blend .obj .glb .gltf .prefab .unity .asset .unitypackage .max .ma .mb .dae .3ds .usdz`. `~/Library`, `node_modules`, `.git`, `vendor` and virtual-envs were excluded.
- **Results:**
  - The only vehicle models anywhere are the Hypercar and the racing-car series.
  - There is **no Unity project** on this machine (no `.prefab` / `.unity` / `.asset` files).
  - Two `sportcar.glb` files exist inside a Flutter package cache (`~/.pub-cache/.../mapbox_maps_flutter/example/assets/`). They are third-party example assets with unknown licensing, not project assets, and are **excluded**.
- **Design documents found** (read-only): `~/Downloads/premium_endless_traffic_racer_feature_document.md` and `~/Downloads/TrafficEscape-3D-Agent-Build-Spec.md`.
  - §9 of the feature document defines four of the player cars only as **gameplay personalities**:

    | Car | Strength | Weakness |
    |---|---|---|
    | Vortex R | Extreme speed and acceleration | Less stable |
    | Titan GT | Very stable, strong braking | Heavier acceleration |
    | Pulse EV | Instant acceleration, clean handling | Lower top-end drama |
    | Raven XR | Balanced sports setup | — |

  - **Zero Gap R appears in neither document.**
  - Traffic types listed: sedan, hatchback, SUV, van, pickup, truck, bus, motorcycle (the build spec adds taxi and police).
  - Both documents ask for **original fictional designs** and **mobile-appropriate polygon counts**.

## 3. Audit — unnamed racing car (`racing_car_09_unity_export_ready.blend`)

Measured with `scripts/va_audit.py` (data in `VA_audit_racing_car_09.json`). Renders are in `previews/VA_racing_car_09_*.png` and side by side with the Hypercar in `previews/VA_compare_racingcar_vs_hypercar.jpg`, using identical camera rig and lighting.

**Measurements**

| Item | Value |
|---|---|
| Dimensions (LOD0, with mirrors) | 4.549 × 2.006 × 1.200 m (L × W × H) |
| Wheelbase / track | 2.70 m / 1.65 m |
| Wheel radius | 0.3445 m front, 0.3645 m rear |
| LOD0 | 176,152 tris · **642 objects** · 27 materials · 49 textures |
| LOD1 | 99,084 tris · 452 objects · 27 materials |
| LOD2 | 44,985 tris · 248 objects · 22 materials |
| LOD3 | 16,386 tris · 199 objects · 21 materials |
| File contents | 2,358 objects in total: 2,059 meshes, 231 curves, **25 cameras, 5 lights**. A hidden high-res reference master of 251,080 tris. 53 collections |
| Colliders | 4 convex closed pieces (Body, Front, Rear, Roof), 96 tris in total, no materials |
| References | `CenterOfMass` (0, 0.22, 0.37); front/rear axle references; 4 `WheelColliderRef_*` |
| Textures | 88 images, **221 MB**. Three UV channels (atlas, tiled `UV_Game`, radial `UV_Rotor`). Unity's standard Lit shader cannot use that layout; it needs a custom shader |
| Exports | **No FBX on disk.** The export notes use `FBX_SCALE_UNITS` with no axis bake, which differs from the project standard |

**Defects**

1. **Left/right mirrored against the project convention.**
   - Under the project convention (forward −Y, up +Z) the vehicle's left is +X. This car puts `Wheel_FL`, `Wheel_RL`, `WheelColliderRef_FL` and `WheelColliderRef_RL` on **−X**, its right side.
   - In Unity the "FL" wheel would be on the right.
   - The wheel pivots themselves are correct: ≤ 0.5 mm from the wheel centres.
2. **Front end** (matches your Zero Gap R brief):
   - no real headlight units, only two dark slots in the hood corners;
   - a flat red band over a large boxy black grille;
   - bumper corners are boxy blocks;
   - the splitter sticks out well beyond the body.
3. **Rear:**
   - tail lights read as **chrome strips, not red lights**, even at chase distance;
   - the exhaust tips poke out through the side of the rear bumper;
   - the diffuser fins look detached;
   - there is a stray glyph near the right tail light.
4. **Glass and roof:**
   - the glass renders grainy and frosted;
   - the roof hoop / A-pillar tubes sit outside the glass like an exposed roll cage;
   - the glass edges do not meet the body cleanly.
5. **Surfaces:** wavy reflections on the door panels; the panel edges are uneven.
6. **Topology (LOD0):** 366 zero-area faces, 2,438 n-gons, 183 duplicate vertices. There are no non-manifold edges and no inside-out shells.
7. **Draw calls:**
   - 642 separate render objects at LOD0, against 84 for the Hypercar;
   - 479 root objects with no `Car_Root` / `LODn_Root` hierarchy.
8. **Light channels:**
   - tail and brake share one red emissive, so the brake light cannot switch on its own;
   - there is no reverse channel;
   - the amber indicators are not split left and right.
9. **Budget:** LOD0 at 176k is above your new player target of 60–120k.
10. **Good, keep:** the proportions and stance, the multi-spoke rims, the brake discs with yellow calipers, the generic tire lettering, the interior (seats, dash, wheel), and the existing simple colliders and centre-of-mass reference.

**If this car is Zero Gap R**, the remaster scope is:
- fix the left/right convention;
- rebuild the front fascia (headlights, bumper, grille, hood, splitter) and the rear (red light units, exhaust integration, diffuser);
- glass as a single thin tinted sheet, with the pillars integrated;
- resurface the doors;
- clean the topology;
- merge the 642 objects into a proper hierarchy;
- reduce 27 materials to about 16 (atlases plus separate tail, brake, indicator L/R, reverse and DRL channels);
- a single standard UV layout with external textures (≈ 40 MB instead of 221 MB);
- LOD0–3 within the new budget, colliders, `Car_Root` hierarchy, and FBX export with axis bake and re-import validation.

## 4. Hypercar compliance check (reference, frozen — read only)

- **LODs:**

  | LOD | Tris | Objects | Materials |
  |---|---|---|---|
  | LOD0 | 206,329 | 84 | 24 |
  | LOD1 | 107,212 | 84 | 24 |
  | LOD2 | 53,807 | 73 | 20 |
  | LOD3 | 17,779 | 38 | 15 |

- **Conventions:** forward −Y, left +X (FL at +X), wheel pivots exact, wheelbase 2.78 m, track 1.67 m, 6 convex colliders, `Car_Root` / `LOD0_Root` hierarchy, `CenterOfMass`, all textures present.
- **Topology (LOD0):** 2 zero-area faces in `Body_LOD0`; nothing else.
- **Budget note:** its LOD0 (206k) is above the new 60–120k player target. It stays frozen as the flagship exception. New cars follow your new targets.

## 5. Budgets for the new work (from your master prompt)

| Class | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Player car | 60–120k | 40–60 % of LOD0 | 15–30 % | 5–10 % |
| Traffic | 8–25k (by size) | about 40–50 % | about 15 % | about 5 % |

The design document targets mobile, so I would aim for the lower half of each range and validate against gameplay-distance renders.

## 6. Remaster priority plan

| Phase | Vehicle | Approach | Blocker |
|---|---|---|---|
| **B** | Zero Gap R | Optimisation remaster of the racing car (if confirmed) | Your confirmation, or the real Zero Gap R files |
| **C** | Titan GT | Medium remaster | **The source from Unity**, or approval of an original new build |
| **D** | Vortex R | Original modern mid-engine supercar | None. Blockout first |
| **E** | Raven XR | Original Japanese-inspired 2-door front-engine coupe | None. Blockout first |
| **F** | Pulse EV | Original electric performance sedan (4 doors) | None. Blockout first |
| **G** | Existing traffic | Upgrade the existing fleet | **Source files from Unity**; if they don't exist, G is skipped and H covers the fleet |
| **H** | Traffic fleet | 9 archetypes on shared fleet materials | None (scope depends on G) |
| **I** | Final validation + transfer | — | — |

**Folder per phase:** `vehicles/<Phase>_<Vehicle>/` with `source_import/` (read-only copies), `blend/`, `exports/`, `textures/`, `previews/`, `reports/`, `scripts/`, `UnityTransfer/`.
- Checkpoints follow the master prompt's eleven steps: `<car>_01_audit` … `_09_export_ready`.
- Experiments run in scratch folders; checkpoints are never overwritten.

**If you want to hand over the Unity originals** (Titan GT, the traffic cars, or the real Zero Gap R): copy each car's model file (`.fbx` / `.blend` / `.obj` from the Unity project's `Assets/` folder) and its textures into `vehicles/_incoming/<Vehicle>/`, plus two or three screenshots from the game. Nothing else is needed. I will import them read-only and audit them like the racing car.

## 7. Integrity baseline

Recorded in `VA_workspace_baseline.json` before any work: **1,554 files** outside `vehicles/`.

| Group | Files |
|---|---|
| Environment P0–P3 (frozen) | 1,186 |
| Hypercar (frozen) | 108 |
| Racing-car blends | 13 |
| Handoff bundles | 28 |
| Root scripts | 79 |
| Root textures | 102 |
| Other root files | 38 |

The end-of-phase re-check (`VA_integrity_check.md`) confirms that nothing changed.

## 8. Files in this phase

| Folder | Contents |
|---|---|
| `scripts/` | `va_baseline.py`, `va_audit.py`, `va_render.py`, `va_sheet.py`, `va_integrity.py` |
| `reports/` | this report, `VA_vehicle_inventory.json`, `VA_audit_racing_car_09.json`, `VA_audit_hypercar_08.json`, `VA_workspace_baseline.json`, `VA_integrity_check.md` |
| `previews/` | 10 identical-rig views per car (front, rear, left, right, front ¾, rear ¾, top, interior through the glass, wheel close-up, chase on the frozen P0 road) and the comparison sheet |
