# Night review, rig v2 (2026-10-10)

**These are Blender preview renders (Cycles). They are not Unity gameplay results.** Night visibility in Unity is unverified until runtime testing.

## The two labelled conditions

| Folder | Condition | Purpose |
|---|---|---|
| `<vehicle>/realistic/` and `*_NIGHT_REALISTIC.jpg` | **Realistic highway night** | Dark roadside. A deep-blue sky with a warm light-pollution glow at the horizon, cool moonlight, and five warm LED street lights, two of them far ahead and behind. Running lights on (DRL, headlamp, tail, marker). AgX Base Contrast at real exposure. This approximates night gameplay. |
| `<vehicle>/visibility_qa/` and `*_NIGHT_VISIBILITY_QA.jpg` | **Night visibility QA** | The same scene plus controlled soft fills (overhead and both sides), AgX Medium Low Contrast, and +0.4 EV. Use it to judge shape, surfaces, glass and lamp placement. **It is not a gameplay condition.** |
| `<vehicle>/brake_on/` and `FLEET_NIGHT_RUNNING_vs_BRAKE.jpg` | Realistic, with brakes on | Brake differentiation and overexposure check |

## Camera coverage per vehicle (realistic)

- **Front ¾, rear ¾, side.**
- **Rear follow at close, normal and far** (7.5 / 22 / 60 m).
- **Front approach at close, normal and far** (10 / 25 / 60 m).

For the truck and bus, the follow and approach cameras keep a car's gap to the vehicle's real rear and front. Without this, the bus close camera sat inside the bus.

## Sheets

| Sheet | Contents |
|---|---|
| `FLEET_NIGHT_REALISTIC_OVERVIEW.jpg` | 8 rows (7 vehicles plus Hatchback A r2) × front ¾, rear ¾, follow normal, approach normal |
| `FLEET_NIGHT_VISIBILITY_QA_OVERVIEW.jpg` | 8 rows × QA front ¾, rear ¾, side |
| `FLEET_NIGHT_OLD_vs_NEW.jpg` | 7 rows × (old v1 rear ¾ / new rear ¾ / old follow normal / new follow normal), with **identical cameras** |
| `<vehicle>/<vehicle>_NIGHT_OLD_vs_NEW.jpg` | Front ¾, rear ¾, follow close and follow normal: old (left) vs new (right) |
| `FLEET_NIGHT_RUNNING_vs_BRAKE.jpg` | Sedan B, SUV B, Box Truck A and Bus A: running lights vs brakes on |

**Scope of changes:** frozen vehicles were rendered read-only. **No vehicle asset was changed by the night work**; it is all in `scripts/ts_night_rig.py` and the night views in `scripts/ts_render.py`.
