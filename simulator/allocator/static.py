import copy
import pickle

class StaticAllocator:
    def __init__(self, demands, total_blocks):
        self.demands = copy.deepcopy(demands)
        self.total_blocks = total_blocks

        self.num_epochs = len(self.demands[list(self.demands.keys())[0]])
        self.num_tenants = len(self.demands)

        self.fair_share = self.total_blocks//self.num_tenants

        self.allocations = {}
        for t in self.demands:
            assert len(self.demands[t]) == self.num_epochs
            self.allocations[t] = []

    def pickle(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def compute(self):
        for t in self.demands:
            self.allocations[t] = [self.fair_share for e in range(self.num_epochs)]

        return self.allocations

