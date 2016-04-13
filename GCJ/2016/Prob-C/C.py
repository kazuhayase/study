def solve(N, J):
    res=''
    col = int(N/2) - 2
    
    for i in range(0,J):
        fmt = "0{}b".format(col)
        bi = format(i, fmt)

        #if N == 16:
        #   bi = format(i, '07b')
        #elif N == 32:
        #   bi = format(i, '015b')
        
        res = '1' + bi + '11' + bi + '1'
        
        for bas in range(2,11):
            if bas % 2 == 1:
                proof = 2
            else :
                ba = bas
                proof = 1
                for j in range(col):
                    proof += ba*int(bi[col-j-1])
                    ba *= bas
                proof += ba
            res += ' ' + str(proof)
        print (res)
    
    return


if __name__ == "__main__":
    T = int(input())
     
    for caseNr in range(T):
        N,J = map(int, input().split())
        print("Case #%i:" % (caseNr+1))
        solve(N,J)
