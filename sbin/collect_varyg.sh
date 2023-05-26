#!/usr/bin/env bash

# NOTE: Hard coded for 100 users

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

config=$1
total_blocks=$2
duration=$3

echo "Utilization"
for g in 8 6 4 2 0; do
    cat ~/karma-eval/$config-g$g.results | grep -i "total useful allocation" | awk -v blocks=$total_blocks -v dur=$duration '{sum += $7} END {print sum/(blocks*dur);}'
done

echo "Throughput"
for g in 8 6 4 2 0; do
    cat ~/karma-eval/$config-g$g.results | grep -i "throughput" | awk '{sum += $5} END {print sum;}'
done

echo "Fairness"
for g in 8 6 4 2 0; do
    min_alloc=$(cat ~/karma-eval/$config-g$g.results | grep -i "total useful allocation" | awk '{print $7;}' | sort -n | head -n 1)
    max_alloc=$(cat ~/karma-eval/$config-g$g.results | grep -i "total useful allocation" | awk '{print $7;}' | sort -n | tail -n 1)
    awk -v min_alloc=$min_alloc -v max_alloc=$max_alloc 'BEGIN {print min_alloc/max_alloc}'
done

echo "Disparity (throughput)"
for g in 8 6 4 2 0; do
    median_xput=$(cat ~/karma-eval/$config-g$g.results | grep -i "throughput" | awk '{print $5;}' | sort -n | head -n 50 | tail -n 1)
    min_xput=$(cat ~/karma-eval/$config-g$g.results | grep -i "throughput" | awk '{print $5;}' | sort -n | head -n 1)
    awk -v min_xput=$min_xput -v median_xput=$median_xput 'BEGIN {print median_xput/min_xput}'
done


