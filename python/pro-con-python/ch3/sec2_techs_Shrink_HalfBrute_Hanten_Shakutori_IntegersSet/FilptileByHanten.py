'''
Created on 2016/12/17

@author: kazuyoshi
'''

D=[(-1,0),(1,0),(0,0),(0,-1),(0,1)]

def get(T, f, x, y):
    c = T[y][x]
    for (dx, dy) in D:
        tx = x + dx
        ty = y + dy
        if 0 <= tx < N and 0 <= ty < M:
            c += f[ty][tx]
    return c % 2
    

def solve(M,N,T):
    numFlip=-1
    Flip=[[0 for x in range(N)] for y in range(M)]
    for i in range(1<<N):
        flag=True
        f=[[0 for x in range(N)] for y in range(M)]
        for j in range(N):
            f[0][N-j-1] = i >> j & 1
            for y in range(1,M):
                for x in range(N):
                    if get(T,f,x,y-1) !=0:
                        f[y][x]=1              

            for x in range(N):
                if get(T,f,x,M-1) !=0:
                    flag=False
            if flag:
                tmpNum=0
                for y in range(M):
                    for x in range(N):
                        tmpNum += f[y][x]
                if numFlip < 0 or tmpNum < numFlip:
                    numFlip = tmpNum
                    Flip = f
    return numFlip, Flip

if __name__ == '__main__':
    M=4
    N=4
    T=[[1,0,0,1],[0,1,1,0],[0,1,1,0],[1,0,0,1]]
    (num, F) =  solve(M,N,T)
    #print("num={}".format(num))
    for row in F:
        print(" ".join([ str(item) for item in row]))
