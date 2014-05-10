#include<map>
#include<vector>
using namespace std;
typedef long long ll;

ll mod_pow(ll x, ll n, ll mod){
  ll res=1;
  while (n>0){
    if(n & 1) res = res * x % mod;
    x = x * x % mod;
    n >>=1;
  }
  return res;
}


// Mebius function
//   (coefficiency for inclusion-exclusion)
//
// Examplel Enumeration of non-recurrence strings

// return the map of mebius function for divisor of n; O(n^1/2)

map<int, int> moebius(int n){
  map<int, int> res;
  vector<int> primes;
  
  // enumerate prime factors of n
  for(int i=2; i * i <= n; i++){
    if(n % i == 0){
      primes.push_back(i);
      while (n % i == 0) n /= i;
    }
  }
  if (n != 1) primes.push_back(n);

  int m = primes.size();
  for (int i=0; i < (1 << m); i++) { // 2^m but less than number of factors of n
    int mu = 1, d = 1;
    for (int j=0; j < m; j++){
      if (i >> j & 1) {
	mu *= -1;
	d *= primes[j];
      }
    }
    res[d] = mu;
  }
  return res;
}

const int MOD = 10009;

// INPUT
int n;

void solve(){
  int res = 0;
  map<int, int> mu = moebius(n);
  for (map<int, int>::iterator it = mu.begin(); it != mu.end(); ++it){
    res += it->second * mod_pow(26, n / it->first, MOD); // mu(d)*26^(n/d)
    res = (res % MOD + MOD) % MOD;
  }
  printf("%d\n", res);
}

int main () {
  n = 2;
  solve();

  n = 4;
  solve();

  n = 15315300;
  solve();
}
