# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class CircleGame:
    def cardsLeft(self, deck):
        deck = deck.replace("K","")
        c2n = ["n","A"]
        for i in range(2,10):
            c2n.append(chr(i+ord('0')))
        c2n += ['T', 'J', 'Q', 'K']
        nn=[]
        for ch in deck:
            nn.append(c2n.index(ch))
        while True:
            l = len(nn)
            if l <= 1:
                return l
            rem=[]
            for i in range(l-1):
                if i in rem:
                    continue
                if nn[i] + nn[i+1] == 13:
                  rem.append(i)
                  rem.append(i+1)  
            if 0 in rem or (l-1) in rem:
                pass
            else:
                    if nn[l-1] + nn[0] == 13:
                        rem.append(0)
                        rem.append(l-1)
            if len(rem) == 0:
                return l
            else:
                i=0
                for r in rem:
                    del nn[r-i]
                    i += 1
        
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

def do_test(deck, __expected):
    startTime = time.time()
    instance = CircleGame()
    exception = None
    try:
        __result = instance.cardsLeft(deck);
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
    sys.stdout.write("CircleGame (250 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("CircleGame.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            deck = f.readline().rstrip()
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(deck, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1549094229
    PT, TT = (T / 60.0, 75.0)
    points = 250 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
