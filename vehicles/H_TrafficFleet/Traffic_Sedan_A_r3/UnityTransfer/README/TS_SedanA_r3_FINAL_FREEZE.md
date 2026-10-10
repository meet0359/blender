# Traffic_Sedan_A H1-r3 — FINAL FREEZE (Phase H traffic, Sedan A)

Date 2026-10-08 21:53. Approved by the project owner ("H1-r3 APPROVED — FREEZE SEDAN A") as a production traffic asset for normal mobile gameplay distances.
- Validation: **18 checks + S1 on every LOD: 0 errors, 0 warnings**. FBX clean re-import: **2 / 2**. Protected-file integrity: **PASS**.

**Status**

| Item | State |
|---|---|
| Blender production | **COMPLETE** |
| Visual approval | **approved for traffic gameplay** |
| Unity runtime verification | **PENDING** |
| Photorealistic / AAA | **NOT CLAIMED** |

- Status: **FROZEN.** Do not modify. Any later change goes to a separate revision (e.g. `Traffic_Sedan_A_r4/`), and only if Unity integration finds a real defect.
- Earlier revisions `Traffic_Sedan_A/` (H1) and `Traffic_Sedan_A_r2/` are preserved unchanged for reference. **Do not import them.**
- Preferred Unity import: `Traffic_Sedan_A_r3/UnityTransfer/`.

Non-blocking limitations (details in `reports/TS_SedanA_H1R3_REPORT.md` §6):
- generic, plain procedural body with no secondary sculpting, so it looks bland in close studio hero shots;
- closed zebra contours at the lower rear corner when seen from a low camera;
- baked shut lines are about 5.5 mm wide and soft in extreme close-ups;
- 8-bit normal-map steps show in game-mesh zebra at extreme range, and ASTC will requantize them;
- slightly irregular hood-highlight edge in the 50 mm close-up;
- the pale A-pillar liner shows through the windshield in studio ¾ views;
- LOD2/3 facets if those LODs are forced close;
- 2 invisible folded master faces;
- no photographic reference comparison;
- **no Unity runtime or performance testing.**

Source of truth: `blend/trafficsedanar3_09_export_ready.blend`. Build scripts are snapshotted in `scripts_snapshot/` (the shared fleet tooling may evolve; this snapshot reproduces r3).
The shared traffic library (`../shared/textures/`) is hashed here as well: it is an approved shared asset.

