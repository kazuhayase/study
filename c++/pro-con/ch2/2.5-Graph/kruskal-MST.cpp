// Kruskal for minimum spanning tree (adding mincost edges)
// using UnionFind to decide if the new vertex is in same connected component

#include <algorithm>
#include <queue>

using namespace std;

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

struct edge {int u, v, cost;};
bool comp(const edge& e1, const edge& e2){
  return e1.cost < e2.cost;
}

edge es[MAX_E];
int V,E;

// From Union Find Tree (a bit edited)

int par[MAX_V];
int Rank[MAX_V];

void init_union_find(int n){
  for(int i=0; i<n; i++){
    par[i]=i;
    Rank[i]=0;
  }
}

int find(int x){
  if (par[x] == x){
    return x;
  } else {
    return par[x] = find(par[x]);
  }
}
void unite(int x, int y) {
  x = find(x);
  y = find(y);

  if (x == y) return;

  if (Rank[x] < Rank[y]){
    par[x] = y;
  } else {
    par[y] = x;
    if (Rank[x] == Rank[y]) Rank[x]++;
  }
}

bool same(int x, int y){
  return find(x) == find(y);
}
int kruskal(){
  sort (es, es+E, comp); //sort from min to max
  init_union_find(V);
  int res=0;

  for(int i=0; i<E; i++){
    edge e = es[i];
    if(!same(e.u, e.v)){
      unite(e.u, e.v);
      res += e.cost;
    }
  }
  return res;
}
