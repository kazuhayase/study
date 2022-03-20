'''
Created on 2018/04/07

@author: kazuyoshi
'''

def solve(D,P):
    target = 'C'
    index = -1
    CI=[]
    while True:
        index = P.find(target, index + 1)
        if index == -1:
            break
        CI.append(index)
    CI.append(len(P))
    if (len(P) - len(CI)+1) > D:
        return "IMPOSSIBLE"
    pi=-1
    v=1
    d=0
    for ci in CI:
        d += v*(ci-pi-1)
        v *= 2
        pi = ci
       
    cnt=0
    pi=len(P)
    i=len(CI)-2
    while d > D:
        v = 2**i
        r = int((d-D)/v)
        if r > (pi - CI[i]-1) or pi -CI[i]-1 == 0:
            d -= v * (pi - CI[i] -1)
            cnt += pi - CI[i] -1
            i -= 1
            pi -= 1
            if i<0 or pi <0:
                print("ERROR")
                exit
        else:
            if ((d-D) - v*r) > 0:
                cnt += r +1
                d -= v *(r+1)
            else:
                cnt +=  r
                d -= v*r
    return cnt

if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        D,P = input().split()
        D = int(D)
        print("Case #%i: %s" % (caseNr+1, solve(D,P)))