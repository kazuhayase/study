import heapq

T = int(input())
    
for t in range(T):
    L,N,M,D = map(int, (input().split()))
    W = list(map(int, input().split()))
    
    we = [0]*N
    db = [0]*L
    de = [0]*L
    
    for i in range(N):
        we[i] = (W[i],W[i])
    heapq.heapify(we)
        
    for l in range(L):
        (ti,w) = heapq.heappop(we)
        db[l] = ti
        heapq.heappush(we, (ti+w, w))
        
        #idx = we.index(min(we))
        #db[l] = we[idx]
        #we[idx] += W[idx]
    
    db.sort()
    
    m = [0 for i in range(min(L,M))]
    heapq.heapify(m)
    
    for l in range(L):
        ti = heapq.heappop(m)
        de[l] = max(db[l], ti) + D
        heapq.heappush(m,de[l])
        #idx = m.index(min(m))
        #de[l] = max(db[l], m[idx]) + D
        #m[idx] = de[l]
    
    print("Case #{}: {}".format(t+1, max(de)))
