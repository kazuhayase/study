def main():
    T = int(input())
    
    for t in range(T):
        N = int(input())
        D = list(map(int, input().split()))
        st=1
        c=0
        i=0
        while i < N:
            if i == N-1:
                if st < 4:
                    c += 1
                break
            if D[i] >= D[i+1]:
                c += 1
                st = 1
                i += 1
                continue
            else:
                diff = D[i+1] - D[i]
                if diff > (4-st) * 10:
                    c += 1
                    st = 1
                    i += 1
                    continue
                else:
                    st += int((diff-1)/10)+1
                    i += 1
                    if st == 4:
                        i += 1
                        c += 1
                        st = 1
                        continue
        res = c * 4 - N
        print("Case #{}: {}".format(t+1, res))        
            
if __name__ == '__main__':
    main()