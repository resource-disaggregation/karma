import os, pickle, sys

filename = sys.argv[1]

with open(filename, 'rb') as handle:
    credits_history = pickle.load(handle)

for t in credits_history:
    print(t + '\t' + credits_history[900])