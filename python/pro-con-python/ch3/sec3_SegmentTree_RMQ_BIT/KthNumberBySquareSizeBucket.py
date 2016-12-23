'''
Created on 2016/12/19

@author: kazuyoshi.hayase
'''
import bisect
B=1000 #size of bucket

def solve(N,M,A,I,J,K):
    bucket=[[] for i in range(int(N/B)+1)]
    num=[]
    for i,a in enumerate(A):
        bucket[int(i/B)].append(a)
        num.append(a)
    num.sort()
    for bk in bucket:
        bk.sort()
    for (l,r,k) in zip(I,J,K):
        lb=0
        ub=N
        while ub-lb >1:
            md = (ub+lb)>>1
            x = num[md]
            tl=l-1
            tr=r-1
            c=1
            while tl<tr and tl % B !=0:
                if A[tl] <= x:
                    c +=1
                tl +=1
            while tl<tr and tr % B !=0:
                if A[tr] <= x:
                    c += 1
                tr -= 1
            while tl<tr:
                b = int (tl/B)
                c += bisect.bisect_right(bucket[b],x)
                tl += B
            if c >= k:
                ub = md
            else:
                lb = md
        #print("lb={},ub={},md={},c={},k={}".format(lb,ub,md,c,k))
        if k==1:
            print(A[tl])
        else:
            print(num[ub])
    
if __name__ == '__main__':
    N=7
    M=3
    A=[1,5,2,6,3,7,4]
    I=[2,4,1]
    J=[5,4,7]
    K=[3,1,3]
    solve(N,M,A,I,J,K)