'''
Created on 2016/12/18

@author: kazuyoshi
'''
DSIZE=1<<18 -1

data=[0 for i in range(DSIZE)]
datb=[0 for i in range(DSIZE)]

def add(a,b,x,k,l,r): #add x to all in range [a,b). k is the operating node which represents [l,r)
    if a<=l and r<=b:
        data[k] += x
    elif l<b and a<r:
        datb[k] += (min(b,r) - max(a,l))*x
        add(a,b,x,k*2+1,l,(l+r)>>1)
        add(a,b,x,k*2+2,(l+r)>>1,r)

def sum(a,b,k,l,r): # sum of [a,b). k is the operating node, represents [l,r)
    if b<=l or r<=a:
        return 0
    elif a <= l and r <= b:
        return data[k] * (r-l) + datb[k]
    else:
        res = (min(b,r) - max(a,l)) * data[k]
        res += sum(a,b,k*2+1,l,(l+r)>>1)
        res += sum(a,b,k*2+2,(l+r)>>1,r)
        return res

def solve(A,N,Q,T,L,R,X):
    for i,a in enumerate(A):
        add(i,i+1,a,0,0,N)

    for (t,l,r,x) in zip(T,L,R,X):
        if t == "C":
            add(l,r+1,x,0,0,N)
        else:
            print(sum(l,r+1,0,0,N))

if __name__ == '__main__':
    A=[5,3,7,9,6,4,1,2]
    N=8
    Q=2
    T=["C","Q"]
    L=[0,0]
    R=[4,7]
    X=[1,0]
    solve(A,N,Q,T,L,R,X)
    print (data[:15])
    print (datb[:15])