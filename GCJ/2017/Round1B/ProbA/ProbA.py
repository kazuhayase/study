'''
Created on 2017/04/23

@author: kazuyoshi
'''

def solve(D,N,K,S):
    t=0
    for i in range(N):
       k=K[i]
       s=S[i]
       tt = (D-k)/s
       if tt > t:
           t=tt
    return D/t
    
if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        D,N = map(int, input().split())
        K=[]
        S=[]
        for i in range(N):
            k,s = map(int, input().split())
            K.append(k)
            S.append(s)
        print("Case #{}: {:.6f}".format(caseNr+1, solve(D,N,K,S)))