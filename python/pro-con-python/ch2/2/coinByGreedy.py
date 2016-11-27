'''
Created on 2016/11/26

@author: kazuyoshi
'''

V=(1,5,10,50,100,500)


if __name__ == '__main__':
    C=list(map(int,input().split()))
    A=int(input())
    ans=0

    for (v,c) in list(zip(V,C))[::-1]:
        t = min(int(A/v),c)
        A -= t*v
        ans += t
    
    print("{}".format(ans))
                