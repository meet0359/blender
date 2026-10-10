# Original phase specifications (P0 and P1), verbatim

These are the exact instructions I gave for each environment phase, in order. They are the source of truth for what each phase had to deliver. Each phase was completed against them; outcomes, deviations and known limitations are in the per-phase digests.


====================================================================================================
# SPEC: P0-BLENDER-01 — Road Foundation
====================================================================================================

````text
<ide_opened_file>The user opened the file /Users/meetshah/Documents/blender/materials_report.md in the IDE. This may or may not be related to the current task.</ide_opened_file>



ACT AS:

A senior AAA Environment Artist, Blender Technical Artist, Hard-Surface Artist,
Procedural Modeling Specialist and Game Asset Optimization Expert with 10+ years
of production experience.

You are working on a BLENDER-ONLY production workstation.

IMPORTANT MACHINE CONTEXT:

This Mac DOES NOT contain the Unity project.

Do NOT look for Unity.

Do NOT install Unity.

Do NOT create Unity scenes, materials, prefabs, shaders or scripts.

Do NOT attempt gameplay testing.

This workstation is ONLY for:

BLENDER MODELING
→ UVs
→ MATERIAL SOURCE SETUP
→ LODs
→ COLLIDERS WHERE APPROPRIATE
→ VALIDATION
→ FBX EXPORT
→ ASSET PACKAGE PREPARATION

The exported assets will later be copied to another computer that contains
the actual Unity racing-game project.

============================================================
CURRENT WORKSPACE
============================================================

Main Blender workspace:

/Users/meetshah/Documents/blender

Existing vehicle work must remain untouched.

Existing folders such as:

new_car/
exports/
textures/
reports/
scripts/

belong to previous vehicle-generation work.

Do NOT overwrite or reorganize finished car assets.

============================================================
NEW ENVIRONMENT ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/

Use this structure:

environment/
├── P0_RoadFoundation/
│   ├── blend/
│   ├── exports/
│   ├── textures/
│   ├── previews/
│   ├── reports/
│   └── scripts/
│
├── P1_Vegetation/
├── P1_Terrain/
├── P1_Props/
├── P1_Tunnel/
├── P2_City/
├── P2_Bridges/
└── P3_MountainCoastal/

Do NOT create all assets now.

For this task work ONLY in:

environment/P0_RoadFoundation/

============================================================
PHASE NAME
============================================================

P0-BLENDER-01

AAA MODULAR HIGHWAY ROAD FOUNDATION

This is the FIRST Blender environment production phase.

============================================================
PROJECT CONTEXT
============================================================

This is a realistic racing game.

Target visual direction:

PREMIUM MODERN PC / CONSOLE RACING GAME QUALITY

while still being optimizable for mobile.

The Unity gameplay architecture is already established.

IMPORTANT:

The road system streams STRAIGHT road chunks of approximately 40 meters.

The player primarily changes lanes laterally.

Therefore:

DO NOT create:

- Road_Curve_L
- Road_Curve_R
- Road_Up
- Road_Down
- spline-road systems
- procedural curved track systems

Do not redesign gameplay.

The Unity project may later use a curved-world shader to visually fake bends
or hills.

Your job is to create assets compatible with the current STRAIGHT 40 m system.

============================================================
PRIMARY GOAL
============================================================

Replace the current flat/basic highway geometry with a premium modular road kit.

The road system must feel:

- realistic
- properly engineered
- modern
- detailed
- modular
- reusable
- optimized
- streamable
- visually premium

This phase focuses on GEOMETRY and BLENDER ASSET PREPARATION.

Do NOT attempt to build the final Unity asphalt shader.

============================================================
REAL-WORLD SCALE
============================================================

Use metric units.

1 Blender unit = 1 meter.

Road modules must align exactly.

Primary length:

40.000 m

Secondary optional module:

20.000 m

Never use approximate module lengths.

============================================================
VEHICLE / ROAD SCALE
============================================================

The flagship hypercar is approximately:

Length:
4.695 m

Width:
2.052 m

Use this as a visual scale reference.

Road lanes must feel realistic for high-speed highway driving.

Use a lane width around:

3.5–3.7 m

unless the existing road-reference geometry clearly requires another value.

Do not change lane count from the current game without reason.

Current target:

4-lane carriageway.

============================================================
PHASE 01 — DISCOVERY
============================================================

Before modeling:

Inspect available existing road references in this Blender workspace.

Search for:

- reference images
- old road exports
- AssetPreviews
- road screenshots
- existing road dimensions if available

Do NOT assume unavailable Unity files exist.

If no original road mesh is present:

use the documented 40 m module architecture and reasonable real-world dimensions.

Create:

reports/P0_road_discovery.md

Document:

- references found
- assumptions
- chosen lane width
- total carriageway width
- shoulder widths
- median treatment
- road thickness
- module grid

============================================================
PHASE 02 — MASTER ROAD MODULE
============================================================

Create:

Road_4Lane_40m

This is the primary base module.

It should contain:

- asphalt carriageway
- lane layout
- realistic cross-section
- subtle crown/camber
- shoulder regions
- road-edge transitions
- clean modular end boundaries

Do NOT create an absolutely flat plane.

Use subtle roadway crown/camber.

Do NOT exaggerate elevation enough to affect existing gameplay assumptions.

============================================================
ROAD CROSS-SECTION
============================================================

The cross-section should support:

- 4 driving lanes
- outside shoulder
- median-side edge
- drainage
- road-edge breakup
- roadside connection

Use believable thickness.

The visible asphalt should not look like a paper sheet.

============================================================
MODULE ENDS
============================================================

At Z/Y direction depending on chosen Blender road axis:

start and end geometry must match exactly.

No vertex mismatch.

No seam.

No height difference.

No UV discontinuity caused by geometry.

Two copies placed end-to-end must appear continuous.

============================================================
ROAD ORIENTATION
============================================================

For environment assets standardize orientation:

+Z = UP

Choose a consistent forward axis for road length.

Preferred for Blender environment source:

-Y or +Y according to the established Blender vehicle/project convention.

Document it.

Do NOT arbitrarily switch axes between modules.

============================================================
ROAD MODULES TO CREATE
============================================================

Create the following:

01.
Road_4Lane_40m

02.
Road_4Lane_20m

03.
Road_4Lane_Joint

04.
Shoulder_Paved_L

05.
Shoulder_Paved_R

06.
Shoulder_Gravel_L

07.
Shoulder_Gravel_R

08.
EdgeBreakup_Verge_L

09.
EdgeBreakup_Verge_R

10.
Median_Concrete

11.
Median_Grass

12.
Median_Barrier

13.
Drain_Channel_4m

14.
Drain_Grate

15.
Road_Reflector

16.
RumbleStrip

Do NOT start bridge/tunnel modules yet.

============================================================
ROAD JOINT
============================================================

Road_4Lane_Joint should represent:

- expansion seam
or
- asphalt joint

Keep subtle.

Do not create a huge bump that would affect vehicle physics.

============================================================
SHOULDERS
============================================================

Create multiple shoulder options.

Paved shoulder:

- asphalt
- slightly different wear
- clear edge

Gravel shoulder:

- transition strip
- edge breakup

Do NOT physically model individual stones at high density.

Use material/normal detail later.

============================================================
ROAD EDGE BREAKUP
============================================================

Create believable road-to-ground transition geometry.

Current road should no longer appear like:

perfect rectangular asphalt floating over green ground.

Use:

- irregular edge
- shallow broken asphalt
- subtle verge transition

Do not create excessive jagged geometry.

============================================================
MEDIANS
============================================================

Create:

Median_Concrete

Median_Grass

Median_Barrier

All must fit the same road grid.

Do not build one huge combined road mesh when modular components can be reused.

============================================================
DRAINAGE
============================================================

Create:

Drain_Channel_4m

Drain_Grate

Use realistic proportions.

Details important to silhouette may use geometry.

Fine grate repetition should preferably be represented with:

- normal map
- trim sheet
or
- low-cost repeating geometry

Do not model hundreds of tiny holes unnecessarily.

============================================================
ROAD REFLECTORS
============================================================

Create a reusable:

Road_Reflector

or CatEye_Reflector.

Small but premium quality.

Use simple geometry.

Prepare separate material slots for:

- body
- reflective/emissive surface

These will later be instanced in Unity.

Do NOT duplicate thousands of reflectors into the road mesh.

============================================================
RUMBLE STRIP
============================================================

Create:

RumbleStrip_4m

or similar modular length.

Use enough geometry to create the major profile.

Fine surface grooves can use normal detail.

============================================================
ROAD MARKINGS
============================================================

Do NOT permanently model thousands of lane markings into high-density geometry.

Provide clean marking geometry/trim-ready strips for:

- lane divider
- road edge
- optional warning line

Prefer thin geometry strips.

Keep them slightly above the road:

approximately 1–3 mm

to prevent z-fighting.

============================================================
MATERIAL SOURCE STRUCTURE
============================================================

Create temporary Blender materials:

MAT_Road_Asphalt
MAT_Road_Marking_White
MAT_Road_Marking_Yellow
MAT_Road_Shoulder
MAT_Road_Concrete
MAT_Road_Metal
MAT_Road_Drain
MAT_Road_Reflector

These are review/source materials.

They are NOT final Unity shaders.

============================================================
ASPHALT SOURCE MATERIAL
============================================================

Create a high-quality Blender preview asphalt material.

It should show:

- dark neutral asphalt
- aggregate variation
- subtle normal detail
- roughness variation
- very subtle lane wear

Avoid:

- tan asphalt
- perfectly uniform asphalt
- extreme cracks everywhere
- mirror-like surface

============================================================
ROAD TEXTURE SOURCE
============================================================

Create texture-source preparation for:

BaseColor
Normal
Roughness
AO

If actual image textures are generated:

store them under:

textures/asphalt/

Use tileable maps.

Preferred source resolution:

2048 × 2048

or 4096 only if genuinely useful.

Do NOT generate unnecessary 8K textures.

============================================================
DECAL SOURCE KIT
============================================================

Prepare optional decal source textures/planes for later Unity use:

Crack_A
Crack_B
Crack_C

Patch_A
Patch_B

TarLine_A
TarLine_B

Skid_A
Skid_B

OilStain_A

Store under:

textures/decals/

These should NOT be permanently baked into every road module.

============================================================
UV STANDARD
============================================================

All renderable meshes must have:

UVMap

Prefer consistent world-aligned / tiling-compatible UV scale.

Road modules should support seamless tiling between 40 m chunks.

Do not stretch one 0–1 texture over an entire 40 m road.

Use repeating UV scale.

============================================================
TEXEL DENSITY
============================================================

Maintain consistent texel density across:

road
shoulder
concrete
drainage
markings

Do not waste texture density on invisible undersides.

============================================================
TRIM SHEET PREPARATION
============================================================

Prepare a shared road/prop trim layout if practical.

Possible trim elements:

- concrete edge
- painted stripe
- metal edge
- drain lip
- reflector strip

Do NOT create a huge complicated atlas in this first phase if it slows production.

============================================================
GEOMETRY QUALITY
============================================================

Do not create unnecessarily dense road surfaces.

Straight surfaces should remain efficient.

Use geometry where it affects:

- silhouette
- profile
- camber
- edge breakup
- drainage
- raised marking
- joints

Use materials/textures for:

- micro cracks
- aggregate
- fine wear
- small dirt
- tar detail

============================================================
LOD STRATEGY
============================================================

Create LODs for appropriate reusable road-side pieces.

Main road surface does not need aggressive traditional LOD if it is already low-poly.

However create LODs for:

- Drain_Grate
- Road_Reflector if useful
- Median/Barrier if geometry benefits
- other non-flat components

Use sensible budgets.

Do not create meaningless LODs that save only a few triangles.

============================================================
COLLISION
============================================================

Create simple collision meshes only where useful.

Road driving surface collision:

Collision_Road_40m

Keep it extremely simple.

It must follow the usable road surface but not micro-detail.

No cracks or reflectors in the collider.

For barriers/medians:

create simple box/convex collider references if useful.

Do not create physics-heavy complex collision.

============================================================
MODULAR SNAP VALIDATION
============================================================

Create a test assembly in Blender:

Road_4Lane_40m
+
Road_4Lane_40m
+
Road_4Lane_20m

Place end-to-end.

Validate:

- exact alignment
- no seams
- no visible height changes
- markings align
- shoulder aligns
- drainage aligns
- median aligns

============================================================
TEST STRIP
============================================================

Create a temporary approximately:

100–120 m road test strip

using repeated modules.

This is for Blender QA only.

Do NOT export the test strip as the primary asset.

Use it for preview rendering.

============================================================
PREVIEW ENVIRONMENT
============================================================

Create a simple neutral presentation setup.

Do not spend time creating the final game environment.

Use:

- neutral sky/world
- directional sun
- soft fill
- simple roadside ground

Purpose:

evaluate road geometry and materials.

============================================================
PREVIEW RENDERS
============================================================

Create:

previews/P0_road_top.png

previews/P0_road_driver_height.png

previews/P0_road_front_3q.png

previews/P0_road_side.png

previews/P0_road_joint_closeup.png

previews/P0_road_edge_closeup.png

previews/P0_road_drainage.png

previews/P0_road_reflector.png

previews/P0_road_100m_test.png

============================================================
OPTIONAL VEHICLE SCALE TEST
============================================================

If the completed Hypercar asset is easily accessible:

link or append ONLY a lightweight reference instance.

Use it for road-scale comparison.

Do NOT modify the Hypercar asset.

Do NOT save changes back into any vehicle .blend.

Do not include the Hypercar in the road export.

============================================================
FILE ORGANIZATION
============================================================

Create:

environment/P0_RoadFoundation/

Inside:

blend/
exports/
textures/
previews/
reports/
scripts/

============================================================
BLEND CHECKPOINTS
============================================================

Use:

blend/road_01_blockout.blend

blend/road_02_modular_geometry.blend

blend/road_03_materials_uv.blend

blend/road_04_lods_collision.blend

blend/road_05_export_ready.blend

Do not overwrite earlier checkpoints.

============================================================
SCRIPT ORGANIZATION
============================================================

Store generated Blender Python under:

scripts/

Suggested:

road_build.py
road_materials.py
road_validate.py
road_render.py
road_export.py

Do not place scripts randomly in root.

============================================================
MASTER ASSET COLLECTION
============================================================

Use collections:

ROAD_MASTER
ROAD_MODULES
ROAD_MARKINGS
ROAD_DRAINAGE
ROAD_SAFETY
ROAD_COLLIDERS
ROAD_QA
ROAD_PRESENTATION

============================================================
OBJECT NAMING
============================================================

Use exact meaningful names.

Examples:

Road_4Lane_40m
Road_4Lane_20m

Shoulder_Paved_L
Shoulder_Paved_R

Shoulder_Gravel_L
Shoulder_Gravel_R

Median_Concrete
Median_Grass
Median_Barrier

Drain_Channel_4m
Drain_Grate

Road_Reflector
RumbleStrip_4m

Collision_Road_40m

============================================================
TRANSFORMS
============================================================

Production export objects should have:

Scale:
1,1,1

No negative scales.

Apply transforms where safe.

Origins should be meaningful.

Road module origin:

prefer center or defined start snap point.

Whichever is chosen:

document consistently.

============================================================
SNAP POINTS
============================================================

Create empties:

Snap_Start
Snap_End

for primary road modules.

For 40 m module:

distance between snap points must be:

40.000 m

For 20 m:

20.000 m

This will make Unity placement easier.

============================================================
EXPORT ORIENTATION
============================================================

Prepare for Unity.

Unity target:

+Y up
+Z forward

Blender source orientation must be documented.

Use the same proven export logic/preset used successfully for the Hypercar where practical.

Do NOT blindly use Blender's Apply Transform option if it causes double axis conversion.

The previous vehicle pipeline already discovered that manual/in-memory axis conversion plus Apply Transform OFF was safer.

Reuse that logic where appropriate.

============================================================
EXPORT FORMAT
============================================================

Primary format:

FBX

Do NOT use GLB as the main runtime asset.

============================================================
EXPORT DIRECTORY
============================================================

Export to:

environment/P0_RoadFoundation/exports/

Create:

road_foundation_unity.fbx

Also export individual modular FBXs if that improves Unity import workflow:

Road_4Lane_40m.fbx
Road_4Lane_20m.fbx
Shoulders.fbx
Medians.fbx
Drainage.fbx
RoadSafety_Core.fbx

Choose the structure that results in the cleanest import.

Document it.

============================================================
EXPORT CONTENT
============================================================

Include only production assets.

Exclude:

- presentation camera
- Blender lights
- QA ground
- test strip
- Hypercar reference
- helper meshes
- hidden cutters
- temporary preview objects

============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

After export:

create a clean temporary Blender scene.

Re-import:

road_foundation_unity.fbx

Validate:

- orientation
- scale
- dimensions
- 40 m length
- 20 m length
- UVs
- normals
- material slots
- object names
- snap points if empties are exported
- collider placement

No assumptions.

============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

environment/P0_RoadFoundation/UnityTransfer/

with:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/

Copy final export files into that transfer package.

Do NOT copy .blend working checkpoints into the runtime transfer package unless separately requested.

============================================================
UNITY TRANSFER README
============================================================

Create:

UnityTransfer/README/ROAD_IMPORT_NOTES.md

Document:

- scale
- orientation
- module length
- lane width
- carriageway width
- material slots
- texture names
- UV conventions
- colliders
- snap points
- FBX names
- intended use
- excluded QA objects

Also clearly state:

THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.

UNITY-SIDE SHADERS, PREFABS, ROADSTREAMER CONFIGURATION AND PERFORMANCE TESTING
MUST BE DONE ON THE UNITY WORKSTATION.

============================================================
VALIDATION
============================================================

Create automated Blender validation.

Check:

- required objects exist
- naming
- dimensions
- 40 m module length
- 20 m module length
- snap-point distances
- scale
- normals
- UVs
- zero-area faces
- non-manifold geometry
- material slots
- collision meshes
- export selection
- texture links
- FBX re-import scale

Output:

reports/P0_road_validation.txt

Target:

0 errors.

============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P0_road_geometry.json

Include:

- triangles per asset
- vertices
- dimensions
- UV presence
- material count
- collider triangles

============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P0_road_export_manifest.json

Include:

- FBX files
- included objects
- excluded objects
- texture files
- scale
- coordinate conversion
- source blend
- module dimensions

============================================================
FINAL COMPLETION GATE
============================================================

Do NOT declare complete until:

1. Road_4Lane_40m exists.
2. It measures exactly 40 m.
3. Road_4Lane_20m exists.
4. It measures exactly 20 m.
5. Four-lane layout is consistent.
6. Camber/crown is subtle and realistic.
7. Shoulder modules exist.
8. Verge/edge breakup exists.
9. Medians exist.
10. Drainage exists.
11. Road reflector exists.
12. Rumble strip exists.
13. Road markings align.
14. Modular road pieces join with no seam.
15. UVs are valid.
16. Materials are assigned.
17. Collider exists.
18. No serious topology errors exist.
19. 100 m QA strip looks coherent.
20. Blender previews exist.
21. FBX exports exist.
22. FBX re-import passes.
23. UnityTransfer package exists.
24. Import README exists.
25. Validation has 0 errors.

============================================================
FINAL REPORT
============================================================

Report:

1. discovery findings
2. chosen coordinate system
3. lane width
4. carriageway width
5. shoulder widths
6. camber/crown
7. modules created
8. module dimensions
9. triangle counts
10. materials
11. UV strategy
12. textures created
13. decal sources
14. collision setup
15. snap points
16. Blender checkpoint paths
17. preview paths
18. FBX export paths
19. FBX re-import result
20. UnityTransfer path
21. validation result
22. known limitations
23. recommended next Blender phase

============================================================
IMPORTANT STOP CONDITION
============================================================

After P0-BLENDER-01 ROAD FOUNDATION is complete:

STOP.

DO NOT START:

- vegetation generation
- terrain generation
- props pack
- tunnel
- city
- bridges
- mountain/coastal
- vehicle rebuilding
- traffic rebuilding
- Unity lighting
- Unity shaders
- RoadStreamer integration
- Unity profiling

DO NOT install Unity.

DO NOT create Unity project files.

FINISH THE BLENDER ROAD FOUNDATION,
EXPORT IT,
VALIDATE IT,
PACKAGE IT FOR TRANSFER,
REPORT RESULTS,
AND STOP.
````


====================================================================================================
# SPEC: P1-BLENDER-01 — Core Roadside Props
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist, Hard-Surface Artist,
Procedural Asset Artist and Game Optimization Specialist with 10+ years of
production experience.

You are working on a BLENDER-ONLY production workstation.

This computer DOES NOT contain the Unity project.

Do NOT search for Unity.

Do NOT install Unity.

Do NOT create Unity prefabs, Unity materials, Unity shaders or Unity scripts.

Your job is:

BLENDER ASSET CREATION
→ MODULAR PROPS
→ MATERIAL SOURCE SETUP
→ UVs
→ LODs
→ SIMPLE COLLIDERS
→ VALIDATION
→ FBX EXPORT
→ UNITY TRANSFER PACKAGE
→ STOP

============================================================
CURRENT WORKSPACE
============================================================

Main workspace:

/Users/meetshah/Documents/blender

The previous road phase is COMPLETE:

environment/P0_RoadFoundation/

It contains:

- road_05_export_ready.blend
- 40 m and 20 m road modules
- shoulders
- medians
- drainage
- road reflectors
- rumble strips
- markings
- collision
- FBX exports
- UnityTransfer package

IMPORTANT:

P0_RoadFoundation IS NOW FROZEN.

Do NOT modify:

environment/P0_RoadFoundation/blend/
environment/P0_RoadFoundation/exports/
environment/P0_RoadFoundation/UnityTransfer/

Do not overwrite any P0 files.

If road geometry is needed for scale/alignment:

LINK or APPEND a reference copy from:

environment/P0_RoadFoundation/blend/road_05_export_ready.blend

Do not save changes back into that file.

============================================================
KNOWN ROAD FOUNDATION DIMENSIONS
============================================================

Use these exact values as the environmental reference:

Road module:
40.000 m

Secondary module:
20.000 m

Unity orientation:
+Y up
+Z forward

Blender source:
+Z up
road runs toward -Y

Lane width:
3.60 m

4 lanes:
14.40 m carriageway

Road module width:
15.40 m including edge strips

Outer/right shoulder:
3.00 m

Inner/median-side shoulder:
1.50 m

Drain channel:
0.50 m

Verge:
approximately 1.50 m

Concrete median:
2.00 m

Grass median:
6.00 m

Road crown:
+36 mm

Do not redesign these dimensions in this phase.

============================================================
NEW PHASE
============================================================

P1-BLENDER-01

AAA CORE ROADSIDE PROPS

Create:

/Users/meetshah/Documents/blender/environment/P1_Props/

Use:

