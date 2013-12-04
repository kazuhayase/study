// get path for dijkstra

#include <vector>
using namespace std;

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

int cost[MAX_V][MAX_V];
int d[MAX_V];
bool used[MAX_V];
int V;

int prv[MAX_V];

void dijkstra(int s){
  fill(d, d+V, INF);
  fill(used, used +V, false);
  fill(prv, prv+V, -1);
  d[s]=0;

  while(true){
    int v=-1;
    for(int u=0; u<V; u++){
      if(!used[u] && (v == -1 || d[u] < d[v])) v=u;
    }

    if(v == -1) break;
    
    used[v] = true;
    for(int u=0; u<V; u++){
      if(d[u]>d[v]+cost[v][u]){
	d[u]=d[v]+cost[v][u];
	prv[u]=v;
      }
    }
  }
}

vector<int> get_path(int t){
  vector<int> path;
  for(; t!=-1; t=prv[t]) path.push_back(t);
  reverse(path.begin(), path.end());
  return path;
}

