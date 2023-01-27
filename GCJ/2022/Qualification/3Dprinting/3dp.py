
def solve(CMYK):
    m=[0 for j in range(4)]
    for j in range(4):
      l=list()
      for i in range(3):
        l.append(CMYK[i][j])
      m[j]=min(l)
    if sum(m)<1000000:
        return " IMPOSSIBLE"
    else:
        rest=1000000
        st=""
        for j in range(4):
            if m[j] >= rest:
                st += " "+ str(rest)
                rest=0
            else:
                st += " "+ str(m[j])
                rest -= m[j]
        return st        



if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        CMYK=[[] for i in range(3)]
        for i in range(3):
            CMYK[i] = list(map(int, input().split()))
        print("Case #%i:%s" % ((caseNr+1), solve(CMYK)))
