#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 5000;

int N;
int dir[MAX_N];//0:F, 1:B
int f[MAX_N];

int calc(int K){
  memset(f, 0, sizeof(f));
  int res=0;
  int sum=0;
  for(int i=0; i+K <= N; i++){
    if ((dir[i] + sum) % 2 !=0){
      res++;
      f[i] = 1;
    }
    sum += f[i];
    if (i-K+1 >=0){
      sum -= f[i-K+1];
    }
  }

  //nokori
  for (int i = N-K+1; i<N; i++){
    if((dir[i]+sum) % 2 !=0){
      return -1;
    }
    if (i-K+1 >=0){
      sum -= f[i-K+1];
    }
  }
  return res;
}

void solve(){

  int K=1, M=N;
  for(int k=1; k<=N; k++){
    int m= calc(k);
    if (m>=0 && M>m){
      M=m;
      K=k;
    }
  }
  printf("%d %d\n", K, M);

}

int main(){
  solve();
  return 0;
}

