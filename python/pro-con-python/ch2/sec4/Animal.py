'''
Created on 2016/12/03

@author: kazuyoshi
'''
import UnionFindTree  # @UnresolvedImport

if __name__ == '__main__':
    N=int(input())
    K=int(input())
    T=list()
    X=list()
    Y=list()
    for i in range(K):
        t,x,y = map(int,input().split())
        T.append(t)
        X.append(x)
        Y.append(y)
    
    uft=UnionFindTree.UFT(N*3)
    ans=0
    err=[]
    for i in range(K):
        t = T[i]
        x = X[i] - 1
        y = Y[i] - 1
        if x<0 or N<=x or y<0 or N<=y:
            ans+=1
            err.append(i)
            continue
        if t==1:
            if uft.same(x, y+N) or uft.same(x,y+N*2):
                ans+=1
                err.append(i)
            else:
                uft.unite(x,y)
                uft.unite(x+N,y+N)
                uft.unite(x+N*2,y+N*2)
        else:
            if uft.same(x,y) or uft.same(x,y+N*2):
                ans+=1
                err.append(i)
            else:
                uft.unite(x,y+N)
                uft.unite(x+N,y+N*2)
                uft.unite(x+N*2,y)
    print("{}".format(ans))
    print("{}".format(err))
