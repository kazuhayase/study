'''
Created on 2016/12/17

@author: kazuyoshi
'''

def solve(n,S,a):
    l=r=s=0
    res=n+1
    while True:
        while r<n and s<S:
            s += a[r]
            r += 1
        if s < S:
            break
        res = min(res,r-l)
        s -= a[l]
        l +=1
    if res>n:
        res=0
    return res

if __name__ == '__main__':
    n=10
    S=15
    a=[5,1,3,5,10,7,4,9,2,8]
    print("{}".format(solve(n,S,a)))
    
    n=5
    S=11
    a=[1,2,3,4,5]
    print("{}".format(solve(n,S,a)))
    