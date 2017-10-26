#!/usr/bin/env bash

time=`date +%s`

for nsteps in 1000 5000 10000 25000 50000 75000 100000 250000 500000 750000 1000000;
do
	for iter in {1..15};
	do
		gmx grompp -f grompp_${nsteps}.mdp -c input.gro -p topol.top -o out.tpr 2>> grompp_out_$nsteps
		perf stat gmx mdrun -ntomp 1 -nt 1 -s out.tpr -c out.gro 2>> perf_stat_$nsteps
	done
done
