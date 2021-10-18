#!/bin/bash

# "AEL" "Drain" "IPLoM" "Lenma" "LFA" "LogCluster" "LogMine" 

algos=("LKE" "LogSig")

for algo in ${algos[@]}; do
    for i in {0..5}; do
        echo "Running ${algo} (iteration $i)"
        python ${algo}_benchmark.py > ${algo}_$i
    done
done
