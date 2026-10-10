# Original phase specifications (P2 and P3), verbatim

These are the exact instructions I gave for each environment phase, in order. They are the source of truth for what each phase had to deliver. Each phase was completed against them; outcomes, deviations and known limitations are in the per-phase digests.


====================================================================================================
# SPEC: P2-BLENDER-01 — Premium Modular Bridges & Overpasses
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Civil-Infrastructure Artist, Hard-Surface Artist and Real-Time Optimization
Specialist with 10+ years of production experience creating bridges,
overpasses and highway structures for racing/open-world games.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

DO NOT:

- search for Unity
- install or launch Unity
- create Unity prefabs
- create Unity shaders
- create Unity scripts
- modify RoadStreamer
- modify gameplay
- modify frozen Road
- modify frozen Props
- modify frozen Terrain
- modify frozen Vegetation
- modify frozen Tunnel
- modify cars
- start City
- start Mountain/Coastal

Your responsibility is:

P2-BLENDER-01 — PREMIUM MODULAR BRIDGES & OVERPASSES

Complete:

DISCOVERY
→ SOURCE INTEGRITY BASELINE
→ READ-ONLY REFERENCE LINKING
→ SCALE / CIVIL DIMENSION STUDY
→ OVERPASS BLOCKOUT
→ BRIDGE BLOCKOUT
→ DECK SYSTEM
→ PIERS / COLUMNS
→ ABUTMENTS
→ RETAINING STRUCTURES
→ UNDERPASS SYSTEM
→ BARRIERS
→ EXPANSION JOINTS
→ DRAINAGE
→ SIGN / LIGHT MOUNTING SUPPORT
→ MATERIAL / TRIM SYSTEM
→ UVs
→ LODs
→ COLLIDERS
→ SNAP / ALIGNMENT REFERENCES
→ ROAD + TERRAIN QA
→ LONG-SEQUENCE QA
→ PREVIEW RENDERS
→ FBX EXPORT
→ RE-IMPORT VALIDATION
→ UNITY TRANSFER PACKAGE
→ FINAL REPORT
→ FREEZE
→ STOP


============================================================
CURRENT WORKSPACE
============================================================

Root:

/Users/meetshah/Documents/blender

Completed and FROZEN:

environment/P0_RoadFoundation/

environment/P1_Props/

environment/P1_Terrain/

environment/P1_Vegetation/

environment/P1_Tunnel/

Finished vehicle folders are also FROZEN.

Final Tunnel source:

environment/P1_Tunnel/blend/tunnel_07_export_ready.blend

Do not modify anything in those phases.

Use only LINKED / READ-ONLY references.


============================================================
CRITICAL SOURCE FREEZE RULE
============================================================

The following are immutable dependencies:

P0 Road Foundation

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel

Finished vehicle assets

If Bridge work exposes a problem in any frozen source:

DOCUMENT THE ISSUE.

Do NOT modify the frozen source to make the Bridge phase easier.


============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P2_Bridges/

Use:

P2_Bridges/
├── blend/
├── exports/
├── textures/
│   ├── concrete/
│   ├── trim/
│   ├── metal/
│   ├── glass/
│   ├── decals/
│   └── signs/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/


============================================================
CORE ROAD CONSTRAINT
============================================================

The runtime highway remains:

STRAIGHT

LEVEL

40 M MODULAR

Do NOT create:

- curved gameplay roads
- climbing bridge roads
- descending bridge roads
- spline-dependent bridge roads
- complex bridge junctions
- interchange ramps
- road banking changes

The bridge / overpass system must be designed AROUND the frozen P0 road.


============================================================
KNOWN ROAD ARCHITECTURE
============================================================

Main road module:

40.000 m

Secondary road module:

20.000 m

Lanes:

4

Lane width:

3.60 m

Carriageway:

14.40 m

Road module including edge strips:

15.40 m

Outer/right paved shoulder:

3.00 m

Inner/median-side shoulder:

1.50 m

Road crown:

approximately +36 mm

Unity target orientation:

+Y up
+Z forward

Blender:

+Z up
road direction -Y


============================================================
PRIMARY GOAL
============================================================

Create a reusable premium bridge / overpass system that gives the highway:

- strong visual landmarks
- vertical layering
- structural variety
- believable highway engineering
- underpass moments
- bridge-driving moments
- improved world depth

The FIRST PREMIUM VERTICAL SLICE must receive at least:

ONE STRONG HERO OVERPASS LANDMARK

that is memorable at gameplay speed.


============================================================
DESIGN LANGUAGE
============================================================

Target:

MODERN HIGHWAY CIVIL INFRASTRUCTURE

Use believable:

- concrete
- steel
- girders
- piers
- cap beams
- abutments
- bearings
- barriers
- drainage
- expansion joints
- retaining walls

Avoid:

- sci-fi bridge design
- fantasy suspension systems
- unrealistically thin slabs
- giant unsupported spans
- decorative geometry with no structural logic
- flat featureless concrete boxes


============================================================
REFERENCE LINKING
============================================================

Link read-only:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel where useful for:

- concrete language
- retaining-wall language
- infrastructure scale

Optional:

lightweight Hypercar reference

Use references for:

- scale
- road alignment
- support clearance
- camera QA
- terrain transition
- prop clearance

Never save modifications into the linked files.


============================================================
PHASE 01 — SOURCE INTEGRITY BASELINE
============================================================

Before production:

hash all files under:

P0_RoadFoundation

P1_Props

P1_Terrain

P1_Vegetation

P1_Tunnel

finished vehicle folders

Create:

reports/P2_bridges_source_baseline.json

Include:

- file count
- file paths
- hashes
- timestamps if useful

At phase completion verify all frozen sources remain byte-for-byte unchanged.


============================================================
PHASE 02 — DISCOVERY
============================================================

Measure the frozen environment.

Record:

- carriageway width
- shoulder width
- total road corridor
- terrain corridor
- guardrail placement
- streetlight placement
- sign clearance
- gantry clearance
- chase-camera height
- vehicle height
- tunnel portal/material language where useful

Create:

reports/P2_bridges_discovery.md

Document:

- chosen overpass span
- chosen bridge deck depth
- chosen clearance
- pier strategy
- abutment strategy
- bridge module architecture
- material strategy
- LOD strategy
- collision strategy


============================================================
STRUCTURE FAMILIES
============================================================

Create at minimum these production families:

A. HERO OVERPASS

Overpass_Hero

Overpass_Standard

Overpass_Wide


B. BRIDGE ROAD STRUCTURE

Bridge_Deck_40m

Bridge_Deck_20m

Bridge_Deck_Start

Bridge_Deck_End


C. PIERS / SUPPORTS

Bridge_Pier_A

Bridge_Pier_B

Bridge_Pier_Wide

Bridge_CapBeam_A

Bridge_CapBeam_B


D. ABUTMENTS

Bridge_Abutment_A

Bridge_Abutment_B

Bridge_WingWall_L

Bridge_WingWall_R


E. UNDERPASS

Underpass_40m

Underpass_20m if useful

Underpass_Wall_L

Underpass_Wall_R

Underpass_Ceiling

Underpass_EndTrim


F. SAFETY / EDGE STRUCTURES

Bridge_Parapet_Concrete

Bridge_Parapet_Metal

Bridge_Parapet_Transition


G. DETAILS

Bridge_ExpansionJoint_A

Bridge_ExpansionJoint_B

Bridge_Bearing_A

Bridge_Bearing_B

Bridge_Drain_A

Bridge_Downpipe_A

Bridge_DeckDrain_4m

Bridge_DeckDrain_8m


============================================================
HERO OVERPASS
============================================================

Create one high-quality landmark:

Overpass_Hero

This is a major visual asset for the premium vertical slice.

It should be readable at:

50 m

100 m

200 m

300 m

It should have a distinct silhouette without becoming unrealistic.


============================================================
HERO OVERPASS REQUIREMENTS
============================================================

The hero overpass must include believable:

- deck
- underside girders / structural system
- edge structure
- barriers/parapets
- supports
- cap beams
- drainage hints
- joints
- optional light/sign mounting

The player will drive underneath it.

The UNDERSIDE is therefore as important as the top silhouette.


============================================================
OVERPASS CLEARANCE
============================================================

Maintain realistic clear height over the roadway.

Target minimum:

approximately 5.5 m

Preferred practical range:

approximately 5.8–6.2 m

depending on structural depth.

Validate using:

- Hypercar
- traffic-scale reference
- chase camera

Nothing structural may intrude below the documented clearance.


============================================================
OVERPASS SPAN
============================================================

The overpass span must clear:

- all active traffic lanes
- shoulders
- median safety area
- roadside barrier requirements

Supports must remain outside active driving lanes.


============================================================
PIER STRATEGIES
============================================================

Create useful support options:

1. CENTRAL SUPPORT

Only if safely located within an appropriate median area.

2. SIDE PIERS

Supports outside the road corridor.

3. WIDE-SPAN

No central road support.

Do NOT place a column directly in a gameplay lane.


============================================================
OVERPASS DECK
============================================================

Use believable structural thickness.

Do not create a paper-thin deck.

Include major visible structure such as:

- slab
- box girder
- I-girder arrangement
- edge beam

Choose a coherent system.

Do not randomly mix structural types.


============================================================
OVERPASS VARIANTS
============================================================

Overpass_Standard:

simple production highway crossing.

Overpass_Wide:

larger span / broader deck.

Overpass_Hero:

strongest visual landmark.

Variants must not merely be scaled copies.


============================================================
BRIDGE ROAD SYSTEM
============================================================

Create bridge structural support for the existing P0 road.

The frozen P0 road remains the actual gameplay-road geometry.

The bridge system should provide:

- structural deck beneath road
- underside
- edge beams
- parapets
- support system
- abutments
- drainage
- transition elements

Do NOT unnecessarily duplicate lane geometry.


============================================================
CRITICAL ROAD HEIGHT RULE
============================================================

The gameplay road remains LEVEL.

Do NOT:

- raise the road
- create ramps onto the bridge
- create slope into bridge
- create road elevation curves

To make the bridge appear elevated:

the ENVIRONMENT drops away below the road.

The road itself remains at its established gameplay height.


============================================================
BRIDGE 40 M MODULE
============================================================

Create:

Bridge_Deck_40m

Runtime snap distance:

40.000 m exactly.

Must align with:

P0 Road_4Lane_40m


============================================================
BRIDGE 20 M MODULE
============================================================

Create:

Bridge_Deck_20m

Runtime snap distance:

20.000 m exactly.


============================================================
BRIDGE START / END
============================================================

Create:

Bridge_Deck_Start

Bridge_Deck_End

Purpose:

visual transition between:

terrain / embankment
→ abutment
→ bridge

and:

bridge
→ abutment
→ terrain

Do not modify P1 Terrain.


============================================================
BRIDGE TRANSITION DESIGN
============================================================

Transition should hide:

- sudden terrain termination
- floating deck
- exposed underside gaps
- unsupported road edges

Use:

abutments
wing walls
retaining elements
soil/terrain overlap allowance

while keeping terrain frozen.


============================================================
ABUTMENTS
============================================================

Create:

Bridge_Abutment_A

Bridge_Abutment_B

Use believable:

- backwall
- bearing shelf
- stem
- footing implication
- wing-wall transition
- drainage zones

Small engineering detail should be texture/normal-driven.


============================================================
WING WALLS
============================================================

Create:

Bridge_WingWall_L

Bridge_WingWall_R

Provide clean visual connection to terrain.

Do not require terrain geometry edits.


============================================================
PIERS
============================================================

Create:

Bridge_Pier_A

Bridge_Pier_B

Bridge_Pier_Wide

Use distinct but coherent shapes.

Examples:

- rectangular pier
- rounded/chamfered pier
- twin-column support

Do not over-detail.


============================================================
PIER BASE
============================================================

Ground contact should look structurally plausible.

Provide:

- footing implication
- widened base if appropriate

Do not create massive underground foundations.


============================================================
CAP BEAMS
============================================================

Create:

Bridge_CapBeam_A

Bridge_CapBeam_B

Cap beam must visually support the deck/girders.


============================================================
BEARINGS
============================================================

Create:

Bridge_Bearing_A

Bridge_Bearing_B

These are optional visible structural details.

Keep geometry simple.

Do not model engineering internals.


============================================================
BRIDGE UNDERSIDE — HIGH PRIORITY
============================================================

The underside MUST NOT be:

one flat concrete plane.

Create readable structure.

Possible system:

- longitudinal girders
- cross beams
- box-girder recesses
- deck ribs

Use a coherent structural pattern.


============================================================
UNDERSIDE RHYTHM
============================================================

At high-speed chase view, underside details should create visible rhythm.

Do not create tiny invisible engineering clutter.

Focus on:

large readable beams
shadows
structural depth


============================================================
UNDERPASS SYSTEM
============================================================

Create a short structural underpass system.

Required:

Underpass_40m

Underpass_Wall_L

Underpass_Wall_R

Underpass_Ceiling

Underpass_EndTrim

Optional:

Underpass_20m


============================================================
UNDERPASS DESIGN RULE
============================================================

Do NOT make the underpass look like another full tunnel.

It should feel like:

a short bridge/structure crossing over the highway.

Visual language:

- shorter enclosure
- daylight visible at both ends
- heavy deck above
- support walls/columns
- structural beams


============================================================
UNDERPASS CLEARANCE
============================================================

Use the same practical road-clearance requirements as the overpass.

Nothing should hang dangerously low.


============================================================
BRIDGE PARAPETS
============================================================

Create:

Bridge_Parapet_Concrete

Bridge_Parapet_Metal

Bridge_Parapet_Transition

These should provide a believable bridge-specific road edge.


============================================================
P0 SAFETY COMPATIBILITY
============================================================

Ensure bridge barriers can transition visually to the frozen:

P0/P1 safety system.

Do NOT modify P0/P1 guardrails.


============================================================
EXPANSION JOINTS
============================================================

Create:

Bridge_ExpansionJoint_A

Bridge_ExpansionJoint_B

These should be primarily visual.

Do not create collision geometry that causes a vehicle bump.


============================================================
EXPANSION JOINT PLACEMENT
============================================================

Use at:

bridge start/end

and selected structural seams where believable.

Do not place them every few metres.


============================================================
DRAINAGE
============================================================

Create:

Bridge_Drain_A

Bridge_Downpipe_A

Bridge_DeckDrain_4m

Bridge_DeckDrain_8m

Potential uses:

deck edges

parapet base

abutment runoff

understructure drainage


============================================================
DRAINAGE PERFORMANCE
============================================================

Repeated grates/drains must have efficient geometry.

Create LODs if worthwhile.

Do not repeat high-detail grate bars hundreds of times.


============================================================
LIGHTING SUPPORT
============================================================

DO NOT create final Unity lights.

Create geometry only:

