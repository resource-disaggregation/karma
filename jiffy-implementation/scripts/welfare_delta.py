import sys, pickle

from karma_sim.util import *

tenants_file = sys.argv[1]
config1 = sys.argv[2]
config2 = sys.argv[3]
trace_file = sys.argv[4]
average = int(sys.argv[5])

prefix = '/home/ubuntu/karma-eval/'

def extract_list(filename):
    ret = []
    f = open(filename, 'r')
    for line in f:
        if line.strip() != '':
            ret.append(line.strip())
    f.close()

    return ret

def compute_welfare(config, tenants, trace_file, average):
    alloc_file = prefix + config + '.alloc'
    with open(alloc_file, 'rb') as handle:
        allocations = pickle.load(handle)

    raw_demands = get_demands(trace_file, average)

    num_epochs = len(allocations[list(allocations.keys())[0]])
    tenant_welfares = []
    for t in tenants:
        used = []
        for e in range(num_epochs):
            used.append(min(allocations[t][e], raw_demands[t][e]))
        sum_used = sum(used)
        sum_demands = sum(raw_demands[t])
        welfare = float(sum_used)/float(sum_demands)
        tenant_welfares.append(welfare)
    
    avg_welfare = sum(tenant_welfares) / len(tenants)

    return avg_welfare



tenants = extract_list(tenants_file)
w1 = compute_welfare(config1, tenants, trace_file, average)
print('Welfare 1')
print(w1)

w2 = compute_welfare(config2, tenants, trace_file, average)
print('Welfare 2')
print(w2)

print('Welfare improvement 1->2')
print(w2/w1)


