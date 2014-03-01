#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
using namespace std;

const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

const int MAX_N = 100;
const int MAX_M = 100;
const int MAX_V = MAX_N + MAX_M +1;

// INPUT
int N=3,M=4;
int X[MAX_N]={-3,-2,2}, Y[MAX_N]={3,-2,2}, B[MAX_N]={5,6,5};
int p[MAX_M]={-1,1,-2,0}, Q[MAX_M]={1,1,-2,-1}, C[MAX_M]={3,4,7,3};
int E[MAX_N][MAX_M]={{3,1,1,0},{0,0,6,0},{0,3,0,2}};

int g[MAX_V][MAX_V]; //distance matrix
int prev[MAX_V][MAX_V]; //shortest path's previous vertex
bool used[MAX_V]; //loop flag

void solve(){
  int V = N + M + 1;
  //distance matrix
  for(int i=0; i < V; i++){
    fill(g[i], g[i]+V, INF);
  }
  for (int j=0; j < M; j++){
    int sum = 0;
    for (int i=0; i<N; i++){
      int c = abs(X[i] - p[j]) + abs(Y[i] - Q[j]) + 1;
      g[i][N+j] = c;
      if (E[i][j] > 0) g[N+j][i] = -c;
      sum += E[i][j];
    }
    if (sum > 0){
      g[N+M][N+j]=0;
    }
    if (sum < C[j]) {
      g[N+j][N+M] = 0;
    }
  }

  //warshall floyd to find negative loop
  for (int i=0; i < V; i++){
    for (int j=0; j < V; j++){
      prev[i][j] = i;
    }
  }
  for (int k=0; k < V; k++){
    for (int i=0; i<V; i++){
      for (int j=0; j<V; j++){
	if(g[i][j] > g[i][k] + g[k][j]){
	  g[i][j] = g[i][k] + g[k][j];
	  prev[i][j] = prev[k][j];
	  if (i == j && g[i][i] < 0){
	    fill(used, used + V, false);
	    // negative loop found
	    for (int v = i; !used[v]; v = prev[i][v]){
	      used[v] = true;
	      if (v != N+M && prev[i][v] != N+M){
		if (v >= N){
		  E[prev[i][v]][v - N]++;
		}else{
		  E[v][prev[i][v] - N]--;
		}
	      }
	    }
	    printf("SUBOPTIMAL\n");
	    for(int x=0; x<N; x++){
	      for(int y=0; y<M; y++){
		printf("%d%c", E[x][y], y+1 == M ? '\n' : ' ');
	      }
	    }
	    return;
	  }
	}
      }
    }
  }
  printf("OPTIMAL\n");
}
  
