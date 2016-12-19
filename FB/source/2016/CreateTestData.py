import random
from random import randint

T=50
A=999999999
B=1000000000
N=100000
C=1000000000

#T=1
#N=1


print(T)
for t in range(1,T+1):
    #n = N
    n = randint(int(N/3),N)
    #a = A
    a = randint(1,A)
    #b = B
    b = randint(1,B)
    while b < a:
        b = randint(1,B)
    
    print("{} {} {}".format(n,a,b))

    CL = ' '.join(map(str, (randint(1,C) for i in range(n)) ))
    print (CL)
    