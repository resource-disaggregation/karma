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
tenant_id=$6
duration=$7
fair_share=10
max_demand=$8
num_shards=$9
shard_idx="${10}"

rm -f ~/karma-eval/$cfg-test*

#python3 microbench_pickles.py $num_tenants $fair_share $duration ~/karma-eval/microbench_demands.pickle ~/karma-eval/microbench_allocs.pickle

echo "Starting threads"
config="$cfg-test";
echo $config;
pids=()
for ((tenant=0;tenant<$max_demand;tenant++)); do
    if [[ $(($tenant%$num_shards)) -ne $shard_idx ]]; then
        continue;
    fi
    python3 -u driver3.py $dir_host $dir_porta $dir_portb $block_size karma-backing $tenant_id $tenant $fair_share foobar 0 foobar > ~/karma-eval/$config.tenant$tenant.txt 2>&1 &
    pids+=($!);
    echo "Launched tenant$tenant";
done
for pid in ${pids[*]}; do
    wait $pid
done

