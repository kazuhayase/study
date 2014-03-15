// ?Beauty Contest??
// Graham scan to find convex
// caryper to find most distant pair by scanning anti clockwise

#include <cstdlib>
#include <cstdio>
#include <vector>
#include <cmath>

using namespace std;

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

//compare by dictionary order
bool cmp_x(const P& p, const P& q){
  if (p.x != q.x) return p.x < q.x;
  return p.y < q.y;
}

vector<P> convex_hull(P* ps, int n){
  sort(ps, ps+n, cmp_x);
  int k=0;// number of vertices
  vector<P> qs(n * 2); // convex

  // lower part
  for (int i=0; i<n; i++){
    while(k > 1 && (qs[k-1] - qs[k-2]).det(ps[i] - qs[k-1]) <= 0) k--;
    qs[k++] = ps[i];
  }
  // upper part
  for (int i=n-2, t=k; i>=0; i--){
    while(k > t && (qs[k-1] - qs[k-2]).det(ps[i] - qs[k-1]) <= 0) k--;
    qs[k++] = ps[i];
  }
  qs.resize(k-1);
  return qs;
}

// square of distance
double dist(P p, P q){
  return (p-q).dot(p-q);
}

//INPUT
const int MAX_N = 50000;
int N;
P ps[MAX_N];

void solve(){
  vector <P> qs = convex_hull(ps, N);
  int n = qs.size();
  if (n == 2){
    printf("%.0f\n", dist(qs[0], qs[1]));
  }

  int i=0, j=0;// most distant pair
  // most distant in x
  for (int k=0; k<n; k++){
    if (!cmp_x(qs[i], qs[k])) i=k;
    if (cmp_x(qs[j], qs[k])) j=k;
  }

  double res=0;
  int si=i, sj=j;
  while(i != sj || j != si){ // change direction 180 degree
    res = max(res, dist(qs[i], qs[j]));
    if((qs[(i+1) % n] - qs[i]).det(qs[(j+1) % n] - qs[j]) < 0){
      i = (i+1) % n;
    } else {
      j = (j+1) % n;
    }
  }
  printf("%.0f\n", res);
}

int main(){
  N=8;
  ps[0]=P(0,5);
  ps[1]=P(1,8);
  ps[2]=P(3,4);
  ps[3]=P(5,0);
  ps[4]=P(6,2);
  ps[5]=P(6,6);
  ps[6]=P(8,3);
  ps[7]=P(8,7);
  solve();
}
  
  
  
