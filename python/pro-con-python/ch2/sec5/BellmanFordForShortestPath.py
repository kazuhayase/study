'''
Created on 2016/12/03

@author: kazuyoshi
'''
es=[]
d=[]
V=0 
E=0

INF=1<<30

def shortest_path(s):
    global es,d,V,E
    d=[INF for i in range(V)]
    d[s]=0
    while True:
        update=False
        for (f,t,c) in es:
            if d[f] != INF and d[t] > d[f] + c:
                d[t] = d[f] + c
                update=True
        if not update:
            break

if __name__ == '__main__':
    V=int(input())
    E=int(input())
    for i in range(E):
        (f,t,c)=map(int, input().split())
        es.append((f,t,c))
        es.append((t,f,c))
    shortest_path(0)
    print (d)