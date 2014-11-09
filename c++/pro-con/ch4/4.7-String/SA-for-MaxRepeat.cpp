#include<string>
#include<algorithm>
using namespace std;

const int MAX_L = 100000;
const int MAX_N = 100000;

int SA_rank[MAX_L+1], LCP_rank[MAX_L+1];
int tmp[MAX_N + 1];
int n,k;

// compare (SA_rank[i], SA_rank[i+k]) vs (SA_rank[j], SA_rank[j+k])
bool compare_sa(int i, int j){
  if(SA_rank[i] != SA_rank[j]) return SA_rank[i] < SA_rank[j];
  else {
    int ri = i+k <=n ? SA_rank[i+k] : -1;
    int rj = j+k <=n ? SA_rank[j+k] : -1;
    return ri < rj;
  }
}

void construct_sa(string S, int *sa){
  n = S.length();
  // start length=1, rank is character code
  for (int i=0; i <=n; i++){
    sa[i] = i;
    SA_rank[i] = i < n ? S[i] : -1;
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
      SA_rank[i] = tmp[i];
    }
  }
}

// LCP (Longest Common Prefix Array)

void construct_lcp(string S, int *sa, int *lcp){
  int n = S.length();
  for (int i=0; i<=n; i++) LCP_rank[sa[i]]=i;

  int h=0;
  lcp[0]=0;
  for(int i=0; i<n; i++){
    int j = sa[LCP_rank[i] - 1];
    if (h>0) h--;
    for(; j+h<n && i+h<n; h++){
      if(S[j+h] != S[i+h]) break;
    }
    lcp[LCP_rank[i] - 1] = h;
  }
}

