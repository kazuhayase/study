def solve(K,C,S):
    res = set()
    if K == S:
        for i in range(1,K+1):
            res.add(i)
    if len(res) > S:
        return ("IMPOSSIBLE")
    else :
        return ' '.join(map(str, res))

if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        K,C,S = map(int, input().split())
        print("Case #%i: %s" % (caseNr+1, solve(K,C,S)))