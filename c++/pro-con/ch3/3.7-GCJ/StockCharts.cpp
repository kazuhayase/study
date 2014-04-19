#include <cstdio>
#include <vector>
using namespace std;

const int MAX_N = 100;
const int MAX_K = 25;
const int MAX_V = 200;

// INPUT
int N, K, P[MAX_N][MAX_K];

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

void solve(){
  V = N*2;
  for (int i=0; i < V; i++) G[i].clear();

  for (int i=0; i < N; i++){
    for (int j=0; j < N; j++){
      if (i==j) continue;
      bool f = true;
      for (int k=0; k < K; k++){
	if (P[j][k] >= P[i][k]) f = false;
      }
      if (f) add_edge(i, N+j);
    }
  }
  int ans = N - bipartite_matching();
  printf("%d\n", ans);
}

int main(){
  N=5, K=2;
  P[0][0]=1, P[0][1]=1;
  P[1][0]=2, P[1][1]=2;
  P[2][0]=5, P[2][1]=4;
  P[3][0]=4, P[3][1]=4;
  P[4][0]=4, P[4][1]=1;
  solve();
}


