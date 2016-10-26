POS = dict()
NEG = dict()

def pos(st):
    res = 0;
    if st in POS:
        return POS[st]  
    elif st == '+' :        
        res = 0
    elif st == '-':
        res = 1
    elif st[-1] == '+':
        res = min(pos(st[:-1]), neg(st[:-1])+1)
    else :
        res = min(pos(st[:-1])+2, neg(st[:-1])+1)
    POS[st] = res
    return res

def neg(st):
    res = 0;
    if st in NEG:
        return NEG[st]  
    elif st == '+' :        
        res = 1
    elif st == '-':
        res = 0
    elif st[-1] == '+':
        res = min(pos(st[:-1])+1, neg(st[:-1])+2)
    else :
        res = min(pos(st[:-1])+1, neg(st[:-1]))
    NEG[st] = res
    return res

def solve(ST):
    res=0
    res = pos(ST)
    return res


if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        ST = input()
        print("Case #%i: %s" % (caseNr+1, solve(ST)))
