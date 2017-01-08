'''
Created on 2017/01/01

@author: kazuyoshi.hayase
'''

#MAX_N = 1<<17
#INT_MAX = 1<<63

MAX_N = 16
INT_MAX = 1<<63

n=0
dat=[0 for i in range(2 * MAX_N-1)]

def init(n_):
    global n
    n=1
    while n < n_ :
        n *= 2
    for i in range (2*n-1):
        dat[i]=INT_MAX
    
def update(k, a):
    global n
    #the leaf
    k += n-1
    dat[k]=a
    #update upwards
    while k>0:
        k = int((k-1)/2)
        dat[k] = min(dat[k*2+1], dat[k*2+2])
    
def query(a,b,k,l,r):
    '''
    return minimum in the range[a,b). k,l,r are for internal computation*
        * k is node and the node is for the range [l,r) 
    Therefore, call from outside as,
    "query(a,b,0,0,n)"
    '''
    
    global n
    # [a,b) not intersect with [l,r)
    if r <= a or b <= l:
        return INT_MAX
    # [a,b) includes all [l,r)
    elif a <=l and r <= b:
        return dat[k]
    else:
        vl = query(a,b, k*2+1, l, int((l+r)/2))
        vr = query(a,b, k*2+2, int((l+r)/2), r)
        return min(vl,vr)

if __name__ == '__main__':
    init(4)
    A=[3,2,1,0]
    for i in range(len(A)):
        update(i,A[i])
    for i in range(1,len(A)+1):
        print(query(0,i,0,0,len(A)))
