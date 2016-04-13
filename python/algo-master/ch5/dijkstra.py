import heapq

def dijkstra(g, startV):
    pot = dict() # potential node, shortest distance
    Q = []
    heapq.heappush(Q,(0,startV)) # distance, node
    while Q:
        edge = heapq.heappop(Q)
        p = edge[1]
        curr = edge[0]
        if p in pot.keys():
            continue
        pot[p] = curr
        es = g[p]
        if es :
            for e in es:
                if e[1] in pot.keys():
                    continue
                heapq.heappush(Q, (curr + e[0], e[1]) )
    return pot

import unittest
class TestDijkstra(unittest.TestCase):

    def test_two_path(self):
        g=[0]*10
        g[1] = [(2,2), (3,4)]
        g[2] = [(4,3)]
        g[3] = [(1,5)]
        g[4] = [(2,5)]
        startV = 1
        self.assertEqual(dijkstra(g,startV), {1:0, 2:2, 3:6, 4:3, 5:5})

if __name__ == '__main__':
    unittest.main()
    