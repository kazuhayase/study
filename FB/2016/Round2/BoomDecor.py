def main():
    T = int(input())
    
    for t in range(T):
        res = 0
        N = int(input())
        A = input()
        B = input()
        a = list(A)
        b = list(B)
        
        c=b[0]
        beg=0
        seg=list()
        for i in range(N):
            if c == b[i]:
                if i == N-1:
                    seg.append((beg,i+1,c,True))
                continue
            else:
                flag=True
                for j in range(beg, i):
                    if a[j] == b[j]:
                        continue
                    else :
                        flag=False
                seg.append((beg,i,c,flag))
                c=b[i]
                beg = i
                if i == N-1:
                    seg.append((N-1,N,c,a[N-1]==b[N-1]))

        even = True
        if len(seg) % 2 != 0:

            mid = int(len(seg)/2)
            if not seg[mid][3]:
                res = mid + 1
                even = False
            else:
                left = mid-1
                right = mid+1
        else:
            left = int(len(seg)/2) -1
            right = int(len(seg)/2)
        
        while even:
            if left ==-1:
                res=0
                break
            if seg[left][3] and seg[right][3]:
                left -= 1
                right += 1
                if left ==-1:
                    res = 0
                    break
            else:
                res = left + 1
                break
                
        print("Case #{}: {}".format(t+1, res))
            
if __name__ == '__main__':
    main()
    