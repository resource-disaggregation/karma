import os, pickle, sys, random

from karma_sim.util import *
from karma_sim.allocator import Allocator,MaxMinAllocator,StaticAllocator

random.seed()

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

def compute_fairness(allocations, raw_demands):
    num_epochs = len(allocations[list(allocations.keys())[0]])
    sum_allocs = []
    for t in allocations:
        used = []
        for e in range(num_epochs):
            used.append(min(allocations[t][e], raw_demands[t][e]))
        sum_allocs.append(sum(used))

    return float(min(sum_allocs))/float(max(sum_allocs))

def compute_perf_cdf(allocations, raw_demands, s3_lat, jiffy_lat):
    num_epochs = len(allocations[list(allocations.keys())[0]])
    lats = []
    for t in allocations:
        used = []
        demands = []
        for e in range(num_epochs):
            used.append(min(allocations[t][e], raw_demands[t][e]))
            demands.append(raw_demands[t][e])

        jiffy_blocks = sum(used)
        s3_blocks = sum(demands) - sum(used)
        avg_lat = (jiffy_blocks*jiffy_lat + s3_blocks*s3_lat)/(jiffy_blocks + s3_blocks)
        lats.append(avg_lat)

    return sorted(lats)[::-1]


def compute_inst_fairness(allocations, raw_demands):
    num_epochs = len(allocations[list(allocations.keys())[0]])
    ret = []
    for e in range(num_epochs):
        utys = []
        for t in allocations:
            uty = float(min(raw_demands[t][e], allocations[t][e]))/float(raw_demands[t][e]) if raw_demands[t][e] > 0 else 1.0
            utys.append(uty)
        inst_fairness = min(utys) / max(utys)
        ret.append(inst_fairness)

    return ret

def compute_jiffy_blocks(allocations, raw_demands):
    num_epochs = len(allocations[list(allocations.keys())[0]])
    used_capacity = 0
    for t in allocations:
        used = []
        for e in range(num_epochs):
            used.append(min(allocations[t][e], raw_demands[t][e]))
        used_capacity += sum(used)
    return used_capacity

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
print(compute_fairness(allocs, raw_demands))

jiffy_blocks = compute_jiffy_blocks(allocs, raw_demands)
print('Jiffy blocks')
print(jiffy_blocks)

s3_blocks = compute_s3_blocks(allocs, raw_demands)
print('S3 blocks')
print(s3_blocks)

est_s3_lat = random.uniform(0.053, 0.057)
est_jiffy_lat = random.uniform(0.00085, 0.00095)

est_lat = (jiffy_blocks*est_jiffy_lat + s3_blocks*est_s3_lat)/(jiffy_blocks + s3_blocks)
print('Est avg latency')
print(est_lat)

print('perf cdf')
cdf = compute_perf_cdf(allocs, raw_demands, est_s3_lat, est_jiffy_lat)
for x in cdf:
    print(x)
# print('Avg Inst fairness')
# inst_fairness = compute_inst_fairness(allocs, raw_demands)
# inst_fairness.sort(reverse=True)
# for i in range(len(inst_fairness)):
#     print(str(i) + '\t' + str(inst_fairness[i]))
# print(sum(inst_fairness) / len(inst_fairness))
