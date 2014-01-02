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

void solve() {
  for (int S=0; S < 1 << n; S++){
    fill(dp[S], dp[S] + n, INF);
  }
  dp[ (1 << n) - 1][0] = 0;

  for(int S = (1 << n) - 2; S >= 0; S--){
    for(int v=0; v<n; v++){
      for(int u=0; u<n; u++){
	if(!(S >> u & 1)){
	  dp[S][v] = min (dp[S][v], dp[S | 1 << u][u] + d[v][u]);
	}
      }
    }
  }
  printf("%d\n", dp[0][0]);
}

int main(){
  solve();
  return 0;
}

