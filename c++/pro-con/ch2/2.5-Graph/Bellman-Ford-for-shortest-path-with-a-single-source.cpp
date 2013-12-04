// Bellman-Ford
// shortest path with a single source

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

struct edge { int from, to, cost};
edge es[MAX_E]

int d[MAX_V]; //shortest path distance
int V,E;

void shortest_path(int s){
  for (int i=0; i<V; i++) d[i] = INF;
  d[s]=0;
  while(true){
    bool update = false;
    for(int i=0; i<E; i++){
      edge e = es[i];
      if(d[e.from] != INF && d[e.to]>d[e.from]+e.cost){
	d[e.to] = d[e.from]+e.cost;
	update = true;
      }
    }
    if (!updaet) break;
  }
}

