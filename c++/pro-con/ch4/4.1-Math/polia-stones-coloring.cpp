#include<vector>
#include<map>
using namespace std;

const int MOD = 1000000007;
typedef long long ll;

//from chapter 2.6

// power (modulo)

ll mod_pow(ll x, ll n, ll mod){
  ll res=1;
  while (n>0){
    if(n & 1) res = res * x % mod;
    x = x * x % mod;
    n >>=1;
  }
  return res;
}


// enumerate prime numbers; O(n^1/2)

vector<int> divisor (int n){
  vector<int> res;
  for (int i=1; i*i<=n; i++){
    if(n % i == 0) {
      res.push_back(i);
      if (i != n / i) res.push_back(n / i);
    }
  }
  return res;
}

// prime factoring; O(n^1/2)

map<int, int> prime_factor(int n){
  map<int, int> res;
  for (int i=2; i*i<n; i++){
    while (n % i == 0){
      ++res[i];
      n /= i;
    }
  }
  if (n != 1) res[n] = 1;
  return res;
}

// INPUT
int n, m;

void solve(){
  map<int, int> primes = prime_factor(n);
  vector<int> divs = divisor(n);
  ll res = 0;
  for (int i = 0; i < divs.size(); i++){
    // compute Euler function value of divs[i]
    ll euler = divs[i];
    for(map<int, int>::iterator it = primes.begin(); it != primes.end(); ++it){
      int p = it->first;
      if(divs[i] % p == 0) euler = euler / p * (p-1);
    }

    res += euler * mod_pow(m, n / divs[i], MOD) % MOD;
    res %= MOD;
  }

  // divide by n
  printf("%lld\n", res * mod_pow(n, MOD - 2, MOD) % MOD);
}

int main () {
  n = 2, m = 10; solve();
  n = 4, m = 10; solve();
  n = 4, m = 2; solve();
  n = 1000000000, m = 1000000000; solve();
}
