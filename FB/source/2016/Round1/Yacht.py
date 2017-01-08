T = int(input())
res=0 

for t in range(T):
    N,A,B = map(int, (input().split()))
    c = list(map(int, input().split()))

    s=[0]
    S=0
    ss=0
    for ci in c:
        S += ci
        s.append(S)
        ss += ci * ci / 2
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
        num += ((a - s[ai]) + c[ai]) / 2 * (s[ai+1] - a)
        for j in range(ai, bi-1):
            num += c[j] * c[j] / 2 
        num += (b - s[bi]) / 2 * (b - s[bi])
    elif ai == bi:
        if a < b:
            num += (b + a - 2 * s[ai]) / 2 * (b - a)
        elif a == b:
            pass
        else:
            num += ss
            num -= (a + b - 2 * s[ai]) / 2 * (a - b)
    elif bi < ai:
        num += ss
        num -= ((b-s[bi]) + c[bi]) / 2 * (s[bi+1] - b)
        for j in range(bi, ai-1):
            num -= c[j] * c[j] / 2
        num -= (a - s[ai]) / 2 * (a - s[ai])

    res = num / enum
        
    print("Case #{}: {:.9f}".format(t+1, res))