#include<cstdio>
#include <algorithm>
using namespace std;

//using DP; O(n W log m)

//INPUT
const int MAX_N = 10000;
const int MAX_W = 10000;
int n, W;
int w[MAX_N], v[MAX_N], m[MAX_N];

int dp[MAX_W + 1]; // DP table

void solve(){
  for (int i=0; i<n; i++){
    int num = m[i];
    for (int k=1; num > 0; k<<=1){
      int mul = min(k, num);
      for (int j = W; j >= w[i] * mul; j--){
	dp[j] = max(dp[j], dp[j - w[i] * mul] + v[i] * mul);
      }
      num -= mul;
    }
  }
  printf("%d\n", dp[W]);
}

int main(){
  n=3, W=12;
  w[0] = 3, v[0] = 2, m[0] = 5;
  w[1] = 2, v[1] = 4, m[1] = 1;
  w[2] = 4, v[2] = 3, m[2] = 3;
  solve();
}
