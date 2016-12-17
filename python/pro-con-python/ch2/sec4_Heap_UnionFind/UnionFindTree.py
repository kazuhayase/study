'''
Created on 2016/12/03

@author: kazuyoshi
'''

class UFT(object):
    '''
    classdocs
    '''
    par = list()
    rank = list()

    def __init__(self, n):
        '''
        Constructor
        '''
        self.par = [i for i in range(n)]
        self.rank = [0 for i in range(n)]

    
    def find(self, x):
        if self.par[x] == x:
            return x
        else:
            self.par[x] = self.find(self.par[x])
            return self.par[x]
    
    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        elif self.rank[x] < self.rank[y]:
            self.par[x] = y
        else:
            self.par[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1
        return
    
    def same(self, x, y):
        return self.find(x) == self.find(y)
    