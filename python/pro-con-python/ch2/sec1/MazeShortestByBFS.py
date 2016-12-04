'''
Created on 2016/11/26

@author: kazuyoshi
'''

INF=10000000

st=()
gl=()
d=dict()
ma=dict()
dx=(1,0,-1,0)
dy=(0,1,0,-1)

def read():
    global st
    global gl
    for y in range(M):
        line=input()
        for x in range(N):
            ma[(x,y)] = line[x]
            if line[x] == 'S':
                st=(x,y)
            if line[x] == 'G':
                gl=(x,y)


def bfs():
    que=list()
    for y in range(M):
        for x in range(N):
            d[(x,y)] = INF
    que.append(st)
    d[st]=0
    while len(que)>0:
        (x,y) = que.pop()
        if (x,y) == gl:
            break
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0<=nx and nx<N and 0<=ny and ny<M and ma[(nx,ny)] != '#' and d[(nx,ny)] == INF:
                que.append((nx,ny))
                d[(nx,ny)] = d[(x,y)] + 1
    return d[gl]
        

if __name__ == '__main__':
    N=int(input())
    M=int(input())
    read()
    res = bfs()
    print("{}".format(res))