Bridge_LightPoleMount

Bridge_UnderdeckLightFixture

Overpass_UnderlightFixture

Optional:

Bridge_ServiceLightFixture

Blender emission is preview only.


============================================================
SIGN SUPPORT
============================================================

Prefer compatibility with P1 Props.

Only create bridge-specific mounts where required:

Bridge_SignMount

Overpass_SignFrame

Bridge_VMS_Mount

Do not recreate all road signs.


============================================================
NOISE BARRIER
============================================================

Optional but useful:

Bridge_NoiseBarrier_4m

Bridge_NoiseBarrier_8m

Bridge_NoiseBarrier_End

Possible style:

metal + transparent/acrylic panel

or:

solid acoustic panel.

Keep modular.


============================================================
NOISE BARRIER PERFORMANCE
============================================================

If transparent:

avoid excessive layered transparency.

Use simple geometry.


============================================================
MATERIAL SYSTEM
============================================================

Create shared Blender source materials:

MAT_Bridge_Concrete

MAT_Bridge_Concrete_Dark

MAT_Bridge_Steel

MAT_Bridge_Galvanized

MAT_Bridge_PaintedMetal

MAT_Bridge_Rubber

MAT_Bridge_Glass

MAT_Bridge_Drain

MAT_Bridge_SignSupport if needed

These are preview/source materials.

Final Unity materials come later.


============================================================
BRIDGE TRIM SHEET
============================================================

Create:

T_Bridge_Trim_2K

Maps:

BaseColor

Normal

Roughness

Metallic

AO

Suggested regions:

- clean concrete edge
- weathered concrete edge
- galvanized metal
- painted steel
- dark structural steel
- rubber
- expansion-joint surface
- drain metal
- utility metal
- barrier detail


============================================================
CONCRETE TEXTURE
============================================================

Create or reuse:

T_Bridge_Concrete_2K

Tileable.

Maps:

BaseColor

Normal

Roughness

AO

Use a realistic modern infrastructure concrete.

Avoid:

heavy noise
giant cracks
uniform white concrete
overly damaged abandoned look


============================================================
VISUAL LANGUAGE CONSISTENCY
============================================================

Bridge concrete should fit visually with:

P1 Terrain retaining walls

and

P1 Tunnel concrete

without requiring exact texture duplication.

If reusing a source texture:

document provenance.

Do not modify the upstream texture.


============================================================
STEEL
============================================================

Use subtle realistic steel variation.

Do not make all structural steel:

perfect chrome

or

pure flat grey.


============================================================
WEATHERING
============================================================

Concentrate wear logically.

Examples:

under expansion joints

around drains

pier bases

abutment edges

underside runoff

metal joint interfaces


============================================================
DECALS
============================================================

Create optional reusable decals:

Bridge_Runoff_A

Bridge_Runoff_B

Bridge_ConcreteStain_A

Bridge_RepairPatch_A

Bridge_RustStreak_A

Bridge_DirtEdge_A

Do NOT bake heavy damage everywhere.


============================================================
UV STRATEGY
============================================================

Long bridge surfaces must use tileable UVs.

Do NOT stretch one 0–1 texture over:

40 m deck

large pier

entire overpass.


============================================================
TEXEL DENSITY
============================================================

Maintain consistent practical environment texel density.

Document:

metres per tile

for:

concrete

metal

trim-sheet sections


============================================================
LOD STRATEGY
============================================================

Create LODs where visually/performance useful.

At minimum consider:

Overpass_Hero

Overpass_Standard

Bridge_Deck_40m

Bridge_Piers

Bridge_Abutments

Underpass

Noise barriers

Drainage

Large sign/light frames


============================================================
LOD GUIDANCE
============================================================

Hero Overpass:

LOD0:
100%

LOD1:
approximately 40–60%

LOD2:
approximately 15–30%

LOD3:
optional 5–10%


Bridge structural module:

LOD0

LOD1

LOD2


Small trivial parts:

do not create pointless LOD chains.


============================================================
LOD SILHOUETTE RULE
============================================================

Preserve:

- overall deck thickness
- major girder count impression
- pier silhouette
- overpass identity
- parapet silhouette

Remove:

- small brackets
- tiny drainage
- small bearing detail
- invisible structural details


============================================================
TRIANGLE GUIDANCE
============================================================

Use only as guidance.

Hero overpass:

LOD0 approximately 5k–20k tris

Bridge 40 m structure:

approximately 4k–12k

Pier:

approximately 500–2.5k

Abutment:

approximately 1k–4k

Underpass:

approximately 3k–10k

Small details:

as low as practical.

DO NOT pad geometry to reach budgets.


============================================================
COLLISION
============================================================

P0 Road remains responsible for driving-surface collision.

Bridge collision should be simple.

Create where needed:

Collision_Bridge_Parapet_L

Collision_Bridge_Parapet_R

Collision_Overpass_Pier

Collision_Bridge_Pier

Collision_Abutment

Collision_UnderpassWall_L

Collision_UnderpassWall_R

Potential:

Collision_NoiseBarrier

if actually needed.


============================================================
COLLISION RULE
============================================================

Do NOT use detailed bridge visual meshes as colliders.

Use:

simple boxes

low-poly hulls

simple convex shapes


============================================================
NO DECK ROAD COLLISION DUPLICATION
============================================================

If frozen P0 road provides driving collision:

do not duplicate a second road collider directly beneath/over it.

Avoid physics conflicts.


============================================================
SNAP POINTS
============================================================

All road-aligned runtime bridge modules must include:

Snap_Start

Snap_End

40 m:

40.000 m exactly

20 m:

20.000 m exactly


============================================================
ALIGNMENT REFERENCES
============================================================

Create documented empties as useful:

RoadCenter

DeckTop

DeckBottom

ClearanceBottom

PierCenter

Pier_L

Pier_R

AbutmentFace

WallInner_L

WallInner_R

OverpassCenter


============================================================
ORIGINS
============================================================

Bridge modules:

road-grid start/centre convention consistent with P0.

Overpass:

road-centre structural reference.

Pier:

base centre.

Abutment:

base / road-facing reference.

Drainage:

mounting point.

Fixtures:

mount point.


============================================================
TRANSFORMS
============================================================

All production assets:

Scale 1,1,1

No negative scale.

Clean rotations.

Apply transforms safely.


============================================================
NORMALS
============================================================

Concrete:

clean hard/smooth transitions based on structure.

Steel:

clean hard-surface shading.

Do not oversmooth:

deck edges
beam corners
panel joints.


============================================================
BRIDGE QA SCENE
============================================================

Create approximately:

400–600 m

temporary QA environment.

Use linked frozen assets.

Suggested sequence:

Open Road
→ Terrain Fill
→ Bridge Start
→ Bridge_40m
→ Bridge_40m
→ Bridge End
→ Open Road
→ Hero Overpass
→ Underpass
→ Open Road


============================================================
IMPORTANT QA RULE
============================================================

Do NOT export the entire QA sequence as one gameplay mesh.

QA is only for visual/scale/testing.


============================================================
USE FROZEN ENVIRONMENT
============================================================

Link:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

Optionally Tunnel in distant/context comparison.

Do not export any linked source.


============================================================
CAR QA
============================================================

Optionally link Hypercar.

Check:

- overpass clearance
- pier scale
- barrier scale
- underpass clearance
- chase-camera composition


============================================================
HERO OVERPASS CAMERA TEST
============================================================

Capture Hero Overpass from:

50 m

100 m

200 m

300 m

At 300 m:

its major silhouette should still be recognizable.


============================================================
DRIVER VIEW QA
============================================================

Test:

approaching overpass

under overpass

bridge-driving section

underpass

Ensure:

road sightline remains clear.


============================================================
CHASE VIEW QA
============================================================

Use:

low chase

high chase

Check:

structure scale

understructure readability

parapets

supports

landmark silhouette


============================================================
BRIDGE DRIVING QA
============================================================

From road level:

bridge should feel elevated because world falls away beneath it.

The road itself stays level.


============================================================
TERRAIN TRANSITION QA
============================================================

Check:

Bridge_Start

Bridge_End

Abutment

Wing Walls

against linked P1 Terrain.

No:

large holes

floating abutments

impossible soil intersections

Do not edit terrain to solve issues.


============================================================
UNDERPASS QA
============================================================

Check a sequence:

daylight
→ shadow beneath structure
→ daylight

Geometry should not become a fake tunnel.


============================================================
NIGHT-LIKE PREVIEW
============================================================

Create Blender-only night-style preview.

Use it to evaluate:

- silhouette
- underside structure
- lighting mounts
- support readability

Do not claim Unity lighting accuracy.


============================================================
WET PREVIEW
============================================================

Optional only.

Do NOT modify frozen P0 road.

Use presentation-only material override if needed.


============================================================
REQUIRED PREVIEWS
============================================================

Create at minimum:

previews/P2_bridge_hero_overpass.png

previews/P2_bridge_overpass_50m.png

previews/P2_bridge_overpass_100m.png

previews/P2_bridge_overpass_200m.png

previews/P2_bridge_overpass_300m.png

previews/P2_bridge_driver_approach.png

previews/P2_bridge_driver_underpass.png

previews/P2_bridge_chase_underpass.png

previews/P2_bridge_high_chase.png

previews/P2_bridge_deck.png

previews/P2_bridge_understructure.png

previews/P2_bridge_piers.png

previews/P2_bridge_abutment.png

previews/P2_bridge_start_end.png

previews/P2_bridge_expansion_joint.png

previews/P2_bridge_drainage.png

previews/P2_bridge_night.png

previews/P2_bridge_full_sequence.png

previews/P2_bridge_asset_library.png


============================================================
VISUAL HARD GATES
============================================================

A. HERO LANDMARK

Hero Overpass must feel memorable and premium.

B. SCALE

Bridge elements must feel correctly scaled to cars and road.

C. CLEARANCE

No structure enters active road clearance.

D. SUPPORT LOGIC

Columns / supports must look structurally believable.

E. UNDERSIDE

Driving underneath must reveal convincing structure.

F. TERRAIN CONNECTION

Abutments / wing walls must visually connect without terrain modification.

G. REPETITION

Long bridge runs must not look like obvious repeated identical boxes.

H. PERFORMANCE

Repeated structure must remain economical.

I. GAMEPLAY VISIBILITY

Supports must not unnecessarily block sightlines.

J. ROAD ARCHITECTURE

Road remains straight and level.


============================================================
CHECKPOINT FILES
============================================================

Create:

blend/bridges_01_blockout.blend

blend/bridges_02_overpass.blend

blend/bridges_03_bridge_deck.blend

blend/bridges_04_structures.blend

blend/bridges_05_materials_uv.blend

blend/bridges_06_lods_collision.blend

blend/bridges_07_export_ready.blend

Never overwrite earlier checkpoints.


============================================================
COLLECTIONS
============================================================

Use:

BRIDGES_MASTER

BRIDGE_OVERPASS

BRIDGE_DECKS

BRIDGE_PIERS

BRIDGE_ABUTMENTS

BRIDGE_RETAINING

BRIDGE_UNDERPASS

BRIDGE_BARRIERS

BRIDGE_EXPANSION

BRIDGE_DRAINAGE

BRIDGE_FIXTURES

BRIDGE_COLLIDERS

BRIDGE_QA

BRIDGE_PRESENTATION


============================================================
AUTOMATION
============================================================

Store Blender Python in:

scripts/

Suggested:

bridges_build.py

bridges_materials.py

bridges_lods.py

bridges_validate.py

bridges_render.py

bridges_export.py


============================================================
EXPORT ORIENTATION
============================================================

Use the SAME proven Blender → Unity export process used by:

Hypercar

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel

Target:

Unity +Y up

Unity +Z forward

Do NOT randomly change axis/export settings.


============================================================
FBX EXPORTS
============================================================

Create:

exports/bridges_complete.fbx

and logical split FBXs:

exports/Overpasses.fbx

exports/BridgeDecks.fbx

exports/Piers_Abutments.fbx

exports/Underpass.fbx

exports/BridgeBarriers.fbx

exports/BridgeDrainage.fbx

exports/BridgeFixtures.fbx

exports/BridgeCollision.fbx

Use approximately 8–10 logical FBXs.

Do not create dozens of tiny files unnecessarily.


============================================================
EXPORT CONTENT
============================================================

Include only P2 Bridges production assets.

DO NOT EXPORT:

- P0 Road
- P1 Props
- P1 Terrain
- P1 Vegetation
- P1 Tunnel
- cars
- QA assembly
- cameras
- Blender lights
- presentation background
- temporary helpers


============================================================
TEXTURE EXPORT
============================================================

Final production textures go under:

textures/

and later UnityTransfer/Textures/

Include only textures necessary for P2 Bridges.

Do not duplicate upstream textures unnecessarily.


============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

After exporting all FBXs:

create a clean empty Blender scene.

Re-import EVERY FBX.

Validate:

- object names
- hierarchy
- world dimensions
- scale
- orientation
- Unity +Y up
- Unity +Z forward
- materials
- UVs
- LOD objects
- colliders
- snap points
- triangle counts
- normals
- origins where verifiable

Target:

0 errors.


============================================================
VALIDATION REPORT
============================================================

Create:

reports/P2_bridges_validation.txt

Check at minimum:

1. source integrity
2. Hero Overpass exists
3. Standard Overpass exists
4. Wide Overpass exists
5. Hero 300 m readability QA exists
6. overpass road clearance
7. support lane clearance
8. Bridge 40 m exists
9. Bridge 20 m exists
10. Bridge Start exists
11. Bridge End exists
12. piers exist
13. cap beams exist
14. abutments exist
15. wing walls exist
16. underpass exists
17. underside structure exists
18. parapets/barriers exist
19. expansion joints exist
20. bearings exist
21. drainage exists
22. lighting/sign mounts exist
23. materials exist
24. trim sheet exists
25. UVs valid
26. LODs valid
27. colliders valid
28. transforms clean
29. pivots/origins valid
30. snap distances valid
31. QA sequence passes
32. exports contain no frozen linked assets
33. FBX re-import passes

Target:

0 errors

0 critical warnings.

Do NOT warn merely because an asset is below triangle guidance.


============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P2_bridges_geometry.json

For each asset include:

- name
- family
- dimensions
- LOD
- triangles
- vertices
- material slots
- UV status
- collider status
- snap references
- clearance relevance


============================================================
MATERIAL REPORT
============================================================

Create:

reports/P2_bridges_materials.md

Document:

- material list
- trim sheet layout
- concrete maps
- steel maps
- glass/noise barrier maps
- texel density
- metres per tile
- decals
- weathering strategy
- Unity expectations


============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P2_bridges_export_manifest.json

Include:

- final source blend
- FBX files
- included objects
- excluded QA objects
- textures
- materials
- LODs
- colliders
- snap conventions
- coordinate conversion


