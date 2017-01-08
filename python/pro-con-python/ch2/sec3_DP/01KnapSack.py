'''
Created on 2016/11/26

@author: kazuyoshi
'''

dp=dict()

def rec(i,j):
    global dp
    if (i,j) in dp:
        return dp[(i,j)]
    res=0
    if i == n:
        res = 0;
    elif j < w[i]:
        res = rec(i+1,j)
    else:
        res = max(rec(i+1,j), rec(i+1,j-w[i])+v[i])
    dp[(i,j)]=res
    return res
        
if __name__ == '__main__':
    n=int(input())
    W=int(input())
    w=list(map(int,input().split()))
    v=list(map(int,input().split()))
    print("{}".format(rec(0,W)))
    