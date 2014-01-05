// Asteroids using "simpler bipartite matching"

#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

const int MAX_V = 100;
const int MAX_K = 100;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

//for simpler bipartite matching
int V;
vector<int> G[MAX_V];
int match[MAX_V]; //pair in matching
bool used[MAX_V]; //flag for DFS

// add an edge with cap(acity) 
void add_edge(int u, int v) {
  G[u].push_back(v);
  G[v].push_back(u);
}

//find increasing path by DFS
bool dfs(int v) {
  used[v] = true;
  for (int i=0; i < G[v].size(); i++){
    int u = G[v][i], w = match[u];
    if (w < 0 || !used[w] && dfs(w)) {
      match[v]=u;
      match[u]=v;
      return true;
    }
  }
  return false;
}

int bipartite_matching(){
  int res=0;
  memset(match, -1, sizeof(match));
  for(int v=0; v<V; v++){
    if(match[v] < 0){
      memset(used, 0, sizeof(used));
      if (dfs(v)){
	res++;
      }
    }
  }
  return res;
}

//INPUT
int N, K;
int R[MAX_K], C[MAX_K];

void solve(){
  V = N*2;
  for (int i=0; i<K; i++){
    add_edge(R[i] - 1, N + C[i] - 1);
  }
  printf("%d\n", bipartite_matching());
}

