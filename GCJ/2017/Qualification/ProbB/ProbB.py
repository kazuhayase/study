'''
Created on 2017/04/08

@author: kazuyoshi
'''

def solve(SN):
    ln=list(map(int,list(SN)))
    if len(ln) == 1:
        return SN
    for i in range(len(ln)-1,0,-1):
        if ln[i-1]>ln[i]:
            ln[i-1] -= 1
            for j in range(i,len(ln)):
                ln[j] = 9
    if ln[0]==0:
        ln=ln[1:]
    return ''.join(list(map(str,ln)))

if __name__ == '__main__':
    T = int(input())
     
    for caseNr in range(T):
        SN = input()
        print("Case #%i: %s" % (caseNr+1, solve(SN)))