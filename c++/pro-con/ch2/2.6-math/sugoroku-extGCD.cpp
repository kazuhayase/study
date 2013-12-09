// a*x+b*y=1
// (or in general, a*x + b*y = gcd(a,b))

// for gcd
// a = b*p + q  /// q = a%b
// ==> a % gcd(b,q) = 0, b % gcd(b,q) = 0 
// ==> gcd(a,b) % gcd(b,q) = 0

// q = a - b*p
// ==> b % gcd(a,b) = 0, q % gcd(a,b) = 0
// ==> gcd(b,q) % gcd (a,b) = 0

// ---> gcd(a,b) = gcd(b, a%b)

// exgcd
// a*x + b*y = gcd(a,b)

// b*x' + (a % b) * y' = gcd(a,b)
// a % b = a - (a/b)*b
// a*y' + b*(x' - (a/b)*y') = gcd(a,b)
// a*1 + b*0 = a = gcd(a,b) if b=0

int extgcd(int a, int b, int& x, int& y){
  int d = a;
  if (b != 0){
    d = extgcd(b, a%b, y, x);
    y -= (a/b) * x;
  } else {
    x = 1; y=0;
  }
  return d;
}
