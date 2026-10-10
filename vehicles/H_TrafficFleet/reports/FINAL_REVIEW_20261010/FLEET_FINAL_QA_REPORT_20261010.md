# Traffic fleet: final Blender QA report (2026-10-10)

All work is Blender-only: no FBX, no UnityTransfer, no Unity files. **No vehicle was frozen in this pass.** Freezing waits for your approval.

**Approval images:**

`/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/reports/FINAL_REVIEW_20261010/` (15 MB)

---

## 1. Verified production status

| # | Vehicle | Status (verified from the files, not earlier reports) | Run date |
|---|---|---|---|
| 1 | Sedan A r3 | **FROZEN**, unchanged. Manifest check: 246 files, 0 changed. | 2026-10-08 |
| 2 | Sedan B | **FROZEN**, unchanged. Manifest check: 259 files, 0 changed. | 2026-10-09 |
| 3 | Hatchback A | **FROZEN** since 2026-10-09 13:25, on your approval, so not "awaiting approval" as the brief said. Unchanged. **A defect was found, see §3.** | 2026-10-09 |
| 4 | SUV A | Production **v2** complete. Awaiting your visual approval. | 2026-10-10 02:19 |
| 5 | SUV B | Production **v3** complete. Awaiting your visual approval. | 2026-10-10 03:46 |
| 6 | Box Truck A | Production **r7** complete. Awaiting your visual approval. | 2026-10-10 01:08 |
| 7 | Bus A | Production **v3** complete. Awaiting your visual approval. | 2026-10-10 03:18 |
| — | Pickup A, Van A, Pulse EV | Postponed, untouched | — |

---

## 2. Corrections completed (root causes found by measurement)

| Vehicle | Defect | Root cause | Fix |
|---|---|---|---|
| **Box Truck A** | Large X across the windshield (`front`, `front34`, `day_front34`) | The windshield glass was a polar fan: one centre vertex with **99 edges**, sliver triangles up to **76:1**, and 24° of normal spread. Smooth shading along the spokes into the four corners showed as an X and shards. | Every glass panel in an end face is now a **structured grid** (`surf_grid`): cosine-spaced columns across, rows top to bottom, all projected onto the skin. Result: one coherent reflection. |
| Box Truck A | Angular dark shapes through the cab side glass | A near-black cab (dark seats and headliner), plus a collapse-decimated headliner | Light-grey seats, and the headliner now uses planar dissolve. Daylight now shows a readable seat and cab. |
| **Bus A** | Same fan "V/X" on the windshield and rear window | Same as the truck | Same glass grid |
| Bus A | Night: no clearance or identification lamps; tail lamps read as thin lines | Lamp set missing for a 2.55 m-wide, 12 m bus | Added: <ul><li>amber front and red rear clearance lamps;</li><li>3 red identification lamps (above the high-mount brake lamp);</li><li>amber front and mid side markers, red rear side markers;</li><li>reflectors;</li><li>tail-lamp glow fill.</li></ul> Surface positions were measured on the v2 body. |
| Bus A | Faint wave in the windshield reflection | Large end-cap pole behind the glass | Smaller cap ring (7 %), so the pole shrinks to a tiny area |
| **SUV A** | Small dark tick on the front bumper band; marks at the rear plate corners | The loft's end-cap **quad bridge folded** the skin: 22 inverted faces at the front, 96 at the rear (game body: 2 front, 32 rear) | End caps closed by an n-gon, with a small 7 % ring at the front so the pole leaves no reflection star. Result: **0 inverted faces at both ends.** LOD0 stays at **17,998** (within 18,000). |
| **SUV B** | Dotted "whiskers" off the rear plate's upper corners | Same fold: 96 inverted skin faces, and 12 game-body faces at x ±0.30, z 0.98 | Same fix at both ends. 0 inverted faces. The approved hood is untouched. |
| SUV B | The fix lowered LOD3 side silhouette overlap to 0.899 (limit 0.90) | The new caps changed the far-LOD collapse | LOD3 body ratio 0.065 → 0.075. Result: IoU **0.965**. LOD3 is 1,939 tris (10 % cap). |
| Renderer | Night views of the bus and truck were badly cropped | Night cameras weren't scaled for long and tall vehicles the way daylight cameras are | Night uses the same scaling. The night follow-camera views stay at game distances. |

**Earlier truck fixes are preserved:**
- the windshield opening;
- the rear-door crack fix;
- the fin removal;
- smooth metal trims;
- truck wheels;
- the marker lamps.

