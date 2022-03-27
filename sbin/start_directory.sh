#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

jiffybin=/home/ubuntu/jiffy/build

function cleanup() {
    killall directoryd;
    echo "Cleaned up";
}


cleanup;

ulimit -n 10240

config=$1
host=$2
# set large lease period
alloc=$3
num_tenants=$4
init_credits=$5
num_storaged=$6
block_size=$7
num_blocks=$8
algo_interval=$9
public_blocks="${10}"

pids=()

# Start directory server
JIFFY_DIRECTORY_HOST=$host JIFFY_LEASE_PERIOD_MS=999999999 $jiffybin/directory/directoryd --alloc $alloc -n $num_tenants --init_credits $init_credits --algo_interval $algo_interval --public_blocks $public_blocks > ~/karma-eval/$config.dir.log 2>&1 &
pids+=($!);
echo "Launched directory server";