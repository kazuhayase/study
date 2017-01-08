'''
Created on 2016/11/26

@author: kazuyoshi
'''

if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    a.sort(reverse=True)
    ans=0
    for i in range(n-2):
        if a[i] < a[i+1] + a[i+2]:
            ans = max(ans,sum(a[i:i+3]))
    print("{}".format(ans))