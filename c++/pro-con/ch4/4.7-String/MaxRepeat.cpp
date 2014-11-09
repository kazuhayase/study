#include<string>
#include<algorithm>
#include "SA-for-MaxRepeat.cpp"
#include "RMQ-for-MaxRepeat.cpp"
using namespace std;

//INPUT
string S;

int sa[MAX_L+1], lcp[MAX_L];
int MR_rank[MAX_L+1];

//int tmp[MAX_N + 1];
//int n,k;

void solve(){
  int org_n = S.length();
  string T = S;
  reverse(T.begin(), T.end());
  S += '$' + T;
  
  construct_sa(S, sa);
  construct_lcp(S, sa, lcp);
  for(int i=0; i <= S.length(); i++) MR_rank[sa[i]]=i;
  construct_rmq(lcp, S.length() +1);

  int ans=0;

  //Repeating sentence centered at character i of odd length
  for(int i=0; i<org_n; i++){
    int j = org_n*2 -i;
    int l = query_rmq(min(MR_rank[i], MR_rank[j]), max(MR_rank[i], MR_rank[j]));
    ans = max(ans, 2 * l - 1);
  }

  //Repeating sentence centered between i-1 & i of even length
  for(int i=1; i<org_n; i++){
    int j = n*2 -i + 1;
    int l = query_rmq(min(MR_rank[i], MR_rank[j]), max(MR_rank[i], MR_rank[j]));
    ans = max(ans, 2*l);
  }

  printf("%d\n", ans);
}

int main(){
  S = "mississippi";
  solve();
}
