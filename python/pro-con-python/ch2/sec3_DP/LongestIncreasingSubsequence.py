'''
Created on 2016/11/27

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    a=list(map(int,input().split()))
    N=1000
    dp=dict()
    
    #Normal
    for i in range(N+1):
        dp[i]=0
    for i in range(n):
        dp[i+1]=1
        for j in range(i):
            if a[j] < a[i]:
                dp[i+1] = max(dp[i+1], dp[j]+1)
    print("{}".format(dp[n]))
    
    #DP to record last element of each length
    INF=10000000
    for i in range(N+1):
        dp[i]=INF
    for j in range(n):
        dp[0] = min(dp[0],a[j])
        for i in range(j):
            if dp[i] < a[j]:
                dp[i+1] = min(dp[i+1],a[j])
    res=-1
    for i in range(n):
        if dp[i]<INF:
            res=i+1
    print("{}".format(res))
    
    #DP searching insertion by lowerbound
    import bisect
    dpa=[] # bisect use len(), dict can't be

    for i in range(N+1):
        dpa.append(INF)
    for i in range(n):
        dpa[bisect.bisect_left(dpa,a[i])]=a[i]
    print("{}".format(bisect.bisect_left(dpa,INF)))
    
    
    #DP same but using array (searching insertion by lowerbound)
    import array
    dpa=array.array('i') # bisect use len(), dict can't be

    for i in range(N+1):
        dpa.append(INF)
    for i in range(n):
        dpa[bisect.bisect_left(dpa,a[i])]=a[i]
    print("{}".format(bisect.bisect_left(dpa,INF)))
    