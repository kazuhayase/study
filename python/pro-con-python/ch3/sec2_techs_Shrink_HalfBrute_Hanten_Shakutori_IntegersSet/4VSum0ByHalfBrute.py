'''
Created on 2016/12/18

@author: kazuyoshi
'''

import bisect

def count(A,B,C,D):
    cd=[]
    
    for c in C:
        for d in D:
            cd.append(c+d)
    cd.sort()
    
    res = 0
    for a in A:
        for b in B:
            res += bisect.bisect_right(cd, -(a+b)) - bisect.bisect_left(cd, -(a+b))
            
    return res 

if __name__ == '__main__':
    n=6
    A=[-45,-41,-36,-36,26,-32]
    B=[22,-27,53,30,-38,-54]
    C=[42,56,-37,-75,-10,-6]
    D=[-16,30,77,-46,62,45]
    print(count(A,B,C,D))