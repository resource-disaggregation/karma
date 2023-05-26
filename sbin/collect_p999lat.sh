#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

config=$1
num_users=$2

paste <(for ((i = 1 ; i <= $num_users ; i++)); do echo $i; done) <(cat ~/karma-eval/$config-static.results | grep -i "p999 latency" | awk '{print $6}' | sort -nr) <(cat ~/karma-eval/$config-maxmin.results | grep -i "p999 latency" | awk '{print $6}' | sort -nr) <(cat ~/karma-eval/$config-karma.results | grep -i "p999 latency" | awk '{print $6}' | sort -nr)