# Vehicle master inventory

Updated 2026-10-09. Machine-readable copy: `VA_vehicle_inventory.json` → `releases`.

| Vehicle | Phase | Status | Unity import (preferred) |
|---|---|---|---|
| Hypercar | — | FROZEN (flagship reference) | `new_car (hypercar_08_unity_export)` |
| Zero Gap R | B | FROZEN — shading QA 2026-10-08: LOD1 trim / lights normal smears confirmed visually (LOD0 flags are false positives) — r1 proposed, awaiting approval | `vehicles/B_ZeroGapR/UnityTransfer/` |
| Titan GT | C | FROZEN original release — SUPERSEDED for import by r1 (LOD1-3 panel-gap shading tears) | `—` |
| Titan GT r1 | C revision r1 | FROZEN corrected revision — PREFERRED Unity import candidate — shading QA 2026-10-08: Lights_LOD1 tail-lamp shards (mild) — r2 normals-only proposed, awaiting approval | `vehicles/C_TitanGT_r1/UnityTransfer/` |
| Vortex R | D | FROZEN original release — SUPERSEDED for import by r1 (LOD1 trim normal tears) | `—` |
| Vortex R r1 | D revision r1 | FROZEN corrected revision — PREFERRED Unity import candidate | `vehicles/D_VortexR_r1/UnityTransfer/` |
| Raven XR | E | FROZEN | `vehicles/E_RavenXR/UnityTransfer/` |
| Pulse EV | F | POSTPONED by the project owner — design blockout kept untouched | `—` |
| Traffic Sedan A r3 | H (traffic) | **FROZEN** — Blender production complete · visual approval for traffic gameplay · **Unity runtime verification pending** (not photorealistic / not AAA). H1 and r2 kept for reference only | `vehicles/H_TrafficFleet/Traffic_Sedan_A_r3/UnityTransfer/` |
| Traffic Sedan B | H (traffic) | **FROZEN (Blender-only) 2026-10-09** — no FBX / UnityTransfer; Unity runtime verification pending | `—` (Blender-only) |
| Traffic Hatchback A | H (traffic) | final production complete (Blender-only, validation 0 errors) — AWAITING FINAL APPROVAL, not frozen | `—` |
| Traffic SUV A | H (traffic) | final production complete (Blender-only, validation 0 errors) — AWAITING FINAL APPROVAL, not frozen | `—` |
| Traffic SUV B | H (traffic) | final production complete (Blender-only, validation 0 errors vs 13k-20k class budget — budget sign-off pending) — AWAITING FINAL APPROVAL, not frozen | `—` |
| Traffic Box Truck A | H (traffic) | design blockout — awaiting visual approval | `—` |
| Traffic Bus A | H (traffic) | design blockout — awaiting visual approval | `—` |
| Traffic Pickup A / Van A | H (traffic) | POSTPONED by the project owner (Pickup A v2 blockout preserved) | `—` |

**Import the r1 revisions** for Titan GT (`C_TitanGT_r1`) and Vortex R (`D_VortexR_r1`); the originals stay frozen for reference only.
Verify: `python3 vehicles/A_Discovery/scripts/va_frozen_check.py` (all freeze manifests) and `va_shading_qa.py` (mandatory LOD0-3 shading QA, see `VA_SHADING_QA_STANDARD.md`).
