'''
Created on 2016/11/27

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    m=int(input())
    s=input()
    t=input()
    dp=dict()
    nm=max(n,m)+1
    for i in range(nm):
        dp[(0,i)]=0
        dp[(i,0)]=0

    for i in range(n):
        for j in range(m):
            if s[i] == t[j]:
                dp[(i+1,j+1)] =dp[(i,j)]+1
            else:
                dp[(i+1,j+1)] =max(dp[(i+1,j)], dp[(i,j+1)])
    print("{}".format(dp[(n,m)]))
    