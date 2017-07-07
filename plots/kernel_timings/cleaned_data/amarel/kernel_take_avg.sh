#!/usr/bin/env bash

pathname=$1

python kernel_stats_aggr.py $pathname/clock_speed/ avg_clkspeed
python kernel_stats_aggr.py $pathname/cpu_util/ avg_cpu_util
python kernel_stats_aggr.py $pathname/cycles/ avg_cycles
python kernel_stats_aggr.py $pathname/cycles_pred/ avg_cycles_pred
python kernel_stats_aggr.py $pathname/cycles_prederr/ avg_cycles_prederr
python kernel_stats_aggr.py $pathname/instructions/ avg_instr
python kernel_stats_aggr.py $pathname/instructions_calc/ avg_instr_calc
python kernel_stats_aggr.py $pathname/instructions_calcerr/ avg_instr_calcerr
python kernel_stats_aggr.py $pathname/p2a/ avg_p2a
python kernel_stats_aggr.py $pathname/p2a_error/ avg_p2a_error
python kernel_stats_aggr.py $pathname/time/ avg_tx

mv avg* $pathname
