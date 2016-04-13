from decimal import *
T = int(input())
res=0 

for t in range(T):
    N,A,B = map(Decimal, (input().split()))
    N = int(N)
    c = list(map(Decimal, input().split()))

    s=[Decimal(0)]
    S=Decimal(0)
    ss=Decimal(0)
    for ci in c:
        S += ci
        s.append(S)
        ss += ci * ci / Decimal(2.0)
    a = A % S
    b = B % S
    ai=0
    bi=0
    
    for i in range(N):
        if s[i] <= a < s[i+1]:
            ai = i
        if s[i] <= b < s[i+1]:
            bi = i
            
    enum = B - A
    
    d = int ((B-A) / S)
    num = d * ss
    
    if ai < bi:
        num += ((a - s[ai]) + c[ai]) / Decimal(2.0) * (s[ai+1] - a)
        for j in range(ai, bi-1):
            num += c[j] * c[j] / Decimal(2.0) 
        num += (b - s[bi]) / Decimal(2.0) * (b - s[bi])
    elif ai == bi:
        if a < b:
            num += (b + a - Decimal(2.0) * s[ai]) / Decimal(2.0) * (b - a)
        elif a == b:
            pass
        else:
            num += ss
            num -= (a + b - Decimal(2.0) * s[ai]) / Decimal(2.0) * (a - b)
    elif bi < ai:
        num += ss
        num -= ((b-s[bi]) + c[bi]) / Decimal(2.0) * (s[bi+1] - b)
        for j in range(bi, ai-1):
            num -= c[j] * c[j] / Decimal(2.0)
        num -= (a - s[ai]) / Decimal(2.0) * (a - s[ai])

    res = num / enum
        
    print("Case #{}: {:.9f}".format(t+1, res))