P1_Props/
├── blend/
├── exports/
├── textures/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/

============================================================
PRIMARY GOAL
============================================================

Create a high-quality reusable modular roadside-prop library for the racing game.

The assets must support:

- premium PC / console visual quality
- scalable mobile use
- efficient instancing
- modular placement
- 40 m road streaming
- multiple road environments
- future highway, city, bridge and tunnel usage

The props must visually upgrade the road without becoming unnecessarily
high-poly.

============================================================
ART DIRECTION
============================================================

Target:

REALISTIC MODERN HIGHWAY INFRASTRUCTURE

The props should feel:

- engineered
- believable
- premium
- clean but not sterile
- production-ready
- modular
- reusable
- optimized

Avoid:

- exaggerated sci-fi styling
- cartoon proportions
- huge bolts/detail everywhere
- excessive bevel density
- unrealistic scale
- decorative geometry that will not be visible from gameplay camera

============================================================
PRIORITY ORDER
============================================================

Work in this exact order:

1. Guardrail system
2. Crash-protection system
3. Streetlight system
4. Sign gantry system
5. Road signs
6. Delineators / roadside markers
7. Highway infrastructure props
8. Shared road/prop trim sheet
9. LODs
10. Colliders
11. QA assembly
12. Export package

Do NOT start terrain, vegetation, tunnel or city work.

============================================================
PHASE 01 — DISCOVERY
============================================================

Before modeling:

Inspect the finished road foundation.

Link it into the new working file.

Confirm:

- lane layout
- shoulder position
- median location
- drain channel
- verge
- road height
- module endpoints
- coordinate orientation

Also inspect any existing roadside-prop images or old assets in the workspace.

Do not assume Unity assets exist locally.

Create:

reports/P1_props_discovery.md

Document:

- road dimensions
- prop placement assumptions
- chosen standard dimensions
- modular-grid decisions
- art direction
- material strategy

============================================================
PHASE 02 — BLOCKOUT CHECKPOINT
============================================================

Create:

blend/props_01_blockout.blend

Use the linked road kit as reference.

Block out all major asset families before detailing them.

Check scale from:

driver camera height
chase camera distance
roadside position
vehicle scale

Do not detail anything before scale is validated.

============================================================
GUARDRAIL SYSTEM
============================================================

Build a modular galvanized W-beam highway guardrail system.

Create:

Guardrail_WBeam_4m
Guardrail_WBeam_8m

Guardrail_Post

Guardrail_End_Terminal

Guardrail_Transition

Guardrail_Median_Variant

Guardrail_OffsetBlock

Optional:
Guardrail_DoubleRail

============================================================
GUARDRAIL DIMENSIONS
============================================================

Use realistic proportions.

Target approximately:

rail top height:
0.70–0.80 m above local ground

post spacing:
approximately 2.0 m

rail profile:
recognizable W-beam

Do not model corrugation with excessive subdivisions.

Use enough geometry to read correctly from:

5 m
15 m
30 m

Fine galvanization comes from material/normal.

============================================================
GUARDRAIL MODULARITY
============================================================

4 m and 8 m modules must tile exactly.

Guardrail start/end geometry must match.

Create snap empties where useful:

Snap_Start
Snap_End

No visible seam when duplicated.

============================================================
GUARDRAIL POSTS
============================================================

Posts should be separate/reusable where practical.

Do not permanently duplicate thousands of posts into long modules if Unity
instancing can handle them.

However, also provide a convenient preassembled module if useful.

Example:

Guardrail_WBeam_8m_Assembly

with:

rail
posts
offset blocks

Maintain a clean hierarchy.

============================================================
GUARDRAIL MATERIAL
============================================================

Create:

MAT_Prop_GalvanizedSteel

Appearance:

slightly cool galvanized metal
medium roughness
very subtle surface variation
no mirror chrome

Optional weather mask:

small dirt
minor discoloration
edge wear

Do not make highway infrastructure heavily rusted.

============================================================
CRASH PROTECTION SYSTEM
============================================================

Create:

CrashCushion_Main

CrashCushion_Short

Barrier_End_Transition

ImpactAttenuator

Guardrail_To_Concrete_Transition

These should sit naturally at:

median ends
lane separation
barrier transitions
gantry protection zones

============================================================
CRASH CUSHION QUALITY
============================================================

Model major visible forms:

- frame
- rails
- energy-absorbing sections
- front face
- reflective warning panel

Do not model tiny internal mechanical components.

Create a separate warning-panel material slot.

============================================================
STREETLIGHT SYSTEM
============================================================

Create a reusable modern highway lighting family.

Required:

Streetlight_Single

Streetlight_Double

Streetlight_Median_Double

HighMastLight

Streetlight_Fixture

Streetlight_Pole

Optional:

Streetlight_Short_City

Do not create final Unity lights.

These are geometry only.

============================================================
STREETLIGHT SCALE
============================================================

Use realistic modern highway proportions.

Suggested range:

standard pole:
9–12 m

high mast:
18–25 m

arm outreach:
approximately 1.5–3.0 m depending on type

Use road width to determine final proportions.

Avoid poles that visually dominate the highway.

============================================================
STREETLIGHT DETAIL
============================================================

Include:

- tapered pole
- mounting base
- arm
- luminaire housing
- glass/lens
- access panel

Optional:

small bolt detail via normal map rather than modeled bolts.

Fixture should have separate material:

MAT_Prop_LightLens

This will later become emissive in Unity.

============================================================
STREETLIGHT LOD STRATEGY
============================================================

Streetlights are repeated heavily.

Create:

LOD0
LOD1
LOD2
LOD3

LOD0:
close-up / PC

LOD1:
gameplay

LOD2:
distance/mobile

LOD3:
very cheap silhouette

Preserve pole silhouette carefully.

Do not waste polygons on hidden base bolts in lower LODs.

============================================================
SIGN GANTRY SYSTEM
============================================================

Create modern modular overhead highway gantries.

Required:

Gantry_4Lane_Full

Gantry_4Lane_Half

Gantry_Support_Left

Gantry_Support_Right

Gantry_CrossBeam

Gantry_SignFrame

Gantry_VMS_Frame

Optional:

Gantry_Cantilever

============================================================
GANTRY WIDTH
============================================================

The main gantry must properly span the current 4-lane road.

Use:

14.40 m carriageway
plus shoulders / safety offset

Target support positions that do not intrude into driveable lanes.

Validate against the road kit.

============================================================
GANTRY DESIGN
============================================================

Create believable:

- vertical supports
- cross beam
- diagonal structural support if appropriate
- maintenance-frame detail
- sign mounting rails

Do not overbuild lattice geometry.

The silhouette matters more than hundreds of tiny beams.

============================================================
SIGN PANELS
============================================================

Create reusable panels:

SignPanel_Large

SignPanel_Medium

SignPanel_Small

VMS_Panel

ExitPanel

LaneArrowPanel

Panels should be separate from gantry structure.

This allows Unity to swap sign textures.

============================================================
SIGN MATERIALS
============================================================

Create:

MAT_Prop_Sign_Back
MAT_Prop_Sign_Face
MAT_Prop_VMS
MAT_Prop_Reflective

Do NOT permanently bake one road name into every sign.

Use generic preview graphics only.

============================================================
ROAD SIGN LIBRARY
============================================================

Create modular sign supports.

Required signs:

Sign_SpeedLimit

Sign_CurveWarning

Sign_Merge

Sign_LaneEnds

Sign_Exit

Sign_Direction

Sign_NoStopping

Sign_RouteMarker

Sign_WorkZone

Sign_Emergency

Do not make every country's exact legal sign system.

Use a coherent fictional/international-style highway set unless a project
country standard is already established.

============================================================
SIGN POSTS
============================================================

Create reusable:

SignPost_Single

SignPost_Double

SignPost_Square

SignPost_Round

Avoid unique post geometry per sign.

============================================================
DELINEATOR SYSTEM
============================================================

Create:

Delineator_Left

Delineator_Right

Delineator_Double

MedianReflectorPost

EdgeMarker

These should be inexpensive.

Use separate reflective-face material.

Target:

very low poly
strong silhouette
good night readability

============================================================
DELINEATOR LODS
============================================================

At minimum:

LOD0
LOD1
LOD2

LOD2 may be extremely simplified.

============================================================
ROAD SAFETY PROPS
============================================================

Create:

TrafficCone

TrafficCone_WithReflectiveBands

FlexibleBollard

RoadDrum

WarningBeacon

PortableBarrier

These are reusable for:

road works
accidents
events
temporary road sections

Do not produce dozens of variants yet.

============================================================
INFRASTRUCTURE PROPS
============================================================

Create:

CCTV_Pole

CCTV_Camera

UtilityCabinet_Small

UtilityCabinet_Large

EmergencyPhoneBox

SOS_Pillar

RoadsideSensor

WeatherSensor

Optional:

SpeedCamera

============================================================
CCTV / SENSOR DETAIL
============================================================

Keep cameras modular.

Create one base camera unit reusable across:

CCTV pole
gantry mount
tunnel later

Do not make unique camera meshes everywhere.

============================================================
SHARED MATERIAL STRATEGY
============================================================

Avoid one material per object.

Create shared materials:

MAT_Prop_GalvanizedSteel

MAT_Prop_PaintedMetal_Dark

MAT_Prop_PaintedMetal_Light

MAT_Prop_Concrete

MAT_Prop_Plastic_Black

MAT_Prop_Plastic_Orange

MAT_Prop_Reflective

MAT_Prop_Sign_Face

MAT_Prop_LightLens

MAT_Prop_Rubber

Keep material count controlled.

============================================================
SHARED TRIM SHEET
============================================================

Create a shared trim sheet for ROAD + PROPS.

This is important.

Suggested resolution:

2048 × 2048

Name:

T_RoadProps_Trim_2K

Prepare:

BaseColor
Normal
Roughness
Metallic
AO

Potential trim zones:

galvanized rail
painted steel
dark painted steel
concrete edge
reflective strip
rubber/plastic
light fixture metal
sign backing
utility metal
bolt/rivet strip

Do NOT create an overly complicated 4K/8K atlas.

============================================================
TRIM SHEET UV WORKFLOW
============================================================

Use shared trim UVs for repeated structural assets.

Objects suitable for trim usage:

guardrails
gantries
streetlight poles
sign posts
utility cabinets
CCTV poles
barrier transitions

Unique sign graphics may use separate UV space.

============================================================
TEXEL DENSITY
============================================================

Maintain consistent density.

Do not waste texture space on:

undersides
hidden interiors
tiny inaccessible faces

============================================================
REFLECTIVE MATERIAL PREPARATION
============================================================

Reflective surfaces should be separate material slots where Unity may later
apply special nighttime treatment.

Examples:

sign faces
guardrail reflectors
delineator reflectors
cone bands
crash-cushion chevrons

Do NOT simulate final Unity emissive behavior in geometry.

============================================================
LOD TARGETS
============================================================

Use sensible reduction targets.

Large assets:

LOD0:
100%

LOD1:
approximately 50–65%

LOD2:
approximately 20–35%

LOD3:
approximately 5–15%

Small props:

LOD0
LOD1
LOD2

Do not create meaningless LODs where the asset is already under ~100 triangles.

============================================================
SUGGESTED TRIANGLE BUDGETS
============================================================

These are target ranges, not absolute limits.

Guardrail 8 m assembly:
LOD0: 1,000–2,500
LOD1: 500–1,200
LOD2: 150–400

Standard streetlight:
LOD0: 1,000–2,000
LOD1: 400–900
LOD2: 120–300
LOD3: 30–100

High mast:
LOD0: 2,000–4,000
LOD1: 800–1,500
LOD2: 200–500

4-lane gantry:
LOD0: 3,000–6,000
LOD1: 1,500–3,000
LOD2: 500–1,200
LOD3: 150–400

Road sign:
LOD0: 200–600
LOD1: 80–250
LOD2: 20–80

Delineator:
LOD0: under 200
LOD1: under 80
LOD2: under 30

Traffic cone:
LOD0: under 500
LOD1: under 200
LOD2: under 80

Infrastructure prop:
typically 300–2,000 depending on importance.

============================================================
COLLIDERS
============================================================

Create simple collider meshes only where useful.

Examples:

Collision_Guardrail_8m

Collision_CrashCushion

Collision_Streetlight

Collision_Gantry_Left

Collision_Gantry_Right

Collision_UtilityCabinet

Do not create detailed collision matching every bolt/profile.

Use:

boxes
simple convex meshes
capsule-equivalent geometry where appropriate

Streetlight poles can use simple cylindrical/box collision.

============================================================
COLLIDER MATERIAL
============================================================

Do not assign visual materials to collider geometry.

Place colliders in:

PROP_COLLIDERS

Exclude from render/export groups when necessary depending on chosen FBX
strategy.

============================================================
ORIGINS
============================================================

Set meaningful origins.

Guardrails:
start/end snap location or assembly center

Streetlights:
ground contact at pole center

Gantry supports:
ground contact

Gantry assembly:
road/world center reference

Signs:
post base

Cones:
bottom center

Utility:
bottom center

No random origins.

============================================================
TRANSFORMS
============================================================

All production objects:

Scale = 1,1,1

No negative scale.

Apply rotation/scale where safe.

Maintain clean transforms.

============================================================
NAMING STANDARD
============================================================

Examples:

Guardrail_WBeam_8m_LOD0
Guardrail_WBeam_8m_LOD1
Guardrail_WBeam_8m_LOD2

Streetlight_Single_LOD0
Streetlight_Single_LOD1
Streetlight_Single_LOD2
Streetlight_Single_LOD3

Gantry_4Lane_Full_LOD0

Sign_SpeedLimit_LOD0

Delineator_Left_LOD0

Collision_Guardrail_8m

Use consistent suffixes.

============================================================
COLLECTION STRUCTURE
============================================================

Use:

PROPS_MASTER

PROPS_GUARDRAIL

PROPS_CRASH

PROPS_LIGHTING

PROPS_GANTRY

PROPS_SIGNS

PROPS_DELINEATORS

PROPS_SAFETY

PROPS_INFRASTRUCTURE

PROPS_COLLIDERS

PROPS_QA

PROPS_PRESENTATION

============================================================
BLEND CHECKPOINTS
============================================================

Create:

blend/props_01_blockout.blend

blend/props_02_guardrails_safety.blend

blend/props_03_lighting_gantries.blend

blend/props_04_signs_infrastructure.blend

blend/props_05_materials_uv.blend

blend/props_06_lods_colliders.blend

blend/props_07_export_ready.blend

Never overwrite previous checkpoints.

============================================================
QA ROAD ASSEMBLY
============================================================

Create a temporary QA strip using the linked P0 road.

Build approximately:

120–160 m

of road.

Populate it with:

- guardrails
- streetlights
- gantry
- signs
- delineators
- crash cushion
- utility/CCTV assets

Purpose:

judge:

- scale
- repetition
- spacing
- silhouettes
- visual rhythm
- gameplay readability

Do NOT export the QA strip as a runtime asset.

============================================================
PROP SPACING QA
============================================================

Test believable spacing.

Examples:

Streetlights:
approximately 25–45 m depending on road type

Delineators:
approximately 10–25 m

Gantries:
much less frequent

Signs:
context-dependent

Do not permanently bake thousands of props into the road.

These assets are intended for Unity placement/instancing.

============================================================
PREVIEW LIGHTING
============================================================

Use a simple neutral preview environment.

Create:

Day
Golden Hour
Night-like preview

Night preview should show reflective materials but does NOT represent final
Unity lighting.

============================================================
PREVIEW RENDERS
============================================================

Create:

previews/P1_props_full_highway.png

previews/P1_guardrail_closeup.png

previews/P1_guardrail_terminal.png

previews/P1_crash_cushion.png

previews/P1_streetlight_single.png

previews/P1_streetlight_highmast.png

previews/P1_gantry_front.png

previews/P1_gantry_driver_view.png

previews/P1_sign_library.png

previews/P1_delineators.png

previews/P1_infrastructure.png

previews/P1_props_night_preview.png

previews/P1_120m_test.png

============================================================
DRIVER CAMERA TEST
============================================================

Create QA camera at a realistic driving viewpoint.

Also test from chase camera height.

Assets must look correct from gameplay distance.

Do not optimize solely for close-up renders.

============================================================
PER-ASSET VALIDATION
============================================================

Check:

- correct names
- clean topology
- no accidental duplicate faces
- no extreme ngons causing shading issues
- normals
- UVs
- material slots
- transforms
- origins
- LOD hierarchy
- colliders
- dimensions

============================================================
SCRIPT ORGANIZATION
============================================================

Store automation scripts under:

scripts/

Suggested:

props_build.py
props_materials.py
props_lods.py
props_validate.py
props_render.py
props_export.py

Do not store random scripts in workspace root.

============================================================
EXPORT ORIENTATION
============================================================

Use the same proven Blender → Unity orientation strategy as the Hypercar and
P0 Road Foundation.

Target Unity:

+Y up
+Z forward

Do not blindly enable Blender Apply Transform if that causes axis errors.

Reuse the proven export method.

============================================================
EXPORT FORMAT
============================================================

Primary:

FBX

Do not use GLB as the primary runtime format.

============================================================
EXPORT FILES
============================================================

Create:

exports/roadside_props_complete.fbx

Also create logical split FBXs:

exports/Guardrails.fbx

exports/RoadSafety.fbx

exports/Streetlights.fbx

exports/Gantries.fbx

exports/RoadSigns.fbx

exports/Delineators.fbx

exports/Infrastructure.fbx

Use whichever grouping gives clean Unity workflow.

============================================================
EXPORT CONTENT
============================================================

Include only production assets.

Exclude:

- QA road strip
- linked P0 road reference
- Hypercar reference if used
- cameras
- lights
- presentation world
- temporary cutters
- construction helpers

============================================================
TEXTURES
============================================================

Export/copy final source textures under:

textures/

Recommended:

textures/trim/
textures/signs/
textures/decals/
textures/utility/

Do not duplicate P0 road textures unless necessary.

If using the new shared RoadProps trim sheet:

include all trim maps.

============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

After exports:

create an empty Blender scene.

Re-import every FBX.

Validate:

- orientation
- dimensions
- object names
- transforms
- UVs
- normals
- material slots
- LOD objects
- collider locations
- origin behavior where preserved
- hierarchy

Output:

reports/P1_props_reimport_validation.txt

Target:

0 errors.

============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P1_props_geometry.json

For every asset include:

- asset name
- LOD
- triangles
- vertices
- dimensions
- materials
- UV status
- collider status

============================================================
VALIDATION REPORT
============================================================

Create:

reports/P1_props_validation.txt

Check:

- all required asset families
- naming
- transforms
- UVs
- normals
- topology
- LOD chain
- materials
- trim usage
- colliders
- export selection
- FBX re-import

Target:

0 errors
0 critical warnings

============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P1_props_export_manifest.json

Include:

- source blend
- FBX files
- included objects
- excluded objects
- texture files
- coordinate system
- LOD groups
- material slots
- collider list

============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

UnityTransfer/

Structure:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/

Copy only final production deliverables.

Do NOT include QA scene or all Blender checkpoints.

============================================================
UNITY IMPORT README
============================================================

Create:

UnityTransfer/README/PROPS_IMPORT_NOTES.md

Document:

1. Unity axis/orientation
2. scale
3. each FBX file
4. LOD hierarchy
5. material names
6. trim-sheet textures
7. reflective material slots
8. collider meshes
9. intended instancing strategy
10. streetlight emissive slots
11. sign-face material strategy
12. gantry setup
13. guardrail modularity
14. expected 40 m road-grid usage
15. excluded QA assets

State clearly:

THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.

UNITY PREFABS, UNITY LIGHTS, UNITY MATERIALS, LODGROUP COMPONENTS,
REFLECTION SETTINGS AND PERFORMANCE TESTING MUST BE COMPLETED ON THE
UNITY WORKSTATION.

============================================================
TRIM SHEET README
============================================================

Create:

UnityTransfer/README/ROAD_PROPS_TRIM_GUIDE.md

Include:

- trim map dimensions
- material channels
- UV strip locations
- asset families using each strip
- expected Unity metallic/roughness handling
- normal-map orientation

============================================================
P0 ROAD PROTECTION CHECK
============================================================

At completion verify:

P0 road files remain unchanged.

Create:

reports/P1_P0_road_integrity_check.md

State:

- linked source path
- whether any P0 file timestamp/content was changed
- confirmation that no P0 source file was overwritten

============================================================
P1 COMPLETION GATE
============================================================

Do NOT declare complete until:

1. P0 Road Foundation remains unchanged.
2. Guardrail system exists.
3. Guardrail terminal exists.
4. Barrier transition exists.
5. Crash cushion exists.
6. Streetlight single exists.
7. Streetlight double exists.
8. High mast exists.
9. 4-lane gantry exists.
10. Gantry sign panels exist.
11. VMS panel exists.
12. Road-sign library exists.
13. Sign posts exist.
14. Delineator system exists.
15. Traffic cone exists.
16. Bollard exists.
17. CCTV exists.
18. Utility cabinet exists.
19. Emergency/SOS prop exists.
20. Shared RoadProps trim sheet exists.
21. UVs are valid.
22. Materials are shared efficiently.
23. Major repeated props have useful LODs.
24. Required colliders exist.
25. QA highway strip looks coherent.
26. Preview renders exist.
27. FBX exports exist.
28. FBX re-import passes.
29. Validation has 0 errors.
30. UnityTransfer package exists.
31. Props import README exists.
32. Trim guide exists.
33. P0 integrity check passes.

============================================================
FINAL REPORT
============================================================

Return one complete report containing:

1. Discovery findings
2. P0 road integrity status
3. Assets created
4. Guardrail variants
5. Crash-protection assets
6. Streetlight variants
7. Gantry variants
8. Sign library
9. Delineators
10. Safety props
11. Infrastructure props
12. Material list
13. Trim-sheet specification
14. UV strategy
15. LOD strategy
16. triangle counts
17. collider setup
18. object origins
19. coordinate system
20. QA-strip result
21. preview paths
22. Blender checkpoint paths
23. FBX export paths
24. FBX re-import results
25. validation results
26. UnityTransfer path
27. import README path
28. known limitations
29. recommended next Blender phase

============================================================
IMPORTANT STOP CONDITION
============================================================

AFTER P1-BLENDER-01 CORE ROADSIDE PROPS IS COMPLETE:

STOP.

DO NOT START:

- Terrain
- Vegetation
- Tunnel
- City
- Bridge rebuild
- Player car rebuilds
- Traffic rebuild
- Mountain/coastal kit
- Unity integration
- Unity lighting
- RoadStreamer changes
- Unity performance testing

DO NOT modify P0 Road Foundation.

DO NOT modify finished car assets.

DO NOT install or launch Unity.

