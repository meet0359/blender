# Checkpoint 08 material handoff

All 27 production materials have `_Engine` names. Original shader assets and separate source maps remain in the hidden reference library and texture folders. `engine_material_manifest.json` lists each material's images. FBX stores material identities and UV channels, but cannot preserve the full Blender node graph; rebuild the materials from this manifest and the packed maps.

## UV mapping

Channel 0 (`UVMap`) is the unchanged atlas UV map. Channel 1 (`UV_Game`) encodes the former per-object physical scale divided by material `tile_m` into loop UV coordinates. Channel 2 (`UV_Rotor`) encodes radial disc sampling as `(0, 8 * sqrt(local_y² + local_z²))`. No production shader requires an object attribute, object coordinates, or procedural scale. Original authoring properties remain as documentation only.

Use channel 1 for regular tile BaseColor, ORM and micro-normal textures. Brake-disc BaseColor/ORM use channel 2; its micro-normal uses channel 1. Tire atlas BaseColor, tire ORM, and all composite tire/interior normal maps use channel 0. Interior BaseColor/ORM tile maps use channel 1. GLB declares these texture coordinate channels explicitly. FBX material importers may default to channel 0; reassign the correct channel during material recreation.

Tire lettering is baked into `game/tire_BaseColor.png`; tire AO is packed into `game/tire_ORM.png`. Interior/tire micro-plus-detail normal arithmetic is realized in the composite atlas maps. Normal strength remains 0.3 for these detail materials, 0.65 for speaker detail. The original standalone display/mirror detail maps retain their prior strength. Tinted color variants are baked with explicit linear/sRGB conversion. Source textures remain untouched.

## ORM and AO

All packed maps are non-color data: R ambient occlusion, G roughness, B metallic. Twelve material tile sets have packed ORM maps; tire has an additional atlas ORM map. Interior isolated cavity AO atlases remain separate on channel 0 because combining atlas AO with channel-1 tile roughness/metallic would require resampling different coordinate domains. Use the retained isolated AO maps for additional interior cavity shading where the engine supports it. Tile ORM AO and tire AO are provided through the exporter-recognized `glTF Material Output` Occlusion socket. Do not multiply AO into base color again.

## Glass

`MAT_Glass_LOD_Thin_Engine` uses linear tint (0.83, 0.91, 0.95), opacity 0.18, roughness 0.025, metallic 0, transmission weight 1 and IOR 1.46. Geometry is the existing single optical sheet. This Principled approximation replaces the original transparent/Fresnel custom graph. Recreate as a thin transparent surface in the engine; avoid double darkening from simultaneously applying full alpha blending and transmission. FBX does not preserve the original optical behavior. glTF stores transmission/IOR extensions, whose rendering varies by viewer.

## Other Blender features

Clear coat, sheen, emission strength, transmission and IOR are retained in the Blender engine variants. GLB uses KHR material extensions where applicable; FBX needs explicit recreation. Emissive light meshes remain geometry, not exported light objects. Alpha sorting, thin glass, clear-coat appearance and material culling require a target-engine visual check. This phase creates no Unity assets or physics settings.

## Normal convention

Normal maps remain OpenGL tangent-space +Y. No silent green-channel inversion was performed. Leave green unflipped as the initial later Unity import setting; verify the imported result against the Blender reference before enabling any pipeline-specific flip. Mark ORM and normals as non-color data, and BaseColor as sRGB. FBX meshes include tangents; GLB render primitives include tangents, while untextured collision pieces do not require them.

## Geometry and portability

FBX and GLB use temporary triangle copies with custom normals explicitly transferred. Zero-area and duplicate triangles are excluded only from export copies; `export_copy_cleanup.json` records each difference. The editable meshes and original UVMap remain unchanged. This avoids importer validation changing triangle topology unpredictably. FBX references external textures through relative paths; distribute `exports/` together with sibling `textures/`. GLB embeds images. UV layer names may become generic on GLB re-import, but channel order and coordinates are validated.

The complete FBX and GLB contain overlapping LOD groups. Show one LOD group at a time; these files do not implement automatic LOD switching. Collision meshes are independent physics candidates, not render meshes. Engines must disable their rendering and set each hull as a convex compound collider. COM is an initial tuning reference only. Fixed calipers do not roll; rotor assemblies roll with the wheels. A later steering carrier can steer both the rolling wheel and fixed caliper together without changing these axle pivots.
