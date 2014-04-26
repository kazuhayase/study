#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;

//MaxFlow by Dinic

const int MAX_N = 500;
const int MAX_V = 500;
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

//INPUT
int n, x[MAX_N], y[MAX_N], r[MAX_N], s[MAX_N];
int sqr(int x){
  return x*x;
}

void solve(){
  //n; source, n+1; sink. Network of n+2 nodes
  for(int v=0; v < n+2; v++){
    G[v].clear();
  }

  int ans = 0;
  for (int i=0; i < n; i++){
    if (s[i] < 0){
      add_edge(n, i, -s[i]);
    } else {
      ans += s[i];
      add_edge(i, n+1, s[i]);
    }
    for (int j = 0; j < n; j++){
      if (i == j) continue;
      if (sqr(x[i] - x[j]) + sqr(y[i] - y[j]) <= sqr(r[i])) {
	add_edge(j, i, INF);
	// add_edge(i, j, INF);
      }
    }
  }

  ans -= max_flow(n, n+1);
  printf("%d\n", ans);
}

int main(){
  n = 5;
  x[0] = 0, y[0] = 1, r[0] = 7, s[0] = 10;
  x[1] = 0, y[1] = -1, r[1] = 7, s[1] = 10;
  x[2] = 5, y[2] = 1, r[2] = 1, s[2] = -15;
  x[3] = 10, y[3] = 6, r[3] = 6, s[3] = 10;
  x[4] = 15, y[4] = 2, r[4] = 2, s[4] = -20;
  solve();

}