FINISH THE COMPLETE ROADSIDE PROP KIT,
CREATE LODS,
CREATE THE SHARED TRIM SHEET,
EXPORT,
RE-IMPORT VALIDATE,
PACKAGE FOR UNITY,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P1-BLENDER-02 — Terrain & Roadside Transition Kit
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Procedural Terrain Artist, World-Building Artist and Game Optimization
Specialist with 10+ years of production experience.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

Do NOT:

- search for Unity
- install Unity
- create Unity prefabs
- create Unity materials
- create Unity shaders
- create Unity scripts
- modify gameplay
- modify RoadStreamer

Your responsibility is:

P1-BLENDER-02 — AAA TERRAIN & ROADSIDE TRANSITION KIT

Complete:

DISCOVERY
→ REFERENCE LINKING
→ TERRAIN BLOCKOUT
→ MODULAR TERRAIN STRIPS
→ CUT/FILL EMBANKMENTS
→ DITCHES
→ RETAINING STRUCTURES
→ ROCK/CLIFF KIT
→ DISTANT TERRAIN/VISTAS
→ UV/MATERIAL SOURCE SETUP
→ LODS
→ COLLISION WHERE APPROPRIATE
→ QA ASSEMBLY
→ PREVIEWS
→ FBX EXPORT
→ RE-IMPORT VALIDATION
→ UNITY TRANSFER PACKAGE
→ FINAL REPORT
→ STOP

============================================================
CURRENT WORKSPACE
============================================================

Main workspace:

/Users/meetshah/Documents/blender

Completed and FROZEN:

environment/P0_RoadFoundation/

environment/P1_Props/

Existing car folders are also frozen.

DO NOT MODIFY ANY FILE INSIDE:

environment/P0_RoadFoundation/

environment/P1_Props/

new_car/

or other completed vehicle directories.

============================================================
REFERENCE POLICY
============================================================

The terrain phase may LINK or APPEND read-only reference copies from:

environment/P0_RoadFoundation/blend/road_05_export_ready.blend

and:

environment/P1_Props/blend/props_07_export_ready.blend

Use them only for:

- scale
- alignment
- roadside clearances
- terrain transition
- guardrail position
- streetlight clearance
- gantry clearance
- sign placement clearance

Do NOT save changes back into either source file.

============================================================
KNOWN ROAD FOUNDATION
============================================================

Use these dimensions as fixed production truth:

Road module:
40.000 m

Secondary road module:
20.000 m

Unity:
+Y up
+Z forward

Blender:
+Z up
road direction -Y

Vehicle physical LEFT:
+X

Vehicle physical RIGHT:
-X

Lane width:
3.60 m

Four-lane carriageway:
14.40 m

Road module including edge strips:
15.40 m

Outer/right paved shoulder:
3.00 m

Inner/median-side shoulder:
1.50 m

Drain:
0.50 m

Existing verge:
approximately 1.50 m

Road crown:
+36 mm

Roadside general terrain level:

approximately -0.30 m

relative to gameplay road level.

This -0.30 m value is the preferred base surrounding-ground level.

Measure the linked P0 road before assuming exact transition points.

============================================================
KNOWN P1 PROP PLACEMENTS
============================================================

The completed Props phase established important clearances.

Examples include:

right-side guardrail post line:
approximately X = -11.0 m

right-side streetlight line:
approximately X = -12.0 m

gantry supports:
verge / median zones

median lighting:
barrier-top placement

Do not build terrain through these assets.

The final terrain corridor must leave reasonable placement space for:

- guardrails
- streetlights
- signs
- gantries
- CCTV
- utility equipment
- future vegetation

============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P1_Terrain/

Use:

P1_Terrain/
├── blend/
├── exports/
├── textures/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/

============================================================
PRIMARY GOAL
============================================================

The current game should stop looking like:

ROAD
+
FLAT GREEN PLANE

The terrain system should make the highway feel embedded naturally into
a believable world.

Target:

AAA MODERN HIGHWAY ENVIRONMENT TERRAIN

while preserving:

- straight 40 m streaming
- mobile scalability
- deterministic snapping
- efficient geometry
- reusable modules
- clean road visibility
- future vegetation placement

============================================================
CRITICAL GAMEPLAY RULE
============================================================

DO NOT CREATE ACTUAL ROAD HILLS OR ROAD CURVES.

The road itself remains:

straight
level
40 m modular

Terrain may:

rise beside the road
fall beside the road
form embankments
form cuts
form hills in the distance
form cliffs
create visual elevation

But the ROAD SURFACE must not change its established gameplay elevation.

This phase is ENVIRONMENT elevation, not ROAD elevation.

============================================================
TERRAIN DESIGN PHILOSOPHY
============================================================

Think like real highway civil engineering.

The road should pass through combinations of:

FLAT GROUND

CUT SECTION
road lower than surrounding terrain

FILL SECTION
road raised above surrounding terrain

SHALLOW EMBANKMENT

DEEP EMBANKMENT

DRAINAGE DITCH

ROCK CUT

RETAINING WALL

OPEN FIELD

DISTANT HILLS

All while the actual drivable road remains straight.

============================================================
MODULAR SEAM RULE
============================================================

This is extremely important.

Terrain modules must be compatible with the 40 m RoadStreamer system.

Every 40 m terrain module must have deterministic end boundaries.

At:

z = 0

and

z = 40 m

the terrain boundary geometry must be compatible with adjacent modules.

Use a SEAM SAFE ZONE near both ends.

Suggested:

first 1–2 m
last 1–2 m

should return toward a standardized boundary profile.

This allows different variants to be sequenced without obvious gaps.

Do not make random terrain peaks directly at chunk boundaries.

============================================================
PHASE 01 — DISCOVERY
============================================================

Link P0 road and P1 props read-only.

Measure:

- road edge
- shoulder
- drain
- verge
- roadside base elevation
- guardrail line
- streetlight line
- gantry supports
- prop clearance

Create:

reports/P1_terrain_discovery.md

Document:

- exact transition positions
- selected terrain width
- base ground height
- seam policy
- material strategy
- module strategy
- LOD strategy

============================================================
PHASE 02 — TERRAIN CORRIDOR WIDTH
============================================================

Create enough terrain on each side that normal chase-camera views do not
see the world ending.

Recommended near-terrain width:

approximately 25–40 m OUTSIDE the road corridor on EACH side.

Choose actual width from camera QA.

Do not build an enormous kilometre-wide mesh into every chunk.

Near terrain should be modular.

Far landscape should use separate vista meshes.

============================================================
BASE TERRAIN MODULES
============================================================

Create at minimum:

Terrain_Flat_L_40m
Terrain_Flat_R_40m

Terrain_Flat_L_20m
Terrain_Flat_R_20m

Suffix convention:

_L = physical left = Blender +X

_R = physical right = Blender -X

============================================================
FLAT TERRAIN
============================================================

Flat does NOT mean mathematically perfect plane.

Use:

- subtle broad elevation variation
- slight roadside drainage
- gentle undulation away from road

Roadside interface must remain deterministic.

Do not introduce visible bumps at chunk seams.

============================================================
ROAD-TO-TERRAIN TRANSITION
============================================================

Build the transition from existing verge to natural terrain.

Create:

TerrainTransition_L_40m
TerrainTransition_R_40m

The road should look physically embedded into surrounding ground.

Avoid:

vertical gap
floating asphalt
perfect straight green edge
terrain clipping through drain
terrain clipping through guardrail

============================================================
CUT TERRAIN MODULES
============================================================

Create:

Terrain_Cut_L_40m
Terrain_Cut_R_40m

Terrain_Cut_Both_40m

Optional 20 m transition modules if useful.

A cut section means surrounding terrain rises beside the road.

Use believable slopes.

Do not place the steep face immediately against traffic.

Provide:

- drainage zone
- shoulder clearance
- safety clearance
- slope toe

============================================================
CUT HEIGHT VARIANTS
============================================================

Create at least:

Cut_Low

Cut_Medium

Potential approximate elevation ranges:

Low:
+1.5 to +3 m above road

Medium:
+4 to +7 m

Do not create giant mountains directly next to the road in this phase.

============================================================
FILL / EMBANKMENT MODULES
============================================================

Create:

Terrain_Fill_L_40m
Terrain_Fill_R_40m

Terrain_Fill_Both_40m

A fill section means the highway appears elevated above surrounding land.

Road itself remains at gameplay elevation.

Instead, terrain falls away from the road.

Provide realistic:

- shoulder
- embankment crest
- slope
- toe
- drainage area

============================================================
FILL DEPTH
============================================================

Create reasonable variants.

Example:

Shallow:
terrain falls approximately 1–2.5 m

Medium:
approximately 3–5 m

Avoid extreme cliffs unless using a dedicated structure.

============================================================
EMBANKMENT SLOPES
============================================================

Use realistic-looking slope ratios.

Avoid near-vertical grass walls.

Typical visual target could be roughly:

1 vertical : 2–3 horizontal

depending on variant.

Exact engineering certification is not required.

Believable proportions are.

============================================================
DITCH SYSTEM
============================================================

Create modular roadside drainage terrain.

Required:

Terrain_Ditch_Shallow_4m

Terrain_Ditch_Deep_4m

Terrain_Ditch_L_40m

Terrain_Ditch_R_40m

Optional:

Culvert_Inlet

Culvert_Outlet

The ditch should integrate with P0 Drain_Channel geometry.

Do not duplicate P0 drain assets unnecessarily.

============================================================
CULVERTS
============================================================

If created, make culvert mouths simple and reusable.

Create:

Culvert_Concrete_Round

or

Culvert_Box

Use low-cost geometry.

Do not model long underground pipe networks.

============================================================
RETAINING WALL SYSTEM
============================================================

Create terrain-support structures:

RetainingWall_4m

RetainingWall_8m

RetainingWall_20m

RetainingWall_End

RetainingWall_CornerVisual

Optional:

RetainingWall_Tiered

Use believable concrete highway construction.

============================================================
RETAINING WALL DETAIL
============================================================

Include only important geometry:

- wall profile
- top cap
- panel joints
- drainage openings if useful

Fine details should use:

normal/trim texture

Do not model every tie hole/bolt.

============================================================
RETAINING WALL MATERIAL
============================================================

Create:

MAT_Terrain_Concrete

Prefer compatibility with existing P0/P1 concrete visual language.

Do not create a completely different concrete style unless justified.

============================================================
ROCK CUT KIT
============================================================

Create modular rock/cliff meshes.

Required:

RockCut_A
RockCut_B
RockCut_C

Cliff_Module_A
Cliff_Module_B
Cliff_Module_C

These should be usable against cut terrain.

Target:

natural stratified road-cut rock

not fantasy mountains.

============================================================
ROCK DESIGN
============================================================

Use:

large readable planes
major fractures
layering
erosion variation

Avoid:

millions of tiny sculpted details

Fine detail should come from normals/material.

============================================================
ROCK LODs
============================================================

Create useful LODs.

Example:

LOD0:
100%

LOD1:
~50%

LOD2:
~20%

LOD3:
~5–10% or billboard/impostor-ready silhouette if useful

Preserve silhouette.

============================================================
SMALL ROCK SET
============================================================

Create approximately:

Rock_A
Rock_B
Rock_C
Rock_D
Rock_E
Rock_F

Optional:

RockCluster_A
RockCluster_B

These are for future terrain dressing.

Do NOT scatter thousands of them now.

============================================================
DISTANT LANDSCAPE / VISTA KIT
============================================================

Create separate very-low-cost distant meshes.

Required:

Vista_Hills_A

Vista_Hills_B

Vista_Hills_C

Optional:

Vista_Ridge_A

Vista_DistantMountain_A

These should sit hundreds of metres to kilometres away in Unity.

Do not attach them permanently to every road module.

============================================================
VISTA DESIGN
============================================================

Use very low-frequency forms.

No small geometry.

The purpose is:

- horizon silhouette
- depth
- preventing empty world
- atmospheric layering

Not close-up terrain.

============================================================
TERRAIN MATERIAL STRATEGY
============================================================

Create shared Blender source materials:

MAT_Terrain_Grass

MAT_Terrain_Soil

MAT_Terrain_Rock

MAT_Terrain_Gravel

MAT_Terrain_Concrete

MAT_Terrain_DryGrass

These are preview/source materials.

Final Unity terrain shading happens later.

============================================================
VERTEX BLEND DATA
============================================================

Prepare terrain meshes for efficient Unity material blending.

Create a vertex colour layer named:

TerrainBlend

Use channels consistently.

Recommended:

R = grass influence

G = soil influence

B = rock influence

A = secondary/wet/dry mask or reserved

Document exact convention.

Do NOT invent different channel meanings per asset.

============================================================
SLOPE-BASED MATERIAL LOGIC
============================================================

In Blender preview:

steep areas should visually favour:

rock / exposed soil

flat/gentle areas:

grass / dirt

Road-edge transition:

gravel / dirt as appropriate

But bake/store useful vertex information rather than relying solely on a
Blender-only procedural material.

============================================================
TEXTURES
============================================================

Prepare reusable tileable source textures.

Recommended:

Terrain_Grass_2K

Terrain_Soil_2K

Terrain_Rock_2K

Terrain_Gravel_2K

For each where appropriate:

BaseColor
Normal
Roughness
AO

Do not create unnecessary 8K textures.

2K tileables are preferable for mobile scalability.

============================================================
MATERIAL SCALE
============================================================

Use realistic world-scale tiling.

Avoid obviously giant grass blades or microscopic rock texture.

Document metres-per-tile for each source.

============================================================
UV STRATEGY
============================================================

Near terrain:

use UVs compatible with repeatable materials.

Do NOT stretch a 0–1 texture across a 40 m × 40 m terrain piece.

Maintain consistent texel density.

Cliffs/rocks may use:

triplanar-friendly layout

or

traditional UVs

depending on future Unity strategy.

Document choice.

============================================================
NO VEGETATION
============================================================

Do NOT create:

trees
bushes
grass cards
flowers
hedges

That is P1-BLENDER-03.

You may place simple dummy markers/empties for future vegetation zones if
useful.

Do not export actual vegetation.

============================================================
VEGETATION PLACEMENT MASK
============================================================

Prepare terrain data so vegetation can later be placed intelligently.

Create a vertex group or colour/mask convention such as:

VegetationAllowed

or use an additional vertex colour layer:

VegetationMask

Exclude:

- road
- shoulder
- drain
- guardrail corridor
- streetlight bases
- gantry supports
- steep rock faces
- retaining walls

This will help the next vegetation phase.

============================================================
PROP CLEARANCE MASK
============================================================

Do not let terrain intersect P1 props.

During QA, place reference:

guardrails
streetlights
gantry
signs
CCTV

Check:

- bases sit correctly
- no terrain penetrates fixtures
- no slopes block roadway sightlines

============================================================
GEOMETRY QUALITY
============================================================

Use geometry for:

- broad terrain shape
- silhouette
- slope changes
- ditch profile
- cliff forms
- retaining-wall profile

Use materials/normals for:

- soil grains
- grass
- tiny stones
- fine cracks
- fine rock texture

Do not subdivide terrain uniformly at excessive density.

============================================================
TERRAIN GRID
============================================================

Use controlled topology.

Near roadside:
more density

far edge:
less density

Avoid hundreds of thousands of triangles per 40 m module.

============================================================
TRIANGLE TARGETS
============================================================

Use these as guidance, not quotas.

Per side 40 m near-terrain module:

LOD0:
approximately 2k–6k tris

LOD1:
~1k–3k

LOD2:
~300–1k

LOD3:
~100–300 if useful

Cut/cliff modules may be somewhat higher.

Distant vistas:

prefer hundreds to a few thousand triangles TOTAL.

Do not pad geometry to meet minimums.

Lower is good if silhouette and shading remain correct.

============================================================
LOD STRATEGY
============================================================

Create LODs for:

terrain strips where worthwhile
rock cuts
cliffs
rocks
retaining-wall detail if useful
vista meshes if necessary

Do not make pointless LODs for already tiny meshes.

============================================================
TERRAIN COLLISION
============================================================

Gameplay road collision already comes from P0.

Terrain collision should be simple.

Create collision only where needed.

Possible:

Collision_Terrain_Flat_L_40m

Collision_Terrain_Flat_R_40m

Collision_RetainingWall

Collision_RockCut

Keep terrain collider substantially simpler than visual mesh.

If gameplay never allows cars off road, do not overbuild terrain collision.

============================================================
MODULAR SNAP POINTS
============================================================

Create:

Snap_Start
Snap_End

for 40 m modules.

Distance:

40.000 m

For 20 m:

20.000 m

Also create roadside alignment empties if useful:

RoadEdge_Ref

TerrainOuter_Ref

Do not export unnecessary debug empties unless documented.

============================================================
SEAM TEST
============================================================

MANDATORY.

Build:

Flat
+
Cut
+
Flat
+
Fill

using four 40 m modules.

Check every 40 m boundary.

No:

visible cracks
vertical walls
z-fighting
holes
material discontinuities
hard impossible slope jumps

============================================================
RANDOM SEQUENCE TEST
============================================================

Create at least one 200–240 m sequence using different terrain types.

Example:

Flat
→ Shallow Cut
→ Cut
→ Flat
→ Shallow Fill
→ Fill

This is Blender QA only.

Do not export the assembled strip as the primary runtime asset.

============================================================
ROAD + PROP QA ASSEMBLY
============================================================

Build approximately:

160–240 m

using LINKED:

P0 road
P1 props

and new terrain.

Include:

road
guardrails
streetlights
gantry
signs
drain
terrain
retaining wall
rock cut
distant hills

No vegetation yet.

============================================================
QA CAMERA
============================================================

Test from:

driver view

low chase view

higher chase view

side cinematic view

The terrain must look good from actual gameplay distance.

============================================================
HORIZON QA
============================================================

From chase camera:

there should be no obvious:

flat world edge
empty void
straight terrain termination

Use vista meshes where necessary.

============================================================
MOBILE QA PRINCIPLE
============================================================

The mobile version should be able to:

- use lower terrain LOD
- reduce rock count
- remove tiny props
- use simpler terrain material
- use lower-detail vistas

Do not create terrain that requires displacement/tessellation.

============================================================
CHECKPOINT FILES
============================================================

Create:

blend/terrain_01_blockout.blend

blend/terrain_02_flat_transition.blend

blend/terrain_03_cut_fill.blend

blend/terrain_04_retaining_rocks.blend

blend/terrain_05_materials_uv.blend

blend/terrain_06_lods_collision.blend

blend/terrain_07_export_ready.blend

Never overwrite earlier checkpoints.

============================================================
COLLECTIONS
============================================================

Use:

TERRAIN_MASTER

TERRAIN_FLAT

TERRAIN_TRANSITION

TERRAIN_CUT

TERRAIN_FILL

TERRAIN_DITCH

TERRAIN_RETAINING

TERRAIN_ROCKS

TERRAIN_VISTAS

TERRAIN_COLLIDERS

TERRAIN_QA

TERRAIN_PRESENTATION

============================================================
NAMING
============================================================

Examples:

Terrain_Flat_L_40m_LOD0

Terrain_Flat_R_40m_LOD0

Terrain_Cut_Low_L_40m_LOD0

Terrain_Cut_Medium_R_40m_LOD0

Terrain_Fill_Shallow_L_40m_LOD0

Terrain_Ditch_R_40m_LOD0

RetainingWall_8m_LOD0

RockCut_A_LOD0

Vista_Hills_A_LOD0

Collision_Terrain_Flat_L_40m

Use consistent suffixes.

============================================================
ORIGINS
============================================================

Terrain modules:

use consistent road-relative origin.

Prefer start-centre or known road-grid origin.

Whichever is selected:

apply consistently.

Retaining walls:

bottom/start snap origin.

Rocks:

bottom centre.

Vistas:

ground centre.

============================================================
TRANSFORMS
============================================================

Production objects:

Scale 1,1,1

No negative scale.

Apply transforms where safe.

No unexplained rotations.

============================================================
NORMALS
============================================================

Terrain shading must remain clean.

Avoid:

faceted terrain where smooth ground is expected

and

over-smoothed sharp rock edges.

Use appropriate smoothing/custom normals.

============================================================
PREVIEW LIGHTING
============================================================

Use simple Blender preview environments:

Day

Golden Hour

Overcast

Do not attempt to reproduce final Unity P0 lighting exactly.

Purpose:

asset readability.

============================================================
PREVIEW RENDERS
============================================================

Create at minimum:

previews/P1_terrain_flat.png

previews/P1_terrain_transition.png

previews/P1_terrain_cut_low.png

previews/P1_terrain_cut_medium.png

previews/P1_terrain_fill.png

previews/P1_terrain_ditch.png

previews/P1_retaining_wall.png

previews/P1_rock_cut.png

previews/P1_rock_library.png

previews/P1_vista_hills.png

previews/P1_terrain_driver_view.png

previews/P1_terrain_chase_view.png

previews/P1_200m_sequence.png

previews/P1_terrain_with_props.png

============================================================
AUTOMATION
============================================================

Store Blender Python in:

scripts/

Suggested:

terrain_build.py

terrain_materials.py

terrain_lods.py

terrain_validate.py

terrain_render.py

terrain_export.py

Do not put generated scripts in workspace root.

============================================================
EXPORT ORIENTATION
============================================================

Use the same proven Blender → Unity export strategy used by:

Hypercar

P0 Road Foundation

P1 Props

Target Unity:

+Y up
+Z forward

Use the established axis conversion.

Do not blindly turn on Blender Apply Transform if prior validation showed it
causes double conversion.

============================================================
FBX EXPORT
============================================================

Primary format:

FBX

Create:

exports/terrain_complete.fbx

Also logical split files:

exports/Terrain_Flat.fbx

exports/Terrain_Cut.fbx

exports/Terrain_Fill.fbx

exports/Terrain_Drainage.fbx

exports/Terrain_Retaining.fbx

exports/Terrain_Rocks.fbx

exports/Terrain_Vistas.fbx

Actual grouping may be adjusted if cleaner.

============================================================
EXPORT CONTENT
============================================================

Include production assets only.

Exclude:

- linked P0 road
- linked P1 props
- cars
- QA assembled strip
- cameras
- Blender lights
- dummy vegetation
- presentation world
- temporary helpers

============================================================
TEXTURE EXPORT
============================================================

Copy final textures to:

textures/

Suggested:

textures/grass/

textures/soil/

textures/rock/

textures/gravel/

textures/masks/

Do not duplicate existing P0/P1 textures without reason.

============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

After exporting:

create a clean empty Blender scene.

Re-import EVERY FBX.

Validate:

- +Y Unity up conversion
- +Z Unity forward
- dimensions
- module length
- snap spacing
- hierarchy
- names
- scale
- UVs
- vertex colours
- VegetationMask
- materials
- LOD objects
- collider placement
- triangle counts

Target:

0 errors.

============================================================
VALIDATION SCRIPT
============================================================

Create:

reports/P1_terrain_validation.txt

Check:

