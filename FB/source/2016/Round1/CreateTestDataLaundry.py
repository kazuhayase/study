import random
from random import randint

T=50
L=1000000
N=10000
M=1000000000
D=1000000000
W=1000000000

T=1
#L=5
#N=5
#M=5
D=5
#W=5


print(T)
for t in range(1,T+1):
    l = L
    #l = randint(1,L)
    n = N
    #n = randint(1,N)
    m = M
    #m = randint(1,M)
    d = D
    #d = randint(1,D)
    
    print("{} {} {} {}".format(l,n,m,d))

    WL = ' '.join(map(str, (randint(1,W) for i in range(n)) ))
    print (WL)