op = ('+', '-', '*', '/')
EPS = 1.0e-15
def check (expr):
    try:
        if 10 - EPS < eval(expr) < 10 + EPS:
            return True
        else:
            return False
    except ZeroDivisionError:
            return False

def solve(a,b,c,d):
    x = (a,b,c,d)
    for op1 in op:
        for op2 in op:
            for op3 in op:
                for i1 in range(4):
                    for i2 in range(4):
                        for i3 in range(4):
                            for i4 in range(4):
                                if not (i1 == i2 or i1 == i3 or i1 == i4 or i2 == i3 or i2 == i4 or i3 == i4):
                                    expr1 = '((( {} {} {}) {} {}) {} {})'.format(x[i1],op1,x[i2],op2,x[i3],op3,x[i4])
                                    expr2 = '(( {} {} {}) {} ({} {} {}))'.format(x[i1],op1,x[i2],op2,x[i3],op3,x[i4])
                                    expr3 = '({} {} ({} {} ({} {} {})))'.format(x[i1],op1,x[i2],op2,x[i3],op3,x[i4])
                                    if check(expr1):
                                        return expr1
                                    elif check(expr2):
                                        return expr2
                                    elif check(expr3):
                                        return expr3
                                    
    return "NG"

def main():
    a,b,c,d = map(int,input().split())
    print (solve(a,b,c,d))
    
if __name__ == '__main__':
    main()
    