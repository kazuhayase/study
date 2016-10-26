def solve(S):
    res=''
    for i in range(len(S)):
        if res + S[i] < S[i] + res:
            res = S[i] + res
        else:
            res = res + S[i]    
    return res


if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        S = input()
        print("Case #%i: %s" % (caseNr+1, solve(S)))
        
