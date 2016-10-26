from random import randint
import random
T=100
S=100
print(T)
for t in range(1,T+1):
    n = 100
    for i in range(2):
        row = ''.join(random.choice("-+") for j in range(n))
        print(row)
        