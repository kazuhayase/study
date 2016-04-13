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
        if p in g.keys():
            es = g[p]
            if es :
                for e in es:
                    if e[1] in pot.keys():
                        continue
                    heapq.heappush(Q, (curr + e[0], e[1]) )
    return pot

def main():
    N,M,L,K,A,H = map(int, input().split())
    g=dict()
    for i in range(L):
        city = map(int, input().split())
        for s in range(M):
            if not (city,s) in g.keys():
                g[(city,s)] = list()
            g[(city,s)].append((1,city,s+1))
            
    for i in range(K):
        X,Y,T = map(int, input().split())
        for s in range(T,M+1):
            if not (X,s) in g.keys():
                g[(X,s)] = list()
            if not (Y,s) in g.keys():
                g[(Y,s)] = list()
            g[(X,s)].append((T,Y,s-T))
            g[(Y,s)].append((T,X,s-T))
    
    pot = dijkstra(g, (A,M))
    
    minTime = 100000000
    for s in range(M+1):
        if (H,s) not in pot:
            continue
        time = pot((H,s))
        if time < minTime:
            minTime = time
    if minTime == 100000000:
        print("Help!")
    else:
        print (minTime)

if __name__ == '__main__':
    main()
    