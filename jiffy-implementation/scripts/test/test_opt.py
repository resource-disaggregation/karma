# Testing optimized matching algorithms
from karma_sim.allocator import Allocator

class TestMatchingSupply:
    def test_one(self):
        demands = {'A': [10], 'B': [0], 'C': [1], 'D': [1]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 1, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [0], 'C': [1], 'D': [1]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D'], ['A'])
        assert alloc.rate_map['B'] == 5
        assert alloc.rate_map['C'] == 0
        assert alloc.rate_map['D'] == 0
        assert alloc.allocations['A'][0] == 10

    def test_two(self):
        demands = {'A': [10], 'B': [0], 'C': [0], 'D': [1]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 100, 'D': 1000, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [0], 'C': [0], 'D': [1]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D'], ['A'])
        assert alloc.rate_map['B'] >= 2
        assert alloc.rate_map['C'] >= 2
        assert alloc.rate_map['B'] == 3 or alloc.rate_map['C'] == 3
        assert alloc.rate_map['D'] == 0
        assert alloc.allocations['A'][0] == 10

    def test_three(self):
        demands = {'A': [10], 'B': [0], 'C': [0], 'D': [0]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [0], 'C': [0], 'D': [0]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D'], ['A'])
        assert sorted([alloc.rate_map[x] for x in ['B', 'C', 'D']]) == [1,2,2]
        assert alloc.allocations['A'][0] == 10

    def test_four(self):
        demands = {'A': [10], 'B': [0], 'C': [0], 'D': [0]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 101, 'D': 102, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [0], 'C': [0], 'D': [0]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D'], ['A'])
        res = sorted([alloc.rate_map[x] for x in ['B', 'C', 'D']])
        assert res == [1,2,2] or res == [0,2,3]
        assert alloc.allocations['A'][0] == 10

    def test_eight(self):
        demands = {'A': [10], 'B': [4], 'C': [0], 'D': [0]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 1, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [4], 'C': [0], 'D': [0]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D'], ['A'])
        assert alloc.rate_map['B'] == 1
        assert alloc.rate_map['C'] == 2
        assert alloc.rate_map['D'] == 2
        assert alloc.allocations['A'][0] == 10

    def test_five(self):
        demands = {'A': [10], 'B': [4], 'C': [4], 'D': [4]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=25, init_credits=0, public_blocks=5)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [4], 'C': [4], 'D': [4]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D', '$public$'], ['A'])
        assert alloc.rate_map['B'] == 1
        assert alloc.rate_map['C'] == 1
        assert alloc.rate_map['D'] == 1
        assert alloc.rate_map['$public$'] == 2
        assert alloc.allocations['A'][0] == 10

    def test_six(self):
        demands = {'A': [10], 'B': [3], 'C': [4], 'D': [4]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=25, init_credits=0, public_blocks=5)
        alloc.credit_map = {'A': 10, 'B': 1, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [3], 'C': [4], 'D': [4]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D', '$public$'], ['A'])
        assert alloc.rate_map['B'] == 2
        assert alloc.rate_map['C'] == 1
        assert alloc.rate_map['D'] == 1
        assert alloc.rate_map['$public$'] == 1
        assert alloc.allocations['A'][0] == 10

    def test_seven(self):
        demands = {'A': [10], 'B': [3], 'C': [3], 'D': [4]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=25, init_credits=0, public_blocks=5)
        alloc.credit_map = {'A': 10, 'B': 1, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [5], 'B': [3], 'C': [3], 'D': [4]}
        alloc.borrow_from_poorest_fast(0, ['B', 'C', 'D', '$public$'], ['A'])
        assert alloc.rate_map['B'] == 2
        assert alloc.rate_map['C'] == 2
        assert alloc.rate_map['D'] == 1
        assert alloc.rate_map['$public$'] == 0
        assert alloc.allocations['A'][0] == 10

    
class TestMatchingDemand:
    def test_one(self):
        demands = {'A': [0], 'B': [10], 'C': [10], 'D': [10]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 1, 'D': 1, '$public$': 0}
        alloc.allocations = {'A': [0], 'B': [5], 'C': [5], 'D': [5]}
        alloc.give_to_richest_fast(0, ['A'], ['B', 'C', 'D'])
        assert alloc.rate_map['A'] == 5
        assert alloc.allocations['B'][0] == 10
        assert alloc.rate_map['B'] == -5
        assert alloc.allocations['C'][0] == 5
        assert alloc.rate_map['C'] == 0
        assert alloc.allocations['D'][0] == 5
        assert alloc.rate_map['D'] == 0

    def test_two(self):
        demands = {'A': [0], 'B': [10], 'C': [10], 'D': [10]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 100, 'D': 1, '$public$': 0}
        alloc.allocations = {'A': [0], 'B': [5], 'C': [5], 'D': [5]}
        alloc.give_to_richest_fast(0, ['A'], ['B', 'C', 'D'])
        assert sorted([alloc.rate_map[x] for x in ['B', 'C', 'D']]) == [-3,-2,0]
        assert sorted([alloc.allocations[x][0] for x in ['B', 'C', 'D']]) == [5,7,8]

    def test_three(self):
        demands = {'A': [0], 'B': [10], 'C': [10], 'D': [10]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 100, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [0], 'B': [5], 'C': [5], 'D': [5]}
        alloc.give_to_richest_fast(0, ['A'], ['B', 'C', 'D'])
        assert sorted([alloc.rate_map[x] for x in ['B', 'C', 'D']]) == [-2,-2,-1]
        assert sorted([alloc.allocations[x][0] for x in ['B', 'C', 'D']]) == [6,7,7]

    def test_four(self):
        demands = {'A': [0], 'B': [10], 'C': [10], 'D': [10]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 102, 'C': 101, 'D': 100, '$public$': 0}
        alloc.allocations = {'A': [0], 'B': [5], 'C': [5], 'D': [5]}
        alloc.give_to_richest_fast(0, ['A'], ['B', 'C', 'D'])
        res = sorted([alloc.rate_map[x] for x in ['B', 'C', 'D']])
        assert res == [-3,-2,0] or res == [-2,-2,-1]
        res = sorted([alloc.allocations[x][0] for x in ['B', 'C', 'D']])
        assert res == [5,7,8] or res == [6,7,7]

    def test_five(self):
        demands = {'A': [0], 'B': [6], 'C': [10], 'D': [10]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 100, 'C': 10, 'D': 10, '$public$': 0}
        alloc.allocations = {'A': [0], 'B': [5], 'C': [5], 'D': [5]}
        alloc.give_to_richest_fast(0, ['A'], ['B', 'C', 'D'])
        assert alloc.rate_map['A'] == 5
        assert alloc.allocations['B'][0] == 6
        assert alloc.rate_map['B'] == -1
        assert alloc.allocations['C'][0] == 7
        assert alloc.rate_map['C'] == -2
        assert alloc.allocations['D'][0] == 7
        assert alloc.rate_map['D'] == -2

    def test_six(self):
        demands = {'A': [0], 'B': [10], 'C': [10], 'D': [10]}
        num_epochs = len(demands[list(demands.keys())[0]])
        alloc = Allocator(demands, total_blocks=20, init_credits=0)
        alloc.credit_map = {'A': 10, 'B': 4, 'C': 1, 'D': 0, '$public$': 0}
        alloc.allocations = {'A': [0], 'B': [5], 'C': [5], 'D': [5]}
        alloc.give_to_richest_fast(0, ['A'], ['B', 'C', 'D'])
        assert alloc.rate_map['A'] == 5
        assert alloc.allocations['B'][0] == 9
        assert alloc.rate_map['B'] == -4
        assert alloc.allocations['C'][0] == 6
        assert alloc.rate_map['C'] == -1
        assert alloc.allocations['D'][0] == 5
        assert alloc.rate_map['D'] == 0

    

