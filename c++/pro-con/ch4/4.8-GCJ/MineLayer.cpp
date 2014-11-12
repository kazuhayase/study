#include<cstdio>
const int MAX_RC = 50*50;
//INPUT
int R, C;
int A[MAX_RC][MAX_RC];

// calc total as 1 dimension
int total(int *a, int n){
  int res = 0;
  // modulo 3 cases
  if (n % 3 == 1 || n % 3 == 2){
    for (int i=0; i<n; i+=3){
      res += a[i];
    }
  }
  else {
    for (int i=1; i<n; i+=3){
      res += a[i];
    }
  }
  return res;
}

// calc center as 1 dimension
int center(int *a, int n){
  int res;
  //modulo 3
  if (n % 3 == 1) {
    res = total(a, n);
    for (int i=1; i<n/2; i+=3){
      res -= a[i];
      res -= a[n-i-1];
    }
  }
  else if (n % 3 == 2) {
    res = total(a, n);
    for (int i=0; i<n/2; i+=3){
      res -= a[i];
      res -= a[n-i-1];
    }
  }
  else {
    res = 0;
    for (int i=0; i<n/2; i+=3){
      res += a[i];
      res += a[n-i-1];
    }
    res -= total(a,n);
  }
  return res;
}

void solve(){
  //sum for each row
  int rows[49];
  for (int i=0; i<R; i++){
    rows[i] = total(A[i], C);
  }
  int ans = center(rows, R);
  printf("%d\n", ans);
}

int main(){
  R=3, C=3;
  A[0][0]=2, A[0][1]=2, A[0][2]=1;
  A[1][0]=3, A[1][1]=4, A[1][2]=3;
  A[2][0]=2, A[2][1]=3, A[2][2]=2;
  solve();
}


