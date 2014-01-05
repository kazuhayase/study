#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;

const int MAX_V = 1000;
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

int const MAX_N = 100;
int const MAX_F = 100;
int const MAX_D = 100;

//INPUT
int N, F, D;
bool likeF[MAX_N][MAX_F];
bool likeD[MAX_N][MAX_D];

void solve(){
  // 0 -- N-1; Cow for food
  // N -- 2N-1; Cow for drink
  // 2N -- 2N + F - 1; Food
  // 2N + F -- 2N + F + D - 1; Drink
  int s = N * 2 + F + D, t = s+1;

  // connect s -> Food
  for (int i=0; i < F; i++) {
    add_edge(s, N * 2 + i, 1);
  }

  // connect Drink -> t
  for (int i=0; i < D; i++) {
    add_edge(N * 2 + F + i, t, 1);
  }

  // Cow & F + D
  for (int i=0; i < N; i++) {

    // connect cows
    add_edge(i, N + i, 1);

    // connect with Food
    for (int j=0; j<F; j++){
      if (likeF[i][j]) add_edge(N * 2 + j, i, 1);
    }

    // connect with Drink
    for (int j=0; j<D; j++){
      if (likeD[i][j]) add_edge(N + i, N * 2 + F + j, 1);
    }
  }

  printf("%d\n", max_flow(s,t));
}

