def main():
    T = int(input())
    for t in range(T):
        N,P = map(int, input().split())
        B = list(map(int, input().split()))
        l,r,sum,res,st=0,0,0,0,0
        while st>=0:
            if st == 0: #initial, l=r
                if B[r] > P:
                    l += 1
                    r += 1
                    if r == N:
                        break
                else :
                    sum += B[r]
                    if r == N-1:
                        res += 1
                        break
                    st = 1 
            elif st == 1: #extending right
                if sum + B[r+1] > P:
                    res += r-l+1
                    sum -= B[l]
                    l += 1
                    if l == r:
                        sum = 0
                        st = 0
                else :
                    sum += B[r+1]                        
                    r += 1
                    if r == N-1:
                        res += int((N-l+1) * (N-l) / 2)
                        break
        
        print("Case #{}: {}".format(t+1, res))

import sys, os

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc == 2:
        fin = open(argvs[1],'r')
        sys.stdin = fin
        
    main()
    #sys.stdin = sys._stdin_