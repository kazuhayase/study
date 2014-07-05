#include <cstdio>
// Nim
// a1 XOR a2 XOR ... XOR an != 0 --> win
// a1 XOR a2 XOR ... XOR an == 0 --> lose

const int MAX_N = 1000000;
// INPUT
int N, A[MAX_N];

void solve(){
  int x = 0;
  for (int i=0; i < N; i++) x ^= A[i];

  if(x != 0) puts("Alice");
  else puts("Bob");
}

int main (){
  N=3, A[0]=1, A[1]=2, A[2]=4;
  solve();

  N=3, A[0]=1, A[1]=2, A[2]=3;
  solve();
}
  
