import bisect
MOD = 1000000007
def main():
    T = int(input())
    
    for t in range(T):
        N = int(input())
        res = 0
        height = []
        ladder = dict()
        inp = []
        for i in range(N):
            X,H = map(int,input().split())
            bisect.insort(inp, (X,H))
            
        for (X,H) in inp:
            if not H in ladder.keys():
                bisect.insort(height,H)
                ladder[H] = []
            l = bisect.bisect_left(height, H)
            ladder[H].append(X)
            for h in height[:l]:
                del ladder[h]
            height = height[l:]
            for x in ladder[H]:
                res += (x-X) * (x-X)
                res %= MOD
                    
        print("Case #{}: {}".format(t+1, res))
            
if __name__ == '__main__':
    main()
    