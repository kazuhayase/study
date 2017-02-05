'''
Created on 2017/02/05

@author: kazuyoshi
'''
MOD=1000
def mul(A,B):
    C = [[0 for i in range(len(B[0]))] for j in range(len(A))]
    for i in range(len(A)):
        for k in range(len(B)):
            for j in range(len(B[0])):
                C[i][j] = (C[i][j] + A[i][k]*B[k][j]) % MOD
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

def solve(n):
    A=[[3,5],[1,3]]
    A = MatPow(A,n)
    return (A[0][0] * 2 + MOD -1) % MOD
    
if __name__ == '__main__':
    n=2
    print('{:03d}'.format(solve(n)))
    n=5
    print('{:03d}'.format(solve(n)))