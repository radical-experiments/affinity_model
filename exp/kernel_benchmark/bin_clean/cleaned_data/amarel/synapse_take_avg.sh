#!/usr/bin/env bash

pathname=$1

python synapse_stats_aggr.py $pathname/clock_speed/ avg_clkspeed
python synapse_stats_aggr.py $pathname/cpu_util/ avg_cpu_util
python synapse_stats_aggr.py $pathname/cycles/ avg_cycles
python synapse_stats_aggr.py $pathname/cycles_pred/ avg_cycles_pred
python synapse_stats_aggr.py $pathname/cycles_prederr/ avg_cycles_prederr
python synapse_stats_aggr.py $pathname/instructions/ avg_instr
python synapse_stats_aggr.py $pathname/instructions_calc/ avg_instr_calc
python synapse_stats_aggr.py $pathname/instructions_calcerr/ avg_instr_calcerr
python synapse_stats_aggr.py $pathname/p2a/ avg_p2a
python synapse_stats_aggr.py $pathname/p2a_error/ avg_p2a_error
python synapse_stats_aggr.py $pathname/time/ avg_tx

mv avg* $pathname
