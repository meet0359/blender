# Vehicle specifications

Generated 2026-10-11 from the packaged FBX files (independent Blender 5.2.2 re-import of each file) and the release records. Unity space: +Z forward, +Y up, -X vehicle left, metres. Machine-readable: `04_Unity_Setup/Vehicle_Configuration/<vehicle>.json`.

| Vehicle | Type | Visual L x W x H (m) | Width incl. mirrors | Traffic footprint W x L (m) | Wheelbase (m) | Wheel radius F / R (m) | LOD0 / 1 / 2 / 3 tris | CenterOfMass | Light channels |
|---|---|---|---|---|---|---|---|---|---|
| Sedan A r3 | traffic | 4.649 x 2.060 x 1.468 | yes | 1.807 x 4.645 | 2.700 | 0.316 / 0.316 | 14,961 / 7,756 / 3,546 / 1,383 | [-0.0, 0.52, 0.22] | 7 |
| Sedan B | traffic | 4.971 x 2.180 x 1.493 | yes | 1.900 x 4.967 | 2.970 | 0.352 / 0.352 | 17,987 / 8,739 / 4,012 / 1,746 | [-0.0, 0.53, 0.08] | 7 |
| Hatchback A r2 | traffic | 4.267 x 2.080 x 1.516 | yes | 1.799 x 4.260 | 2.630 | 0.317 / 0.317 | 17,174 / 8,391 / 3,887 / 1,652 | [-0.0, 0.5, 0.18] | 7 |
| SUV A v2 | traffic | 4.479 x 2.190 x 1.704 | yes | 1.847 x 4.474 | 2.680 | 0.37 / 0.37 | 17,998 / 8,768 / 4,027 / 1,728 | [-0.0, 0.62, 0.12] | 7 |
| SUV B v3 | traffic | 4.978 x 2.300 x 1.811 | yes | 1.970 x 4.970 | 2.980 | 0.391 / 0.391 | 19,840 / 9,566 / 4,325 / 1,939 | [-0.0, 0.7, 0.1] | 7 |
| Box Truck A r7 | traffic | 7.070 x 2.544 x 3.254 | yes | 2.342 x 6.891 | 3.850 | 0.405 / 0.405 | 20,063 / 10,765 / 4,796 / 2,591 | [-0.0, 1.1, 0.4] | 8 |
| Bus A v4 | traffic | 12.008 x 2.984 x 3.198 | yes | 2.557 x 11.970 | 6.000 | 0.478 / 0.478 | 34,506 / 15,126 / 6,210 / 2,999 | [-0.0, 1.1, -0.3] | 8 |
| Hypercar | player | 4.695 x 2.211 x 1.173 | yes | - | 2.780 | 0.355 / 0.3775 | 206,327 / 107,210 / 53,786 / 17,747 | [-0.0, 0.35, -0.12] | 6 |
| Zero Gap R | player | 4.460 x 2.006 x 1.200 | yes | - | 2.700 | 0.3445 / 0.3645 | 89,681 / 44,794 / 20,372 / 6,513 | [-0.0, 0.37, -0.22] | 7 |
| Titan GT r1 | player | 4.814 x 2.230 x 1.272 | yes | - | 2.820 | 0.347 / 0.358 | 77,370 / 39,752 / 18,527 / 7,729 | [-0.0, 0.42, -0.15] | 7 |
| Vortex R r1 | player | 4.580 x 2.270 x 1.275 | yes | - | 2.720 | 0.339 / 0.348 | 73,665 / 34,060 / 15,026 / 6,146 | [-0.0, 0.38, -0.25] | 7 |
| Raven XR | player | 4.521 x 2.046 x 1.320 | yes | - | 2.680 | 0.331 / 0.341 | 74,271 / 34,711 / 15,185 / 5,818 | [-0.0, 0.44, 0.08] | 7 |

## Traffic footprint overrides (collision body, mirrors excluded)

| Vehicle | Width (m) | Width from hull | Length (m) | Height (m) | Centre (Unity) | Mirror-zone hulls excluded | Visual width incl. mirrors |
|---|---|---|---|---|---|---|---|
| Sedan A r3 | 1.8067 | Collision_Rear | 4.645 | 1.3081 | [0.0, 0.8192, -0.0496] | Collision_Cabin | 2.06 |
| Sedan B | 1.9001 | Collision_Rear | 4.9669 | 1.2996 | [0.0, 0.846, -0.0073] | Collision_Cabin | 2.18 |
| Hatchback A r2 | 1.7987 | Collision_Rear | 4.2597 | 1.3604 | [0.0, 0.8356, -0.0032] | Collision_Body, Collision_Cabin | 2.08 |
| SUV A v2 | 1.8473 | Collision_Rear | 4.4739 | 1.4809 | [0.0, 0.9501, 0.0029] | Collision_Cabin | 2.19 |
| SUV B v3 | 1.9702 | Collision_Rear | 4.9695 | 1.5492 | [0.0, 1.0181, 0.0048] | Collision_Cabin | 2.3 |
| Box Truck A r7 | 2.3423 | Collision_Rear | 6.8913 | 2.6435 | [0.0, 1.924, -0.0043] | Collision_Cabin, Collision_Front | 2.544 |
| Bus A v4 | 2.5572 | Collision_Body | 11.9699 | 2.6844 | [0.0, 1.6632, -0.002] | Collision_Cabin, Collision_Front | 2.984 |

