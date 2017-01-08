'''
Created on 2016/12/17

@author: kazuyoshi
'''

def solve(P,a):
    aSet = set(a)
    n=len(a)
    l=r=0
    cover={}
    for i in aSet:
        cover[i]=0
    numCover=0
    res=n+1
    while True:
        while numCover<len(aSet) and r<n:
            if cover[a[r]] == 0:
                numCover += 1
            cover[a[r]] += 1
            r += 1
        if numCover<len(aSet):
            break
        res = min(res, r-l)
        if cover[a[l]] == 1:
            numCover -=1
        cover[a[l]] -= 1
        l+=1
    return res
        

if __name__ == '__main__':
    P=5
    a=[1,8,8,8,1]
    print("{}".format(solve(P,a)))