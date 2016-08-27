def solve(caseNr,B,M):
    res=''
    if M > (2 ** (B-2)) :
        print("Case #{0}: IMPOSSIBLE".format(caseNr+1))
        return
    print("Case #{0}: POSSIBLE".format(caseNr+1))
    fmt = '0'+str(B)+'b'
    row = format(M, fmt)
    print(row)
    Bin = format(M, 'b')
    Len = len(Bin)
    for i in range(B-Len-2):
        row = format(0,fmt)
        print(row)
    if Len > 1:
        for i in range(Len):
            row = '0' * (B-Len+i) + '1' * (Len-i)
            print(row)
    row = format(0,fmt)    
    print(row)
    return

if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        B, M = map(int, input().split())
        solve(caseNr,B,M)