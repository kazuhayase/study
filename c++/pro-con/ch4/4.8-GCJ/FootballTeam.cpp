#include<cstdio>
#include<algorithm>

using namespace std;

const int MAX_N = 1000;
const int MAX_X = 1000;
const int MAX_Y = 30;

//INPUT
int N;
int x[MAX_N], y[MAX_N];

bool g[MAX_N][MAX_N]; // adjuscent matrix
int color[MAX_N]; // color of vertices
bool used[MAX_N][MAX_N];

//3-colorable?
//colors of v,u are fixed. investigate triangles sharing v-u edge recursively.
bool rec(int v, int u){
  used[v][u] = used[u][v] = true;
  int c = 3 - color[v] - color[u];
  for (int w=0; w < N; w++){
    if(g[v][w] && g[u][w]){
      if (color[w] < 0){
	color[w] = c;
	// investigate the two other edges of the triangle recursively.
	if (!rec(v, w) || !rec(u, w)) {
	  return false;
	}
      } else if (color[w] != c){
	// same color
	return false;
      }
    }
  }
  return true;
}

void solve(){
  //create the graph
  for(int i=0; i<N; i++){
    int v[3] = {-1, -1, -1};
    for(int j=0; j<N; j++){
      if(x[i]<x[j]){
	int k = y[j] - y[i] + 1;
	if( 0 <= k && k < 3 && (v[k] < 0 || x[j] < x[v[k]])) {
	  v[k] = j;
	}
      }
    }
    for (int k = 0; k<3; k++){
      if (v[k] >= 0){
	g[i][v[k]] = g[v[k]][i] = true;
      }
    }
  }
  // find triangles and compute number of colors
  int res = 1;

  // triple loops, but #edges is O(N), then O(N^2)
  for (int v=0; v<N; v++){
    for (int u=0; u<N; u++){
      if (g[v][u] && !used[v][u]){
	// if an edge exists, greater than or equal to 2
	res = max(res, 2);
	for (int w=0; w < N; w++){
	  if(g[v][w] && g[u][w]){
	    // if a triangle exists, greater than or equal to 3
	    res = max(res, 3);
	    memset(color, -1, sizeof(color));
	    color[v]=0;
	    color[u]=1;
	    if(!rec(v,u)) {
	      //not 3 colorble, then 4
	      printf("4\n");
	      return;
	    }
	    break;
	  }
	}
      }
    }
  }
  printf("%d\n", res);
}

int main(){
  N=3;
  x[0] = 10, x[1] = 8, x[2] = 12;
  y[0] = 10, y[1] = 15, y[2] = 7;
  solve();

  N=5;
  x[0] = 1, x[1] = 2, x[2] = 3, x[3] = 4, x[4] = 5;
  y[0] = 1, y[1] = 1, y[2] = 1, y[3] = 1, y[4] = 1;
  solve();

  N=3;
  x[0] = 1, x[1] = 2, x[2] = 3;
  y[0] = 1, y[1] = 2, y[2] = 1;
  solve();
}

