'''
Created on 2017/04/23

@author: kazuyoshi
'''

def solve(N,L):
    C=['R','O','Y','G','B','V']
    S=[]
    Q=[]
    lmax=max(L)
    imax=L.index(lmax)
    L[imax] -= 1
    S.append(imax)
    Q.append((S,L))
    while len(Q)>0:
        s,l = Q.pop()
        if len(s) == N:
            id1=s[0]
            id2=s[-1]
            if id1 != id2 and (id1-id2 + 6) % 6 != 1 and (id2-id1+6)%6 !=1:
                res = ''
                for i in range(N):
                    res += C[s[i]]
                return res
            else:
                continue
        id = s[-1]
        ii = [0 for i in range (3)]
        ll = [0 for i in range (3)]
        for i in range(3):
            ii[i] = (id + 2 + i) % 6 
            ll[i] = l[ii[i]]
        lmax = max(ll)
        imax = ii[ll.index(lmax)]
        s.append(imax)
        l[imax]=l[imax]-1
        Q.append((s,l))
    return 'IMPOSSIBLE'
        
        
        
if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        L = list(map(int, input().split()))
        N = L[0]
        L = L[1:]
        print("Case #{}: {}".format(caseNr+1, solve(N,L)))