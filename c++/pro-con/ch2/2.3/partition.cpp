#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 1000;
const int MAX_m = 1000;
const int MAX_M = 10000;

int n,m,M;
int dp[MAX_N + 1][MAX_m + 1];

void read(){
  scanf("%d %d %d\n", &n, &m, &M);
}

void solve(){

  // dp[i][j]=dp[i][j-i] + dp[i-1][j] 

  dp[0][0]=1;
  for(int i=1; i<=m; i++){
    for(int j=0; j<=n; j++){
      if(j-i>=0){
	dp[i][j] = (dp[i][j-i] + dp[i-1][j]) % M;
      } else {
	dp[i][j] = dp[i-1][j];
      }
    }
  }

  printf("%d\n", dp[m][n]);

}

int main(){
  read();
  solve();
  return 0;
}

