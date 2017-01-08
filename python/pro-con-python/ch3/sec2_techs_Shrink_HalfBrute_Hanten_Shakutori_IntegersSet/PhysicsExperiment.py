'''
Created on 2016/12/17

@author: kazuyoshi
'''
import math

g=10.0

def height(H,T):
    t = math.sqrt(2*H/g)
    k = int(T/t)
    tau=0.0
    if k%2==0:
        tau = T - k*t
    else:
        tau = (k+1) * t - T
    return H - g * pow(tau,2.0) / 2.0

def solve(N,H,R,T):
    res0=[]
    res=[]
    for i in range(N):
        res0.append(height(H,T-i))
    res0.sort()
    for i in range(len(res0)):
        res.append(res0[i]+2*R*i/100)
    return res
        
if __name__ == '__main__':
    N=1
    H=10
    R=10
    T=100
    y = solve(N,H,R,T)
    print(" ".join(["{:.2f}".format(h) for h in y]))
    
    N=2
    H=10
    R=10
    T=100
    y = solve(N,H,R,T)
    print(" ".join(["{:.2f}".format(h) for h in y]))