1. required modules exist
2. naming
3. 40 m lengths
4. 20 m lengths
5. snap spacing
6. terrain ground level
7. road transition
8. P0/P1 source integrity
9. transforms
10. normals
11. UVs
12. TerrainBlend
13. VegetationMask
14. materials
15. LODs
16. colliders
17. non-manifold errors
18. zero-area geometry
19. export selection
20. re-import validation

Target:

0 errors

0 critical warnings.

Do not treat an asset being below triangle budget as a warning.

============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P1_terrain_geometry.json

For each asset:

- name
- type
- LOD
- triangles
- vertices
- dimensions
- materials
- UV status
- TerrainBlend status
- VegetationMask status
- collider status

============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P1_terrain_export_manifest.json

Include:

- FBX files
- source blend
- object list
- excluded objects
- texture files
- material names
- axis conversion
- snap convention
- vertex-data convention
- LODs
- colliders

============================================================
P0 / P1 PROPS INTEGRITY
============================================================

Before finishing, verify:

P0 Road Foundation remains byte-for-byte unchanged.

P1 Props remains byte-for-byte unchanged.

Create:

reports/P1_terrain_source_integrity_check.md

Include:

P0 file count/hash comparison

P1 Props file count/hash comparison

Car source integrity

Target:

NO SOURCE MODIFICATIONS.

============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

UnityTransfer/

with:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/

Copy final production deliverables only.

============================================================
UNITY IMPORT README
============================================================

Create:

UnityTransfer/README/TERRAIN_IMPORT_NOTES.md

Document:

1. source phase
2. Unity orientation
3. scale
4. module lengths
5. terrain width
6. road-edge transition
7. ground level
8. terrain types
9. FBX files
10. LOD naming
11. materials
12. texture channels
13. TerrainBlend vertex channels
14. VegetationMask convention
15. colliders
16. snap points
17. expected instancing
18. expected RoadStreamer relationship
19. vista usage
20. excluded QA content

State clearly:

THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.

UNITY TERRAIN MATERIALS, PREFABS, ROADSTREAMER PLACEMENT, VEGETATION
SYSTEMS, CULLING, HLOD, FOG AND PERFORMANCE TESTING MUST BE COMPLETED
ON THE UNITY WORKSTATION.

============================================================
TERRAIN BLEND README
============================================================

Create:

UnityTransfer/README/TERRAIN_BLEND_GUIDE.md

Document exactly:

TerrainBlend R meaning

TerrainBlend G meaning

TerrainBlend B meaning

TerrainBlend A meaning

VegetationMask meaning

texture scale

material recommendations

Unity shader expectations

============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P1-BLENDER-02 COMPLETE UNTIL:

1. P0 Road Foundation is unchanged.
2. P1 Props is unchanged.
3. Car assets are unchanged.
4. Flat L/R 40 m terrain exists.
5. Flat L/R 20 m terrain exists.
6. Road-transition modules exist.
7. Cut terrain exists.
8. Fill terrain exists.
9. Ditch terrain exists.
10. Retaining-wall system exists.
11. Rock-cut system exists.
12. Small rock library exists.
13. Vista hills exist.
14. Terrain seam-safe boundaries are implemented.
15. Random multi-module sequence joins correctly.
16. Road/terrain transition looks natural.
17. Props do not intersect terrain incorrectly.
18. TerrainBlend data exists.
19. VegetationMask data exists.
20. UVs are valid.
21. Shared materials exist.
22. Tileable terrain textures exist.
23. Useful LODs exist.
24. Required simple colliders exist.
25. QA road+props+terrain scene looks coherent.
26. Driver-view preview passes.
27. Chase-view preview passes.
28. Horizon has no obvious world edge.
29. Required preview renders exist.
30. FBX exports exist.
31. Every FBX re-import passes.
32. Validation has 0 errors.
33. Geometry report exists.
34. Export manifest exists.
35. UnityTransfer exists.
36. TERRAIN_IMPORT_NOTES exists.
37. TERRAIN_BLEND_GUIDE exists.
38. Source-integrity check passes.

============================================================
FINAL REPORT
============================================================

Return ONE complete report containing:

1. Discovery findings
2. P0 integrity
3. P1 Props integrity
4. chosen terrain corridor width
5. base terrain elevation
6. seam-safe strategy
7. flat modules
8. transition modules
9. cut modules
10. fill modules
11. ditch modules
12. retaining-wall assets
13. rock-cut assets
14. rock library
15. vista assets
16. material list
17. texture list
18. UV strategy
19. TerrainBlend convention
20. VegetationMask convention
21. LOD strategy
22. triangle counts
23. collision strategy
24. snap points
25. random sequence QA
26. driver-view QA
27. chase-view QA
28. road+props+terrain QA
29. checkpoint paths
30. preview paths
31. FBX paths
32. FBX re-import result
33. validation result
34. UnityTransfer path
35. import-notes path
36. known limitations
37. recommended next Blender phase

============================================================
STOP CONDITION
============================================================

After P1-BLENDER-02 TERRAIN is complete:

STOP.

DO NOT START:

- vegetation
- tunnel
- city
- bridge remaster
- player-car rebuilding
- traffic rebuilding
- mountain/coastal kit
- Unity integration
- Unity terrain shaders
- RoadStreamer modification

Do NOT modify:

P0 Road Foundation

P1 Props

finished car assets

Do NOT launch/install Unity.

FINISH THE COMPLETE TERRAIN SYSTEM,
VALIDATE,
EXPORT,
RE-IMPORT,
PACKAGE FOR UNITY,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P1-BLENDER-02A — Terrain Visual Polish & Final Freeze
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Procedural Terrain Artist, Natural Environment Artist and Game Optimization
Specialist with 10+ years of production experience.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

This is NOT a new terrain-generation phase.

The main terrain system:

P1-BLENDER-02

is already technically complete and validated.

Your task is a SHORT, TARGETED VISUAL POLISH PHASE:

P1-BLENDER-02A — TERRAIN VISUAL POLISH & FINAL FREEZE

The goal is to correct ONLY the known visual weaknesses before the terrain
becomes a frozen dependency for vegetation.

Do not redesign the terrain architecture.

Do not generate vegetation.

Do not change gameplay-road geometry.

Do not expand scope.

Complete:

BASELINE
→ VISUAL REVIEW
→ ROCK-CUT POLISH
→ ROAD-EDGE TRANSITION POLISH
→ FLAT-TERRAIN VARIATION POLISH
→ QA
→ VALIDATION
→ EXPORT UPDATE
→ TRANSFER PACKAGE UPDATE
→ FINAL FREEZE
→ STOP

============================================================
CURRENT WORKSPACE
============================================================

Main workspace:

/Users/meetshah/Documents/blender

Completed:

environment/P0_RoadFoundation/
environment/P1_Props/
environment/P1_Terrain/

Finished vehicle folders also exist.

P0 Road Foundation and P1 Props are FROZEN.

Do not modify them.

Cars are FROZEN.

The only phase that may be modified in this task is:

environment/P1_Terrain/

But do NOT overwrite the previous validated P1 terrain checkpoints.

Preserve the existing completed terrain phase.

============================================================
SOURCE SAFETY
============================================================

Before changing anything:

1. Hash all files under:
   environment/P1_Terrain/

2. Save the baseline hashes to:

reports/P1_terrain_02A_prepolish_hashes.json

3. Do not overwrite:
   terrain_01_blockout.blend
   terrain_02_flat_transition.blend
   terrain_03_cut_fill.blend
   terrain_04_retaining_rocks.blend
   terrain_05_materials_uv.blend
   terrain_06_lods_collision.blend
   terrain_07_export_ready.blend

4. Create NEW checkpoints only.

============================================================
KNOWN VALIDATED TERRAIN FACTS
============================================================

Do not change these unless fixing an actual defect requires it:

- 40.000 m module lengths
- 20.000 m module lengths
- first/last 2 m seam-safe zones
- 0.000 m verified seam gaps
- Unity +Y up
- Unity +Z forward
- Blender +Z up
- road direction -Y
- base ground at verge approximately -0.30 m
- terrain extends to ~50 m from centreline
- far ground extends toward ~1.5 km
- TerrainBlend:
    R = grass
    G = soil
    B = rock
    A = gravel
- VegetationMask:
    U = density
    V = dryness
- prop clearance zones
- existing snap points
- existing LOD structure
- existing collider strategy

Do not destabilize these systems.

============================================================
CURRENT KNOWN VISUAL DEFECTS
============================================================

Three issues were identified from actual preview inspection:

1. ROCK CUTS / CLIFFS

RockCut_A/B/C and Cliff_Module_A/B/C currently read as:

stacked stratified slabs

rather than believable natural road-cut rock.

2. ROAD-EDGE GRAVEL

The gravel/verge transition currently reads as:

a clean hard line

instead of a naturally irregular road-to-soil transition.

3. FLAT TERRAIN

Flat terrain looks too visually plain.

The geometry and technical setup are correct, but the surface lacks enough
large-scale variation to read as natural land.

These THREE issues are the focus of this phase.

============================================================
DO NOT SOLVE WITH VEGETATION
============================================================

Do not hide these defects with:

- trees
- bushes
- grass cards
- flowers
- heavy ground clutter

Fix the underlying terrain/readability first.

Vegetation comes next.

============================================================
NEW CHECKPOINTS
============================================================

Create:

blend/terrain_08_visual_polish.blend

and after final validation:

blend/terrain_09_final_frozen.blend

Do not modify terrain_07_export_ready.blend.

============================================================
STEP 01 — BASELINE REVIEW
============================================================

Open:

terrain_07_export_ready.blend

as reference.

Create a duplicate working copy:

terrain_08_visual_polish.blend

Inspect all existing previews.

Also inspect specifically:

- flat
- transition
- cut low
- cut medium
- rock cut
- cliff modules
- chase camera
- driver camera
- 200 m sequence
- road + props + terrain

Create:

reports/P1_terrain_02A_visual_baseline.md

Document:

- defect
- affected assets
- likely cause
- intended corrective action

============================================================
STEP 02 — ROCK-CUT ART DIRECTION
============================================================

The rock cuts must read as:

REAL EXPOSED HIGHWAY CUT ROCK

not:

stacked concrete slabs
horizontal pancakes
repeated terraces

Target characteristics:

- irregular large fracture planes
- discontinuous strata
- broken vertical joints
- asymmetric ledges
- occasional undercuts
- varied plane orientation
- believable erosion
- uneven silhouette
- larger primary rock masses
- secondary fractured areas

Keep some stratification if geologically appropriate.

But break its continuity.

============================================================
STEP 03 — ROCK FORM LANGUAGE
============================================================

Use a hierarchy:

PRIMARY FORMS
large mass/silhouette

SECONDARY FORMS
fractures and shelves

TERTIARY DETAIL
normal/material only

Do NOT model tiny cracks everywhere.

Do NOT uniformly subdivide.

Do NOT create noise-only rock.

The rock should still read clearly at:

5 m
20 m
50 m
100 m

============================================================
STEP 04 — BREAK HORIZONTAL REPETITION
============================================================

For:

RockCut_A
RockCut_B
RockCut_C

Cliff_Module_A
Cliff_Module_B
Cliff_Module_C

reduce the appearance of continuous horizontal bands.

Introduce:

- interrupted strata
- local vertical fractures
- angled bedding
- uneven erosion
- different major-plane directions per variant

Each variant should have its own silhouette identity.

============================================================
ROCK VARIANT TARGETS
============================================================

RockCut_A:

moderately stratified
but broken by strong vertical joints

RockCut_B:

more massive block structure
less obvious layering

RockCut_C:

diagonal/fractured geology
strong asymmetry

Cliff_A:

broad large planes

Cliff_B:

more fractured

Cliff_C:

mixed shelves and vertical break

Do not simply rotate one asset six times.

============================================================
STEP 05 — ROAD-CUT TOE
============================================================

Where rock meets terrain:

create a believable transition.

Use subtle:

- broken soil
- gravel
- small rock accumulation
- irregular toe geometry

Do not create a perfectly straight line between:

rock
and
grass.

Do not add thousands of individual stones.

============================================================
STEP 06 — ROCK LOD REVIEW
============================================================

After changing LOD0 rock silhouette:

regenerate/review LOD1–LOD3.

Maintain:

LOD1:
major fracture character

LOD2:
main silhouette

LOD3:
broad rock shape

Do not allow lower LODs to revert to obviously rectangular slabs.

============================================================
STEP 07 — ROCK UV / BLEND REVIEW
============================================================

Preserve:

TerrainBlend
VegetationMask
material conventions

Rock-heavy slopes should continue to have:

high B / Rock influence

Do not wipe vertex data.

Do not alter documented channel semantics.

============================================================
STEP 08 — ROAD EDGE TRANSITION
============================================================

The current road-edge gravel strip reads too much like:

ROAD
|
GRAVEL LINE
|
TERRAIN

Replace that visual impression with:

ROAD
→ irregular broken edge
→ gravel/soil mix
→ vegetation-ready soil
→ terrain

The transition should be subtle.

============================================================
STEP 09 — BREAK STRAIGHT GRAVEL EDGE
============================================================

Do NOT alter the P0 road mesh.

Terrain-side only.

Create variation in terrain transition using:

- irregular lateral edge
- varying gravel width
- small soil intrusions
- broken grass/soil patches
- occasional exposed dirt
- slight erosion

The road-side interface must still remain safe and deterministic.

Do NOT introduce geometry into:

- drivable road
- shoulder
- drain
- guardrail corridor

============================================================
GRAVEL WIDTH
============================================================

Avoid one constant perfect-width strip.

Allow subtle variation.

For example:

narrow areas
~0.15–0.30 m

normal:
~0.30–0.60 m

occasional broader erosion:
~0.60–0.90 m

Use actual road-clearance measurements.

Do not let the edge encroach on gameplay geometry.

============================================================
STEP 10 — GRAVEL BLEND MASK
============================================================

Improve TerrainBlend around road transition.

Instead of an abrupt:

A = 1
then
R = 1

create a smooth but irregular zone containing mixtures of:

gravel
soil
grass

Preserve the existing channel meanings.

Do not create new undocumented channels.

============================================================
STEP 11 — TRANSITION MACRO VARIATION
============================================================

Add low-frequency variation to the terrain-side transition.

Avoid:

perfectly continuous parallel lines.

At gameplay distance, the roadside should look naturally worn.

============================================================
STEP 12 — FLAT TERRAIN POLISH
============================================================

Flat terrain geometry currently reads too plain.

Do NOT solve this with excessive geometric noise.

Improve using three scales:

LARGE SCALE:
broad height variation

MEDIUM SCALE:
subtle drainage / depressions / soft mounds

SMALL SCALE:
material/normal variation

============================================================
LARGE-SCALE FLAT VARIATION
============================================================

Maintain seam-safe boundaries.

Interior of each 40 m module may have:

gentle undulation

Target only subtle height changes.

Approximate useful range:

±0.10 m to ±0.30 m

away from prop/road corridor.

Do not create bumps beside pole/gantry bases.

============================================================
MEDIUM-SCALE VARIATION
============================================================

Add restrained:

shallow depression
soft mound
erosion channel
soil patch

Each module should not contain every feature.

Create natural asymmetry.

Do not create obvious procedural waves.

============================================================
STEP 13 — MACRO MATERIAL VARIATION
============================================================

Use the existing 64 m macro variation mask or improve it.

Flat terrain should show subtle shifts in:

- grass value
- dryness
- soil exposure
- roughness

Do not make giant visible noise blobs.

============================================================
STEP 14 — TERRAIN MATERIAL REVIEW
============================================================

Review existing 2K:

Grass
Soil
Rock
Gravel

The goal is NOT to replace everything.

Improve only if necessary.

Check:

- scale
- contrast
- saturation
- roughness
- repetition

Flat grass must not look:

uniform bright green
painted
plastic

Prefer natural muted variation.

============================================================
STEP 15 — FUTURE VEGETATION SUPPORT
============================================================

Preserve and improve:

VegetationMask

where needed.

After terrain polish:

high vegetation density may exist on:
- flat grass
- gentle slopes
- open soil/grass mixes

lower density on:
- roadside transition
- dry zones
- steep slopes

zero on:
- road
- shoulder
- drain
- gravel-heavy transition
- prop clearance
- rock
- retaining wall

Do not generate vegetation yet.

============================================================
STEP 16 — PROP CLEARANCE RECHECK
============================================================

Link/reference P1 Props.

Re-check:

guardrail X ≈ -11

streetlights ≈ -12

signs ≈ -12.8

CCTV ≈ -14

and corresponding opposite-side placements where applicable.

No terrain polish may bury:

- pole bases
- guardrail posts
- sign posts
- CCTV
- gantry supports

============================================================
STEP 17 — SEAM SAFETY
============================================================

Re-run all seam validation after visual changes.

First 2 m and last 2 m of every modular terrain piece must still use the
standard boundary profile.

Test:

Flat
→ Cut
→ Flat
→ Fill

and:

Cut_In
→ Cut_Run
→ Cut_Run
→ Cut_Out
→ Flat

Tolerance target:

0.000 m visual gap

or the existing validated numeric tolerance.

============================================================
STEP 18 — RANDOM SEQUENCE QA
============================================================

Create a new 240 m QA sequence.

Example:

Flat
→ Cut Low
→ Rock Cut
→ Flat
→ Fill
→ Ditch

Use polished assets.

Inspect:

driver
chase
high chase

Look specifically for:

- slabby cliffs
- hard gravel stripe
- plain flat terrain
- visible seams

============================================================
STEP 19 — LIGHTING REVIEW
============================================================

Use Blender-only preview environments:

Day
Golden Hour
Overcast

Do not reproduce final Unity lighting.

Rock should remain readable in:

direct light
soft light
grazing light

============================================================
STEP 20 — REQUIRED BEFORE/AFTER RENDERS
============================================================

Create:

previews/02A_before_rockcut.png
previews/02A_after_rockcut.png

previews/02A_before_roadedge.png
previews/02A_after_roadedge.png

previews/02A_before_flatterrain.png
previews/02A_after_flatterrain.png

Also:

previews/02A_rockcut_driver.png

previews/02A_rockcut_chase.png

previews/02A_roadedge_close.png

previews/02A_flat_chase.png

previews/02A_240m_sequence.png

previews/02A_full_environment.png

============================================================
STEP 21 — VISUAL ACCEPTANCE TEST
============================================================

Do NOT rely only on automated validation.

Actually inspect every new render.

Hard visual gates:

A. ROCK

Must no longer primarily read as repeated horizontal slabs.

B. ROAD EDGE

Must no longer primarily read as one clean straight gravel line.

C. FLAT TERRAIN

Must no longer primarily read as a uniformly textured flat sheet.

If any of the three fails:

iterate before export.

============================================================
STEP 22 — GEOMETRY BUDGET
============================================================

Do not inflate geometry merely for detail.

Existing budgets are already healthy.

Rock/cliff LOD0 around ~2k tris is acceptable if silhouette works.

Terrain strips near the low end of existing budgets are acceptable.

Add geometry only when it materially improves:

- silhouette
- fracture plane
- edge transition
- broad terrain shape

============================================================
STEP 23 — COLLIDER INTEGRITY
============================================================

Visual polish should not require complex new collision.

Do not increase collider density unless absolutely required.

Retain existing simple collision strategy.

Verify visual changes do not cause collider/visual mismatch in accessible areas.

============================================================
STEP 24 — UPDATED EXPORT
============================================================

After visual acceptance passes:

create:

blend/terrain_09_final_frozen.blend

Export updated final production files.

Use the same grouping as P1-BLENDER-02:

terrain_complete.fbx

Terrain_Flat.fbx

Terrain_Cut.fbx

Terrain_Fill.fbx

Terrain_Drainage.fbx

Terrain_Retaining.fbx

Terrain_Rocks.fbx

Terrain_Vistas.fbx

Do not rename file families unnecessarily because Unity integration will later
depend on predictable names.

============================================================
STEP 25 — RE-IMPORT VALIDATION
============================================================

Re-import all 8 FBX files into a clean Blender scene.

Revalidate:

- coordinate conversion
- +Y Unity up
- +Z Unity forward
- 40 m modules
- 20 m modules
- snap points
- UVs
- TerrainBlend
- VegetationMask / UV1
- materials
- LODs
- colliders
- names
- hierarchy
- triangle counts

Target:

0 errors
0 critical warnings

============================================================
STEP 26 — UPDATE TERRAIN REPORTS
============================================================

Create:

reports/P1_terrain_02A_visual_polish.md

Include:

- original issue
- changes made
- affected assets
- before/after preview path
- triangle change
- LOD impact
- mask impact

Also create:

reports/P1_terrain_02A_validation.txt

and:

reports/P1_terrain_02A_export_manifest.json

============================================================
STEP 27 — SOURCE INTEGRITY
============================================================

Verify:

P0 Road Foundation unchanged

P1 Props unchanged

Cars unchanged

Also verify original terrain checkpoints:

terrain_01 through terrain_07

are unchanged.

Only new/updated final 02A deliverables may differ.

============================================================
STEP 28 — UNITY TRANSFER UPDATE
============================================================

Update:

P1_Terrain/UnityTransfer/

Replace only final terrain deliverables with polished validated versions.

Preserve:

README structure
Reports structure
Texture structure

Update:

README/TERRAIN_IMPORT_NOTES.md

to state:

P1-BLENDER-02A terrain polish applied.

Document:

- rock improvement
- transition improvement
- flat-terrain variation
- any changed triangle counts
- any changed texture/mask behavior

============================================================
STEP 29 — FINAL FREEZE
============================================================

Once validation passes, consider:

environment/P1_Terrain/

FROZEN.

Create:

reports/P1_terrain_FINAL_FREEZE.md

Include:

- final blend file
- final FBXs
- final UnityTransfer
- final validation status
- hashes
- date
- known remaining limitations

============================================================
COMPLETION GATE
============================================================

Do NOT declare complete until:

1. P0 remains unchanged.
2. P1 Props remains unchanged.
3. Cars remain unchanged.
4. Original terrain checkpoints 01–07 remain unchanged.
5. Rock cuts no longer primarily read as stacked slabs.
6. Cliff modules show differentiated natural silhouettes.
7. Rock LODs preserve improved silhouette.
8. Road-edge gravel transition is irregular/natural.
9. No gravel transition intrudes into gameplay road.
10. TerrainBlend transition remains valid.
11. VegetationMask remains valid.
12. Flat terrain has believable macro variation.
13. Flat terrain remains seam safe.
14. Prop clearances remain correct.
15. 40 m seam tests pass.
16. 20 m modules remain correct.
17. Random sequence passes.
18. Driver view passes.
19. Chase view passes.
20. Required before/after renders exist.
21. Visual review has been performed manually.
22. Updated FBXs export successfully.
23. All 8 FBXs re-import successfully.
24. Validation reports 0 errors.
25. UnityTransfer is updated.
26. Terrain import notes are updated.
27. Final freeze report exists.

============================================================
FINAL REPORT
============================================================

Return one complete report containing:

