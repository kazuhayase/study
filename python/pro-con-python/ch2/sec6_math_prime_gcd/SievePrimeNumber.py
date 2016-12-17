prime=[]
isPrime=[]

def	sieve(n):
	p=0
	for i in range(n+1):
		isPrime.append(True)
	isPrime[0]=False
	isPrime[1]=False
	for i in range(2,n+1):
		if isPrime[i]:
			prime.append(i)
			p+=1
			j=i*2
			while j<=n:
				isPrime[j]=False
				j+=i
	return p

if __name__ == '__main__':
	print("{}".format(sieve(1000000)))
