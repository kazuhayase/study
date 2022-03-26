'''
Created on 2018/04/07

@author: kazuyoshi
'''

def solve(N,V):
    V0=[]
    V1=[]
    for i in range(len(V)):
        if i % 2 == 0:
            V0.append(V[i])
        else:
            V1.append(V[i])
    V0.sort()
    V1.sort()
    VV=[]
    for i in range(len(V1)):
        VV.append(V0[i])
        VV.append(V1[i])
    if len(V) % 2 == 1:
        VV.append(V0[i+1])
    for i in range(len(VV)-1):
        if VV[i] > VV[i+1]:
            return i
    return 'OK'

if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        N = int(input())
        V = list(map(int, input().split()))
        print("Case #%i: %s" % (caseNr+1, solve(N,V)))