Rule: width = the widest convex collision hull that is not wider than the vehicle's design body width + 3 cm (design width is only used to identify hulls that extend into the mirror zone); length and height = union of all collision hulls. All values are measured from the packaged FBX.

## Wheels (WheelColliderRef positions, Unity local to Car_Root)

| Vehicle | FL | FR | RL | RR | Radius F / R | Width F / R | Track F / R |
|---|---|---|---|---|---|---|---|
| Sedan A r3 | [-0.78, 0.316, 1.35] | [0.78, 0.316, 1.35] | [-0.7775, 0.316, -1.35] | [0.7775, 0.316, -1.35] | 0.316 / 0.316 | 0.205 / 0.205 | 1.56 / 1.555 |
| Sedan B | [-0.8125, 0.352, 1.62] | [0.8125, 0.352, 1.62] | [-0.82, 0.352, -1.35] | [0.82, 0.352, -1.35] | 0.352 / 0.352 | 0.245 / 0.245 | 1.625 / 1.64 |
| Hatchback A r2 | [-0.77, 0.317, 1.25] | [0.77, 0.317, 1.25] | [-0.765, 0.317, -1.38] | [0.765, 0.317, -1.38] | 0.317 / 0.317 | 0.225 / 0.225 | 1.54 / 1.53 |
| SUV A v2 | [-0.8, 0.37, 1.32] | [0.8, 0.37, 1.32] | [-0.805, 0.37, -1.36] | [0.805, 0.37, -1.36] | 0.37 / 0.37 | 0.235 / 0.235 | 1.6 / 1.61 |
| SUV B v3 | [-0.84, 0.391, 1.55] | [0.84, 0.391, 1.55] | [-0.845, 0.391, -1.43] | [0.845, 0.391, -1.43] | 0.391 / 0.391 | 0.275 / 0.275 | 1.68 / 1.69 |
| Box Truck A r7 | [-0.84, 0.405, 2.3] | [0.84, 0.405, 2.3] | [-0.84, 0.405, -1.55] | [0.84, 0.405, -1.55] | 0.405 / 0.405 | 0.225 / 0.225 | 1.68 / 1.68 |
| Bus A v4 | [-1.05, 0.478, 3.3] | [1.05, 0.478, 3.3] | [-0.95, 0.478, -2.7] | [0.95, 0.478, -2.7] | 0.478 / 0.478 | 0.275 / 0.275 | 2.1 / 1.9 |
| Hypercar | [-0.835, 0.355, 1.39] | [0.835, 0.355, 1.39] | [-0.835, 0.3775, -1.39] | [0.835, 0.3775, -1.39] | 0.355 / 0.3775 | 0.31 / 0.35 | 1.67 / 1.67 |
| Zero Gap R | [-0.825, 0.345, 1.35] | [0.825, 0.345, 1.35] | [-0.835, 0.365, -1.35] | [0.835, 0.365, -1.35] | 0.3445 / 0.3645 | 0.296 / 0.336 | 1.65 / 1.67 |
| Titan GT r1 | [-0.845, 0.347, 1.41] | [0.845, 0.347, 1.41] | [-0.855, 0.358, -1.41] | [0.855, 0.358, -1.41] | 0.347 / 0.358 | 0.265 / 0.305 | 1.69 / 1.71 |
| Vortex R r1 | [-0.86, 0.339, 1.36] | [0.86, 0.339, 1.36] | [-0.85, 0.348, -1.36] | [0.85, 0.348, -1.36] | 0.339 / 0.348 | 0.255 / 0.325 | 1.72 / 1.7 |
| Raven XR | [-0.83, 0.331, 1.34] | [0.83, 0.331, 1.34] | [-0.835, 0.341, -1.34] | [0.835, 0.341, -1.34] | 0.331 / 0.341 | 0.255 / 0.285 | 1.66 / 1.67 |

Truck and bus rear widths are per tyre; their rear wheel meshes carry dual tyres.

## LOD0 triangle budget (Unity validation uses 15,000 for traffic)

| Vehicle | LOD0 tris | vs 15,000 |
|---|---|---|
| Sedan A r3 | 14,961 | within |
| Sedan B | 17,987 | over by 2,987 |
| Hatchback A r2 | 17,174 | over by 2,174 |
| SUV A v2 | 17,998 | over by 2,998 |
| SUV B v3 | 19,840 | over by 4,840 |
| Box Truck A r7 | 20,063 | over by 5,063 |
| Bus A v4 | 34,506 | over by 19,506 |
