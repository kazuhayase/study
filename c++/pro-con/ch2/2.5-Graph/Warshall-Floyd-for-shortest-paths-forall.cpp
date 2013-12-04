// Warshall-Floyd for shortest paths for all pairs
// O(|V|^3)

const int MAX_V = 100;
const int MAX_E = 10000;

// d is cost for e=(u,v); if non-exist d is INF. for e=(i,i), d is 0.
int d[MAX_V][MAX_V]; 
int V;

void warshall_floyd(){

  for(int k=0; k<V; k++)
    for(int i=0; i<V; i++)
      for(int j=0; j<V; j++) d[i][j] = min(d[i][j], d[i][k] + d[k][j]);

}
