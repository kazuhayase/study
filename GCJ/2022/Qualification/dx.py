def solve(N, S):
    S.sort()

    i=0
    s=1
    while i<N:
        if S[i]>=s:
            s=s+1
        i=i+1
    return s-1

if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        N = int(input())
        S=list(map(int, input().split()))
        print("Case #%i: %s" % (caseNr+1, solve(N,S)))
               