**Rollback copies:**
- Truck: `_rollback_r4`, `_rollback_r6`.
- Bus: `_rollback_v1`, `_rollback_v2`.
- SUV A and SUV B: `_rollback_v1`.
- SUV B also keeps its failed v2 run as `_superseded_v2`.

---

## 3. Remaining visual issues

1. **Hatchback A (frozen): visible marks around the rear plate.**
   - The plate-recess outline bulges into a hexagon at the top and bottom centre.
   - Crack-like marks sit below the plate's lower corners. The game body has 18 inverted faces at x ±0.22, z 0.70.
   - Evidence: `FINAL_REVIEW_20261010/Traffic_Hatchback_A/FROZEN_plate_rear_defect.jpg`.
   - **Fixing it needs you to approve unfreezing it.** I have not touched it.
2. **SUV A hood and fascia: zebra-only stepping.**
   - The game mesh's baked normal map shows centimetre-scale stepping, and only in zebra close-ups.
   - Tested in scratch, none of which removed it:
     - 4× supersampled bake;
     - dithered 8-bit output;
     - 4096 bake;
     - no hood dissolve.
   - So it is the bake correction limit of the coarse game mesh against the smooth master. It does not show in studio, daylight or game renders.
   - A real fix means a denser hood and fascia mesh, which SUV A's 18,000 budget (17,998 used) doesn't allow. That's your call: raise the budget, or accept.
3. **Stand-in road.** Daylight, game and night renders use a stand-in road because `environment/` is archived.
4. **Minor realism limits, unchanged since the earlier reports:**
   - generic plates and badges;
   - single review paint colours;
   - the truck's mirror heads are body colour;
   - the car-derived cab interior on the truck.

---

## 4–6. Budgets and validation

**Triangles per LOD** (LOD0 / LOD1 / LOD2 / LOD3):

| Vehicle | LOD0 / LOD1 / LOD2 / LOD3 | Budget |
|---|---|---|
| Sedan A r3 | 14,961 / 7,756 / 3,546 / 1,383 | 10–15k |
| Sedan B | 17,987 / 8,739 / 4,012 / 1,746 | 12–18k |
| Hatchback A | 17,126 / 8,367 / 3,880 / 1,647 | 12–18k |
| SUV A | 17,998 / 8,768 / 4,027 / 1,728 | 12–18k |
| SUV B | 19,840 / 9,566 / 4,325 / 1,939 | 13–20k (approved) |
| Box Truck A | 20,063 / 10,765 / 4,796 / 2,591 | 15–25k |
| Bus A | 34,154 / 14,774 / 6,114 / 2,903 | 20–35k |

**Materials, draw calls and validation result:**

| Vehicle | Materials per LOD | Draw calls per LOD | Validation |
|---|---|---|---|
| Sedan A r3 | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0 errors at freeze |
| Sedan B | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0 errors at freeze |
| Hatchback A | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | 0 errors at freeze |
| SUV A | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | **16 PASS, S1 PASS, 1 FAIL (check 1), FBX SKIP** |
| SUV B | 8 / 8 / 8 / 6 | 19 / 19 / 19 / 13 | **16 PASS, S1 PASS, 1 FAIL (check 1), FBX SKIP** |
| Box Truck A | 8 / 8 / 8 / 6 | 20 / 20 / 20 / 14 | **16 PASS, S1 PASS, 1 FAIL (check 1), FBX SKIP** |
| Bus A | 8 / 8 / 8 / 6 | 20 / 20 / 20 / 14 | **16 PASS, S1 PASS, 1 FAIL (check 1), FBX SKIP** |

**What the 16 checks cover:**
- hierarchy;
- complete LODs;
- orientation;
- wheel pivots and front steering references;
- ground clearance;
- triangle budget;
- material slots;
- LOD silhouette;
- shared materials only;
- independent light channels;
- textures;
- UVs and atlas cells;
- topology;
- colliders and CenterOfMass;
- QA renders present.

S1 is the shading screen.

**Check 1** (protected files) fails for every vehicle for one reason only: the frozen `environment/` folder (1,186 files) is archived on the external drive at your request.

**Worst S1 per vehicle:**

| Vehicle | Worst mesh |
|---|---|
| SUV A | 0.14 % |
| SUV B | 0.17 % |
| Box Truck A | Body LODs 0.0 % |
| Bus A | 0.48 % |

**Check 9 (LOD silhouette), max dimension delta:**

