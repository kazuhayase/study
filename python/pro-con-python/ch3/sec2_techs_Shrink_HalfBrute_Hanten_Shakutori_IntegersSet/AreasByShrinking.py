'''
Created on 2016/12/18

@author: kazuyoshi
'''
dx=(-1,1,0,0)
dy=(0,0,-1,1)

def compress(N,x1,x2,w):
    xs=set()
    for i in range(N):
        for d in range(-1,2):
            tx1 = x1[i] + d
            tx2 = x2[i] + d
            if 1<= tx1 <= w:
                xs.add(tx1)
            if 1<= tx2 <= w:
                xs.add(tx2)
    xs=list(xs)
    rx1=[]
    rx2=[]
    for x in x1:
        rx1.append(xs.index(x))
    for x in x2:
        rx2.append(xs.index(x))
    return (len(xs),rx1,rx2)        

def Areas(N,H,W,X1,X2,Y1,Y2):
    W,x1,x2 = compress(N,X1,X2,W)    
    H,y1,y2 = compress(N,Y1,Y2,H)
    fld=[[False for i in range (N*6)] for i in range(N*6)]
    for i in range(N):
        for y in range(y1[i], y2[i]+1):
            for x in range(x1[i], x2[i]+1):
                fld[y][x] = True
    ans=0
    for y in range(H):
        for x in range(W):
            if fld[y][x]:
                continue
            ans +=1
            que=[]
            que.append((x,y))
            while len(que)>0:
                (sx,sy) = que.pop()
                for i in range(4):
                    tx=sx+dx[i]
                    ty=sy+dy[i]
                    if 0<= tx < W and 0<= ty < H:
                        if not fld[ty][tx]:
                            que.append((tx,ty))
                            fld[ty][tx] = True
    return ans
    
if __name__ == '__main__':
    W=10
    H=10
    N=5
    X1=[1,1,4,9,10]
    X2=[6,10,4,9,10]
    Y1=[4,8,1,1,6]
    Y2=[4,8,10,5,10]
    print(Areas(N,H,W,X1,X2,Y1,Y2))