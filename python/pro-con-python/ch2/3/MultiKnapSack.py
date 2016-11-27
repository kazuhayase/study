'''
Created on 2016/11/27

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    W=int(input())
    w=list(map(int,input().split()))
    v=list(map(int,input().split()))
    N=100
    V=100
    INF=100000000000
    
    dp=dict()
    nV = N*V+1
    for i in range(nV):
        dp[(0,i)]=INF
    dp[(0,0)]=0
    
    for i in range(n):
        for j in range(N*V+1):
            if j < v[i]:
                dp[(i+1,j)] = dp[(i,j)]
            else:
                dp[(i+1,j)] = min(dp[(i,j)], dp[(i,j-v[i])]+w[i])
    res = 0
    for i in range(N*V+1):
        if dp[(n,i)] <= W:
            res=i
    
    print("{}".format(res))
