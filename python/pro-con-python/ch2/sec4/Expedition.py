'''
Created on 2016/12/03

@author: kazuyoshi
'''
import heapq

if __name__ == '__main__':
    N,L,P=map(int,input().split())
    A=list(map(int,input().split()))
    B=list(map(int,input().split()))
    A.append(L)
    B.append(0)
    gas=list()
    for (a, b) in zip(A, B):
        heapq.heappush(gas,(a,b))
    tank=P
    ans=0
    pos=0
    que=list()
    for (a,b) in gas:
        d = a - pos
        while tank - d < 0:
            if len(que)==0:
                print("-1")
                exit
            tank += -1 * heapq.heappop(que)
            ans += 1
        tank -= d
        pos = a
        heapq.heappush(que, -1 * b)
    print("{}".format(ans))
        
    