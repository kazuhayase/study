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

int rec(int i, int j) {
  if (dp[i][j] >=0){
    return dp[i][j];
  }

  int res;
  if (i == n){
    res = 0;
  } else if (j<w[i]) {
    res = rec(i+1, j);
  } else {
    res = max (rec(i+1, j), rec(i+1, j-w[i]) + v[i]);
  }
  return dp[i][j]=res;
}

void solve(){
  memset(dp, -1, sizeof(dp));
  printf("%d\n", rec(0,W));

}
