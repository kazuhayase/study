// Min Cost Flow 
// find shorteset path in residual graph with Dijkstra by introducing 'potential'
// O(F|E|log|V|) or O(F|V|^2)

#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;

const int MAX_V = 100;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

typedef pair<int, int> P; // first is shortest distance, second is vertex number

struct edge { int to, cap, cost, rev; };

int V;
vector<edge> G[MAX_V];
int h[MAX_V];// "potential"
int dist[MAX_V];
int prevv[MAX_V], preve[MAX_V];

// 
void init(){
  memset(G,0,sizeof(G));
  memset(h,0,sizeof(h));
  memset(dist,0,sizeof(dist));
  memset(prevv,0,sizeof(prevv));
  memset(preve,0,sizeof(preve));
}

// add an edge with cap(acity) and cost
void add_edge(int from, int to, int cap, int cost){
  G[from].push_back((edge){to, cap, cost, G[to].size()});
  G[to].push_back((edge){from, 0, -cost, G[from].size() - 1});
}

// find minimum cost flow f from s to t
// return -1 if impossible

int min_cost_flow(int s, int t, int f){
  int res = 0;
  fill(h, h +V, 0);
  while(f > 0){
    //using dijkstra to update h "potential"
    priority_queue<P, vector<P>, greater<P> > que;
    fill(dist, dist +V, INF);
    dist[s] = 0;
    que.push(P(0,s));
    while(!que.empty()){
      P p = que.top(); que.pop();
      int v = p.second;
      if (dist[v] < p.first) continue;// updated dist after this pair pushed
      for (int i=0; i < G[v].size(); i++){
	edge &e = G[v][i];
	if (e.cap > 0 && dist[e.to] > dist[v] + e.cost + h[v] - h[e.to]) {
	  dist[e.to] = dist[v] + e.cost + h[v] - h[e.to];
	  prevv[e.to] = v;
	  preve[e.to] = i;
	  que.push(P(dist[e.to], e.to));
	}
      }	   
    }

    if(dist[t] == INF) {
      return -1;
    }
    for (int v=0; v < V; v++) h[v] += dist[v];


    // flow s-t maximally 
    int d = f;
    for(int v = t; v != s; v = prevv[v]){
      d = min(d, G[prevv[v]][preve[v]].cap);
    }
    f -= d;
    res += d * h[t];
    for(int v = t; v != s; v = prevv[v]){
      edge &e = G[prevv[v]][preve[v]];
      e.cap -= d;
      G[v][e.rev].cap += d;
    }
  }
  return res;
}

//INPUT
const int MAX_N=50;
const int MAX_M=50;
int N,M;
int Z[MAX_N][MAX_M];


void solve(){
  // 0 -- N-1; toy
  // N -- 2*N-1; 0th factory
  // 2*N -- 3*N-1; 1st factory
  // M*N -- (M+1)*N-1; (M-1)th factory
  int s = N + N * M; int t = s+1;
  V = t+1;
  for(int i=0; i < N; i++){
    add_edge(s, i, 1, 0); // s to i-th toy
  }
  for (int j=0; j < M; j++){
    for (int k=0; k < N; k++){
      add_edge(N + j*N + k, t, 1, 0); // k-th time slot of j-th factory to t
      for (int i=0; i < N; i++){
	add_edge(i, N + j*N + k, 1, (k+1) * Z[i][j]);// i-th toy is built in j-th factory at k-th time slot
      }
    }
  }
  printf("%.6f\n", (double) min_cost_flow(s,t,N) / N);
}

int main(){
  //example1
  N=3, M=4;
  int Z0[3][4] = {{100,100,100,1}, {99,99,99,1}, {98,98,98,1}};
  for(int i=0; i < N; i++){
    for(int j=0; j < M; j++){
      Z[i][j]=Z0[i][j];
    }
  }
  solve();

  //example2
  init();
  N=3, M=4;
  int Z1[3][4] = {{1,100,100,100}, {99,1,99,99}, {98,98,1,98}};
  for(int i=0; i < N; i++){
    for(int j=0; j < M; j++){
      Z[i][j]=Z1[i][j];
    }
  }

  solve();

  //example3
  init();
  N=3, M=4;
  int Z2[3][4] = {{1,100,100,100}, {1,99,99,99}, {98,1,98,98}};
  for(int i=0; i < N; i++){
    for(int j=0; j < M; j++){
      Z[i][j]=Z2[i][j];
    }
  }

  solve();

  return 0;
}
