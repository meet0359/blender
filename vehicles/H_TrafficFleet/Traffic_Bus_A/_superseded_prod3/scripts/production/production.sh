#!/bin/zsh
# usage: production.sh <design> <Vehicle_Folder> <base name> <budget_lo> <budget_hi>   (+ framing env TS_SHIFT_*/TS_LIFT_*/TS_CAM_SCALE... exported by the caller; RESUME=1 resumes from a saved 09)
# Blender-only FINAL PRODUCTION: builder v2 stages 02-08 -> 09 (TS_NO_FBX) -> renders -> validation (FBX SKIP) -> review sheets (TS_NO_UNITY).
# Disk: owner removed the 5 GB rule (2026-10-09); only a 1 GB emergency floor remains so a write never fills the disk.
guard() { local f=$(df -k /Users/meetshah/Documents/blender | tail -1 | awk '{print $4}'); echo "DISKGUARD $1: $(( f / 1048576 )) GB free"; [ $f -ge 1048576 ] || { echo "DISKGUARD STOP: below 1 GB before $1"; return 1; }; }
B=/Applications/Blender.app/Contents/MacOS/Blender; SC=/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/scripts; V=/Users/meetshah/Documents/blender/vehicles/H_TrafficFleet/$2; D=$1; BASE=$3
CKP=$(grep -o "CKP_ = '[a-z0-9]*'" $SC/designs/$D.py | cut -d"'" -f2); PRE=$(grep -o "PRE = '[A-Za-z0-9_]*'" $SC/designs/$D.py | cut -d"'" -f2); COLL=$(grep -o "COLL_NAME = '[A-Z0-9_]*'" $SC/designs/$D.py | cut -d"'" -f2)
L=$V/reports/production_logs; mkdir -p $L $V/scripts/production; export TS_NO_FBX=1 TS_NO_UNITY=1
st() { echo "$(date +%H:%M) $*" | tee -a $L/progress.log; }
guard "production $D" || exit 1
if [ -n "$RESUME" ]; then [ -f $V/blend/${CKP}_09_export_ready.blend ] || { st "RESUME: no 09 checkpoint"; exit 1; }; st "RESUME from saved 09 (no rebuild)"; else
ex=($V/blend/${CKP}_0[2-9]_*.blend(N)); (( ${#ex} )) && { st "EXISTS production checkpoints in $V/blend - not overwriting"; exit 1; }
cp $SC/ts_vehicle_v2.py $SC/ts_loft.py $SC/ts_classes.py $SC/ts_lib.py $SC/ts_export.py $SC/ts_validate.py $SC/ts_render.py $SC/ts_zebra.py $SC/ts_package.py $SC/production.sh $SC/designs/$D.py $V/scripts/production/
st "build 02-08"; cd $SC && TS_SCRATCH=$V $B -b --factory-startup --python ts_vehicle_v2.py -- $D 8 > $L/build.log 2>&1
[ -f $V/blend/${CKP}_08_rig.blend ] || { st "BUILD FAILED"; grep -A6 Traceback $L/build.log | tail -6; exit 1; }
st "09 export-ready (no FBX)"; $B -b --factory-startup --python ts_export.py -- $2 $CKP $BASE $COLL > $L/export.log 2>&1; [ -f $V/blend/${CKP}_09_export_ready.blend ] || { st "09 FAILED"; tail -5 $L/export.log; exit 1; }
fi
cd $SC; F=$V/blend/${CKP}_09_export_ready.blend; F2=$V/blend/${CKP}_02_body.blend; P=$V/previews
r() { guard "$*" || { st "STOPPED (disk)"; exit 1; }; $B -b --factory-startup --python ts_render.py -- "$@" </dev/null >> $L/render.log 2>&1; }
st "renders"; TS_RES=1600 r $F $BASE $P studio; TS_RES=1600 r $F $BASE $P daylight; TS_RES=1280 r $F $BASE $P game
for look in clay wire; do TS_LOOK=$look TS_RES=1280 r $F $look $P/qa studio front34 rear34 side front rear lamp_front bumper_rear; done
for k in 0 1 2 3; do TS_LOD=$k TS_RES=1280 r $F LOD$k $P/lod studio front34 side; TS_LOD=$k TS_RES=1280 r $F LOD$k $P/lod game game_close; done
TS_ONLY=REF_Master $B -b --factory-startup --python ts_zebra.py -- $F2 $P/zebra_master </dev/null > $L/zebra.log 2>&1
$B -b --factory-startup --python ts_zebra.py -- $F $P/zebra_game </dev/null >> $L/zebra.log 2>&1
st "renders done: $(grep -c RENDERED $L/render.log) + zebra $(grep -c '^ZEBRA' $L/zebra.log)"
st "validate"; $B -b --factory-startup --python ts_validate.py -- $2 $CKP $BASE $COLL $4 $5 .12 > $L/validate.log 2>&1; grep "SUMMARY" $V/reports/${CKP}_validation.txt | tee -a $L/progress.log
st "package (sheets, integrity, candidate)"; $B -b --factory-startup --python ts_package.py -- $2 $CKP $BASE $PRE > $L/package.log 2>&1; tail -2 $L/package.log | tee -a $L/progress.log
st "DONE"
