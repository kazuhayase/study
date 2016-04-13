import random
from random import randint

T=50
N=100000
DM=100

#T=2
#N=5

print(T)
for t in range(1,T+1):
    n = N # or randint
    n = randint(1,N)
    print("{}".format(n))

    D = ' '.join(map(str, (randint(1,DM) for i in range(n)) ))
    print (D)