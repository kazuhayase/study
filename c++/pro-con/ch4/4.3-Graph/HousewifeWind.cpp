#include<cstdio>
#include<vector>
#include <climits>
#include <algorithm>
using namespace std;

const int MAX_V = 10000;
const int MAX_Q = 10000;

////////////
//RMQ Range Minimum Queue
//Segment tree

//const int MAX_N = 1 << 17;
const int MAX_N = MAX_V*2;
int rmq_n, dat[2*MAX_N-1], idx[2*MAX_N-1];

// update (0-indexed) k-th to value "a"

void update(int k, int a){
  dat[k+rmq_n-1]=a;
  idx[k+rmq_n-1]=k;
  k += rmq_n-1;
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
  rmq_n = (n_ +1) / 2;
  for(int i=0; i<n_; i++) dat[i]=INT_MAX;
  for(int i=0; i<n_; i++) idx[i]=-1;
  for(int i=0; i<rmq_n; i++) update(i, array[i]);
}

// return idx of minimum in [a,b)
// other parameters; k is node for [l,r)
// usage; call query(a,b,0,0,n)

int query(int a, int b, int k, int l, int r){
  //[a,b) does not intersect with [l,r) -> return INT_MAX
  if (r <= a || b <= l) return 0;

  //[a,b) includes [l,r) -> return node number 'k'
  if (a <= l && r <= b) return idx[k];
  else { // otherwise, return min of children
    int vl = query(a, b, k*2+1, l, (l+r)/2);
    int vr = query(a, b, k*2+2, (l+r)/2, r);
    if(dat[vl+rmq_n-1]<=dat[vr+rmq_n-1]){
      return vl;
    } else {
      return vr;
    }      
  }
}

////////////
//BIT Binary Indexed Tree
//  1-indexed array 
// sum(i) := a1 + a2 + ... + ai
// add(i,x) : ai += x

// last 1bit of i == i & -i
// i - last 1bit == i - (i&-i) = i & (i-1)

//[1,n]

int bit[MAX_N * 2 + 1], bit_n;

int sum(int i){
  int s = 0;
  while(i > 0){ 
    s += bit[i];
    i -= i & -i;
  }
  return s;
}

void add(int i, int x){
  while(i <= bit_n){
    bit[i] += x;
    i += i & -i;
  }
}

////////////

struct edge {int id, to, cost; };

int n,q,s;
int a[MAX_V-1], b[MAX_V-1], w[MAX_V-1];
int type[MAX_Q]; //0; type=A, 1; type=B
int x[MAX_Q], t[MAX_Q];

vector<edge> G[MAX_V]; // graph by adjacent list
int root;

int vs[MAX_V * 2 - 1]; //DFS order
int depth[MAX_V * 2 - 1]; //depth from root
int id[MAX_V]; //the 1st index for each vertex in es
int es[(MAX_V - 1) *2]; // index of edge (i*2 +{to leaf; 0 \ to root; 1}) 

void dfs(int v, int p, int d, int &k){
  id[v] = k;
  vs[k] = v;
  depth[k++] = d;
  for (int i=0; i < G[v].size(); i++){
    edge &e = G[v][i];
    if (e.to != p){
      add(k, e.cost);
      es[e.id *2] = k;
      dfs(e.to, v, d+1, k);
      vs[k] = v;
      depth[k++] = d;
      add(k, -e.cost);
      es[e.id*2 + 1] = k;
    }
  }
}
/* ???
  int stack_v[MAX_V + 10];
  int stack_i[MAX_V + 10];
*/

//initialization
void init(int V){
  //init. BIT 
  bit_n = (V-1) *2;
  //init. vs,dpth,id,es
  int k=0;
  dfs(root, -1, 0, k);
  //init RMQ(return not minimum value but its index)
  rmq_init(depth, V*2-1); 
}

//LCA of u&v
int lca(int u, int v){
  return vs[query(min(id[u], id[v]), max(id[u], id[v]) +1, 0, 0, rmq_n)];
}

void solve(){
  //init.
  root = n/2; // we can define root as any vertex
  for(int i=0; i<n-1; i++){
    G[a[i]-1].push_back( (edge){i, b[i]-1, w[i]});
    G[b[i]-1].push_back( (edge){i, a[i]-1, w[i]});
  }
  init(n);
  //process queries
  int v=s-1; //current position
  for(int i=0; i<q; i++){
    if(type[i]==0){
      //move to x[i]
      int u = x[i]-1;
      int p = lca(v,u);
      // cost(p->v) + cost(p->u). using BIT to calculate 
      //  (id[p], id[v]] & (id[p], id[u]]
      printf("%d\n", sum(id[v]) + sum(id[u]) - sum(id[p]) *2);
      v = u;
    } else {
      // change cost of x[i] to t[i]
      int k=x[i] -1;
      add(es[k*2], t[i] - w[k]);
      add(es[k*2+1], w[k] - t[i]);
      w[k] = t[i];
    }
  }
}
      
int main(){
  n=3, q=3, s=1;
  a[0]=1, b[0]=2, w[0]=1;
  a[1]=2, b[1]=3, w[1]=2;
  type[0]=0, x[0]=2, t[0]=0;
  type[1]=1, x[1]=2, t[1]=3;
  type[2]=0, x[2]=3, t[2]=0;

  solve();
}





