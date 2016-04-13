class Goldbach:
    def sieve(n):
        ps = [True for i in range(n+1)]
        ps[0] = False
        ps[1] = False
        for i in range(2,n):
            if not ps[i]:
                continue
            for k in range(2,int(n/i)):
                ps[k * i] = False
        return ps

    if __name__ == '__main__':
        ps = sieve(1000000)
        while True:
            n = int(input())
            if n == 0:
                break
            for a in range(2,n):
                b = n - a
                if ps[a] and ps[b]:
                    print ('{} {}'.format(a, b))
                    break
                    
