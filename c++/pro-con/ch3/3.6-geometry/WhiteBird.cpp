#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <cstdio>

using namespace std;

double EPS = 1e-10;

const double g = 9.8;
const int MAX_N = 100;
//INPUT
int N, V, X, Y;
int L[MAX_N], B[MAX_N], R[MAX_N], T[MAX_N];

// locate  @t seconds after shot upwards @ speed vy
double calc (double vy, double t){
  return vy * t - g * t * t /2;
}

// position of a relative to lb and ub
int cmp(double lb, double ub, double a){
  return a < lb + EPS ? -1 : a > ub - EPS ? 1: 0;
}

// decide if shoot egg at the pig when the bird shot through point (qx, qy)
bool check(double qx, double qy){
  // start spped vx, vy. the time t at qx, qy. solve the following equation.
  // vx^2 + vy^2 = V^2, vx*t = qx, vy*t - 1/2 g t^2 =qy
  double a = g * g / 4, b = g* qy - V*V, c = qx * qx + qy*qy;
  double D = b * b - 4 * a * c;
  if (D < 0 && D > -EPS) D = 0;
  if (D < 0) return false;
  for (int d = -1; d <=1; d+=2){ // try two solution of the equation
    double t2 = (-b + d * sqrt(D)) / (2*a);
    if (t2 <= 0) continue;
    double t = sqrt(t2);
    double vx = qx / t, vy = (qy + g * t *t / 2) / t;

    // is it possible to go over the pig?
    double yt = calc (vy, X / vx);
    if (yt < Y - EPS) continue;

    bool ok = true;
    for (int i=0; i<N; i++){
      if (L[i] >= X) continue;
      // when over the pig, no obstacles to the pig
      if (R[i] == X && Y <= T[i] && B[i] <= yt) ok = false;
      // no obstacles in the path
      int yL = cmp(B[i], T[i], calc(vy, L[i] / vx) ); // left-end
      int yR = cmp(B[i], T[i], calc(vy, R[i] / vx) ); // right-end
      int xH = cmp(L[i], R[i], vx * (vy / g)); // relative location of the highest point
      int yH = cmp(B[i], T[i], calc(vy, vy / g) ); 
      if (xH == 0 && yH >= 0 && yL < 0) ok = false;
      if (yL * yR <= 0) ok = false;
    }
    if (ok) return true;
  }
  return false;
}

void solve(){
  for (int i=0; i<N; i++){
    R[i] = min(R[i], X);
  }
  bool ok = check(X,Y);//direct attack
  for (int i=0; i<N; i++){
    ok |= check(L[i], T[i]); // left upper corner
    ok |= check(R[i], T[i]); // right upper corner
  }
  puts (ok ? "Yes" : "No");
}

int main(){
  //case1
  N=0; 
  V=7;
  X=3, Y=1;
  solve();

  //case2
  N=1; 
  V=7;
  X=3, Y=1;
  L[0] = 1, B[0] = 1, R[0] = 2, T[0] = 2;
  solve();

}


  
