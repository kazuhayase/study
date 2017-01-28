'''
Created on 2017/01/09

@author: kazuyoshi
'''
import math
g=9.8
EPS=1e-10

#locate at t seconds, initial velocity vy
def calc(vy,t):
    return vy*t - g*t**2/2
def cmp(lb,ub,a):
    if a<lb+EPS:
        return -1
    elif a>ub+EPS:
        return 1
    else:
        return 0
#check if hit the pig via (qx,qy)
def check(qx,qy,N,V,X,Y,LBRT):
    #vx^2+vy^2=V^2,vx*t=qx, vy*t-1/2g*t^2=qy
    a=g**2/4
    b=g*qy-V**2
    c=qx**2+qy**2
    D=b**2 - 4*a*c
    if D<0 and D>-EPS:
        D=0
    if D<0:
        return False
    for d in [-1,1]:
        t2 = (-b+d*math.sqrt(D)) / (2*a)
        if t2<=0:
            continue
        t=math.sqrt(t2)
        vx=qx/t
        vy=(qy+g*t**2/2)/t
        yt=calc(vy,X/vx)
        if yt<Y-EPS:
            continue
        ok=True
        for (l,b,r,t) in LBRT:
            if l>=X:
                continue
            if r==X and Y<=t and b<=yt:
                ok=False
            yL=cmp(b,t,calc(vy,l/vx))
            yR=cmp(b,t,calc(vy,r/vx))
            xH=cmp(l,r,vx*(vy/g))
            yH=cmp(b,t,calc(vy,vy/g))
            if xH==0 and yH>=0 and yL<0:
                ok=False
            if yL*yR<=0:
                ok=False
        if ok:
            return True
    return False
def solve(N,V,X,Y,LBRT):
    for i in range(N): # don't care right of pig
        LBRT[i][2]=min(LBRT[i][2],X)
    ok=check(X,Y,N,V,X,Y,LBRT)
    for (l,b,r,t) in LBRT:
        ok |= check(l,t,N,V,X,Y,LBRT)
        ok |= check(r,t,N,V,X,Y,LBRT)
    if ok:
        print('Yes')
    else:
        print('No')
            
if __name__ == '__main__':
    #1
    N=0
    V=7
    (X,Y)=(3,1)
    LBRT=[]
    solve(N,V,X,Y,LBRT)
    
    #2
    N=1
    V=7
    (X,Y)=(3,1)
    LBRT=[[1,1,2,2]]
    solve(N,V,X,Y,LBRT)