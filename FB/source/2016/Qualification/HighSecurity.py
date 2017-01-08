def main():
    T = int(input())
    
    for t in range(T):
        N = int(input())
        #seg = [[(0,0,False) for j in range(N)] for i in range(2)]
        seg = [[] for i in range(2)]
        pt = [[] for i in range(2)]
        G = ['' for i in range(2)]
        for r in range(2):
            G[r] = input()
            st=0
            l=0
            index=0
            for i in range(N):
                if st == 0: #prev=X
                    if G[r][i] == 'X':
                        continue
                    else:
                        st = 1 #==.
                        l=i
                elif st == 1: #prev=.
                    if G[r][i] == 'X':
                        seg[r].append([l,i-1,False]) #left, right, guarded?
                        if l==i-1:
                            pt[r].append(index)
                        index += 1
                        st = 0
            if st == 1:
                seg[r].append([l, i, False])
                if l == i:
                    pt[r].append(index)
                    
        res=0
        
        for r in range(2):
            j=0
            for p in pt[r]:
                if seg[r][p][2] == True:
                    continue
                for i in range(j, len(seg[1-r])):
                    if seg[1-r][i][0] <= seg[r][p][0] <= seg[1-r][i][1]:
                        seg[1-r][i][2] = True
                        seg[r][p][2] = True
                        j=i+1
                        res += 1
        for r in range(2):
            for se in seg[r]:
                if se[2] == True:
                    continue
                else:
                    #se[2] = True
                    res += 1
                        
        print("Case #{}: {}".format(t+1, res))

if __name__ == '__main__':
    main()