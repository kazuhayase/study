def solve(N):
    if N == 0:
        return "INSOMNIA"
    see = set()
    n = N
    while len(see) < 10:
        num = str(n)
        n += N
        nl = list(num)
        for c in nl:
            see.add(c)
    return num


if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        N = int(input())
        print("Case #%i: %s" % (caseNr+1, solve(N)))
        
