import os, pickle, sys

from karma_sim.util import *
from karma_sim.allocator import Allocator,MaxMinAllocator,StaticAllocator

def compute_utilization(allocations, raw_demands, total_blocks):
    num_epochs = len(allocations[list(allocations.keys())[0]])
    used_capacity = 0
    for t in allocations:
        used = []
        for e in range(num_epochs):
            used.append(min(allocations[t][e], raw_demands[t][e]))
        used_capacity += sum(used)
    util = float(used_capacity)/float(total_blocks * num_epochs)
    return util

def compute_fairness(allocations):
    sum_allocs = []
    for t in allocations:
        sum_allocs.append(sum(allocations[t]))

    return float(min(sum_allocs))/float(max(sum_allocs))

def compute_jiffy_blocks(allocations, raw_demands):
    num_epochs = len(allocations[list(allocations.keys())[0]])
    used_capacity = 0
    for t in allocations:
        used = []
        for e in range(num_epochs):
            used.append(min(allocations[t][e], raw_demands[t][e]))
        used_capacity += sum(used)
    return used

def compute_s3_blocks(allocations, raw_demands):
    total_blocks = 0
    for t in raw_demands:
        total_blocks += sum(raw_demands[t])
    
    return total_blocks - compute_jiffy_blocks(allocations, raw_demands)


config = sys.argv[1]
trace_file = sys.argv[2]
fair_share = int(sys.argv[3])
total_blocks = int(sys.argv[4])

prefix = '/home/ubuntu/karma-eval/'
alloc_file = prefix + config + '.alloc'
with open(alloc_file, 'rb') as handle:
    allocs = pickle.load(handle)

raw_demands = get_demands(trace_file, fair_share)

print('Utilization')
print(compute_utilization(allocs, raw_demands, total_blocks))

print('Fairness (min/max)')
print(compute_fairness(allocs))

print('Jiffy blocks')
print(compute_jiffy_blocks(allocs, raw_demands))

print('S3 blocks')
print(compute_s3_blocks(allocs, raw_demands))
