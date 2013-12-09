#include <cstdio>
#include <iostream>
#include <algorithm>

using namespace std;

int T;
const int MAX_T = 20;

int N,K,C;
const int MAX_N = 1000000;//1M
const int MAX_K = 1000000;//1M

void read_T();
void read();
int solve(int t);

int main(){
  read_T();
  for(int t=0; t < T; t++){
    read();
    printf("Case #%d: %d\n", t+1, solve(t));
  }
  return 0;
}

void read_T(){
  cin >> T;
  fprintf(stderr, "T=%d\n", T);
}

void read(){
  scanf("%d %d %d", &N,&K,&C);
  fprintf(stderr, "N=%d, K=%d, C=%d\n", N,K,C);
}

int solve(int t){

  int qk,rk,qc,rc;
  int ans;

  rk = K % N;
  qk = (K - rk) / N;
  rc = C % N;
  qc = (C - rc) / N;

  if( rc==0 || qc < qk ) return C;

  if( qk==0 ) return C + (N-K);

  int rest = N - rk;

  if( qk==1 ) return C + (rest+1)/2;

  int alpha = rest % (qk+1);
  int move = (rest - alpha) / (qk+1);
  if (alpha==0) return C+move+1;
  return C+move+1;

}
