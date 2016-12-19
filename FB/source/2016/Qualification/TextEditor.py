def main():
    T = int(input())
    
    for t in range(T):
        N,K = map(int, input().split())
        W = [input() for n in range(N)]
        W.sort()
        MAXCOST = 100000*2*300
        cost=[[0 for i in range(N)] for j in range(K+1)]
        com=[0 for i in range(N)]
        for i in range(N):
            cost[0][i] = 0
            cost[1][i] = len(W[i]) * 2
            if i == N-1:
                com[i]=0
                continue
            else:
                com[i] = 0
                length = min(len(W[i]), len(W[i+1]))
                for j in range(length):
                    if W[i][j] == W[i+1][j]:
                        com[i] += 1
                    else:
                        break
        
        for size in range(2,K+1):
            for i in range(0,N+1-size):
                cost[size][i] = cost[size-1][i] + cost[1][i+size-1] - 2 * com[i+size-1]
        
        res = MAXCOST
        for size in range(K,int(K/2)-2,-1):
                for i in range(0, N-K+1):
                    for j in range(i+size,N-(K-size)):
                        if res > cost[size][i] + cost[K-size][j]:
                            res = cost[size][i] + cost[K-size][j]
                    for j in range(0,i-size):
                        if res > cost[size][i] + cost[K-size][j]:
                            res = cost[size][i] + cost[K-size][j]

        print("Case #{}: {}".format(t+1, res+K))
            
if __name__ == '__main__':
    main()