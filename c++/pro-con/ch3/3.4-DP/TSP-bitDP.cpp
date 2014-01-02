#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <vector>

using namespace std;

const int MAX_N = 15;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

//INPUT

int n;
int d[MAX_N][MAX_N];

//memo
int dp[1 << MAX_N][MAX_N];

int rec(int S, int v){
  if (dp[S][v] >= 0){
    return dp[S][v];
  }

  if (S == (1 << n) - 1 && v == 0){
    return dp[S][v] = 0;
  }

  int res = INF;
  for(int u=0; u<n; u++){
    if(!(S >> u & 1)) {
      res = min (res, rec(S | 1 << u, u) + d[v][u]);
    }
  }
  return dp[S][v] = res;
}

void solve(){

  memset(dp, -1, sizeof(dp));
  printf("%d\n", rec(0, 0));

}

int main(){
  solve();
  return 0;
}

