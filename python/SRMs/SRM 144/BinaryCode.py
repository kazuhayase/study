# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class BinaryCode:
    def decode(self, message):
        M = list(message)
        length = len(M)
        if length < 2:
            return("NONE", "NONE")
        
        Q=[]
        for m in M:
            Q.append(int(m))
        
        P = [[0 for i in range(length)] for j in range(2)]
        result = ["" for i in range(2)]
        flag = [True for i in range(2)]
        P[0][0] = 0
        P[1][0] = 1
        for i in (0,1):
            P[i][1] = Q[0] - P[i][0]

        index = 2

        for q in Q[1:-1]:
            for i in (0,1):
                P[i][index] = q - P[i][index - 1] - P[i][index - 2]
                if not 0 <= P[i][index] <= 1:
                    flag[i] = False
            index += 1
        else:
            q = Q[-1]
            for i in (0,1):
                if q != P[i][-1] + P[i][-2]:
                    flag[i] = False

        for i in (0,1):
            if flag[i]:
                for j in P[i]:
                    result[i] += str(j)
            else:
                result[i] = "NONE"

        return (result)

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

def do_test(message, __expected):
    startTime = time.time()
    instance = BinaryCode()
    exception = None
    try:
        __result = instance.decode(message);
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
    sys.stdout.write("BinaryCode (300 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("BinaryCode.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            message = f.readline().rstrip()
            f.readline()
            __answer = []
            for i in range(0, int(f.readline())):
                __answer.append(f.readline().rstrip())
            __answer = tuple(__answer)

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(message, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1451724272
    PT, TT = (T / 60.0, 75.0)
    points = 300 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