1. baseline/hash status
2. rock-cut defects confirmed
3. rock-cut changes
4. cliff changes
5. road-edge defect confirmed
6. road-edge changes
7. flat-terrain defect confirmed
8. flat-terrain changes
9. TerrainBlend changes
10. VegetationMask changes
11. triangle changes
12. LOD changes
13. collider changes
14. seam validation
15. prop-clearance result
16. before/after previews
17. driver/chase QA
18. exported FBXs
19. re-import result
20. updated UnityTransfer path
21. validation result
22. final frozen blend path
23. source-integrity status
24. remaining known limitations
25. recommended next Blender phase

============================================================
STOP CONDITION
============================================================

After P1-BLENDER-02A is complete:

STOP.

DO NOT START:

- Vegetation
- Tunnel
- City
- Bridge
- Vehicles
- Traffic
- Unity integration

Do not modify P0/P1 Props/cars.

Fix ONLY these terrain-quality defects,
freeze the terrain,
report results,
and STOP.
````


====================================================================================================
# SPEC: P1-BLENDER-03 — Production Vegetation System
====================================================================================================

````text
ACT AS:

A senior AAA Vegetation Artist, Blender Technical Artist,
Environment Artist, Procedural Asset Artist and Game Optimization Specialist
with 10+ years of production experience creating vegetation for modern
open-world, driving and racing games.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

DO NOT:

- search for Unity
- install Unity
- create Unity prefabs
- create Unity shaders
- create Unity materials
- modify RoadStreamer
- modify gameplay systems
- modify completed road assets
- modify completed prop assets
- modify completed terrain assets
- modify vehicle assets
- start Tunnel work
- start City work

Your responsibility is:

P1-BLENDER-03 — AAA PRODUCTION VEGETATION SYSTEM

Complete the entire phase:

DISCOVERY
→ FROZEN-SOURCE BASELINE
→ READ-ONLY REFERENCE LINKING
→ SPECIES PLAN
→ TREE BLOCKOUT
→ TREE PRODUCTION
→ TREE VARIANTS
→ SHRUBS
→ GRASS
→ WEEDS / SMALL PLANTS
→ MATERIAL / TEXTURE ATLASES
→ WIND DATA
→ LODs
→ IMPOSTOR SOURCE OUTPUTS
→ TERRAIN-MASK QA
→ PROP-CLEARANCE QA
→ ENVIRONMENT QA
→ OPTIMIZATION
→ FBX EXPORT
→ FBX RE-IMPORT VALIDATION
→ UNITY TRANSFER PACKAGE
→ FINAL REPORT
→ FREEZE
→ STOP


============================================================
CURRENT WORKSPACE
============================================================

Main workspace:

/Users/meetshah/Documents/blender

Completed and FROZEN:

environment/P0_RoadFoundation/

environment/P1_Props/

environment/P1_Terrain/

Finished vehicle directories are also frozen.

The FINAL terrain source is:

environment/P1_Terrain/blend/terrain_09_final_frozen.blend

Use ONLY that terrain checkpoint.

DO NOT use:

terrain_07_export_ready.blend

or any pre-02A terrain source as the active terrain reference.


============================================================
CRITICAL TERRAIN FREEZE RULE
============================================================

P1-BLENDER-02A is FINAL and FROZEN.

DO NOT modify:

- terrain geometry
- TerrainBlend
- VegetationMask
- rock cuts
- cliffs
- road-edge transition
- retaining walls
- terrain textures
- terrain UVs
- terrain LODs
- terrain colliders
- terrain exports
- P1 Terrain UnityTransfer package

The vegetation system must ADAPT TO THE TERRAIN.

If vegetation placement exposes a terrain problem:

DOCUMENT IT.

Do NOT edit the frozen terrain to make vegetation easier.


============================================================
OTHER FROZEN SOURCES
============================================================

P0 Road Foundation:

FROZEN

P1 Props:

FROZEN

Cars:

FROZEN

Use all only as LINKED / READ-ONLY references.

Do not save changes back into any frozen source file.


============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P1_Vegetation/

Use this structure:

P1_Vegetation/
├── blend/
├── exports/
├── textures/
│   ├── foliage/
│   ├── bark/
│   ├── grass/
│   ├── weeds/
│   └── impostors/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/


============================================================
PROJECT GOAL
============================================================

This is a realistic racing game.

The vegetation must support:

PREMIUM MODERN PC / CONSOLE VISUAL QUALITY

while remaining scalable for:

MOBILE

The current weakest vegetation signal in the project is the obvious
low-quality / faceted / simplistic tree look.

This phase must replace that look with a reusable production vegetation library.


============================================================
ART DIRECTION
============================================================

Target:

REALISTIC MODERN ROADSIDE VEGETATION

Suitable for:

- open highway
- suburban highway edges
- cut sections
- fill sections
- roadside embankments
- mixed grass / soil
- slightly dry roadside
- distant tree lines

Avoid:

- faceted sphere trees
- perfectly round crowns
- perfect cones
- identical cloned trees
- huge opaque foliage blobs
- thousands of individual modeled leaves
- noisy photogrammetry-style geometry
- fantasy vegetation
- giant hero trees
- overly tropical-specific vegetation
- overly specific country-only vegetation

The initial vegetation set should remain flexible enough for the existing
generic highway environment.


============================================================
VISUAL PRIORITY
============================================================

Vegetation should read in this order:

1. SILHOUETTE
2. CANOPY MASS
3. MAJOR BRANCHING
4. CANOPY GAPS
5. LEAF DETAIL

At gameplay distance, silhouette matters more than tiny leaf geometry.


============================================================
KNOWN ROAD / TERRAIN DATA
============================================================

Road modules:

40.000 m

Secondary road module:

20.000 m

Unity target orientation:

+Y up
+Z forward

Blender:

+Z up
road direction -Y

Road:

4 lanes × 3.60 m

Terrain extends approximately:

38–40 m outside the road kit on each side

Near-terrain outer edge:

approximately 50 m from road centreline

Far vistas continue beyond that.

Ground near verge:

approximately -0.30 m


============================================================
FINAL TERRAIN DATA
============================================================

TerrainBlend vertex colour semantics:

R = grass influence

G = soil influence

B = rock influence

A = gravel influence

Weights sum approximately to 1.


============================================================
FINAL VEGETATION MASK DATA
============================================================

VegetationMask is stored in:

UV CHANNEL 1

because Unity only imports one primary vertex-colour set.

Convention:

U = vegetation density

V = dryness


============================================================
NO-VEGETATION AREAS
============================================================

Vegetation density is already zero or should be treated as zero in:

- road
- shoulder
- drain
- d < approximately 16.5 m
- main prop corridor
- rock
- exposed cliff
- gravel-heavy transition
- retaining walls
- steep unsuitable faces

Do not override this logic.


============================================================
KNOWN PROP CLEARANCES
============================================================

Reference placements include approximately:

Guardrail:
X -11.0 m

Streetlights:
X -12.0 m

Signs:
X -12.8 m

CCTV:
X -14.0 m

Corresponding opposite-side clearances apply where relevant.

Vegetation must not intersect or obscure these systems.


============================================================
SOURCE INTEGRITY BASELINE
============================================================

Before creating anything:

Hash the frozen source folders:

P0_RoadFoundation

P1_Props

P1_Terrain

finished car folders

Save baseline to:

reports/P1_vegetation_source_baseline.json

At completion verify they are byte-for-byte unchanged.


============================================================
PHASE 01 — DISCOVERY
============================================================

Link read-only:

P0 road

P1 props

P1 final terrain

Optionally link a lightweight Hypercar reference for scale.

Inspect:

- TerrainBlend
- VegetationMask
- slopes
- cut sections
- fill sections
- roadside transition
- retaining walls
- rocks
- prop corridor
- chase-camera view
- driver-camera view

Create:

reports/P1_vegetation_discovery.md

Document:

- available placement data
- biome direction
- planned tree families
- planned bush families
- grass strategy
- material strategy
- atlas strategy
- LOD strategy
- wind-data strategy
- impostor strategy
- expected Unity integration assumptions


============================================================
PHASE 02 — SPECIES PLAN
============================================================

Create a focused first production library.

Required:

8 TREE ARCHETYPES

6 SHRUB / BUSH ASSETS

8–12 GRASS / GROUND-COVER ASSETS

4–6 WEED / SMALL PLANT ASSETS

Optional:

2 dry/dead vegetation assets

Do not create dozens of unnecessary species.


============================================================
TREE ARCHETYPES
============================================================

Create:

Tree_Broadleaf_A

Tree_Broadleaf_B

Tree_Broadleaf_C

Tree_Broadleaf_D

Tree_SmallRoadside_A

Tree_SmallRoadside_B

Tree_Conifer_A

Tree_Conifer_B


============================================================
TREE DESIGN TARGETS
============================================================

Tree_Broadleaf_A:

- broad roadside canopy
- rounded but irregular
- wide lower silhouette

Tree_Broadleaf_B:

- taller
- narrower
- asymmetric crown

Tree_Broadleaf_C:

- open canopy
- visible branching
- irregular gaps

Tree_Broadleaf_D:

- denser umbrella-like canopy
- natural uneven outline

Tree_SmallRoadside_A:

- compact young tree
- approximately 4–6 m

Tree_SmallRoadside_B:

- more asymmetrical
- slight natural lean
- approximately 5–7 m

Tree_Conifer_A:

- taller narrow conifer

Tree_Conifer_B:

- broader irregular conifer

Do NOT create the same tree and only scale it.


============================================================
TREE HEIGHT GUIDANCE
============================================================

Small roadside:

4–7 m

Medium broadleaf:

7–12 m

Large broadleaf:

10–15 m

Conifers:

8–16 m

These are guidance values, not rigid quotas.


============================================================
TREE VARIANTS
============================================================

For each major archetype create at least:

Variant_A

Variant_B

Variant_C

Variation should come from:

- crown shape
- branch orientation
- trunk lean
- canopy gaps
- canopy density
- major silhouette
- mild scale variation

Do not create 3 variants by only rotating the same tree.


============================================================
TREE BLOCKOUT
============================================================

Create:

blend/vegetation_01_blockout.blend

Block out all 8 tree archetypes first.

Before detailed foliage:

validate:

- height
- width
- road-scale relationship
- streetlight relationship
- chase-camera silhouette

Do not detail badly proportioned trees.


============================================================
TREE STRUCTURE
============================================================

Use geometry for:

- trunk
- major branches
- silhouette-relevant secondary branches

Do NOT model every twig.

Use efficient tapered branch meshes.

Avoid:

- perfect cylinders
- repetitive Y branches
- excessive subdivisions
- identical branch spacing


============================================================
TREE BASE
============================================================

Create:

- subtle trunk widening
- modest root flare where useful

Do not build giant exposed roots.

Origin:

bottom-centre of trunk at ground contact.


============================================================
CANOPY STRATEGY
============================================================

Use optimized foliage clusters / foliage cards.

Do NOT model thousands of individual leaves.

Foliage should create:

- depth
- layered canopy
- natural silhouette
- internal gaps
- believable mass

Avoid obvious giant X-shaped cards.


============================================================
ALPHA OVERDRAW — CRITICAL
============================================================

Mobile scalability is important.

Do NOT create huge foliage planes with mostly transparent pixels.

Leaf-cluster cards should be tightly cropped.

Prefer:

more efficient leaf clusters

instead of:

large nearly empty alpha quads.

Inspect alpha-card density visually.


============================================================
FOLIAGE ATLAS
============================================================

Create a shared atlas:

T_Vegetation_Leaves_Atlas_2K

Preferred maps:

BaseColor + Alpha

Normal

Roughness

Optional:
AO / variation mask if beneficial

Do NOT create a unique 2K foliage texture per tree species.


============================================================
BARK ATLAS
============================================================

Create:

T_Vegetation_Bark_Atlas_2K

Include useful regions such as:

- light smooth bark
- medium bark
- dark/coarse bark
- conifer bark

Maps:

BaseColor

Normal

Roughness

AO

Share bark across species where visually acceptable.


============================================================
DRYNESS / COLOUR VARIATION SUPPORT
============================================================

Prepare material/texture data to support later Unity colour variation.

Useful visual states:

healthy green

slightly dry green

yellow/dry tint

Do NOT create fully separate seasonal tree texture sets.

If useful create a variation mask in a spare texture channel.


============================================================
TREE MATERIALS
============================================================

Create Blender source materials:

MAT_Veg_Bark

MAT_Veg_Leaves_Broadleaf

MAT_Veg_Leaves_Conifer

MAT_Veg_Leaves_Dry

These are SOURCE/PREVIEW materials.

Do not attempt final Unity vegetation shaders.


============================================================
LEAF NORMALS
============================================================

Configure foliage normals to create fuller canopy lighting.

Avoid:

- black card backs
- harsh planar shading
- plastic-looking leaves

Document any custom normal approach.


============================================================
DOUBLE-SIDED FOLIAGE
============================================================

Prepare foliage for double-sided rendering later in Unity.

Do NOT duplicate all cards just to produce a back face unless Blender/export
requires it.

Document expected Unity double-sided setup.


============================================================
WIND DATA
============================================================

Create a vertex colour layer named:

WindData

Use consistent channel meanings:

R = primary branch bend strength

G = leaf / fine flutter strength

B = phase / random offset

A = stiffness / anchor influence


============================================================
WIND EXAMPLE
============================================================

Trunk base:

R ≈ 0
G ≈ 0
A high stiffness

Upper trunk / branches:

increasing R

Leaf clusters:

higher G

Different clusters:

vary B slightly for phase differences

Do not create actual Unity wind animation.

Only prepare data.


============================================================
TREE LOD STRATEGY
============================================================

Each major tree must have:

LOD0

LOD1

LOD2

LOD3

plus:

IMPOSTOR-READY SOURCE OUTPUT


============================================================
TREE LOD PURPOSE
============================================================

LOD0:

PC close-up / garage-like showcase / premium near field

LOD1:

normal PC gameplay / high-end mobile near

LOD2:

normal mobile gameplay / medium distance

LOD3:

far mesh

Impostor:

very far distance


============================================================
TREE TRIANGLE GUIDANCE
============================================================

Large Broadleaf:

LOD0:
approximately 6k–12k

LOD1:
3k–6k

LOD2:
1k–2.5k

LOD3:
250–700

Small Tree:

LOD0:
3k–7k

LOD1:
1.5k–3.5k

LOD2:
600–1.5k

LOD3:
150–500

Conifer:

LOD0:
5k–10k

LOD1:
2.5k–5k

LOD2:
800–2k

LOD3:
200–600

Do NOT pad geometry to reach these ranges.

If silhouette quality is good at lower triangle counts:

keep the lower counts.


============================================================
LOD REDUCTION RULE
============================================================

Remove first:

- hidden interior foliage cards
- tiny branches
- small internal leaf groups

Preserve:

- overall height
- width
- trunk position
- major canopy gaps
- species identity
- outer silhouette


============================================================
LOD POP QA
============================================================

Create side-by-side or distance QA for:

LOD0
LOD1
LOD2
LOD3

Check:

- silhouette
- density
- trunk popping
- branch popping
- canopy collapse

Do not allow major visual popping.


============================================================
IMPOSTOR SOURCE OUTPUT
============================================================

Create impostor source renders for each main tree archetype.

Do NOT create final Unity impostor shaders.

Preferred captures:

8 horizontal directions

plus optional top/down view if useful.

Transparent background.

Consistent camera.

Consistent lighting.

Consistent scale.


============================================================
IMPOSTOR FILES
============================================================

Store under:

textures/impostors/

For each main species include:

BaseColor + Alpha

and where practical:

Normal

Depth

Avoid baked dramatic directional shadows in colour.


============================================================
IMPOSTOR GUIDE
============================================================

Create:

reports/P1_vegetation_impostor_guide.md

Document:

- species
- view directions
- resolution
- camera setup
- lighting setup
- alpha
- normal
- depth
- intended Unity usage


============================================================
SHRUB LIBRARY
============================================================

Create:

Bush_A

Bush_B

Bush_C

Bush_D

Bush_Dry_A

Hedge_Organic_A


============================================================
SHRUB SILHOUETTES
============================================================

Bush_A:
rounded but irregular

Bush_B:
wide / low

Bush_C:
upright

Bush_D:
sparse / asymmetrical

Bush_Dry_A:
dry / sparse

Hedge_Organic_A:
linear but natural

Do NOT make all bushes into foliage spheres.


============================================================
SHRUB SIZE
============================================================

Target approximately:

0.5–2.0 m height

depending on type.


============================================================
SHRUB LODS
============================================================

At least:

LOD0
LOD1
LOD2

Optional:
LOD3

Suggested:

LOD0:
500–2,000 tris

LOD1:
250–800

LOD2:
80–250

Lower is acceptable if quality holds.


============================================================
GRASS LIBRARY
============================================================

Create:

Grass_Short_A

Grass_Short_B

Grass_Medium_A

Grass_Medium_B

Grass_Tall_A

Grass_Tall_B

Grass_Dry_A

Grass_Dry_B

Optional:

Grass_RoadEdge_A

Grass_RoadEdge_B


============================================================
GRASS DESIGN
============================================================

Create reusable grass clumps.

Do NOT create whole 40 m grass-covered meshes.

Unity will later handle runtime distribution.

Use tightly cropped alpha cards.

Multiple orientations per clump.

Avoid giant empty transparent quads.


============================================================
GRASS ATLAS
============================================================

Create:

T_Vegetation_Grass_Atlas_2K

Include:

- short green
- medium green
- tall green
- dry grass
- small weeds

Maps:

BaseColor + Alpha

Normal

Roughness


============================================================
WEED / SMALL PLANT LIBRARY
============================================================

Create approximately:

Weed_A

Weed_B

Weed_C

WildPlant_A

WildPlant_B

Optional:

FlowerSparse_A

Keep these subtle.

This is a racing game.

Do not turn them into hero botanical assets.


============================================================
GROUND-COVER RULE
============================================================

Do NOT bake thousands of grass/weed instances into exported terrain.

Create reusable assets only.

Blender scatter is QA only.


============================================================
TERRAIN PLACEMENT RULES
============================================================

Use TerrainBlend + VegetationMask for QA placement.

General rules:

High R / Grass:
vegetation-friendly

High G / Soil:
reduced or mixed density

High B / Rock:
very low / none

High A / Gravel:
very low / none

VegetationMask U:
primary density

VegetationMask V:
dryness


============================================================
DRYNESS QA
============================================================

Higher dryness may favour:

Grass_Dry

Bush_Dry

less saturated green

lower density

Do not make dry areas entirely yellow.


============================================================
SLOPE RULES
============================================================

Flat / gentle slopes:

trees
bushes
grass

Moderate slope:

bushes
grass
occasional tree

Steep cut:

sparse small vegetation

Rock face:

almost none

Do not grow trees sideways from cliff faces.


============================================================
ROAD CLEARANCE
============================================================

No vegetation inside:

- road
- lane markings
- shoulder
- drain
- immediate road transition
- guardrail clearance
- streetlight base
- sign base
- gantry support
- CCTV base


============================================================
LARGE TREE DISTANCE FROM ROAD
============================================================

Do not place large trees directly beside high-speed traffic.

QA placement strategy:

Near road:
grass
small bushes
occasional small tree

Further away:
medium / large trees

Far edge:
tree clusters / larger vegetation


============================================================
GUARDRAIL RELATIONSHIP
============================================================

Grass may approach behind guardrails.

Do not:

- grow through rail
- hide reflectors
- bury posts
- cover delineators


============================================================
SIGN / GANTRY VISIBILITY
============================================================

Vegetation must not block:

- sign faces
- VMS
- gantry panels
- sightlines

Preserve believable road visibility.


============================================================
TREE CLUSTERING
============================================================

Do NOT uniformly randomize every species.

Use natural clustering.

Example:

Broadleaf_A cluster

gap

Broadleaf_C + shrubs

gap

mixed small trees

Avoid:

Tree A
Tree B
Tree C
Tree D
every 10 m in a repeating pattern.


============================================================
SCALE VARIATION
============================================================

For QA scatter:

Trees:
approximately 0.85–1.15

Shrubs:
0.8–1.25

Grass:
0.7–1.3

Use restrained variation.


============================================================
ROTATION
============================================================

Yaw:
0–360°

Small natural tree lean may be used.

Do not randomly tilt all trees heavily.


============================================================
BLENDER QA SCATTER TOOL
============================================================

Create a Blender-only procedural QA scatter system/script.

It may use:

- VegetationMask
- TerrainBlend
- slope
- road distance
- prop distance
- dryness

This is ONLY for preview/testing.

Do NOT export scattered instances as part of terrain/road FBXs.


============================================================
QA DENSITY PRESETS
============================================================

Create preview presets:

Sparse_Highway

Normal_Highway

Dense_FarEdge

Use Normal_Highway for primary art QA.


============================================================
MATERIAL COUNT
============================================================

Keep runtime-oriented shared material categories low.

Target approximately:

4–8 shared material categories

before Unity-specific material instances.

Do not create one material per species.


============================================================
ATLAS STRATEGY
============================================================

Prefer:

1 shared broadleaf foliage atlas

1 shared conifer/alternate foliage section or atlas

1 shared bark atlas

1 shared grass/weed atlas

Do not create 30 separate textures.


============================================================
TEXTURE RESOLUTION
============================================================

Preferred:

2048 × 2048

Use 4K only if a shared atlas clearly requires it.

Do not create 8K vegetation maps.


============================================================
ALPHA PADDING
============================================================

Ensure leaf and grass islands have enough colour bleed/padding.

No:

white fringe

black fringe

mipmap halo

Document alpha-cutoff expectations for Unity.


============================================================
NORMAL MAP QUALITY
============================================================

Keep foliage normals subtle.

Do not make leaves look embossed or plastic.

Bark normals can carry more structural detail.


============================================================
OPTIONAL TREE COLLIDERS
============================================================

Do not create foliage collision.

For major trees only, if useful, create OPTIONAL simple trunk proxies:

Collision_Tree_Broadleaf_A

etc.

Use simple:

cylinder/capsule-like low-poly geometry.

Do not create branch collision.

If gameplay does not currently need off-road tree collisions, document them as optional.


============================================================
ORIGINS
============================================================

Trees:

bottom centre of trunk

Bushes:

bottom centre

Grass:

bottom centre

Weeds:

bottom centre

No random origins.


============================================================
TRANSFORMS
============================================================

All production assets:

Scale = 1,1,1

No negative scales.

Apply transforms where safe.

No unexplained residual rotations.


============================================================
COLLECTION STRUCTURE
============================================================

Use:

VEGETATION_MASTER

VEG_TREES_BROADLEAF

VEG_TREES_SMALL

VEG_TREES_CONIFER

VEG_SHRUBS

VEG_GRASS

VEG_WEEDS

VEG_IMPOSTOR_SOURCE

VEG_COLLISION_OPTIONAL

VEG_QA

