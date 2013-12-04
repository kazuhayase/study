// Dikstra
// shortest path with a single source without negative edge
// with adjacent matrix cost[][]

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

int cost[MAX_V][MAX_V];
int d[MAX_V];
bool used[MAX_V];
int V;

void dijkstra(int s){
  fill(d,d+V,INF);
  fill(used,used+V,false);
  d[s]=0;

  while(true){
    int v=-1;
    // find shortest vertex
    for(int u=0; u<V; u++){
      if (!used[u]&&(v == -1 || d[u] < d[v])) v=u;
    }
    if(v==-1) break;

    used[v] = true;

    for(int u=0; u<V; u++){
      d[u] = min(d[u], d[v] + cost[v][u]);
    }
  }
}

    
      