| File | SHA-1 |
|---|---|
| `UnityTransfer/FBX/TrafficSedanA_LOD0_unity_test.fbx` | `23bd3c0d6407b395533ab2bf170ea99e10e2d8f6` |
| `UnityTransfer/FBX/TrafficSedanA_complete_unity.fbx` | `257f709198d8d3c8c5404bf5c510efd4e438dde8` |
| `UnityTransfer/README/TrafficSedanA_UNITY_IMPORT_NOTES.md` | `a92b7ae94d50efa432ef507f9aaf3564f36a4d94` |
| `UnityTransfer/Reports/TS_SedanA_H1R3_REPORT.md` | `8b51498bcd8a6e7a4e778e2592fb30ed5a8c8120` |
| `UnityTransfer/Reports/TS_SedanA_build_log.json` | `dc056395c73c826d94a904a32301e7a7b6ee3c04` |
| `UnityTransfer/Reports/trafficsedanar3_export_manifest.json` | `94d82792b1dd57f843b46b2497c25c6d83fd7e6a` |
| `UnityTransfer/Reports/trafficsedanar3_geometry.json` | `ef0969b15b3203c842e991cb4773317fce690c7e` |
| `UnityTransfer/Reports/trafficsedanar3_integrity_check.md` | `1be7cb721ea0615ed9a9981b09bb520a60e26efb` |
| `UnityTransfer/Reports/trafficsedanar3_validation.txt` | `fd821d9cd69f57d28252e70c454a2b07bde7b0a8` |
| `UnityTransfer/Textures/TS_SedanA_Body_AO_Grime.png` | `6e36f4e0925e1740fbc230e03c2d36828e3eb027` |
| `UnityTransfer/Textures/TS_SedanA_Body_Normal.png` | `583bdda4b0176862d238684b6e2c0facecab5a6a` |
| `UnityTransfer/Textures/TS_SedanA_Body_Normal_LOD1.png` | `63f765d1663894a7d0740e25e7e751b16683d505` |
| `UnityTransfer/Textures/Shared/TS_Atlas_BaseColor.png` | `478e55fdeb2f83b290ff174e0fd976ffc7cc727f` |
| `UnityTransfer/Textures/Shared/TS_Atlas_Metallic.png` | `e5de8cdb579c670c127fd4456960caae52387d20` |
| `UnityTransfer/Textures/Shared/TS_Atlas_MetallicSmoothness.png` | `4420edba6dba74cfb4206ec7f69796fca89e2ac4` |
| `UnityTransfer/Textures/Shared/TS_Atlas_Normal.png` | `3e023d1b7c1f969918e5eaf203c387159ba150fb` |
| `UnityTransfer/Textures/Shared/TS_Atlas_Roughness.png` | `9f845c3a1236bed57f596313fd3aa8143b9c401b` |
| `UnityTransfer/Textures/Shared/TS_Lights_BaseColor.png` | `5ef7f4fef04acb94350c9709e2f5c75009813127` |
| `UnityTransfer/Textures/Shared/TS_Lights_ChannelID.png` | `0efb36167fd6dbd5db7874fd8d841028da798430` |
| `UnityTransfer/Textures/Shared/TS_Lights_Emission.png` | `cf305913ac336e2fdb21acd1d0de4a67326fc942` |
| `UnityTransfer/Textures/Shared/TS_PaintFlake_Normal.png` | `eea9e5960841e08937eaef45c4346587376a70ac` |
| `UnityTransfer/Textures/Shared/TS_Tire_BaseColor.png` | `f9ce8bbfe8ed6d1e58bba5747126419969b9e4b1` |
| `UnityTransfer/Textures/Shared/TS_Tire_Normal.png` | `b9e1998b42e42c530aa504f2be840995ccde2f87` |
| `UnityTransfer/Textures/Shared/TS_Tire_Roughness.png` | `4cdea5f8c04a5fbcf305a32d3fb64d22986144e5` |
| `blend/trafficsedanar3_02_body.blend` | `8847237f629c0371ad684cf678b22dad076fa6a2` |
| `blend/trafficsedanar3_03_parts_lights.blend` | `3fcba458347ddc6324529b7ec83c3a1ffb988872` |
| `blend/trafficsedanar3_04_wheels.blend` | `053be49e0582916c3cd96fceaac93dfcf6c06fd8` |
| `blend/trafficsedanar3_05_interior.blend` | `f1822aa0a497cc53d03f60a7bf2d4d041c58d59b` |
| `blend/trafficsedanar3_06_materials_uv.blend` | `28ea31b3c3a3bdb0c6fb80f347afede0642e0aab` |
| `blend/trafficsedanar3_07_lods.blend` | `cc9ef03a6e67812f7b83d2af5fa5071cde0f1360` |
| `blend/trafficsedanar3_08_rig.blend` | `d134161233de35e11cbbf8722532e9913d84d7b4` |
| `blend/trafficsedanar3_09_export_ready.blend` | `898791c95ae3a8ef6e2a2d34aaf989786f51194b` |
| `exports/TrafficSedanA_LOD0_unity_test.fbx` | `23bd3c0d6407b395533ab2bf170ea99e10e2d8f6` |
| `exports/TrafficSedanA_complete_unity.fbx` | `257f709198d8d3c8c5404bf5c510efd4e438dde8` |
| `previews/TrafficSedanA_arch_rear.png` | `8f6b4b90f581e08900483054740174abeba4e9bb` |
| `previews/TrafficSedanA_bumper_front.png` | `18637c7c00b4ef1344260bf3f935584125a44f8c` |
| `previews/TrafficSedanA_bumper_rear.png` | `05a86a522e577f38837bf5b7d94d7a6c79659c00` |
| `previews/TrafficSedanA_day_front34.png` | `3cff494421ab49eccc42e6104cf0cbc621428cfe` |
| `previews/TrafficSedanA_day_glass.png` | `dda3e998a897d2cb644260c24c7e57f1122d2959` |
| `previews/TrafficSedanA_day_rear34.png` | `a126446739bf731ffbd574e7cdd3fd614fcdf0bb` |
| `previews/TrafficSedanA_day_side.png` | `2f94fc881bf9050def4c2745ce59a74f945413b9` |
| `previews/TrafficSedanA_front.png` | `5633887298535a3edec33c6143024bc09ed6be25` |
| `previews/TrafficSedanA_front34.png` | `6cc4e94aa6c9e47a159632425021befb927d44ac` |
| `previews/TrafficSedanA_front_detail.png` | `510cd828bd0fc8aeb20332bf64837cd6d3dc332c` |
| `previews/TrafficSedanA_game_close.png` | `538a85bbaa8b4759ea9b54c71d42581739d4018b` |
| `previews/TrafficSedanA_game_far.png` | `6593d865307be3f82eb2d8ab4b85a3a5f1fa68e6` |
| `previews/TrafficSedanA_game_normal.png` | `b38455d90d403750d2860ecdd2defa6bfda2ebf1` |
| `previews/TrafficSedanA_interior.png` | `f5578e6bc18611eec0ab732fcbf4ec4f6451b180` |
| `previews/TrafficSedanA_lamp_front.png` | `bd9617104fd840130a00171d0998b210d9a65cc9` |
| `previews/TrafficSedanA_lamp_front_R.png` | `5652091e0542025e50a167d83fe8f443c91763d9` |
| `previews/TrafficSedanA_lamp_rear.png` | `b1f135ef0977012cf3d47e1051c01f5a0067ac4f` |
| `previews/TrafficSedanA_ortho_front.png` | `45c19c94f394d4de27a9de9e533517540fdb4973` |
| `previews/TrafficSedanA_ortho_rear.png` | `d72d432d5cf81dbf29291db835e7bc95c82ac342` |
| `previews/TrafficSedanA_ortho_side.png` | `a4bd022ce41dd332f0d15a0ebf5b52f793d0d6a4` |
| `previews/TrafficSedanA_plate_rear.png` | `25983be6ec72962052a795d6a02b625c837b80b0` |
| `previews/TrafficSedanA_quarter_rear_L.png` | `6a2e5040a15db020051b061f61630031dd7a600e` |
| `previews/TrafficSedanA_quarter_rear_R.png` | `d0e4f0bfe379826f003199cfffb1e065458e352e` |
| `previews/TrafficSedanA_rear.png` | `8c513183247556eb64e6f66c24e843e531da2816` |
| `previews/TrafficSedanA_rear34.png` | `e2a47de7e6e3044faa34298e3b4979e963e9db8e` |
| `previews/TrafficSedanA_rear_detail.png` | `d683010af6b32e5d331d5a01379e9b58786e184c` |
| `previews/TrafficSedanA_sheet_closeups_bumpers_lamps.jpg` | `75d4bd834582b79c5bca7cef1733b9aee959b11a` |
| `previews/TrafficSedanA_sheet_closeups_wheel_glass_plate.jpg` | `853120f7b386ba4d3d1e9e6b8ccf4d31619dcc0f` |
| `previews/TrafficSedanA_sheet_daylight.jpg` | `cfda9cea1313f198c01dc37c2d3836d7972e72af` |
| `previews/TrafficSedanA_sheet_details.jpg` | `6096fe01290e747d62855bb88acc5024ff65ec3d` |
| `previews/TrafficSedanA_sheet_distant_lods_plates.jpg` | `abd1fa9b5dcaa2f489027e79f1da1d943a865e28` |
| `previews/TrafficSedanA_sheet_game_camera.jpg` | `f5fc0da15a5df79d9f153aa52d0d22f41e6cceaa` |
| `previews/TrafficSedanA_sheet_lights_off_on.jpg` | `11d7fe38bd0aa0fbc403cc8f0ce2d005caa82935` |
| `previews/TrafficSedanA_sheet_lod_comparison.jpg` | `15fc81b32852754a163634b909b455f58f65f594` |
| `previews/TrafficSedanA_sheet_orthographic.jpg` | `ede58159768a4d481bac74cd321a2d7923e462a8` |
| `previews/TrafficSedanA_sheet_paint_variants_a.jpg` | `4ad15c629879fea147194895c9c1dfbb3df44dad` |
| `previews/TrafficSedanA_sheet_paint_variants_b.jpg` | `0526df6e4580c12894131012e98d64fd2bad0058` |
| `previews/TrafficSedanA_sheet_qa_clay.jpg` | `ca43a609abefd773642af71e261c56a28819610e` |
| `previews/TrafficSedanA_sheet_qa_clay_wire_details.jpg` | `f8906cf98474af9bbd9bd1c369fc2daf1d649c57` |
| `previews/TrafficSedanA_sheet_qa_normal.jpg` | `e2b8a0ff2546b7f2e468bfd5492a8ac44fd43834` |
| `previews/TrafficSedanA_sheet_qa_wire.jpg` | `ac878d2eacf33aa6111d7c30d93504d6efbd51ba` |
| `previews/TrafficSedanA_sheet_r2_vs_r3_bumper_corners.jpg` | `91399b1bdbdfd09ce76306e53f2a687cf4231a5c` |
| `previews/TrafficSedanA_sheet_r2_vs_r3_front_fender.jpg` | `542de9d8e3416d0aa038e9606155c1b4e45e47ef` |
| `previews/TrafficSedanA_sheet_r2_vs_r3_glass_interior.jpg` | `7be70a83cf2c61cd4df5b490280a3b12f0e9afa8` |
| `previews/TrafficSedanA_sheet_r2_vs_r3_overall.jpg` | `29d541198fd0af21b3432f4e40edeb846cd006e3` |
| `previews/TrafficSedanA_sheet_r2_vs_r3_rear_quarter.jpg` | `b37dd3742c300fc801e8a9be00cc3c46cd288b21` |
| `previews/TrafficSedanA_sheet_realism_vs_h0_audit.jpg` | `569c5b069cde5f38044884df07cfe04c6164a5a6` |
| `previews/TrafficSedanA_sheet_studio_1.jpg` | `7bb1b61c7622f0b5712dd20dced14490b57dc7e8` |
| `previews/TrafficSedanA_sheet_studio_2.jpg` | `4dc9c29a0c8ce30a619ba29ac086d10ab860a9ab` |
| `previews/TrafficSedanA_sheet_zebra_artifact_zones_r2_vs_r3.jpg` | `ec10afbd99ffaa3c40804cc483864187922ee07d` |
| `previews/TrafficSedanA_sheet_zebra_master_vs_game.jpg` | `b512f45dc27fbeb3a8d4007e4a33792a085a7781` |
| `previews/TrafficSedanA_sheet_zebra_r2game_r3game_r3master.jpg` | `0e7c2f23b7b5b9401d3f57a500688298b577c084` |
| `previews/TrafficSedanA_side.png` | `12927c8e80170fafb134d739ffc3a19ce61bc208` |
| `previews/TrafficSedanA_top.png` | `15ed4335baddd62f3441d9377eca491795aadf33` |
| `previews/TrafficSedanA_wheel.png` | `1f5dba7b536e7a8533f50d47945341595e49ba8b` |
| `previews/lights/off_front_detail.png` | `3e74b171b1ab2038daccfdd2a6fcfa833affb74c` |
| `previews/lights/off_lamp_front.png` | `a0ac666d5262effaa0efbfbb4a63f076aa141b5f` |
| `previews/lights/off_lamp_rear.png` | `82fec3ec05004875f9a14e0c3c1b97291756c12d` |
| `previews/lights/off_rear_detail.png` | `8db8ae2f4dd082cf2774e00190afdc598e734504` |
| `previews/lights/on_front_detail.png` | `6f89c990b19c5e27fea033ec2a7b29e5f1d2dfd2` |
| `previews/lights/on_lamp_front.png` | `ac88b6e177be637a131eadff799f2188cc69118a` |
| `previews/lights/on_lamp_rear.png` | `eaef2ef68fa3864788015a955ef53995600e0062` |
| `previews/lights/on_rear_detail.png` | `9b0db65ed24d804c7557ff174efeef75bfb9f233` |
| `previews/lod/LOD0_front34.png` | `af86b8617a5d883bd0e11ca53bb3f5f6552e39f0` |
| `previews/lod/LOD0_game_close.png` | `4a89f039581e85298e1993316005be713eb12439` |
| `previews/lod/LOD0_game_far.png` | `58909399f0f4507833a1463569983f9d1f6a1df4` |
| `previews/lod/LOD0_game_normal.png` | `1df8e210fb8c28df3349ca2ede427f9013ae3e3a` |
| `previews/lod/LOD0_rear34.png` | `1cd722291533d7c8f4018d349846fc682f60ef97` |
| `previews/lod/LOD0_side.png` | `2e9028d319d1260b451db6217c0a611e0b5c8f26` |
| `previews/lod/LOD1_front34.png` | `5320224ad13a5d058034600f545303ac6168aad3` |
| `previews/lod/LOD1_game_close.png` | `1c06e342fd1e7edca89d6d60be1ee1abfd92888a` |
| `previews/lod/LOD1_game_far.png` | `e56ecb12d1fddf2d2a76e7efa8e54b5e29b23301` |
| `previews/lod/LOD1_game_normal.png` | `b298f0bb59152853158446d65d3180576d4c0c92` |
| `previews/lod/LOD1_rear34.png` | `9d12ae410b93d4a57a03c94166012aaed59ac4b5` |
| `previews/lod/LOD1_side.png` | `cb3e02f8de96fff6aae04e0d0e19f6accd441ec2` |
| `previews/lod/LOD2_front34.png` | `484ad4bc8ebf46648c09efe98e41cdbb93ecac43` |
| `previews/lod/LOD2_game_close.png` | `c3b737027b45b4299eb680d79a6189c6c45e43ca` |
| `previews/lod/LOD2_game_far.png` | `8f4fdf04ca3cd1b298dd85835c56b642cf4aa1dc` |
| `previews/lod/LOD2_game_normal.png` | `86d9d920b241612a2a1c8730d0e149e8b2244c22` |
| `previews/lod/LOD2_rear34.png` | `9b3be49eed1bd701742a17146d2c72bde15c905d` |
| `previews/lod/LOD2_side.png` | `2b9fac0e6a797f2ce9570497326f594f66a08e29` |
| `previews/lod/LOD3_front34.png` | `9805a1b017c8d70a50a8127594ba5009da439d31` |
| `previews/lod/LOD3_game_close.png` | `dae429745c6f023aa67cb580c8a5e453295478de` |
| `previews/lod/LOD3_game_far.png` | `47c4d8eabbf0677f16ad5680b97b7cd282313b26` |
| `previews/lod/LOD3_game_normal.png` | `1dd57c9a3f3c37bcdfd431af19ac24cdc079a310` |
| `previews/lod/LOD3_rear34.png` | `c4a57a7737b66eea9f93ee42de129fb90d9f3482` |
| `previews/lod/LOD3_side.png` | `2ac7e95a1c6175ec26e4c893e6bcddd649be3c53` |
| `previews/qa/clay_arch_rear.png` | `ec0780edfc588855be707ed17ab57b8435360bfe` |
| `previews/qa/clay_bumper_front.png` | `bd481dcbd0494a4c1cca9b3d734e87eb7bb0187d` |
| `previews/qa/clay_bumper_rear.png` | `e528be7e7b4f355310c1501d0a9b3fade78442f8` |
| `previews/qa/clay_front34.png` | `c9a3db8f409411822fbb503a9ddadfb13d3a877b` |
| `previews/qa/clay_lamp_front.png` | `1fb40b46758bce707e2df051a4066925564e5f64` |
| `previews/qa/clay_quarter_rear_R.png` | `3eca3af367123fa2de54b95d2ac5e0d858d2a542` |
| `previews/qa/clay_rear34.png` | `10687c42ed2ee098d0088abd179aac3157ab9eac` |
| `previews/qa/clay_side.png` | `0b436860f7c3e0f4b6026422448ee9428469034f` |
| `previews/qa/normal_arch_rear.png` | `10e26f5939246ca0ad057a2ec766e67dba595f6d` |
| `previews/qa/normal_bumper_front.png` | `2d867cea2514c042108a8b0c74347f207f320242` |
| `previews/qa/normal_bumper_rear.png` | `7f8ecb2018a189aa3b1a82bcd872032dab617c2e` |
| `previews/qa/normal_front34.png` | `0403ff7c08479b200ec8986ffaf8127af5ff4a6d` |
| `previews/qa/normal_lamp_front.png` | `845f3bfa7f6f1ccd312c30514aad9ec1cb78ba6c` |
| `previews/qa/normal_quarter_rear_R.png` | `d84b97916c361f083d0d564bcaee8ddfd62e42fb` |
| `previews/qa/normal_rear34.png` | `a535ae0707212add3c504e476d2f3b98bec9039d` |
| `previews/qa/normal_side.png` | `3a88b6023e913f6a701a6df5a15fb5b12d6d89e2` |
| `previews/qa/wire_arch_rear.png` | `855406ca3635cde4f70b3dcc83b28aade7991d84` |
| `previews/qa/wire_bumper_front.png` | `66461592d05cd9a0a6804ac165d1b6d03cd5bc2d` |
| `previews/qa/wire_bumper_rear.png` | `8f0e0fab27bb8173ecf428bbf6ebe7260e8f063e` |
| `previews/qa/wire_front34.png` | `3a4a318dde243255841b5d3117cbbb35513efe19` |
| `previews/qa/wire_lamp_front.png` | `37a534cd040f37bf02713cd1a190d810e2c3a369` |
| `previews/qa/wire_quarter_rear_R.png` | `8841c89c4d30152963169d82836fad1e012819d2` |
| `previews/qa/wire_rear34.png` | `17f18d2e4703e00d8c3f26545967749f6de084ee` |
| `previews/qa/wire_side.png` | `264935c0b010e129234379fd3479a50139872a3b` |
| `previews/r2_compare/R2_bumper_front.png` | `d640d65dc08f26a496ae077745a65ddd59438fab` |
| `previews/r2_compare/R2_bumper_rear.png` | `34a0b70db936edaf114152fdd2b984af4867db5a` |
| `previews/r2_compare/R2_day_glass.png` | `bcb079eb76f06439a953a13ec74d68235f8b141f` |
| `previews/r2_compare/R2_front34.png` | `7d7eb5d29a624ea4a3360f871a2759413f5cca20` |
| `previews/r2_compare/R2_interior.png` | `af12e2dc7754692c75cf7aa580c285862de2280f` |
| `previews/r2_compare/R2_lamp_front.png` | `eb93e7ba5bc5b05338df68c790bb03e15dcf8ff0` |
| `previews/r2_compare/R2_lamp_front_R.png` | `eeadff62c69e8c56f39d1206fe782a4ed43fb430` |
| `previews/r2_compare/R2_quarter_rear_L.png` | `e29f5c692823112e2a92a59b0a3164caf3608fd7` |
| `previews/r2_compare/R2_quarter_rear_R.png` | `3c08f62977b6eaaabfe053249156e60d0fa6aa8c` |
| `previews/r2_compare/R2_rear34.png` | `41f18a2f021a62bc610ee139935e77a7dceadb2a` |
| `previews/r2_compare/R2_side.png` | `b880cf3ee49617b267ef2e26e239616e41ef9c65` |
| `previews/r2_compare/R3_bumper_front.png` | `18637c7c00b4ef1344260bf3f935584125a44f8c` |
| `previews/r2_compare/R3_bumper_rear.png` | `05a86a522e577f38837bf5b7d94d7a6c79659c00` |
| `previews/r2_compare/R3_day_glass.png` | `dda3e998a897d2cb644260c24c7e57f1122d2959` |
| `previews/r2_compare/R3_front34.png` | `6cc4e94aa6c9e47a159632425021befb927d44ac` |
| `previews/r2_compare/R3_interior.png` | `f5578e6bc18611eec0ab732fcbf4ec4f6451b180` |
| `previews/r2_compare/R3_lamp_front.png` | `bd9617104fd840130a00171d0998b210d9a65cc9` |
| `previews/r2_compare/R3_lamp_front_R.png` | `5652091e0542025e50a167d83fe8f443c91763d9` |
| `previews/r2_compare/R3_quarter_rear_L.png` | `6a2e5040a15db020051b061f61630031dd7a600e` |
| `previews/r2_compare/R3_quarter_rear_R.png` | `d0e4f0bfe379826f003199cfffb1e065458e352e` |
| `previews/r2_compare/R3_rear34.png` | `e2a47de7e6e3044faa34298e3b4979e963e9db8e` |
| `previews/r2_compare/R3_side.png` | `12927c8e80170fafb134d739ffc3a19ce61bc208` |
| `previews/variants/black_front34.png` | `3283f70795102c3f9965f7b2c36891d04bb3134d` |
| `previews/variants/blue_front34.png` | `b98f79fd64e2753afef5e87d274e02b2b145d3ec` |
| `previews/variants/graphite_front34.png` | `7ca5f8934edf2be4b28a8571500b8970e243c44a` |
| `previews/variants/red_front34.png` | `b21e86194d058004a758b09e395ebc0a0ccdde01` |
| `previews/variants/silver_front34.png` | `7925d23b3eb5ba952f6dd2bf01e03a8ee4463605` |
| `previews/variants/white_front34.png` | `b341386db947222e6b2d156a7e5a5ed9e65d0dc6` |
| `previews/zebra_diag/R2_doortop.png` | `66862e822e5ba9296f1f3466bff897bcf2564ea3` |
| `previews/zebra_diag/R2_fender_L.png` | `6d83914ab1af8d4e4470247208f7ad508d279420` |
| `previews/zebra_diag/R2_fender_R.png` | `3e64e8278821b74b64adbcccc04a1af59e217d15` |
| `previews/zebra_diag/R2_hood.png` | `7b2e2ed9d30f21ca364e3c2a07911b5ee889b456` |
| `previews/zebra_diag/R2_quarter_L.png` | `23078506475d69c609e0c9fb0c9812e1bb141dc6` |
| `previews/zebra_diag/R2_quarter_R.png` | `a5b2a351824c0c07b4f917733ecdcebd765494bf` |
| `previews/zebra_diag/R2master_doortop.png` | `af4beaedf539af86cdde132095d044827fe361d4` |
| `previews/zebra_diag/R2master_fender_L.png` | `ca3c1eb1c0edf75832120c958348ec5b726a8d8b` |
| `previews/zebra_diag/R2master_fender_R.png` | `0c7d91ae9a82ca727e854988ed77c4291983720c` |
| `previews/zebra_diag/R2master_hood.png` | `db2253ef554697545830a0125eccffa0b475a8f6` |
| `previews/zebra_diag/R2master_quarter_L.png` | `4195cb5b0b363281f7bc5bd6d8763646bd9537e6` |
| `previews/zebra_diag/R2master_quarter_R.png` | `27c4777887dff549af20c0fbcd7eb87033b8ee05` |
| `previews/zebra_diag/R3_doortop.png` | `8cfe2c00d59e5111b680bc78b42517e51ac1d277` |
| `previews/zebra_diag/R3_fender_L.png` | `5d8171bc7fb75264f6b486456a870e474fca4324` |
| `previews/zebra_diag/R3_fender_R.png` | `1036da255f7353e7822dbdc427e02ab2ec62f5cb` |
| `previews/zebra_diag/R3_hood.png` | `e6fbd6e3a2896f025da0558b0230afb64a27774f` |
| `previews/zebra_diag/R3_quarter_L.png` | `9e819f45d36ebd634d499bafbc3633737aea4c9a` |
| `previews/zebra_diag/R3_quarter_R.png` | `1468cca89e69c8ef5f238cd013c59b91709380d7` |
| `previews/zebra_diag/R3master_doortop.png` | `1befbed845f0b51e2beab7215d6b8cf6a320c34f` |
| `previews/zebra_diag/R3master_fender_L.png` | `81775263e670250c7b889cd3900b0a31556601b4` |
| `previews/zebra_diag/R3master_fender_R.png` | `1071539318bc40a477e050043ad69aecc98a11f9` |
| `previews/zebra_diag/R3master_hood.png` | `4919f096d14d2fa6d5338645982a90d6f5207515` |
| `previews/zebra_diag/R3master_quarter_L.png` | `cf6fceada9a6e993ba4963836a895e930d49fb5e` |
| `previews/zebra_diag/R3master_quarter_R.png` | `8e6b6c9615055b79d2372732e24275e6bdc29800` |
| `previews/zebra_game/zebra_deck.png` | `bcdd8775f4a353c39172ae5f56fcf23b5811486a` |
| `previews/zebra_game/zebra_deck_r.png` | `c2812b730e7a33997b05429bb7b810a2ac16664b` |
| `previews/zebra_game/zebra_door.png` | `ad6c658c3b50c20efcffe4698d2d61b32c2ae628` |
| `previews/zebra_game/zebra_hood.png` | `4d3040650d894b47802dc916640a774ad2c59128` |
| `previews/zebra_game/zebra_quarter.png` | `281980c717489d8258f807d8e1bf1b90d819ae81` |
| `previews/zebra_game/zebra_quarter_r.png` | `4c4d65408edc0d426d75a2df0e1c34654976cbd0` |
| `previews/zebra_game/zebra_roof.png` | `55d314d68d6fb15ddb0812c6efee7fa3dc1e6511` |
| `previews/zebra_game/zebra_side_full.png` | `ca57681820542bfd4121db71270815b08844b967` |
| `previews/zebra_game/zebra_tail_corner.png` | `8aa3774808decf679484a7a9bd57a9aef97a0309` |
| `previews/zebra_game/zebra_tail_corner_r.png` | `39b44d84979aaf60609694558e291d55ebac2079` |
| `previews/zebra_master/zebra_deck.png` | `77d140c81d33b786ee146d25cc9d7d60de23503f` |
| `previews/zebra_master/zebra_deck_r.png` | `6fc48167caef08477b3000dcc7fa1ca16dc5f664` |
| `previews/zebra_master/zebra_door.png` | `58734f456af074be6bb01c867a66eb805890ac47` |
| `previews/zebra_master/zebra_hood.png` | `22dcc73ad2eb23405c03aa445ba20a44dbd59aaf` |
| `previews/zebra_master/zebra_quarter.png` | `ae4d6396f9f2d1d3b102749e18d08afc54d89ce8` |
| `previews/zebra_master/zebra_quarter_r.png` | `3e5acc016e56ef40b55d0654c6e35641e866ba61` |
| `previews/zebra_master/zebra_roof.png` | `261ebf38cadba9dafede9ee29123fcc5d3f70e6f` |
| `previews/zebra_master/zebra_side_full.png` | `2aea5858c8a4bd1051b99f758425a1f4e5a34bc5` |
| `previews/zebra_master/zebra_tail_corner.png` | `1dc483624d8fa18b209015f170312b458f71bb45` |
| `previews/zebra_master/zebra_tail_corner_r.png` | `7afe439f97ae57efcd4f0487a0ce7fd2fcf7dd6b` |
| `reports/TS_SedanA_H1R3_REPORT.md` | `8b51498bcd8a6e7a4e778e2592fb30ed5a8c8120` |
| `reports/TS_SedanA_build_log.json` | `dc056395c73c826d94a904a32301e7a7b6ee3c04` |
| `reports/trafficsedanar3_FREEZE_CANDIDATE.md` | `6a4ca57864d1149d4d1cfd81e4d93988787bc590` |
| `reports/trafficsedanar3_export_manifest.json` | `94d82792b1dd57f843b46b2497c25c6d83fd7e6a` |
| `reports/trafficsedanar3_geometry.json` | `ef0969b15b3203c842e991cb4773317fce690c7e` |
| `reports/trafficsedanar3_integrity_check.md` | `1be7cb721ea0615ed9a9981b09bb520a60e26efb` |
| `reports/trafficsedanar3_validation.txt` | `fd821d9cd69f57d28252e70c454a2b07bde7b0a8` |
| `scripts_snapshot/ts_export.py` | `5c1c033bd634335b68637ddb304fbc304316cac1` |
| `scripts_snapshot/ts_lib.py` | `d7113d4aa57fb0afe4d774acd58095aca22b0497` |
| `scripts_snapshot/ts_package.py` | `8ab161c2e345e943bdc9259ca9a45848369360ad` |
| `scripts_snapshot/ts_render.py` | `79a36ab5a7d7a358c8295e90e177c9cc62b91f4b` |
| `scripts_snapshot/ts_sedan_a_r3.py` | `f1d0278f9b90229be7bf986122a33ef0b72abf00` |
| `scripts_snapshot/ts_validate.py` | `bce5cfe76f975916660a63fefd9263b9a7dd2eaf` |
| `scripts_snapshot/ts_zebra.py` | `9d1f43c58418ce1269327622984cdbe9a610c92d` |
| `textures/TS_SedanA_Body_AO_Grime.png` | `6e36f4e0925e1740fbc230e03c2d36828e3eb027` |
| `textures/TS_SedanA_Body_Normal.png` | `583bdda4b0176862d238684b6e2c0facecab5a6a` |
| `textures/TS_SedanA_Body_Normal_LOD1.png` | `63f765d1663894a7d0740e25e7e751b16683d505` |
| `../shared/textures/TS_Atlas_BaseColor.png` | `478e55fdeb2f83b290ff174e0fd976ffc7cc727f` |
| `../shared/textures/TS_Atlas_Metallic.png` | `e5de8cdb579c670c127fd4456960caae52387d20` |
| `../shared/textures/TS_Atlas_MetallicSmoothness.png` | `4420edba6dba74cfb4206ec7f69796fca89e2ac4` |
| `../shared/textures/TS_Atlas_Normal.png` | `3e023d1b7c1f969918e5eaf203c387159ba150fb` |
| `../shared/textures/TS_Atlas_Roughness.png` | `9f845c3a1236bed57f596313fd3aa8143b9c401b` |
| `../shared/textures/TS_Lights_BaseColor.png` | `5ef7f4fef04acb94350c9709e2f5c75009813127` |
| `../shared/textures/TS_Lights_ChannelID.png` | `0efb36167fd6dbd5db7874fd8d841028da798430` |
| `../shared/textures/TS_Lights_Emission.png` | `cf305913ac336e2fdb21acd1d0de4a67326fc942` |
| `../shared/textures/TS_PaintFlake_Normal.png` | `eea9e5960841e08937eaef45c4346587376a70ac` |
| `../shared/textures/TS_Tire_BaseColor.png` | `f9ce8bbfe8ed6d1e58bba5747126419969b9e4b1` |
| `../shared/textures/TS_Tire_Normal.png` | `b9e1998b42e42c530aa504f2be840995ccde2f87` |
| `../shared/textures/TS_Tire_Roughness.png` | `4cdea5f8c04a5fbcf305a32d3fb64d22986144e5` |
