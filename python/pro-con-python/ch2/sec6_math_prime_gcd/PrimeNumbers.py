'''
Created on 2016/12/04

@author: kazuyoshi
'''

def isPrime(n):
    i=2
    while i*i <=n:
        if n%i == 0:
            return False
        i+=1
    return n != 1

def divisor(n):
    res=[]
    i=1
    while i*i <=n:
        if n%i == 0:
            res.append(i)
            if i != int(n/i):
                res.append(int(n/i))
        i+=1
        
    return res

def primeFactor(n):
    res = {}
    i=2
    while i*i <=n:
        cnt=0
        while n % i == 0:
            cnt += 1
            n /= i
        if cnt>0:
            res[int(i)]=int(cnt)
        i += 1
    if n != 1:
        res[int(n)]=1
    return res

if __name__ == '__main__':
    for i in range(1,100):
        print("{}:{},divisor={},prime factor=".format(i,isPrime(i),divisor(i)), end="")
        print("*".join(["^".join(list(map(str,p))) for p in primeFactor(i).items()]))
        

        
        
        
        
    