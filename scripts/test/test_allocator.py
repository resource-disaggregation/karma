import random
random.seed(1995)

from karma_sim.allocator import Allocator

# demands = {'tenant0': [8,14,8,8,14,8,8,14,8,8,14,8], 'tenant1': [6,12,12,6,12,12,6,12,12,6,12,12]}
# num_epochs = len(demands[demands.keys()[0]])
# num_tenants = len(demands)

# total_blocks = (num_tenants * 160)
# public_blocks = int(0.00*total_blocks)
# init_credits = 160*10*2065
# redistribution_freq = 1

# Basic sanity checks
def basic_checks(demands, allocations):
    assert len(demands) == len(allocations)
    num_epochs = len(demands[list(demands.keys())[0]])
    for t in allocations:
        assert len(allocations[t]) == num_epochs

    # allocation can never exceed demand
    for t in demands:
        for e in range(num_epochs):
            assert allocations[t][e] >= 0
            assert allocations[t][e] <= demands[t][e]

# Checks on credit assignment
def credit_checks(demands, allocations, credit_history, fair_share):
    num_epochs = len(demands[list(demands.keys())[0]])
    for t in demands:
        for e in range(1, num_epochs):
            if credit_history[t][e] > credit_history[t][e-1]:
                assert demands[t][e-1] < fair_share
                assert credit_history[t][e] - credit_history[t][e-1] <= fair_share - demands[t][e-1]
            elif credit_history[t][e] < credit_history[t][e-1]:
                assert demands[t][e-1] > fair_share and allocations[t][e-1] > fair_share
                assert credit_history[t][e-1] - credit_history[t][e] == allocations[t][e-1] - fair_share

class TestAllocator:
    def test_static_simple(self):
        demands = {'A': [1, 3, 5, 7, 10, 0], 'B': [10, 8, 0, 5, 3, 1]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=10, init_credits=0)
        allocations = alloc.compute()
        basic_checks(demands, allocations)
        for t in demands:
            for e in range(num_epochs):
                assert allocations[t][e] <= 5
                assert allocations[t][e] == min(demands[t][e], 5)
    
    def test_inf_simple(self):
        demands = {'A': [1, 3, 5, 7, 10, 0], 'B': [10, 8, 0, 5, 3, 1]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=10, init_credits=999999)
        allocations = alloc.compute()
        basic_checks(demands, allocations)
        for e in range(num_epochs):
            total_allocation = 0
            total_demand = 0
            for t in demands:
                # Isolation
                assert allocations[t][e] >= min(demands[t][e], 5)
                total_allocation += allocations[t][e]
                total_demand += allocations[t][e]
            # Work conservation
            assert total_allocation == min(total_demand, 10)

    def test_inf_random(self):
        num_tenants = 5
        num_epochs = 2000
        demands = {}
        for i in range(5):
            t = 'tenant%d' % (i)
            demands[t] = []
            for e in range(num_epochs):
                # Uniform random between 0,20. Avg => 10
                demands[t].append(random.randrange(0,21))
        alloc = Allocator(demands, total_blocks=50, init_credits=999999999)
        allocations = alloc.compute()
        basic_checks(demands, allocations)
        for e in range(num_epochs):
            total_allocation = 0
            total_demand = 0
            for t in demands:
                # Isolation
                assert allocations[t][e] >= min(demands[t][e], 10)
                total_allocation += allocations[t][e]
                total_demand += allocations[t][e]
            # Work conservation
            assert total_allocation == min(total_demand, 50)
        
        credit_checks(demands, allocations, alloc.credits_history, 10)

    def test_limited_random(self):
        num_tenants = 5
        num_epochs = 2000
        demands = {}
        for i in range(5):
            t = 'tenant%d' % (i)
            demands[t] = []
            for e in range(num_epochs):
                # Uniform random between 0,20. Avg => 10
                demands[t].append(random.randrange(0,21))
        alloc = Allocator(demands, total_blocks=50, init_credits=10)
        allocations = alloc.compute()
        basic_checks(demands, allocations)
        for e in range(num_epochs):
            total_allocation = 0
            total_demand = 0
            for t in demands:
                # Isolation
                assert allocations[t][e] >= min(demands[t][e], 10)
                total_allocation += allocations[t][e]
                total_demand += allocations[t][e]
        
        credit_checks(demands, allocations, alloc.credits_history, 10)


