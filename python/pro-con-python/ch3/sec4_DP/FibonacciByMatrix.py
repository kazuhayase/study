'''
Created on 2017/01/01

@author: kazuyoshi.hayase
'''

M=10000

def mul(A,B):
    C = [[0 for i in range(len(B[0]))] for j in range(len(A))]
    for i in range(len(A)):
        for k in range(len(B)):
            for j in range(len(B[0])):
                C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % M
    return C

def pow(A, n):
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
    n=10
    A=[[1,1],[1,0]]
    A = pow(A,n)
    print(A[1][0])
    