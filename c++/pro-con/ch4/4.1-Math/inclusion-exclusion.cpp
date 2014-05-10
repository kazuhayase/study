#import<cstdio>

// 包除原理
// number of integers between 1 & n divisible by some a1, a2, ..., am

int gcd(int a, int b) {
  if (b==0) return a;
  return gcd(b, a%b);
}

typedef long long ll;

const int MAX_M = 15;

int a [MAX_M];
int n, m;

void solve(){
  ll res = 0;
  for (int i = 1; i < (1<<m); i++){
    int num = 0;
    for (int j=i; j !=0; j >>=1) num += j & 1; //number of 1 bits of i
    ll lcm = 1;
    for (int j=0; j < m; j++) {
      if (i >> j & 1){
	lcm = lcm / gcd(lcm, a[j]) * a[j];
	// if lcm > n, then n/lcm = 0 == overflow
	if(lcm > n) break;
      }
    }
    if (num % 2 == 0) res -= n / lcm;
    else res += n / lcm;
  }
  printf("%lld\n", res);
}
 
int main(){
  n = 100, m = 2;
  a[0] = 2, a[1] = 3;
  solve();

  n = 100, m = 3;
  a[0] = 2, a[1] = 3, a[2] = 7;
  solve();
}
  
