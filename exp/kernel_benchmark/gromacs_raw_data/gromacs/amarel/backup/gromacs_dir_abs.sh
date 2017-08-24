#/usr/bin/env bash

time=`date +%s`
mkdir /scratch/mingtha/gromacs_$time

indir=/scratch/mingtha/bin
outdir=/scratch/mingtha/gromacs_$time

cp $indir/input.gro $outdir
cp $indir/topol.top $outdir

for nsteps in 1000 5000 10000 25000 50000 75000 100000 250000 500000 750000 1000000
do
	cp $indir/grompp_${nsteps}.mdp $outdir
	for iter in {1..15}
	do
		gmx_mpi grompp -f $outdir/grompp_${nsteps}.mdp -c $outdir/input.gro -p $outdir/topol.top -o $outdir/out.tpr 2>> $outdir/grompp_out_$nsteps
		perf stat gmx_mpi mdrun -ntomp 1 -s $outdir/out.tpr -c $outdir/out.gro 2>> $outdir/perf_stat_$nsteps
	done
done
