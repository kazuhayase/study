#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 1000;
const int MAX_m = 1000;
const int MAX_A = 1000;
const int MAX_M = 10000;

int n,m,M;
int a[MAX_N];
int dp[MAX_N + 1][MAX_m + 1];

void read(){
  scanf("%d\n%d", &n, &m);
  for(int i=0; i<n; i++)
      scanf("%d", &a[i]);
  scanf("%d\n", &M);
}

void solve(){

  // l=k-1

  // dp[i+1][j]=sigma(min(j,a[i]), k=0, dp[i][j-k])
  // sigma(min(j,a[i]), k=0, dp[i][j-k]) = sigma(min(j, a[i]), k=1, dp[i][j-k]) + dp[i][j]
  // = sigma(min(j-1, a[i]+1), l=0, dp[i][j-l-1]) + dp[i][j] - dp[i][j-1-a[i]]
  // sigma(min(j,a[i]), k=0, dp[i][j-k]) = sigma(min(j-1, a[i]), k=0, dp[i][j-1-k]) + dp[i][j] - dp[i][j-1-a_i]

  for(int i=0; i<=n; i++){
    dp[i][0]=1;
  }
      
  for(int i=0; i<n; i++){
    for(int j=1; j<=m; j++){
      if(j-1-a[i] >=0){
	dp[i+1][j] = (dp[i+1][j-1] + dp[i][j] - dp[i][j - 1 - a[i]] + M) % M;
      } else {
	dp[i+1][j] = (dp[i+1][j-1] + dp[i][j]) % M;
      }
    }
  }

  printf("%d\n", dp[n][m]);

}

int main(){
  read();
  solve();
  return 0;
}

