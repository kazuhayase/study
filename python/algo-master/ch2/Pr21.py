def solve(sc):
    minsc = min(sc)
    maxsc = max(sc)
    print('Min={}, Max={}, Len={}'.format(minsc, maxsc, len(sc)))
    return (sum(sc) - minsc - maxsc) / (len(sc)-2)

if __name__ == '__main__':
    sc = [1,2,3,4,5,6,7]
    print (solve(sc))
    
