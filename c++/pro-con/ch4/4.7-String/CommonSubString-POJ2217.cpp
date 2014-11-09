#include<string>
using namespace std;

const int MAX_N = 20001;
const int MAX_L = 10000;

int n,k;
int sarank[MAX_N + 1];
int lcprank[MAX_N + 1];
int tmp[MAX_N + 1];

// compare (sarank[i], sarank[i+k]) vs (sarank[j], sarank[j+k])
bool compare_sa(int i, int j){
  if(sarank[i] != sarank[j]) return sarank[i] < sarank[j];
  else {
    int ri = i+k <=n ? sarank[i+k] : -1;
    int rj = j+k <=n ? sarank[j+k] : -1;
    return ri < rj;
  }
}

void construct_sa(string S, int *sa){
  n = S.length();
  // start length-1, rank is character code
  for (int i=0; i <=n; i++){
    sa[i] = i;
    sarank[i] = i < n ? S[i] : -1;
  }

  //k -> 2k
  for (k=1; k <= n; k *=2) {
    sort (sa, sa+n+1, compare_sa);
    
    // once computed in tmp and move to rank
    tmp[sa[0]] = 0;
    for (int i=1; i <= n; i++){
      tmp[sa[i]] = tmp[sa[i-1]] + (compare_sa(sa[i-1], sa[i]) ? 1 : 0);
    }
    for(int i=0; i<=n; i++){
      sarank[i] = tmp[i];
    }
  }
}

// LCP (Longest Common Prefix Array)

void construct_lcp(string S, int *sa, int *lcp){
  int n = S.length();
  for (int i=0; i<=n; i++) lcprank[sa[i]]=i;

  int h=0;
  lcp[0]=0;
  for(int i=0; i<=n; i++){
    int j = sa[lcprank[i] - 1];
    if (h>0) h--;
    for(; j+h<n && i+h<n; h++){
      if(S[j+h] != S[i+h]) break;
    }
    lcp[lcprank[i] - 1] = h;
  }
}

//INPUT 
string S,T;

int sa[MAX_L], lcp[MAX_L];

void solve(){
  int s1 = S.length();
  S += '\0' + T;

  construct_sa(S, sa);
  construct_lcp(S, sa, lcp);

  int ans=0;
  for(int i=0; i<S.length(); i++){
    if ((sa[i]<s1) !=(sa[i+1]<s1)){
      ans=max(ans, lcp[i]);
    }
  }
  printf("%d\n", ans);
}

int main(){
  S="ABRACADABRA";
  T="ECADADABRBCRDAR";
  solve();
}