============================================================
SOURCE INTEGRITY CHECK
============================================================

At completion hash all frozen dependencies again.

Create:

reports/P2_bridges_source_integrity_check.md

Confirm:

P0 Road unchanged

P1 Props unchanged

P1 Terrain unchanged

P1 Vegetation unchanged

P1 Tunnel unchanged

Cars unchanged

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
BRIDGES IMPORT NOTES
============================================================

Create:

UnityTransfer/README/BRIDGES_IMPORT_NOTES.md

Document:

1. source phase
2. Unity orientation
3. scale
4. road relationship
5. level-road requirement
6. 40 m module convention
7. 20 m module convention
8. Hero Overpass
9. other overpass variants
10. Bridge Deck modules
11. Start/End modules
12. piers
13. cap beams
14. abutments
15. wing walls
16. underpass
17. parapets
18. expansion joints
19. drainage
20. LOD naming
21. materials
22. texture channels
23. colliders
24. snap points
25. alignment empties
26. excluded QA assets

State clearly:

THIS PACKAGE WAS CREATED ON A BLENDER-ONLY WORKSTATION.

UNITY-SIDE:

MATERIALS

REFLECTIONS

REAL LIGHTS

SHADOWS

LODGroup COMPONENTS

ROADSTREAMER INTEGRATION

TERRAIN PLACEMENT

CULLING

QUALITY TIERS

AND PERFORMANCE TESTING

MUST BE COMPLETED ON THE UNITY WORKSTATION.


============================================================
BRIDGE STREAMING GUIDE
============================================================

Create:

UnityTransfer/README/BRIDGES_STREAMING_GUIDE.md

Document example compositions:

A. BRIDGE RUN

Open Road
→ Bridge Start
→ Bridge 40
→ Bridge 40
→ Bridge End
→ Open Road

B. OVERPASS

Open Road
→ Hero/Standard Overpass
→ Open Road

C. SHORT UNDERPASS

Open Road
→ Underpass
→ Open Road

Explain:

- which assets are structural
- which are optional details
- snap conventions
- what should remain from P0
- what must not be duplicated

Do not write Unity code.


============================================================
PERFORMANCE NOTES
============================================================

Create:

UnityTransfer/README/BRIDGES_PERFORMANCE_GUIDE.md

Document recommended concepts:

PC:

- highest useful structural LOD
- Hero Overpass full quality near
- underside detail retained

Mobile:

- earlier LOD transitions
- reduce drain/fixture detail
- limit transparent noise barriers
- aggressive small-detail culling
- GPU instancing where appropriate

Do not claim measured Unity FPS.


============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P2-BLENDER-01 COMPLETE UNTIL:

1. P0 is unchanged.
2. Props are unchanged.
3. Terrain is unchanged.
4. Vegetation is unchanged.
5. Tunnel is unchanged.
6. Cars are unchanged.

7. Hero Overpass exists.
8. Hero Overpass passes 50 m view.
9. Hero Overpass passes 100 m view.
10. Hero Overpass passes 200 m view.
11. Hero Overpass passes 300 m view.

12. Standard Overpass exists.
13. Wide Overpass exists.

14. Supports remain outside active lanes.
15. Overpass vertical clearance passes.

16. Bridge_Deck_40m exists.
17. 40 m snap is exactly 40.000 m.
18. Bridge_Deck_20m exists.
19. 20 m snap is exactly 20.000 m.

20. Bridge Start exists.
21. Bridge End exists.

22. Pier system exists.
23. Cap beams exist.
24. Abutments exist.
25. Wing walls exist.

26. Underpass exists.
27. Underpass clearance passes.
28. Understructure reads correctly.

29. Bridge parapets exist.
30. Barrier transitions exist.
31. Expansion joints exist.
32. Bearings exist.
33. Drainage exists.
34. Sign/light mounts exist.

35. Shared materials exist.
36. Trim sheet exists.
37. Concrete texture exists.
38. UVs are valid.

39. Useful LODs exist.
40. Simple colliders exist.

41. Driver-view QA passes.
42. Low-chase QA passes.
43. High-chase QA passes.
44. Terrain-transition QA passes.
45. Full-sequence QA passes.

46. Road remains straight.
47. Road remains level.
48. No frozen road geometry has been duplicated unnecessarily.

49. FBXs export.
50. Every FBX re-imports successfully.
51. Re-import hierarchy matches.
52. Re-import materials match.
53. Re-import triangle counts match.

54. Validation reports 0 errors.
55. No frozen linked asset is accidentally included in exports.

56. Geometry report exists.
57. Material report exists.
58. Export manifest exists.
59. Source-integrity report passes.

60. UnityTransfer exists.
61. BRIDGES_IMPORT_NOTES exists.
62. BRIDGES_STREAMING_GUIDE exists.
63. BRIDGES_PERFORMANCE_GUIDE exists.


============================================================
FINAL FREEZE
============================================================

After all validation passes:

create:

reports/P2_bridges_FINAL_FREEZE.md

Record:

- final source blend
- final FBXs
- final textures
- final reports
- UnityTransfer
- validation state
- important hashes
- known limitations

Then treat:

environment/P2_Bridges/

as FROZEN.


============================================================
FINAL REPORT
============================================================

Create:

reports/P2_bridges_FINAL_REPORT.md

Return ONE complete report covering:

1. discovery findings
2. source-integrity result
3. chosen bridge design language
4. Hero Overpass
5. Hero Overpass dimensions
6. 50/100/200/300 m landmark QA
7. Standard Overpass
8. Wide Overpass
9. clearance
10. support placement
11. Bridge 40 m module
12. Bridge 20 m module
13. Start/End modules
14. deck structural system
15. underside structure
16. pier system
17. cap beams
18. abutments
19. wing walls
20. underpass
21. parapets/barriers
22. expansion joints
23. bearings
24. drainage
25. lights/sign supports
26. material list
27. trim sheet
28. concrete texture
29. UV strategy
30. weathering/decal strategy
31. LOD strategy
32. triangle counts
33. collider strategy
34. snap points
35. alignment references
36. driver-view QA
37. chase-view QA
38. high-chase QA
39. terrain-transition QA
40. full-sequence QA
41. checkpoint paths
42. preview paths
43. FBX paths
44. FBX re-import result
45. validation result
46. UnityTransfer path
47. import notes
48. streaming guide
49. performance guide
50. freeze report
51. known limitations
52. recommended next Blender phase


============================================================
STOP CONDITION
============================================================

After P2-BLENDER-01 BRIDGES & OVERPASSES is complete:

STOP.

DO NOT START:

- City
- Mountain / Coastal
- additional road phases
- Tunnel revisions
- Traffic rebuild
- Player-car rebuild
- Unity integration
- Unity materials
- Unity lighting
- Unity performance work

Do NOT modify:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel

finished vehicles

Do NOT launch or install Unity.

FINISH THE COMPLETE BRIDGES / OVERPASSES KIT,
CREATE THE HERO OVERPASS,
VALIDATE ALL CLEARANCES,
EXPORT,
RE-IMPORT,
PACKAGE FOR UNITY,
FREEZE,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P2-BLENDER-01A — Bridge Valley, Embankment & Terrain Context Addendum
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Terrain Artist, Civil-Infrastructure Artist and Real-Time Optimization
Specialist with 10+ years of production experience creating highway valleys,
bridge approaches, embankments and terrain transitions for racing/open-world games.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

Your responsibility is:

P2-BLENDER-01A — BRIDGE VALLEY, EMBANKMENT & TERRAIN CONTEXT ADDENDUM

This is a SMALL TARGETED ADD-ON PHASE.

The Bridge system is already complete and frozen.

The P1 Terrain system is already complete and frozen.

DO NOT reopen or modify either one.

Your job is to create the missing ENVIRONMENT CONTEXT required to use the
finished bridges convincingly:

- shallow bridge valleys
- deep bridge valleys
- bridge approach embankments
- abutment terrain transitions
- under-bridge terrain
- ravine / drainage valley options
- optional dry riverbed / stream-bed context
- bridge terrain vistas

Complete:

DISCOVERY
→ FROZEN-SOURCE BASELINE
→ READ-ONLY REFERENCE LINKING
→ VALLEY PROFILE STUDY
→ SHALLOW VALLEY
→ MEDIUM VALLEY
→ DEEP VALLEY
→ BRIDGE APPROACH EMBANKMENTS
→ ABUTMENT TRANSITIONS
→ UNDER-BRIDGE TERRAIN
→ RAVINE / RIVERBED CONTEXT
→ MATERIAL / TERRAINBLEND COMPATIBILITY
→ VEGETATIONMASK COMPATIBILITY
→ LODs
→ COLLISION WHERE NEEDED
→ SEAM QA
→ BRIDGE QA ASSEMBLY
→ PREVIEWS
→ FBX EXPORT
→ RE-IMPORT VALIDATION
→ UNITY TRANSFER PACKAGE
→ FINAL REPORT
→ FREEZE
→ STOP


============================================================
WORKSPACE
============================================================

Root:

/Users/meetshah/Documents/blender


============================================================
FROZEN SOURCES
============================================================

The following phases are COMPLETE and IMMUTABLE:

environment/P0_RoadFoundation/

environment/P1_Props/

environment/P1_Terrain/

environment/P1_Vegetation/

environment/P1_Tunnel/

environment/P2_Bridges/

Finished vehicle folders are also frozen.


============================================================
IMPORTANT FINAL SOURCES
============================================================

Terrain:

environment/P1_Terrain/blend/terrain_09_final_frozen.blend

Vegetation:

environment/P1_Vegetation/blend/vegetation_09_final_frozen.blend

Tunnel:

environment/P1_Tunnel/blend/tunnel_07_export_ready.blend

Bridges:

environment/P2_Bridges/blend/bridges_07_export_ready.blend


============================================================
CRITICAL FREEZE RULE
============================================================

DO NOT MODIFY:

- P1 Terrain
- P2 Bridges
- Road
- Props
- Vegetation
- Tunnel
- Vehicles

Do NOT "fix" terrain by changing terrain_09.

Do NOT "fix" bridges by changing bridges_07.

This is a separate additive package.

If the new context exposes a problem in a frozen phase:

DOCUMENT IT.

Do not edit the frozen source.


============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P2_BridgeTerrainContext/

Use:

P2_BridgeTerrainContext/
├── blend/
├── exports/
├── textures/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/


============================================================
WHY THIS PHASE EXISTS
============================================================

P2-BLENDER-01 Bridges is complete.

However:

the current frozen P1 Terrain does not contain a sufficiently deep valley
environment for convincing bridge runs.

The bridge QA scene used temporary terrain beneath the bridge.

That temporary terrain was correctly excluded from the Bridge export.

This phase converts that missing context into a reusable production kit.

Do NOT make this a second general terrain phase.


============================================================
PRIMARY GOAL
============================================================

Create terrain context so the finished bridge system can convincingly support:

1. SHORT SHALLOW BRIDGE CROSSING

2. MEDIUM VALLEY BRIDGE

3. DEEP VALLEY BRIDGE

4. RAVINE CROSSING

5. DRY / SEASONAL RIVERBED CROSSING

6. BRIDGE APPROACH / ABUTMENT TRANSITION

while keeping:

- the gameplay road straight
- the gameplay road level
- P0 Road unchanged
- P1 Terrain unchanged
- P2 Bridges unchanged


============================================================
CRITICAL ROAD RULE
============================================================

The road remains at its existing elevation.

Do NOT create:

- bridge approach slopes
- road hills
- curved bridge road
- dipping road
- raised bridge deck road
- spline-based terrain-road transitions

The terrain falls AWAY beneath / around the bridge.

The road does not move vertically.


============================================================
KNOWN BRIDGE FACTS
============================================================

Treat these P2-BLENDER-01 facts as fixed:

Hero Overpass:

length:
83 m

main span:
33.5 m

minimum measured road clearance:
6.18 m

Wide Overpass minimum clearance:
5.96 m

Supports:

outside active driving lanes

Bridge modules:

40.000 m
20.000 m

Bridge road:

frozen P0 road remains the gameplay surface

Expansion joints:

visual-only

Bridge Start / End:

wing walls and barrier transitions extend approximately:

8.7 m

into neighboring open-road chunks.

IMPORTANT:

The terrain-context design must account for this 8.7 m overlap.


============================================================
KNOWN TERRAIN FACTS
============================================================

P1 Terrain is frozen.

Near-terrain corridor generally extends approximately:

50 m from road centreline.

Existing terrain includes:

- Flat
- Cut
- Fill
- Ditch
- Retaining
- Rock Cut
- Vistas

But it does NOT contain the deep bridge-valley context needed here.


============================================================
TERRAIN DATA CONVENTIONS
============================================================

Maintain compatibility with final P1 Terrain.

TerrainBlend:

R = grass

G = soil

B = rock

A = gravel


VegetationMask UV1:

U = vegetation density

V = dryness

Do NOT invent different semantics.


============================================================
SOURCE INTEGRITY BASELINE
============================================================

Before production:

hash all frozen sources:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel

P2 Bridges

Vehicles

Create:

reports/P2_bridgeTerrain_source_baseline.json

At completion:

verify byte-for-byte unchanged.


============================================================
PHASE 01 — DISCOVERY
============================================================

Link read-only:

P0 Road

P1 Terrain

P1 Vegetation

P2 Bridges

Optional:

Props
Tunnel
Hypercar

Measure:

- Bridge Start/End overlap
- abutment dimensions
- pier positions
- deck underside
- valley visibility from chase camera
- terrain-width requirements
- bridge viewing distance
- frozen terrain seam profiles

Create:

reports/P2_bridgeTerrain_discovery.md


============================================================
DISCOVERY MUST DOCUMENT
============================================================

1. Bridge Start overlap
2. Bridge End overlap
3. abutment interface
4. pier clear zones
5. chosen valley widths
6. chosen valley depths
7. approach lengths
8. seam strategy
9. terrain material strategy
10. vegetation-mask strategy
11. LOD strategy
12. collision strategy


============================================================
DESIGN PHILOSOPHY
============================================================

Think like a highway crossing a natural low area.

The bridge should look necessary.

Avoid terrain that looks like:

a rectangular hole dug beneath the road.

Valleys should use:

- broad slopes
- asymmetric sides
- erosion
- natural drainage direction
- changing slope angle
- rock exposure where appropriate
- natural toe transitions


============================================================
REQUIRED TERRAIN FAMILIES
============================================================

Create at minimum:

A. SHALLOW VALLEY

BridgeValley_Shallow_L_40m

BridgeValley_Shallow_R_40m

BridgeValley_Shallow_Both_40m


B. MEDIUM VALLEY

BridgeValley_Medium_L_40m

BridgeValley_Medium_R_40m

BridgeValley_Medium_Both_40m


C. DEEP VALLEY

