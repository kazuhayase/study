#include <string>
#include <vector>
const char *AGCT="AGCT";

using namespace std;

const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1
const int MAX_N = 10000;
const int MAX_K = 50;
const int MAX_STATE = 1000;
const int MAX_LEN_S = 100;

//INPUT
int N;
string S, P[MAX_N];

int nextS[MAX_STATE][4];
bool ng[MAX_STATE];

int dp[MAX_LEN_S + 1][MAX_STATE];

void solve(){
  //enumerate all prefixes
  vector<string> pfx;

  for (int i=0; i<N; i++){
    for (int j=0; j<= P[i].length(); j++){
      pfx.push_back(P[i].substr(0,j));
    }
  }
  // sort & erase duplications
  sort(pfx.begin(), pfx.end());
  pfx.erase(unique(pfx.begin(), pfx.end()), pfx.end());
  int K = pfx.size();

  // compute for each state
  for (int i=0; i<K; i++){
    //NG if tail matches a forbidden pattern
    ng[i]=false;
    for (int j=0; j<N; j++){
      ng[i] |= P[j].length() <= pfx[i].length() 
	&& pfx[i].substr(pfx[i].length() - P[j].length(), P[j].length()) == P[j];
    }
    for (int j=0; j<4; j++){
      string s= pfx[i] + AGCT[j];
      int k;
      for(;;){
	k=lower_bound(pfx.begin(), pfx.end(), s) - pfx.begin();
	if (k < K && pfx[k]==s) break;
	s = s.substr(1);
      }
      nextS[i][j]=k;
    }
  }

  //initialize DP
  dp[0][0]=1;
  for(int i=1; i<K; i++) dp[0][i]=0;

  //DP
  for (int t=0; t < S.length(); t++){
    for(int i=0; i<K; ++i) dp[t+1][i]=INF;

    for(int i=0; i<K; i++){
      if (ng[i]) continue;
      for (int j=0; j<4; j++){
	int k = nextS[i][j];
	dp[t+1][k] = min(dp[t+1][k], dp[t][i] + (S[t] == AGCT[j] ? 0 : 1));
      }
    }
  }

  int ans=INF;
  for (int i=0; i < K; ++i) {
    if(ng[i]) continue;
    ans = min(ans, dp[S.length()][i]);
  }
  if (ans == INF) puts("-1");
  else printf("%d\n", ans);
}

int main(){
  N=2;
  S="AAAG", P[0] = "AAA", P[1]="AAG";
  solve();

  N=2;
  S="TGAATG", P[0] = "A", P[1]="TG";
  solve();

  N=4;
  S="AGT", P[0] = "A", P[1]="G", P[2]="C", P[3]="T";
  solve();
}
