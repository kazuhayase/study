#include <cstdio>
const int MAX_K = 100;
const int MAX_X = 10000;

//INPUT
int X, K, A[MAX_K];

// array for DP
bool win[MAX_X + 1];

void solve(){
  // 0 is lost
  win[0] = false;

  for(int j=1; j<=X; j++){
    win[j] = false;
    for (int i=0; i < K; i++){
      win[j] |= A[i]<= j && !win[j - A[i]];
    }
  }

  if(win[X]) puts("Alice");
  else puts("Bob");
}

int main(){
  X=9; K=2; A[0] = 1, A[1] = 4;
  solve();

  X=10; K=2; A[0] = 1, A[1] = 4;
  solve();
}
