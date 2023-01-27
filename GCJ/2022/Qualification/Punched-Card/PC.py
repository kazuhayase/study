def makepd(C):
    return '+-'*C+'+'

def makecd(C):
    return '|.'*C+'|'

def draw1st2(C):
   
    os=".."
    os=os+makepd(C-1)
    print(os)
    os=".."
    os=os+makecd(C-1)
    print(os)
    return        

def drawRest(R,C):
    for i in range(R-1):
        os=""
        os=os+makepd(C)
        print(os)
        os=""
        os=os+makecd(C)
        print(os)

    os=""
    os=os+makepd(C)
    print(os)
    return        


def solve(R,C):
    draw1st2(C)
    drawRest(R,C)
    return


if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        R,C = map(int, input().split())
        print("Case #%i:" % (caseNr+1))
        solve(R,C)