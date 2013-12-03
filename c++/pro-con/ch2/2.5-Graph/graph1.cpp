#include <vector>
using namespace std;

const int MAX_V = 100;

vector<int> G[MAX_V];

// if edge has attribute (cost)
// struct edge {int to, cost; };
// vector<edge> G[MAX_V];

int main (){
  int V, E;
  scanf("%d %d", &V, &E);
  for (int i=0; i < E; i++){
    int s,t;
    scanf("%d %d", &s, &t);
    G[s].push_back(t);
    // G[t].push_back(s);
  }
  return 0;
}
