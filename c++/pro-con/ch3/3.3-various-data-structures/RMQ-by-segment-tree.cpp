#include <climits>
#include <algorithm>
using namespace std;

//RMQ Range Minimum Queue
//Segment tree

const int MAX_N = 1 << 17;
int n, dat[2*MAX_N-1];

void init(int n_){
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

    


