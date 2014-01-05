#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;

const int MAX_V = 20002;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

struct edge { int to, cap, rev; };
vector<edge> G[MAX_V];
int level[MAX_V]; // distance from s
int iter[MAX_V]; // investigation status

// add an edge with cap(acity) 
void add_edge(int from, int to, int cap){
  G[from].push_back((edge){to, cap, G[to].size()});
  G[to].push_back((edge){from, 0, G[from].size() - 1});
}

//calc shortest distance by BFS
void bfs(int s){
  memset(level, -1, sizeof(level));
  queue<int> que;
  level[s]=0;
  que.push(s);
  while(!que.empty()){
    int v = que.front(); que.pop();
    for(int i=0; i < G[v].size(); i++){
      edge &e = G[v][i];
      if (e.cap > 0 && level[e.to] < 0){
	level[e.to] = level[v]+1;
	que.push(e.to);
      }
    }
  }
}

//find increasing path by DFS and return its flow size
int dfs(int v, int t, int f){
  if(v == t) return f;
  for (int &i = iter[v]; i < G[v].size(); i++){
    edge &e = G[v][i];
    if (e.cap > 0 && level[v] < level[e.to]){
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
    bfs(s);
    if(level[t] < 0) return flow;
    memset(iter, 0, sizeof(iter));
    int f;
    while( (f = dfs(s, t, INF)) > 0){
      flow += f;
    }
  }
}

const int MAX_N = 20000;
const int MAX_M = 200000;

//INPUT
int N, M;
int A[MAX_N], B[MAX_N];
int a[MAX_M], b[MAX_M], w[MAX_M];

void solve(){
  int s = N, t = s+1;

  for (int i=0; i < N; i++){
    add_edge(i, t, A[i]);
    add_edge(s, i, B[i]);
  }

  for (int i=0; i < M; i++){
    add_edge(a[i]-1, b[i]-1, w[i]);
    add_edge(b[i]-1, a[i]-1, w[i]);
  }

  printf("%d\n", max_flow(s,t));
}


