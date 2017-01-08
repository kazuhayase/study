'''
Created on 2016/12/18

@author: kazuyoshi
'''
MAX_N=1<<20
#[1,n] 1-indexed array
bit = [0 for i in range(MAX_N+1)]
n=0

def sum(i): # sum of a1, a2, ..., a_i
    s=0
    while i>0:
        s += bit[i]
        i -= i& -i  ## or i = i&(i-1)
    return s

def add(i, x): # add x to a_i
    while i<=n:
        bit[i] += x
        i += i& -i

def CountBubbleSort(n,a):
    ans=0
    bit = [0 for i in range(MAX_N+1)]
    for j in range(n):
        ans += j - sum(a[j])
        add(a[j],1)
    return ans