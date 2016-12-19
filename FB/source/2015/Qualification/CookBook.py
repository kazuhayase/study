def main():
    T = int(input())
    
    for t in range(T):
        N = list(input())
        l = len(N)
        s = set()
        for a in range(l):
            for b in range(l):
                m = N[:]
                m[a], m[b] = m[b], m[a]
                if not m[0] == '0':
                    s.add(int("".join(m)))
        if not s:
            s.add(0)
        print("Case #{}: {} {}".format(t+1, min(s), max(s)))
            
if __name__ == '__main__':
    main()