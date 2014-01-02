#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <vector>

using namespace std;

const int MAX_N = 100000;
const int MAX_M = 5000;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

const int ST_SIZE = (1 << 18) -1;

//INPUT

int N,M;
int A[MAX_N];
int I[MAX_N], J[MAX_N], K[MAX_N];

int nums[MAX_N];
vector<int> dat[ST_SIZE];

void init(int k, int l, int r){
  if(r-l == 1){
    dat[k].push_back(A[l]);
  }
  else {
    int lch = k*2+1, rch = k*2+2;
    init(lch, l, (l+r)/2);
    init(rch, (l+r)/2, r);
    dat[k].resize(r-l);

    merge(dat[lch].begin(), dat[lch].end(), dat[rch].begin(), dat[rch].end(), dat[k].begin());
  }
}

// count number of numbers which are lower than or equal to x in [i,j)
int query(int i, int j, int x, int k, int l, int r){
  if(j <= l || r <= i){
    return 0;
  }
  else if (i <= l && r <= j){
    return upper_bound(dat[k].begin(), dat[k].end(), x) - dat[k].begin();
  }
  else {
    int lc = query(i,j,x, k*2+1, l, (l+r)/2);
    int rc = query(i,j,x, k*2+2, (l+r)/2, r);
    return lc + rc;
  }
}

void solve(){
  for(int i=0; i<N; i++) nums[i] = A[i];
  sort(nums, nums+N);

  init(0,0,N);

  for(int i=0; i<M; i++){
    int l=I[i], r=J[i]+1, k=K[i];
    int lb=-1, ub=N-1;
    while(ub - lb > 1){
      int md = (lb+ub)/2;
      int c = query(l, r, nums[md], 0, 0, N);
      if (c >= k) ub = md;
      else lb = md;
    }
    printf("%d\n", nums[ub]);
  }
}

int main(){
  solve();
  return 0;
}

