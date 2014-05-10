// Fermat small theorem
// for a prime p 
//   x^p = x (mod p) 
//   x^{p-1} = 1 (mod p)
//    ---> a^-1 = a^{p-2} (mod p) 

// Euler theorem for m = p1^e1 X p2^e2 X ... X pn^en
//
// Euler function is equal to the number of natural numbers coprime to m
//  phi(m) = m X (p1 - 1)/p1 X (p2 - 1)/p2 X ... X (pn -1)/pn
//    if m is a prime, phi(m) = m-1 ==> Fermat small theorem

// Compute Euler function phi
int euler_phi (int n) {
  int res = n;
  for(int i = 2; i * i <= n; i++){
    if(n % i == 0){
      res = res / i * (i-1);
      for(; n % i == 0; n/=i);
    }
  }
  if (n != 1) res = res / n * (n-1); // n is a prime 
  return res;
}

// Build table of Euler function

const int MAX_N = 10000;
int euler[MAX_N];
void euler_phi2(){
  for (int i=0; i < MAX_N; i++) euler[i] = i;
  for (int i=2; i < MAX_N; i++) {
    if(euler[i] == i) {
      for (int j = i; j < MAX_N; j += i) euler[j] = euler[j] / i * (i-1);
    }
  }
}

  
