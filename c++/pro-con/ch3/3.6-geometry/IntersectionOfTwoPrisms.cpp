#include <cstdio>
#include <climits>
#include <vector>

using namespace std;

const int MAX_M = 100;
const int MAX_N = 100;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

//INPUT
int M,N;
int X1[MAX_M], Y1[MAX_M];
int X2[MAX_N], Z2[MAX_N];

// slice by x
double width(int* X, int* Y, int n, double x){
  double lb = INF, ub = -INF;
  for (int i=0; i<n; i++){
    double x1 = X[i], y1 = Y[i], x2 = X[(i+1) % n], y2 = Y[(i+1) % n];
    // intersects with edge i?
    if ( (x1-x) * (x2 -x) <= 0 && x1 != x2){
      // intersecting point
      double y = y1 + (y2 - y1) * (x - x1) / (x2 - x1);
      lb = min (lb, y);
      ub = max (ub, y);
    }
  }
  return max(0.0, ub - lb);
}

void solve(){
  // enumerate vertices of segments
  int min1 = *min_element(X1, X1+M), max1 = *max_element(X1, X1+M);
  int min2 = *min_element(X2, X2+N), max2 = *max_element(X2, X2+N);
  vector<int> xs;
  for(int i=0; i<M; i++) xs.push_back(X1[i]);
  for(int i=0; i<N; i++) xs.push_back(X2[i]);
  sort(xs.begin(), xs.end());

  double res = 0;
  for (int i=0; i+1 < xs.size(); i++){
    double a = xs[i], b = xs[i+1], c = (a+b)/2;
    if (min1 <= c && c <= max1 && min2 <= c && c<= max2) {
      // Simpson
      double fa = width(X1, Y1, M, a) * width(X2, Z2, N, a);
      double fb = width(X1, Y1, M, b) * width(X2, Z2, N, b);
      double fc = width(X1, Y1, M, c) * width(X2, Z2, N, c);
      res += (b-a) / 6 * (fa + 4 * fc + fb);
    }
  }
  printf("%.10f\n", res);
}

int main(){
  //INPUT
  M=4,N=3;

  X1[0] = 7, Y1[0] = 2;
  X1[1] = 3, Y1[1] = 3;
  X1[2] = 0, Y1[2] = 2;
  X1[3] = 3, Y1[3] = 1;

  X2[0] = 4, Z2[0] = 2;
  X2[1] = 0, Z2[1] = 1;
  X2[2] = 8, Z2[2] = 1;

  solve();
}

