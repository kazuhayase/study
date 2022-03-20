# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class ChristmasPudding:
    def eat(self, N, Vall, Vsweet, Vprefix, Tprefix, Sprefix, seed):
        V, T, S = Vprefix, Tprefix, Sprefix
        state = seed
        while length(V) < N:
            state = (state * 1103515245 + 12345) % 2^31
            V.append( 1 + (state % 10^6) )
            state = (state * 1103515245 + 12345) % 2^31
            T.append( 1 + (state % 10^6) )
            state = (state * 1103515245 + 12345) % 2^31
            S.append( (state / 1024) % 2 )
        return 0

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

def do_test(N, Vall, Vsweet, Vprefix, Tprefix, Sprefix, seed, __expected):
    startTime = time.time()
    instance = ChristmasPudding()
    exception = None
    try:
        __result = instance.eat(N, Vall, Vsweet, Vprefix, Tprefix, Sprefix, seed);
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
    sys.stdout.write("ChristmasPudding (500 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("ChristmasPudding.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            N = int(f.readline().rstrip())
            Vall = int(f.readline().rstrip())
            Vsweet = int(f.readline().rstrip())
            Vprefix = []
            for i in range(0, int(f.readline())):
                Vprefix.append(int(f.readline().rstrip()))
            Vprefix = tuple(Vprefix)
            Tprefix = []
            for i in range(0, int(f.readline())):
                Tprefix.append(int(f.readline().rstrip()))
            Tprefix = tuple(Tprefix)
            Sprefix = []
            for i in range(0, int(f.readline())):
                Sprefix.append(int(f.readline().rstrip()))
            Sprefix = tuple(Sprefix)
            seed = int(f.readline().rstrip())
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(N, Vall, Vsweet, Vprefix, Tprefix, Sprefix, seed, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1576950785
    PT, TT = (T / 60.0, 75.0)
    points = 500 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
