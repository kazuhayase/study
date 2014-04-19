#include <vector>
using namespace std;

const int MAX_V = 10000;

// simpler bipartite matching

// input
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
    if (w < 0 || (!used[w] && dfs(w)) ) {
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
