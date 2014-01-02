#include <algorithm>
using namespace std;
typedef long long ll;
const int DAT_SIZE = (1<<18) - 1;

const int MAX_N = 100000;
const int MAX_Q = 100000;

//INPUT
int N, Q;
int A[MAX_N];
char T[MAX_Q];
int L[MAX_Q], R[MAX_Q], X[MAX_Q];

// BIT
ll bit0[MAX_N+1], bit1[MAX_N+1];

// calc sum
ll sum(ll *b, int i){
  ll s = 0;
  while(i>0){
    s += b[i];
    i -= i & -i;
  }
  return s;
}

void add(ll *b, int i, int v){
  while(i <= N){
    b[i] += v;
    i += i & -i;
  }
}


void solve(){
  for(int i=1; i<=N; i++){
    add(bit0, i, A[i]);
  }
  for(int i=0; i<Q; i++){
    if(T[i] == 'C'){
      add(bit0, L[i], -X[i] * (L[i] - 1));
      add(bit1, L[i], X[i]);
      add(bit0, R[i]+1, X[i] * R[i]);
      add(bit1, R[i]+1, -X[i]);
    } else {
      ll res = 0;
      res += sum(bit0, R[i]) + sum(bit1, R[i]) * R[i];
      res -= sum(bit0, L[i]-1) + sum(bit1, L[i]-1) * (L[i]-1);
      printf("%lld\n", res);
    }
  }
}

