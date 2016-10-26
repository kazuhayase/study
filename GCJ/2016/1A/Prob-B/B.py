def solve(N, lines):
    res=list()
    missing = -1
    prev = [0] * N
    diag = [0] * N
    direct = 0 # 0=row, 1=column
    row = [-1] * 2 * N
    for i in range(N):
        min = 2501
        idx1 = -1
        idx2 = -1
        for n,li in enumerate(lines):
            if li[i] <= prev[i] :
                continue
            if min > li[i]:
                min = li[i]
                idx1 = n
                idx2 = -1
            elif min == li[i]:
                idx2 = n
        diag[i] = min
        if i == 0:
            row[i] = idx1
            row[N+i] = idx2
            continue            
        elif idx2 == -1:
            missing = i
        flag=True
        for j in range(i):
            if lines[row[j]][i] != lines[idx1]:
                flag=False
                row[i] = idx1
                prev = lines[idx1]
                if idx2 != -1:
                    row[N+i] = idx2
                break
        if flag == True:
            row[N+i] = idx1
            prev = lines[idx1]
            if idx2 != -1:
                row[i] = idx2
                prev = linex[idx2]
    res = "" 
    if row[missing] == -1:
        for i in range(N):
            #print (" ".join(map(str, lines[row[N+i]][missing])))
            res += " " + str(lines[row[N+i]][missing])
    else :
        for i in range(N):
            #print (" ".join(map(str, lines[row[i]][missing])))
            #print (" ".join(lines[row[i]][missing]))
            res += " " + str(lines[row[i]][missing])
    return res
            
if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        N = int(input())
        lines = list()
        for i in range(2*N-1):
            line = list(map(int, input().split()))
            lines.append(line)
        print("Case #%i: %s" % (caseNr+1, solve(N,lines)))
               
