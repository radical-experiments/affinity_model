#!/usr/bin/env bash

pathname=$1

for flops in 1000000 1000000000 10000000000 100000000000 250000000000 500000000000 750000000000 1000000000000
do
    python cleaning_amarel.py $pathname/perfstat_$flops
done
