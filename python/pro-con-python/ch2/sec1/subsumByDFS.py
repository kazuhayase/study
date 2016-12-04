'''
Created on 2016/11/26

@author: kazuyoshi
'''
a=list()
n=0
k=0

def dfs(i, s):
    if i == n:
        return s == k
    if dfs(i+1, s):
        return True
    if dfs(i+1, s+a[i]):
        return True
    return False

if __name__ == '__main__':
    n=int(input())
    a=list(map(int,input().split()))
    k=int(input())
    if dfs(0,0):
        print("Yes")
    else:
        print("No")