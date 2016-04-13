import random
from random import randint

T=50

N=200000
X=1000000000
H=1000000000

T=1
#N=100


print(T)
for t in range(1,T+1):
    #n = N
    n = randint(int(N/3),N)
        
    print("{}".format(n))
    
    for i in range(n):
        print("{} {}".format(randint(1,X),randint(1,H)))
