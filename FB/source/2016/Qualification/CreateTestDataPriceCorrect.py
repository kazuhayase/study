import random
from random import randint

T=40
N=100000

T=2
N=5
P=1000000000
B=1000000000

print(T)
for t in range(1,T+1):
    n = N # or randint
    p = randint(1,P)
    print("{} {}".format(n,p))

    b = ' '.join(map(str, (randint(B/10,B) for i in range(n)) ))
    print (b)



    