#include<cstdio>
#include<vector>
using namespace std;

#define FILL(ptr, value) FILL_((ptr), sizeof(ptr) / sizeof(value), (value))
template <typename T>
void FILL_(void* ptr, size_t size, T value) {
  std::fill((T*)ptr, (T*)ptr + size, value);
}

const int MAX_T = 50;
const int MAX_M = 50;
const int MAX_N = 1000000000;
const int MAX_D = 10000;

//INPUT
int N, T;
int m[MAX_T];
int d[MAX_T][MAX_M];

// GCP function
int gcd(int a, int b) {
  if (b==0) return a;
  return gcd(b, a%b);
}
// Table of expectation (denomitor is N)
int E[MAX_T][MAX_D + 1];

void solve(){
  // expectation foreach t in T.
  for (int i=0; i<T; i++){
    for (int j=0; j<m[i]; j++){
      E[i][d[i][j]]++;
    }
    for (int a=1; a<=MAX_D; a++){
      E[i][a] += E[i][a-1];
    }
  }
  // total expectation
  // K + A / B
  long long K=0, A=0, B= (long long) N*N;
  for (int a = 1; a <= N && a <= MAX_D; a++){
    long long sum = 0, sum2 =0;
    for(int i=0; i<T; i++){
      sum += E[i][a];
      sum2 += E[i][a] * E[i][a];
    }
    if (a < MAX_D) {
      A += sum * sum - sum2 + sum * N;
      K += A / B;
      A %= B;
    } else {
      // expectation is equal for greater than MAX_D
      // care about overflow
      long long n = N - MAX_D + 1;
      K += sum * n / N;
      A += (sum * sum - sum2) * n + sum * n % N * N;
      K += A / B;
      A %= B;
      if (A<0){
	A += B;
	K--;
      }
    }
  }
  long long d = gcd (A, B);
  printf("%lld+%lld/%lld\n", K, A / d, B / d);
}

int main(){
  //fill(E.start(), E.end(), 0); 
  //fill(E, E+MAX_T*(MAX_D+1), 0); 
  FILL(E,0);
  N=1, T=1, m[0]=2, d[0][0]=1, d[0][1]=2;
  solve();

  FILL(E,0);
  N=4, T=2, m[0]=3, m[1] = 2;
  d[0][0]=1, d[0][1]=2, d[0][2]=4;
  d[1][0]=1, d[1][1]=3;
  solve();
}
