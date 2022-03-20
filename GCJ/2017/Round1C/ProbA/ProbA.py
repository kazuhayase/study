'''
Created on 2017/04/30

@author: kazuyoshi
'''
import math

def solve(N,K,PC):
    # DP[j,i] using i-th as base, j+1 pieces in i. == (a, S)
    DP=[[0 for i in range(N)] for j in range(K)]
    for i in range(N):
        DP[0][i] = PC[i][2] + PC[i][3]
    
    for j in range(1,K):
        for i in range(N):
            #aa=0
            for k in range(i):
                DP[j][i] = max(DP[j][i], DP[j][k], DP[j-1][k] + PC[i][3] + PC[i][2] - PC[k][2])
    res=0
    for i in range(N):
        res = max(res, DP[K-1][i])
    return res
    
if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        N,K = list(map(int, input().split()))
        PC=[]
        for i in range(N):
            r,h = list(map(int, input().split()))
            u = r*r
            s = 2*r*h
            PC.append((r,h,u,s))
        PC.sort()
        
        print("Case #{}: {:.9f}".format(caseNr+1, solve(N,K,PC)*math.pi))