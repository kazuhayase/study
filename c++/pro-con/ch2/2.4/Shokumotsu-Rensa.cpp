#include <cstdio>
#include <algorithm>
#include <queue>

using namespace std;

const int MAX_N = 50000;
const int MAX_K = 100000;

// Union Find Tree

int par[MAX_N];
int Rank[MAX_N];

void init(int n){
  for(int i=0; i<n; i++){
    par[i]=i;
    Rank[i]=0;
  }
}

int find(int x){
  if (par[x] == x){
    return x;
  } else {
    return par[x] = find(par[x]);
  }
}
void unite(int x, int y) {
  x = find(x);
  y = find(y);

  if (x == y) return;

  if (Rank[x] < Rank[y]){
    par[x] = y;
  } else {
    par[y] = x;
    if (Rank[x] == Rank[y]) Rank[x]++;
  }
}

bool same(int x, int y){
  return find(x) == find(y);
}

int N,K;
int T[MAX_K], X[MAX_K], Y[MAX_K];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d %d\n", &N,&K);

  for(int i=0; i<K; i++){
    scanf("%d %d %d", &T[i],&X[i],&Y[i]);
  }
}

void solve(){
  init(N*3);

  int ans=0;
  for (int i=0; i < K; i++){
    int t=T[i];
    int x=X[i]-1, y=Y[i]-1;

    if(x<0||N<=x||y<0||N<=y){
      ans++;
      continue;
    }
    if(t==1){
      if(same(x,y+N) || same(x,y+2*N)){
	ans++;
      } else {
	unite(x,y);
	unite(x+N, y+N);
	unite(x+N*2, y+N*2);
      }
    } else {
      if (same(x,y) || same(x,y+2*N)) {
	ans++;
      } else {
	unite(x,y+N);
	unite(x+N,y+2*N);
	unite(x+2*N,y);
      }
    }
  }
  printf ("%d\n", ans);
}


	
      
