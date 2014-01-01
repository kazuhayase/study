#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 4000;

//input
int n;
int A[MAX_N],B[MAX_N],C[MAX_N],D[MAX_N];

int CD[MAX_N * MAX_N];

void solve(){
  // enumerate all CD
  for(int i=0; i<n; i++){
    for(int j=0; i<n; i++){
      CD[i*n+j]=C[i]+D[j];
    }
  }
  sort(CD,CD+n*n);

  long long res=0;
  for(int i=0; i<n; i++){
    for(int j=0; i<n; i++){
      int cd = a(A[i] + B[j]);
      res += upper_bound(CD, CD+n*n, cd) - lower_bound(CD, CD+n*n, cd);
    }
  }
  printf("%lld\n", res);
}

int main(){
  solve();
  return 0;
}

