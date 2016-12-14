'''
Created on 2016/12/14

@author: kazuyoshi
'''

INF=1<<32

def C(d,N,M,x):
    last=0
    for i in range(1,M):
        crt=last+1
        while crt<N and x[crt] - x[last] <d:
            crt+=1
        if crt==N:
            return False
        last = crt
    return True

def solve(N,M,x):
    x.sort()
    lb=0
    ub=INF
    
    while ub - lb > 1:
        mid = int((ub+lb)/2)
        if C(mid,N,M,x):
            lb=mid
        else:
            ub=mid
    return lb

if __name__ == '__main__':
    N=5
    M=3
    x=[1,2,8,4,9]
    print("{}".format(solve(N,M,x)))