'''
Created on 2016/12/04

@author: kazuyoshi
'''

if __name__ == '__main__':
    INF=1<<30
    V=int(input())
    E=int(input())
    d=[[INF for i in range(V)] for j in range(V)]
    for i in range(V):
        d[i][i]=0
    for i in range(E):
        (f,t,c)=map(int, input().split())
        d[f][t] = c
        d[t][f] = c
    for k in range(V):
        for i in range(V):
            for j in range(V):
                d[i][j] = min(d[i][j], d[i][k]+d[k][j])
    print(d)

            