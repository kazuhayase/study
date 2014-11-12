const int MAX_P=100;

int fact[MAX_P]; // table of n! mod p; O(p)

void pre_compute_mod_fact(int p){
  fact[0]=1;
  for(int i=1; i< p; i++){
    fact[i] = fact[i-1] * i % p;
  }
} 

// n! = a X p^e 
//   compute a mod p; O(log_p n)
// need to call "pre_compute_mod_fact" in advance

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
}

int mod_fact_wo_pre_compute(int n, int p, int& e){
  e = 0;
  if (n == 0) return 1;

  // compute for multiples of p (p, 2p, 3p, ...)
  int res = mod_fact(n / p, p, e);
  e += n / p;

  // (p-1)! = -1 (mod p) by Wilson's. => (p-1)!^(n/p) depends on odd/even of n/p

  // no pre-compute fact []
  int mod_fact_np =1;
  for(int i=1; i <= n % p; i++){
    mod_fact_np = mod_fact_np * i % p;
  }
  if (n/p % 2 != 0) return res * (p - mod_fact_np) % p;
  return res * mod_fact_np % p;
  
}

