#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 100;
const int MAX_W = 10000;

int n,W;
int w[MAX_N],v[MAX_N];

int dp[MAX_N + 1][MAX_W +1];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &n);

  for(int i=0; i<n; i++){
    scanf("%d %d", &w[i],&v[i]);
  }

  scanf("%d\n", &W);
}

void solve(){

  for (int i=0; i<n; i++){
    for (int j=0; j <= W; j++){
      if (j < w[i]){
	dp[i+1][j] = dp[i][j];
      } else {
	dp[i+1][j] = max (dp[i][j], dp[i][j-w[i]] + v[i]);
      }
    }
  }
  printf("%d\n", dp[n][W]);
}
