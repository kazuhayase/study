'''
Created on 2017/01/01

@author: kazuyoshi.hayase
'''

M=10007

def mul(A,B):
    C = [[0 for i in range(len(B[0]))] for j in range(len(A))]
    for i in range(len(A)):
        for k in range(len(B)):
            for j in range(len(B[0])):
                C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % M
    return C

def MatPow(A, n):
    B = [[0 for i in range(len(A))] for j in range(len(A))]
    for i in range(len(A)):
        B[i][i]=1      
    while n>0:
        if n&1:
            B = mul(B,A)
        A = mul(A,A)
        n>>=1
    return B

if __name__ == '__main__':
    A=[[0,1,1,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]]
    k=2
    R=MatPow(A,k)
    res=sum([sum(R[i]) for i in range(len(R[0]))])
    print(res)