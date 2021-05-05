import random
import copy
from heapq import *
# random.seed(1995)

def reset_map(m):
	for k in m:
		m[k] = 0

class Allocator:
	def __init__(self, demands, total_blocks, init_credits, public_blocks = 0, redistribution_freq = 1):
		self.demands = copy.deepcopy(demands)
		self.total_blocks = total_blocks
		self.init_credits = init_credits
		self.public_blocks = public_blocks
		self.redistribution_freq = redistribution_freq

		self.num_epochs = len(self.demands[list(self.demands.keys())[0]])
		self.num_tenants = len(self.demands)

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
			assert len(self.demands[t]) == self.num_epochs
			self.fair_share[t] = self.public_blocks if t == '$public$' else self.normal_share
			self.allocations[t] = []
			self.rate_map[t] = 0
			self.credit_map[t] = 0 if t == '$public$' else self.init_credits
			self.credits_history[t] = []
	
	# Compute allocation schedule
	def compute(self):
		for e in range(self.num_epochs):
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

			assert sum(self.credit_map.values()) == self.num_tenants*self.init_credits
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

		for e in range(self.num_epochs):
			assert self.allocations['$public$'][e] == 0
		
		ret = {}
		for t in self.demands:
			if t == '$public$':
				continue
			ret[t] = self.allocations[t]
		
		return ret


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



class BroadcastHeap:
	def __init__(self):
		self.base_val = 0
		self.h = []

	def push(self, key, val):
		heappush(self.h, (val-self.base_val, key))
	
	def pop(self):
		val, key = heappop(self.h)
		return (key, val + self.base_val)

	def min_val(self):
		return self.h[0][0] + self.base_val

	def size(self):
		return len(self.h)

	def add_to_all(self, delta):
		self.base_val += delta
