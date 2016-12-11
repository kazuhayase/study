'''
Created on 2016/12/11

@author: kazuyoshi
'''

if __name__ == '__main__':
    n=int(input())
    v1=list(map(int,input().split()))
    v2=list(map(int,input().split()))
    
    v1.sort()
    v2.sort(Reversed=True)
    ans=0
    for x1,x2 in zip(v1,v2):
        ans += x1*x2
    print("{}".format(ans))
    