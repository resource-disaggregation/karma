# import random
# random.seed(1995)
import pickle
import math

def extract_demands(filename, scale_factor):
	ret = {}
	f = open(filename, 'r')
	idx = 0
	first = True
	for l in f:
		if first:
			first = False
			continue

		cols = l.strip().split(',')
		assert len(cols) == 5

		tenant_id = cols[0]
		norm_demand = float(cols[4])
		di = int(norm_demand * scale_factor)
		if not tenant_id in ret:
			ret[tenant_id] = []

		ret[tenant_id].append(di)
	f.close()
	return ret

def get_demands(filename, scale_factor):
	with open(filename, 'rb') as handle:
		norm_d = pickle.load(handle)

	ret = {}
	for t in norm_d:
		ret[t] = []
		for i in range(len(norm_d[t])):
			ret[t].append(math.ceil(norm_d[t][i] * scale_factor))

	return ret

def load_obj(filename):
	with open(filename, 'rb') as handle:
		return pickle.load(handle)


# # Compute utilization
# used_capacity = 0
# for t in demands:
# 	if t == '$public$':
# 		continue
# 	used = []
# 	for e in xrange(num_epochs):
# 		used.append(min(allocations[t][e], raw_demands[t][e]))
# 		# used.append(allocations[t][e])
# 		# print (allocations[t][e], raw_demands[t][e])
# 	used_capacity += sum(used)

# util = float(used_capacity)/float(total_blocks * num_epochs)
# print 'Utilization'
# print util

# # Compute fairness
# xs = []
# for t in allocations:
# 	if t == '$public$':
# 		continue
# 	xs.append(sum(allocations[t]))
# assert len(xs) == num_tenants

# num = (sum(xs))**2
# den = num_tenants * sum([xi**2 for xi in xs])
# fairness = float(num)/float(den)
# print 'Fairness'
# print fairness

# print 'Welfares'
# alt_welfares = []
# for t in demands:
# 	if t == '$public$':
# 		continue
# 	mismatch = [(allocations[t][e] - fair_share[t]) for e in xrange(num_epochs) if raw_demands[t][e] > fair_share[t]]

# 	avg_welfare = sum(mismatch)/float(len(mismatch))
# 	print t + ': ' + str(avg_welfare) + ', ' + str(t in na_tenants)
# 	if not t in na_tenants:
# 		alt_welfares.append(avg_welfare)

# print 'Avg welfare of alt tenants'
# assert len(alt_welfares) == altruistic_tenants
# print sum(alt_welfares)/len(alt_welfares)


# print 'non-altruistic tenants bankrupt'
# for t in na_tenants:
# 	assert all(x>=y for x, y in zip(credits_history[t], credits_history[t][1:]))
# 	for e in xrange(num_epochs):
# 		if credits_history[t][e] == 0:
# 			print t + ': ' + str(e)
# 			break
# 	print 'Last credits ' + t + ': ' + str(credits_history[t][num_epochs-1])


# out_allocs = []
# out_demands = []
# out_tenants = []
# out_credits = []
# for t in sorted(demands.keys()):
# 	if t == '$public$':
# 		continue
# 	out_tenants = []
# 	out_demands.append(','.join([str(x) for x in demands[t]]))
# 	out_allocs.append(','.join([str(x) for x in allocations[t]]))
# 	out_credits.append(','.join([str(x) for x in credits_history[t]]))

# f = open('traces/'+exp_name+'.txt', 'w')
# f.write('data=' + '|'.join(out_allocs))
# f.write('\n')
# f.write('demands=' + '|'.join(out_demands))
# f.write('\n')
# # f.write('credits=' + '|'.join(out_credits))

# f.close()