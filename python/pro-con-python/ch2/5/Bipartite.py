'''
Created on 2016/12/03

@author: kazuyoshi
'''
V=0
color=[]
G=[]

def dfs(v,c):
    global V,G,color
    color[v]=c
    for w in G[v]:
        if color[w] == c:
            return False
        if color[w] == 0 and not(dfs(w,-c)):
            return False
    return True
            
if __name__ == '__main__':

    V=int(input())
    G=[list() for i in range(V)]
    color=[0 for i in range(V)]
    while True:
        s,t = map(int, input().split())
        if (s,t) == (-1,-1):
            break
        else:
            G[s].append(t)
            G[t].append(s)
    ans = True
    for i in range(V):
        if color[i] == 0:
            if not dfs(i,1):
                ans = False
    if ans:
        print("Yes")
    else:
        print("No")
        