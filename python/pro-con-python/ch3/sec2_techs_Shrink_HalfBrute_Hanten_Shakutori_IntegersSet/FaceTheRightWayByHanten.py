'''
Created on 2016/12/17

@author: kazuyoshi
'''

def solve(N,D):
    dir=[]
    for c in D:
        if c =="F":
            dir.append(0)
        else:
            dir.append(1)
    M=N
    K=1
    for k in range(1,N+1):
        m=0
        s=0
        f=[0 for i in range(N)]
        for i in range(N-k+1): #[i,i+k-1]
            if (dir[i] + s) %2 !=0:
                m += 1
                f[i]=1
            s+=f[i]
            if i-k+1 >= 0:
                s -= f[i-k+1]
        for i in range(N-k+1, N):
            if (dir[i] + s) %2 !=0:
                m=-1
            if i-k+1 >= 0:
                s -= f[i-k+1]
        if M>m>=0:
            M=m
            K=k
    return K,M
            
if __name__ == '__main__':
    N=7
    D="BBFBFBB"
    K,M=solve(N,D)
    print("K={}, M={}".format(K,M))
    