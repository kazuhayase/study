'''
Created on 2017/04/09

@author: kazuyoshi
'''

def solve(N,M,X,T,O):
    trow=-1
    tcol=-1
    if len(T)>0:
        if len(T)==1:
            trow = T[0][0]
        else:
            if T[0][0] == T[1][0]:
                trow = T[0][0]
            else:
                tcol = T[0][1]
    else:
        trow=1
    xsum=-1
    xdir=0
    if len(X)>0:
        if len(X)==1:
          xsum = X[0][0]  + X[0][1]
          xdir=1
        else:
            if (X[0][0] + X[0][1]) == (X[1][0]+X[1][1]):
                xsum = X[0][0]  + X[0][1]
                xdir = 1
            else:
                xsum = X[0][0]  - X[0][1]
                xdir = -1
        
        


if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        N,M = list(map(int,input().split()))
        T=[[0 for i in range(N+1)] for j in range(N+1)]
        X=[[0 for i in range(N+1)] for j in range(N+1)]
        O=[[0 for i in range(N+1)] for j in range(N+1)]
        M=[[0 for i in range(N+1)] for j in range(N+1)]
        for i in range(M):
            (t,r,c) = input().split()
            r=int(r)
            c=int(c)
            M[c][r]=t
            if t == '+':
                xsum=r+c
                for rr in range(1,xsum+1):
                    cc=xsum-rr
                    T[cc][rr] +=1
                    O[cc][rr] +=1
                xsum=r-c
                for rr in range(1,N+1):
                    cc=rr-xsum
                    if 0<cc<N+2:
                        T[cc][rr] +=1
                        O[cc][rr] +=1
            elif t == 'x':
                for rr in range(1,N+1):
                    X[c][rr] +=1
                    O[c][rr] +=1
                for cc in range(1,N+1):
                    X[cc][r] +=1
                    O[cc][r] +=1

        print("Case #%i: %s" % (caseNr+1, solve(N,M,X,T,O)))