// Bellman-Ford
// shortest path with a single source
// find negative loop by initializing d[i]=0 for all.

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

struct edge { int from, to, cost};
edge es[MAX_E]

int d[MAX_V]; //shortest path distance
int V,E;

bool find_negative_loop(){
  memset(d, 0, sizeof(d));

  for(int i=0; i<V; i++){
    for(int j=0; j<E; j++){
      edge e = es[j];
      if(d[e.to]>d[e.from]+e.cost){
	d[e.to] = d[e.from]+e.cost;
	if (i == V-1) return true;
      }
    }
  }
  return false;
}
