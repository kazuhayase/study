#include <vector>
using namespace std;

// GCD
int gcd(int a, int b) {
  if (b==0) return a;
  return gcd(b, a%b);
}

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

// Coalition linear congruence equation
// 連立線形合同式
// ai X x = bi (mod mi)
//  --> solution would be like x = b (mod m)
//
// x = b1 (mod m1),  a X x = b2 (mod m2) ---> x = b (mod m)
// (solution)
//   x = b1 + m1 X t  
//    -> a X (b1 + m1 X t) = b2 (mod m2)
//     -> a X m1 X t = b2 - a X b1 (mod m2)
//        (if gcd(m2, a X m1) does not divide (b2 - a X b1), no solution)

// return the pair (b, m)

pair<int, int> linear_congruence(const vector<int>& A, const vector<int>& B, 
				 const vector<int>& M) {
  // initialize by "valid for all interger" x = 0 (mod 1)
  int x = 0, m = 1;

  for (int i=0; i < A.size(); i++){
    int a = A[i] * m, b = B[i] - A[i] * x, d = gcd(M[i], a);
    if (b % d !=0) return make_pair(0, -1); // no solution
    int t = b / d * mod_inverse(a / d, M[i] / d) % (M[i] / d);
    x = x + m * t;
    m *= M[i] / d;
  }
  return make_pair(x % m, m);
}

