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

def SumOfMatSer(n,k,A):
    B=[[0 for i in range(n*2)] for j in range(n*2)]
    for i in range(n):
        for j in range(n):
            B[i][j] = A[i][j]
        B[n+i][i] = B[n+i][n+i] = 1
    B = MatPow(B, k+1)
    for i in range(n):
        row=[]
        for j in range(n):
            a = B[n+i][j] % M
            if i==j:
                a = (a + M-1) % M
            row.append(str(a))
        print(' '.join(row))

if __name__ == '__main__':
    n=2
    k=2
    M=4
    A=[[0,1],[1,1]]
    SumOfMatSer(n,k,A)
    
    
    
    