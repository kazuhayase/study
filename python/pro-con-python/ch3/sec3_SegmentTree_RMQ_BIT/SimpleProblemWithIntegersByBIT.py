'''
Created on 2016/12/18

@author: kazuyoshi
'''
MAX_N=100

#BIT
bit0=[0 for i in range(MAX_N+1)]
bit1=[0 for i in range(MAX_N+1)]
N=0

def sum(bit, i): # sum of a1, a2, ..., a_i
    s=0
    while i>0:
        s += bit[i]
        i -= i& -i  ## or i = i&(i-1)
    return s

def add(bit, i, x,N): # add x to a_i
    while i<=N:
        bit[i] += x
        i += i& -i

def solve(A,N,Q,T,L,R,X):
    for i,a in enumerate(A[1:]):
        add(bit0,i+1,a,N)
        
    for (t,l,r,x) in zip(T,L,R,X):
        if t == "C":
            add(bit0, l, -x*(l-1),N)
            add(bit1, l, x,N)
            add(bit0, r+1, x*r,N)
            add(bit1, r+1, -x,N)
        else:
            res =sum(bit0,r) + sum(bit1, r)*r
            res-=sum(bit0,l-1) + sum(bit1, l-1) * (l-1)
            print(res)

if __name__ == '__main__':
    A=[0,5,3,7,9,6,4,1,2]
    N=8
    Q=2
    T=["C","Q"]
    L=[1,1]
    R=[5,8]
    X=[1,0]
    solve(A,N,Q,T,L,R,X)
