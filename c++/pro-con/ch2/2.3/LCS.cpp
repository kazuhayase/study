#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 1000;
const int MAX_M = 1000;

int n,m;
char s[MAX_N],t[MAX_M];

int dp[MAX_N + 1][MAX_M +1];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &n);
  scanf("%d\n", &m);

  for(int i=0; i<n; i++){
    scanf("%c", &s[i]);
  }
  scanf("\n");

  for(int i=0; i<m; i++){
    scanf("%c", &t[i]);
  }
  scanf("\n");

}

void solve(){

  for (int i=0; i<n; i++){
    for (int j=0; j <m; j++){
      if (s[i] == t[j]){
	dp[i+1][j+1] = dp[i][j]+1;
      } else {
	dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1]);
      }
    }
  }
  printf("%d\n", dp[n][m]);
}