BridgeValley_Deep_L_40m

BridgeValley_Deep_R_40m

BridgeValley_Deep_Both_40m


D. VALLEY TRANSITIONS

BridgeValley_In_L_40m

BridgeValley_In_R_40m

BridgeValley_Run_L_40m

BridgeValley_Run_R_40m

BridgeValley_Out_L_40m

BridgeValley_Out_R_40m


E. APPROACH / ABUTMENT

BridgeApproach_L

BridgeApproach_R

BridgeAbutmentTerrain_L

BridgeAbutmentTerrain_R


F. UNDER-BRIDGE CONTEXT

BridgeUnderTerrain_A

BridgeUnderTerrain_B

BridgePierGround_A

BridgePierGround_B


G. DRAINAGE / RAVINE

BridgeRavine_A

BridgeRavine_B

BridgeDryRiverbed_A

BridgeDryRiverbed_B


============================================================
OPTIONAL 20 M MODULES
============================================================

If useful for bridge transition composition, create:

BridgeValley_In_20m

BridgeValley_Out_20m

Do not create 20 m versions of every asset without reason.


============================================================
VALLEY DEPTH TARGETS
============================================================

Use these as art-direction guidance.

SHALLOW:

approximately 2–4 m below road elevation.


MEDIUM:

approximately 5–9 m below road elevation.


DEEP:

approximately 10–16 m below road elevation.

Adjust based on actual bridge/pier visual requirements.

Do not create extreme canyon depths in this small phase.


============================================================
VALLEY WIDTH
============================================================

Valley terrain should extend far enough that from chase camera:

the player does not see an artificial terrain termination.

Suggested local environment reach:

approximately 60–100 m from road centreline

where needed.

Do NOT attach a gigantic kilometre mesh to every 40 m module.

Use:

near context modules

+

separate distant vista/filler where required.


============================================================
VALLEY SLOPES
============================================================

Use believable slope ratios.

Shallow / soil slopes:

roughly 1 vertical : 2–4 horizontal.

Steeper sections may expose:

rock

soil

retaining structure

Do not make grassy near-vertical walls.


============================================================
ASYMMETRY
============================================================

Natural valley profiles should not be perfectly mirrored.

Create variation such as:

left side steeper

right side broader

one rock exposure

one drainage channel

one flatter floodplain section


============================================================
BRIDGE APPROACH EMBANKMENTS
============================================================

Create context that visually explains:

normal terrain
→ bridge abutment
→ valley.

Remember:

road itself stays level.

The approach terrain should fall away from the road rather than push the road upward.


============================================================
8.7 M OVERLAP REQUIREMENT
============================================================

The P2 Bridges Start / End structures extend up to approximately:

8.7 m

into neighboring open-road chunks.

Therefore:

leave sufficient clear terrain interface around Bridge Start / End.

Do not place:

large rock

tree zone

steep terrain face

or terrain wall

where it would intersect that designed overlap.


============================================================
ABUTMENT TERRAIN
============================================================

Build terrain context that receives:

Bridge_Abutment_A/B

and:

Bridge_WingWall_L/R

naturally.

Do NOT merge frozen bridge geometry into terrain.

Allow controlled visual overlap to avoid gaps.


============================================================
ABUTMENT QA
============================================================

Check:

- no visible hole
- no floating wing wall
- no terrain piercing through bridge concrete
- no impossible slope
- no obvious rectangular cut


============================================================
PIER GROUND CONTEXT
============================================================

Create simple terrain context around bridge piers.

Examples:

- compacted ground
- exposed soil
- shallow erosion
- rock pad
- dry drainage gravel

Do not build concrete foundations that belong to the frozen Bridge kit.


============================================================
UNDER-BRIDGE TERRAIN
============================================================

Create terrain that looks believable from:

driver view

side cinematic view

high chase view

and beneath bridge where visible.

Avoid:

perfect flat green ground under a large bridge.


============================================================
RAVINE SYSTEM
============================================================

Create:

BridgeRavine_A

BridgeRavine_B

Suitable for:

narrower erosion channel beneath a bridge.

Use:

- rocky sides
- gravel base
- soil
- modest vegetation-compatible ledges

Do not make a giant fantasy canyon.


============================================================
DRY RIVERBED SYSTEM
============================================================

Create:

BridgeDryRiverbed_A

BridgeDryRiverbed_B

Use:

- gravel
- stones/rock influence
- soil
- channel shape
- flood-wash pattern

Do NOT create actual Unity water.

Do NOT create fluid simulation.


============================================================
OPTIONAL STREAM CHANNEL
============================================================

You may create:

BridgeStreamBed_A

as terrain geometry only.

Do not create production water.

Unity may later add water if desired.


============================================================
ROCK USAGE
============================================================

Prefer compatibility with frozen P1 Terrain rock language.

Do not modify or duplicate frozen rock sources unnecessarily.

You may create terrain-integrated rock surfaces where needed.

If linking P1 rock assets for QA:

do not export them in this package.


============================================================
TERRAINBLEND
============================================================

Use the SAME semantics:

R grass

G soil

B rock

A gravel

Weights should remain normalized / sensible.

Do not redefine channels.


============================================================
VEGETATIONMASK
============================================================

Store vegetation placement compatibility in UV1 using the same convention:

U = density

V = dryness


============================================================
VEGETATION RULES
============================================================

Higher density:

- broad grass slopes
- valley shoulders
- stable flats


Reduced density:

- erosion areas
- soil
- dry slopes


Zero / near-zero:

- riverbed centre
- gravel drainage channel
- steep rock
- abutment contact area
- pier bases
- retaining interface


============================================================
BRIDGE CLEARANCE MASK
============================================================

Do not allow future vegetation directly beneath / inside:

- bridge structure
- abutment
- wing walls
- piers
- drainage outlets

Provide appropriate mask values.


============================================================
VALLEY SEAM STRATEGY
============================================================

Modules intended for sequential 40 m streaming must remain seam-compatible.

Use a controlled boundary profile at:

Snap_Start

Snap_End

Recommended seam-safe distance:

first 2 m

last 2 m

where appropriate.

Do not create dramatic valley changes exactly at a module edge.


============================================================
SNAP POINTS
============================================================

40 m modules:

Snap_Start
Snap_End

exactly:

40.000 m


20 m modules if created:

exactly:

20.000 m


============================================================
LONG VALLEY COMPOSITION
============================================================

Create a modular sequence such as:

Flat
→ Valley_In
→ Valley_Run
→ Valley_Run
→ Valley_Out
→ Flat

The terrain should form one coherent low area.


============================================================
BRIDGE SEQUENCE QA
============================================================

Build temporary QA using LINKED frozen Bridge assets.

Recommended:

Open Road
→ Bridge Start
→ Bridge 40
→ Bridge 40
→ Bridge End

with:

Valley_In
→ Valley_Run
→ Deep/Medium Valley
→ Valley_Run
→ Valley_Out

under/around it.


============================================================
HERO OVERPASS QA
============================================================

Also test frozen:

Overpass_Hero

with terrain context.

Do not bury:

V-piers

or eliminate their silhouette.


============================================================
DO NOT OVER-TERRAIN OVERPASSES
============================================================

Overpasses generally need:

normal roadside terrain

not deep valleys.

Deep valley kit is primarily for:

Bridge Deck runs.

Use appropriate context.


============================================================
TERRAIN MATERIALS
============================================================

Reuse the P1 Terrain visual language.

Create source materials only if needed:

MAT_BridgeTerrain_Grass

MAT_BridgeTerrain_Soil

MAT_BridgeTerrain_Rock

MAT_BridgeTerrain_Gravel

MAT_BridgeTerrain_DryGround

Do not create a completely different biome.


============================================================
TEXTURES
============================================================

Prefer reusing / referencing compatible P1 Terrain source textures.

If a new texture is genuinely required, keep it minimal.

Potential:

T_BridgeTerrain_Riverbed_2K

T_BridgeTerrain_Erosion_2K

Do NOT create an entirely new terrain texture library.


============================================================
UV STRATEGY
============================================================

Use world-planar / repeatable UV strategy compatible with P1 Terrain.

No 0–1 stretching across an entire valley.


============================================================
MACRO VARIATION
============================================================

Use broad material variation so large valley slopes do not look tiled.

Keep restrained.


============================================================
GEOMETRY STRATEGY
============================================================

Use geometry for:

- valley silhouette
- slope changes
- erosion form
- riverbed profile
- abutment transition

Use textures / normals for:

- small stones
- soil grain
- fine cracks
- small erosion


============================================================
TRIANGLE GUIDANCE
============================================================

Guidance only.

40 m valley side LOD0:

approximately 2k–8k tris

depending on depth/profile.

LOD1:

roughly 30–50%

LOD2:

roughly 10–20%

Very broad filler/vista:

hundreds to low thousands.

Do NOT pad geometry.


============================================================
LOD STRATEGY
============================================================

Create LODs for:

- medium valley
- deep valley
- ravine
- riverbed
- large approach terrain
- distant context

Do not create unnecessary LODs for tiny simple pieces.


============================================================
LOD SILHOUETTE
============================================================

Preserve:

- valley depth
- major slope profile
- ravine shape
- riverbed width
- approach silhouette

Do not flatten the valley at distance.


============================================================
COLLISION
============================================================

Gameplay road collision remains P0.

Terrain collision is optional/minimal.

Create simple terrain collision only where useful for:

- off-road fall
- bridge-side environment
- accessible under-bridge region

Do not overbuild.


============================================================
COLLIDER EXAMPLES
============================================================

Optional:

Collision_BridgeValley_L

Collision_BridgeValley_R

Collision_BridgeUnderTerrain

Collision_BridgeRavine

Keep substantially simpler than visuals.


============================================================
PIER COLLISION
============================================================

Pier collision belongs to P2 Bridges.

Do not duplicate bridge pier colliders in this terrain-context package.


============================================================
CHECKPOINTS
============================================================

Create:

blend/bridgeTerrain_01_blockout.blend

blend/bridgeTerrain_02_valleys.blend

blend/bridgeTerrain_03_approaches.blend

blend/bridgeTerrain_04_ravine_riverbed.blend

blend/bridgeTerrain_05_materials_masks.blend

blend/bridgeTerrain_06_lods_collision.blend

blend/bridgeTerrain_07_export_ready.blend


============================================================
COLLECTIONS
============================================================

Use:

BRIDGE_TERRAIN_MASTER

BT_VALLEY_SHALLOW

BT_VALLEY_MEDIUM

BT_VALLEY_DEEP

BT_TRANSITIONS

BT_APPROACH

BT_ABUTMENT

BT_UNDERBRIDGE

BT_RAVINE

BT_RIVERBED

BT_VISTAS

BT_COLLIDERS

BT_QA

BT_PRESENTATION


============================================================
ORIGINS
============================================================

Runtime modules:

use road-grid aligned start reference.

Standalone valley/under-bridge pieces:

use documented road-relative origin.

Maintain consistency.


============================================================
TRANSFORMS
============================================================

Production assets:

Scale 1,1,1

No negative scale.

Clean transforms.


============================================================
NORMALS
============================================================

Ground:

smooth natural shading.

Rock transitions:

controlled harder forms where appropriate.

Avoid visible grid/faceted terrain.


============================================================
QA CAMERAS
============================================================

Inspect from:

driver

low chase

high chase

bridge side

under bridge

distant cinematic


============================================================
DRIVER VIEW QA
============================================================

From road:

the bridge must feel elevated because the terrain drops away.

Do not expose obvious world holes.


============================================================
CHASE VIEW QA
============================================================

Check:

- valley depth
- abutment integration
- wing-wall transition
- distant ground
- vegetation-ready slopes


============================================================
SIDE VIEW QA
============================================================

This is important.

A bridge viewed from the side should show:

road/deck
→ support
→ valley floor

with believable proportions.


============================================================
UNDER-BRIDGE QA
============================================================

Check:

- pier ground contact
- riverbed/ravine
- no floating terrain
- no terrain piercing structure


============================================================
REQUIRED PREVIEWS
============================================================

Create at minimum:

previews/P2_BT_shallow_valley.png

previews/P2_BT_medium_valley.png

previews/P2_BT_deep_valley.png

previews/P2_BT_valley_transition.png

previews/P2_BT_bridge_approach.png

previews/P2_BT_abutment_transition.png

previews/P2_BT_underbridge.png

previews/P2_BT_ravine.png

previews/P2_BT_dry_riverbed.png

previews/P2_BT_driver_view.png

previews/P2_BT_chase_view.png

previews/P2_BT_high_chase.png

previews/P2_BT_side_view.png

previews/P2_BT_bridge_full_sequence.png

previews/P2_BT_asset_library.png


============================================================
VISUAL HARD GATES
============================================================

A. BRIDGE NECESSITY

Terrain must make the bridge look structurally necessary.

B. ROAD HEIGHT

Road must remain visually and physically level.

C. VALLEY FORM

Valleys must not look like rectangular excavations.

D. TERRAIN CONNECTION

Bridge abutments / wing walls must meet terrain convincingly.

E. SUPPORT CONTACT

Piers must sit naturally relative to ground.

F. DEPTH

Medium / deep valleys must read clearly at gameplay distance.

G. STREAMING

Modular transitions must not show obvious seams.

H. FROZEN SOURCES

No existing phase may be edited.


============================================================
AUTOMATION
============================================================

Store scripts in:

scripts/

Suggested:

bridgeTerrain_build.py

bridgeTerrain_materials.py

bridgeTerrain_lods.py

bridgeTerrain_validate.py

bridgeTerrain_render.py

bridgeTerrain_export.py


============================================================
EXPORT ORIENTATION
============================================================

Use the proven pipeline established by previous phases.

Target:

Unity +Y up

Unity +Z forward


============================================================
FBX EXPORTS
============================================================

Create:

exports/bridgeTerrain_complete.fbx

and logical groups:

exports/BridgeValleys.fbx

exports/BridgeValleyTransitions.fbx

exports/BridgeApproaches.fbx

exports/BridgeUnderTerrain.fbx

exports/BridgeRavines.fbx

exports/BridgeRiverbeds.fbx

exports/BridgeTerrainCollision.fbx

Approximately 6–8 FBXs is enough.

Do not create dozens of tiny exports.


============================================================
EXPORT EXCLUSIONS
============================================================

DO NOT EXPORT:

- P0 Road
- P1 Props
- P1 Terrain
- P1 Vegetation
- P1 Tunnel
- P2 Bridges
- cars
- QA assembly
- cameras
- lights
- presentation objects


============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

Re-import EVERY exported FBX into a clean Blender scene.

Validate:

- names
- hierarchy
- dimensions
- +Y Unity up
- +Z Unity forward
- module lengths
- UVs
- TerrainBlend
- VegetationMask UV1
- materials
- LODs
- colliders
- snap points
- triangle counts
- normals

