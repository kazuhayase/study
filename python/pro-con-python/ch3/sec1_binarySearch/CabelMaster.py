'''
Created on 2016/12/14

@author: kazuyoshi
'''
INF=1<<32

def C(x,N,L,K):
    num=0
    for i in range(N):
        num += int(L[i]/x)
    return num >= K

def solve(N,L,K):
    lb=0
    ub=INF
    for i in range(100):
        mid = (lb+ub)/2
        if C(mid, N,L,K):
            lb=mid
        else:
            ub=mid
    return ub

if __name__ == '__main__':
    #1
    N=4
    K=11
    L=[8.02, 7.43, 4.57, 5.39]
    print("{:.2f}".format(int(solve(N,L,K) * 100) / 100))