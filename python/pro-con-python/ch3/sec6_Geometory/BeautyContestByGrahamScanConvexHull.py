'''
Created on 2017/01/14

@author: kazuyoshi
'''
EPS=1e-10

def add(a,b):
    if abs(a+b) < EPS * (abs(a)+abs(b)):
        return 0
    return a+b
class P2D:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self, p):
        return P2D(add(self.x, p.x), add(self.y, p.y))
    def __sub__(self, p):
        return P2D(add(self.x, -p.x), add(self.y, -p.y))
    def __mul__(self, d):
        return P2D(self.x * d, self.y * d)
    def dot(self, p):
        return add(self.x * p.x, self.y * p.y)
    def det(self, p):
        return add(self.x * p.y, -self.y * p.x)    
def onSeg(p1,p2,q):
    return (p1-q).det(p2-q) == 0 and (p1-q).dot(p2-q)<=0
def intersection(p1,p2,q1,q2):
    return p1 + (p2-p1) * ((q2-q1).det(q1-p1) / (q2-q1).det(p2-p1))
def ccw(a,b,c):
    #ret1= (b.x - a.x) * (c.y - a.y) > (b.y - a.y) * (c.x - a.x)
    ret2=(b-a).det(c-a)>0
    #if ret1 != ret2:
    #    print("Error")
    #return ret1, ret2
    return ret2
def intersect(a1,b1,a2,b2):
    return ccw(a1,b1,a2) != ccw(a1,b1,b2) and ccw(a2,b2,a1) != ccw(a2,b2,b1)

def convexHull(ps, n):
    ps.sort(key=lambda p:(p.x, p.y))
    k=0   #nodes of convex
    qs=[0 for i in range(n)] #convex
    #lower
    for i in range(n):
        while k>1 and (qs[k-1]-qs[k-2]).det(ps[i]-qs[k-1]) <= 0:
            k -= 1
        qs[k] = ps[i]
        k += 1
    #upper
    t=k
    for i in range(n-2,-1,-1):
        while k>t and (qs[k-1]-qs[k-2]).det(ps[i]-qs[k-1]) <= 0:
            k -= 1
        qs[k] = ps[i]
        k += 1
    qs=qs[:k]
    return qs

def dist(p,q):
    return (p-q).dot(p-q)

def solve(N,ps):
    qs=convexHull(ps,N)
    res=0
    rs=[]
    for q in qs:
        rs.append(q)
        for r in rs:
            res=max(res,dist(q,r))
    print('{:.0f}'.format(res))

if __name__ == '__main__':
    N=8
    XY=[[0,5],[1,8],[3,4],[5,0],[6,2],[6,6],[8,3],[8,7]]
    ps=[]
    for x,y in XY:
        ps.append(P2D(x,y))
    solve(N,ps)
    