Target:

0 errors.


============================================================
VALIDATION REPORT
============================================================

Create:

reports/P2_bridgeTerrain_validation.txt

Check at minimum:

1. frozen source integrity
2. shallow valley
3. medium valley
4. deep valley
5. In/Run/Out system
6. approach context
7. abutment transition
8. under-bridge terrain
9. ravine
10. dry riverbed
11. bridge-start 8.7 m overlap clearance
12. road stays level
13. TerrainBlend compatibility
14. VegetationMask compatibility
15. seam safety
16. snap distances
17. LODs
18. colliders
19. UVs
20. materials
21. QA bridge sequence
22. FBX export
23. FBX re-import

Target:

0 errors

0 critical warnings.


============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P2_bridgeTerrain_geometry.json

Include:

- asset
- family
- dimensions
- valley depth
- valley width
- LOD
- triangles
- vertices
- materials
- TerrainBlend status
- VegetationMask status
- collider status
- snap references


============================================================
MATERIAL / MASK REPORT
============================================================

Create:

reports/P2_bridgeTerrain_materials_masks.md

Document:

- reused terrain materials
- new materials if any
- texture sources
- UV scale
- TerrainBlend convention
- VegetationMask convention
- bridge exclusion zones


============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P2_bridgeTerrain_export_manifest.json


============================================================
SOURCE INTEGRITY CHECK
============================================================

At completion:

rehash frozen dependencies.

Create:

reports/P2_bridgeTerrain_source_integrity_check.md

Confirm:

P0 Road unchanged

P1 Props unchanged

P1 Terrain unchanged

P1 Vegetation unchanged

P1 Tunnel unchanged

P2 Bridges unchanged

Cars unchanged

Target:

BYTE-FOR-BYTE UNCHANGED.


============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/


============================================================
UNITY IMPORT NOTES
============================================================

Create:

UnityTransfer/README/BRIDGE_TERRAIN_IMPORT_NOTES.md

Document:

1. phase
2. scale
3. orientation
4. relationship to frozen P1 Terrain
5. relationship to P2 Bridges
6. shallow valley
7. medium valley
8. deep valley
9. transitions
10. approaches
11. abutment terrain
12. under-bridge terrain
13. ravines
14. riverbeds
15. LOD naming
16. TerrainBlend
17. VegetationMask
18. colliders
19. snap points
20. Bridge Start/End 8.7 m overlap requirement
21. excluded QA assets


============================================================
BRIDGE TERRAIN COMPOSITION GUIDE
============================================================

Create:

UnityTransfer/README/BRIDGE_TERRAIN_COMPOSITION_GUIDE.md

Document example:

OPEN ROAD
→ Bridge Start
→ Bridge 40
→ Bridge 40
→ Bridge End
→ OPEN ROAD

paired with:

Flat / Fill
→ Valley_In
→ Valley_Run
→ Valley_Run
→ Valley_Out
→ Flat / Fill

Explain that:

the Bridge and Terrain Context remain separate runtime layers.

Do not prescribe Unity code.


============================================================
PERFORMANCE GUIDE
============================================================

Create:

UnityTransfer/README/BRIDGE_TERRAIN_PERFORMANCE_GUIDE.md

Document concepts for:

PC:

higher terrain LOD
larger vista range
more rock/erosion detail


Mobile:

earlier terrain LOD
simpler under-bridge ground
reduced distant detail
aggressive vista simplification

Do not claim measured Unity performance.


============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P2-BLENDER-01A COMPLETE UNTIL:

1. P0 unchanged.
2. Props unchanged.
3. P1 Terrain unchanged.
4. Vegetation unchanged.
5. Tunnel unchanged.
6. P2 Bridges unchanged.
7. Cars unchanged.

8. Shallow valley exists.
9. Medium valley exists.
10. Deep valley exists.

11. Valley_In exists.
12. Valley_Run exists.
13. Valley_Out exists.

14. Bridge approach terrain exists.
15. Abutment terrain exists.
16. Under-bridge terrain exists.

17. Ravine exists.
18. Dry riverbed exists.

19. Bridge Start/End 8.7 m overlap is respected.

20. Road remains straight.
21. Road remains level.

22. TerrainBlend compatible.
23. VegetationMask compatible.

24. Bridge piers do not float.
25. Terrain does not intersect bridge structures incorrectly.

26. Shallow valley visual gate passes.
27. Medium valley visual gate passes.
28. Deep valley visual gate passes.

29. Driver view passes.
30. Chase view passes.
31. High-chase passes.
32. Side view passes.
33. Under-bridge view passes.

34. Full bridge sequence passes.

35. Module seams pass.
36. Snap distances pass.

37. Useful LODs exist.
38. Simple collision exists where needed.

39. FBXs export.
40. Every FBX re-imports.

41. Validation reports 0 errors.
42. No frozen linked asset is accidentally exported.

43. Geometry report exists.
44. Material/mask report exists.
45. Export manifest exists.
46. Integrity report passes.

47. UnityTransfer exists.
48. Import notes exist.
49. Composition guide exists.
50. Performance guide exists.


============================================================
FINAL FREEZE
============================================================

After validation passes:

create:

reports/P2_bridgeTerrain_FINAL_FREEZE.md

Record:

- final source blend
- FBXs
- textures
- reports
- UnityTransfer
- hashes
- validation result
- known limitations

Then treat:

environment/P2_BridgeTerrainContext/

as FROZEN.


============================================================
FINAL REPORT
============================================================

Create:

reports/P2_bridgeTerrain_FINAL_REPORT.md

Return ONE report covering:

1. discovery
2. integrity
3. reason for addendum
4. shallow valley
5. medium valley
6. deep valley
7. valley depths
8. valley widths
9. In/Run/Out system
10. bridge approaches
11. abutment context
12. 8.7 m overlap handling
13. under-bridge terrain
14. pier-ground context
15. ravines
16. dry riverbeds
17. optional stream-bed context
18. TerrainBlend
19. VegetationMask
20. materials
21. textures
22. UV strategy
23. LODs
24. triangle counts
25. collision
26. snap points
27. driver QA
28. chase QA
29. high-chase QA
30. side-view QA
31. full bridge sequence
32. checkpoint files
33. previews
34. FBX files
35. FBX re-import
36. validation
37. UnityTransfer
38. import notes
39. composition guide
40. performance guide
41. freeze report
42. known limitations
43. recommended next Blender phase


============================================================
STOP CONDITION
============================================================

After P2-BLENDER-01A is complete:

STOP.

DO NOT START:

- City
- Mountain / Coastal
- another terrain expansion
- Bridge modification
- Tunnel modification
- Vehicle work
- Traffic
- Unity integration

Do NOT modify any frozen source.

Do NOT launch or install Unity.

FINISH ONLY THE SMALL BRIDGE TERRAIN CONTEXT ADDENDUM,
VALIDATE,
EXPORT,
RE-IMPORT,
PACKAGE,
FREEZE,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P2-BLENDER-02 — Premium City / Urban Highway Environment
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Urban Environment Artist, Modular Building Artist, Hard-Surface Artist
and Real-Time Optimization Specialist with 10+ years of production
experience creating cities and highway environments for racing/open-world games.

You are working on a BLENDER-ONLY asset-production workstation.

There is NO Unity project on this machine.

DO NOT:

- search for Unity
- install or launch Unity
- create Unity prefabs
- create Unity shaders
- create Unity scripts
- modify RoadStreamer
- modify gameplay
- modify frozen Road
- modify frozen Props
- modify frozen Terrain
- modify frozen Vegetation
- modify frozen Tunnel
- modify frozen Bridges
- modify frozen Bridge Terrain Context
- modify finished vehicles
- start Mountain / Coastal
- start traffic rebuild

Your responsibility is:

P2-BLENDER-02 — PREMIUM CITY / URBAN HIGHWAY ENVIRONMENT

Complete:

DISCOVERY
→ SOURCE INTEGRITY BASELINE
→ READ-ONLY REFERENCE LINKING
→ CITY ART DIRECTION
→ URBAN HIGHWAY CORRIDOR BLOCKOUT
→ BUILDING MODULAR SYSTEM
→ NEAR BUILDINGS
→ MID-DISTANCE BUILDINGS
→ SKYLINE BUILDINGS
→ PARKING / SERVICE STRUCTURES
→ URBAN RETAINING / NOISE STRUCTURES
→ STREET / HIGHWAY EDGE ARCHITECTURE
→ ROOFTOP KIT
→ WINDOW / FACADE SYSTEM
→ NIGHT-LIGHTING SOURCE DATA
→ MATERIAL / TRIM SYSTEM
→ UVs
→ LODs
→ HLOD-READY CLUSTERS
→ SIMPLE COLLIDERS
→ CITY QA STRIP
→ DAY / GOLDEN / NIGHT PREVIEWS
→ FBX EXPORT
→ RE-IMPORT VALIDATION
→ UNITY TRANSFER PACKAGE
→ FINAL REPORT
→ FREEZE
→ STOP


============================================================
CURRENT WORKSPACE
============================================================

Root:

/Users/meetshah/Documents/blender


============================================================
FROZEN SOURCES
============================================================

The following are complete and immutable:

environment/P0_RoadFoundation/

environment/P1_Props/

environment/P1_Terrain/

environment/P1_Vegetation/

environment/P1_Tunnel/

environment/P2_Bridges/

environment/P2_BridgeTerrainContext/

Finished vehicle directories are also frozen.


============================================================
FINAL REFERENCE SOURCES
============================================================

Terrain:

environment/P1_Terrain/blend/terrain_09_final_frozen.blend

Vegetation:

environment/P1_Vegetation/blend/vegetation_09_final_frozen.blend

Tunnel:

environment/P1_Tunnel/blend/tunnel_07_export_ready.blend

Bridges:

environment/P2_Bridges/blend/bridges_07_export_ready.blend

Bridge Terrain Context:

environment/P2_BridgeTerrainContext/blend/bridgeTerrain_07_export_ready.blend


============================================================
CRITICAL FREEZE RULE
============================================================

DO NOT MODIFY ANY FROZEN SOURCE.

Use them only as:

LINKED
READ-ONLY
REFERENCE

If City work exposes a problem in Road, Props, Terrain, Tunnel, Bridges or
another frozen phase:

DOCUMENT IT.

Do NOT edit the frozen phase.


============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P2_City/

Use:

P2_City/
├── blend/
├── exports/
├── textures/
│   ├── facades/
│   ├── windows/
│   ├── trim/
│   ├── concrete/
│   ├── metal/
│   ├── roofs/
│   ├── decals/
│   └── signs/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/


============================================================
PRIMARY GOAL
============================================================

Create a reusable PREMIUM URBAN HIGHWAY ENVIRONMENT.

This is NOT a full open-world city.

The player remains on the existing highway.

The City kit must make the highway feel like it passes through a believable,
modern urban area.

Target:

- premium racing-game city backdrop
- strong city silhouette
- believable near-road architecture
- layered depth
- readable night windows
- efficient repeated buildings
- scalable mobile / PC asset hierarchy


============================================================
IMPORTANT SCOPE LIMIT
============================================================

Do NOT build:

- full drivable city street network
- intersections
- traffic-light gameplay
- pedestrians
- explorable building interiors
- subway network
- hundreds of unique buildings
- complete downtown map

This phase is specifically:

URBAN HIGHWAY ENVIRONMENT + CITY BACKDROP.


============================================================
CORE ROAD RULE
============================================================

The existing highway remains:

STRAIGHT
LEVEL
40 M MODULAR

Do not change:

road geometry
lane count
lane width
road elevation
RoadStreamer assumptions


============================================================
KNOWN ROAD SYSTEM
============================================================

Runtime road:

40.000 m main module

20.000 m secondary module

4 lanes × 3.60 m

Carriageway:

14.40 m

Unity target:

+Y up
+Z forward

Blender:

+Z up
road direction -Y


============================================================
CITY VISUAL TARGET
============================================================

Target:

MODERN INTERNATIONAL CITY / URBAN HIGHWAY

Suitable for:

- downtown approach
- business district
- mixed-use corridor
- commercial highway edge
- urban overpass
- night racing environment

Avoid making it strongly identifiable as one real-world city.

Do not copy branded buildings.


============================================================
VISUAL PROBLEM TO AVOID
============================================================

The existing city was previously identified as weak because of:

- wrong-scale windows
- flat building boxes
- little facade depth
- no layered skyline
- poor night readability

This phase must specifically solve those problems.


============================================================
CITY DEPTH LAYERS
============================================================

Design the city in THREE major distance layers:

A. NEAR URBAN

approximately:

20–80 m from highway

Requires:

real geometry
facade depth
service structures
parking
walls
visible rooftop details


B. MID CITY

approximately:

80–250 m

Requires:

optimized building geometry
strong silhouettes
simplified facade depth


C. FAR SKYLINE

approximately:

250 m–1.5+ km

Requires:

very low-cost skyline meshes
strong silhouettes
window/emission support
almost no small geometry


============================================================
SOURCE INTEGRITY BASELINE
============================================================

Before starting:

hash:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel

P2 Bridges

P2 BridgeTerrainContext

Vehicles

Create:

reports/P2_city_source_baseline.json

At completion re-hash and verify byte-for-byte unchanged.


============================================================
PHASE 01 — DISCOVERY
============================================================

Link read-only:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P1 Tunnel

P2 Bridges

P2 BridgeTerrainContext if useful

Optional Hypercar for scale

Inspect:

- chase camera
- road corridor width
- sign/gantry heights
- city visibility distance
- roadside terrain
- overpass relationship
- tunnel transition relationship

Create:

reports/P2_city_discovery.md


============================================================
DISCOVERY REPORT MUST INCLUDE
============================================================

1. urban corridor width
2. near-building setback
3. mid-city distance
4. far skyline distance
5. building height ranges
6. window size convention
7. floor-height convention
8. facade module width
9. material strategy
10. window-night strategy
11. LOD strategy
12. HLOD strategy
13. collision policy


============================================================
CITY SCALE STANDARD
============================================================

Use realistic architectural proportions.

General floor-to-floor height:

office:
approximately 3.6–4.2 m

residential:
approximately 3.0–3.4 m

ground-floor commercial:
approximately 4–5 m

Do not use tiny windows repeated hundreds of times at unrealistic scale.


============================================================
WINDOW SCALE
============================================================

Office windows:

roughly 1.2–2.0 m wide depending on facade.

Residential windows:

roughly 0.9–1.5 m.

Curtain-wall panels:

approximately 1.2–1.8 m bay rhythm.

Use consistent scale.

This is a HARD visual requirement.


============================================================
REQUIRED BUILDING FAMILIES
============================================================

Create approximately:

12–16 PRIMARY BUILDING ARCHETYPES.

Do not create 50 unique buildings.

Required categories:

