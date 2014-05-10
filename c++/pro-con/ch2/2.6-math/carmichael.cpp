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

ll mod_pow2(ll x, ll n, ll mod){
  if (n==0) return 1;
  ll res = mod_pow2(x* x % mod, n / 2, mod);
  if (n&1) res = res*x % mod;
  return res;
}

bool carmichael(int n){
  for(int x=2; x<n; x++){
    if (mod_pow((long long) x, (long long) n, (long long) n) != x) return false;
  }
  return true;
}
