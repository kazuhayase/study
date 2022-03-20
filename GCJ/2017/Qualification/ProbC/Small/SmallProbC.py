'''
Created on 2017/04/08

@author: kazuyoshi
'''

import heapq

def solve(N,K):
    q=[]
    heapq.heappush(q,N*-1)
    ma=mb=0
    for i in range(K):
        a=heapq.heappop(q)
        a *= -1
        ma=(a-1)>>1
        mb=a-1-ma
        heapq.heappush(q,ma*-1)
        heapq.heappush(q,mb*-1)
    return(' '.join(map(str,[max(ma,mb), min(ma,mb)])))

if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        N,K = map(int, input().split())
        print("Case #%i: %s" % (caseNr+1, solve(N,K)))
        