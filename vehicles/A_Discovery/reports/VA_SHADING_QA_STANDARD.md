# Vehicle shading QA standard (mandatory from Phase E on)

Applies to every vehicle release at **LOD0, LOD1, LOD2 and LOD3**. Read-only on frozen releases; findings are reported, never auto-fixed.

## 1. Numeric screen — `scripts/va_shading_qa.py`

```
Blender -b --factory-startup --python vehicles/A_Discovery/scripts/va_shading_qa.py -- <export_ready.blend> <out.json>
```

- Counts **torn loop normals** on every render mesh: the corner normal deviates more than 50° from its own face normal.
- This is the signature of transferred or smeared normals on decimated or creased geometry: chrome tears, blotches, silvery carbon, shards in lamps.
- Verdicts per mesh: **FAIL > 1 %**, **WARN > 0.3 %**.

## 2. Calibration (2026-10-08, every case confirmed visually)

| Case | Screen | Visual | Verdict |
|---|---|---|---|
| Titan GT original `Body_LOD1` | 11.9 % | chrome tears along every panel gap | real defect (fixed in r1) |
| Titan GT original `Trim_LOD1` | 26.6 % | rocker blotches | real defect (fixed in r1) |
| Vortex R original `Trim_LOD1` | 23.0 % | silvery blotchy wing, smeared rocker and diffuser fins | real defect (fixed in r1) |
| Raven XR scratch `Lights_LOD1` | 9.8 % | — | caught before release |
| **Titan GT r1 `Lights_LOD1`** | **4.4 %** (all 50–60°) | **triangular red / dark shards inside the tail lamp at LOD1; LOD0 clean** | **real, mild** — open item, see §4 |
| **Zero Gap R `Trim_LOD1`** (33 %), `Lights_LOD1` (15.5 %) | high | **silver-chrome smear in the side intake at LOD1; LOD0 dark** | **real** — open item, see §4 |
| Zero Gap R LOD0 meshes (wheels 10 %, brake discs 22 %, calipers 26 %, doors 4.7 %) | high | **clean** (`ZG_LOD0_wheel.png`, `ZG_LOD0_door_zoom.png`) | **false positive**: source-authored custom normals on thin features |
| Titan GT r1 / Vortex R r1 / Raven XR bodies and LOD1 trim | 0–0.1 % | clean | pass |

**Conclusion:**
- The screen reliably flags real problems on **reduced LODs (LOD1–3) built by this pipeline**.
- It over-reports on **source-derived LOD0 meshes with authored normals** (Zero Gap R).
- So a flag is confirmed only when **the LODk render differs visibly from LOD0 with the same camera**. LOD0 is the reference.

## 3. Mandatory procedure for every release

1. **Run the numeric screen on all LODs.** Any FAIL or WARN mesh must be inspected.
2. **Render the comparison** with `rv_render.py` and `RV_LOD=<k>` (or the vehicle's equivalent). Compare LOD0 against LOD1, and LOD1 against LOD2, using identical cameras. Views:
   - close-ups: hood, door/rocker, tail/lamps, wing/spoiler, wheel;
   - gameplay distance: ¾ views and chase.
3. **Inspect for:**
   - torn or invalid normals;
   - shading discontinuities;
   - distorted reflected highlights (zebra on LOD0; sky reflection on LODk);
   - hard-surface smoothing defects (silvery or blotchy carbon, smeared trim);
   - panel-gap artifacts;
   - wheel and trim shading;
   - lamp shards;
   - LOD transition pops (silhouette, colour or shading jumps between consecutive LODs).
4. **Release rule:** no FAIL on LOD1 or LOD2 hard-surface or body meshes unless the visual check proves a false positive; that exception is documented in the release report. Supplementary check **S1** in `rv_validate.py` and Vortex R r1's validator enforces this.
5. **Build rule:** never transfer LOD0 normals onto decimated hard-surface parts, and never decimate a body that has panel-gap grooves. Use a groove-free body with smooth-reference normals; use own normals with LOD0 sharp angles for hard-surface parts.

## 4. Read-only audit of frozen releases (2026-10-08)

| Release | PASS / WARN / FAIL meshes | Visually confirmed defects | Proposed action (needs approval) |
|---|---|---|---|
| Zero Gap R | 23 / 2 / 62 | LOD1 side-intake trim smear; lamp and interior LOD1–2 flags likely the same cause. LOD0 flags are false positives | `B_ZeroGapR_r1`: own normals on LOD1–3 Trim / Lights / Interior / Wheel / BrakeDisc / Caliper, normals only |
| Titan GT original | 73 / 3 / 3 | superseded by r1 | none |
| **Titan GT r1** (preferred import) | 75 / 3 / 1 | `Lights_LOD1` tail-lamp shards (mild) | `C_TitanGT_r2`: normals-only on `Lights_LOD1` (+ Interior/Steering LOD1 WARNs), same as Vortex R r1 |
| Vortex R original | 75 / 1 / 3 | superseded by r1 | none |
| **Vortex R r1** | **79 / 0 / 0** | none | — |
| **Raven XR** | **79 / 0 / 0** | none | — |

- **Per-mesh numbers:** `reports/shading_qa/*.json`.
- **Evidence:** `previews/shading_qa/` (Zero Gap R LOD0 vs LOD1 door, LOD1 rear ¾, LOD0 wheel; Titan GT r1 LOD0 vs LOD1 tail).
- **Unchanged:** no frozen file was modified. SHA-1 was checked before and after every read.
