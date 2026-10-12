# Hypercar FBX re-export provenance

The frozen Hypercar release (`new_car/`) has no FBX on disk any more; its Phase 9 export folder `new_car/exports/` is gone. The FBX in `FBX/` was re-exported on 2026-10-11 with the established, unchanged Phase 9 pipeline (`new_car/scripts/export_fbx.py`), run on an isolated scratch copy of the hash-verified source. No frozen file was opened for writing.

| Item | Value |
|---|---|
| Source checkpoint | `hypercar_07_colliders_hierarchy.blend` SHA-1 `5f991548919f5f19c65d3ed10eb44c95578a2005` (matches the release manifest) |
| Export checkpoint | `hypercar_08_unity_export.blend` SHA-1 `f8897c50a177b42a1c06526df5dd16f772c84324` (frozen original, matches the release manifest) |
| Textures | 48 / 48 PNG match the release manifest SHA-1 |
| Blender | 5.2.2 LTS |
| New FBX | `hypercar_complete_unity.fbx` 22,085,340 bytes, SHA-1 `cf5b184335ac1af7ccda6eb407748d902b15657f`, 308 objects |
| Original FBX (2026-10-06, not on disk) | 22,078,332 bytes, SHA-1 `58f0edbf6fe59d297df902e11f0ab4bb92252463`, 308 objects |
| Re-import validation (`fbx_validate.py`) | hypercar_complete_unity.fbx: 85 PASS, 0 WARNING, 0 ERROR |
| Validation data vs the frozen 2026-10-06 run | identical (`REEXPORT_fbx_validation_complete.json` vs `fbx_validation_complete.json`) |

The byte size differs by about 7 KB because each FBX stores the absolute texture paths of the machine and folder it was written from (here the scratch folder, a longer path). The relative paths `../textures/hypercar/<group>/*.png` that Unity resolves are the same. Object count, triangle counts (incl. the 57 coincident duplicate triangles removed at export), 133 n-gon triangulations, axis bake residual 1.79e-07, dimensions, wheel refs, pivots, colliders and materials all match the original export.

Also shipped: `reports/REEXPORT_fbx_validation_complete.txt` / `.json` (validator output for this exact file) and `reports/REEXPORT_fbx_export_settings.json` (exporter settings + SHA-1).
