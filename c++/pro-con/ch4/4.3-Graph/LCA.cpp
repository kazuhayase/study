#include<cstdio>
#include<vector>
using namespace std;

const int MAX_V = 1000000;

//INPUT
vector<int> G[MAX_V];
int root;

int parent[MAX_V];
int depth[MAX_V];

void dfs(int v, int p, int d){
  parent[v] = p;
  depth[v] = d;
  for (int i=0; i < G[v].size(); i++){
    if (G[v][i] != p) dfs(G[v][i], v, d+1);
  }
}

void init(){
  //init parent[], depth[] 
  dfs(root, -1, 0);
}

int lca(int u, int v){
  while(depth[u] > depth[v]) u = parent[u];
  while(depth[v] > depth[u]) v = parent[v];

  while(u!=v){
    u=parent[u];
    v=parent[v];
  }
  return u;
}


