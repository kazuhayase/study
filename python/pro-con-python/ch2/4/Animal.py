'''
Created on 2016/12/03

@author: kazuyoshi
'''
import UnionFindTree

if __name__ == '__main__':
    N=int(input())
    K=int(input())
    T=list()
    X=list()
    Y=list()
    for i in range(N):
        t,x,y = map(int,input().split())
        T.append(t)
        X.append(x)
        Y.append(y)
    
    