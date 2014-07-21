#include<cstdio>
#include<set>
using namespace std;

const int MAX_N = 1000000;
const int MAX_K = 100;
const int MAX_X = 10000;

//INPUT
int N, K, X[MAX_N], A[MAX_K];

//Grundy number
int grundy[MAX_X + 1];

void solve(){
  // 0 is lost
  grundy[0] = 0;

  // compute grundy number
  int max_x = *max_element(X, X+N);

  for (int j=1; j <= max_x; j++){
    set<int> s;
    for (int i=0; i < K; i++){
      if (A[i] <= j) s.insert(grundy[j - A[i]]);
    }

    int g = 0;
    while (s.count(g) != 0) g++;
    grundy[j] = g;
  }

  //decide win/lost
  int x = 0;
  for (int i=0; i < N; i++) x ^= grundy[X[i]];

  if(x != 0) puts("Alice");
  else puts("Bob");
}

int main(){
  N=3, K=3;
  A[0]=1, A[1]=3, A[2]=4;
  X[0]=5, X[1]=6, X[2]=7;
  solve();

  fill(grundy, grundy+MAX_X+1, 0);

  N=3, K=3;
  A[0]=1, A[1]=3, A[2]=4;
  X[0]=5, X[1]=6, X[2]=8;
  solve();

  /*
  for(int i=1; i<1000; i++){
    X[2]=i;
    printf("%d:", i);
    solve();
  }
  */

}
