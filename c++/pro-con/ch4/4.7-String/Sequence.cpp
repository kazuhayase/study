#include<string>
using namespace std;

const int MAX_N = 1000;

//INPUT
int N, A[MAX_N];

int rev[MAX_N * 2], sa[MAX_N * 2];

int n,k;
int myrank[MAX_N + 1];
int tmp[MAX_N + 1];

// compare (myrank[i], myrank[i+k]) vs (myrank[j], myrank[j+k])
bool compare_sa(int i, int j){
  if(myrank[i] != myrank[j]) return myrank[i] < myrank[j];
  else {
    int ri = i+k <=n ? myrank[i+k] : -1;
    int rj = j+k <=n ? myrank[j+k] : -1;
    return ri < rj;
  }
}

void construct_sa(int *S, int n, int *sa){
  // n = (sizeof S) / (sizeof S[0]);
  // start length-1, rank is character code
  for (int i=0; i <=n; i++){
    sa[i] = i;
    myrank[i] = i < n ? S[i] : -1;
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
      myrank[i] = tmp[i];
    }
  }
}

void solve(){
  // inverse A and construct its Suffix Array;
  reverse_copy(A, A+N, rev);
  construct_sa(rev, N, sa); // for interger array

  // first separation (A1 | A2)
  int p1; 
  for (int i=0; i < N; i++){
    p1 = N - sa[i];
    if(p1 >= 1 && N - p1 >=2) break;
  }

  // for A2|A3. reverse & double & SA
  int m = N - p1;
  reverse_copy(A+p1, A+N, rev);
  reverse_copy(A+p1, A+N, rev+m);
  construct_sa(rev, m * 2, sa);

  // find separation on A2|A3. 
  int p2;
  for (int i=0; i<=2 * m; i++){
    p2 = p1 + m - sa[i];
    if (p2 - p1 >= 1 && N - p2 >=1) break;
  }

  reverse(A, A+p1);
  reverse(A+p1, A+p2);
  reverse(A+p2, A+N);
  for(int i=0; i<N; i++) printf("%d\n", A[i]);
}

int main(){
  N=5;
  A[0]=10, A[1]=1, A[2]=2, A[3]=3, A[4]=4;
  solve();
}
