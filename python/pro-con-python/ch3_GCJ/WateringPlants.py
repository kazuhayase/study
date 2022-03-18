'''
Created on 2017/03/05

@author: kazuyoshi
'''

import math

def cover(x,y,r,N,XYR):
    S=0
    for i in range(N):
        (xx,yy,rr) = XYR[i]
        if rr <= r:
            dx = x - xx
            dy = y - yy
            dr = r - rr
            if dx**2 + dy**2 <= dr**2:
                S |= 1 << i
    return S

def C(r,N,XYR):
    cand=[]
    cand.append(0)
    for i in range(N):
        (ix,iy,ir) = XYR[i]
        for j in range(i):
            (jx,jy,jr) = XYR[j]
            if ir < r and jr < r:
                idr = r - ir
                jdr = r - jr
                dx = jx - ix
                dy = jy - iy
                a = dx**2 + dy**2
                b = ((idr**2 - jdr**2) / 1 +1) / 2
                d = idr**2/a - b**2
                if d>=0:
                    d=math.sqrt(d)
                    x3=ix+dx*b
                    y3=iy+dy*b
                    x4=-dy*d
                    y4=dx*d
                    ij=1<<i|1<<j
                    cand.append(cover(x3-x4,y3-y4,r,N,XYR)|ij)
                    cand.append(cover(x3+x4,y3+y4,r,N,XYR)|ij)
    for i in range(N):
        (xx,yy,rr) = XYR[i]
        if rr<=r:
            cand.append(cover(xx,yy,r,N,XYR)|1<<i)
    for i in range(len(cand)):
        for j in range(i):
            if (cand[i]|cand[j] == (1<<N)-1):
                return True
    return False

def solve(N,XYR):
    lb=0
    ub=10000
    for i in range(100):
        mid = (lb+ub)/2
        if C(mid,N,XYR):
            ub=mid
        else:
            lb=mid
    print('{:.6f}'.format(ub))

if __name__ == '__main__':
    N=3
    XYR=[[20,10,2],[20,20,2],[40,10,3]]
    solve(N,XYR)
    
    N=3
    XYR=[[20,10,3],[30,10,3],[40,10,3]]
    solve(N,XYR)