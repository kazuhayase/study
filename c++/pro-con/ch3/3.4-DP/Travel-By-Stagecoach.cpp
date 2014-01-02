#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <vector>

using namespace std;

const int MAX_N = 8;
const int MAX_M = 30;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

//INPUT

int n,m,a,b;
int t[MAX_N];
int d[MAX_M][MAX_M];

//dp[S][v] := S of tickets and at v.
double dp[1 << MAX_N][MAX_M];

void solve(){
  for(int i=0; i < 1<<n; i++){
    fill(dp[i], dp[i]+m, INF);
  }
  dp[(1<<n) - 1][a - 1] = 0;
  double res = INF;
  for(int S= (1<<n) - 1; S>=0; S--){
    res = min(res, dp[S][b - 1]);
    for(int v=0; v < m; v++){
      for(int i=0; i < n; i++){
	if (S >> i & 1){
	  for(int u=0; u < m; u++){
	    if(d[v][u] >= 0){
	      dp[S & ~(1 << i)][u] = min(dp[S & ~(1 << i)][u], dp[S][v] + (double) d[v][u] / t[i]);
	    }
	  }
	}
      }
    }
  }
  if (res == INF){
    printf("Impossible\n");
  } else {
    printf("%.3f\n", res);
  }
}

int main(){
  solve();
  return 0;
}

