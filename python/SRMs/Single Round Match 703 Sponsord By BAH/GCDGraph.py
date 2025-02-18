# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b, a%b)

def primeFactor(n):
    res = {}
    i=2
    while i*i <=n:
        cnt=0
        while n % i == 0:
            cnt += 1
            n /= i
        if cnt>0:
            res[int(i)]=int(cnt)
        i += 1
    if n != 1:
        res[int(n)]=1
    return res

class GCDGraph:
    def possible(self, n, k, x, y):
        pfx=primeFactor(x)
        pfy=primeFactor(y)
        comFactor = pfx.keys() & pfy.keys()
        comDiv = 1
        for f in comFactor:
            comDiv *= f ** max(pfx[f],pfy[f])
        xDiv=comDiv
        while xDiv <=k:
            for f in sorted(pfx.keys() - comFactor,reverse=True):
                for i in range(pfx[f]):
                    xDiv *= f
                    if xDiv > k:
                        break
                if xDiv > k:
                    break
        if xDiv <=k:
            return "Impossilbe"
        yDiv=comDiv
        while yDiv <=k:
            for f in sorted(pfy.keys() - comFactor,reverse=True):
                for i in range(pfy[f]):
                    yDiv *= f
                    if yDiv > k:
                        break
                if yDiv > k:
                    break
        if yDiv <=k:
            return "Impossilbe"
        if xDiv * yDiv / (gcd(xDiv, yDiv) **2) > n:
            return "Impossible"
        else:
            return "Possible"
            
        
        
        return ""

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

def do_test(n, k, x, y, __expected):
    startTime = time.time()
    instance = GCDGraph()
    exception = None
    try:
        __result = instance.possible(n, k, x, y);
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
    sys.stdout.write("GCDGraph (500 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("GCDGraph.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            n = int(f.readline().rstrip())
            k = int(f.readline().rstrip())
            x = int(f.readline().rstrip())
            y = int(f.readline().rstrip())
            f.readline()
            __answer = f.readline().rstrip()

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(n, k, x, y, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1481681517
    PT, TT = (T / 60.0, 75.0)
    points = 500 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
