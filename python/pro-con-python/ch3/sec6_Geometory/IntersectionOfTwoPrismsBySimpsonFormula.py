'''
Created on 2017/01/28

@author: kazuyoshi
'''
INF=1<<32

def width(X,Y,n,x):
    lb=INF
    ub=-INF
    for i in range(n):
        x1=X[i]
        y1=Y[i]
        x2=X[(i+1)%n]
        y2=Y[(i+1)%n]
        if (x1-x)*(x2-x)<=0 and x1 != x2:
            y= y1 + (y2-y1) * (x-x1) / (x2-x1)
            lb = min(lb,y)
            ub = max(ub,y)
    return max(0.0, ub-lb)

def solve(M,N,XY1,XZ2):
    X1=[]
    Y1=[]
    X2=[]
    Z2=[]
    for x,y in XY1:
        X1.append(x)
        Y1.append(y)
    for x,z in XZ2:
        X2.append(x)
        Z2.append(z)
    min1=min(X1)
    max1=max(X1)
    min2=min(X2)
    max2=max(X2)
    xs=X1+X2
    xs=sorted(xs)
    res=0
    for i in range(len(xs)-1):
        a=xs[i]
        b=xs[i+1]
        c=(a+b)/2
        if min1 <= c <= max1 and min2<=c<=max2:
            fa=width(X1,Y1,M,a) * width(X2,Z2,N,a)
            fb=width(X1,Y1,M,b) * width(X2,Z2,N,b)
            fc=width(X1,Y1,M,c) * width(X2,Z2,N,c)
            res += (b-a)/6 * (fa + 4*fc + fb)
    return res

if __name__ == '__main__':
    M=4
    N=3
    XY1=[[7,2],[3,3],[0,2],[3,1]]
    XZ2=[[4,2],[0,1],[8,1]]
    print('{:.10f}'.format(solve(M,N,XY1,XZ2)))
    