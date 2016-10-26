def solve(C,I,Items):
    sItems = sorted(Items)
    mid = int (C/2)
    for n in sItems:
        if n > mid:
            break
        if C-n in Items:
            if C-n == n:
                res = [Items.index(n)+1, Items.index(n,Items.index(n))+2]
            else:
                res = [Items.index(n)+1, Items.index(C-n)+1]
            return sorted(res)
            

if __name__ == "__main__":
    N = int(input())
     
    for caseNr in range(N):
        C = int(input())
        I = int(input())
        Items = list(map(int, input().split()))
        print("Case #{0}: {1[0]} {1[1]}".format(caseNr+1, solve(C,I,Items)))
