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

const int MAX_V = 100;
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

const int MAX_N=200;

//INPUT

int N,K;
int a[MAX_N], b[MAX_N], w[MAX_N];

void solve(){
  // vertex set
  vector<int> x;
  for(int i=0; i<N; i++){
    x.push_back(a[i]);
    x.push_back(b[i]);
  }
  sort(x.begin(), x.end());
  x.erase(unique(x.begin(), x.end()), x.end());

  //graph
  int m=x.size();
  int s=m, t=s+1;
  V = t+1;
  int res=0;
  add_edge(s, 0, K, 0);
  add_edge(m-1, t, K, 0);
  for(int i=0; i+1 < m; i++){
    add_edge(i, i+1, INF, 0);
  }
  for(int i=0; i < N; i++){
    int u = find(x.begin(), x.end(), a[i]) - x.begin();
    int v = find(x.begin(), x.end(), b[i]) - x.begin();
    // u->v, capacity=1, cost=-w[i]
    add_edge(v,u,1,w[i]);
    add_edge(s,v,1,0);
    add_edge(u,t,1,0);
    res -= w[i];
  }
  res += min_cost_flow(s,t,K+N);
  printf("%d\n", -res);
}


int main(){
  N = 3, K=1;

  int a1[3] = {1,2,3}; 
  int b1[3] = {2,3,4};
  int w1[3] = {2,4,8};

  for(int i=0; i < N; i++){
      a[i]=a1[i];
      b[i]=b1[i];
      w[i]=w1[i];
    }

  solve();

  return 0;
}
