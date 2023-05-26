#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

jiffybin=/home/ubuntu/jiffy/build

function cleanup() {
    killall storaged;
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

# Start storage servers
base_port=9090
for ((i = 0 ; i < $num_storaged ; i++)); do
    cur_port=$(($base_port + 10*$i))
    cur_blocks=$(($num_blocks/$num_storaged))
    if (( $i < $(($num_blocks%$num_storaged)) )); then
        cur_blocks=$(($cur_blocks+1))
    fi
    JIFFY_DIRECTORY_HOST=$host JIFFY_STORAGE_HOST=$(ifconfig ens5 | grep 'inet' | head -n 1 | awk '{print $2}') JIFFY_STORAGE_MGMT_PORT=$(($cur_port+3)) JIFFY_STORAGE_SCALING_PORT=$(($cur_port+4)) JIFFY_STORAGE_SERVICE_PORT=$(($cur_port+5)) JIFFY_STORAGE_NUM_BLOCKS=$cur_blocks JIFFY_STORAGE_NUM_BLOCK_GROUPS=1 JIFFY_BLOCK_CAPACITY=$block_size $jiffybin/storage/storaged > ~/karma-eval/$config.storage$i.log 2>&1 &
    pids+=($!);
    echo "Launched storage server $i";
done