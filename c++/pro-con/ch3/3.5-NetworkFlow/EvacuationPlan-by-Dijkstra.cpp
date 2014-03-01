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

const int MAX_V = 300;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

typedef pair<int, int> P; // first is shortest distance, second is vertex number

struct edge { int to, cap, cost, rev; };

int V;
vector<edge> G[MAX_V];
int h[MAX_V];// "potential"
int dist[MAX_V];
int prevv[MAX_V], preve[MAX_V];

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

const int MAX_N = 100;
const int MAX_M = 100;


//INPUT
int N=3,M=4;
int X[MAX_N]={-3,-2,2}, Y[MAX_N]={3,-2,2}, B[MAX_N]={5,6,5};
int p[MAX_M]={-1,1,-2,0}, Q[MAX_M]={1,1,-2,-1}, C[MAX_M]={3,4,7,3};
int E[MAX_N][MAX_M]={{3,1,1,0},{0,0,6,0},{0,3,0,2}};

//void solve(){
int main(){
  // matching graph
  // 0 -- N-1; Building
  // N -- N+M-1; shelter
  int s = N+M, t = s+1;
  V = t+1;
  int cost = 0; // sum of the plan E
  int F = 0; //number of people
  for (int i=0; i < N; i++){
    for (int j=0; j < M; j++){
      int c = abs(X[i] - p[j]) + abs(Y[i] - Q[j]) + 1;
      add_edge(i, N+j, INF, c);
      cost += E[i][j] * c;
    }
  }
  for (int i=0; i < N; i++){
    add_edge(s, i, B[i], 0);
    F += B[i];
  }
  for (int i=0; i < M; i++){
    add_edge(N+i, t, C[i], 0);
  }
  
  if (min_cost_flow(s, t, F) < cost){
    printf("SUBOPTIMAL\n");
    for (int i=0; i < N; i++) {
      for (int j=0; j < M; j++){
	printf("%d%c", G[N+j][i].cap, j+1 == M ? '\n' : ' '); // rev path cap in residual graph == size of the path's flow
      }
    }
  } else {
    printf("OPTIMAL\n");
  }
}
