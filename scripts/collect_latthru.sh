cfg=$1

for para in 1 2 4 8 16; do
    prefix="~/karma-eval/$cfg-latthru-para$para";
    lat_sum=$(cat $prefix.tenant* | grep -i 'latency sum' | awk '{sum += $5;} END {print sum}')
    lat_count=$(cat $prefix.tenant* | grep -i 'latency count' | awk '{sum += $5;} END {print sum}')
    jiffy_blocks=$(cat $prefix.tenant* | grep -i 'jiffy blocks' | awk '{sum += $5} END {print sum}')
    persistent_blocks=$(cat $prefix.tenant* | grep -i 'persistent blocks' | awk '{sum += $5} END {print sum}')
    total_ops=$(cat $prefix.tenant* | grep -i 'total ops' | awk '{sum += $5} END {print sum}')
    duration=$(cat $prefix.tenant*.txt | grep -i 'execution time' | head | awk '{sum += $5} END {print sum}')

    avg_latency=$(echo - | awk -v sum=$lat_sum -v count=$lat_count '{print sum/count;}')
    xput=$(echo - | awk -v sum=$total_ops -v count=$duration '{print sum/count;}')

    paste <(echo $para) <(echo $xput) <(echo $avg_latency)
done