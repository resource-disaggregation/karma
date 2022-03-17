import sys
import pickle

# python3 microbench_pickles.py $num_tenants $fair_share $duration ~/karma-eval/microbench_demands.pickle ~/karma-eval/microbench_allocs.pickle

num_tenants = int(sys.argv[1])
fair_share = int(sys.argv[2])
duration = int(sys.argv[3])
demands_out = sys.argv[4]
allocs_out = sys.argv[5]

demands = {}
allocs = {}

for t in range(num_tenants):
    demands[t] = []
    allocs[t] = []
    for e in range(duration):
        demands[t].append(fair_share)
        allocs[t].append(fair_share)


with open(demands_out, 'wb') as handle:
    pickle.dump(demands, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(allocs_out, 'wb') as handle:
    pickle.dump(allocs, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Dumped pickles')