'''
Created on 2016/12/04

@author: kazuyoshi
'''
def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b, a%b)

# ax+by=gcd(a,b)
def extgcd(a,b):
    d=a
    if b != 0:
       (d,y,x) = extgcd(b,a%b)
       y -= int(a/b) * x
    else:
        x=1
        y=0
    return (d,x,y) 

if __name__ == '__main__':
    a=4
    b=11
    r=[0,0,0,0]
    (d,x,y) = extgcd(a,b)
    if x<0:
        r[0]=0
        r[2]=-x
    else:
        r[0]=x
        r[2]=0
    if y<0:
        r[1]=0
        r[3]=-y
    else:
        r[1]=y
        r[3]=0
print(r)
print(d)