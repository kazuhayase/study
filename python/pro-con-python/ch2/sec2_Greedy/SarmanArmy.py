'''
Created on 2016/11/26

@author: kazuyoshi
'''

if __name__ == '__main__':
    N=int(input())
    R=int(input())
    X=list(map(int,input().split()))
    X.sort()
    i=0
    ans=0
    while i<N:
        s=X[i]
        i += 1
        while i<N and X[i]<=s+R:
            i+=1
        p=X[i-1]
        while i<N and X[i]<=p+R:
            i+=1
        ans +=1
    print("{}".format(ans))
    