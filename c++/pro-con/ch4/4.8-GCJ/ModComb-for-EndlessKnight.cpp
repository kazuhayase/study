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


const int MAX_P=10010;

int fact[MAX_P]; // table of n! mod p; O(p)

void pre_compute_mod_fact(int p){
  fact[0]=1;
  for(int i=1; i< p; i++){
    fact[i] = fact[i-1] * i % p;
  }
} 

// n! = a X p^e 
//   compute a mod p; O(log_p n)
int mod_fact(int n, int p, int& e){
  e = 0;
  if (n == 0) return 1;

  // compute for multiples of p (p, 2p, 3p, ...)
  int res = mod_fact(n / p, p, e);
  e += n / p;

  // (p-1)! = -1 (mod p) by Wilson's. => (p-1)!^(n/p) depends on odd/even of n/p

  // needs pre-compute fact[]
  if (n/p % 2 != 0) return res * (p - fact[n % p]) % p;
  return res * fact[n % p] % p;

  // no pre-compute fact []
  //int mod_fact_np =1;
  //for(int i=1; i <= n % p; i++){
  //  mod_fact_np = mod_fact_np * i % p;
  //}
  // if (n/p % 2 != 0) return res * (p - mod_fact_np) % p;
  // return res * mod_fact_np % p;
}



// nCk mod p ; O(log_p n)
// nCk = n! / (k!(n-k)!)
int mod_comb(int n, int k, int p){
  if (n<0 || k<0 || n<k) return 0;
  int e1, e2, e3;
  int a1 = mod_fact(n, p, e1), a2 = mod_fact(k, p, e2), a3 = mod_fact(n-k, p, e3);
  if (e1 > e2+e3) return 0; // nCk is divided by p
  return a1 * mod_inverse(a2 * a3 % p, p) % p;
}
	
