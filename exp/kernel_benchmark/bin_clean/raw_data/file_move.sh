#!/usr/bin/env bash

src_pathname=$1
dst_pathname=$2
epoch_id=${src_pathname##*/}

if [ ! -d $dst_pathname/clock_speed ]
then
    mkdir -p $dst_pathname/clock_speed
fi

if [ ! -d $dst_pathname/cpu_util ]
then
    mkdir -p $dst_pathname/cpu_util
fi

if [ ! -d $dst_pathname/cycles ]
then
    mkdir -p $dst_pathname/cycles
fi

if [ ! -d $dst_pathname/cycles_pred ]
then
    mkdir -p $dst_pathname/cycles_pred
fi

if [ ! -d $dst_pathname/cycles_prederr ]
then
    mkdir -p $dst_pathname/cycles_prederr
fi

if [ ! -d $dst_pathname/instr_rate ]
then
    mkdir -p $dst_pathname/instr_rate
fi

if [ ! -d $dst_pathname/p2a ]
then
    mkdir -p $dst_pathname/p2a
fi

if [ ! -d $dst_pathname/p2a_error ]
then
    mkdir -p $dst_pathname/p2a_error
fi

if [ ! -d $dst_pathname/instructions ]
then
    mkdir -p $dst_pathname/instructions
fi

if [ ! -d $dst_pathname/instructions_calc ]
then
    mkdir -p $dst_pathname/instructions_calc
fi

if [ ! -d $dst_pathname/instructions_calcerr ]
then
    mkdir -p $dst_pathname/instructions_calcerr
fi

if [ ! -d $dst_pathname/time ]
then
    mkdir -p $dst_pathname/time
fi

mv $src_pathname/clock\ speed.csv $dst_pathname/clock_speed/$epoch_id.csv

mv $src_pathname/CPU\ utilized.csv $dst_pathname/cpu_util/$epoch_id.csv

mv $src_pathname/cycles.csv $dst_pathname/cycles/measured_$epoch_id.csv

mv $src_pathname/predicted\ cycles.csv $dst_pathname/cycles_pred/prediction_$epoch_id.csv

mv $src_pathname/cycles\ prediction\ error.csv $dst_pathname/cycles_prederr/prederr_$epoch_id.csv

mv $src_pathname/estimated\ number\ of\ instructions.csv $dst_pathname/instructions_calc/calculated_$epoch_id.csv

mv $src_pathname/instruction\ calculation\ error.csv $dst_pathname/instructions_calcerr/calcerr_$epoch_id.csv

mv $src_pathname/instructions.csv $dst_pathname/instructions/measured_$epoch_id.csv

mv $src_pathname/instructions\ per\ cycle.csv $dst_pathname/instr_rate/measured_$epoch_id.csv

mv $src_pathname/p2a\ ratio\ to\ instruction\ rate\ error.csv $dst_pathname/p2a_error/p2a_error_$epoch_id.csv

mv $src_pathname/prediction\ to\ actual\ cycles.csv $dst_pathname/p2a/p2a_$epoch_id.csv

mv $src_pathname/time* $dst_pathname/time/$epoch_id.csv
