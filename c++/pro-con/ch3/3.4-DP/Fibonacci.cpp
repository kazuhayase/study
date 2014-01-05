#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <vector>

using namespace std;

typedef vector<int> vec;
typedef vector<vec> mat;
typedef long long ll;
const int M = 10000;

const int MAX_N = 50;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

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

ll n;

void solve(){
  mat A(2, vec(2));
  A[0][0] = 1; A[0][1] = 1;
  A[1][0] = 1; A[1][1] = 0;
  A = pow(A, n);
  printf("%d\n", A[1][0]);
}

int main(){
  solve();
  return 0;
}

