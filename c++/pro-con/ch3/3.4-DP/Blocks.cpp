#include <algorithm>
#include <vector>

using namespace std;

typedef vector<int> vec;
typedef vector<vec> mat;
typedef long long ll;
const int M = 10007;

//const int MAX_N = 1000;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

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

int N;

void solve(){
  mat A(3, vec(3));
  A[0][0] = 2; A[0][1] = 1; A[0][2] = 0;
  A[1][0] = 2; A[1][1] = 2; A[1][2] = 2;
  A[2][0] = 0; A[2][1] = 1; A[2][2] = 2;
  A = pow(A, N);
  printf("%d\n", A[0][0]);
}

int main(){
  solve();
  return 0;
}

