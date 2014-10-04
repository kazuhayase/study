#include <cstdio>
#include <climits>
#include <cmath>
#include <vector>
#include <algorithm>
using namespace std;

typedef pair<double, double> P; // first; x, second; y

const int MAX_N = 10000;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

//INPUT
int N;
P A[MAX_N];

// comparing function for merging by y-increasing
bool compare_y(P a, P b){
  return a.second < b.second;
}

// a is given as sorted by x increasing
double closest_pair(P *a, int n){
  if (n <= 1) return INF;
  int m = n/2;
  double x = a[m].first;
  double d = min(closest_pair(a, m), closest_pair(a+m, n-m));; //(1)
  inplace_merge(a, a+m, a+n, compare_y);// merge two sorted array. a is sorted by y

  //(2')
  vector<P> b; 
  for (int i=0; i<n ; i++){
    if (fabs(a[i].first - x) >= d) continue;

    // check vertex in b from tail to where diff in y is more than d
    for (int j=0; j<b.size(); j++){
      double dx = a[i].first - b[b.size()-j-1].first;
      double dy = a[i].second - b[b.size()-j-1].second;
      if (dy>=d) break;
      d = min (d, sqrt(dx * dx + dy * dy));
    }
    b.push_back(a[i]);
  }
  return d;
}

void solve(){
  sort(A, A+N);
  printf("%f\n", closest_pair(A,N));
}

int main(){
  N=5;

  A[0].first=0, A[0].second=2;
  A[1].first=6, A[1].second=67;
  A[2].first=43, A[2].second=71;
  A[3].first=39, A[2].second=107;
  A[4].first=189, A[2].second=140;

  solve();
}

