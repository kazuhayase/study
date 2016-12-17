isPrime=[]
isPrimeSmall=[]

#primes in [a,b)
def	segmentSieve(a,b):

	i=0
	while i*i < b:
		isPrimeSmall.append(True)
		i += 1

	for i in range(b-a):
		isPrime.append(True)
		
	i=2
	while i*i < b:
		if isPrimeSmall[i]:
			j=i*2
			while j*j<b:
				isPrimeSmall[j]=False
				j+=i
			for j in range(max(2, int((a+i -1)/i))*i, b, i):
				isPrime[j-a] = False
		i += 1
	res = isPrime.count(True)
	return res

if __name__ == '__main__':
	print("{}".format(segmentSieve(22,37))) #3
	print("{}".format(segmentSieve(22801763489,22801787297))) #1000 --> ? 1014?
	
