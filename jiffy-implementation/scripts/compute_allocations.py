# python3 compute_allocations.py test /home/midhul/snowflake_demands_nogaps10.pickle static 100 90000 0 100 0

import os, pickle, sys, random

from karma_sim.util import *
from karma_sim.allocator import Allocator,MaxMinAllocator,StaticAllocator

import math
def smoothed_avg(a, alpha, avg):
    ret = []
    ret.append(avg)
    for i in range(1, len(a)):
        prev = a[i-1]
        avg = alpha * prev + (1-alpha) * avg
        ret.append(math.ceil(avg))
    return ret

def add_noise(a, error):
    ret = []
    for x in a:
        eps = random.uniform(-1*error, error)
        ret.append(math.ceil(x + eps*x))
    return ret

def extract_list(filename):
    ret = []
    f = open(filename, 'r')
    for line in f:
        if line.strip() != '':
            ret.append(line.strip())
    f.close()

    return ret


config = sys.argv[1]
trace_file = sys.argv[2]
alloc_type = sys.argv[3]
average = int(sys.argv[4])
init_credits = int(sys.argv[5])
public_blocks = int(sys.argv[6])
guarantee = int(sys.argv[7])
oracle = bool(int(sys.argv[8]))
estimator = sys.argv[9]
error = float(sys.argv[10])
alt_file = sys.argv[11]
selfish_file = sys.argv[12]

alloc_gran = 1
if len(sys.argv) >= 14:
    alloc_gran = int(sys.argv[13])

prefix = os.path.expanduser('~/karma-eval/') + config

raw_demands = get_demands(trace_file, average)

alt_tenants = extract_list(alt_file)
selfish_tenants = extract_list(selfish_file)


demands = {}
if oracle:
    for t in raw_demands:
        demands[t] = raw_demands[t][:]
else:
    if estimator == 'savg':
        for t in raw_demands:
            demands[t] = smoothed_avg(raw_demands[t], 0.5, average)
    elif estimator == 'noise':
        print('Injecting noise')
        for t in raw_demands:
            demands[t] = add_noise(raw_demands[t], error)
    else:
        raise Exception('Unsupported estimator')

    # Simulate reclaim
    # for t in demands:
    #     for i in range(len(demands[t])):
    #         if demands[t][i] < guarantee and demands[t][i] < raw_demands[t][i]:
    #             demands[t][i] = min(raw_demands[t][i], guarantee)

# Selfish tenants
for t in selfish_tenants:
    for i in range(len(demands[t])):
        demands[t][i] = max(average, demands[t][i])


num_tenants = len(demands)
capacity = num_tenants*average
taken_away = num_tenants*(average-guarantee)

alloc = None
if alloc_type == 'static':
    alloc = StaticAllocator(raw_demands, total_blocks=capacity)
elif alloc_type == 'maxmin':
    alloc = MaxMinAllocator(raw_demands, total_blocks=capacity)
elif alloc_type == 'karma':
    alloc = Allocator(demands, total_blocks=capacity+public_blocks, init_credits=init_credits, public_blocks=taken_away + public_blocks, redistribution_thresh=taken_away, inflation=(average-guarantee))
else:
    raise Exception('unsupported allocator')

allocations = alloc.compute()

out_file = prefix + '.alloc'
with open(out_file, 'wb') as handle:
    pickle.dump(allocations, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Dumped allocations')

if alloc_type == 'karma':
    out_file = prefix + '.credits'
    with open(out_file, 'wb') as handle:
        pickle.dump(alloc.credits_history, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('Dumped credit log')






