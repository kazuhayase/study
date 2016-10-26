def solve(Words):
    Words.reverse()
    return " ".join(Words)


if __name__ == "__main__":
    N = int(input())
     
    for caseNr in range(N):
        Words = list(input().split())
        print("Case #{0}: {1}".format(caseNr+1, solve(Words)))