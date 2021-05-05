from heapq import *

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