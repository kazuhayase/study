def solve(N,P):
    res=''
    if sum(P) % 2 == 1:
        idx = P.index(max(P))
        P[idx] -= 1
        res += ' ' + chr(ord('A')+idx)
    while sum(P) > 0:
        idx1 = P.index(max(P))
        P[idx1] -= 1
        idx2 = P.index(max(P))
        P[idx2] -= 1
        res += ' ' + chr(ord('A')+idx1) + chr(ord('A')+idx2)
    return res

if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        N = int(input())
        P = list(map(int, input().split()))
        print("Case #{0}:{1}".format(caseNr+1, solve(N,P)))