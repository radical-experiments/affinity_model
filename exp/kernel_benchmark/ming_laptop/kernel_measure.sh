#!/usr/bin/env bash

for loops in 1000000 1000000000 10000000000 100000000000
do
    echo "emulating ~($loops * 7) cycles"
    for iter in {1..25}
    do
        echo "Iteration $iter"
        perf stat ./kernel $loops 2>> perfstat_$loops
    done
done

for loops in 250000000000 500000000000 750000000000 1000000000000
do
        echo "emulating ~($loops * 7) cycles"
        for iter in {1..10}
        do
            echo "Iteration $iter"
            perf stat ./kernel $loops 2>> perfstat_$loops
        done
done
