'''
Created on 2016/12/17

@author: kazuyoshi
'''

n=100
k=10

# f(S) = sigma(2**i)
# {}(empty) : 0
# {i} : 1<<i
# {0,1,...,n-1} : (1<<n) -1
# i in S : if (S>>i &1)
# S + {i} : S | 1 << i 
# S - {i} : S & ~(1<<i)
# S + T : S | T
# S * T : S & T

# all subsets of {0,1,...,n-1}
for S in range(1<<n):
    pass

# all subsets of a subset "sup"
sup=0b0011101010101
sub = sup
while True:
    pass
    sub = (sub-1) & sup
    if sub == sup: # next of "0" is -1&sup==sup
        break

# subsets of size k
comb = (1<<k) - 1
while comb < 1 <<n:
    pass
    x = comb & -comb
    y = comb + x
    comb = ((comb & ~y) / x >>1) | y