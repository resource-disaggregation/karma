#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

config=$1
num_users=$2

numbers=$(for ((i = 1 ; i <= $num_users ; i++)); do echo $i; done)
static=$(cat ~/karma-eval/$config-static.results | grep -i throughput | awk '{print $5}' | sort -n)
maxmin=$(cat ~/karma-eval/$config-maxmin.results | grep -i throughput | awk '{print $5}' | sort -n)
karma=$(cat ~/karma-eval/$config-karma.results | grep -i throughput | awk '{print $5}' | sort -n)

paste <(for ((i = 1 ; i <= $num_users ; i++)); do echo $i; done) <(cat ~/karma-eval/$config-static.results | grep -i throughput | awk '{print $5}' | sort -n) <(cat ~/karma-eval/$config-maxmin.results | grep -i throughput | awk '{print $5}' | sort -n) <(cat ~/karma-eval/$config-karma.results | grep -i throughput | awk '{print $5}' | sort -n)