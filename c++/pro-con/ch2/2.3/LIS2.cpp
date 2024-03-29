#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 1000;
const int INF = 10000;

int n;
int a[MAX_N];

int dp[MAX_N];

void read(){
  scanf("%d\n", &n);
  for(int i=0; i<n; i++){
    scanf("%d", &a[i]);
  }
}

void solve(){
  
  fill(dp, dp +n, INF);
  
  for(int i=0; i<n; i++){
    *lower_bound(dp, dp+n, a[i]) = a[i];
  }
  printf("%ld\n", lower_bound(dp, dp+n, INF) - dp);
}

int main(){
  read();
  solve();
  return 0;
}

