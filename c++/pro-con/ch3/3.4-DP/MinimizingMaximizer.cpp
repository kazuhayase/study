#include <climits>
#include <algorithm>
using namespace std;

const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

const int MAX_M = 500000;
const int MAX_N = 50000;

int dat[2*MAX_N -1];

//INPUT
int n,m;
int s[MAX_M], t[MAX_M];

int dp[MAX_N + 1];

void rmq_init(int n_){
  n=1;
  while(n<n_) n*=2;
  for(int i=0; i<2*n-1; i++) dat[i]=INT_MAX;
}

// update (0-indexed) k-th to value "a"

void update(int k, int a){
  k += n-1;
  dat[k]=a;
  while(k>0){
    k = (k-1)/2;
    dat[k] = min(dat[k*2+1], dat[k*2+2]);
  }
}

// return minimum in [a,b)
// other parameters; k is node for [l,r)
// usage; call query(a,b,0,0,n)

int query(int a, int b, int k, int l, int r){
  //[a,b) does not intersect with [l,r) -> return INT_MAX
  if (r <= a || b <= l) return INT_MAX;

  //[a,b) includes [l,r) -> return node k's value
  if (a <= l && r <= b) return dat[k];
  else { // otherwise, return min of children
    int vl = query(a, b, k*2+1, l, (l+r)/2);
    int vr = query(a, b, k*2+2, (l+r)/2, r);
    return min(vl, vr);
  }
}

void solve(){
  rmq_init();
  fill(dp, dp+n+1, INF);
  dp[1]=0;
  update(1,0);
  for(int i=0; i < m; i++){
    int v = min(dp[t[i]], query(s[i], t[i]+1) +1);
    dp[t[i]]=v;
    update(t[i], v);
  }