| Vehicle | Delta |
|---|---|
| SUV A | 4.6 mm |
| SUV B | 2.2 mm |
| Truck | 0.0 mm |
| Bus | 0.0 mm |

---

## 7. Visual evidence (in `FINAL_REVIEW_20261010/`)

**Overview:**
- `FLEET_7_FINAL_OVERVIEW.jpg`: one row per vehicle, showing studio front ¾, rear ¾, daylight and night.

**Per vehicle:**
- `<vehicle>_REVIEW.jpg`, with 4 rows:
  - studio front ¾ / rear ¾ / side;
  - daylight ×3;
  - night front ¾ / rear ¾ / follow camera;
  - gameplay close / normal / far.
- `<vehicle>_LOD_comparison.jpg`.

**Night views for the three frozen cars** were rendered read-only into the review folder. The frozen files are unchanged.

**Before / after:**

| Vehicle | Sheets |
|---|---|
| Box Truck A | `sheet_windshield_r6_vs_r7`, `sheet_night_lights` (running vs brake / indicator / reverse), `sheet_marker_lamps_wheels`, `sheet_before_r4_vs_after_r6`, `sheet_defect_history` |
| Bus A | `windshield_before_after` |
| SUV A | `bumper_rear_before_after` (bumper, rear plate, hood zebra) |
| SUV B | `plate_before_after` |
| Hatchback A | `FROZEN_plate_rear_defect.jpg` |

**Night lighting (truck):** running, brake, indicator and reverse are independently switchable and visibly distinct. None are blown out. The emitters are small boxes, which adds no realtime light cost.

**Night lighting (bus):** tail glow, the clearance and identification row, and side markers are all visible from the follow camera.

---

## 8. Frozen asset integrity

- `va_frozen_check.py`: **PASS.** All 9 releases have 0 changed or missing files:
  - Zero Gap R, Titan GT (+r1), Vortex R (+r1), Raven XR;
  - Hatchback A, Sedan A r3, Sedan B.
- `va_integrity.py`: **FAIL**, with 0 changed, 0 added and 1,186 removed outside `vehicles/`.
  - All 1,186 are the archived `environment/` folder.
  - The archive was hash-verified: all 1,186 files match.
  - Nothing is corrupted. This is the archive condition only, reported separately and not hidden.
- No manifest was edited.

---

## 9. Disk

| Item | Status |
|---|---|
| Free space | **9.0 GB**. No Blender or Unity process is running; swap is 3.1 GB. |
| `vehicles/_TO_DELETE_cleanup_20261009/` | **494 MB, verified safe and not deleted** (details below). |
| New rollback and superseded folders from this pass | About 0.8 GB. They can be staged the same way after you approve the final versions. |

**What the staging folder holds** (41 items in total):
- 24 failed or superseded attempts (407 MB, 30 .blend files of superseded runs);
- 14 v1 blockout previews (14 MB);
- 3 comparison source-frame folders (73 MB).

**Why it is safe:**
- Every item is still present.
- None has been re-created at its original path.
- None is referenced by any of the freeze manifests. One name match, SUV A's `_superseded_prod1`, is only a name collision with Hatchback A's own folder.

**To recover the space, after your OK:**

`rm -rf /Users/meetshah/Documents/blender/vehicles/_TO_DELETE_cleanup_20261009`

---

## 10. Files awaiting your approval

| Vehicle | Final file | Validation report |
|---|---|---|
| SUV A | `Traffic_SUV_A/blend/trafficsuva_09_export_ready.blend` | `Traffic_SUV_A/reports/trafficsuva_validation.txt` |
| SUV B | `Traffic_SUV_B/blend/trafficsuvb_09_export_ready.blend` | `Traffic_SUV_B/reports/trafficsuvb_validation.txt` |
| Box Truck A | `Traffic_Box_Truck_A/blend/trafficboxtrucka_09_export_ready.blend` | `Traffic_Box_Truck_A/reports/trafficboxtrucka_validation.txt` |
| Bus A | `Traffic_Bus_A/blend/trafficbusa_09_export_ready.blend` | `Traffic_Bus_A/reports/trafficbusa_validation.txt` |

**Decisions for you:**
1. Approve SUV A, SUV B, Box Truck A and Bus A for a Blender-only freeze, or list corrections.
2. Hatchback A: unfreeze it so the plate-area fold can be fixed, or keep it as is.
3. SUV A: accept the zebra-only hood stepping, or raise its budget for a denser hood mesh.
4. Approve deleting the staging folder (494 MB).