A. OFFICE

Office_Tower_A

Office_Tower_B

Office_Midrise_A

Office_Midrise_B


B. RESIDENTIAL

Residential_Tower_A

Residential_Tower_B

Residential_Midrise_A

Residential_Midrise_B


C. COMMERCIAL

Commercial_Block_A

Commercial_Block_B

Hotel_Midrise_A


D. INDUSTRIAL / SERVICE

Warehouse_Urban_A

ServiceBuilding_A

UtilityBuilding_A


E. LANDMARK

City_Landmark_A

City_Landmark_B


============================================================
BUILDING VARIANTS
============================================================

Each important family should support restrained variants using:

- facade material swap
- rooftop variation
- window pattern
- floor count
- podium option
- side-wall treatment

Do NOT create variants by only scaling XYZ.


============================================================
NEAR BUILDINGS
============================================================

Near buildings require:

real facade depth

Use geometry for:

- major window recesses
- balcony slabs where applicable
- podium
- facade fins
- major columns
- rooftop silhouette
- loading/service areas

Use materials/normals for:

- fine mullions
- bolts
- tiny joints
- small bricks


============================================================
MID BUILDINGS
============================================================

Mid-distance buildings should prioritize:

- strong shape
- correct floor rhythm
- readable window bands
- rooftop silhouette

Use less geometry than Near buildings.


============================================================
FAR BUILDINGS
============================================================

Far skyline buildings should be VERY efficient.

Use:

- silhouette
- major setbacks
- roof shape
- window/emission texture

Avoid:

individual window geometry
balcony geometry
small AC units


============================================================
LANDMARK BUILDINGS
============================================================

Create two original urban landmarks:

City_Landmark_A

City_Landmark_B

They must be:

recognizable at distance

but:

not copies of real skyscrapers.


============================================================
LANDMARK QA
============================================================

Must remain distinguishable at:

200 m

500 m

1000 m

through silhouette.


============================================================
MODULAR FACADE SYSTEM
============================================================

Create reusable facade modules where appropriate.

Examples:

Facade_OfficeGlass_4m

Facade_OfficeConcrete_4m

Facade_Residential_4m

Facade_Commercial_4m

Facade_Service_4m


============================================================
FACADE MODULE RULE
============================================================

Facade modularity should reduce texture/geometry duplication.

Do not create every building from unique unrelated textures.


============================================================
PODIUM SYSTEM
============================================================

Create reusable:

Building_Podium_A

Building_Podium_B

Commercial_Podium_A

ParkingPodium_A

Useful for:

tower base variation
street-scale massing
service/loading areas


============================================================
PARKING STRUCTURES
============================================================

Create:

ParkingGarage_A

ParkingGarage_B

ParkingGarage_RampVisual_A

ParkingGarage_Roof_A

Do not create drivable internal parking gameplay.

Exterior only.


============================================================
PARKING GARAGE DESIGN
============================================================

Use believable:

- floor heights
- open ventilation bays
- columns
- parapets
- ramp hint
- lighting fixtures

Avoid giant empty rectangular holes.


============================================================
URBAN HIGHWAY EDGE STRUCTURES
============================================================

Create:

Urban_RetainingWall_A

Urban_RetainingWall_B

Urban_NoiseWall_A

Urban_NoiseWall_B

Urban_ServiceWall_A

Urban_Fence_A


============================================================
NOISE BARRIERS
============================================================

Support:

solid acoustic wall

and:

transparent/acrylic variant

Avoid excessive transparency layering.


============================================================
URBAN EMBANKMENT RELATIONSHIP
============================================================

Use frozen Terrain as reference.

Do not modify terrain.

City structures should visually connect using:

retaining walls
service walls
building podiums
landscape strips


============================================================
UTILITY / SERVICE ASSETS
============================================================

Create reusable:

City_UtilityCabinet_A

City_UtilityCabinet_B

City_TransformerBox_A

City_ServiceDoor_A

City_VentUnit_A

Use only where useful.

Do not duplicate P1 Props unnecessarily.


============================================================
ROOFTOP KIT
============================================================

Create:

Roof_HVAC_A

Roof_HVAC_B

Roof_Vent_A

Roof_Chiller_A

Roof_WaterTank_A

Roof_Antenna_A

Roof_ServiceRoom_A

Roof_Railing_A


============================================================
ROOFTOP DETAIL RULE
============================================================

Near buildings:

more rooftop detail.

Mid:

selected silhouette features.

Far:

almost none.


============================================================
ROOFTOP PERFORMANCE
============================================================

Do not place 100 unique AC units on every building.

Create clustered rooftop assemblies where useful.


============================================================
WINDOW SYSTEM
============================================================

This is a MAJOR phase requirement.

Create shared window atlas:

T_City_Windows_2K

Support categories:

office bright

office dark

residential warm

residential cool

commercial

hotel

utility / dark


============================================================
WINDOW NIGHT MASK
============================================================

Create separate mask such as:

T_City_WindowEmissionMask_2K

or pack efficiently into a channel.

Unity later controls emission.

Do NOT bake final lighting intensity.


============================================================
WINDOW RANDOMIZATION SUPPORT
============================================================

Provide data that can allow:

some windows on

some windows off

warm/cool variation

floor variation

Do not create one giant uniformly glowing facade.


============================================================
WINDOW PATTERN REQUIREMENT
============================================================

At night:

a building must NOT look like every window is lit.

Target mixed occupancy.


============================================================
WINDOW DEPTH
============================================================

Near buildings:

window recess may be actual geometry.

Mid/far:

use texture/parallax-ready representation.

Do not build thousands of deep window boxes on distant towers.


============================================================
OPTIONAL INTERIOR PARALLAX SUPPORT
============================================================

If useful, create a basic source atlas suitable for later Unity fake interiors.

Example:

T_City_InteriorRooms_2K

But DO NOT implement Unity parallax shader here.

Keep scope controlled.


============================================================
FACADE MATERIAL SYSTEM
============================================================

Create shared material families:

MAT_City_Concrete

MAT_City_ConcreteDark

MAT_City_Glass

MAT_City_Window

MAT_City_Brick

MAT_City_Stone

MAT_City_PaintedMetal

MAT_City_Galvanized

MAT_City_Roof

MAT_City_AsphaltRoof

MAT_City_Signage


============================================================
CITY TRIM SHEET
============================================================

Create:

T_City_Trim_2K

Maps:

BaseColor

Normal

Roughness

Metallic

AO


Suggested strips:

concrete frame

painted metal

dark metal

window mullion

balcony edge

roof parapet

service door

vent

utility metal

sign frame


============================================================
FACADE ATLAS
============================================================

Create shared atlas where appropriate:

T_City_Facade_2K

Use for:

office panels

residential walls

commercial panels

service walls


============================================================
BRICK / STONE
============================================================

Create or use tileable:

T_City_Brick_2K

T_City_Stone_2K

only if required.

Do not create unnecessary textures.


============================================================
GLASS
============================================================

Blender preview glass should be simple.

Unity will later implement final:

reflection

fresnel

window emission

interior fake

Do not build a complex Blender-only glass solution.


============================================================
GLASS COLOUR
============================================================

Avoid:

solid bright blue skyscrapers.

Use restrained neutral / slightly cool glass.


============================================================
NIGHT CITY DATA
============================================================

Prepare:

emission masks

window states

sign emissive masks

roof warning-light source surfaces

Do NOT create final Unity light sources.


============================================================
BUILDING SIGNAGE
============================================================

Use invented generic signage only.

No copyrighted real brands.

Create optional:

City_SignPanel_A

City_SignPanel_B

City_RooftopSign_A


============================================================
GROUND / SERVICE AREAS
============================================================

Create urban context assets such as:

ServiceLot_A

ParkingSurface_A

BuildingLoadingArea_A

UrbanConcretePad_A

Do not duplicate the road.


============================================================
SIDEWALKS
============================================================

Because the highway is not pedestrian gameplay:

keep sidewalks/service paths simple.

Create only where they improve building grounding.


============================================================
STREETLIGHTS
============================================================

Do not recreate the full P1 streetlight kit.

Reuse linked Props in QA.

Create city-specific facade/under-building light fixture geometry only if needed.


============================================================
URBAN OVERPASS RELATIONSHIP
============================================================

Use frozen P2 Bridges.

A city QA scene should include at least one:

Hero or Standard Overpass.

Do not modify bridge assets.


============================================================
TUNNEL RELATIONSHIP
============================================================

City should also be compatible with a tunnel approach.

One QA composition may use:

Urban Highway
→ Tunnel Portal

without modifying Tunnel.


============================================================
URBAN VEGETATION
============================================================

Reuse P1 Vegetation as linked QA content.

Do not create new trees here.

City vegetation should be sparser and more controlled than open highway.

Examples:

small roadside tree

median planting

building setback shrubs

but no new vegetation assets.


============================================================
CITY BLOCK / CLUSTER SYSTEM
============================================================

Create reusable city clusters.

Required:

CityCluster_Near_A

CityCluster_Near_B

CityCluster_Near_C

CityCluster_Mid_A

CityCluster_Mid_B

CityCluster_Mid_C

CityCluster_Skyline_A

CityCluster_Skyline_B


============================================================
CLUSTER PURPOSE
============================================================

Clusters are intended to reduce:

runtime placement complexity

and enable:

HLOD / combined distant representations later.


============================================================
DO NOT BAKE EVERYTHING TOGETHER
============================================================

Keep individual buildings available.

Clusters should be additional composition assets, not destructive replacements.


============================================================
HLOD-READY OUTPUT
============================================================

Prepare very-low-cost representations for:

Near cluster distant state

Mid clusters

Skyline clusters

Do NOT implement Unity HLOD system.

Provide source meshes that Unity can use.


============================================================
CITY LOD STRATEGY
============================================================

Near Building:

LOD0
LOD1
LOD2
LOD3 if useful

Mid Building:

LOD0
LOD1
LOD2

Far Skyline:

LOD0
possibly LOD1


============================================================
BUILDING TRIANGLE GUIDANCE
============================================================

Guidance only.

Near tower:

LOD0:
approximately 8k–25k

LOD1:
~40–60%

LOD2:
~15–30%

LOD3:
~5–10%


Midrise:

LOD0:
approximately 4k–15k


Far tower:

approximately 200–2k depending silhouette.


Do NOT pad geometry.


============================================================
LOD PRIORITY
============================================================

Remove first:

small rooftop detail

tiny facade relief

small balconies

small service parts


Preserve:

overall mass

setbacks

roof shape

podium

major facade rhythm


============================================================
HLOD / SKYLINE TRIANGLE TARGET
============================================================

A complete far skyline cluster should remain extremely efficient.

Prefer:

few thousand triangles per cluster

rather than:

hundreds of thousands.


============================================================
COLLIDERS
============================================================

Since buildings are roadside/background:

use minimal collision.

Near accessible structures may have:

Collision_Building_Box

Collision_ParkingGarage

Collision_UrbanWall


Do not create per-window collision.


============================================================
BUILDING ORIGINS
============================================================

Building:

ground centre or consistent building-grid corner.

Clusters:

documented cluster origin.

Rooftop props:

mount point.


============================================================
TRANSFORMS
============================================================

All production assets:

Scale 1,1,1

No negative scales.

Clean transforms.


============================================================
UV STRATEGY
============================================================

Buildings must support:

shared atlases

tileable materials

trim sheet

Do NOT unwrap each skyscraper into one unique 4K texture.


============================================================
TEXEL DENSITY
============================================================

Near assets:

higher consistent density.

Mid:

moderate.

Far:

lower.

Document strategy.


============================================================
CITY MODULE LENGTH RELATIONSHIP
============================================================

Buildings themselves do NOT need to be exactly 40 m long.

However, city corridor compositions should align sensibly with the:

40 m RoadStreamer rhythm.


============================================================
CITY CHUNK GUIDES
============================================================

Create optional city placement reference empties every:

40 m

in QA composition.

Do not force every building footprint to fit 40 m.


============================================================
NEAR BUILDING SETBACK
============================================================

Do not put towers directly against highway shoulder.

Recommended near-building frontage generally begins:

approximately 20–35 m from centreline

depending on:

wall

terrain

service road visual

noise barrier

Use actual linked environment measurements.


============================================================
SKYLINE DISTANCE
============================================================

Place far skyline examples:

approximately 300–1000+ m away.

The purpose is:

depth

not:

close detail.


============================================================
CITY QA ENVIRONMENT
============================================================

Create approximately:

600–1000 m

temporary city-highway presentation.

Use LINKED:

P0 Road

P1 Props

P1 Terrain

P1 Vegetation

P2 Bridges

Optional Tunnel transition


============================================================
QA COMPOSITION EXAMPLE
============================================================

Open Highway
→ suburban edge
→ midrise buildings
→ Hero / Standard Overpass
→ dense business district
→ landmark view
→ urban retaining/noise walls
→ optional Tunnel approach


============================================================
DO NOT EXPORT QA WORLD
============================================================

The assembled city strip is QA only.

Export individual assets / approved clusters.


============================================================
DRIVER CAMERA QA
============================================================

Check:

- building scale
- window scale
- noise walls
- skyline depth
- sign visibility
- road visibility


============================================================
CHASE CAMERA QA
============================================================

Check:

- near facade depth
- building repetition
- rooftop silhouette
- skyline layering


============================================================
HIGH CHASE QA
============================================================

Check:

- city composition
- repeated footprint patterns
- roofs
- parking/service areas
- skyline density


============================================================
SIDE CINEMATIC QA
============================================================

Use one side perspective showing:

highway

near building layer

mid layer

far skyline

to verify proper depth.


============================================================
DAY QA
============================================================

Buildings should not look:

flat

overly reflective

uniform grey

plastic.


============================================================
GOLDEN HOUR QA
============================================================

Check:

facade depth

long shadows

glass response

silhouette.


============================================================
NIGHT QA — CRITICAL
============================================================

Create a Blender-only night preview.

Night city must show:

- varied lit/unlit windows
- warm/cool occupancy differences
- identifiable building silhouettes
- rooftop/service accents

Avoid:

every window ON

giant glowing facade

neon overload.


============================================================
RAIN / OVERCAST PREVIEW
============================================================

Optional but useful.

Do not modify frozen Road.

Presentation-only environment.


============================================================
REPETITION QA
============================================================

At normal chase-camera distance:

the same building asset should not obviously repeat every 40–80 m.

Use:

rotation where physically valid

facade variation

roof variation

spacing

cluster variation

height variation


============================================================
REQUIRED PREVIEWS
============================================================

Create at minimum:

previews/P2_city_blockout.png

previews/P2_city_building_library.png

previews/P2_city_office_library.png

previews/P2_city_residential_library.png

previews/P2_city_commercial_library.png

previews/P2_city_parking_service.png

previews/P2_city_landmarks.png

