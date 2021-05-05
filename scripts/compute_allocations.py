# python3 compute_allocations.py test /home/midhul/snowflake_demands_nogaps10.pickle static 100 90000 0

import os, pickle, sys

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


config = sys.argv[1]
trace_file = sys.argv[2]
alloc_type = sys.argv[3]
fair_share = int(sys.argv[4])
init_credits = int(sys.argv[5])
public_blocks = int(sys.argv[6])

prefix = '/home/midhul/karma-eval/' + config

raw_demands = get_demands(trace_file, fair_share)

demands = {}
for t in raw_demands:
    demands[t] = smoothed_avg(raw_demands[t], 0.5, fair_share)

# Simulate reclaim
for t in demands:
    for i in range(len(demands[t])):
        if demands[t][i] < fair_share and demands[t][i] < raw_demands[t][i]:
            demands[t][i] = min(raw_demands[t][i], fair_share)

num_tenants = len(demands)
capacity = num_tenants*fair_share

alloc = None
if alloc_type == 'static':
    alloc = StaticAllocator(raw_demands, total_blocks=capacity)
elif alloc_type == 'maxmin':
    alloc = MaxMinAllocator(raw_demands, total_blocks=capacity)
elif alloc_type == 'karma':
    alloc = Allocator(demands, total_blocks=capacity+public_blocks, init_credits=init_credits, public_blocks=public_blocks)
else:
    raise Exception('unsupported allocator')

allocations = alloc.compute()

out_file = prefix + '.alloc'
with open(out_file, 'wb') as handle:
    pickle.dump(allocations, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Dumped allocations')






