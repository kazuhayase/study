#include<cstdio>
#include<vector>
#include <climits>
#include <algorithm>
using namespace std;

const int MAX_V = 1000000;
const int MAX_LOG_V = 20;

//RMQ Range Minimum Queue
//Segment tree

const int MAX_N = 1 << 17;
int n, dat[2*MAX_N-1], idx[2*MAX_N-1];

// update (0-indexed) k-th to value "a"

void update(int k, int a){
  dat[k+n-1]=a;
  idx[k+n-1]=k;
  k += n-1;
  while(k>0){
    k = (k-1)/2;
    if(dat[k*2+1]<=dat[k*2+2]){
      dat[k] = dat[k*2+1];
      idx[k] = idx[k*2+1];
    } else {
      dat[k] = dat[k*2+2];
      idx[k] = idx[k*2+2];
    }
  }
}

void rmq_init(int array[], int n_){
  n = (n_ +1) / 2;
  for(int i=0; i<n_; i++) dat[i]=INT_MAX;
  for(int i=0; i<n_; i++) idx[i]=-1;
  for(int i=0; i<n; i++) update(i, array[i]);
}

// return idx of minimum in [a,b)
// other parameters; k is node for [l,r)
// usage; call query(a,b,0,0,n)

int query(int a, int b, int k, int l, int r){
  //[a,b) does not intersect with [l,r) -> return INT_MAX
  if (r <= a || b <= l) return INT_MAX;

  //[a,b) includes [l,r) -> return node number 'k'
  if (a <= l && r <= b) return idx[k];
  else { // otherwise, return min of children
    int vl = query(a, b, k*2+1, l, (l+r)/2);
    int vr = query(a, b, k*2+2, (l+r)/2, r);
    if(dat[vl+n-1]<=dat[vr+n-1]){
      return vl;
    } else {
      return vr;
    }      
  }
}

//INPUT
vector<int> G[MAX_V];
int root;

int vs[MAX_V*2 - 1]; //DFS order
int depth[MAX_V*2 - 1];
int id[MAX_V];

void dfs(int v, int p, int d, int &k){
  id[v] = k;
  vs[k] = v;
  depth[k++]=d;
  for(int i=0; i< G[v].size(); i++){
    if (G[v][i] != p) {
      dfs(G[v][i], v, d+1, k);
      vs[k] = v;
      depth[k++]=d;
    }
  }
}

void init(int V){
  //init vs, depth, id
  int k=0;
  dfs(root, -1, 0, k);
  //init RMQ
  rmq_init(depth, V*2-1);
}

int lca(int u, int v){
  return vs[query(min(id[u], id[v]), max(id[u], id[v])+1, 0, 0, n-1)];
}

