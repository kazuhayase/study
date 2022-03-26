'''
Created on 2017/04/08

@author: kazuyoshi
'''

def solve(N,K):
    LI0 = {N:1}
    LI1 = {}
    k0=0
    k1=0
    while True:
        LI1=LI0
        k1=k0
        LI0={}
        for l in sorted(LI1.keys(),reverse=True):
            if l==0:
                continue
            k0 += LI1[l]
            ma = int((l - 1) / 2)
            mb = l - 1 - ma
            if k0 >= K:
                return (" ".join(map(str, [max(ma, mb), min(ma, mb)])))
            if ma in LI0.keys():
                LI0[ma] += LI1[l]
            else:
                LI0[ma] = LI1[l]
            if mb in LI0.keys():
                LI0[mb] += LI1[l]
            else:
                LI0[mb] = LI1[l]

if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        N,K = map(int, input().split())
        print("Case #%i: %s" % (caseNr+1, solve(N,K)))
