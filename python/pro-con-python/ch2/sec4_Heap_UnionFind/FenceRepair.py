'''
Created on 2016/12/03

@author: kazuyoshi
'''

import heapq

if __name__ == '__main__':
    N=int(input())
    L=list(map(int,input().split()))
    ans=0
    que=list()
    for l in L:
        heapq.heappush(que,l)
    while len(que)>1:
        l1 = heapq.heappop(que)
        l2 = heapq.heappop(que)
        ans += l1+l2
        heapq.heappush(que, l1+l2)
    print("{}".format(ans))