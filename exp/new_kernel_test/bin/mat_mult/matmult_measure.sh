#!/usr/bin/env bash

for loops in 1000 2500 5000 7500 10000
do
        echo "Multiplying $loops by $loops"
        for iter in {1..10}
        do
            echo "Iteration $iter"
            perf stat ./matrix_mult mat1_${loops}_1.txt mat2_${loops}_1.txt $loops 2>> perfstat_$loops
        done
done
