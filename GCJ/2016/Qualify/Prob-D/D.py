def solve(K,C,S):
    res = set()
    if C == 1:
        for i in range(K):
            res.add(i+1)
    else:
        if K <= C:
            offset = 1
            for j in range(K):
                offset += j * K **(C-j-1)
            res.add(offset)
        else :
            #for i in range(max(1,int((K+C-1)/C))):
            offset = 1
            for j in range(C):
                offset += j * K ** (C-j-1)            
            for i in range(int((K-1)/C)+1):
                res.add(offset + i * C * K **(C-1))
    if len(res) > S:
        return ("IMPOSSIBLE")
    else :
        return ' '.join(map(str, res))
    
if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        K,C,S = map(int, input().split())
        print("Case #%i: %s" % (caseNr+1, solve(K,C,S)))
