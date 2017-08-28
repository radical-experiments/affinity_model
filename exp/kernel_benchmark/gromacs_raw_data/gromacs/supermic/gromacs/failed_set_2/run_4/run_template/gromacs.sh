#!/usr/bin/env bash

time=`date +%s`
pwd=$1

for nsteps in 1000 5000 10000 25000 50000 75000 100000 250000 500000 750000 1000000;
do
	for iter in {1..15};
	do
		gmx grompp -f $pwd/grompp_${nsteps}.mdp -c $pwd/input.gro -p $pwd/topol.top -o $pwd/out.tpr 2>> $pwd/grompp_out_$nsteps
		perf stat gmx mdrun -ntomp 1 -s $pwd/out.tpr -c $pwd/out.gro 2>> $pwd/perf_stat_$nsteps
		rm /home/mha/\#*
	done
done
