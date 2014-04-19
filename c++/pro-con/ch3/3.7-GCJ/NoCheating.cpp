#include <cstdio>
#include <vector>
using namespace std;

const int dx[4] = {-1, -1, 1, 1}, dy[4] = {-1, 0, -1, 0};
const int MAX_M = 80, MAX_N = 80;
const int MAX_V = 6400;

// INPUT
int M, N;
char seat[MAX_M][MAX_N + 1];

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


void solve(){
  int num = 0;
  V = M * N;
  for (int y = 0; y < M; y++){
    for (int x = 0; x < N; x++){
      if (seat[y][x] == '.') {
	num++;
	for (int k = 0; k < 4; k++){
	  int x2 = x + dx[k], y2 = y + dy[k];
	  if (0 <= x2 && x2 < N && 0 <= y2 && y2 < M && seat[y2][x2] == '.') {
	    add_edge(x * M + y, x2 * M + y2);
	  }
	}
      }
    }
  }
  printf("%d\n", num - bipartite_matching());
}

int main(){
  M=2, N=3;
  for(int y=0; y<2; y++){
    for(int x=0; x<3; x++){
      seat[y][x]='.';
    }
  }
  solve();

  memset(G, 0, sizeof(G));

  for(int y=0; y<2; y++){
    for(int x=0; x<3; x++){
      seat[y][x]='x';
    }
  }
  seat[0][1] = '.';
  solve();

  memset(G, 0, sizeof(G));

  for(int y=0; y<2; y++){
    for(int x=0; x<3; x++){
      seat[y][x]='x';
    }
  }
  seat[0][1] = '.';
  seat[1][1] = '.';
  solve();
  
}
    
