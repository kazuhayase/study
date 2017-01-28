'''
Created on 2017/01/09

@author: kazuyoshi
'''
import bisect

def inside(i,j,X,Y,R):
    dx=X[i]-X[j]
    dy=Y[i]-Y[j]
    return dx**2 + dy**2 <= (R[j]-R[i])**2 and R[j] > R[i] 
    #return dx**2 + dy**2 <= R[j]**2
    
def solve(N,XYR):
    X=[]
    Y=[]
    R=[]
    events=[]
    for i,(x,y,r) in enumerate(XYR):
        X.append(x)
        Y.append(y)
        R.append(r)
        events.append((x-r,i))
        events.append((x+r,N+i))
    events.sort()
    outers=[]
    res=[]
    for e in events:
        ID=e[1]%N
        if e[1] < N:
            it=bisect.bisect_left(outers, (Y[ID],ID))
            if len(outers) == 0:
                res.append(ID)
                bisect.insort(outers,(Y[ID],ID))
                continue
            if it != len(outers) and inside(ID,outers[it][1],X,Y,R):
                continue
            if it != 0 and inside(ID,outers[it-1][1],X,Y,R):
                continue
            res.append(ID)
            bisect.insort(outers,(Y[ID],ID))
        else:
            y=(Y[ID],ID)
            i=bisect.bisect_left(outers,y)
            if i!=len(outers) and outers[i] == y:
                outers.remove((Y[ID],ID))
    res.sort()
    print(len(res))
    print(' '.join(map(str,[r+1 for r in res])))

if __name__ == '__main__':
    N=5
    XYR=[[0,-2,1],[0,3,3],[0,0,10],[0,1.5,1],[50,50,10]]
    solve(N,XYR)