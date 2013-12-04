// a*x+b*y=1
// a*x + b*y = gcd(x,y)

// b*x' + (a % b) * y' = gcd(a,b)
// a % b = a- (a/b)*b

int extgcd(int a, int b, int& x, int& y)
