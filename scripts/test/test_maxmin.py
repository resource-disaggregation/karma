import random
random.seed(1995)

from karma_sim.allocator import MaxMinAllocator

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


class TestMaxMinAllocator:
    def test_simple(self):
        demands = {'A': [1, 3, 5, 7, 10, 0], 'B': [10, 8, 0, 5, 3, 1]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = MaxMinAllocator(demands, total_blocks=10)
        allocations = alloc.compute()
        basic_checks(demands, allocations)
        assert allocations['A'] == [1,3,5,5,7,0]
        assert allocations['B'] == [9,7,0,5,3,1]

    def test_two(self):
        demands = {'A': [10], 'B': [10], 'C': [10]}
        alloc = MaxMinAllocator(demands, total_blocks=15)
        allocations = alloc.compute()
        assert allocations['A'] == [5]
        assert allocations['B'] == [5]
        assert allocations['C'] == [5]

    def test_three(self):
        demands = {'A': [3], 'B': [10], 'C': [10]}
        alloc = MaxMinAllocator(demands, total_blocks=15)
        allocations = alloc.compute()
        assert allocations['A'] == [3]
        assert allocations['B'] == [6]
        assert allocations['C'] == [6]

    def test_four(self):
        demands = {'A': [1], 'B': [9], 'C': [6]}
        alloc = MaxMinAllocator(demands, total_blocks=15)
        allocations = alloc.compute()
        assert allocations['A'] == [1]
        assert allocations['B'] == [8]
        assert allocations['C'] == [6]

    def test_random(self):
        num_tenants = 5
        num_epochs = 2000
        demands = {}
        for i in range(5):
            t = 'tenant%d' % (i)
            demands[t] = []
            for e in range(num_epochs):
                # Uniform random between 0,20. Avg => 10
                demands[t].append(random.randrange(0,21))
        alloc = MaxMinAllocator(demands, total_blocks=50)
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
