#include <string>
const char *AGCT="AGCT";
const int MOD = 10009;

using namespace std;

const int MAX_N = 10000;
const int MAX_K = 50;

//INPUT
int N,K;
string S;

int nextS[MAX_K][4];
int dp[MAX_N+1][MAX_K];

void solve(){
  //pre computation
  for (int i=0; i<K; i++){
    for (int j=0; j<4; j++){
      // add one character to the matched string of length i
      string s = S.substr(0, i) + AGCT[j];
      // delete character for matching the head of S
      while(S.substr(0, s.length()) != s){
	s = s.substr(1);
      }
      nextS[i][j] = s.length();
    }
  }

  // initialize DP
  dp[0][0]=1;
  for(int i=1; i<K; i++) dp[0][i]=0;
  //DP
  for (int t=0; t<N; t++){
    for (int i=0; i<K; i++) dp[t+1][i]=0;
    for (int i=0; i<K; i++) {
      for (int j=0; j<4; j++){
	int ti = nextS[i][j];
	if (ti == K) continue; //NG because S appears
	dp[t+1][ti] = (dp[t+1][ti] + dp[t][i]) % MOD;
      }
    }
  }

  int ans=0;
  for (int i=0; i < K; i++) ans = (ans + dp[N][i]) % MOD;
  printf("%d\n", ans);
}

int main(){
  N=3, K=2, S="AT";
  solve();
}
