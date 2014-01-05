#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

const int MAX_V = 100;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

struct edge { int to, cap, rev; };
vector<edge> G[MAX_V];
bool used[MAX_V];

// add an edge with cap(acity) 
void add_edge(int from, int to, int cap){
  G[from].push_back((edge){to, cap, G[to].size()});
  G[to].push_back((edge){from, 0, G[from].size() - 1});
}

//find increasing path by DFS and return its flow size
int dfs(int v, int t, int f){
  if(v == t) return f;
  used[v] = true;
  for (int i=0; i < G[v].size(); i++){
    edge &e = G[v][i];
    if (!used[e.to] && e.cap > 0) {
      int d = dfs(e.to, t, min(f, e.cap));
      if(d > 0){
	e.cap -= d;
	G[e.to][e.rev].cap += d;
	return d;
      }
    }
  }
  return 0;
}

int max_flow(int s, int t){
  int flow = 0;
  for(;;){
    memset(used, 0, sizeof(used));
    int f = dfs(s, t, INF);
    if (f == 0) return flow;
    flow += f;
  }
}

/// bipartite matching 

const int MAX_N = 100;
const int MAX_K = 100;

/// INPUT
int N,K;
bool can[MAX_N][MAX_K]; //can[i][j] := computer i can process j

void solve(){
  // 0 -- N-1; computers
  // N -- N+K-1; jobs
  int s = N+K, t = s+1;

  // s to computers
  for(int i=0; i<N; i++){
    add_edge(s, i, 1);
  }

  // jobs to t
  for(int i=0; i<K; i++){
    add_edge(N+i, t, 1);
  }

  // computers to jobs
  for(int i=0; i<N; i++){
    for(int j=0; j<K; j++){
      if(can[i][j]){
	add_edge(i, N+j, 1);
      }
    }
  }
  printf("%d\n", max_flow(s, t));
}