VEG_PRESENTATION


============================================================
NAMING
============================================================

Examples:

Tree_Broadleaf_A_VariantA_LOD0

Tree_Broadleaf_A_VariantA_LOD1

Tree_Broadleaf_A_VariantA_LOD2

Tree_Broadleaf_A_VariantA_LOD3

Bush_A_LOD0

Grass_Short_A

Collision_Tree_Broadleaf_A

Use consistent naming.


============================================================
BLEND CHECKPOINTS
============================================================

Create:

blend/vegetation_01_blockout.blend

blend/vegetation_02_trees.blend

blend/vegetation_03_shrubs_grass.blend

blend/vegetation_04_materials_atlases.blend

blend/vegetation_05_wind_lods.blend

blend/vegetation_06_terrain_qa.blend

blend/vegetation_07_export_ready.blend

Do NOT overwrite previous checkpoints.


============================================================
TREE QUALITY QA
============================================================

Inspect each main tree from:

front

side

back

slightly elevated view

driver-distance view

chase-camera view

approximately 50 m

approximately 100 m

Do not approve a tree based only on studio close-up.


============================================================
ALPHA OVERDRAW QA
============================================================

Create a debug foliage-card view.

Inspect:

- overlapping cards
- transparent empty area
- hidden cards
- excessive interior foliage

Optimize obvious waste.


============================================================
LOD QA
============================================================

Create:

previews/P1_tree_LODs.png

Show representative:

LOD0
LOD1
LOD2
LOD3

for at least:

Broadleaf_A

Broadleaf_C

Conifer_A

SmallRoadside_A


============================================================
STUDIO PREVIEWS
============================================================

Create:

previews/P1_vegetation_tree_library.png

previews/P1_tree_broadleaf_A.png

previews/P1_tree_broadleaf_B.png

previews/P1_tree_broadleaf_C.png

previews/P1_tree_broadleaf_D.png

previews/P1_tree_conifer_A.png

previews/P1_tree_conifer_B.png

previews/P1_small_trees.png

previews/P1_shrub_library.png

previews/P1_grass_library.png

previews/P1_weeds.png

previews/P1_tree_LODs.png

previews/P1_impostor_sources.png


============================================================
ENVIRONMENT QA SCENE
============================================================

Build a temporary:

240–320 m

highway vegetation QA scene.

LINK read-only:

P0 road

P1 props

P1 final terrain

Optionally link Hypercar for scale.

Populate using the QA scatter system.

Do NOT export this populated scene as a runtime asset.


============================================================
QA ENVIRONMENT MUST INCLUDE
============================================================

At least:

Flat terrain

Cut section

Rock cut

Fill section

Ditch section

Guardrail

Streetlights

Signs

Gantry

CCTV

Mixed vegetation


============================================================
ENVIRONMENT PREVIEWS
============================================================

Create:

previews/P1_vegetation_driver_view.png

previews/P1_vegetation_chase_view.png

previews/P1_vegetation_high_chase.png

previews/P1_vegetation_cut_section.png

previews/P1_vegetation_fill_section.png

previews/P1_vegetation_roadside.png

previews/P1_vegetation_golden_hour.png

previews/P1_vegetation_overcast.png

previews/P1_vegetation_full_environment.png


============================================================
BEFORE / AFTER
============================================================

Create:

previews/P1_vegetation_before_after.png

Use same camera.

Compare:

Terrain only

vs

Terrain + Vegetation

The visual improvement should be obvious.


============================================================
VISUAL HARD GATES
============================================================

A. TREE QUALITY

Trees must NOT look like:

faceted spheres

perfect cones

simple cylinders with balls

B. SPECIES DIFFERENTIATION

Main species must be distinguishable by silhouette.

C. CLONING

At chase-camera distance, variants must reduce obvious repetition.

D. SCALE

Trees must look correctly scaled relative to:

car

road

streetlights

gantries

E. TERRAIN CONTACT

No floating vegetation.

No buried trunks.

F. INFRASTRUCTURE CLEARANCE

No vegetation intersects:

road

guardrails

streetlights

signs

gantries

CCTV

G. PERFORMANCE DESIGN

Vegetation must use:

LODs

shared materials

atlases

optimized cards

H. ALPHA OVERDRAW

Cards must not waste huge transparent areas.


============================================================
AUTOMATION
============================================================

Store scripts under:

scripts/

Suggested:

vegetation_build.py

vegetation_materials.py

vegetation_lods.py

vegetation_wind.py

vegetation_impostors.py

vegetation_scatter_qa.py

vegetation_validate.py

vegetation_render.py

vegetation_export.py


============================================================
EXPORT ORIENTATION
============================================================

Use the same proven Blender → Unity export process used by:

Hypercar

P0 Road

P1 Props

P1 Terrain

Target Unity:

+Y up
+Z forward

Do not blindly enable Blender Apply Transform if the proven pipeline uses
another axis-conversion approach.


============================================================
FBX EXPORT
============================================================

Primary format:

FBX

Create:

exports/vegetation_complete.fbx

Also split files:

exports/Trees_Broadleaf.fbx

exports/Trees_Small.fbx

exports/Trees_Conifer.fbx

exports/Shrubs.fbx

exports/Grass.fbx

exports/Weeds.fbx

exports/Vegetation_CollisionOptional.fbx

Adjust grouping only if there is a cleaner production reason.


============================================================
EXPORT CONTENT
============================================================

Export only production assets.

EXCLUDE:

- P0 road references
- P1 props references
- terrain references
- Hypercar reference
- QA scatter
- QA cameras
- Blender lights
- presentation ground
- impostor rendering rigs
- temporary helpers


============================================================
IMPOSTOR EXPORT
============================================================

Do not put Blender impostor render rigs in main FBX.

Package source renders separately under:

textures/impostors/


============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

After export:

create a clean Blender scene.

Re-import EVERY FBX.

Validate:

- scale
- dimensions
- orientation
- Unity +Y up conversion
- Unity +Z forward
- hierarchy
- names
- pivots
- UVs
- materials
- WindData
- LODs
- optional colliders
- triangle counts

Target:

0 errors.


============================================================
VALIDATION REPORT
============================================================

Create:

reports/P1_vegetation_validation.txt

Check:

1. required tree archetypes
2. tree variants
3. shrubs
4. grass assets
5. weeds
6. foliage atlas
7. bark atlas
8. grass atlas
9. alpha padding
10. UVs
11. materials
12. WindData
13. LOD chains
14. decreasing triangle counts
15. pivots
16. transforms
17. normals
18. source integrity
19. terrain-mask QA
20. prop-clearance QA
21. impostor sources
22. FBX export
23. FBX re-import

Target:

0 errors

0 critical warnings

DO NOT warn merely because geometry is below suggested triangle budgets.


============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P1_vegetation_geometry.json

For each asset include:

- name
- family
- archetype
- variant
- LOD
- triangle count
- vertex count
- height
- canopy width
- materials
- UV status
- WindData status
- collider status


============================================================
MATERIAL REPORT
============================================================

Create:

reports/P1_vegetation_materials.md

Document:

- foliage atlas
- bark atlas
- grass atlas
- texture dimensions
- texture channels
- alpha strategy
- padding
- bark strategy
- leaf strategy
- grass strategy
- colour/dryness variation


============================================================
WIND GUIDE
============================================================

Create:

reports/P1_vegetation_wind_guide.md

Document:

WindData R

WindData G

WindData B

WindData A

Include examples for:

trunk base

upper branch

leaf cluster

grass


============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P1_vegetation_export_manifest.json

Include:

- source blend
- FBXs
- included assets
- LODs
- materials
- textures
- impostor sources
- optional colliders
- excluded QA objects
- axis conversion


============================================================
SOURCE INTEGRITY CHECK
============================================================

At completion verify frozen sources again.

Create:

reports/P1_vegetation_source_integrity_check.md

Confirm:

P0 Road unchanged

P1 Props unchanged

P1 Terrain unchanged

cars unchanged

Target:

BYTE-FOR-BYTE UNCHANGED


============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

UnityTransfer/

Structure:

UnityTransfer/
├── FBX/
├── Textures/
│   ├── Foliage/
│   ├── Bark/
│   ├── Grass/
│   ├── Weeds/
│   └── Impostors/
├── Reports/
└── README/


============================================================
UNITY IMPORT NOTES
============================================================

Create:

UnityTransfer/README/VEGETATION_IMPORT_NOTES.md

Document:

1. phase
2. Unity orientation
3. scale
4. tree families
5. variants
6. FBX files
7. LOD naming
8. foliage atlas
9. bark atlas
10. grass atlas
11. alpha clipping expectation
12. double-sided foliage expectation
13. WindData
14. optional colliders
15. impostor sources
16. expected GPU instancing
17. recommended LOD usage
18. culling recommendations
19. terrain relationship
20. excluded QA content

State clearly:

THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.

UNITY-SIDE:

VEGETATION SHADERS

WIND

GPU INSTANCING

LODGroup COMPONENTS

IMPOSTOR RUNTIME SETUP

SCATTERING

CULLING

QUALITY TIERS

AND PERFORMANCE TESTING

MUST BE DONE ON THE UNITY WORKSTATION.


============================================================
VEGETATION PLACEMENT GUIDE
============================================================

Create:

UnityTransfer/README/VEGETATION_PLACEMENT_GUIDE.md

Document how Unity should interpret:

TerrainBlend

VegetationMask UV1

Slope

Road distance

Prop distance

Dryness

for placement of:

trees

shrubs

grass

dry grass

weeds

Do not prescribe one rigid implementation if multiple valid Unity approaches exist.


============================================================
UNITY PERFORMANCE GUIDANCE
============================================================

Document expected policy:

PC:

LOD0 near

LOD1 normal gameplay

LOD2 mid distance

LOD3 far

Impostor very far


Mobile:

often LOD1 or LOD2 near

LOD3 earlier

Impostor sooner

reduced grass distance

GPU instancing

aggressive culling

Do NOT claim measured Unity performance.

This workstation cannot test Unity.


============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P1-BLENDER-03 COMPLETE UNTIL:

1. P0 Road is unchanged.
2. P1 Props is unchanged.
3. P1 Terrain is unchanged.
4. Cars are unchanged.
5. Eight tree archetypes exist.
6. Major trees have useful variants.
7. Broadleaf silhouettes differ clearly.
8. Conifer silhouettes differ clearly.
9. Small-roadside trees exist.
10. Six shrub/bush assets exist.
11. Grass library exists.
12. Weed/small-plant library exists.
13. Shared foliage atlas exists.
14. Shared bark atlas exists.
15. Shared grass atlas exists.
16. Alpha padding is valid.
17. UVs are valid.
18. WindData exists.
19. WindData semantics are consistent.
20. Major tree LOD0–LOD3 exist.
21. Shrub LODs exist.
22. Grass assets are optimized.
23. Impostor source renders exist.
24. Pivots are correct.
25. Production transforms are clean.
26. No negative scales.
27. QA scatter reads VegetationMask.
28. QA scatter reads TerrainBlend.
29. Vegetation avoids prop corridor.
30. No trees penetrate road.
31. No trees penetrate guardrails.
32. Signs remain readable.
33. Driver-view QA passes.
34. Chase-view QA passes.
35. High-chase QA passes.
36. Species repetition is acceptable.
37. Before/after comparison exists.
38. FBXs export.
39. Every FBX re-imports correctly.
40. Validation has 0 errors.
41. Geometry report exists.
42. Material report exists.
43. Wind guide exists.
44. Impostor guide exists.
45. Export manifest exists.
46. UnityTransfer exists.
47. Import notes exist.
48. Placement guide exists.
49. Source integrity passes.


============================================================
FINAL FREEZE
============================================================

After successful validation:

Create:

reports/P1_vegetation_FINAL_FREEZE.md

Record:

- final blend
- FBXs
- textures
- UnityTransfer
- validation
- important hashes
- known limitations

Treat:

environment/P1_Vegetation/

as FROZEN after completion.


============================================================
FINAL REPORT
============================================================

Return ONE complete report containing:

1. discovery findings
2. source integrity
3. tree archetypes
4. tree variants
5. tree heights
6. canopy widths
7. shrub library
8. grass library
9. weed library
10. material list
11. foliage atlas
12. bark atlas
13. grass atlas
14. alpha strategy
15. UV strategy
16. WindData
17. tree LOD strategy
18. shrub LOD strategy
19. triangle counts
20. impostor source setup
21. optional colliders
22. TerrainBlend QA
23. VegetationMask QA
24. prop-clearance QA
25. driver-view QA
26. chase-view QA
27. high-chase QA
28. repetition QA
29. before/after result
30. checkpoint paths
31. preview paths
32. FBX paths
33. FBX re-import result
34. validation result
35. UnityTransfer path
36. import notes
37. placement guide
38. freeze report
39. known limitations
40. recommended next Blender phase


============================================================
STOP CONDITION
============================================================

After P1-BLENDER-03 VEGETATION is complete:

STOP.

DO NOT START:

- Tunnel
- City
- Bridge remaster
- Traffic rebuild
- Player-car rebuild
- Mountain/coastal environment
- Unity integration
- Unity vegetation shader
- Unity scatter system
- Unity performance work

Do NOT modify:

P0 Road Foundation

P1 Props

P1 Terrain

finished vehicles

Do NOT launch or install Unity.

FINISH THE VEGETATION LIBRARY,
CREATE TREE VARIANTS,
CREATE LODS,
CREATE WIND DATA,
CREATE IMPOSTOR SOURCE OUTPUTS,
VALIDATE EVERYTHING,
EXPORT,
RE-IMPORT,
PACKAGE FOR UNITY,
FREEZE THE PHASE,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P1-BLENDER-03A — Vegetation LOD0 / Foliage Quality / Final Polish
====================================================================================================

````text
ACT AS:

A senior AAA Vegetation Artist, Blender Technical Artist,
Environment Artist and Real-Time Optimization Specialist
with 10+ years of production experience.

You are working on a BLENDER-ONLY workstation.

There is NO Unity project on this machine.

P1-BLENDER-03 — PRODUCTION VEGETATION SYSTEM is COMPLETE.

This is NOT a vegetation rebuild.

Your task is a short targeted production polish phase:

P1-BLENDER-03A — VEGETATION LOD0 / FOLIAGE QUALITY / FINAL POLISH

Complete:

BASELINE
→ VISUAL REVIEW
→ WOOD GEOMETRY OPTIMIZATION
→ FOLIAGE DEPTH / INTERIOR SHADING POLISH
→ CONIFER POLISH
→ SPECIES MIX QA
→ LOD REGRESSION
→ ALPHA / NORMAL / WIND REGRESSION
→ EXPORT
→ RE-IMPORT
→ VALIDATION
→ UPDATE UNITY TRANSFER
→ FINAL FREEZE
→ STOP


============================================================
CURRENT WORKSPACE
============================================================

Workspace:

/Users/meetshah/Documents/blender

Frozen completed phases:

environment/P0_RoadFoundation/
environment/P1_Props/
environment/P1_Terrain/

Current vegetation phase:

environment/P1_Vegetation/

Current final vegetation checkpoint:

environment/P1_Vegetation/blend/vegetation_07_export_ready.blend

P0, Props, Terrain and vehicles are STRICTLY FROZEN.

Do not modify them.


============================================================
CRITICAL SCOPE RULE
============================================================

DO NOT:

- rebuild the vegetation library
- create new biomes
- create more tree species unless absolutely necessary
- create Unity shaders
- launch Unity
- create terrain
- edit terrain masks
- edit props
- edit road
- edit vehicles
- start Tunnel
- start City

Fix ONLY the remaining vegetation-quality weaknesses.


============================================================
KNOWN VALIDATED STATUS
============================================================

P1-BLENDER-03 currently has:

39 validation checks

0 errors

0 warnings

8 FBXs re-import successfully

8 tree archetypes × 3 variants

6 shrubs

10 grass clumps

6 weeds/small plants

WindData

LOD0–LOD3

impostor sources

optional trunk colliders

shared 2K foliage / bark / grass atlases

UnityTransfer package

All frozen upstream sources are byte-for-byte unchanged.


============================================================
KNOWN CURRENT WEAKNESSES
============================================================

The following issues are confirmed from the completed phase:

1. BROADLEAF LOD0 IS WOOD-HEAVY

Example:

Tree_Broadleaf_A LOD0:
~8,932 triangles

Approximately:
~6,500 triangles are trunk / branch geometry

and only around:
~1,200 foliage cards

This means approximately 73% of LOD0 is wood geometry.

That ratio is unnecessarily expensive for a racing-game tree.

2. CLOSE FOLIAGE STILL SHOWS INDIVIDUAL CARDS

The system is acceptable at gameplay distance but individual cards remain
visible close-up.

3. CONIFERS ARE DARK AND TOO UNIFORM

Their silhouette works but internal foliage lighting and colour variation need
improvement.

4. QA SPECIES MIX IS UNEVEN

7 of 8 archetypes are used normally.

Broadleaf_D appears only once in the QA scatter.

This is not a library defect but makes visual repetition QA less representative.

5. IMPOSTORS HAVE HORIZONTAL VIEWS ONLY

This is acceptable for now.

Do NOT expand impostor scope unless needed for validation.

6. GRASS LOOKS LIKE TUFTS AT CURRENT QA DENSITY

This is expected.

Do NOT solve it by baking massive grass populations in Blender.

Unity will handle real density later.


============================================================
SOURCE SAFETY
============================================================

Before modifying vegetation:

hash all existing files under:

environment/P1_Vegetation/

Create:

reports/P1_vegetation_03A_prepolish_hashes.json

Do not overwrite existing checkpoints:

vegetation_01_blockout.blend
vegetation_02_trees.blend
vegetation_03_shrubs_grass.blend
vegetation_04_materials_atlases.blend
vegetation_05_wind_lods.blend
vegetation_06_terrain_qa.blend
vegetation_07_export_ready.blend

Create NEW checkpoints only.


============================================================
NEW CHECKPOINTS
============================================================

Create:

blend/vegetation_08_lod0_polish.blend

Then final:

blend/vegetation_09_final_frozen.blend


============================================================
STEP 01 — VISUAL BASELINE
============================================================

Review actual existing previews.

Inspect especially:

- Broadleaf_A close
- Broadleaf_C close
- Conifer_A
- Conifer_B
- tree library
- LOD comparison
- driver view
- chase view
- high chase
- before/after environment
- alpha-overdraw debug

Do NOT rely only on validator output.

Create:

reports/P1_vegetation_03A_visual_baseline.md

For each defect document:

- affected asset
- visual symptom
- technical cause
- intended fix


============================================================
STEP 02 — WOOD GEOMETRY AUDIT
============================================================

Audit all tree archetypes, not only Broadleaf_A.

Report per tree:

- total LOD0 tris
- trunk tris
- primary branch tris
- secondary branch tris
- foliage tris
- foliage-card count

Create:

reports/P1_vegetation_wood_geometry_audit.json


============================================================
STEP 03 — WOOD OPTIMIZATION GOAL
============================================================

Reduce branch/trunk geometry that does NOT materially affect silhouette.

Do not simply decimate everything.

Preserve:

- trunk silhouette
- major branch silhouette
- important open-canopy branch structure
- crown-supporting branch forms

Remove / simplify:

- tiny branch tubes hidden inside foliage
- excessive radial segments
- excessive branch rings
- branches that are never visible
- very small secondary wood geometry


============================================================
WOOD TARGET
============================================================

For large broadleaf LOD0:

try to reduce wood contribution substantially.

Ideal production direction:

wood should no longer dominate ~70%+ of total tree triangles unless that tree's
visual identity genuinely requires exposed branches.

Do NOT target a percentage mechanically.

Visual silhouette is the priority.

A reasonable improvement target for Broadleaf_A would be approximately:

8,932 current total
→ roughly 6,000–7,500 total

IF quality remains equal or better.

Do not force this exact number.

Lower is acceptable.

Higher is acceptable if justified visually.


============================================================
STEP 04 — TRUNK RADIAL SEGMENTS
============================================================

Review trunk and major branch cross sections.

Do not use more radial segments than the gameplay silhouette needs.

Large trunk near camera:

enough to remain round

internal branches:

fewer segments

small branches:

very low radial count or remove completely

Avoid visible hexagonal trunks in close QA.


============================================================
STEP 05 — BRANCH LENGTH SEGMENTS
============================================================

Remove unnecessary longitudinal rings.

Use geometry only where:

- curvature changes
- taper changes
- branching changes

Do not subdivide straight branch segments repeatedly.


============================================================
STEP 06 — HIDDEN BRANCH REMOVAL
============================================================

Determine whether interior branches are visible from:

front
side
back
driver distance
chase distance

If a small branch is completely hidden by foliage from normal views:

remove or simplify it.

Do NOT remove important exposed branches from:

Broadleaf_C
or other intentionally open-canopy trees.


============================================================
STEP 07 — FOLIAGE CARD QUALITY
============================================================

Improve close-range foliage readability WITHOUT massively increasing card count.

Focus on:

- cluster orientation
- card size variation
- canopy depth
- edge breakup
- intersecting card patterns

Avoid visible repeated flat rectangles.


============================================================
STEP 08 — CARD ORIENTATION
============================================================

Review foliage cards from several camera angles.

Reduce obvious:

front-facing rectangle
side-on invisible card
repeated parallel card

patterns.

Use restrained orientation variation.

Do not scatter card angles randomly without regard to canopy form.


============================================================
STEP 09 — CANOPY LAYERING
============================================================

Use foliage in layers:

outer silhouette layer

middle canopy mass

limited interior depth

Do not fill the centre with excessive hidden alpha geometry.

Interior cards should exist only where they materially improve depth.


============================================================
STEP 10 — DARK INTERIOR / AO TERM
============================================================

Add a restrained canopy-interior shading/AO concept.

Goal:

give foliage depth.

Do NOT simply make interior foliage black.

Use either:

vertex colour
texture mask
material preview input

or another exportable/data-driven approach.

Preferred behavior:

outer leaves:
normal brightness

middle canopy:
slightly darker

deep canopy:
moderately darker

Keep subtle.


============================================================
UNITY COMPATIBILITY
============================================================

If adding exportable interior-shading data:

do NOT destroy WindData.

WindData already occupies vertex colours.

Therefore prefer:

- spare UV channel
- texture mask
- atlas variation channel

or another compatible data route.

Document exactly where this data lives.

Do not silently repurpose WindData channels.


============================================================
STEP 11 — LEAF COLOUR VARIATION
============================================================

Reduce the impression of one perfectly uniform foliage colour.

Use subtle variation between:

- canopy clusters
- heights
- species
- dry state

Variation should remain physically plausible.

Do not create spotted/noisy trees.


============================================================
STEP 12 — CONIFER POLISH
============================================================

Conifer_A and Conifer_B currently read:

too dark

too uniform.

Improve:

- internal value separation
- foliage-layer readability
- slight hue/value variation
- branch/canopy gap structure

Do not turn conifers bright lime green.


