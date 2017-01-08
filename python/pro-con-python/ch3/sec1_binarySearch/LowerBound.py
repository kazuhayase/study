'''
Created on 2016/12/11

@author: kazuyoshi
'''
# minimum i s.t. a_i >= k

def solve(n,k,a):
    lb=-1
    ub=n
    while ub - lb > 1:
        mid = int((ub+lb)/2)
        if a[mid] >= k:
            ub = mid
        else:
            lb = mid
    return ub #ub=lb+1

if __name__ == '__main__':
    #1
    n=5
    a=[2,3,3,5,6]
    k=3
    print("n={},a={},k={} => ans={}".format(n,a,k,solve(n,k,a)))
    
    #2
    n=10
    a=[2,2,3,3,5,6,7,8,9,19]
    k=4
    print("n={},a={},k={} => ans={}".format(n,a,k,solve(n,k,a)))
    