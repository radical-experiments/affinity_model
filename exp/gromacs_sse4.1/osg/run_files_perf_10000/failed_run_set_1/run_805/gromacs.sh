#!/bin/bash


module load gromacs
gmx grompp -f grompp_10000.mdp -c input.gro -p topol.top -o out.tpr 2>> grompp_10000.out
perf stat gmx mdrun -ntomp 1 -nt 1 -s out.tpr -c out.gro 2>> perf_mdrun_10000.out
