#include <cstdio>
#include <cmath>
#include <algorithm>
using namespace std;

const double g = 10.0;

const int MAX_N = 100;

//input
int N,H,R,T;
int y[MAX_N];

double calc(int T){
  if(T<0) return H;
  double t = sqrt(2*H/g);
  int k = (int) (T/t);
  if(k%2 == 0){
    double d = T - k*t;
    return H - g * d * d / 2;
  } else {
    double d = k*t+t-T;
    return H - g * d * d / 2;
  }
}  

void solve(){
  for(int i=0; i<N; i++){
    y[i] = calc(T-i);
  }
  sort(y,y+N);
  for(int i=0; i<N; i++){
    printf("%.2f%c", y[i] + 2*R*i/100.0, i+1 == N ? '\n' : ' ');
  }
}

int main(){
  solve();
  return 0;
}

