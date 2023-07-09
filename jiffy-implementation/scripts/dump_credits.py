import os, pickle, sys

filename = sys.argv[1]

with open(filename, 'rb') as handle:
    credits_history = pickle.load(handle)

for t in credits_history:
    print(t + '\t' + str(credits_history[t][-1]))

for t in credits_history:
    for x in credits_history[t]:
        if x == 0:
            print('Tenant hit 0 creds ' + str(t) + ', ' + str(x))