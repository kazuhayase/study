'''
Created on 2016/12/17

@author: kazuyoshi
'''
INF=1<<32

def C(V,W,x,k):
    y=[]
    for v,w in zip(V,W):
        y.append(v - x *w)
    y.sort(reverse=True)
    return sum(y[0:k])>=0

def solve(V,W,k):
    lb=0
    ub=INF
    for i in range(100):
        mid = (lb+ub)/2
        if C(V,W,mid,k):
            lb = mid
        else:
            ub=mid
    return ub

if __name__ == '__main__':
    n=3
    k=2
    W =[2,5,2]
    V =[2,3,1]
    print("{:.2f}".format(solve(V,W,k)))