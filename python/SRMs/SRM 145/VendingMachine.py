# -*- coding: utf-8 -*-
import math,string,itertools,fractions,heapq,collections,re,array,bisect

class VendingMachine:

    def move(self, s,t,c):
        dist = abs(t-s)
        return min(dist, c-dist)
    
    def motorUse(self, prices, purchases):
        M = len(prices)
        shelf =  [ list(map(int, prices[i].split(' '))) for i in range (M) ] 
        N = len(shelf[0])
        column = [ [s[j] for s in shelf] for j in range (N) ]
        co=[]
        heapq.heapify(co)
        for j in range (N):
            heapq.heappush(co,[-sum(column[j]),j,column[j]])
        pat = re.compile('(\d+),(\d+):(\d+)')
        col=0
        tim=0
        Sum=0
        [tmps, tmpcolnum, tmpco] = heapq.heappop(co)
        Sum += self.move(0,tmpcolnum,N)
        col = tmpcolnum
        heapq.heappush(co,[tmps,tmpcolnum,tmpco])
        flag = True
        for pur in purchases:
            ma = pat.match(pur)
            (sh,cc,ti) = map(int, ma.groups())
            if ti - tim > 4:
                [tmps, tmpcolnum, tmpco] = heapq.heappop(co)
                Sum += self.move(col,tmpcolnum,N)
                col = tmpcolnum
                heapq.heappush(co,[tmps,tmpcolnum,tmpco])
            Sum += self.move(col,cc,N)
            col=cc
            tim=ti
            for CO in co:
                [tmps, tmpcolnum, tmpco] = CO
                if tmpcolnum == cc:
                    if tmpco[sh] == 0:
                        flag = False
                    CO[0] += tmpco[sh]
                    tmpco[sh] = 0
            heapq.heapify(co)
        [tmps, tmpcolnum, tmpco] = heapq.heappop(co)
        Sum += self.move(col,tmpcolnum,N)
        if flag:
            return Sum
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

def do_test(prices, purchases, __expected):
    startTime = time.time()
    instance = VendingMachine()
    exception = None
    try:
        __result = instance.motorUse(prices, purchases);
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
    sys.stdout.write("VendingMachine (600 Points)\n\n")

    passed = cases = 0
    case_set = set()
    for arg in sys.argv[1:]:
        case_set.add(int(arg))

    with open("VendingMachine.sample", "r") as f:
        while True:
            label = f.readline()
            if not label.startswith("--"): break

            prices = []
            for i in range(0, int(f.readline())):
                prices.append(f.readline().rstrip())
            prices = tuple(prices)
            purchases = []
            for i in range(0, int(f.readline())):
                purchases.append(f.readline().rstrip())
            purchases = tuple(purchases)
            f.readline()
            __answer = int(f.readline().rstrip())

            cases += 1
            if len(case_set) > 0 and (cases - 1) in case_set: continue
            sys.stdout.write("  Testcase #%d ... " % (cases - 1))
            passed += do_test(prices, purchases, __answer)

    sys.stdout.write("\nPassed : %d / %d cases\n" % (passed, cases))

    T = time.time() - 1474720366
    PT, TT = (T / 60.0, 75.0)
    points = 600 * (0.3 + (0.7 * TT * TT) / (10.0 * PT * PT + TT * TT))
    sys.stdout.write("Time   : %d minutes %d secs\n" % (int(T/60), T%60))
    sys.stdout.write("Score  : %.2f points\n" % points)

if __name__ == '__main__':
    run_tests()

# }}}
# CUT end