previews/P2_city_rooftop_library.png

previews/P2_city_facade_closeup.png

previews/P2_city_windows_scale.png

previews/P2_city_near_cluster.png

previews/P2_city_mid_cluster.png

previews/P2_city_skyline.png

previews/P2_city_driver_view.png

previews/P2_city_chase_view.png

previews/P2_city_high_chase.png

previews/P2_city_side_depth.png

previews/P2_city_overpass.png

previews/P2_city_golden_hour.png

previews/P2_city_night.png

previews/P2_city_full_environment.png


============================================================
VISUAL HARD GATES
============================================================

A. WINDOW SCALE

Windows must look correctly scaled relative to cars and floors.

B. BUILDING DEPTH

Near buildings must not read as flat boxes with textures.

C. SILHOUETTES

Major building families must have distinct forms.

D. SKYLINE

Far skyline must provide believable depth.

E. REPETITION

Repeated assets must not be obvious during gameplay.

F. NIGHT

Window lighting must look varied and believable.

G. MATERIALS

Glass, concrete, metal and brick must be distinguishable.

H. ROOFTOPS

High-chase view must not reveal empty flat roofs everywhere.

I. PERFORMANCE DESIGN

Far buildings must be extremely cheap.

J. ROAD VISIBILITY

City must not compromise gameplay road readability.


============================================================
CHECKPOINTS
============================================================

Create:

blend/city_01_blockout.blend

blend/city_02_buildings.blend

blend/city_03_facades_rooftops.blend

blend/city_04_clusters.blend

blend/city_05_materials_uv.blend

blend/city_06_lods_hlod_collision.blend

blend/city_07_export_ready.blend

Never overwrite earlier checkpoints.


============================================================
COLLECTIONS
============================================================

Use:

CITY_MASTER

CITY_OFFICE

CITY_RESIDENTIAL

CITY_COMMERCIAL

CITY_SERVICE

CITY_PARKING

CITY_LANDMARKS

CITY_FACADES

CITY_ROOFTOPS

CITY_URBAN_WALLS

CITY_CLUSTERS_NEAR

CITY_CLUSTERS_MID

CITY_SKYLINE

CITY_COLLIDERS

CITY_QA

CITY_PRESENTATION


============================================================
AUTOMATION
============================================================

Store scripts in:

scripts/

Suggested:

city_build.py

city_materials.py

city_lods.py

city_clusters.py

city_validate.py

city_render.py

city_export.py


============================================================
FBX EXPORT ORIENTATION
============================================================

Use the established proven export pipeline.

Target:

Unity +Y up

Unity +Z forward

Do not alter established axis settings.


============================================================
FBX EXPORTS
============================================================

Create logical groups such as:

exports/city_complete.fbx

exports/City_Office.fbx

exports/City_Residential.fbx

exports/City_Commercial.fbx

exports/City_ServiceParking.fbx

exports/City_Landmarks.fbx

exports/City_UrbanStructures.fbx

exports/City_Rooftops.fbx

exports/City_Clusters.fbx

exports/City_Skyline.fbx

exports/City_Collision.fbx

Approximately 9–12 FBXs is acceptable.


============================================================
EXPORT EXCLUSIONS
============================================================

DO NOT EXPORT:

- Road
- Props
- Terrain
- Vegetation
- Tunnel
- Bridges
- Bridge Terrain Context
- vehicles
- QA city strip
- cameras
- Blender lights
- temporary helpers


============================================================
FBX RE-IMPORT VALIDATION
============================================================

MANDATORY.

Re-import EVERY exported FBX into a clean Blender scene.

Validate:

- names
- hierarchy
- dimensions
- +Y Unity up
- +Z Unity forward
- materials
- UVs
- trim usage
- window scale
- LODs
- HLOD-ready objects
- colliders
- triangle counts
- normals

Target:

0 errors.


============================================================
VALIDATION REPORT
============================================================

Create:

reports/P2_city_validation.txt

Check at minimum:

1. frozen source integrity
2. required building families
3. office assets
4. residential assets
5. commercial assets
6. service assets
7. parking
8. landmarks
9. rooftop kit
10. urban walls/noise barriers
11. window scale
12. floor-height scale
13. facade modules
14. materials
15. trim sheet
16. window atlas
17. emission mask
18. UVs
19. LODs
20. HLOD-ready clusters
21. skyline assets
22. colliders
23. transforms
24. pivots
25. day QA
26. night QA
27. repetition QA
28. export selection
29. FBX re-import

Target:

0 errors

0 critical warnings.

Do NOT warn just because an asset is below triangle guidance.


============================================================
GEOMETRY REPORT
============================================================

Create:

reports/P2_city_geometry.json

For every major asset record:

- asset name
- family
- dimensions
- floors
- height
- footprint
- LOD
- triangles
- vertices
- material count
- window system
- collider
- intended distance layer


============================================================
MATERIAL REPORT
============================================================

Create:

reports/P2_city_materials.md

Document:

- materials
- facade atlas
- window atlas
- emission masks
- trim sheet
- glass
- concrete
- brick
- stone
- metal
- roof
- night-light strategy
- UV scale
- Unity expectations


============================================================
CITY SCALE REPORT
============================================================

Create:

reports/P2_city_scale_audit.md

Include:

- floor heights
- window widths
- window heights
- facade bay widths
- door scale
- parking floor heights
- guardrail/car comparisons

This is important because the previous city had wrong-scale architectural
details.


============================================================
EXPORT MANIFEST
============================================================

Create:

reports/P2_city_export_manifest.json


============================================================
SOURCE INTEGRITY CHECK
============================================================

At completion verify:

P0 Road unchanged

P1 Props unchanged

P1 Terrain unchanged

P1 Vegetation unchanged

P1 Tunnel unchanged

P2 Bridges unchanged

P2 BridgeTerrainContext unchanged

Vehicles unchanged

Create:

reports/P2_city_source_integrity_check.md

Target:

BYTE-FOR-BYTE UNCHANGED.


============================================================
UNITY TRANSFER PACKAGE
============================================================

Create:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/


============================================================
CITY IMPORT NOTES
============================================================

Create:

UnityTransfer/README/CITY_IMPORT_NOTES.md

Document:

1. orientation
2. scale
3. building families
4. distance-layer strategy
5. FBX list
6. building LODs
7. cluster/HLOD sources
8. window atlas
9. emission mask
10. materials
11. trim sheet
12. rooftop assets
13. parking/service assets
14. urban structures
15. collision
16. intended highway setback
17. night-light expectations
18. excluded QA assets


============================================================
CITY MATERIAL GUIDE
============================================================

Create:

UnityTransfer/README/CITY_MATERIAL_GUIDE.md

Document:

- facade materials
- glass
- window masks
- night emission
- fake interiors if provided
- trim sheet
- concrete
- metal
- recommended GPU instancing/material sharing


============================================================
CITY PLACEMENT GUIDE
============================================================

Create:

UnityTransfer/README/CITY_PLACEMENT_GUIDE.md

Document recommended layers:

Near:
20–80 m

Mid:
80–250 m

Far:
250 m–1.5 km+

Explain:

- setback principles
- cluster use
- skyline use
- overpass relationship
- tunnel relationship
- vegetation usage
- repetition avoidance

Do not prescribe Unity code.


============================================================
CITY PERFORMANCE GUIDE
============================================================

Create:

UnityTransfer/README/CITY_PERFORMANCE_GUIDE.md

Document concepts:

PC:

- Near LOD0/1
- Mid LOD1/2
- Far skyline meshes
- richer window effects


Mobile:

- aggressive LODs
- earlier HLOD
- simplified windows
- restricted transparent glass
- fewer rooftop details
- skyline clusters
- GPU instancing/material sharing

Do not claim measured Unity FPS.


============================================================
FINAL COMPLETION GATE
============================================================

DO NOT DECLARE P2-BLENDER-02 COMPLETE UNTIL:

1. All frozen sources are unchanged.

2. At least 12 primary building archetypes exist.

3. Office family exists.
4. Residential family exists.
5. Commercial family exists.
6. Service/industrial family exists.
7. Parking structures exist.
8. Two landmark buildings exist.

9. Near buildings contain real facade depth.
10. Mid buildings are optimized.
11. Far skyline buildings are highly optimized.

12. Window scale passes.
13. Floor heights pass.
14. Door/building scale passes.

15. Rooftop kit exists.
16. Parking/service kit exists.
17. Urban retaining/noise wall kit exists.

18. Window atlas exists.
19. Window emission mask exists.
20. Night variation data exists.

21. Shared materials exist.
22. City trim sheet exists.
23. UVs are valid.

24. Near clusters exist.
25. Mid clusters exist.
26. Skyline clusters exist.
27. HLOD-ready source meshes exist.

28. LODs exist where required.
29. LOD silhouettes remain acceptable.

30. Simple colliders exist where required.

31. Day driver view passes.
32. Day chase view passes.
33. High-chase roof view passes.
34. Side-depth view passes.
35. Golden Hour passes.
36. Night passes.

37. City does not look like identical boxes.
38. Building repetition is acceptable.
39. Skyline depth is convincing.
40. Road remains readable.

41. FBXs export.
42. Every FBX re-imports.
43. Re-import materials match.
44. Re-import hierarchy matches.
45. Re-import triangle counts match.

46. Validation reports 0 errors.
47. No frozen linked source is accidentally exported.

48. Geometry report exists.
49. Material report exists.
50. Scale audit exists.
51. Export manifest exists.
52. Integrity report passes.

53. UnityTransfer exists.
54. CITY_IMPORT_NOTES exists.
55. CITY_MATERIAL_GUIDE exists.
56. CITY_PLACEMENT_GUIDE exists.
57. CITY_PERFORMANCE_GUIDE exists.


============================================================
FINAL FREEZE
============================================================

After validation:

create:

reports/P2_city_FINAL_FREEZE.md

Record:

- final blend
- FBXs
- textures
- reports
- UnityTransfer
- validation
- important hashes
- known limitations

Then treat:

environment/P2_City/

as FROZEN.


============================================================
FINAL REPORT
============================================================

Create:

reports/P2_city_FINAL_REPORT.md

Return ONE complete report covering:

1. discovery
2. source integrity
3. city art direction
4. urban corridor strategy
5. near/mid/far distance layers
6. building families
7. office buildings
8. residential buildings
9. commercial buildings
10. service buildings
11. parking structures
12. landmarks
13. building heights
14. window scale
15. floor-height audit
16. facade system
17. rooftop system
18. urban walls/noise barriers
19. utility/service kit
20. materials
21. trim sheet
22. facade atlas
23. window atlas
24. emission mask
25. night-lighting strategy
26. glass strategy
27. UV strategy
28. texel density
29. LOD strategy
30. triangle counts
31. clusters
32. HLOD-ready assets
33. skyline system
34. collision
35. day QA
36. driver QA
37. chase QA
38. high-chase QA
39. side-depth QA
40. golden-hour QA
41. night QA
42. repetition QA
43. overpass integration QA
44. tunnel approach QA if performed
45. checkpoints
46. previews
47. FBXs
48. FBX re-import
49. validation
50. UnityTransfer
51. import notes
52. material guide
53. placement guide
54. performance guide
55. freeze report
56. known limitations
57. recommended next Blender phase


============================================================
STOP CONDITION
============================================================

After P2-BLENDER-02 CITY is complete:

STOP.

DO NOT START:

- Mountain / Coastal
- another City expansion
- player-car rebuild
- traffic rebuild
- Unity integration
- Unity city shaders
- Unity city lighting

Do NOT modify any frozen phase.

Do NOT launch or install Unity.

BUILD THE COMPLETE URBAN HIGHWAY CITY KIT,
VALIDATE,
EXPORT,
RE-IMPORT,
PACKAGE FOR UNITY,
FREEZE,
RETURN THE FINAL REPORT,
AND STOP.
````


====================================================================================================
# SPEC: P3-BLENDER-01 — Premium Mountain & Coastal Highway Biome
====================================================================================================

````text
ACT AS:

A senior AAA Environment Artist, Blender Technical Artist,
Terrain Artist, Rock/Cliff Artist, Coastal Environment Artist and
Real-Time Optimization Specialist with 10+ years of production experience
creating premium racing-game mountain and coastal environments.

You are working on a BLENDER-ONLY workstation.

There is NO Unity project on this machine.

Your responsibility is:

P3-BLENDER-01 — PREMIUM MOUNTAIN & COASTAL HIGHWAY BIOME

This is a NEW OPTIONAL BIOME EXPANSION.

Do NOT modify any completed/frozen environment phase.

Complete:

DISCOVERY
→ SOURCE INTEGRITY BASELINE
→ READ-ONLY REFERENCE LINKING
→ BIOME ART DIRECTION
→ MOUNTAIN TERRAIN BLOCKOUT
→ MOUNTAIN SLOPES
→ CLIFFS
→ ROCK CUTS
→ SCREE / TALUS
→ MOUNTAIN VISTAS
→ COASTAL TERRAIN BLOCKOUT
→ COASTAL CLIFFS
→ ROCKY SHORE
→ BEACH / PEBBLE SHORE
→ HEADLANDS
→ COASTAL VISTAS
→ WATERLINE REFERENCE SYSTEM
→ SCENIC OVERLOOKS
→ BIOME TRANSITIONS
→ TERRAIN MATERIAL/MASK SUPPORT
→ VEGETATION MASK SUPPORT
→ LODs
→ SIMPLE COLLIDERS
→ QA HIGHWAY SEQUENCES
→ PREVIEWS
→ FBX EXPORT
→ CLEAN RE-IMPORT VALIDATION
→ UNITY TRANSFER
→ FINAL REPORT
→ FREEZE
→ STOP


============================================================
WORKSPACE
============================================================

Root:

/Users/meetshah/Documents/blender


============================================================
FROZEN SOURCES
============================================================

Treat all of these as IMMUTABLE:

environment/P0_RoadFoundation/

environment/P1_Props/

environment/P1_Terrain/

environment/P1_Vegetation/

environment/P1_Tunnel/

environment/P2_Bridges/

environment/P2_BridgeTerrainContext/

environment/P2_City/

All finished vehicle assets are also frozen.

Use only LINKED / READ-ONLY references.


============================================================
CRITICAL ROAD RULE
============================================================

The gameplay road remains:

STRAIGHT

LEVEL

40 M MODULAR

Secondary:

20 M

Do NOT create:

curved gameplay road

mountain switchbacks

road slopes

road climbs

road descents

banked bends

coastal road curves

spline roads

The ENVIRONMENT creates the feeling of mountain/coastal driving.

The ROAD DOES NOT CHANGE.


============================================================
NEW PHASE ROOT
============================================================

Create:

/Users/meetshah/Documents/blender/environment/P3_MountainCoastal/

Structure:

