'''
Created on 2017/04/08

@author: kazuyoshi
'''

def flip(pc,i,K):
    for j in range(i,i+K):
        if pc[j]=='-':
            pc[j]='+'
        else:
            pc[j]='-'
    return pc

def solve(S,K):
    pc=list(S)
    res=0
    for i in range(len(pc)-K+1):
        if pc[i] == '-':
            pc=flip(pc,i,K)
            res+=1
    for i in range(len(pc)-K,len(pc)):
        if pc[i] == '-':
            return "IMPOSSIBLE"
    return res
if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        S,K = input().split()
        K = int(K)
        print("Case #%i: %s" % (caseNr+1, solve(S,K)))