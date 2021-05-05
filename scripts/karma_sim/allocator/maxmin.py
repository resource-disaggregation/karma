import copy
import pickle
from .bheap import *

class MaxMinAllocator:
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
        for e in range(self.num_epochs):
            # Allocate blocks
            total_demand = sum([self.demands[t][e] for t in self.demands])

            if self.total_blocks >= total_demand:
                # We can satisfy everyone's demands
                for t in self.demands:
                    assert len(self.allocations[t]) == e
                    self.allocations[t].append(self.demands[t][e])

            if self.total_blocks < total_demand:
                # Waterfilling algorithm
                active_tenants = BroadcastHeap()
                for t in self.demands:
                    active_tenants.push(t, self.demands[t][e])
                    self.allocations[t].append(0)

                sup = self.total_blocks
                while sup > 0:
                    if sup < active_tenants.size():
                        for i in range(sup):
                            t, x = active_tenants.pop()
                            x -= 1
                            sup -= 1
                            self.allocations[t][e] = self.demands[t][e] - x
                    else:
                        alpha = min(active_tenants.min_val(), sup//active_tenants.size())
                        active_tenants.add_to_all(-1*alpha)
                        sup -= active_tenants.size() * alpha
                
                    # get rid of tenants with x = 0
                    while active_tenants.size() > 0 and active_tenants.min_val() == 0:
                        t, _ = active_tenants.pop()
                        self.allocations[t][e] = self.demands[t][e]
                
                while active_tenants.size() > 0:
                        t, x = active_tenants.pop()
                        self.allocations[t][e] = self.demands[t][e] - x

        return self.allocations
