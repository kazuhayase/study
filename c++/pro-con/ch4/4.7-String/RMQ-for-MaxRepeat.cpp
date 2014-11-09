#include <climits>
#include <algorithm>
using namespace std;

//RMQ Range Minimum Queue
//Segment tree

const int MAX_RMQ_N = 1 << 17;

int RMQ_n, RMQ_dat[2*MAX_RMQ_N-1];

void init_rmq(int n_){
  RMQ_n=1;
  while(RMQ_n<n_) RMQ_n*=2;
  for(int i=0; i<2*RMQ_n-1; i++) RMQ_dat[i]=INT_MAX;
}

// update (0-indexed) k-th to value "a"

void update_rmq(int k, int a){
  k += RMQ_n-1;
  RMQ_dat[k]=a;
  while(k>0){
    k = (k-1)/2;
    RMQ_dat[k] = min(RMQ_dat[k*2+1], RMQ_dat[k*2+2]);
  }
}

// return minimum in [a,b)
// other parameters; k is node for [l,r)
// usage; call inter_query_rmq(a,b,0,0,RMQ_n)

int inter_query_rmq(int a, int b, int k, int l, int r){
  //[a,b) does not intersect with [l,r) -> return INT_MAX
  if (r <= a || b <= l) return INT_MAX;

  //[a,b) includes [l,r) -> return node k's value
  if (a <= l && r <= b) return RMQ_dat[k];
  else { // otherwise, return min of children
    int vl = inter_query_rmq(a, b, k*2+1, l, (l+r)/2);
    int vr = inter_query_rmq(a, b, k*2+2, (l+r)/2, r);
    return min(vl, vr);
  }
}

// called from outside
// return minimum in [a,b)
// other parameters; k is node for [l,r)
// usage; call query_rmq(a,b)
int query_rmq(int a, int b){
  return inter_query_rmq(a, b, 0, 0, RMQ_n);
}

void construct_rmq(int *lcp, int n_){
  init_rmq(n_);
  for(int i=0; i<n_; i++){
    update_rmq(i, lcp[i]);
  }
}

