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

//INPUT

int n,m,M;
bool color[MAX_N][MAX_M]; // false:white, true:black

int rec(int i, int j, bool used[MAX_N][MAX_M]){
  if (j == m){ // next row
    return rec(i+1, 0, used);
  }

  if (i == n){// finish
    return 1;
  }

  if(used[i][j] || color[i][j]){
    return rec(i, j+1, used);
  }

  int res = 0;
  used[i][j] = true;

  // Yoko
  if (j+1 < m && !used[i][j+1] && !color[i][j+1]) {
    used[i][j+1] = true;
    res += rec(i, j+1, used);
    used[i][j+1] = false;
  }

  // Tate
  if (i+1 < n && !used[i+1][j] && !color[i+1][j]) {
    used[i+1][j] = true;
    res += rec(i, j+1, used);
    used[i+1][j] = false;
  }

  used[i][j] = false;
  return res % M;
}

void solve(){

  bool used[MAX_N][MAX_M];
  memset(used, 0, sizeof(used));
  printf("%d\n", rec(0, 0, used));

}

int main(){
  solve();
  return 0;
}

