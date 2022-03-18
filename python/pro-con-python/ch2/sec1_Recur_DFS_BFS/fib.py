'''
Created on 2016/11/26

@author: kazuyoshi
'''  
memo=dict()

def fib(n):
    if n <=1:
        return n
    elif n in memo:
        return memo[n]
    else:
        memo[n] = fib(n-1) + fib(n-2)
        return memo[n]

if __name__ == '__main__':
    for i in range(100):
        print("fib({})={}".format(i, fib(i)))
