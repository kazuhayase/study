'''
Created on 2016/12/11

@author: kazuyoshi
'''

if __name__ == '__main__':
    N=int(input())
    mtx=[[0 for i in range(N)] for i in range(N)]
    lastOne = [-1 for i in range(N)]
    res=0
    
    for i in range(N):
        line = input()
        for j in range(N):
            mtx[i][j]=line[j]
            if line[j] == '1':
                lastOne[i] = j
    
    for i in range(N):
        pos = -1
        for j in range(i,N):
            if lastOne[j] <= i:
                pos = j
                break
        for j in range (pos,i,-1):
            lastOne[j], lastOne[j-1] = lastOne[j-1], lastOne[j]
            res += 1
    print("{}".format(res))