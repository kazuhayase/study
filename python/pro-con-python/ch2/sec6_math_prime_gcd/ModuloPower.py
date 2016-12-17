'''
Created on 2016/12/11

@author: kazuyoshi
'''
def modPow(x,n,mod):
    res=1
    while n>0:
        if n&1:
            res = res * x % mod
        x = x*x % mod
        n >>=1
    return res

def modPow2(x,n,mod):
    if n==0:
        return 1
    res = modPow2(x*x % mod, int (n/2), mod)
    if n & 1:
        res = res * x % mod
    return res

if __name__ == '__main__':
    print("2^4 mod 4 ={}".format(modPow(2,4,4)))
    print("2^4 mod 4 ={}".format(modPow2(2,4,4)))