#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 1000;

//INPU
int N, P[MAX_N];

void solve(){
  if (N % 2 == 1) P[N++] =0;

  sort(P, P + N);

  int x = 0;
  for (int i=0; i+1 < N; i += 2){
    x ^= (P[i+1] - P[i] - 1);
  }
  if (x == 0) puts ("Bob will win");
  else puts ("Georgia will win");
}

int main(){
  N=3, P[0] = 1, P[1] = 2, P[2] = 3;
  solve();

  N=8, P[0] = 1, P[1] = 5, P[2] = 6, P[3] =7, P[4] = 9,
    P[5] = 12, P[6] = 14, P[7] = 17;
  solve();

}
