'''
Created on 2016/11/26

@author: kazuyoshi
'''

if __name__ == '__main__':
    N=int(input())
    S=list(map(int,input().split()))
    T=list(map(int,input().split()))
    
    ans=0
    ti=0
    for (t,s) in sorted(zip(T,S)):
        if ti < s:
            ans+=1
            ti=t
    print("{}".format(ans))  
        