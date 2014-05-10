const int MAX_P=100;

int fact[MAX_P]; // table of n! mod p; O(p)

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
  //if (n/p % 2 != 0) return res * (p - fact[n % p]) % p;
  //return res * fact[n % p] % p;

  // no pre-compute fact []
  int dummy;
  if (n/p % 2 != 0) return res * (p - mod_fact(n % p, p, dummy)) % p;
  return res * mod_fact(n % p, p, dummy) % p;
}