============================================================
CONIFER SILHOUETTE
============================================================

Ensure:

Conifer_A remains taller/narrower

Conifer_B remains broader/irregular

At:

25 m
50 m
100 m

they should remain distinguishable.


============================================================
STEP 13 — CONIFER CARD REVIEW
============================================================

Validation previously found one oversized conifer card.

Audit all conifer foliage cards.

Check:

- card dimensions
- alpha empty area
- overlapping transparency
- orientation

No single card should dominate an entire canopy zone.


============================================================
STEP 14 — ALPHA OVERDRAW REGRESSION
============================================================

Re-run alpha-card debug.

Compare BEFORE vs AFTER.

Target:

same or lower obvious overdraw.

Do not improve close-up appearance by doubling transparent geometry everywhere.


============================================================
STEP 15 — NORMAL REGRESSION
============================================================

A previous defect existed where custom normals exported without correct
rotation.

Do NOT reintroduce this.

Re-run:

custom-normal orientation validation

after all geometry changes.

Validate exported/re-imported normals.


============================================================
STEP 16 — WINDDATA REGRESSION
============================================================

Revalidate WindData after geometry regeneration.

Convention MUST remain:

R = branch bend

G = leaf flutter

B = phase

A = stiffness

Check:

trunk base

upper branch

leaf cards

grass

Values must remain logically correct.


============================================================
STEP 17 — LOD REGENERATION
============================================================

If LOD0 tree structure changes materially:

regenerate affected LOD1–LOD3 from the corrected species skeleton.

Do NOT leave old LODs with incompatible branch structure.


============================================================
LOD RULE
============================================================

Existing strategy remains:

LOD0:
close / premium

LOD1:
normal gameplay

LOD2:
medium distance/mobile

LOD3:
far mesh

Preserve:

height
width
crown identity
major gaps
trunk position


============================================================
STEP 18 — LOD2/LOD3 CANOPY ENVELOPE
============================================================

Current lower LOD canopies grow modestly wider than LOD0.

Review this.

Small enlargement to compensate for lost cards is acceptable.

But it must NOT produce visible tree expansion during LOD transition.

Target:

closer visual envelope agreement.

Do not force mathematically identical bounds if it hurts silhouette.


============================================================
STEP 19 — LOD POP QA
============================================================

Review transitions for at least:

Broadleaf_A

Broadleaf_C

Broadleaf_D

SmallRoadside_A

Conifer_A

Conifer_B

Inspect from likely gameplay distance.

Check:

- canopy size
- trunk thickness
- branch disappearance
- foliage density
- colour shift


============================================================
STEP 20 — QA SPECIES DISTRIBUTION
============================================================

The existing scatter QA under-represents Broadleaf_D.

Fix QA DISTRIBUTION ONLY.

Do NOT alter the production library just to change frequency.

Ensure the new QA environment contains meaningful samples of all 8 tree
archetypes.

Still use:

natural clustering.

Do NOT force equal grid distribution.


============================================================
STEP 21 — QA SCATTER MASK RULES
============================================================

Preserve existing successful placement constraints.

Must continue to respect:

TerrainBlend

VegetationMask UV1

road distance

prop corridor

rocks

retaining walls

slope


============================================================
STEP 22 — CLEARANCE REGRESSION
============================================================

Validate again:

no vegetation < required roadside exclusion

no tree crown over road

no vegetation clipping:

guardrails

streetlights

signs

gantries

CCTV

rocks

retaining walls


============================================================
STEP 23 — GROUND CONTACT
============================================================

Existing bases sit approximately 1–8 cm into terrain.

Keep natural contact.

No:

floating tree

deep buried trunk

floating shrub

grass hovering above ground


============================================================
STEP 24 — GRASS SCOPE
============================================================

Do NOT rebuild the grass system.

The current tuft look at QA density is expected.

Only fix a grass asset if there is an actual asset defect.

Unity later owns:

high density
GPU instancing
draw distance
culling


============================================================
STEP 25 — SHRUBS / WEEDS
============================================================

Do not redesign them unless a visible regression/problem is discovered.

This phase is primarily:

TREES
+
FOLIAGE QUALITY
+
LOD0 OPTIMIZATION
+
CONIFERS


============================================================
STEP 26 — REQUIRED BEFORE / AFTER RENDERS
============================================================

Create:

previews/03A_before_broadleaf_A.png
previews/03A_after_broadleaf_A.png

previews/03A_before_conifer_A.png
previews/03A_after_conifer_A.png

previews/03A_before_tree_library.png
previews/03A_after_tree_library.png

previews/03A_before_chase.png
previews/03A_after_chase.png


============================================================
STEP 27 — REQUIRED NEW QA RENDERS
============================================================

Create:

previews/03A_broadleaf_close.png

previews/03A_broadleaf_25m.png

previews/03A_broadleaf_50m.png

previews/03A_broadleaf_100m.png

previews/03A_conifer_library.png

previews/03A_tree_LODs.png

previews/03A_alpha_overdraw.png

previews/03A_driver_view.png

previews/03A_chase_view.png

previews/03A_high_chase.png

previews/03A_full_environment.png


============================================================
STEP 28 — VISUAL ACCEPTANCE GATES
============================================================

Do NOT rely only on automated tests.

Actually inspect renders.

A. WOOD

Large broadleaf trees should no longer feel overbuilt with hidden branch tubes.

B. FOLIAGE

Close foliage should read more as clustered canopy mass and less as obvious
individual rectangles.

C. DEPTH

Canopy should have believable interior depth.

No black cavity.

D. CONIFERS

Conifers should no longer read as one dark uniform mass.

E. LOD

Transitions must not dramatically expand/shrink the canopy.

F. REPETITION

QA environment must demonstrate all main archetypes sufficiently to evaluate
repetition.


============================================================
STEP 29 — PERFORMANCE PRINCIPLE
============================================================

This is a Blender optimization pass.

Do not chase ultra-low triangle counts at the cost of tree quality.

But remove geometry that provides no visible benefit.

Target:

better visual quality per triangle.


============================================================
STEP 30 — UPDATED GEOMETRY REPORT
============================================================

Create:

reports/P1_vegetation_03A_geometry_delta.json

For each changed tree include:

BEFORE:

total tris
wood tris
foliage tris

AFTER:

total tris
wood tris
foliage tris

And:

percentage reduction

Do not count a reduction as success if the silhouette became worse.


============================================================
STEP 31 — CHECKPOINTS
============================================================

Work in:

blend/vegetation_08_lod0_polish.blend

After approval create:

blend/vegetation_09_final_frozen.blend


============================================================
STEP 32 — EXPORT
============================================================

Export using the SAME existing file names:

vegetation_complete.fbx

Trees_Broadleaf.fbx

Trees_Small.fbx

Trees_Conifer.fbx

Shrubs.fbx

Grass.fbx

Weeds.fbx

Vegetation_CollisionOptional.fbx

Do not change file naming unnecessarily.


============================================================
ARCHIVE PREVIOUS EXPORT
============================================================

Before replacing current final exports:

archive them under:

exports/_pre_03A/

Do not destroy the previously validated set.


============================================================
STEP 33 — FBX RE-IMPORT
============================================================

MANDATORY.

Re-import all 8 FBXs into a clean Blender scene.

Validate:

- scale
- dimensions
- +Y Unity up
- +Z Unity forward
- hierarchy
- names
- materials
- UVs
- custom normals
- WindData
- LODs
- colliders
- triangle counts

Target:

0 errors.


============================================================
STEP 34 — VALIDATION
============================================================

Create:

reports/P1_vegetation_03A_validation.txt

Re-run all important P1-BLENDER-03 validation.

Add specific checks for:

- wood geometry audit
- oversized foliage cards
- custom normal orientation
- foliage interior shading channel
- LOD envelope
- Broadleaf_D QA presence
- conifer value variation

Target:

0 errors
0 critical warnings.


============================================================
STEP 35 — SOURCE INTEGRITY
============================================================

Verify AGAIN:

P0 Road Foundation unchanged

P1 Props unchanged

P1 Terrain unchanged

Cars unchanged

Also verify original vegetation checkpoints:

vegetation_01 through vegetation_07

are unchanged.

Create:

reports/P1_vegetation_03A_source_integrity_check.md


============================================================
STEP 36 — UNITY TRANSFER UPDATE
============================================================

Update:

environment/P1_Vegetation/UnityTransfer/

with ONLY final polished production files.

Preserve directory structure.

Update:

README/VEGETATION_IMPORT_NOTES.md

Document:

- P1-BLENDER-03A applied
- wood reduction
- foliage depth changes
- conifer changes
- new interior-shading data if any
- updated triangle counts
- LOD changes


============================================================
STEP 37 — WIND GUIDE UPDATE
============================================================

If WindData remains unchanged:

state explicitly:

WindData convention unchanged.

If any geometry regeneration affected values:

document revalidation.

Do NOT change semantics.


============================================================
STEP 38 — FINAL FREEZE
============================================================

Create:

reports/P1_vegetation_FINAL_FREEZE_03A.md

Include:

- final blend
- final FBXs
- final texture set
- UnityTransfer path
- validation result
- important hashes
- remaining limitations

Then treat:

environment/P1_Vegetation/

as FINAL/FROZEN.


============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P1-BLENDER-03A COMPLETE UNTIL:

1. P0 remains unchanged.
2. Props remain unchanged.
3. Terrain remains unchanged.
4. Cars remain unchanged.
5. Vegetation 01–07 checkpoints remain unchanged.
6. Wood geometry audit exists.
7. Hidden/unnecessary branch geometry is reduced.
8. Broadleaf silhouettes remain correct.
9. Open-canopy trees retain important branches.
10. Foliage card readability improves.
11. Alpha overdraw does not regress significantly.
12. Canopy interior depth improves.
13. WindData semantics remain correct.
14. Custom normals revalidate.
15. Conifer darkness improves.
16. Conifer variation improves.
17. No oversized conifer cards remain.
18. LOD chains regenerate where necessary.
19. LOD envelope transitions are acceptable.
20. Broadleaf_D is adequately represented in QA.
21. Terrain masks still work.
22. Prop clearance still works.
23. Ground contact still works.
24. Driver-view QA passes.
25. Chase-view QA passes.
26. High-chase QA passes.
27. Before/after renders exist.
28. Geometry delta report exists.
29. All 8 FBXs export.
30. All 8 FBXs re-import.
31. Validation reports 0 errors.
32. UnityTransfer is updated.
33. Import notes are updated.
34. Final freeze report exists.


============================================================
FINAL REPORT
============================================================

Return ONE complete report containing:

1. baseline integrity
2. visual defects confirmed
3. tree wood audit
4. Broadleaf_A before/after triangles
5. other tree geometry changes
6. branches removed/simplified
7. foliage-card changes
8. canopy-depth implementation
9. conifer improvements
10. WindData regression result
11. normal regression result
12. alpha-overdraw result
13. LOD changes
14. LOD-envelope QA
15. species-distribution QA
16. terrain-mask QA
17. prop-clearance QA
18. ground-contact QA
19. before/after previews
20. driver/chase previews
21. final checkpoint
22. FBX paths
23. re-import result
24. validation result
25. UnityTransfer path
26. source-integrity status
27. remaining limitations
28. recommended next Blender phase


============================================================
STOP CONDITION
============================================================

After P1-BLENDER-03A is complete:

STOP.

DO NOT START:

- Tunnel
- City
- Bridge
- Mountain/coastal
- Traffic
- Player-car rebuilding
- Unity integration
- Unity vegetation shader
- Unity scatter system

Do not modify:

P0 Road

P1 Props

P1 Terrain

finished vehicles

Do not install or launch Unity.

POLISH ONLY THE EXISTING VEGETATION SYSTEM,
OPTIMIZE TREE LOD0 GEOMETRY,
IMPROVE FOLIAGE DEPTH AND CONIFERS,
REVALIDATE,
RE-EXPORT,
UPDATE THE TRANSFER PACKAGE,
FREEZE,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P1-BLENDER-03A — documentation-only closure
====================================================================================================

````text
P1-BLENDER-03A asset work is accepted.

Do NOT modify any vegetation asset, texture, FBX, LOD, source checkpoint,
frozen upstream source, or UnityTransfer production file.

Perform documentation-only closure.

Using the existing evidence:

- reports/P1_vegetation_03A_validation.txt
- reports/P1_vegetation_03A_geometry_delta.json
- reports/P1_vegetation_wood_geometry_audit.json
- reports/P1_vegetation_03A_visual_baseline.md
- reports/P1_vegetation_03A_source_integrity.md
- reports/P1_vegetation_FINAL_FREEZE_03A.md

create:

reports/P1_vegetation_03A_FINAL_REPORT.md

The report must consolidate these 28 items:

1. baseline integrity
2. visual defects confirmed
3. tree wood audit
4. Broadleaf_A before/after triangles
5. other tree geometry changes
6. branches removed/simplified
7. foliage-card changes
8. canopy-depth implementation
9. conifer improvements
10. WindData regression result
11. custom-normal regression result
12. alpha-overdraw result
13. LOD changes
14. LOD-envelope QA
15. species-distribution QA
16. terrain-mask QA
17. prop-clearance QA
18. ground-contact QA
19. before/after previews
20. driver/chase previews
21. final checkpoint
22. FBX paths
23. FBX re-import result
24. validation result
25. UnityTransfer path
26. source-integrity status
27. remaining limitations
28. recommended next Blender phase

Important:
- Do not invent missing evidence.
- Do not rerender anything.
- Do not regenerate anything.
- State that the close-up and 25/50/100 m images are standalone AFTER/QA
  renders and were not required before/after pairs.
- State that the approved re-import dimensional tolerance is 6 mm and why.
- Confirm that vegetation_01 through vegetation_07 remain unchanged.
- Confirm vegetation_09_final_frozen.blend is the final source.
- Confirm P1_Vegetation remains FROZEN.

After creating the report:

STOP.

Do not begin Tunnel or any other phase.
````


====================================================================================================
# SPEC: P1-BLENDER-04 — Premium Modular Tunnel & Highway Structures
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Hard-Surface Artist, Infrastructure Artist and Real-Time Optimization
Specialist with 10+ years of production experience creating tunnels,
highways and streamed racing environments.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

DO NOT:

- search for Unity
- install Unity
- launch Unity
- create Unity prefabs
- create Unity shaders
- create Unity scripts
- modify RoadStreamer
- modify gameplay
- modify completed road assets
- modify completed props
- modify completed terrain
- modify completed vegetation
- modify vehicle assets
- start City
- start Bridge/Overpass
- start Mountain/Coastal

Your responsibility is:

P1-BLENDER-04 — PREMIUM MODULAR TUNNEL & HIGHWAY STRUCTURES SYSTEM

Complete:

DISCOVERY
→ SOURCE INTEGRITY BASELINE
→ READ-ONLY REFERENCE LINKING
→ TUNNEL DIMENSION STUDY
→ TUNNEL BLOCKOUT
→ 40 M MODULAR SHELL
→ 20 M SUPPORT MODULE
→ PORTALS
→ ENTRY / EXIT TRANSITIONS
→ WALL / CEILING SYSTEM
→ SAFETY / SERVICE FEATURES
→ VENTILATION
→ LIGHT FIXTURES
→ TUNNEL SIGNS / MARKINGS SUPPORT
→ EMERGENCY BAYS
→ DRAINAGE
→ MATERIAL / TRIM SYSTEM
→ UVs
→ LODs
→ COLLIDERS
→ SNAP POINTS
→ LONG QA ASSEMBLY
→ LIGHT / DARK PREVIEWS
→ FBX EXPORT
→ FBX RE-IMPORT VALIDATION
→ UNITY TRANSFER PACKAGE
→ FINAL REPORT
→ FREEZE
→ STOP


============================================================
CURRENT WORKSPACE
============================================================

Main workspace:

/Users/meetshah/Documents/blender

Completed and FROZEN:

environment/P0_RoadFoundation/

environment/P1_Props/

environment/P1_Terrain/

environment/P1_Vegetation/

Finished vehicle folders are also FROZEN.

Final terrain source:

environment/P1_Terrain/blend/terrain_09_final_frozen.blend

Final vegetation source:

environment/P1_Vegetation/blend/vegetation_09_final_frozen.blend


============================================================
CRITICAL FREEZE RULE
============================================================

DO NOT MODIFY:

P0 Road Foundation

P1 Props

P1 Terrain

P1 Vegetation

Cars

Use them ONLY as LINKED / READ-ONLY references.

If the tunnel design exposes a problem in a frozen phase:

DOCUMENT IT.

Do NOT edit the frozen source to make Tunnel easier.


============================================================
ROAD ARCHITECTURE — HARD CONSTRAINT
============================================================

The game's RoadStreamer uses:

STRAIGHT

LEVEL

approximately 40 m streamed chunks.

Do NOT create:

- curved tunnel road
- climbing road
- descending road
- junction road
- tunnel forks
- spline-dependent tunnel modules

unless only as non-runtime concept/reference.

The actual road remains:

STRAIGHT
LEVEL
40 M MODULAR


============================================================
KNOWN ROAD DIMENSIONS
============================================================

Road module:

40.000 m

Secondary:

20.000 m

4 lanes:

4 × 3.60 m

Carriageway:

14.40 m

Road kit including edge strips:

15.40 m

Outer/right shoulder:

3.00 m

Inner/median-side shoulder:

1.50 m

Road crown:

approximately +36 mm

Unity target:

+Y up
+Z forward

Blender:

+Z up
road direction -Y


============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P1_Tunnel/

Use:

P1_Tunnel/
├── blend/
├── exports/
├── textures/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/


============================================================
PRIMARY GOAL
============================================================

The existing tunnel was previously identified as one of the weakest visual
areas.

Create a modern premium highway tunnel suitable for:

- high-speed racing gameplay
- Day → Tunnel → Day transitions
- Night driving
- Wet / rainy road
- Mobile scalability
- PC premium rendering

The tunnel must feel like a real engineered highway structure, not:

- a dark tube
- a rectangular box
- a repeated grey corridor
- an empty cave
- a brightly glowing sci-fi tunnel


============================================================
DESIGN LANGUAGE
============================================================

Target:

MODERN HIGHWAY ROAD TUNNEL

Use believable:

- concrete
- wall panels
- structural joints
- service features
- drainage
- lighting
- ventilation
- signage
- emergency infrastructure

Keep design broadly international / generic.

Do not copy branding or exact proprietary tunnel design.


============================================================
TUNNEL CROSS SECTION
============================================================

Design the tunnel around the EXISTING frozen road.

Do not narrow or reshape the road.

Provide enough interior clearance for:

- 4-lane road
- shoulders
- barriers
- signs
- service access
- wall lighting
- ceiling systems

Suggested starting interior dimensions:

clear usable width:
approximately 22–26 m

clear driving height:
minimum approximately 5.5–6.0 m

ceiling crown:
approximately 7–9 m depending on final profile

These are starting guidance.

Measure linked P0 road and refine realistically.


============================================================
TUNNEL PROFILE
============================================================

Prefer a believable modern tunnel profile such as:

- gently arched ceiling
- segmented arch
- broad curved crown with vertical lower walls

Avoid:

perfect rectangle

and

perfect circular pipe

unless justified.

The profile should read clearly from chase camera.


============================================================
PHASE 01 — DISCOVERY
============================================================

Link read-only:

P0 road

P1 props where useful

P1 terrain

P1 vegetation

Optional lightweight car for scale.

Measure:

- road width
- shoulder width
- barrier position
- vehicle height
- chase-camera height
- tunnel-required clearances

Create:

reports/P1_tunnel_discovery.md

Document:

- chosen interior width
- chosen height
- portal dimensions
- structural rhythm
- module length
- light spacing
- wall-panel rhythm
- emergency-bay spacing concept
- ventilation concept
- material strategy
- LOD strategy


============================================================
SOURCE INTEGRITY BASELINE
============================================================

Before work:

hash frozen source directories.

Create:

reports/P1_tunnel_source_baseline.json

At completion verify everything upstream remains byte-for-byte unchanged.


============================================================
TUNNEL MODULE SYSTEM
============================================================

Create at minimum:

Tunnel_Straight_40m

Tunnel_Straight_20m

Tunnel_Entry_40m

Tunnel_Exit_40m

Tunnel_Portal_Entry

Tunnel_Portal_Exit

Tunnel_ServiceBay_40m

Tunnel_EmergencyBay_40m

Tunnel_Ventilation_40m

Tunnel_DarkVariant_40m

Do not make every variant completely different.

Use a shared modular shell.


============================================================
40 M MODULE RULE
============================================================

Tunnel_Straight_40m must align exactly with:

P0 Road_4Lane_40m

Snap_Start

to

Snap_End

Distance:

40.000 m


============================================================
20 M MODULE
============================================================

Create:

Tunnel_Straight_20m

for future composition / transitions.

Distance:

20.000 m


============================================================
SEAM-SAFE STRUCTURAL RHYTHM
============================================================

Tunnel details must align across module boundaries.

Examples:

wall panel joints

ceiling ribs

cable trays

drainage

lighting support tracks

Do not place half-finished structural details across snap boundaries unless
they continue correctly.


============================================================
STRUCTURAL BAY RHYTHM
============================================================

Use a repeated engineering rhythm.

Example:

4 m

5 m

or

8 m

structural bays.

Choose a system that divides logically into 40 m.

Recommended:

5 m or 8 m rhythm.

Document the final decision.


============================================================
TUNNEL SHELL
============================================================

Create:

TunnelShell_40m_LOD0

and useful lower LODs if needed.

Shell should include:

- lower wall
- upper wall
- ceiling/arch
- structural seams
- major reinforcement ribs only where visually justified

Do not model every concrete pore or tiny joint.


============================================================
WALL PANEL SYSTEM
============================================================

Create reusable wall parts:

TunnelWall_Panel_A

TunnelWall_Panel_B

TunnelWall_LowerPanel

TunnelWall_ServicePanel

TunnelWall_EndTrim

TunnelWall_DirtyVariant

Use texture / trim detail for:

- small joints
- bolts
- stains
- fine cracks


============================================================
LOWER WALL / SAFETY ZONE
============================================================

Create clear separation between:

road

barrier

lower wall

service/walk zone

Use realistic wall protection / service ledge if appropriate.


============================================================
TUNNEL BARRIER SYSTEM
============================================================

Prefer reuse/reference compatibility with P0/P1 concrete barrier assets.

Do NOT modify P0/P1 barrier source.

If Tunnel genuinely needs a unique wall-integrated barrier:

create a Tunnel-specific variant.

Name clearly.


============================================================
PORTAL SYSTEM
============================================================

Create premium tunnel portals.

Required:

Tunnel_Portal_Entry

Tunnel_Portal_Exit

Tunnel_PortalWing_L

Tunnel_PortalWing_R

Tunnel_PortalTop

Tunnel_PortalRetaining_L

Tunnel_PortalRetaining_R

