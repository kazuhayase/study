#include<cstdio>
#include<vector>
using namespace std;

const int MAX_V = 1000000;
const int MAX_LOG_V = 20;

//INPUT
vector<int> G[MAX_V];
int root;

int parent[MAX_LOG_V][MAX_V];
int depth[MAX_V];

void dfs(int v, int p, int d){
  parent[0][v] = p;
  depth[v] = d;
  for (int i=0; i < G[v].size(); i++){
    if (G[v][i] != p) dfs(G[v][i], v, d+1);
  }
}

void init(int V){
  //init parent[0], depth[] 
  dfs(root, -1, 0);
  //init parent
  for(int k=0; k+1 < MAX_LOG_V; k++){
    for(int v=0; v<V; v++){
      if (parent[k][v]<0) parent[k+1][v]=-1;
      else parent[k+1][v]=parent[k][parent[k][v]];
    }
  }
}

int lca(int u, int v){
  if(depth[u] > depth[v]) swap(u,v);
  for(int k=0; k<MAX_LOG_V; k++){
    if((depth[v] - depth[u]) >> k & 1) {
      v = parent[k][v];
    }
  }
  if(u==v) return u;
  // bin search
  for(int k=MAX_LOG_V - 1; k >= 0; k--){
    if (parent[k][u] != parent[k][v]){
    u=parent[k][u];
    v=parent[k][v];
    }
  }
  return parent[0][u];
}
