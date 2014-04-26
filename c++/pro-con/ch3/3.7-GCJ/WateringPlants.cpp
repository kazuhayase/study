#include <cstdio>
#include <cmath>
#include <vector>
using namespace std;

typedef long long ll;
const int MAX_N = 40;

//INPUT
int N; 
int X[MAX_N], Y[MAX_N], R[MAX_N];

// the set of circles which are covered by a circle centered (x,y) and radius r
ll cover(double x, double y, double r){
  ll S=0;
  for(int i=0; i<N; i++){
    if(R[i] <= r){
      double dx = x - X[i], dy = y - Y[i], dr = r - R[i];
      if (dx * dx + dy * dy <= dr * dr){
	S |= 1LL << i;
      }
    }
  }
  return S;
}

// decide if two circles of radius r can cover all.
bool C(double r){
  vector<ll> cand; // list of the set of circles by a circle
  cand.push_back(0);

  // pattern a; two circles come in contact with the surrounding circle
  for (int i=0; i<N; i++){
    for (int j=0; j<i; j++){
      if (R[i] < r && R[j] < r){
	// the intersection of the two circles (R-r1, R-r2)
	double x1 = X[i], y1 = Y[i], r1 = r - R[i];
	double x2 = X[j], y2 = Y[j], r2 = r - R[j];
	double dx = x2-x1, dy = y2-y1;
	double a = dx*dx + dy*dy;
	double b = ((r1*r1 - r2*r2) / a + 1) / 2;
	double d = r1*r1 / a - b*b;
	if (d >= 0){
	  d = sqrt(d);
	  double x3 = x1 + dx * b;
	  double y3 = y1 + dy * b;
	  double x4 = -dy * d;
	  double y4 = dx * d;
	  // consider error range
	  ll ij = 1LL << i | 1LL << j;
	  cand.push_back(cover(x3 - x4, y3 - y4, r) | ij);
	  cand.push_back(cover(x3 + x4, y3 + y4, r) | ij);
	}
      }
    }
  }

  // pattern b; center is same with another circle
  for (int i=0; i < N; i++){
    if(R[i] <= r){
      cand.push_back(cover(X[i], Y[i], r) | 1LL<<i);
    }
  }

  // select two circles and verify if they cover all
  for(int i=0; i < cand.size(); i++){
    for(int j=0; j<i; j++){
      if ((cand[i] | cand[j]) == (1LL<<N) - 1){
	return true;
      }
    }
  }
  return false;
}

void solve(){
  // binary search on radius r
  double lb=0, ub=10000;
  for(int i=0; i < 100; i++){
    double mid = (lb+ub)/2;
    if( C(mid) ) ub = mid;
    else lb = mid;
  }
  printf("%.6f\n", ub);
}

int main(){
  N=3;
  X[0] = 20, Y[0] = 10, R[0] = 2;
  X[1] = 20, Y[1] = 20, R[1] = 2;
  X[2] = 40, Y[2] = 10, R[2] = 2;
  solve();

  N=3;
  X[0] = 20, Y[0] = 10, R[0] = 3;
  X[1] = 30, Y[1] = 10, R[1] = 3;
  X[2] = 40, Y[2] = 10, R[2] = 3;
  solve();

}
