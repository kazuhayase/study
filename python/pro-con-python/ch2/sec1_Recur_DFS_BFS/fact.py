'''
Created on 2016/11/26

@author: kazuyoshi
'''  
memo=dict()

def fact(n):
    if n == 0:
        return 1
    elif n in memo:
        return memo[n]
    else:
        memo[n] = n * fact(n-1)
        return memo[n]

if __name__ == '__main__':
    for i in range(100):
        print("fact({})={}".format(i, fact(i)))
