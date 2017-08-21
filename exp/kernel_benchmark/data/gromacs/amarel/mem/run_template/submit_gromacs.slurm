#!/bin/bash

#SBATCH --partition=mem                 # Partition (job queue)
#SBATCH --job-name=gmdrun               # Assign an 8-character name to your job
#SBATCH --nodes=1                       # Number of nodes
#SBATCH --ntasks=1                      # Processes (usually cores) on each node
#SBATCH --cpus-per-task=1               # Threads per process (or per core)
#SBATCH --mem=8000                      # Memory per node (MB)
#SBATCH --time=48:00:00                 # Total run time limit (HH:MM:SS)
#SBATCH --output=slurm.%N.%j.out        # combined STDOUT and STDERR output file
#SBATCH --export=ALL                    # Export you current env to the job env
#SBATCH --exclusive

srun gromacs.sh
