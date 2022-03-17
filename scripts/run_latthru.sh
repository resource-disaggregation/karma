function cleanup() {
    killall python3;
    echo "Cleaned up";
}

trap cleanup EXIT

cleanup;

dir_host=$1
dir_porta=$2
dir_portb=$3
block_size=$4
num_tenants=$5
duration=$6
fair_share=100

python3 microbench_pickles.py $num_tenants $fair_share $duration ~/karma-eval/microbench_demands.pickle ~/karma-eval/microbench_allocs.pickle

echo "Starting tenants"
for para in 1 2 4 8 16; do
    config="latthru-para$para";
    echo $config;
    for ((tenant=0;tenant<$num_tenants;tenant++)); do
        echo $tenant; 
        python3 -u driver2.py $dir_host $dir_porta $dir_portb $tenant $para ~/karma-eval/microbench_demands.pickle $block_size foobar 0 0 ~/karma-eval/microbench_allocs.pickle $fair_share > ~/karma-eval/$config.tenant$tenant.txt 2>&1 &
        pids+=($!);
        echo "Launched tenant$tenant";
    done
done
