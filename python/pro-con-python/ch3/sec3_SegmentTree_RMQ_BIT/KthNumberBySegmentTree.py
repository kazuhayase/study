'''
Created on 2016/12/23

@author: kazuyoshi.hayase
'''
import bisect
from heapq import merge

def init(k,l,r,A,dat):
    if r-l==1:
        dat[k].append(A[l])
    else:
        lch=2*k+1
        rch=2*k+2
        init(lch, l, (l+r)>>1, A ,dat)
        init(rch, (l+r)>>1, r, A, dat)
        dat[k]=list(merge(dat[lch],dat[rch]))

def query(i,j,x,k,l,r,dat,A):
    if j <= l or r <= i:
        return 0
    elif i <= l and r <= j:
        return bisect.bisect_right(dat[k],x)
    else:
        lc = query(i,j,x,k*2+1,l,(l+r)>>1,dat,A)
        rc = query(i,j,x,k*2+2,(l+r)>>1,r,dat,A)
        return lc+rc

def solve(N,M,A,I,J,K):
    nums=[]
    for a in A:
        nums.append(a)
    nums.sort()
    dat=[[] for i in range(len(A)*2+2)]
    init(0,0,N,A,dat)
    for (l,r,k) in zip(I,J,K):
        l -= 1
        #r -= 1
        
        lb = 0
        ub = N
        while ub-lb>1:
            md = (lb+ub)>>1
            c = query(l,r,nums[md],0,0,N,dat,A)
            if c>=k:
                ub=md
            else:
                lb=md
        #print("c={},k={},md={},lb={},ub={}".format(c,k,md,lb,ub))
        print(nums[ub])
        
if __name__ == '__main__':
    N=7
    M=3
    A=[1,5,2,6,3,7,4]
    I=[2,4,1]
    J=[5,4,7]
    K=[3,1,3]
    solve(N,M,A,I,J,K)