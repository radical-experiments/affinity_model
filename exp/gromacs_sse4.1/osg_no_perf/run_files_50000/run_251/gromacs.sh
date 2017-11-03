#!/bin/bash


module load gromacs
gmx grompp -f grompp_50000.mdp -c input.gro -p topol.top -o out.tpr 2>> grompp_50000.out
gmx mdrun -ntomp 1 -nt 1 -s out.tpr -c out.gro 2>> mdrun_50000.out
