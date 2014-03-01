#include <cstdlib>
#include <cstdio>

double EPS = 1e-10;

// gosa
double add(double a, double b){
  if (abs(a+b) < EPS * (abs(a) + abs(b))) return 0;
  return a+b;
}

//2 dimensions vector
struct P {
  double x, y;
  P(){};
  P(double x, double y) : x(x), y(y) {
  }
  P operator + (P p) {
    return P(add(x, p.x), add(y, p.y));
  }
  P operator - (P p) {
    return P(add(x, -p.x), add(y, -p.y));
  }
  P operator * (double d) {
    return P(x*d, y*d);
  }
  double dot(P p) {// naiseki
    return add(x * p.x, y * p.y);
  }
  double det(P p) {// gaiseki
    return add(x * p.y, -y *p.x);
  }
};

// decision if q is on segment p1-p2
bool on_seg(P p1, P p2, P q){
  return (p1 - q).det(p2 - q) == 0 && (p1 - q).dot(p2 - q) <= 0;
}

// intersecting point of lines p1-p2 and q1-q2
P intersection(P p1, P p2, P q1, P q2){
  return p1 + (p2 - p1) * ((q2 - q1).det(q1 - p1) / (q2 - q1).det(p2 - p1));
}

const int MAX_N = 100;
const int MAX_M = 100;

//INPUT
int n = 4;
P p[MAX_N] = { P(0,4), P(0,1), P(1,2), P(1,0)}, 
  q[MAX_N] = { P(4,1), P(2,3), P(3,4), P(2,1)};
int m = 4;
int a[MAX_M] = {1,1,2,2}, b[MAX_M] = {2,4,3,4};

bool g[MAX_N][MAX_N]; // graph on connection

void solve(){
  for (int i=0; i<n; i++){
    g[i][i] = true;
    for (int j=0; j<i; j++){
      // do bar i & j have a common point?
      if ((p[i] - q[i]).det(p[j] - q[j]) == 0) {
	// case of parallel
	g[i][j] = g[j][i] = on_seg(p[i], q[i], p[j])
	  || on_seg(p[i], q[i], q[j])
	  || on_seg(p[j], q[j], p[i])
	  || on_seg(p[j], q[j], q[i]);
      } else {
	// not parallel
	P r = intersection(p[i], q[i], p[j], q[j]);
	g[i][j] = g[j][i] = on_seg(p[i], q[i], r) && on_seg(p[j], q[j], r);
      }
    }
  }
  // warshall-froyd to decide connectivity
  for (int k=0; k < n; k++){
    for (int i=0; i < n; i++){
      for (int j=0; j < n; j++){
	g[i][j] |= g[i][k] && g[k][j];
      }
    }
  }

  for (int i=0; i<m; i++){
    puts(g[a[i] - 1][b[i] - 1] ? "CONNECTED" : "NOT CONNECTED");
  }
}

int main(){
  n = 4;
  //p[MAX_N] = { P(0,4), P(0,1), P(1,2), P(1,0)}; 
  //q[MAX_N] = { P(4,1), P(2,3), P(3,4), P(2,1)};
  m = 4;
  //a[MAX_M] = {1,1,2,2}, b[MAX_M] = {2,4,3,4};
  solve();
}
