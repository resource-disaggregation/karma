function cleanup() {
    killall python3;
    echo "Cleaned up";
}

trap cleanup EXIT

cleanup;

cfg=$1
dir_host=$2
dir_porta=$3
dir_portb=$4
block_size=$5
num_tenants=$6
duration=$7
fair_share=100
num_shards=$8
shard_idx=$9

rm -f ~/karma-eval/$cfg-latthru*

python3 microbench_pickles.py $num_tenants $fair_share $duration ~/karma-eval/microbench_demands.pickle ~/karma-eval/microbench_allocs.pickle

echo "Starting tenants"
for para in 1 2 4 8 16; do
    config="$cfg-latthru-para$para";
    echo $config;
    pids=()
    for ((tenant=0;tenant<$num_tenants;tenant++)); do
        if [[ $(($tenant%$num_shards)) -ne $shard_idx ]]; then
            continue;
        fi
        python3 -u driver2.py $dir_host $dir_porta $dir_portb $tenant $para ~/karma-eval/microbench_demands.pickle $block_size foobar 0 0 ~/karma-eval/microbench_allocs.pickle $fair_share > ~/karma-eval/$config.tenant$tenant.txt 2>&1 &
        pids+=($!);
        echo "Launched tenant$tenant";
    done
    for pid in ${pids[*]}; do
        wait $pid
    done
done
