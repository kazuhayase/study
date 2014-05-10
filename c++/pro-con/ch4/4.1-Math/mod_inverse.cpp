// extended GCD
// solve ax + by = gcd(a,b) when a and b are input

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

// compute a^-1 (mod m)
// ax + my = gcd(a,m) == 1, then, 
// ax + my = ax = 1 (mod m)

int mod_inverse(int a, int m){
  int x, y;
  extgcd(a,m,x,y);
  return (m + x % m) %m;
}

// when a and m have a common diviser (互いに素でない), 
// the equation "ax = b (mod m)" is identical to 
// (a/gcd(a,m))x = b/gcd(a,m) (mod m/gcd(a,m)) 
//
//    --> b/gcd(a,m) must be an integer to have a solution
//     --> x = (a/gcd(a,m))^(-1) X (b/gcd(a,m)) X k (mod m) (0<=k<gcd(a,m))

