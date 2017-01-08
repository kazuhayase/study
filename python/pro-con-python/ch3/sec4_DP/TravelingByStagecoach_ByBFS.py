'''
Created on 2016/12/25

@author: kazuyoshi
'''

#node; (T,v)
#edge; d(v,u) / tx
INF=1<<32

def solve(n,m,a,b,t,g):
    q=[]
    memo={}
    S=(1<<n)-1
    q.append((S,a))
    memo[(S,a)]=0
    res=INF
    while len(q)>0:
        v=q.pop()
        cost=memo[v]
        for e in g[v[1]]:
            for i in range(n):
                if (v[0] >> i) & 1:
                    newNode=(v[0] & ~(1<<i), e[0])
                    q.append(newNode)
                    addCost = e[1] / t[i]
                    if newNode in memo.keys():
                        memo[newNode] = min (memo[newNode], cost + addCost)
                    else:
                            memo[newNode] = cost + addCost
                    if e[0]==b:
                        res = min(res, memo[newNode])
    return res
                

if __name__ == '__main__':
    n=2
    m=4
    a=2
    b=1
    t=(3,1)
    g=[[],[(3,3),(4,2)],[(3,3),(4,5)],[(1,3),(2,3)],[(1,2),(2,5)]]
    print(solve(n,m,a,b,t,g))