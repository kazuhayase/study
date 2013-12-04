//graph2
// adjacent list
//  vector of pointers to adjacent vertexes for each vertex

#include <vector>
using namespace std;

const int MAX_V = 100;

struct vertex {
  vector<vertex*> edge;
  // if vertex has attribute (cost)
  //int cost;
};

vertex G[MAX_V];

int main (){
  int V, E;
  scanf("%d %d", &V, &E);
  for (int i=0; i < E; i++){
    int s,t;
    scanf("%d %d", &s, &t);
    G[s].edge.push_back(&G[t]);
    // G[t].edge.push_back(&G[s]);
  }
  return 0;
}
