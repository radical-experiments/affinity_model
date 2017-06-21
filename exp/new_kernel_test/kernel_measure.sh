#!/usr/bin/env bash

for loops in 1000000 1000000000 1000000000000
do
    echo "emulating ~($loops * 7) cycles"
    for iter in {1..25}
    do
        echo "Iteration $iter"
        perf stat ./kernel $loops 2>> perfstat_$loops
    done
done

echo "emulating ~(1000000000000 * 7) cycles"
for iter in {1..25}
do
    echo "Iteration $iter"
    perf stat ./kernel 1000000000000 2>> perfstat_1000000000000
done
