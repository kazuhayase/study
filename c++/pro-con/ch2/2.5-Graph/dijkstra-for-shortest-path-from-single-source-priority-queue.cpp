// dijkstra with priority queue (with greater <P>)
// O(|E| log |V|)

#include <vector>
#include <queue>
using namespace std;

#include <limits>
const int INF = std::numeric_limits<int>::max(); // 2,147,483,647 == 2^31 -1

const int MAX_V = 100;
const int MAX_E = 10000;

struct edge{int to, cost; };
typedef pair<int, int> P; // first = distance, second = vertex

int V;
vector<edge> G[MAX_V];
int d[MAX_V];


void dijkstra(int s) {

  priority_queue<P, vector<P>, greater<P> > que;
  fill(d, d+V, INF);
  d[s] = 0;
  que.push(P(0,s));

  while(!que.empty()){
    P p = que.top(); que.pop();
    int v = p.second;
    if (d[v] < p.first) continue; 
    for (int i=0; i<G[v].size(); i++){
      edge e = G[v][i];
      if (d[e.to] > d[v] + e.cost){
	d[e.to] = d[v] + e.cost;
	que.push(P(d[e.to], e.to));
      }
    }
  }
}
