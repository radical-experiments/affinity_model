#!/usr/bin/env bash

time=`date +%s`

for nsteps in 100000;
do
	for iter in {1..15};
	do
		gmx_mpi grompp -f grompp_${nsteps}.mdp -c input.gro -p topol.top -o out.tpr 2>> grompp_out_$nsteps
		perf stat gmx_mpi mdrun -ntomp 1 -s out.tpr -c out.gro 2>> perf_stat_$nsteps
	done
done
