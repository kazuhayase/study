'''
Created on 2017/01/01

@author: kazuyoshi.hayase
'''

def rec(i,j,used,color):
    if j==m:
        return rec(i+1,0,used,color)
    if i==n:
        return 1
    if used[i][j] or color[i][j]:
        return rec(i, j+1, used,color)
    
    res=0
    used[i][j]=True
    
    if j+1 < m and (not used[i][j+1]) and (not color[i][j+1]):
        used[i][j+1] = True
        res += rec(i,j+2,used,color)
        used[i][j+1] = False
    
    if i+1 < n and (not used[i+1][j]) and (not color[i+1][j]):
        used[i+1][j] = True
        res += rec(i,j+1,used,color)
        used[i+1][j] = False
    
    used[i][j] = False
    return res % M

def solve(n,m,color):
    used = [[False for i in range(m)] for j in range(n)]
    print(rec(0,0,used,color))

if __name__ == '__main__':
    M=1<<32
    n=3
    m=3
    color=[[False,False,False],[False,True,False],[False,False,False]]
    solve(n,m,color)
    