P3_MountainCoastal/
├── blend/
├── exports/
├── textures/
│   ├── mountain/
│   ├── coastal/
│   ├── rock/
│   ├── ground/
│   └── decals/
├── previews/
├── reports/
├── scripts/
├── references/
└── UnityTransfer/


============================================================
SOURCE INTEGRITY
============================================================

Hash every frozen dependency before work.

Create:

reports/P3_MC_source_baseline.json

At final completion:

rehash everything.

Target:

BYTE-FOR-BYTE UNCHANGED.


============================================================
PRIMARY GOAL
============================================================

Create two related premium highway environment styles:

A. MOUNTAIN HIGHWAY

B. COASTAL HIGHWAY

They should share the existing road architecture while creating visually
different driving environments.


============================================================
MOUNTAIN EXPERIENCE
============================================================

The Mountain environment should feel like:

highway cutting through large natural terrain

with:

large slopes

rock cuts

cliffs

ridges

scree

talus

distant mountains

occasional retaining / safety infrastructure

Do NOT make it look like:

small rocks randomly placed beside a flat highway.


============================================================
COASTAL EXPERIENCE
============================================================

The Coastal environment should feel like:

highway running beside elevated coastline

with:

sea-facing cliffs

rocky shore

headlands

beach/pebble sections

distant coastal formations

open horizon

scenic overlooks

Do NOT build the final ocean rendering system.


============================================================
NO FINAL WATER IMPLEMENTATION
============================================================

Blender may create:

waterline reference

shoreline geometry

sea-floor edge context

preview water plane

BUT:

final ocean

waves

foam

reflections

water shader

underwater system

must NOT be implemented here.

Unity owns those systems.


============================================================
MOUNTAIN REQUIRED ASSETS
============================================================

Create at minimum:

MountainSlope_Low_A

MountainSlope_Low_B

MountainSlope_Medium_A

MountainSlope_Medium_B

MountainSlope_Steep_A

MountainSlope_Steep_B

MountainCliff_A

MountainCliff_B

MountainCliff_C

MountainRockCut_A

MountainRockCut_B

MountainRockCut_C

MountainTalus_A

MountainTalus_B

MountainScree_A

MountainScree_B

MountainRockCluster_A

MountainRockCluster_B

MountainRockCluster_C

MountainRidge_A

MountainRidge_B

MountainRidge_C

MountainVista_A

MountainVista_B

MountainVista_C

MountainDistantRange_A

MountainDistantRange_B


============================================================
MOUNTAIN TRANSITIONS
============================================================

Create:

Mountain_In_40m

Mountain_Run_40m

Mountain_Out_40m

Mountain_In_20m

Mountain_Out_20m

These must allow:

existing terrain
→ mountain environment
→ mountain run
→ existing terrain

without modifying P1 Terrain.


============================================================
MOUNTAIN ROAD CUT
============================================================

Create believable highway cut conditions:

one-sided rock cut

two-sided rock cut

lower soil cut

tall cliff cut

Do not narrow the road.


============================================================
ROCK ART DIRECTION
============================================================

Rock formations should have:

large primary masses

secondary fracture planes

irregular crest

undercuts

talus

weathering

Avoid:

stacked cubes

uniform noise

repeating vertical stripes

perfectly flat cliff tops.


============================================================
ROCK VARIETY
============================================================

Create meaningful variations.

For example:

A:
broad massive rock planes

B:
fractured angular formation

C:
layered / diagonal geological formation

Keep visual language compatible with P1 Terrain while substantially expanding
the mountain scale.


============================================================
MOUNTAIN DISTANCE LAYERS
============================================================

Use:

NEAR:
0–100 m

MID:
100–500 m

FAR:
500 m–2 km+

Far mountain meshes must be extremely efficient.


============================================================
COASTAL REQUIRED ASSETS
============================================================

Create at minimum:

CoastalSlope_A

CoastalSlope_B

CoastalSlope_C

CoastalCliff_A

CoastalCliff_B

CoastalCliff_C

CoastalRockShore_A

CoastalRockShore_B

CoastalRockShore_C

CoastalPebbleBeach_A

CoastalPebbleBeach_B

CoastalSandStrip_A

CoastalHeadland_A

CoastalHeadland_B

CoastalHeadland_C

CoastalRockStack_A

CoastalRockStack_B

CoastalIsland_A

CoastalIsland_B

CoastalVista_A

CoastalVista_B

CoastalDistantLand_A


============================================================
COASTAL TRANSITIONS
============================================================

Create:

Coastal_In_40m

Coastal_Run_40m

Coastal_Out_40m

Coastal_In_20m

Coastal_Out_20m


============================================================
COASTAL ROAD POSITION
============================================================

Support compositions such as:

MOUNTAIN SIDE | HIGHWAY | COAST

and:

SLOPE | HIGHWAY | CLIFF DROP | COAST

and:

OPEN LAND | HIGHWAY | BEACH / SHORE

Road itself stays unchanged.


============================================================
COASTAL DROP-OFF
============================================================

Create believable terrain below the highway.

Do not simply terminate terrain at the road edge.

Use:

cliff shoulder

sloping ground

rock shelf

lower shore

distant horizon.


============================================================
WATERLINE REFERENCES
============================================================

Create documented empties:

Waterline

ShorelineReference

CoastalHorizon

SeaFloorReference

Use a consistent world elevation.

Do not make water part of gameplay geometry.


============================================================
SHORELINE
============================================================

Create shoreline geometry that supports future Unity:

foam

wetness

wave intersection

without implementing those effects.

Include irregular shoreline shape.

Avoid perfectly straight coastline edges.


============================================================
SCENIC OVERLOOK
============================================================

Create:

MountainOverlook_A

CoastalOverlook_A

These are environment context modules only.

Use existing P1 safety props as linked QA references where possible.


============================================================
DO NOT DUPLICATE PROPS
============================================================

Do not recreate:

guardrails

signs

streetlights

barriers

generic safety props

if P1 Props already provides them.

Create only biome-specific infrastructure where genuinely required.


============================================================
BIOME-SPECIFIC INFRASTRUCTURE
============================================================

You may create:

Mountain_RockfallFence_A

Mountain_RockfallFence_B

Mountain_DrainChannel_A

Coastal_CliffFence_A

Coastal_SeaWall_A

Coastal_RockBarrier_A

Keep this kit small.


============================================================
VEGETATION
============================================================

P1 Vegetation remains frozen.

Use it read-only in QA.

Mountain:

use conifers / shrubs / grass appropriately.

Coastal:

use grass / shrubs sparingly.

Do NOT create another full vegetation library.


============================================================
TERRAINBLEND
============================================================

Maintain:

R = grass

G = soil

B = rock

A = gravel

Do not change semantics.


============================================================
VEGETATIONMASK
============================================================

Maintain UV1:

U = vegetation density

V = dryness


============================================================
VEGETATION EXCLUSION
============================================================

Near-zero vegetation on:

vertical cliffs

rock cuts

scree-heavy regions

shoreline

beaches

waterline

large exposed rock

safety infrastructure zones.


============================================================
MATERIAL SYSTEM
============================================================

Prefer compatible P1 Terrain materials where appropriate.

Create only what the new biome actually needs.

Possible new shared materials:

MAT_MC_MountainRock

MAT_MC_DryRock

MAT_MC_Scree

MAT_MC_CoastalRock

MAT_MC_WetShoreSource

MAT_MC_Pebble

MAT_MC_Sand

MAT_MC_SeaWall


============================================================
TEXTURES
============================================================

Keep texture additions controlled.

Possible:

T_MC_MountainRock_2K

T_MC_CoastalRock_2K

T_MC_Pebble_2K

T_MC_Sand_2K

Maps as appropriate:

BaseColor

Normal

Roughness

AO

No massive unique texture library.


============================================================
WET SHORE SUPPORT
============================================================

Prepare coastal rock so Unity can later implement:

wet darkening

waterline wetness

foam proximity

Do not create Blender-dependent final wet shaders.


============================================================
UV STRATEGY
============================================================

Use repeatable/world-scaled terrain UVs.

No single stretched 0–1 UV over giant cliffs.


============================================================
LOD STRATEGY
============================================================

Create LODs for:

large mountain slopes

cliffs

rock cuts

rock clusters

headlands

coastal cliffs

shore formations

islands

mountain vistas

coastal vistas.


============================================================
LOD RULE
============================================================

Preserve:

major silhouette

cliff profile

ridge line

headland profile

rock-stack identity

Remove:

small fractures

small rocks

tiny ledges

fine erosion.


============================================================
TRIANGLE GUIDANCE
============================================================

Guidance only.

Near large cliff LOD0:

approximately 8k–30k

Medium terrain module:

approximately 3k–12k

Rock cluster:

approximately 1k–6k

Far ridge:

approximately 500–4k

Distant mountain:

hundreds to a few thousand.

Do NOT pad geometry.


============================================================
COLLISION
============================================================

Road collision remains P0.

Create simple environment collision only where needed:

Collision_MountainCliff

Collision_MountainSlope

Collision_CoastalCliff

Collision_Overlook

Do not use dense visual meshes for collision.


============================================================
SEAM SYSTEM
============================================================

Streaming terrain modules must be seam-safe.

40 m modules:

Snap_Start

Snap_End

exactly 40.000 m

20 m modules:

exactly 20.000 m.

Use standardized boundary profiles.


============================================================
MOUNTAIN QA STRIP
============================================================

Create approximately:

600–800 m

temporary QA sequence:

Open Terrain
→ Mountain_In
→ Rock Cut
→ Mountain Run
→ Cliff Section
→ Scenic Overlook
→ Mountain_Out
→ Open Terrain


============================================================
COASTAL QA STRIP
============================================================

Create approximately:

600–800 m

temporary QA:

Open Terrain
→ Coastal_In
→ Coastal Cliff
→ Headland
→ Rocky Shore
→ Coastal Overlook
→ Coastal_Run
→ Coastal_Out


============================================================
MIXED QA
============================================================

Create one optional composition:

mountain side
+
highway
+
coastal drop

to validate a premium scenic highway look.


============================================================
CAMERA QA
============================================================

Validate from:

driver

low chase

high chase

side cinematic

long-distance approach.


============================================================
REQUIRED PREVIEWS
============================================================

Create at minimum:

previews/P3_MC_mountain_library.png

previews/P3_MC_mountain_rockcut.png

previews/P3_MC_mountain_cliff.png

previews/P3_MC_mountain_driver.png

previews/P3_MC_mountain_chase.png

previews/P3_MC_mountain_vista.png

previews/P3_MC_coastal_library.png

previews/P3_MC_coastal_cliff.png

previews/P3_MC_coastal_shore.png

previews/P3_MC_coastal_headland.png

previews/P3_MC_coastal_driver.png

previews/P3_MC_coastal_chase.png

previews/P3_MC_coastal_vista.png

previews/P3_MC_mixed_highway.png

previews/P3_MC_full_mountain_sequence.png

previews/P3_MC_full_coastal_sequence.png


============================================================
CHECKPOINTS
============================================================

Create:

blend/mountainCoastal_01_blockout.blend

blend/mountainCoastal_02_mountain.blend

blend/mountainCoastal_03_coastal.blend

blend/mountainCoastal_04_transitions.blend

blend/mountainCoastal_05_materials_masks.blend

blend/mountainCoastal_06_lods_collision.blend

blend/mountainCoastal_07_export_ready.blend

Never overwrite an earlier official checkpoint.


============================================================
FBX EXPORTS
============================================================

Create:

exports/mountainCoastal_complete.fbx

exports/MountainTerrain.fbx

exports/MountainCliffs.fbx

exports/MountainRocks.fbx

exports/MountainVistas.fbx

exports/CoastalTerrain.fbx

exports/CoastalShore.fbx

exports/CoastalVistas.fbx

exports/MC_Infrastructure.fbx

exports/MC_Collision.fbx

Keep logical grouping.


============================================================
DO NOT EXPORT
============================================================

Exclude:

P0 Road

Props

P1 Terrain

Vegetation

Tunnel

Bridges

Bridge Terrain

City

Vehicles

QA scenes

preview water

cameras

lights.


============================================================
CLEAN FBX RE-IMPORT
============================================================

MANDATORY.

Re-import every FBX into a clean Blender scene.

Validate:

names

hierarchy

orientation

scale

dimensions

UVs

materials

TerrainBlend

VegetationMask

LOD naming

colliders

snap references

triangle counts

normals.

Target:

0 errors.


============================================================
REPORTS
============================================================

Create:

reports/P3_MC_validation.txt

reports/P3_MC_geometry.json

reports/P3_MC_materials_masks.md

reports/P3_MC_export_manifest.json

reports/P3_MC_source_integrity_check.md

reports/P3_MC_FINAL_FREEZE.md

reports/P3_MC_FINAL_REPORT.md


============================================================
UNITY TRANSFER
============================================================

Create:

UnityTransfer/
├── FBX/
├── Textures/
├── Reports/
└── README/

Create:

UnityTransfer/README/MC_IMPORT_NOTES.md

UnityTransfer/README/MC_PLACEMENT_GUIDE.md

UnityTransfer/README/MC_WATERLINE_GUIDE.md

UnityTransfer/README/MC_PERFORMANCE_GUIDE.md


============================================================
UNITY NOTES MUST STATE
============================================================

Unity owns:

final water

waves

foam

reflection

fog

lighting

weather

terrain shaders

LODGroup components

streaming integration

quality tiers

performance profiling.


============================================================
FINAL COMPLETION GATE
============================================================

Do NOT declare complete until:

- all frozen sources remain byte-identical
- Mountain slopes exist
- Mountain cliffs exist
- Rock cuts exist
- Scree/talus exists
- Mountain vistas exist
- Coastal cliffs exist
- Rocky shore exists
- Beach/pebble context exists
- Headlands exist
- Coastal vistas exist
- waterline references exist
- Mountain In/Run/Out exists
- Coastal In/Run/Out exists
- road remains straight
- road remains level
- 40 m snaps are exact
- 20 m snaps are exact
- TerrainBlend is compatible
- VegetationMask is compatible
- useful LODs exist
- simple collision exists where needed
- Mountain driver QA passes
- Mountain chase QA passes
- Coastal driver QA passes
- Coastal chase QA passes
- distant vista QA passes
- all FBXs export
- every FBX cleanly re-imports
- validation reports 0 errors
- UnityTransfer is complete
- integrity check passes.


============================================================
FINAL FREEZE
============================================================

Final source:

blend/mountainCoastal_07_export_ready.blend

After successful validation:

treat:

environment/P3_MountainCoastal/

as FROZEN.


============================================================
STOP CONDITION
============================================================

After P3-BLENDER-01 completes:

STOP.

Do NOT:

start another environment biome

modify City

modify Bridges

modify Tunnel

modify Terrain

modify Road

start Unity integration.

Return the final report and stop.
````

