'''
Created on 2016/12/11

@author: kazuyoshi
'''
def isPrime(n):
    i=2
    while i*i <=n:
        if n%i == 0:
            return False
        i+=1
    return n != 1

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

def isCarmichaelNumber(n):
    if isPrime(n):
        return False
    for x in range(2,n):
        if modPow(x,n,n) != x:
            return False
    return True

if __name__ == '__main__':
    case = [17, 561, 4]
    for n in case:
        print("Is {} a Carmichael Number?: {}".format(n, isCarmichaelNumber(n)))