Portal must integrate visually with P1 Terrain.

Do not modify terrain.

Tunnel portal should appear cut into terrain / hillside naturally.


============================================================
PORTAL SILHOUETTE
============================================================

The portal is an important landmark.

It should be readable at:

100 m

200 m

300 m

without excessive geometry.


============================================================
PORTAL DETAIL
============================================================

Include useful large forms:

- concrete opening frame
- retaining wings
- drainage edge
- signage support
- service area
- lighting mounting area

Use textures for small detail.


============================================================
ENTRY TRANSITION
============================================================

Create:

Tunnel_Entry_40m

The transition should visually move from:

open highway
→ portal
→ partially enclosed
→ full tunnel

This is geometry/art transition only.

Do NOT create Unity exposure logic.


============================================================
EXIT TRANSITION
============================================================

Create:

Tunnel_Exit_40m

Allow:

full tunnel
→ bright portal opening
→ open highway

Do not bake final exposure into materials.


============================================================
LIGHT FIXTURE LIBRARY
============================================================

Create tunnel-specific light fixtures.

Required:

TunnelLight_Linear

TunnelLight_Linear_Double

TunnelLight_Wall

TunnelLight_Emergency

TunnelLight_EntranceBoost

Optional:

TunnelLight_Inspection

Do not create Unity Light components.

Geometry + emissive-source material only.


============================================================
LIGHT SPACING
============================================================

Use believable rhythm.

Example:

linear fixtures every 5–10 m

Entrance zone may use denser fixtures.

Avoid:

one light every metre

or

huge empty dark stretches

unless intentionally designed.


============================================================
LIGHTING CHANNELS / MATERIALS
============================================================

Prepare shared source materials such as:

MAT_Tunnel_Light_White

MAT_Tunnel_Light_Emergency

These are Blender preview materials.

Unity later owns:

actual emissive intensity

real lights

quality tiers

shadows

exposure


============================================================
VENTILATION SYSTEM
============================================================

Create:

Tunnel_JetFan

Tunnel_JetFan_DoubleMount

Tunnel_Vent_Duct_A

Tunnel_Vent_Grille

Tunnel_FanSupport

Use realistic large tunnel jet fans.

Do not make them sci-fi turbines.


============================================================
JET FAN SCALE
============================================================

Typical visual target:

approximately 1–1.5 m diameter

depending on tunnel profile.

Check against car and ceiling.


============================================================
JET FAN DETAIL
============================================================

Geometry for:

- outer housing
- central fan body
- visible blades if useful
- support brackets

Texture/normal for:

- bolts
- fine grille detail
- labels


============================================================
CABLE / SERVICE INFRASTRUCTURE
============================================================

Create:

Tunnel_CableTray_4m

Tunnel_CableTray_8m

Tunnel_UtilityConduit_A

Tunnel_ServiceBox_A

Tunnel_ServiceBox_B

Use modular reuse.


============================================================
EMERGENCY BAY
============================================================

Create:

Tunnel_EmergencyBay_40m

Include believable widened / recessed infrastructure where practical.

Assets:

Tunnel_EmergencyDoor

Tunnel_EmergencyPhone

Tunnel_FireCabinet

Tunnel_SOS_Sign

Tunnel_EmergencyLight

Do not make the bay so large that it changes road gameplay.


============================================================
SERVICE DOORS
============================================================

Create:

Tunnel_ServiceDoor_A

Tunnel_ServiceDoor_B

Include:

frame
door
handle
warning plate area

Fine detail through texture.


============================================================
FIRE / SAFETY CABINET
============================================================

Create:

Tunnel_FireCabinet_A

Could include:

cabinet
hose/reel hint
extinguisher silhouette

Do not over-model interiors.


============================================================
SIGNAGE SUPPORT
============================================================

Create tunnel-safe supports for:

speed sign

lane sign

emergency exit sign

direction sign

VMS

Prefer compatibility with P1 Props sign assets.

Do not duplicate entire P1 sign library unless tunnel mounting requires it.


============================================================
OVERHEAD SIGN SUPPORT
============================================================

Create:

Tunnel_OverheadSignFrame

Tunnel_VMS_Frame

Keep enough road clearance.


============================================================
LANE CONTROL SIGNALS
============================================================

Create:

Tunnel_LaneSignal_Frame

Optional source faces:

green arrow

red X

These can later become Unity emissive materials.


============================================================
DRAINAGE
============================================================

Tunnel needs its own edge drainage integration.

Create:

Tunnel_Drain_Channel

Tunnel_Drain_Grate_4m

Tunnel_Drain_Grate_8m

Tunnel_Drain_Access

Keep geometry efficient.


============================================================
DRAINAGE LODS
============================================================

Repeated drainage can become expensive.

Provide useful low-detail versions.

Do not keep detailed grates at long distance.


============================================================
WALL RECESSES
============================================================

Create limited modular recesses:

Tunnel_Recess_A

Tunnel_Recess_B

Use them for:

- emergency equipment
- utility
- ventilation
- visual rhythm

Do not recess every 2 metres.


============================================================
CEILING SYSTEM
============================================================

Create believable ceiling detail.

Potential:

- segmented concrete
- suspended utilities
- light tracks
- fan mounts
- cable runs

Do not fill ceiling with unnecessary geometry.


============================================================
TUNNEL MATERIAL SYSTEM
============================================================

Create source materials:

MAT_Tunnel_Concrete

MAT_Tunnel_Concrete_Dark

MAT_Tunnel_WallPanel

MAT_Tunnel_Metal

MAT_Tunnel_Galvanized

MAT_Tunnel_Rubber

MAT_Tunnel_Light

MAT_Tunnel_Sign

MAT_Tunnel_Drain

Keep shared material count reasonable.


============================================================
TRIM SHEET
============================================================

Create shared:

T_Tunnel_Trim_2K

Preferred channels:

BaseColor

Normal

Roughness

Metallic

AO

Potential regions:

clean concrete edge

dirty concrete

painted wall panel

galvanized metal

black rubber

service door

utility metal

sign frame

Do not create one texture per tunnel object.


============================================================
CONCRETE TEXTURE
============================================================

Create or reuse:

T_Tunnel_Concrete_2K

Tileable.

Maps:

BaseColor

Normal

Roughness

AO

Use restrained staining.

Do not make every surface heavily damaged.


============================================================
TUNNEL DIRT / WEAR
============================================================

Use believable concentration:

lower wall:
more dirt

near drains:
more grime

ceiling:
subtle soot / darkening

portal:
weathering

Avoid uniform procedural dirt everywhere.


============================================================
WATER / WETNESS SOURCE SUPPORT
============================================================

Prepare materials/textures so Unity can later add:

wetness

leaks

road reflection

Do not create Blender-only wet material dependence.


============================================================
DECALS
============================================================

Optional reusable tunnel decals:

Tunnel_LeakStain_A

Tunnel_LeakStain_B

Tunnel_WallGrime_A

Tunnel_RepairPatch_A

Tunnel_Soot_A

Keep separate / reusable.

Do not bake every stain into geometry.


============================================================
UV STRATEGY
============================================================

Use consistent world-scale UVs.

Long tunnel surfaces must tile.

Do NOT stretch one 0–1 texture over 40 m.


============================================================
TEXEL DENSITY
============================================================

Keep compatible with previous environment assets where practical.

Document:

metres per tile

for:

concrete

wall panels

trim sheet


============================================================
VERTEX DATA
============================================================

If useful, add a documented vertex layer such as:

TunnelWear

for:

dirt
wetness
soot
grime

Only do this if it has a clear Unity-side use.

Do not add undocumented data.


============================================================
LOD STRATEGY
============================================================

Create LODs where they matter:

portal

jet fans

light fixtures

sign frames

service equipment

drain grates

large wall detail assemblies

Do not create pointless LODs for simple tunnel planes.


============================================================
TRIANGLE GUIDANCE
============================================================

Use budgets as guidance, not quotas.

40 m tunnel shell:

LOD0:
approximately 5k–15k tris

LOD1:
~40–60%

LOD2:
~15–30%

Portal assembly:

LOD0:
approximately 8k–20k depending on silhouette

Jet fan:

LOD0:
1k–3k

Light fixture:

LOD0:
100–500

Service props:
as low as practical

Do NOT pad geometry.


============================================================
COLLISION
============================================================

Road collision remains from P0.

Tunnel collision should cover:

walls

barriers

portal structures

service obstacles if needed

Use simple collider meshes.

Do NOT use full tunnel visual mesh as collider if avoidable.


============================================================
COLLIDER ASSETS
============================================================

Create approximately:

Collision_TunnelWall_L_40m

Collision_TunnelWall_R_40m

Collision_TunnelPortal

Collision_TunnelBarrier

Collision_ServiceBay

Keep low-poly.


============================================================
NO CEILING COLLISION UNLESS NEEDED
============================================================

If gameplay vehicle cannot reach ceiling:

do not build overly detailed ceiling collision.


============================================================
SNAP POINTS
============================================================

Every runtime module must include:

Snap_Start

Snap_End

40 m:

exact 40.000 m

20 m:

exact 20.000 m


============================================================
PORTAL ALIGNMENT POINTS
============================================================

Add documented reference empties if useful:

RoadCenter

PortalFace

TunnelCenter

CeilingClearance

WallInner_L

WallInner_R


============================================================
TUNNEL QA ASSEMBLY
============================================================

Create approximately:

320–480 m

temporary tunnel QA sequence.

Example:

Open Road
→ Portal
→ Entry
→ Straight
→ Straight
→ Ventilation
→ Emergency Bay
→ Straight
→ Exit
→ Open Road

Use LINKED P0 road.

Do not duplicate P0 road into exports.


============================================================
QA MUST USE REAL ROAD
============================================================

Link the actual P0 Road Foundation.

Do not create a fake replacement floor.


============================================================
PROP REFERENCES
============================================================

Use P1 Props read-only where useful:

signs

barriers

VMS

Do not export linked P1 assets in Tunnel FBXs.


============================================================
CAR SCALE QA
============================================================

Optionally link Hypercar at:

road centre

lane centre

Check:

- ceiling clearance
- wall clearance
- portal scale
- service objects
- light height


============================================================
DRIVER CAMERA QA
============================================================

Capture from:

driver height

Check:

tunnel should not feel:

too low

too wide

too narrow

too empty


============================================================
CHASE CAMERA QA
============================================================

Use:

low chase

high chase

Check structural rhythm at speed.


============================================================
PORTAL APPROACH QA
============================================================

View portal from approximately:

50 m

100 m

200 m

300 m

It must remain readable as a strong landmark.


============================================================
NIGHT / DARK QA
============================================================

Create Blender-only preview of tunnel lighting.

Important:

these are NOT final Unity light values.

Use only to inspect:

- fixture rhythm
- ceiling readability
- emergency accents
- wall readability
- silhouette


============================================================
DAY ENTRY QA
============================================================

Render:

bright exterior
→ darker tunnel interior

Do not fake final Unity exposure.

Just verify geometry/material readability.


============================================================
EXIT QA
============================================================

Check sightline toward bright exit.

Avoid geometry blocking road view.


============================================================
WET QA
============================================================

Optional Blender preview:

slightly wet tunnel road/reference

Do NOT modify P0 road material/source.

Use preview-only approach.


============================================================
REQUIRED PREVIEWS
============================================================

Create at minimum:

previews/P1_tunnel_portal_front.png

previews/P1_tunnel_portal_100m.png

previews/P1_tunnel_entry.png

previews/P1_tunnel_straight.png

previews/P1_tunnel_driver_view.png

previews/P1_tunnel_chase_view.png

previews/P1_tunnel_high_chase.png

previews/P1_tunnel_wall_detail.png

previews/P1_tunnel_ceiling.png

previews/P1_tunnel_ventilation.png

previews/P1_tunnel_emergency_bay.png

previews/P1_tunnel_drainage.png

previews/P1_tunnel_night.png

previews/P1_tunnel_exit.png

previews/P1_tunnel_full_sequence.png

previews/P1_tunnel_asset_library.png


============================================================
VISUAL HARD GATES
============================================================

A. SCALE

Tunnel must feel realistically sized around cars and road.

B. REPETITION

40 m modules must not make every 40 m visually identical.

C. STRUCTURE

Tunnel must read as engineered infrastructure.

D. PORTAL

Portal must look like a premium landmark.

E. EMPTY SPACE

Tunnel must not read as an empty concrete box.

F. CLUTTER

Tunnel must also not become overloaded with props.

G. CEILING

Ceiling needs readable structure.

H. LIGHT RHYTHM

Fixtures must form believable rhythm.

I. GAMEPLAY VISIBILITY

Road and lanes must remain readable.


============================================================
CHECKPOINT FILES
============================================================

Create:

blend/tunnel_01_blockout.blend

blend/tunnel_02_shell_portal.blend

blend/tunnel_03_structures.blend

blend/tunnel_04_service_safety.blend

blend/tunnel_05_materials_uv.blend

blend/tunnel_06_lods_collision.blend

blend/tunnel_07_export_ready.blend

Never overwrite earlier checkpoints.


============================================================
COLLECTIONS
============================================================

Use:

TUNNEL_MASTER

TUNNEL_SHELL

TUNNEL_PORTALS

TUNNEL_WALLS

TUNNEL_CEILING

TUNNEL_LIGHTS

TUNNEL_VENTILATION

TUNNEL_SERVICE

TUNNEL_SAFETY

TUNNEL_DRAINAGE

TUNNEL_SIGNS

TUNNEL_COLLIDERS

TUNNEL_QA

TUNNEL_PRESENTATION


============================================================
TRANSFORMS
============================================================

Production assets:

Scale:
1,1,1

No negative scale.

Clean rotations.

Apply transforms where safe.


============================================================
ORIGINS
============================================================

Tunnel modules:

consistent road-centre/start origin

Portal:

road-centre / base reference

Props:

ground/mounting point

Lights:

fixture mounting point

Fans:

mount centre or documented pivot


============================================================
NORMALS
============================================================

Concrete shell:

smooth where curved

hard where structural

Do not oversmooth wall-panel seams.

Metal fixtures:

clean shading.


============================================================
AUTOMATION
============================================================

Store scripts under:

scripts/

Suggested:

tunnel_build.py

tunnel_materials.py

tunnel_lods.py

tunnel_validate.py

tunnel_render.py

tunnel_export.py


============================================================
FBX EXPORT ORIENTATION
============================================================

Use same proven Blender → Unity workflow as:

Hypercar

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

Target Unity:

+Y up
+Z forward

Reuse proven axis conversion.

Do NOT blindly change Apply Transform settings.


============================================================
FBX EXPORTS
============================================================

Create:

exports/tunnel_complete.fbx

and logical split files such as:

exports/Tunnel_Shell.fbx

exports/Tunnel_Portals.fbx

exports/Tunnel_Structures.fbx

exports/Tunnel_Lights.fbx

exports/Tunnel_Ventilation.fbx

exports/Tunnel_ServiceSafety.fbx

exports/Tunnel_Drainage.fbx

exports/Tunnel_Collision.fbx

Use 8–10 logical files if appropriate.

Do not create dozens of tiny FBXs without reason.


============================================================
EXPORT EXCLUSIONS
============================================================

DO NOT EXPORT:

P0 road

P1 props

terrain

vegetation

cars

QA sequence

cameras

Blender preview lights

presentation background

temporary helpers


============================================================
TEXTURE OUTPUT
============================================================

Store:

textures/concrete/

textures/trim/

textures/metal/

textures/decals/

textures/signs/

Do not duplicate frozen source textures unnecessarily.


============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

Re-import EVERY FBX into a clean Blender scene.

Validate:

- orientation
- +Y Unity up
- +Z Unity forward
- scale
- dimensions
- 40 m module length
- 20 m module length
- snap points
- hierarchy
- names
- pivots
- UVs
- materials
- LODs
- colliders
- triangle counts
- normals

Target:

0 errors.


============================================================
VALIDATION REPORT
============================================================

Create:

reports/P1_tunnel_validation.txt

Check at minimum:

1. required modules exist
2. 40 m dimensions
3. 20 m dimensions
4. snap distance
5. tunnel interior width
6. height clearance
7. portal alignment
8. road clearance
9. wall clearance
10. ceiling clearance
11. module seams
12. materials
13. trim textures
14. UVs
15. LODs
16. colliders
17. pivots
18. transforms
19. normals
20. naming
21. export selection
22. re-import
23. frozen-source integrity

Target:

0 errors

0 critical warnings.

Do not warn because an asset is below triangle budget.


============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P1_tunnel_geometry.json

For each asset include:

- name
- category
- dimensions
- LOD
- triangles
- vertices
- materials
- UV status
- collider
- snap references


============================================================
MATERIAL REPORT
============================================================

Create:

reports/P1_tunnel_materials.md

Document:

- material list
- trim-sheet layout
- concrete texture
- texel density
- metres per tile
- decal strategy
- emissive-source materials
- Unity expectations


============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P1_tunnel_export_manifest.json

Include:

- FBXs
- source blend
- included objects
- excluded QA objects
- materials
- textures
- LODs
- colliders
- coordinate conversion
- snap conventions


============================================================
SOURCE INTEGRITY CHECK
============================================================

At completion verify:

P0 Road unchanged

P1 Props unchanged

P1 Terrain unchanged

P1 Vegetation unchanged

Cars unchanged

Create:

reports/P1_tunnel_source_integrity_check.md

Target:

BYTE-FOR-BYTE UNCHANGED.


============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

UnityTransfer/

Structure:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/


============================================================
UNITY IMPORT NOTES
============================================================

Create:

UnityTransfer/README/TUNNEL_IMPORT_NOTES.md

Document:

1. source phase
2. Unity orientation
3. scale
4. road relationship
5. 40 m module convention
6. 20 m convention
7. portal dimensions
8. tunnel interior dimensions
9. FBX list
10. LOD naming
11. material names
12. trim sheet
13. texture channels
14. emissive source materials
15. light fixture spacing
16. ventilation assets
17. safety assets
18. drainage
19. collider strategy
20. snap points
21. excluded QA assets
22. expected RoadStreamer usage

State clearly:

THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.

UNITY-SIDE:

TUNNEL MATERIALS

REAL LIGHTS

EMISSIVE INTENSITY

REFLECTION PROBES

EXPOSURE TRANSITION

FOG

ROADSTREAMER INTEGRATION

LODGroup COMPONENTS

CULLING

QUALITY TIERS

AND PERFORMANCE TESTING

MUST BE COMPLETED ON THE UNITY WORKSTATION.


============================================================
TUNNEL LIGHTING GUIDE
============================================================

Create:

UnityTransfer/README/TUNNEL_LIGHTING_GUIDE.md

Document:

- fixture families
- intended spacing
- entrance boost fixtures
- standard fixtures
- emergency fixtures
- expected emissive surfaces
- recommended Unity-side distinction between real lights and emissive-only
- mobile scalability concept

Do NOT prescribe exact final lumen values unless supported by real Unity tests.


============================================================
ROADSTREAMER GUIDE
============================================================

Create:

UnityTransfer/README/TUNNEL_STREAMING_GUIDE.md

Document:

- 40 m chunk assumptions
- entry module
- straight module
- special module
- exit module
- snap convention
- which assets are optional
- what must not be duplicated
- recommended runtime composition


============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P1-BLENDER-04 COMPLETE UNTIL:

1. P0 Road is unchanged.
2. P1 Props is unchanged.
3. P1 Terrain is unchanged.
4. P1 Vegetation is unchanged.
5. Cars are unchanged.
6. Tunnel 40 m module exists.
7. Tunnel 20 m module exists.
8. Entry module exists.
9. Exit module exists.
10. Portal exists.
11. Portal wings/retaining structures exist.
12. Wall system exists.
13. Ceiling system exists.
14. Structural rhythm is consistent.
15. Light fixtures exist.
16. Ventilation system exists.
17. Emergency/service assets exist.
18. Safety assets exist.
19. Tunnel drainage exists.
20. Sign/VMS support exists.
21. Material system exists.
22. Tunnel trim sheet exists.
23. Concrete texture exists.
24. UVs are valid.
25. Useful LODs exist.
26. Simple colliders exist.
27. Snap_Start/Snap_End exist.
28. 40 m snap = exactly 40 m.
29. 20 m snap = exactly 20 m.
30. Road clearance passes.
31. Car clearance passes.
32. Portal approach looks correct.
33. Driver view passes.
34. Chase view passes.
35. High-chase passes.
36. Night/dark preview passes.
37. Full QA sequence passes.
38. No visible tunnel seams.
39. No linked frozen asset is exported accidentally.
40. FBX files export.
41. Every FBX re-imports.
42. Validation has 0 errors.
43. Geometry report exists.
44. Material report exists.
45. Export manifest exists.
46. Source integrity passes.
47. UnityTransfer exists.
48. Tunnel import notes exist.
49. Tunnel lighting guide exists.
50. Tunnel streaming guide exists.


============================================================
FINAL FREEZE
============================================================

After successful validation:

create:

reports/P1_tunnel_FINAL_FREEZE.md

Record:

- final blend
- FBXs
- textures
- reports
- UnityTransfer
- validation status
- hashes
- known limitations

Treat:

environment/P1_Tunnel/

as FROZEN.


============================================================
FINAL REPORT
============================================================

Return ONE complete report containing:

1. discovery findings
2. source integrity
3. tunnel dimensions
4. tunnel profile
5. structural rhythm
6. 40 m module
7. 20 m module
8. entry
9. exit
10. portal
11. wall system
12. ceiling
13. barriers
14. lighting fixtures
15. light spacing
16. ventilation
17. cable/service infrastructure
18. emergency bay
19. service doors
20. safety equipment
21. signs/VMS supports
22. drainage
23. material list
24. trim-sheet strategy
25. concrete textures
26. decal/wear strategy
27. UV scale
28. LOD strategy
29. triangle counts
30. collider strategy
31. snap points
32. car-clearance QA
33. driver-view QA
34. chase-view QA
35. portal QA
36. night QA
37. full-sequence QA
38. checkpoint files
39. preview paths
40. FBX paths
41. re-import result
42. validation result
43. UnityTransfer path
44. import notes
45. lighting guide
46. streaming guide
47. freeze report
48. known limitations
49. recommended next Blender phase


============================================================
STOP CONDITION
============================================================

After P1-BLENDER-04 TUNNEL is complete:

STOP.

DO NOT START:

- Bridge / Overpass
- City
- Mountain / Coastal
- Traffic rebuild
- Player-car rebuild
- Unity integration
- Unity lighting
- Unity tunnel materials

Do NOT modify:

P0 Road Foundation

P1 Props

P1 Terrain

P1 Vegetation

finished vehicles

Do NOT launch or install Unity.

FINISH THE PREMIUM MODULAR TUNNEL SYSTEM,
VALIDATE,
EXPORT,
RE-IMPORT,
PACKAGE FOR UNITY,
FREEZE,
RETURN THE FINAL REPORT,
AND STOP.
````

