def sieve(n):
    ps = [True for i in range(n+1)]
    ps[0] = False
    ps[1] = False
    for i in range(2,n):
        if not ps[i]:
            continue
        for k in range (2, int(n/i)):
            ps[k * i] = False
    return ps

if __name__ == '__main__':
    ps = sieve(1000000)
    while True:
        k = int(input())
        if k == 0:
            break
        count=0;
        for a in range(1,1000000):
            if ps[a] and ps[a+2]:
                count += 1
                if count == k:
                    print (a,a+2)
                    break
