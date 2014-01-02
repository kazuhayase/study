#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>

using namespace std;

const int MAX_N = 10000;
const int MAX_C = 10000;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1
const int ST_SIZE = (1 << 15) -1;

//INPUT

int N,C;
int L[MAX_N];
int S[MAX_C], A[MAX_C];

//segment tree
double vx[ST_SIZE], vy[ST_SIZE];
double ang[ST_SIZE];

double prv[MAX_N];

// initialize segment tree
// k-th node is for [l,r)
void init(int k, int l, int r){
  ang[k] = vx[k] = 0.0;

  if (r-l == 1){
    //leaf
    vy[k] = L[l];
  } else {
    //non-leaf
    int chl = k*2+1, chr = k*2+2;
    init(chl, l, (l+r)/2);
    init(chr, (l+r)/2, r);
    vy[k] = vy[chl] + vy[chr];
  }
}

// angle at location "s" is modified by "a"
void change(int s, double a, int v, int l, int r) {
  if (s <= l) return;
  else if (s < r){
    int chl = v*2+1, chr = v*2+2;
    int m = (l+r)/2;
    change(s, a, chl, l, m);
    change(s, a, chr, m, r);
    if (s<=m) ang[v] += a;

    double s = sin(ang[v]), c = cos(ang[v]);
    vx[v] = vx[chl] + (c*vx[chr] - s*vy[chr]);
    vy[v] = vy[chl] + (s*vx[chr] + c*vy[chr]);
  }
}

void solve(){

  init(0,0,N);
  for (int i=0; i<N; i++) prv[i] = M_PI;

  // process queries
  for (int i=0; i<C; i++){
    int s = S[i];
    double a = A[i] / 360.0 * 2 * M_PI; //radian
    change(s, a - prv[s], 0,  0, N);
    prv[s] = a;

    printf("%.2f %.2f\n", vx[0], vy[0]);
  }
}

int main(){
  solve();
  return 0;
}

