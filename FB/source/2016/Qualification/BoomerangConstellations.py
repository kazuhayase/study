def main():
    T = int(input())
    
    for t in range(T):
        N = int(input())
        s = set()
        m = dict()
        for i in range (N):
            x,y = map(int, input().split())
            s.add((x,y))
    
        for p in s:
            for q in s:
                if not p == q:
                    dist = (p[0] - q[0])**2 + (p[1]-q[1])**2
                    if not dist in m:
                        ss = set()
                        m[dist] = ss
                    else :
                        ss = m[dist]
                    ss.add((min(p,q), max(p,q)))
        res = 0;
        for d in iter(m):
            size = len(m[d])
            if size > 1:
                for (p,q) in m[d]:
                    for (pp,qq) in m[d]:
                        if p == pp and q == qq:
                            continue
                        if p == pp or p == qq or q == pp or q == qq:
                            res += 1
        
        res = int(res/2)
                
        print("Case #{}: {}".format(t+1, res))
            
if __name__ == '__main__':
    main()