#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 100;
const int MAX_W = 10000;

int n,W;
int w[MAX_N],v[MAX_N];

int dp[MAX_W +1];

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
    for (int j=W; j >= w[i]; j--){
      dp[j] = max(dp[j], dp[j-w[i]]+v[i]);
    }
  }
  printf("%d\n", dp[W]);
}
