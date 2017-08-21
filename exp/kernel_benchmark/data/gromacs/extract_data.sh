#!/usr/bin/env bash

START_DIR=$1

for nsteps in 1000 5000 10000 25000 50000 75000 100000 250000 500000 750000 1000000
do
    echo "NUMBER OF STEPS: $nsteps" >> $START_DIR/num_mpi_process.txt
    echo "NUMBER OF STEPS: $nsteps" >> $START_DIR/num_omp_threads.txt
    echo "NUMBER OF STEPS: $nsteps" >> $START_DIR/task_clock.txt
    echo "NUMBER OF STEPS: $nsteps" >> $START_DIR/cycles.txt
    echo "NUMBER OF STEPS: $nsteps" >> $START_DIR/instructions.txt
    echo "NUMBER OF STEPS: $nsteps" >> $START_DIR/time.txt
    grep 'MPI process' $START_DIR/perf_stat_$nsteps >> $START_DIR/num_mpi_process.txt
    grep "OpenMP thread" $START_DIR/perf_stat_$nsteps >> $START_DIR/num_omp_threads.txt
    grep "task-clock" $START_DIR/perf_stat_$nsteps >> $START_DIR/task_clock.txt
    grep "cycles" $START_DIR/perf_stat_$nsteps | grep -v "support" | grep -v "stalled" >> $START_DIR/cycles.txt
    grep "per cycle" $START_DIR/perf_stat_$nsteps >> $START_DIR/instructions.txt
    grep "time elapsed" $START_DIR/perf_stat_$nsteps >> $START_DIR/time.txt
done
