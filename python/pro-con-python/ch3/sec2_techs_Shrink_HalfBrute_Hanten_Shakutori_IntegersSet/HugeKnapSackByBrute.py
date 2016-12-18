'''
Created on 2016/12/18

@author: kazuyoshi
'''
import bisect
INF=1<<64

def KP(n,w,v,W):
    n2=int(n/2)
    ps=[]
    for i in range(1<<n2):
        sw=sv=0
        for j in range(n2):
            if i >>j & 1:
                sw += w[j]
                sv += v[j]
        ps.append((sw,sv))
    ps.sort()
    m=1
    for i in range(1,1<<n2):
       if ps[m-1][1] < ps[i][1]:
           ps[m]=ps[i] 
           m += 1
    ps=ps[:m]
    res=0
    for i in range(1<<(n-n2)):
        sw=sv=0
        for j in range(n-n2):
            if i>>j&1:
                sw += w[n2+j]
                sv += v[n2+j]
        if sw <= W:
            tv = bisect.bisect_left(ps, (W-sw, INF))-1
            res = max (res, sv + ps[tv][1])
    return res

if __name__ == '__main__':
    n=4
    w=[2,1,3,2]
    v=[3,2,4,2]
    W=5
    print(KP(n,w,v,W))