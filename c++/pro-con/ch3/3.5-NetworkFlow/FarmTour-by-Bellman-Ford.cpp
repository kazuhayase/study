// Min Cost Flow 
// find shorteset path in residual graph with Belman Ford
// O(F |V| |E|)

#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

const int MAX_V = 1000;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

struct edge { int to, cap, cost, rev; };

int V;
vector<edge> G[MAX_V];
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
  while(f > 0){
    fill(dist, dist +V, INF);
    dist[s] = 0;
    bool update = true;
    while(update){
      update = false;
      for (int v = 0; v < V; v++){
	if(dist[v] == INF) continue;
	for(int i=0; i < G[v].size(); i++){
	  edge &e = G[v][i];
	  if (e.cap > 0 && dist[e.to] > dist[v] + e.cost) {
	    dist[e.to] = dist[v] + e.cost;
	    prevv[e.to] = v;
	    preve[e.to] = i;
	    update = true;
	  }
	}
      }
    }

    if(dist[t] == INF) {
      return -1;
    }

    // flow s-t maximally 
    int d = f;
    for(int v = t; v != s; v = prevv[v]){
      d = min(d, G[prevv[v]][preve[v]].cap);
    }
    f -= d;
    res += d * dist[t];
    for(int v = t; v != s; v = prevv[v]){
      edge &e = G[prevv[v]][preve[v]];
      e.cap -= d;
      G[v][e.rev].cap += d;
    }
  }
  return res;
}


const int MAX_M = 10000;

//INPUT
int N=4, M=5;
int a[MAX_M]={1,2,3,1,2}, b[MAX_M]={2,3,4,3,4}, c[MAX_M]={1,1,1,2,2};

int main(){
  int s=0, t=N-1;
  V = N;
  for(int i=0; i<M; i++){
    add_edge(a[i]-1, b[i]-1, 1, c[i]);
    add_edge(b[i]-1, a[i]-1, 1, c[i]);
  }
  printf("%d\n", min_cost_flow(s,t,2));
  return 0;
}

