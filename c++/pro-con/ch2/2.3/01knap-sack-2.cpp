#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 100;
const int MAX_w = 10000000;
const int MAX_v = 100;
const int MAX_W = 1000000000;
const int INF = 1000000000;

int n,W;
int w[MAX_N],v[MAX_N];

int dp[MAX_N + 1][MAX_N * MAX_v + 1];

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

  fill(dp[0], dp[0] + MAX_N * MAX_v +1, INF);
  dp[0][0] = 0;
  for (int i=0; i<n; i++){
    for (int j=0; j <= MAX_N * MAX_v; j++){
      if (j < v[i]){
	dp[i+1][j] = dp[i][j];
      } else {
	dp[i+1][j] = min ( dp[i][j], dp[i][j - v[i]] + w[i] );
      }
    }
  }

  int res=0;
  for (int i=0; i <= MAX_N * MAX_v; i++){
    if (dp[n][i] <=W) res=i;
  }
  printf("%d\n", res);
}
