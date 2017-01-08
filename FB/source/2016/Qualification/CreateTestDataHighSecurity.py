from random import randint
import random
T=200
N=1000
ch = ('X', '.')
print(T)
for t in range(1,T+1):
    n = 1000 # or randint
    print(n)
    for i in range(2):
        row = ''.join(random.choice("X.") for j in range(n))
        print(row)
        
        