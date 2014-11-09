#include<string>
using namespace std;

const int MAX_N = 1000;
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
  // start length=1, rank is character code
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

// search
bool contain(string S, int *sa, string T) {
  int a=0, b=S.length();
  while (b-a>1){
    int c = (a+b)/2;
    // compare T-length S from sa[c] with T
    if (S.compare(sa[c], T.length(), T) < 0) a=c;
    else b=c;
  }
  return S.compare(sa[b], T.length(), T) == 0;
}

// LCP (Longest Common Prefix Array)

void construct_lcp(string S, int *sa, int *lcp){
  int n = S.length();
  for (int i=0; i<=n; i++) lcprank[sa[i]]=i;

  int h=0;
  lcp[0]=0;
  for(int i=0; i<n; i++){
    int j = sa[lcprank[i] - 1];
    if (h>0) h--;
    for(; j+h<n && i+h<n; h++){
      if(S[j+h] != S[i+h]) break;
    }
    lcp[lcprank[i] - 1] = h;
  }
}
    
int main(){
  string S="abracadabra";
  int SA[100];
  int LCP[100];
  construct_sa(S, SA);
  construct_lcp(S, SA, LCP);

  //printf("i, S[i], SA[i], LCP[i]\n");
  printf("i, SA[i], LCP[i]\n");
  for(int i=0; i<15; i++){
    printf("%d,%d,%d\n", i,SA[i],LCP[i]);
  }
}
  
