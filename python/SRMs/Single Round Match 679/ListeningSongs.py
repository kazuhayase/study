# -*- coding: utf-8 -*-
import math, string, itertools, fractions, heapq, collections, re, array, bisect
import sys, time, math


class ListeningSongs:
    def listen(self, durations1, durations2, minutes, T):
        limit = minutes * 60
        durations1 = list(durations1)
        durations2 = list(durations2)
        durations1.sort()
        durations2.sort()
        total = 0
        res=0
        
        if len(durations1) < T or len(durations2) < T:
            return -1
        
        for t in range(T):
            total += durations1[t] + durations2[t]
            res +=2
        
        if total > limit:
            return -1
        
        rest = durations1[T:] + durations2[T:]
        rest.sort()
        
        for r in rest:
            total += r
            if total > limit:
                return res
            else:
                res +=1
                
        return res

# CUT begin
# TEST CODE FOR PYTHON {{{

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

def do_test(durations1, durations2, minutes, T, __expected):
    startTime = time.time()
    instance = ListeningSongs()
    exception = None
    try:
        __result = instance.listen(durations1, durations2, minutes, T);
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
    sys.stdout.write("ListeningSongs (250 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("ListeningSongs.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            durations1 = []
            for i in range(0, int(f.readline())):
                durations1.append(int(f.readline().rstrip()))
            durations1 = tuple(durations1)
            durations2 = []
            for i in range(0, int(f.readline())):
                durations2.append(int(f.readline().rstrip()))
            durations2 = tuple(durations2)
            minutes = int(f.readline().rstrip())
            T = int(f.readline().rstrip())
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(durations1, durations2, minutes, T, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1453291204
    PT, TT = (T / 60.0, 75.0)
    points = 250 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
