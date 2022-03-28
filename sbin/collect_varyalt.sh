#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

config=$1
total_blocks=$2
duration=$3

echo "Utilization"
for alt in 25 50 75; do
    cat ~/karma-eval/$config.results | grep -i "total useful allocation" | awk -v blocks=$total_blocks -v dur=$duration '{sum += $7} END {print sum/(blocks*dur);}'
done

echo "Throughput"
for alt in 25 50 75; do
    cat ~/karma-eval/$config.results | grep -i "throughput" | awk '{sum += $5} END {print sum;}'
done


