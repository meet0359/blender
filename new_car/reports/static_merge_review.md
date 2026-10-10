# Static merge review (Phase 8): nothing merged yet

Goal: cut draw calls later without losing gameplay control. Objects are listed per LOD (same pattern LOD0-LOD3
unless noted).

## KEEP_SEPARATE (functional transforms or runtime control)

| Objects | Why |
|---|---|
| `Wheel_FL/FR/RL/RR_LODn` (+ child `Tire_*`, `BrakeDisc_*`) | roll on local X; tire + rotor ride on the wheel |
| `SteerPivot_FL/FR_LODn` (+ `Caliper_FL/FR`) | front steering yaw; calipers steer but never roll |
| `Caliper_RL/RR_LODn` | static, but keep separate for the caliper colour option (MAT_BrakeCaliper) |
| `SteeringWheel_LOD0/1/2` | rotates on its column axis (local Z) |
| `Paddle_L/R_LOD0/1` | separate pivots (paddle pull animation) |
| `Door_L/R_LOD0/1` + `DoorPanel_*`, `Window_F*`, `DoorHandle_*` | opening doors (hinge empties) |
| `ActiveSpoiler_LODn` | rotates about its hinge (default 3 deg) |
| `Headlight_*`, `Taillight_*` (MAT_LED_White / ProjectorLens / LED_Red / LED_Brake / LED_Amber / LED_Reverse) | independently switched light channels |
| `HeadlightLens_*`, `TaillightLens_*`, all glass | transparent pass; side windows move with doors |
| `InstrumentCluster`, `CenterScreen` (displays) | may be driven live by the game |
| `COLLIDERS` pieces | physics only, never merged with render meshes |

## SAFE_TO_MERGE_LATER (static, same LOD, no runtime control)

| Merge group | Members | Expected saving |
|---|---|---|
| Body static | `Body`, `Body_Buttress`, `ArchLip_*`, `Mirror_*` (+ `MirrorGlass_*` as a 2nd material) | ~8 objects -> 1 |
| Aero / trim static | `FrontSplitter`, `RearDiffuser`, `SideSkirt_*`, `SideIntakeVane_*`, `FrontIntakeVanes`, `RearVent_*`, `EngineVents`, `RearFascia_Trim`, `Exhaust_*`, `Chassis_*`, `ActiveSpoilerHinge` | ~14 objects -> 1 (1 trim atlas material + carbon) |
| Interior static | `Dashboard`, `Dashboard_Vents`, `CenterTunnel`, `CenterConsole`, `Seat_*`, `RearBulkhead`, `Headliner`, `PillarTrim`, `Interior_Tub`, `EngineBay_Detail`, `RearViewMirror`, `SteeringColumn`, `Pedal_*` | ~16 objects -> 1-2 (atlas + carbon + emissive strips) |
| Static light housings | housing/bezel parts of `Headlight_*` / `Taillight_*` | only if emitters are split into their own objects first |

Rule: merge per LOD, keep each merged object's origin at Car_Root / LOD root, and re-check UVs + material slots after
joining (all members already share their atlas UV layout, so no repack is needed).
