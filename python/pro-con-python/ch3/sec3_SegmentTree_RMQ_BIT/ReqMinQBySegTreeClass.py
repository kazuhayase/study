'''
Created on 2016/12/18

@author: kazuyoshi
'''

class RMQ(object):
    '''
    RMQ; Request Minimum Query By Segment Tree
    '''
    
    MAX_N = 1<<17
    INT_MAX = 1<<63
    n=0
    dat=[0 for i in range(2 * MAX_N-1)]

    def __init__(self, n_):
        '''
        Constructor; adjust n to be 2**x
        '''
        self.n=1
        while self.n < n_ :
            self.n *= 2
        for i in range (2*self.n-1):
            self.dat[i]=self.INT_MAX
    
    def update(self, k, a):
        '''
        0-indexed k-th value to be a
        '''
        #the leaf
        k += self.n-1
        self.dat[k]=a
        #update upwards
        while k>0:
            k = int((k-1)/2)
            self.dat[k] = min(self.dat[k*2+1], self.dat[k*2+2])
    
    def query(self,a,b,k,l,r):
        '''
        return minimum in the range[a,b). k,l,r are for internal computation*
          * k is node and the node is for the range [l,r) 
        Therefore, call from outside as,
            "query(a,b,0,0,n)"
        '''
        # [a,b) not intersect with [l,r)
        if r <= a or b <= l:
            return self.INT_MAX
        # [a,b) includes all [l,r)
        elif a <=l and r <= b:
            return self.dat[k]
        else:
            vl = self.query(self,a,b, k*2+1, l, int((l+r)/2))
            vr = self.query(self,a,b, k*2+2, int((l+r)/2), r)
            return min(vl,vr)
        