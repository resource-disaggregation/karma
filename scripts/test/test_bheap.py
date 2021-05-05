from karma_sim.allocator import BroadcastHeap

class TestBroadcastHeap:
    def test_simple(self):
        h = BroadcastHeap()
        assert h.size() == 0
        h.push('a', 7)
        h.push('b', 1)
        assert h.size() == 2
        h.add_to_all(10)
        k, v = h.pop()
        assert k == 'b'
        assert v == 11
        h.push('c', 1)
        assert h.size() == 2
        k, v = h.pop()
        assert k == 'c'
        assert v == 1
        


