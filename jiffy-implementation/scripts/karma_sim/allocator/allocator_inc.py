import random
import copy
import pickle
from .bheap import *
import numpy as np
random.seed(1995)

def reset_map(m):
    for k in m:
        m[k] = 0

def remove_from_list(my_list, indexes):
    for index in sorted(indexes, reverse=True):
        del my_list[index]

def trace_from_demands_tenant(demands):
    cur_tasks = []
    task_list = []
    cur_demand = 0
    num_epochs = len(demands)
    for e in range(len(demands)):
        if demands[e] > cur_demand:
            for i in range(demands[e] - cur_demand):
                cur_tasks.append({'start': e})

        elif demands[e] < cur_demand:
            for i in range(cur_demand - demands[e]):
                task = cur_tasks.pop(0)
                task_list.append({'start': task['start'], 'duration': e - task['start']})
        
        cur_demand = demands[e]

    res = [[] for _ in range(num_epochs)]
    for task in task_list:
        res[task['start']].append(task['duration'])

    return res


def trace_from_demands(demands):
    trace = {}
    for t in demands:
        trace[t] = trace_from_demands_tenant(demands[t])

    return trace



class AllocatorInc:
    def __init__(self, trace, total_blocks, init_credits, public_blocks = 0, redistribution_freq = 1, oracle=False):
        self.trace = copy.deepcopy(trace)
        self.demands = {}
        for t in trace:
            self.demands[t] = []

        self.task_seq_no = 0
        self.used_slices = []
        self.oracle = oracle
        
        self.total_blocks = total_blocks
        self.init_credits = init_credits
        self.public_blocks = public_blocks
        self.redistribution_freq = redistribution_freq

        self.tenants = list(self.trace.keys())
        self.num_epochs = len(self.trace[list(self.trace.keys())[0]])
        self.num_tenants = len(self.trace)

        # Task: {id, start, end}
        self.active_tasks = {}
        # Task: {id, start, duration}
        self.task_queue = {}
        self.task_times = {}
        for t in self.tenants:
            self.active_tasks[t] = []
            self.task_queue[t] = []
            self.task_times[t] = []

        # Initialize state
        # Add admin tenant
        self.demands['$public$'] = []
        for i in range(self.num_epochs):
            self.demands['$public$'].append(0)

        self.normal_share = ((self.total_blocks-self.public_blocks)//self.num_tenants)

        self.fair_share = {}
        self.allocations = {}
        self.rate_map = {}
        self.credit_map = {}
        self.credits_history = {}
        for t in self.demands:
            # assert len(self.trace[t]) == self.num_epochs
            self.fair_share[t] = self.public_blocks if t == '$public$' else self.normal_share
            self.allocations[t] = []
            self.rate_map[t] = 0
            self.credit_map[t] = 0 if t == '$public$' else self.init_credits
            self.credits_history[t] = []

    def pickle(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Simulate
    def compute(self):
        self.total_credits = sum([self.credit_map[t] for t in self.credit_map])
        for e in range(self.num_epochs):
            # Retire completed tasks
            for t in self.active_tasks:
                to_remove = []
                for idx in range(len(self.active_tasks[t])):
                    task = self.active_tasks[t][idx]
                    if task['end'] == e:
                        self.task_times[t].append(e - task['start'])
                        to_remove.append(idx)
                remove_from_list(self.active_tasks[t], to_remove)

            # For normal compute advertised demand
            if not self.oracle:
                for t in self.tenants:
                    adv_demand = len(self.active_tasks[t]) + len(self.task_queue[t])
                    assert len(self.demands[t]) == e
                    self.demands[t].append(adv_demand)
                    
            # Enqueue requests
            for t in self.tenants:
                for task_duration in self.trace[t][e]:
                    self.task_queue[t].append({'id': self.task_seq_no, 'start': e, 'duration': task_duration})
                    self.task_seq_no += 1

            # For oracle compute advertised demand
            if self.oracle:
                for t in self.tenants:
                    adv_demand = len(self.active_tasks[t]) + len(self.task_queue[t])
                    assert len(self.demands[t]) == e
                    self.demands[t].append(adv_demand)
                    


            # Compute allocation ---  KARMA algorithm start 

            #  Update credits
            for t in self.credit_map:
                if(self.rate_map[t] < 0):
                    assert self.allocations[t][e-1] > self.fair_share[t]
                    assert -self.rate_map[t] == self.allocations[t][e-1] - self.fair_share[t]
                self.credit_map[t] += self.rate_map[t]
                assert self.credit_map[t] >= 0
            reset_map(self.rate_map)
            # Re-distribute public credits
            if e % self.redistribution_freq == 0:
                if self.credit_map['$public$'] > self.num_tenants:
                    for t in self.credit_map:
                        if t == '$public$':
                            continue
                        self.credit_map[t] += self.credit_map['$public$'] // self.num_tenants

                    self.credit_map['$public$'] = self.credit_map['$public$'] % self.num_tenants

            assert sum(self.credit_map.values()) == self.total_credits
            # Log credits
            for t in self.credit_map:
                assert self.credit_map[t] >= 0
                assert len(self.credits_history[t]) == e
                self.credits_history[t].append(self.credit_map[t])
                # if(self.credits_history[t][e] < self.credits_history[t][e-1]):
                    # assert self.allocations[t][e-1] > self.fair_share[t]
                    # assert self.credits_history[t][e-1] - self.credits_history[t][e] == self.allocations[t][e-1] - self.fair_share[t]

            # Allocate blocks
            donors = [t for t in self.demands if self.demands[t][e] < self.fair_share[t]]
            borrowers = [t for t in self.demands if self.demands[t][e] > self.fair_share[t]]
            total_supply = sum([(self.fair_share[t] - self.demands[t][e]) for t in donors])
            total_demand = sum([min(self.demands[t][e] - self.fair_share[t], self.credit_map[t]) for t in borrowers])
            # print(total_supply,total_demand)

            for t in self.demands:
                assert len(self.allocations[t]) == e
                self.allocations[t].append(min(self.demands[t][e], self.fair_share[t]))

            if total_supply >= total_demand:
                    num_exchanged = self.borrow_from_poorest_fast(e, donors, borrowers)
                    assert num_exchanged == total_demand

            elif total_supply < total_demand:
                    num_exchanged = self.give_to_richest_fast(e, donors, borrowers)
                    assert num_exchanged == total_supply

            # Compute allocation ---  KARMA algorithm end

            # Start / revoke tasks
            for t in self.tenants:
                while len(self.active_tasks[t]) > self.allocations[t][e]:
                    # Preempt task
                    idx = random.randrange(len(self.active_tasks[t]))
                    task = self.active_tasks[t][idx]
                    left_over = task['end'] - e
                    self.task_queue[t].insert(0, {'id': task['id'], 'start': task['start'], 'duration': left_over})
                    del self.active_tasks[t][idx]

                # Start running new tasks
                while len(self.task_queue[t]) > 0 and len(self.active_tasks[t]) < self.allocations[t][e]:
                    task = self.task_queue[t][0]
                    self.active_tasks[t].append({'id': task['id'], 'start': task['start'], 'end': e + task['duration']})
                    del self.task_queue[t][0]

            # Compute used slices
            assert len(self.used_slices) == e
            self.used_slices.append(sum([len(self.active_tasks[t]) for t in self.tenants]))

        for e in range(self.num_epochs):
            assert self.allocations['$public$'][e] == 0
        
        ret = {}
        for t in self.demands:
            if t == '$public$':
                continue
            ret[t] = self.allocations[t]
        
        summary = {}
        summary['util'] = np.mean([float(x)/self.total_blocks for x in self.used_slices])
        agg_task_time = 0
        agg_task_count = 0
        for t in self.task_times:
            agg_task_time += sum(self.task_times[t])
            agg_task_count += len(self.task_times[t])
        summary['avg_task_time'] = float(agg_task_time)/float(agg_task_count)
        return summary


    def borrow_from_poorest(self, e, donors, borrowers):
        credit_map = self.credit_map
        allocations = self.allocations
        rate_map = self.rate_map
        fair_share = self.fair_share
        demands = self.demands

        num_exchanged = 0
        donor_credits = {}
        for t in donors:
            donor_credits[t] = credit_map[t]
        borrower_credits = {}
        for t in borrowers:
            borrower_credits[t] = credit_map[t]

        # Always prioritize normal tenants over admin tenant
        if '$public$' in donor_credits:
            donor_credits['$public$'] = float('inf')

        for b in borrowers:
            to_borrow = min(borrower_credits[b], demands[b][e] - fair_share[b])
            for i in range(to_borrow):
                active_donors = [d for d in donors if donor_credits[d] - credit_map[d] < fair_share[d] - demands[d][e]]
                min_credits = min([donor_credits[d] for d in active_donors])
                poorest_donors = [d for d in active_donors if donor_credits[d] == min_credits]
                poorest_donor = random.choice(poorest_donors)
                allocations[b][e] += 1
                rate_map[b] -= 1
                rate_map[poorest_donor] += 1
                # Speculatively increase donor credits
                donor_credits[poorest_donor] += 1
                num_exchanged += 1

        return num_exchanged

    def give_to_richest(self, e, donors, borrowers):
        credit_map = self.credit_map
        allocations = self.allocations
        rate_map = self.rate_map
        fair_share = self.fair_share
        demands = self.demands

        num_exchanged = 0
        donor_credits = {}
        for t in donors:
            donor_credits[t] = credit_map[t]
        borrower_credits = {}
        for t in borrowers:
            borrower_credits[t] = credit_map[t]

        for d in donors:
            to_give = fair_share[d] - demands[d][e]
            for i in range(to_give):
                active_borrowers = [b for b in borrowers if allocations[b][e] < demands[b][e]]
                max_credits = max([borrower_credits[b] for b in active_borrowers])
                richest_borrowers = [b for b in active_borrowers if borrower_credits[b] == max_credits]
                if max_credits <= 0:
                    return num_exchanged
                richest_borrower = random.choice(richest_borrowers)
                allocations[richest_borrower][e] += 1
                rate_map[richest_borrower] -= 1
                rate_map[d] += 1
                # Speculatively increase borrower credits
                borrower_credits[richest_borrower] -= 1
                num_exchanged += 1

        return num_exchanged


    def borrow_from_poorest_fast(self, e, donors, borrowers):
        credit_map = self.credit_map
        allocations = self.allocations
        rate_map = self.rate_map
        fair_share = self.fair_share
        demands = self.demands

        # Can satisfy all demands of borrowers
        total_demand=0
        for b in borrowers:
            to_borrow = min(credit_map[b], demands[b][e] - fair_share[b])
            allocations[b][e] += to_borrow
            rate_map[b] -= to_borrow
            total_demand += to_borrow

        
        # Borrow from poorest donors and update their rate maps
        donor_list = []
        for d in donors:
            d_credits = credit_map[d] if d != '$public$' else self.num_tenants*self.init_credits + 7777777777
            donor_list.append({'id': d, 'c': d_credits, 'x': fair_share[d] - demands[d][e]})
        donor_list.append({'id': '$dummy$', 'c': float('inf'), 'x': 0})
        

        # sort donor_list by credits
        donor_list.sort(key=lambda x: x['c'])

        dem = total_demand
        cur_c = -1
        next_c = donor_list[0]['c']
        # poorest active donor set (heap internally ordered by x)
        poorest_donors = BroadcastHeap()
        idx = 0
        while dem > 0:
            # update poorest_donors
            if poorest_donors.size() == 0:
                cur_c = next_c
                assert cur_c != float('inf')
            while donor_list[idx]['c'] == cur_c:
                poorest_donors.push(donor_list[idx]['id'], donor_list[idx]['x'])
                idx += 1
            next_c = donor_list[idx]['c']
            
            # perform c,x update
            if dem < poorest_donors.size():
                for i in range(dem):
                    d, x = poorest_donors.pop()
                    x -= 1
                    dem -= 1
                    rate_map[d] += fair_share[d] - demands[d][e] - x
            else:
                alpha = min(poorest_donors.min_val(), dem//poorest_donors.size(), next_c - cur_c)
                poorest_donors.add_to_all(-1*alpha)
                cur_c += alpha
                dem -= poorest_donors.size() * alpha
                

            # get rid of donors with x = 0
            while poorest_donors.size() > 0 and poorest_donors.min_val() == 0:
                d, _ = poorest_donors.pop()
                rate_map[d] += fair_share[d] - demands[d][e]
            
        while poorest_donors.size() > 0:
            d, x = poorest_donors.pop()
            rate_map[d] += fair_share[d] - demands[d][e] - x

        return total_demand

    def give_to_richest_fast(self, e, donors, borrowers):
        credit_map = self.credit_map
        allocations = self.allocations
        rate_map = self.rate_map
        fair_share = self.fair_share
        demands = self.demands

        # Can match all donations
        total_supply=0
        for d in donors:
            to_give = fair_share[d] - demands[d][e]
            rate_map[d] += to_give
            total_supply += to_give

        # Give to richest borrowers and update their allocations/rate_map
        borrower_list = []
        for b in borrowers:
            b_credits = credit_map[b]
            borrower_list.append({'id': b, 'c': b_credits, 'x': min(credit_map[b], demands[b][e] - fair_share[b])})
        borrower_list.append({'id': '$dummy$', 'c': float('-inf'), 'x': 0})

        borrower_list.sort(key=lambda x: x['c'], reverse=True)

        sup = total_supply
        cur_c = float('inf')
        next_c = borrower_list[0]['c']
        # richest active borrower set (heap internally ordered by x)
        richest_borrowers = BroadcastHeap()
        idx = 0
        while sup > 0:
            # update richest_borrowers
            if richest_borrowers.size() == 0:
                cur_c = next_c
                assert cur_c != float('-inf')
            while borrower_list[idx]['c'] == cur_c:
                richest_borrowers.push(borrower_list[idx]['id'], borrower_list[idx]['x'])
                idx += 1
            next_c = borrower_list[idx]['c']

            # perform c,x update
            if sup < richest_borrowers.size():
                for i in range(sup):
                    b, x = richest_borrowers.pop()
                    x -= 1
                    sup -= 1
                    allocations[b][e] += min(credit_map[b], demands[b][e] - fair_share[b]) - x
                    rate_map[b] -= min(credit_map[b], demands[b][e] - fair_share[b]) - x
            else:
                alpha = min(richest_borrowers.min_val(), sup//richest_borrowers.size(), cur_c - next_c)
                richest_borrowers.add_to_all(-1*alpha)
                cur_c -= alpha
                sup -= richest_borrowers.size() * alpha

            # get rid of borrowers with x = 0
            while richest_borrowers.size() > 0 and richest_borrowers.min_val() == 0:
                b, _ = richest_borrowers.pop()
                allocations[b][e] += min(credit_map[b], demands[b][e] - fair_share[b])
                rate_map[b] -= min(credit_map[b], demands[b][e] - fair_share[b])


        while richest_borrowers.size() > 0:
            b, x = richest_borrowers.pop()
            allocations[b][e] += min(credit_map[b], demands[b][e] - fair_share[b]) - x
            rate_map[b] -= min(credit_map[b], demands[b][e] - fair_share[b]) - x


        return total_supply

