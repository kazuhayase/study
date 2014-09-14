#include<cstdio>
#include <algorithm>
using namespace std;

// L[i] := max{j; j<=i && h[j-1] < h[i]}
// R[i] := min{j; i< j && h[j] < h[i]}
// solution = max{h[i] * (R[i] - L[i])
// L[i] is calculated by a stack s.t. (1) x[i]>x[i+1]  && (2) h[x[i]] > h[x[i+1]]

//INPUT
const int MAX_N = 100000;
int n;
int h[MAX_N];

int L[MAX_N], R[MAX_N];
int st[MAX_N]; //stack

void solve(){

  // Calculation of L
  int t=0; // size of the stack
  for (int i=0; i<n; i++){
    while (t > 0 && h[st[t-1]] >= h[i]) t--;
    L[i] = t == 0 ? 0 : (st[t-1] + 1);
    st[t++] = i;
  }

  // Calculation of R
  t=0; // size of the stack
  for (int i=n-1; i>=0; i--){
    while (t > 0 && h[st[t-1]] >= h[i]) t--;
    R[i] = t == 0 ? n : st[t-1];
    st[t++] = i;
  }

  long long res = 0;
  for (int i=0; i < n; i++) {
    res = max (res, (long long) h[i] * (R[i] - L[i]));
  }
  printf("%lld\n", res);
}

int main(){
  n=7;
  h[0]=2, h[1]=1, h[2]=4, h[3]=5, h[4]=1, h[5]=3, h[6]=3;
  solve();
}

