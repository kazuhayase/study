// Prim for minimum spanning tree (like dijkstra)
// using adjacent matrix cost[][]

#include <algorithm>

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

int cost[MAX_V][MAX_V]; // cost for each edge; INF if non exist
int mincost[MAX_V];// min cost edge to X for each vertex
bool used[MAX_V]; // X; true,  V\X; false
int V;

int prim(){
  for(int i=0; i<V; i++){
    mincost[i]=INF;
    used[i]=false;
  }

  mincost[0]=0;
  int res=0;

  while(true){
    int v=-1;
    //find min cost vertex from V\X
    for(int u=0; u<V; u++){
      if(!used[u] && (v == -1 || mincost[u]<mincost[v])) v=u;
    }
    if (v==-1) break;

    used[v] = true;
    res += mincost[v];

    for (int u=0; u<V; u++){
      mincost[u] = std::min(mincost[u], cost[v][u]);
    }
  }
  return res;
}
