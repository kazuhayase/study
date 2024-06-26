#include <vector>

using namespace std;

typedef vector<int> vec;
typedef vector<vec> mat;
typedef long long ll;

int n, k, M;

// matrix mul & pow

mat mul(mat &A, mat &B){
  mat C(A.size(), vec(B[0].size()));
  for(int i=0; i < A.size(); i++){
    for(int k=0; k < B.size(); k++){
      for(int j=0; j < B[0].size(); j++){
      C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % M;
      }
    }
  }
  return C;
}

mat pow(mat A, ll n){
  mat B(A.size(), vec(A.size()));
  for (int i=0; i < A.size(); i++){
    B[i][i] = 1;
  }
  while(n > 0){
    if (n & 1) B = mul(B,A);
    A = mul(A,A);
    n >>= 1;
  }
  return B;
}

//INPUT
//int n, k, M;
mat A;

void solve(){
  mat B(n*2, vec(n*2));
  for(int i=0; i<n; i++){
    for(int j=0; j<n; j++){
      B[i][j] = A[i][j];
    }
    B[n+i][i] = B[n+i][n+i] = 1;
  }
  B = pow(B, k+1);
  for (int i=0; i<n; i++){
    for(int j=0; j<n; j++){
      int a = B[n+i][j] % M;
      if(i == j) a = (a + M -1) % M;
      printf ("%d%c", a, j+1 == n ? '\n' : ' ');
    }
  }
}
