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
const int MAX_M = 15;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

int dp[2][1 << MAX_M];

//INPUT

int n,m,M;
bool color[MAX_N][MAX_M]; // false:white, true:black


void solve(){
  int *crt = dp[0], *next = dp[1];
  crt[0] = 1;
  for(int i = n-1; i >= 0; i--){
    for(int j = m-1; j >= 0; j--){
      for(int used = 0; used < 1<<m; used++){
	if( (used >> j & 1) || color[i][j]) {
	  next[used] = crt[used & ~(1 << j)];
	} else {
	  int res = 0;

	  //Yoko
	  if ( j+1 < m && !(used >> (j+1) & 1) && !color[i][j+1]){
	    res += crt[used | 1 << (j+1)];
	  }

	  //Tate
	  if ( i+1 < n && !color[i+1][j]){
	    res += crt[used | 1 << j];
	  }
	  next[used] = res % M;
	}
      }
      swap(crt, next);
    }
  }
  printf("%d\n", crt[0]);
}

int main(){
  solve();
  return 0;
}

