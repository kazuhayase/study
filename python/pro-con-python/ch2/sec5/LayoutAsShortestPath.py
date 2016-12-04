'''
Created on 2016/12/04

@author: kazuyoshi
'''
INF=1<<30

if __name__ == '__main__':
    N=int(input())
    ML=int(input())
    MD=int(input())
    like=[[x for x in map(int, input().split())] for i in range(ML)]
    dislike=[[x for x in map(int, input().split())] for i in range(MD)]
    d=[INF for i in range(N)]
    d[0]=0
    
    #BelmanFord
    for k in range(N):
        for i in range(N-1): #d[i]<=d[i+1] := i+1->i, cost=0
            if d[i+1] < INF:
                d[i] = min(d[i], d[i+1])
        for (a,b,c) in like: #d[AL]+DL>=d[BL] := a -> b, cost=dl
            if d[a-1] < INF:
                d[b-1] = min(d[b-1], d[a-1]+c)
        for (a,b,c) in dislike: #d[AD]+DD<=d[BD] := b -> a, cost=-dd
            if d[b-1] < INF:
                d[a-1] = min(d[a-1], d[b-1]-c)
    res = d[N-1]
    if d[0] < 0:
        res=-1
    elif res==INF:
        res=-2
    print("{}".format(res))
    print(d)
            
            