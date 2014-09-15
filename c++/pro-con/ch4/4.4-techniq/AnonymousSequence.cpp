#include<cstdio>
#include <algorithm>
using namespace std;
typedef long long ll;

//Using Deque

//INPUT
const int MAX_N = 10000;
int n,k;
ll a[MAX_N];

ll dp[MAX_N + 1]; // DP table
ll S[MAX_N + 1]; // sum of a
int deq[MAX_N];  // deque

// value f_j(x)
ll f(int j, int x) {
  return -a[j] * x + dp[j] - S[j] + a[j] * j;
} 

// decision to delete f2
bool check (int f1, int f2, int f3) {
  ll a1 = -a[f1], b1 = dp[f1] - S[f1] + a[f1] * f1;
  ll a2 = -a[f2], b2 = dp[f2] - S[f2] + a[f2] * f2;
  ll a3 = -a[f3], b3 = dp[f3] - S[f3] + a[f3] * f3;
  return (a2 - a1) * (b3 - b2) >= (b2 - b1) * (a3 - a2);
}

void solve(){
  // sum
  for (int i=0; i < n; i++){
    S[i+1]  = S[i] + a[i];
  }

  // init deq
  int s=0, t=1;
  deq[0]=0;

  dp[0]=0;

  for (int i=k; i <= n; i++){

    if (i-k >= k) {// ???
      // delete "not minumum candidate lines" from tail.
      while (s+1 < t && check(deq[t-2], deq[t-1], i-k)) t--;

      // add i-k to deq
      deq[t++] = i-k;
    }

    // delete the head if it is not minumum
    while (s+1 < t && f(deq[s], i) >= f(deq[s+1], i)) s++;

    dp[i] = S[i] + f(deq[s], i);
  }

  printf("%lld\n", dp[n]);

}

int main(){
  n=7, k=3;
  a[0]=2, a[1]=2, a[2]=3, a[3]=4, a[4]=4, a[5]=5, a[6]=5;
  solve();
}
