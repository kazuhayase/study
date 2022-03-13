# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect


class LastDigit:
    
    @classmethod
    def zorome(cls, d, length):
        return int (str(d)*length)
    
    @classmethod
    def findOne(cls, S, length):
        strS = str(S)
        if len(strS) < length:
            return 0, False
        elif len(strS) == length:
            S0 = int(strS[0]) 
            newS = cls.zorome(S0, length)
            if newS > S:
                newS = cls.zorome(S0 - 1, length)
                return S0 - 1, False
            else:
                return S0, False
        else:
            if length < 2:
                return 0, True
            
            newS = cls.zorome(9, length-1)
            #if len(str(S-newS))>length-2:
             #   return 0, True
            #else:
            return 9, False
        
    def findX(self, S):
        strS = str(S)
        res=0
        length = len(strS)
        flg=True
        for i in range (length):
            if len(str(S))<length-i:
                res = res*10
            else:
                nextD, tmpf= self.findOne(S, length-i)
                res = res*10 + nextD
                S = S - self.zorome(nextD,length-i)
                if tmpf:
                    flg=False
        if flg:        
            return res
        else:
            return -1
# CUT begin
# TEST CODE FOR PYTHON {{{
import sys, time, math

def tc_equal(expected, received):
    try:
        _t = type(expected)
        received = _t(received)
        if _t == list or _t == tuple:
            if len(expected) != len(received): return False
            return all(tc_equal(e, r) for (e, r) in zip(expected, received))
        elif _t == float:
            eps = 1e-9
            d = abs(received - expected)
            return not math.isnan(received) and not math.isnan(expected) and d <= eps * max(1.0, abs(expected))
        else:
            return expected == received
    except:
        return False

def pretty_str(x):
    if type(x) == str:
        return '"%s"' % x
    elif type(x) == tuple:
        return '(%s)' % (','.join( (pretty_str(y) for y in x) ) )
    else:
        return str(x)

def do_test(S, __expected):
    startTime = time.time()
    instance = LastDigit()
    exception = None
    try:
        __result = instance.findX(S);
    except:
        import traceback
        exception = traceback.format_exc()
    elapsed = time.time() - startTime   # in sec

    if exception is not None:
        sys.stdout.write("RUNTIME ERROR: \n")
        sys.stdout.write(exception + "\n")
        return 0

    if tc_equal(__expected, __result):
        sys.stdout.write("PASSED! " + ("(%.3f seconds)" % elapsed) + "\n")
        return 1
    else:
        sys.stdout.write("FAILED! " + ("(%.3f seconds)" % elapsed) + "\n")
        sys.stdout.write("           Expected: " + pretty_str(__expected) + "\n")
        sys.stdout.write("           Received: " + pretty_str(__result) + "\n")
        return 0

def run_tests():
    sys.stdout.write("LastDigit (500 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("LastDigit.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            S = int(f.readline().rstrip())
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(S, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1474902504
    PT, TT = (T / 60.0, 75.0)
    points = 500 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
