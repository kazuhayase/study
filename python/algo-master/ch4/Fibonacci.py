def calculateFib(n, fs):
    fs[:2] = [1,1]
    for i in range(2, n+1):
        fs.append(fs[i-1] + fs[i-2])
    return fs

def main():
    fs=[]
    calculateFib(45, fs)
    for i in range(46):
        print(fs[i])
        
if __name__ == '__main__':
    main()
    