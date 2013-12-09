#include<algorithm>
#include<cstdio>
using namespace std;

const int MAX_N=10000;
const int MAX_W=1000000;
const double INF=1000000000.0;

int n,k;
int w[MAX_N], v[MAX_N];

double y[MAX_N]; // v - x*w

bool C(double x){
  for (int i=0; i<n; i++){
    y[i] = v[i] - x * w[i];
  }
  sort(y, y+n);
  double sum = 0;
  for (int i=0; i< k; i++){
    sum += y[n - i - 1];
  }
  return sum>=0;
}

void solve(){
  double lb=0, ub=INF;
  for(int i=0; i<100; i++){
    double mid=(lb+ub)/2;
    if(C(mid)) lb = mid;
    else ub = mid;
  }

  printf("%.2f\n", ub);
}
