'''
Created on 2016/12/18

@author: kazuyoshi
'''

#from ReqMinQBySegTree import RMQ  # @UnresolvedImport
import math

ST_SIZE=1<<15 -1
MAX_N=100

vx=[0.0 for i in range(ST_SIZE)]
vy=[0.0 for i in range(ST_SIZE)]
ang=[0.0 for i in range(ST_SIZE)]
prv=[0.0 for i in range(MAX_N)]

def init(k,l,r,N,L):
    ang[k]=vx[k]=0.0
    if r-l == 1: # leaf
        vy[k]=L[l]
    else:
        chl=k*2+1
        chr=k*2+2
        init(chl, l, (l+r)>>1, N,L)
        init(chr, (l+r)>>1, r, N,L)
        vy[k] = vy[chl]+vy[chr]

def change(s,a, v,l,r):
    if s<=l:
        return
    elif s<r:
        chl=v*2+1
        chr=v*2+2
        m = (l+r)>>1
        change(s,a,chl,l,m)
        change(s,a,chr,m,r)
        if s<=m:
            ang[v] +=a
        s = math.sin(ang[v])
        c = math.cos(ang[v])
        vx[v]=vx[chl]+(c*vx[chr]-s*vy[chr])
        vy[v]=vy[chl]+(s*vx[chr]+c*vy[chr])

def solve(N,C,L,S,A):
    init(0,0,N,N,L)
    for i in range(1,N):
        prv[i]=math.pi
    for i in range(C):
        s = S[i]
        a = A[i] / 360.0 * 2 * math.pi
        change(s,a-prv[s], 0,0,N)
        prv[s] = a
    return (vx[0],vy[0])

if __name__ == '__main__':
    N=2
    C=1
    L=[10,5]
    S=[1]
    A=[90]
    
    resX, resY = solve(N,C,L,S,A)
    print("{:.2f} {:.2f}".format(resX, resY))
    
    N=3
    C=2
    L=[5,5,5]
    S=[1,2]
    A=[270,90]
    
    resX, resY = solve(N,C,L,S,A)
    print("{:.2f} {:.2f}".format(resX, resY))
    