'''
Created on 2017/01/09

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

def solve(n,p,q,m,AB):
    g=[[False for i in range(n)] for j in range(m)]
    for i in range(n):
        g[i][i]=True
        for j in range(i):
            if (p[i] - q[i]).det(p[j]-q[j]) == 0:
                g[i][j] = g[j][i] = onSeg(p[i],q[i],p[j]) or onSeg(p[i],q[i],q[j]) or onSeg(p[j],q[j],p[i]) or onSeg(p[j],q[j],q[i])
            else:
                r = intersection(p[i],q[i],p[j],q[j])
                g[i][j] = g[j][i] = onSeg(p[i],q[i],r) and onSeg(p[j],q[j],r)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                g[i][j] |= g[i][k] and g[k][j]
    for a,b in AB:
        if g[a-1][b-1]:
            print('CONNECTED')
        else:
            print('NOT CONNECTED')                    

def solveByCCW(n,p,q,m,AB):
    g=[[False for i in range(n)] for j in range(m)]
    for i in range(n):
        g[i][i]=True
        for j in range(i):
            g[i][j]=g[j][i] = intersect(p[i],q[i],p[j],q[j])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                g[i][j] |= g[i][k] and g[k][j]
    for a,b in AB:
        if g[a-1][b-1]:
            print('CONNECTED')
        else:
            print('NOT CONNECTED')                    
    

if __name__ == '__main__':
    n=4
    P=[[0,4],[0,1],[1,2],[1,0]]
    Q=[[4,1],[2,3],[3,4],[2,1]]
    m=4
    AB=[[1,2],[1,4],[2,3],[2,4]]
    PP=[]
    QQ=[]
    for p in P:
        PP.append(P2D(p[0],p[1]))
    for q in Q:
        QQ.append(P2D(q[0],q[1]))
    print('[solve]')
    solve(n,PP,QQ,m,AB)
    print('[solve By CCW]')
    solveByCCW(n,PP,QQ,m,AB)